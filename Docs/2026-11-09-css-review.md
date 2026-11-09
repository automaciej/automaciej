# CSS review: structure, tokens, dead and overridden rules

**Date**: 2026-11-09
**Scope**: `themes/multi-stream/assets/css/main.css` (2884 lines, the only stylesheet the site links
besides the vendored `static/css/lineicons.css`), and `static/css/bio.css` (104 lines).
**Method**: read the whole file, then checked class usage against every template, JS file,
content file and data file; counted repeated values; checked which `var(--x)` have a definition.
Line numbers refer to `main.css` as of commit `01c01d0`. Nothing was changed.

## Summary

The structure is better than most hand-written stylesheets of this size: grouped by component, with each
component's responsive rules directly under its base rule, and `TestCssStructure` guarding that.
The weak spot is the **value layer**. There are almost no tokens besides colours, so the same radius, padding,
gap, shadow and font size are retyped dozens of times, and the "phones use `--gutter`" rule is
re-declared in seven separate media blocks. Behind that sit a handful of real bugs, mostly Pico-era
leftovers, and a fair amount of dead or self-cancelling CSS.

Ordered by value for effort:

1. Fix the real bugs (section 1). Small, and they change what users see.
2. Delete dead CSS (section 2). Zero visual risk.
3. Add the missing tokens and a card primitive (sections 4 and 5). This is the refactor that makes the site more consistent.
4. Clean up the override-and-undo patterns (section 3), then the breakpoint strategy (section 6).

## 1. Bugs and likely bugs

**1.1 Undefined variables from the old Pico theme: `--secondary` (10 uses) and `--muted-border-color` (5 uses).**
Neither is defined anywhere. `var(--secondary)` has no fallback, so `color` computes to `inherit`
and the "secondary" text is simply the primary colour. Affected: `.performances-simple-table`
`.perf-date`/`.perf-venue` (2313, 2323), `.credits-role-single` and `.credits-role summary` (2401, 2408),
`.report-meta`, `.report-count`, `.report-detail-label`, `.report-perf-venue`/`-details`, and the
`.report-section h2` border (2492).
The `--muted-border-color` uses fall back to hard-coded light greys (`#e0e0e0`, `#ddd`, `#eee`), which are
**bright lines on the black dark-mode page** (2307, 2526, 2557, 2567, 2609).
Fix: replace `--secondary` with `--text-secondary` and `--muted-border-color` with `--border-color`.
This visibly changes those pages (secondary text becomes grey, as presumably intended).

**1.2 `.app-post-preview` has no CSS at all.** The homepage Apps column renders update posts as
`<article class="app-post-preview">` (`index.html:78`), but every card rule targets `.app-preview`.
These entries get no background, padding or radius, and their `h3` gets browser-default size instead of
the 1.25rem "card title" (line 324). If that is intentional (plain text entries between cards) it deserves a
comment. If not, it is a missing-class bug. Check it on the live homepage.

**1.3 Hard-coded accent in the priority-task shadow.** `rgba(0, 113, 227, 0.2)` (1438) is the light-mode
`--accent`; in dark mode the accent is `#2997ff`, so the glow is the wrong colour. Use
`color-mix(in srgb, var(--accent) 20%, transparent)`.

**1.4 `.music-report` ignores the font tokens** (`font-family: Georgia, "Times New Roman", serif`, 2442) where
`--font-serif` exists. Also, the whole `/music/report/` section assumes a white page: `#000` in print is fine, but
the on-screen colours rely on the broken variables from 1.1.

**1.5 `bio.css` is not linked from anywhere** (`head.html` loads only `lineicons.css` and `main.css`; no other reference).
It is a Pico-theme remnant: it sets `--primary`, targets `header > nav > div`, `#TableOfContents`, `.iframe-container`, `.portrait`,
`.responsive-iframe`, `main.bio`. Delete it. (Check whether any content uses `.portrait` or `#TableOfContents`; if so, move
those rules into `main.css` first. The unlinked file means they are not styled today either.)

**1.6 Possible double spacing in the blog list.** `.post-card` has `margin-bottom: 1rem` (1244) inside `.posts-list`,
a grid that already has `gap: 1rem` (1223). On wide screens the rows are 2rem apart, but on phones the card margin is
zeroed so the gap is `--gutter`. Verify visually whether the 2rem is intended. If the gap is meant to
be the only spacing, remove the margin. The same applies to `.blog-post-preview` (a margin, where music/apps
use a flex `gap`; see 3.6).

**1.7 Stale comments that describe behaviour that no longer exists.**
Line 656 says the role label is "hidden by default (tablets)", and line 723 says "tablet: thumbnail beside the text".
But the `≥768px` block (769-800) shows the strip for every width from 768 up, and no tablet layout exists in the CSS.
The Docs describe three breakpoints; the CSS has effectively two (see section 6).

## 2. Dead CSS (safe to delete)

Verified by exact-token search over layouts, theme layouts, JS, content and data:

| Selector | Lines | Why dead |
|---|---|---|
| `.app-download-banner` and its `a`, `.download-text`, `.download-caption`, `.app-card .app-download-banner/-link`, the `z-index: 2` rule | 1528-1531, 1556-1558, 1566-1595 | Not in any template since apps moved to content bundles (`01c01d0`). Also the only other use of `#28A745` besides `.testflight-banner`. |
| `.app-preview .app-type` | 867-871 | Markup uses `.app-category`, never `.app-type` |
| `.app-preview h3 a`, `.app-preview h3 a:hover` | 817-820, 862-865 | The app card's `h3` contains no `<a>` (stretched link is used) |
| `.music-preview h3 a`, `:hover` | 513-520 | Same: the card title is a plain `h3.card-row-title` |
| `.music-preview-artist, .music-preview-details { white-space; overflow; text-overflow }` | 526-531 | Exactly repeated by `.card-row .card-row-meta` (377-384), which both elements carry. Keep only the `font-weight`/`color` rules. |
| `.music-preview h3 { font-size: 1.25rem; margin: 0 }` | 324-330 | Every card `h3` is `.card-row-title`; `.card-row .card-row-title` (0,2,0) overrides it on phones, and `.music-preview .card-row-title` does at ≥768. Only `.blog-post-preview h3` and `.post-card-content h3` still need the group. |
| `.stream-content { /* Removed background */ }` | 476-478 | Empty rule |
| `.blog-posts-list img { }` | 1360-1361 | Empty rule |
| `.blog-post-preview:last-of-type { margin-bottom: 1rem }` | 844-846 | Identical to the base rule |
| `.blog-posts-list .post-card:hover { box-shadow … }` inside the phone media block | 1372-1374 | The hover ring only exists at `min-width: 768px`, so this phone-only reset overrides nothing |
| `.blog-posts-list .post-card .post-meta, .post-description { display: block }` (phones) | 1376-1379 | Only needed to undo `.post-card .post-description { display:none }` (1349); see 3.1 |
| `.service-icon-outline` / `.service-icon-glow` | 602-608 | *Not dead*: the class is built by `service-icon.html` (`service-icon-<effect>`). Listed only because a plain search flags them. Same for `.music-preview-role-<role>`. |
| `.music-preview { align-items: normal; gap: normal }` at ≥768 | 729-730 | The card is `display: block` there, so flex properties do nothing |
| `.music-preview-image img { flex-shrink: 1 }` at ≥768 | 741 | Its parent is `display: block`, so the image is not a flex item |
| `.view-all-link-mobile/-desktop` `!important` | 898, 902 | Same specificity as the base rules and later in the file, so source order alone wins. Drop both `!important`s. |
| `@media print` rule `nav, … { display: none !important }` | 2846 | `!important` is only needed if something later sets `display`; test, then drop |
| Theme `themes/multi-stream/layouts/partials/head.html` | n/a | Shadowed by the project's `layouts/partials/head.html`, so it is never used (and it has already drifted: no fingerprinting, no JSON-LD). Delete to avoid editing the wrong copy. |

Estimated reduction: roughly 120-150 lines, with no visual change.

## 3. Overrides that cancel each other (set high, undone lower)

These are the "higher level defines it, the lower level always overrides it" cases you asked about.

**3.1 `.post-card` phone block vs `.blog-posts-list .post-card` (1337-1380).** The phone rule strips
`background`, `padding`, `margin` and hides `.post-description`. Two rules later, `.blog-posts-list .post-card`
restores `background`, `padding`, `border-radius`, `margin`, `border-bottom: none` and shows meta/description again.
The strip rule is only "live" for the other `.post-card` users (`_default/list.html`, `_default/app.html`). Make the
two behaviours explicit instead: either `.post-card--plain` for the stripped phone variant, or put the strip rule under
`:not(.blog-posts-list) > .post-card`. Then the blog list needs no restore block at all. Same for `border-bottom: none`:
nothing sets a bottom border on `.post-card`, so the reset is meaningless.

**3.2 `.card-row` (345-394) vs `.music-preview` at ≥768 (726-764).** `music-preview` opts into `card-row` in markup, then 40 lines
reset it from 768px (`display`, `padding`, `overflow`, margin of the art, `object-fit`, `white-space`, `font-size`…). The
card-row layout is therefore the *phone-only* layout of this card, while its CSS declares it unconditional.
Option A: make `.card-row` mobile-first and have the base rules apply only `max-width: 767px` for `music-preview`.
Option B, cleaner: keep `.card-row` for `.project-card` (a genuine row at all widths) and give `.music-preview` its own two
layouts (row on phones, stacked ≥768) via a modifier such as `.card-row--phone`, so the undo block disappears.

**3.3 Heading margins.** Global `h1…h6 { margin-top: 1rem; margin-bottom: .5rem }` (314-319) is undone with `margin-top: 0` in six
places (`.stream-column h2`, `.music-header h2`, `.music-release-header h1`, …) and by `margin: 0` on titles. Either let
headings be `margin-top: 0` and add spacing via a flow utility (`* + h2`) / `.prose` wrapper, or accept the global
margin and stop resetting it per component. Today every new heading needs a decision.

**3.4 List reset repeated 12 times.** `main ul, main ol, .stream-content ul … { padding-left: 1.5rem }` (947-954) is a *global* list
style for all of `main`. Each component that wants a clean list then re-declares `list-style: none; margin: 0; padding: 0`
(`.social ul`, `.credits-toc ul`, `.music-credits ul`, `.music-releases-years`, `.music-releases-chips`, `.genres-grid`,
`.genre-card-examples`, `.streaming-list`, `.music-project-page section ul`, …). Scope the prose list style to prose
containers (`.post-content`, `.section-intro`, `.bio-summary`; the first two already have their own copies at 1110-1118 and 1629-1633, so the
`main ul` one is the surplus) and the 12 resets mostly vanish.

**3.5 `.container` is capped at 1200px and then un-capped in five places**: `.site-header/.site-footer > .container` (286),
`.streams > .container` (440), `.list-page-wide > .container` (1503), `.music-page-wide > .container` (1702). The default is the
exception. Invert it: `.container` fluid with `--page-pad`, and `.container--narrow`/`-- capped` where a cap is wanted. Or at
least, add one `.container-wide` class and use it in these four templates.

**3.6 Spacing between cards is expressed three ways**: flex `gap` (`.stream-content`), grid `gap` (`.posts-list`, `.apps-list`,
`.projects-grid`, `.genres-grid`, `.music-productions`), and `margin-bottom` on the card (`.blog-post-preview`,
`.post-card`, `.contact`). The file's own comment (480-487) explains why gap is right. Move `.blog-post-preview` into a flex `gap`
container and delete the margins and their phone overrides (848-855, 1229-1237).

**3.7 `.card-shadow` rule list (1261-1267 and 1279-1286).** `.post-card, .genre-card, .project-card` "bake in" the shadow
under their own name while `.card-shadow` is added in markup elsewhere. Add `class="card-shadow"` to those three templates and
reduce both rules to `.card-shadow`. The hover-reset for the blog list (1310) then becomes simply "don't add `card-shadow`".

## 4. Repeated values that should be tokens

Counts are occurrences in `main.css`.

| Value | Count | Proposed token |
|---|---|---|
| `border-radius: 12px` (+ `12px 12px 0 0`, `0 0 12px 12px`) | 18 (+3) | `--radius-card: 12px` |
| `border-radius: 8px` | 9 | `--radius-md: 8px` |
| `border-radius: 4px` | 5 | `--radius-sm: 4px` |
| `border-radius: 999px` | 4 | `--radius-pill` |
| `padding: 1.25rem` (card padding), plus `1.5rem` ×4 and `1rem` | ≥10 | `--card-pad` (1.25rem), with `--card-pad-lg` if the 1.5rem variants are real |
| `20px` page padding (container, streams, header calc, `streams` top) | 4 | `--page-pad: 20px` |
| `1rem` / `2rem` card gaps, and the phone `--gutter` override | 1rem ×9, 2rem ×6, `--gutter` gaps ×7 | `--card-gap` (see below) |
| `box-shadow: 0 2px 8px rgba(0,0,0,.08)` | 3 | `--shadow-card` |
| `rgba(255,255,255,.3)` + `rgba(255,255,255,.25)` glow | 2 pairs | `--glow` (dark only) |
| `#fff` / `#ffffff` / `white` on accent or green | 5 | `--on-accent: #fff` |
| `#28A745` | 2 (1 dead) | `--success` |
| Hover tint `color-mix(in srgb, var(--text-primary) 8%, transparent)` and the accent tints 10 %/12 % | 4 | `--tint-hover`, `--tint-accent` |
| `0.2s` / `0.15s` / `0.3s` transitions | 6 | `--ease: 0.2s` |
| Font sizes in 0.8-0.95rem: 0.8 ×7, 0.85 ×4, 0.875 ×2, 0.88 ×1, 0.9 ×10, 0.95 ×10 | 34 | a type scale: `--text-sm: 0.875rem`, `--text-xs: 0.8rem`, and merge 0.9 / 0.95 (see below) |
| `font-size: 1.25rem`, `1.1rem`, `1.125rem`, `1.05rem`, `1.75rem` | 6, 4, 2, 2, 3 | `--text-lg`, `--text-xl`, `--text-2xl` |

**Type scale.** There are 27 distinct font-size values. Six of them lie within 0.8-0.95rem and are visually
indistinguishable (0.8, 0.85, 0.875, 0.88, 0.9, 0.95). A four-step scale (`0.8`, `0.9`, `1`, `1.125`, `1.25`, `1.75`) covers
almost everything and is the single biggest "consistency for free" change; expect a 1-2 px shift on a few labels.

**The gutter pattern.** Seven blocks read "Phones: the space between cards is `--gutter`" (499, 851, 1230, 1510, 1682, 2201, 2829).
Replace with one token that flips at the breakpoint:

```css
:root            { --card-gap: var(--gutter); --card-gap-lg: var(--gutter); }
@media (min-width: 768px) { :root { --card-gap: 1rem; --card-gap-lg: 2rem; } }
/* each list: */   .posts-list { display: grid; gap: var(--card-gap); }
```

That removes seven media blocks and makes the rule impossible to forget on the next list. The same trick
(`--card-pad`, `--page-pad`, `--header-pad` already does it) works for any value that changes at 768px.

**Token housekeeping.** `--gutter` (a spacing token) sits in the "Light mode" colour block (36); move it with the other
non-colour tokens next to `--font-*`. Add `color-scheme: light dark` to `:root`: form controls, scrollbars and the
canvas then follow the theme (currently only the colour variables flip). `--text-tertiary` is used four times and in dark mode
equals `--text-secondary` in light mode (`#6e6e73`): fine, but name by role if more get added.

## 5. Consistency: a card primitive

At least 13 selectors repeat `background: var(--bg-secondary); border-radius: 12px; padding: 1.25rem` with small variations:
`.music-preview`, `.app-preview`, `.app-card`, `.blog-post-preview`, `.bio-summary`, `.post-card`, `.section-intro`, `.music-card`,
`.music-releases-card`, `.project-card`, `.genre-card`, `.reminder-card`, `.testflight-banner`. Some use `1.25rem`, some `1.5rem`
and one `2rem`, apparently by accident (the `music-card`, 2rem on desktop, is the outlier, and phone-only overrides exist for two of them).
Introduce:

```css
.card { background: var(--bg-secondary); border-radius: var(--radius-card); padding: var(--card-pad); }
.card-shadow { /* existing, shadow + hover ring */ }
```

and add `class="card"` in the templates (or, at minimum, group the selectors in one rule in the tokens section while the markup
is migrated). Component classes then only carry what is specific to them. This is also what the Docs call "card chrome shared
by …"; the CSS currently implements it as a selector list instead of a class.

Other near-duplicates worth merging:

- **Plain link with primary colour, no underline** (`.music-preview h3 a`, `.app-preview h3 a`, `.blog-post-preview h3 a`,
  `.stream-column h2 a`, `.site-title`, `.project-card`, `.genre-card`): one `.link-plain` utility (hover colour as a
  modifier). Today the hover behaviour is inconsistent: music hovers accent, app hovers underline.
- **Pill buttons**: `.release-button` (1906), `.streaming-link a / .listen-links a` (2038), `.presave-chip`, `.release-chip`.
  Three of them are accent pills with `border-radius: 999px; font-weight: 600; color: #fff`. A `.pill` base plus a size modifier would
  halve the code and make hover behaviour uniform (brightness vs opacity vs colour swap today).
- **Section label / meta text**: `.section-label`, `.report-detail-label`, `.report-summary-table th`, `.genre-card-count` repeat
  `uppercase + letter-spacing + small` with 0.04, 0.05 and 0.06em; pick one.
- **Plain separator rows** (`border-bottom: 1px solid var(--border-color)` + last-child reset) appear in `.music-releases-year`,
  `.music-project-page section ul li`, `.credits-person`, `.events-group`, `.toc-block`: one `.rule-list` utility.

## 6. Breakpoint strategy

Counts: `max-width: 767px` ×24, `min-width: 768px` ×11, `min-width: 1024px` ×3. So:

- The Docs say mobile-first, but the file is a **mix**. Components like `.post-card`, `.music-card`, `.genre-card`, `.app-card`
  and `.music-preview` define the *desktop* look in the base rule and patch the phone look in a `max-width` block, then
  sometimes patch back (3.1, 3.2). Pick one direction per component. Mobile-first means phone rules in the base and
  `min-width: 768px` for the rest, which also removes most "undo" declarations.
- **The tablet range does not exist in practice**: nothing is scoped to `768-1023px` (the only `1024px` uses are the
  cover layout, credits columns and the streaming list). The Docs' three-breakpoint table is stale; either document two breakpoints plus
  the 1024px special cases, or add the third where it is wanted.
- Breakpoints appear as magic numbers; `@custom-media` is not baseline-supported, so keep literals, but a one-line comment at the
  top is already there. Consider adding a test that no other width appears (an easy extension of `TestCssStructure`).
- The `sizes` string in `music-preview-card.html` encodes the grid arithmetic (45vw / 30vw / 25vw, 883px / 1175px) and will
  silently go wrong if `minmax(max(260px, …))` (1694) changes; keep the two together by commenting the CSS side, too.

## 7. Smaller observations

- `.post-content` uses `font-size: large` (1052): the only keyword size in the file; use a rem value from the scale.
- `.post-card-image { width: 200px; /* Adjust as needed */ }` and the `max-height: 200px; /* Adjust as needed */` (1358): placeholder
  comments with real values.
- Inline styles remain in `jogger/book.html` (`#666`, `0.6em`), `shortcodes/wide.html` (`background-color: yellow`, looks like a debug
  leftover) and `reminder_comparison.html`: they bypass the tokens and are invisible to dark mode (`#666` on black).
- `.music-report` and `.music-project-page section ul li` and `.credits-*` carry 0.88rem / 0.9rem / 0.95rem variants for the same
  "small body" role: fold into the type scale.
- Dark-mode work is spread over five `@media (prefers-color-scheme: dark)` blocks (aura/glow, share icon, cover backdrop, tokens). That is
  acceptable, since they hold component-specific effects, but give them a shared comment marker so a future theme toggle (`data-theme`) can find them.
- `.nav-toggle span { transition: all 0.3s }` should list the properties (`transform, opacity`).
- `lineicons.css` (2469 lines) is loaded on every page for **five** icons (facebook, github, instagram, linkedin, soundcloud, link: six). Either
  subset it or replace with inline SVGs, which the Bluesky icon already is. The largest single CSS payload on the site is probably this file.

## 8. Suggested order of work

1. **Bug and dead-code pass** (sections 1 and 2). One commit, no design decisions except 1.2 and 1.6, which need a look at the live site.
2. **Tokens pass** (section 4): add the variables, replace values mechanically, with no visual change except the type-scale
   merge, which is a deliberate one. Run the site expectations test; `TestCssStructure` should keep passing.
3. **Card primitive** (section 5) with the three markup changes in 3.7, then the `post-card` and `music-preview` undo blocks (3.1, 3.2).
4. **Container and list scoping** (3.4, 3.5), then the `--card-gap` token (section 4), which deletes seven media blocks.
5. **Breakpoint direction** (section 6) only if you want it; it is the biggest churn and the least urgent.
6. Add tests for what got fixed (CLAUDE.md asks for that when a feature was restored): no `var(--x)` without a definition in `:root` (this would
   have caught 1.1), and no media width other than the canonical set.

## Appendix: checks run

- Class usage: every class selector in `main.css` was matched as an exact token against all `.html`, `.js`, `.md`, `.toml` and `.xml` files under
  `layouts/`, `themes/multi-stream/layouts/`, `content/`, `data/` and the JS directories. The only unmatched names were the
  ones in section 2's first rows, plus names built dynamically in templates (`service-icon-<effect>`, `music-preview-role-<role>`).
- Variable definitions: `grep var(--` against the `:root` definitions: `--secondary` and `--muted-border-color` are never defined.
- Values: counts from `grep -o` over `main.css` for `border-radius`, `font-size`, `box-shadow`, colours and `!important`.
- Not done: no visual regression run and no screenshots, so items marked "verify" (1.2, 1.6, `:is(.music-productions, .stream-columns)` in
  769-800 covering every `.music-preview`) need a look in the browser before acting.

## Resolution (2026-11-09)

Done in the working tree, uncommitted. `main.css` went from 2884 to about 2675 lines (plus a new token
block and card primitives); `static/css/bio.css` (104 lines) and the shadowed theme `head.html` are gone.
`python3 util/test_site_expectations.py` passes (127 tests), including two new `TestCssStructure` tests: every
`var(--x)` is defined, and only 767px/768px/1024px appear in media queries. Nothing was checked visually.

**1 Bugs.** `--secondary` and `--muted-border-color` replaced by `--text-secondary` and `--border-color`
(those pages now show grey secondary text and theme-aware rules). Priority-task shadow uses `color-mix` on
`--accent`. `.music-report` uses `--font-serif`. `bio.css` deleted (no content or template used `.portrait`, `#TableOfContents`,
`.iframe-container`; nothing to move). Theme `head.html` deleted (the project's `layouts/partials/head.html` is the
one Hugo resolves). Stale comments fixed. 1.2: `.app-post-preview` entries are now `.card`s with the card title size
and a plain accent-on-hover title link. 1.6: `.posts-list` had gap and margin stacking, so the card margin was
removed and the gap kept (rows are now 1rem apart on desktop instead of about 2rem on `_default/list.html` and app pages). The
blog list (`.blog-posts-list`) has no gap, only the card margin, so that margin stays (as `--card-gap`).

**2 Dead CSS.** Everything in the table deleted except the dynamically built `service-icon-*` and
`music-preview-role-*` rules. The `view-all-link` and print `!important`s are gone (source order and specificity
suffice); I also removed the one in `.report-details-cell` by raising its specificity.

**3 Overrides.** 3.1: `.post-card` is layout only; the card look is `.card` in the blog list and a `min-width: 768px`
rule for `.posts-list`, so there is no strip-and-restore block. 3.2: only the no-op undo declarations were removed
(flex `align-items`/`gap`, `flex-shrink`, the meta font size); the rest of the 768px undo block stays, because a
phone-only copy of the row rules would cost as many lines, and `.project-card` needs them at every width.
3.3: not restructured. A `* + h2` flow rule would shift the first heading of most pages by 1rem and needs a visual
pass; the convention is now documented above the global rule. 3.4: the global `main ul` indent is a `:where(prose containers)`
rule and the `margin/padding: 0` resets were deleted. 3.5: `.container-wide` replaces the four un-cap rules.
3.6: `.blog-post-preview` lives in a `.stream-cards` flex column (Music, Apps, Blog) and has no margins. 3.7: `.card-shadow`
(shadow and hover ring) was added to the post-card, genre-card and project-card markup; blog cards use the new `.card-shadow-static`.

**4 Tokens.** Added as proposed (radii, `--card-pad`/`--card-pad-lg`, `--page-pad`, `--card-gap`/`--card-gap-lg` with
the 768px flip, `--shadow-card`, `--glow` (dark block), `--on-accent`, `--success`, `--tint-*`, `--ease`, type scale,
`--tracking-caps`), `--gutter` moved next to them, `color-scheme: light dark` on `:root`. The seven "phones use
`--gutter`" media blocks are gone. Type scale: 0.7x-0.95rem folded into `--text-xs` 0.8 / `--text-sm` 0.9;
1.05/1.1/1.125 into `--text-lg`; 1.2/1.3 into `--text-xl`; 1.7 into `--text-2xl`. Letter-spacing of caps labels is one value (0.05em).

**5 Card primitive and merges.** `.card` added to 12 card templates; `.link-plain` (+ `-accent`) used for stream
headings, blog/app post titles, project and genre cards (plain links no longer underline on hover); the accent-pill
base is a grouped rule for `.release-button` and the "Listen on" links (no `.pill` class: their markup has none);
`.rule-list` for the releases-by-year list and the project page list. Not merged: `.credits-person`, `.events-group` and `.toc-block`
(different border colours and sides), and the outlined `.presave-chip` / `.release-chip` (not solid pills).

**6 Smaller items.** `font-size: large` is `--text-lg` (same 18px); placeholder comments removed;
`transition: all` lists `transform, opacity`; inline styles in `book.html` (own stylesheet, a print document that does
not load `main.css`, so classes with literal colours), `wide.html` (`.shortcode-error`) and `reminder_comparison.html` (`.reminders-title`)
moved to classes. `lineicons.css` was left as it is (not subset or replaced), as instructed; it is still the biggest CSS payload.

**7 Breakpoints.** No dedicated conversion; the mobile-first form fell out for the container, streams, header, card gap
and post-card. The theme doc's breakpoint table now says two breakpoints plus the 1024px cases, and its gutter,
token, card and container sections are updated.

**Judgment calls and visual checks needed.** Card padding is now 1.25rem for `.music-card` (was 2rem), `.app-card` and
`.music-releases-card` (were 1.5rem); `.apps-list` gap on desktop is 2rem (was 1.5rem); caps labels moved to 0.05em;
the type-scale merge shifts several labels by 1-2px; `.posts-list` rows are closer; hover underlines on plain links
are gone. Please look at: home (Apps column with update posts, Blog column spacing), `/blog/`, `/apps/` and an app page, a section list page,
`/music/` and a release page, `/music/report/` and `/music/performances/` in dark mode, at phone and desktop widths.
