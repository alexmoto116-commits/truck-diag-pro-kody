# -*- coding: utf-8 -*-
"""
Два новых раздела (09.11.2026):
  /j1587/            - коды J1587/J1708: MID / PID / SID / FMI (данные j1587_data.py)
  /vag-otopiteli/    - ошибки автономных отопителей VAG в VCDS/ODIS, блок 18 Aux. Heat (данные vagaux_data.py)
Оглавление и страницы, ru и en (/en/...). Вызывается из build_pages.build() рядом с разборами; отдаёт адреса для карт.
Источники и расхождения - novye_kody_istochniki.md.
"""
import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp                                    # noqa: E402
import j1587_data as jd                                     # noqa: E402
import vagaux_data as vd                                    # noqa: E402

SITE = bp.SITE
esc = bp.esc

CSS = (u'<style>.nk p,.nk li{color:#CBD7E3;font-size:15.5px;line-height:1.65}.nk ul,.nk ol{margin:0 0 14px;padding-left:22px}'
       u'.nk p{margin:0 0 12px;max-width:68ch}.nk td,.nk th{overflow-wrap:anywhere}.nk h3.faq-q{font-size:1em;font-weight:700;margin:14px 0 4px}'
       u'.nk .short{border:1px solid rgba(111,227,211,.3);border-radius:12px;background:rgba(111,227,211,.05);padding:12px 16px;margin:0 0 26px}'
       u'.nk .short p{margin:0}.nk .tw{overflow-x:auto}.nk .risk p{max-width:68ch}.nk .src a{overflow-wrap:anywhere}</style>')

CFG = {
    'j1587': dict(dir='j1587', ru_sec=u'Коды J1587', en_sec=u'J1587 codes'),
    'vag-otopiteli': dict(dir='vag-otopiteli', ru_sec=u'Отопители VAG', en_sec=u'VAG heaters'),
}

L = {
    'ru': dict(home=u'Главная', verdict=u'Можно ли ехать', mean=u'Что значит код', checks=u'Что проверить по порядку',
               service=u'Когда нужен сервис', faq=u'Вопросы и ответы', src=u'Источники', near=u'Соседние страницы',
               hub=u'Оглавление раздела', disc=u'Расхождения источников', causes=u'Возможные причины',
               cta=u'Не нашли свой код? <a href="/">Введите его в поиск</a> — или вставьте сразу весь список со сканера, покажем, какая поломка настоящая.',
               note_brand=u'Названия узлов (PID, SID) и смысл FMI — по стандарту SAE J1587; набор FMI у узла — по таблицам Volvo. '
                          u'У Mack, Freightliner, International, Detroit и других производителей состав кодов и подписи могут отличаться: '
                          u'сверяйте с руководством вашей марки. Решение о поездке остаётся за водителем.',
               note_vag=u'Решение о поездке остаётся за водителем. Описания ориентированы на VW, Audi и Skoda; номера компонентов (V6, V54, G18 и др.) '
                        u'взяты из руководств Audi и могут отличаться у вашей модели.'),
    'en': dict(home=u'Home', verdict=u'Can you drive', mean=u'What the code means', checks=u'What to check, in order',
               service=u'When a workshop is needed', faq=u'Questions and answers', src=u'Sources', near=u'Related pages',
               hub=u'Section index', disc=u'Where the sources differ', causes=u'Possible causes',
               cta=u'Cannot find your code? <a href="/en/">Type it into the search</a> — or paste the whole list from the scanner and we will show which fault is the real one.',
               note_brand=u'Part names (PID, SID) and the meaning of FMI follow the SAE J1587 standard; the FMI set for a part follows Volvo tables. '
                          u'Mack, Freightliner, International, Detroit and other makers may differ in which codes exist and how they are labelled: '
                          u'check the manual for your make. The decision to drive remains with the driver.',
               note_vag=u'The decision to drive remains with the driver. The descriptions target VW, Audi and Skoda; component numbers (V6, V54, G18 etc.) '
                        u'come from Audi manuals and may differ on your model.'),
}

TIER = {'calm': 'calm', 'warn': 'warn', 'now': 'now'}


def _write(rel, html):
    full = os.path.join(bp.ROOT, rel.replace('/', os.sep))
    d = os.path.dirname(full)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(full, 'w', encoding='utf-8').write(html)


def _pre(sec, lang):
    return ('/%s/' if lang == 'ru' else '/en/%s/') % CFG[sec]['dir']


def _nav(sec, lang, here=None):
    c = CFG[sec]
    if lang == 'ru':
        return bp.nav_of(sec, here)
    items = [u'<a href="/en/">%s</a>' % L['en']['home']]
    if here:
        items.append(u'<a href="%s">%s</a>' % (_pre(sec, 'en'), c['en_sec']))
        items.append(u'<span>%s</span>' % esc(here))
    else:
        items.append(u'<span>%s</span>' % c['en_sec'])
    return u'<span class="sep">&rsaquo;</span>'.join(items)


def _crumb(sec, lang, here, canon):
    c = CFG[sec]
    base = SITE + ('/' if lang == 'ru' else '/en/')
    items = [{'@type': 'ListItem', 'position': 1, 'name': L[lang]['home'], 'item': base},
             {'@type': 'ListItem', 'position': 2, 'name': c['ru_sec' if lang == 'ru' else 'en_sec'],
              'item': SITE + _pre(sec, lang)}]
    if here:
        items.append({'@type': 'ListItem', 'position': 3, 'name': here, 'item': canon})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}


def _search(lang):
    if lang == 'ru':
        return bp.search_form(None)
    return bp.search_form(None, ph=u'Your code, e.g. 1078/3', action=u'/en/', btn=u'Search', label=u'Fault code')


def _head(sec, lang, rel, title, desc, h1, ld_objs, here):
    assert len(title) <= 65, (len(title), title)
    assert u'codetruck' not in title.lower() and u'…' not in title and u'...' not in title, title
    pub = rel[:-len('index.html')] if rel.endswith('index.html') else rel
    canon = '%s/%s' % (SITE, pub)
    ru_rel = pub if lang == 'ru' else pub[len('en/'):]
    ld = u''.join(bp.ld_script(o) for o in ld_objs(canon)) + bp.ld_script(_crumb(sec, lang, here, canon))
    head = bp.HEAD.format(title=esc(title), desc=esc(desc), canon=canon, ogtitle=esc(h1), mid=bp.METRIKA_ID, ld=ld,
                          nav=_nav(sec, lang, here), lang=lang, locale='ru_RU' if lang == 'ru' else 'en_US',
                          alt=bp.alt_links(True, ru_rel))
    return head


def _tbl(hdr, rows):
    return (u'<div class="tw"><table><tr>%s</tr>%s</table></div>' % (
        u''.join(u'<th>%s</th>' % esc(h) for h in hdr),
        u''.join(u'<tr>%s</tr>' % u''.join(c if c.startswith(u'<td') else u'<td>%s</td>' % esc(c) for c in r) for r in rows)))


def _tier(lvl):
    return TIER[lvl]


def _faq_ld(faq):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}


def _src_html(keys, SRC, lang):
    i = 0 if lang == 'ru' else 1
    return u'<section class="src"><h2>%s</h2><ul>%s</ul></section>' % (
        L[lang]['src'], u''.join(u'<li><a href="%s" rel="nofollow noopener">%s</a></li>' % (esc(SRC[k][2]), esc(SRC[k][i])) for k in keys))


def _foot(lang, body):
    body.append(u'</div>')
    body.append(u'<p class="cta">%s</p>' % L[lang]['cta'])
    body.append(bp.soc_foot(lang))
    body.append(u'</div>\n' + bp.CF_SNIPPET + u'\n</body>\n</html>\n')
    return u''.join(body)


# ---------------------------------------------------------------------------------------------------- J1587
def _mid_row(mid, lang):
    for m, sr, se, vr, ve in jd.MIDS:
        if m == mid:
            return (sr, vr) if lang == 'ru' else (se, ve)


def j_page(p, lang):
    sec = 'j1587'
    lg = L[lang]
    t = p[lang]
    title = p['title_' + lang]
    rel = ('%s/%s.html' % (CFG[sec]['dir'], p['slug'])) if lang == 'ru' else ('en/%s/%s.html' % (CFG[sec]['dir'], p['slug']))
    nm = p['nm_' + lang]
    sae, volvo = _mid_row(p['mid'], lang)
    desc = t['short']
    if len(desc) > 190:
        desc = desc[:190].rsplit(u' ', 1)[0].rstrip(u',;:—-') + u'.'

    def ld(canon):
        return [{'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': title, 'description': desc,
                 'url': canon, 'inLanguage': lang, 'datePublished': jd.DATE, 'dateModified': jd.DATE,
                 'author': {'@type': 'Organization', 'name': 'codetruck', 'url': SITE + '/'}}, _faq_ld(t['faq'])]

    body = [_head(sec, lang, rel, title, desc, title, ld, title), CSS, u'<div class="nk">', u'<h1>%s</h1>' % esc(title), _search(lang),
            u'<div class="short"><p>%s</p></div>' % esc(t['short'])]
    body.append(u'<section><h2>%s</h2><div class="risk t-%s"><span class="rkb">%s</span><p>%s</p></div></section>'
                % (lg['verdict'], _tier(p['lvl']), esc(t['badge']), esc(t['verdict'])))
    if lang == 'ru':
        hdr = [u'Что', u'Значение']
        rows = [[u'MID %d' % p['mid'], u'по SAE J1587: %s; в таблицах Volvo: %s' % (sae, volvo)],
                [u'%s %s' % (p['kind'], p['num']), u'%s (названия — по SAE J1587)' % nm]]
    else:
        hdr = [u'Item', u'Meaning']
        rows = [[u'MID %d' % p['mid'], u'SAE J1587: %s; Volvo tables: %s' % (sae, volvo)],
                [u'%s %s' % (p['kind'], p['num']), u'%s (names per SAE J1587)' % nm]]
    mean = _tbl(hdr, rows)
    if p['fmis']:
        i = 0 if lang == 'ru' else 1
        fr = [[u'<td class="fmi">FMI %d</td>' % f, jd.FMI[f][i]] for f in p['fmis']]
        mean += _tbl([u'FMI', u'Значение по SAE J1587' if lang == 'ru' else u'Meaning per SAE J1587'], fr)
        if lang == 'ru':
            mean += u'<p class="sub">Перечислены FMI, которые таблица Volvo приводит для этого узла. Полный список FMI — <a href="%s">в оглавлении раздела</a>.</p>' % _pre(sec, lang)
        else:
            mean += u'<p class="sub">The FMIs listed are those the Volvo table gives for this part. The full FMI list is <a href="%s">in the section index</a>.</p>' % _pre(sec, lang)
    else:
        mean += (u'<p class="sub">В нашем источнике (таблица Volvo) для этой строки FMI по отдельности не указаны. Значения FMI — <a href="%s">в таблице на странице-оглавлении</a>.</p>' if lang == 'ru'
                 else u'<p class="sub">Our source (the Volvo table) does not give FMIs separately for this row. The FMI meanings are <a href="%s">in the table on the section index page</a>.</p>') % _pre(sec, lang)
    body.append(u'<section><h2>%s</h2>%s</section>' % (lg['mean'], mean))
    body.append(u'<section><h2>%s</h2><ol>%s</ol></section>' % (lg['checks'], u''.join(u'<li>%s</li>' % esc(c) for c in t['checks'])))
    body.append(u'<section><h2>%s</h2><p>%s</p></section>' % (lg['service'], esc(t['service'])))
    # расхождения
    disc = []
    if p['mid'] == 144:
        disc.append(u'По стандарту SAE J1587 MID 144 — круиз-контроль; в таблицах Volvo этот блок — ЭБУ автомобиля (VECU), в руководстве VNL — «Cab Controller». Берите смысл по марке вашей машины.' if lang == 'ru'
                    else u'In the SAE J1587 standard MID 144 is cruise control; in Volvo tables the unit is the Vehicle ECU (VECU), and the VNL manual labels it "Cab Controller". Use the meaning for your make.')
    if p['fmis'] and 9 in p['fmis']:
        disc.append(u'FMI 9: по SAE — неверная частота обновления данных, в таблицах Volvo — ошибка связи. На практике это потеря сообщений.' if lang == 'ru'
                    else u'FMI 9: SAE says abnormal update rate, Volvo tables say communication fault. In practice it is lost messages.')
    if disc:
        body.append(u'<section><h2>%s</h2>%s</section>' % (lg['disc'], u''.join(u'<p>%s</p>' % esc(d) for d in disc)))
    body.append(u'<section><h2>%s</h2>%s</section>' % (lg['faq'], u''.join(
        u'<h3 class="faq-q">%s</h3><p>%s</p>' % (esc(q), esc(a)) for q, a in t['faq'])))
    pre = _pre(sec, lang)
    near = [q for q in jd.PAGES if q['mid'] == p['mid'] and q['slug'] != p['slug']][:8]
    li = u''.join(u'<li><a href="%s%s.html"><span class="mono">%s</span><span class="nm">%s</span></a></li>' % (
        pre, q['slug'], esc(u'MID %d %s' % (q['mid'], q['label'])), esc(q['nm_' + lang])) for q in near)
    li += u'<li><a href="%s"><span class="nm">%s</span></a></li>' % (pre, lg['hub'])
    body.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>' % (lg['near'], li))
    body.append(_src_html(p['src'], jd.SRC, lang))
    body.append(u'<p class="sub">%s</p>' % esc(lg['note_brand']))
    return rel, _foot(lang, body)


HUB_J = {
    'ru': dict(h1=u'Коды J1587/J1708: MID, PID, SID, FMI — что значат',
               title=u'Коды J1587 и J1708: MID, PID, SID, FMI — расшифровка',
               desc=u'Как читать коды MID, PID, SID и FMI на старых грузовиках Volvo, Mack, Freightliner, Kenworth, Peterbilt, International: '
                    u'таблицы, частые сочетания (MID 128, 130, 136, 140, 144), можно ли ехать и что проверить.',
               intro=u'Старые американские и европейские грузовики (и часть Volvo FH и FM до EURO 5) показывают неисправности не парой SPN и FMI, а тройкой '
                     u'<b>MID</b> + <b>PID или SID</b> + <b>FMI</b> по стандарту SAE J1587 (шина J1708). MID — какой блок говорит '
                     u'(128 — двигатель, 130 — коробка, 136 — тормоза и ABS, 140 — приборная панель, 144 — по Volvo ЭБУ автомобиля). '
                     u'PID — параметр (давление, температура, скорость), SID — подсистема (датчик, исполнитель, канал связи). '
                     u'FMI — вид отказа: обрыв, замыкание, значение выше или ниже нормы.',
               how=u'Как читать запись',
               how_p=u'Пример: <b>MID 130 SID 231 FMI 2</b> — блок коробки (130), канал связи SAE J1939 (SID 231), данные прерывистые или неверные (FMI 2). '
                     u'Это не поломка коробки, а запись о нестабильной связи по CAN. Ищите плохой контакт и обрыв в проводах J1939.',
               mid_h=u'MID: какой блок', mid_cols=[u'MID', u'По SAE J1587', u'В таблицах Volvo'],
               sid_h=u'Частые SID по стандарту SAE J1587', sid_cols=[u'SID', u'Название'],
               fmi_h=u'FMI: вид отказа', fmi_cols=[u'FMI', u'Значение по SAE J1587'],
               pages_h=u'Страницы самых частых сочетаний', other_h=u'Другие MID по стандарту',
               other_p=u'Остальные MID (несколько десятков: турбонагнетатель 129, ретардер 173, парковочный отопитель 224 и др.) перечислены в самом стандарте. '
                       u'Страниц на них нет: у разных производителей они отличаются сильнее всего.',
               brands=u'Состав кодов и их подписи отличаются у производителей. Страницы этого раздела опираются на стандарт SAE J1587 и таблицы Volvo '
                      u'(MID 128, 130, 136, 140, 144). У Mack, Freightliner, International, Detroit, Kenworth и Peterbilt основные MID и SID '
                      u'(в том числе SID 231) совпадают с стандартом, но проверяйте код по руководству вашей машины.',
               n=u'%d страниц'),
    'en': dict(h1=u'J1587/J1708 codes: MID, PID, SID, FMI - what they mean',
               title=u'J1587 and J1708 fault codes: MID, PID, SID, FMI explained',
               desc=u'How to read MID, PID, SID and FMI codes on older Volvo, Mack, Freightliner, Kenworth, Peterbilt and International trucks: '
                    u'tables, common combinations (MID 128, 130, 136, 140, 144), whether you can drive and what to check.',
               intro=u'Older American and European trucks (and some Volvo FH and FM before EURO 5) report faults not as an SPN and FMI pair but as a triple '
                     u'<b>MID</b> + <b>PID or SID</b> + <b>FMI</b> under the SAE J1587 standard (J1708 bus). The MID says which unit reports '
                     u'(128 engine, 130 transmission, 136 brakes and ABS, 140 instrument cluster, 144 the vehicle ECU at Volvo). '
                     u'The PID is a parameter (pressure, temperature, speed), the SID a subsystem (a sensor, an actuator, a data link). '
                     u'The FMI is the failure type: open, short, value too high or too low.',
               how=u'How to read an entry',
               how_p=u'Example: <b>MID 130 SID 231 FMI 2</b> - the transmission unit (130), the SAE J1939 data link (SID 231), erratic or intermittent data (FMI 2). '
                     u'It is not a gearbox failure but a record of an unstable CAN link. Look for a poor contact or an open wire in the J1939 harness.',
               mid_h=u'MID: which unit', mid_cols=[u'MID', u'SAE J1587', u'Volvo tables'],
               sid_h=u'Common SIDs in the SAE J1587 standard', sid_cols=[u'SID', u'Name'],
               fmi_h=u'FMI: failure type', fmi_cols=[u'FMI', u'Meaning per SAE J1587'],
               pages_h=u'Pages for the most common combinations', other_h=u'Other MIDs in the standard',
               other_p=u'The other MIDs (several dozen: turbocharger 129, engine retarder 173, parking heater 224 and so on) are listed in the standard itself. '
                       u'There are no pages for them: they differ most between makers.',
               brands=u'Which codes exist and how they are labelled differs between makers. The pages in this section rely on the SAE J1587 standard and Volvo tables '
                      u'(MID 128, 130, 136, 140, 144). On Mack, Freightliner, International, Detroit, Kenworth and Peterbilt the main MIDs and SIDs '
                      u'(including SID 231) match the standard, but check the code against the manual for your truck.',
               n=u'%d pages'),
}

SIDS = [(u'231', u'SAE J1939 Data Link', u'канал связи SAE J1939'), (u'232', u'5 Volts DC Supply', u'питание датчиков 5 В'),
        (u'230', u'Idle Validation Switch', u'выключатель подтверждения холостого хода'), (u'240', u'Program Memory', u'память программы'),
        (u'250', u'SAE J1708 (J1587) Data Link', u'канал SAE J1708 (J1587)'), (u'251', u'Power Supply', u'питание блока'),
        (u'253', u'Calibration Memory', u'память калибровок'), (u'254', u'Controller #1', u'контроллер №1 (блок управления)')]


def j_hub(lang):
    sec = 'j1587'
    lg = L[lang]
    H = HUB_J[lang]
    rel = 'j1587/index.html' if lang == 'ru' else 'en/j1587/index.html'
    pre = _pre(sec, lang)

    def ld(canon):
        return [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': H['h1'], 'description': H['desc'], 'url': canon, 'inLanguage': lang},
                {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [
                    {'@type': 'ListItem', 'position': i + 1, 'url': '%s%s%s.html' % (SITE, pre, p['slug']), 'name': p['title_' + lang]}
                    for i, p in enumerate(jd.PAGES)]}]

    body = [_head(sec, lang, rel, H['title'], H['desc'], H['h1'], ld, None), CSS, u'<div class="nk">', u'<h1>%s</h1>' % esc(H['h1']), _search(lang),
            u'<p class="sub">%s</p>' % (H['n'] % len(jd.PAGES)), u'<p>%s</p>' % H['intro'],
            u'<section><h2>%s</h2><p>%s</p></section>' % (H['how'], H['how_p'])]
    i = 0 if lang == 'ru' else 1
    mrows = [[u'<td class="fmi">%d</td>' % m, (sr if lang == 'ru' else se), (vr if lang == 'ru' else ve)] for m, sr, se, vr, ve in jd.MIDS]
    body.append(u'<section><h2>%s</h2>%s</section>' % (H['mid_h'], _tbl(H['mid_cols'], mrows)))
    srows = [[u'<td class="fmi">%s</td>' % s, (ru if lang == 'ru' else en)] for s, en, ru in SIDS]
    body.append(u'<section><h2>%s</h2>%s</section>' % (H['sid_h'], _tbl(H['sid_cols'], srows)))
    frows = [[u'<td class="fmi">%d</td>' % f, jd.FMI[f][i]] for f in range(15)]
    body.append(u'<section><h2>%s</h2>%s</section>' % (H['fmi_h'], _tbl(H['fmi_cols'], frows)))
    for m, sr, se, vr, ve in jd.MIDS:
        ps = [p for p in jd.PAGES if p['mid'] == m]
        if not ps:
            continue
        body.append(u'<section><h2>MID %d: %s</h2><ul class="near">%s</ul></section>' % (m, esc(vr if lang == 'ru' else ve), u''.join(
            u'<li><a href="%s%s.html"><span class="mono">%s</span><span class="nm">%s</span></a></li>' % (pre, p['slug'], esc(p['label']), esc(p['nm_' + lang])) for p in ps)))
    body.append(u'<section><h2>%s</h2><p>%s</p></section>' % (H['other_h'], esc(H['other_p'])))
    body.append(_src_html(['sae', 'volvo', 'tsi', 'vnl'], jd.SRC, lang))
    body.append(u'<p class="sub">%s</p>' % esc(H['brands']))
    return rel, _foot(lang, body)


# ---------------------------------------------------------------------------------------------------- VAG
def v_page(p, lang):
    sec = 'vag-otopiteli'
    lg = L[lang]
    t = p[lang]
    title = p['title_' + lang]
    rel = ('%s/%s.html' % (CFG[sec]['dir'], p['slug'])) if lang == 'ru' else ('en/%s/%s.html' % (CFG[sec]['dir'], p['slug']))
    desc = t['short']
    if len(desc) > 190:
        desc = desc[:190].rsplit(u' ', 1)[0].rstrip(u',;:—-') + u'.'

    def ld(canon):
        return [{'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': title, 'description': desc,
                 'url': canon, 'inLanguage': lang, 'datePublished': vd.DATE, 'dateModified': vd.DATE,
                 'author': {'@type': 'Organization', 'name': 'codetruck', 'url': SITE + '/'}}, _faq_ld(t['faq'])]

    body = [_head(sec, lang, rel, title, desc, title, ld, title), CSS, u'<div class="nk">', u'<h1>%s</h1>' % esc(title), _search(lang),
            u'<div class="short"><p>%s</p></div>' % esc(t['short'])]
    body.append(u'<section><h2>%s</h2><div class="risk t-%s"><span class="rkb">%s</span><p>%s</p>%s</div></section>' % (
        lg['verdict'], _tier(p['lvl']), esc(t['badge']), esc(t['verdict']),
        (u'<p class="rkn">%s</p>' % esc(t['note'])) if t.get('note') else u''))
    meaning = _tbl([u'Код', u'Название'] if lang == 'ru' else [u'Code', u'Name'],
                   [[u'<td class="fmi">%s</td>' % esc(p['code']), p['nm_' + lang]]])
    meaning += u'<p class="sub">%s</p>' % (u'Блок 18 в VCDS называется Aux. Heat (автономный отопитель).' if lang == 'ru' else u'Address 18 in VCDS is called Aux. Heat (auxiliary heater).')
    body.append(u'<section><h2>%s</h2>%s</section>' % (lg['mean'], meaning))
    body.append(u'<section><h2>%s</h2><ul>%s</ul></section>' % (lg['causes'], u''.join(u'<li>%s</li>' % esc(c) for c in t['causes'])))
    body.append(u'<section><h2>%s</h2><ol>%s</ol></section>' % (lg['checks'], u''.join(u'<li>%s</li>' % esc(c) for c in t['checks'])))
    body.append(u'<section><h2>%s</h2><p>%s</p></section>' % (lg['service'], esc(t['service'])))
    body.append(u'<section><h2>%s</h2>%s</section>' % (lg['faq'], u''.join(
        u'<h3 class="faq-q">%s</h3><p>%s</p>' % (esc(q), esc(a)) for q, a in t['faq'])))
    pre = _pre(sec, lang)
    idx = [q['slug'] for q in vd.PAGES].index(p['slug'])
    near = [vd.PAGES[j] for j in (idx - 1, idx + 1) if 0 <= j < len(vd.PAGES)]
    li = u''.join(u'<li><a href="%s%s.html"><span class="mono">%s</span><span class="nm">%s</span></a></li>' % (
        pre, q['slug'], esc(q['code'].split(u',')[0]), esc(q['nm_' + lang])) for q in near)
    li += u'<li><a href="%s"><span class="nm">%s</span></a></li>' % (pre, lg['hub'])
    body.append(u'<section><h2>%s</h2><ul class="near">%s</ul></section>' % (lg['near'], li))
    body.append(_src_html(p['src'], vd.SRC, lang))
    body.append(u'<p class="sub">%s</p>' % esc(lg['note_vag']))
    return rel, _foot(lang, body)


HUB_V = {
    'ru': dict(h1=u'Ошибки автономных отопителей VAG в VCDS и ODIS',
               title=u'Ошибки отопителя VAG в VCDS: блок 18 Aux. Heat, коды',
               desc=u'Ошибки автономных отопителей Webasto и Eberspächer на VW T5, T6, Crafter, Touareg, Audi, Skoda в VCDS и ODIS (блок 18 Aux. Heat): '
                    u'01406, 01410, 02251 и другие, можно ли ехать и что проверить.',
               intro=u'Если автономный отопитель (Webasto, Eberspächer) поставлен или заложен на заводе в машину концерна VAG, его блок управления виден в '
                     u'VCDS и ODIS как <b>адрес 18, Aux. Heat</b> (иногда 0B, Sec. Air Heating, для воздушного отопителя). Ошибки там записываются '
                     u'пятизначными кодами (0xxxx) или на новых машинах короткими четырёхзначными. Отопитель на управление и тормоза не влияет, '
                     u'поэтому почти всегда ехать можно; задача — понять, чем вызвано, и не оставлять отопитель включённым, если пахнет топливом или идёт дым.',
               cols=[u'Код', u'Что значит', u'Можно ли ехать'],
               n=u'%d страниц', go_calm=u'Ехать можно',
               srcnote=u'Описания составлены по заводским таблицам Audi (A4 8E, A2), Ross-Tech wiki и темам Ross-Tech и t6forum. '
                       u'Дилерские базы не использовались.',
               more=u'Родственные разделы: <a href="/otopiteli/">коды Eberspächer, Webasto и Планар (заводские коды самого отопителя)</a>.'),
    'en': dict(h1=u'Auxiliary heater faults on VAG cars in VCDS and ODIS',
               title=u'VAG heater fault codes in VCDS: address 18 Aux. Heat',
               desc=u'Auxiliary Webasto and Eberspacher heater faults on VW T5, T6, Crafter, Touareg, Audi and Skoda in VCDS and ODIS (address 18 Aux. Heat): '
                    u'01406, 01410, 02251 and others, whether you can drive and what to check.',
               intro=u'If an auxiliary heater (Webasto, Eberspacher) is fitted to a VAG group vehicle, its control unit appears in VCDS and ODIS as '
                     u'<b>address 18, Aux. Heat</b> (sometimes 0B, Sec. Air Heating, for an air heater). Faults are stored as five-digit codes (0xxxx) or, on newer vehicles, short four-digit ones. '
                     u'The heater does not affect steering or brakes, so you can almost always drive; the task is to find the cause and not to leave the heater on if you smell fuel or see smoke.',
               cols=[u'Code', u'What it means', u'Can you drive'],
               n=u'%d pages', go_calm=u'You can drive',
               srcnote=u'The descriptions are based on factory Audi tables (A4 8E, A2), the Ross-Tech wiki and Ross-Tech and t6forum threads. '
                       u'Dealer databases were not used.',
               more=u'Related section: <a href="/en/otopiteli/">Eberspacher, Webasto and Planar heater codes (the heater own factory codes)</a>.'),
}


def v_hub(lang):
    sec = 'vag-otopiteli'
    H = HUB_V[lang]
    rel = 'vag-otopiteli/index.html' if lang == 'ru' else 'en/vag-otopiteli/index.html'
    pre = _pre(sec, lang)

    def ld(canon):
        return [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': H['h1'], 'description': H['desc'], 'url': canon, 'inLanguage': lang},
                {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [
                    {'@type': 'ListItem', 'position': i + 1, 'url': '%s%s%s.html' % (SITE, pre, p['slug']), 'name': p['title_' + lang]}
                    for i, p in enumerate(vd.PAGES)]}]

    body = [_head(sec, lang, rel, H['title'], H['desc'], H['h1'], ld, None), CSS, u'<div class="nk">', u'<h1>%s</h1>' % esc(H['h1']), _search(lang),
            u'<p class="sub">%s</p>' % (H['n'] % len(vd.PAGES)), u'<p>%s</p>' % H['intro']]
    rows = [[u'<td class="fmi"><a href="%s%s.html">%s</a></td>' % (pre, p['slug'], esc(p['code'])), p['nm_' + lang],
             p[lang]['badge']] for p in vd.PAGES]
    body.append(u'<section><h2>%s</h2>%s</section>' % (u'Все коды' if lang == 'ru' else u'All codes', _tbl(H['cols'], rows)))
    body.append(u'<section><p>%s</p></section>' % H['more'])
    body.append(_src_html(['a4', 'a2', 'rt02251', 'rtf', 't6a'], vd.SRC, lang))
    body.append(u'<p class="sub">%s</p>' % esc(H['srcnote']))
    return rel, _foot(lang, body)


def build():
    urls = []
    for lang in ('ru', 'en'):
        for hub, pages, fn in ((j_hub, jd.PAGES, j_page), (v_hub, vd.PAGES, v_page)):
            rel, html = hub(lang)
            _write(rel, html)
            urls.append('%s/%s' % (SITE, rel[:-len('index.html')]))
            for p in pages:
                rel, html = fn(p, lang)
                _write(rel, html)
                urls.append('%s/%s' % (SITE, rel))
    return {'urls': urls}


if __name__ == '__main__':
    print(len(build()['urls']))
