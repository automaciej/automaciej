# Release artwork on cards: height never exceeds width

Date: 2026-11-09

Release covers are meant to be square, but a few aren't (11ell 11eaven is 1415x1464, Je Te Veux and
Little Bird are a pixel or two taller than wide, and five older covers are 4:3 landscape). On the
cards the rule is: **the image's height is at most its width.**

- Taller than square: cropped to a square from the centre, so equal amounts come off the top and
  the bottom.
- Square or landscape: only scaled, keeping its proportions (no crop).

It is done by Hugo's image processing, not CSS, so the browser downloads an image that is already
the right shape: `partials/release-art.html` takes `(dict "img" <resource> "width" <px>)` and
returns the webp (`Fill "WxW center"` for tall images, `Resize "Wx"` otherwise). Both card
partials use it: `music-preview-card.html` (`/music/`, the homepage, project pages, role lists;
240/480/800/1200px for the `srcset`) and `music-card.html` (genre pages, 400px). Release pages,
og images and JSON-LD still use the original artwork. A new card that shows a cover should call the
partial rather than `.Resize`.

On phones the card's artwork box is a fixed 120px square and `object-fit: cover` crops a landscape
cover there (see "Card row" in `main.css`).
