# -*- coding: utf-8 -*-
"""
Соцсети сайта: единый список scripts/socials.json -> разметка шапки и подвала
русских страниц, sameAs и блоки в корневом index.html.

Подключается из build_pages.py (HEAD и подвал), а сам запускается как
    python -X utf8 -I scripts/socials.py
и подставляет блоки между маркерами <!--soc:...--> в index.html
(build_lang_pages.py вызывает это сам и вырезает блоки из языковых главных).
Иностранные версии соцсетей не показывают: ролики русские.
"""
import io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Значки 24x24, контур currentColor. Имя = поле icon в socials.json.
ICONS = {
    'telegram': '<path d="M21 4.2 3.2 11.1c-.7.3-.7.8 0 1l4.5 1.4 1.7 5.3c.2.5.4.6.8.2l2.4-2 4.6 3.4c.8.5 1.4.2 1.6-.8L22.2 5.3c.3-1.2-.4-1.7-1.2-1.1Z"/><path d="m8 13.4 9.6-7.2"/>',
    'vk': '<rect x="2.5" y="2.5" width="19" height="19" rx="5"/><path d="m6.8 9 2.1 6.2L11 9M14.2 9v6.2M18 9l-3.4 3.2 3.6 3"/>',
    'dzen': '<circle cx="12" cy="12" r="9.2"/><path d="M12 5.2c0 3.8-3 6.8-6.8 6.8 3.8 0 6.8 3 6.8 6.8 0-3.8 3-6.8 6.8-6.8-3.8 0-6.8-3-6.8-6.8Z"/>',
    'youtube': '<rect x="2.3" y="5.8" width="19.4" height="12.4" rx="3.6"/><path d="M10.2 9.4v5.2l4.5-2.6Z"/>',
    'rutube': '<rect x="2.5" y="2.5" width="19" height="19" rx="5"/><path d="M8 17V7.5h5a2.6 2.6 0 0 1 0 5.2H8M13 12.7l3 4.3"/>',
    'tiktok': '<path d="M14 3v11.2a3.6 3.6 0 1 1-3.6-3.6M14 3c.3 2.4 1.9 4 4.4 4.2"/>',
}


def load():
    d = json.loads(io.open(os.path.join(HERE, 'socials.json'), encoding='utf-8').read())
    return d['socials']


def shown():
    return [s for s in load() if s.get('show') and s.get('url')]


def svg(s):
    return ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % ICONS[s['icon']])


def top_html():
    """Значки в шапке (только значки, подпись — в aria-label)."""
    a = ''.join('<a href="%s" target="_blank" rel="noopener" aria-label="%s" title="%s" '
                'style="--c:%s">%s</a>' % (s['url'], s['label'], s['name'], s['color'], svg(s))
                for s in shown())
    return '<span class="soc" role="group" aria-label="Мы в соцсетях">%s</span>' % a


def foot_html():
    """Строка «Мы в соцсетях:» внизу страницы: значок + название."""
    a = ' '.join('<a href="%s" target="_blank" rel="noopener" style="--c:%s">%s<span>%s</span></a>'
                 % (s['url'], s['color'], svg(s), s['name']) for s in shown())
    return '<p class="socf"><b>Мы в соцсетях:</b> %s</p>' % a


CSS = u"""
.soc{display:inline-flex;align-items:center;gap:2px;margin-left:auto}
.tick .soc a{display:inline-flex;align-items:center;justify-content:center;width:36px;height:44px;border:0;padding:0;margin:0;color:#6F7E90;border-radius:8px;transition:color .15s}
.tick .soc a:first-child{margin:0;padding:0;font-size:inherit;animation:none;background:none;border-radius:8px;color:#6F7E90}
.tick .soc a:hover,.tick .soc a:focus-visible{color:var(--c)}
.tick .soc a:focus-visible{outline:2px solid var(--c);outline-offset:-2px}
.tick .soc svg{display:block}
.tick{display:flex;flex-wrap:wrap;align-items:center}
.tick .crumbs{display:inline-flex;flex-wrap:wrap;align-items:center}
@media (max-width:480px){.tick .soc a{width:30px}.soc{gap:0}}
.socf{margin:14px 0 0;font-size:13.5px;color:#94A2B4;display:flex;flex-wrap:wrap;align-items:center;gap:4px 16px}
.socf b{font-weight:600;color:#94A2B4}
.socf a{display:inline-flex;align-items:center;gap:6px;min-height:36px;color:#94A2B4;text-decoration:none}
.socf a:hover,.socf a:focus-visible{color:var(--c)}
"""


def same_as():
    return [s['url'] for s in load() if s.get('url')]


# ---- корневой index.html ----
TOP_RE = re.compile(r'<!--soc:top-->.*?<!--/soc:top-->', re.S)
FOOT_RE = re.compile(r'<!--soc:foot-->.*?<!--/soc:foot-->', re.S)
LD_RE = re.compile(r'<!--soc:ld-->.*?<!--/soc:ld-->', re.S)
CSS_RE = re.compile(r'/\*soc:css\*/.*?/\*/soc:css\*/', re.S)

INDEX_CSS = u"""
/*soc:css*/
.soc-top{position:absolute;top:clamp(14px,2.5vw,22px);left:50%;transform:translateX(-50%);z-index:19;display:flex;align-items:center;min-height:44px}
.soc-top .soc{display:inline-flex;align-items:center;margin:0;gap:0;background:rgba(12,19,28,.5);border-radius:12px;padding:0 4px;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.soc-top .soc a,.socf a{color:var(--ink-3);text-decoration:none;transition:color .15s}
.soc-top .soc a{display:inline-flex;align-items:center;justify-content:center;width:38px;height:44px}
.soc-top .soc a:hover,.soc-top .soc a:focus-visible,.socf a:hover,.socf a:focus-visible{color:var(--c)}
.socf{margin:0 0 14px;display:flex;flex-wrap:wrap;align-items:center;gap:4px 16px}
.socf b{font-weight:600}
.socf a{display:inline-flex;align-items:center;gap:6px;min-height:36px}
@media(max-width:560px){.soc-top .soc a{width:32px}.soc-top .soc{padding:0 2px}}
@media(max-width:400px){.soc-top .soc a{width:28px}}
[data-theme="light"] .soc-top .soc{background:rgba(255,255,255,.6)}
@media print{.soc-top{display:none}}
/*/soc:css*/
"""


def index_ld():
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "codetruck.ru",
           "url": "https://codetruck.ru/", "logo": "https://codetruck.ru/assets/favicon.svg",
           "sameAs": same_as()}
    return ('<!--soc:ld--><script type="application/ld+json">%s</script><!--/soc:ld-->'
            % json.dumps(org, ensure_ascii=False, separators=(',', ':')))


def sync_index(html):
    """Подставляет блоки соцсетей в русский index.html (идемпотентно)."""
    def one(rx, new, where, text):
        t, n = rx.subn(lambda m: new, text, count=1)
        if n != 1:
            raise ValueError(u'index.html: нет маркера %s (см. scripts/socials.py)' % where)
        return t
    html = one(TOP_RE, u'<!--soc:top--><div class="soc-top">%s</div><!--/soc:top-->' % top_html(), 'soc:top', html)
    html = one(FOOT_RE, u'<!--soc:foot-->%s<!--/soc:foot-->' % foot_html(), 'soc:foot', html)
    html = one(LD_RE, index_ld(), 'soc:ld', html)
    html = one(CSS_RE, INDEX_CSS.strip(), 'soc:css', html)
    return html


def strip_index(html):
    """Для языковых главных: вырезает блоки соцсетей (ролики русские)."""
    nl = chr(10)
    for rx in (TOP_RE, FOOT_RE, LD_RE, CSS_RE):
        html = rx.sub('', html)
    # пустые строки, оставшиеся на месте блоков
    html = html.replace('</script>' + nl + nl + '<style>', '</script>' + nl + '<style>')
    html = html.replace('<body>' + nl + nl, '<body>' + nl)
    html = html.replace('opacity:1}' + nl + nl + '</style>', 'opacity:1}' + nl + '</style>')
    return html


if __name__ == '__main__':
    p = os.path.join(ROOT, 'index.html')
    old = io.open(p, encoding='utf-8').read()
    new = sync_index(old)
    if new != old:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(new)
        print(u'index.html: соцсети обновлены')
    else:
        print(u'index.html: без изменений')
