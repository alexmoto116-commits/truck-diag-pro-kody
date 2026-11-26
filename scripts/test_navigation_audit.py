#!/usr/bin/env python3
"""Regression tests for local vs external links in SEO navigation audit."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_static_seo as seo


class LinkResolutionTests(unittest.TestCase):
    def setUp(self):
        self.src = seo.ROOT / "marki" / "example.html"

    def test_self_domain_absolute(self):
        self.assertEqual(seo.local_link_target(self.src, "https://codetruck.ru/marki/"), seo.ROOT / "marki")

    def test_self_domain_protocol_relative(self):
        self.assertEqual(seo.local_link_target(self.src, "//codetruck.ru/kody/spn-91.html"),
                         seo.ROOT / "kody" / "spn-91.html")

    def test_relative_path(self):
        self.assertEqual(seo.local_link_target(self.src, "../kody/spn-91.html"),
                         self.src.parent / ".." / "kody" / "spn-91.html")

    def test_encoded_path_and_query(self):
        self.assertEqual(seo.local_link_target(self.src, "/marki/%66ord.html?test=1#codes"),
                         seo.ROOT / "marki" / "ford.html")

    def test_external_links_ignored(self):
        for url in ("https://example.net/missing", "//example.net/foo",
                    "mailto:help@example.net", "tel:+123", "javascript:void(0)", "#example"):
            self.assertIsNone(seo.local_link_target(self.src, url), url)


if __name__ == "__main__":
    unittest.main()
