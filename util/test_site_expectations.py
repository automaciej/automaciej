#!/usr/bin/env python3
"""Build the site once and check the things every website is expected to have.

Each check guards a feature that was once missing and had to be added later
(see the commit hashes in the docstrings), so a refactor that silently drops
it fails here instead of in production.

Usage:
    python3 util/test_site_expectations.py            # build + test
    SITE_DIR=/path/to/built/site python3 util/test_site_expectations.py
        # skip the build, test an existing output directory
        # (must have been built with --baseURL https://blizin.ski)

The build runs on a copy of the working tree in a temp directory under $HOME
(same approach as util/diff_commits.sh) with an explicit --baseURL, so it never
touches public/ or the running `hugo server`. Drafts and future-dated pages
are NOT built: this mirrors what gets deployed.
"""

import atexit
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlparse

REPO = Path(__file__).resolve().parent.parent
BASE_URL = "https://blizin.ski"
# Releases are the leaf bundles directly under content/music/ (/music/<slug>/);
# other /music/ pages (spotify, credits, performances, projects) are not releases.
RELEASE_SLUGS = sorted(d.parent.name for d in (REPO / "content/music").glob("*/index.md"))
RELEASE_URL = re.compile(r"^/music/(%s)/$" % "|".join(map(re.escape, RELEASE_SLUGS)))

# Sections with their own RSS feed. Jogger is Polish and has a separate feed;
# the home feed must not contain it (60f8eb0).
SERVICE_FEEDS = {"/music/spotify/": "open.spotify.com", "/music/apple/": "music.apple.com",
                "/music/youtube/": "music.youtube.com"}
FEED_SECTIONS = ["/", "/blog/", "/jogger/", "/music/"] + list(SERVICE_FEEDS)


class PageParser(HTMLParser):
    """Collects the head metadata, links and JSON-LD blocks of one page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = None
        self.title = ""
        self.meta = []  # list of (key, content), key is name= or property=
        self.links = []  # list of attr dicts for <link>
        self.refs = []  # href/src values from body elements
        self.jsonld = []
        self.scripts = []  # inline script bodies
        self.refresh = None
        self._in_title = False
        self._in_script = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            if (a.get("http-equiv") or "").lower() == "refresh":
                self.refresh = a.get("content")
            key = a.get("name") or a.get("property")
            if key:
                self.meta.append((key, a.get("content", "")))
        elif tag == "link":
            self.links.append(a)
        elif tag == "script":
            self._in_script = "jsonld" if a.get("type") == "application/ld+json" else "js"
            self._script_buf = []
            if a.get("src"):
                self.refs.append(a["src"])
        for attr in ("href", "src"):
            if tag in ("a", "img", "source", "audio", "video", "iframe") and a.get(attr):
                self.refs.append(a[attr])
        if tag == "img" and a.get("srcset"):
            for part in a["srcset"].split(","):
                self.refs.append(part.strip().split(" ")[0])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_script:
            body = "".join(self._script_buf)
            (self.jsonld if self._in_script == "jsonld" else self.scripts).append(body)
            self._in_script = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_script:
            self._script_buf.append(data)

    def meta_values(self, key):
        return [v for k, v in self.meta if k == key]

    def meta_one(self, key):
        vals = self.meta_values(key)
        return vals[0] if len(vals) == 1 else None


class Site:
    """The built site: pages parsed lazily, keyed by URL path."""

    def __init__(self, root: Path):
        self.root = root
        self.pages = {}  # url path -> PageParser (real pages only)
        self.aliases = {}  # url path -> redirect target
        for f in sorted(root.rglob("*.html")):
            url = "/" + str(f.relative_to(root)).replace("index.html", "")
            p = PageParser()
            p.feed(f.read_text(encoding="utf-8"))
            if p.refresh:
                self.aliases[url] = p.refresh
            elif "googl" not in f.name:  # skip search-console verification file
                self.pages[url] = p

    def exists(self, url_path: str) -> bool:
        path = unquote(url_path).lstrip("/")
        target = self.root / path
        return target.is_file() or (target / "index.html").is_file()


def build_site() -> Path:
    """Copy the working tree and build it, as util/diff_commits.sh does.

    The workdir lives under $HOME with a name not starting with a dot:
    snap-confined hugo and sandboxed tools can't read /tmp or dotdirs.
    """
    if os.environ.get("SITE_DIR"):
        return Path(os.environ["SITE_DIR"])
    workdir = Path(tempfile.mkdtemp(prefix="site_expectations_tmp.", dir=Path.home()))
    atexit.register(shutil.rmtree, workdir, ignore_errors=True)
    src, out = workdir / "src", workdir / "build"
    # Working tree incl. uncommitted/untracked files; .git stays for enableGitInfo.
    subprocess.run(["rsync", "-a", "--exclude", "/public/", f"{REPO}/", f"{src}/"], check=True)
    subprocess.run(
        ["hugo", "--logLevel", "error", "--baseURL", BASE_URL, "--destination", str(out)],
        cwd=src,
        check=True,
    )
    return out


SITE = None


def setUpModule():
    global SITE
    SITE = Site(build_site())


def non_home(pages):
    return {u: p for u, p in pages.items() if u != "/"}


class TestBasicHead(unittest.TestCase):
    """Title, description, language: the minimum every page needs."""

    def test_every_page_has_title_and_description(self):
        """086f62b, 92b48e5: release pages once lacked descriptions."""
        bad = []
        for url, p in SITE.pages.items():
            if not p.title.strip():
                bad.append(f"{url}: empty <title>")
            if not (p.meta_one("description") or "").strip():
                bad.append(f"{url}: missing or empty/duplicate meta description")
        self.assertEqual(bad, [])

    def test_jogger_declares_polish(self):
        """f012537: Jogger posts are Polish, everything else English."""
        bad = []
        for url, p in SITE.pages.items():
            want = "pl" if url.startswith("/jogger/") else "en"
            if p.html_lang != want:
                bad.append(f"{url}: lang={p.html_lang!r}, want {want!r}")
        self.assertEqual(bad, [])

    def test_blog_titles_have_no_section_suffix(self):
        """f6454f2: '<Article> - Blog' titles were dropped."""
        bad = [u for u, p in SITE.pages.items()
               if re.match(r"^/blog/\d{4}/", u) and p.title.strip().endswith("- Blog")]
        self.assertEqual(bad, [])

    def test_stylesheet_is_fingerprinted_with_sri(self):
        """3c1dd9a: unhashed main.css was served stale from mobile caches."""
        p = SITE.pages["/"]
        css = [l for l in p.links if l.get("rel") == "stylesheet"
               and re.search(r"/css/main[.\-]", l.get("href", ""))]
        self.assertTrue(css, "no main.css stylesheet link")
        for l in css:
            self.assertRegex(l["href"], r"main\.[0-9a-f]{16,}\.css", "main.css not fingerprinted")
            self.assertTrue(l.get("integrity", "").startswith("sha"), "main.css has no integrity=")


class TestSocialTags(unittest.TestCase):
    """OpenGraph / Twitter cards on every page (f6454f2, 086f62b, a751fe5)."""

    REQUIRED = ["og:type", "og:title", "og:description", "og:url", "og:site_name",
                "twitter:card", "twitter:title", "twitter:description"]

    def test_every_page_has_complete_tags_exactly_once(self):
        """f6454f2: blog had none; the first fix duplicated tags on release pages."""
        bad = []
        for url, p in SITE.pages.items():
            for key in self.REQUIRED:
                vals = p.meta_values(key)
                if len(vals) != 1:
                    bad.append(f"{url}: {key} appears {len(vals)}x")
                elif not vals[0].strip():
                    bad.append(f"{url}: {key} is empty")
        self.assertEqual(bad, [])

    def test_social_image_is_absolute_and_never_a_generic_fallback(self):
        """086f62b: release pages lacked og:image; pages without their own image get none."""
        bad = []
        for url, p in SITE.pages.items():
            for key in ("og:image", "twitter:image"):
                vals = p.meta_values(key)
                if len(vals) > 1 or any(not v.startswith("https://") for v in vals):
                    bad.append(f"{url}: {key}={vals}")
            if "/images/logo" in (p.meta_one("og:image") or "") or bool(p.meta_values("og:image")) != bool(p.meta_values("twitter:image")):
                bad.append(f"{url}: generic or mismatched social image")
        self.assertEqual(bad, [])

    def test_homepage_social_image_is_latest_release_cover(self):
        img = SITE.pages["/"].meta_one("og:image")
        self.assertTrue(img, "homepage has no og:image")
        self.assertEqual(SITE.pages["/"].meta_one("twitter:image"), img)

    def test_local_social_images_exist_in_output(self):
        bad = []
        for url, p in SITE.pages.items():
            img = p.meta_one("og:image") or ""
            if img.startswith(BASE_URL) and not SITE.exists(urlparse(img).path):
                bad.append(f"{url}: {img}")
        self.assertEqual(bad, [])

    def test_og_url_is_the_page_itself(self):
        bad = [f"{u}: {p.meta_one('og:url')}" for u, p in SITE.pages.items()
               if unquote(p.meta_one("og:url") or "") != BASE_URL + u]
        self.assertEqual(bad, [])

    def test_social_title_matches_tab_title(self):
        """c169259: social previews of /genres/jazz/ showed a bare 'Jazz'."""
        bad = []
        for url, p in SITE.pages.items():
            if not re.match(r"^/(genres|tags)/[^/]+/$", url):
                continue  # other pages may set a deliberate og:title
            t = p.title.strip()
            if p.meta_one("og:title") != t or p.meta_one("twitter:title") != t:
                bad.append(f"{url}: <title>={t!r} og={p.meta_one('og:title')!r}")
        self.assertEqual(bad, [])

    def test_content_pages_do_not_fall_back_to_site_description(self):
        """92b48e5, 8ffe04c: releases, genres, posts need their own description."""
        site_default = SITE.pages["/"].meta_one("description")
        per_page = re.compile(r"^/(music/(?:%s)|genres/[^/]+|blog/\d{4}/[^/]+)/$" % "|".join(map(re.escape, RELEASE_SLUGS)))
        bad = [u for u, p in SITE.pages.items()
               if per_page.match(u) and p.meta_one("description") == site_default]
        self.assertEqual(bad, [])

    def test_per_service_lists_use_a_release_cover_not_the_default(self):
        """7e81648: /music/spotify etc. share the latest release's artwork."""
        for url in ("/music/spotify/", "/music/apple/", "/music/youtube/"):
            with self.subTest(url=url):
                self.assertIn(url, SITE.pages)
                self.assertTrue(SITE.pages[url].meta_one("og:image"))
                self.assertRegex(SITE.pages[url].title, r"on (Spotify|Apple Music|YouTube Music)")


class TestFeeds(unittest.TestCase):
    """RSS feeds and autodiscovery (60f8eb0)."""

    def feed_path(self, section):
        return section.rstrip("/") + "/index.xml" if section != "/" else "/index.xml"

    def parse_feed(self, section):
        path = SITE.root / unquote(self.feed_path(section)).lstrip("/")
        self.assertTrue(path.is_file(), f"no feed at {path}")
        return ET.parse(path).getroot().find("channel")

    def test_sections_advertise_their_own_feed(self):
        for section in FEED_SECTIONS:
            with self.subTest(section=section):
                p = SITE.pages[section]
                hrefs = [l["href"] for l in p.links
                         if l.get("rel") == "alternate" and l.get("type") == "application/rss+xml"]
                self.assertEqual(hrefs, [BASE_URL + self.feed_path(section)])

    def test_every_advertised_feed_exists_and_is_valid_xml(self):
        bad = []
        for url, p in SITE.pages.items():
            for l in p.links:
                if l.get("rel") == "alternate" and l.get("type") == "application/rss+xml":
                    path = urlparse(l["href"]).path
                    if not SITE.exists(path):
                        bad.append(f"{url}: {l['href']} missing")
                        continue
                    try:
                        ET.parse(SITE.root / unquote(path).lstrip("/"))
                    except ET.ParseError as e:
                        bad.append(f"{url}: {l['href']} invalid XML: {e}")
        self.assertEqual(bad, [])

    def test_genre_pages_and_overview_advertise_a_feed(self):
        for u in ["/genres/"] + [u for u in SITE.pages if re.match(r"^/genres/[^/]+/$", u)]:
            self.assertTrue([l for l in SITE.pages[u].links if l.get("type") == "application/rss+xml"], u)

    def test_every_index_xml_is_advertised_by_its_html_page(self):
        """Every generated feed is linked from the matching index.html (2026-10-16)."""
        bad = []
        for xml in sorted(SITE.root.rglob("index.xml")):
            url = "/" + xml.parent.relative_to(SITE.root).as_posix().strip(".") + "/"
            url = url.replace("//", "/")
            page = SITE.pages.get(url)
            if page is None:
                bad.append(f"{url}: no html page")
                continue
            hrefs = [unquote(l["href"]) for l in page.links
                     if l.get("rel") == "alternate" and l.get("type") == "application/rss+xml"]
            if BASE_URL + unquote(url) + "index.xml" not in hrefs:
                bad.append(f"{url}: no alternate link to its index.xml")
        self.assertEqual(bad, [])

    def test_feed_link_type_is_not_html_escaped(self):
        """The raw tag must read type="application/rss+xml", not rss&#43;xml."""
        raw = (SITE.root / "index.html").read_text(encoding="utf-8")
        tags = re.findall(r'<link[^>]*rel="alternate"[^>]*>', raw)
        self.assertTrue(tags)
        for tag in tags:
            self.assertIn('type="application/rss+xml"', tag)

    def test_service_feeds_mirror_their_pages(self):
        """/music/<service>/index.xml lists the same songs as the page (2026-10-16)."""
        for section, host in SERVICE_FEEDS.items():
            with self.subTest(section=section):
                raw = (SITE.root / section.strip("/") / "index.html").read_text(encoding="utf-8")
                items = self.parse_feed(section).findall("item")
                self.assertTrue(items)
                self.assertEqual(len(items), raw.count('<li class="streaming-item">'))
                guids = [i.findtext("guid") for i in items]
                self.assertEqual(len(guids), len(set(guids)))
                for i in items:
                    self.assertIn(host, i.findtext("description"))
                    self.assertTrue(i.findtext("link").startswith(BASE_URL + "/music/"))

    def test_release_feed_items_link_to_listen_services(self):
        """Release feed items carry direct links to the services (2026-10-16)."""
        items = self.parse_feed("/music/").findall("item")
        self.assertTrue(items)
        with_links = [i for i in items if "Listen on" in i.findtext("description")]
        self.assertTrue(with_links)
        self.assertTrue(any("open.spotify.com" in i.findtext("description") for i in with_links))

    def test_feed_copyright_is_not_double_escaped(self):
        for section in FEED_SECTIONS:
            with self.subTest(section=section):
                text = self.parse_feed(section).findtext("copyright", "")
                self.assertNotIn("&", text)

    def test_feeds_are_not_truncated(self):
        """60f8eb0: rssLimit removed, every entry is listed."""
        jogger = len(self.parse_feed("/jogger/").findall("item"))
        posts = len([u for u in SITE.pages if re.match(r"^/jogger/\d{4}/[^/]+/$", u)])
        excluded = sum(1 for f in (REPO / "content/jogger").rglob("*.md")
                       if re.search(r"^excludeFromRSS\s*[:=]\s*true", f.read_text(encoding="utf-8"), re.M))
        self.assertEqual(jogger, posts - excluded)

    def test_newest_items_have_full_text_and_all_have_descriptions(self):
        for section in ("/blog/", "/music/", "/", "/jogger/", "/genres/", "/tags/"):
            with self.subTest(section=section):
                items = self.parse_feed(section).findall("item")
                self.assertTrue(items)
                for i, item in enumerate(items):
                    self.assertTrue((item.findtext("description") or "").strip(),
                                    f"{item.findtext('link')} has empty description")
                    self.assertTrue(item.findtext("link", "").startswith(BASE_URL))

    def test_home_feed_excludes_jogger_and_jogger_feed_only_has_jogger(self):
        home = [i.findtext("link") for i in self.parse_feed("/").findall("item")]
        self.assertFalse([l for l in home if "/jogger/" in l])
        jog = [i.findtext("link") for i in self.parse_feed("/jogger/").findall("item")]
        self.assertTrue(jog)
        self.assertFalse([l for l in jog if "/jogger/" not in l])

    def test_home_feed_has_no_static_pages_or_undated_items(self):
        """Performances/Photos/Press/Bio leaked into the home feed (2026-10-16)."""
        items = self.parse_feed("/").findall("item")
        links = [i.findtext("link") for i in items]
        for page in ("/music/performances/", "/photos/", "/press/", "/bio/", "/meu-nome/"):
            self.assertNotIn(BASE_URL + page, links)
        undated = [i.findtext("link") for i in items if " 0001 " in i.findtext("pubDate", "")]
        self.assertEqual(undated, [])

    def test_feed_images_resolve_and_are_not_item_images(self):
        """Item images were `<image>` with a 404ing URL; now `media:content`."""
        media = "{http://search.yahoo.com/mrss/}content"
        bad = []
        for section in FEED_SECTIONS:
            for item in self.parse_feed(section).findall("item"):
                self.assertIsNone(item.find("image"), item.findtext("link"))
                m = item.find(media)
                if m is not None and not SITE.exists(urlparse(m.get("url")).path):
                    bad.append(f"{section}: {m.get('url')}")
        self.assertEqual(bad, [])

    def test_meu_nome_moved_to_jogger_and_old_url_redirects(self):
        self.assertIn("/jogger/2016/meu-nome/", SITE.pages)
        self.assertIn("/meu-nome/", SITE.aliases)
        self.assertIn("/jogger/2016/meu-nome/", SITE.aliases["/meu-nome/"])


def jsonld_blocks(page):
    out = []
    for raw in page.jsonld:
        try:
            out.append(json.loads(raw))
        except ValueError:
            pass  # reported by test_all_jsonld_is_valid_json
    return out


def types_in(page):
    return {b.get("@type") for b in jsonld_blocks(page)}


class TestNoCookieEmbeds(unittest.TestCase):
    """Third-party players are links; the only iframes left are youtube-nocookie (2026-10-16)."""

    def test_only_nocookie_youtube_iframes(self):
        bad = {}
        for f in SITE.root.rglob("*.html"):
            for src in re.findall(r'<iframe[^>]*\ssrc="([^"]+)"', f.read_text(encoding="utf-8")):
                if not src.startswith("https://www.youtube-nocookie.com/"):
                    bad.setdefault(str(f.relative_to(SITE.root)), []).append(src)
        self.assertEqual(bad, {})


class TestStructuredData(unittest.TestCase):
    """JSON-LD (f6454f2, 086f62b)."""

    def test_all_jsonld_is_valid_json(self):
        bad = []
        for url, p in SITE.pages.items():
            for raw in p.jsonld:
                try:
                    json.loads(raw)
                except ValueError as e:
                    bad.append(f"{url}: {e}")
        self.assertEqual(bad, [])

    def test_home_has_person_and_website(self):
        self.assertTrue({"Person", "WebSite"} <= types_in(SITE.pages["/"]))

    def test_every_inner_page_has_breadcrumbs(self):
        bad = [u for u, p in non_home(SITE.pages).items() if "BreadcrumbList" not in types_in(p)]
        self.assertEqual(bad, [])

    def test_posts_have_blogposting_in_their_language(self):
        """f6454f2: JSON-LD was Jogger-only and hardcoded to Polish."""
        bad = []
        for url, p in SITE.pages.items():
            m = re.match(r"^/(jogger|blog)/\d{4}/[^/]+/$", url)
            if not m:
                continue
            posts = [b for b in jsonld_blocks(p) if b.get("@type") == "BlogPosting"]
            if len(posts) != 1:
                bad.append(f"{url}: {len(posts)} BlogPosting blocks")
                continue
            want = "pl" if m.group(1) == "jogger" else "en"
            lang = posts[0].get("inLanguage")
            if isinstance(lang, dict):
                lang = lang.get("alternateName")
            if lang not in (want, {"pl": "Polish", "en": "English"}[want]):
                bad.append(f"{url}: inLanguage={lang!r}, want {want}")
            if not posts[0].get("description"):
                bad.append(f"{url}: BlogPosting without description")
        self.assertEqual(bad, [])

    def test_app_pages_have_softwareapplication(self):
        """f6454f2: only the /apps/ list had app schema."""
        app_dirs = [d.parent.name for d in (REPO / "content").glob("*/_index.md")
                    if re.search(r"^app\s*[:=]", d.read_text(encoding="utf-8"), re.M)]
        self.assertTrue(app_dirs, "no content/*/_index.md declares an `app` param")
        for name in app_dirs:
            with self.subTest(app=name):
                self.assertIn("SoftwareApplication", types_in(SITE.pages[f"/{name}/"]))

    def test_release_pages_have_jsonld_image(self):
        """086f62b: release JSON-LD had no image."""
        bad = []
        for url, p in SITE.pages.items():
            if not RELEASE_URL.match(url):
                continue
            blocks = jsonld_blocks(p)
            if not any(b.get("image") for b in blocks):
                bad.append(url)
        self.assertEqual(bad, [])


# Releases that existed when /music/releases/<slug>/ became /music/<slug>/ (2026-10-16).
# Only these keep an old-style alias; newer releases must not get one.
LEGACY_RELEASE_SLUGS = {
    "11ell-11eaven",
    "a-ginga-do-mane",
    "andre-de-sapato-novo",
    "bolero-de-sata",
    "burza",
    "butterfly",
    "estate",
    "guitar-duo-session",
    "hidden-beach",
    "hope-is-the-one",
    "ill-be-gone",
    "jazz-piano-trio-in-54",
    "je-te-veux",
    "libera",
    "little-bird-frost-is-all-over-cormac-murphys-jig",
    "loser",
    "ocean",
    "river",
    "run-for-me",
    "runnin",
    "song-for-you-and-bob",
    "talkative",
    "tentativa",
    "to-promenade",
    "triste",
}


class TestMusicUrls(unittest.TestCase):
    """Releases live at /music/<slug>/ (2026-10-16); the old /music/releases/ URLs redirect."""

    def test_release_slugs_do_not_collide_with_other_music_pages(self):
        others = {p.stem for p in (REPO / "content/music").glob("*.md") if p.name != "_index.md"}
        others |= {d.name for d in (REPO / "content/music").iterdir() if d.is_dir()} - set(RELEASE_SLUGS)
        self.assertEqual(sorted(set(RELEASE_SLUGS) & others), [])

    def test_only_legacy_releases_have_old_style_aliases(self):
        """New releases must not carry a /music/releases/ alias (copied front matter)."""
        for slug in RELEASE_SLUGS:
            text = (REPO / "content/music" / slug / "index.md").read_text(encoding="utf-8")
            has = f"/music/releases/{slug}/" in text
            with self.subTest(slug=slug):
                self.assertEqual(has, slug in LEGACY_RELEASE_SLUGS)

    def test_old_releases_urls_redirect_to_new_ones(self):
        for slug in LEGACY_RELEASE_SLUGS:
            with self.subTest(slug=slug):
                old = SITE.root / "music" / "releases" / slug / "index.html"
                self.assertTrue(old.is_file())
                self.assertIn(f"{BASE_URL}/music/{slug}/", old.read_text(encoding="utf-8"))
        self.assertTrue((SITE.root / "music" / "releases" / "index.html").is_file())

    def test_every_service_icon_has_light_and_dark_files(self):
        """service_icons maps each service to {light, dark}; both files must exist."""
        text = (REPO / "content/music/_index.md").read_text(encoding="utf-8")
        block = text.split("service_icons:\n", 1)[1].split("\n---", 1)[0]
        entries = re.findall(r"^  (\w+):\n    light: (\S+)\n    dark: (\S+)$", block, re.M)
        self.assertTrue(entries)
        self.assertEqual(len(entries), len(re.findall(r"^  \w+:", block, re.M)),
                         "a service_icons entry is not a {light, dark} pair")
        for key, light, dark in entries:
            for path in (light, dark):
                with self.subTest(service=key, path=path):
                    self.assertTrue((REPO / "static" / path.lstrip("/")).is_file())

    def test_music_page_lists_every_release(self):
        html = (SITE.root / "music" / "index.html").read_text(encoding="utf-8")
        for slug in RELEASE_SLUGS:
            with self.subTest(slug=slug):
                self.assertIn(f'href="/music/{slug}/"', html)


class TestLinks(unittest.TestCase):
    """No dead internal links or assets (f6454f2: /task-compass/ was linked from every page)."""

    def test_internal_links_and_assets_resolve(self):
        bad = {}
        for url, p in SITE.pages.items():
            for ref in p.refs + [l["href"] for l in p.links if l.get("href")]:
                ref = urldefrag(ref.strip())[0]
                if not ref or re.match(r"^(mailto:|tel:|javascript:|data:)", ref):
                    continue
                parsed = urlparse(ref)
                if parsed.scheme in ("http", "https") and not ref.startswith(BASE_URL):
                    continue  # external, not checked offline
                if parsed.netloc and not ref.startswith(BASE_URL):
                    continue
                path = parsed.path
                if not path.startswith("/"):
                    path = urlparse(BASE_URL + url).path.rsplit("/", 1)[0] + "/" + path
                if not SITE.exists(path) and path not in SITE.aliases:
                    bad.setdefault(ref, []).append(url)
        report = [f"{ref}  (on {len(pages)} pages, e.g. {pages[0]})" for ref, pages in sorted(bad.items())]
        self.assertEqual(report, [])

    def test_aliases_still_redirect_to_existing_pages(self):
        """~90 legacy URLs are kept alive through `aliases:` front matter."""
        self.assertGreaterEqual(len(SITE.aliases), 90, "URL aliases were lost")
        bad = []
        for url, content in SITE.aliases.items():
            m = re.search(r"url=(\S+)", content)
            target = urlparse(m.group(1)).path if m else None
            if not target or not SITE.exists(target):
                bad.append(f"{url} -> {content}")
        self.assertEqual(bad, [])


class TestBioReleasesList(unittest.TestCase):
    """/bio/ ends with every published release, grouped by year (8f094bd)."""

    def bio_html(self):
        path = SITE.root / "bio" / "index.html"
        self.assertTrue(path.is_file(), "no /bio/ page")
        return path.read_text(encoding="utf-8")

    def test_bio_lists_every_published_release_grouped_by_year_newest_first(self):
        """8f094bd: turning /bio from a section into a leaf page dropped the list."""
        html = self.bio_html()
        self.assertIn("<h2>Music Releases</h2>", html)
        published = {u for u in SITE.pages if RELEASE_URL.match(u)}
        self.assertTrue(published, "no release pages were built")
        chips = set(re.findall(r'<a class="release-chip[^"]*" href="([^"]+)"', html))
        self.assertEqual(sorted(published - chips), [], "releases missing from /bio/")
        self.assertEqual(sorted(chips - published), [], "/bio/ links to non-releases")
        years = re.findall(r'class="music-releases-year-label">(\d{4})<', html)
        self.assertTrue(years)
        self.assertEqual(years, sorted(set(years), reverse=True))

    def test_bio_releases_list_comes_after_the_bio_text(self):
        html = self.bio_html()
        self.assertLess(html.index('class="post-content"'), html.index("<h2>Music Releases</h2>"))

    def test_bio_releases_list_has_itemlist_jsonld(self):
        lists = [b for b in jsonld_blocks(SITE.pages["/bio/"]) if b.get("@type") == "ItemList"]
        self.assertEqual(len(lists), 1)
        self.assertTrue(lists[0]["itemListElement"])


class TestBioProfilePage(unittest.TestCase):
    def test_bio_has_profilepage_jsonld(self):
        """8f094bd: head.html checked Kind == section, so the leaf /bio/ lost it."""
        profiles = [b for b in jsonld_blocks(SITE.pages["/bio/"]) if b.get("@type") == "ProfilePage"]
        self.assertEqual(len(profiles), 1, "want exactly one ProfilePage block on /bio/")
        profile = profiles[0]
        self.assertEqual(profile.get("url"), BASE_URL + "/bio/")
        person = profile.get("mainEntity", {})
        self.assertEqual(person.get("@type"), "Person")
        self.assertTrue(person.get("name"))
        self.assertTrue(person.get("sameAs"), "Person has no sameAs profile links")

    def test_profilepage_only_on_bio(self):
        bad = [u for u, p in SITE.pages.items() if u != "/bio/" and "ProfilePage" in types_in(p)]
        self.assertEqual(bad, [])


class TestCrawlerBasics(unittest.TestCase):
    def test_sitemap_lists_every_page_and_robots_points_to_it(self):
        sitemap = SITE.root / "sitemap.xml"
        self.assertTrue(sitemap.is_file(), "no sitemap.xml")
        text = sitemap.read_text(encoding="utf-8")
        locs = {unquote(l) for l in re.findall(r"<loc>([^<]+)</loc>", text)}
        missing = [u for u in SITE.pages if BASE_URL + u not in locs]
        self.assertEqual(missing, [])
        robots = (SITE.root / "robots.txt")
        self.assertTrue(robots.is_file(), "no robots.txt")
        self.assertIn("sitemap.xml", robots.read_text(encoding="utf-8").lower())

    def test_share_script_only_on_release_pages(self):
        """d8452f2: share-button JS was shipped on every page."""
        bad = []
        for url, p in SITE.pages.items():
            has = any("navigator.share" in s for s in p.scripts)
            is_release = bool(RELEASE_URL.match(url))
            if has != is_release:
                bad.append(f"{url}: share script present={has}")
        self.assertEqual(bad, [])


if __name__ == "__main__":
    sys.exit(unittest.main(verbosity=2) and 0)
