# -*- coding: utf-8 -*-
"""
Отправка новых и изменившихся адресов в IndexNow (Яндекс, Bing и др.).

Адреса берутся из карт сайта: sitemap.xml - индекс, он ссылается на карты
по разделам (sitemap-ru-kody.xml и т.д.). Закрытые от индекса страницы
в карты не попадают, так что отправляются только открытые адреса.

Ключ лежит в корне сайта файлом <ключ>.txt - поисковик сверяет его
с keyLocation, поэтому запускать ПОСЛЕ выкладки на сайт (после git push),
иначе файл ключа ещё не доступен и запрос будет отклонён.

Запуск из корня репозитория:
    python -X utf8 scripts/indexnow.py
"""
import io, json, os, re, sys
import urllib.request
import xml.etree.ElementTree as ET

HOST = 'codetruck.ru'
KEY = '3e48dd7e20f477f1e1ea01f3ac73d71b'  # совпадает с именем файла в корне сайта
KEY_LOCATION = 'https://%s/%s.txt' % (HOST, KEY)
ENDPOINT = 'https://api.indexnow.org/indexnow'
LIMIT = 10000  # максимум адресов в одном запросе
NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def main():
    key_file = os.path.join(ROOT, KEY + '.txt')
    if not os.path.isfile(key_file):
        sys.exit('нет файла ключа %s - сначала выложите сайт' % key_file)
    if io.open(key_file, encoding='utf-8').read().strip() != KEY:
        sys.exit('содержимое файла ключа не совпадает с KEY')

    urls = collect_urls()
    if not urls:
        sys.exit('карты сайта пусты - нечего отправлять')
    if len(urls) > LIMIT:
        sys.exit('адресов %d, больше лимита %d за один запрос' % (len(urls), LIMIT))

    body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': KEY_LOCATION,
                       'urlList': urls}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(ENDPOINT, data=body, method='POST',
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status = r.status
    except urllib.error.HTTPError as e:
        status = e.code
    # 200 и 202 - приняты; 403 - ключ не найден на сайте; 422 - адреса не того хоста
    print('адресов отправлено: %d, ответ IndexNow: %s' % (len(urls), status))


if __name__ == '__main__':
    main()
