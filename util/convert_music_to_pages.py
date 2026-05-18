#!/usr/bin/env python3
"""Convert /data/music/*.toml to /content/music/releases/{slug}/index.md"""

import os
import re
import sys
import unicodedata
import tomli
import yaml
from pathlib import Path

REPO = Path(__file__).parent.parent
DATA_DIR = REPO / "data" / "music"
OUT_DIR = REPO / "content" / "music" / "releases"


def slugify(text):
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.ASCII)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def convert(toml_path):
    with open(toml_path, "rb") as f:
        data = tomli.load(f)

    PAGE_DATE = "2026-05-18"

    title = data.pop("title")
    release_date = data.pop("date")
    description = data.pop("description", "").strip()

    # Build front matter dict
    fm = {
        "title": title,
        "date": PAGE_DATE,
        "release_date": release_date.isoformat() if hasattr(release_date, "isoformat") else str(release_date),
    }

    # Pass through all remaining scalar/structured fields as params
    for key in ["artist", "single", "album", "project", "image"]:
        if key in data:
            fm[key] = data.pop(key)

    credits = data.pop("credits", None)
    if credits:
        fm["credits"] = credits

    links = data.pop("links", None)
    if links:
        fm["links"] = links

    slug = slugify(title)
    out_dir = OUT_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.md"

    front = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
    body = description if description else ""

    content = f"---\n{front}---\n"
    if body:
        content += f"\n{body}\n"

    out_file.write_text(content, encoding="utf-8")
    print(f"  {toml_path.name} → releases/{slug}/index.md")
    return slug


def main():
    toml_files = sorted(DATA_DIR.glob("*.toml"))
    if not toml_files:
        print("No TOML files found in", DATA_DIR)
        sys.exit(1)

    print(f"Converting {len(toml_files)} files...")
    slugs = []
    for f in toml_files:
        slugs.append(convert(f))

    print(f"\nDone. {len(slugs)} releases written to {OUT_DIR}")
    print("\nCheck for duplicate slugs:")
    seen = set()
    for s in slugs:
        if s in seen:
            print(f"  DUPLICATE SLUG: {s}")
        seen.add(s)


if __name__ == "__main__":
    main()
