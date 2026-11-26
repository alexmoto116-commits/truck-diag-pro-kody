#!/usr/bin/env python3
"""Check that codes catalog doesn't promise an exhaustive list of linked SPNs."""
from html.parser import HTMLParser
from pathlib import Path
import ast
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "kody" / "index.html").read_text(encoding="utf-8")
generator = (ROOT / "scripts" / "build_pages.py").read_text(encoding="utf-8")
issues = []
links = set(re.findall(r'href="(spn-\d+\.html)"', html))
if not links:
    issues.append("Catalog SPN links missing")
if "избранные подробные разборы" not in html:
    issues.append("Scope explanation missing from rendered catalog")
if "Если нужного SPN нет в списке" not in html:
    issues.append("Search fallback missing")
if "Ниже — весь список по системам" in html or "Полный список разобранных кодов" in html:
    issues.append("Catalog still claims an exhaustive list")
if "избранные подробные разборы" not in generator:
    issues.append("Generator will regress catalog scope")
try:
    ast.parse(generator)
except SyntaxError as exc:
    issues.append("Generator syntax error: " + str(exc))
for issue in issues:
    print("FAIL:", issue)
if not issues:
    print(f"PASS: curated catalog described accurately ({len(links)} SPN links)")
sys.exit(bool(issues))
