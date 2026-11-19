import pathlib
import unittest

from geo_audit import audit_html, robots_blocks

SAMPLE = (pathlib.Path(__file__).parent / "examples" / "sample.html").read_text()


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.report = audit_html("https://acme-lighting.test/", SAMPLE,
                                 robots_txt="User-agent: GPTBot\nDisallow: /\n",
                                 llms_txt_found=False)
        self.checks = {c.id: c for c in self.report.checks}

    def test_detects_core_seo_signals(self):
        self.assertTrue(self.checks["title"].passed)
        self.assertTrue(self.checks["single_h1"].passed)
        self.assertTrue(self.checks["canonical"].passed)
        self.assertFalse(self.checks["image_alt"].passed)  # one image has no alt

    def test_detects_geo_signals(self):
        self.assertTrue(self.checks["entity_schema"].passed)
        self.assertTrue(self.checks["faq_or_qa"].passed)
        self.assertFalse(self.checks["ai_crawlers_allowed"].passed)
        self.assertIn("GPTBot", self.checks["ai_crawlers_allowed"].detail)

    def test_scores_are_percentages(self):
        for s in (self.report.seo_score, self.report.geo_score):
            self.assertGreaterEqual(s, 0)
            self.assertLessEqual(s, 100)


class RobotsTests(unittest.TestCase):
    def test_wildcard_block(self):
        self.assertTrue(robots_blocks("User-agent: *\nDisallow: /", "ClaudeBot"))

    def test_specific_allow_overrides(self):
        txt = "User-agent: *\nDisallow: /\n\nUser-agent: ClaudeBot\nAllow: /\n"
        self.assertFalse(robots_blocks(txt, "ClaudeBot"))

    def test_partial_disallow_is_not_block(self):
        self.assertFalse(robots_blocks("User-agent: *\nDisallow: /admin", "GPTBot"))


if __name__ == "__main__":
    unittest.main()
