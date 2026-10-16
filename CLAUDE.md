# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Maciej Bliziński's personal website and music portfolio at [blizin.ski](https://blizin.ski), built with Hugo. The site has several content streams: a music portfolio (releases, projects, performances), app pages (across several platforms, not iOS-only), a Polish-language blog (Jogger) dating back to 2001, and a separate English blog.

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

Detailed, dated descriptions live in `Docs/`; start with `Docs/2026-10-16-site-architecture.md`
(content vs. data, release link formats, collaborator projects, per-service song lists, theme,
Jogger, homepage, deployment, CSS). Read the relevant doc before changing that area, and update or
add a dated doc there rather than expanding this file.

Principles that hold across the repo:

- **Content vs. data.** Releases, collaborator projects, the blogs and static pages are Markdown
  content pages; apps and performances are TOML in `data/`. Follow the newest existing examples
  when adding an item, and grep existing front matter for a key's format before adding it.
- **Theme.** The active theme is the custom `themes/multi-stream/`; project-level `layouts/`
  overrides it. Shortcodes live in `layouts/shortcodes/`.
- **No cookie-setting embeds.** Music services and social posts are links, not iframes; the only
  embeds are `youtube-nocookie.com` players. `util/test_site_expectations.py` enforces this.
- **Jogger** is Polish, stays off the homepage, and its front matter is a mix of TOML and YAML, so
  tools touching it must handle both.
- **CSS** is hand-written with no framework, mobile-first, with canonical breakpoints (phones
  `max-width: 767px`, tablet `768px`–`1023px`, desktop `min-width: 1024px`). See "CSS Architecture"
  in `Docs/2025-11-12-multi-stream-theme.md`.
- **Deployment** goes through `./util/deploy.sh`; preview settings live in the gitignored
  `private_cfg.sh`.
- **URL preservation.** Many URL aliases are kept in front matter (`aliases:` / `aliases =`). Do not
  remove them when editing pages.

### HTML templates

When closing a `<div>` (or other container tag) in template files, annotate the closing tag with its class: `<div class="foo">` ... `</div><!-- foo -->`. Helps track matching tags in templates with deep nesting.

### Before committing

Before running `git commit`, run `git diff` (staged + unstaged) and read it against the
instruction/intent that prompted the change. Confirm every hunk is explained by that intent —
no stray edits, no leftover debug code, no unrelated files swept in. Do this each time, even for
small changes.

Run the site expectations test; it builds the site and checks head tags,
structured data, feeds, links, and the /bio/ releases list:

```bash
python3 util/test_site_expectations.py
```

All tests must pass before `git commit`. When a feature once went missing and
had to be restored, add a test for it in `util/test_site_expectations.py`.

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
