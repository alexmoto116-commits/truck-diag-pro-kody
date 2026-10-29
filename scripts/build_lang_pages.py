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


# I18N, RISK_TX, FMI_I18N, RISK_LVL в app.js - объектные литералы JS (ключи
# без кавычек), а не JSON, поэтому читаем их через eval в Node, а не парсером.
# Границу литерала ищем счётчиком скобок от знака равенства.
#
# Массивы (FMI_ELEC) читаются тем же кодом: скобку-открывашку не задаём
# заранее, а берём ту, что стоит после «=», и ищем парную ей. Пробелы между
# именем и «=» произвольные - в app.js константы выровнены в колонку, и
# прежний поиск подстроки «var <ИМЯ> = {» на них уже не срабатывал.
def extract_js_object(name='I18N'):
    app_js = os.path.join(ROOT, 'assets', 'app.js').replace('\\', '/')
    node_script = (
        "const fs=require('fs');"
        "const src=fs.readFileSync(%r,'utf8');"
        "const key='var '+%r;"
        "let i=-1;"
        "for(let p=src.indexOf(key);p>=0;p=src.indexOf(key,p+1)){"
        "let q=p+key.length;"
        "while(q<src.length&&src.charCodeAt(q)<=32)q++;"
        "if(src[q]==='='){i=q+1;break;}"
        "}"
        "if(i<0)throw new Error('not declared: '+%r);"
        "while(i<src.length&&src.charCodeAt(i)<=32)i++;"
        "const open=src[i];"
        "if(open!=='{'&&open!=='[')throw new Error('not a literal: '+%r);"
        "const close=open==='{'?'}':']';"
        "let depth=0,end=-1;"
        "for(let j=i;j<src.length;j++){"
        "if(src[j]===open)depth++;"
        "else if(src[j]===close){depth--;if(depth===0){end=j;break;}}"
        "}"
        "if(end<0)throw new Error('unbalanced: '+%r);"
        "const OBJ=eval('('+src.slice(i,end+1)+')');"
        "process.stdout.write(JSON.stringify(OBJ));"
    ) % (app_js, name, name, name, name)
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
# То же самое теперь верно и для /marki/ и /problemy/ (см.
# scripts/build_en_marki_problemy.py) - раньше эти два раздела были
# единственным местом, где любая языковая версия всё равно утаскивала
# на русский текст.
def point_to_en(html):
    def spn(m):
        page = 'en/kody/spn-%s.html' % m.group(1)
        return ('href="/%s"' % page) if os.path.isfile(os.path.join(ROOT, page)) else m.group(0)

    def brand(m):
        page = 'en/marki/%s.html' % m.group(1)
        return ('href="/%s"' % page) if os.path.isfile(os.path.join(ROOT, page)) else m.group(0)

    def symptom(m):
        page = 'en/problemy/%s.html' % m.group(1)
        return ('href="/%s"' % page) if os.path.isfile(os.path.join(ROOT, page)) else m.group(0)

    html = re.sub(r'href="/kody/spn-(\d+)\.html"', spn, html)
    html = re.sub(r'href="/marki/([a-z0-9]+)\.html"', brand, html)
    html = re.sub(r'href="/problemy/([a-z-]+)\.html"', symptom, html)
    if os.path.isfile(os.path.join(ROOT, 'en', 'kody', 'index.html')):
        html = html.replace('href="/kody/"', 'href="/en/kody/"')
    if os.path.isfile(os.path.join(ROOT, 'en', 'marki', 'index.html')):
        html = html.replace('href="/marki/"', 'href="/en/marki/"')
    if os.path.isfile(os.path.join(ROOT, 'en', 'problemy', 'index.html')):
        html = html.replace('href="/problemy/"', 'href="/en/problemy/"')
    return html


# Числа на главной считаем из данных, а не держим в тексте.
# Марки: ключи таблиц brands (с тахографами и блоками КамАЗ/ZF) плюс дилерские
# pcode - 72 сейчас. Коды: строки brands плюс строки pcode - 39 054 сейчас.
# Округление вниз: 70+ марок, 39 000+ кодов. Тот же набор, что уже даёт
# 72 и 39 054 в аудите (отдельно тахографы: 5 марок и 246 кодов).
# Текст со старыми числами живёт в index.html и в I18N (assets/app.js). Здесь
# подставляем новые числа по шаблонам; если шаблон не нашёлся - падаем, а не
# оставляем старое число молча.
def home_counts():
    """(марок, кодов) по данным; None, если нет pcode-source (чужой чекаут)."""
    import base64
    path_pcode = os.path.join(ROOT, 'pcode-source', 'pcode.json')
    if not os.path.isfile(path_pcode):
        return None
    raw = io.open(os.path.join(ROOT, 'assets', 'dtc.enc.js'), encoding='utf-8').read()
    db = json.loads(base64.b64decode(re.search(r"b64='([^']+)'", raw).group(1)).decode('utf-8'))
    pcode = json.loads(io.open(path_pcode, encoding='utf-8').read())
    # Марки - это позиции списка выбора на сайте (DB.brandNames): марки техники,
    # системы и агрегаты, отопители, тахографы. Блоки КАМАЗ (kamaz5490, kamazebs,
    # kamazecas, zfintarder) в brandNames не входят, поэтому в счёт не идут.
    brands = set(db['brandNames']) | set(pcode)
    # Коды - как есть: строки брендов из базы плюс pcode.
    codes = sum(len(t) for t in db['brands'].values()) + sum(len(t) for t in pcode.values())
    return len(brands), codes


def _sub_once(text, pattern, repl, expect, where):
    new, n = re.subn(pattern, repl, text)
    if n != expect:
        raise ValueError(u'%s: шаблон %r нашёлся %d раз, ожидалось %d - поправить шаблон в build_lang_pages.py'
                         % (where, pattern, n, expect))
    return new


def patch_counts(text, counts, where, meta=False):
    """Подставляет марки и коды в текст главной.
    meta=True - поле description (в I18N там «12 марок» / «12 makes» и т.д.);
    иначе - строка purposeStats («70+ маркам», «31 000+ кодов», «31.000 códigos»).
    Знак «+» и разделитель тысяч берём из исходного текста, меняем только число."""
    brands, codes = counts
    b_val = brands // 10 * 10
    c_val = codes // 1000 * 1000
    if meta:
        # 12 - старое число в исходнике, 80 - уже вписанное: шаблон ловит любое из двух.
        return _sub_once(text, r'(?<![\d.,])(?:12|80)\+?(?![\d.,])', u'%d+' % b_val, 1, where)

    def codes_repl(m):
        sep = m.group(1) or u''
        return str(c_val)[:-3] + sep + u'000'

    text = _sub_once(text, r'(?<![\d.,])(?:70|80)(\+?)', lambda m: u'%d%s' % (b_val, m.group(1)), 1, where)
    return _sub_once(text, r'(?:31|39)([ ,.  ]?)000(?!\d)', codes_repl, 1, where)


def patch_root_meta(text, counts, where):
    """Русский index.html: description и og:description содержат «60 марок»."""
    brands, _ = counts
    # 60 и 70 - прежние значения, 80+ - уже подставленное: шаблон идемпотентен.
    return _sub_once(text, r'(?<![\d.,])(?:60|70|80)\+?(?= марок)', u'%d+' % (brands // 10 * 10), 2, where)


# Переключатель языков внизу главной. Разметка лежит в index.html (ru); здесь его
# оставляем только на ru и en. На остальных девяти главных язык уже выбирается в
# шапке, поэтому там блок убираем. Для en строим свой: русская ссылка на корень,
# текущий язык - обычным текстом.
LANG_NAV_RE = re.compile(r'<nav class="langlinks".*?</nav>\n?', re.S)
LANG_NAV_LABELS = [('ru', u'Русский'), ('en', u'English'), ('de', u'Deutsch'), ('fr', u'Français'),
                   ('es', u'Español'), ('pt', u'Português'), ('pl', u'Polski'), ('tr', u'Türkçe'),
                   ('hi', u'हिन्दी'), ('zh', u'中文')]


def lang_nav(html, lang):
    nav = u''
    if lang == 'en':
        links = []
        for code, name in LANG_NAV_LABELS:
            if code == 'en':
                links.append(u'<span class="langlinks-cur" lang="en">%s</span>' % name)
            else:
                href = u'/' if code == 'ru' else u'/%s/' % code
                links.append(u'<a href="%s" hreflang="%s" lang="%s">%s</a>' % (href, code, code, name))
        nav = u'<nav class="langlinks" aria-label="Site languages">%s</nav>\n' % u''.join(links)
    new, n = LANG_NAV_RE.subn(lambda m: nav, html, count=1)
    if n != 1:
        raise ValueError(u'langlinks: в главной нет блока переключателя языков (%s)' % lang)
    return new


def build():
    i18n = extract_i18n()
    ru_html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    counts = home_counts()
    if counts is None:
        print(u'pcode-source не найден: числа на главной не пересчитаны')
    else:
        new_root = patch_root_meta(ru_html, counts, 'index.html')
        # Строку «31 000+ кодов ... 70+ маркам» берём только из её элемента: цифра 70
        # встречается в index.html и вне него (стили, цвета).
        new_root, n_stats = re.subn(
            r'(<p class="stats" data-i18n="purposeStats">)(.*?)(</p>)',
            lambda m: m.group(1) + patch_counts(m.group(2), counts, 'index.html purposeStats') + m.group(3),
            new_root, count=1, flags=re.S)
        if n_stats != 1:
            raise ValueError(u'index.html: нет элемента purposeStats')
        if new_root != ru_html:
            io.open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(new_root)
            print(u'index.html: числа марок и кодов обновлены из данных')
        ru_html = new_root

    # Соцсети (scripts/socials.json): в русский index.html подставляем блоки,
    # из языковых главных вырезаем - ролики русские.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import socials
    _с = socials.sync_index(ru_html)
    if _с != ru_html:
        io.open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline=chr(10)).write(_с)
        print(u'index.html: соцсети обновлены')
        ru_html = _с

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
        d = dict(i18n[lang])
        html = socials.strip_index(base)
        if counts is not None:
            d['metaDescription'] = patch_counts(d['metaDescription'], counts, lang, meta=True)
            d['purposeStats'] = patch_counts(d['purposeStats'], counts, lang)

        html = html.replace('<html lang="ru" data-lock-lang="ru">',
                            '<html lang="%s" data-lock-lang="%s">' % (lang, lang), 1)
        # Заголовок языковой версии - из I18N (pageTitle). Раньше сюда подставлялась
        # строка с другим текстом, чем в index.html, совпадения не было, и все
        # языковые главные оставались с русским title: тег меняем целиком.
        html = _sub_once(html, r'<title>[^<]*</title>',
                         lambda m: u'<title>%s</title>' % d['pageTitle'], 1, 'title %s' % lang)
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
        html = lang_nav(html, lang)

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
