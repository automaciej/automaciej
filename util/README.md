## jogger_to_pdf.py

Generate a PDF book from all Jogger blog posts.

### Usage

```bash
# Generate jogger.pdf in the repo root
./util/jogger_to_pdf.py

# Specify output location
./util/jogger_to_pdf.py -o /path/to/my-jogger.pdf

# Save the intermediate markdown file for debugging
./util/jogger_to_pdf.py --temp-md jogger-combined.md
```

### Requirements

- **pandoc** - Install with `brew install pandoc`
- **LaTeX** (for PDF generation) - Install with `brew install --cask mactex-no-gui`

### What it does

1. Collects all markdown files from `content/jogger/`
2. Sorts them chronologically by date from frontmatter
3. Combines them into a single markdown document
4. Converts to PDF using pandoc with:
   - Table of contents
   - A4 paper size
   - 1 inch margins
   - Each post as a separate chapter

### Output

The generated PDF includes:
- All 172+ blog posts in chronological order
- Post titles as chapter headings
- Publication dates
- Full content including formatting
- Page breaks between posts

## check_service_metadata.py

Checks that each music service credits a release to the artists in its `artist:` front matter,
flags a single bundled artist ("Gaia Marenghi x Maciej Bliziński") where there should be two
collaborating ones, and prints a plain-text report to paste into a distributor support request:
per release, each problem with the link, what the service shows, and what is expected (with the
existing artist profile IDs where the services show them), plus the UPC/ISRC.

Reads public pages and APIs only: Apple Music/iTunes, Spotify, Deezer and YouTube. Qobuz blocks
automated page reads, so for Qobuz only the artist words in our own Qobuz link are judged, and the
report says so. Tidal, Amazon Music, Bandcamp and SoundCloud are listed as not checked. Standard
library only.

Which releases and services to check is configured in `util/service_metadata.json` (`releases`,
`services`, `cache_ttl_hours`). Results are cached per service resource in
`.cache/service-metadata.json` (gitignored) for 24 hours; failed lookups are never cached.

```bash
python3 util/check_service_metadata.py                      # the configured releases
python3 util/check_service_metadata.py loser 11ell-11eaven  # chosen releases instead of the config
python3 util/check_service_metadata.py --service apple      # one service
python3 util/check_service_metadata.py --refresh            # ignore the cache (after a fix)
python3 util/check_service_metadata.py --no-cache           # do not read or write the cache
python3 util/test_check_service_metadata.py                 # offline tests, no network
```

Exit status is 1 when any service is MERGED (one combined artist) or MISSING (an expected artist
is not credited).
