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

# Значки 24x24, заливка currentColor. Telegram, VK, YouTube — пути из Simple Icons
# (simple-icons@16.0.0, CC0; cdn.jsdelivr.net/npm/simple-icons@16.0.0/icons/<имя>.svg).
# Дзена и Рутуба в Simple Icons нет — свои знаки в том же стиле (заливка, вырез).
# Имя = поле icon в socials.json.
ICONS = {
    'telegram': '<path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>',
    'vk': '<path d="m9.489.004.729-.003h3.564l.73.003.914.01.433.007.418.011.403.014.388.016.374.021.36.025.345.03.333.033c1.74.196 2.933.616 3.833 1.516.9.9 1.32 2.092 1.516 3.833l.034.333.029.346.025.36.02.373.025.588.012.41.013.644.009.915.004.98-.001 3.313-.003.73-.01.914-.007.433-.011.418-.014.403-.016.388-.021.374-.025.36-.03.345-.033.333c-.196 1.74-.616 2.933-1.516 3.833-.9.9-2.092 1.32-3.833 1.516l-.333.034-.346.029-.36.025-.373.02-.588.025-.41.012-.644.013-.915.009-.98.004-3.313-.001-.73-.003-.914-.01-.433-.007-.418-.011-.403-.014-.388-.016-.374-.021-.36-.025-.345-.03-.333-.033c-1.74-.196-2.933-.616-3.833-1.516-.9-.9-1.32-2.092-1.516-3.833l-.034-.333-.029-.346-.025-.36-.02-.373-.025-.588-.012-.41-.013-.644-.009-.915-.004-.98.001-3.313.003-.73.01-.914.007-.433.011-.418.014-.403.016-.388.021-.374.025-.36.03-.345.033-.333c.196-1.74.616-2.933 1.516-3.833.9-.9 2.092-1.32 3.833-1.516l.333-.034.346-.029.36-.025.373-.02.588-.025.41-.012.644-.013.915-.009ZM6.79 7.3H4.05c.13 6.24 3.25 9.99 8.72 9.99h.31v-3.57c2.01.2 3.53 1.67 4.14 3.57h2.84c-.78-2.84-2.83-4.41-4.11-5.01 1.28-.74 3.08-2.54 3.51-4.98h-2.58c-.56 1.98-2.22 3.78-3.8 3.95V7.3H10.5v6.92c-1.6-.4-3.62-2.34-3.71-6.92Z"/>',
    'youtube': '<path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>',
    'dzen': '<path fill-rule="evenodd" d="M12 0a12 12 0 1 0 0 24 12 12 0 0 0 0-24Zm0 3.4c0 5.2 3.4 8.6 8.6 8.6-5.2 0-8.6 3.4-8.6 8.6 0-5.2-3.4-8.6-8.6-8.6 5.2 0 8.6-3.4 8.6-8.6Z"/>',
    'rutube': '<path fill-rule="evenodd" d="M5.5 1h13A4.5 4.5 0 0 1 23 5.5v13a4.5 4.5 0 0 1-4.5 4.5h-13A4.5 4.5 0 0 1 1 18.5v-13A4.5 4.5 0 0 1 5.5 1ZM7 17.5h2.4v-4.4h2l2.8 4.4h2.8l-3.1-4.7A3.3 3.3 0 0 0 12.9 6H7Zm2.4-9.2h3.5a1.4 1.4 0 0 1 0 2.8H9.4Z"/>',
    'tiktok': '<path d="M14 3v11.2a3.6 3.6 0 1 1-3.6-3.6M14 3c.3 2.4 1.9 4 4.4 4.2" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
}


def load():
    d = json.loads(io.open(os.path.join(HERE, 'socials.json'), encoding='utf-8').read())
    return d['socials']


def shown():
    return [s for s in load() if s.get('show') and s.get('url')]


def svg(s):
    return ('<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">%s</svg>'
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
