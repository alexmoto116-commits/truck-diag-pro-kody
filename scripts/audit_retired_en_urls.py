#!/usr/bin/env python3
"""Read-only inventory of retired English CodeTruck URL references.

This script does NOT change indexing, sitemap, robots, redirects or pages.
Old Google search results are not proof that the URL is currently published.
"""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "scripts" / "index_keep.json"
URL_PREFIX = "https://codetruck.ru/en/"


def report():
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    listed = [p for p in data.get("страницы", []) if p.startswith("en/")]
    existing = [p for p in listed if (ROOT / p).is_file()]
    absent = [p for p in listed if not (ROOT / p).is_file()]
    live_en_files = list((ROOT / "en").rglob("*.html")) if (ROOT / "en").exists() else []
    sitemap_en = []
    for path in ROOT.glob("sitemap*.xml"):
        try:
            root = ET.parse(path).getroot()
        except (ET.ParseError, OSError):
            continue
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        for node in root.findall(".//" + ns + "loc"):
            if node.text and node.text.strip().startswith(URL_PREFIX):
                sitemap_en.append(node.text.strip())
    return {
        "legacy_en_allowlist_entries": len(listed),
        "legacy_en_allowlist_existing_files": len(existing),
        "legacy_en_allowlist_missing_files": len(absent),
        "en_html_files_in_repository": len(live_en_files),
        "en_urls_in_current_root_sitemaps": len(sitemap_en),
        "note": "Historical allowlist entries are not an instruction to publish or index these URLs. Validate HTTP 404 and Google Search Console separately.",
    }


if __name__ == "__main__":
    print(json.dumps(report(), ensure_ascii=False, indent=2))
