#!/usr/bin/env python3
"""Read-only validation of the CodeTruck RU SPN indexing allowlist.

Run from repository root:
    python scripts/audit_index_policy.py

Does NOT change index_keep.json, sitemap files, HTML, or deployment.
"""
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "scripts" / "index_keep.json"
SITEMAP = ROOT / "sitemap-ru-kody.xml"
URL_PREFIX = "https://codetruck.ru/kody/"
SPN_PAGE = re.compile(r"^kody/spn-\d+\.html$")
META_NOINDEX = re.compile(
    r'<meta\s+[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
    re.IGNORECASE,
)


def main():
    errors = []
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    kept = [p for p in data["страницы"] if SPN_PAGE.fullmatch(p)]
    if len(kept) != len(set(kept)):
        errors.append("Duplicate RU code URL in allowlist")
    allowed = set(kept)
    tree = ET.parse(SITEMAP)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = [
        e.text.strip() for e in tree.findall(".//s:url/s:loc", ns) if e.text
    ]
    listed = set()
    for url in sitemap_urls:
        if not url.startswith(URL_PREFIX):
            errors.append(f"Unexpected URL in RU codes sitemap: {url}")
            continue
        rel = "kody/" + url[len(URL_PREFIX):]
        if not SPN_PAGE.fullmatch(rel):
            errors.append(f"Unexpected path in RU codes sitemap: {rel}")
        listed.add(rel)
    if len(sitemap_urls) != len(set(sitemap_urls)):
        errors.append("Duplicate URLs in RU codes sitemap")
    if allowed != listed:
        errors.append(f"In allowlist but not sitemap: {len(allowed - listed)}")
        errors.append(f"In sitemap but not allowlist: {len(listed - allowed)}")
        for path in sorted(allowed ^ listed)[:20]:
            errors.append(f"URL set mismatch: {path}")

    checked = 0
    code_dir = ROOT / "kody"
    for path in sorted(code_dir.glob("spn-*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if not SPN_PAGE.fullmatch(rel):
            continue
        checked += 1
        content = path.read_text(encoding="utf-8")
        noindex = bool(META_NOINDEX.search(content))
        if (rel in allowed) == noindex:
            errors.append(f"Index policy mismatch: {rel} (allowed={rel in allowed}, noindex={noindex})")
    for rel in allowed:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing allowlisted HTML file: {rel}")

    print(f"RU SPN HTML pages checked: {checked}")
    print(f"RU allowlisted SPN pages: {len(allowed)}")
    print(f"RU code sitemap entries: {len(sitemap_urls)}")
    if errors:
        print("\n".join("FAIL: " + e for e in errors[:100]))
        if len(errors) > 100:
            print(f"...and {len(errors) - 100} more issues")
        return 1
    print("PASS: RU SPN index allowlist, sitemap, and HTML noindex match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
