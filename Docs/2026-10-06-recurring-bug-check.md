# Recurring-bug check: bugs found by `util/test_site_expectations.py`

Date: 2026-10-06

## Why this exists

The last two months of git history contain a series of fixes for things a
website is generally expected to have and that were missing: OpenGraph/Twitter
tags, RSS feeds and autodiscovery links, JSON-LD, working internal links,
correct `lang`, fingerprinted CSS, scoped scripts, URL aliases. Each was
added after the fact, and each is the kind of thing a template refactor can
silently drop again.

`util/test_site_expectations.py` builds a copy of the working tree (same
approach as `util/diff_commits.sh`) and asserts those expectations over every
generated page. Each test names the commit that introduced the feature it
guards. The first run found 9 failing tests, all caused by real defects in the
site rather than in the test.

## Bugs found

| # | Bug | Root cause | Test that caught it |
|---|-----|------------|---------------------|
| 1 | `/apps/` and `/ego-destroyer/` serve **invalid JSON-LD** (the `SoftwareApplication` data is unusable by crawlers) | The `jsonld/app-fields.html` partial returns text that Hugo HTML-escapes when it is placed inside the `<script>` block: quotes become `&#34;`, and the whole field list collapses into one bogus key | `test_all_jsonld_is_valid_json`, `test_app_pages_have_softwareapplication` |
| 2 | `/music/performances/` has no `og:description` / `twitter:description` | The page uses `music/single.html`, whose `head_extra` block is written for release pages and only emits description tags when the page has body text before the shortcode output | `test_every_page_has_complete_tags_exactly_once` |
| 3 | `/music/performances/` ships the release page share-button script | `scripts_extra` in `music/single.html` is not limited to release pages (the same layout serves non-release pages under `/music/`) | `test_share_script_only_on_release_pages` |
| 4 | Home page `og:image` returns 404 (`/maciej_on_bass_360px.jpg`) | `content/_index.md` `image:` holds a bare filename; the default og partial resolves it against the site root, but the file lives in `static/bio/images/`. The Person JSON-LD works around this by prefixing `bio/images/` itself | `test_local_social_images_exist_in_output` |
| 5 | 8 Jogger posts from 2017 missing from `/jogger/index.xml` | They live in sub-folders (e.g. `content/jogger/porta-dos-fundos/opcje.md`); the feed template uses `RegularPages`, which is not recursive | `test_feeds_are_not_truncated` |
| 6 | Home and `/music/` feeds contain `/music/apple/` (and the other per-service lists) with an empty description | The list pages have no body text and are not marked `excludeFromRSS` | `test_newest_items_have_full_text_and_all_have_descriptions` |
| 7 | 4 dead links/assets in Jogger posts | Leftovers of the pre-page-bundle URL scheme (`/2014/09/...`, `/2018/08/...`), a `../../../images/...` path to an image that is a page resource, and a source-file link (`spotkaj-dyskutanta/index.md`) | `test_internal_links_and_assets_resolve` |

Bugs 2 and 3 share a cause: `music/single.html` assumes every page that uses
it is a release.

## Related structural change

`/apps/` was a standalone page (`content/apps.md` with `layout: apps`), so it
was neither a section nor able to have a feed, and it was the one top-level
entry that did not follow the section pattern. It moves to
`content/apps/_index.md` so it is a real section. It stays HTML-only (no RSS
output): the app update posts live in per-app sections (e.g. `/ego-destroyer/`)
that have their own feeds, so an `/apps/` feed would be empty.

## Not bugs (decisions recorded)

- `/music/performances/` sets its own `og:title` ("Performances by Maciej
  Bliziński") on purpose, so the title-equals-`<title>` check only applies to
  taxonomy pages (`/genres/*`, `/tags/*`), where it matters (c169259).
- Sitemap, `robots.txt`, aliases (at least 90 redirect pages), fingerprinted
  CSS, `lang="pl"` on Jogger and BlogPosting language all passed on the first
  run.

## Fix log

All items below verified by a clean run of `util/test_site_expectations.py`
(27 tests, all passing).

1. **JSON-LD (bug 1).** `jsonld/app-fields.html` now emits its `jsonify`
   values with `safeHTML` (it is rendered in HTML text context, where
   `safeJS` was itself escaped), and `apps.html` / `app-single.html` pass the
   partial's output through `safeJS` so Hugo does not re-escape it inside the
   `<script>` block.
2. **Performances page (bugs 2, 3).** `music/single.html` now applies its
   `music.song` head tags and the share-button script only when the page is
   under `/music/releases/`; other pages using the layout get the default og
   partial and no script.
3. **Home og:image (bug 4).** `content/_index.md` `image:` is now the full
   static path (`bio/images/maciej_on_bass_360px.jpg`). The two templates that
   prefixed `bio/images/` themselves (`index.html` hero, `jsonld/person.html`)
   now use the value as given. Previously the default og partial resolved the
   bare filename against the site root.
4. **Jogger feed (bug 5).** `rss.xml` uses `RegularPagesRecursive` for
   sections (the home feed keeps `Site.RegularPages`, which is already
   site-wide). Side effect: the `/music/` feed now also includes the release
   pages, which is what a music feed should contain.
5. **Empty feed items (bug 6).** `excludeFromRSS: true` added to
   `/music/spotify`, `/music/apple`, `/music/youtube` and `/music/credits`
   (generated listings with no body text).
6. **Dead links (bug 7).** Four Jogger posts now use page-bundle relative
   paths (`wlazl-kotek-na-plotek.png`, `wezel-ratowniczy-wiazanie.gif/.webm`,
   `sloneczniki-we-francji.jpg`) and a `relref` for the `spotkaj-dyskutanta`
   post.
7. **`/apps/` is a section.** `content/apps.md` moved to
   `content/apps/_index.md` (URL unchanged), `layout: apps` kept, and
   `outputs: [html]` set so no empty feed is generated or advertised.
