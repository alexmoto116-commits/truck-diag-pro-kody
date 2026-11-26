#!/usr/bin/env python3
"""SPN 91 content consistency guard: visible HTML, SEO snippets and JSON-LD.

Checks output copy and generator override without rebuilding the private code DB.
"""
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "kody" / "spn-91.html").read_text(encoding="utf-8")
GEN = (ROOT / "scripts" / "build_pages.py").read_text(encoding="utf-8")
FAIL = []


class PageReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.visible = []
        self.description = []
        self.structured = []
        self.in_json = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "script" and data.get("type") == "application/ld+json":
            self.in_json = True
        if tag == "meta" and (data.get("name") == "description" or data.get("property") == "og:description"):
            self.description.append(data.get("content", ""))

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_json = False

    def handle_data(self, data):
        if self.in_json:
            self.structured.append(json.loads(data))
        else:
            self.visible.append(data)


p = PageReader()
p.feed(PAGE)
visible = " ".join(p.visible)
faq = [x for x in p.structured if x.get("@type") == "FAQPage"]
if len(faq) != 1:
    FAIL.append("Expected exactly one FAQPage")
else:
    answers = [q.get("acceptedAnswer", {}).get("text", "") for q in faq[0].get("mainEntity", [])]
    if not any("По одному SPN 91 нельзя определить" in x for x in answers):
        FAIL.append("JSON-LD driving FAQ not updated")
for name, text in [("visible page", visible), ("SEO descriptions", " ".join(p.description)),
                   ("FAQ answers", " ".join(answers) if faq else "")]:
    for phrase in ("Обычно ехать можно", "Можно доехать до сервиса", "Ехать можно, следить самому"):
        if phrase in text:
            FAIL.append(f"{name} still claims: {phrase}")
if "По одному SPN 91 нельзя определить, безопасно ли движение" not in visible:
    FAIL.append("Visible SPN 91 caution missing")
if "91: {" not in GEN or "'no_elec_note': True" not in GEN:
    FAIL.append("SPN 91 generator override missing")
if FAIL:
    for issue in FAIL:
        print("FAIL:", issue)
    sys.exit(1)
print("PASS: SPN 91 HTML, SEO and FAQ agree on pedal-response warning")
