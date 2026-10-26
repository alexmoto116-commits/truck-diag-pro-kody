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

# Блоки КАМАЗ (см. BLOCK_LABEL в build_pages.py): английские подписи.
BLOCK_LABEL_EN = {
    'kamaz': u'KAMAZ engine (J1939)',
    'kamaz5490': u'KAMAZ-5490 (Mercedes, K-line)',
    'cumminsisb': u'Cummins ISB 6.7 engine',
    'kamazebs': u'EBS3 brakes (WABCO)',
    'kamazecas': u'ECAS air suspension (KAMAZ-5490)',
    'zfintarder': u'ZF Intarder retarder',
    'zfastronic': u'ZF AS-Tronic gearbox',
}
BLOCK_SHORT_EN = {
    'kamaz5490': u'KAMAZ-5490',
    'kamazebs': u'KAMAZ EBS3',
    'kamazecas': u'KAMAZ ECAS',
    'zfintarder': u'ZF Intarder',
}

# Названия систем и совет «что проверить» - ключи того же I18N.
SYS_KEY = {'scr': 'sysScr', 'oil': 'sysOil', 'cool': 'sysCool', 'fuel': 'sysFuel',
           'air': 'sysAir', 'power': 'sysPower', 'can': 'sysCan', 'brake': 'sysBrake',
           'trans': 'sysTrans', 'prot': 'sysProt', 'other': 'sysOther'}
ACT_KEY = {'scr': 'actScr', 'oil': 'actOil', 'cool': 'actCool', 'fuel': 'actFuel',
           'air': 'actAir', 'power': 'actPower', 'can': 'actCan', 'brake': 'actBrake'}

# Единственное, чего в I18N нет: обвязка именно страницы, а не инструмента.
# Английская пара к OWN_NUMBERING из build_pages.py - держать в согласии.
OWN_NUMBERING_EN = {
    'ford': u'Ford Trucks/Ecotorq writes fault numbers in its own format: '
            u'the code in the table below is a Ford code: before the dot is '
            u'the fault number in digits (leading zeros are not on every '
            u'code), after the dot is the fault type in digits and letters '
            u'A–F, for example 6.1F. It is not a J1939 SPN. It matches the standard only '
            u'where the signal itself is standard, and usually matches the '
            u'title of this page by digit alone.',
    'zfastronic': u'ZF AS-Tronic uses its own fault numbering: the number in '
                  u'the table below is an internal ZF code, not a J1939 SPN. '
                  u'It matches the title of this page by digit only and means '
                  u'something different.',
}

TX = {
    'navUp':      u'&larr; code lookup',
    'navSection': u'Codes',
    'fmiStd':     u'What FMI means in J1939',
    'fmiCommon':  u'Common FMI values',
    'canDrive':   u'Can I keep driving',
    'checkNow':   u'What to check on the spot',
    'nearby':     u'Nearby: %s',
    'casStart':   u'Where to start',
    'casStartP':  u'This code is often not the fault itself but a knock-on. '
                  u'If any of these is in the same readout, start with it:',
    'casFollow':  u'Which codes follow',
    'casPhys':    u'If the value really did go out of range, rather than a sensor '
                  u'circuit being broken, these normally light up after it:',
    'casAny':     u'These normally light up after this code:',
    'casNote':    u'They are not fixed separately — they go out together with this '
                  u'one. The list is deliberately short: only the links the '
                  u'reference is sure about.',
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
    # раздел «свой разбор» (own_checks_en.py): заголовки, как у русского в build_pages.py
    'ownH':       u'How to check it yourself',
    'ownNorm':    u'What it should read',
    'ownSteps':   u'Check order',
    'ownCauses':  u'Common causes — from most to least frequent',
}


# Английский свой разбор: данные из own_checks_en.py (тот же SPN и те же поля,
# что у русского own_checks.py). Вёрстка повторяет own_section() из build_pages.py.
from own_checks_en import CHECKS as OWN_EN                  # noqa: E402


def own_section_en(spn):
    c = OWN_EN.get(spn)
    if not c:
        return u''
    out = [u'<style>%s</style><section class="diy"><h2>%s</h2>' % (bp.DIY_CSS, TX['ownH']),
           u'<p>%s</p>' % bp.esc(c['узел'])]
    if c.get('нормы'):
        out.append(u'<h3>%s</h3><table class="norm">%s</table>' % (TX['ownNorm'], u''.join(
            u'<tr><td>%s</td><td><b>%s</b></td></tr>' % (bp.esc(a), bp.esc(b)) for a, b in c['нормы'])))
    # Different meaning by make (see own_checks_en_6): steps are listed per make.
    for brand, node, steps in c.get('по_маркам', []):
        li = []
        for s in steps:
            m = bp.FMI_PREFIX.match(s)
            if m:
                li.append(u'<li><b>%s%s:</b> %s</li>' % (bp.esc(m.group(1)), bp.esc(m.group(2) or u''),
                                                         bp.esc(s[m.end():])))
            else:
                li.append(u'<li>%s</li>' % bp.esc(s))
        out.append(u'<h3>%s</h3><p>%s</p><ol>%s</ol>' % (bp.esc(brand), bp.esc(node), u''.join(li)))
    if c.get('шаги'):
        li = []
        for s in c['шаги']:
            m = bp.FMI_PREFIX.match(s)
            if m:
                li.append(u'<li><b>%s%s:</b> %s</li>' % (bp.esc(m.group(1)), bp.esc(m.group(2) or u''),
                                                         bp.esc(s[m.end():])))
            else:
                li.append(u'<li>%s</li>' % bp.esc(s))
        out.append(u'<h3>%s</h3><ol>%s</ol>' % (TX['ownSteps'], u''.join(li)))
    if c.get('причины'):
        out.append(u'<h3>%s</h3><ol>%s</ol>' % (TX['ownCauses'], u''.join(
            u'<li>%s</li>' % bp.esc(p) for p in c['причины'])))
    out.append(u'</section>')
    return u''.join(out)


def code_desc_en(spn, name, sysname, names, urgent, how):
    """Описание английской страницы кода (до 155 знаков). Смысл тот же, что у
    русского bp.code_desc_ru: номер и название, система, срочность, марки для
    FMI и, если есть, раздел «how to check it yourself»."""
    head = (u'SPN %d — %s' % (spn, name)) if name else (u'SPN %d' % spn)
    sysc = (u': %s system' % sysname) if sysname else u''
    urg = u'Do not drive.' if urgent else u'Safe to drive to a service.'
    tail = u', how to check it yourself' if how else u''
    variants = []
    for n in (3, 2, 1):
        if len(names) >= n:
            pick = names[:n]
            joined = (u', '.join(pick[:-1]) + u' and ' + pick[-1]) if n > 1 else pick[0]
            variants.append(u'FMI decoded for %s%s.' % (joined, tail))
    variants.append(u'FMI decoded against the J1939 standard%s.' % tail)
    for v in variants:
        d = u'%s%s. %s %s' % (head, sysc, urg, v)
        if len(d) <= 155:
            return d
    return bp.cut_words(u'%s%s. %s %s' % (head, sysc, urg, variants[-1]))


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
    risk_flag = extract_js_object('RISK_FLAG')['en']
    risk_map = extract_js_object('RISK_MAP')
    fmi_en = extract_js_object('FMI_I18N')['en']

    per_en = per_spn_en(en_db)
    urgent_fmi = set(ru_db['urgentFmi'])
    urgent_spn = set(ru_db['urgentSpn'])
    own_fmi = bp.own_fmi_blocks(ru_db)

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
    # закрытые от индекса (их ровно столько же, сколько у русской версии)
    closed_en = set(info.get('noindex_en', ()))
    closed_ru = set(info.get('noindex', ()))
    # Ссылки на соседние коды ведут только на английские страницы, которые реально
    # записаны в этой сборке и открыты. en_set - это список КАНДИДАТОВ (есть перевод),
    # а не список записанных страниц: код из en_set, которого нет в written, ссылкой
    # давать нельзя (так и появлялись битые ссылки на spn-975, spn-2005, spn-3719).
    open_en = set(written) - closed_en
    # Соседние, похожие и рубричные коды en-страниц берём из открытых en-страниц,
    # а не из русского списка открытых (по нему на en-страницах могли бы оказаться
    # ссылки на закрытые en-адреса). Порядок тот же, что у русской сборки: по номеру.
    by_sys_en = {}
    for s in sorted((en_set & set(sys_of)) - closed_en):
        by_sys_en.setdefault(sys_of[s], []).append(s)

    brand_names = ru_db['brandNames']

    # Марки, чьё имя в базе записано кириллицей, на английских страницах
    # берём из I18N (КамАЗ, ЯМЗ, ...), а если ключа там нет - из того же
    # BRAND_OVERRIDE в app.js, которым инструмент подписывает марку на
    # любом нерусском языке. Иначе английская страница получила бы
    # русское имя марки.
    brand_en = extract_js_object('BRAND_OVERRIDE')

    def bname(b):
        if b in BLOCK_SHORT_EN:
            return BLOCK_SHORT_EN[b]
        key = BRAND_LBL.get(b)
        return ((i18n.get(key) if key else None) or brand_en.get(b)
                or brand_names.get(b, b))

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

    # Английская пара к causal_section() из build_pages.py: та же таблица
    # CAUSAL из app.js, но ссылки только на коды, у которых есть /en/-версия.
    def causal_section(spn):
        as_root, as_cons = bp.causal_rules(spn)
        out = []
        causes = sorted(({s for r in as_cons for s in r['root']} & open_en) - {spn})
        if causes:
            out.append(u'<section><h2>%s</h2><p>%s</p><ul class="near">%s</ul></section>'
                       % (TX['casStart'], TX['casStartP'],
                          ''.join(code_link(s, 'spn-%d.html' % s) for s in causes)))
        follow = sorted(({s for r in as_root for s in r['cons']} & open_en) - {spn})
        if follow:
            out.append(u'<section><h2>%s</h2><p>%s</p><ul class="near">%s</ul>'
                       u'<p>%s</p></section>'
                       % (TX['casFollow'],
                          TX['casPhys'] if any(r.get('phys') for r in as_root) else TX['casAny'],
                          ''.join(code_link(s, 'spn-%d.html' % s) for s in follow),
                          TX['casNote']))
        return ''.join(out)

    def nav(here=None):
        # Видимые крошки «Home › Codes › SPN N», как в JSON-LD
        items = [u'<a href="/en/">Home</a>', u'<a href="/en/kody/">%s</a>' % TX['navSection']]
        if here:
            items.append(u'<span>%s</span>' % bp.esc(here))
        return u'<span class="sep">&rsaquo;</span>'.join(items)

    def alt_links(rel, both_open):
        # hreflang только когда открыты обе версии (как alt_pair в build_pages.py)
        if not both_open:
            return u''
        ru, en = '%s/%s' % (SITE, rel), '%s/en/%s' % (SITE, rel)
        return (u'\n<link rel="alternate" hreflang="ru" href="%s">'
                u'\n<link rel="alternate" hreflang="en" href="%s">'
                u'\n<link rel="alternate" hreflang="x-default" href="%s">' % (ru, en, ru))

    def breadcrumb(name, canon):
        return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/en/'},
            {'@type': 'ListItem', 'position': 2, 'name': TX['navSection'],
             'item': SITE + '/en/kody/'},
            {'@type': 'ListItem', 'position': 3, 'name': name, 'item': canon},
        ]}

    # Скан показывает «SPN 100 FMI 1», «100/1» или «100.1» - ищут ровно то,
    # что видно на экране. В стандартной таблице печатаем все три написания
    # и вешаем якорь на сочетание (см. тот же приём в build_pages.py).
    def fmi_table(rows, spn=None, uf=None):
        out = ['<table>']
        for f, text in rows:
            cls = ' class="hit"' if f in (uf if uf is not None else urgent_fmi) else ''
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

    # Горизонт риска считаем не своей копией правил, а той же bp.page_risk(),
    # что и русская сборка: ключ текста и уровень от языка не зависят, поэтому
    # английская страница обязана говорить ровно то же, что русская.
    #
    # Раньше здесь стояло «нет правила у системы - нет блока», и блок теряли
    # четыре страницы из пяти: правил в RISK_MAP десяток, а систем на сайте
    # больше. У русской версии на этот случай есть общий текст (gen/genUrgent/
    # elecGen), английский перевод для него в app.js лежал неиспользованным -
    # из-за чего английские карточки выходили заметно тоньше русских.
    def risk_section(sys_key, fmis, urgent_spn_hit, uf=None):
        uf = urgent_fmi if uf is None else uf
        key, lvl, _ = bp.page_risk(sys_key, fmis, uf, urgent_spn_hit)
        if not key or key not in risk_tx:
            return u''
        happens, ends = risk_tx[key][0], risk_tx[key][1]
        note = u''
        rule = risk_map.get(sys_key)
        # Оговорку про электрический код ставим, только если такие FMI на
        # странице действительно есть: раньше она печаталась у всей системы
        # без разбора и попадала на страницы, где электрики нет вовсе.
        if (rule and rule.get('elec') and key != rule['elec'][0]
                and any(f in bp.fmi_elec() for f in (fmis or []))):
            e = risk_tx[rule['elec'][0]]
            note = u'<p class="rkn">%s %s</p>' % (bp.esc(e[0]), bp.esc(e[1]))
        # Метка производителя перевешивает наш спокойный вывод - говорим
        # о расхождении вслух, как и русская версия.
        if (urgent_spn_hit or any(f in uf for f in (fmis or []))) and lvl != 'now':
            note += u'<p class="rkn">%s</p>' % bp.esc(risk_flag)
        tier = bp.tier_of(lvl)
        return (u'<section><h2>%s</h2>'
                u'<div class="risk t-%s"><span class="rkb">Time you have: %s</span>'
                u'<p>%s</p><p>%s</p>%s</div></section>'
                % (bp.esc(risk_title), tier,
                   bp.esc(risk_h[lvl]), bp.esc(happens), bp.esc(ends), note))

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for f in glob.glob(os.path.join(OUT, 'spn-*.html')):
        os.remove(f)

    for spn in written:
        makes = per_en.get(spn, {})
        # как у русской: ZF/Ford со своей нумерацией не смешиваем с обычными
        # марками - есть обычные, их блоки не печатаем
        own_here_en = {}
        if any(b not in OWN_NUMBERING_EN for b in makes):
            own_here_en = {b: r for b, r in makes.items() if b in OWN_NUMBERING_EN}
            makes = {b: r for b, r in makes.items() if b not in OWN_NUMBERING_EN}
        # Как в русской сборке: на странице с блоком КАМАЗ строка ZF выводится текстом.
        shown = dict(makes)
        if 'zfastronic' in own_here_en and any(b in bp.KAMAZ_GROUP for b in makes):
            shown['zfastronic'] = own_here_en['zfastronic']
        # Какие FMI вообще встречаются у этого кода - нужно и в FAQ (вопрос
        # про конкретное сочетание), и ниже в таблице, поэтому считаем сразу.
        seen = sorted({f for rows in makes.values() for f, _ in rows})
        seen_std = sorted({f for m, rows in makes.items() if m not in own_fmi for f, _ in rows})
        uf_here = bp.urgent_fmi_for(spn, urgent_fmi, makes)
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
        # Описание открытой страницы строим из её данных (см. code_desc_en);
        # у закрытых от индекса остаётся прежний общий текст.
        if spn not in info.get('noindex_en', ()):
            ordered_b = sorted(makes, key=lambda b: (bp.ЧАСТЫЕ_МАРКИ.index(b)
                                                     if b in bp.ЧАСТЫЕ_МАРКИ else 99, bname(b)))
            desc = code_desc_en(spn, name, (i18n.get(SYS_KEY.get(sys_key, 'sysOther'))
                                            if sys_key != 'other' else None),
                                [bname(b) for b in ordered_b],
                                spn in urgent_spn or any(f in uf_here for f in seen),
                                spn in OWN_EN or bool(i18n.get(ACT_KEY.get(sys_key, ''))))
        title = bp.fit_title(page_name)  # без суффикса сайта, не длиннее 65, без многоточия
        rel = 'kody/spn-%d.html' % spn
        canon = '%s/en/%s' % (SITE, rel)

        faq = [{'@type': 'Question',
                'name': (u'Can I keep driving with code SPN %d (%s)?' % (spn, name) if name
                         else u'Can I keep driving with code SPN %d?' % spn),
                'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'</?b>', '', verdict)}}]
        # Вопрос в FAQ и блок на странице должны отвечать одинаково, поэтому
        # ключ текста здесь берётся тем же способом, что и в risk_section().
        rkey, _, _ = bp.page_risk(sys_key, seen, uf_here, spn in urgent_spn)
        if rkey and rkey in risk_tx:
            happens, ends = risk_tx[rkey][0], risk_tx[rkey][1]
            faq.append({'@type': 'Question',
                        'name': u'What happens if I keep driving with SPN %d?' % spn,
                        'acceptedAnswer': {'@type': 'Answer', 'text': happens + u' ' + ends}})

        for f in sorted(seen_std, key=lambda x: (x not in uf_here, x))[:2]:
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
                               nav=nav(u'SPN %d' % spn), lang='en', locale='en_US', alt=alt_links(rel, spn not in closed_ru and spn not in closed_en))]
        if spn in info.get('noindex_en', ()):      # закрыты по своему адресу en/kody/
            body[0] = body[0].replace(u'<meta charset="utf-8">',
                                      u'<meta charset="utf-8">\n<meta name="robots" content="noindex, follow">', 1)
        body.append(u'<h1>%s</h1>' % bp.esc(page_name))
        body.append(bp.search_form(ph=u'Another code, e.g. %d/3' % spn, action=u'/en/', btn=u'Search',
                                   label=u'Fault code'))
        lvl = lvl_of.get(spn, 'plan')
        tier = bp.tier_of(lvl)
        body.append(u'<p class="vline t-%s"><b>%s</b><span class="hz">%s</span></p>'
                    % (tier, i18n['vStop'] if stop_of.get(spn) else i18n['vWarn'],
                       bp.esc(risk_h.get(lvl, u''))))
        if not makes:
            body.append(u'<p class="sub">%s</p>' % (TX['subNone'] % spn))
        else:
            body.append(u'<p class="sub">%s</p>'
                        % ((TX['subStd'] if std_name(spn) else TX['subOwn'])
                           % (spn, bp.esc(brands_all))))

        # свой разбор - в том же месте, что и на русской странице (до таблиц марок)
        body.append(bp.extra_html('code-en:%d' % spn, 'head'))
        own = own_section_en(spn)
        if own:
            body.append(own)

        ordered = sorted(shown, key=lambda x: bname(x))
        if len(ordered) >= 3:
            body.append(u'<p class="jump">%s</p>' % u''.join(
                u'<a href="#mk-%s">%s</a>' % (b, bp.esc(bname(b))) for b in ordered))
        for b in ordered:
            # См. OWN_NUMBERING в build_pages.py: у ZF номер свой, не SPN.
            note = OWN_NUMBERING_EN.get(b)
            if b in own_fmi:
                note = u"FMI is per the block maker's own table, not the J1939 table below."
            head = BLOCK_LABEL_EN.get(b) or bname(b)
            body.append(u'<section><h2 class="mk" id="mk-%s">%s</h2>%s%s</section>'
                        % (b, bp.esc(head),
                           (u'<p class="sub">%s</p>' % bp.esc(note)) if note else u'',
                           fmi_table(sorted(shown[b], key=lambda r: r[0]), None, bp.urgent_fmi_for(spn, urgent_fmi, {b: shown[b]}))))

        if seen_std:
            std_rows = [(f, fmi_en[str(f)]) for f in seen_std if str(f) in fmi_en]
            if std_rows:
                body.append(u'<section><h2>%s</h2>%s</section>'
                            % (TX['fmiStd'], fmi_table(std_rows, spn, bp.urgent_fmi_for(spn, urgent_fmi))))
        elif not makes:
            common = [(f, fmi_en[str(f)]) for f in (0, 1, 2, 3, 4, 5) if str(f) in fmi_en]
            body.append(u'<section><h2>%s</h2>%s</section>'
                        % (TX['fmiCommon'], fmi_table(common, spn, bp.urgent_fmi_for(spn, urgent_fmi))))

        body.append(u'<section><h2>%s</h2><p>%s</p></section>' % (TX['canDrive'], verdict))
        body.append(risk_section(sys_key, seen, spn in urgent_spn, uf_here))
        act = i18n.get(ACT_KEY.get(sys_key, ''))
        if act:
            body.append(u'<section><h2>%s</h2><p>%s</p></section>'
                        % (TX['checkNow'], bp.esc(act)))

        body.append(causal_section(spn))

        neigh = [s for s in bp.neighbors_of(spn, by_sys_en.get(sys_key, []))]
        if neigh:
            body.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                        % (TX['nearby'] % bp.esc(i18n.get(SYS_KEY.get(sys_key, 'sysOther'), '')),
                           ''.join(code_link(s, 'spn-%d.html' % s) for s in neigh)))

        # Related codes: 5–8 открытых кодов той же системы, сначала с разделом
        # «how to check it yourself»; ссылки из «Nearby» не повторяем.
        similar = bp.similar_codes(spn, by_sys_en.get(sys_key, []),
                                   set(neigh), set(OWN_EN))
        if similar:
            body.append(u'<section><h2>Related codes</h2><ul class="near">%s</ul></section>'
                        % ''.join(code_link(s, 'spn-%d.html' % s) for s in similar))

        body.append(bp.extra_html('code-en:%d' % spn, 'tail'))
        body.append(u'<p class="cta">%s</p>' % TX['cta'])
        body.append(u'</div>\n' + bp.CF_SNIPPET + u'\n</body>\n</html>\n')
        io.open(os.path.join(OUT, 'spn-%d.html' % spn), 'w',
                encoding='utf-8').write(''.join(body))

    # --- рубрика en/kody/ ------------------------------------------
    secs = [u'<section><h2>%s</h2><p class="lead">%s</p>%s</section>'
            % (TX['fmiStd'], TX['hubFmiLead'],
               fmi_table(sorted(((int(f), t) for f, t in fmi_en.items())), None, bp.urgent_fmi_for(None, urgent_fmi)))]
    for key in ['oil', 'cool', 'fuel', 'air', 'scr', 'power', 'can',
                'brake', 'trans', 'prot', 'other']:
        bucket = by_sys_en.get(key, [])
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
                              {'@type': 'ListItem', 'position': 1, 'name': 'Home',
                               'item': SITE + '/en/'},
                              {'@type': 'ListItem', 'position': 2, 'name': TX['hubH1'],
                               'item': canon}]}))
    n_brands = len({b for spn in written for b in per_en.get(spn, {})} - bp.BLOCK_ONLY)
    body = [bp.HEAD.format(title=bp.esc(TX['hubTitle']),
                           desc=bp.esc(TX['hubDesc'] % len(written)), canon=canon,
                           ogtitle=bp.esc(TX['hubH1']), mid=bp.METRIKA_ID, ld=ld,
                           nav=u'<a href="/en/">Home</a><span class="sep">&rsaquo;</span><span>%s</span>' % bp.esc(TX['hubH1']),
                           lang='en', locale='en_US', alt=alt_links('kody/', True))]
    body.append(u'<h1>%s</h1>' % bp.esc(TX['hubH1']))
    body.append(bp.search_form(None, ph=u'Your code, e.g. 1078/3', action=u'/en/', btn=u'Search', label=u'Fault code'))
    body.append(u'<p class="sub">%s</p>' % (TX['hubSub'] % (len(written), n_brands)))
    body.extend(secs)
    body.append(u'<p class="cta">%s</p>' % TX['ctaHub'])
    body.append(u'</div>\n' + bp.CF_SNIPPET + u'\n</body>\n</html>\n')
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(''.join(body))

    # Карта сайта пересобирается ПОСЛЕ записи английских страниц: только
    # тогда их можно захешировать и понять, изменились ли они на самом деле.
    bp.write_sitemap()

    print('английских страниц: %d' % len(written))
    print('без английского:    %d' % (len(info['written']) - len(written)))
    return written


if __name__ == '__main__':
    build()
