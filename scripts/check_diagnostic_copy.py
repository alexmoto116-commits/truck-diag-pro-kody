#!/usr/bin/env python3
"""Regression checks for safety-critical wording in published static pages.

Run after site generation:
    python scripts/check_diagnostic_copy.py

These are copy-level safeguards, not a medical/mechanical validation of all advice.
"""
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "build_pages.py"
NO_START = ROOT / "problemy" / "ne-zavoditsya.html"


def main() -> int:
    errors = []
    try:
        ast.parse(GENERATOR.read_text(encoding="utf-8"), filename=str(GENERATOR))
    except SyntaxError as exc:
        errors.append(f"Generator has a Python syntax error: {exc}")
    generator = GENERATOR.read_text(encoding="utf-8")
    page = NO_START.read_text(encoding="utf-8")
    if "slug != 'ne-zavoditsya'" not in generator:
        errors.append("Generator no longer excludes no-start from generic risk section")
    if "if slug == 'ne-zavoditsya':" not in generator:
        errors.append("Generator no longer provides specific no-start advice")
    required = (
        "Если двигатель не заводится",
        "не продолжайте",
        "Что проверить безопасно",
    )
    for term in required:
        if term.casefold() not in page.casefold():
            errors.append(f"Missing on no-start page: {term}")
    forbidden = (
        "лучше доехать не глуша двигатель",
        "Среди кодов этой части справочник не отмечает таких, при которых нельзя ехать",
    )
    for term in forbidden:
        if term.casefold() in page.casefold():
            errors.append(f"Misleading no-start advice returned: {term}")
    if errors:
        print("\n".join("FAIL: " + error for error in errors))
        return 1
    print("PASS: no-start page and generator safety-copy regression checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
