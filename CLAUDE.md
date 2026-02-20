# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Maciej Bliziński's personal website and music portfolio at [blizin.ski](https://blizin.ski), built with Hugo. The site has three main content streams: a music portfolio (data-driven), iOS app pages, and a Polish-language blog (Jogger) dating back to 2003.

## Commands

```bash
# Development server (live reload, includes drafts and future posts)
./util/deploy.sh dev

# Production build
hugo --cleanDestinationDir

# Deploy to production (blizin.ski)
./util/deploy.sh deploy

# Deploy preview (requires private_cfg.sh with PREVIEW_DEST and PREVIEW_URL)
./util/deploy.sh preview

# Create a new post
hugo new content jogger/<name>/index.md
```

### Image optimization

```bash
magick <name>-big.jpg -interlace jpeg -quality 35 <name>.jpg
```

### Python utilities

```bash
python3 util/tags_helper.py <content-dir>   # Audit tag coverage
python3 util/add_aliases.py <input> --write  # Add URL aliases to front matter
python3 util/jogger_to_pdf.py               # Export Jogger blog to PDF (needs pandoc + LaTeX)
```

## Architecture

### Content vs. Data separation

- **Markdown posts** (`/content/`) — Jogger blog, app support pages, static EPK pages
- **TOML data files** (`/data/`) — Music productions, performances, app definitions

Music and performances are rendered from `/data/` files via templates, not as individual content pages. Adding a new music release means creating a TOML file in `/data/music/`, not a Markdown post.

### Theme

The active theme is `themes/multi-stream/` (custom). The older `themes/hugo-split-theme/` is a git submodule but no longer active. Template precedence follows standard Hugo lookup order: project-level `layouts/` overrides theme templates.

### Jogger blog

- 183+ posts in `/content/jogger/`, written in Polish
- Uses **TOML** front matter (`+++...+++`), unlike other content which uses YAML (`---...---`)
- Permalink pattern: `/jogger/:year/:contentbasename/`
- Explicitly excluded from the homepage (language separation); appears only on `/jogger/`

### Homepage layout

Two-column desktop / stacked mobile layout:
- Left/top: Latest 3 music productions (from `/data/music/`)
- Right/bottom: App updates + bio snippet
- Jogger posts do not appear here

### Deployment

Production target: `atemoia.blizinski.pl:www/blizin.ski` via rsync (755 dirs, 644 files). Preview deployment configuration lives in `private_cfg.sh` (gitignored).

### URL preservation

192 URL aliases are maintained via `aliases:` in front matter. Do not remove these when editing pages.

### CSS dependency

Styles use [Pico CSS](https://picocss.com/docs) as a base framework.
