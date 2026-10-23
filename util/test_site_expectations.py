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
                "/music/youtube/": "music.youtube.com", "/music/qobuz/": "www.qobuz.com"}
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


class TestEscaping(unittest.TestCase):
    """Text must not show raw entities like &rsquo; (double-escaped HTML)."""

    # The post about a mangled "&amp;" in a password quotes the literal text "&amp;amp;"
    # (its summary is repeated on the Jogger index), so those pages legitimately contain it.
    INTENTIONAL = {"/jogger/": {"&amp;amp;"},
                   "/jogger/2015/co-trzeba-potrafic-zeby-byc-klientem-rwe/": {"&amp;amp;"}}
    DOUBLE_ESCAPED = re.compile(r"&amp;(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);")

    def test_no_double_escaped_entities(self):
        """/music/projects/ showed "Maciej&rsquo;s" and "&ldquo;Little Bird&rdquo;" (2026-10-16)."""
        bad = {}
        for url in SITE.pages:
            html = (SITE.root / url.strip("/") / "index.html").read_text(encoding="utf-8")
            html = re.sub(r"<(pre|code|script|style)\b.*?</\1>", "", html, flags=re.S)
            found = sorted(set(self.DOUBLE_ESCAPED.findall(html)) - self.INTENTIONAL.get(url, set()))
            if found:
                bad[url] = found[:5]
        self.assertEqual(bad, {})


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

    def test_release_list_pages_use_latest_release_cover(self):
        """/music/ lost its og:image when the site-logo fallback was dropped."""
        for url in ("/", "/music/", "/music/spotify/", "/music/apple/", "/music/youtube/", "/music/qobuz/",
                    "/music/projects/gaia_marenghi/", "/genres/", "/genres/jazz/"):
            with self.subTest(url=url):
                self.assertIn(url, SITE.pages)
                self.assertTrue(SITE.pages[url].meta_one("og:image"), f"{url} has no og:image")
                self.assertEqual(SITE.pages[url].meta_one("twitter:image"), SITE.pages[url].meta_one("og:image"))

    def test_music_page_social_image_is_newest_cover_like_homepage(self):
        """/music/ and / list the same releases, so they share one cover."""
        self.assertEqual(SITE.pages["/music/"].meta_one("og:image"), SITE.pages["/"].meta_one("og:image"))

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
        for url in ("/music/spotify/", "/music/apple/", "/music/youtube/", "/music/qobuz/"):
            with self.subTest(url=url):
                self.assertIn(url, SITE.pages)
                self.assertTrue(SITE.pages[url].meta_one("og:image"))
                self.assertRegex(SITE.pages[url].title, r"on (Spotify|Apple Music|YouTube Music|Qobuz)")


class TestMusicSocialTags(unittest.TestCase):
    """Social tags in /music (2026-10-15 audit, Docs/social-jsonld-audit.md)."""

    SECTION_PAGES = ["/music/", "/music/projects/",
                     "/music/performances/", "/music/credits/"]

    def test_only_the_homepage_may_use_a_non_specific_image(self):
        """Release pages without a cover must not fall back to the site share image."""
        for url, p in SITE.pages.items():
            if RELEASE_URL.match(url):
                img = p.meta_one("og:image") or ""
                self.assertNotIn("maciej_on_bass", img, url)
                card = p.meta_one("twitter:card")
                self.assertEqual(card, "summary_large_image" if img else "summary", url)

    def test_albums_are_music_album_and_singles_music_song(self):
        self.assertEqual(SITE.pages["/music/libera/"].meta_one("og:type"), "music.album")
        self.assertEqual(SITE.pages["/music/river/"].meta_one("og:type"), "music.song")
        # no `single:` key = a single recording (old releases)
        self.assertEqual(SITE.pages["/music/burza/"].meta_one("og:type"), "music.song")

    def test_music_sections_have_their_own_description(self):
        site_default = SITE.pages["/"].meta_one("description")
        for url in self.SECTION_PAGES:
            with self.subTest(url=url):
                d = SITE.pages[url].meta_one("description")
                self.assertNotEqual(d, site_default)
                self.assertLess(len(d), 200, "description looks like a body dump")

    def test_music_titles_share_one_suffix(self):
        for url in self.SECTION_PAGES[1:]:
            with self.subTest(url=url):
                self.assertTrue(SITE.pages[url].title.strip().endswith("- Music Production"))

    def test_release_titles_have_no_section_suffix(self):
        for url, p in SITE.pages.items():
            if RELEASE_URL.match(url):
                self.assertNotIn("Music Production", p.title, url)

    def test_index_style_pages_are_not_articles(self):
        for url in ("/music/credits/", "/music/performances/", "/music/spotify/"):
            self.assertEqual(SITE.pages[url].meta_one("og:type"), "website", url)

    def test_local_cover_images_declare_size_and_alt(self):
        p = SITE.pages["/music/libera/"]
        self.assertTrue(p.meta_one("og:image:width"))
        self.assertTrue(p.meta_one("og:image:height"))
        self.assertIn("Libera", p.meta_one("og:image:alt"))


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
            data = json.loads(raw)
        except ValueError:
            continue  # reported by test_all_jsonld_is_valid_json
        out.extend(data if isinstance(data, list) else [data])  # a script may hold an array
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

    def test_release_jsonld_declares_service_links_upc_and_isrc(self):
        """Loser's JSON-LD lists each service (sameAs + ListenAction) plus its UPC and ISRC."""
        rec = next(b for b in jsonld_blocks(SITE.pages["/music/loser/"]) if b.get("@type") == "MusicRecording")
        hosts = ("open.spotify.com", "music.apple.com", "music.youtube.com", "www.qobuz.com",
                 "www.deezer.com", "tidal.com", "music.amazon.com", "gaiamarenghi.bandcamp.com")
        targets = [t["urlTemplate"] for t in rec["potentialAction"]["target"]]
        for host in hosts:
            with self.subTest(host=host):
                self.assertTrue(any(host in u for u in rec["sameAs"]), rec["sameAs"])
                self.assertTrue(any(host in u for u in targets), targets)
        self.assertEqual(rec["isrcCode"], "QTA7T2691650")
        self.assertEqual(rec["identifier"], {"@type": "PropertyValue", "propertyID": "UPC", "value": "700536369090"})

    def test_collaborating_artists_are_joined_with_and(self):
        """One join-names partial: "A and B", "A, B, and C", never "A x B"."""
        def html(url):
            return (SITE.root / url.strip("/") / "index.html").read_text(encoding="utf-8")
        cases = {"/music/loser/": "Gaia Marenghi and Maciej Bliziński",
                 "/music/tentativa/": "Luisa Annibali, Julio Batista, and William Alexandre"}
        for url, expected in cases.items():
            with self.subTest(url=url):
                self.assertIn(f'class="artist">{expected}<', html(url))
        for url in SITE.pages:
            if RELEASE_URL.match(url):
                with self.subTest(url=url):
                    self.assertNotRegex(html(url), r'class="artist">[^<]* x ')


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


def css_rules(text):
    """Yield (media query or None, selector, position) for every rule in a stylesheet."""
    text = re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), text, flags=re.S)
    out, i, n = [], 0, len(text)

    def block_end(start):
        depth, j = 0, start
        while True:
            depth += (text[j] == "{") - (text[j] == "}")
            j += 1
            if depth == 0:
                return j

    def walk(lo, hi, query):
        i = lo
        while i < hi:
            if text[i].isspace():
                i += 1
                continue
            brace = text.index("{", i)
            head = " ".join(text[i:brace].split())
            end = block_end(brace)
            if head.startswith("@media"):
                walk(brace + 1, end - 1, head)
            elif not head.startswith("@"):
                for sel in head.split(","):
                    out.append((query, " ".join(sel.split()), i))
            i = end

    walk(0, n, None)
    return out


class TestCssStructure(unittest.TestCase):
    """The stylesheet is grouped by component; responsive rules sit under their base (2026-10-16)."""

    @classmethod
    def setUpClass(cls):
        cls.text = (REPO / "themes/multi-stream/assets/css/main.css").read_text(encoding="utf-8")
        cls.rules = css_rules(cls.text)

    def test_templates_do_not_emit_hr(self):
        """No <hr> as a separator: use spacing or a border on the item (2026-10-16)."""
        bad = [str(f.relative_to(REPO)) for root in ("layouts", "themes/multi-stream/layouts")
               for f in (REPO / root).rglob("*.html")
               if re.search(r"<hr\b", f.read_text(encoding="utf-8")) and f.name != "book.html"]
        self.assertEqual(bad, [])

    def test_no_catch_all_media_blocks(self):
        """A 28-rule "General Mobile Styles" block once hid stale overrides (2026-10-01 bug)."""
        per_block = {}
        for query, sel, pos in self.rules:
            if query and query != "print":
                per_block.setdefault((query, self.block_start(pos)), set()).add(sel)
        big = {k[0]: len(v) for k, v in per_block.items() if len(v) > 12}
        self.assertEqual(big, {}, "a media block holds many unrelated rules; move them under their components")

    def block_start(self, pos):
        # Rules of one @media block share the nearest preceding "@media" that is still open.
        before = self.text[:pos]
        return before.rfind("@media")

    def test_no_selector_overridden_in_two_blocks_of_the_same_query(self):
        seen, dup = {}, []
        for query, sel, pos in self.rules:
            if not query:
                continue
            block = self.block_start(pos)
            if seen.setdefault((query, sel), block) != block:
                dup.append(f"{query}: {sel}")
        self.assertEqual(dup, [])

    def test_responsive_overrides_come_after_their_base_rule(self):
        base_first, bad = {}, []
        for query, sel, pos in self.rules:
            if not query:
                base_first.setdefault(sel, pos)
        for query, sel, pos in self.rules:
            if query and query != "print" and sel in base_first and base_first[sel] > pos:
                bad.append(f"{query}: {sel}")
        self.assertEqual(bad, [], "a breakpoint override is declared before its base rule and would lose to it")


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


class TestMusicReleaseJsonLd(unittest.TestCase):
    """One jsonld/music-release.html partial describes a release everywhere it appears."""

    PERSON_ID = BASE_URL + "/person/#maciej"
    WEBSITE_ID = BASE_URL + "/#website"
    # Pages that show releases and the ItemList each must carry.
    LIST_PAGES = ["/", "/music/", "/music/spotify/", "/music/apple/", "/music/youtube/",
                  "/music/qobuz/", "/music/credits/", "/genres/", "/genres/jazz/",
                  "/music/projects/gaia_marenghi/", "/bio/"]

    def release_item_list(self, url):
        lists = [b for b in jsonld_blocks(SITE.pages[url]) if b.get("@type") == "ItemList"
                 and any(e.get("item", {}).get("@id", "").endswith("#release")
                         for e in b.get("itemListElement", []))]
        return lists

    def test_person_and_website_have_ids_other_nodes_can_reference(self):
        blocks = {b["@type"]: b for b in jsonld_blocks(SITE.pages["/"]) if b.get("@type") in ("Person", "WebSite")}
        self.assertEqual(blocks["Person"].get("@id"), self.PERSON_ID)
        self.assertEqual(blocks["WebSite"].get("@id"), self.WEBSITE_ID)

    def test_release_page_describes_the_release_once(self):
        recs = [b for b in jsonld_blocks(SITE.pages["/music/loser/"]) if b.get("@type") == "MusicRecording"]
        self.assertEqual(len(recs), 1)
        rec = recs[0]
        self.assertEqual(rec["@id"], BASE_URL + "/music/loser/#release")
        self.assertEqual(rec["url"], BASE_URL + "/music/loser/")
        self.assertEqual(rec["genre"], ["Pop"])
        self.assertEqual([a["name"] for a in rec["byArtist"]], ["Gaia Marenghi", "Maciej Bliziński"])
        self.assertTrue(rec.get("description"))
        self.assertNotRegex(rec["description"], r"&\w+;", "HTML entities leaked into the description")
        self.assertEqual([x.get("@id") for x in rec["producer"]], [self.PERSON_ID])
        self.assertEqual(rec["isPartOf"], {"@id": self.WEBSITE_ID})

    def test_credit_roles_map_to_schema_properties(self):
        rec = next(b for b in jsonld_blocks(SITE.pages["/music/loser/"]) if b.get("@type") == "MusicRecording")
        comp = rec["recordingOf"]
        self.assertEqual([c["name"] for c in comp["lyricist"]], ["Gaia Marenghi"])
        self.assertEqual([c["name"] for c in comp["composer"]], ["Gaia Marenghi", "Maciej Bliziński"])

    def test_album_is_a_music_album_with_its_upc(self):
        alb = next(b for b in jsonld_blocks(SITE.pages["/music/to-promenade/"]) if b.get("@type") == "MusicAlbum")
        self.assertEqual(alb["@id"], BASE_URL + "/music/to-promenade/#release")
        self.assertEqual(alb["identifier"]["value"], "199518640188")

    def test_every_release_page_has_exactly_one_release_node(self):
        bad = []
        for url, p in SITE.pages.items():
            if RELEASE_URL.match(url):
                n = [b for b in jsonld_blocks(p) if b.get("@type") in ("MusicRecording", "MusicAlbum")]
                if len(n) != 1:
                    bad.append(f"{url}: {len(n)}")
        self.assertEqual(bad, [])

    def test_pages_that_show_releases_carry_an_itemlist_of_them(self):
        for url in self.LIST_PAGES:
            with self.subTest(page=url):
                lists = self.release_item_list(url)
                self.assertEqual(len(lists), 1, f"{url} wants exactly one release ItemList")
                items = lists[0]["itemListElement"]
                self.assertTrue(items)
                for e in items:
                    it = e["item"]
                    self.assertIn(it["@type"], ("MusicRecording", "MusicAlbum"))
                    self.assertTrue(RELEASE_URL.match(it["url"].replace(BASE_URL, "")), it["url"])
                    self.assertTrue(it["name"] and it["byArtist"] and it["datePublished"], it)

    def test_music_page_itemlist_has_every_release(self):
        want = {BASE_URL + u for u in SITE.pages if RELEASE_URL.match(u)}
        got = {e["item"]["url"] for e in self.release_item_list("/music/")[0]["itemListElement"]}
        self.assertEqual(sorted(want - got), [])
        self.assertEqual(sorted(got - want), [])

    def test_list_items_use_the_same_id_as_the_release_page(self):
        for e in self.release_item_list("/music/")[0]["itemListElement"]:
            self.assertEqual(e["item"]["@id"], e["item"]["url"] + "#release")

    def test_service_pages_only_list_releases_on_that_service(self):
        everything = {e["item"]["url"] for e in self.release_item_list("/music/")[0]["itemListElement"]}
        qobuz = {e["item"]["url"] for e in self.release_item_list("/music/qobuz/")[0]["itemListElement"]}
        self.assertLess(qobuz, everything)
        self.assertIn(BASE_URL + "/music/loser/", qobuz)

    def test_project_group_references_its_releases_and_members(self):
        group = next(b for b in jsonld_blocks(SITE.pages["/music/projects/gaia_marenghi/"]) if b.get("@type") == "MusicGroup")
        refs = [t["@id"] for t in group.get("track", []) + group.get("album", [])]
        self.assertIn(BASE_URL + "/music/loser/#release", refs)
        self.assertTrue(any(m.get("@id") == BASE_URL + "/person/#gaia-marenghi" for m in group.get("member", [])), group.get("member"))

    def test_owner_links_to_the_releases_he_produced(self):
        person = next(b for b in jsonld_blocks(SITE.pages["/"]) if b.get("@type") == "Person")
        produced = [r["@id"] for r in person["@reverse"]["producer"]]
        self.assertIn(BASE_URL + "/music/loser/#release", produced)
        self.assertLessEqual(set(produced), {r["@id"] for r in person["@reverse"]["contributor"]})

    def test_credits_page_declares_every_credited_musician_once(self):
        lists = [b for b in jsonld_blocks(SITE.pages["/music/credits/"])
                 if b.get("@type") == "ItemList" and b.get("name") == "People credited on releases"]
        self.assertEqual(len(lists), 1)
        people = {e["item"]["name"]: e["item"] for e in lists[0]["itemListElement"]}
        self.assertEqual(len(people), len(lists[0]["itemListElement"]), "a person appears twice")
        riccardo = people["Riccardo Marenghi"]
        self.assertEqual(riccardo["@id"], BASE_URL + "/person/#riccardo-marenghi")
        self.assertEqual(riccardo["url"], BASE_URL + "/music/credits/#riccardo-marenghi")
        self.assertIn("drums", [o["name"] for o in riccardo["hasOccupation"]])
        self.assertIn(BASE_URL + "/music/loser/#release", [r["@id"] for r in riccardo["@reverse"]["contributor"]])
        self.assertEqual(people["Maciej Bliziński"]["@id"], self.PERSON_ID)

    def test_release_contributors_point_at_credits_page_people(self):
        rec = next(b for b in jsonld_blocks(SITE.pages["/music/loser/"]) if b.get("@type") == "MusicRecording")
        drummer = next(c for c in rec["contributor"] if c["name"] == "Riccardo Marenghi")
        self.assertEqual(drummer["@id"], BASE_URL + "/person/#riccardo-marenghi")
        self.assertEqual(drummer["roleName"], ["drums"])
        credits_html = (SITE.root / "music/credits/index.html").read_text(encoding="utf-8")
        self.assertIn('id="riccardo-marenghi"', credits_html)


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
