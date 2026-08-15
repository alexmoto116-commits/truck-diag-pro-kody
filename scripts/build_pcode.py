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
        Cloudflare KV для API-бэкенда (см. worker/pcode-api.js).

Запуск из корня репозитория.
"""
import base64, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, 'pcode-source')
PCODE_JSON = os.path.join(SRC_DIR, 'pcode.json')
KV_BULK_JSON = os.path.join(SRC_DIR, 'kv-bulk.json')

RU_PATH = os.path.join(ROOT, 'assets', 'dtc.enc.js')
EN_PATH = os.path.join(ROOT, 'assets', 'dtc.en.js')

# Держать в согласии со списком KNOWN_PCODE_BRANDS в worker/pcode-api.js.
KNOWN_PCODE_BRANDS = ['volvo', 'mercedes', 'scania', 'shacman', 'tata', 'ashokleyland', 'howo', 'faw', 'jac', 'international', 'powerstroke',
                       'cumminsisb', 'cumminsislisc', 'cumminsism', 'cumminsisx', 'paccarmx13', 'hino', 'renault', 'caterpillar']

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


def norm(code):
    return re.sub(r'\s+', '', code.upper())


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

    # 1) публичные файлы без pcode
    ru = load_blob(RU_PATH)
    en = load_blob(EN_PATH)
    ru.pop('pcode', None)
    en.pop('pcode', None)
    write_blob(RU_PATH, ru, '__TDP_DTC')
    write_blob(EN_PATH, en, '__TDP_DTC_EN')
    print('rewritten', RU_PATH, 'and', EN_PATH, '(pcode removed)')

    # 2) kv-bulk.json для wrangler kv bulk put
    entries = []
    counts = {}
    for brand, table in pcode.items():
        counts[brand] = len(table)
        for code, texts in table.items():
            value = json.dumps({'ru': texts.get('ru'), 'en': texts.get('en')}, ensure_ascii=False)
            entries.append({'key': 'pcode:%s:%s' % (brand, norm(code)), 'value': value})

    io.open(KV_BULK_JSON, 'w', encoding='utf-8').write(
        json.dumps(entries, ensure_ascii=False, indent=1))

    total = sum(counts.values())
    summary = ', '.join('%s: %d' % (b, n) for b, n in sorted(counts.items()))
    print('%s -> %d keys (%s)' % (KV_BULK_JSON, total, summary))


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'migrate':
        cmd_migrate(force='--force' in args)
    elif not args or args[0] == 'build':
        cmd_build()
    else:
        print('usage: python scripts/build_pcode.py [migrate [--force] | build]')
        sys.exit(1)
