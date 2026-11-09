# -*- coding: utf-8 -*-
"""
Раздел «Разборы» (09.11.2026): список статей и ссылки «Подробный разбор» со страниц кодов.

Тексты - razbory_ru.py и razbory_en.py (ключ = slug). Здесь - порядок, группы, ролик по теме
(ключ из video_razbory.json; берётся первый из списка, который там есть) и страницы кодов,
на которых ставится ссылка «Подробный разбор» (пути без /en/, как у русской версии).
Страницы статей: /razbory/<slug>.html и /en/razbory/<slug>.html, оглавление - /razbory/ и /en/razbory/.
Как добавить статью: _мозг/дело/razbory.md.
"""
from html import escape

DATE = '2026-11-09'

# (группа ru, группа en) - порядок групп на оглавлении
GROUPS = [
    ('engine', u'Двигатель и топливо', u'Engine and fuel'),
    ('exhaust', u'Выхлоп: сажевый фильтр и мочевина', u'Exhaust: particulate filter and urea'),
    ('heaters', u'Автономные отопители', u'Parking heaters'),
]

ARTICLES = [
    dict(slug='kamaz-spn-97-voda-v-toplive', group='engine', video=['spn-97'], pages=['kody/spn-97.html']),
    dict(slug='spn-100-davlenie-masla', group='engine', video=['spn-100'], pages=['kody/spn-100.html']),
    dict(slug='spn-110-peregrev', group='engine', video=['spn-110'], pages=['kody/spn-110.html']),
    dict(slug='spn-102-davlenie-nadduva', group='engine', video=['spn-102'], pages=['kody/spn-102.html']),
    dict(slug='mercedes-actros-spn-107', group='engine', video=['spn-107'], pages=['kody/spn-107.html']),
    dict(slug='sazhevyy-filtr-dpf', group='exhaust', video=['spn-3719'], pages=['kody/spn-3251.html']),
    dict(slug='spn-1761-mochevina-adblue', group='exhaust', video=['spn-1761'], pages=['kody/spn-1761.html']),
    dict(slug='eberspacher-011', group='heaters', video=['eberspacher-011'],
         pages=['otopiteli/eberspacher-011.html']),
    dict(slug='planar-kod-13-i-miganiya-pu5', group='heaters', video=['planar-13'],
         pages=['otopiteli/planar-13.html', 'otopiteli/planar-2.html', 'otopiteli/planar-4.html',
                'otopiteli/planar-6.html']),
    dict(slug='planar-kod-29-sryv-plameni', group='heaters', video=['planar-29'],
         pages=['otopiteli/planar-29.html', 'otopiteli/planar-78.html']),
    dict(slug='webasto-f-kody-i-sluzhebnye-kody', group='heaters', video=['webasto-dlinny', 'webasto-f01'],
         pages=['otopiteli/webasto-f%02d.html' % n for n in range(0, 16)]),
    dict(slug='webasto-f03', group='heaters', video=['webasto-f03'], pages=['otopiteli/webasto-f03.html']),
    dict(slug='webasto-f10', group='heaters', video=['webasto-f10'], pages=['otopiteli/webasto-f10.html']),
]

BY_SLUG = dict((a['slug'], a) for a in ARTICLES)


def texts(lang):
    if lang == 'ru':
        import razbory_ru as m
    else:
        import razbory_en as m
    return m.A


def page_rel(slug, lang='ru'):
    return ('razbory/%s.html' if lang == 'ru' else 'en/razbory/%s.html') % slug


def back_link(rel, lang='ru'):
    """Блок «Подробный разбор» для страницы кода rel (путь вида kody/spn-97.html, без /en/)."""
    arts = [a for a in ARTICLES if rel in a['pages']]
    if not arts:
        return u''
    T = texts(lang)
    h2 = u'Подробный разбор' if lang == 'ru' else u'Detailed breakdown'
    items = u''.join(u'<li><a href="/%s">%s</a></li>' % (page_rel(a['slug'], lang), escape(T[a['slug']]['h1']))
                     for a in arts)
    return (u'<section class="razb"><h2>%s</h2><ul class="lines">%s</ul></section>' % (h2, items))
