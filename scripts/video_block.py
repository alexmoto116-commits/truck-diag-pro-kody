# -*- coding: utf-8 -*-
"""
Блок «Видеоразбор этого кода» на русских страницах кодов, у которых есть ролик.

Данные: scripts/video_razbory.json, ключ = имя страницы без .html
(spn-97, planar-13, eberspacher-011). Поля: topic (тема в подписи), name,
description, poster (путь от корня сайта; файл лежит в assets/video/), w, h,
vk, vk_embed, youtube, dzen, telegram, uploadDate.

Плеер заранее не грузится: картинка-ссылка. Если задан vk_embed, по нажатию
вставляется iframe ВК-плеера (скрипт и стили попадают на страницу только в этом
случае), иначе ссылка просто открывается в новой вкладке.
Разметка VideoObject — только если есть ролик на Ютубе (embedUrl): без адреса
плеера Google видео на странице не засчитает.
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
.vid .vplay iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
</style>"""

JS = u"""<script>
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.vplay[data-embed]');
if(!a||e.metaKey||e.ctrlKey||e.shiftKey)return;e.preventDefault();var f=document.createElement('iframe');
f.src=a.getAttribute('data-embed');f.allow='autoplay; encrypted-media; fullscreen; picture-in-picture';f.allowFullscreen=true;
f.title=a.getAttribute('data-title')||'Видеоразбор';a.textContent='';a.appendChild(f);a.parentNode.classList.add('on');
a.removeAttribute('href');});
</script>"""


def _yt_id(url):
    m = re.search(r'(?:shorts/|v=|youtu\.be/|embed/)([\w-]{11})', url or '')
    return m.group(1) if m else None


def has(slug):
    return slug in DATA


def block(slug):
    v = DATA.get(slug)
    if not v:
        return u''
    topic = v['topic']
    cap = u'Видеоразбор: %s, 30 с' % topic
    primary = v.get('vk') or v.get('youtube') or v.get('dzen') or v.get('telegram') or TG
    embed = v.get('vk_embed')
    links = []
    for key, name in (('vk', u'ВК'), ('youtube', u'Ютуб'), ('rutube', u'Рутуб'), ('telegram', u'Телеграм'), ('dzen', u'Дзен')):
        if v.get(key):
            links.append(u'<a href="%s" target="_blank" rel="noopener">%s</a>' % (escape(v[key]), name))
    play = (u'<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true">'
            u'<path d="M8.5 5.5v13l10.5-6.5z"/></svg>')
    a_attrs = u'href="%s" target="_blank" rel="noopener"' % escape(primary)
    if embed:
        a_attrs += u' data-embed="%s" data-title="%s"' % (escape(embed), escape(cap))
    out = [u'<section class="vid" id="video">']
    out.append(CSS)
    out.append(u'<h2>Видеоразбор этого кода</h2>')
    out.append(u'<div class="vcard"><a class="vplay" %s aria-label="Смотреть: %s">'
               u'<img src="%s" width="%d" height="%d" loading="lazy" decoding="async" alt="Обложка видеоразбора: %s">'
               u'<span class="vi">%s</span></a>'
               % (a_attrs, escape(cap), escape(v['poster']), v['w'], v['h'], escape(topic), play))
    out.append(u'<div class="vtxt"><p class="vcap">%s</p>' % escape(cap))
    if links:
        out.append(u'<p class="vlinks">Смотреть: %s</p>' % u' · '.join(links))
    out.append(u'<a class="vsub" href="%s" target="_blank" rel="noopener">'
               u'Подписаться в Телеграме — разборы новых кодов</a></div></div>' % TG)
    out.append(u'</section>')
    if embed:
        out.append(JS)
    yid = _yt_id(v.get('youtube'))
    if yid:
        ld = {'@context': 'https://schema.org', '@type': 'VideoObject',
              'name': v['name'], 'description': v['description'],
              'thumbnailUrl': [SITE + v['poster']], 'uploadDate': v['uploadDate'],
              'embedUrl': 'https://www.youtube.com/embed/' + yid,
              'inLanguage': 'ru'}
        out.append(u'<script type="application/ld+json">%s</script>'
                   % json.dumps(ld, ensure_ascii=False).replace('</', '<' + chr(92) + '/'))
    return u''.join(out)
