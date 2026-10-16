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
