# -*- coding: utf-8 -*-
"""
Разбивка недостающих дилерских кодов на порции под дневной лимит Cloudflare KV.

Зачем: на бесплатном плане Cloudflare разрешает ~1000 операций записи в KV в
сутки, а в pcode-source/kv-bulk.json их сейчас 9486. Заливка всего файла разом
падает с `code: 10048 - your account has reached the free usage limit for this
operation for today`, причём падает целиком: частичной записи не происходит.

Скрипт сверяет то, что уже лежит в KV, с тем, что должно там быть, и
раскладывает разницу по файлам не больше 1000 ключей каждый. Порядок не
случайный: сначала новые и ходовые марки, большие хвосты (Scania, Deutz)
уезжают в конец - чтобы полезное появилось на сайте в первые же дни.

Как пользоваться (из корня репозитория):

  1) выгрузить текущее содержимое KV - это операция чтения, её лимит намного
     выше, и она не тратит дневную квоту записи:

     npx wrangler kv key list --namespace-id=<NS> --remote > pcode-source/kv-existing.json

  2) пересчитать разницу и порции:

     python scripts/kv_plan.py

  3) заливать по одной порции в сутки, пока список не кончится:

     npx wrangler kv bulk put pcode-source/kv-chunks/kv-part-01.json \
       --namespace-id=<NS> --remote

     Токен передавать переменной окружения CLOUDFLARE_API_TOKEN, в файлы
     репозитория его не класть.

Всё, что читает и пишет скрипт, лежит в pcode-source/ - а она в .gitignore,
так что дилерские коды в git по-прежнему не попадают.

Альтернатива всей этой возне - платный план Workers: лимит на запись в KV
снимается, и kv-bulk.json заливается одной командой.
"""
import collections, io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'pcode-source')
EXISTING = os.path.join(SRC, 'kv-existing.json')
BULK = os.path.join(SRC, 'kv-bulk.json')
CHUNK_DIR = os.path.join(SRC, 'kv-chunks')
CHUNK = 1000

# Порядок заливки. Всё, чего здесь нет, уезжает в самый конец.
PRIORITY = ['cumminsisf', 'fuso', 'thermoking', 'carrier', 'planar', 'webasto',
            'eberspacher', 'daewoo', 'eaton', 'cumminsisb', 'cumminsislisc',
            'cumminsism', 'cumminsisx', 'paccarmx13', 'hino', 'caterpillar',
            'renault', 'mahindra', 'deutz', 'scania']


def brand(key):
    return key.split(':')[1]


def main():
    if not os.path.exists(EXISTING):
        print(u'нет %s - сначала выгрузите ключи, см. docstring' % EXISTING)
        return
    # wrangler пишет вывод с BOM, поэтому utf-8-sig.
    existing = {e['name'] for e in json.loads(io.open(EXISTING, encoding='utf-8-sig').read())}
    bulk = json.loads(io.open(BULK, encoding='utf-8').read())

    have = collections.Counter(brand(k) for k in existing)
    need = collections.Counter()
    missing = []
    for e in bulk:
        if e['key'] not in existing:
            missing.append(e)
            need[brand(e['key'])] += 1

    print(u'в KV сейчас: %d, должно быть: %d, НЕ ЗАЛИТО: %d\n'
          % (len(existing), len(bulk), len(missing)))
    print(u'%-16s %8s %12s' % (u'марка', u'в KV', u'не хватает'))
    for b in sorted(set(list(have) + list(need))):
        print(u'%-16s %8d %12d' % (b, have[b], need[b]))

    if not missing:
        print(u'\nвсё залито, порции не нужны')
        return

    missing.sort(key=lambda e: (PRIORITY.index(brand(e['key']))
                                if brand(e['key']) in PRIORITY else len(PRIORITY),
                                e['key']))
    if not os.path.isdir(CHUNK_DIR):
        os.makedirs(CHUNK_DIR)
    for old in os.listdir(CHUNK_DIR):
        if old.startswith('kv-part-'):
            os.remove(os.path.join(CHUNK_DIR, old))

    print('')
    for i in range(0, len(missing), CHUNK):
        part = missing[i:i + CHUNK]
        name = 'kv-part-%02d.json' % (i // CHUNK + 1)
        io.open(os.path.join(CHUNK_DIR, name), 'w', encoding='utf-8').write(
            json.dumps(part, ensure_ascii=False, indent=1))
        by = collections.Counter(brand(e['key']) for e in part)
        print(u'%s  %4d ключей  %s' % (name, len(part),
              ', '.join('%s:%d' % kv for kv in by.most_common())))


if __name__ == '__main__':
    main()
