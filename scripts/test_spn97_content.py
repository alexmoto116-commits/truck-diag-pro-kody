#!/usr/bin/env python3
"""Read-only regression for SPN 97 code-specific copy, visible HTML and JSON-LD.

Does not require private dealer data or change index policy.
"""
import ast
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "kody" / "spn-97.html").read_text(encoding="utf-8")
gen = (ROOT / "scripts" / "build_pages.py").read_text(encoding="utf-8")
issues = []


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.description = []
        self.structured = []
        self._json = False
        self._parts = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta" and (d.get("name") == "description" or d.get("property") == "og:description"):
            self.description.append(d.get("content", ""))
        if tag == "script" and d.get("type") == "application/ld+json":
            self._json = True
            self._parts = []

    def handle_data(self, data):
        if self._json:
            self._parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._json:
            self.structured.append(json.loads("".join(self._parts)))
            self._json = False


scan = Scan()
scan.feed(html)
faq = [x for x in scan.structured if x.get("@type") == "FAQPage"]
answers = [q.get("acceptedAnswer", {}).get("text", "") for item in faq
           for q in item.get("mainEntity", [])]
if not any("По одному SPN 97 нельзя подтвердить безопасность" in a for a in answers):
    issues.append("Structured FAQ driving advice still unconditional")
if not any("Электрические FMI" in a for a in answers):
    issues.append("Structured FAQ does not distinguish electrical FMI")
if not all("Проверка FMI" in d for d in scan.description):
    issues.append("SEO descriptions not aligned")
if '<b>По одному SPN 97 нельзя подтвердить безопасность движения.</b>' not in html:
    issues.append("Visible driving warning missing")
if "Уточнение к ролику:" not in html:
    issues.append("Old video transcript requires a correction note")
if "Топливо приходит не в том количестве или не под тем давлением" in html:
    issues.append("Generic fuel-pressure scenario returned")
if "'no_elec_note': True" not in gen or "    97: {" not in gen:
    issues.append("Generator-specific SPN 97 override missing")
try:
    ast.parse(gen)
except SyntaxError as exc:
    issues.append(f"Generator syntax error: {exc}")
for issue in issues:
    print("FAIL:", issue)
if not issues:
    print("PASS: SPN 97 safety and diagnostic content is consistent")
sys.exit(bool(issues))
