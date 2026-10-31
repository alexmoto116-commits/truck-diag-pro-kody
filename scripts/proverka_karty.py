#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка карты сайта codetruck.ru по живому сайту (только чтение).

Запуск:
    python proverka_karty.py                 # полная проверка, отчёт в консоль и в report.txt рядом
    python proverka_karty.py --no-file       # только консоль

Что проверяет:
  * sitemap.xml (индекс) -> все карты -> все адреса;
  * код ответа без следования переадресации (переадресация выводится отдельной строкой);
  * noindex в <meta name="robots"> или в заголовке X-Robots-Tag;
  * canonical: совпадает ли с самим адресом;
  * hreflang: каждая пара отдаёт 200;
  * дубли адресов между картами.

Ограничения: не чаще 5 запросов в секунду, повтор при сетевой ошибке (до 4 попыток).
Код выхода: 0 - проблем нет, 1 - есть проблемы, 2 - карта не загрузилась.
Только стандартная библиотека и requests.
"""
import sys
import os
import time
import threading
import xml.etree.ElementTree as ET
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.parse import urljoin

import requests

SITEMAP_INDEX = "https://codetruck.ru/sitemap.xml"
RATE = 5.0          # запросов в секунду, не больше
WORKERS = 5
RETRIES = 4
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) proverka-karty/1.0"
HOST = "codetruck.ru"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


class Limiter:
    """Общий ограничитель частоты для всех потоков."""

    def __init__(self, rate):
        self.interval = 1.0 / rate
        self.lock = threading.Lock()
        self.next_slot = 0.0

    def wait(self):
        with self.lock:
            now = time.monotonic()
            if self.next_slot < now:
                self.next_slot = now
            slot = self.next_slot
            self.next_slot += self.interval
        delay = slot - time.monotonic()
        if delay > 0:
            time.sleep(delay)


limiter = Limiter(RATE)
session = requests.Session()
session.headers["User-Agent"] = UA


def fetch(url):
    """GET без следования переадресации. Повтор при сетевой ошибке."""
    last_exc = None
    for attempt in range(RETRIES):
        limiter.wait()
        try:
            return session.get(url, allow_redirects=False, timeout=30)
        except requests.RequestException as exc:
            last_exc = exc
            time.sleep(2 ** attempt)
    raise last_exc


class HeadParser(HTMLParser):
    """Собирает robots-meta, canonical и hreflang-ссылки."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.robots = []
        self.canonicals = []
        self.alternates = []  # (hreflang, href)

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta" and a.get("name", "").lower() in ("robots", "googlebot"):
            self.robots.append(a.get("content", ""))
        elif tag == "link":
            rel = a.get("rel", "").lower().split()
            href = a.get("href", "").strip()
            if "canonical" in rel and href:
                self.canonicals.append(href)
            if "alternate" in rel and a.get("hreflang") and href:
                self.alternates.append((a["hreflang"].strip(), href))


def local(tag):
    return tag.split("}")[-1]


def load_sitemap(url, depth=0):
    """Возвращает список (адрес, карта) и список ошибок загрузки карт."""
    entries, errors = [], []
    r = fetch(url)
    if r.status_code != 200:
        errors.append(f"карта недоступна {r.status_code} — {url}")
        return entries, errors
    try:
        root = ET.fromstring(r.content)
    except ET.ParseError as exc:
        errors.append(f"карта не разбирается ({exc}) — {url}")
        return entries, errors
    if local(root.tag) == "sitemapindex":
        if depth > 1:
            return entries, errors
        for el in root:
            if local(el.tag) != "sitemap":
                continue
            for sub in el:
                if local(sub.tag) == "loc" and sub.text:
                    e, er = load_sitemap(sub.text.strip(), depth + 1)
                    entries += e
                    errors += er
        return entries, errors
    name = url.rsplit("/", 1)[-1]
    for el in root:
        if local(el.tag) != "url":
            continue
        for sub in el:
            if local(sub.tag) == "loc" and sub.text:
                entries.append((sub.text.strip(), name))
    return entries, errors


def check_page(url):
    """Проверка одного адреса из карты."""
    res = {"url": url, "code": None, "location": "", "noindex": "",
           "canonical": "", "pairs": [], "error": ""}
    try:
        r = fetch(url)
    except requests.RequestException as exc:
        res["error"] = f"ошибка сети ({exc.__class__.__name__})"
        return res
    res["code"] = r.status_code
    if 300 <= r.status_code < 400:
        res["location"] = urljoin(url, r.headers.get("Location", ""))
    xrt = r.headers.get("X-Robots-Tag", "")
    if "noindex" in xrt.lower():
        res["noindex"] = "X-Robots-Tag"
    if r.status_code == 200 and "html" in r.headers.get("Content-Type", "").lower():
        p = HeadParser()
        try:
            p.feed(r.text)
        except Exception:
            pass
        if not res["noindex"] and any("noindex" in c.lower() for c in p.robots):
            res["noindex"] = "meta robots"
        if p.canonicals:
            res["canonical"] = urljoin(url, p.canonicals[0])
        for lang, href in p.alternates:
            pair = urljoin(url, href)
            if pair != url:
                res["pairs"].append((lang, pair))
    return res


def main():
    write_file = "--no-file" not in sys.argv
    out_lines = []

    def say(line=""):
        print(line)
        out_lines.append(line)

    # 1. Карты
    all_entries, load_errors = [], []
    index_r = fetch(SITEMAP_INDEX)
    if index_r.status_code != 200:
        print(f"Индекс карт недоступен: {index_r.status_code} — {SITEMAP_INDEX}")
        return 2
    root = ET.fromstring(index_r.content)
    child_maps = []
    for el in root:
        if local(el.tag) == "sitemap":
            for sub in el:
                if local(sub.tag) == "loc" and sub.text:
                    child_maps.append(sub.text.strip())
    for cm in child_maps:
        e, er = load_sitemap(cm)
        all_entries += e
        load_errors += er

    # 2. Дубли между картами
    where = defaultdict(list)
    for url, mp in all_entries:
        where[url].append(mp)
    unique = list(where.keys())
    duplicates = {u: sorted(set(m)) for u, m in where.items() if len(m) > 1}

    # 3. Проверка адресов
    results = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for url, res in zip(unique, ex.map(check_page, unique)):
            results[url] = res

    # 4. hreflang-пары, которых нет среди адресов карт, и пары из карт
    pair_urls = set()
    for res in results.values():
        if res["code"] == 200:
            for _lang, pair in res["pairs"]:
                pair_urls.add(pair)
    pair_codes = {}
    missing_pairs = [p for p in pair_urls if p not in results]

    def pair_status(p):
        try:
            r = fetch(p)
            return p, r.status_code, (urljoin(p, r.headers.get("Location", "")) if 300 <= r.status_code < 400 else "")
        except requests.RequestException:
            return p, "сеть", ""

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for p, code, loc in ex.map(pair_status, missing_pairs):
            pair_codes[p] = (code, loc)
    for p in pair_urls:
        if p in results:
            pair_codes[p] = (results[p]["code"], results[p]["location"])

    # 5. Сбор проблем
    problems = []  # (группа, строка)
    for url in unique:
        r = results[url]
        if r["error"]:
            problems.append(("сеть", f"{r['error']} — {url}"))
            continue
        code = r["code"]
        if code == 200:
            pass
        elif 300 <= code < 400:
            problems.append(("переадресация", f"переадресация {code} — {url} → {r['location'] or '(нет Location)'}"))
            continue
        else:
            problems.append(("код", f"{code} — {url}"))
            continue
        if r["noindex"]:
            problems.append(("noindex", f"noindex ({r['noindex']}) — {url}"))
        if r["canonical"] and r["canonical"] != url:
            problems.append(("canonical", f"canonical на другой адрес — {url} → {r['canonical']}"))
        for _lang, pair in r["pairs"]:
            pcode, ploc = pair_codes.get(pair, ("?", ""))
            if pcode == 200:
                continue
            if isinstance(pcode, int) and 300 <= pcode < 400:
                problems.append(("hreflang", f"hreflang-пара переадресация {pcode} — {url} → {pair} (куда: {ploc or 'нет Location'})"))
            elif pcode == 404:
                problems.append(("hreflang", f"hreflang-пара 404 — {url} → {pair}"))
            else:
                problems.append(("hreflang", f"hreflang-пара {pcode} — {url} → {pair}"))
    for u, maps in duplicates.items():
        problems.append(("дубль", f"дубль между картами ({', '.join(maps)}) — {u}"))
    for e in load_errors:
        problems.append(("карта", e))

    # 6. Сводка
    code_counts = defaultdict(int)
    for url in unique:
        r = results[url]
        code_counts[r["code"] if r["code"] is not None else "сеть"] += 1
    ru_n = sum(1 for _, mp in all_entries if "-ru-" in mp)
    en_n = sum(1 for _, mp in all_entries if "-en-" in mp)
    no_canon = sum(1 for u in unique if results[u]["code"] == 200 and not results[u]["canonical"])
    no_pairs = sum(1 for u in unique if results[u]["code"] == 200 and not results[u]["pairs"])
    group_counts = defaultdict(int)
    for g, _ in problems:
        group_counts[g] += 1

    say("=" * 70)
    say("ПРОВЕРКА КАРТЫ САЙТА codetruck.ru")
    say("=" * 70)
    say("Проблемы:")
    if not problems:
        say("  нет")
    # группировка при большом числе: печатаем все строки, но по группам
    order = ["карта", "код", "переадресация", "сеть", "noindex", "canonical", "hreflang", "дубль"]
    grouped = defaultdict(list)
    for g, line in problems:
        grouped[g].append(line)
    for g in order + [k for k in grouped if k not in order]:
        for line in grouped.get(g, []):
            say("  " + line)
    say("")
    say("Сводка:")
    say(f"  карт в индексе: {len(child_maps)}; адресов в картах (с повторами): {len(all_entries)}; уникальных: {len(unique)}")
    say(f"  по языкам (строки карт): ru {ru_n}, en {en_n}")
    say("  коды ответа: " + ", ".join(f"{k}: {v}" for k, v in sorted(code_counts.items(), key=lambda x: str(x[0]))))
    say(f"  адресов без canonical (при 200): {no_canon}; без hreflang (при 200): {no_pairs}")
    say(f"  hreflang-пар проверено: {len(pair_urls)}")
    say(f"  дублей между картами: {len(duplicates)}")
    say("  проблем по группам: " + ", ".join(f"{k} {v}" for k, v in sorted(group_counts.items())) if problems else "  проблем: 0")
    say(f"  ИТОГ: {'проблемы есть' if problems else 'проблем нет'}")

    if write_file:
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "report.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines) + "\n")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
