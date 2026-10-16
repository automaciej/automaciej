# RSS feed cleanup

Date: 2026-10-16

## Audit findings (home feed, `/index.xml`)

Built with Hugo and parsed the feed. The home feed lists every regular page
except Jogger and pages marked `excludeFromRSS: true`, so static pages leak in:

| Entry | Problem |
|-------|---------|
| Performances | No `date`, so `pubDate` is `01 Jan 0001`; the description is 38 KB of escaped `<div>`/`<script>` + JSON dump |
| Photos | 2022 page that is only figure markup |
| Press | 2022 static EPK page, 6.9 KB of embed markup |
| Bio | 2022 static page |
| Meu nome | Portuguese post outside `/jogger/`, breaks language separation |
| (`music/report.md`) | `draft: true`; not in production builds but shows up with `-D` |

Template problem: 16 items carry an `<image>` element built as
`BaseURL + .Params.image`. Release front matter holds a bare filename
(`image: loser.jpg`), giving `https://blizin.ski/loser.jpg`, which 404s because
the image is a page resource. `<image>` is also not valid inside an RSS 2.0
`<item>`.

## Plan

1. Add `excludeFromRSS: true` to `content/music/performances.md`,
   `content/photos.md`, `content/press.md`, `content/bio/index.md` and
   `content/music/report.md`.
2. Move `content/meu-nome.md` to `content/jogger/meu-nome.md`. Jogger
   permalinks are `/jogger/:year/:contentbasename/`, so the new URL is
   `/jogger/2016/meu-nome/`. Keep the old URL working with
   `aliases: ["/meu-nome/"]`.
3. In `layouts/_default/rss.xml`, replace the item-level `<image>` with
   `<media:content medium="image">` (declaring the `media` namespace). The URL
   is resolved from the page resource named by `image`, or from a resource
   matching `**.jpg`; a static-path image (e.g. `/images/...`) is resolved
   against the site root; if nothing resolves, no element is emitted. No
   `<enclosure>`, because it requires a byte length that Hugo cannot supply.
4. Add tests to `util/test_site_expectations.py`:
   - no home-feed item has a year-0001 `pubDate`;
   - the home feed does not contain Performances, Photos, Press, Bio;
   - every feed's `media:content` URL resolves to a file in the build;
   - `/meu-nome/` still exists (redirect) and points to the new Jogger URL.
5. Run `python3 util/test_site_expectations.py`, re-inspect the generated
   feeds, review `git diff`, and commit.

## Implementation log (append-only)

Entries are added at the end; earlier entries are never edited.

- 2026-10-16: Plan written. No code changed yet.
- 2026-10-16: Step 1 done: `excludeFromRSS: true` added to performances, photos, press, bio, report.
- 2026-10-16: Step 2 done: `git mv content/meu-nome.md content/jogger/meu-nome.md`, added `aliases: [/meu-nome/]`.
- 2026-10-16: Step 3 edited `layouts/_default/rss.xml`: item `<image>` replaced with `<media:content>`, `media` namespace declared. Not yet built.
- 2026-10-16: Step 3 built: home/music feeds have 15 resolving media:content URLs, no junk items; /meu-nome/ redirects to /jogger/2016/meu-nome/.
- 2026-10-16: Step 4: added 3 tests to TestFeeds in util/test_site_expectations.py.
- 2026-10-16: Step 5: full test suite passes (36 tests); diff reviewed; committed.
- 2026-10-16: Added tag `portugalski` (alongside `języki`) to meu-nome, jak-sie-ucze-portugalskiego(+komentarze), portugalski-lekcja-1, portugalski-lekcja-trzecia. Porta dos Fundos series left untouched.
- 2026-10-16: Added tag `portugalski` (no `języki`) to the Porta dos Fundos series: _index.md and 8 posts.
- 2026-10-16: Found while re-checking other feeds: Jogger post zasypiam-na-wykladach had an empty feed description (leading <!--more--> made the summary empty). Removed the marker; added /jogger/ to the empty-description feed test. Taxonomy feeds (/genres/index.xml, /tags/index.xml) still open.
- 2026-10-16: Requested: every index.xml must be advertised by a `<link rel="alternate">` in its HTML page. Removed the taxonomy exclusion in `layouts/partials/head.html` (`/genres/` and `/tags/` were the only gaps; the 7 non-ASCII tag pages were fine, their href is percent-encoded). Replaced `test_genres_index_has_no_feed_but_genre_pages_do` with `test_genre_pages_and_overview_advertise_a_feed` and added `test_every_index_xml_is_advertised_by_its_html_page`.
- 2026-10-16: Correction: the tag rendered `type="application/rss&#43;xml"` because `.MediaType.Type` is HTML-escaped by Hugo. A browser decodes it, but it is not what feed-discovery tools and the user expect. The type is now the literal `application/rss+xml` in `head.html`; added `test_feed_link_type_is_not_html_escaped`, which checks only the alternate `<link>` tags (the SRI `integrity` attribute legitimately contains `&#43;`).
- 2026-10-16: Taxonomy feeds (`/genres/`, `/tags/`) still list term pages with empty item descriptions; they are now advertised, so this is no longer an orphan problem. Open.
- 2026-10-16: Taxonomy overview feeds (/genres/, /tags/): term items now get a generated description in rss.xml ("Posts tagged X from Site" for tags, "Releases in the X genre from Site" for genres; front-matter description wins if set). Added both feeds to the empty-description test. Nothing left open from the audit except deployment.
- 2026-10-16: Requested: per-service feeds (`/music/apple/`, `/music/spotify/`, `/music/youtube/`), e.g. a reader with Apple Music wants new releases from me. Plan: `outputs: [html, rss]` in the three page front matters; new `themes/multi-stream/layouts/music/streaming.rss.xml` built on `partials/streaming-items.html` (same items as the page: per-track where track IDs exist, else per-release; future/draft/artist-only skipped). Item `<link>` is the release page on the site, `<guid isPermaLink="false">` is release permalink + `#<service_key>-<n>`-style fragment unique per item, description carries artist, date and a "Listen on <service>" link to the service URL, `media:content` is the release cover. Tests: feeds exist, are advertised, item count equals the page's list length, every description links to the service. Then update CLAUDE.md.
- 2026-10-16: Built per-service feeds (/music/apple|spotify|youtube/index.xml): streaming.rss.xml + outputs [html, rss]; item counts match the pages (11/12/11); autodiscovery links appear via head.html. History check: these pages (created 2026-10-05, 3c0f4cc) never had an RSS output; the only earlier trace was /music/apple/ etc. appearing as empty items in the home and /music/ feeds, fixed by excludeFromRSS in 7aa2f46 (2026-10-06). Also fixed pre-existing double-escaped copyright (&amp;copy;) in all feeds via htmlUnescape. Tests: test_service_feeds_mirror_their_pages, test_feed_copyright_is_not_double_escaped; service feeds added to FEED_SECTIONS. CLAUDE.md updated.
