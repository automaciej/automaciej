# Primary role: original, production or engineering

Date: 2026-11-09

`/music/` lists music Maciej co-created, plus work that was mainly recording or mixing
someone else's music (e.g. Level Design by 8-bit Funk), in one flat list with URLs unchanged.
Each release has a primary role, one of:

- `original`: he wrote or co-wrote the music. Computed when his own credits (release or track
  level) include `songwriter`, `composer`, `music` or `lyrics`.
- `production`: the default.
- `engineering`: mainly recorded or mixed. Only ever set by hand, because mixing and recording
  credits also appear on productions.

Front matter `primary_role` overrides the computed value (Hope Is the One sets `original` by hand;
the engineering releases set `engineering`). This is not `composition_origin`, which says whether the
piece is an original, a cover or a standard, whoever wrote it.

- `partials/release-primary-role.html` resolves the role; `partials/release-role-pages.html`
  returns the releases with a given role.
- Cards (`partials/music-preview-card.html`) end with a coloured `.music-preview-role` strip
  reading "Original", "Production" or "Engineering"; it is shown from 1024px up only.
  Two visual levels: Original is a solid accent fill; Production and Engineering share the same
  light accent tint (an engineering-specific grey was too dim).
- `/music/engineering/` and `/music/originals/` (`content/music/<name>.md`, `layout: role-list`,
  front matter `role`) are filtered lists, each with its own feed (`index.xml`). All releases also
  stay in `/music/`, the homepage preview and `/music/index.xml`.
- `/music/` no longer shows a visible header (a visually hidden `<h1>Music</h1>` stays for
  accessibility); the section title is "Music", not "Music Production".
- Current engineering releases: Level Design, Libera, Tentativa, Little Bird (Cormac Murphy's
  jig), Run for Me, To Promenade.

## Release page: one button, no second set of listen links

Every service icon above the title is a listen link, so nothing below repeats them. A release with a
`links.streaming` (HyperFollow) link gets one `.release-button` in the header, after the date: "Listen now",
or "Pre-save" while the article has `.is-unreleased` (set by `unreleased.js`; without JS it reads
"Listen now"). It replaces the old `presave-button`. The block below the description
(`partials/music-playback.html`) holds only tracks: an album (`single: false`) gets a plain numbered list
(`music-playback-album.html`); any other release with tracks keeps per-track credits and links
(`music-playback-tracks.html`).
