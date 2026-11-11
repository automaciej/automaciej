#!/usr/bin/env python3
"""Offline tests for util/check_service_metadata.py (no network)."""

import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_service_metadata as c  # noqa: E402

BOTH = ["Gaia Marenghi", "Maciej Bliziński"]


class TestJudge(unittest.TestCase):
    def test_two_separate_artists_are_ok(self):
        f = c.Fetched(credit="Gaia Marenghi & Maciej Bliziński", entities=BOTH)
        self.assertEqual(c.judge(BOTH, f)[0], c.OK)

    def test_bundled_artist_is_merged(self):
        f = c.Fetched(credit="Gaia Marenghi x Maciej Bliziński",
                      entities=["Gaia Marenghi x Maciej Bliziński"])
        self.assertEqual(c.judge(BOTH, f)[0], c.MERGED)

    def test_diacritics_do_not_matter(self):
        f = c.Fetched(entities=["Gaia Marenghi x Maciej Blizinski"])
        self.assertEqual(c.judge(BOTH, f)[0], c.MERGED)

    def test_missing_collaborator(self):
        f = c.Fetched(credit="Maciej Bliziński", entities=["Maciej Bliziński"])
        status, detail = c.judge(BOTH, f)
        self.assertEqual(status, c.MISSING)
        self.assertIn("Gaia Marenghi", detail)

    def test_real_apple_collaboration(self):
        # Apple's lookup for Teminite & Nokae "Burn It Down" (1873885489): the credit line names
        # both artists while the artist ID resolves only to the primary one.
        f = c.Fetched(credit="Teminite & Nokae", entities=["Teminite"])
        self.assertEqual(c.judge(["Teminite", "Nokae"], f)[0], c.OK)

    def test_credit_line_covers_a_primary_only_lookup(self):
        f = c.Fetched(credit="Gaia Marenghi & Maciej Bliziński", entities=["Gaia Marenghi"])
        self.assertEqual(c.judge(BOTH, f)[0], c.OK)

    def test_lenient_service_does_not_flag_missing(self):
        f = c.Fetched(entities=["Maciej Bliziński"], strict=False)
        self.assertEqual(c.judge(BOTH, f)[0], c.OK)

    def test_solo_release_is_ok(self):
        f = c.Fetched(credit="Maciej Bliziński", entities=["Maciej Bliziński"])
        self.assertEqual(c.judge(["Maciej Bliziński"], f)[0], c.OK)

    def test_extra_artist_is_not_a_problem(self):
        f = c.Fetched(entities=["Maciej Bliziński", "Zoe Hayter"])
        self.assertEqual(c.judge(["Maciej Bliziński"], f)[0], c.OK)


class TestFrontMatter(unittest.TestCase):
    def test_reads_artists_and_links(self):
        fm = c.parse_front_matter(
            "---\ntitle: X\nartist:\n- Gaia Marenghi\n- Maciej Bliziński\nlinks:\n"
            "  spotify_album: abc\n  apple_music_album: '123'\n---\nbody\n")
        self.assertEqual(fm["artist"], BOTH)
        self.assertEqual(fm["links"], {"spotify_album": "abc", "apple_music_album": "123"})

    def test_non_yaml_front_matter_is_skipped(self):
        self.assertIsNone(c.parse_front_matter("+++\ntitle = 'x'\n+++\n"))


class TestCache(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = pathlib.Path(self.tmp.name) / "sub" / "cache.json"
        self.now = [1000.0]
        self.calls = []

        def fetch(rid):
            self.calls.append(rid)
            return c.Fetched(credit="Maciej Bliziński", entities=["Maciej Bliziński"])

        self.registry = {"fake": ("Fake", lambda links: links.get("fake"), fetch)}
        self.releases = [("one", {"artist": ["Maciej Bliziński"], "links": {"fake": "A1"}}),
                         ("two", {"artist": ["Maciej Bliziński"], "links": {}})]

    def tearDown(self):
        self.tmp.cleanup()

    def cache(self, **kw):
        return c.Cache(path=self.path, clock=lambda: self.now[0], **kw)

    def run_check(self, cache):
        out = c.check(self.releases, ["fake"], cache, delay=0, registry=self.registry)
        cache.save()
        return out

    def test_second_run_uses_the_cache(self):
        self.run_check(self.cache())
        results, counts = self.run_check(self.cache())
        self.assertEqual(self.calls, ["A1"])
        self.assertEqual(counts, {"fetched": 0, "cached": 1})
        self.assertEqual([(r.slug, r.status) for r in results], [("one", c.OK)])

    def test_entry_expires_after_the_ttl(self):
        self.run_check(self.cache(ttl_hours=1))
        self.now[0] += 3601
        self.run_check(self.cache(ttl_hours=1))
        self.assertEqual(self.calls, ["A1", "A1"])

    def test_refresh_and_no_cache_fetch_again(self):
        self.run_check(self.cache())
        self.run_check(self.cache(refresh=True))
        self.run_check(self.cache(enabled=False))
        self.assertEqual(self.calls, ["A1", "A1", "A1"])

    def test_no_cache_writes_nothing(self):
        self.run_check(self.cache(enabled=False))
        self.assertFalse(self.path.exists())

    def test_failed_lookups_are_not_cached(self):
        def broken(rid):
            raise LookupError("not found")
        registry = {"fake": ("Fake", lambda links: links.get("fake"), broken)}
        cache = self.cache()
        results, _ = c.check(self.releases, ["fake"], cache, delay=0, registry=registry)
        cache.save()
        self.assertEqual([(r.slug, r.status) for r in results], [("one", c.UNKNOWN)])
        self.assertEqual(self.cache().entries, {})

    def test_cached_result_keeps_its_verdict(self):
        merged = c.Fetched(credit="A x B", entities=["A x B"])
        cache = self.cache()
        cache.put("fake:A1", merged)
        cache.save()
        releases = [("one", {"artist": ["A", "B"], "links": {"fake": "A1"}})]
        results, _ = c.check(releases, ["fake"], self.cache(), delay=0, registry=self.registry)
        self.assertEqual([r.status for r in results], [c.MERGED])
        self.assertEqual(self.calls, [])


    def test_cache_from_an_older_format_is_ignored(self):
        cache = self.cache()
        cache.put("fake:A1", c.Fetched(credit="x"))
        cache.entries["fake:A1"]["v"] = c.CACHE_VERSION - 1
        self.assertIsNone(cache.get("fake:A1"))


CREDITS = [{"name": "Gaia Marenghi", "roles": ["music", "lyrics", "vocals"]},
           {"name": "Maciej Bliziński", "roles": ["music", "producer", "bass"]},
           {"name": "Riccardo Marenghi", "roles": ["drums"]}]


class TestSongwriters(unittest.TestCase):
    def test_only_writing_roles_count(self):
        self.assertEqual(c.songwriters(CREDITS), BOTH)

    def test_both_songwriters_shown_is_ok(self):
        f = c.Fetched(composers=["Gaia Marenghi & Maciej Bliziński"])
        self.assertEqual(c.judge_songwriters(CREDITS, f), (c.OK, ""))

    def test_missing_songwriter(self):
        f = c.Fetched(composers=["Gaia Marenghi"])
        self.assertEqual(c.judge_songwriters(CREDITS, f), (c.MISSING, "Maciej Bliziński"))

    def test_no_composer_shown_at_all(self):
        self.assertEqual(c.judge_songwriters(CREDITS, c.Fetched(composers=[]))[0], c.MISSING)

    def test_diacritics_do_not_matter(self):
        f = c.Fetched(composers=["Gaia Marenghi, Maciej Blizinski"])
        self.assertEqual(c.judge_songwriters(CREDITS, f), (c.OK, ""))

    def test_nothing_to_compare_gives_no_verdict(self):
        self.assertIsNone(c.judge_songwriters(CREDITS, c.Fetched(composers=None)))
        self.assertIsNone(c.judge_songwriters([{"name": "X", "roles": ["drums"]}], c.Fetched(composers=[])))
        self.assertIsNone(c.judge_songwriters([], c.Fetched(composers=[])))

    def test_credits_are_read_from_front_matter(self):
        fm = c.parse_front_matter(
            "---\ntitle: X\nartist:\n- A\ncredits:\n- name: Gaia Marenghi\n  roles:\n  - music\n"
            "  - vocals\n- name: Riccardo Marenghi\n  roles:\n  - drums\nlinks:\n  spotify_album: s\n---\n")
        self.assertEqual(fm["credits"], [{"name": "Gaia Marenghi", "roles": ["music", "vocals"]},
                                         {"name": "Riccardo Marenghi", "roles": ["drums"]}])
        self.assertEqual(fm["links"], {"spotify_album": "s"})

    def page(self, composers):
        tracks = ",".join('{"composer": "%s"}' % x for x in composers)
        return ('<html><script type="application/json" id="serialized-server-data">'
                '{"data": [{"tracks": [%s]}]}</script></html>' % tracks)

    def with_page(self, html):
        orig = c.get
        c.get = lambda url: html
        self.addCleanup(setattr, c, "get", orig)

    def test_apple_page_composer_is_read(self):
        self.with_page(self.page(["Gaia Marenghi & Maciej Bliziński", "Gaia Marenghi & Maciej Bliziński"]))
        self.assertEqual(c.apple_composers("1"), ["Gaia Marenghi & Maciej Bliziński"])

    def test_apple_page_without_composer_is_empty_not_unknown(self):
        self.with_page(self.page([]))
        self.assertEqual(c.apple_composers("1"), [])

    def test_unreadable_apple_page_is_unknown(self):
        self.with_page("<html>no data</html>")
        self.assertIsNone(c.apple_composers("1"))


class TestQobuz(unittest.TestCase):
    BASE = "https://www.qobuz.com/us-en/album/%s/xwhg4gjlc762f"

    def test_bundled_artist_in_the_slug_is_merged(self):
        f = c.fetch_qobuz(self.BASE % "11ell-11eaven-gaia-marenghi-x-maciej-blizinski")
        self.assertEqual(f.source, "URL slug")
        self.assertEqual(c.judge(BOTH, f)[0], c.MERGED)

    def test_ampersand_in_the_slug_is_a_collaboration(self):
        f = c.fetch_qobuz(self.BASE % "loser-gaia-marenghi-amp-maciej-blizinski")
        self.assertEqual(c.judge(BOTH, f)[0], c.OK)

    def test_slug_without_the_second_artist_is_missing(self):
        f = c.fetch_qobuz(self.BASE % "loser-gaia-marenghi")
        self.assertEqual(c.judge(BOTH, f)[0], c.MISSING)

    def test_qobuz_is_never_fetched_over_the_network(self):
        orig = c.get
        c.get = lambda url: self.fail("network call: " + url)
        try:
            c.fetch_qobuz(self.BASE % "loser-gaia-marenghi")
        finally:
            c.get = orig


class TestReport(unittest.TestCase):
    def results(self):
        fm = {"title": "11ell 11eaven", "artist": BOTH, "isrc": "QT1",
              "links": {"qobuz": "https://www.qobuz.com/us-en/album/a-gaia-marenghi-x-maciej-blizinski/x",
                        "apple_music_album": "1", "tidal": "https://tidal.com/album/1"}}
        solo = {"title": "Loser", "artist": BOTH, "links": {"apple_music_album": "2"}}
        merged = c.Fetched(credit="Gaia Marenghi x Maciej Bliziński",
                           entities=["Gaia Marenghi x Maciej Bliziński"], ids=["9"])
        good = c.Fetched(credit="Gaia Marenghi & Maciej Bliziński", entities=BOTH, ids=["11", "22"])
        return [
            c.Result("11ell", fm, "apple", c.MERGED, merged.entities[0], merged),
            c.Result("11ell", fm, "qobuz", c.MERGED, "x", c.fetch_qobuz(fm["links"]["qobuz"])),
            c.Result("loser", solo, "apple", c.OK, "", good),
        ]

    def report(self):
        return c.format_report(self.results(), ["apple", "qobuz"], {"fetched": 3, "cached": 0},
                               today="2026-11-11")

    def test_lists_problems_with_link_shows_and_expected(self):
        text = self.report()
        self.assertIn("PROBLEM, Apple Music: one combined artist", text)
        self.assertIn("Link: https://music.apple.com/us/album/1", text)
        self.assertIn('Shows: "Gaia Marenghi x Maciej Bliziński"', text)
        self.assertIn("Expected: Gaia Marenghi (existing Apple artist ID 11) and "
                      "Maciej Bliziński (existing Apple artist ID 22)", text)

    def test_qobuz_problem_says_it_is_url_evidence(self):
        self.assertIn("only the artist words in the Qobuz link", self.report())

    def test_correct_and_unchecked_services_are_listed(self):
        text = self.report()
        self.assertIn("Correct: Apple Music", text)
        self.assertIn("Not checked", text)
        self.assertIn("Tidal", text)

    def test_correct_qobuz_is_marked_as_link_only(self):
        fm = {"title": "T", "artist": BOTH, "links": {"qobuz": "https://www.qobuz.com/us-en/album/t-gaia-marenghi-amp-maciej-blizinski/x"}}
        f = c.fetch_qobuz(fm["links"]["qobuz"])
        text = c.format_report([c.Result("t", fm, "qobuz", c.OK, "", f)], ["qobuz"],
                               {"fetched": 1, "cached": 0}, today="2026-11-11")
        self.assertIn("Correct: Qobuz (from the link only)", text)

    def test_songwriter_problem_is_listed_with_link_shows_and_expected(self):
        fm = {"title": "T", "artist": BOTH, "credits": CREDITS, "links": {"apple_music_album": "7"}}
        f = c.Fetched(credit="Gaia Marenghi & Maciej Bliziński", entities=BOTH, composers=["Gaia Marenghi"])
        res = c.Result("t", fm, "apple", c.OK, "", f, songwriters=c.judge_songwriters(CREDITS, f))
        text = c.format_report([res], ["apple"], {"fetched": 1, "cached": 0}, today="2026-11-11")
        self.assertIn("PROBLEM, Apple Music songwriter credit: no credit for Maciej Bliziński", text)
        self.assertIn('Shows: "Gaia Marenghi"', text)
        self.assertIn("Expected: Gaia Marenghi, Maciej Bliziński", text)
        self.assertIn("1 problem(s) found", text)
        self.assertTrue(res.problem)

    def test_correct_songwriter_credit_is_listed_as_correct(self):
        fm = {"title": "T", "artist": BOTH, "credits": CREDITS, "links": {"apple_music_album": "7"}}
        f = c.Fetched(credit="Gaia Marenghi & Maciej Bliziński", entities=BOTH,
                      composers=["Gaia Marenghi & Maciej Bliziński"])
        res = c.Result("t", fm, "apple", c.OK, "", f, songwriters=c.judge_songwriters(CREDITS, f))
        text = c.format_report([res], ["apple"], {"fetched": 1, "cached": 0}, today="2026-11-11")
        self.assertIn("Correct: Apple Music, Apple Music songwriter credit", text)
        self.assertFalse(res.problem)

    def test_report_is_plain_lists_without_table_drawing(self):
        text = self.report()
        for ch in "|+=":
            self.assertNotIn(ch, text.replace("Gaia Marenghi + Maciej", ""))


class TestConfig(unittest.TestCase):
    def test_missing_config_is_empty(self):
        self.assertEqual(c.load_config("/nonexistent/config.json"), {})

    def test_shipped_config_names_real_releases(self):
        config = c.load_config()
        self.assertTrue(config["releases"])
        found = [slug for slug, _ in c.load_releases(config["releases"])]
        self.assertEqual(found, config["releases"])
        self.assertTrue(set(config["services"]) <= set(c.SERVICES))

    def test_releases_keep_the_configured_order(self):
        found = [slug for slug, _ in c.load_releases(["river", "loser"])]
        self.assertEqual(found, ["river", "loser"])


class TestRepo(unittest.TestCase):
    def test_every_release_with_links_parses(self):
        releases = c.load_releases()
        self.assertTrue(releases)
        for slug, fm in releases:
            self.assertTrue(fm["artist"], slug)


if __name__ == "__main__":
    unittest.main()
