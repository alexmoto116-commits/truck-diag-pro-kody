# -*- coding: utf-8 -*-
"""
Отдельные страницы кодов автономных отопителей (Eberspächer, Webasto, Планар):
  otopiteli/<марка>-<код>.html, en/otopiteli/<марка>-<код>.html,
  оглавления otopiteli/index.html и en/otopiteli/index.html.

Данные - pcode-source/pcode.json, только чтение. Коды Eberspächer, у которых
в тексте стоит «модель отопителя не определена, не подтверждено», получают
<meta name="robots" content="noindex,follow"> и в карты сайта не попадают.

Вызывается из scripts/build_pages.py (build() передаёт сюда свой pcode и берёт
список адресов для карт). Отдельно запускать не нужно.
"""
import io, json, os, re, sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp                                    # noqa: E402

SITE = bp.SITE
BRANDS = bp.HEATER_BRANDS
NAME_RU = {'eberspacher': u'Eberspächer', 'webasto': u'Webasto', 'planar': u'Планар'}
NAME_EN = {'eberspacher': u'Eberspächer', 'webasto': u'Webasto', 'planar': u'Planar'}
UNCONFIRMED = u'не подтверждено'
ROBOTS_NOINDEX = u'<meta name="robots" content="noindex,follow">\n'

# Выпуск частями: страница кода создаётся только для кода из партии с датой
# не позже даты сборки. Партии - в scripts/heater_release.json.
RELEASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heater_release.json')
HEATER_EXAMPLE_RU = u'031'
HEATER_EXAMPLE_EN = u'031'

# Тексты страниц кодов (тема по заводскому тексту, общие блоки) - scripts/heater_texts.json.
# Тема подбирается по русскому тексту кода: первая подошедшая из списка topics.
TEXTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heater_texts.json')
MIN_WORDS = 250
SECTION_HEAD = {
    'ru': {'what': u'Что означает код', 'causes': u'Почему появляется',
           'zero_causes': u'Почему ошибки может не быть',
           'causes_intro': u'Чаще всего первая причина, дальше примерно по убыванию вероятности:',
           'steps': u'Порядок действий', 'check': u'Что проверить самому',
           'check_intro': u'Простые проверки без разборки:',
           'service': u'Когда нужен сервис', 'drive': u'Можно ли ехать и ночевать',
           'danger': u'Чем это опасно'},
    'en': {'what': u'What the code means', 'causes': u'Why it appears',
           'zero_causes': u'Why there may be no code',
           'causes_intro': u'The first cause is the most common; the rest follow roughly in order of likelihood:',
           'steps': u'Steps to take', 'check': u'What to check yourself',
           'check_intro': u'Simple checks, no dismantling:',
           'service': u'When you need a service', 'drive': u'Can you drive and sleep with it',
           'danger': u'Why it matters'},
}

_TEXTS = {}


def texts():
    if not _TEXTS:
        _TEXTS.update(json.loads(io.open(TEXTS_FILE, encoding='utf-8').read()))
    return _TEXTS


def topic_of(ru_text):
    """Первая тема из heater_texts.json, чей шаблон подошёл к русскому тексту кода."""
    for t in texts()['topics']:
        if re.search(t['pattern'], ru_text, re.I):
            return t
    raise ValueError(u'нет темы для кода: %s' % ru_text)


def _li(items):
    return u''.join(u'<li>%s</li>' % bp.esc(x) for x in items)


def topic_sections(lang, entry, text):
    """Разделы страницы кода: что значит, почему, что проверить, сервис, езда, опасность."""
    h = SECTION_HEAD[lang]
    topic = topic_of(entry.get('ru') or '')
    t = topic[lang]
    cm = texts()['common'][lang]
    zero = topic['id'] == 'zero'
    return [
        u'<section><h2>%s</h2><p>%s</p><p>%s</p></section>'
        % (h['what'], bp.esc(text), bp.esc(t['meaning'])),
        u'<section><h2>%s</h2><p>%s</p><ol>%s</ol></section>'
        % (h['zero_causes' if zero else 'causes'], bp.esc(h['causes_intro']), _li(t['causes'])),
        u'<section><h2>%s</h2><ol>%s</ol></section>' % (h['steps'], _li(cm['steps'])),
        u'<section><h2>%s</h2><p>%s</p><ul>%s</ul></section>'
        % (h['check'], bp.esc(h['check_intro']), _li(t['checks'] + cm['checks'])),
        u'<section><h2>%s</h2><p>%s</p><p>%s</p></section>'
        % (h['service'], bp.esc(t['service']), bp.esc(cm['service'])),
        u'<section><h2>%s</h2><p>%s</p><p>%s</p></section>'
        % (h['drive'], bp.esc(cm['drive']), bp.esc(cm['sleep'])),
        u'<section><h2>%s</h2><p>%s</p></section>' % (h['danger'], bp.esc(cm['danger'])),
    ]


TITLE_LIM = 65


def _short(text):
    """Текст кода без скобок-пояснений: «Блокировка отопителя»."""
    return re.sub(r'\s*\([^)]*\)', u'', text).strip().rstrip(u'.')


def _lower_first(s):
    return s[:1].lower() + s[1:] if len(s) > 1 and s[1].islower() else s


def _slug(brand, code):
    return u'%s-%s' % (brand, code.lower())


def _unconfirmed(entry):
    return UNCONFIRMED in (entry.get('ru') or '')


def load_release():
    """Партии из heater_release.json: {'planar:1': '2026-10-17', ...}.
    Код в двух партиях - ошибка данных, падаем сразу."""
    batches = json.loads(io.open(RELEASE_FILE, encoding='utf-8').read())
    out = {}
    for batch in batches:
        for key in batch['keys']:
            if key in out:
                raise ValueError(u'код в двух партиях: %s' % key)
            out[key] = batch['date']
    return out


def make_title(prefix, short, lang_sep=u' — '):
    """Заголовок кода: без многоточия и без названия сайта, не длиннее TITLE_LIM.
    Обрезка по слову - bp.fit_title (build_pages.py)."""
    core = prefix + lang_sep + _lower_first(short) if short else prefix
    title = bp.fit_title(core)
    if len(title) > TITLE_LIM:
        raise ValueError(u'title длиннее %d: %s' % (TITLE_LIM, title))
    return title


def make_desc(lang, prefix, full):
    if lang == 'ru':
        d = (u'%s: %s. Что проверить на месте, соседние коды марки и поиск по вашему коду '
             u'на codetruck.ru.' % (prefix, full))
    else:
        d = (u'%s: %s. What to check on site, the neighbouring codes of this make and a search '
             u'for your code on codetruck.ru.' % (prefix, full))
    return bp.cut_words(d, 160)


def render(lang, rel, title, desc, h1, sub, sections, here, brand=None, noindex=False):
    """Полная HTML-страница. rel - публичный путь файла относительно корня сайта."""
    ru = lang == 'ru'
    pub = rel[:-len('index.html')] if rel.endswith('index.html') else rel
    canon = '%s/%s' % (SITE, pub)
    ru_rel = pub if ru else pub[len('en/'):]
    alt = bp.alt_links(True, ru_rel)
    ld = (bp.ld_script({'@context': 'https://schema.org', '@type': 'TechArticle',
                        'headline': title, 'description': desc, 'url': canon,
                        'inLanguage': lang})
          + bp.ld_script(bp.breadcrumb_ld(here, canon, 'otopiteli') if ru
                         else breadcrumb_en(here, canon)))
    nav = bp.nav_of('otopiteli', here) if ru else nav_en(here)
    head = bp.HEAD.format(title=bp.esc(title), desc=bp.esc(desc), canon=canon,
                          ogtitle=bp.esc(h1), mid=bp.METRIKA_ID, ld=ld, nav=nav,
                          lang=lang, locale='ru_RU' if ru else 'en_US', alt=alt)
    if noindex:
        head = head.replace(u'<meta name="theme-color"', ROBOTS_NOINDEX + u'<meta name="theme-color"', 1)
    body = [head, u'<h1>%s</h1>' % bp.esc(h1)]
    if ru:
        body.append(bp.search_form(brand, mode='heater',
                                   ph=(u'Код %s, например %s' % (NAME_RU[brand], brand_example(brand))
                                       if brand else u'Код отопителя, например %s' % HEATER_EXAMPLE_RU)))
        cta = (u'<p class="cta">Знаете номер кода? <a href="%s">Введите его в поиск</a> — или вставьте '
               u'сразу весь список со сканера, покажем, какая поломка настоящая.</p>'
               % (u'/?mode=heater&amp;b=%s' % brand if brand else u'/?mode=heater'))
    else:
        body.append(bp.search_form(brand, mode='heater',
                                   ph=(u'Your %s code, e.g. %s' % (NAME_EN[brand], brand_example(brand))
                                       if brand else u'Heater code, e.g. %s' % HEATER_EXAMPLE_EN),
                                   action=u'/en/', btn=u'Search', label=u'Heater fault code'))
        cta = (u'<p class="cta">Know the code number? <a href="%s">Type it into the search</a> — or paste '
               u'the whole list from the scanner and we will show which fault is the real one.</p>'
               % (u'/en/?mode=heater&amp;b=%s' % brand if brand else u'/en/?mode=heater'))
    body.append(u'<p class="sub">%s</p>' % sub)
    body.extend(sections)
    body.append(cta)
    body.append(u'</div>\n' + bp.CF_SNIPPET + u'\n</body>\n</html>\n')
    return u''.join(body)


_EXAMPLES = {}


def brand_example(brand):
    return _EXAMPLES.get(brand, u'')


def breadcrumb_en(name, canon):
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/en/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'Heaters',
              'item': SITE + '/en/otopiteli/'},
             {'@type': 'ListItem', 'position': 3, 'name': name, 'item': canon}]
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}


def nav_en(here):
    return (u'<a href="/en/">Home</a><span class="sep">&rsaquo;</span>'
            u'<a href="/en/otopiteli/">Heaters</a><span class="sep">&rsaquo;</span>'
            u'<span>%s</span>' % bp.esc(here))


def _write(root, rel, html):
    full = os.path.join(root, rel.replace('/', os.sep))
    d = os.path.dirname(full)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(full, 'w', encoding='utf-8').write(html)


def _code_page(lang, b, code, entry, prev_c, next_c):
    ru = lang == 'ru'
    name = NAME_RU[b] if ru else NAME_EN[b]
    text = entry.get(lang) or entry.get('ru') or ''
    short = _short(text)
    prefix = (u'Ошибка %s %s' % (code, name)) if ru else (u'%s heater error %s' % (name, code))
    h1 = prefix
    title = make_title(prefix, short)
    desc = make_desc(lang, prefix, short)
    rel = ('otopiteli/%s.html' if ru else 'en/otopiteli/%s.html') % _slug(b, code)
    if ru:
        sub = (u'Код <b>%s</b> отопителя %s. Текст из заводской таблицы; ниже — что проверить '
               u'на месте и соседние коды.' % (esc_c(code), esc_c(name)))
        s_what, s_check, s_near, s_more = u'Что означает код', u'Что проверить', u'Соседние коды', u'Где ещё смотреть'
        near_lbl = (u'Предыдущий код', u'Следующий код')
        more = [(u'/marki/%s.html' % b, u'Все коды марки %s' % name),
                (u'/otopiteli/', u'Оглавление: все отопители'),
                (u'/?mode=heater&amp;b=%s&amp;q=%s' % (b, code),
                 u'Найти этот код в режиме отопителя')]
    else:
        sub = (u'Code <b>%s</b>, %s heater. Factory text below; then what to check and the '
               u'neighbouring codes.' % (esc_c(code), esc_c(name)))
        s_what, s_check, s_near, s_more = u'What the code means', u'What to check', u'Nearby codes', u'Where else to look'
        near_lbl = (u'Previous code', u'Next code')
        more = [(u'/en/marki/%s.html' % b, u'All %s codes' % name),
                (u'/en/otopiteli/', u'Index: all heaters'),
                (u'/en/?mode=heater&amp;b=%s&amp;q=%s' % (b, code),
                 u'Find this code in heater mode')]
    sections = topic_sections(lang, entry, text)
    # Соседи - только выпущенные (prev_c/next_c уже отфильтрованы в build()).
    # Строка как в kody/: номер в колонке span.mono, текст в span.nm.
    near = []
    if prev_c is not None:
        cp = (u'/otopiteli/%s.html' if ru else u'/en/otopiteli/%s.html') % _slug(b, prev_c)
        near.append(u'<li><a href="%s"><span class="mono">← %s</span><span class="nm">%s</span></a></li>'
                    % (cp, bp.esc(prev_c), bp.esc(_short(c_text(b, prev_c, lang)))))
    if next_c is not None:
        cn = (u'/otopiteli/%s.html' if ru else u'/en/otopiteli/%s.html') % _slug(b, next_c)
        near.append(u'<li><a href="%s"><span class="mono">%s</span><span class="nm">%s →</span></a></li>'
                    % (cn, bp.esc(next_c), bp.esc(_short(c_text(b, next_c, lang)))))
    if near:
        sections.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                        % (s_near, u''.join(near)))
    sections.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                    % (s_more, u''.join(u'<li><a href="%s"><span class="nm">%s</span></a></li>'
                                        % (h, bp.esc(t)) for h, t in more)))
    noindex = _unconfirmed(entry)
    html = render(lang, rel, title, desc, h1, sub, sections, here=h1, brand=b, noindex=noindex)
    return rel, html, noindex


# Тексты соседних кодов нужны из общего словаря текущей сборки.
_CUR = {}


def c_text(b, c, lang):
    entry = _CUR['codes'][b][c]
    return entry.get(lang) or entry.get('ru') or ''


def esc_c(t):
    return bp.esc(t)


def _index_page(lang, codes_by, is_live):
    ru = lang == 'ru'
    total = sum(len(v) for v in codes_by.values())
    if ru:
        title = u'Коды отопителей Eberspächer, Webasto, Планар | codetruck.ru'
        h1 = u'Коды отопителей'
        desc = (u'Расшифровка кодов автономных отопителей грузовика: Eberspächer, Webasto и Планар. '
                u'Все коды со ссылками на описание и проверки на месте.')
        sub = (u'Автономные отопители кабины: <b>%s</b> в трёх марках. Выберите марку ниже '
               u'или введите код на главной.' % bp.n_codes(total))
        lbl_more = u'Страница марки'
        h_tpl = u'%s — %s'
    else:
        title = u'Heater fault codes: Eberspächer, Webasto, Planar | codetruck.ru'
        h1 = u'Heater fault codes'
        desc = (u'Fault codes of truck cab heaters: Eberspächer, Webasto and Planar. All codes with '
                u'links to the description and checks on site.')
        sub = (u'Standalone cab heaters: <b>%d codes</b> across three makes. Pick a make below or type '
               u'a code on the homepage.' % total)
        lbl_more = u'Make page'
        h_tpl = u'%s — %d codes'
    sections = []
    for b in BRANDS:
        rows = codes_by.get(b, [])
        name = NAME_RU[b] if ru else NAME_EN[b]
        head = (h_tpl % (name, len(rows))) if not ru else (u'%s — %s' % (name, bp.n_codes(len(rows))))
        tr = []
        for code, entry in rows:
            text = bp.esc(_short(entry.get(lang) or entry.get('ru') or ''))
            if not is_live(b, code):
                # Код видно текстом, страницы пока нет - ссылки нет.
                tr.append(u'<tr><td class="fmi">%s</td><td>%s</td></tr>' % (bp.esc(code), text))
                continue
            cp = (u'/otopiteli/%s.html' if ru else u'/en/otopiteli/%s.html') % _slug(b, code)
            tr.append(u'<tr><td class="fmi"><a href="%s">%s</a></td><td>%s</td></tr>'
                      % (cp, bp.esc(code), text))
        mk = (u'/marki/%s.html' if ru else u'/en/marki/%s.html') % b
        sections.append(u'<section id="%s"><h2>%s</h2><p class="lead"><a href="%s">%s</a></p>'
                        u'<table>%s</table></section>'
                        % (b, bp.esc(head), mk, lbl_more, u''.join(tr)))
    rel = 'otopiteli/index.html' if ru else 'en/otopiteli/index.html'
    return rel, render(lang, rel, title, desc, h1, sub, sections, here=h1)


def _rel(lang, b, code):
    return ('otopiteli/%s.html' if lang == 'ru' else 'en/otopiteli/%s.html') % _slug(b, code)


def build(root=None, pcode=None, today=None):
    """Пишет страницы отопителей в root (по умолчанию корень сайта): только коды
    из партий с датой не позже today (по умолчанию - сегодня). Файлы невыпущенных
    кодов удаляет, если остались от прошлой сборки. Оглавления пишет всегда.
    Возвращает адреса для карт сайта (только выпущенные, без noindex),
    список записанных файлов, noindex-страницы и удалённые файлы."""
    root = root or bp.ROOT
    if pcode is None:
        pcode = bp.load_pcode()
    today = (today or date.today()).isoformat()
    codes_by = {}
    for b in BRANDS:
        src = pcode.get(b) or {}
        items = [(c, e) for c, e in src.items() if e.get('ru') or e.get('en')]
        items.sort(key=lambda kv: bp.code_sort_key(kv[0]))
        if items:
            codes_by[b] = items
    if not codes_by:
        return {'urls': [], 'written': [], 'noindex': [], 'removed': []}
    _CUR['codes'] = {b: dict(v) for b, v in codes_by.items()}
    for b, items in codes_by.items():
        _EXAMPLES[b] = items[0][0]

    # Партии: каждый ключ должен существовать в pcode.json.
    release = load_release()
    known = set('%s:%s' % (b, c) for b, items in codes_by.items() for c, _ in items)
    missing = sorted(k for k in release if k not in known)
    if missing:
        raise ValueError(u'в партиях есть коды, которых нет в pcode.json: %s' % u', '.join(missing))
    live = set(k for k, d in release.items() if d <= today)

    def is_live(b, code):
        return '%s:%s' % (b, code) in live

    urls, written, noindex, removed = [], [], [], []
    slugs = set()
    for lang in ('ru', 'en'):
        for b, items in codes_by.items():
            for i, (code, entry) in enumerate(items):
                slug = (lang, _slug(b, code))
                if slug in slugs:
                    raise ValueError(u'повтор адреса: %s %s' % slug)
                slugs.add(slug)
                if not is_live(b, code):
                    # Файла быть не должно: если остался от прошлой сборки - убираем.
                    stale = os.path.join(root, _rel(lang, b, code).replace('/', os.sep))
                    if os.path.isfile(stale):
                        os.remove(stale)
                        removed.append(_rel(lang, b, code))
                    continue
                prev_c = items[i - 1][0] if i > 0 and is_live(b, items[i - 1][0]) else None
                next_c = items[i + 1][0] if i + 1 < len(items) and is_live(b, items[i + 1][0]) else None
                rel, html, is_no = _code_page(lang, b, code, entry, prev_c, next_c)
                _write(root, rel, html)
                written.append(rel)
                if is_no:
                    noindex.append(rel)
                else:
                    urls.append('%s/%s' % (SITE, rel))
        rel, html = _index_page(lang, codes_by, is_live)
        _write(root, rel, html)
        written.append(rel)
        urls.append('%s/%s' % (SITE, rel[:-len('index.html')]))
    return {'urls': urls, 'written': written, 'noindex': noindex, 'removed': removed}
