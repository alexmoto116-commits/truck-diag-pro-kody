#!/usr/bin/env python3
"""Regression test: SPN 100/110 warning copy, structured data and generator."""
import ast
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
GEN = (ROOT / "scripts/build_pages.py").read_text(encoding="utf-8")
errors = []

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_json = False
        self.buf = []
        self.structured = []
        self.descriptions = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "script" and d.get("type") == "application/ld+json":
            self.in_json, self.buf = True, []
        if tag == "meta" and (d.get("name") == "description" or d.get("property") == "og:description"):
            self.descriptions.append(d.get("content", ""))

    def handle_data(self, data):
        if self.in_json:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json:
            self.structured.append(json.loads("".join(self.buf)))
            self.in_json = False

tests = {
    100: ("При предупреждении о низком давлении масла", "Электрический FMI может указывать на цепь датчика",
          "Само давление, скорее всего, в норме"),
    110: ("При признаках перегрева", "Ошибка цепи датчика способна давать недостоверные показания",
          "Код электрический: врёт датчик"),
}
for spn, (warning, risk, obsolete) in tests.items():
    page = (ROOT / f"kody/spn-{spn}.html").read_text(encoding="utf-8")
    parsed = Page()
    parsed.feed(page)
    faq = [o for o in parsed.structured if o.get("@type") == "FAQPage"]
    article = [o for o in parsed.structured if o.get("@type") == "TechArticle"]
    answers = [q.get("acceptedAnswer", {}).get("text", "")
               for f in faq for q in f.get("mainEntity", [])]
    if warning not in page or risk not in page:
        errors.append(f"{spn}: warning/risk missing")
    if len(answers) < 2 or warning not in answers[0] or risk not in answers[1]:
        errors.append(f"{spn}: structured FAQ not updated")
    if len(parsed.descriptions) != 2 or not all(f"SPN {spn}" in s for s in parsed.descriptions):
        errors.append(f"{spn}: SEO descriptions inconsistent")
    if len(article) != 1 or article[0].get("description") != parsed.descriptions[0]:
        errors.append(f"{spn}: TechArticle/SEO descriptions disagree")
    if obsolete in page:
        errors.append(f"{spn}: obsolete unconditional reassurance returned")
    if not re.search(rf"    {spn}: \{{[\s\S]*?'no_elec_note': True", GEN):
        errors.append(f"{spn}: generator does not suppress misleading generic electrical note")
try:
    ast.parse(GEN)
except SyntaxError as exc:
    errors.append(f"Generator syntax error: {exc}")
for err in errors:
    print("FAIL:", err)
if not errors:
    print("PASS: SPN 100/110 warning copy, FAQ, SEO meta and generator")
sys.exit(bool(errors))
