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
- **TOML data files** (`/data/`) — App definitions (`/data/apps/`), performances (`/data/performances/`), and a couple of not-yet-migrated music releases (`/data/music/`)

Music releases are primarily **content pages**, not data files: each lives at `content/music/releases/<slug>/index.md` (YAML front matter: title, artist, genres, release_date, project, image, credits, links), rendered via a dedicated single-page layout. `/data/music/*.toml` still exists but only for the newest release or two that hasn't been migrated to a content page yet — when adding a new release, follow the existing `content/music/releases/*` examples, not the TOML format.

`links.youtube` in release front matter is a **bare video ID**, not a full URL (e.g. `youtube: YlDtj9GgfdY`, not `https://www.youtube.com/watch?v=...`) — true at both album level and per-track level. Other `links.*` keys (spotify, bandcamp_url, apple_music, etc.) are full URLs. When adding any link field, grep existing `content/music/releases/*/index.md` for that key first to match its format rather than assuming a URL.

Apps and performances remain purely data-driven (`/data/*.toml`), rendered via templates/partials. There are 7 apps (`task_compass`, `ego_destroyer`, `roadlapse`, `sunrise_watch`, `icantstart`, `whatsapp_archive`, `phpbb3_static`) spanning iOS, macOS, Android, Web, Linux, and Windows — not all iOS. Some apps (e.g. `ego-destroyer`) have their own content section for update posts.

Collaborator projects are **content pages**, not data files: each lives at `content/music/projects/<slug>/_index.md`. Front matter (`type: "music-project"`) carries `params.key` (the slug, used to match performances' and releases' `project` field) plus optional `params.country`, `params.start_year`, `params.end_year`, `params.url`, and `params.with` (a list of collaborator names). The page `title` is the project's display name — there is no separate `name` field. `params.roles` is intentionally not tracked here; it's inferable from release credits. The page body (Markdown) is the project description, rendered via `.Content`/`.Plain` — not a `description` field. `/data/projects/*.toml` no longer exists; templates read project metadata from these content pages' `Params`/`Title`/`Plain` directly (e.g. via `$.Site.GetPage (printf "/music/projects/%s" $key)`), not `hugo.Data.projects`.

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

### HTML templates

When closing a `<div>` (or other container tag) in template files, annotate the closing tag with its class: `<div class="foo">` ... `</div><!-- foo -->`. Helps track matching tags in templates with deep nesting.

### CSS

No CSS framework — `themes/multi-stream/assets/css/main.css` is 100% hand-written, custom CSS (despite what earlier versions of this file claimed about Pico CSS). Mobile-first with three canonical breakpoints: narrow/phones (`max-width: 767px`), tablet (`768px`–`1023px`), desktop (`min-width: 1024px`); a few grids (`.projects-grid`, `.genres-grid`) intentionally use their own `640px` breakpoint tied to their own column math. See `Docs/2025-11-12-multi-stream-theme.md`'s "CSS Architecture" section for the full reasoning (fluid `.container`, gap-based list spacing instead of per-card margins, why rules for one selector must stay co-located rather than scattered across the file).

### Before committing

Before running `git commit`, run `git diff` (staged + unstaged) and read it against the
instruction/intent that prompted the change. Confirm every hunk is explained by that intent —
no stray edits, no leftover debug code, no unrelated files swept in. Do this each time, even for
small changes.

### Change-landing checklist (CSS / responsive images / cross-content links)

Learned from recurring same-day fix-up commits — check these before considering a change done, not after:

- **New or moved CSS selector near a media query**: verify the base (non-media-query) rule and
  any breakpoint overrides for the same selector are co-located and in the right source order
  (base rules first, breakpoint overrides after) — a base rule declared *after* a breakpoint
  block silently wins at every width. See `Docs/2025-11-12-multi-stream-theme.md`'s CSS
  Architecture section.
- **`sizes`/`srcset` attributes on `<img>`**: the `sizes` value is a claim about the image's
  *actual rendered width* at each breakpoint. Before adding or changing it, check the current
  CSS for that selector at each breakpoint it mentions — don't write `sizes` against an assumed
  layout.
- **New partial that links content item A to content item B by matching on a field** (e.g. a
  person's name, a slug): handle the "no match found" case explicitly (fall back to plain text/
  no link) rather than assuming the match always exists. Test against at least one item that is
  known *not* to match.
- **New page layout / redesigned partial**: before considering it done, check it against the
  full range of real content it will render — items with missing optional fields (no image, no
  playback links, no credits), not just the item used while developing it.
- **Removing a feature/block from a template**: prefer deleting the `{{ }}` logic outright (or
  gating it behind a boolean/feature check) over wrapping it in an HTML comment — Hugo's
  Go-template actions still execute inside an HTML comment, so "commented out" markup is not
  actually inert.
- **Adding script/markup to a shared template** (`baseof.html` or any partial included on every
  page): check which pages the feature actually applies to. If it's one page type, scope the
  addition to that page's own template (e.g. a `define`d block baseof only renders a default
  for), not the shared wrapper every page pays for.
- **Commit messages**: before writing "Remove X," confirm the diff actually removes X's
  execution path, not just its visible markup — "commented out" is not "removed."
- **Naming a new taxonomy/field/key**: decide the final name before wiring it into front matter
  or config across multiple files. A same-day rename after the fact means touching every
  reference twice for no functional reason.
