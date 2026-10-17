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
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp                                    # noqa: E402

SITE = bp.SITE
BRANDS = bp.HEATER_BRANDS
NAME_RU = {'eberspacher': u'Eberspächer', 'webasto': u'Webasto', 'planar': u'Планар'}
NAME_EN = {'eberspacher': u'Eberspächer', 'webasto': u'Webasto', 'planar': u'Planar'}
UNCONFIRMED = u'не подтверждено'
ROBOTS_NOINDEX = u'<meta name="robots" content="noindex,follow">\n'

# Общие советы по типу неисправности. Подбираются по словам в русском тексте
# кода: по одному совету на тему, не больше четырёх, в порядке списка.
# Только безопасные общие проверки, без номеров деталей.
TOPICS = [
    (u'перегрев|перегрет',
     u'Проверьте, не забиты ли воздухозабор и выхлоп, и не загрязнён ли теплообменник.',
     u'Check that the air intake and exhaust are clear and the heat exchanger is clean.'),
    (u'пламен|пламя|срыв',
     u'Проверьте, загорается ли пламя при пуске: грязная камера сгорания и слабая подача топлива дают срыв пламени.',
     u'Check whether the flame lights at start-up: a dirty combustion chamber or weak fuel supply causes flame loss.'),
    (u'насос|топлив',
     u'Проверьте топливный насос: питание и разъём, подачу топлива по линии и не забит ли фильтр.',
     u'Check the fuel pump: its power and connector, fuel flow in the line, and whether the filter is clogged.'),
    (u'свеч|штифт|накаливан|зажиган',
     u'Проверьте свечу накаливания или штифт зажигания: состояние контактов и сопротивление по заводским данным.',
     u'Check the glow plug or ignition pin: contact condition and resistance per the manufacturer data.'),
    (u'вентилятор|нагнетател|воздух',
     u'Проверьте нагнетатель воздуха: свободно ли вращается крыльчатка, нет ли подсоса и засора воздуховодов.',
     u'Check the air blower: the impeller should turn freely, and check for air leaks and blocked ducts.'),
    (u'напряжени|питани|по току',
     u'Измерьте напряжение питания на разъёме отопителя во время работы: провал ниже нормы указывает на аккумулятор, клеммы или проводку.',
     u'Measure the supply voltage at the heater connector while it runs: a drop below normal points to the battery, terminals or wiring.'),
    (u'обрыв|замыкани',
     u'Проверьте жгут у разъёма: обрыв или замыкание чаще всего на изломах, у клемм и там, где провод перетёрт.',
     u'Check the harness at the connector: an open circuit or short is most often at bends, at terminals or where the wire is chafed.'),
    (u'датчик',
     u'Проверьте датчик: разъём, целостность провода и сопротивление по схеме марки.',
     u'Check the sensor: connector, wire continuity and resistance per the brand wiring diagram.'),
    (u'связ|пульт|шин|тревог',
     u'Проверьте пульт и линию связи: питание пульта, разъём и целостность провода связи.',
     u'Check the control panel and the communication line: panel power, connector and wire continuity.'),
    (u'блокировк|блок управления',
     u'При блокировке выключите отопитель, дайте ошибке сброситься и повторите пуск; если блокировка возвращается, ищите причину в блоке управления.',
     u'On a lockout, switch the heater off, let the fault clear and retry; if the lockout returns, look for the cause in the control unit.'),
]
# Запасные советы, если по тексту ни одна тема не подошла (нужно минимум два).
FALLBACK = [
    (u'Запишите код, время появления и условия: холодный пуск, работа на ходу или стоянка.',
     u'Note the code, when it appeared and the conditions: cold start, driving or idling.'),
    (u'Осмотрите разъёмы этого узла: окисление и слабые клеммы - частая причина.',
     u'Inspect the connectors of this part: corrosion and loose terminals are a common cause.'),
]
ZERO_NOTE = (u'Это не ошибка: строка означает, что неисправностей нет. Если отопитель не работает, '
             u'ищите в считывании код с ненулевым номером.',
             u'This is not a fault: the line means no faults are stored. If the heater does not work, '
             u'look for a code with a non-zero number in the readout.')

TITLE_LIM = 65
TITLE_SUFFIX = u' | codetruck.ru'


def _short(text):
    """Текст кода без скобок-пояснений: «Блокировка отопителя»."""
    return re.sub(r'\s*\([^)]*\)', u'', text).strip().rstrip(u'.')


def _lower_first(s):
    return s[:1].lower() + s[1:] if len(s) > 1 and s[1].islower() else s


def _slug(brand, code):
    return u'%s-%s' % (brand, code.lower())


def _unconfirmed(entry):
    return UNCONFIRMED in (entry.get('ru') or '')


def make_title(prefix, short, lang_sep=u' — '):
    """Заголовок не длиннее TITLE_LIM: короткое описание режем по слову."""
    room = TITLE_LIM - len(prefix) - len(TITLE_SUFFIX) - len(lang_sep)
    title = prefix + TITLE_SUFFIX
    if short and room >= 12:
        title = prefix + lang_sep + bp.cut60(_lower_first(short), room) + TITLE_SUFFIX
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


def advice(lang, ru_text):
    """Два-четыре совета по ключевым словам русского текста кода."""
    picked = [(ru, en) for pat, ru, en in TOPICS if re.search(pat, ru_text, re.I)][:4]
    for pair in FALLBACK:
        if len(picked) >= 2:
            break
        if pair not in picked:
            picked.append(pair)
    return [p[1] if lang == 'en' else p[0] for p in picked]


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
        body.append(bp.search_form(brand, ph=(u'Код %s, например %s' % (NAME_RU[brand], brand_example(brand))
                                              if brand else u'Ваш код, например 1078/3')))
        cta = (u'<p class="cta">Знаете номер кода? <a href="%s">Введите его в поиск</a> — или вставьте '
               u'сразу весь список со сканера, покажем, какая поломка настоящая.</p>'
               % (u'/?b=%s' % brand if brand else u'/'))
    else:
        body.append(bp.search_form(brand, ph=(u'Your %s code, e.g. %s' % (NAME_EN[brand], brand_example(brand))
                                              if brand else u'Your code, e.g. 1078/3'),
                                   action=u'/en/', btn=u'Search', label=u'Fault code'))
        cta = (u'<p class="cta">Know the code number? <a href="%s">Type it into the search</a> — or paste '
               u'the whole list from the scanner and we will show which fault is the real one.</p>'
               % (u'/en/?b=%s' % brand if brand else u'/en/'))
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
        sub = (u'Код <b>%s</b> отопителя %s. Текст из заводской таблицы; ниже - что проверить '
               u'на месте и соседние коды.' % (esc_c(code), esc_c(name)))
        s_what, s_check, s_near, s_more = u'Что означает код', u'Что проверить', u'Соседние коды', u'Где ещё смотреть'
        near_lbl = (u'Предыдущий код', u'Следующий код')
        more = [(u'/marki/%s.html' % b, u'Все коды марки %s' % name),
                (u'/otopiteli/', u'Оглавление: все отопители'),
                (u'/?mode=heater&amp;b=%s&amp;q=%s' % (b, code),
                 u'Найти этот код в режиме отопителя')]
        zero = ZERO_NOTE[0]
    else:
        sub = (u'Code <b>%s</b>, %s heater. Factory text below; then what to check and the '
               u'neighbouring codes.' % (esc_c(code), esc_c(name)))
        s_what, s_check, s_near, s_more = u'What the code means', u'What to check', u'Nearby codes', u'Where else to look'
        near_lbl = (u'Previous code', u'Next code')
        more = [(u'/en/marki/%s.html' % b, u'All %s codes' % name),
                (u'/en/otopiteli/', u'Index: all heaters'),
                (u'/en/?mode=heater&amp;b=%s&amp;q=%s' % (b, code),
                 u'Find this code in heater mode')]
        zero = ZERO_NOTE[1]
    sections = [u'<section><h2>%s</h2><p>%s</p></section>' % (s_what, bp.esc(text))]
    if text.startswith(u'Ошибок нет') or text.startswith(u'No faults'):
        checks = u'<p>%s</p>' % bp.esc(zero)
    else:
        items = advice(lang, entry.get('ru') or '')
        checks = u'<ul>%s</ul>' % u''.join(u'<li>%s</li>' % bp.esc(t) for t in items)
    sections.append(u'<section><h2>%s</h2>%s</section>' % (s_check, checks))
    near = []
    for lbl, c in ((near_lbl[0], prev_c), (near_lbl[1], next_c)):
        if c is None:
            continue
        cp = (u'/otopiteli/%s.html' if ru else u'/en/otopiteli/%s.html') % _slug(b, c)
        ctext = _short(c_text(b, c, lang))
        near.append(u'<li>%s: <a href="%s">%s %s</a> - %s</li>'
                    % (lbl, cp, bp.esc(c), bp.esc(name), bp.esc(ctext)))
    if near:
        sections.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                        % (s_near, u''.join(near)))
    sections.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                    % (s_more, u''.join(u'<li><a href="%s">%s</a></li>' % (h, bp.esc(t)) for h, t in more)))
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


def _index_page(lang, codes_by):
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
            cp = (u'/otopiteli/%s.html' if ru else u'/en/otopiteli/%s.html') % _slug(b, code)
            tr.append(u'<tr><td class="fmi"><a href="%s">%s</a></td><td>%s</td></tr>'
                      % (cp, bp.esc(code), bp.esc(_short(entry.get(lang) or entry.get('ru') or ''))))
        mk = (u'/marki/%s.html' if ru else u'/en/marki/%s.html') % b
        sections.append(u'<section id="%s"><h2>%s</h2><p class="lead"><a href="%s">%s</a></p>'
                        u'<table>%s</table></section>'
                        % (b, bp.esc(head), mk, lbl_more, u''.join(tr)))
    rel = 'otopiteli/index.html' if ru else 'en/otopiteli/index.html'
    return rel, render(lang, rel, title, desc, h1, sub, sections, here=h1)


def build(root=None, pcode=None):
    """Пишет все страницы отопителей в root (по умолчанию корень сайта).
    Возвращает адреса для карт сайта (без noindex) и список noindex-страниц."""
    root = root or bp.ROOT
    if pcode is None:
        pcode = bp.load_pcode()
    codes_by = {}
    for b in BRANDS:
        src = pcode.get(b) or {}
        items = [(c, e) for c, e in src.items() if e.get('ru') or e.get('en')]
        items.sort(key=lambda kv: bp.code_sort_key(kv[0]))
        if items:
            codes_by[b] = items
    if not codes_by:
        return {'urls': [], 'written': [], 'noindex': []}
    _CUR['codes'] = {b: dict(v) for b, v in codes_by.items()}
    for b, items in codes_by.items():
        _EXAMPLES[b] = items[0][0]

    urls, written, noindex = [], [], []
    slugs = set()
    for lang in ('ru', 'en'):
        for b, items in codes_by.items():
            for i, (code, entry) in enumerate(items):
                slug = (lang, _slug(b, code))
                if slug in slugs:
                    raise ValueError(u'повтор адреса: %s %s' % slug)
                slugs.add(slug)
                prev_c = items[i - 1][0] if i > 0 else None
                next_c = items[i + 1][0] if i + 1 < len(items) else None
                rel, html, is_no = _code_page(lang, b, code, entry, prev_c, next_c)
                _write(root, rel, html)
                written.append(rel)
                if is_no:
                    noindex.append(rel)
                else:
                    urls.append('%s/%s' % (SITE, rel))
        rel, html = _index_page(lang, codes_by)
        _write(root, rel, html)
        written.append(rel)
        urls.append('%s/%s' % (SITE, rel[:-len('index.html')]))
    return {'urls': urls, 'written': written, 'noindex': noindex}
