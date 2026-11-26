#!/usr/bin/env python3
"""SPN 799/802 HTML, FAQ and generator diagnostic regression checks."""
import ast
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
generator = (ROOT / "scripts/build_pages.py").read_text(encoding="utf-8")
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
    799: ("SPN 799 не доказывает, что рабочие тормоза исправны",
          "Неисправность клапана-модулятора",
          "модулятор давления ABS"),
    802: ("По одному SPN 802 нельзя подтвердить безопасность движения",
          "Нарушение питания реле диагонали",
          "реле диагонали тормозной системы ABS/EBS"),
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
        errors.append(f"{spn}: meta descriptions mismatch")
    if len(articles) != 1 or articles[0].get("description") != page.meta[0]:
        errors.append(f"{spn}: TechArticle metadata mismatch")
    if "обычные тормоза работают" in text or "обычные тормоза при этом действуют" in text:
        errors.append(f"{spn}: unconditional braking assurance")
    if f"    {spn}: {{" not in generator:
        errors.append(f"{spn}: generator override missing")
if "Бортовая сеть не держит напряжение" in (ROOT / "kody/spn-802.html").read_text(encoding="utf-8"):
    errors.append("802: generic generator-failure scenario remains")
if "Проверьте напряжение питания ABS/EBS" not in (ROOT / "kody/spn-802.html").read_text(encoding="utf-8"):
    errors.append("802: code-specific inspection missing")
try:
    ast.parse(generator)
except SyntaxError as exc:
    errors.append(f"Generator syntax error: {exc}")
for err in errors:
    print("FAIL:", err)
if not errors:
    print("PASS: SPN 799 and 802 HTML, FAQ, SEO and generator agree")
sys.exit(bool(errors))
