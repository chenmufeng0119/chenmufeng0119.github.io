#!/usr/bin/env python3
"""Update citation metadata for the configured Google Scholar profile."""

from __future__ import annotations

import os
import sys
from collections.abc import Mapping
from datetime import datetime

import yaml
from scholarly import scholarly

CONFIG_FILE = "_config.yml"
SOCIALS_FILE = "_data/socials.yml"
OUTPUT_FILE = "_data/citations.yml"


def load_profile_identity() -> tuple[str, str]:
    """Read the site owner's name and Scholar ID from the site configuration."""
    try:
        with open(CONFIG_FILE, encoding="utf-8") as config_stream:
            config = yaml.safe_load(config_stream) or {}
        with open(SOCIALS_FILE, encoding="utf-8") as socials_stream:
            socials = yaml.safe_load(socials_stream) or {}
    except (OSError, yaml.YAMLError) as error:
        print(f"Could not read profile identity from {CONFIG_FILE} and {SOCIALS_FILE}: {error}")
        sys.exit(1)

    name = " ".join(
        str(part).strip()
        for part in (config.get("first_name"), config.get("last_name"))
        if part and str(part).strip()
    )
    scholar_user_id = socials.get("scholar_userid")
    if not name:
        print(f"No first_name/last_name found in {CONFIG_FILE}.")
        sys.exit(1)
    if not scholar_user_id:
        print(f"No 'scholar_userid' found in {SOCIALS_FILE}.")
        sys.exit(1)
    return name, str(scholar_user_id).strip()


def normalized_name(value: object) -> str:
    return " ".join(str(value or "").split()).casefold()


def load_existing_data() -> dict:
    """Load prior citation data, including the valid empty-file case."""
    existing_data = {}
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, encoding="utf-8") as data_stream:
                existing_data = yaml.safe_load(data_stream) or {}
            if not isinstance(existing_data, dict):
                raise ValueError("expected a YAML mapping")
        except (OSError, ValueError, yaml.YAMLError) as error:
            print(f"Warning: Could not read existing citation data from {OUTPUT_FILE}: {error}.")
            existing_data = {}
    return existing_data


def get_scholar_citations() -> None:
    """Fetch and update Google Scholar citation data for the configured owner."""
    profile_name, scholar_user_id = load_profile_identity()
    existing_data = load_existing_data()
    today = datetime.now().strftime("%Y-%m-%d")
    metadata = existing_data.get("metadata", {})
    if not isinstance(metadata, Mapping):
        metadata = {}

    cached_papers = existing_data.get("papers")
    cache_matches_profile = (
        isinstance(cached_papers, Mapping)
        and all(
            str(pub_id).startswith(f"{scholar_user_id}:")
            for pub_id in cached_papers
        )
    )
    if (
        metadata.get("scholar_userid") == scholar_user_id
        and normalized_name(metadata.get("author_name")) == normalized_name(profile_name)
        and metadata.get("last_updated") == today
        and cache_matches_profile
    ):
        print(f"Citation data for {profile_name} was already updated today; skipping fetch.")
        return

    print(f"Fetching citations for {profile_name} (Google Scholar ID: {scholar_user_id})")
    scholarly.set_timeout(15)
    scholarly.set_retries(3)
    try:
        author = scholarly.search_author_id(scholar_user_id)
        author_data = scholarly.fill(author)
    except Exception as error:
        print(f"Error fetching Scholar author data for ID '{scholar_user_id}': {error}")
        sys.exit(1)

    if not author_data:
        print(f"Could not fetch author data for Scholar ID '{scholar_user_id}'.")
        sys.exit(1)
    author_scholar_id = author_data.get("scholar_id") or author_data.get("user_id")
    if (
        author_scholar_id != scholar_user_id
        or normalized_name(author_data.get("name")) != normalized_name(profile_name)
    ):
        print(
            "Scholar identity mismatch: expected "
            f"'{profile_name}' ({scholar_user_id}), received "
            f"'{author_data.get('name', '')}' ({author_scholar_id or 'missing ID'}). "
            "Citation data was not updated."
        )
        sys.exit(1)
    if "publications" not in author_data:
        print(f"No publications found in author data for Scholar ID '{scholar_user_id}'.")
        sys.exit(1)

    citation_data = {
        "metadata": {
            "scholar_userid": scholar_user_id,
            "author_name": profile_name,
            "last_updated": today,
        },
        "papers": {},
    }

    for pub in author_data["publications"]:
        try:
            pub_id = pub.get("pub_id") or pub.get("author_pub_id")
            if not pub_id:
                title = pub.get("bib", {}).get("title", "Unknown")
                print(f"Warning: Skipping publication without an ID: {title}")
                continue
            if not str(pub_id).startswith(f"{scholar_user_id}:"):
                print(f"Publication ID '{pub_id}' does not match the configured Scholar profile.")
                sys.exit(1)

            title = pub.get("bib", {}).get("title", "Unknown Title")
            year = pub.get("bib", {}).get("pub_year", "Unknown Year")
            citations = pub.get("num_citations", 0)
            print(f"Found: {title} ({year}) - Citations: {citations}")
            citation_data["papers"][pub_id] = {
                "title": title,
                "year": year,
                "citations": citations,
            }
        except Exception as error:
            title = pub.get("bib", {}).get("title", "Unknown")
            print(f"Error processing publication '{title}': {error}. Skipping it.")

    if citation_data == existing_data:
        print("Citation data matches the existing data; skipping file update.")
        return

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as output_stream:
            yaml.safe_dump(
                citation_data,
                output_stream,
                width=1000,
                sort_keys=True,
                allow_unicode=True,
            )
        print(f"Citation data saved to {OUTPUT_FILE}")
    except OSError as error:
        print(f"Error writing citation data to {OUTPUT_FILE}: {error}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        get_scholar_citations()
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)
