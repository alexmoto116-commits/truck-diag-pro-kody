#!/usr/bin/env python3
"""Verify SEO scope and contextual WABCO braking links remain in generated pages."""
import ast
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
issues = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.description = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a":
            self.links.append(d.get("href"))
        if tag == "meta" and (d.get("name") == "description" or d.get("property") == "og:description"):
            self.description.append(d.get("content", ""))


wabco = (ROOT / "marki/wabco.html").read_text(encoding="utf-8")
codes = (ROOT / "kody/index.html").read_text(encoding="utf-8")
g = (ROOT / "scripts/build_pages.py").read_text(encoding="utf-8")
a, b = Page(), Page()
a.feed(wabco)
b.feed(codes)
if len(a.description) != 2 or any("Все коды неисправностей" in x for x in a.description):
    issues.append("WABCO SEO metadata still claims all codes are listed")
if "а не все записи базы" not in wabco or "в поиск по WABCO" not in wabco:
    issues.append("WABCO page missing precise scope and filtered-search advice")
if 'name="b" value="wabco"' not in wabco:
    issues.append("WABCO brand filter missing")
if "/marki/wabco.html" not in b.links:
    issues.append("Codes hub lacks a crawlable WABCO context link")
if "разборы ошибок WABCO ABS/ESC" not in codes:
    issues.append("Codes hub missing helpful anchor text")
for token in ("elif b == 'wabco':", "а не все записи базы",
              'href="/marki/wabco.html"'):
    if token not in g:
        issues.append("Generator missing " + token)
try:
    ast.parse(g)
except SyntaxError as exc:
    issues.append("Generator Python syntax error: " + str(exc))
for issue in issues:
    print("FAIL:", issue)
if not issues:
    print("PASS: WABCO context, scope, metadata and regenerated links")
sys.exit(bool(issues))
