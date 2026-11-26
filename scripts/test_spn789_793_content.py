#!/usr/bin/env python3
"""SPN 789 and 793 safety, metadata, FAQ and generator consistency."""
import ast
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
gen = (ROOT / "scripts/build_pages.py").read_text(encoding="utf-8")
errors = []

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_json = False
        self.buf = []
        self.structured = []
        self.meta = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta" and (d.get("name") == "description" or d.get("property") == "og:description"):
            self.meta.append(d.get("content", ""))
        if tag == "script" and d.get("type") == "application/ld+json":
            self.in_json, self.buf = True, []

    def handle_data(self, data):
        if self.in_json:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json:
            self.structured.append(json.loads("".join(self.buf)))
            self.in_json = False

checks = {
    789: ("SPN 789 сам по себе не подтверждает исправность рабочих тормозов",
          "При неисправности датчика скорости левого колеса первой оси",
          "датчик ABS левого колеса первой оси"),
    793: ("SPN 793 сам по себе не подтверждает исправность рабочих тормозов",
          "Недостоверный сигнал скорости колеса третьей оси",
          "датчик ABS левого колеса третьей оси"),
}
for spn, (verdict, risk, meta) in checks.items():
    text = (ROOT / f"kody/spn-{spn}.html").read_text(encoding="utf-8")
    page = Page()
    page.feed(text)
    articles = [x for x in page.structured if x.get("@type") == "TechArticle"]
    faq = [x for x in page.structured if x.get("@type") == "FAQPage"]
    answers = [q.get("acceptedAnswer", {}).get("text", "")
               for f in faq for q in f.get("mainEntity", [])]
    if verdict not in text or risk not in text:
        errors.append(f"{spn}: visible diagnosis missing")
    if len(answers) < 2 or verdict not in answers[0] or risk not in answers[1]:
        errors.append(f"{spn}: FAQ disagreement")
    if len(page.meta) != 2 or not all(meta in x for x in page.meta):
        errors.append(f"{spn}: SEO metadata mismatch")
    if len(articles) != 1 or articles[0].get("description") != page.meta[0]:
        errors.append(f"{spn}: TechArticle/SEO descriptions disagree")
    for obsolete in ("обычные тормоза работают", "обычные тормоза при этом действуют", "Хватит доехать до базы"):
        if obsolete in text:
            errors.append(f"{spn}: old blanket reassurance: {obsolete}")
    if f"    {spn}: {{" not in gen:
        errors.append(f"{spn}: generator override missing")
if "Уточнение к ролику:" not in (ROOT / "kody/spn-789.html").read_text(encoding="utf-8"):
    errors.append("789: video transcript needs correction note")
try:
    ast.parse(gen)
except SyntaxError as exc:
    errors.append(f"Generator syntax error: {exc}")
for err in errors:
    print("FAIL:", err)
if not errors:
    print("PASS: SPN 789/793 risk, FAQ, SEO meta and generator")
sys.exit(bool(errors))
