# JSON-LD: the music production graph

Music releases, the people who made them and the site owner form one linked graph, built from
stable `@id`s instead of re-declaring nodes on every page.

## Nodes and ids

| Node | `@id` | Declared in full on |
| --- | --- | --- |
| Site owner (`Person`) | `<base>person/#maciej` | home page (`jsonld/person.html`), `/bio/` (`ProfilePage`) |
| `WebSite` | `<base>#website` | home page |
| Release (`MusicRecording` / `MusicAlbum`) | `<release URL>#release` | the release page |
| Other musician (`Person`) | `<base>person/#<anchor>` | `/music/credits/` |

People ids live in one namespace, `<base>person/#<slug>`. Nothing is served at `/person/`: an
`@id` is a name, not an address. Each person's `url` is their section on the credits page
(`/music/credits/#<slug>`), which is where to read about them; if person pages ever exist, only
`url` changes. Only people credited on a release have one; anyone else (for example a project member who
was never credited) is a plain named `Person`.

## Partials (`layouts/partials/jsonld/`)

- `music-release.html` returns the release as a dict. `full=true` (release page only) adds
  description, UPC/ISRC, tracks, service links (`sameAs` + `ListenAction`), `producer`,
  `contributor` (with `roleName`), and `recordingOf` with `composer`/`lyricist`. `full=false`
  is the compact form used in lists: type, id, name, url, artists, date, genre, image.
- `release-list.html` renders an `ItemList` of compact releases.
- `page-releases.html` picks the releases for each page that shows them: home (the 3 shown),
  `/music/`, the per-service pages (`/music/spotify/`, `/music/youtube/`, ...), credits, genre
  pages and project pages. `/bio/` calls `release-list.html` from `music-releases.html`.
- `person-ref.html` builds a person reference (owner id, credits-page id, or plain name);
  `person-links.html` finds the releases a person is artist/producer/contributor on;
  `credits-people.html` is the `ItemList` of people on the credits page.

## Edges, walkable from both sides

- release `byArtist`, `producer`, `contributor`, `recordingOf.composer/lyricist` -> person
- person `@reverse` `byArtist` / `producer` / `contributor` -> release (home page for the owner,
  credits page for everyone else)
- `MusicGroup` (project page) `member` -> person, `album` / `track` -> release `@id`
- release `isPartOf` -> `WebSite`

Roles map from the `credits` front matter: `producer`/`co-producer` -> `producer`;
`music`/`composer`/`songwriter` -> `composer`; `lyrics`/`songwriter` -> `lyricist`.

## Changes worth knowing

- A release's `url` is now its own page; the streaming link is no longer used there (the service
  links are in `sameAs`/`potentialAction`).
- The project page's track list and `VideoObject`s read `hugo.Data.music`, which no longer exists,
  so they were always empty. They now come from the release pages.
- `jsonld_blocks()` in `util/test_site_expectations.py` flattens scripts holding an array.
