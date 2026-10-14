#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ключи доступа приложений к воркеру codetruck-pcode-api (PCODE_KV).

Ключ хранится в KV: apikey:<ключ> -> {"имя", "лимит", "до", "активен", "создан"}.
Воркер (pcode-api.js) читает запись и считает поиски по ключу.

Команды (запускать из папки worker):
  python ключи.py создать "<имя>" [--лимит 50] [--до ГГГГ-ММ-ДД]
  python ключи.py список
  python ключи.py отключить <ключ>
  python ключи.py включить <ключ>
  python ключи.py продлить <ключ> ГГГГ-ММ-ДД
  python ключи.py лимит <ключ> <N>

Флаг --показать (в любой команде) только печатает команды wrangler, ничего не выполняя.

Токен Cloudflare берётся из переменной окружения CLOUDFLARE_API_TOKEN (задаёт Алекс).
Скрипт токен никуда не пишет и в выводе не показывает. Команды выполняются через
`npx wrangler kv key ...` с --binding=PCODE_KV --remote.
"""

import argparse
import datetime
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BINDING = 'PCODE_KV'
PREFIX = 'apikey:'
KEY_RE = re.compile(r'^ct_[a-z0-9]{24}$')
ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789'
DEFAULT_LIMIT = 50  # совпадает с DAILY_LIMIT_PER_DAY в pcode-api.js
TARIFFS = ('платный', 'демо')
DEFAULT_TARIFF = 'платный'


def fail(msg):
    print('ОШИБКА: ' + msg, file=sys.stderr)
    sys.exit(1)


def new_key():
    return 'ct_' + ''.join(secrets.choice(ALPHABET) for _ in range(24))


def check_key(key):
    if not KEY_RE.match(key):
        fail('неверный формат ключа: нужен ct_ + 24 символа a-z0-9')


def check_date(value):
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        fail('дата должна быть в формате ГГГГ-ММ-ДД, а не «%s»' % value)
    return value


def check_tariff(value):
    if value not in TARIFFS:
        fail('тариф должен быть «платный» или «демо», а не «%s»' % value)
    return value


def check_limit(value):
    try:
        n = int(value)
    except ValueError:
        fail('лимит должен быть целым числом')
    if n <= 0:
        fail('лимит должен быть больше нуля')
    return n


def wrangler(*args):
    """Команда wrangler kv key ... для PCODE_KV (список аргументов, без shell)."""
    npx = shutil.which('npx')
    if not npx:
        fail('не найден npx (нужен Node.js в PATH)')
    return [npx, 'wrangler', 'kv', 'key'] + list(args) + ['--binding=' + BINDING, '--remote']


def show_cmd(cmd):
    """Строка команды для печати (без токена: он в переменной окружения и сюда не попадает)."""
    return ' '.join(cmd)


def need_token(show):
    if not show and not os.environ.get('CLOUDFLARE_API_TOKEN'):
        fail('не задана переменная CLOUDFLARE_API_TOKEN (в PowerShell: $env:CLOUDFLARE_API_TOKEN = "...")')


def run(cmd):
    """Выполняет команду wrangler и возвращает stdout. Ошибку выводит без токена."""
    try:
        p = subprocess.run(cmd, cwd=HERE, stdin=subprocess.DEVNULL, capture_output=True,
                           text=True, encoding='utf-8', errors='replace', timeout=300)
    except (OSError, subprocess.SubprocessError) as e:
        fail('не удалось запустить wrangler: %s' % e)
    if p.returncode != 0:
        fail('wrangler завершился с кодом %d:\n%s' % (p.returncode, (p.stderr or p.stdout).strip()))
    return p.stdout


def put_record(key, record, show):
    """Записывает запись ключа в KV через временный файл (JSON не попадает в командную строку)."""
    if show:
        print('  ' + show_cmd(wrangler('put', PREFIX + key, '--path=<временный файл>')))
        print('  содержимое: ' + json.dumps(record, ensure_ascii=False))
        return
    fd, path = tempfile.mkstemp(suffix='.json', prefix='apikey-')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False)
        run(wrangler('put', PREFIX + key, '--path=' + path))
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def get_record(key, show):
    """Читает запись ключа из KV. В режиме --показать возвращает None."""
    cmd = wrangler('get', PREFIX + key, '--text')
    if show:
        print('  ' + show_cmd(cmd))
        return None
    out = run(cmd).strip()
    try:
        rec = json.loads(out)
    except ValueError:
        fail('ключ %s не найден в базе' % key)
    if not isinstance(rec, dict):
        fail('ключ %s: запись имеет неверный вид' % key)
    return rec


def list_keys(show):
    """Список ключей apikey: из KV. В режиме --показать возвращает None."""
    cmd = wrangler('list', '--prefix=' + PREFIX)
    if show:
        print('  ' + show_cmd(cmd))
        return None
    out = run(cmd)
    start, end = out.find('['), out.rfind(']')
    if start < 0 or end < start:
        fail('неожиданный ответ wrangler при списке ключей')
    try:
        items = json.loads(out[start:end + 1])
    except ValueError:
        fail('не удалось разобрать список ключей')
    names = [i['name'] for i in items if isinstance(i, dict) and 'name' in i]
    return [n[len(PREFIX):] for n in names if n.startswith(PREFIX)]


def cmd_create(args):
    name = args.имя.strip()
    if not name:
        fail('имя ключа не может быть пустым')
    limit = check_limit(args.лимит) if args.лимит is not None else DEFAULT_LIMIT
    until = check_date(args.до) if args.до else None
    tariff = check_tariff(args.тариф)
    key = new_key()
    record = {
        'имя': name,
        'лимит': limit,
        'до': until,
        'тариф': tariff,
        'активен': True,
        'создан': datetime.date.today().isoformat(),
    }
    need_token(args.показать)
    put_record(key, record, args.показать)
    if args.показать:
        return
    line = '=' * 64
    print(line)
    print('  Ключ для «%s»:' % name)
    print()
    print('      ' + key)
    print()
    print('  лимит: %d поисков в сутки, до: %s, тариф: %s' % (limit, until or 'без срока', tariff))
    print('  Передайте ключ приложению (заголовок X-Codetruck-Key). Сохраните его: в базе он хранится открыто.')
    print(line)


def cmd_list(args):
    need_token(args.показать)
    keys = list_keys(args.показать)
    if args.показать:
        return
    if not keys:
        print('Ключей нет.')
        return
    print('%-28s %-24s %8s %-12s %-9s %s' % ('ключ', 'имя', 'лимит', 'до', 'тариф', 'активен'))
    for key in keys:
        rec = get_record(key, False) or {}
        print('%-28s %-24s %8s %-12s %-9s %s' % (
            key,
            str(rec.get('имя', '?'))[:24],
            rec.get('лимит', DEFAULT_LIMIT),
            rec.get('до') or 'без срока',
            rec.get('тариф', DEFAULT_TARIFF),
            'да' if rec.get('активен', True) else 'нет'))


def change(args, field, value, describe):
    key = args.ключ.strip()
    check_key(key)
    need_token(args.показать)
    if args.показать:
        print('  чтение записи:')
        get_record(key, True)
        print('  запись с изменением (' + describe + '):')
        put_record(key, {'изменено': describe}, True)
        return
    rec = get_record(key, False)
    rec[field] = value
    put_record(key, rec, False)
    print('Готово: ' + describe)


def cmd_disable(args):
    change(args, 'активен', False, 'ключ %s отключён' % args.ключ)


def cmd_enable(args):
    change(args, 'активен', True, 'ключ %s включён' % args.ключ)


def cmd_extend(args):
    until = check_date(args.дата)
    change(args, 'до', until, 'ключ %s действует до %s' % (args.ключ, until))


def cmd_tariff(args):
    tariff = check_tariff(args.тариф)
    change(args, 'тариф', tariff, 'ключ %s: тариф %s' % (args.ключ, tariff))


def cmd_limit(args):
    limit = check_limit(args.N)
    change(args, 'лимит', limit, 'ключ %s: лимит %d поисков в сутки' % (args.ключ, limit))


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--показать', action='store_true',
                        help='только печатать команды wrangler, ничего не выполнять')

    p = argparse.ArgumentParser(description='Ключи доступа приложений к воркеру codetruck-pcode-api.')
    sub = p.add_subparsers(dest='команда', required=True)

    c = sub.add_parser('создать', parents=[common], help='создать новый ключ')
    c.add_argument('имя', help='название приложения или человека')
    c.add_argument('--лимит', type=str, default=None, help='поисков в сутки (по умолчанию 50)')
    c.add_argument('--до', type=str, default=None, help='срок ГГГГ-ММ-ДД (по умолчанию без срока)')
    c.add_argument('--тариф', type=str, default=DEFAULT_TARIFF, help='платный (по умолчанию) или демо')
    c.set_defaults(func=cmd_create)

    s = sub.add_parser('список', parents=[common], help='показать ключи')
    s.set_defaults(func=cmd_list)

    d = sub.add_parser('отключить', parents=[common], help='отключить ключ')
    d.add_argument('ключ')
    d.set_defaults(func=cmd_disable)

    e = sub.add_parser('включить', parents=[common], help='включить ключ')
    e.add_argument('ключ')
    e.set_defaults(func=cmd_enable)

    x = sub.add_parser('продлить', parents=[common], help='поставить срок действия')
    x.add_argument('ключ')
    x.add_argument('дата', help='ГГГГ-ММ-ДД')
    x.set_defaults(func=cmd_extend)

    tf = sub.add_parser('тариф', parents=[common], help='поменять тариф ключа (платный или демо)')
    tf.add_argument('ключ')
    tf.add_argument('тариф', help='платный или демо')
    tf.set_defaults(func=cmd_tariff)

    lm = sub.add_parser('лимит', parents=[common], help='поменять суточный лимит ключа')
    lm.add_argument('ключ')
    lm.add_argument('N', help='поисков в сутки')
    lm.set_defaults(func=cmd_limit)
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
