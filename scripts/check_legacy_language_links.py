#!/usr/bin/env python3
"""Verify retired-language 404 stays local and is not indexable."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "404.html").read_text(encoding="utf-8")
errors = []
if "dieselcodes.com" in html.lower() or "dieselcodes" in html.lower():
    errors.append("Cross-site migration reference returned to CodeTruck 404")
if '<meta name="robots" content="noindex">' not in html:
    errors.append("404 must remain noindex")
if '<a href="/"' not in html and 'href="https://codetruck.ru/"' not in html:
    errors.append("404 needs a working route back to its own homepage")
if 'name="q"' not in html and 'id="pf-code"' not in html:
    errors.append("404 no longer exposes local code search")
for err in errors:
    print("FAIL:", err)
if not errors:
    print("PASS: self-contained, noindex 404 without cross-domain move links")
sys.exit(bool(errors))
