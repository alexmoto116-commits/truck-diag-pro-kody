#!/usr/bin/env python3
"""Read-only static HTML SEO audit. No network and no third-party packages.

Usage:
    python scripts/audit_static_seo.py
    python scripts/audit_static_seo.py --json seo-audit-results.json

Review findings before changing robots/noindex, sitemap, or publishing pages.
"""
import argparse
import collections
import html
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", ".venv", "venv", "__pycache__"}
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts = []
        self.in_title = False
        self.canonicals = []
        self.robots = []
        self.links = []
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "link" and "canonical" in data.get("rel", "").lower().split():
            self.canonicals.append(data.get("href", ""))
        if tag == "meta" and data.get("name", "").lower() == "robots":
            self.robots.append(data.get("content", ""))
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self):
        return " ".join(" ".join(self.title_parts).split())


def parse_xml_sitemap(path):
    try:
        tree = ET.parse(path)
    except (ET.ParseError, OSError) as exc:
        return [], [], str(exc)
    root = tree.getroot()
    urls = [e.text.strip() for e in root.findall(".//" + SITEMAP_NS + "url/" + SITEMAP_NS + "loc") if e.text]
    children = [e.text.strip() for e in root.findall(".//" + SITEMAP_NS + "sitemap/" + SITEMAP_NS + "loc") if e.text]
    return urls, children, None


def local_path_from_url(url):
    parsed = urlparse(url)
    rel = unquote(parsed.path).lstrip("/")
    if not rel or rel.endswith("/"):
        rel += "index.html"
    return ROOT / rel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_out", help="Write machine-readable results")
    args = parser.parse_args()
    pages = {}
    issues = []
    def add(kind, path, detail):
        issues.append({"type": kind, "path": str(path), "detail": detail})

    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP for part in path.relative_to(ROOT).parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
            p = PageParser()
            p.feed(content)
        except (OSError, UnicodeError, ValueError) as exc:
            add("html_parse_error", rel, str(exc))
            continue
        noindex = any("noindex" in x.lower() for x in p.robots)
        pages[rel] = {"title": p.title, "canonical": p.canonicals, "noindex": noindex,
                      "links": p.links, "h1_count": p.h1_count}
        if not p.title:
            add("missing_title", rel, "")
        if p.h1_count != 1:
            add("h1_count", rel, str(p.h1_count))
        if len(p.canonicals) != 1:
            add("canonical_count", rel, str(len(p.canonicals)))
        if not noindex and not p.title:
            add("indexable_without_title", rel, "")

    title_owners = collections.defaultdict(list)
    for rel, data in pages.items():
        if not data["noindex"] and data["title"]:
            title_owners[data["title"].casefold()].append(rel)
    for title, owners in title_owners.items():
        if len(owners) > 1:
            add("duplicate_indexable_title", ", ".join(owners[:10]), title[:120])

    for rel, data in pages.items():
        path = ROOT / rel
        for href in data["links"]:
            if href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue
            u = urlparse(href)
            if u.scheme or u.netloc:
                continue
            dest = (ROOT / u.path.lstrip("/")) if href.startswith("/") else (path.parent / u.path)
            if u.path and not dest.exists() and not (dest / "index.html").exists():
                add("missing_internal_link", rel, href)
        for canonical in data["canonical"]:
            u = urlparse(canonical)
            if u.scheme not in ("http", "https") or not u.netloc:
                add("invalid_canonical", rel, canonical)
                continue
            canonical_file = local_path_from_url(canonical)
            if not canonical_file.exists():
                add("canonical_target_missing_locally", rel, canonical)

    sitemap_urls = set()
    sitemap_files = sorted(ROOT.glob("sitemap*.xml"))
    for sm in sitemap_files:
        urls, children, error = parse_xml_sitemap(sm)
        if error:
            add("sitemap_xml_error", sm.name, error)
            continue
        sitemap_urls.update(urls)
        for child in children:
            p = local_path_from_url(child)
            if not p.exists():
                add("referenced_sitemap_missing", sm.name, child)
    for url in sorted(sitemap_urls):
        local = local_path_from_url(url)
        rel = local.relative_to(ROOT).as_posix()
        if not local.exists():
            add("sitemap_url_missing_file", "sitemap", url)
        elif rel in pages and pages[rel]["noindex"]:
            add("noindex_in_sitemap", rel, url)

    summary = {"html_pages_checked": len(pages), "sitemaps_checked": len(sitemap_files),
               "sitemap_urls_checked": len(sitemap_urls),
               "issues_by_type": dict(collections.Counter(i["type"] for i in issues)),
               "issues": issues}
    print(json.dumps({k: v for k, v in summary.items() if k != "issues"},
                     ensure_ascii=False, indent=2))
    for item in issues[:40]:
        print("{type}: {path}: {detail}".format(**item))
    if len(issues) > 40:
        print("... {} additional findings".format(len(issues) - 40))
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
