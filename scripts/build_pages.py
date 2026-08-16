# -*- coding: utf-8 -*-
"""
Сборка страниц по кодам (kody/spn-*.html) и sitemap.xml из базы assets/dtc.enc.js.

Страница заводится только на тот SPN, по которому есть что сказать: либо он
разобран в заводской таблице хотя бы одной марки, либо входит в кураторский
список важнейших. На чистую телеметрию вроде «пробег за поездку» страницы не
делаем - искать её никто не будет, а тысячи почти одинаковых страниц тянут
за собой фильтр за малополезный контент.

Стандартную таблицу FMI печатаем не целиком, а только по тем значениям,
которые у этого SPN реально встречаются: иначе половина каждой страницы -
один и тот же текст на весь сайт.

Запуск из корня репозитория:  python scripts/build_pages.py
"""
import base64, glob, io, json, os, re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://codetruck.ru'
METRIKA_ID = '111407659'

# ---------------------------------------------------------------- данные

def load_db():
    raw = io.open(os.path.join(ROOT, 'assets', 'dtc.enc.js'), encoding='utf-8').read()
    b64 = re.search(r"b64='([^']+)'", raw).group(1)
    return json.loads(base64.b64decode(b64).decode('utf-8'))

# Дилерские коды (pcode-source/pcode.json) не в git - см. .gitignore: полную
# таблицу отдавать одним файлом нельзя, для этого и сделан Worker, который
# отдаёт по одному коду за раз. Если файла нет (чужой чекаут, CI), просто
# не строим витрины дилерских марок - остальная сборка не должна падать.
def load_pcode():
    path = os.path.join(ROOT, 'pcode-source', 'pcode.json')
    if not os.path.isfile(path):
        return {}
    return json.loads(io.open(path, encoding='utf-8').read())

# ------------------------------------------------------- система по SPN
# Та же раскладка, что в index.html: она решает, какие коды показывать
# в блоке «рядом» - человеку с горящей лампой полезны соседи по узлу,
# а не соседи по номеру.
SYS_SPN = {
    'scr':   [1761,3216,3226,3242,3246,3250,3251,3361,3363,3364,3480,3609,3610,3719,3936,
              4090,4094,4095,4096,4225,4334,4364,4809,5394,5841],
    'oil':   [98,100,175,1208],
    'cool':  [110,111,975,1134,4076,4193],
    'fuel':  [94,95,97,157,164,174,651,652,653,654,655,656,657,658,1076,1077,1239,1347,1348,1349],
    'air':   [102,103,105,106,107,132,411,412,1127,1172,1176,2630,2659,2789,2791,5401,5541],
    'power': [158,167,168,620,627,628,629,1079,1080,3509,3510,3511],
    'can':   [520,639,1231,1235,1237,2003,2005,2011,523212,523216],
    'brake': [46,70,563,597,598,1086,520192],
    'trans': [191,522,523,524,560,561,573,574,787],
    'prot':  [1108,1110,1569,2629,3607,5246],
}
SYS_WORD = {
    'scr':   ['adblue','мочевин','реаген','nox','scr','сажев','катализат','dpf','выхлоп','отработавш','сажи'],
    'oil':   ['масл','смазк'],
    'cool':  ['охлажд','антифриз','радиатор','вентилятор',' ож'],
    'fuel':  ['топлив','форсунк','рампе','рампы','рампа','тнвд','впрыск','солярк'],
    'air':   ['наддув','турбо','воздуш','впуск','интеркул','дроссел'],
    'power': ['напряж','аккумул','генерат','питани','бортов','реле'],
    'can':   ['can','шина','сообщени','связ'],
    'brake': ['тормоз','abs','ebs','пневмо','ресивер'],
    'trans': ['коробк','сцеплен','передач','кпп','трансмисс'],
    'prot':  ['ограничен','защит','останов двигател'],
}
SYS_TITLE = {
    'scr':'AdBlue и выпуск', 'oil':'Смазка', 'cool':'Охлаждение', 'fuel':'Топливная система',
    'air':'Впуск и наддув', 'power':'Электропитание', 'can':'CAN-шина', 'brake':'Тормоза',
    'trans':'Трансмиссия', 'prot':'Защита двигателя', 'other':'Прочие системы',
}

# Что человек может проверить сам, не снимая ничего с машины. Советы
# намеренно осторожные: справочник не ставит диагноз.
ADVICE = {
    'scr':   u'Начните с уровня AdBlue — пустой бак даёт целую гроздь кодов по выпуску. '
             u'Если бак полный, дело в дозировании или качестве реагента, и нужен сканер.',
    'oil':   u'Заглушите двигатель и проверьте уровень масла щупом, осмотрите низ на течи. '
             u'Не заводите, пока давление не восстановится: на низком давлении двигатель '
             u'выхаживает считаные минуты.',
    'cool':  u'Дайте двигателю остыть — пробку расширительного бачка на горячем не открывают. '
             u'Потом проверьте уровень охлаждающей жидкости, патрубки и радиатор.',
    'fuel':  u'Проверьте топливный фильтр и отстойник, слейте воду. Зимой добавьте к подозрениям '
             u'парафинизацию солярки.',
    'air':   u'Осмотрите воздушный фильтр и патрубки наддува: подсос воздуха и трещины дают '
             u'именно такие коды.',
    'power': u'Проверьте клеммы аккумулятора и массу — окисление и слабая затяжка сыплют ложные '
             u'коды по всей машине. На заведённом двигателе норма 27–29 В.',
    'can':   u'Смотрите разъёмы и жгут: обрыв витой пары CAN разом лишает связи все блоки, '
             u'и коды посыпятся отовсюду.',
    'brake': u'Дайте пневмосистеме накачать рабочее давление и послушайте утечки. '
             u'С неисправными тормозами не выезжают.',
}

# Горизонт риска. «Ехать нельзя» - это ещё не ответ: на обочине человек
# решает не да/нет, а дотянет ли до базы и что будет, если всё-таки
# поедет. Поэтому здесь три вещи - сколько есть времени, что произойдёт
# дальше и чем это кончится. Тот же слой, что и в разборе на главной:
# страница кода обязана отвечать на тот же вопрос, с которым на неё
# пришли из поиска.
#
# Формат: (запас времени, тир для цвета, что происходит, чем кончится,
#          оговорка про электрический код или None).
RISK = {
    'oil': (u'Счёт на минуты', 'now',
            u'Масляная плёнка в подшипниках уже рвётся. Каждая минута под нагрузкой — '
            u'это металл по металлу на шейках коленвала.',
            u'Дальше — провёрнутые вкладыши и капитальный ремонт двигателя. Глушить сразу, '
            u'к обочине катиться накатом, не подгазовывая.',
            u'Если код электрический (FMI 3–6), давление, скорее всего, в норме: оборван или '
            u'замкнут провод датчика. Ехать можно, но настоящее падение давления приборка '
            u'уже не покажет — до ремонта цепи проверяйте уровень щупом на каждой остановке.'),
    'cool': (u'Счёт на минуты', 'now',
             u'Двигатель за пределом по температуре. Алюминиевая головка ведёт себя быстро: '
             u'сначала уходит геометрия, потом прогорает прокладка.',
             u'Дальше — пробитая прокладка ГБЦ, повреждённая головка, в худшем случае трещина '
             u'в блоке. Заглушить и дать остыть; крышку расширительного бачка на горячую '
             u'не открывать.',
             u'Если код электрический (FMI 3–6), врёт датчик или его проводка, а не система '
             u'охлаждения. Ехать можно, но стрелка температуры ненадёжна и вентилятор может '
             u'не включиться вовремя.'),
    'brake': (u'Счёт на минуты', 'now',
              u'Часть тормозного контура или ABS/EBS вышла из работы. Педаль при этом может '
              u'ощущаться нормально — до первого экстренного торможения или спуска.',
              u'Дальше — увеличенный тормозной путь, занос на скользком, отказ на затяжном '
              u'спуске. Это тот случай, когда «доеду потихоньку» не работает.', None),
    'scr': (u'Хватит доехать до базы', 'warn',
            u'Дозирование мочевины прервано, и блок это считает. Сначала лампа, потом срез '
            u'момента, потом принудительное ограничение до скорости пешехода — ступени '
            u'включаются по наработке, а не разом.',
            u'Посреди трассы машина не заглохнет, но запас времени тает с каждым часом работы. '
            u'Планировать ремонт нужно сейчас, а не когда мощности уже не останется: эмулятор '
            u'и «отключить мочевину» проблему не убирают, коды копятся дальше.', None),
    'power': (u'До ближайшей остановки', 'warn',
              u'Бортовая сеть не держит напряжение. Пока двигатель работает, всё тянет '
              u'генератор; заглушите — можете не завестись.',
              u'Дальше сядет свет, начнут отваливаться блоки и сыпаться ложные коды по всей '
              u'машине. До места, где есть помощь, лучше доехать не глуша двигатель.', None),
    'can': (u'Хватит доехать до базы', 'warn',
            u'Блоки перестали слышать друг друга по шине. Часть показаний на панели теперь '
            u'берётся из воздуха, часть функций просто выключена.',
            u'Физически ехать можно, но приборке верить нельзя, и остальные коды вполне могут '
            u'быть ложными: сначала лечится шина, потом всё остальное.', None),
    'fuel': (u'До ближайшей остановки', 'warn',
             u'Топливо приходит не в том количестве или не под тем давлением. На подъёме '
             u'и под нагрузкой это вылезет первым.',
             u'Скорее всего, заглохнете на трассе, и не факт, что заведётесь с обочины. '
             u'Если причина в фильтре или воде в баке — до сервиса дотянуть реально; '
             u'если в ТНВД — нет.', None),
    'air': (u'Хватит доехать до базы', 'warn',
            u'Наддув не выходит на расчётные значения: турбина, интеркулер или впуск. '
            u'Двигатель компенсирует это составом смеси и греется сильнее обычного.',
            u'Тяги не будет, расход вырастет, на затяжном подъёме добавится перегрев. '
            u'Если со стороны турбины слышен вой или свист — не тянуть: там разрушается '
            u'крыльчатка.', None),
    'trans': (u'До ближайшей остановки', 'warn',
              u'Коробка или сцепление ушли в аварийный режим: часть передач может стать '
              u'недоступна, робот — перестать переключаться под нагрузкой.',
              u'Главный риск — остаться на подъёме без передачи и покатиться назад. '
              u'Гружёным в горы не идти; до ровного места и сервиса — можно.', None),
    'prot': (u'Хватит доехать до базы', 'warn',
             u'Это не поломка, а реакция на неё: блок сам режет мощность, чтобы защитить '
             u'двигатель или выпуск.',
             u'Ограничение будут ужесточать, пока причину не устранят. Искать надо не этот '
             u'код, а тот, из-за которого он появился.', None),
}


def risk_section(sys_key):
    r = RISK.get(sys_key)
    if not r:
        return u''
    horizon, tier, happens, ends, elec = r
    note = u'<p class="rkn">%s</p>' % elec if elec else u''
    return (u'<section><h2>Что будет, если ехать дальше</h2>'
            u'<div class="risk t-%s"><span class="rkb">Запас времени: %s</span>'
            u'<p>%s</p><p>%s</p>%s</div></section>'
            % (tier, esc(horizon), esc(happens), esc(ends), note))


def system_of(spn, name):
    for k, lst in SYS_SPN.items():
        if spn in lst:
            return k
    low = (name or '').lower()
    for k, words in SYS_WORD.items():
        if any(w in low for w in words):
            return k
    return 'other'

# ---------------------------------------------------------------- вывод

def esc(t):
    return (str(t).replace('&', '&amp;').replace('<', '&lt;')
                  .replace('>', '&gt;').replace('"', '&quot;'))

# В базе разметка markdown-стиля; на странице она должна стать HTML,
# иначе пользователь видит звёздочки.
def rich(t):
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return t


def ld_script(obj):
    return u'<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False)


# Раньше сосед по системе был всегда "первые 10 по номеру во всём бакете" -
# одни и те же для каждой страницы бакета. У бакета в сотни SPN это значит,
# что 990 страниц из 1000 ссылаются на одну и ту же верхушку, а сами не
# получают ни одной входящей ссылки "Рядом" - только запись в sitemap.xml.
# Окно вокруг СВОЕЙ позиции в отсортированном бакете превращает бакет в
# цепочку: сосед ссылается на соседа, и через неё связаны почти все.
def neighbors_of(spn, bucket, n=10):
    if len(bucket) <= 1:
        return []
    i = bucket.index(spn) if spn in bucket else 0
    lo = i - n // 2
    hi = lo + n + 1
    if lo < 0:
        hi -= lo
        lo = 0
    if hi > len(bucket):
        lo = max(0, lo - (hi - len(bucket)))
        hi = len(bucket)
    return [s for s in bucket[lo:hi] if s != spn][:n]


# Хлебные крошки одного уровня: сайт плоский, у страницы кода/марки/
# симптома нет промежуточной страницы-раздела - только "← поиск по коду"
# на главную, поэтому и разметка честно в два уровня, без выдуманной
# иерархии.
def breadcrumb_ld(name, canon):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'codetruck.ru', 'item': SITE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': name, 'item': canon},
    ]}

HEAD = u"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#05070A">
<meta property="og:type" content="article">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="codetruck.ru">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://codetruck.ru/assets/tyagach-noch.jpg">
<meta name="twitter:card" content="summary_large_image">
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id={mid}', 'ym');

    ym({mid}, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/{mid}" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
{ld}
<style>
body{{margin:0;background:#05070A;color:#EAF0F7;font-family:"Segoe UI Variable Display","Segoe UI",Inter,system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}}
.w{{max-width:680px;margin:0 auto;padding:36px 20px 70px}}
a{{color:#6FE3D3}}
.tick{{font-family:"Cascadia Mono",Consolas,monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#8B9AAC;margin-bottom:16px}}
.tick a{{display:inline-flex;align-items:center;min-height:44px}}
.tick a{{color:#8B9AAC;text-decoration:none;border-bottom:1px solid rgba(139,154,172,.4)}}
h1{{font-size:26px;line-height:1.25;margin:0 0 8px;letter-spacing:-.01em}}
.sub{{color:#94A2B4;font-size:14.5px;margin:0 0 28px}}
.mono{{font-family:"Cascadia Mono",Consolas,monospace}}
table{{width:100%;border-collapse:collapse;margin:0 0 28px;font-size:14.5px}}
th{{text-align:left;font-family:"Cascadia Mono",Consolas,monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#7A8998;padding:0 10px 8px 0;border-bottom:1px solid rgba(255,255,255,.12);font-weight:600}}
td{{padding:9px 10px 9px 0;border-bottom:1px solid rgba(255,255,255,.06);vertical-align:top}}
td.fmi{{font-family:"Cascadia Mono",Consolas,monospace;color:#6FE3D3;white-space:nowrap;width:1%}}
tr.hit td.fmi{{color:#FF6B5A}}
h2{{font-family:"Cascadia Mono",Consolas,monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#7A8998;margin:0 0 12px;font-weight:600}}
section{{margin-bottom:32px}}
.near{{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:8px}}
.near li{{margin:0}}
.near a{{display:inline-flex;align-items:center;gap:6px;min-height:44px;text-decoration:none;color:#AFBECD;font-size:13.5px;
  border:1px solid rgba(255,255,255,.13);border-radius:9px;padding:6px 13px;background:rgba(255,255,255,.03)}}
.near a:hover{{color:#EAF0F7;border-color:rgba(111,227,211,.45)}}
.near a .mono{{color:#6FE3D3}}
.risk{{border:1px solid rgba(255,255,255,.13);border-radius:14px;padding:14px 16px;background:rgba(255,255,255,.022)}}
.risk .rkb{{display:inline-block;font-family:"Cascadia Mono",Consolas,monospace;font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;border:1px solid;border-radius:6px;padding:3px 8px;margin-bottom:12px}}
.risk p{{margin:0;font-size:15px;line-height:1.6;color:#CBD7E3}}
.risk p+p{{margin-top:9px;color:#AFBECD}}
.risk .rkn{{margin-top:12px;font-size:13.5px;color:#94A2B4}}
.risk.t-now{{color:#FF6B5A;border-color:rgba(255,107,90,.3)}}
.risk.t-warn{{color:#FF9B3D;border-color:rgba(255,155,61,.28)}}
.cta{{margin-top:44px;padding-top:24px;border-top:1px solid rgba(255,255,255,.06);font-size:14px;color:#94A2B4}}
</style>
</head>
<body>
<div class="w">
<div class="tick"><a href="../">&larr; поиск по коду</a></div>
"""

# Freightliner/Mack/Detroit Diesel используют трёхчастный код MID-PID/SID-FMI
# вместо SPN.FMI (см. index.html, MID_BRANDS). В assets/dtc.enc.js это лежит
# как составной ключ "M<mid>-<P|S><num>.<fmi>" - основной цикл ниже такие
# ключи отбрасывает фильтром .isdigit(), потому что для них нет самого SPN
# и, значит, нет отдельной страницы kody/spn-*. Но у Mack и Detroit Diesel
# (в отличие от Freightliner, где текст собирается на лету в JS из справочных
# таблиц имён) есть готовые построчные описания в brands.* - для них можно
# и нужно сделать страницу марки, просто сгруппированную по модулю (MID),
# а не по SPN.
MID_RE = re.compile(r'^M(\d+)-([A-Z]\d+)$')
MID_MODULE_NAMES = {
    'mack':          {'128': u'Двигатель (EECU)', '142': u'Приборка/шасси (VECU)',
                       '143': u'Двигатель, доп. блок'},
    'detroitdiesel': {'128': u'Двигатель (DDEC)'},
}


def fmi_table(rows, urgent_fmi):
    out = ['<table><tr><th>Код</th><th>Расшифровка</th></tr>']
    for f, text in rows:
        cls = ' class="hit"' if f in urgent_fmi else ''
        out.append('<tr%s><td class="fmi">FMI %s</td><td>%s</td></tr>' % (cls, f, rich(text)))
    out.append('</table>')
    return ''.join(out)


# Дилерский код может быть числом ("10004"), точечным парным ("100.1", как
# у Caterpillar) или буквенно-цифровым ("P0122", "C1312"). Числовые сортируем
# по значению, остальные - по алфавиту следом за ними.
def code_sort_key(code):
    try:
        return (0, float(code))
    except ValueError:
        return (1, code)


def pcode_table(rows):
    out = ['<table><tr><th>Код</th><th>Расшифровка</th></tr>']
    for code, text in rows:
        out.append('<tr><td class="fmi">%s</td><td>%s</td></tr>' % (esc(code), rich(text)))
    out.append('</table>')
    return ''.join(out)


# Витрина, не вся база: страница даёт вкус (равномерная выборка по всей
# отсортированной таблице, не только первые коды) и отправляет за
# остальным в поиск. Публиковать таблицу целиком нельзя - см. load_pcode().
def sample_rows(rows, n=15):
    if len(rows) <= n:
        return rows
    step = len(rows) / float(n)
    idxs, seen = [], set()
    for i in range(n):
        idx = int(i * step)
        if idx not in seen:
            seen.add(idx)
            idxs.append(idx)
    return [rows[i] for i in idxs]


def build():
    db = load_db()
    pcode = load_pcode()
    universal, spn_cur = db['universal'], db['spn']
    brands, brand_names = db['brands'], db['brandNames']
    urgent_fmi = set(db['urgentFmi'])

    # какие FMI разобраны у каждого SPN и какими марками
    per_spn = {}
    for b, table in brands.items():
        for key, text in table.items():
            parts = key.split('.')
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                continue
            spn, fmi = int(parts[0]), int(parts[1])
            per_spn.setdefault(spn, {}).setdefault(b, []).append((fmi, text))

    # страница нужна там, где есть заводской разбор либо кураторская важность
    keep = sorted(set(per_spn) | set(int(k) for k in spn_cur))

    def name_of(spn):
        s = str(spn)
        return spn_cur.get(s) or universal.get(s) or ('SPN ' + s)

    # соседи по системе - для перелинковки
    by_sys = {}
    for spn in keep:
        by_sys.setdefault(system_of(spn, name_of(spn)), []).append(spn)

    out_dir = os.path.join(ROOT, 'kody')
    for f in glob.glob(os.path.join(out_dir, 'spn-*.html')):
        os.remove(f)

    written = []
    for spn in keep:
        name = name_of(spn)
        sys_key = system_of(spn, name)
        makes = per_spn.get(spn, {})

        # Вердикт и риск нужны заранее - они уходят в FAQPage в <head>,
        # а не только в тело страницы ниже.
        seen_all_early = sorted({f for rows in makes.values() for f, _ in rows})
        stop = spn in set(db['urgentSpn']) or bool(set(seen_all_early) & urgent_fmi)
        if stop:
            verdict = (u'<b>По этому коду ехать нельзя.</b> Он относится к неисправностям, '
                       u'при которых остановиться нужно при первой безопасной возможности: '
                       u'дальше поедет дороже.')
        else:
            verdict = (u'<b>Обычно ехать можно</b>, но код нужно показать на ближайшем ТО. '
                       u'Если вместе с ним горит красная лампа или падает мощность — '
                       u'останавливайтесь.')

        page_name = u'SPN %d — %s' % (spn, name)
        title = page_name + u' | codetruck.ru'
        desc = (u'SPN %d (%s): расшифровка по стандарту J1939 и заводским таблицам марок. '
                u'Что означает код и можно ли ехать.' % (spn, name))
        canon = '%s/kody/spn-%d.html' % (SITE, spn)

        faq = [{'@type': 'Question',
                'name': u'Можно ли ехать с кодом SPN %d (%s)?' % (spn, name),
                'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'</?b>', '', verdict)}}]
        risk = RISK.get(sys_key)
        if risk:
            _, _, happens, ends, _ = risk
            faq.append({'@type': 'Question',
                        'name': u'Что будет, если ехать дальше с кодом SPN %d?' % spn,
                        'acceptedAnswer': {'@type': 'Answer', 'text': happens + u' ' + ends}})

        ld = (ld_script({'@context': 'https://schema.org', '@type': 'TechArticle',
                         'headline': title, 'description': desc, 'url': canon})
              + ld_script(breadcrumb_ld(page_name, canon))
              + ld_script({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': faq}))

        body = [HEAD.format(title=esc(title), desc=esc(desc), canon=canon,
                            ogtitle=esc(page_name), mid=METRIKA_ID, ld=ld)]
        body.append(u'<h1>SPN %d — %s</h1>' % (spn, esc(name)))

        if makes:
            body.append(u'<p class="sub">Код J1939 SPN %d. Ниже — как эту неисправность '
                        u'формулируют на заводе у %d %s, и что вторая половина кода (FMI) '
                        u'означает по стандарту.</p>'
                        % (spn, len(makes), u'марки' if len(makes) == 1 else u'марок'))
        else:
            body.append(u'<p class="sub">Код J1939 SPN %d. Заводской расшифровки по маркам '
                        u'для него в справочнике нет — ниже стандартное значение FMI.</p>' % spn)

        # заводские таблицы - это и есть уникальная часть страницы
        for b in sorted(makes, key=lambda x: brand_names.get(x, x)):
            rows = sorted(makes[b], key=lambda r: r[0])
            body.append(u'<section><h2>%s</h2>%s</section>'
                        % (esc(brand_names.get(b, b)), fmi_table(rows, urgent_fmi)))

        # стандартную таблицу печатаем только по встреченным FMI
        seen_fmi = sorted({f for rows in makes.values() for f, _ in rows})
        if seen_fmi:
            std_rows = [(f, db['fmi'][str(f)]) for f in seen_fmi if str(f) in db['fmi']]
            if std_rows:
                body.append(u'<section><h2>Что значит FMI по стандарту J1939</h2>%s</section>'
                            % fmi_table(std_rows, urgent_fmi))
        else:
            common = [f for f in (0, 1, 2, 3, 4, 5) if str(f) in db['fmi']]
            body.append(u'<section><h2>Частые значения FMI</h2>%s</section>'
                        % fmi_table([(f, db['fmi'][str(f)]) for f in common], urgent_fmi))

        # Вердикт (verdict) и признак stop уже посчитаны выше, до <head> - они
        # нужны были заранее для FAQPage.
        body.append(u'<section><h2>Можно ли ехать</h2><p>%s</p></section>' % verdict)
        body.append(risk_section(sys_key))

        if ADVICE.get(sys_key):
            body.append(u'<section><h2>Что проверить на месте</h2><p>%s</p></section>'
                        % ADVICE[sys_key])

        # соседи по узлу: и человеку полезно, и роботу есть куда идти
        neigh = neighbors_of(spn, by_sys.get(sys_key, []))
        if neigh:
            links = ''.join(
                u'<li><a href="spn-%d.html"><span class="mono">SPN %d</span> — %s</a></li>'
                % (s, s, esc(name_of(s))) for s in neigh)
            body.append(u'<section><h2>Рядом: %s</h2><ul class="near">%s</ul></section>'
                        % (esc(SYS_TITLE.get(sys_key, SYS_TITLE['other'])), links))

        body.append(u'<p class="cta">Сканер выдал несколько кодов сразу? '
                    u'<a href="../">Вставьте весь список</a> — покажем, какой из них '
                    u'первопричина, а какие пришли следом.</p>')
        body.append(u'</div>\n</body>\n</html>\n')

        io.open(os.path.join(out_dir, 'spn-%d.html' % spn), 'w', encoding='utf-8').write(''.join(body))
        written.append(spn)

    # ---------------------------------------------------------------
    # Страницы под живые запросы. Страницы кодов отвечают тому, кто уже
    # знает номер со сканера. Но большинство ищет словами - «загорелся
    # чек на камазе», «ошибка адблю» - и на такие запросы у справочника
    # ответа не было. Эти страницы ловят вопрос и уводят к разбору.
    # ---------------------------------------------------------------
    def is_stop(spn, makes):
        fmis = {f for rows in makes.values() for f, _ in rows}
        return spn in set(db['urgentSpn']) or bool(fmis & urgent_fmi)

    def code_links(spns, prefix='../kody/'):
        return ''.join(
            u'<li><a href="%sspn-%d.html"><span class="mono">SPN %d</span> — %s</a></li>'
            % (prefix, s, s, esc(name_of(s))) for s in spns)

    def page(path, title, desc, h1, sub, sections, extra_head=''):
        canon = '%s/%s' % (SITE, path)
        ld = (ld_script({'@context': 'https://schema.org', '@type': 'TechArticle',
                         'headline': title, 'description': desc, 'url': canon})
              + ld_script(breadcrumb_ld(h1, canon)))
        body = [HEAD.format(title=esc(title), desc=esc(desc), canon=canon,
                            ogtitle=esc(h1), mid=METRIKA_ID, ld=ld)]
        body.append(u'<h1>%s</h1>' % esc(h1))
        body.append(u'<p class="sub">%s</p>' % sub)
        body.extend(sections)
        body.append(u'<p class="cta">Знаете номер кода? '
                    u'<a href="../">Введите его в поиск</a> — или вставьте сразу весь '
                    u'список со сканера, покажем, какая поломка настоящая.</p>')
        body.append(u'</div>\n</body>\n</html>\n')
        full = os.path.join(ROOT, path)
        d = os.path.dirname(full)
        if not os.path.isdir(d):
            os.makedirs(d)
        io.open(full, 'w', encoding='utf-8').write(''.join(body))
        return path

    def mid_brand_page(b, mod_names):
        table = brands.get(b)
        if not table:
            return None
        entries = []
        for key, text in table.items():
            composite, dot, fmi = key.rpartition('.')
            m = MID_RE.match(composite)
            if not (m and dot and fmi.isdigit()):
                continue
            entries.append((m.group(1), m.group(2), int(fmi), text))
        if not entries:
            return None

        by_mid = {}
        for mid, pidsid, fmi, text in entries:
            by_mid.setdefault(mid, []).append((pidsid, fmi, text))

        bn = brand_names.get(b, b)
        secs = []
        for mid in sorted(by_mid, key=int):
            rows = sorted(by_mid[mid])
            title = mod_names.get(mid, u'Модуль MID %s' % mid)
            t = [u'<table><tr><th>Код</th><th>Расшифровка</th></tr>']
            for pidsid, fmi, text in rows:
                t.append(u'<tr><td class="fmi">M%s-%s.%d</td><td>%s</td></tr>'
                         % (mid, pidsid, fmi, rich(text)))
            t.append('</table>')
            secs.append(u'<section><h2>%s</h2>%s</section>' % (esc(title), ''.join(t)))

        secs.append(
            u'<section><h2>Как читать код</h2><p>Код состоит из трёх частей: '
            u'<b>MID</b> — какой блок управления его выдал, <b>PID/SID</b> — '
            u'какой параметр или узел неисправен, <b>FMI</b> — тип неисправности '
            u'(замыкание, обрыв, значение вне нормы). На сканере код обычно '
            u'показывается как MID-PID/SID-FMI, например MID128 PID100 FMI4.</p></section>')

        path = 'marki/%s.html' % b
        title = u'Коды ошибок %s | codetruck.ru' % bn
        desc = (u'Расшифровка кодов неисправностей %s: %d разобранных кодов '
                u'по модулям управления (MID), с параметром и типом неисправности.'
                % (bn, len(entries)))
        sub = (u'В справочнике разобрано <b>%d кодов %s</b> по заводским таблицам, '
               u'сгруппированы по блоку управления (MID).' % (len(entries), esc(bn)))
        return page(path, title, desc, u'Коды ошибок %s' % bn, sub, secs)

    extra = []

    # --- по маркам -------------------------------------------------
    brand_dir = os.path.join(ROOT, 'marki')
    if os.path.isdir(brand_dir):
        for f in glob.glob(os.path.join(brand_dir, '*.html')):
            os.remove(f)

    marki_built = set()
    for b in sorted(brands, key=lambda x: brand_names.get(x, x)):
        bn = brand_names.get(b, b)
        mine = sorted({int(k.split('.')[0]) for k in brands[b]
                       if k.split('.')[0].isdigit()})
        mine = [s for s in mine if s in set(written)]
        if not mine:
            continue
        marki_built.add(b)
        stop_codes = [s for s in mine if is_stop(s, per_spn.get(s, {}))][:12]
        rest = [s for s in mine if s not in stop_codes][:14]

        secs = []
        if stop_codes:
            secs.append(u'<section><h2>С этими кодами ехать нельзя</h2>'
                        u'<ul class="near">%s</ul></section>' % code_links(stop_codes))
        if rest:
            secs.append(u'<section><h2>Другие частые коды %s</h2>'
                        u'<ul class="near">%s</ul></section>' % (esc(bn), code_links(rest)))
        secs.append(
            u'<section><h2>Как читать код</h2><p>Код состоит из двух половин. '
            u'<b>SPN</b> — что именно барахлит: датчик, узел, параметр. '
            u'<b>FMI</b> — что с ним не так: значение вне нормы, обрыв, замыкание, '
            u'недостоверные данные. Поэтому «SPN 100» без FMI — это ещё не диагноз, '
            u'а «100/1» уже говорит, что давление масла упало ниже нормы.</p></section>')
        secs.append(
            u'<section><h2>Если кодов сразу несколько</h2><p>Так почти всегда и бывает: '
            u'одна поломка тянет за собой пять-шесть кодов. Пустой бак AdBlue сначала '
            u'даёт ошибку уровня, потом прерванное дозирование, следом превышение NOx '
            u'и ограничение момента. Чинить нужно первопричину, остальное погаснет само. '
            u'<a href="../">Вставьте весь список</a> — покажем, какой код корневой.</p></section>')

        path = 'marki/%s.html' % b
        title = u'Коды ошибок %s | codetruck.ru' % bn
        desc = (u'Расшифровка кодов неисправностей %s: %d разобранных кода, '
                u'какие требуют немедленной остановки и что проверить на месте.'
                % (bn, len(mine)))
        sub = (u'В справочнике разобрано <b>%d кодов %s</b> по заводским таблицам. '
               u'Ниже — те, что встречаются чаще всего.' % (len(mine), esc(bn)))
        extra.append(page(path, title, desc,
                          u'Коды ошибок %s' % bn, sub, secs))

    # --- по маркам с MID-структурой кода (Mack, Detroit Diesel) -----
    for b in sorted(MID_MODULE_NAMES, key=lambda x: brand_names.get(x, x)):
        built = mid_brand_page(b, MID_MODULE_NAMES[b])
        if built:
            extra.append(built)
            marki_built.add(b)

    # --- дилерские марки без своей SPN/FMI-таблицы (Scania, Caterpillar,
    # Cummins и т.п.) ------------------------------------------------
    # Полную таблицу публиковать нельзя (см. load_pcode) - вместо неё
    # карточка марки: сколько кодов есть и выборка из ~15 примеров,
    # за остальным - в поиск на главной с фильтром по марке.
    for b in sorted(pcode, key=lambda x: brand_names.get(x, x)):
        if b in marki_built:
            continue
        bn = brand_names.get(b)
        if not bn:
            continue
        rows = sorted(
            ((code, (entry.get('ru') or entry.get('en') or '')) for code, entry in pcode[b].items()
             if entry.get('ru') or entry.get('en')),
            key=lambda r: code_sort_key(r[0]))
        if not rows:
            continue

        secs = [u'<section><h2>Примеры кодов %s</h2>%s</section>'
                % (esc(bn), pcode_table(sample_rows(rows)))]

        path = 'marki/%s.html' % b
        title = u'Коды ошибок %s | codetruck.ru' % bn
        desc = (u'Расшифровка кодов неисправностей %s: %d дилерских кодов в базе, '
                u'с описанием на русском. Введите свой код на codetruck.ru.'
                % (bn, len(rows)))
        sub = (u'В базе разобрано <b>%d дилерских кодов %s</b> — свой заводской формат, '
               u'не входит в стандарт J1939 (SPN/FMI). Несколько примеров ниже; '
               u'свой код — в поиск на главной, там же можно выбрать марку «%s» из списка.'
               % (len(rows), esc(bn), esc(bn)))
        extra.append(page(path, title, desc, u'Коды ошибок %s' % bn, sub, secs))
        marki_built.add(b)

    # --- по симптомам ----------------------------------------------
    sym_dir = os.path.join(ROOT, 'problemy')
    if os.path.isdir(sym_dir):
        for f in glob.glob(os.path.join(sym_dir, '*.html')):
            os.remove(f)

    SYMPTOMS = [
        ('gorit-check-engine', u'Загорелся Check Engine на грузовике — что делать',
         u'Загорелась лампа Check Engine',
         u'Янтарная лампа означает, что электроника нашла неисправность и записала код. '
         u'Сама по себе она не говорит, насколько всё плохо: под ней может быть и '
         u'забитый фильтр, и упавшее давление масла. Смотреть надо код.',
         None, None),
        ('oshibka-adblue', u'Ошибка AdBlue на грузовике — причины и что делать',
         u'Ошибка AdBlue (мочевины)',
         u'Больше половины ошибок по AdBlue — это пустой или заправленный не тем бак. '
         u'Система SCR быстро переходит к ограничению мощности, поэтому тянуть нельзя.',
         'scr', 'scr'),
        ('upala-moshchnost', u'Упала мощность на грузовике — ограничение момента',
         u'Упала мощность, машина не тянет',
         u'Ограничение момента — это не поломка сама по себе, а защита: электроника '
         u'срезает мощность, потому что нашла проблему. Искать надо код, который '
         u'привёл к ограничению.',
         'prot', None),
        ('nizkoe-davlenie-masla', u'Низкое давление масла на грузовике — что делать',
         u'Низкое давление масла',
         u'Это самая срочная из частых неисправностей. На низком давлении двигатель '
         u'выхаживает считаные минуты, поэтому останавливаться нужно сразу, а не '
         u'«до базы».',
         'oil', 'oil'),
        ('peregrev-dvigatelya', u'Перегрев двигателя грузовика — коды и причины',
         u'Перегрев двигателя',
         u'Перегрев редко приходит один: следом идут ограничение мощности и остановка '
         u'по защите. Важно отличать реальный перегрев от отказавшего датчика — по FMI.',
         'cool', 'cool'),
        ('zabit-sazhevyy-filtr', u'Забит сажевый фильтр DPF — признаки и коды',
         u'Забит сажевый фильтр (DPF)',
         u'Фильтр забивается, когда машина много ходит на холостых и по городу: '
         u'регенерация не запускается. Сначала растёт противодавление, потом падает '
         u'мощность.',
         'scr', 'scr'),
        ('problemy-s-toplivom', u'Вода в топливе и засор фильтра — коды грузовика',
         u'Вода в топливе, засор фильтра',
         u'Зимой к этому добавляется парафинизация солярки. Коды по топливной системе '
         u'часто идут вместе с потерей мощности и тяжёлым запуском.',
         'fuel', 'fuel'),
        ('propalo-pitanie', u'Ошибки по питанию и CAN-шине на грузовике',
         u'Пропало питание, ошибки по всей машине',
         u'Если сканер выдал десяток кодов из разных систем разом — почти наверняка '
         u'дело не в десяти поломках, а в питании или шине. Просевшее напряжение и '
         u'оборванная витая пара CAN сыплют ложные коды по всему автомобилю.',
         'power', 'power'),
    ]

    for slug, title_h, h1, intro, sys_key, adv in SYMPTOMS:
        if sys_key:
            pool = [s for s in by_sys.get(sys_key, [])]
        else:
            pool = [s for s in written if is_stop(s, per_spn.get(s, {}))]
        stop_codes = [s for s in pool if is_stop(s, per_spn.get(s, {}))][:12]
        rest = [s for s in pool if s not in stop_codes][:12]

        secs = []
        if stop_codes:
            secs.append(u'<section><h2>Коды, при которых нужно встать</h2>'
                        u'<ul class="near">%s</ul></section>' % code_links(stop_codes))
        if rest:
            secs.append(u'<section><h2>Другие коды по этой части</h2>'
                        u'<ul class="near">%s</ul></section>' % code_links(rest))
        if sys_key:
            secs.append(risk_section(sys_key))
        if adv and ADVICE.get(adv):
            secs.append(u'<section><h2>Что проверить на месте</h2><p>%s</p></section>'
                        % ADVICE[adv])
        secs.append(
            u'<section><h2>Можно ли ехать</h2><p>Ответ зависит от кода, а не от лампы. '
            u'Янтарная лампа — предупреждение, красная означает, что двигаться нельзя. '
            u'Но и под янтарной попадаются неисправности, при которых остановиться нужно '
            u'сразу: низкое давление масла, перегрев, потеря тормозного давления. '
            u'<a href="../">Введите код</a> — справочник скажет прямо, ехать или '
            u'вставать.</p></section>')

        path = 'problemy/%s.html' % slug
        desc = intro[:155]
        extra.append(page(path, title_h + u' | codetruck.ru', desc, h1,
                          esc(intro), secs))

    # sitemap: главная плюс только те страницы, что реально существуют.
    # Языковые версии главной (codetruck.ru/en/ и т.д.) собирает отдельный
    # scripts/build_lang_pages.py - список кодов языков продублирован
    # здесь же (не тянуть импортом ради 9 строк), держать в согласии с
    # LANGS в том файле.
    LANG_HOMEPAGES = ['en', 'de', 'fr', 'es', 'pt', 'pl', 'tr', 'hi', 'zh']
    urls = ([SITE + '/']
            + ['%s/%s/' % (SITE, lang) for lang in LANG_HOMEPAGES]
            + ['%s/%s' % (SITE, p) for p in extra]
            + ['%s/kody/spn-%d.html' % (SITE, s) for s in written])
    today = date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for i, u in enumerate(urls):
        sm.append('<url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>'
                  % (u, today, '1.0' if i == 0 else '0.7'))
    sm.append('</urlset>')
    io.open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(sm))

    print('страниц собрано: %d' % len(written))
    print('в sitemap URL:   %d' % len(urls))
    return written


if __name__ == '__main__':
    build()
