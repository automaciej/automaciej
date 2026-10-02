# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Maciej Bliziński's personal website and music portfolio at [blizin.ski](https://blizin.ski), built with Hugo. The site has several content streams: a music portfolio (releases, projects, performances), app pages (7 apps across iOS/macOS/Android/Web/Linux/Windows — not iOS-only), a Polish-language blog (Jogger) dating back to 2001, and a separate English blog.

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

- **Markdown/content pages** (`/content/`) — Jogger (Polish blog), English blog (`/blog/`), music releases (`/music/releases/<slug>/`), app support/landing pages, genres taxonomy, static EPK pages (bio, photos, press, performances)
- **TOML data files** (`/data/`) — App definitions (`/data/apps/`), performances (`/data/performances/`), collaborator projects (`/data/projects/`), and a couple of not-yet-migrated music releases (`/data/music/`)

Music releases are primarily **content pages**, not data files: each lives at `content/music/releases/<slug>/index.md` (YAML front matter: title, artist, genres, release_date, project, image, credits, links), rendered via a dedicated single-page layout. `/data/music/*.toml` still exists but only for the newest release or two that hasn't been migrated to a content page yet — when adding a new release, follow the existing `content/music/releases/*` examples, not the TOML format.

`links.youtube` in release front matter is a **bare video ID**, not a full URL (e.g. `youtube: YlDtj9GgfdY`, not `https://www.youtube.com/watch?v=...`) — true at both album level and per-track level. Other `links.*` keys (spotify, bandcamp_url, apple_music, etc.) are full URLs. When adding any link field, grep existing `content/music/releases/*/index.md` for that key first to match its format rather than assuming a URL.

Apps, performances, and projects remain purely data-driven (`/data/*.toml`), rendered via templates/partials. There are 7 apps (`task_compass`, `ego_destroyer`, `roadlapse`, `sunrise_watch`, `icantstart`, `whatsapp_archive`, `phpbb3_static`) spanning iOS, macOS, Android, Web, Linux, and Windows — not all iOS. Some apps (e.g. `ego-destroyer`) have their own content section for update posts.

### Theme

The active theme is `themes/multi-stream/` (custom), set via `theme = "multi-stream"` in `config.toml`. This is a plain directory, not a git submodule (no `.gitmodules` in the repo). `themes/musician/` is leftover cruft — an empty directory tree (`static/js/`, no files) not referenced by any config; safe to ignore or delete. The old `hugo-split-theme` has already been fully removed from the repo. Template precedence follows standard Hugo lookup order: project-level `layouts/` overrides theme templates.

### Jogger blog

- 173 posts in `/content/jogger/`, written in Polish, dating back to 2001
- Front matter is a **mix of TOML (`+++...+++`) and YAML (`---...---`)** — roughly 94 TOML / 79 YAML as of this writing. This is a migration in progress, not a settled convention; any script or tool touching Jogger front matter must handle both formats.
- Permalink pattern: `/jogger/:year/:contentbasename/`
- Explicitly excluded from the homepage (language separation); appears only on `/jogger/`

### Homepage layout

Three columns on desktop (`grid-template-columns: 1fr 1fr 1fr` at ≥1024px), stacked on mobile/tablet (order: Music, Apps, Bio on tablet):
- **Music** — latest 3 releases, same preview-card component used on `/music/`
- **Apps** — featured apps + latest update posts
- **Bio** — bio summary, plus a nested "Blog" sub-list (latest 2 posts from `/blog/`, the English blog — distinct from Jogger)

Jogger posts do not appear on the homepage (language separation); the English blog does.

### Deployment

Production target: `atemoia.blizinski.pl:www/blizin.ski` via rsync (755 dirs, 644 files). Preview deployment configuration lives in `private_cfg.sh` (gitignored).

### URL preservation

~93 URL aliases are maintained via `aliases:`/`aliases =` in front matter across content files. Do not remove these when editing pages.

### CSS

No CSS framework — `themes/multi-stream/assets/css/main.css` is 100% hand-written, custom CSS (despite what earlier versions of this file claimed about Pico CSS). Mobile-first with three canonical breakpoints: narrow/phones (`max-width: 767px`), tablet (`768px`–`1023px`), desktop (`min-width: 1024px`); a few grids (`.projects-grid`, `.genres-grid`) intentionally use their own `640px` breakpoint tied to their own column math. See `Docs/2025-11-12-multi-stream-theme.md`'s "CSS Architecture" section for the full reasoning (fluid `.container`, gap-based list spacing instead of per-card margins, why rules for one selector must stay co-located rather than scattered across the file).
