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

# Сверенные заводские сведения (модель, источник, заводская рекомендация) -
# scripts/heater_sources.json, собирается scripts/heater_apply.py. Нет файла -
# страницы строятся только по pcode.json, как раньше.
SOURCES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heater_sources.json')
_SRC = {}


def texts():
    if not _TEXTS:
        _TEXTS.update(json.loads(io.open(TEXTS_FILE, encoding='utf-8').read()))
    return _TEXTS


def sources():
    if not _SRC:
        if os.path.isfile(SOURCES_FILE):
            _SRC.update(json.loads(io.open(SOURCES_FILE, encoding='utf-8').read()))
        _SRC.setdefault('_loaded', True)
    return _SRC


def is_f(code):
    return bool(re.match(r'^F\d\d$', code))


def rec_of(b, code):
    """Сверенная запись кода. Webasto F-код: {'rows': [по моделям]}; иначе запись как в файле."""
    s = sources()
    if b == 'webasto':
        w = s.get('webasto') or {}
        if is_f(code):
            rows = (w.get('f') or {}).get(code)
            return {'rows': rows} if rows else None
        return (w.get('pc') or {}).get(code)
    return (s.get(b) or {}).get(code)


def topic_of(ru_text, key=None):
    """Тема из heater_texts.json: сначала явная привязка assign (марка:код), иначе
    первая тема, чей шаблон подошёл к русскому тексту кода."""
    tx = texts()
    if key and key in (tx.get('assign') or {}):
        want = tx['assign'][key]
        for t in tx['topics']:
            if t['id'] == want:
                return t
        raise ValueError(u'нет темы %s для кода %s' % (want, key))
    for t in tx['topics']:
        if re.search(t['pattern'], ru_text, re.I):
            return t
    raise ValueError(u'нет темы для кода: %s' % ru_text)


def _li(items):
    return u''.join(u'<li>%s</li>' % bp.esc(x) for x in items)


LEVEL = {
    'ru': {'service': u'Это работа для сервиса.',
           'driver+service': u'Часть проверок под силу водителю, остальное — работа сервиса.'},
    'en': {'service': u'This is a job for a service.',
           'driver+service': u'Some checks the driver can do, the rest is a job for a service.'},
}


def src_section(lang, srcs):
    """Блок «Источник»: документ (со ссылкой на PDF) и страница."""
    if not srcs:
        return u''
    ru = lang == 'ru'
    li = []
    seen = set()
    for s in srcs:
        key = (s.get('doc'), s.get('page'))
        if key in seen:
            continue
        seen.add(key)
        label = bp.esc(s.get('doc') or u'')
        if s.get('url'):
            label = u'<a href="%s" rel="nofollow noopener">%s</a>' % (bp.esc(s['url']), label)
        pg = s.get('page')
        if pg and re.match(r'^\d', pg):
            tail = (u', стр. %s' if ru else u', p. %s') % bp.esc(pg)
        else:
            tail = (u', %s' % bp.esc(pg)) if pg else u''
        li.append(u'<li>%s%s</li>' % (label, tail))
    return u'<section><h2>%s</h2><ul>%s</ul></section>' % (
        u'Источник' if ru else u'Source', u''.join(li))


def topic_sections(lang, entry, text, key=None, lead=u'', remedy=u''):
    """Разделы страницы кода: что значит, (заводская рекомендация), почему, что проверить,
    сервис, езда, опасность. lead - готовый html после основного текста (модель, Hydronic),
    remedy - готовый html раздела с заводской рекомендацией (стоит выше шаблонных советов)."""
    h = SECTION_HEAD[lang]
    topic = topic_of(entry.get('ru') or '', key)
    t = topic[lang]
    cm = texts()['common'][lang]
    zero = topic['id'] == 'zero'
    out = [u'<section><h2>%s</h2><p>%s</p>%s<p>%s</p></section>'
           % (h['what'], bp.esc(text), lead, bp.esc(t['meaning']))]
    if remedy:
        out.append(remedy)
    out += [
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
    return out


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


# Тексты соседних кодов нужны из общего словаря текущей сборки.
_CUR = {}


def c_text(b, c, lang):
    entry = _CUR['codes'][b][c]
    return entry.get(lang) or entry.get('ru') or ''


def esc_c(t):
    return bp.esc(t)


def _is_live_now(b, code):
    f = _CUR.get('live')
    return bool(f and f(b, code))


def _page_url(lang, b, code):
    return (u'/otopiteli/%s.html' if lang == 'ru' else u'/en/otopiteli/%s.html') % _slug(b, code)


def short_of(b, code, lang):
    """Короткое название кода (для title, соседей и оглавления): без скобок-пояснений."""
    rec = rec_of(b, code)
    if rec and b == 'eberspacher':
        return _short(rec['title'] if lang == 'ru' else rec['en'])
    if rec and b == 'webasto' and 'rows' in rec:
        key = 'title' if lang == 'ru' else 'en'
        uniq = []
        for r in rec['rows']:
            if r[key] not in uniq:
                uniq.append(r[key])
        # Заголовок не должен заканчиваться на «<10.5 V»: при знаках сравнения берём часть до двоеточия.
        uniq = [x.split(u': ')[0] if (u'<' in x or u'>' in x) else x for x in uniq]
        return u'; '.join(_short(x) for x in uniq[:1])
    sh = _short(c_text(b, code, lang))
    if b == 'planar':
        # «Датчик ... на входе - только для AIR-8D»: для заголовка берём часть до тире.
        sh = sh.split(u' - ')[0].strip()
        if lang == 'en':
            # «Fault 04 (same as 06): temperature sensor ...» - в заголовок идёт часть после двоеточия.
            m = re.match(r'^[^:]{0,32}\d[^:]{0,20}: (.+)$', sh)
            if m:
                sh = m.group(1)[:1].upper() + m.group(1)[1:]
    return sh


def _f_by_model(fmap):
    """{'F02': ['Air Top 2000 ST', ...]} по словарю модель -> F-код."""
    g = {}
    for model, fv in fmap.items():
        if fv:
            g.setdefault(fv, []).append(model)
    return g


def _f_link(lang, fv):
    if _is_live_now('webasto', fv):
        return u'<a href="%s">%s</a>' % (_page_url(lang, 'webasto', fv), fv)
    return fv


def webasto_pc_plaque(lang, rec):
    """Плашка первой строкой на странице ПК-кода Webasto."""
    g = _f_by_model(rec['f'])
    ru = lang == 'ru'
    if not g:
        body = (u'На таймере для него отдельного F-кода нет: код виден только в программе.' if ru else
                u'There is no separate F-code for it on the timer: the code is visible only in the program.')
    elif len(g) == 1:
        fv, ms = list(g.items())[0]
        if len(ms) == len(rec['f']):
            body = (u'На таймере водитель увидит %s.' if ru else u'On the timer the driver will see %s.') % _f_link(lang, fv)
        else:
            body = ((u'На таймере водитель увидит %s (по модели: %s).' if ru else
                     u'On the timer the driver will see %s (by model: %s).')
                    % (_f_link(lang, fv), bp.esc(u', '.join(ms))))
    else:
        parts = u'; '.join(u'%s — %s' % (_f_link(lang, fv), bp.esc(u', '.join(ms)))
                           for fv, ms in sorted(g.items()))
        body = ((u'На таймере водитель увидит F-код, который зависит от модели: %s.' if ru else
                 u'On the timer the driver will see an F-code that depends on the model: %s.') % parts)
    lead = (u'Это служебный код программы Webasto Thermo Test (ПК).' if ru else
            u'This is a service code of the Webasto Thermo Test program (PC).')
    return u'<div class="risk"><p><b>%s</b> %s</p></div>' % (lead, body)


DRIVER_EN = [
    u'Combination timer (1531): a number F00-F15 appears on the display while the fault remains.',
    u'Heater with only an ON indicator: five seconds of fast flashing, then a number of long flashes equal to the F-code '
    u'(F04 is four long flashes).',
    u'MultiControl / SmartControl: codes F01-F15 on the display (F16-F19 show as "- -"); over W-Bus the display may show '
    u'hexadecimal codes Hxx instead.',
]
NO_F_RU = (u'Пульты Telestart и ThermoCall номер ошибки не показывают — смотрите таймер или пульт в кабине '
           u'(по руководствам Telestart T91, T100 HTM и ThermoCall, которые удалось проверить).')
NO_F_EN = (u'Telestart and ThermoCall remotes do not show the error number: look at the timer or the control in the cab '
           u'(according to the Telestart T91, T100 HTM and ThermoCall manuals that could be checked).')


def driver_section(lang):
    ru = lang == 'ru'
    disp = (sources().get('webasto') or {}).get('display') or []
    if ru:
        li = [u'<li><b>%s.</b> %s</li>' % (bp.esc(d['control']), bp.esc(d['how']))
              for d in disp if not d.get('no_f')]
        if not li:
            return u''
        li.append(u'<li>%s</li>' % bp.esc(NO_F_RU))
        return u'<section><h2>Как увидит водитель</h2><ul>%s</ul></section>' % u''.join(li)
    li = [u'<li>%s</li>' % bp.esc(x) for x in DRIVER_EN]
    li.append(u'<li>%s</li>' % bp.esc(NO_F_EN))
    return u'<section><h2>What the driver sees</h2><ul>%s</ul></section>' % u''.join(li)


def _hydronic_note(lang, rec):
    note = rec.get('hydronic_note') or u''
    if rec['kind'] == 'hydronic':
        if lang == 'ru':
            return u'Этот код есть в таблице Hydronic; в таблице Airtronic D2/D4 его нет.'
        return u'This code is in the Hydronic table; it is not in the Airtronic D2/D4 table.'
    if not note:
        return u''
    if lang == 'ru':
        if note.startswith(u'Тот же смысл.') and len(note) <= 14:
            return u'В отопителях Hydronic этот код значит то же самое.'
        if note.startswith(u'В Hydronic нет'):
            return u'В таблицах Hydronic такого кода нет.'
        if note.startswith(u'В Hydronic '):
            return u'В отопителях Hydronic ' + note[len(u'В Hydronic '):]
        return u'В отопителях Hydronic: ' + note
    if note.startswith(u'Тот же смысл.') and len(note) <= 14:
        return u'In Hydronic heaters this code means the same.'
    if note.startswith(u'В Hydronic нет'):
        return u'The Hydronic tables have no such code.'
    return u'Hydronic heaters may use this number differently; see the Russian version of the page.'


def _remedy_section(lang, text, level=u''):
    if lang != 'ru' or not text:
        return u''
    lv = LEVEL['ru'].get(level, u'')
    return (u'<section><h2>Что делать по заводской инструкции</h2><p>%s</p>%s</section>'
            % (bp.esc(text), (u'<p>%s</p>' % bp.esc(lv)) if lv else u''))


PLANAR_EN = [(u'ремонт', u'repair code'), (u'ПУ-5', u'PU-5'), (u'миганий', u'blinks'),
             (u'мигания', u'blinks'), (u'мигание', u'blink')]


def planar_plaque(lang, code, rec):
    """Подпись системы: код таблицы ремонта или число миганий пульта ПУ-5, и соответствие."""
    ru = lang == 'ru'
    sysm = rec['system']
    eq = rec['equivalent']
    if u'совпадают' in sysm:
        cap = (u'Номер совпадает в обеих системах: это и код таблицы ремонта, и число миганий пульта ПУ-5.' if ru else
               u'The number is the same in both systems: it is both a repair-table code and a PU-5 remote blink count.')
    elif sysm.startswith(u'ПУ-5'):
        cap = (u'Это число миганий пульта ПУ-5, а не код таблицы ремонта.' if ru else
               u'This is the PU-5 remote blink count, not a repair-table code.')
    else:
        cap = (u'Это код таблицы ремонта, а не число миганий пульта ПУ-5.' if ru else
               u'This is a repair-table code, not the PU-5 remote blink count.')
    if ru:
        body = u'<p><b>%s</b></p><p>Соответствие в другой системе: %s.</p>' % (bp.esc(cap), bp.esc(eq))
        if sysm.startswith(u'таблица ремонта') and u'. ' in sysm:
            body += u'<p>%s</p>' % bp.esc(sysm.split(u'. ', 1)[1])
    else:
        e2 = re.sub(r'\s*\([^)]*\)', u'', eq)
        for k, v in PLANAR_EN:
            e2 = e2.replace(k, v)
        body = u'<p><b>%s</b></p><p>Match in the other system: %s.</p>' % (bp.esc(cap), bp.esc(e2))
    return u'<div class="risk">%s</div>' % body


def _code_page(lang, b, code, entry, prev_c, next_c):
    ru = lang == 'ru'
    name = NAME_RU[b] if ru else NAME_EN[b]
    text = entry.get(lang) or entry.get('ru') or ''
    rec = rec_of(b, code)
    short = short_of(b, code, lang)
    fcode = b == 'webasto' and is_f(code)
    hyd = bool(rec and b == 'eberspacher' and rec['kind'] == 'hydronic')
    if ru:
        prefix = u'Ошибка %s %s' % (code, name) + (u' Hydronic' if hyd else u'')
    else:
        prefix = u'%s%s heater error %s' % (name, u' Hydronic' if hyd else u'', code)
    h1 = prefix
    if fcode and rec:
        pcs = []
        for r in rec['rows']:
            for x in r['pc']:
                if x not in pcs:
                    pcs.append(x)
        if len(pcs) <= 4:
            h1 = prefix + ((u' (ПК-коды %s)' if ru else u' (PC codes %s)') % u', '.join(sorted(pcs)))
    title = make_title(prefix, short)
    full = text if b == 'planar' else short
    desc = make_desc(lang, prefix, full)
    rel = ('otopiteli/%s.html' if ru else 'en/otopiteli/%s.html') % _slug(b, code)
    model_txt = u''
    if rec and b == 'eberspacher':
        model_txt = rec['model']
    if ru:
        if model_txt:
            sub = (u'Код <b>%s</b> отопителя %s, модель: %s. Текст по заводскому руководству; ниже — '
                   u'что проверить на месте и соседние коды.' % (esc_c(code), esc_c(name), esc_c(model_txt)))
        else:
            sub = (u'Код <b>%s</b> отопителя %s. Текст из заводской таблицы; ниже — что проверить '
                   u'на месте и соседние коды.' % (esc_c(code), esc_c(name)))
        s_near, s_more = u'Соседние коды', u'Где ещё смотреть'
        more = [(u'/marki/%s.html' % b, u'Все коды марки %s' % name),
                (u'/otopiteli/', u'Оглавление: все отопители'),
                (u'/?mode=heater&amp;b=%s&amp;q=%s' % (b, code),
                 u'Найти этот код в режиме отопителя')]
    else:
        if model_txt:
            sub = (u'Code <b>%s</b>, %s heater, model: %s. Factory text below; then what to check and the '
                   u'neighbouring codes.' % (esc_c(code), esc_c(name), esc_c(model_txt)))
        else:
            sub = (u'Code <b>%s</b>, %s heater. Factory text below; then what to check and the '
                   u'neighbouring codes.' % (esc_c(code), esc_c(name)))
        s_near, s_more = u'Nearby codes', u'Where else to look'
        more = [(u'/en/marki/%s.html' % b, u'All %s codes' % name),
                (u'/en/otopiteli/', u'Index: all heaters'),
                (u'/en/?mode=heater&amp;b=%s&amp;q=%s' % (b, code),
                 u'Find this code in heater mode')]
    key = '%s:%s' % (b, code)
    pre, post = [], []        # блоки до разделов шаблона и после них
    lead, remedy, srcs = u'', u'', None
    what_text = text
    if rec and b == 'eberspacher':
        what_text = rec['ru'] if ru else rec['en']
        lead = (u'<p><b>%s:</b> %s.</p>' % (u'Модель' if ru else u'Model', bp.esc(rec['model'])))
        hn = _hydronic_note(lang, rec)
        if hn:
            lead += u'<p>%s</p>' % bp.esc(hn)
        remedy = _remedy_section(lang, rec.get('remedy'), rec.get('level'))
        srcs = rec['sources']
    elif rec and b == 'webasto' and not fcode:
        pre.append(webasto_pc_plaque(lang, rec))
        what_text = rec['ru'] if ru else rec['en']
        srcs = rec['sources']
    elif rec and b == 'webasto':
        rows = rec['rows']
        h = SECTION_HEAD[lang]
        th = ((u'Модель', u'Что значит', u'ПК-коды') if ru else (u'Model', u'Meaning', u'PC codes'))
        tr = []
        srcs = []
        for r in rows:
            pcl = u', '.join((u'<a href="%s">%s</a>' % (_page_url(lang, 'webasto', x), x))
                             if _is_live_now('webasto', x) else x for x in r['pc'])
            tr.append(u'<tr><td>%s</td><td><b>%s.</b> %s</td><td class="fmi">%s</td></tr>'
                      % (bp.esc(r['model']), bp.esc(r['title'] if ru else r['en']),
                         bp.esc(r['ru']) if ru else u'', pcl))
            srcs += r['sources']
        what_text = ((u'Код %s показывает таймер или пульт Webasto. Смысл зависит от модели отопителя, поэтому ниже — '
                      u'таблица по моделям.' % code) if ru else
                     (u'Code %s is shown by the Webasto timer or control. The meaning depends on the heater model, '
                      u'so the table below is by model.' % code))
        lead = (u'<table><tr><th>%s</th><th>%s</th><th>%s</th></tr>%s</table>'
                % (th[0], th[1], th[2], u''.join(tr)))
        rem = {}
        for r in rows:
            if r['remedy']:
                rem.setdefault(r['remedy'], []).append(r['model'])
        if ru and rem:
            remedy = (u'<section><h2>Что делать по заводской инструкции</h2><ul>%s</ul></section>'
                      % u''.join(u'<li><b>%s.</b> %s</li>' % (bp.esc(u', '.join(ms)), bp.esc(t))
                                 for t, ms in rem.items()))
        post.append(driver_section(lang))
    elif rec and b == 'planar':
        pre.append(planar_plaque(lang, code, rec))
        what_text = rec['ru'] if ru else rec['en']
        remedy = _remedy_section(lang, rec.get('remedy'))
        srcs = rec['sources']
    sections = list(pre)
    sections += topic_sections(lang, entry, what_text, key, lead, remedy)
    sections += [p for p in post if p]
    if srcs:
        sections.append(src_section(lang, srcs))
    # Соседи - только выпущенные (prev_c/next_c уже отфильтрованы в build()).
    # Строка как в kody/: номер в колонке span.mono, текст в span.nm.
    near = []
    if prev_c is not None:
        cp = _page_url(lang, b, prev_c)
        near.append(u'<li><a href="%s"><span class="mono">← %s</span><span class="nm">%s</span></a></li>'
                    % (cp, bp.esc(prev_c), bp.esc(short_of(b, prev_c, lang))))
    if next_c is not None:
        cn = _page_url(lang, b, next_c)
        near.append(u'<li><a href="%s"><span class="mono">%s</span><span class="nm">%s →</span></a></li>'
                    % (cn, bp.esc(next_c), bp.esc(short_of(b, next_c, lang))))
    if near:
        sections.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                        % (s_near, u''.join(near)))
    sections.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                    % (s_more, u''.join(u'<li><a href="%s"><span class="nm">%s</span></a></li>'
                                        % (h, bp.esc(t)) for h, t in more)))
    noindex = _unconfirmed(entry)
    html = render(lang, rel, title, desc, h1, sub, sections, here=h1, brand=b, noindex=noindex)
    return rel, html, noindex


def _row(lang, b, code, is_live, text, first=None):
    """Строка оглавления: код (ссылка, если страница выпущена) и текст."""
    cell = bp.esc(code)
    if is_live(b, code):
        cell = u'<a href="%s">%s</a>' % (_page_url(lang, b, code), cell)
    return cell


def _webasto_tables(lang, rows, is_live):
    """Две таблицы Webasto: по F-коду таймера и по ПК-коду программы."""
    ru = lang == 'ru'
    w = sources().get('webasto') or {}
    pcs = [(c, e) for c, e in rows if not is_f(c)]
    fs = [(c, e) for c, e in rows if is_f(c)]
    out = []
    # 1) F-код на таймере -> ПК-коды
    th = (u'<tr><th>F-код на таймере</th><th>Что значит</th><th>ПК-коды</th></tr>' if ru else
          u'<tr><th>F-code on the timer</th><th>Meaning</th><th>PC codes</th></tr>')
    tr = []
    for code, entry in fs:
        rec = rec_of('webasto', code)
        pl = []
        for r in (rec['rows'] if rec else []):
            for x in r['pc']:
                if x not in pl:
                    pl.append(x)
        pcl = u', '.join(u'<a href="%s">%s</a>' % (_page_url(lang, 'webasto', x), x)
                         if is_live('webasto', x) else x for x in sorted(pl))
        tr.append(u'<tr><td class="fmi">%s</td><td>%s</td><td>%s</td></tr>'
                  % (_row(lang, 'webasto', code, is_live, None), bp.esc(short_of('webasto', code, lang)), pcl))
    if tr:
        out.append(u'<table>%s%s</table>' % (th, u''.join(tr)))
    # 2) ПК-код -> F-код на таймере
    th = (u'<tr><th>ПК-код</th><th>F-код на таймере</th><th>Что значит</th></tr>' if ru else
          u'<tr><th>PC code</th><th>F-code on the timer</th><th>Meaning</th></tr>')
    tr = []
    for code, entry in pcs:
        rec = rec_of('webasto', code)
        g = _f_by_model(rec['f']) if rec else {}
        if not g:
            fl = u'—'
        elif len(g) == 1:
            fl = list(g)[0]
            fl = u'<a href="%s">%s</a>' % (_page_url(lang, 'webasto', fl), fl) if is_live('webasto', fl) else fl
        else:
            fl = u', '.join((u'<a href="%s">%s</a>' % (_page_url(lang, 'webasto', fv), fv))
                            if is_live('webasto', fv) else fv for fv in sorted(g))
            fl += u' ' + (u'(по модели)' if ru else u'(by model)')
        tr.append(u'<tr><td class="fmi">%s</td><td>%s</td><td>%s</td></tr>'
                  % (_row(lang, 'webasto', code, is_live, None), fl, bp.esc(short_of('webasto', code, lang))))
    if tr:
        out.append(u'<table>%s%s</table>' % (th, u''.join(tr)))
    return u''.join(out)


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
        mk = (u'/marki/%s.html' if ru else u'/en/marki/%s.html') % b
        if b == 'webasto' and sources().get('webasto'):
            note = (u'У Webasto две системы кодов. На таймере и пульте водитель видит F-код, в программе Webasto Thermo '
                    u'Test — ПК-код; один F-код объединяет несколько ПК-кодов.' if ru else
                    u'Webasto has two code systems. The driver sees an F-code on the timer or control; the Webasto '
                    u'Thermo Test program shows a PC code. One F-code covers several PC codes.')
            sections.append(u'<section id="%s"><h2>%s</h2><p class="lead"><a href="%s">%s</a></p><p class="lead">%s</p>'
                            u'%s</section>' % (b, bp.esc(head), mk, lbl_more, bp.esc(note),
                                               _webasto_tables(lang, rows, is_live)))
            continue
        tr = []
        for code, entry in rows:
            text = bp.esc(short_of(b, code, lang))
            if not is_live(b, code):
                # Код видно текстом, страницы пока нет - ссылки нет.
                tr.append(u'<tr><td class="fmi">%s</td><td>%s</td></tr>' % (bp.esc(code), text))
                continue
            cp = _page_url(lang, b, code)
            tr.append(u'<tr><td class="fmi"><a href="%s">%s</a></td><td>%s</td></tr>'
                      % (cp, bp.esc(code), text))
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
    _CUR['live'] = None
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

    _CUR['live'] = is_live

    def same_group(b, c1, c2):
        # Webasto: F-коды и ПК-коды - разные ряды, соседями не считаются.
        return b != 'webasto' or is_f(c1) == is_f(c2)

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
                prev_c = (items[i - 1][0] if i > 0 and is_live(b, items[i - 1][0])
                          and same_group(b, code, items[i - 1][0]) else None)
                next_c = (items[i + 1][0] if i + 1 < len(items) and is_live(b, items[i + 1][0])
                          and same_group(b, code, items[i + 1][0]) else None)
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
    # Страницы кодов, которых больше нет в таблицах (убраны как выдуманные), - удаляем:
    # адрес честно отвечает 404, заглушек нет. Папка небольшая, обходим только её.
    keep = set(written)
    for pref in ('otopiteli', 'en/otopiteli'):
        d = os.path.join(root, pref.replace('/', os.sep))
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            rel = '%s/%s' % (pref, fn)
            if (fn.endswith('.html') and fn.split('-')[0] in BRANDS and rel not in keep
                    and os.path.isfile(os.path.join(d, fn)) and rel not in removed):
                os.remove(os.path.join(d, fn))
                removed.append(rel)
    return {'urls': urls, 'written': written, 'noindex': noindex, 'removed': removed}
