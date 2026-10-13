#!/usr/bin/env python3
"""Generate the downloadable public CV PDF from the site's cv.yml source."""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_data" / "cv.yml"
SOCIALS_SOURCE = ROOT / "_data" / "socials.yml"
DEFAULT_OUTPUT = ROOT / "assets" / "pdf" / "cv.pdf"
DEFAULT_JSON_OUTPUT = ROOT / "assets" / "json" / "resume.json"
PAGE_WIDTH = 612
PAGE_HEIGHT = 792
LEFT = 48
RIGHT = 48
TOP = 744
BOTTOM = 48


def pdf_string(value: str) -> bytes:
    """Encode text for a built-in Helvetica font with WinAnsiEncoding."""
    raw = value.encode("cp1252", errors="replace")
    escaped = bytearray(b"(")
    for byte in raw:
        if byte in (40, 41, 92):
            escaped.extend(b"\\" + bytes([byte]))
        elif byte < 32 or byte > 126:
            escaped.extend(f"\\{byte:03o}".encode("ascii"))
        else:
            escaped.append(byte)
    escaped.extend(b")")
    return bytes(escaped)


class CVPDF:
    def __init__(self, cv: dict):
        self.cv = cv
        self.pages: list[list[bytes]] = [[]]
        self.y = TOP

    def _raw(self, command: str) -> None:
        self.pages[-1].append(command.encode("ascii"))

    def _new_page(self) -> None:
        self.pages.append([])
        self.y = TOP
        if len(self.pages) > 1:
            self._line(self.cv.get("name", "Mufeng Chen"), size=10, bold=True)
            self._line("Curriculum Vitae (continued)", size=8, color="0.35 0.35 0.35")
            self.y -= 8

    def _ensure(self, height: float) -> None:
        if self.y - height < BOTTOM:
            self._new_page()

    def _line(
        self,
        value: str,
        *,
        size: float = 9,
        bold: bool = False,
        x: float = LEFT,
        color: str = "0.12 0.14 0.18",
        leading: float | None = None,
    ) -> None:
        leading = leading or size * 1.28
        self._ensure(leading)
        font = "F2" if bold else "F1"
        self._raw(f"{color} rg BT /{font} {size:.1f} Tf {x:.1f} {self.y:.1f} Td ")
        self.pages[-1].append(pdf_string(value) + b" Tj ET")
        self.y -= leading

    def _paragraph(self, value: str, *, size: float = 9, indent: float = 0, bold: bool = False) -> None:
        width = max(35, int((PAGE_WIDTH - LEFT - RIGHT - indent) / (size * 0.50)))
        lines = textwrap.wrap(
            " ".join(str(value).split()),
            width=width,
            break_long_words=True,
            break_on_hyphens=False,
        ) or [""]
        for line in lines:
            self._line(line, size=size, bold=bold, x=LEFT + indent)

    def _section(self, title: str) -> None:
        self.y -= 1
        self._ensure(18)
        self._line(title.upper(), size=9.5, bold=True, color="0.10 0.29 0.45", leading=12)
        self._raw(f"0.68 0.75 0.81 RG 0.6 w {LEFT} {self.y + 4:.1f} m {PAGE_WIDTH - RIGHT} {self.y + 4:.1f} l S")
        self.y -= 2

    def _date_range(self, item: dict) -> str:
        start = item.get("start_date")
        end = item.get("end_date")
        if not start:
            return ""
        return f"{start}–{end}" if end else str(start)

    def _entry(self, item: dict, section: str) -> None:
        if "bullet" in item:
            citation = str(item["bullet"])
            if section == "Selected Publications":
                title_match = re.search(r"“([^”]+)”", citation)
                if title_match:
                    authors = citation[: title_match.start()].strip().rstrip(" .")
                    title = title_match.group(1).rstrip(" .")
                    venue = citation[title_match.end() :].split("DOI:", 1)[0].strip().rstrip(" .")
                    first_author = authors.split(",", 1)[0]
                    citation = f"{first_author} et al. “{title}.” {venue}"
                self._paragraph(f"- {citation}", size=8.1, indent=4)
            else:
                self._paragraph(f"- {citation}", size=8.4, indent=4)
            return
        if "label" in item and "details" in item:
            self._paragraph(f"{item['label']}: {item['details']}", size=8.4)
            self.y -= 2
            return

        if section == "Education":
            title = str(item.get("institution", ""))
            degree = str(item.get("degree", ""))
            if degree:
                title += f" — {degree}"
            self._paragraph(title, size=9.2, bold=True)
            metadata = " | ".join(part for part in [item.get("area"), item.get("location")] if part)
            dates = self._date_range(item)
            if dates:
                metadata = " | ".join(part for part in [metadata, dates] if part)
            if metadata:
                self._paragraph(metadata, size=8.4)
        else:
            title = " — ".join(str(item.get(k, "")) for k in ("position", "company") if item.get(k))
            self._paragraph(title, size=9.2, bold=True)
            metadata = " | ".join(part for part in [item.get("location"), self._date_range(item)] if part)
            if metadata:
                self._paragraph(metadata, size=8.4)

        if item.get("summary"):
            self._paragraph(str(item["summary"]), size=8.6, indent=5)
        for highlight in item.get("highlights", []) or []:
            self._paragraph(f"- {highlight}", size=8.4, indent=5)
        self.y -= 2

    def render(self) -> bytes:
        self._line(self.cv.get("name", "Mufeng Chen"), size=23, bold=True, color="0.08 0.15 0.22", leading=28)
        self._line(str(self.cv.get("headline", "")), size=10, color="0.25 0.29 0.33", leading=14)
        contact = " | ".join(str(part) for part in [self.cv.get("email"), self.cv.get("location")] if part)
        if contact:
            self._line(contact, size=8.7, color="0.25 0.29 0.33", leading=12)
        social = self.cv.get("social_networks", []) or []
        social_text = " | ".join(f"{x.get('network')}: github.com/{x.get('username')}" for x in social if x.get("username"))
        if social_text:
            self._line(social_text, size=8.2, color="0.25 0.29 0.33", leading=11)
        self.y -= 6

        for section, entries in (self.cv.get("sections", {}) or {}).items():
            if section == "Technical Skills":
                self._ensure(74)
            self._section(str(section))
            for item in entries or []:
                if not isinstance(item, dict):
                    self._paragraph(str(item))
                else:
                    self._entry(item, str(section))

        return self._make_pdf()

    def _make_pdf(self) -> bytes:
        objects: list[bytes] = []

        def add(value: bytes) -> int:
            objects.append(value)
            return len(objects)

        catalog_id = add(b"")
        pages_id = add(b"")
        font_regular_id = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        font_bold_id = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        page_ids: list[int] = []

        for page_commands in self.pages:
            content = b"\n".join(page_commands) + b"\n"
            stream_id = add(b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"endstream")
            page_id = add(
                (
                    f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                    f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >> >> "
                    f"/Contents {stream_id} 0 R >>"
                ).encode("ascii")
            )
            page_ids.append(page_id)

        objects[catalog_id - 1] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii")
        kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
        objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")

        result = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for object_id, value in enumerate(objects, start=1):
            offsets.append(len(result))
            result.extend(f"{object_id} 0 obj\n".encode("ascii"))
            result.extend(value)
            result.extend(b"\nendobj\n")
        xref_offset = len(result)
        result.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        result.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            result.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
        result.extend(
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode(
                "ascii"
            )
        )
        return bytes(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    args = parser.parse_args()

    data = yaml.safe_load(SOURCE.read_text(encoding="utf-8")) or {}
    cv = data.get("cv")
    if not isinstance(cv, dict):
        raise SystemExit(f"Expected a 'cv' mapping in {SOURCE}")

    pdf_bytes = CVPDF(cv).render()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pdf_bytes)

    resume = resume_json(cv)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(resume, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    try:
        output_label = args.output.relative_to(ROOT)
    except ValueError:
        output_label = args.output
    try:
        json_label = args.json_output.relative_to(ROOT)
    except ValueError:
        json_label = args.json_output
    print(f"Wrote {output_label} ({len(pdf_bytes)} bytes)")
    print(f"Wrote {json_label}")


def resume_json(cv: dict) -> dict:
    """Build the site's JSON Resume record from its CV YAML."""
    sections = cv.get("sections", {}) or {}
    summary = " ".join(str(item.get("bullet", "")) for item in sections.get("Summary", []) if isinstance(item, dict))
    location_parts = [part.strip() for part in str(cv.get("location", "")).split(",", 1)]
    location = {"city": location_parts[0]} if location_parts and location_parts[0] else {}
    if len(location_parts) > 1:
        location["region"] = location_parts[1].strip()
    if location:
        location["countryCode"] = "US"

    profiles = []
    for social in cv.get("social_networks", []) or []:
        network, username = social.get("network"), social.get("username")
        if network and username:
            profiles.append({"network": network, "url": f"https://github.com/{username}", "username": username})
    if SOCIALS_SOURCE.exists():
        socials = yaml.safe_load(SOCIALS_SOURCE.read_text(encoding="utf-8")) or {}
        scholar_id = socials.get("scholar_userid")
        if scholar_id:
            profiles.append({
                "network": "Google Scholar",
                "url": f"https://scholar.google.com/citations?user={scholar_id}&hl=en",
                "username": scholar_id,
            })
        orcid = socials.get("orcid_id")
        if orcid:
            profiles.append({"network": "ORCID", "url": f"https://orcid.org/{orcid}", "username": orcid})

    image = "/assets/img/prof_pic.png"
    basics = {
        "name": cv.get("name", ""),
        "label": cv.get("headline", ""),
        "email": cv.get("email", ""),
        "location": location,
        "summary": summary,
        "profiles": profiles,
    }
    if (ROOT / image.lstrip("/")).exists():
        basics["image"] = image

    work = []
    for section in ("Experience", "Research Internships", "Earlier Experience"):
        for item in sections.get(section, []) or []:
            work.append({
                "name": item.get("company", ""),
                "position": item.get("position", ""),
                "location": item.get("location", ""),
                "startDate": str(item.get("start_date", "")),
                **({"endDate": str(item["end_date"])} if item.get("end_date") else {}),
                "summary": item.get("summary", ""),
                "highlights": item.get("highlights", []) or [],
            })

    education = []
    for item in sections.get("Education", []) or []:
        education.append({
            "institution": item.get("institution", ""),
            "location": item.get("location", ""),
            "area": item.get("area", ""),
            "studyType": item.get("degree", ""),
            "startDate": str(item.get("start_date", "")),
            **({"endDate": str(item["end_date"])} if item.get("end_date") else {}),
        })

    publications = []
    for item in sections.get("Selected Publications", []) or []:
        citation = str(item.get("bullet", ""))
        title_match = re.search(r"“([^”]+)”", citation)
        title = title_match.group(1) if title_match else citation
        before = citation[: title_match.start()].strip() if title_match else ""
        after = citation[title_match.end() :].strip() if title_match else ""
        doi_match = re.search(r"DOI:\s*(\S+)", after, re.IGNORECASE)
        year_match = re.search(r"\b(?:19|20)\d{2}\b", after)
        publisher = after[: doi_match.start()].rstrip(" .") if doi_match else after.rstrip(" .")
        publication = {"name": title, "publisher": publisher}
        if year_match:
            publication["releaseDate"] = year_match.group(0)
        if doi_match:
            publication["url"] = f"https://doi.org/{doi_match.group(1).rstrip('.')}"
        if before:
            publication["summary"] = before.rstrip(" .")
        publications.append(publication)

    skills = []
    for item in sections.get("Technical Skills", []) or []:
        if item.get("label") and item.get("details"):
            skills.append({"name": item["label"], "keywords": [x.strip() for x in str(item["details"]).split(",")]})

    return {
        "basics": basics,
        "work": work,
        "education": education,
        "publications": publications,
        "skills": skills,
    }


if __name__ == "__main__":
    main()
