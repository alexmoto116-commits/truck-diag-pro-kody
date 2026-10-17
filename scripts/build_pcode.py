# -*- coding: utf-8 -*-
"""
Вынос дилерских таблиц (pcode.*) из публичных assets/dtc.enc.js и
assets/dtc.en.js в приватный, не попадающий в git источник
pcode-source/pcode.json, плюс сборка обратно.

GitHub Pages отдаёт наружу любой закоммиченный файл репозитория вне
зависимости от того, ссылается ли на него index.html - значит, спрятать
дилерские коды можно только выкинув их из публичных файлов совсем, а не
просто перестав их читать на клиенте.

Два режима:

  python scripts/build_pcode.py migrate [--force]
      Разовый шаг. Читает СЕГОДНЯШНИЕ assets/dtc.enc.js и dtc.en.js,
      вынимает из них ключ "pcode", складывает в pcode-source/pcode.json.
      Дальше pcode.json - место, где переводы дилерских кодов правятся
      руками; в публичные файлы он больше не попадает через git.

  python scripts/build_pcode.py build (по умолчанию)
      Повторяемый шаг, запускать после каждой правки pcode-source/pcode.json:
      - пересобирает assets/dtc.enc.js и dtc.en.js БЕЗ ключа pcode
        (остальные ключи - brandNames, brands, spn, universal, spnName,
        fmi, urgentSpn/Fmi, kamazUrgent - остаются как есть);
      - генерирует pcode-source/kv-bulk.json - файл в формате
        `wrangler kv bulk put`, которым дилерские коды заливаются в
        Cloudflare KV для API-бэкенда (см. worker/pcode-api.js);
      - генерирует pcode-source/kv-idx.json - индекс «код -> марки» для
        поиска без марки, SHARDS шардов (ключи pcode:_idx:XX). Заливать
        ОТДЕЛЬНО, и только его, когда меняется состав кодов:
        `wrangler kv bulk put ... kv-idx.json`. Шарды всегда пишутся все,
        даже пустые: отсутствующий шард воркер считает признаком «индекс
        ещё не залит».

Запуск из корня репозитория.
"""
import base64, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, 'pcode-source')
PCODE_JSON = os.path.join(SRC_DIR, 'pcode.json')
KV_BULK_JSON = os.path.join(SRC_DIR, 'kv-bulk.json')
KV_IDX_JSON = os.path.join(SRC_DIR, 'kv-idx.json')

# Число шардов индекса без марки. Держать в согласии с INDEX_SHARDS в
# worker/pcode-api.js. Записей в KV при заливке - ровно столько же.
SHARDS = 64
SHARD_MAX_BYTES = 100 * 1024  # разбор JSON шарда должен укладываться в ~10 мс CPU

RU_PATH = os.path.join(ROOT, 'assets', 'dtc.enc.js')
EN_PATH = os.path.join(ROOT, 'assets', 'dtc.en.js')

# Держать в согласии со списком KNOWN_PCODE_BRANDS в worker/pcode-api.js.
KNOWN_PCODE_BRANDS = ['volvo', 'mercedes', 'scania', 'shacman', 'tata', 'ashokleyland', 'howo', 'faw', 'jac', 'international', 'powerstroke',
                       'cumminsisb', 'cumminsislisc', 'cumminsism', 'cumminsisx', 'paccarmx13', 'hino', 'renault', 'caterpillar',
                       'mahindra', 'deutz', 'fuso', 'thermoking', 'carrier',
                       'planar', 'webasto', 'eberspacher', 'daewoo', 'cumminsisf',
                       'eaton', 'hyundai', 'haldex', 'allison', 'weichai', 'volkswagen', 'mwm', 'isuzu', 'baw',
                        'ivecoedc', 'ivecoeurotronic', 'iveco', 'daf', 'manzbr2', 'manebs', 'man', 'mack', 'yamz', 'volvomid', 'jingwei', 'gaz']

# ------------------------------------------------- индекс номеров сканера
#
# ЗАЧЕМ. У части марок код на щитке (SPN/FMI) и номер, который показывает
# сканер, - разные вещи. Мы их знаем и печатаем прямо в описании: «Код по
# K-line на КамАЗ-5490: ADM3 10103», «Код FODP (сканер): P0513-00», «Код
# сканера: P023D». Но лежат они ВНУТРИ ТЕКСТА, а поиск по тексту описаний
# не идёт - он идёт по ключам. Человек с дешёвым сканером вводит ровно то,
# что видит на экране, и не находит ничего: 908 номеров были написаны на
# страницах и при этом недоступны поиску.
#
# ЧТО СТРОИМ. Обратный индекс «номер сканера -> марка|SPN.FMI». Ответ по
# нему выходит полноценной карточкой (расшифровка FMI, срочность, ссылка
# на страницу кода), а не одной строкой из KV: мы ведём человека к нашему
# же коду, а не заводим отдельную запись с тем же текстом.
#
# ПОЧЕМУ НЕ В KV. Эти описания и так лежат в публичной таблице - прятать
# нечего, а лишний сетевой запрос на обочине с одной палкой связи стоит
# дороже 29 КБ в файле, который и без того грузится.
#
# ПОЧЕМУ ТОЛЬКО В РУССКОМ ФАЙЛЕ. Индекс - это отображение номера на ключ
# SPN.FMI, оно от языка не зависит. dtc.enc.js грузится всегда, dtc.en.js -
# только для нерусских языков; класть одно и то же в оба значит платить
# весом дважды. Номера при этом собираются из ОБОИХ файлов: английские
# формулировки писались отдельно, и там, где русского номера нет, может
# найтись английский.
SCAN_PATTERNS = [
    # (язык, зачем, регулярка)
    (u'ru', u'Ford, собственная нумерация FODP',    re.compile(r'Код FODP \(сканер\): ([A-Z0-9-]+)')),
    (u'ru', u'SITRAK/Dongfeng/Foton, обычный OBD',  re.compile(u'Код сканера: ([A-Z0-9-]+)')),
    (u'en', u'Ford FODP',                           re.compile(r'FODP code \(scan tool\): ([A-Z0-9-]+)')),
    (u'en', u'SITRAK/Dongfeng/Foton OBD',           re.compile(u'Scan tool code: ([A-Z0-9-]+)')),
]

# K-line КамАЗ-5490 живёт ТОЛЬКО в разделе brands.kamaz5490 (16.10.2026).
# Номера сканера - все «ADM3 N» / «MR2 N» из текста записи: и в хвосте
# «Код по K-line на КамАЗ-5490: ADM3 10514, MR2 12020.», и в скобках у
# вариантов внутри описания: «... (MR2 10101); ... (MR2 10149)». Каждый номер
# даёт ссылку «kamaz5490|SPN.FMI» на ключ записи. Раньше номера брались из
# brands.kamaz; теперь brands.kamaz (J1939) хвостов не содержит, и
# build_scan_index это проверяет.
KLINE_BRAND = 'kamaz5490'
KLINE_NUM = re.compile(r'(?:ADM3|MR2) ([0-9]+)')
KLINE_WHY = u'КамАЗ-5490, старый сканер по K-line (brands.kamaz5490)'


def build_scan_index(blobs):
    """blobs - список разобранных таблиц (русская и английская).

    Возвращает {номер: ["марка|SPN.FMI", ...]}. Один номер часто отвечает
    сразу нескольким кодам (P060C у SITRAK - девятнадцати: одна причина,
    девятнадцать проявлений), поэтому значение всегда список.
    """
    idx = {}
    stats = {}

    def add(num, ref, why, brand):
        bucket = idx.setdefault(norm(num), [])
        if ref not in bucket:
            bucket.append(ref)
        stats[(why, brand)] = stats.get((why, brand), 0) + 1

    for blob in blobs:
        for brand, table in (blob.get('brands') or {}).items():
            for key, text in table.items():
                if not isinstance(text, str):
                    continue
                ref = '%s|%s' % (brand, key)
                if brand == KLINE_BRAND:
                    for num in KLINE_NUM.findall(text):
                        add(num, ref, KLINE_WHY, brand)
                elif 'K-line на КамАЗ-5490' in text or 'K-line code on KamAZ-5490' in text:
                    raise SystemExit(
                        u'K-line КамАЗ-5490 в разделе %r (ключ %s): номера сканера ведутся '
                        u'только в brands.kamaz5490. Перенесите запись туда.' % (brand, key))
                for lang, why, rx in SCAN_PATTERNS:
                    for m in rx.finditer(text):
                        add(m.group(1), ref, why, brand)
    for bucket in idx.values():
        bucket.sort()
    if not idx:
        raise SystemExit(
            u'ПУСТОЙ ИНДЕКС НОМЕРОВ СКАНЕРА: ни одна из формулировок SCAN_PATTERNS '
            u'не встретилась в описаниях. Скорее всего изменилась формулировка при '
            u'заливке новых данных - поправьте регулярку, а не выбрасывайте проверку: '
            u'молча пустой индекс означает, что 900 номеров опять не ищутся.')
    return idx, stats


TEMPLATE = u"""(function(){{
  var b64='{b64}';
  var bin=atob(b64);
  var bytes=new Uint8Array(bin.length);
  for(var i=0;i<bin.length;i++) bytes[i]=bin.charCodeAt(i);
  var json=new TextDecoder('utf-8').decode(bytes);
  window.{glob}=JSON.parse(json);
}})();
"""


def load_blob(path):
    raw = io.open(path, encoding='utf-8').read()
    b64 = re.search(r"b64='([^']+)'", raw).group(1)
    return json.loads(base64.b64decode(b64).decode('utf-8'))


def write_blob(path, data, glob):
    b64 = base64.b64encode(json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).decode('ascii')
    io.open(path, 'w', encoding='utf-8', newline='\n').write(TEMPLATE.format(b64=b64, glob=glob))


# Кириллические двойники латинских букв (верхний регистр). Держать в согласии с
# homoglyphs в worker/pcode-api.js.
CYR_HOMO = u'АВСЕНКМОРТХУ'  # А В С Е Н К М О Р Т Х У
LAT_HOMO = u'ABCEHKMOPTXY'
HOMO_TABLE = str.maketrans(CYR_HOMO, LAT_HOMO)

# Блинк-коды: «Мигающий код: 2-1» (Isuzu, Hino, Ashok Leyland), «Flash code: 68» (HOWO).
BLINK_RE = re.compile(
    r'(?:Мигающий код|Flash code|Blink code|Blink-код|Flashing code)\s*:?\s*([0-9][0-9 -]*[0-9]|[0-9])',
    re.I)


def norm(code):
    """Нормализованный код - ровно тот, что ищет воркер (norm в pcode-api.js):
    без пробелов, заглавными, кириллические двойники заменены латиницей; у кода
    вида «100.01» ведущие нули дробной части убираются («100.1»)."""
    c = re.sub(r'\s+', '', code.upper()).translate(HOMO_TABLE)
    if re.match(r'^[0-9]{1,7}\.[0-9]{1,2}$', c):
        whole, frac = c.split('.')
        c = whole + '.' + re.sub(r'^0+(?=[0-9])', '', frac)
    return c


def shard_of(code):
    """Шард индекса для нормализованного кода: FNV-1a по UTF-8 байтам mod SHARDS.
    Зеркало функции shardKey в worker/pcode-api.js - менять только вместе."""
    h = 0x811c9dc5
    for b in code.encode('utf-8'):
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h % SHARDS


def build_blink_aliases(pcode):
    """Алиасы блинк-кодов: {марка: {алиас: [ключи]}}.

    Алиас - номер мигающего кода из текста записи («Мигающий код: 2-1» у
    Isuzu C0201). Две формы: с дефисом («2-1») и без («21»). Если номер
    совпадает с собственным ключом марки, алиас не нужен и не пишется.
    Один номер часто указывает на несколько кодов (одна флэш-группа) - тогда
    список ключей длиннее одного, воркер вернёт все.
    """
    out = {}
    for brand, table in pcode.items():
        direct = set(norm(c) for c in table)
        amap = {}
        for code, texts in table.items():
            for lang in ('ru', 'en'):
                s = (texts or {}).get(lang) or ''
                for m in BLINK_RE.finditer(s):
                    tok = norm(m.group(1))
                    for form in (tok, tok.replace('-', '')):
                        if form in direct:
                            continue
                        amap.setdefault(form, set()).add(norm(code))
        if amap:
            out[brand] = {f: sorted(keys) for f, keys in amap.items()}
    return out


def build_code_index(pcode, aliases):
    """Индекс «нормализованный код -> марки» по шардам.

    Ключ - ровно тот, что лежит в KV (norm(code) из kv-bulk.json), поэтому
    варианты написания воркер строит тем же codeVariants, что и для KV.
    Значение - список записей: «марка» для прямого ключа и «марка>ключ» для
    блинк-алиаса (ключ, на который указывает алиас). Возвращает список из
    SHARDS словарей {код: [записи]}.
    """
    shards = [dict() for _ in range(SHARDS)]
    for brand, table in pcode.items():
        for code in table:
            ncode = norm(code)
            bucket = shards[shard_of(ncode)].setdefault(ncode, [])
            if brand not in bucket:
                bucket.append(brand)
    for brand, amap in aliases.items():
        for form, keys in amap.items():
            bucket = shards[shard_of(form)].setdefault(form, [])
            for key in keys:
                entry = '%s>%s' % (brand, key)
                if entry not in bucket:
                    bucket.append(entry)
    for shard in shards:
        for entries in shard.values():
            entries.sort()
    return shards


# ------------------------------------------------------------- migrate

def cmd_migrate(force):
    if os.path.exists(PCODE_JSON) and not force:
        print('pcode-source/pcode.json уже существует - используйте --force, если точно хотите перезаписать')
        sys.exit(1)

    ru = load_blob(RU_PATH)
    en = load_blob(EN_PATH)
    ru_pcode = ru.get('pcode', {})
    en_pcode = en.get('pcode', {})

    out = {}
    for brand, table in ru_pcode.items():
        out[brand] = {}
        for code, ru_text in table.items():
            out[brand][code] = {'ru': ru_text, 'en': (en_pcode.get(brand) or {}).get(code)}

    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    io.open(PCODE_JSON, 'w', encoding='utf-8').write(
        json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True))

    for brand, table in out.items():
        missing = sum(1 for v in table.values() if v['en'] is None)
        print(u'%s: %d кодов, без EN - %d' % (brand, len(table), missing))
    print('written', PCODE_JSON)


# ---------------------------------------------------------------- build

def cmd_build():
    if not os.path.exists(PCODE_JSON):
        print('pcode-source/pcode.json не найден - сначала запустите: python scripts/build_pcode.py migrate')
        sys.exit(1)

    pcode = json.loads(io.open(PCODE_JSON, encoding='utf-8').read())

    unknown = [b for b in pcode if b not in KNOWN_PCODE_BRANDS]
    if unknown:
        print(u'ВНИМАНИЕ: в pcode.json есть марки, которых нет в KNOWN_PCODE_BRANDS '
              u'(worker/pcode-api.js тоже надо обновить): %s' % ', '.join(unknown))

    # 1) публичные файлы: без pcode, зато с индексом номеров сканера
    ru = load_blob(RU_PATH)
    en = load_blob(EN_PATH)
    ru.pop('pcode', None)
    en.pop('pcode', None)
    # Старый индекс снимаем ДО разбора, а не дописываем к нему: иначе номер,
    # исчезнувший из описаний (поправили формулировку, откатили данные),
    # остался бы в индексе навсегда и вёл в никуда.
    ru.pop('scan', None)
    en.pop('scan', None)
    scan, scan_stats = build_scan_index([ru, en])
    ru['scan'] = scan
    write_blob(RU_PATH, ru, '__TDP_DTC')
    write_blob(EN_PATH, en, '__TDP_DTC_EN')
    print('rewritten', RU_PATH, 'and', EN_PATH, '(pcode removed)')
    print(u'индекс номеров сканера: %d номеров -> %d кодов'
          % (len(scan), sum(len(v) for v in scan.values())))
    for (why, brand), n in sorted(scan_stats.items()):
        print(u'    %-42s %-10s %d' % (why, brand, n))

    # 2) kv-bulk.json для wrangler kv bulk put
    entries = []
    counts = {}
    for brand, table in pcode.items():
        counts[brand] = len(table)
        for code, texts in table.items():
            value = json.dumps({'ru': texts.get('ru'), 'en': texts.get('en')}, ensure_ascii=False)
            entries.append({'key': 'pcode:%s:%s' % (brand, norm(code)), 'value': value})

    # Блинк-алиасы: pcode:_alias:<марка>:<алиас> -> список ключей.
    aliases = build_blink_aliases(pcode)
    alias_pairs = 0
    alias_ambiguous = 0
    for brand, amap in sorted(aliases.items()):
        for form, keys in sorted(amap.items()):
            alias_pairs += len(keys)
            if len(keys) > 1:
                alias_ambiguous += 1
            entries.append({'key': 'pcode:_alias:%s:%s' % (brand, form),
                            'value': json.dumps(keys, ensure_ascii=False)})

    io.open(KV_BULK_JSON, 'w', encoding='utf-8').write(
        json.dumps(entries, ensure_ascii=False, indent=1))

    total = sum(counts.values())
    summary = ', '.join('%s: %d' % (b, n) for b, n in sorted(counts.items()))
    print('%s -> %d keys (%s)' % (KV_BULK_JSON, total, summary))
    alias_total = sum(len(a) for a in aliases.values())
    print('блинк-алиасы: %d алиасов (%d неоднозначных), %d пар алиас->ключ, марок: %d'
          % (alias_total, alias_ambiguous, alias_pairs, len(aliases)))
    print('всего записей в kv-bulk.json: %d' % len(entries))

    # 3) kv-idx.json: индекс поиска без марки, отдельным файлом
    shards = build_code_index(pcode, aliases)
    idx_entries = []
    biggest = 0
    for n, shard in enumerate(shards):
        value = json.dumps(shard, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
        size = len(value.encode('utf-8'))
        if size > SHARD_MAX_BYTES:
            raise SystemExit(u'ШАРД pcode:_idx:%02x: %d байт > %d. Увеличьте SHARDS.'
                             % (n, size, SHARD_MAX_BYTES))
        biggest = max(biggest, size)
        idx_entries.append({'key': 'pcode:_idx:%02x' % n, 'value': value})

    io.open(KV_IDX_JSON, 'w', encoding='utf-8').write(
        json.dumps(idx_entries, ensure_ascii=False, indent=1))
    indexed = sum(len(s) for s in shards)
    print('%s -> %d shards, %d codes, largest shard %d bytes'
          % (KV_IDX_JSON, len(shards), indexed, biggest))


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'migrate':
        cmd_migrate(force='--force' in args)
    elif not args or args[0] == 'build':
        cmd_build()
    else:
        print('usage: python scripts/build_pcode.py [migrate [--force] | build]')
        sys.exit(1)
