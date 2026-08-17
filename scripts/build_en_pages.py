# -*- coding: utf-8 -*-
"""
Английские страницы кодов: en/kody/spn-*.html и рубрика en/kody/.

Зачем: до этого английской у сайта была ровно одна страница - главная
(en/index.html), а все ссылки с неё вели на русские карточки кодов.
Для англоязычной выдачи справочника физически не существовало, хотя
J1939 - мировой стандарт и «SPN 3251 FMI 16» ищут прежде всего
по-английски.

Русские страницы и sitemap собирает scripts/build_pages.py - этот скрипт
вызывает его сам, передав список SPN, у которых английская страница
реально получается. Поэтому запускать нужно ЭТОТ скрипт; build_pages.py
отдельно - только когда английские страницы не нужны.

Тексты не сочиняются заново. Разбор неисправностей берётся из
assets/dtc.en.js, а вся обвязка страницы (названия систем, вердикт «можно
ли ехать», что проверить на месте, горизонт риска, значения FMI) - из тех
же объектов I18N / RISK_TX / RISK_H / FMI_I18N в assets/app.js, которыми
живёт сам инструмент. Иначе статическая страница начнёт расходиться с
интерфейсом, и человек, пришедший из поиска и нажавший «decode», получит
два разных ответа на один код.

Страница заводится не на каждый SPN: нужна либо хотя бы одна переведённая
заводская строка, либо английское имя узла из стандарта. Если нет ни того,
ни другого (сейчас это только Renault, чья таблица не переведена), страницы
нет. Подставлять на английскую страницу русский текст нельзя - hreflang
обещает английский, и такой «перевод» поисковик засчитает как ошибку языка,
а не как контент.

Запуск из корня репозитория:  python scripts/build_en_pages.py
"""
import base64, glob, io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp                                    # noqa: E402
from build_lang_pages import extract_js_object              # noqa: E402

ROOT = bp.ROOT
SITE = bp.SITE
OUT = os.path.join(ROOT, 'en', 'kody')

# Марки, чьё имя в базе записано кириллицей: на английской странице
# показываем латиницей, теми же подписями, что и в интерфейсе.
BRAND_LBL = {'kamaz': 'brandKamazLbl', 'yamz': 'brandYamzLbl', 'gaz': 'brandGazLbl',
             'maz': 'brandMazLbl', 'kraz': 'brandKrazLbl', 'ural': 'brandUralLbl',
             'planar': 'brandPlanarLbl', 'teplostar': 'brandTeplostarLbl'}

# Названия систем и совет «что проверить» - ключи того же I18N.
SYS_KEY = {'scr': 'sysScr', 'oil': 'sysOil', 'cool': 'sysCool', 'fuel': 'sysFuel',
           'air': 'sysAir', 'power': 'sysPower', 'can': 'sysCan', 'brake': 'sysBrake',
           'trans': 'sysTrans', 'prot': 'sysProt', 'other': 'sysOther'}
ACT_KEY = {'scr': 'actScr', 'oil': 'actOil', 'cool': 'actCool', 'fuel': 'actFuel',
           'air': 'actAir', 'power': 'actPower', 'can': 'actCan', 'brake': 'actBrake'}

# Единственное, чего в I18N нет: обвязка именно страницы, а не инструмента.
TX = {
    'navUp':      u'&larr; code lookup',
    'navSection': u'All fault codes',
    'fmiStd':     u'What FMI means in J1939',
    'fmiCommon':  u'Common FMI values',
    'canDrive':   u'Can I keep driving',
    'checkNow':   u'What to check on the spot',
    'nearby':     u'Nearby: %s',
    'cta':        u'Scanner threw several codes at once? '
                  u'<a href="/en/">Paste the whole list</a> — we will show which one is '
                  u'the root cause and which ones simply followed.',
    'ctaHub':     u'Know the code number? <a href="/en/">Type it into the search</a> — or '
                  u'paste the whole list from the scanner and we will show which fault '
                  u'is the real one.',
    'subStd':     u'J1939 code SPN %d. Below — how the fault is worded at the factory by %s, '
                  u'and what the second half of the code (FMI) means in the standard.',
    'subOwn':     u'SPN %d is a manufacturer number outside the standard J1939 table: '
                  u'different makes can put different things under it. Below — how it is '
                  u'worded by %s, and what the second half of the code (FMI) means.',
    'subNone':    u'J1939 code SPN %d. No factory wording for it in the reference — '
                  u'below is the standard meaning of FMI.',
    'titleStd':   u'SPN %d — %s',
    'titleOwn':   u'SPN %d — %s (%s)',
    'titleBare':  u'SPN %d — factory code %s',
    'descStd':    u'SPN %d (%s): decoded against the J1939 standard and factory tables. '
                  u'What the code means and whether you can keep driving.',
    'descOwn':    u'SPN %d (%s) on %s: what this factory code means, the FMI values '
                  u'and whether you can keep driving.',
    'descBare':   u'SPN %d on %s: how the factory words this code, what the FMI values '
                  u'mean and whether you can keep driving.',
    'descNone':   u'SPN %d: what the code means under the J1939 standard, the FMI values '
                  u'and whether you can keep driving.',
    'hubTitle':   u'All truck fault codes — SPN and FMI under J1939 | codetruck.ru',
    'hubH1':      u'All fault codes: SPN and FMI',
    'hubDesc':    u'Full list of decoded truck fault codes: %d SPN codes by system plus '
                  u'the standard FMI table. What a code means and whether you can drive.',
    'hubSub':     u'%d codes decoded from the factory tables of %d makes. Below — the full '
                  u'list by system and the standard FMI table: with it the code reads '
                  u'whole, not by halves.',
    'hubFmiLead': u'The SPN number says <i>what</i> is faulty, FMI says <i>what exactly</i> '
                  u'is wrong with it. The second half of the code is the same for every '
                  u'make — that is the J1939 standard.',
    'hubRange':   u'SPN %d — %d',
}


def load_en():
    raw = io.open(os.path.join(ROOT, 'assets', 'dtc.en.js'), encoding='utf-8').read()
    b64 = re.search(r"b64='([^']+)'", raw).group(1)
    return json.loads(base64.b64decode(b64).decode('utf-8'))


def per_spn_en(en_db):
    """SPN -> {марка: [(fmi, английский текст)]} только по переведённым строкам."""
    out = {}
    for b, table in en_db.get('brands', {}).items():
        for key, text in table.items():
            parts = key.split('.')
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                continue
            if not text:
                continue
            out.setdefault(int(parts[0]), {}).setdefault(b, []).append((int(parts[1]), text))
    return out


def build():
    ru_db = bp.load_db()
    en_db = load_en()
    i18n = extract_js_object('I18N')['en']
    risk_tx = extract_js_object('RISK_TX')['en']
    risk_h = extract_js_object('RISK_H')['en']
    risk_title = extract_js_object('RISK_TITLE')['en']
    risk_map = extract_js_object('RISK_MAP')
    fmi_en = extract_js_object('FMI_I18N')['en']

    per_en = per_spn_en(en_db)
    urgent_fmi = set(ru_db['urgentFmi'])

    def en_std(spn):
        s = str(spn)
        return en_db.get('spn', {}).get(s) or en_db.get('universal', {}).get(s) or u''

    # Кураторские коды (SPN 1569 «ограничение момента» и подобные) заводских
    # строк не имеют вовсе - ни на русском, ни на английском, - но страница
    # у них есть и на русском: стандартное имя, частые FMI, вердикт. Английской
    # версии без них не хватало бы ровно тех кодов, что вынесены на главную.
    en_set = set(per_en) | {int(k) for k in en_db.get('universal', {})}         | {int(k) for k in en_db.get('spn', {})}

    # Русская сборка знает, какие страницы вообще существуют, в какой они
    # системе и какой у них вердикт. Английская обязана повторить это
    # один в один, поэтому спрашивает, а не считает заново.
    info = bp.build(en_spns=en_set)
    written = [s for s in info['written'] if s in en_set]
    sys_of, stop_of, by_sys = info['sys'], info['stop'], info['by_sys']
    lvl_of = info['lvl']

    brand_names = ru_db['brandNames']

    def bname(b):
        key = BRAND_LBL.get(b)
        return (i18n.get(key) if key else None) or brand_names.get(b, b)

    def brand_list(spn, limit=0):
        names = sorted(bname(b) for b in per_en.get(spn, {}))
        if not names:
            return u''
        if limit and len(names) > limit:
            return u', '.join(names[:limit]) + u' and others'
        if len(names) == 1:
            return names[0]
        return u', '.join(names[:-1]) + u' and ' + names[-1]

    # Имя узла: сначала английский стандарт/кураторский список, затем -
    # вывод из английских же заводских строк тем же разбором, что и у
    # русских страниц (см. build_pages.derive_names).
    std_name = en_std

    derived = bp.derive_names(per_en, [s for s in written if not std_name(s)])

    def name_of(spn):
        return std_name(spn) or derived.get(spn) or u''

    def code_link(spn, href):
        nm = name_of(spn)
        return (u'<li><a href="%s"><span class="mono">SPN %d</span>%s</a></li>'
                % (href, spn, (u'<span class="nm">%s</span>' % bp.esc(nm)) if nm else u''))

    def nav():
        return (u'<a href="/en/">%s</a><span class="sep">&middot;</span>'
                u'<a href="/en/kody/">%s</a>' % (TX['navUp'], TX['navSection']))

    def alt_links(rel):
        ru, en = '%s/%s' % (SITE, rel), '%s/en/%s' % (SITE, rel)
        return (u'\n<link rel="alternate" hreflang="ru" href="%s">'
                u'\n<link rel="alternate" hreflang="en" href="%s">'
                u'\n<link rel="alternate" hreflang="x-default" href="%s">' % (ru, en, ru))

    def breadcrumb(name, canon):
        return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'codetruck.ru', 'item': SITE + '/en/'},
            {'@type': 'ListItem', 'position': 2, 'name': TX['navSection'],
             'item': SITE + '/en/kody/'},
            {'@type': 'ListItem', 'position': 3, 'name': name, 'item': canon},
        ]}

    # Скан показывает «SPN 100 FMI 1», «100/1» или «100.1» - ищут ровно то,
    # что видно на экране. В стандартной таблице печатаем все три написания
    # и вешаем якорь на сочетание (см. тот же приём в build_pages.py).
    def fmi_table(rows, spn=None):
        out = ['<table>']
        for f, text in rows:
            cls = ' class="hit"' if f in urgent_fmi else ''
            if spn is None:
                cell = 'FMI %s' % f
            else:
                cell = ('<a id="fmi-%s"></a>SPN %d FMI %s'
                        '<span class="alt">%d/%s &middot; %d.%s</span>'
                        % (f, spn, f, spn, f, spn, f))
            out.append('<tr%s><td class="fmi">%s</td><td>%s</td></tr>'
                       % (cls, cell, bp.rich(text)))
        out.append('</table>')
        return ''.join(out)

    # Горизонт риска собирается из RISK_MAP/RISK_TX ровно так же, как его
    # собирает инструмент: «any» - основной вариант, «elec» - оговорка про
    # электрический код. Уровень (now/short/base/watch) даёт и подпись
    # запаса времени, и цвет плашки.
    def risk_section(sys_key):
        rule = risk_map.get(sys_key)
        if not rule or 'any' not in rule:
            return u''
        key, lvl = rule['any']
        happens, ends = risk_tx[key]
        note = u''
        if 'elec' in rule:
            note = u'<p class="rkn">%s</p>' % bp.esc(u' '.join(risk_tx[rule['elec'][0]]))
        return (u'<section><h2>%s</h2>'
                u'<div class="risk t-%s"><span class="rkb">Time you have: %s</span>'
                u'<p>%s</p><p>%s</p>%s</div></section>'
                % (bp.esc(risk_title), 'now' if lvl == 'now' else 'warn',
                   bp.esc(risk_h[lvl]), bp.esc(happens), bp.esc(ends), note))

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for f in glob.glob(os.path.join(OUT, 'spn-*.html')):
        os.remove(f)

    for spn in written:
        makes = per_en.get(spn, {})
        # Какие FMI вообще встречаются у этого кода - нужно и в FAQ (вопрос
        # про конкретное сочетание), и ниже в таблице, поэтому считаем сразу.
        seen = sorted({f for rows in makes.values() for f, _ in rows})
        sys_key = sys_of.get(spn, 'other')
        name = name_of(spn)
        brands_short, brands_all = brand_list(spn, 3), brand_list(spn)

        if stop_of.get(spn):
            verdict = u'<b>%s.</b> %s' % (i18n['vStop'], i18n['vStopSub'])
        else:
            verdict = u'<b>%s.</b> %s' % (i18n['vWarn'], i18n['vWarnSub'])

        if std_name(spn):
            page_name = TX['titleStd'] % (spn, name)
            desc = TX['descStd'] % (spn, name)
        elif name:
            page_name = TX['titleOwn'] % (spn, name, brands_short)
            desc = TX['descOwn'] % (spn, name, brands_short)
        elif brands_short:
            page_name = TX['titleBare'] % (spn, brands_short)
            desc = TX['descBare'] % (spn, brands_short)
        else:
            page_name = u'SPN %d' % spn
            desc = TX['descNone'] % spn
        title = page_name + u' | codetruck.ru'
        rel = 'kody/spn-%d.html' % spn
        canon = '%s/en/%s' % (SITE, rel)

        faq = [{'@type': 'Question',
                'name': (u'Can I keep driving with code SPN %d (%s)?' % (spn, name) if name
                         else u'Can I keep driving with code SPN %d?' % spn),
                'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'</?b>', '', verdict)}}]
        rule = risk_map.get(sys_key)
        if rule and 'any' in rule:
            happens, ends = risk_tx[rule['any'][0]]
            faq.append({'@type': 'Question',
                        'name': u'What happens if I keep driving with SPN %d?' % spn,
                        'acceptedAnswer': {'@type': 'Answer', 'text': happens + u' ' + ends}})

        for f in sorted(seen, key=lambda x: (x not in urgent_fmi, x))[:2]:
            if str(f) not in fmi_en:
                continue
            faq.append({'@type': 'Question',
                        'name': u'What does SPN %d FMI %d (%d/%d) mean?' % (spn, f, spn, f),
                        'acceptedAnswer': {'@type': 'Answer',
                                           'text': u'%s: %s.' % (name or u'SPN %d' % spn,
                                                                 fmi_en[str(f)])}})

        ld = (bp.ld_script({'@context': 'https://schema.org', '@type': 'TechArticle',
                            'headline': title, 'description': desc, 'url': canon,
                            'inLanguage': 'en'})
              + bp.ld_script(breadcrumb(page_name, canon))
              + bp.ld_script({'@context': 'https://schema.org', '@type': 'FAQPage',
                              'mainEntity': faq}))

        body = [bp.HEAD.format(title=bp.esc(title), desc=bp.esc(desc), canon=canon,
                               ogtitle=bp.esc(page_name), mid=bp.METRIKA_ID, ld=ld,
                               nav=nav(), lang='en', locale='en_US', alt=alt_links(rel))]
        body.append(u'<h1>%s</h1>' % bp.esc(page_name))
        lvl = lvl_of.get(spn, 'plan')
        tier = 'now' if lvl == 'now' else ('warn' if lvl in ('short', 'base') else 'calm')
        body.append(u'<p class="vline t-%s"><b>%s</b><span class="hz">%s</span></p>'
                    % (tier, i18n['vStop'] if stop_of.get(spn) else i18n['vWarn'],
                       bp.esc(risk_h.get(lvl, u''))))
        if not makes:
            body.append(u'<p class="sub">%s</p>' % (TX['subNone'] % spn))
        else:
            body.append(u'<p class="sub">%s</p>'
                        % ((TX['subStd'] if std_name(spn) else TX['subOwn'])
                           % (spn, bp.esc(brands_all))))

        ordered = sorted(makes, key=lambda x: bname(x))
        if len(ordered) >= 3:
            body.append(u'<p class="jump">%s</p>' % u''.join(
                u'<a href="#mk-%s">%s</a>' % (b, bp.esc(bname(b))) for b in ordered))
        for b in ordered:
            body.append(u'<section><h2 class="mk" id="mk-%s">%s</h2>%s</section>'
                        % (b, bp.esc(bname(b)),
                           fmi_table(sorted(makes[b], key=lambda r: r[0]))))

        if seen:
            std_rows = [(f, fmi_en[str(f)]) for f in seen if str(f) in fmi_en]
            if std_rows:
                body.append(u'<section><h2>%s</h2>%s</section>'
                            % (TX['fmiStd'], fmi_table(std_rows, spn)))
        else:
            common = [(f, fmi_en[str(f)]) for f in (0, 1, 2, 3, 4, 5) if str(f) in fmi_en]
            body.append(u'<section><h2>%s</h2>%s</section>'
                        % (TX['fmiCommon'], fmi_table(common, spn)))

        body.append(u'<section><h2>%s</h2><p>%s</p></section>' % (TX['canDrive'], verdict))
        body.append(risk_section(sys_key))
        act = i18n.get(ACT_KEY.get(sys_key, ''))
        if act:
            body.append(u'<section><h2>%s</h2><p>%s</p></section>'
                        % (TX['checkNow'], bp.esc(act)))

        neigh = [s for s in bp.neighbors_of(spn, [x for x in by_sys.get(sys_key, [])
                                                  if x in en_set])]
        if neigh:
            body.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                        % (TX['nearby'] % bp.esc(i18n.get(SYS_KEY.get(sys_key, 'sysOther'), '')),
                           ''.join(code_link(s, 'spn-%d.html' % s) for s in neigh)))

        body.append(u'<p class="cta">%s</p>' % TX['cta'])
        body.append(u'</div>\n</body>\n</html>\n')
        io.open(os.path.join(OUT, 'spn-%d.html' % spn), 'w',
                encoding='utf-8').write(''.join(body))

    # --- рубрика en/kody/ ------------------------------------------
    secs = [u'<section><h2>%s</h2><p class="lead">%s</p>%s</section>'
            % (TX['fmiStd'], TX['hubFmiLead'],
               fmi_table(sorted(((int(f), t) for f, t in fmi_en.items()))))]
    for key in ['oil', 'cool', 'fuel', 'air', 'scr', 'power', 'can',
                'brake', 'trans', 'prot', 'other']:
        bucket = [s for s in by_sys.get(key, []) if s in en_set]
        if not bucket:
            continue
        head = u'%s — %d' % (i18n.get(SYS_KEY[key], key), len(bucket))
        if len(bucket) <= 200:
            secs.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                        % (bp.esc(head), ''.join(code_link(s, 'spn-%d.html' % s)
                                                 for s in bucket)))
            continue
        secs.append(u'<section><h2>%s</h2></section>' % bp.esc(head))
        for i in range(0, len(bucket), 120):
            chunk = bucket[i:i + 120]
            secs.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                        % (TX['hubRange'] % (chunk[0], chunk[-1]),
                           ''.join(code_link(s, 'spn-%d.html' % s) for s in chunk)))

    canon = SITE + '/en/kody/'
    ld = (bp.ld_script({'@context': 'https://schema.org', '@type': 'TechArticle',
                        'headline': TX['hubTitle'], 'description': TX['hubDesc'] % len(written),
                        'url': canon, 'inLanguage': 'en'})
          + bp.ld_script({'@context': 'https://schema.org', '@type': 'BreadcrumbList',
                          'itemListElement': [
                              {'@type': 'ListItem', 'position': 1, 'name': 'codetruck.ru',
                               'item': SITE + '/en/'},
                              {'@type': 'ListItem', 'position': 2, 'name': TX['hubH1'],
                               'item': canon}]}))
    n_brands = len({b for spn in written for b in per_en.get(spn, {})})
    body = [bp.HEAD.format(title=bp.esc(TX['hubTitle']),
                           desc=bp.esc(TX['hubDesc'] % len(written)), canon=canon,
                           ogtitle=bp.esc(TX['hubH1']), mid=bp.METRIKA_ID, ld=ld,
                           nav=u'<a href="/en/">%s</a>' % TX['navUp'],
                           lang='en', locale='en_US', alt=alt_links('kody/'))]
    body.append(u'<h1>%s</h1>' % bp.esc(TX['hubH1']))
    body.append(u'<p class="sub">%s</p>' % (TX['hubSub'] % (len(written), n_brands)))
    body.extend(secs)
    body.append(u'<p class="cta">%s</p>' % TX['ctaHub'])
    body.append(u'</div>\n</body>\n</html>\n')
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(''.join(body))

    # Карта сайта пересобирается ПОСЛЕ записи английских страниц: только
    # тогда их можно захешировать и понять, изменились ли они на самом деле.
    bp.write_sitemap()

    print('английских страниц: %d' % len(written))
    print('без английского:    %d' % (len(info['written']) - len(written)))
    return written


if __name__ == '__main__':
    build()
