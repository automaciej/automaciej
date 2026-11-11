#!/usr/bin/env python3
"""Check that each music service credits a release to the same artists as the site, and write
the findings as a plain-text report that can be pasted into a distributor support request.

The site's `artist:` front matter is the source of truth. For every configured release and every
service the script can read without logging in (Apple Music/iTunes, Spotify, Deezer, YouTube) it
reads which artist(s) the service shows. Qobuz blocks automated page reads, so for Qobuz the
script reads only the artist credit that is part of our own Qobuz link (its URL slug); the report
says so. Each service is judged as:

  ok       every expected artist is credited, each as its own artist
  MERGED   one artist entity bundles several expected artists ("Gaia Marenghi x Maciej Bliziński"
           instead of two collaborating artists)
  MISSING  an expected artist is not credited at all
  ?        the service could not be read (offline, not found)

Exit status is 1 when any service is MERGED or MISSING. Read-only: it only fetches public pages.

Which releases to check lives in util/service_metadata.json ("releases", optional "services" and
"cache_ttl_hours"); slugs given on the command line override the list.

Results are cached per service resource (for example Spotify album ID) in
.cache/service-metadata.json, so a repeat run does not call the services again until the entry is
older than the TTL. Failed lookups are never cached. After you fix something at the distributor,
run with --refresh.

Usage:
    python3 util/check_service_metadata.py                 # the configured releases
    python3 util/check_service_metadata.py loser 11ell-11eaven
    python3 util/check_service_metadata.py --service apple --service spotify
    python3 util/check_service_metadata.py --refresh       # ignore the cache, fetch again
    python3 util/check_service_metadata.py --no-cache      # neither read nor write the cache
"""

import argparse
import datetime
import json
import pathlib
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
MUSIC = REPO / "content" / "music"
CONFIG = pathlib.Path(__file__).resolve().parent / "service_metadata.json"
CACHE = REPO / ".cache" / "service-metadata.json"
CACHE_VERSION = 2
DEFAULT_TTL_HOURS = 24
USER_AGENT = "Mozilla/5.0 (compatible; release-metadata-check)"

OK, MERGED, MISSING, UNKNOWN = "ok", "MERGED", "MISSING", "?"

# Services linked from a release that this tool does not read (login or scraping needed).
UNCHECKED_LINKS = {"tidal": "Tidal", "amazon_music": "Amazon Music",
                   "bandcamp_url": "Bandcamp", "soundcloud_url": "SoundCloud"}


class Fetched:
    """What a service shows for a release.

    credit:   the artist line as displayed ("A & B"), or "" when the service only exposes entities
    entities: names of the separate artist entities the service links the release to
    ids:      the service's ID for each entity, parallel to `entities` ("" when unknown)
    strict:   whether an expected artist missing from entities and credit counts as MISSING
              (False for services that only show one channel per upload, like YouTube)
    source:   "page" for what the service itself returned, "URL slug" for Qobuz
    upc:      the release's UPC when the service exposes it
    """

    def __init__(self, credit="", entities=(), strict=True, ids=(), source="page", upc=""):
        self.credit = credit
        self.entities = list(entities)
        self.ids = list(ids) + [""] * (len(self.entities) - len(ids))
        self.strict = strict
        self.source = source
        self.upc = upc

    def to_json(self):
        return dict(self.__dict__)

    @classmethod
    def from_json(cls, d):
        return cls(d["credit"], d["entities"], d["strict"], d["ids"], d["source"], d["upc"])


# --- Pure logic -------------------------------------------------------------------------------

def norm(name):
    """Casefolded name without diacritics, so "Bliziński" matches "Blizinski"."""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("ł", "l").replace("Ł", "l")
    return re.sub(r"\s+", " ", s).strip().casefold()


def judge(expected, fetched):
    """(status, detail) for the expected artist names against what a service shows."""
    want = [norm(n) for n in expected]
    entities = [norm(n) for n in fetched.entities]
    credit = norm(fetched.credit)
    # An entity naming more than one expected artist is the bundled "A x B" artist.
    for ent, raw in zip(entities, fetched.entities):
        if sum(1 for w in want if w in ent) > 1 and ent not in want:
            return MERGED, raw
    missing = [n for n, w in zip(expected, want) if w not in entities and w not in credit]
    if missing and fetched.strict:
        return MISSING, ", ".join(missing)
    return OK, ""


def qobuz_credit_from_url(url):
    """The artist words in a Qobuz album URL slug, e.g. "loser gaia marenghi amp maciej blizinski".
    Qobuz writes "&" as "amp" and our bundled "x" as "x"."""
    m = re.search(r"/album/([^/]+)/", url or "")
    return m.group(1).replace("-", " ") if m else ""


def parse_front_matter(text):
    """The few keys this tool needs from a release's YAML front matter."""
    if not text.startswith("---"):
        return None
    front = text.split("---", 2)[1]
    out = {"artist": [], "links": {}}
    section = None
    for line in front.splitlines():
        if re.match(r"^\S", line) and not line.startswith("- "):
            m = re.match(r"^(\w+):\s*(.*)$", line)
            section = m.group(1) if m else None
            if m and m.group(2) and section not in ("artist", "links"):
                out[section] = m.group(2).strip("'\"")
            continue
        if section == "artist":
            m = re.match(r"^\s*-\s+(.*)$", line)
            if m:
                out["artist"].append(m.group(1).strip("'\""))
        elif section == "links":
            m = re.match(r"^  (\w+):\s*(.*)$", line)
            if m:
                out["links"][m.group(1)] = m.group(2).strip("'\"")
    return out


def load_config(path=CONFIG):
    """{"releases": [...], "services": [...], "cache_ttl_hours": n}; empty when there is no file."""
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def load_releases(slugs=()):
    """(slug, front matter) for each release with an artist and links, in the order of `slugs`
    when given, else alphabetically."""
    found = {}
    for path in sorted(MUSIC.glob("*/index.md")):
        slug = path.parent.name
        if slugs and slug not in slugs:
            continue
        fm = parse_front_matter(path.read_text(encoding="utf-8"))
        if fm and fm["artist"] and fm["links"]:
            found[slug] = fm
    if slugs:
        return [(s, found[s]) for s in slugs if s in found]
    return list(found.items())


# --- Cache ------------------------------------------------------------------------------------

class Cache:
    """Fetch results keyed by service resource, e.g. "spotify:<album id>", with a TTL."""

    def __init__(self, path=CACHE, ttl_hours=DEFAULT_TTL_HOURS, enabled=True, refresh=False,
                 clock=time.time):
        self.path = pathlib.Path(path)
        self.ttl = ttl_hours * 3600
        self.enabled = enabled
        self.refresh = refresh
        self.clock = clock
        self.entries = {}
        if enabled:
            try:
                self.entries = json.loads(self.path.read_text(encoding="utf-8"))
            except (FileNotFoundError, ValueError):
                self.entries = {}

    def get(self, key):
        """(Fetched, age in seconds) for a fresh entry, else None."""
        if not self.enabled or self.refresh:
            return None
        entry = self.entries.get(key)
        if not entry or entry.get("v") != CACHE_VERSION:
            return None
        age = self.clock() - entry["fetched_at"]
        if age > self.ttl:
            return None
        return Fetched.from_json(entry["data"]), age

    def put(self, key, fetched):
        if self.enabled:
            self.entries[key] = {"v": CACHE_VERSION, "fetched_at": self.clock(),
                                 "data": fetched.to_json()}

    def save(self):
        if not self.enabled:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.entries, indent=2, sort_keys=True, ensure_ascii=False),
                             encoding="utf-8")


# --- Fetchers ---------------------------------------------------------------------------------

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def get_json(url):
    return json.loads(get(url))


def spotify_entity(kind, sid):
    html = get("https://open.spotify.com/embed/%s/%s" % (kind, sid))
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    return json.loads(m.group(1))["props"]["pageProps"]["state"]["data"]["entity"]


def apple_id(links):
    return links.get("apple_music_album")


def spotify_id(links):
    return links.get("spotify_album")


def deezer_id(links):
    m = re.search(r"/album/(\d+)", links.get("deezer") or "")
    return m.group(1) if m else None


def youtube_id(links):
    return links.get("youtube_music_track") or links.get("youtube")


def qobuz_id(links):
    return links.get("qobuz")


def fetch_apple(album):
    results = get_json("https://itunes.apple.com/lookup?id=%s&entity=song&country=us" % album)["results"]
    if not results:
        raise LookupError("album not found")
    credit = results[0].get("artistName", "")
    artist_ids = []
    for r in results:
        if r.get("artistId") and r["artistId"] not in artist_ids:
            artist_ids.append(r["artistId"])
    names = []
    for i in artist_ids:
        for r in get_json("https://itunes.apple.com/lookup?id=%s" % i)["results"]:
            names.append(r["artistName"])
    # The displayed credit ("A & B") is checked too: a true collaboration shows both names even
    # when the lookup resolves only to the primary artist.
    return Fetched(credit=credit, entities=names, ids=[str(i) for i in artist_ids])


def fetch_spotify(album):
    entity = spotify_entity("album", album)
    names, ids = [], []
    for t in entity.get("trackList", []):
        tid = t["uri"].rsplit(":", 1)[-1]
        for a in spotify_entity("track", tid).get("artists", []):
            if a["name"] not in names:
                names.append(a["name"])
                ids.append(a["uri"].rsplit(":", 1)[-1])
    return Fetched(credit=entity.get("subtitle", ""), entities=names, ids=ids)


def fetch_deezer(album_id):
    album = get_json("https://api.deezer.com/album/%s" % album_id)
    if "error" in album:
        raise LookupError(album["error"].get("message", "error"))
    people = album.get("contributors") or [album["artist"]]
    return Fetched(credit=album["artist"]["name"], entities=[p["name"] for p in people],
                   ids=[str(p["id"]) for p in people], upc=album.get("upc", ""))


def fetch_youtube(vid):
    data = get_json("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(
        "https://www.youtube.com/watch?v=" + vid, safe=""))
    return Fetched(entities=[re.sub(r"\s+-\s+Topic$", "", data["author_name"])], strict=False)


def fetch_qobuz(url):
    """Qobuz refuses automated page reads, so judge the artist credit that is part of the link."""
    credit = qobuz_credit_from_url(url)
    if not credit:
        raise LookupError("not a Qobuz album URL")
    # A bundled " x " artist becomes one entity so that judge() sees it as MERGED.
    return Fetched(credit=credit, entities=[credit] if " x " in credit else [], source="URL slug")


# name -> (display name, resource id from a release's links, fetch by resource id)
SERVICES = {
    "apple": ("Apple Music", apple_id, fetch_apple),
    "spotify": ("Spotify", spotify_id, fetch_spotify),
    "deezer": ("Deezer", deezer_id, fetch_deezer),
    "qobuz": ("Qobuz", qobuz_id, fetch_qobuz),
    "youtube": ("YouTube", youtube_id, fetch_youtube),
}


def service_url(name, links):
    """A link a person can open for the release on that service, or "" when it has none."""
    rid = SERVICES[name][1](links)
    if not rid:
        return ""
    if name in ("deezer", "qobuz"):
        return links[name]
    return {"apple": "https://music.apple.com/us/album/%s",
            "spotify": "https://open.spotify.com/album/%s",
            "youtube": "https://music.youtube.com/watch?v=%s"}[name] % rid


ID_LABEL = {"apple": "Apple artist ID", "spotify": "Spotify artist ID", "deezer": "Deezer artist ID"}


# --- Checking and report ----------------------------------------------------------------------

class Result:
    def __init__(self, slug, fm, service, status, detail="", fetched=None, error=""):
        self.slug, self.fm, self.service = slug, fm, service
        self.status, self.detail, self.fetched, self.error = status, detail, fetched, error


def check(releases, services, cache, delay=0.2, registry=None):
    """Returns (results, counts); counts is {"fetched": n, "cached": n}. A release without a link
    for a service has no result for it."""
    registry = registry or SERVICES
    results = []
    counts = {"fetched": 0, "cached": 0}
    for slug, fm in releases:
        for name in services:
            _, find_id, fetch = registry[name]
            rid = find_id(fm["links"])
            if not rid:
                continue
            key = "%s:%s" % (name, rid)
            hit = cache.get(key)
            if hit:
                fetched = hit[0]
                counts["cached"] += 1
            else:
                try:
                    fetched = fetch(rid)
                except (urllib.error.URLError, LookupError, KeyError, ValueError, OSError) as e:
                    results.append(Result(slug, fm, name, UNKNOWN, error=str(e)))
                    continue
                cache.put(key, fetched)
                counts["fetched"] += 1
                if name != "qobuz":
                    time.sleep(delay)
            status, detail = judge(fm["artist"], fetched)
            results.append(Result(slug, fm, name, status, detail, fetched))
    return results, counts


def known_profiles(results):
    """{service: {normalized artist name: ID}}: the IDs of artists the services already show as
    their own entity, so a fix request can point at the profile that should be used."""
    out = {}
    for r in results:
        if not r.fetched:
            continue
        for name, rid in zip(r.fetched.entities, r.fetched.ids):
            if rid and norm(name) in [norm(a) for a in r.fm["artist"]]:
                out.setdefault(r.service, {})[norm(name)] = rid
    return out


def shows(fetched):
    if fetched.entities and norm(fetched.credit) not in [norm(e) for e in fetched.entities]:
        return '"%s" (artist entities: %s)' % (fetched.credit, ", ".join(fetched.entities))
    return ", ".join('"%s"' % e for e in fetched.entities) or '"%s"' % fetched.credit


def expected_line(result, profiles):
    parts = []
    for a in result.fm["artist"]:
        rid = profiles.get(result.service, {}).get(norm(a))
        label = ID_LABEL.get(result.service)
        parts.append("%s (existing %s %s)" % (a, label, rid) if rid and label else a)
    return " and ".join(parts) if len(parts) == 2 else ", ".join(parts)


def release_title(slug, fm):
    return fm.get("title", slug)


def format_report(results, services, counts, today=None):
    """The plain-text report: one section per release, problems first, no tables."""
    today = today or datetime.date.today().isoformat()
    profiles = known_profiles(results)
    out = ["Artist credit check, %s" % today, ""]
    problems = sum(1 for r in results if r.status in (MERGED, MISSING))
    out += ["%d problem(s) found. Expected on every release: the artists listed in the site's front "
            "matter, each credited as its own existing artist, never as one combined artist." % problems, ""]
    order = []
    for r in results:
        if r.slug not in order:
            order.append(r.slug)
    for slug in order:
        mine = [r for r in results if r.slug == slug]
        fm = mine[0].fm
        out.append("%s" % release_title(slug, fm))
        out.append("  Expected artists: %s" % " + ".join(fm["artist"]))
        upc = fm.get("upc") or next((r.fetched.upc for r in mine if r.fetched and r.fetched.upc), "")
        ids = ["UPC %s%s" % (upc, "" if fm.get("upc") else " (from Deezer)")] if upc else []
        if fm.get("isrc"):
            ids.append("ISRC %s" % fm["isrc"])
        if ids:
            out.append("  Identifiers: %s" % ", ".join(ids))
        for r in mine:
            if r.status not in (MERGED, MISSING):
                continue
            name = SERVICES[r.service][0]
            what = ('one combined artist "%s" instead of separate artists' % r.detail
                    if r.status == MERGED else "no credit for %s" % r.detail)
            out.append("  PROBLEM, %s: %s" % (name, what))
            out.append("    Link: %s" % service_url(r.service, r.fm["links"]))
            out.append("    Shows: %s" % shows(r.fetched))
            out.append("    Expected: %s" % expected_line(r, profiles))
            if r.fetched.source != "page":
                out.append("    Evidence: only the artist words in the %s link, not the page itself "
                           "(%s blocks automated reads); open the link to confirm." % (name, name))
        good = [SERVICES[r.service][0] + ("" if r.fetched.source == "page" else " (from the link only)")
                for r in mine if r.status == OK]
        if good:
            out.append("  Correct: %s" % ", ".join(good))
        for r in mine:
            if r.status == UNKNOWN:
                out.append("  Could not read %s: %s" % (SERVICES[r.service][0], r.error))
        linked = {r.service for r in mine}
        skipped = [SERVICES[s][0] for s in services if s not in linked]
        skipped += [label for key, label in UNCHECKED_LINKS.items() if key in fm["links"]]
        if skipped:
            out.append("  Not checked (no link on the site, or not readable by this tool): %s"
                       % ", ".join(skipped))
        out.append("")
    out.append("(%d looked up, %d from cache)" % (counts["fetched"], counts["cached"]))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("slugs", nargs="*", help="release slugs (default: the config's list)")
    ap.add_argument("--config", default=str(CONFIG), help="config file (default: %(default)s)")
    ap.add_argument("--service", action="append", choices=sorted(SERVICES),
                    help="only this service (repeatable)")
    ap.add_argument("--refresh", action="store_true", help="ignore cached results and fetch again")
    ap.add_argument("--no-cache", action="store_true", help="do not read or write the cache")
    args = ap.parse_args(argv)

    config = load_config(args.config)
    slugs = args.slugs or config.get("releases", [])
    if not slugs:
        print("no releases configured: list them in %s or pass slugs" % args.config, file=sys.stderr)
        return 2
    services = args.service or config.get("services") or list(SERVICES)
    unknown = [s for s in services if s not in SERVICES]
    if unknown:
        print("unknown service(s) in config: %s" % ", ".join(unknown), file=sys.stderr)
        return 2
    releases = load_releases(slugs)
    for s in slugs:
        if s not in [r[0] for r in releases]:
            print("warning: %s has no release with an artist and links; skipped" % s, file=sys.stderr)
    if not releases:
        return 2

    cache = Cache(ttl_hours=config.get("cache_ttl_hours", DEFAULT_TTL_HOURS),
                  enabled=not args.no_cache, refresh=args.refresh)
    results, counts = check(releases, services, cache)
    cache.save()
    print(format_report(results, services, counts))
    return 1 if any(r.status in (MERGED, MISSING) for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
