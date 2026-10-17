# -*- coding: utf-8 -*-
"""План индекса страниц кодов: какие адреса kody/spn-N.html и en/kody/spn-N.html
индексируются. Только чтение; без --write файл scripts/index_keep.json не меняется.

Правило (решение Алекса от 17.10.2026, вариант 2):
страница кода индексируется, если выполнено одно из условий:
  - показы в выгрузке Search Console >= 1;
  - марок (<h2 class="mk">) >= 3 и уникальных слов >= 300.
ru и en считаются отдельно, по своему адресу.
Уникальные слова: слова тела страницы без меню, таблиц, форм и блоков «Рядом»,
минус слова абзацев, которые встречаются больше чем на 50 страницах кодов (шаблон).

Запуск из корня репозитория:
  python -X utf8 -I scripts/index_plan.py <папка с выгрузкой>            # показать разницу
  python -X utf8 -I scripts/index_plan.py <папка с выгрузкой> --write    # записать index_keep.json

Папка с выгрузкой: в ней есть CSV, у которого первая колонка «Популярные страницы»
(выгрузка Search Console, вкладка «Страницы» с показами и кликами).
Страницы, которых нет в выгрузке, считаются с 0 показов.
"""
import os
import re
import csv
import glob
import html
import json
import sys
import datetime
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP_FILE = os.path.join(ROOT, 'scripts', 'index_keep.json')
SITE = 'https://codetruck.ru'
N_MARKS = 3
M_WORDS = 300
IMPR_MIN = 1
TPL = 50  # абзац считается шаблонным, если встречается на большем числе страниц

PAR_RE = re.compile(r'<p(?:\s[^>]*)?>(.*?)</p>', re.S)


def norm_url(u):
    u = urllib.parse.unquote(u.strip()).replace('http://', 'https://').replace('https://www.', 'https://')
    if u.endswith('/') and u.count('/') > 3:
        u = u.rstrip('/')
    return u


def read_perf(folder):
    """Показы по адресам из CSV «Популярные страницы»."""
    rows = None
    for f in sorted(glob.glob(os.path.join(folder, '*.csv'))):
        with open(f, encoding='utf-8', newline='') as fh:
            data = list(csv.reader(fh))
        if data and data[0] and data[0][0] == 'Популярные страницы':
            rows = data
            break
    if rows is None:
        raise SystemExit('В папке нет CSV с колонкой «Популярные страницы»: ' + folder)
    perf = {}
    for r in rows[1:]:
        if len(r) < 3 or not r[0].startswith('http'):
            continue
        try:
            impr = int(float(r[2].replace(',', '.')))
        except ValueError:
            impr = 0
        perf[norm_url(r[0])] = impr
    return perf


def body_of(s):
    i = s.find('<div class="w">')
    j = s.find('<p class="cta"')
    if j < 0:
        j = s.find('</body>')
    b = s[i if i >= 0 else 0: j]
    b = re.sub(r'<table\b.*?</table>', ' ', b, flags=re.S)
    b = re.sub(r'<ul class="(?:near|lines|own)">.*?</ul>', ' ', b, flags=re.S)
    b = re.sub(r'<form\b.*?</form>', ' ', b, flags=re.S)
    b = re.sub(r'<div class="tick">.*?</div>', ' ', b, flags=re.S)
    b = re.sub(r'<h1>.*?</h1>', ' ', b, flags=re.S)
    b = re.sub(r'<p class="vline[^"]*">.*?</p>', ' ', b, flags=re.S)
    b = re.sub(r'<p class="jump">.*?</p>', ' ', b, flags=re.S)
    return b


def norm_par(t):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = re.sub(r'\d+', 'N', t.lower())
    return re.sub(r'\s+', ' ', t).strip()


def words(t):
    return re.findall(r'\w+', html.unescape(re.sub(r'<[^>]+>', ' ', t)))


def collect():
    """Все страницы кодов обоих языков: относительный путь, язык, марки, уникальные слова."""
    files = []
    for lang, base, prefix in (('ru', os.path.join(ROOT, 'kody'), 'kody'),
                               ('en', os.path.join(ROOT, 'en', 'kody'), 'en/kody')):
        for f in os.listdir(base):
            if re.match(r'spn-\d+\.html$', f):
                files.append((prefix + '/' + f, lang, os.path.join(base, f)))
    texts = {}
    par_df = {}
    for rel, lang, path in files:
        with open(path, encoding='utf-8') as fh:
            s = fh.read()
        texts[rel] = s
        seen = set(norm_par(p) for p in PAR_RE.findall(body_of(s)))
        for p in seen:
            if p:
                par_df[p] = par_df.get(p, 0) + 1
    result = []
    for rel, lang, path in files:
        s = texts[rel]
        b = body_of(s)
        tpl_words = 0
        for p in PAR_RE.findall(b):
            n = norm_par(p)
            if n and par_df.get(n, 0) > TPL:
                tpl_words += len(words(p))
        uniq = len(words(b)) - tpl_words
        result.append(dict(rel=rel, lang=lang,
                           url=SITE + '/' + rel,
                           marks=len(re.findall(r'<h2 class="mk"', s)),
                           uniq=uniq))
    return result


def decide(page, perf):
    impr = perf.get(norm_url(page['url']), 0)
    keep = impr >= IMPR_MIN or (page['marks'] >= N_MARKS and page['uniq'] >= M_WORDS)
    return keep, impr


def main(argv):
    write = '--write' in argv
    args = [a for a in argv if not a.startswith('--')]
    if len(args) != 1:
        raise SystemExit('Укажите папку с выгрузкой Search Console: index_plan.py <папка> [--write]')
    perf = read_perf(args[0])
    pages = collect()
    keep_now = []
    by_lang = {'ru': [0, 0], 'en': [0, 0]}
    impr_pages = 0
    for p in pages:
        ok, impr = decide(p, perf)
        by_lang[p['lang']][1] += 1
        if impr >= IMPR_MIN:
            impr_pages += 1
        if ok:
            keep_now.append(p['rel'])
            by_lang[p['lang']][0] += 1
    keep_now.sort(key=lambda r: (r.startswith('en/'), int(re.search(r'spn-(\d+)', r).group(1))))
    print('страниц кодов всего: ru %d, en %d' % (by_lang['ru'][1], by_lang['en'][1]))
    print('в выгрузке с показами >= %d: %d' % (IMPR_MIN, impr_pages))
    print('по правилу индексируются: ru %d, en %d, всего %d'
          % (by_lang['ru'][0], by_lang['en'][0], len(keep_now)))
    if os.path.isfile(KEEP_FILE):
        with open(KEEP_FILE, encoding='utf-8') as fh:
            old = set(json.load(fh)['страницы'])
        new = set(keep_now)
        print('в index_keep.json сейчас: %d' % len(old))
        print('добавится: %d' % len(new - old))
        for r in sorted(new - old):
            print('  + ' + r)
        print('уберётся: %d' % len(old - new))
        for r in sorted(old - new):
            print('  - ' + r)
        if new == old:
            print('без изменений')
    else:
        print('файла index_keep.json ещё нет')
    if write:
        doc = {
            'дата': datetime.date.today().isoformat(),
            'правило': ('страница кода (ru и en отдельно, по своему адресу) индексируется, если '
                        'показы в Search Console >= %d ИЛИ марок >= %d и уникальных слов >= %d; '
                        'шаблонные абзацы (на >%d страницах) в уникальные слова не входят'
                        % (IMPR_MIN, N_MARKS, M_WORDS, TPL)),
            'решение': 'вариант 2 (N=3, M=300); 82 страницы с показами открыты (решение Алекса, 17.10.2026)',
            'источник': 'выгрузка Search Console «Страницы» (вкладка «Эффективность»), 17.10.2026',
            'как_пересчитать': ('python -X utf8 -I scripts/index_plan.py <папка с выгрузкой> --write; '
                                'затем пересобрать страницы (см. коммит)'),
            'страницы': keep_now,
        }
        with open(KEEP_FILE, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        print('записан ' + KEEP_FILE)
    else:
        print('файл не изменён (для записи добавьте --write)')


if __name__ == '__main__':
    main(sys.argv[1:])
