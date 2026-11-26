#!/usr/bin/env python3
"""Verify public KamAZ/Volvo overview does not claim exhaustive linked code lists."""
import ast
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
issues = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.description = []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and (d.get("name") == "description" or d.get("property") == "og:description"):
            self.description.append(d.get("content", ""))


for slug, phrase in (("kamaz", "а не все коды базы"),
                     ("volvo", "а не полный перечень записей")):
    html = (ROOT / "marki" / (slug + ".html")).read_text(encoding="utf-8")
    page = Page()
    page.feed(html)
    if phrase not in html:
        issues.append(f"{slug}: explicit preview scope missing")
    if len(page.description) != 2 or any("Все коды неисправностей" in x for x in page.description):
        issues.append(f"{slug}: misleading or missing description")
    if "ниже весь список по системам" in html:
        issues.append(f"{slug}: exhaustive list claim returned")
    if "name=\"b\" value=\"" + slug + "\"" not in html:
        issues.append(f"{slug}: brand-specific search lost")
    if page.h1 != 1:
        issues.append(f"{slug}: expected one h1")
generator = (ROOT / "scripts" / "build_pages.py").read_text(encoding="utf-8")
for keyword in ("if b == 'kamaz':", "elif b == 'volvo':",
                "а не все коды базы", "а не полный перечень записей"):
    if keyword not in generator:
        issues.append("Generator missing: " + keyword)
try:
    ast.parse(generator)
except SyntaxError as exc:
    issues.append("Generator syntax error: " + str(exc))
for issue in issues:
    print("FAIL:", issue)
if not issues:
    print("PASS: KamAZ/Volvo landing scope, search filters, and generator")
sys.exit(bool(issues))
