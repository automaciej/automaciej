# Site architecture reference

Date: 2026-10-16

Detailed description of how the site is put together, moved out of `CLAUDE.md`
so that file can stay generic. Counts and lists below are a snapshot of this
date; check the repo for current numbers.

## Content vs. data

- **Content pages** (`content/`): Jogger (Polish blog), English blog (`/blog/`),
  music releases (`/music/<slug>/`), app support/landing pages, genres
  taxonomy, static EPK pages (bio, photos, press, performances).
- **TOML data files** (`data/`): app definitions (`data/apps/`), performances
  (`data/performances/`), and a couple of not-yet-migrated music releases
  (`data/music/`).

### Music releases

Releases are content pages: `content/music/<slug>/index.md` (YAML front
matter: title, artist, genres, release_date, project, image, credits, links),
rendered by a dedicated single-page layout. `data/music/*.toml` only holds the
newest release or two that have not been migrated; new releases follow the
`content/music/<slug>/` examples, not the TOML format.

Releases sit directly under `/music/`, beside other kinds of `/music/<thing>/` pages
(performances, credits, the per-service lists, projects). `/music/` itself is the
release list; there is no `/music/releases/` section any more. A page counts as a
release when it has `Params.release_date`; templates get them from
`partials/release-pages.html` and never from a section lookup. A release slug must not
equal another `/music/` page name (tested).

Redirects: releases that existed on 2026-10-16 carry `aliases: [/music/releases/<slug>/]`,
and `/music/` aliases `/music/releases`. New releases must not get an old-style alias;
the frozen list is `LEGACY_RELEASE_SLUGS` in the tests, so a copied alias fails the
build. The old `/music/releases/index.xml` feed is gone; `/music/index.xml` replaces it.

### Release `links` front matter

- `links.youtube` is a **bare video ID**, not a URL, at album and per-track level.
- Spotify and Apple Music are bare IDs too, one key per kind: `spotify_track`,
  `spotify_album`, `spotify_artist`, `apple_music_track`, `apple_music_album`
  (also valid per track under `tracks[].links`; a track with only
  `apple_music_track` takes the album ID from the release's `apple_music_album`).
- YouTube Music reuses the `youtube` video ID; set `youtube_music_track` only when
  it differs, or `youtube_music_album` (an `OLAK5uy_…` playlist ID) for an album.
- `instagram` is a bare reel ID.
- `bandcamp_url`, `soundcloud_url`, `streaming`, `deezer`, `tidal`,
  `amazon_music` and similar are full URLs.
- URLs are built from the IDs in `partials/music-service-urls.html`.
- Before adding any link field, grep existing releases for that key to match its
  format.

### Apps

Apps and performances are purely data-driven (`data/*.toml`) and rendered by
templates/partials. There are 7 apps (`task_compass`, `ego_destroyer`,
`roadlapse`, `sunrise_watch`, `icantstart`, `whatsapp_archive`, `phpbb3_static`)
across iOS, macOS, Android, Web, Linux and Windows. Some (e.g. `ego-destroyer`)
have their own content section for update posts.

### Collaborator projects

Content pages at `content/music/projects/<slug>/_index.md`, `type: "music-project"`.
`params.key` is the slug, matched against performances' and releases' `project`
field. Optional: `params.country`, `start_year`, `end_year`, `url`, `with` (list
of collaborator names). The page `title` is the display name (no separate `name`);
the Markdown body is the description (not a `description` field). `params.roles`
is deliberately not tracked; it is inferable from release credits. Templates read
these pages via `$.Site.GetPage (printf "/music/projects/%s" $key)`. There is no
`data/projects/` any more and no `hugo.Data.projects`.

## Third-party players and cookies

No third-party player sets cookies on the site.

- Spotify, Apple Music, YouTube Music, Bandcamp, SoundCloud and Instagram are
  plain links, never iframes.
- The only embeds are YouTube players from `youtube-nocookie.com`:
  `partials/music-release.html`, and the built-in `{{< youtube >}}` shortcode used
  in Jogger via `privacy.youtube.privacyEnhanced` in `config.toml`.
- `util/test_site_expectations.py` fails on any other iframe.
- The `{{< listen >}}` shortcode (`layouts/shortcodes/listen.html`) renders link
  buttons using the same keys as release `links` front matter
  (e.g. `{{< listen bandcamp_url="…" title="…" >}}`,
  `{{< listen instagram="REEL_ID" >}}`). It and the release RSS feed share
  `partials/listen-links.html`.
- Release RSS items end with "Listen on …" links (release-level, then per track).
- Link buttons (`.listen-links a`, `.streaming-link a`, `.instagram-link a`) are
  accent-blue pills in `main.css`.

## Per-service song lists

`/music/spotify/`, `/music/apple/` and `/music/youtube/` are reverse-chronological
lists of releases with a direct link on that service.

- Content pages (`content/music/{spotify,apple,youtube}.md`) with
  `layout: streaming` (`themes/multi-stream/layouts/music/streaming.html`).
- Front matter `service_key` (`spotify` / `apple_music` / `youtube_music`) picks
  the service; `title` is the service name, from which the page title
  ("Maciej Bliziński: Music on Spotify") and breadcrumb are composed.
- The page `<h1>` is "On <Service>". Each entry is a row: release artwork thumbnail
  (same Hugo-resized cover as the homepage preview cards) with the service logo, or
  a generic external-link icon, in its top right corner (3px inset); then the song title linking to
  the service (external-link icon after it) with "by artist · Mon Year" beneath
  (the date links to the release page). Artwork and title both open the service.
- Service logos come from `service_icons` in `content/music/_index.md` front matter,
  keyed by `service_key` (e.g. `spotify: /images/services/spotify.png`, file in
  `static/images/services/`). A service without an entry gets the generic icon.
- Per release: if any `tracks[]` has an ID for the service, each such track is
  listed; otherwise the release-level ID is used. Artist-only Spotify links,
  future-dated and draft releases are skipped. Logic lives in
  `partials/streaming-items.html`.
- Each page has its own RSS feed (`/music/<service>/index.xml`): front matter
  `outputs: [html, rss]` plus `layouts/music/streaming.rss.xml`, which reuses
  `streaming-items.html`. Item `<link>` is the release page; the description holds
  the "Listen on <service>" link. A new service page needs the `outputs` line.
- Adding a service means a new content page plus a branch in
  `music-service-urls.html` (and in `listen-links.html` for the shortcode/RSS).

## Theme

`themes/multi-stream/` (custom), `theme = "multi-stream"` in `config.toml`. A plain
directory, not a submodule. `themes/musician/` is an empty leftover and can be
ignored or deleted. `hugo-split-theme` is gone. Project-level `layouts/` overrides
theme templates (standard Hugo lookup order).

## Jogger blog

- 173 posts in `content/jogger/`, Polish, dating back to 2001.
- Front matter is a mix of TOML (`+++`) and YAML (`---`): roughly 94 / 79. A
  migration in progress; tools touching Jogger front matter must handle both.
- Permalink pattern `/jogger/:year/:contentbasename/`.
- Excluded from the homepage (language separation); appears only on `/jogger/`.

## Homepage layout

Three columns at ≥1024px (`grid-template-columns: 1fr 1fr 1fr`), stacked on
mobile/tablet (tablet order: Music, Apps, Bio):

- **Music**: latest 3 releases, same preview card as `/music/`.
- **Apps**: featured apps and latest update posts.
- **Bio**: bio summary plus a nested "Blog" list (latest 2 posts from `/blog/`,
  the English blog, distinct from Jogger).

## Deployment

Production: `atemoia.blizinski.pl:www/blizin.ski` via rsync (755 dirs, 644 files).
Preview configuration is in `private_cfg.sh` (gitignored).

## URL preservation

About 93 aliases are kept via `aliases:` / `aliases =` in front matter across
content files.

## CSS

`themes/multi-stream/assets/css/main.css` is hand-written, no framework.
Mobile-first with three canonical breakpoints: phones (`max-width: 767px`),
tablet (`768px`–`1023px`), desktop (`min-width: 1024px`). A few grids
(`.projects-grid`, `.genres-grid`) use their own `640px` breakpoint tied to their
column math. See `Docs/2025-11-12-multi-stream-theme.md` ("CSS Architecture")
for the reasoning: fluid `.container`, gap-based list spacing, and why rules for
one selector stay co-located.
