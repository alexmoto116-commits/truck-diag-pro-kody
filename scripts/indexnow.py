# -*- coding: utf-8 -*-
"""
Отправка новых и изменившихся адресов в IndexNow (Яндекс, Bing и др.).

Адреса берутся из карт сайта: sitemap.xml - индекс, он ссылается на карты
по разделам (sitemap-ru-kody.xml и т.д.). Закрытые от индекса страницы
в карты не попадают, так что отправляются только открытые адреса.

По умолчанию отправляются только изменившиеся адреса: для каждого адреса
запоминается хэш файла страницы в scripts/indexnow-state.json (он пишется
после успешной отправки). Адрес уходит, если его не было в состоянии или
хэш изменился. Первый запуск без файла состояния отправит все адреса один раз.

Ключ лежит в корне сайта файлом <ключ>.txt - поисковик сверяет его
с keyLocation, поэтому запускать ПОСЛЕ выкладки на сайт (после git push),
иначе файл ключа ещё не доступен и запрос будет отклонён.

Запуск из корня репозитория:
    python -X utf8 scripts/indexnow.py             - только изменившиеся
    python -X utf8 scripts/indexnow.py --all       - все адреса (как раньше)
    python -X utf8 scripts/indexnow.py --dry-run   - напечатать адреса, без сети и без записи состояния
    python -X utf8 scripts/indexnow.py --seed      - записать состояние по текущим файлам, без сети
                                                     (запускать, когда файлы в репозитории = живой сайт)
"""
import argparse, hashlib, io, json, os, sys
import urllib.request
import xml.etree.ElementTree as ET

HOST = 'codetruck.ru'
KEY = '3e48dd7e20f477f1e1ea01f3ac73d71b'  # совпадает с именем файла в корне сайта
KEY_LOCATION = 'https://%s/%s.txt' % (HOST, KEY)
ENDPOINT = 'https://api.indexnow.org/indexnow'
LIMIT = 10000  # максимум адресов в одном запросе
NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Состояние лежит в scripts/, а не в корне сайта, чтобы не публиковаться вместе с сайтом.
STATE = os.path.join(ROOT, 'scripts', 'indexnow-state.json')


def read_locs(path):
    tree = ET.parse(path)
    return [e.text.strip() for e in tree.iter(NS + 'loc') if e.text]


def collect_urls():
    """Адреса из всех карт, на которые ссылается sitemap.xml (без повторов)."""
    index_path = os.path.join(ROOT, 'sitemap.xml')
    urls, seen = [], set()
    for child in read_locs(index_path):
        name = os.path.basename(child)
        for u in read_locs(os.path.join(ROOT, name)):
            if u not in seen:
                seen.add(u)
                urls.append(u)
    return urls


def page_file(url):
    """Файл страницы на диске для адреса - то же правило, что в build_pages.url_to_file."""
    rel = url[len('https://' + HOST):].lstrip('/')
    if rel == '' or rel.endswith('/'):
        rel += 'index.html'
    return os.path.join(ROOT, rel.replace('/', os.sep))


def page_hash(url):
    """Хэш содержимого страницы или None, если файла нет (адрес не отправляем)."""
    path = page_file(url)
    if not os.path.isfile(path):
        return None
    return hashlib.sha1(io.open(path, 'rb').read()).hexdigest()[:12]


def load_state():
    if not os.path.isfile(STATE):
        return {}
    return json.loads(io.open(STATE, encoding='utf-8').read())


def save_state(state):
    io.open(STATE, 'w', encoding='utf-8').write(
        json.dumps(state, ensure_ascii=False, indent=0, sort_keys=True))


def main():
    ap = argparse.ArgumentParser(description='Отправка адресов в IndexNow')
    ap.add_argument('--all', action='store_true',
                    help='отправить все адреса карт, а не только изменившиеся')
    ap.add_argument('--dry-run', action='store_true',
                    help='только напечатать адреса к отправке: без сети и без записи состояния')
    ap.add_argument('--seed', action='store_true',
                    help='записать состояние по текущим файлам страниц, без сети; '
                         'запускать, когда репозиторий совпадает с живым сайтом')
    args = ap.parse_args()

    if args.seed:
        urls = collect_urls()
        hashes = {}
        for u in urls:
            h = page_hash(u)
            if h is not None:
                hashes[u] = h
        save_state(hashes)
        print('состояние записано: адресов %d, с файлом страницы %d -> %s'
              % (len(urls), len(hashes), STATE))
        return

    key_file = os.path.join(ROOT, KEY + '.txt')
    if not os.path.isfile(key_file):
        sys.exit('нет файла ключа %s - сначала выложите сайт' % key_file)
    if io.open(key_file, encoding='utf-8').read().strip() != KEY:
        sys.exit('содержимое файла ключа не совпадает с KEY')

    urls = collect_urls()
    if not urls:
        sys.exit('карты сайта пусты - нечего отправлять')

    hashes = {}
    no_file = []
    for u in urls:
        h = page_hash(u)
        if h is None:
            no_file.append(u)
        else:
            hashes[u] = h

    state = load_state()
    if args.all:
        to_send = [u for u in urls if u in hashes]
    else:
        to_send = [u for u in urls if u in hashes and state.get(u) != hashes[u]]

    print('адресов в картах: %d, файла страницы нет: %d, к отправке: %d (%s)'
          % (len(urls), len(no_file), len(to_send),
             'все' if args.all else 'изменившиеся с прошлой отправки'))
    if not to_send:
        print('нечего отправлять')
        return
    if len(to_send) > LIMIT:
        sys.exit('адресов %d, больше лимита %d за один запрос' % (len(to_send), LIMIT))

    if args.dry_run:
        for u in to_send:
            print(u)
        print('сухой прогон: сеть не трогали, состояние не записано')
        return

    body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': KEY_LOCATION,
                       'urlList': to_send}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(ENDPOINT, data=body, method='POST',
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status = r.status
    except urllib.error.HTTPError as e:
        status = e.code
    # 200 и 202 - приняты; 403 - ключ не найден на сайте; 422 - адреса не того хоста
    print('адресов отправлено: %d, ответ IndexNow: %s' % (len(to_send), status))
    if status in (200, 202):
        # состояние - только после успешной отправки, иначе при ошибке адреса потеряются
        save_state({u: hashes[u] for u in hashes})
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
