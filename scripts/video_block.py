# -*- coding: utf-8 -*-
"""
Блок «Видеоразбор этого кода» на страницах кодов и отопителей (ru и en), у которых есть ролик.

Данные: scripts/video_razbory.json, ключ = имя страницы без .html
(spn-97, planar-13, eberspacher-011). Поля: topic (тема в подписи), duration (секунды),
poster (путь от корня сайта; файл лежит в assets/video/), w, h,
vk, vk_embed, youtube, dzen, telegram, youtube_id, name, uploadDate.
Тексты роликов - scripts/video_texts.py (TEXTS[ключ] = {'ru', 'en', 'topic_en', 'name_en', ...}).

Плеер заранее не грузится: обложка с кнопкой. Если задан youtube_id, по нажатию
вставляется iframe youtube-nocookie (31.10.2026); иначе, если задан vk_embed, -
плеер ВК; иначе ссылка просто открывается в новой вкладке. Скрипт попадает на
страницу только когда есть встраиваемый плеер.
Под плеером (09.11.2026) стоит «Текст ролика» - озвучка в читаемом виде; на en-страницах
перевод и пометка, что ролик на русском.
Разметка VideoObject (JSON-LD) ставится, когда есть youtube_id, name и uploadDate:
поля name, uploadDate (с поясом), duration берутся со страницы ролика на Ютубе
и лежат в video_razbory.json. thumbnailUrl - своя обложка (постоянный адрес).
"""
import io, json, os, re
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://codetruck.ru'
TG = 'https://t.me/codetruck'

try:
    DATA = json.loads(io.open(os.path.join(HERE, 'video_razbory.json'), encoding='utf-8').read())
except IOError:
    DATA = {}

try:
    import video_texts as _T
    TEXTS = _T.TEXTS
except ImportError:
    TEXTS = {}

CSS = u"""<style>
.vid .vcard{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}
.vid .vplay{position:relative;display:block;flex:none;width:150px;aspect-ratio:9/16;border-radius:12px;overflow:hidden;background:#0C131C;border:1px solid rgba(255,255,255,.13)}
.vid .vplay img{display:block;width:100%;height:100%;object-fit:cover}
.vid .vplay .vi{position:absolute;left:50%;top:50%;width:48px;height:48px;margin:-24px 0 0 -24px;border-radius:50%;background:rgba(5,7,10,.7);border:1.5px solid #6FE3D3;display:flex;align-items:center;justify-content:center;color:#6FE3D3;transition:transform .15s,background .15s}
.vid .vplay:hover .vi,.vid .vplay:focus-visible .vi{transform:scale(1.08);background:rgba(5,7,10,.85)}
.vid .vplay:focus-visible{outline:2px solid #6FE3D3;outline-offset:2px}
.vid .vtxt{flex:1 1 220px;min-width:0}
.vid .vcap{margin:0 0 10px;font-size:15px;line-height:1.5;color:#CBD7E3}
.vid .vlinks{margin:0 0 14px;font-size:13.5px;color:#94A2B4}
.vid .vlinks a{display:inline-block;padding:7px 2px}
.vid .vsub{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:10px;border:1px solid rgba(111,227,211,.45);text-decoration:none;font-size:14px;font-weight:600;line-height:1.3}
.vid .vsub:hover{background:rgba(111,227,211,.1)}
.vid .vcard.on .vplay{width:min(100%,360px);flex-basis:100%}
.vid .vplay.land{width:min(100%,360px);aspect-ratio:16/9;flex-basis:100%}
.vid .vtext{margin:16px 0 0;max-width:68ch}
.vid .vtext h3{margin:0 0 8px;font-size:16px}
.vid .vtext p{margin:0 0 10px;font-size:15px;line-height:1.6;color:#CBD7E3}
.vid .vtext .vnote{font-size:13.5px;color:#94A2B4}
.vid .vplay iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
</style>"""

JS = u"""<script>
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.vplay[data-embed]');
if(!a||e.metaKey||e.ctrlKey||e.shiftKey)return;e.preventDefault();var f=document.createElement('iframe');
f.src=a.getAttribute('data-embed');f.setAttribute('referrerpolicy','strict-origin-when-cross-origin');f.allow='autoplay; encrypted-media; fullscreen; picture-in-picture';f.allowFullscreen=true;
f.title=a.getAttribute('data-title')||'Видеоразбор';a.textContent='';a.appendChild(f);a.parentNode.classList.add('on');
a.removeAttribute('href');});
</script>"""


def _yt_id(url):
    m = re.search(r'(?:shorts/|v=|youtu\.be/|embed/)([\w-]{11})', url or '')
    return m.group(1) if m else None


def _iso_dur(sec):
    sec = int(sec)
    return 'PT%dM%dS' % (sec // 60, sec % 60)


def _excerpt(text, limit=300):
    """Начало текста до границы предложения (для description в разметке)."""
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    k = max(cut.rfind('. '), cut.rfind('! '), cut.rfind('? '))
    return cut[:k + 1] if k > 80 else cut.rsplit(' ', 1)[0] + u'…'


def _dur_text(sec, lang):
    sec = int(sec)
    if sec >= 120:
        return (u'%d мин %d с' % (sec // 60, sec % 60)) if lang == 'ru' else (u'%d min %d s' % (sec // 60, sec % 60))
    return (u'%d с' % sec) if lang == 'ru' else (u'%d s' % sec)


def _txt(slug, lang):
    return (TEXTS.get(slug) or {}).get(lang) or u''


def ld(slug, lang='ru'):
    """JSON-LD VideoObject или пустая строка, если данных не хватает."""
    v = DATA.get(slug)
    if not v or not v.get('youtube_id') or not v.get('name') or not v.get('uploadDate'):
        return u''
    t = TEXTS.get(slug) or {}
    text = _txt(slug, lang)
    if lang == 'ru':
        name = v['name']
        desc = _excerpt(text) if text else u'Видеоразбор: %s. Что означает код, можно ли ехать и что проверить.' % v['topic']
    else:
        name = t.get('name_en') or v['name']
        desc = _excerpt(text) if text else u'Video breakdown (in Russian): %s.' % (t.get('topic_en') or v['topic'])
    obj = {'@context': 'https://schema.org', '@type': 'VideoObject',
           'name': name,
           'description': desc,
           'thumbnailUrl': [SITE + v['poster']],
           'uploadDate': v['uploadDate'],
           'embedUrl': 'https://www.youtube.com/embed/' + v['youtube_id'],
           'inLanguage': 'ru'}
    if text:
        obj['transcript'] = text.replace(u'\n\n', u' ')
    if v.get('duration'):
        obj['duration'] = _iso_dur(v['duration'])
    return u'<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False)


def has(slug):
    return slug in DATA


L = {
    'ru': {'h2': u'Видеоразбор этого кода', 'cap': u'Видеоразбор: %s, %s', 'watch': u'Смотреть: ',
           'alt': u'Обложка видеоразбора: %s', 'aria': u'Смотреть: %s',
           'sub': u'Подписаться в Телеграме — разборы новых кодов',
           'links': ((u'vk', u'ВК'), (u'youtube', u'Ютуб'), (u'rutube', u'Рутуб'), (u'telegram', u'Телеграм'), (u'dzen', u'Дзен')),
           'th': u'Текст ролика', 'note': u''},
    'en': {'h2': u'Video breakdown of this code', 'cap': u'Video breakdown (in Russian): %s, %s', 'watch': u'Watch: ',
           'alt': u'Cover of the video breakdown: %s', 'aria': u'Watch: %s',
           'sub': u'Follow on Telegram — breakdowns of new codes',
           'links': ((u'vk', u'VK'), (u'youtube', u'YouTube'), (u'rutube', u'Rutube'), (u'telegram', u'Telegram'), (u'dzen', u'Dzen')),
           'th': u'Text of the video', 'note': u'The video is in Russian; below is an English translation of the narration.'},
}


def block(slug, lang='ru'):
    v = DATA.get(slug)
    if not v:
        return u''
    lg = L[lang]
    t = TEXTS.get(slug) or {}
    topic = v['topic'] if lang == 'ru' else (t.get('topic_en') or v['topic'])
    cap = lg['cap'] % (topic, _dur_text(v['duration'], lang))
    primary = v.get('vk') or v.get('youtube') or v.get('dzen') or v.get('telegram') or TG
    yt = v.get('youtube_id')
    embed = ('https://www.youtube-nocookie.com/embed/%s?autoplay=1&rel=0&playsinline=1' % yt) if yt else v.get('vk_embed')
    if yt:
        primary = v.get('youtube') or primary
    links = []
    for key, name in lg['links']:
        if v.get(key):
            links.append(u'<a href="%s" target="_blank" rel="noopener">%s</a>' % (escape(v[key]), name))
    play = (u'<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true">'
            u'<path d="M8.5 5.5v13l10.5-6.5z"/></svg>')
    a_attrs = u'href="%s" target="_blank" rel="noopener"' % escape(primary)
    if embed:
        a_attrs += u' data-embed="%s" data-title="%s"' % (escape(embed), escape(cap))
    h2 = (t.get('h2_en') if lang == 'en' else t.get('h2')) or lg['h2']
    cls = u'vplay land' if v['w'] > v['h'] else u'vplay'
    out = [u'<section class="vid" id="video">']
    out.append(CSS)
    out.append(u'<h2>%s</h2>' % escape(h2))
    out.append(u'<div class="vcard"><a class="%s" %s aria-label="%s">'
               u'<img src="%s" width="%d" height="%d" loading="lazy" decoding="async" alt="%s">'
               u'<span class="vi">%s</span></a>'
               % (cls, a_attrs, escape(lg['aria'] % cap), escape(v['poster']), v['w'], v['h'],
                  escape(lg['alt'] % topic), play))
    out.append(u'<div class="vtxt"><p class="vcap">%s</p>' % escape(cap))
    if links:
        out.append(u'<p class="vlinks">%s%s</p>' % (lg['watch'], u' · '.join(links)))
    out.append(u'<a class="vsub" href="%s" target="_blank" rel="noopener">%s</a></div></div>' % (TG, lg['sub']))
    text = _txt(slug, lang)
    if text:
        out.append(u'<div class="vtext"><h3>%s</h3>' % lg['th'])
        if lg['note']:
            out.append(u'<p class="vnote">%s</p>' % escape(lg['note']))
        for para in text.split(u'\n\n'):
            out.append(u'<p>%s</p>' % escape(para.strip()))
        out.append(u'</div>')
    out.append(u'</section>')
    if embed:
        out.append(JS)
    out.append(ld(slug, lang))
    return u''.join(out)
