# Site-wide audit: OpenGraph/Twitter tags, JSON-LD, broken links

Date: 2026-09-16

## Fixed in this session

1. **Blog posts had zero OpenGraph/Twitter tags.** Only `music/single.html`
   had any (via the theme's `head_extra` block). Added a sitewide default
   (`layouts/partials/og-tags-default.html`), wired into
   `themes/multi-stream/layouts/_default/baseof.html`'s `head_extra` block
   default. Every page now gets og:type/title/description/url/site_name/image
   and twitter:card/title/description/image unless a template overrides the
   `head_extra` block (music pages still do, for `music.song`-specific tags).
2. **`<title>` on blog posts read "Article Title - Blog"**, which is boring.
   Blog section now renders just the article title (`layouts/partials/head.html`).
3. **Bug introduced then fixed within this session:** my first attempt put the
   default og/twitter tags directly in `head.html`, which runs for every page
   including music pages that already define their own via `head_extra` —
   resulted in duplicate `<meta>` tags on all 23 release pages, project pages,
   and the performances page. Fixed by moving the default tags into the
   `head_extra` block's default slot instead, so the theme's existing
   override mechanism handles it with no duplication and no reimplementation.

## Other findings (not fixed — flagging for a decision)

### JSON-LD gaps

- **`content/blog/*` gets no article-level structured data.** Jogger posts
  get `BlogPosting` schema via `rich-data-single.html`, but the condition in
  `head.html` only checks `.Section "jogger"`, not `.Section "blog"`. Blog
  posts get breadcrumb JSON-LD only.
- **Individual app pages (e.g. `/ego-destroyer/`) have no `SoftwareApplication`
  schema of their own** — only breadcrumb. The `ItemList` of all apps lives
  solely on `/apps/`.
- **`layouts/partials/jsonld/music-list.html` appears to be dead code** — no
  template references it.

### Content/title oddity

- `/music/projects/maciej/index.html` renders `og:title` as the site name
  ("Maciej Bliziński") instead of a real project title — its `.Title` appears
  to resolve empty. Pre-existing, unrelated to the og-tags work.

### Broken links

- **`/task-compass/` is linked from the main nav on every page (246
  references) but no content exists for it** (`content/task-compass/` is
  absent, no template matches it). Dead link site-wide.
- **`/2009/02/26/wrodzone-uzdolnienia/`** referenced from
  `jogger/2009/jak-niewidomemu-wykazac-istnienie-fotografii/` — target page
  does not exist in the build.
- **`/2016/10/portugalski-lekcja-trzecia/portugalski-lekcja-trzecia.mp3`**
  referenced twice from `jogger/2016/portugalski-lekcja-trzecia/` — audio
  file missing from output.

(Percent-encoded Polish-tag/jogger-slug hrefs like `/tags/%C5%BCe-jak/` were
checked and are false positives of the link-scan script — the decoded paths
exist on disk.)

## Implementation log (append-only)

All items from "Other findings" above, fixed:

- **Blog BlogPosting JSON-LD**: extended `head.html`'s condition from
  `.Section "jogger"` to `(in (slice "jogger" "blog") .Section)`, so both
  sections route through `rich-data-single.html`.
  - That partial hardcoded `"inLanguage": Polish` and a Polish fallback
    description ("Wpis na blogu Automacieja") — correct for Jogger but wrong
    for the English blog. Branched both on `.Section` so blog posts get
    English/`en` and Jogger keeps Polish/`pl`.
  - **Course correction**: first attempt wrote
    `{{ with .Description }}...{{ else if eq .Section "jogger" }}...{{ end }}`.
    Build failed: `unexpected <if> in input` — Go's `with` action does not
    support `else if` chaining (only `if`/`range` do). Rewrote as a plain
    `{{ if .Description }}...{{ else if ... }}...{{ end }}`. Rebuilt clean.

- **App single pages had no SoftwareApplication schema**: rather than writing
  a second, separate JSON-LD block, factored the per-app field list already
  used by `jsonld/apps.html`'s `ItemList` into a new shared partial
  `jsonld/app-fields.html` (name/description/category/platforms/url/
  installUrl/license/author). `jsonld/apps.html` now calls it per list item;
  new `jsonld/app-single.html` wraps the same fields in a top-level
  `SoftwareApplication` object for a single app page. Wired into `head.html`
  via `else if .Params.app` (same front-matter key `_default/list.html`
  already uses to look up `hugo.Data.apps`, so no new convention introduced).
  Verified on `/ego-destroyer/`.

- **Dead code**: deleted unused `layouts/partials/jsonld/music-list.html` —
  confirmed with a repo-wide grep that nothing referenced it.

- **`/music/projects/maciej/` og:title "bug"**: investigated, not a bug.
  `content/music/projects/maciej/_index.md` sets `title: "Maciej Bliziński"`
  deliberately (it's the author's own project). It happens to match
  `Site.Title`, which is what looked wrong in the original report. No change.

- **`/task-compass/` dead nav link (246 refs)**: `content/task-compass/`
  was never built, but `data/apps/task_compass.toml` has a real
  `app_site = "https://task-compass.app"`. Repointed both the hardcoded nav
  link (`themes/multi-stream/layouts/partials/header.html`) and the same
  dangling reference in `config.toml`
  (`params.links.list1.link` "Task Compass" entry) to that external URL.
  - Side note found while tracing this: `params.links.list1` (the config.toml
    block the Task Compass ref lived in) isn't rendered by any current
    template — grepped all layouts, nothing reads `params.links`. Left the
    config entry in place (now pointing somewhere valid) rather than deleting
    it, since removing unused-but-not-broken config wasn't part of the ask.

- **`/2009/02/26/wrodzone-uzdolnienia/` dead link**: traced via
  `git log --all --diff-filter=D` — the target post was intentionally
  deleted in commit `5c18b94` ("Usunięcie postów które nie mają większej
  wartości" — removal of low-value posts). Restoring it would contradict
  that decision, so instead unlinked the phrase in
  `content/jogger/jak-niewidomemu-wykazac-istnienie-fotografii.md`, keeping
  the sentence as plain text instead of a link to nowhere.

- **Missing mp3 on `/jogger/2016/portugalski-lekcja-trzecia/`**: the file
  was never missing from the build — it's a page-bundle resource and gets
  copied to the page's actual permalink,
  `/jogger/2016/portugalski-lekcja-trzecia/portugalski-lekcja-trzecia.mp3`.
  The markdown link still used the pre-migration URL shape
  (`/2016/10/portugalski-lekcja-trzecia/...`, from before the "Use year in
  the blog URLs" restructuring). Updated the link in
  `content/jogger/portugalski-lekcja-trzecia/index.md` to the current
  permalink path. Verified the file exists at that path in `public/` after
  rebuild.

All fixes verified with a full `hugo --cleanDestinationDir` rebuild (293
pages, zero errors) plus targeted greps against `public/` for each item.

---

# Audit: social tags in the /music section

Date: 2026-10-15

Scope: OpenGraph/Twitter tags on `/music/` and everything below it, read from a
fresh `hugo` build.

## Findings

1. **`/music/` has a junk description.** Front matter has `description: ""`,
   so the tags fall back to `.Summary`, which is a run-on dump of the body
   ("Music Production Selected Productions To Promenade by emily jane (June
   2025) Je te veux by Zoe Hayter ...").
   - Correction to the first read of this: the body of `content/music/_index.md`
     is stale (stops at 2025, 13 productions vs 26 releases) but is **not
     rendered**: `music/list.html` draws live release cards. It only leaks into
     the description via `.Summary`, so the fix is a real description, not a
     body rewrite.
2. **`/music/releases/`, `/music/projects/`, `/music/performances/` use the
   site-wide tagline** ("Dublin-based musician and software engineer.") as
   description. No `description` in their front matter.
3. **Inconsistent title suffixes.** `/music/releases/` and `/music/projects/`
   end in "- Maciej Bliziński"; `/music/credits/` and `/music/performances/`
   end in "- Music Production".
4. **Album releases are tagged `og:type=music.song`** (Libera, Tentativa),
   although the JSON-LD already switches between `MusicAlbum` and
   `MusicRecording` on `single`.
5. **Generic image on release pages.** Releases without a cover or YouTube
   video (Burza, Ocean, Butterfly, the Regional Massapê tracks, the guitar
   duo session) fall back to the site `shareImage` portrait and are tagged
   `summary_large_image`.
   - Already handled before this entry: the site-logo fallback in
     `og-tags-default.html` was removed in `d504d99`, so the index-style pages
     emit no image and `twitter:card=summary`.
6. **`og:type=article` on non-article pages** (`/music/credits/`,
   `/music/performances/`, `/music/spotify|apple|youtube/`).
7. **No `og:image:width`/`height`/`alt`** on pages whose image is a local
   resource.

Policy decided with this entry: the site-wide image is served only on the
homepage. Every other page emits `og:image` only for an entry-specific or
section-specific image.

## Implementation log

1. **`/music/` description**: set a real `description` in
   `content/music/_index.md`. The stale body was left alone (not rendered).
2. **Section descriptions**: added `description` to `music/projects/_index.md`
   and `music/performances.md` (a `music/releases/_index.md` description was
   dropped when upstream moved releases to `/music/<slug>/` and deleted that
   page). `music/list.html` also prints `description` under the heading, so
   `/music/` now shows that line too.
3. **Titles**: `partials/page-title.html` now suffixes sections below `/music/`
   with their parent section ("Projects - Music Production",
   "Arthur's Jazz Jam - Projects"), matching what pages already did.
   `/music/` itself keeps "- Maciej Bliziński".
   Follow-up (2026-10-16): release pages (anything with `release_date`) render
   just the release title, with no suffix, like blog posts.
4. **og:type music.album**: release pages use `music.album`/`MusicAlbum` only
   when front matter has `single: false`. First attempt used
   `cond .Params.single`, which tagged the 10 old single recordings (no
   `single` key) as albums too. Added `single: false` to Libera, Tentativa and
   To Promenade, the only real albums, and made the JSON-LD `@type` use the
   same rule (old recordings are now `MusicRecording` there as well).
5. **Generic image**: release pages no longer use `params.shareImage` for
   `og:image`/`twitter:image` and send `twitter:card=summary` when they have no
   cover or YouTube thumbnail. The JSON-LD `image` keeps the fallback, since
   `test_release_pages_have_jsonld_image` requires it.
6. **og:type article**: `og-tags-default.html` uses `article` only for dated
   pages; credits, performances and the per-service lists are `website`.
7. **Image size/alt**: `og:image:width`/`height` for local images (default
   partial and release pages), `og:image:alt` ("Cover art for ...") on releases.

Tests: new `TestMusicSocialTags` in `util/test_site_expectations.py`. Rebased
onto upstream's `/music/<slug>/` move (release tests use the new URLs). Full
suite passes.

Not done: `/music/` and the other section pages have no section-specific
image, so they emit none, per the policy above.
