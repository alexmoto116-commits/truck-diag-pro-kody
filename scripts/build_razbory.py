# -*- coding: utf-8 -*-
"""
Раздел «Разборы»: оглавление /razbory/ и /en/razbory/ и страница на каждую статью
(razbory_data.ARTICLES, тексты - razbory_ru.py / razbory_en.py). Вызывается из build_pages.build()
рядом с отопителями; отдаёт адреса для карт сайта.
"""
import io, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp                                    # noqa: E402
import razbory_data as rd                                   # noqa: E402
import video_block                                          # noqa: E402

SITE = bp.SITE
X = bp._xt

CSS = (u'<style>.art p,.art li{color:#CBD7E3;font-size:15.5px;line-height:1.65}'
       u'.art ul,.art ol{margin:0 0 14px;padding-left:22px}.art p{margin:0 0 12px;max-width:68ch}'
       u'.art table{margin:0 0 18px}.art td,.art th{overflow-wrap:anywhere}'
       u'.art td:first-child{font-weight:600;color:#EAF0F7}.art h3.faq-q{font-size:1em;font-weight:700;margin:14px 0 4px}'
       u'.art .short{border:1px solid rgba(111,227,211,.3);border-radius:12px;background:rgba(111,227,211,.05);'
       u'padding:12px 16px;margin:0 0 26px}.art .short p{margin:0}.art .gt{margin:26px 0 10px;font-size:17px}'
       u'.razb ul{margin:0}</style>')

L = {
    'ru': dict(home=u'Главная', sec=u'Разборы', faq=u'Вопросы и ответы', more=u'Страницы кодов на сайте',
               all=u'Все разборы', short=u'Коротко', src=u'Сверено по заводским руководствам и таблицам '
               u'производителей; факты те же, что в наших роликах и статьях. Решение о поездке остаётся за водителем.',
               hub_h1=u'Разборы кодов и неисправностей',
               hub_title=u'Разборы кодов и неисправностей грузовиков и отопителей',
               hub_desc=u'Подробные разборы: что значит код, можно ли ехать, что проверить самому и когда '
                        u'нужен сервис. Коды двигателей, сажевого фильтра, мочевины и отопителей Webasto, '
                        u'Eberspächer, Планар.',
               hub_sub=u'Длинные статьи по одному коду или одной теме: таблица расшифровки, порядок проверки, '
                       u'вопросы и ответы и ролик, если он есть. Каждый разбор ведёт на страницы кодов сайта.',
               n=u'%d разборов', cta=u'Не нашли свой код? <a href="/">Введите его в поиск</a> — или вставьте сразу весь '
                                     u'список со сканера, покажем, какая поломка настоящая.'),
    'en': dict(home=u'Home', sec=u'Breakdowns', faq=u'Questions and answers', more=u'Code pages on the site',
               all=u'All breakdowns', short=u'In short', src=u'Checked against manufacturer manuals and '
               u'tables; the same facts as in our videos and articles. The decision to drive remains with the driver.',
               hub_h1=u'Code and fault breakdowns',
               hub_title=u'Truck and heater code breakdowns - what it means, what to check',
               hub_desc=u'Detailed breakdowns: what a code means, whether you can drive, what to check yourself and '
                        u'when a workshop is needed. Engine, particulate filter, urea and Webasto, Eberspächer, '
                        u'Planar heater codes.',
               hub_sub=u'Long articles on one code or one topic: a decoding table, the order of checks, questions '
                       u'and answers and a video where there is one. Each breakdown links to the code pages of the site.',
               n=u'%d breakdowns', cta=u'Cannot find your code? <a href="/en/">Type it into the search</a> — or paste the '
                                       u'whole list from the scanner and we will show which fault is the real one.'),
}


def _write(rel, html):
    full = os.path.join(bp.ROOT, rel.replace('/', os.sep))
    d = os.path.dirname(full)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(full, 'w', encoding='utf-8').write(html)


def _nav(lang, here=None):
    lg = L[lang]
    if lang == 'ru':
        return bp.nav_of('razbory', here)
    items = [u'<a href="/en/">%s</a>' % lg['home']]
    if here:
        items.append(u'<a href="/en/razbory/">%s</a>' % lg['sec'])
        items.append(u'<span>%s</span>' % bp.esc(here))
    else:
        items.append(u'<span>%s</span>' % lg['sec'])
    return u'<span class="sep">&rsaquo;</span>'.join(items)


def _crumb_ld(lang, here, canon):
    lg = L[lang]
    base = SITE + ('/' if lang == 'ru' else '/en/')
    items = [{'@type': 'ListItem', 'position': 1, 'name': lg['home'], 'item': base},
             {'@type': 'ListItem', 'position': 2, 'name': lg['sec'], 'item': base + 'razbory/'}]
    if here:
        items.append({'@type': 'ListItem', 'position': 3, 'name': here, 'item': canon})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}


def _search(lang):
    if lang == 'ru':
        return bp.search_form(None)
    return bp.search_form(None, ph=u'Your code, e.g. 1078/3', action=u'/en/', btn=u'Search', label=u'Fault code')


def _head(lang, rel, title, desc, h1, ld, here):
    pub = rel[:-len('index.html')] if rel.endswith('index.html') else rel
    canon = '%s/%s' % (SITE, pub)
    ru_rel = pub if lang == 'ru' else pub[len('en/'):]
    ld_all = u''.join(bp.ld_script(o) for o in ld(canon)) + bp.ld_script(_crumb_ld(lang, here, canon))
    head = bp.HEAD.format(title=bp.esc(title), desc=bp.esc(desc), canon=canon, ogtitle=bp.esc(h1),
                          mid=bp.METRIKA_ID, ld=ld_all, nav=_nav(lang, here), lang=lang,
                          locale='ru_RU' if lang == 'ru' else 'en_US', alt=bp.alt_links(True, ru_rel))
    return head, canon


def _blocks(items):
    out = []
    for it in items:
        if isinstance(it, tuple) and it[0] == 'tbl':
            _, hdr, rows = it
            out.append(u'<table><tr>%s</tr>%s</table>' % (
                u''.join(u'<th>%s</th>' % X(h) for h in hdr),
                u''.join(u'<tr>%s</tr>' % u''.join(u'<td>%s</td>' % X(c) for c in r) for r in rows)))
        elif isinstance(it, tuple) and it[0] == 'ol':
            out.append(u'<ol>%s</ol>' % u''.join(u'<li>%s</li>' % X(x) for x in it[1]))
        elif isinstance(it, list):
            out.append(u'<ul>%s</ul>' % u''.join(u'<li>%s</li>' % X(x) for x in it))
        else:
            out.append(u'<p>%s</p>' % X(it))
    return u''.join(out)


def _video(art, lang):
    for k in art['video']:
        if video_block.has(k):
            return video_block.block(k, lang)
    return u''


def article_page(art, lang):
    slug = art['slug']
    t = rd.texts(lang)[slug]
    lg = L[lang]
    rel = rd.page_rel(slug, lang)

    def ld(canon):
        article = {'@context': 'https://schema.org', '@type': 'Article', 'headline': t['h1'],
                   'description': t['desc'], 'inLanguage': lang, 'datePublished': rd.DATE,
                   'dateModified': rd.DATE, 'image': SITE + '/assets/og.png',
                   'mainEntityOfPage': canon,
                   'author': {'@type': 'Organization', 'name': 'codetruck', 'url': SITE + '/'},
                   'publisher': {'@type': 'Organization', 'name': 'codetruck', 'url': SITE + '/'}}
        faq = {'@context': 'https://schema.org', '@type': 'FAQPage',
               'mainEntity': [{'@type': 'Question', 'name': q,
                               'acceptedAnswer': {'@type': 'Answer', 'text': bp._BOLD.sub(r'\1', bp._LINK_TOKEN.sub(r'\2', a))}}
                              for q, a in t['faq']]}
        return [article, faq]

    head, canon = _head(lang, rel, t['title'], t['desc'], t['h1'], ld, t['h1'])
    body = [head, CSS, u'<div class="art">', u'<h1>%s</h1>' % bp.esc(t['h1']), _search(lang),
            u'<div class="short"><p><b>%s.</b> %s</p></div>' % (lg['short'], bp.esc(t['short']))]
    body.append(_video(art, lang))
    for h2, items in t['body']:
        body.append(u'<section><h2>%s</h2>%s</section>' % (bp.esc(h2), _blocks(items)))
    body.append(u'<section><h2>%s</h2>%s</section>' % (lg['faq'], u''.join(
        u'<h3 class="faq-q">%s</h3><p>%s</p>' % (bp.esc(q), X(a)) for q, a in t['faq'])))
    body.append(u'<section><h2>%s</h2><ul class="lines">%s</ul></section>' % (lg['more'], u''.join(
        u'<li><a href="%s">%s</a></li>' % (bp.esc(h), bp.esc(txt)) for h, txt in t['more'])))
    body.append(u'<p class="sub">%s</p>' % bp.esc(lg['src']))
    body.append(u'<p><a href="%s">&larr; %s</a></p>' % ('/razbory/' if lang == 'ru' else '/en/razbory/', lg['all']))
    body.append(u'</div>')
    body.append(u'<p class="cta">%s</p>' % lg['cta'])
    body.append(bp.soc_foot(lang))
    body.append(u'</div>\n' + bp.CF_SNIPPET + u'\n</body>\n</html>\n')
    return rel, u''.join(body)


def hub_page(lang):
    lg = L[lang]
    T = rd.texts(lang)
    rel = 'razbory/index.html' if lang == 'ru' else 'en/razbory/index.html'
    pre = '/razbory/' if lang == 'ru' else '/en/razbory/'

    def ld(canon):
        return [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': lg['hub_h1'],
                 'description': lg['hub_desc'], 'url': canon, 'inLanguage': lang},
                {'@context': 'https://schema.org', '@type': 'ItemList',
                 'itemListElement': [{'@type': 'ListItem', 'position': i + 1,
                                      'url': '%s%s%s.html' % (SITE, pre, a['slug']), 'name': T[a['slug']]['h1']}
                                     for i, a in enumerate(rd.ARTICLES)]}]

    head, canon = _head(lang, rel, lg['hub_title'], lg['hub_desc'], lg['hub_h1'], ld, None)
    body = [head, CSS, u'<div class="art">', u'<h1>%s</h1>' % bp.esc(lg['hub_h1']), _search(lang),
            u'<p class="sub">%s %s</p>' % (bp.esc(lg['hub_sub']), lg['n'] % len(rd.ARTICLES))]
    for key, g_ru, g_en in rd.GROUPS:
        arts = [a for a in rd.ARTICLES if a['group'] == key]
        body.append(u'<section><h2>%s</h2><ul class="lines">%s</ul></section>' % (
            g_ru if lang == 'ru' else g_en,
            u''.join(u'<li><a href="%s%s.html"><b>%s</b></a><br><span>%s</span></li>' % (
                pre, a['slug'], bp.esc(T[a['slug']]['h1']), bp.esc(T[a['slug']]['short'])) for a in arts)))
    body.append(u'</div>')
    body.append(u'<p class="cta">%s</p>' % lg['cta'])
    body.append(bp.soc_foot(lang))
    body.append(u'</div>\n' + bp.CF_SNIPPET + u'\n</body>\n</html>\n')
    return rel, u''.join(body)


def build():
    urls = []
    for lang in bp.LANGS_ON:   # en - только при CODETRUCK_EN=1
        rel, html = hub_page(lang)
        _write(rel, html)
        urls.append('%s/%s' % (SITE, rel[:-len('index.html')]))
        for art in rd.ARTICLES:
            rel, html = article_page(art, lang)
            _write(rel, html)
            urls.append('%s/%s' % (SITE, rel))
    return {'urls': urls}


if __name__ == '__main__':
    print(len(build()['urls']))
