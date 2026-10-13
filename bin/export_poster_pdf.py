#!/usr/bin/env python3
"""Create a lossless, single-page PDF from an RGB/RGBA PNG poster."""

from __future__ import annotations

import argparse
import struct
import zlib
from pathlib import Path


def paeth(left: int, above: int, upper_left: int) -> int:
    estimate = left + above - upper_left
    distances = (abs(estimate - left), abs(estimate - above), abs(estimate - upper_left))
    return (left, above, upper_left)[distances.index(min(distances))]


def decode_png(path: Path) -> tuple[int, int, bytes, bytes | None]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"{path} is not a PNG file")

    offset = 8
    width = height = bit_depth = color_type = None
    compressed = bytearray()
    while offset < len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk = data[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(">IIBBBBB", chunk)
            if compression != 0 or filtering != 0 or interlace != 0:
                raise ValueError("Only non-interlaced PNG files are supported")
        elif chunk_type == b"IDAT":
            compressed.extend(chunk)
        elif chunk_type == b"IEND":
            break

    if bit_depth != 8 or color_type not in (2, 6):
        raise ValueError("Only 8-bit RGB and RGBA PNG files are supported")
    channels = 3 if color_type == 2 else 4
    row_bytes = width * channels
    packed = zlib.decompress(compressed)
    rows: list[bytes] = []
    previous = bytearray(row_bytes)
    cursor = 0
    for _ in range(height):
        filter_type = packed[cursor]
        cursor += 1
        source = packed[cursor : cursor + row_bytes]
        cursor += row_bytes
        row = bytearray(row_bytes)
        for index, value in enumerate(source):
            left = row[index - channels] if index >= channels else 0
            above = previous[index]
            upper_left = previous[index - channels] if index >= channels else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = above
            elif filter_type == 3:
                predictor = (left + above) // 2
            elif filter_type == 4:
                predictor = paeth(left, above, upper_left)
            else:
                raise ValueError(f"Unsupported PNG filter type {filter_type}")
            row[index] = (value + predictor) & 0xFF
        rows.append(bytes(row))
        previous = row

    if channels == 3:
        return width, height, b"".join(rows), None

    rgb = bytearray(width * height * 3)
    alpha = bytearray(width * height)
    rgb_cursor = alpha_cursor = 0
    for row in rows:
        for index in range(0, len(row), 4):
            rgb[rgb_cursor : rgb_cursor + 3] = row[index : index + 3]
            alpha[alpha_cursor] = row[index + 3]
            rgb_cursor += 3
            alpha_cursor += 1
    mask = None if all(value == 255 for value in alpha) else bytes(alpha)
    return width, height, bytes(rgb), mask


def pdf_bytes(width: int, height: int, rgb: bytes, alpha: bytes | None, page_width: float, page_height: float) -> bytes:
    rgb_stream = zlib.compress(rgb, level=9)
    image_extra = f" /SMask 6 0 R" if alpha is not None else ""
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width:g} {page_height:g}] "
            "/Resources << /XObject << /Im0 4 0 R >> >> /Contents 5 0 R >>"
        ).encode("ascii"),
        (
            f"<< /Type /XObject /Subtype /Image /Width {width} /Height {height} "
            f"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode "
            f"/Length {len(rgb_stream)}{image_extra} >>\nstream\n"
        ).encode("ascii")
        + rgb_stream
        + b"\nendstream",
        (
            f"<< /Length {len(f'q {page_width:g} 0 0 {page_height:g} 0 0 cm /Im0 Do Q'.encode('ascii'))} >>\nstream\n"
            f"q {page_width:g} 0 0 {page_height:g} 0 0 cm /Im0 Do Q\nendstream"
        ).encode("ascii"),
    ]
    if alpha is not None:
        alpha_stream = zlib.compress(alpha, level=9)
        objects.append(
            (
                f"<< /Type /XObject /Subtype /Image /Width {width} /Height {height} "
                f"/ColorSpace /DeviceGray /BitsPerComponent 8 /Filter /FlateDecode "
                f"/Length {len(alpha_stream)} >>\nstream\n"
            ).encode("ascii")
            + alpha_stream
            + b"\nendstream"
        )

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref_offset = len(output)
    output.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for position in offsets[1:]:
        output.extend(f"{position:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return bytes(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_png", type=Path)
    parser.add_argument("output_pdf", type=Path)
    parser.add_argument("--width-inches", type=float, default=36)
    parser.add_argument("--height-inches", type=float, default=48)
    args = parser.parse_args()
    width, height, rgb, alpha = decode_png(args.source_png)
    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    args.output_pdf.write_bytes(pdf_bytes(width, height, rgb, alpha, args.width_inches * 72, args.height_inches * 72))
    print(f"Wrote {args.output_pdf}: {width}x{height} pixels, {args.width_inches:g}x{args.height_inches:g} inches")


if __name__ == "__main__":
    main()
