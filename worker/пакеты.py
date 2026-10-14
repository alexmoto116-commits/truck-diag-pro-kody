#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Пакеты данных моделей КАМАЗ в KV воркера codetruck-pcode-api (PCODE_KV).

Пакет модели - файл пакет-<модель>.json (например пакет-6520.json). В KV он лежит
как pack:<модель>, воркер отдаёт его по GET /pack?model=<модель> с ключом, где эта
модель есть (см. pcode-api.js, блок «Пакеты моделей»). При каждой выдаче в пакет
вшивается метка ключа: поле _выдано и скрытые символы в названиях единиц.

Команды (запускать из папки worker):
  python пакеты.py залить <папка_с_пакетами> [--показать]
  python пакеты.py список [--показать]
  python пакеты.py чья-метка <файл_пакета> [--ключи <файл>]

залить - кладёт каждый пакет-<модель>.json в KV как pack:<модель>.
список - какие пакеты лежат в KV (kv key list --prefix=pack:).
чья-метка - читает метку из (скопированного) файла пакета и находит, какому ключу
из базы она принадлежит: по полю _выдано (sha-256 первых 12 hex) и по скрытым битам.
--ключи <файл> - список ключей вместо базы (строки «ct_... имя», без сети).
Без --ключи список берётся из базы: kv key list --prefix=apikey: (нужен токен).

Флаг --показать (в залить и списке) только печатает команды wrangler.
Токен Cloudflare берётся из переменной CLOUDFLARE_API_TOKEN и не печатается.
"""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK_PREFIX = 'pack:'
FILE_RE = re.compile(r'^пакет-([A-Za-z0-9]{1,16})\.json$')
MAX_BYTES = 24 * 1024 * 1024   # значение KV до 25 МБ
ZW0 = '​'
ZW1 = '‌'
MARK_UNITS = 8                 # единиц с меткой (как в воркере)


def fail(msg):
    print('ОШИБКА: ' + msg, file=sys.stderr)
    sys.exit(1)


def load_keys_module():
    """Модуль ключи.py (имя с кириллицей) - берём wrangler, run, список ключей."""
    path = os.path.join(HERE, 'ключи.py')
    spec = importlib.util.spec_from_file_location('ключи_модуль', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


K = load_keys_module()


def read_pack(path):
    if os.path.getsize(path) > MAX_BYTES:
        fail('пакет больше 24 МБ: %s' % path)
    with open(path, encoding='utf-8') as f:
        try:
            pack = json.load(f)
        except ValueError as e:
            fail('%s: не JSON (%s)' % (path, e))
    if not isinstance(pack, dict):
        fail('%s: верхний уровень пакета должен быть объектом' % path)
    return pack


def kv_names(out, prefix):
    """Имена ключей из ответа `wrangler kv key list` (JSON-массив внутри текста)."""
    start, end = out.find('['), out.rfind(']')
    if start < 0 or end < start:
        fail('неожиданный ответ wrangler при списке')
    try:
        items = json.loads(out[start:end + 1])
    except ValueError:
        fail('не удалось разобрать список из wrangler')
    names = [i['name'] for i in items if isinstance(i, dict) and 'name' in i]
    return [n[len(prefix):] for n in names if n.startswith(prefix)]


def cmd_zalit(args):
    folder = os.path.abspath(args.папка)
    if not os.path.isdir(folder):
        fail('нет папки: ' + folder)
    files = sorted(f for f in os.listdir(folder) if FILE_RE.match(f))
    if not files:
        fail('в папке нет файлов пакет-<модель>.json: ' + folder)
    plan = []
    for f in files:
        model = FILE_RE.match(f).group(1)
        path = os.path.join(folder, f)
        read_pack(path)  # проверка JSON до заливки
        plan.append((model, path))
    K.need_token(args.показать)
    for model, path in plan:
        cmd = K.wrangler('put', PACK_PREFIX + model, '--path=' + path)
        if args.показать:
            print('  ' + K.show_cmd(cmd))
            continue
        K.run(cmd)
        print('залит: %s (%d байт)' % (PACK_PREFIX + model, os.path.getsize(path)))
    if not args.показать:
        print('Готово: пакетов %d.' % len(plan))


def cmd_spisok(args):
    K.need_token(args.показать)
    cmd = K.wrangler('list', '--prefix=' + PACK_PREFIX)
    if args.показать:
        print('  ' + K.show_cmd(cmd))
        return
    models = kv_names(K.run(cmd), PACK_PREFIX)
    if not models:
        print('Пакетов в KV нет.')
        return
    for m in sorted(models):
        print('pack:' + m)


def decode_hidden(pack):
    """Скрытые биты: по 4 символа в конце названий первых восьми помеченных единиц.
    Возвращает (8 hex или None, сколько единиц помечено)."""
    units = pack.get('единицы')
    if not isinstance(units, list):
        return None, 0
    tails = []
    for u in units:
        t = u.get('т') if isinstance(u, dict) else None
        if not isinstance(t, str) or len(t) < 4:
            continue
        tail = t[-4:]
        if all(c in (ZW0, ZW1) for c in tail):
            tails.append(tail)
    if len(tails) < MARK_UNITS:
        return None, len(tails)
    v = 0
    for tail in tails[:MARK_UNITS]:
        n = 0
        for c in tail:
            n = (n << 1) | (1 if c == ZW1 else 0)
        v = (v << 4) | n
    return '%08x' % (v & 0xFFFFFFFF), len(tails)


def candidate_keys(path):
    """Пары (ключ, имя): из файла --ключи или из базы KV."""
    out = []
    if path:
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(None, 1)
                if parts and K.KEY_RE.match(parts[0]):
                    out.append((parts[0], parts[1] if len(parts) > 1 else ''))
        return out
    K.need_token(False)
    for key in K.list_keys(False):
        if not K.KEY_RE.match(key):
            continue
        rec = K.get_record(key, False) or {}
        out.append((key, str(rec.get('имя', ''))))
    return out


def cmd_chya(args):
    pack = read_pack(args.файл)
    выд = pack.get('_выдано')
    hidden, marked = decode_hidden(pack)
    print('Файл: ' + args.файл)
    if isinstance(выд, dict):
        print('  поле _выдано: модель %s, дата %s, отпечаток к=%s'
              % (выд.get('м'), выд.get('д'), выд.get('к')))
    else:
        print('  поля _выдано нет (пакет без метки или метка удалена)')
    if hidden is None:
        print('  скрытая метка: нет (помечено единиц: %d из %d)' % (marked, MARK_UNITS))
    else:
        print('  скрытая метка: %s' % hidden)
    keys = candidate_keys(args.ключи)
    if not keys:
        fail('нет ключей для сопоставления')
    found = []
    for key, name in keys:
        h = hashlib.sha256(key.encode('utf-8')).digest()
        by_field = isinstance(выд, dict) and выд.get('к') == h.hex()[:12]
        by_hidden = hidden is not None and hidden == h[:4].hex()
        if by_field or by_hidden:
            found.append((key, name, by_field, by_hidden))
    if not found:
        print('Совпадений нет среди %d ключей (метка чужая или ключа уже нет в базе).' % len(keys))
        return
    for key, name, by_field, by_hidden in found:
        how = []
        if by_field:
            how.append('поле _выдано')
        if by_hidden:
            how.append('скрытая метка')
        print('Совпадение: %s «%s» - %s' % (key, name, ', '.join(how)))


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--показать', action='store_true',
                        help='только печатать команды wrangler, ничего не выполнять')
    p = argparse.ArgumentParser(description='Пакеты данных моделей в KV воркера codetruck-pcode-api.')
    sub = p.add_subparsers(dest='команда', required=True)

    z = sub.add_parser('залить', parents=[common], help='залить пакеты pack:<модель> в KV')
    z.add_argument('папка', help='папка с файлами пакет-<модель>.json')
    z.set_defaults(func=cmd_zalit)

    s = sub.add_parser('список', parents=[common], help='показать пакеты в KV')
    s.set_defaults(func=cmd_spisok)

    c = sub.add_parser('чья-метка', help='найти, чьему ключу принадлежит пакет')
    c.add_argument('файл', help='файл пакета (скопированный)')
    c.add_argument('--ключи', default=None, help='файл со списком ключей (без сети)')
    c.set_defaults(func=cmd_chya)
    return p


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    args = build_parser().parse_args()
    os.chdir(HERE)
    args.func(args)


if __name__ == '__main__':
    main()
