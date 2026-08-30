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
import base64, glob, hashlib, io, json, os, re
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
# Раскладка живёт в assets/app.js (SYS_SPN, SYS_WORD, SYS_WORD_EXCLUDE) и
# читается оттуда - см. system_of(). Здесь её копии больше нет: она тут
# была, отстала и разошлась с оригиналом на четыре слова. В app.js
# «сажи», «бортов» и «напряж» выкинули по замерам (395 срабатываний
# «напряж» из 503 оказались про цепь одного датчика, а не про бортовую
# сеть), здесь же они продолжали работать - и страница молча относила код
# к другой системе, чем инструмент на главной.
# Порядок систем на страницах-каталогах: от того, что убивает двигатель
# быстрее всего, к тому, что терпит. «Прочие» всегда последними.
# МАРКИ СО СВОЕЙ НУМЕРАЦИЕЙ НЕИСПРАВНОСТЕЙ.
#
# У ZF AS-Tronic номер в таблице - НЕ SPN по J1939, а собственный номер ZF,
# и это видно прямо в подписях: 2 - это клапан Y2, 3 - Y3, 4..7 - клапаны
# выбора, 10 - главный воздушный Y10; весь диапазон 2..251 плотный, 164
# номера. Совпадение с номером SPN случайное, поэтому из 164 номеров 116
# попадают на страницы, озаглавленные совсем другим смыслом: на странице
# "SPN 27 - Положение клапана EGR №1" стоит строка ZF про конфигурацию
# моторного тормоза.
#
# Убрать таблицу из бесплатных нельзя: 38 страниц держатся только на ней и
# уже проиндексированы, их удаление даст 404. Поэтому строка не прячется, а
# честно помечается - и на странице кода, и на странице марки.
OWN_NUMBERING = {
    'ford': u'У Ford Trucks/Ecotorq своя запись номера: в таблице ниже — '
            u'код в формате Ford (шестнадцатеричный, с ведущими нулями), '
            u'а не SPN по стандарту J1939. Со стандартом он совпадает лишь '
            u'там, где сам сигнал стандартный, а с названием этой страницы — '
            u'как правило, только цифрой.',
    'zfastronic': u'У ZF AS-Tronic своя нумерация неисправностей: номер в '
                  u'таблице ниже — внутренний код ZF, а не SPN по стандарту '
                  u'J1939. С названием этой страницы он совпадает только '
                  u'цифрой, но означает другое.',
}

# Дилерские марки, у которых код собирается из номера блока: MID (кто
# сообщил) + PID/SID (о чём) + FMI (что не так). Выбрать в поиске одну
# марку тут мало - без модуля ключ не собрать, и человек упрётся в
# «выберите блок». Поэтому на странице пишем это прямо.
MID_PCODE_BRANDS = {'volvomid'}

SYS_ORDER_BRAND = ['oil', 'cool', 'fuel', 'air', 'scr', 'power', 'can',
                   'brake', 'trans', 'prot', 'other']
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


# Модель риска берётся из assets/app.js - оттуда же, откуда её берёт сам
# инструмент на главной (RISK_MAP / RISK_TX / RISK_H). Раньше здесь лежала
# СВОЯ копия текстов и свой критерий вердикта: страница считала «ехать
# нельзя» по сырому флагу urgentSpn/urgentFmi, а инструмент - по уровню
# риска. Расходились они не теоретически: 40 страниц писали «обычно ехать
# можно» и тут же «запас времени: счёт на минуты», ещё 57 - наоборот.
# Одна модель на оба места - единственный способ, чтобы это не вернулось.
_RISK_JS = {}


def risk_model():
    if not _RISK_JS:
        from build_lang_pages import extract_js_object
        _RISK_JS['map'] = extract_js_object('RISK_MAP')
        _RISK_JS['tx'] = extract_js_object('RISK_TX')['ru']
        _RISK_JS['h'] = extract_js_object('RISK_H')['ru']
        _RISK_JS['title'] = extract_js_object('RISK_TITLE')['ru']
        _RISK_JS['flag'] = extract_js_object('RISK_FLAG')['ru']
        # Набор «электрических» FMI и таблица тиров лежат там же, в app.js.
        # До этого оба были переписаны сюда руками: FMI_ELEC одной строкой,
        # тир - выражением в пяти местах сразу. Разъехаться они могли молча,
        # потому что ошибка вылезла бы не падением, а чужим текстом на
        # странице - ровно тем сортом расхождения, о котором комментарий выше.
        _RISK_JS['elec'] = extract_js_object('FMI_ELEC')
        _RISK_JS['lvl'] = extract_js_object('RISK_LVL')
        # Классификатор системы - там же и по той же причине: именно он
        # выбирает строку RISK_MAP, то есть весь текст блока риска.
        _RISK_JS['sysSpn'] = extract_js_object('SYS_SPN')
        _RISK_JS['sysWord'] = extract_js_object('SYS_WORD')
        _RISK_JS['sysExcl'] = extract_js_object('SYS_WORD_EXCLUDE')
        # Порядок уровней: в RISK_RANK меньше число - серьёзнее уровень.
        # Здесь лежал свой список LVL_ORDER в обратном порядке; совпадал,
        # но был последней константой, заведённой дважды.
        _RISK_JS['rank'] = extract_js_object('RISK_RANK')
        # Известные цепочки «причина -> следствия» и набор FMI, при
        # которых величина ДЕЙСТВИТЕЛЬНО вышла за норму (а не оборвана
        # цепь датчика). Тем же правилом, что и analyze() в app.js.
        _RISK_JS['causal'] = extract_js_object('CAUSAL')
        _RISK_JS['fmiRange'] = extract_js_object('FMI_RANGE')
    return _RISK_JS


def fmi_elec():
    """FMI электрики самого датчика - из app.js, а не своей копией."""
    return risk_model()['elec']


def tier_of(lvl):
    """Тир для цвета плашки - из RISK_LVL в app.js."""
    return risk_model()['lvl'][lvl]['tier']


def risk_of(sys_key, fmi, urgent):
    """Тот же выбор, что и riskOf() в assets/app.js - строка в строку."""
    m = risk_model()['map'].get(sys_key)
    if m:
        pick = m['elec'] if (m.get('elec') and fmi in fmi_elec()) else m['any']
    elif fmi in fmi_elec():
        pick = ['elecGen', 'watch']
    else:
        pick = ['genUrgent', 'short'] if urgent else ['gen', 'plan']
    key, lvl, flag = pick[0], pick[1], False
    # Метка производителя перевешивает наш спокойный вывод - и мы говорим
    # об этом расхождении вслух, а не втихую (см. RISK_FLAG в app.js).
    if urgent and lvl in ('plan', 'watch'):
        lvl, flag = 'short', True
    return key, lvl, flag


def page_risk(sys_key, fmis, urgent_fmi, urgent_spn_hit):
    """Худший случай по всем FMI страницы: карточка отвечает за код целиком."""
    rank = risk_model()['rank']
    worst_key, worst_lvl, worst_flag = None, None, False
    for f in (fmis or [None]):
        urgent = urgent_spn_hit or (f in urgent_fmi)
        key, lvl, flag = risk_of(sys_key, f, urgent)
        if worst_lvl is None or rank[lvl] < rank[worst_lvl]:
            worst_key, worst_lvl, worst_flag = key, lvl, flag
    return worst_key, worst_lvl, worst_flag


def page_blind(sys_key, fmis, urgent_fmi, urgent_spn_hit):
    """Есть ли на странице код с меткой завода, для системы которого модели
    нет: risk_of() отдаёт таким ключ genUrgent и уровень «short».

    В app.js это blind в analyze(), и он входит в вердикт наравне с уровнем
    «минуты»: «чего мы не понимаем, тем не рискуем». Помеченный критическим
    код без модели остаётся запретом, потому что сказать, что именно
    откажет следующим, по нему нельзя.
    """
    for f in (fmis or [None]):
        urgent = urgent_spn_hit or (f in urgent_fmi)
        if risk_of(sys_key, f, urgent)[0] == 'genUrgent':
            return True
    return False


def page_stop(sys_key, fmis, urgent_fmi, urgent_spn_hit):
    """«Ехать нельзя» - дословно критерий analyze() из app.js."""
    _, lvl, _ = page_risk(sys_key, fmis, urgent_fmi, urgent_spn_hit)
    return lvl == 'now' or page_blind(sys_key, fmis, urgent_fmi, urgent_spn_hit)


def causal_rules(spn):
    """Правила CAUSAL, где код - первопричина и/или следствие.

    Список в app.js намеренно неполный и консервативный: лучше не связать
    два кода, чем связать неверно. Страница повторяет ровно его, ничего
    не достраивая.
    """
    R = risk_model()
    return ([r for r in R['causal'] if spn in r['root']],
            [r for r in R['causal'] if spn in r['cons']])


def risk_section(sys_key, fmis, urgent_fmi, urgent_spn_hit):
    R = risk_model()
    key, lvl, flag = page_risk(sys_key, fmis, urgent_fmi, urgent_spn_hit)
    if not key or key not in R['tx']:
        return u''
    happens, ends = R['tx'][key][0], R['tx'][key][1]
    # Оговорку про электрический код показываем, только если у системы
    # действительно есть отдельный электрический вариант и такие FMI на
    # странице встречаются: иначе это чужой текст.
    note = u''
    m = R['map'].get(sys_key)
    if m and m.get('elec') and any(f in fmi_elec() for f in (fmis or [])) and key != m['elec'][0]:
        e = R['tx'][m['elec'][0]]
        note = u'<p class="rkn">%s %s</p>' % (esc(e[0]), esc(e[1]))
    # Флаг из risk_of() относится к одному коду; на странице кодов много,
    # и при выборе худшего он теряется. Здесь условие страничное и оно
    # честнее: метка производителя есть, а наш вердикт мягче «минут» -
    # значит мы разошлись с заводом и обязаны сказать об этом.
    flagged = urgent_spn_hit or any(f in urgent_fmi for f in (fmis or []))
    if flagged and lvl != 'now':
        note += u'<p class="rkn">%s</p>' % esc(R['flag'])
    tier = tier_of(lvl)
    return (u'<section><h2>%s</h2>'
            u'<div class="risk t-%s"><span class="rkb">Запас времени: %s</span>'
            u'<p>%s</p><p>%s</p>%s</div></section>'
            % (esc(R['title']), tier, esc(R['h'][lvl]), esc(happens), esc(ends), note))


def system_of(spn, name):
    """Дословно systemOf() из app.js, на его же таблицах.

    Исключения (SYS_WORD_EXCLUDE) - точечные заплатки под конкретный брак
    подстрочного поиска: слово нашлось, но случайно, а не по смыслу. Если у
    совпавшего слова есть исключение и его текст ТОЖЕ есть в строке, это
    совпадение не считается и перебор идёт дальше.
    """
    R = risk_model()
    for k, lst in R['sysSpn'].items():
        if spn in lst:
            return k
    low = (name or '').lower()
    for k, words in R['sysWord'].items():
        for w in words:
            if w not in low:
                continue
            if any(bad in low for bad in R['sysExcl'].get(w, [])):
                continue
            return k
    return 'other'

# ------------------------------------------------------- имя кода из таблиц
# Больше половины кодов - заводские номера, которых нет ни в стандарте J1939,
# ни в кураторском списке: у них не было имени, и страница получала заголовок
# «SPN 1 — SPN 1». В выдаче такой заголовок не значит ничего, а во внутренних
# ссылках даёт пустой анкор. Само название узла при этом на странице есть -
# в заводской строке («Иммобилайзер — несовместимый ключ»), просто из неё
# ничего не извлекали. Ниже - извлечение: берём только то, что написал завод,
# ничего не досочиняя, и молчим там, где марки называют код по-разному.

DASH = re.compile(u'\\s+[\u2014\u2013-]\\s+|;\\s+')
COLON = re.compile(u':\\s+')
PAREN = re.compile(u'\\s+\\(')

# Строка часто начинается с типа неисправности, а узел стоит после него
# («Short circuit to ground at output stage to Y4 (Valve Select)»): срезаем
# приставку, иначе узел теряется и код остаётся безымянным.
LEAD = [re.compile(p, re.I | re.U) for p in [
    u'^short\\s+circuit\\s+to\\s+(ground|positive|low|high)\\s*(source\\s*)?(at|on)\\s+output\\s+stage\\s+to\\s+',
    u'^(interruption|open\\s+load|overload)\\s+(at|on)\\s+output\\s+stage\\s+to\\s+',
    u'^short\\s+circuit\\s+to\\s+(ground|positive)\\s+(at|on)\\s+',
    u'^error\\s+on\\s+',
    u'^\u043d\u0435\u0438\u0441\u043f\u0440\u0430\u0432\u043d\u043e\u0441\u0442\u044c\\s+\u0432\\s+\u0446\u0435\u043f\u0438\\s+',
    u'^\u043e\u0448\u0438\u0431\u043a\u0430\\s+\u0432\\s+\u0446\u0435\u043f\u0438\\s+',
]]

# Обрывки, которые сами по себе не значат ничего.
GENERIC = set(u'''j1939 can ecu \u044d\u0431\u0443 abs ebs pto eeprom lin error fault failure signal
\u0441\u0438\u0433\u043d\u0430\u043b \u043e\u0448\u0438\u0431\u043a\u0430 \u043d\u0435\u0438\u0441\u043f\u0440\u0430\u0432\u043d\u043e\u0441\u0442\u044c \u0434\u0430\u0442\u0447\u0438\u043a \u043a\u043b\u0430\u043f\u0430\u043d \u0432\u044b\u0445\u043e\u0434 \u0432\u0445\u043e\u0434 \u0431\u043b\u043e\u043a \u0440\u0435\u043b\u0435 \u043c\u043e\u0434\u0443\u043b\u044c \u0446\u0435\u043f\u044c'''.split())

# Фразы про ТИП неисправности, а не про узел: как имя кода они бесполезны -
# «SPN 85 — Замыкание на массу» не лучше, чем «SPN 85».
JUNK_RE = [re.compile(p, re.I | re.U) for p in [
    u'^(\u043a\u043e\u0440\u043e\u0442\u043a\u043e\u0435\\s+)?\u0437\u0430\u043c\u044b\u043a\u0430\u043d\u0438\u0435\\b.*',
    u'^\u043e\u0431\u0440\u044b\u0432\\b.*',
    u'^\u043a\u0437\\b.*',
    u'^\u043d\u0430\u043f\u0440\u044f\u0436\u0435\u043d\u0438\u0435\\s+(\u0432\u044b\u0448\u0435|\u043d\u0438\u0436\u0435|\u0432\u043d\u0435|\u0441\u043b\u0438\u0448\u043a\u043e\u043c)\\b.*',
    u'^\u0442\u043e\u043a\\s+(\u0432\u044b\u0448\u0435|\u043d\u0438\u0436\u0435|\u0432\u043d\u0435)\\b.*',
    u'^(\u043d\u0435\u0442|\u043e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442|\u043e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u044e\u0442|\u043f\u043e\u0442\u0435\u0440\u044f\u043d|\u043f\u043e\u0442\u0435\u0440\u044f\u043d\u0430)\\s+(\u0441\u0438\u0433\u043d\u0430\u043b\\w*|\u0441\u0432\u044f\u0437\u044c|\u0441\u0432\u044f\u0437\u0438|\u0434\u0430\u043d\u043d\\w+|\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\\w*)\\b.*',
    u'^\u0441\u0438\u0433\u043d\u0430\u043b\\s+(\u043e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442|\u043f\u043e\u0442\u0435\u0440\u044f\u043d|\u0432\u043d\u0435|\u043d\u0435\u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u043d\\w*|\u043d\u0435\u0432\u0435\u0440\u043d\\w*)\\b.*',
    u'^\u043e\u0448\u0438\u0431\u043a\u0430\\s+(\u0441\u0438\u0433\u043d\u0430\u043b\u0430|\u0434\u0430\u043d\u043d\u044b\u0445|\u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u043d\u043e\u0441\u0442\u0438|\u0441\u0432\u044f\u0437\u0438|\u0447\u0442\u0435\u043d\u0438\u044f|\u0437\u0430\u043f\u0438\u0441\u0438)\\b.*',
    u'^(\u043d\u0435\u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u043d\\w*|\u043d\u0435\u0434\u043e\u043f\u0443\u0441\u0442\u0438\u043c\\w*|\u043d\u0435\u0432\u0435\u0440\u043d\\w*|\u043d\u0435\u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\\w*|\u043d\u0435\u043f\u0440\u0430\u0432\u0434\u043e\u043f\u043e\u0434\u043e\u0431\u043d\\w*)\\b.*',
    u'^\u0434\u0430\u043d\u043d\u044b\u0435\\s+(\u0432\u044b\u0448\u0435|\u043d\u0438\u0436\u0435|\u0432\u043d\u0435|\u043d\u0435\u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u043d\\w*)\\b.*',
    u'^\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435\\s+(\u0432\u044b\u0448\u0435|\u043d\u0438\u0436\u0435|\u0432\u043d\u0435)\\b.*',
    u'^(\u0441\u043b\u0438\u0448\u043a\u043e\u043c|\u043f\u0440\u0435\u0432\u044b\u0448\u0435\u043d\\w*|\u0438\u0441\u0442\u0435\u0447\u0435\u043d\u0438\u0435)\\b.*',
    u'^\u043d\u0435\\s+(\u0441\u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0438\u0440\u043e\u0432\u0430\u043d\\w*|\u043e\u0442\u043a\u0430\u043b\u0438\u0431\u0440\u043e\u0432\u0430\u043d\\w*|\u043e\u043f\u0440\u0435\u0434\u0435\u043b\\w*)\\b.*',
    u'^(short|open)[-\\s]+circuit\\b.*',
    u'^no\\s+(signal|fault|data|message)\\b.*',
    u'^(signal|voltage|current)\\s+(too|above|below|out|not)\\b.*',
    u'^(invalid|implausible|erroneous|missing|unknown)\\b.*',
    u'^\\W*$',
]]


def _norm(c):
    return re.sub(u'[^0-9a-z\u0430-\u044f]+', u'', (c or u'').lower())


def component_of(text, short=True):
    """Первая, «узловая» половина заводской строки: до тире/двоеточия/скобки."""
    t = re.sub(u'\\*\\*', u'', text or u'').strip().strip(u'"\u00ab\u00bb\u201c\u201d\u201e\u26a0 ')
    for r in LEAD:
        t = r.sub(u'', t, count=1)
    m = DASH.search(t)
    if m:
        t = t[:m.start()]
    # Двоеточие и скобку режем, только если слева осталось что-то осмысленное:
    # у «J1939: нет сообщения VDHR» и «Y4 (Valve Select)» весь смысл справа.
    for rx in (COLON, PAREN):
        m = rx.search(t)
        if m and len(t[:m.start()].strip()) >= 12:
            t = t[:m.start()]
    t = re.split(u'\\.\\s', t)[0]
    # Хвост после запятой обычно уже симптом, а не узел. Но у Meritor именно
    # он различает колёса («ось 1, левое колесо»), поэтому длинный вариант
    # сохраняем и берём его, когда короткий совпал с чужим кодом.
    if short and len(t) > 45 and u',' in t:
        t = t.split(u',')[0]
    return t.strip(u' .,;:\u2014\u2013-')


def usable_name(c):
    if not c or len(c) < 6 or len(c) > 70:
        # Длинная строка без тире и двоеточия - это проза заводского описания,
        # а не название узла: резать её по букве значит выдумать заголовок.
        return False
    if not re.search(u'[A-Za-z\u0410-\u042f\u0430-\u044f]', c):
        return False
    if _norm(c) in GENERIC:
        return False
    return not any(r.match(c) for r in JUNK_RE)


def brand_pick(rows, short=True):
    """Самый частый пригодный узел у одной марки (при равенстве - по младшему FMI)."""
    cnt, first, order = {}, {}, []
    for f, txt in sorted(rows):
        c = component_of(txt, short)
        if usable_name(c):
            k = _norm(c)
            cnt[k] = cnt.get(k, 0) + 1
            if k not in first:
                first[k] = c
                order.append(k)
    if not order:
        return None
    return first[max(order, key=lambda k: (cnt[k], -order.index(k)))]


def derive_name(makes, short=True):
    """Имя SPN: у одной марки - её узел, у нескольких - только если совпали.
    Разные названия у разных марок - это не имя кода, а разные коды под одним
    номером: тогда честнее оставить страницу без имени, чем выбрать одно.

    Марки из OWN_NUMBERING в выборе не участвуют вовсе. Их строка описывает
    СВОЙ код, а не этот SPN, и в заголовке она делала одно из двух: либо
    врала прямо (5 страниц назывались по строке ZF, при том что тут же под
    заголовком стояло предупреждение «номер ZF означает другое»), либо
    накладывала вето на верное имя от нормальной марки - расходится с ней,
    значит имени нет ни у кого. Вторых было больше: 21 против 22.
    """
    makes = dict((b, r) for b, r in makes.items() if b not in OWN_NUMBERING)
    picks = [p for p in (brand_pick(makes[b], short) for b in sorted(makes)) if p]
    if not picks or len({_norm(p) for p in picks}) > 1:
        return None
    return picks[0][0].upper() + picks[0][1:]


def derive_names(per_spn, spns):
    """Имена пачкой: одно имя на двух кодах - тот же дубль заголовка, от
    которого и уходим, поэтому у совпавших берём неурезанный вариант."""
    names = {}
    for s in spns:
        n = derive_name(per_spn[s])
        if n:
            names[s] = n
    seen = {}
    for n in names.values():
        seen[_norm(n)] = seen.get(_norm(n), 0) + 1
    for s, n in list(names.items()):
        if seen[_norm(n)] > 1:
            long_n = derive_name(per_spn[s], short=False)
            if long_n:
                names[s] = long_n
    return names

# ---------------------------------------------------------------- вывод

# «1384 кодов» и «52 марок» - машинный русский, который сразу видно.
def plural(n, one, few, many):
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        return one
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14:
        return few
    return many


def n_codes(n):
    return u'%d %s' % (n, plural(n, u'код', u'кода', u'кодов'))


def n_brands(n):
    return u'%d %s' % (n, plural(n, u'марки', u'марок', u'марок'))


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


# Раньше крошки были в два уровня честно: у страницы кода/марки/симптома не
# было промежуточной страницы-раздела, придумывать её в разметке значило бы
# врать. Теперь разделы есть (kody/, marki/, problemy/), и третий уровень -
# уже не выдумка: на него можно кликнуть.
SECTIONS = {
    'kody':     (u'Все коды ошибок', 'kody/'),
    'marki':    (u'Все марки', 'marki/'),
    'problemy': (u'Неисправности по симптомам', 'problemy/'),
}


def breadcrumb_ld(name, canon, section=None):
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'codetruck.ru', 'item': SITE + '/'}]
    if section:
        sec_name, sec_path = SECTIONS[section]
        items.append({'@type': 'ListItem', 'position': 2, 'name': sec_name,
                      'item': '%s/%s' % (SITE, sec_path)})
    items.append({'@type': 'ListItem', 'position': len(items) + 1, 'name': name, 'item': canon})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}


# hreflang ставим только там, где английская страница действительно есть.
# Обещать перевод, которого нет, хуже, чем не обещать ничего: поисковик
# сходит по ссылке, получит 404 и перестанет доверять всей разметке.
def alt_links(has_en, rel_path):
    if not has_en:
        return u''
    ru, en = '%s/%s' % (SITE, rel_path), '%s/en/%s' % (SITE, rel_path)
    return (u'\n<link rel="alternate" hreflang="ru" href="%s">'
            u'\n<link rel="alternate" hreflang="en" href="%s">'
            u'\n<link rel="alternate" hreflang="x-default" href="%s">' % (ru, en, ru))


# Ссылка на раздел в верхней строке страницы: без неё раздел существует
# только в sitemap, а человеку и обходчику некуда шагнуть вверх.
def nav_of(section=None):
    up = u'<a href="/">&larr; поиск по коду</a>'
    if not section:
        return up
    sec_name, sec_path = SECTIONS[section]
    return u'%s<span class="sep">&middot;</span><a href="/%s">%s</a>' % (up, sec_path, sec_name)

HEAD = u"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">{alt}
<meta name="theme-color" content="#05070A">
<meta property="og:type" content="article">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="codetruck.ru">
<meta property="og:locale" content="{locale}">
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
.tick a:first-child{{color:#6FE3D3;font-weight:700;font-size:12.5px;border-bottom-color:rgba(111,227,211,.55);border-radius:6px;padding:0 6px;margin-left:-6px}}
@media (prefers-reduced-motion: no-preference){{.tick a:first-child{{animation:tickGlow 4.5s ease-out 1}}}}
@keyframes tickGlow{{0%,25%{{background:rgba(111,227,211,.32);box-shadow:0 0 16px 2px rgba(111,227,211,.5)}}100%{{background:rgba(111,227,211,0);box-shadow:0 0 0 rgba(111,227,211,0)}}}}
.tick .sep{{margin:0 10px;color:#4C5A6B}}
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
/* Раньше это были плашки в строку - хорошо, пока подпись короткая.
   Теперь в ссылке полное название узла, и на телефоне плашки рвались:
   «SPN» и номер вставали друг под другом, ширина скакала. Строка во всю
   ширину с колонкой номера читается сверху вниз и не зависит от длины. */
.near{{margin:0;padding:0;list-style:none;border-top:1px solid rgba(255,255,255,.06)}}
.near li{{margin:0;border-bottom:1px solid rgba(255,255,255,.06)}}
.near a{{display:flex;align-items:baseline;gap:12px;min-height:44px;padding:10px 2px;
  text-decoration:none;color:#AFBECD;font-size:14.5px;line-height:1.45}}
.near a:hover{{color:#EAF0F7}}
.near a .mono{{color:#6FE3D3;flex:none;min-width:5.4em}}
.near a .nm{{flex:1}}
.risk{{border:1px solid rgba(255,255,255,.13);border-radius:14px;padding:14px 16px;background:rgba(255,255,255,.022)}}
.risk .rkb{{display:inline-block;font-family:"Cascadia Mono",Consolas,monospace;font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;border:1px solid;border-radius:6px;padding:3px 8px;margin-bottom:12px}}
.risk p{{margin:0;font-size:15px;line-height:1.6;color:#CBD7E3}}
.risk p+p{{margin-top:9px;color:#AFBECD}}
.risk .rkn{{margin-top:12px;font-size:13.5px;color:#94A2B4}}
.risk.t-now{{color:#FF6B5A;border-color:rgba(255,107,90,.3)}}
.risk.t-warn{{color:#FF9B3D;border-color:rgba(255,155,61,.28)}}
.risk.t-calm{{color:#6FE3D3;border-color:rgba(111,227,211,.28)}}
.lead{{margin:0 0 18px;font-size:14.5px;color:#94A2B4}}
td.fmi .alt{{display:block;font-size:11px;letter-spacing:.02em;color:#7A8998;margin-top:2px}}
.lines{{margin:0;padding:0;list-style:none}}
.lines li{{padding:9px 0;border-bottom:1px solid rgba(255,255,255,.06);font-size:14.5px;color:#94A2B4}}
.lines a{{text-decoration:none;border-bottom:1px solid rgba(111,227,211,.35)}}
/* Ответ на главный вопрос - сразу под заголовком. Подробный блок риска
   ниже объясняет, а эта строка отвечает: человек на обочине не должен
   пролистывать десять заводских таблиц, чтобы узнать, ехать ему или нет. */
.vline{{display:inline-flex;align-items:baseline;flex-wrap:wrap;gap:4px 10px;
  margin:0 0 24px;padding:9px 14px;border:1px solid;border-radius:10px;font-size:15px}}
.vline b{{font-weight:650}}
.vline .hz{{font-size:13.5px;opacity:.85}}
.vline.t-now{{color:#FF6B5A;border-color:rgba(255,107,90,.35);background:rgba(255,107,90,.06)}}
.vline.t-warn{{color:#FF9B3D;border-color:rgba(255,155,61,.3);background:rgba(255,155,61,.05)}}
.vline.t-calm{{color:#6FE3D3;border-color:rgba(111,227,211,.3);background:rgba(111,227,211,.05)}}
/* Марка - то, что ищут глазами. Раньше она была набрана как шапка
   таблицы, мелким серым капсом, и терялась среди служебных подписей. */
h2.mk{{font-family:var(--sans-fallback,inherit);font-size:17.5px;letter-spacing:-.01em;
  text-transform:none;color:#EAF0F7;font-weight:640;margin:30px 0 10px}}
.jump{{margin:0 0 26px;font-size:13.5px;color:#7A8998;display:flex;flex-wrap:wrap;gap:6px 14px}}
.jump a{{text-decoration:none;border-bottom:1px solid rgba(111,227,211,.35)}}
.cta{{margin-top:44px;padding-top:24px;border-top:1px solid rgba(255,255,255,.06);font-size:14px;color:#94A2B4}}
</style>
</head>
<body>
<div class="w">
<div class="tick">{nav}</div>
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


# На сканере одна и та же неисправность показывается по-разному: «SPN 100
# FMI 1», «100/1», «100.1». Человек ищет ровно то, что видит на экране, а
# на странице стояло голое «FMI 1» - совпасть было не с чем. В стандартной
# таблице печатаем код целиком во всех трёх написаниях (spn задан) и вешаем
# якорь, чтобы на конкретное сочетание можно было дать ссылку. В заводских
# таблицах марок оставляем как было: там строк много и марка своя у каждой.
def fmi_table(rows, urgent_fmi, spn=None):
    # Шапка «Код / Расшифровка» повторялась над каждой заводской таблицей -
    # на SPN 100 десять раз подряд, и ничего не сообщала: что слева код, а
    # справа расшифровка, видно и так.
    out = ['<table>']
    for f, text in rows:
        cls = ' class="hit"' if f in urgent_fmi else ''
        if spn is None:
            cell = 'FMI %s' % f
        else:
            cell = ('<a id="fmi-%s"></a>SPN %d FMI %s'
                    '<span class="alt">%d/%s &middot; %d.%s</span>'
                    % (f, spn, f, spn, f, spn, f))
        out.append('<tr%s><td class="fmi">%s</td><td>%s</td></tr>' % (cls, cell, rich(text)))
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
    out = ['<table>']
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


# ---------------------------------------------------------------- sitemap
# Раньше здесь стояла одна строка: today = date.today() - и эта дата
# уходила ВСЕМ адресам при каждой сборке. То есть sitemap ежедневно
# заявлял, что изменился весь сайт целиком. Поисковик такие даты
# перестаёт принимать всерьёз и начинает их игнорировать - а вместе с
# ними теряется единственный способ сказать «вот это обновилось,
# перечитай». Поэтому дату двигаем только тем страницам, у которых
# реально изменилось содержимое: сверяем хеш отрендеренного файла с
# запомненным в sitemap-lastmod.json (он в git, иначе на чистом
# чекауте все даты обнулятся разом и мы вернёмся к тому же вранью).
LASTMOD_DB = 'sitemap-lastmod.json'

# Русские и английские адреса разнесены по двум картам под общим
# индексом: в Search Console охват показывается по каждому файлу
# отдельно, и сразу видно, какую половину сайта робот берёт, а какую
# нет. Одним файлом это неразличимо.
SITEMAPS = [('sitemap-ru.xml', lambda u: '/en/' not in u),
            ('sitemap-en.xml', lambda u: '/en/' in u)]


def url_to_file(url):
    rel = url[len(SITE):].lstrip('/')
    if rel == '' or rel.endswith('/'):
        rel += 'index.html'
    return os.path.join(ROOT, rel.replace('/', os.sep))


def write_sitemap(urls=None):
    """Пересобирает карты сайта, сохраняя даты у неизменившихся страниц."""
    path = os.path.join(ROOT, LASTMOD_DB)
    db = {'urls': [], 'pages': {}}
    if os.path.isfile(path):
        db = json.loads(io.open(path, encoding='utf-8').read())
    if urls is None:
        urls = db.get('urls') or []
    today = date.today().isoformat()
    pages = db.get('pages', {})
    fresh = {}
    changed = 0
    for u in urls:
        f = url_to_file(u)
        try:
            h = hashlib.sha1(io.open(f, 'rb').read()).hexdigest()[:12]
        except IOError:
            # Страницы ещё нет на диске (например, английская до первой
            # сборки) - дату не выдумываем, берём прежнюю или сегодняшнюю.
            prev = pages.get(u)
            fresh[u] = prev if prev else {'h': '', 'd': today}
            continue
        prev = pages.get(u)
        if prev and prev.get('h') == h:
            fresh[u] = prev
        else:
            fresh[u] = {'h': h, 'd': today}
            changed += 1

    written_files = []
    for name, keep in SITEMAPS:
        part = [u for u in urls if keep(u)]
        if not part:
            continue
        sm = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for u in part:
            sm.append('<url><loc>%s</loc><lastmod>%s</lastmod></url>'
                      % (u, fresh[u]['d']))
        sm.append('</urlset>')
        io.open(os.path.join(ROOT, name), 'w', encoding='utf-8').write('\n'.join(sm))
        written_files.append(name)

    idx = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for name in written_files:
        idx.append('<sitemap><loc>%s/%s</loc><lastmod>%s</lastmod></sitemap>'
                   % (SITE, name, today))
    idx.append('</sitemapindex>')
    io.open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(idx))

    io.open(os.path.join(ROOT, LASTMOD_DB), 'w', encoding='utf-8').write(
        json.dumps({'urls': urls, 'pages': fresh}, ensure_ascii=False,
                   indent=0, sort_keys=True))
    print('обновилось страниц: %d из %d' % (changed, len(urls)))
    return changed


# Симптом - это вход для того, у кого номера кода нет: он видит дым,
# слышит звук, чувствует, что не тянет. Список кодов у каждой страницы
# свой, а не «всё, что есть по системе»: иначе «ошибка AdBlue» и «забит
# сажевый фильтр» показывали бы один и тот же набор и были бы для поиска
# одной страницей по двум адресам.
# Формат: (slug, title, H1, вступление, система для блока риска,
#          ключ совета, коды).
SYMPTOMS = [
    ('gorit-check-engine', u'Загорелся Check Engine на грузовике — что делать',
     u'Загорелась лампа Check Engine',
     u'Жёлтая лампа означает, что электроника нашла неисправность и записала код. '
     u'Сама по себе она не говорит, насколько всё плохо: под ней может быть и '
     u'забитый фильтр, и упавшее давление масла. Смотреть надо код.',
     None, None, None),
    ('oshibka-adblue', u'Ошибка AdBlue на грузовике — причины и что делать',
     u'Ошибка AdBlue (мочевины)',
     u'Больше половины ошибок по AdBlue — это пустой или заправленный не тем бак. '
     u'Система SCR быстро переходит к ограничению мощности, поэтому тянуть нельзя.',
     'scr', 'scr', (1761, 4096, 4095, 4094, 3364, 3361, 3362, 3363, 4334, 3031, 5392)),
    ('upala-moshchnost', u'Упала мощность на грузовике — ограничение момента',
     u'Упала мощность, машина не тянет',
     u'Ограничение момента — это не поломка сама по себе, а защита: электроника '
     u'срезает мощность, потому что нашла проблему. Искать надо код, который '
     u'привёл к ограничению.',
     'prot', None, None),
    ('nizkoe-davlenie-masla', u'Низкое давление масла на грузовике — что делать',
     u'Низкое давление масла',
     u'Это самая срочная из частых неисправностей. На низком давлении двигатель '
     u'выхаживает считаные минуты, поэтому останавливаться нужно сразу, а не '
     u'«до базы».',
     'oil', 'oil', (100, 98, 175, 99, 104, 19, 1378)),
    ('peregrev-dvigatelya', u'Перегрев двигателя грузовика — коды и причины',
     u'Перегрев двигателя',
     u'Перегрев редко приходит один: следом идут ограничение мощности и остановка '
     u'по защите. Важно отличать реальный перегрев от отказавшего датчика — по FMI.',
     'cool', 'cool', (110, 111, 4076, 175, 1071, 647)),
    ('zabit-sazhevyy-filtr', u'Забит сажевый фильтр DPF — признаки и коды',
     u'Забит сажевый фильтр (DPF)',
     u'Фильтр забивается, когда машина много ходит на холостых и по городу: '
     u'регенерация не запускается. Сначала растёт противодавление, потом падает '
     u'мощность.',
     'scr', 'scr', (3251, 81, 4782, 131, 173, 3050, 3226, 3489, 3500)),
    ('problemy-s-toplivom', u'Вода в топливе и засор фильтра — коды грузовика',
     u'Вода в топливе, засор фильтра',
     u'Зимой к этому добавляется парафинизация солярки. Коды по топливной системе '
     u'часто идут вместе с потерей мощности и тяжёлым запуском.',
     'fuel', 'fuel', (97, 94, 174, 1075, 96, 38)),
    ('propalo-pitanie', u'Ошибки по питанию и CAN-шине на грузовике',
     u'Пропало питание, ошибки по всей машине',
     u'Если сканер выдал десяток кодов из разных систем разом — почти наверняка '
     u'дело не в десяти поломках, а в питании или шине. Просевшее напряжение и '
     u'оборванная витая пара CAN сыплют ложные коды по всему автомобилю.',
     'power', 'power', (158, 168, 620, 627, 628, 629, 1079, 1080, 3509, 3510, 3511)),

    # --- вход по симптому, а не по системе -------------------------
    ('ne-zavoditsya', u'Грузовик не заводится — причины и коды',
     u'Двигатель не заводится',
     u'Стартер крутит, но не схватывает — это одно; не крутит вовсе — совсем другое. '
     u'Начинают с питания и массы: просевший аккумулятор не даёт блокам нормально '
     u'проснуться и сыплет ложные коды по всей машине. Дальше смотрят подачу топлива '
     u'и датчики оборотов — без их сигнала блок просто не даст впрыск.',
     'power', 'power', (168, 158, 677, 1321, 1041, 1081, 729, 730, 190, 723, 1075, 96)),
    ('glohnet-na-hodu', u'Грузовик глохнет на ходу — коды и причины',
     u'Двигатель глохнет на ходу',
     u'Почти всегда это питание топливом: подсос воздуха, забитый фильтр, отказ '
     u'подкачки. Машина глохнет под нагрузкой или на холостых, и не факт, что '
     u'заведётся обратно с обочины. Коды по рампе и ТНВД показывают, доедете вы '
     u'до сервиса своим ходом или нет.',
     'fuel', 'fuel', (94, 157, 156, 1076, 1077, 1078, 164, 190, 723)),
    ('troit-dvigatel', u'Двигатель троит на грузовике — пропуски воспламенения',
     u'Троит двигатель, пропуски воспламенения',
     u'Пропуски электроника считает по каждому цилиндру отдельно, поэтому код сразу '
     u'называет виновника. Чаще всего это форсунка, реже — компрессия или проводка. '
     u'Долго так ездить нельзя: несгоревшее топливо уходит в выпуск и сажает '
     u'катализатор вместе с сажевым фильтром.',
     'fuel', 'fuel', (1322, 1323, 1324, 1325, 1326, 1327, 1328,
                      651, 652, 653, 654, 655, 656)),
    ('chernyy-dym', u'Чёрный дым из выхлопа грузовика — причины и коды',
     u'Чёрный дым из выхлопа',
     u'Чёрный дым — это лишнее топливо или нехватка воздуха. Смотрят впуск: забитый '
     u'фильтр, подсос через патрубки, отказ турбины или её изменяемой геометрии. '
     u'Вместе с дымом обычно падает тяга и растёт расход.',
     'air', 'air', (102, 103, 132, 641, 1188, 5401, 51, 107, 2630, 5285)),
    ('belyy-dym', u'Белый дым из выхлопа грузовика — причины и коды',
     u'Белый дым из выхлопа',
     u'На холодную белый пар — норма. Белый дым на прогретом двигателе означает либо '
     u'несгоревшее топливо от плохой форсунки, либо охлаждающую жидкость в цилиндрах. '
     u'Второе серьёзнее: уходит антифриз, а следом идёт прокладка головки.',
     'cool', 'cool', (111, 110, 105, 172, 97, 651, 652, 653, 654)),
    ('siniy-dym', u'Синий дым из выхлопа грузовика — масло в цилиндрах',
     u'Синий дым, масло в выхлопе',
     u'Сизый дым означает, что в камеру сгорания попадает масло. На пробеге частая '
     u'причина — уплотнения турбины: масло тянет через неё прямо во впуск. Проверяют '
     u'уровень и давление масла, а заодно слушают турбину на выбеге.',
     'oil', 'oil', (100, 98, 175, 104, 103, 99)),
    ('bolshoy-rashod-topliva', u'Большой расход топлива на грузовике — коды и причины',
     u'Вырос расход топлива',
     u'Расход растёт, когда двигатель работает не в своём режиме: не хватает воздуха, '
     u'льёт форсунка, забит сажевый фильтр. Электроника видит это по своим датчикам '
     u'раньше, чем вы заметите цифру на бортовом компьютере.',
     'fuel', 'fuel', (156, 157, 651, 652, 102, 132, 3251, 3216, 3226, 94)),
    ('ne-idet-regeneratsiya', u'Не идёт регенерация сажевого фильтра — коды DPF',
     u'Не идёт регенерация DPF',
     u'Регенерация не запускается, если машина много ходит на холостых или система не '
     u'может поднять температуру выпуска. Противодавление растёт, дальше пойдёт '
     u'ограничение мощности. Принудительная регенерация в сервисе лечит следствие: '
     u'если причина осталась, фильтр забьётся снова.',
     'scr', 'scr', (4782, 3241, 3249, 173, 131, 4360, 4363, 4809, 3050, 1074, 5543)),
    ('nasos-adblue', u'Не качает AdBlue — насос и дозирование мочевины',
     u'Не качает AdBlue, ошибка дозирования',
     u'Насосный модуль не создаёт давление или не держит его: забита магистраль, '
     u'кристаллизовалась мочевина, отказал подогрев. Зимой это самая частая причина '
     u'ошибок SCR. Дозирование прерывается, и блок начинает отсчёт до ограничения '
     u'мощности — по наработке, а не по километрам.',
     'scr', 'scr', (3361, 3362, 4334, 5392, 3363, 4340, 4342, 3031, 3364)),
    ('datchik-nox', u'Ошибка датчика NOx на грузовике — коды и причины',
     u'Ошибка датчика NOx',
     u'Датчиков NOx обычно два — до и после катализатора, и блок сравнивает их между '
     u'собой. Ошибка приходит и от самого датчика, и от плохой мочевины, и от '
     u'неработающего дозирования. По коду видно, что именно не сошлось.',
     'scr', 'scr', (3216, 3226, 3234, 4090, 4094, 4095, 4096, 4225)),
    ('ne-zaryazhaet-generator', u'Не заряжается аккумулятор на грузовике — генератор',
     u'Не заряжает генератор',
     u'На заведённом двигателе в бортовой сети должно быть 27–29 В. Меньше — генератор, '
     u'ремень или проводка. Больше — регулятор напряжения, и это опаснее: перезаряд '
     u'выкипячивает батареи и выбивает электронику.',
     'power', 'power', (167, 115, 3353, 3381, 3382, 168, 158)),
    ('ne-nabiraet-vozduh', u'Не набирает воздух в пневмосистеме грузовика',
     u'Не набирает воздух',
     u'Долгая накачка или падающее давление — это утечка, компрессор или осушитель. '
     u'С неполным давлением машина не растормаживается, а на затяжном спуске тормозов '
     u'может не хватить. Тот случай, когда выезжать нельзя.',
     'brake', 'brake', (46, 117, 118, 1087, 1351, 37, 82, 1048, 1051)),
    ('gorit-lampa-abs', u'Горит лампа ABS на грузовике — коды и причины',
     u'Горит лампа ABS',
     u'Чаще всего виноват датчик колеса: увеличенный зазор, грязь, разбитый зубчатый '
     u'венец. Рабочие тормоза при этом работают, но ABS отключена — на скользком '
     u'тормозить придётся аккуратнее. Код прямо называет ось и сторону.',
     'brake', 'brake', (789, 790, 791, 792, 793, 794,
                        795, 796, 797, 798, 799, 800, 575)),
    ('stoyanochnyy-tormoz', u'Стояночный тормоз не отпускает — коды грузовика',
     u'Не отпускает стояночный тормоз',
     u'Энергоаккумуляторы отпускают колодки давлением воздуха, поэтому первое, что '
     u'смотрят, — добрало ли давление в контуре. Второе — сам выключатель стояночного '
     u'тормоза и его цепь: блок считает, что ручник поднят, и не даёт ехать.',
     'brake', 'brake', (70, 597, 603, 46, 117, 118)),
    ('ne-pereklyuchayutsya-peredachi', u'Не переключаются передачи на роботе грузовика',
     u'Не переключаются передачи',
     u'Роботизированная коробка уходит в аварийный режим и оставляет одну-две передачи '
     u'или нейтраль. По частоте: давление воздуха в контуре КПП, датчики положения '
     u'вилок, привод сцепления. Главный риск — остаться без передачи на подъёме.',
     'trans', None, (523, 524, 525, 32, 59, 33, 123, 598, 36, 3187, 37)),
    ('probuksovyvaet-sceplenie', u'Буксует сцепление на грузовике — коды и признаки',
     u'Буксует сцепление',
     u'Обороты растут, а скорость нет — диски не держат момент. Электроника ловит это '
     u'по расхождению оборотов двигателя и выходного вала коробки и пишет код раньше, '
     u'чем разница станет заметна в кабине. Гружёным в гору дальше идти не стоит.',
     'trans', None, (33, 36, 123, 598, 684, 191, 160)),
    ('oshibka-retardera', u'Ошибка ретардера на грузовике — коды и причины',
     u'Ошибка ретардера',
     u'Ретардер отключается сам, когда перегрето масло или потеряна связь с блоком. '
     u'Ехать можно, но на затяжном спуске тормозить придётся рабочими тормозами, а они '
     u'на длинном спуске перегреваются. Это меняет план поездки, а не только запись '
     u'в памяти неисправностей.',
     'trans', None, (119, 120, 520, 556, 801, 1085, 1716, 1781)),
    ('greetsya-v-goru', u'Греется в гору под нагрузкой — коды охлаждения',
     u'Греется под нагрузкой',
     u'Если температура растёт только на подъёме и падает на ровной дороге, дело обычно '
     u'в отводе тепла: вязкостная муфта вентилятора, забитый радиатор, интеркулер. '
     u'Датчики и уровень при этом в норме, поэтому лампа загорается поздно — когда '
     u'запас уже выбран.',
     'cool', 'cool', (647, 1071, 986, 1639, 985, 52, 2630, 5285, 975)),
    ('oshibka-tahografa', u'Ошибка тахографа на грузовике — коды и причины',
     u'Ошибка тахографа',
     u'Тахограф раздаёт скорость и пробег по шине, поэтому его ошибка тянет за собой '
     u'чужие коды — от круиз-контроля до ограничителя скорости. Причина чаще в датчике '
     u'на коробке и его проводке, чем в самом приборе.',
     'can', 'can', (1623, 1624, 84, 810, 904, 1592, 74, 2596)),
    ('ne-rabotaet-motornyy-tormoz', u'Не работает моторный тормоз на грузовике — коды',
     u'Не работает моторный тормоз',
     u'Моторный тормоз отключается сам, если неисправна заслонка в выпуске или её '
     u'привод. На спуске это сразу перекладывает всю работу на рабочие тормоза — '
     u'с гружёной машиной так вниз не идут.',
     None, None, (122, 973, 1072, 1073, 1074, 1716, 5543)),
]

# Собственная нумерация марки, а не SPN J1939. В таблице brands она нужна -
# её спрашивают только когда выбрана эта марка, - но отдельная страница
# «SPN 7001» врала бы: такого параметра в J1939 нет, и по запросу «spn 7001»
# человек пришёл бы не туда. КамАЗ CBCU3-E нумерует так свет, прицеп,
# таймауты сообщений CAN и линии кнопок руля.
PRIVATE_SPN = [('kamaz', 7000, 7199)]


def is_private_spn(brand, spn):
    return any(b == brand and lo <= spn <= hi for b, lo, hi in PRIVATE_SPN)


def build(en_spns=()):
    """en_spns - SPN, у которых есть английская страница: только на них
    ставится hreflang и только они попадают в sitemap с адресом /en/.
    Список считает scripts/build_en_pages.py, он же и вызывает эту сборку."""
    en_spns = set(en_spns)
    db = load_db()
    pcode = load_pcode()
    universal, spn_cur = db['universal'], db['spn']
    brands, brand_names = db['brands'], db['brandNames']
    urgent_fmi = set(db['urgentFmi'])
    urgent_spn = set(db['urgentSpn'])

    # какие FMI разобраны у каждого SPN и какими марками
    per_spn = {}
    for b, table in brands.items():
        for key, text in table.items():
            parts = key.split('.')
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                continue
            spn, fmi = int(parts[0]), int(parts[1])
            if is_private_spn(b, spn):
                continue
            per_spn.setdefault(spn, {}).setdefault(b, []).append((fmi, text))

    # страница нужна там, где есть заводской разбор либо кураторская важность
    keep = sorted(set(per_spn) | set(int(k) for k in spn_cur))

    # Имя из стандарта/кураторского списка - и только оно идёт в классификатор
    # системы: выведенное из заводской строки имя туда пускать нельзя, иначе
    # «питание ручки» у ZF попадёт в электропитание и страница получит чужой
    # блок «что будет, если ехать дальше». Заголовкам оно годится, советам нет.
    def std_name(spn):
        s = str(spn)
        return spn_cur.get(s) or universal.get(s) or u''

    derived = derive_names(per_spn, [s for s in keep if not std_name(s) and s in per_spn])

    def name_of(spn):
        return std_name(spn) or derived.get(spn) or u''

    # Анкор без имени («SPN 4099 — SPN 4099») не говорит ни человеку, ни
    # поиску ничего: там, где имени нет, оставляем один номер.
    def code_link(spn, href):
        nm = name_of(spn)
        return (u'<li><a href="%s"><span class="mono">SPN %d</span>%s</a></li>'
                % (href, spn, (u'<span class="nm">%s</span>' % esc(nm)) if nm else u''))

    # Цепочки из app.js: инструмент на главной по ним отвечает, какой код
    # первопричина, а страница молчала - при том что «с чего начинать»
    # это ровно её вопрос. Ссылки ведут на соседние страницы, поэтому
    # заодно чинится и внутренняя перелинковка этих 48 адресов.
    def causal_section(spn):
        as_root, as_cons = causal_rules(spn)
        page = set(keep)
        out = []
        causes = sorted(({s for r in as_cons for s in r['root']} & page) - {spn})
        if causes:
            out.append(u'<section><h2>С чего начинать</h2>'
                       u'<p>Этот код часто не сам по себе, а следствие. Если в том '
                       u'же считывании есть какой-то из этих — разбираться надо '
                       u'с него:</p><ul class="near">%s</ul></section>'
                       % ''.join(code_link(s, 'spn-%d.html' % s) for s in causes))
        follow = sorted(({s for r in as_root for s in r['cons']} & page) - {spn})
        if follow:
            # phys-цепочка работает только когда величина реально вышла за
            # норму: перегрев тянет за собой ограничение мощности, а обрыв
            # провода датчика перегрева - нет. Это разные неисправности.
            cond = (u'Если величина действительно вышла за норму, а не оборвана '
                    u'цепь датчика, следом обычно загораются:'
                    if any(r.get('phys') for r in as_root)
                    else u'Следом за этим кодом обычно загораются:')
            out.append(u'<section><h2>Какие коды приходят следом</h2>'
                       u'<p>%s</p><ul class="near">%s</ul>'
                       u'<p>Отдельно они не чинятся — гаснут вместе с этим. Список '
                       u'намеренно короткий: здесь только те связи, в которых '
                       u'справочник уверен.</p></section>'
                       % (cond, ''.join(code_link(s, 'spn-%d.html' % s) for s in follow)))
        return ''.join(out)

    def brand_list(spn, limit=0):
        names = [brand_names.get(b, b) for b in
                 sorted(per_spn.get(spn, {}), key=lambda x: brand_names.get(x, x))]
        if not names:
            return u''
        if limit and len(names) > limit:
            return u', '.join(names[:limit]) + u' и др.'
        if len(names) == 1:
            return names[0]
        return u', '.join(names[:-1]) + u' и ' + names[-1]

    # соседи по системе - для перелинковки
    by_sys = {}
    for spn in keep:
        by_sys.setdefault(system_of(spn, std_name(spn)), []).append(spn)

    out_dir = os.path.join(ROOT, 'kody')
    for f in glob.glob(os.path.join(out_dir, 'spn-*.html')):
        os.remove(f)

    written = []
    for spn in keep:
        name = name_of(spn)
        sys_key = system_of(spn, std_name(spn))
        makes = per_spn.get(spn, {})

        # Вердикт и риск нужны заранее - они уходят в FAQPage в <head>,
        # а не только в тело страницы ниже.
        seen_all_early = sorted({f for rows in makes.values() for f, _ in rows})
        # «Ехать нельзя» ставим там же, где его ставит инструмент, - см.
        # page_stop(): либо худший код страницы вышел на уровень «минуты»,
        # либо есть помеченный заводом код, для системы которого модели нет.
        # Второе слагаемое здесь долго отсутствовало, и 259 страниц писали
        # «обычно ехать можно» над собственной же строкой «запас времени: до
        # ближайшей остановки» и текстом «продолжать движение без разбора
        # нельзя» - то есть спорили сами с собой, а не только с виджетом.
        urgent_spn_hit = spn in urgent_spn
        _, worst_lvl, _ = page_risk(sys_key, seen_all_early, urgent_fmi, urgent_spn_hit)
        stop = page_stop(sys_key, seen_all_early, urgent_fmi, urgent_spn_hit)
        if stop:
            verdict = (u'<b>По этому коду ехать нельзя.</b> Он относится к неисправностям, '
                       u'при которых остановиться нужно при первой безопасной возможности: '
                       u'дальше поедет дороже.')
        else:
            verdict = (u'<b>Обычно ехать можно</b>, но код нужно показать на ближайшем ТО. '
                       u'Если вместе с ним горит красная лампа или падает мощность — '
                       u'останавливайтесь.')

        # Заводской номер вне стандарта ищут вместе с маркой («spn 4099 knorr»),
        # поэтому у таких кодов марка стоит прямо в заголовке; у стандартных
        # SPN она там лишняя - имя узла и так однозначно.
        brands_short, brands_all = brand_list(spn, 3), brand_list(spn)
        if std_name(spn):
            page_name = u'SPN %d — %s' % (spn, name)
            desc = (u'SPN %d (%s): расшифровка по стандарту J1939 и заводским таблицам марок. '
                    u'Что означает код и можно ли ехать.' % (spn, name))
        elif name:
            page_name = u'SPN %d — %s (%s)' % (spn, name, brands_short)
            desc = (u'SPN %d (%s) у %s: что означает заводской код, значения FMI '
                    u'и можно ли ехать.' % (spn, name, brands_short))
        elif brands_short:
            page_name = u'SPN %d — заводской код %s' % (spn, brands_short)
            desc = (u'SPN %d у %s: как этот заводской код формулирует завод, что означают '
                    u'значения FMI и можно ли ехать.' % (spn, brands_short))
        else:
            page_name = u'SPN %d' % spn
            desc = (u'SPN %d: что означает код по стандарту J1939, значения FMI '
                    u'и можно ли ехать.' % spn)
        title = page_name + u' | codetruck.ru'
        canon = '%s/kody/spn-%d.html' % (SITE, spn)

        faq = [{'@type': 'Question',
                'name': (u'Можно ли ехать с кодом SPN %d (%s)?' % (spn, name) if name
                         else u'Можно ли ехать с кодом SPN %d?' % spn),
                'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'</?b>', '', verdict)}}]
        rk_key, _, _ = page_risk(sys_key, seen_all_early, urgent_fmi, urgent_spn_hit)
        if rk_key and rk_key in risk_model()['tx']:
            happens, ends = risk_model()['tx'][rk_key][0], risk_model()['tx'][rk_key][1]
            faq.append({'@type': 'Question',
                        'name': u'Что будет, если ехать дальше с кодом SPN %d?' % spn,
                        'acceptedAnswer': {'@type': 'Answer', 'text': happens + u' ' + ends}})
        # Спрашивают не «что такое SPN 100», а «что такое 100.1»: половина кода
        # без второй половины ничего не решает. Берём сначала те FMI, что уже
        # помечены срочными - на них и приходят с горящей лампой.
        for f in (sorted(seen_all_early, key=lambda x: (x not in urgent_fmi, x))[:2]):
            if str(f) not in db['fmi']:
                continue
            faq.append({'@type': 'Question',
                        'name': u'Что означает SPN %d FMI %d (%d/%d)?' % (spn, f, spn, f),
                        'acceptedAnswer': {'@type': 'Answer',
                                           'text': u'%s: %s.' % (name or u'SPN %d' % spn,
                                                                 db['fmi'][str(f)])}})

        ld = (ld_script({'@context': 'https://schema.org', '@type': 'TechArticle',
                         'headline': title, 'description': desc, 'url': canon})
              + ld_script(breadcrumb_ld(page_name, canon, 'kody'))
              + ld_script({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': faq}))

        body = [HEAD.format(title=esc(title), desc=esc(desc), canon=canon,
                            ogtitle=esc(page_name), mid=METRIKA_ID, ld=ld,
                            nav=nav_of('kody'), lang='ru', locale='ru_RU',
                            alt=alt_links(spn in en_spns, 'kody/spn-%d.html' % spn))]
        body.append(u'<h1>%s</h1>' % esc(page_name))
        _tier = tier_of(worst_lvl)
        body.append(u'<p class="vline t-%s"><b>%s</b><span class="hz">%s</span></p>'
                    % (_tier,
                       u'Ехать нельзя' if stop else u'Ехать можно',
                       esc(risk_model()['h'].get(worst_lvl, u''))))

        if makes and std_name(spn):
            # Марки называем поимённо: раньше здесь стояло «у 3 марок», и самые
            # нужные человеку слова - названия марок - на странице не звучали.
            body.append(u'<p class="sub">Код J1939 SPN %d. Ниже — как эту неисправность '
                        u'формулируют на заводе у %s, и что вторая половина кода (FMI) '
                        u'означает по стандарту.</p>' % (spn, esc(brands_all)))
        elif makes:
            body.append(u'<p class="sub">SPN %d — заводской номер вне стандартной таблицы '
                        u'J1939: у разных марок под ним может быть разное. Ниже — как его '
                        u'формулируют у %s, и что означает вторая половина кода (FMI).</p>'
                        % (spn, esc(brands_all)))
        else:
            body.append(u'<p class="sub">Код J1939 SPN %d. Заводской расшифровки по маркам '
                        u'для него в справочнике нет — ниже стандартное значение FMI.</p>' % spn)

        # заводские таблицы - это и есть уникальная часть страницы
        # На странице с десятком марок человек ищет свою. Строка переходов
        # экономит ему всю прокрутку - он приходит сюда по запросу с маркой.
        ordered = sorted(makes, key=lambda x: brand_names.get(x, x))
        if len(ordered) >= 3:
            body.append(u'<p class="jump">%s</p>' % u''.join(
                u'<a href="#mk-%s">%s</a>' % (b, esc(brand_names.get(b, b)))
                for b in ordered))
        for b in ordered:
            rows = sorted(makes[b], key=lambda r: r[0])
            note = OWN_NUMBERING.get(b)
            body.append(u'<section><h2 class="mk" id="mk-%s">%s</h2>%s%s</section>'
                        % (b, esc(brand_names.get(b, b)),
                           (u'<p class="sub">%s</p>' % esc(note)) if note else u'',
                           fmi_table(rows, urgent_fmi)))

        # стандартную таблицу печатаем только по встреченным FMI
        seen_fmi = sorted({f for rows in makes.values() for f, _ in rows})
        if seen_fmi:
            std_rows = [(f, db['fmi'][str(f)]) for f in seen_fmi if str(f) in db['fmi']]
            if std_rows:
                body.append(u'<section><h2>Что значит FMI по стандарту J1939</h2>%s</section>'
                            % fmi_table(std_rows, urgent_fmi, spn))
        else:
            common = [f for f in (0, 1, 2, 3, 4, 5) if str(f) in db['fmi']]
            body.append(u'<section><h2>Частые значения FMI</h2>%s</section>'
                        % fmi_table([(f, db['fmi'][str(f)]) for f in common], urgent_fmi, spn))

        # Вердикт (verdict) и признак stop уже посчитаны выше, до <head> - они
        # нужны были заранее для FAQPage.
        body.append(u'<section><h2>Можно ли ехать</h2><p>%s</p></section>' % verdict)
        body.append(risk_section(sys_key, seen_all_early, urgent_fmi, urgent_spn_hit))

        if ADVICE.get(sys_key):
            body.append(u'<section><h2>Что проверить на месте</h2><p>%s</p></section>'
                        % ADVICE[sys_key])

        body.append(causal_section(spn))

        # соседи по узлу: и человеку полезно, и роботу есть куда идти
        neigh = neighbors_of(spn, by_sys.get(sys_key, []))
        if neigh:
            links = ''.join(code_link(s, 'spn-%d.html' % s) for s in neigh)
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
        fmis = sorted({f for rows in makes.values() for f, _ in rows})
        return page_stop(system_of(spn, std_name(spn)), fmis, urgent_fmi,
                         spn in urgent_spn)

    def code_links(spns, prefix='../kody/'):
        return ''.join(code_link(s, '%sspn-%d.html' % (prefix, s)) for s in spns)

    def page(path, title, desc, h1, sub, sections, section=None, extra_ld=None, alt=u''):
        # Рубрику публикуем как /kody/, а не /kody/index.html: ссылки в
        # навигации ведут на директорию, и canonical должен вести туда же,
        # иначе на одну страницу заводится два адреса.
        pub = path[:-len('index.html')] if path.endswith('index.html') else path
        canon = '%s/%s' % (SITE, pub)
        ld = (ld_script({'@context': 'https://schema.org', '@type': 'TechArticle',
                         'headline': title, 'description': desc, 'url': canon})
              + ld_script(breadcrumb_ld(h1, canon, section))
              + (ld_script(extra_ld) if extra_ld else u''))
        body = [HEAD.format(title=esc(title), desc=esc(desc), canon=canon,
                            ogtitle=esc(h1), mid=METRIKA_ID, ld=ld, nav=nav_of(section),
                            lang='ru', locale='ru_RU', alt=alt)]
        body.append(u'<h1>%s</h1>' % esc(h1))
        body.append(u'<p class="sub">%s</p>' % sub)
        body.extend(sections)
        body.append(u'<p class="cta">Знаете номер кода? '
                    u'<a href="/">Введите его в поиск</a> — или вставьте сразу весь '
                    u'список со сканера, покажем, какая поломка настоящая.</p>')
        body.append(u'</div>\n</body>\n</html>\n')
        full = os.path.join(ROOT, path)
        d = os.path.dirname(full)
        if not os.path.isdir(d):
            os.makedirs(d)
        io.open(full, 'w', encoding='utf-8').write(''.join(body))
        return pub

    # Что попало в раздел марок - собираем по ходу, чтобы рубричная
    # страница /marki/ строилась из фактически созданных страниц,
    # а не из отдельного, расходящегося с ними списка.
    brand_index = []

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

        # У MID-марки тоже может быть отдельная дилерская таблица в
        # совсем другом формате: у Mack это 175 OBD-кодов вида P0016,
        # никак не связанных с MID/PID. Раньше эта ветка про них не
        # знала, и таблица молча терялась - ровно та же дыра, что
        # чинили выше для марок с бесплатной SPN-таблицей.
        dealer_rows = None
        if b in pcode:
            dealer_rows = sorted(
                ((code, (entry.get('ru') or entry.get('en') or ''))
                 for code, entry in pcode[b].items()
                 if entry.get('ru') or entry.get('en')),
                key=lambda r: code_sort_key(r[0]))
            if dealer_rows:
                secs.append(
                    u'<section><h2>Ещё %s %s в другом формате</h2>'
                    u'<p>Кроме кодов по модулям (MID) выше, у %s есть и отдельная '
                    u'дилерская таблица OBD-II — код вида P0016, без MID и FMI. '
                    u'Несколько примеров:</p>%s</section>'
                    % (n_codes(len(dealer_rows)), esc(bn), esc(bn),
                       pcode_table(sample_rows(dealer_rows))))

        secs.append(
            u'<section><h2>Как читать код</h2><p>Код состоит из трёх частей: '
            u'<b>MID</b> — какой блок управления его выдал, <b>PID/SID</b> — '
            u'какой параметр или узел неисправен, <b>FMI</b> — тип неисправности '
            u'(замыкание, обрыв, значение вне нормы). На сканере код обычно '
            u'показывается как MID-PID/SID-FMI, например MID128 PID100 FMI4.</p></section>')

        path = 'marki/%s.html' % b
        title = u'Коды ошибок %s | codetruck.ru' % bn
        total_n = len(entries) + (len(dealer_rows) if dealer_rows else 0)
        desc = (u'Расшифровка кодов неисправностей %s: %s по модулям управления '
                u'(MID), с параметром и типом неисправности.' % (bn, n_codes(total_n)))
        sub = (u'В справочнике разобрано <b>%s %s</b> по заводским таблицам, '
               u'сгруппированы по блоку управления (MID).' % (n_codes(len(entries)), esc(bn)))
        if dealer_rows:
            sub += (u' Плюс отдельно ниже — %s %s в дилерском формате OBD-II.'
                    % (n_codes(len(dealer_rows)), esc(bn)))
        brand_index.append((path, bn, total_n, 'mid'))
        return page(path, title, desc, u'Коды ошибок %s' % bn, sub, secs, 'marki')

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

        secs = []
        if stop_codes:
            secs.append(u'<section><h2>С этими кодами ехать нельзя</h2>'
                        u'<ul class="near">%s</ul></section>' % code_links(stop_codes))

        # Дальше - полный список кодов марки, а не витрина из полутора десятков.
        # ВАЖНО, ПРОВЕРЕНО ПЕРЕД ТЕМ, КАК ДЕЛАТЬ: здесь только свободные таблицы
        # brands.* - те самые данные, что уже полностью напечатаны на страницах
        # кодов. Ничего нового мы не раскрываем, это ссылки на открытое.
        # Дилерские pcode.* сюда не попадают физически: у них своя ветка ниже,
        # с выборкой примеров (см. load_pcode и sample_rows). Не объединять.
        by_sys_brand = {}
        for s in mine:
            by_sys_brand.setdefault(system_of(s, std_name(s)), []).append(s)
        for key in SYS_ORDER_BRAND:
            bucket = by_sys_brand.get(key)
            if not bucket:
                continue
            secs.append(u'<section><h2>%s — %s</h2><ul class="near">%s</ul></section>'
                        % (esc(SYS_TITLE[key]), n_codes(len(bucket)), code_links(bucket)))

        secs.append(
            u'<section><h2>Как читать код</h2><p>Код состоит из двух половин. '
            u'<b>SPN</b> — что именно барахлит: датчик, узел, параметр. '
            u'<b>FMI</b> — что с ним не так: значение вне нормы, обрыв, замыкание, '
            u'недостоверные данные. Поэтому «SPN 100» без FMI — это ещё не диагноз, '
            u'а «100/1» уже говорит, что давление масла упало ниже нормы.</p></section>')
        if b in OWN_NUMBERING:
            secs.append(u'<section><h2>Как читать номер</h2><p>%s</p></section>'
                        % esc(OWN_NUMBERING[b]))
        secs.append(
            u'<section><h2>Если кодов сразу несколько</h2><p>Так почти всегда и бывает: '
            u'одна поломка тянет за собой пять-шесть кодов. Пустой бак AdBlue сначала '
            u'даёт ошибку уровня, потом прерванное дозирование, следом превышение NOx '
            u'и ограничение момента. Чинить нужно первопричину, остальное погаснет само. '
            u'<a href="../">Вставьте весь список</a> — покажем, какой код корневой.</p></section>')

        # У марки МОЖЕТ одновременно быть и своя бесплатная SPN/FMI-таблица
        # (выше), и отдельная дилерская pcode.* (другой формат кода - у
        # Isuzu, например, это OBD-II P/U-коды NPR/NQR рядом с J1939 для
        # тяжёлых моделей). Раньше такое не встречалось - дилерский цикл
        # ниже просто пропускал уже построенную марку, и вторая таблица
        # молча терялась. Добавляем секцию-примеры прямо сюда, пока страница
        # ещё не записана, а не постфактум.
        dealer_rows = None
        if b in pcode:
            dealer_rows = sorted(
                ((code, (entry.get('ru') or entry.get('en') or '')) for code, entry in pcode[b].items()
                 if entry.get('ru') or entry.get('en')),
                key=lambda r: code_sort_key(r[0]))
            if dealer_rows:
                secs.append(
                    u'<section><h2>Ещё %s %s в другом формате</h2>'
                    u'<p>Кроме стандарта J1939 (SPN/FMI) выше, у %s есть и отдельная '
                    u'дилерская таблица — свой заводской код, другая нумерация. '
                    u'Несколько примеров:</p>%s</section>'
                    % (n_codes(len(dealer_rows)), esc(bn), esc(bn), pcode_table(sample_rows(dealer_rows))))

        path = 'marki/%s.html' % b
        title = u'Коды ошибок %s | codetruck.ru' % bn
        total_n = len(mine) + (len(dealer_rows) if dealer_rows else 0)
        desc = (u'Все коды неисправностей %s: %s по системам — какие требуют '
                u'немедленной остановки, что означает каждый и можно ли ехать.'
                % (bn, n_codes(total_n)))
        sub = (u'В справочнике разобрано <b>%s %s</b> по заводским таблицам — '
               u'ниже весь список по системам. Сначала те, с которыми ехать нельзя.'
               % (n_codes(len(mine)), esc(bn)))
        if dealer_rows:
            sub += (u' Плюс отдельно ниже — %s %s в дилерском формате.'
                    % (n_codes(len(dealer_rows)), esc(bn)))
        brand_index.append((path, bn, total_n, 'spn'))
        extra.append(page(path, title, desc,
                          u'Коды ошибок %s' % bn, sub, secs, 'marki'))

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
        n_d = u'%d дилерских %s' % (len(rows), plural(len(rows), u'код', u'кода', u'кодов'))
        desc = (u'Расшифровка кодов неисправностей %s: %s в базе, '
                u'с описанием на русском. Введите свой код на codetruck.ru.' % (bn, n_d))
        if b in MID_PCODE_BRANDS:
            sub = (u'В базе разобрано <b>%s %s</b>. Код здесь состоит из трёх частей: '
                   u'<b>MID</b> — какой блок сообщил о неисправности, <b>PID/SID</b> — '
                   u'какой параметр или узел неисправен, <b>FMI</b> — что именно с ним '
                   u'не так; на сканере это выглядит как MID128 PID100 FMI4. Несколько '
                   u'примеров ниже; свой код — в поиск на главной: выберите марку «%s» '
                   u'и блок, в котором записан код.'
                   % (n_d, esc(bn), esc(bn)))
        else:
            sub = (u'В базе разобрано <b>%s %s</b> — свой заводской формат, '
                   u'не входит в стандарт J1939 (SPN/FMI). Несколько примеров ниже; '
                   u'свой код — в поиск на главной, там же можно выбрать марку «%s» из списка.'
                   % (n_d, esc(bn), esc(bn)))
        brand_index.append((path, bn, len(rows), 'pcode'))
        extra.append(page(path, title, desc, u'Коды ошибок %s' % bn, sub, secs, 'marki'))
        marki_built.add(b)

    # --- по симптомам ----------------------------------------------
    sym_dir = os.path.join(ROOT, 'problemy')
    if os.path.isdir(sym_dir):
        for f in glob.glob(os.path.join(sym_dir, '*.html')):
            os.remove(f)

    # SYMPTOMS - теперь модульная константа, см. выше файла.

    sym_index = []
    have = set(written)
    for slug, title_h, h1, intro, sys_key, adv, spns in SYMPTOMS:
        if spns:
            # Кураторский список: порядок задан руками, от самого частого
            # к более редкому, и сортировать его по номеру нельзя.
            pool = [s for s in spns if s in have]
        elif sys_key:
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
            secs.append(risk_section(sys_key, sorted(urgent_fmi), urgent_fmi, False))
        if adv and ADVICE.get(adv):
            secs.append(u'<section><h2>Что проверить на месте</h2><p>%s</p></section>'
                        % ADVICE[adv])
        secs.append(
            u'<section><h2>Можно ли ехать</h2><p>Ответ зависит от кода, а не от лампы. '
            u'Жёлтая лампа — предупреждение, красная означает, что двигаться нельзя. '
            u'Но и под жёлтой попадаются неисправности, при которых остановиться нужно '
            u'сразу: низкое давление масла, перегрев, потеря тормозного давления. '
            u'<a href="../">Введите код</a> — справочник скажет прямо, ехать или '
            u'вставать.</p></section>')

        path = 'problemy/%s.html' % slug
        # Описание в выдаче обрывать на полуслове нельзя - режем по границе
        # слова и добавляем многоточие, если что-то осталось за кадром.
        desc = intro if len(intro) <= 155 else intro[:155].rsplit(u' ', 1)[0] + u'…'
        sym_index.append((path, h1, intro))
        extra.append(page(path, title_h + u' | codetruck.ru', desc, h1,
                          esc(intro), secs, 'problemy'))

    # ---------------------------------------------------------------
    # Рубричные страницы. До них у разделов не было ни одной страницы:
    # kody/, marki/ и problemy/ отдавали 404, наверх с карточки шагнуть
    # было некуда, а под общий запрос («коды ошибок грузовиков», «таблица
    # FMI») отвечать было нечем - на весь сайт одна главная. Каталог тут
    # ещё и связывает граф: до этого до кода добирались только цепочкой
    # соседей по системе.
    # ---------------------------------------------------------------
    secs = [u'<section><h2>Что значит FMI</h2><p class="lead">Номер SPN говорит, '
            u'<i>что</i> неисправно, FMI — <i>что именно</i> с ним не так. Вторая '
            u'половина кода одинакова для всех марок, это стандарт J1939.</p>%s</section>'
            % fmi_table(sorted(((int(f), t) for f, t in db['fmi'].items())), urgent_fmi)]
    for key in SYS_ORDER_BRAND:
        bucket = by_sys.get(key)
        if not bucket:
            continue
        # «Прочие системы» - это 4/5 справочника: заводские номера, которые
        # классификатор по имени не разбирает. Одним списком в тысячу ссылок
        # в нём не найти свой номер, поэтому режем на диапазоны - по ним
        # человек с кодом в руках попадает в нужный кусок с одного взгляда.
        if len(bucket) <= 200:
            secs.append(u'<section><h2>%s — %s</h2><ul class="near">%s</ul></section>'
                        % (esc(SYS_TITLE[key]), n_codes(len(bucket)),
                           code_links(bucket, prefix='')))
            continue
        secs.append(u'<section><h2>%s — %s</h2></section>'
                    % (esc(SYS_TITLE[key]), n_codes(len(bucket))))
        for i in range(0, len(bucket), 120):
            chunk = bucket[i:i + 120]
            secs.append(u'<section><h2>SPN %d — %d</h2><ul class="near">%s</ul></section>'
                        % (chunk[0], chunk[-1], code_links(chunk, prefix='')))

    extra.append(page(
        'kody/index.html',
        u'Все коды ошибок грузовиков — SPN и FMI по J1939 | codetruck.ru',
        u'Полный список разобранных кодов неисправностей грузовиков: %s SPN '
        u'по системам и стандартная таблица FMI. Что означает код и можно ли ехать.'
        % n_codes(len(written)),
        u'Все коды ошибок: SPN и FMI',
        u'В справочнике разобрано <b>%s</b> по заводским таблицам %s. '
        u'Ниже — весь список по системам и стандартная таблица FMI: с ней номер '
        u'кода читается целиком, а не наполовину.'
        % (n_codes(len(written)), n_brands(len(brand_index))),
        secs,
        alt=alt_links(bool(en_spns), 'kody/')))

    veh = [r for r in brand_index if r[3] != 'pcode']
    dlr = [r for r in brand_index if r[3] == 'pcode']

    def brand_rows(rows):
        return u'<ul class="near">%s</ul>' % ''.join(
            u'<li><a href="%s">%s <span class="mono">%d</span></a></li>'
            % (os.path.basename(path), esc(name), cnt)
            for path, name, cnt, _ in sorted(rows, key=lambda r: r[1]))

    secs = []
    if veh:
        secs.append(u'<section><h2>Коды SPN/FMI по стандарту J1939</h2>'
                    u'<p class="lead">У этих марок код читается по стандарту: номер узла '
                    u'плюс тип неисправности. Рядом с маркой — сколько кодов разобрано.</p>'
                    u'%s</section>' % brand_rows(veh))
    if dlr:
        secs.append(u'<section><h2>Дилерские коды в своём формате</h2>'
                    u'<p class="lead">Эти марки нумеруют неисправности по-своему, вне '
                    u'стандарта J1939. Код ищется на главной с выбором марки.</p>'
                    u'%s</section>' % brand_rows(dlr))

    extra.append(page(
        'marki/index.html',
        u'Коды ошибок грузовиков по маркам — расшифровка | codetruck.ru',
        u'Коды неисправностей по маркам грузовиков: %s с заводскими таблицами, '
        u'от КамАЗа и МАЗа до Volvo, Scania и Shacman.' % n_brands(len(brand_index)),
        u'Коды ошибок по маркам',
        u'Заводские таблицы <b>%s</b>: у одних код читается по стандарту J1939, '
        u'у других — свой дилерский формат. Выберите марку или введите код на главной.'
        % n_brands(len(brand_index)),
        secs))

    secs = [u'<section><h2>С чего начать</h2><ul class="lines">%s</ul></section>'
            % ''.join(u'<li><a href="%s">%s</a> — %s</li>'
                      % (os.path.basename(path), esc(h1), esc(intro.split(u'. ')[0]))
                      for path, h1, intro in sym_index)]
    secs.append(
        u'<section><h2>Если код всё-таки есть</h2><p>Симптом сужает круг, но точный '
        u'ответ даёт номер. <a href="/">Введите код со сканера</a> — справочник скажет '
        u'прямо, ехать или вставать, и сколько есть времени. Несколько кодов сразу — '
        u'вставьте весь список, покажем, какой из них первопричина.</p></section>')

    extra.append(page(
        'problemy/index.html',
        u'Неисправности грузовика по симптомам — что делать | codetruck.ru',
        u'Что делать, если на грузовике горит Check Engine, упала мощность, ошибка '
        u'AdBlue или перегрев: вероятные коды, можно ли ехать и что проверить на месте.',
        u'Неисправности по симптомам',
        u'Кода нет, а машина ведёт себя не так? Начните с симптома: ниже — что за ним '
        u'обычно стоит, какие коды это подтверждают и можно ли доехать.',
        secs))

    # sitemap: главная плюс только те страницы, что реально существуют.
    # Языковые версии главной (codetruck.ru/en/ и т.д.) собирает отдельный
    # scripts/build_lang_pages.py - список кодов языков продублирован
    # здесь же (не тянуть импортом ради 9 строк), держать в согласии с
    # LANGS в том файле.
    LANG_HOMEPAGES = ['en', 'de', 'fr', 'es', 'pt', 'pl', 'tr', 'hi', 'zh']
    urls = ([SITE + '/']
            + ['%s/%s/' % (SITE, lang) for lang in LANG_HOMEPAGES]
            + ['%s/%s' % (SITE, p) for p in extra]
            + ['%s/kody/spn-%d.html' % (SITE, s) for s in written]
            + (['%s/en/kody/' % SITE] if en_spns else [])
            + ['%s/en/kody/spn-%d.html' % (SITE, s)
               for s in written if s in en_spns])
    write_sitemap(urls)

    print('страниц собрано: %d' % len(written))
    print('в sitemap URL:   %d' % len(urls))
    # Отдаём разбивку по системам и признак «ехать нельзя»: английская
    # сборка обязана расставить коды по тем же узлам и с тем же вердиктом,
    # иначе два языка одного сайта начнут расходиться в советах.
    return {'written': written,
            'sys': dict((s, system_of(s, std_name(s))) for s in written),
            'stop': dict((s, is_stop(s, per_spn.get(s, {}))) for s in written),
            'lvl': dict((s, page_risk(system_of(s, std_name(s)),
                                      sorted({f for rows in per_spn.get(s, {}).values()
                                              for f, _ in rows}),
                                      urgent_fmi, s in urgent_spn)[1]) for s in written),
            'by_sys': by_sys}


if __name__ == '__main__':
    build()
