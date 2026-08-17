# -*- coding: utf-8 -*-
"""
Языковые версии главной (codetruck.ru/en/, /de/ и т.д.) под hreflang.

index.html (корень, ru) - источник правды по разметке и оформлению.
Инструмент один на все версии (assets/app.js, см. build_pages.py не
трогает этот файл), а сам HTML главной на 9 языков собирается отсюда:
заголовок/описание/og-теги - на язык версии, все data-i18n элементы -
подставлены строкой из I18N (не оставлены на клиентский JS, чтобы
краулер увидел готовый текст без выполнения скрипта). <html> получает
data-lock-lang - см. assets/app.js: на такой странице язык не
угадывается по браузеру/localStorage, а сам переключатель ведёт на
нужный URL, а не перерисовывает текст на месте.

Запуск из корня репозитория: python scripts/build_lang_pages.py
"""
import io, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://codetruck.ru'
LANGS = ['en', 'de', 'fr', 'es', 'pt', 'pl', 'tr', 'hi', 'zh']
OG_LOCALE = {'en': 'en_US', 'de': 'de_DE', 'fr': 'fr_FR', 'es': 'es_ES', 'pt': 'pt_PT',
             'pl': 'pl_PL', 'tr': 'tr_TR', 'hi': 'hi_IN', 'zh': 'zh_CN'}


# I18N, RISK_TX, FMI_I18N в app.js - объектные литералы JS (ключи без
# кавычек), а не JSON, поэтому читаем их через eval в Node, а не парсером.
# Границу объекта ищем счётчиком скобок от «var <ИМЯ> = {».
def extract_js_object(name='I18N'):
    app_js = os.path.join(ROOT, 'assets', 'app.js').replace('\\', '/')
    node_script = (
        "const fs=require('fs');"
        "const src=fs.readFileSync(%r,'utf8');"
        "const start=src.indexOf('var ' + %r + ' = {');"
        "let i=src.indexOf('{',start),depth=0,end=-1;"
        "for(let j=i;j<src.length;j++){"
        "if(src[j]==='{')depth++;"
        "else if(src[j]==='}'){depth--;if(depth===0){end=j;break;}}"
        "}"
        "const OBJ=eval('('+src.slice(i,end+1)+')');"
        "process.stdout.write(JSON.stringify(OBJ));"
    ) % (app_js, name)
    out = subprocess.run(['node', '-e', node_script], cwd=ROOT,
                          capture_output=True, check=True)
    return json.loads(out.stdout.decode('utf-8'))


def extract_i18n():
    return extract_js_object('I18N')


I18N_TAG_RE = re.compile(r'<(\w+)([^>]*\bdata-i18n="([a-zA-Z0-9]+)"[^>]*)>(.*?)</\1>', re.DOTALL)


def apply_i18n(html, lang_dict):
    def repl(m):
        tag, attrs, key, inner = m.group(1), m.group(2), m.group(3), m.group(4)
        value = lang_dict.get(key)
        if value is None:
            return m.group(0)
        return u'<%s%s>%s</%s>' % (tag, attrs, value, tag)
    return I18N_TAG_RE.sub(repl, html)


# Языковая главная досталась от русской вместе со ссылками на русские же
# карточки кодов: человек переключал язык, кликал первую ссылку и снова
# оказывался в русском тексте. Английские карточки теперь есть (см.
# scripts/build_en_pages.py), и туда уводим не только английскую версию:
# у остальных девяти языков описания неисправностей и так показываются
# по-английски - таково устройство базы, английский тут ближе, чем русский.
# Разделы /marki/ и /problemy/ пока только русские, их не трогаем.
def point_to_en(html):
    def spn(m):
        page = 'en/kody/spn-%s.html' % m.group(1)
        return ('href="/%s"' % page) if os.path.isfile(os.path.join(ROOT, page)) else m.group(0)
    html = re.sub(r'href="/kody/spn-(\d+)\.html"', spn, html)
    if os.path.isfile(os.path.join(ROOT, 'en', 'kody', 'index.html')):
        html = html.replace('href="/kody/"', 'href="/en/kody/"')
    return html


def build():
    i18n = extract_i18n()
    ru_html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

    # Раннего скрипта-подмены языка в index.html больше нет: убран 2026-08-17,
    # потому что Googlebot выполняет JS, представляется английским и получал
    # английские title/description на русском адресе - см. комментарий на его
    # месте в index.html. Если он когда-нибудь вернётся, здесь его вырежем:
    # языковой версии он не нужен, её язык известен из URL.
    early_flash = re.search(r'<script>\n/\* Первый кадр.*?\n</script>\n', ru_html, re.DOTALL)
    base = (ru_html[:early_flash.start()] + ru_html[early_flash.end():]
            if early_flash else ru_html)

    written = []
    for lang in LANGS:
        d = i18n[lang]
        html = base

        html = html.replace('<html lang="ru" data-lock-lang="ru">',
                            '<html lang="%s" data-lock-lang="%s">' % (lang, lang), 1)
        html = html.replace(
            '<title>Код неисправности грузовика — расшифровка SPN/FMI и дилерских кодов</title>',
            u'<title>%s</title>' % d['pageTitle'], 1)
        html = re.sub(
            r'<meta name="description" content="[^"]*">',
            lambda m: u'<meta name="description" content="%s">' % d['metaDescription'].replace('"', '&quot;'),
            html, count=1)
        html = html.replace(
            '<link rel="canonical" href="https://codetruck.ru/">',
            '<link rel="canonical" href="%s/%s/">' % (SITE, lang), 1)
        html = html.replace(
            '<meta property="og:url" content="https://codetruck.ru/">',
            '<meta property="og:url" content="%s/%s/">' % (SITE, lang), 1)
        html = html.replace(
            '<meta property="og:locale" content="ru_RU">',
            '<meta property="og:locale" content="%s">' % OG_LOCALE[lang], 1)
        html = re.sub(
            r'<meta property="og:title" content="[^"]*">',
            lambda m: u'<meta property="og:title" content="%s">' % d['pageTitle'].replace('"', '&quot;'),
            html, count=1)
        html = re.sub(
            r'<meta property="og:description" content="[^"]*">',
            lambda m: u'<meta property="og:description" content="%s">' % d['metaDescription'].replace('"', '&quot;'),
            html, count=1)
        html = html.replace(
            'https://codetruck.ru/","potentialAction"',
            '%s/%s/","potentialAction"' % (SITE, lang), 1)
        html = html.replace(
            'https://codetruck.ru/?q={search_term_string}',
            '%s/%s/?q={search_term_string}' % (SITE, lang), 1)

        html = apply_i18n(html, d)
        html = point_to_en(html)

        out_dir = os.path.join(ROOT, lang)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        out_path = os.path.join(out_dir, 'index.html')
        io.open(out_path, 'w', encoding='utf-8', newline='\n').write(html)
        written.append('%s/index.html' % lang)

    # Языковые главные пишутся последними, поэтому дату в карте сайта им
    # проставляем здесь - иначе она отставала бы ровно на одну сборку.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import build_pages
    build_pages.write_sitemap()

    print(u'языковых версий собрано: %d' % len(written))
    return written


if __name__ == '__main__':
    build()
