#!/usr/bin/env python3
"""SPN 1761/792 page and structured-data consistency, without private code data."""
import ast
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
GEN = (ROOT / "scripts/build_pages.py").read_text(encoding="utf-8")
errors = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_json = False
        self.js = []
        self.parsed = []
        self.meta = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "script" and d.get("type") == "application/ld+json":
            self.in_json = True
            self.js = []
        if tag == "meta" and (d.get("name") == "description" or d.get("property") == "og:description"):
            self.meta.append(d.get("content", ""))

    def handle_data(self, data):
        if self.in_json:
            self.js.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json:
            self.parsed.append(json.loads("".join(self.js)))
            self.in_json = False


tests = {
    1761: {
        "expected": "По одному SPN 1761 нельзя определить, безопасно ли продолжать движение.",
        "forbidden": ["Посреди трассы машина не заглохнет", "Дозирование мочевины прервано, и блок"],
        "badge": "Проверьте уровень AdBlue",
        "meta": "ошибки датчика",
    },
    792: {
        "expected": "Сам по себе SPN 792 не подтверждает исправность рабочих тормозов.",
        "forbidden": ["обычные тормоза работают", "обычные тормоза при этом действуют"],
        "badge": "Проверьте тормозную систему",
        "meta": "предупреждения тормозов",
    },
}
for spn, checks in tests.items():
    page = (ROOT / f"kody/spn-{spn}.html").read_text(encoding="utf-8")
    parser = Page()
    parser.feed(page)
    faq = [x for x in parser.parsed if x.get("@type") == "FAQPage"]
    articles = [x for x in parser.parsed if x.get("@type") == "TechArticle"]
    answers = [q.get("acceptedAnswer", {}).get("text", "")
               for item in faq for q in item.get("mainEntity", [])]
    if checks["expected"] not in page:
        errors.append(f"{spn}: visible driving warning absent")
    if not any(checks["expected"] in a for a in answers):
        errors.append(f"{spn}: driving answer missing from structured FAQ")
    if checks["badge"] not in page:
        errors.append(f"{spn}: correct top warning missing")
    if len(parser.meta) != 2 or not all(checks["meta"] in m for m in parser.meta):
        errors.append(f"{spn}: meta and OG description disagree")
    if len(articles) != 1 or checks["meta"] not in articles[0].get("description", ""):
        errors.append(f"{spn}: TechArticle description disagree")
    for phrase in checks["forbidden"]:
        if phrase in page:
            errors.append(f"{spn}: obsolete unconditional claim: {phrase}")
    if f"    {spn}: {{" not in GEN:
        errors.append(f"{spn}: missing generator override")
if "no_elec_note" not in GEN:
    errors.append("Generator no longer suppresses generic unrelated electrical risk")
try:
    ast.parse(GEN, filename="scripts/build_pages.py")
except SyntaxError as exc:
    errors.append(f"Generator Python syntax error: {exc}")
for err in errors:
    print("FAIL:", err)
if not errors:
    print("PASS: SPN 1761 and 792 visible copy, metadata, FAQ and generator")
sys.exit(bool(errors))
