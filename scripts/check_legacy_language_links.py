#!/usr/bin/env python3
"""Read-only regression guard for retired language paths on CodeTruck 404."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "404.html").read_text(encoding="utf-8")
errors = []
for locale in ("en", "pl", "de", "fr", "es", "it", "pt", "cs", "sk"):
    if not re.search(r"\b" + locale + r"\b", html):
        errors.append("Missing legacy language route or message: " + locale)
for term in ("https://dieselcodes.com/", "a.href = 'https://dieselcodes.com/'",
             "document.body.appendChild(d)", "Ta wersja strony została przeniesiona"):
    if term not in html:
        errors.append("Missing language-move notice/link: " + term)
if 'rel="nofollow"' in html[html.find("Old translated paths are retired"):]:
    errors.append("Do not apply nofollow to the relocation link")
for item in errors:
    print("FAIL:", item)
if not errors:
    print("PASS: language notice and clickable DieselCodes destination")
sys.exit(1 if errors else 0)
