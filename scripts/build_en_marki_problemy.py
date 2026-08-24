# -*- coding: utf-8 -*-
"""
Английские версии рубрик en/marki/*.html и en/problemy/*.html.

До этого скрипта у /marki/ и /problemy/ не было английской версии вообще -
языковые главные (включая /en/) вели на русские страницы этих разделов.
Данные для перевода к этому моменту уже готовы целиком: свободные таблицы
(brands.*) переведены на 100% ещё 08-17, дилерские (pcode.*) - 08-18 (эта же
сессия, партии 7-11 по Scania закрыли остаток). Поэтому это не задача
перевода данных, а задача сборки - обвязка, которой раньше не было.

Запускать ПОСЛЕ scripts/build_en_pages.py (нужны его en/kody/*.html и общий
sitemap-lastmod.json): python scripts/build_en_marki_problemy.py

Что делает:
  1. Строит en/marki/<brand>.html для каждой марки, у которой есть хоть один
     переведённый код - три варианта разметки те же, что и на русской
     странице (SPN/FMI по стандарту, MID-структура у Mack/Detroit Diesel,
     дилерская витрина-выборка у Scania/Caterpillar/...).
  2. Строит en/marki/index.html и en/problemy/index.html.
  3. Строит en/problemy/<slug>.html - 28 симптомных страниц. Тексты
     (заголовок/H1/вступление) переведены вручную (SYMPTOMS_EN ниже),
     список кодов и система риска - те же самые SPN.SYS_KEY.SPNS, что и на
     русской странице, импортированы напрямую из build_pages.SYMPTOMS, а
     не продублированы: расхождение списков кодов между языками было бы
     багом, а не мелочью.
  4. Дописывает hreflang в уже собранные русские marki/*.html и
     problemy/*.html (постобработкой - вставляет <link> сразу после
     canonical, см. bp.HEAD: там для этого зарезервировано место {alt}).
  5. Добавляет новые адреса в sitemap-en.xml (через bp.write_sitemap с
     объединённым списком URL, а не только своими - иначе потерялись бы
     все адреса, которые в тот же файл писали build_pages/build_en_pages).
"""
import glob, io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp                                    # noqa: E402
import build_en_pages as be                                 # noqa: E402
from build_lang_pages import extract_js_object               # noqa: E402

ROOT = bp.ROOT
SITE = bp.SITE

# Названия систем и совет "что проверить" - те же ключи I18N, что уже
# использует build_en_pages.py для страниц кодов; здесь та же обвязка.
SYS_KEY = be.SYS_KEY
ACT_KEY = be.ACT_KEY
BRAND_LBL = be.BRAND_LBL

MID_MODULE_NAMES_EN = {
    'mack':          {'128': u'Engine (EECU)', '142': u'Chassis/dash (VECU)',
                       '143': u'Engine, secondary module'},
    'detroitdiesel': {'128': u'Engine (DDEC)'},
}

SECTIONS_EN = {
    'marki':    (u'All makes', 'en/marki/'),
    'problemy': (u'Faults by symptom', 'en/problemy/'),
    'kody':     (u'All fault codes', 'en/kody/'),
}

MK = {
    'stopHead':  u'Codes that mean stop now',
    'howHead':   u'How to read a code',
    'howBody':   u'A code has two halves. <b>SPN</b> is what is actually at fault — '
                 u'the sensor, component, or parameter. <b>FMI</b> is what is wrong with '
                 u'it — value out of range, open circuit, short circuit, invalid '
                 u'data. So “SPN 100” alone is not a diagnosis yet, but '
                 u'“100/1” already tells you oil pressure has dropped below '
                 u'normal.',
    'midHowBody': u'A code has three parts: <b>MID</b> is which control unit reported it, '
                  u'<b>PID/SID</b> is which parameter or component is at fault, <b>FMI</b> '
                  u'is the type of fault (short circuit, open circuit, value out of '
                  u'range). On the scanner the code usually shows as MID-PID/SID-FMI, '
                  u'e.g. MID128 PID100 FMI4.',
    'multiHead': u'If there are several codes at once',
    'multiBody': u'That is almost always how it goes: one fault drags five or six codes '
                 u'behind it. An empty AdBlue tank first throws a level error, then '
                 u'interrupted dosing, then a NOx excess and a torque derate. Fix the '
                 u'root cause and the rest clear on their own. '
                 u'<a href="/en/">Paste the whole list</a> — we will show which '
                 u'code is the root cause.',
    'titleTpl':  u'%s fault codes | codetruck.ru',
    'h1Tpl':     u'%s fault codes',
    'descStd':   u'All %s fault codes: %d by system — which ones mean stop '
                 u'immediately, what each one means, and whether you can keep driving.',
    'subStd':    u'The reference covers <b>%d codes</b> from the factory tables of %s '
                 u'— the full list by system is below, stop-now codes first.',
    'descMid':   u'Decoded %s fault codes: %d by control module (MID), with the '
                 u'parameter and fault type.',
    'subMid':    u'The reference covers <b>%d codes</b> from the factory tables of %s, '
                 u'grouped by control module (MID).',
    'dealerHead': u'%s code examples',
    'dealerDesc': u'%s fault code reference: %d dealer codes in the database, with an '
                  u'English description. Look up your code on codetruck.ru.',
    'dealerSub': u'The database covers <b>%d dealer codes</b> — %s uses its own '
                 u'factory format, outside the J1939 SPN/FMI standard. A few examples '
                 u'below; look up your own code in the search on the homepage, where '
                 u'you can also pick “%s” from the brand list.',
}

# ---------------------------------------------------------------- проблемы
#
# (slug, title, H1, вступление) - тексты переведены вручную по смыслу
# русских формулировок из build_pages.SYMPTOMS, не сокращённый пересказ.
# sys_key/adv/spns для того же slug берутся из RУ-списка напрямую - см.
# symptoms_en_full() ниже.
SYMPTOMS_EN = {
    'gorit-check-engine': (
        u'Check Engine light on a truck — what it means',
        u'Check Engine light is on',
        u'A yellow light means the electronics found a fault and logged a code. On its '
        u'own it does not say how serious it is — it could be a clogged filter or '
        u'dropped oil pressure. You need to look at the code.'),
    'oshibka-adblue': (
        u'AdBlue error on a truck — causes and what to do',
        u'AdBlue (DEF) error',
        u'More than half of AdBlue errors come from an empty tank or the wrong fluid. '
        u'The SCR system moves to a power derate quickly, so do not put it off.'),
    'upala-moshchnost': (
        u'Truck lost power — torque derate',
        u'Power dropped, the truck will not pull',
        u'Torque derate is not a fault by itself — it is a protection response: '
        u'the electronics cut power because they found a problem. You need to find the '
        u'code that triggered the derate.'),
    'nizkoe-davlenie-masla': (
        u'Low oil pressure on a truck — what to do',
        u'Low oil pressure',
        u'This is the most urgent of the common faults. An engine survives only a few '
        u'minutes on low pressure — stop right away, do not try to make it back '
        u'to base.'),
    'peregrev-dvigatelya': (
        u'Truck engine overheating — codes and causes',
        u'Engine overheating',
        u'Overheating rarely comes alone — a power derate and a protective '
        u'shutdown usually follow. It is important to tell a real overheat apart from '
        u'a failed sensor — the FMI shows which.'),
    'zabit-sazhevyy-filtr': (
        u'Clogged DPF (diesel particulate filter) — signs and codes',
        u'Clogged particulate filter (DPF)',
        u'The filter clogs when the truck spends a lot of time idling or driving in the '
        u'city — regeneration never gets a chance to run. Back pressure rises '
        u'first, then power drops.'),
    'problemy-s-toplivom': (
        u'Water in the fuel and a clogged filter — truck codes',
        u'Water in the fuel, clogged filter',
        u'In winter, diesel waxing adds to the problem. Fuel-system codes often come '
        u'together with power loss and hard starting.'),
    'propalo-pitanie': (
        u'Power supply and CAN-bus errors on a truck',
        u'Power dropped, errors across the whole truck',
        u'If the scanner throws a dozen codes from different systems at once, it is '
        u'almost never ten separate faults — it is the power supply or the bus. '
        u'A sagging voltage or a broken CAN twisted pair floods the whole truck with '
        u'false codes.'),
    'ne-zavoditsya': (
        u'Truck will not start — causes and codes',
        u'Engine will not start',
        u'The starter cranks but the engine will not catch — that is one thing; '
        u'the starter does not turn at all — that is another. Start with power '
        u'and ground: a weak battery keeps the control units from waking up properly '
        u'and floods the truck with false codes. Next check fuel delivery and the '
        u'speed sensors — without their signal the control unit will not allow '
        u'injection at all.'),
    'glohnet-na-hodu': (
        u'Truck stalls while driving — codes and causes',
        u'Engine stalls while driving',
        u'Almost always this is fuel delivery: an air leak, a clogged filter, a failed '
        u'lift pump. The truck stalls under load or at idle, and it may not restart on '
        u'the shoulder. Rail and injection-pump codes tell you whether you will make '
        u'it to the shop under your own power.'),
    'troit-dvigatel': (
        u'Truck engine misfiring — cylinder misses',
        u'Engine running rough, misfires',
        u'The electronics count misfires per cylinder, so the code names the culprit '
        u'directly. Most often it is an injector, less often compression or wiring. '
        u'Do not keep driving like this — unburned fuel goes into the exhaust '
        u'and fouls the catalyst along with the particulate filter.'),
    'chernyy-dym': (
        u'Black smoke from a truck exhaust — causes and codes',
        u'Black exhaust smoke',
        u'Black smoke means too much fuel or not enough air. Check the intake: a '
        u'clogged filter, a leak in the ducting, a failed turbo or its variable '
        u'geometry. Power usually drops and fuel consumption rises along with the '
        u'smoke.'),
    'belyy-dym': (
        u'White smoke from a truck exhaust — causes and codes',
        u'White exhaust smoke',
        u'White vapor on a cold start is normal. White smoke on a warmed-up engine '
        u'means either unburned fuel from a bad injector, or coolant in the cylinders. '
        u'The second is more serious — you are losing coolant, and the head '
        u'gasket usually follows.'),
    'siniy-dym': (
        u'Blue smoke from a truck exhaust — oil in the cylinders',
        u'Blue smoke, oil in the exhaust',
        u'Bluish smoke means oil is entering the combustion chamber. On higher-mileage '
        u'trucks the usual cause is worn turbo seals — oil gets pulled through '
        u'the turbo straight into the intake. Check the oil level and pressure, and '
        u'listen to the turbo as it spins down.'),
    'bolshoy-rashod-topliva': (
        u'High fuel consumption on a truck — codes and causes',
        u'Fuel consumption has gone up',
        u'Consumption rises when the engine is not running in its intended range: not '
        u'enough air, a leaking injector, a clogged particulate filter. The '
        u'electronics see this through their sensors before you notice the number on '
        u'the trip computer.'),
    'ne-idet-regeneratsiya': (
        u'DPF regeneration will not run — particulate filter codes',
        u'DPF regeneration will not run',
        u'Regeneration will not start if the truck idles a lot or the system cannot '
        u'raise exhaust temperature. Back pressure rises, and a power derate follows. '
        u'A forced regeneration at the shop only treats the symptom — if the '
        u'underlying cause is still there, the filter will clog again.'),
    'nasos-adblue': (
        u'AdBlue pump not delivering — DEF dosing faults',
        u'AdBlue not pumping, dosing error',
        u'The pump module is not building pressure or cannot hold it: a blocked line, '
        u'crystallized DEF, a failed heater. In winter this is the most common cause '
        u'of SCR errors. Dosing gets interrupted, and the control unit starts counting '
        u'down to a power derate — by run time, not by mileage.'),
    'datchik-nox': (
        u'NOx sensor error on a truck — codes and causes',
        u'NOx sensor error',
        u'There are usually two NOx sensors — upstream and downstream of the '
        u'catalyst — and the control unit compares them. The error can come '
        u'from the sensor itself, from poor-quality DEF, or from dosing that is not '
        u'working. The code shows exactly what did not match up.'),
    'ne-zaryazhaet-generator': (
        u'Battery not charging on a truck — alternator fault',
        u'Alternator is not charging',
        u'With the engine running, the on-board network should read 27–29 V. '
        u'Lower — the alternator, the belt, or the wiring. Higher — the '
        u'voltage regulator, and this is more dangerous: overcharging boils the '
        u'batteries dry and can knock out electronics.'),
    'ne-nabiraet-vozduh': (
        u'Air system not building pressure on a truck',
        u'Air pressure will not build',
        u'Slow build-up or falling pressure points to a leak, the compressor, or the '
        u'air dryer. Without full pressure the brakes will not release fully, and on '
        u'a long downgrade there may not be enough braking at all. This is one case '
        u'where you do not head out.'),
    'gorit-lampa-abs': (
        u'ABS light is on — truck codes and causes',
        u'ABS light is on',
        u'The wheel speed sensor is the usual culprit — excess air gap, dirt, a '
        u'damaged tone ring. The service brakes still work, but ABS is disabled '
        u'— on a slippery surface you will need to brake more carefully. The '
        u'code names the axle and side directly.'),
    'stoyanochnyy-tormoz': (
        u'Parking brake will not release — truck codes',
        u'Parking brake will not release',
        u'Spring brake chambers release the shoes with air pressure, so the first '
        u'thing to check is whether the circuit has built full pressure. Second is '
        u'the parking brake switch and its circuit itself — the control unit '
        u'thinks the parking brake is still set and will not let the truck move.'),
    'ne-pereklyuchayutsya-peredachi': (
        u'AMT gearbox will not shift — truck codes',
        u'Gears will not shift',
        u'The automated manual gearbox drops into limp-home mode and leaves you with '
        u'one or two gears, or neutral. By frequency: air pressure in the gearbox '
        u'circuit, shift-fork position sensors, the clutch actuator. The main risk is '
        u'losing your gear on a grade.'),
    'probuksovyvaet-sceplenie': (
        u'Clutch slipping on a truck — codes and signs',
        u'Clutch is slipping',
        u'RPM climbs but speed does not — the discs are not holding torque. The '
        u'electronics catch this from the mismatch between engine speed and the '
        u'gearbox output shaft, and log a code before the difference is noticeable '
        u'from the cab. Do not keep pulling a loaded truck uphill like this.'),
    'oshibka-retardera': (
        u'Retarder error on a truck — codes and causes',
        u'Retarder error',
        u'The retarder shuts itself off when the oil overheats or it loses '
        u'communication with the control unit. You can still drive, but on a long '
        u'downgrade you will be braking with the service brakes alone, and those '
        u'overheat on a long descent. This changes your trip plan, not just a '
        u'fault-memory entry.'),
    'greetsya-v-goru': (
        u'Overheats on a grade under load — cooling codes',
        u'Overheats under load',
        u'If the temperature climbs only on grades and drops back on level ground, '
        u'the problem is usually heat rejection: the fan viscous clutch, a clogged '
        u'radiator, the intercooler. Sensors and coolant level read normal, which is '
        u'why the warning light comes on late — once the margin is already used '
        u'up.'),
    'oshibka-tahografa': (
        u'Tachograph error on a truck — codes and causes',
        u'Tachograph error',
        u'The tachograph broadcasts speed and distance over the bus, so its fault '
        u'pulls in codes from other systems too — from cruise control to the '
        u'speed limiter. The cause is more often the sensor on the gearbox and its '
        u'wiring than the instrument itself.'),
    'ne-rabotaet-motornyy-tormoz': (
        u'Engine (compression) brake not working — truck codes',
        u'Engine brake not working',
        u'The engine (compression) brake shuts itself off if the exhaust flap or its '
        u'actuator is faulty. On a descent this immediately shifts the whole braking '
        u'load to the service brakes — not something you do with a loaded truck '
        u'going downhill.'),
}


def nav_en(section=None):
    up = u'<a href="/en/">&larr; code lookup</a>'
    if not section:
        return up
    name, path = SECTIONS_EN[section]
    return u'%s<span class="sep">&middot;</span><a href="/%s">%s</a>' % (up, path, name)


def breadcrumb_en(name, canon, section=None):
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'codetruck.ru', 'item': SITE + '/en/'}]
    if section:
        sname, spath = SECTIONS_EN[section]
        items.append({'@type': 'ListItem', 'position': 2, 'name': sname,
                      'item': '%s/%s' % (SITE, spath)})
    items.append({'@type': 'ListItem', 'position': len(items) + 1, 'name': name, 'item': canon})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}


def page_en(path, title, desc, h1, sub, sections, section=None, rel_ru=None):
    pub = path[:-len('index.html')] if path.endswith('index.html') else path
    canon = '%s/%s' % (SITE, pub)
    # rel_ru кладём той же обрезкой, что и pub - иначе у рубричных index.html
    # hreflang указывал бы на .../index.html, а canonical на .../ (расхождение).
    if rel_ru:
        rel_ru = rel_ru[:-len('index.html')] if rel_ru.endswith('index.html') else rel_ru
    alt = bp.alt_links(True, rel_ru) if rel_ru else u''
    ld = (bp.ld_script({'@context': 'https://schema.org', '@type': 'TechArticle',
                        'headline': title, 'description': desc, 'url': canon,
                        'inLanguage': 'en'})
          + bp.ld_script(breadcrumb_en(h1, canon, section)))
    body = [bp.HEAD.format(title=bp.esc(title), desc=bp.esc(desc), canon=canon,
                           ogtitle=bp.esc(h1), mid=bp.METRIKA_ID, ld=ld, nav=nav_en(section),
                           lang='en', locale='en_US', alt=alt)]
    body.append(u'<h1>%s</h1>' % bp.esc(h1))
    body.append(u'<p class="sub">%s</p>' % sub)
    body.extend(sections)
    body.append(u'<p class="cta">Know the code number? <a href="/en/">Type it into the '
                u'search</a> — or paste the whole list from the scanner and we will '
                u'show which fault is the real one.</p>')
    body.append(u'</div>\n</body>\n</html>\n')
    full = os.path.join(ROOT, path)
    d = os.path.dirname(full)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(full, 'w', encoding='utf-8').write(''.join(body))
    return pub


def add_hreflang_to_ru(rel_path):
    """Дописывает hreflang в уже собранную русскую marki/problemy-страницу
    постобработкой: она была сгенерирована без alt (bp.page() вызывался без
    en_marki/en_problemy - переделывать саму сборку ради трёх строк не
    стали, HEAD.format() уже вставил на это место пустую строку).
    Рубричные index.html публикуются под директорией (canonical без
    index.html - см. bp.page()), поэтому здесь та же обрезка."""
    full = os.path.join(ROOT, rel_path)
    if not os.path.isfile(full):
        return False
    html = io.open(full, encoding='utf-8').read()
    if 'hreflang' in html:
        return False
    pub = rel_path[:-len('index.html')] if rel_path.endswith('index.html') else rel_path
    pub = pub.replace(os.sep, '/')
    canon_line = '<link rel="canonical" href="%s/%s">' % (SITE, pub)
    if canon_line not in html:
        return False
    alt = bp.alt_links(True, pub)
    html = html.replace(canon_line, canon_line + alt, 1)
    io.open(full, 'w', encoding='utf-8').write(html)
    return True


def build():
    ru_db = bp.load_db()
    en_db = be.load_en()
    pcode = bp.load_pcode()
    i18n = extract_js_object('I18N')['en']
    risk_tx = extract_js_object('RISK_TX')['en']
    risk_h = extract_js_object('RISK_H')['en']
    risk_title = extract_js_object('RISK_TITLE')['en']
    risk_flag = extract_js_object('RISK_FLAG')['en']
    risk_map = extract_js_object('RISK_MAP')
    urgent_fmi = set(ru_db['urgentFmi'])
    urgent_spn = set(ru_db['urgentSpn'])
    brand_names = ru_db['brandNames']

    per_en = be.per_spn_en(en_db)
    en_set = (set(per_en) | {int(k) for k in en_db.get('universal', {})}
              | {int(k) for k in en_db.get('spn', {})})

    # Та же сборка, что и build_en_pages.py делает для en/kody/ - нужна
    # разбивка по системам (sys_of/by_sys) и признак "ехать нельзя"
    # (stop_of), в точности как её видит английская сборка кодов, а не
    # заново посчитанная своим способом (расхождение было бы багом).
    info = bp.build(en_spns=en_set)
    written = [s for s in info['written'] if s in en_set]
    sys_of, stop_of, by_sys = info['sys'], info['stop'], info['by_sys']

    def bname(b):
        key = BRAND_LBL.get(b)
        return (i18n.get(key) if key else None) or brand_names.get(b, b)

    def en_std(spn):
        s = str(spn)
        return en_db.get('spn', {}).get(s) or en_db.get('universal', {}).get(s) or u''

    derived = bp.derive_names(per_en, [s for s in written if not en_std(s)])

    def name_of(spn):
        return en_std(spn) or derived.get(spn) or u''

    def code_link(spn, href):
        nm = name_of(spn)
        return (u'<li><a href="%s"><span class="mono">SPN %d</span>%s</a></li>'
                % (href, spn, (u'<span class="nm">%s</span>' % bp.esc(nm)) if nm else u''))

    def code_links(spns, prefix='../kody/'):
        return u''.join(code_link(s, '%sspn-%d.html' % (prefix, s)) for s in spns)

    def is_stop(spn):
        return bool(stop_of.get(spn))

    def risk_section(sys_key, fmis, urgent_spn_hit):
        key, lvl, _ = bp.page_risk(sys_key, fmis, urgent_fmi, urgent_spn_hit)
        if not key or key not in risk_tx:
            return u''
        happens, ends = risk_tx[key][0], risk_tx[key][1]
        note = u''
        rule = risk_map.get(sys_key)
        if (rule and rule.get('elec') and key != rule['elec'][0]
                and any(f in bp.FMI_ELEC for f in (fmis or []))):
            e = risk_tx[rule['elec'][0]]
            note = u'<p class="rkn">%s %s</p>' % (bp.esc(e[0]), bp.esc(e[1]))
        if (urgent_spn_hit or any(f in urgent_fmi for f in (fmis or []))) and lvl != 'now':
            note += u'<p class="rkn">%s</p>' % bp.esc(risk_flag)
        tier = 'now' if lvl == 'now' else ('warn' if lvl in ('short', 'base') else 'calm')
        return (u'<section><h2>%s</h2>'
                u'<div class="risk t-%s"><span class="rkb">Time you have: %s</span>'
                u'<p>%s</p><p>%s</p>%s</div></section>'
                % (bp.esc(risk_title), tier, bp.esc(risk_h[lvl]),
                   bp.esc(happens), bp.esc(ends), note))

    en_marki, en_problemy = set(), set()

    # --- по маркам: SPN/FMI (стандарт) -----------------------------
    brands = ru_db['brands']
    for b in sorted(brands, key=lambda x: bname(x)):
        mine_en = sorted({s for s in per_en if b in per_en[s]})
        if not mine_en:
            continue
        bn = bname(b)
        stop_codes = [s for s in mine_en if is_stop(s)][:12]
        secs = []
        if stop_codes:
            secs.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                        % (MK['stopHead'], code_links(stop_codes)))
        by_sys_brand = {}
        for s in mine_en:
            by_sys_brand.setdefault(sys_of.get(s, 'other'), []).append(s)
        for key in bp.SYS_ORDER_BRAND:
            bucket = by_sys_brand.get(key)
            if not bucket:
                continue
            secs.append(u'<section><h2>%s — %d codes</h2><ul class="near">%s</ul></section>'
                        % (bp.esc(i18n.get(SYS_KEY[key], key)), len(bucket), code_links(bucket)))
        secs.append(u'<section><h2>%s</h2><p>%s</p></section>' % (MK['howHead'], MK['howBody']))
        secs.append(u'<section><h2>%s</h2><p>%s</p></section>' % (MK['multiHead'], MK['multiBody']))

        title = MK['titleTpl'] % bname(b)
        h1 = MK['h1Tpl'] % bname(b)
        desc = MK['descStd'] % (bn, len(mine_en))
        sub = MK['subStd'] % (len(mine_en), bp.esc(bn))
        rel = 'marki/%s.html' % b
        page_en('en/' + rel, title, desc, h1, sub, secs, 'marki', rel_ru=rel)
        en_marki.add(b)

    # --- по маркам с MID-структурой (Mack, Detroit Diesel) ---------
    for b, mod_names in MID_MODULE_NAMES_EN.items():
        table = en_db.get('brands', {}).get(b)
        if not table:
            continue
        entries = []
        for key, text in table.items():
            if not text:
                continue
            composite, dot, fmi = key.rpartition('.')
            m = bp.MID_RE.match(composite)
            if not (m and dot and fmi.isdigit()):
                continue
            entries.append((m.group(1), m.group(2), int(fmi), text))
        if not entries:
            continue
        by_mid = {}
        for mid, pidsid, fmi, text in entries:
            by_mid.setdefault(mid, []).append((pidsid, fmi, text))
        bn = bname(b)
        secs = []
        for mid in sorted(by_mid, key=int):
            rows = sorted(by_mid[mid])
            title_mod = mod_names.get(mid, u'Module MID %s' % mid)
            t = [u'<table><tr><th>Code</th><th>Meaning</th></tr>']
            for pidsid, fmi, text in rows:
                t.append(u'<tr><td class="fmi">M%s-%s.%d</td><td>%s</td></tr>'
                         % (mid, pidsid, fmi, bp.rich(text)))
            t.append('</table>')
            secs.append(u'<section><h2>%s</h2>%s</section>' % (bp.esc(title_mod), ''.join(t)))
        secs.append(u'<section><h2>%s</h2><p>%s</p></section>' % (MK['howHead'], MK['midHowBody']))

        title = MK['titleTpl'] % bn
        h1 = MK['h1Tpl'] % bn
        desc = MK['descMid'] % (bn, len(entries))
        sub = MK['subMid'] % (len(entries), bp.esc(bn))
        rel = 'marki/%s.html' % b
        page_en('en/' + rel, title, desc, h1, sub, secs, 'marki', rel_ru=rel)
        en_marki.add(b)

    # --- дилерские марки (Scania, Caterpillar, ...) -----------------
    for b in sorted(pcode, key=lambda x: bname(x)):
        if b in en_marki:
            continue
        bn = brand_names.get(b)
        if not bn:
            continue
        rows = sorted(
            ((code, entry.get('en') or '') for code, entry in pcode[b].items()
             if entry.get('en')),
            key=lambda r: bp.code_sort_key(r[0]))
        if not rows:
            continue
        bn_en = bname(b)
        secs = [u'<section><h2>%s</h2>%s</section>'
                % (MK['dealerHead'] % bn_en, bp.pcode_table(bp.sample_rows(rows)))]

        title = MK['titleTpl'] % bn_en
        h1 = MK['h1Tpl'] % bn_en
        desc = MK['dealerDesc'] % (bn_en, len(rows))
        sub = MK['dealerSub'] % (len(rows), bp.esc(bn_en), bp.esc(bn_en))
        rel = 'marki/%s.html' % b
        page_en('en/' + rel, title, desc, h1, sub, secs, 'marki', rel_ru=rel)
        en_marki.add(b)

    # --- рубрика en/marki/ -------------------------------------------
    veh, mid, dlr = [], [], []
    for b in en_marki:
        bn = bname(b)
        if b in pcode and b not in MID_MODULE_NAMES_EN and not any(
                k.split('.')[0].isdigit() for k in brands.get(b, {})):
            dlr.append((b, bn))
        elif b in MID_MODULE_NAMES_EN:
            mid.append((b, bn))
        else:
            veh.append((b, bn))

    def brand_rows(rows):
        return u'<ul class="near">%s</ul>' % ''.join(
            u'<li><a href="%s.html">%s</a></li>' % (b, bp.esc(bn))
            for b, bn in sorted(rows, key=lambda r: r[1]))

    secs = []
    if veh or mid:
        secs.append(u'<section><h2>SPN/FMI codes under the J1939 standard</h2>'
                    u'<p class="lead">For these makes the code follows the standard: a '
                    u'component number plus a fault type.</p>%s</section>'
                    % brand_rows(veh + mid))
    if dlr:
        secs.append(u'<section><h2>Dealer codes in their own format</h2>'
                    u'<p class="lead">These makes number faults their own way, outside '
                    u'the J1939 standard. Look up a code in the search on the '
                    u'homepage.</p>%s</section>' % brand_rows(dlr))

    page_en('en/marki/index.html',
            u'Truck fault codes by make — decoded | codetruck.ru',
            u'Truck fault codes by make: %d makes with factory tables, from Volvo and '
            u'Scania to Mercedes and Shacman.' % len(en_marki),
            u'Fault codes by make',
            u'Factory tables for <b>%d makes</b>: some read by the J1939 standard, '
            u'others use their own dealer format. Pick a make or type a code on the '
            u'homepage.' % len(en_marki),
            secs, 'marki', rel_ru='marki/index.html')

    # --- проблемы (симптомы) ----------------------------------------
    ru_symptoms = {row[0]: row for row in bp.SYMPTOMS}
    sym_index = []
    have = set(written)
    for slug, (title_h, h1, intro) in SYMPTOMS_EN.items():
        row = ru_symptoms.get(slug)
        if not row:
            continue
        _, _, _, _, sys_key, adv, spns = row
        if spns:
            pool = [s for s in spns if s in have]
        elif sys_key:
            pool = [s for s in by_sys.get(sys_key, [])]
        else:
            pool = [s for s in written if is_stop(s)]
        stop_codes = [s for s in pool if is_stop(s)][:12]
        rest = [s for s in pool if s not in stop_codes][:12]
        if not (stop_codes or rest):
            continue

        secs = []
        if stop_codes:
            secs.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>'
                        % (MK['stopHead'], code_links(stop_codes)))
        if rest:
            secs.append(u'<section><h2>Other codes for this system</h2>'
                        u'<ul class="near">%s</ul></section>' % code_links(rest))
        if sys_key:
            sec = risk_section(sys_key, sorted(urgent_fmi), False)
            if sec:
                secs.append(sec)
        act = i18n.get(ACT_KEY.get(adv, '')) if adv else None
        if act:
            secs.append(u'<section><h2>What to check on the spot</h2><p>%s</p></section>' % act)
        secs.append(
            u'<section><h2>Can I keep driving</h2><p>The answer depends on the code, not '
            u'the light. A yellow light is a warning; a red one means do not move. But '
            u'even under a yellow light there are faults that require stopping right '
            u'away — low oil pressure, overheating, lost brake pressure. '
            u'<a href="/en/">Enter the code</a> — the reference will tell you '
            u'plainly whether to keep driving or stop.</p></section>')

        rel = 'problemy/%s.html' % slug
        desc = intro if len(intro) <= 155 else intro[:155].rsplit(u' ', 1)[0] + u'…'
        sym_index.append((rel, h1, intro))
        page_en('en/' + rel, title_h + u' | codetruck.ru', desc, h1, bp.esc(intro),
                secs, 'problemy', rel_ru=rel)
        en_problemy.add(slug)

    # --- рубрика en/problemy/ ----------------------------------------
    secs = [u'<section><h2>Where to start</h2><ul class="lines">%s</ul></section>'
            % ''.join(u'<li><a href="%s">%s</a> — %s</li>'
                      % (os.path.basename(rel), bp.esc(h1), bp.esc(intro.split(u'. ')[0]))
                      for rel, h1, intro in sym_index)]
    secs.append(
        u'<section><h2>If you do have a code</h2><p>A symptom narrows things down, but '
        u'the code number gives the exact answer. <a href="/en/">Type the code from '
        u'the scanner</a> — the reference will tell you plainly whether to keep '
        u'driving or stop, and how much time you have. Several codes at once — '
        u'paste the whole list, we will show which one is the root cause.</p></section>')

    page_en('en/problemy/index.html',
            u'Truck faults by symptom — what to do | codetruck.ru',
            u'What to do if a truck throws Check Engine, loses power, an AdBlue error, '
            u'or overheats: likely codes, whether you can keep driving, and what to '
            u'check on the spot.',
            u'Faults by symptom',
            u'No code, but the truck is not behaving right? Start with the symptom '
            u'— below is what usually causes it, which codes confirm it, and '
            u'whether you can make it in.',
            secs, 'problemy', rel_ru='problemy/index.html')

    # --- hreflang в уже собранные русские страницы --------------------
    patched = 0
    for b in en_marki:
        if add_hreflang_to_ru('marki/%s.html' % b):
            patched += 1
    if add_hreflang_to_ru('marki/index.html'):
        patched += 1
    for slug in en_problemy:
        if add_hreflang_to_ru('problemy/%s.html' % slug):
            patched += 1
    if add_hreflang_to_ru('problemy/index.html'):
        patched += 1

    # --- sitemap: добавляем новые адреса к уже накопленным ------------
    lastmod_path = os.path.join(ROOT, bp.LASTMOD_DB)
    db = json.loads(io.open(lastmod_path, encoding='utf-8').read())
    urls = list(db.get('urls') or [])
    # sorted() - иначе порядок в sitemap.xml плясал бы от запуска к запуску:
    # en_marki/en_problemy - множества, у Python порядок обхода set() по
    # строкам не гарантирован между процессами (рандомизация хеша).
    new_urls = (['%s/en/marki/' % SITE]
                + ['%s/en/marki/%s.html' % (SITE, b) for b in sorted(en_marki)]
                + ['%s/en/problemy/' % SITE]
                + ['%s/en/problemy/%s.html' % (SITE, s) for s in sorted(en_problemy)])
    for u in new_urls:
        if u not in urls:
            urls.append(u)
    bp.write_sitemap(urls)

    print(u'марок с английской страницей: %d' % len(en_marki))
    print(u'симптомов с английской страницей: %d' % len(en_problemy))
    print(u'hreflang дописан в русских страниц: %d' % patched)
    return en_marki, en_problemy


if __name__ == '__main__':
    build()
