#!/usr/bin/env python3
"""
Add release_date param and reset date to page-publish date in all release pages.
"""
import re
from pathlib import Path

RELEASES_DIR = Path(__file__).parent.parent / "content" / "music" / "releases"
PAGE_DATE = "2026-05-18"

for md_file in sorted(RELEASES_DIR.rglob("index.md")):
    text = md_file.read_text()
    # Extract date value from front matter
    m = re.search(r"^date: '?([^'\n]+)'?", text, re.MULTILINE)
    if not m:
        print(f"  SKIP (no date): {md_file}")
        continue
    release_date = m.group(1).strip()
    # Already patched?
    if "release_date:" in text:
        print(f"  SKIP (already has release_date): {md_file}")
        continue
    # Replace date line with page date, insert release_date on next line
    new_text = re.sub(
        r"^(date: )'?[^'\n]+'?",
        lambda _: f"date: '{PAGE_DATE}'\nrelease_date: '{release_date}'",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    md_file.write_text(new_text)
    slug = md_file.parent.name
    print(f"  {slug}: date={PAGE_DATE}, release_date={release_date}")
