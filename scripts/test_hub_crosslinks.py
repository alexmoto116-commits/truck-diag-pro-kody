#!/usr/bin/env python3
"""Check bidirectional, crawlable links between CodeTruck's two main directories."""
import ast
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "kody/index.html": "/marki/",
    "marki/index.html": "/kody/",
}
GENERATOR = ROOT / "scripts" / "build_pages.py"
issues = []


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.anchors.append(dict(attrs).get("href"))


for page, target in PAGES.items():
    text = (ROOT / page).read_text(encoding="utf-8")
    parser = Links()
    parser.feed(text)
    if target not in parser.anchors:
        issues.append(f"{page} must link to {target} with ordinary HTML anchor")
    target_path = ROOT / target.lstrip("/") / "index.html"
    if not target_path.is_file():
        issues.append(f"Missing target: {target_path.relative_to(ROOT)}")
    if "<h2>" not in text:
        issues.append(f"{page} lost page sections")
g = GENERATOR.read_text(encoding="utf-8")
for anchor in ('href="/marki/"', 'href="/kody/"'):
    if anchor not in g:
        issues.append(f"Generator missing {anchor}")
try:
    ast.parse(g, filename=str(GENERATOR))
except SyntaxError as e:
    issues.append(f"Generator syntax error: {e}")
for issue in issues:
    print("FAIL:", issue)
if not issues:
    print("PASS: bidirectional contextual links from code and make directories")
sys.exit(bool(issues))
