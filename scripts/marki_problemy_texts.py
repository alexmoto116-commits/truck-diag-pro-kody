# -*- coding: utf-8 -*-
"""
Тексты блоков «Коды <марки>: что важно знать» и «Как подойти к проблеме».

Блоки собирают build_pages.py (ru) и build_en_marki_problemy.py (en).
Здесь только сами абзацы. Числа в них подставляются при сборке из данных
сайта: {codes} - сколько кодов марки разобрано бесплатно (SPN/FMI или своя
нумерация), {dealer} - сколько записей в дилерском разборе. Ссылки на коды
и списки «с этих кодов стоит начать» формирует сборщик, сюда их не пишем.

Правила текстов: без служебных отсылок, английский - точный перевод русского.
"""

BRAND_TEXT = {
    'kamaz': {
        'ru': u'Коды КамАЗ записаны по стандарту J1939: номер узла (SPN) и вид неисправности (FMI). '
              u'В бесплатном разборе на сайте {codes}. Там, где узел определён по названию, чаще всего '
              u'встречаются выпуск и AdBlue, топливо и впуск. Код читается парой: SPN без FMI говорит, '
              u'какой узел, но не что с ним произошло. При FMI 3, 4, 5 или 6 обычно речь об электрической '
              u'цепи датчика, поэтому сначала проверьте разъём и жгут. Если нужного кода нет в списке, '
              u'введите полный код в поиске на главной.',
        'en': u'KAMAZ codes follow the J1939 standard: a component number (SPN) and a fault type (FMI). '
              u'The free tables on the site cover {codes}. Where the component is named, the most common ones '
              u'are the exhaust and AdBlue system, fuel and intake. A code only makes sense as a pair: an SPN '
              u'without its FMI tells you which component, not what happened to it. With FMI 3, 4, 5 or 6 the '
              u'problem is usually the sensor circuit, so check the connector and the harness first. If the code '
              u'you need is not in the list, type the full code into the search on the homepage.',
    },
    'sitrak': {
        'ru': u'SITRAK записывает коды по J1939: SPN и FMI идут парой. Бесплатно разобрано {codes}. Чаще всего '
              u'встречаются выпуск и AdBlue, воздух и наддув, электропитание. Для большинства кодов стандартного '
              u'названия SPN нет, поэтому название узла на странице кода взято из заводской строки. Если FMI '
              u'электрический (с 3 по 6), начинайте с разъёма и цепи, а не с самого узла.',
        'en': u'SITRAK records codes under J1939: the SPN and the FMI come as a pair. The free tables cover '
              u'{codes}. The most common are the exhaust and AdBlue system, intake and boost, and the power supply. '
              u'Most codes have no standard SPN name, so the component name on the code page is taken from the '
              u'factory entry. If the FMI is electrical (3 to 6), start with the connector and the circuit, not '
              u'the component itself.',
    },
    'yamz': {
        'ru': u'ЯМЗ в бесплатном разборе записан по J1939: {codes}. Как и у КамАЗ, для большинства номеров '
              u'стандартного названия нет, и узел виден по заводской строке. В разборе чаще всего выпуск и AdBlue, '
              u'топливо и воздух. Дилерский формат у ЯМЗ другой: трёхзначные коды вроде 111 и 112, где в описании '
              u'прямо написано, например, что нужно заменить блок управления. Таких записей {dealer}.',
        'en': u'YAMZ is recorded under J1939 in the free tables: {codes}. As with KAMAZ, most numbers have no '
              u'standard name, so the component shows through the factory entry. The most common areas are the '
              u'exhaust and AdBlue system, fuel and intake air. The dealer format is different: three-digit codes '
              u'such as 111 and 112, where the description says outright, for example, that the control unit must '
              u'be replaced. There are {dealer} of these.',
    },
    'maz': {
        'ru': u'МАЗ разобран по стандарту J1939 (SPN и FMI): {codes}. Чаще всего встречаются топливная система, '
              u'впуск и электропитание. У большинства кодов название узла берётся из заводской строки, а не из '
              u'стандарта. Записывайте код целиком вместе с FMI: номер узла сам по себе не говорит, что случилось '
              u'и с чем именно.',
        'en': u'MAZ is covered under the J1939 standard (SPN and FMI): {codes}. The most common areas are the fuel '
              u'system, intake and power supply. For most codes the component name comes from the factory entry, '
              u'not from the standard. Write the code down in full with its FMI: the component number on its own '
              u'does not say what happened or to what.',
    },
    'dongfeng': {
        'ru': u'Dongfeng в бесплатном разборе записан по J1939: {codes}. Чаще всего встречаются выпуск и AdBlue, '
              u'электропитание и топливо. Таблица для этой марки короче, чем у КамАЗ или МАЗ, поэтому часть кодов '
              u'сразу не находится на странице, и тогда помогает поиск на главной по полному коду.',
        'en': u'Dongfeng is recorded under J1939 in the free tables: {codes}. The most common areas are the exhaust '
              u'and AdBlue system, the power supply and fuel. This table is shorter than those for KAMAZ or MAZ, so '
              u'some codes will not appear on the page straight away; the search on the homepage, using the full '
              u'code, will find them.',
    },
    'renault': {
        'ru': u'Renault Trucks в бесплатном разборе: {codes} по J1939, и это одна из самых полных таблиц по SPN. '
              u'Чаще всего встречаются топливо, тормоза и электропитание. Тормозные коды записаны отдельно, и если '
              u'в считывании есть коды ABS, начинайте именно с тормозов, а не с двигателя. Дилерских записей '
              u'у Renault {dealer}, в основном с буквами вида IND103.',
        'en': u'Renault Trucks in the free tables: {codes} under J1939, one of the fuller SPN tables on the site. '
              u'The most common areas are fuel, brakes and the power supply. Brake codes are listed separately, and '
              u'if ABS codes are in the reading, start with the brakes rather than the engine. Renault has {dealer} '
              u'in the dealer format, mostly with letter codes such as IND103.',
    },
    'international': {
        'ru': u'International — самая большая из бесплатных таблиц по SPN на сайте: {codes}. Для большинства '
              u'кодов стандартного названия нет, поэтому название узла на странице взято из заводской строки. '
              u'Среди кодов, где узел определён, чаще всего трансмиссия, тормоза и электропитание. Дилерский формат '
              u'у International отдельный: {dealer}.',
        'en': u'International has the largest free SPN table on the site: {codes}. Most codes have no standard name, '
              u'so the component name on the page comes from the factory entry. Among the codes where the component '
              u'is known, the most common are transmission, brakes and the power supply. International also has its '
              u'own dealer format: {dealer}.',
    },
    'iveco': {
        'ru': u'Iveco в бесплатном разборе: {codes} по J1939, и у них почти нет стандартного названия узла, '
              u'поэтому название берётся из заводской строки. Из марок со стандартными SPN у Iveco больше всего '
              u'кодов, при которых ехать нельзя: в таблице их {stops}, и на странице они идут первыми. Дилерские записи '
              u'отдельно: {dealer}, чаще всего топливо и выпуск.',
        'en': u'Iveco in the free tables: {codes} under J1939, almost none of them with a standard component name, '
              u'so the name comes from the factory entry. Of the makes with standard SPN codes, Iveco has the most '
              u'codes that mean stop: {stops} on the page, listed first. The dealer entries are separate: {dealer}, '
              u'most often fuel and exhaust.',
    },
    'man': {
        'ru': u'У MAN два формата. В бесплатном разборе код записан по J1939 (SPN и FMI): {codes}, и здесь заметнее '
              u'всего тормоза, трансмиссия и выпуск. Дилерские коды MAN другие: пятизначные номера вроде 00001, где '
              u'сначала модуль, потом неисправность, таких {dealer}. Сначала определите, какой блок записал код, и '
              u'только потом читайте расшифровку.',
        'en': u'MAN uses two formats. In the free tables the code follows J1939 (SPN and FMI): {codes}, where the '
              u'brakes, transmission and exhaust stand out most. The dealer codes are different: five-digit numbers '
              u'such as 00001, where the module comes first and then the fault; there are {dealer} of them. First '
              u'work out which unit logged the code, and only then read the explanation.',
    },
    'manebs': {
        'ru': u'MAN EBS — отдельная дилерская таблица тормозного модуля: {dealer}. По системам чаще всего шина CAN, '
              u'тормоза и электропитание. Код записан номером модуля, а в тексте стоит FMI, например, для ножного '
              u'тормоза — замыкание на массу. Если горит лампа тормозов вместе с несколькими кодами из этой таблицы, '
              u'проверяйте жгут модуля, а не только датчик.',
        'en': u'MAN EBS is a separate dealer table for the brake module: {dealer}. The most common areas are the CAN '
              u'bus, brakes and the power supply. A code is written as a module number, and the text gives the FMI; '
              u'for the foot brake, for example, it is a short to earth. If the brake lamp is on together with several '
              u'codes from this table, check the module harness, not just the sensor.',
    },
    'manzbr2': {
        'ru': u'MAN ZBR2 — ещё одна дилерская таблица: {dealer}. По системам чаще всего шина CAN, электропитание '
              u'и тормоза. Код состоит из пятизначного номера и текста, в котором иногда указан FMI. Таблица описывает '
              u'блоки управления, поэтому перед разбором уточните, какой модуль записал код.',
        'en': u'MAN ZBR2 is another dealer table: {dealer}. The most common areas are the CAN bus, the power supply '
              u'and brakes. A code is a five-digit number plus text, which sometimes gives the FMI. The table covers '
              u'control units, so before reading it, establish which module logged the code.',
    },
    'daf': {
        'ru': u'DAF разобран в двух форматах: стандартные SPN/FMI ({codes}) и дилерский разбор, где код вида 12401-20 '
              u'с описанием вроде «VIC: защита кулисы», таких {dealer}. Больше всего записей именно в дилерском '
              u'разборе: шина CAN, выпуск и AdBlue, электропитание и тормоза. Код с дефисом — дилерский, его смысл '
              u'в описании рядом.',
        'en': u'DAF is covered in two formats: standard SPN/FMI ({codes}) and the dealer format, where a code such as '
              u'12401-20 has a description like "VIC: gear shift gate protection"; there are {dealer} of these. Most '
              u'of the records are in the dealer format: the CAN bus, exhaust and AdBlue, power supply and brakes. A '
              u'code with a hyphen is a dealer code, and its meaning is in the description beside it.',
    },
    'isuzu': {
        'ru': u'У Isuzu два формата. Для тяжёлых моделей код записан по J1939 (SPN и FMI): {codes}. Для лёгких NPR и '
              u'NQR — буквенно-цифровые коды вида C0201, таких {dealer}. Чаще всего в дилерском разборе встречаются '
              u'топливо, воздух и электропитание. Перед поиском определите модель: SPN для коротких NPR и NQR не '
              u'применяется, и номер из таблицы J1939 к ним не подходит.',
        'en': u'Isuzu uses two formats. For heavy models the code follows J1939 (SPN and FMI): {codes}. For the light '
              u'NPR and NQR the codes are alphanumeric, such as C0201; there are {dealer} of them. The most common '
              u'areas in the dealer records are fuel, intake air and the power supply. Before searching, establish the '
              u'model: SPNs do not apply to the NPR and NQR, and a J1939 number does not match them.',
    },
    'knorrbremse': {
        'ru': u'Knorr-Bremse EBS — тормозной контроллер, коды записаны по J1939: {codes}. Тормоза и трансмиссия здесь '
              u'заметнее всего, но для большинства кодов стандартного названия нет. Коды, при которых ехать нельзя, '
              u'собраны первыми на странице, всего таких в таблице {stops}.Если EBS пишет о питании, сначала проверьте напряжение, '
              u'а не сам клапан.',
        'en': u'Knorr-Bremse EBS is a brake controller; its codes follow J1939: {codes}. Brakes and transmission stand '
              u'out most, but most codes have no standard name. The codes that mean stop are listed first on the page, '
              u'and there are {stops} of them in the table. If the EBS reports a power problem, check the voltage first, not the valve.',
    },
    'meritor': {
        'ru': u'Meritor — бывший WABCO. Таблица тормозных кодов по J1939: {codes}. Тормоза — основная система в ней, '
              u'за ними идут электропитание и CAN. Для большинства кодов узел берётся из заводской строки. Перед тем '
              u'как снимать датчик или клапан, проверьте в считывании код электропитания: без него сигнал тормозов '
              u'может быть ложным.',
        'en': u'Meritor is the former WABCO. The brake-code table under J1939 has {codes}. Brakes are the main system '
              u'in it, followed by the power supply and the CAN bus. For most codes the component name comes from the '
              u'factory entry. Before you remove a sensor or valve, check the reading for a power-supply code: without '
              u'it, a brake signal may be false.',
    },
    'bendix': {
        'ru': u'Bendix ABS/ESP — отдельная таблица электроники тормозов: {codes} по J1939. В основном тормоза и '
              u'электропитание. Лампа ABS означает, что антиблокировка не работает, даже если тормоза в целом '
              u'тормозят, поэтому относитесь к коду серьёзно и не откладывайте разбор.',
        'en': u'Bendix ABS/ESP is a separate table for brake electronics: {codes} under J1939, mostly brakes and the '
              u'power supply. The ABS lamp means anti-lock braking is not working, even if the brakes still stop the '
              u'truck, so take the code seriously and do not put off the check.',
    },
    'wabco': {
        'ru': u'WABCO ABS/ESC — таблица тормозной электроники: {codes} по J1939. Большинство кодов относится к тормозам. '
              u'Коды, при которых ехать нельзя, стоят на странице первыми. Если в считывании несколько кодов ABS '
              u'вместе с кодами CAN, сначала проверьте разъём и питание блока, а не датчики колёс.',
        'en': u'WABCO ABS/ESC is a table of brake electronics: {codes} under J1939. Most of the codes concern the '
              u'brakes. The codes that mean stop are listed first on the page. If the reading has several ABS codes '
              u'together with CAN codes, check the connector and the unit power first, not the wheel sensors.',
    },
    'foton': {
        'ru': u'Foton разобран по J1939, но бесплатных кодов немного: {codes}. Чаще всего встречаются выпуск и AdBlue, '
              u'топливо. Дилерского разбора по Foton на сайте нет, поэтому если нужного кода нет в списке, введите его '
              u'целиком в поиск на главной.',
        'en': u'Foton is covered under J1939, but there are few free codes: {codes}. The most common areas are the '
              u'exhaust and AdBlue system and fuel. There is no dealer table for Foton on the site, so if the code you '
              u'need is not listed, type the full code into the search on the homepage.',
    },
    'ford': {
        'ru': u'У Ford Trucks и Ecotorq номер записан по собственной схеме: это шестнадцатеричный код с ведущими '
              u'нулями, а не SPN по J1939. Записей {codes}, и все они собраны на одной странице, с заводским описанием '
              u'у каждого номера. Номер, совпавший с SPN на другой странице, означает другое, поэтому ищите код по '
              u'полному номеру из считывания, а не по SPN.',
        'en': u'Ford Trucks and Ecotorq record the number in their own scheme: a hexadecimal code with leading zeros, '
              u'not a J1939 SPN. There are {codes}, all gathered on this page with the factory description for each '
              u'number. A number that matches an SPN on another page means something else, so look the code up by its '
              u'full number from the reading, not by an SPN.',
    },
    'zfastronic': {
        'ru': u'У ZF AS-Tronic своя нумерация: номер в таблице — внутренний код ZF, а не SPN. Записей {codes}. '
              u'Цифры здесь означают конкретные элементы: 2 — клапан Y2, 3 — клапан Y3, с 4 по 7 — клапаны выбора, '
              u'10 — главный воздушный клапан Y10. Поэтому читайте описание на этой странице, а не название страницы '
              u'кода с тем же числом.',
        'en': u'ZF AS-Tronic has its own numbering: the number in the table is an internal ZF code, not an SPN. There '
              u'are {codes}. The numbers name specific parts: 2 is valve Y2, 3 is valve Y3, 4 to 7 are the selector '
              u'valves, and 10 is the main air valve Y10. So read the description on this page, not the title of the '
              u'code page with the same number.',
    },
    'mack': {
        'ru': u'Код Mack собран из трёх частей: номер модуля MID (например, 128 — двигатель, 142 — шасси и приборная '
              u'панель), PID/SID параметр и FMI вид неисправности. Записей по модулям {codes}, и на странице они '
              u'разложены по модулю. Отдельно есть дилерская таблица OBD-II вида P0016, которая не связана с MID и FMI.',
        'en': u'A Mack code has three parts: the MID module number (for example 128 is the engine, 142 is the chassis and '
              u'dash), the PID/SID parameter, and the FMI fault type. There are {codes} by module, and on this page they '
              u'are grouped by module. There is also a separate dealer table in OBD-II form, such as P0016, which is '
              u'not linked to the MID or FMI.',
    },
    'detroitdiesel': {
        'ru': u'Detroit Diesel записывается так же, как Mack: номер модуля MID, PID/SID и FMI. В разборе записан блок '
              u'двигателя DDEC (модуль 128), записей {codes}. Если по коду не видно параметр, сверьте его с той же '
              u'строкой в таблице, а не с общим описанием неисправности.',
        'en': u'Detroit Diesel is written like Mack: the MID module number, the PID/SID and the FMI. The reading covers '
              u'the DDEC engine unit (module 128), with {codes} in total. If the parameter is not clear from the code, '
              u'check it against the same row in the table, not against a general description of the fault.',
    },
    'allison': {
        'ru': u'Allison — автоматическая коробка, и коды здесь почти все про трансмиссию: {dealer}. Чаще всего встречаются '
              u'трансмиссия, смазка и CAN-шина. Формат смешанный: цифры вроде 11 и 12, а также коды вида P0121 и C1312. '
              u'Прежде чем искать, уточните, из какого блока пришёл код: коробка, двигатель и приборы могут записывать '
              u'похожие по смыслу коды с разными номерами.',
        'en': u'Allison is an automatic gearbox, and its codes are almost all about the transmission: {dealer}. The most '
              u'common areas are transmission, lubrication and the CAN bus. The format is mixed: numbers such as 11 and '
              u'12, and codes such as P0121 and C1312. Before you search, establish which unit the code came from: the '
              u'gearbox, the engine and the instruments can log similar faults under different numbers.',
    },
    'ashokleyland': {
        'ru': u'Ashok Leyland — дилерский разбор: {dealer}. Чаще всего встречаются защита двигателя, топливная система и '
              u'электропитание. Большинство номеров записано по OBD-II (вида P0016), поэтому смысл читается по строке '
              u'таблицы, без SPN.',
        'en': u'Ashok Leyland has a dealer table: {dealer}. The most common areas are engine protection, the fuel system '
              u'and the power supply. Most numbers are OBD-II codes (such as P0016), so the meaning is read from the row '
              u'in the table, with no SPN involved.',
    },
    'baw': {
        'ru': u'BAW — дилерский разбор: {dealer}. По системам чаще всего топливо, защита двигателя и воздух. Коды вида '
              u'P0016 и P0069 записаны по OBD-II, поэтому смысл читается по строке таблицы.',
        'en': u'BAW has a dealer table: {dealer}. The most common areas are fuel, engine protection and intake air. Codes '
              u'such as P0016 and P0069 follow OBD-II, so the meaning is read from the row in the table.',
    },
    'carrier': {
        'ru': u'Carrier Transicold — холодильная установка, а не двигатель: {dealer}. Чаще всего встречаются охлаждение, '
              u'электропитание и топливо. Коды короткие, например 1, 11 и 12, и относятся к самой установке. Если горит '
              u'лампа на холодильнике, сначала смотрите код установки, а лампу двигателя — на панели грузовика.',
        'en': u'Carrier Transicold is a refrigeration unit, not the engine: {dealer}. The most common areas are cooling, '
              u'the power supply and fuel. The codes are short, such as 1, 11 and 12, and they refer to the unit itself. '
              u'If the lamp on the refrigeration unit is on, read the unit code first, and the engine lamp on the truck '
              u'panel second.',
    },
    'caterpillar': {
        'ru': u'Caterpillar — дилерский разбор: {dealer}, и коды записаны парами чисел через точку, например 100.1 и 1.11. '
              u'Чаще всего встречаются топливо, воздух и SCR. По виду они похожи на SPN и FMI, но таблица Caterpillar '
              u'своя, поэтому значение берите из строки, а не из стандарта J1939. Соленоиды форсунок и датчики в ней '
              u'расписаны по цилиндрам.',
        'en': u'Caterpillar has a dealer table: {dealer}, and the codes are written as pairs of numbers separated by a '
              u'dot, such as 100.1 and 1.11. The most common areas are fuel, intake air and SCR. They look like SPN and '
              u'FMI, but the Caterpillar table has its own scheme, so take the value from the row, not from the J1939 '
              u'standard. Injector solenoids and sensors are listed by cylinder.',
    },
    'cumminsisb': {
        'ru': u'Cummins ISB — двигатель с числовыми кодами: {dealer} дилерского разбора, например 111 и 115. Чаще всего '
              u'встречаются топливо, воздух и смазка. Это не SPN и не FMI, поэтому код ищите по номеру целиком. Многие '
              u'коды относятся к блоку управления ECM, и в описании часто есть признак, например «двигатель может не '
              u'запускаться».',
        'en': u'Cummins ISB is an engine with numeric codes: {dealer} in the dealer table, such as 111 and 115. The most '
              u'common areas are fuel, intake air and lubrication. These are not SPNs or FMIs, so look the code up by its '
              u'full number. Many codes relate to the ECM control unit, and the description often gives a sign, such as '
              u'"the engine may fail to start".',
    },
    'cumminsisf': {
        'ru': u'Cummins ISF 2.8 и 3.8 — {dealer} числовых кодов. Больше всего относятся к выпуску и AdBlue, воздуху и '
              u'топливу. Как и у ISB, номер короткий (111, 1117) и не является SPN, поэтому сверяйте его с описанием в '
              u'той же строке. Если в описании есть «ECM», записала внутреннюю неисправность блок управления, и код сам '
              u'по себе не говорит о датчике.',
        'en': u'Cummins ISF 2.8 and 3.8 have {dealer} numeric codes. Most concern the exhaust and AdBlue system, intake air '
              u'and fuel. As with the ISB, the number is short (111, 1117) and is not an SPN, so check it against the '
              u'description in the same row. If the description mentions the ECM, the control unit logged an internal '
              u'fault, and the code by itself does not point to a sensor.',
    },
    'cumminsislisc': {
        'ru': u'Cummins ISL и ISC — один из крупнейших наборов числовых кодов Cummins: {dealer}. Чаще всего встречаются '
              u'выпуск и AdBlue, топливо и впуск. Коды записаны четырьмя цифрами с ведущими нулями, например 0001, и '
              u'описывают датчики давления и температуры выхлопа. Перед заменой датчика проверьте, что код относится '
              u'именно к датчику, а не к блоку управления.',
        'en': u'Cummins ISL and ISC have one of the larger sets of numeric Cummins codes: {dealer}. The most common areas '
              u'are exhaust and AdBlue, fuel and intake. The codes are written as four digits with leading zeros, such as '
              u'0001, and describe the exhaust pressure and temperature sensors. Before you replace a sensor, check that '
              u'the code really points to the sensor and not to the control unit.',
    },
    'cumminsism': {
        'ru': u'Cummins ISM — {dealer} числовых кодов с трёх- и четырёхзначными номерами. Чаще всего встречаются выпуск '
              u'и AdBlue, топливо и смазка. Часть кодов относится к ECM и датчикам напряжения (ECM, датчики температуры '
              u'и давления), и в описании стоит признак, например «двигатель может не запускаться».',
        'en': u'Cummins ISM has {dealer} numeric codes with three- and four-digit numbers. The most common areas are the '
              u'exhaust and AdBlue system, fuel and lubrication. Some codes relate to the ECM and to voltage sensors (the '
              u'ECM, and temperature and pressure sensors), and the description gives a sign such as "the engine may fail '
              u'to start".',
    },
    'cumminsisx': {
        'ru': u'Cummins ISX — самый большой из блоков Cummins в дилерском разборе: {dealer}. Чаще всего встречаются '
              u'топливо, выпуск и AdBlue, CAN-шина и воздух. Коды короткие, например 111, 1117, 1119. Многие описывают '
              u'внутренний сбой блока управления, поэтому прежде чем менять датчик, проверьте, не записал ли код сам ECM.',
        'en': u'Cummins ISX is the largest of the Cummins units in the dealer table: {dealer}. The most common areas are '
              u'fuel, exhaust and AdBlue, the CAN bus and intake air. The codes are short, such as 111, 1117 and 1119. '
              u'Many describe an internal fault in the control unit, so before you replace a sensor, check whether the '
              u'ECM itself logged the code.',
    },
    'daewoo': {
        'ru': u'Tata Daewoo разобран дилерским форматом: {dealer}. Чаще всего встречаются электропитание и топливо. Код '
              u'записан парой чисел, например 1.1 и 1.2, а в описании иногда указан SPN, как у датчика температуры '
              u'охлаждающей жидкости (SPN 110). Если в описании есть SPN, страница этого SPN даст стандартное описание узла.',
        'en': u'Tata Daewoo is covered in the dealer format: {dealer}. The most common areas are the power supply and fuel. '
              u'The code is a pair of numbers, such as 1.1 and 1.2, and the description sometimes names an SPN, as in the '
              u'coolant temperature sensor (SPN 110). Where the description gives an SPN, that SPN\'s page gives the '
              u'standard description of the component.',
    },
    'deutz': {
        'ru': u'Deutz — дилерский разбор: {dealer}. По системам это в основном выпуск и AdBlue (SCR), топливо и воздух. '
              u'Коды вида 100.0 и 100.1 похожи на SPN и FMI, но таблица Deutz своя, поэтому смысл берите из описания. '
              u'Например, 100.0 — критическое превышение давления масла.',
        'en': u'Deutz has a dealer table: {dealer}. The most common areas are the exhaust and AdBlue system (SCR), fuel and '
              u'intake air. Codes such as 100.0 and 100.1 look like SPN and FMI, but the Deutz table has its own scheme, so '
              u'take the meaning from the description. For example, 100.0 is critical overpressure of the engine oil.',
    },
    'eaton': {
        'ru': u'Eaton Fuller — коробка передач, {dealer}. Чаще всего встречаются трансмиссия, электропитание и CAN. Коды '
              u'короткие, например 11, 12 и 13, и описывают блок управления переключением. Внутренняя неисправность блока '
              u'и ошибки питания в описаниях стоят рядом, поэтому сверяйте по строке.',
        'en': u'Eaton Fuller is a gearbox: {dealer}. The most common areas are transmission, the power supply and CAN. The '
              u'codes are short, such as 11, 12 and 13, and describe the shift controller. Internal faults in the unit and '
              u'supply errors sit next to each other in the descriptions, so check against the row.',
    },
    'eberspacher': {
        'ru': u'Eberspächer — автономный отопитель: {dealer}, коды вида 000 и 001. Чаще всего встречаются топливо и '
              u'охлаждение. Многие строки означают «ошибок нет», это нормальное состояние, а не сбой. Ищите строку с '
              u'ненулевым номером.',
        'en': u'Eberspächer is an independent heater: {dealer}, with codes such as 000 and 001. The most common areas are '
              u'fuel and cooling. Many rows mean "no faults", which is a normal state, not a failure. Look for the row '
              u'with a non-zero number.',
    },
    'faw': {
        'ru': u'FAW — {dealer} трёхзначных кодов вида 001 и 002. Чаще всего встречаются топливо, выпуск и CAN. В таблице '
              u'много описаний внешнего оборудования, например указателей поворота, и такие коды относятся к кузову, а '
              u'не к двигателю.',
        'en': u'FAW has {dealer} three-digit codes such as 001 and 002. The most common areas are fuel, exhaust and the CAN '
              u'bus. The table has many descriptions of external equipment, such as turn indicators; these codes concern the '
              u'body, not the engine.',
    },
    'fuso': {
        'ru': u'Mitsubishi Fuso — {dealer} кодов в формате P-кодов вида P0016, P0045 и P0046. Чаще всего встречаются '
              u'топливо, воздух и выпуск. Смысл записан в той же строке, поэтому сначала читайте описание, а общие P-коды '
              u'OBD-II используйте, когда описания нет.',
        'en': u'Mitsubishi Fuso has {dealer} in P-code form, such as P0016, P0045 and P0046. The most common areas are fuel, '
              u'intake air and exhaust. The meaning is written in the same row, so read the description first and use the '
              u'general OBD-II P-codes only when there is no description.',
    },
    'gaz': {
        'ru': u'ГАЗ — небольшая дилерская таблица: {dealer}. В основном воздух, топливо и охлаждение. Коды вида P0016 и '
              u'P0087 записаны по OBD-II, поэтому описание в строке и есть расшифровка. Если нужного кода нет, введите его '
              u'целиком в поиск на главной.',
        'en': u'GAZ has a small dealer table: {dealer}. Mostly intake air, fuel and cooling. Codes such as P0016 and P0087 '
              u'follow OBD-II, so the description in the row is the explanation. If the code you need is not there, type it '
              u'in full into the search on the homepage.',
    },
    'haldex': {
        'ru': u'Haldex ABS — {dealer}, и почти все они относятся к тормозам или электропитанию. Коды короткие: 00, 01, 02. '
              u'Код 00 означает, что ABS исправна при скорости выше 6 миль в час. Поэтому читайте номер вместе с описанием, '
              u'иначе нормальное состояние легко принять за неисправность.',
        'en': u'Haldex ABS has {dealer}, almost all of them about the brakes or the power supply. The codes are short: 00, '
              u'01, 02. Code 00 means the ABS is working correctly at a speed above 6 mph. So read the number together with '
              u'its description, or a normal state is easy to mistake for a fault.',
    },
    'hino': {
        'ru': u'Hino — {dealer} кодов в формате P0016, P0045 и аналогичных. Чаще всего встречаются топливо, выпуск, '
              u'воздух и электропитание. Коды синхронизации коленвала и распредвала, например P0016, разобраны подробно, и '
              u'при них сначала смотрите датчики положения, а не сам распредвал.',
        'en': u'Hino has {dealer} in the form P0016, P0045 and similar. The most common areas are fuel, exhaust, intake air '
              u'and the power supply. The crankshaft and camshaft timing codes, such as P0016, are described in detail, and '
              u'for them check the position sensors first, not the camshaft itself.',
    },
    'howo': {
        'ru': u'HOWO — {dealer} кодов, в основном топливо, электропитание и воздух. Коды P0088 и P0091 записаны по OBD-II. '
              u'В описании часто указан код мигания лампы, например 68 для давления в рампе, и по нему строку найти проще.',
        'en': u'HOWO has {dealer}, mostly fuel, the power supply and intake air. Codes P0088 and P0091 follow OBD-II. The '
              u'description often gives the flash code of the lamp, for example 68 for common-rail pressure, and the row is '
              u'easier to find with it.',
    },
    'hyundai': {
        'ru': u'Hyundai — {dealer}, в основном топливо и электропитание. Коды записаны по OBD-II, например P0072 и P0073 про '
              u'датчик температуры воздуха. Прежде чем менять датчик, смотрите описание: часто речь о слишком низком сигнале, '
              u'а не об отсутствии датчика.',
        'en': u'Hyundai has {dealer}, mostly fuel and the power supply. The codes follow OBD-II, for example P0072 and P0073 for '
              u'the intake air temperature sensor. Before replacing the sensor, read the description: it is often a signal '
              u'that is too low, not a missing sensor.',
    },
    'ivecoedc': {
        'ru': u'Iveco EDC — электронный дизель, {dealer} кодов вида 1.1 и 1.3. Чаще всего встречаются топливо, CAN и '
              u'электропитание. Код 1.1 относится к сигналу скорости: при нём отключаются тахограф и круиз-контроль, поэтому '
              u'относитесь к нему серьёзно.',
        'en': u'Iveco EDC is an electronically controlled diesel: {dealer}, with codes such as 1.1 and 1.3. The most common '
              u'areas are fuel, the CAN bus and the power supply. Code 1.1 concerns the speed signal: with it the tachograph '
              u'and cruise control switch off, so take it seriously.',
    },
    'ivecoeurotronic': {
        'ru': u'Iveco EuroTronic — коробка и её клапаны: {dealer}. Чаще всего встречаются трансмиссия, электропитание и '
              u'тормоза. Коды короткие, например 02 и 07, и описывают электроклапаны. Например, Y2 — управление делителем, '
              u'с замыканием на массу. Перед заменой клапана проверьте жгут и разъём клапанного блока.',
        'en': u'Iveco EuroTronic is the gearbox and its valves: {dealer}. The most common areas are transmission, the power '
              u'supply and brakes. The codes are short, such as 02 and 07, and describe solenoid valves; for example Y2 is '
              u'splitter control, with a short to earth. Before replacing a valve, check the harness and the valve block '
              u'connector.',
    },
    'jac': {
        'ru': u'JAC — один из самых больших дилерских разборов: {dealer}. Чаще всего встречаются топливо, воздух и выпуск. '
              u'В таблице есть коды подушки безопасности, например B0020, и они относятся к кабине, а не к двигателю. Для '
              u'двигательных неисправностей ищите P-коды вида P0030 и P0031.',
        'en': u'JAC has one of the largest dealer tables: {dealer}. The most common areas are fuel, intake air and exhaust. '
              u'The table includes airbag codes, such as B0020, which concern the cab rather than the engine. For engine faults, '
              u'look for P-codes such as P0030 and P0031.',
    },
    'jingwei': {
        'ru': u'Jingwei — отопитель, который ставят на SITRAK: {dealer}, коды вида E00 и E01. Чаще всего встречаются '
              u'охлаждение и электропитание. Коды описывают датчик пламени и цепь отопителя, поэтому при их появлении '
              u'смотрите отопитель, а не двигатель.',
        'en': u'Jingwei is a heater fitted to the SITRAK: {dealer}, with codes such as E00 and E01. The most common areas are '
              u'cooling and the power supply. The codes describe the flame sensor and the heater circuit, so when they appear, '
              u'check the heater, not the engine.',
    },
    'mahindra': {
        'ru': u'Mahindra — небольшой дилерский список: {dealer}, коды вида P0001 и P0003. Чаще всего встречаются топливо и '
              u'электропитание. Например, P0001 — обрыв нагрузки дозирующего блока: проверьте разъём блока, прежде чем менять '
              u'сам блок.',
        'en': u'Mahindra has a small dealer list: {dealer}, with codes such as P0001 and P0003. The most common areas are fuel '
              u'and the power supply. For example, P0001 is an open load on the metering unit: check the unit connector before '
              u'replacing the unit itself.',
    },
    'mercedes': {
        'ru': u'Mercedes-Benz записывает коды двумя способами. В бесплатном разборе {codes} по J1939: SPN и FMI идут парой. '
              u'Основная часть записей дилерская, {dealer}: коды из 4–7 знаков, например 0004 или MR 9961, а в описании '
              u'названы модель (Atego, Actros, Axor) и узел. Чаще всего встречаются датчики и электрические цепи, клапаны '
              u'и тормоза, давление и шина CAN. Сначала выясните, в каком формате ваш код: SPN с FMI ищите в бесплатной '
              u'таблице, а остальное — в дилерском разборе по описанию модели.',
        'en': u'Mercedes-Benz records codes in two ways. The free tables cover {codes} under J1939, where the SPN and the FMI '
              u'come as a pair. Most records are dealer records, {dealer}: codes of 4 to 7 characters, such as 0004 or MR 9961, '
              u'and the description names the model (Atego, Actros, Axor) and the component. The most common areas are sensors '
              u'and electrical circuits, valves and brakes, pressure and the CAN bus. First establish which format your code '
              u'is in: an SPN with its FMI is in the free table, and anything else is in the dealer list, where you match the '
              u'model in the description.',
    },
    'mwm': {
        'ru': u'MWM — {dealer} кодов вида P0105-01, где суффикс обозначает вариант неисправности. Чаще всего встречаются '
              u'топливо, электропитание и смазка. Датчики давления и температуры описаны по каждому варианту отдельно, '
              u'поэтому на суффикс тоже смотрите в описании.',
        'en': u'MWM has {dealer} such as P0105-01, where the suffix gives the variant of the fault. The most common areas are '
              u'fuel, the power supply and lubrication. Pressure and temperature sensors are described variant by variant, so '
              u'read the description for the suffix as well.',
    },
    'paccarmx13': {
        'ru': u'PACCAR MX-13 — {dealer} кодов, среди них P0016 и коды датчиков распредвала. Чаще всего встречаются топливо, '
              u'воздух, CAN и охлаждение. Номера записаны по OBD-II, а описание иногда содержит внутреннее обозначение '
              u'датчика, например F558, такой код сверяйте с проводкой.',
        'en': u'PACCAR MX-13 has {dealer}, among them P0016 and the camshaft sensor codes. The most common areas are fuel, '
              u'intake air, the CAN bus and cooling. The numbers follow OBD-II, but the description sometimes gives an internal '
              u'sensor label such as F558; check such a code against the wiring.',
    },
    'planar': {
        'ru': u'Planar — отопитель: {dealer}, коды вида 1, 10 и 11. Чаще всего встречаются CAN, топливо и электропитание. '
              u'Код 1 относится к теплообменнику отопителя, и при нём проблема в самом теплообменнике, а не в двигателе.',
        'en': u'Planar is a heater: {dealer}, with codes such as 1, 10 and 11. The most common areas are the CAN bus, fuel and '
              u'the power supply. Code 1 concerns the heat exchanger of the heater, so the fault is in the heat exchanger, not '
              u'the engine.',
    },
    'powerstroke': {
        'ru': u'Ford PowerStroke — {dealer} кодов в формате P0107 и P0108 (датчик барометрического давления). Чаще всего '
              u'встречаются топливо, электропитание, воздух и трансмиссия. Для датчика давления воздуха сначала смотрите его '
              u'питание и сигнал, а не блок целиком.',
        'en': u'Ford PowerStroke has {dealer} in the form P0107 and P0108 (the barometric pressure sensor). The most common '
              u'areas are fuel, the power supply, intake air and transmission. For the air pressure sensor, check its supply '
              u'and signal first, not the whole unit.',
    },
    'scania': {
        'ru': u'Scania — вторая по числу записей дилерская таблица на сайте: {dealer}. Коды короткие, например 1, 10 и 100, '
              u'а в описаниях стоят сокращения модулей: ACC, BWS, COO, CTS, ICL, VIS. Сначала найдите модуль по сокращению, '
              u'потом читайте описание. Чаще всего встречаются шина CAN, выпуск и AdBlue, топливо и электропитание.',
        'en': u'Scania has the second-largest dealer table on the site: {dealer}. The codes are short, such as 1, 10 and 100, '
              u'and the descriptions use module abbreviations: ACC, BWS, COO, CTS, ICL and VIS. Find the module from its '
              u'abbreviation first, then read the description. The most common areas are the CAN bus, exhaust and AdBlue, '
              u'fuel and the power supply.',
    },
    'shacman': {
        'ru': u'Shacman — {dealer} кодов, короткие номера вида 1, 10 и 100, а в описании, например, «ошибка напряжения в '
              u'расходомере впускного воздуха». Чаще всего встречаются шина CAN, топливо, выпуск и AdBlue. Короткий номер сам '
              u'по себе ничего не говорит, смысл в описании.',
        'en': u'Shacman has {dealer}, with short numbers such as 1, 10 and 100, and descriptions such as "intake air flow '
              u'sensor voltage fault". The most common areas are the CAN bus, fuel, exhaust and AdBlue. A short number on its '
              u'own says nothing; the meaning is in the description.',
    },
    'tata': {
        'ru': u'Tata Motors — {dealer} кодов шестизначного формата, например P000100 и P000300. Чаще всего встречаются '
              u'AdBlue, топливо, воздух и электропитание. Формат длинный, смысл записан в строке с описанием.',
        'en': u'Tata Motors has {dealer} in a six-digit format, such as P000100 and P000300. The most common areas are AdBlue, '
              u'fuel, intake air and the power supply. The format is long; the meaning is in the row with the description.',
    },
    'thermoking': {
        'ru': u'Thermo King — холодильная установка: {dealer}. Среди них много строк «ошибок нет», коды 0 и 00 — нормальное '
              u'состояние. Чаще всего встречаются охлаждение, электропитание и топливо. Ищите код с ненулевым номером и '
              u'смотрите описание в той же строке.',
        'en': u'Thermo King is a refrigeration unit: {dealer}. Many rows say "no alarms", and codes 0 and 00 are a normal state. '
              u'The most common areas are cooling, the power supply and fuel. Look for a code with a non-zero number and read '
              u'the description in the same row.',
    },
    'volkswagen': {
        'ru': u'Volkswagen — {dealer} кодов с косой чертой, например 0027/04: до косой номер неисправности, после — вид. '
              u'Чаще всего встречаются топливо, AdBlue, воздух и охлаждение. Например, 0027/04 — цепь положения клапана EGR '
              u'с напряжением ниже нормы.',
        'en': u'Volkswagen has {dealer} with a slash, such as 0027/04: the number before the slash is the fault number, and the '
              u'part after it is the type. The most common areas are fuel, AdBlue, intake air and cooling. For example, 0027/04 '
              u'is the EGR valve position circuit with voltage below normal.',
    },
    'webasto': {
        'ru': u'Webasto — отопитель: {dealer}, коды вида 00, 01 и 02. Чаще всего встречаются топливо, охлаждение и '
              u'электропитание. Как и у Eberspächer, нулевая строка означает «нет неисправностей», поэтому ищите код с '
              u'ненулевым номером.',
        'en': u'Webasto is a heater: {dealer}, with codes such as 00, 01 and 02. The most common areas are fuel, cooling and '
              u'the power supply. As with Eberspächer, the zero row means "no faults", so look for a code with a non-zero '
              u'number.',
    },
    'weichai': {
        'ru': u'Weichai (WP10 и WP12) — {dealer} кодов, в основном трёхзначные номера вида 111, 112 и 113. Чаще всего '
              u'встречаются топливо, электропитание и воздух. Некоторые описания прямо говорят «двигатель не запускается» '
              u'или «замените ECU», поэтому сначала читайте признак в описании.',
        'en': u'Weichai (WP10 and WP12) has {dealer}, mostly three-digit numbers such as 111, 112 and 113. The most common areas '
              u'are fuel, the power supply and intake air. Some descriptions say outright "engine will not start" or "replace the '
              u'ECU", so read the sign in the description first.',
    },
    'volvo': {
        'ru': u'У Volvo два формата. В бесплатном разборе {codes} по J1939, и это коды, у которых SPN совпадает со стандартом. '
              u'Основная часть записей Volvo дилерская, {dealer} вида B000101, где код собран из нескольких частей. Старые '
              u'грузовики Volvo записывают код через MID и PID, и такие коды разобраны отдельно, на странице блоков MID.',
        'en': u'Volvo has two formats. In the free tables there are {codes} under J1939, where the SPN matches the standard. Most '
              u'Volvo records are dealer records, {dealer} such as B000101, where the code is made of several parts. Older Volvo '
              u'trucks record the code through MID and PID; those codes are covered separately, on the MID module page.',
    },
    'volvomid': {
        'ru': u'Код Volvo здесь состоит из трёх частей: MID — какой блок записал неисправность, PID/SID — какой параметр или '
              u'узел, FMI — что с ним. Записей {dealer}, и чаще всего встречаются электропитание, шина CAN и выпуск. Чтобы '
              u'найти код, сначала выберите блок по MID, потом внутри блока параметр и FMI. Вид M128-P100.1 показывает все три '
              u'части сразу.',
        'en': u'A Volvo code here has three parts: the MID is the unit that logged the fault, the PID/SID is the parameter or '
              u'component, and the FMI is the fault type. There are {dealer}, and the most common areas are the power supply, the '
              u'CAN bus and exhaust. To find a code, pick the unit by its MID first, then the parameter and the FMI inside it. A '
              u'form such as M128-P100.1 shows all three parts at once.',
    },
}


PROBLEM_TEXT = {
    'gorit-check-engine': {
        'ru': u'Сама лампа не говорит о серьёзности: под ней может быть и забитый фильтр, и падение давления масла. '
              u'Первое действие — считать код сканером и записать его целиком, с номером SPN и FMI, а не только слово «ошибка». '
              u'Если лампа красная, не продолжайте движение, даже когда мотор работает ровно. Жёлтая лампа с кодом электрической '
              u'цепи обычно даёт время доехать до сервиса, но решать надо по коду, а не по цвету.',
        'en': u'The lamp alone does not show how serious it is: a clogged filter and falling oil pressure can both light it. '
              u'The first step is to read the code with a scanner and write it down in full, with the SPN and FMI, not just the '
              u'word "error". If the lamp is red, do not keep driving even if the engine runs smoothly. A yellow lamp with an '
              u'electrical circuit code usually leaves time to reach a service point, but decide by the code, not by the colour.',
    },
    'oshibka-adblue': {
        'ru': u'Больше половины ошибок по AdBlue дают пустой бак или реагент не того качества, поэтому начните с уровня в баке и '
              u'с марки жидкости. Если бак полный, проверьте датчик уровня и температуры, затем дозатор и линию подачи. Ошибка по '
              u'AdBlue быстро переводит систему в ограничение мощности, поэтому не продолжайте долгую поездку с пустым баком. Коды '
              u'дозирования и NOx обычно идут за ошибкой уровня, и разбирайте их по порядку, начиная с первого.',
        'en': u'More than half of AdBlue faults come from an empty tank or a reagent of the wrong quality, so start with the level '
              u'in the tank and the fluid grade. If the tank is full, check the level and temperature sensor, then the dosing unit '
              u'and the supply line. An AdBlue fault quickly moves the system into a power limit, so do not drive long distances with '
              u'an empty tank. Dosing and NOx codes usually follow the level error, so work through them in order, starting with the first.',
    },
    'upala-moshchnost': {
        'ru': u'Падение мощности почти всегда значит, что блок ограничил момент из-за другой неисправности. Прочитайте все коды '
              u'целиком и не стирайте их до разбора, потому что ограничение идёт за первопричиной. Если есть коды впуска, проверьте '
              u'воздушный фильтр и наддув, а если есть коды питания, начните с напряжения и массы. Падение мощности вместе с низким '
              u'давлением масла или перегревом — повод остановиться, не дожидаясь разбора.',
        'en': u'A loss of power almost always means the control unit has limited torque because of another fault. Read all the codes '
              u'in full and do not clear them before analysing them, since the limit follows the root cause. If there are intake codes, '
              u'check the air filter and the boost; if there are power supply codes, start with voltage and earth. A loss of power '
              u'together with low oil pressure or overheating is a reason to stop without waiting for a diagnosis.',
    },
    'belyy-dym': {
        'ru': u'Белый дым на холодном двигателе часто бывает конденсатом и уходит за несколько минут, а густой белый дым на прогретом '
              u'моторе говорит о попадании жидкости в камеру сгорания. Не доливайте охлаждающую жидкость, пока не поняли, куда она уходит. '
              u'Сначала проверьте уровень и состояние охлаждающей жидкости и масла, а также запах выхлопа. Если дым не уходит или двигатель '
              u'теряет обороты, остановитесь.',
        'en': u'White smoke on a cold engine is often condensation and clears within a few minutes; thick white smoke from a warm engine '
              u'points to liquid getting into the combustion chamber. Do not top up the coolant until you know where it is going. First '
              u'check the coolant and oil levels and their condition, and the smell of the exhaust. If the smoke does not clear or the engine '
              u'loses revs, stop.',
    },
    'bolshoy-rashod-topliva': {
        'ru': u'Большой расход топлива редко сопровождается одним понятным кодом: обычно причин несколько сразу. Сначала посмотрите, нет ли '
              u'кодов топливной системы, затем проверьте сливы форсунок, давление, фильтр и воздух на впуске. Если есть коды педали или '
              u'сигнала скорости, проверьте, не искажают ли они показания. Расход без других симптомов обычно не требует остановки, но новые '
              u'коды после него — повод для проверки.',
        'en': u'High fuel consumption rarely comes with one clear code; there are usually several causes at once. First check for fuel-system '
              u'codes, then the injector returns, the pressure, the filter and the intake air. If there are pedal or speed-signal codes, check '
              u'whether they distort the readings. Consumption without other symptoms usually does not require stopping, but new codes after '
              u'it are a reason to check.',
    },
    'chernyy-dym': {
        'ru': u'Чёрный дым означает, что топливо сгорает не полностью: не хватает воздуха, форсунки подают лишнее или сажевый фильтр забит. '
              u'Сначала проверьте воздушный фильтр и наддув, затем форсунки и давление топлива. Если дым появился на подъёме и мощность упала, '
              u'ехать дальше без проверки не стоит. Коды впуска и топлива обычно идут вместе, смотрите их парой.',
        'en': u'Black smoke means the fuel is not burning fully: there is not enough air, the injectors deliver too much, or the particulate '
              u'filter is blocked. First check the air filter and the boost, then the injectors and the fuel pressure. If the smoke appears on a '
              u'climb and power drops, do not carry on without a check. Intake and fuel codes usually come together, so read them as a pair.',
    },
    'datchik-nox': {
        'ru': u'Датчик NOx измеряет окислы азота в выхлопе, и ошибка по нему чаще относится к цепи датчика, чем к реальному выбросу. Сначала '
              u'осмотрите разъём датчика и жгут, особенно у выпускной трубы, где проводка греется. Затем проверьте, не связана ли ошибка с '
              u'AdBlue: дозирование влияет на показания. Коды SCR обычно идут вместе с датчиком, разбирайте их по порядку.',
        'en': u'The NOx sensor measures nitrogen oxides in the exhaust, and a fault on it is more often about the sensor circuit than an actual '
              u'emission. First inspect the sensor connector and the harness, especially near the exhaust pipe where the wiring gets hot. Then check '
              u'whether the fault is linked to AdBlue, because dosing affects the readings. SCR codes usually come with the sensor, so work '
              u'through them in order.',
    },
    'glohnet-na-hodu': {
        'ru': u'Двигатель, который глохнет на ходу, потерял питание, зажигание или подачу топлива, а не просто мощность. Сначала запишите все коды, '
              u'особенно электропитания и топливной системы, и отметьте, глох ли двигатель прогретым или холодным. Проверьте клеммы аккумулятора и '
              u'массу: обрыв питания даёт именно такую внезапную остановку. Не пытайтесь доехать с глохнущим двигателем, если он заглох снова, '
              u'вызывайте помощь.',
        'en': u'An engine that stalls while driving has lost power, ignition or fuel supply, not just output. First record all the codes, especially '
              u'the power supply and fuel-system ones, and note whether the engine stalled warm or cold. Check the battery terminals and the earth: a '
              u'supply break produces exactly this kind of sudden stop. Do not try to drive on with a stalling engine; if it stalls again, call for help.',
    },
    'gorit-lampa-abs': {
        'ru': u'Лампа ABS означает, что антиблокировка не работает, но обычные тормоза должны действовать. Сначала проверьте, не горит ли вместе с ней '
              u'лампа тормозов или давления, и запишите все коды тормозной системы. Если рядом горит красная лампа тормозов, не ездите, пока не '
              u'понятно, что с давлением. Чаще всего причина в датчике колеса или в питании блока ABS, поэтому первым делом проверьте разъёмы у колёс.',
        'en': u'The ABS lamp means anti-lock braking is not working, but the normal brakes should still work. First check whether a brake or pressure '
              u'lamp is lit with it, and record all the brake-system codes. If a red brake lamp is also on, do not drive until the pressure is '
              u'understood. The cause is most often a wheel sensor or the ABS unit power, so check the wheel connectors first.',
    },
    'greetsya-v-goru': {
        'ru': u'Перегрев на подъёме обычно значит, что системе охлаждения не хватает запаса: при нагрузке на малой скорости вентилятор и радиатор не '
              u'справляются. Сначала дайте двигателю остыть, затем проверьте уровень охлаждающей жидкости, пробку, ремень вентилятора и радиатор. Если '
              u'температура растёт и появляются коды охлаждения, не продолжайте подъём. Несколько кодов с датчиком температуры обычно связаны, их '
              u'разбирают вместе.',
        'en': u'Overheating on a climb usually means the cooling system has no reserve: under load at low speed the fan and radiator cannot keep up. '
              u'First let the engine cool, then check the coolant level, the cap, the fan belt and the radiator. If the temperature keeps rising and '
              u'cooling codes appear, do not continue the climb. Several codes with the temperature sensor are usually linked, so read them together.',
    },
    'nasos-adblue': {
        'ru': u'Насос AdBlue подаёт реагент из бака к дозатору, и ошибка по нему нередко идёт вслед за пустым баком или воздухом в линии. Сначала '
              u'проверьте уровень и качество жидкости, затем фильтр и линию подачи на подсос воздуха. Если насос шумит или не выходит на давление, '
              u'дальше разбирайтесь на сервисе, а не продолжайте ездить с ошибкой. Коды насоса и дозатора обычно идут парой, разбирайте их вместе.',
        'en': u'The AdBlue pump feeds reagent from the tank to the dosing unit, and a pump fault often follows an empty tank or air in the line. First '
              u'check the level and fluid quality, then the filter and the supply line for air leaks. If the pump is noisy or does not build pressure, '
              u'get it sorted at a service rather than carrying on with the fault. Pump and dosing codes usually come as a pair, so read them together.',
    },
    'ne-idet-regeneratsiya': {
        'ru': u'Регенерация сажевого фильтра не идёт, когда двигатель не выходит на нужный режим: короткие поездки, низкая температура выхлопа или '
              u'неисправен датчик давления на фильтре. Сначала проверьте, давала ли машина длительную поездку на скорости, и посмотрите коды датчиков '
              u'давления и температуры. Не выключайте двигатель во время регенерации, дайте процессу закончиться. Частые неудачные попытки могут '
              u'привести к забиванию фильтра, поэтому их лучше заметить сразу.',
        'en': u'Particulate filter regeneration does not start when the engine never reaches the right operating conditions: short trips, low exhaust '
              u'temperature, or a faulty filter pressure sensor. First check whether the truck has done a long run at speed, and look at the pressure and '
              u'temperature sensor codes. Do not switch the engine off during regeneration; let the process finish. Repeated failed attempts can lead to a '
              u'blocked filter, so spot them early.',
    },
    'ne-nabiraet-vozduh': {
        'ru': u'Двигатель, который не набирает воздух, — это проблема наддува или впуска: турбина, интеркулер, воздушный фильтр или трубки. Сначала '
              u'осмотрите воздушный фильтр и трубки наддува на трещины и подсос, затем проверьте датчик давления наддува. Если есть коды впуска и '
              u'давления, не нагружайте двигатель, пока не найдена потеря. Резкое падение мощности обычно сопровождается ограничением момента.',
        'en': u'An engine that does not build boost has a problem in the intake or the turbo: the turbocharger, intercooler, air filter or hoses. First '
              u'inspect the air filter and the boost hoses for cracks and leaks, then check the boost pressure sensor. If there are intake and pressure '
              u'codes, do not work the engine hard until the leak is found. A sudden loss of power is usually accompanied by a torque limit.',
    },
    'ne-pereklyuchayutsya-peredachi': {
        'ru': u'Если коробка не переключается, причина чаще всего в давлении воздуха или масла, в клапанах выбора или в электронике управления. '
              u'Сначала проверьте уровень масла в коробке и давление воздуха в системе, затем коды трансмиссии и питания блока управления. Если '
              u'переключение пропадает на ходу, не давите на рычаг силой, остановитесь в безопасном месте.',
        'en': u'If the gearbox will not shift, the cause is most often air or oil pressure, the selector valves or the control electronics. First check '
              u'the gearbox oil level and the air pressure in the system, then the transmission codes and the control-unit power. If shifting drops out '
              u'on the move, do not force the lever; stop in a safe place.',
    },
    'ne-rabotaet-motornyy-tormoz': {
        'ru': u'Моторный тормоз не работает, когда не получает команду или не может её выполнить: клапан, датчик положения или питание. Сначала проверьте, '
              u'включён ли тормоз в кабине и не стоит ли блокировка, затем коды клапана и питания. Без моторного тормоза спуски тяжелее для рабочих тормозов, '
              u'поэтому заранее планируйте маршрут. Если коды клапана идут вместе с кодами тормозов, сначала разбирайте тормоза.',
        'en': u'The engine brake does not work when it gets no command or cannot carry one out: the valve, a position sensor or the power supply. First '
              u'check that the brake is switched on in the cab and that no interlock is set, then the valve and power codes. Without the engine brake, '
              u'descents are harder on the service brakes, so plan the route ahead. If the valve codes come with brake codes, check the brakes first.',
    },
    'ne-zaryazhaet-generator': {
        'ru': u'Генератор не заряжает, когда напряжение бортовой сети падает при работающем двигателе. Сначала измерьте напряжение на клеммах аккумулятора '
              u'при работе двигателя, затем проверьте ремень генератора и затяжку клемм. Если генератор греется или шумит, остановитесь и проверьте его, '
              u'пока не сел аккумулятор. Коды электропитания обычно идут вместе с кодами генератора, разбирайте их вместе.',
        'en': u'The alternator is not charging when the on-board voltage drops with the engine running. First measure the battery terminal voltage with '
              u'the engine on, then check the alternator belt and the tightness of the terminals. If the alternator runs hot or noisy, stop and check it '
              u'before the battery goes flat. Power supply codes usually come with alternator codes, so read them together.',
    },
    'ne-zavoditsya': {
        'ru': u'Двигатель не заводится: либо нет питания для стартера и блока управления, либо нет топлива, либо блок не получает сигнал синхронизации. '
              u'Сначала проверьте напряжение аккумулятора и клеммы, затем уровень топлива и фильтр. Если стартер крутит, а двигатель не схватывает, смотрите '
              u'коды топливной системы и синхронизации. Если блок записал код, из-за которого двигатель не запускается, разберите его, а не крутите стартер подряд.',
        'en': u'The engine will not start: either there is no power for the starter and the control unit, or no fuel, or the control unit gets no timing '
              u'signal. First check the battery voltage and the terminals, then the fuel level and the filter. If the starter turns but the engine does not '
              u'catch, look at the fuel-system and timing codes. If the control unit has logged a code that stops the engine from starting, read it before '
              u'cranking again and again.',
    },
    'nizkoe-davlenie-masla': {
        'ru': u'Низкое давление масла — одна из самых опасных частых неисправностей: двигатель может выйти из строя за минуты. Сначала остановитесь и '
              u'заглушите двигатель, проверьте уровень масла щупом и осмотрите низ двигателя на течи. Не заводите, пока давление не восстановится, и не '
              u'продолжайте движение при красной лампе давления. Причину ищите уже после остановки: датчик, насос, перепускной клапан или сам уровень.',
        'en': u'Low oil pressure is one of the most dangerous common faults: the engine can be destroyed within minutes. First stop and switch the engine off, '
              u'check the oil level on the dipstick and look under the engine for leaks. Do not restart until the pressure is back, and do not drive with the '
              u'pressure lamp red. Look for the cause after stopping: the sensor, the pump, the bypass valve or the oil level itself.',
    },
    'oshibka-retardera': {
        'ru': u'Ошибка ретардера означает, что тормоз-замедлитель не получает команду или не выполняет её. Сначала проверьте, включён ли ретардер на панели, и '
              u'не горит ли при этом лампа тормозов. Если ретардер не работает, на спуске рассчитывайте только на рабочие тормоза и двигайтесь медленнее. '
              u'Коды клапана и питания обычно идут вместе, разбирайте их по очереди.',
        'en': u'A retarder error means the retarder brake does not get a command or does not carry it out. First check whether the retarder is switched on at '
              u'the panel and whether a brake lamp is lit with it. If the retarder does not work, rely only on the service brakes on a descent and drive more '
              u'slowly. Valve and power codes usually come together, so work through them one by one.',
    },
    'oshibka-tahografa': {
        'ru': u'Ошибка тахографа означает, что прибор не записывает данные или записывает их с перерывами. Сначала проверьте, не сорвана ли пломба и не отключён '
              u'ли датчик скорости, затем коды скорости. Можно ли ехать, решает код, а не сама ошибка тахографа, поэтому сверяйте его в поиске на главной.',
        'en': u'A tachograph error means the unit is not recording data, or records it with gaps. First check whether the seal is broken and whether the speed '
              u'sensor is disconnected, then the speed codes. Whether you can keep driving depends on the code, not on the tachograph error alone, so check the '
              u'code in the search on the homepage.',
    },
    'peregrev-dvigatelya': {
        'ru': u'Перегрев двигателя серьёзен, потому что головка блока и прокладки не выдерживают долгого перегрева. Сначала остановитесь и дайте двигателю '
              u'остыть, пробку на горячем не открывайте. Затем проверьте уровень охлаждающей жидкости, работу вентилятора и термостат. Если температура растёт '
              u'при нормальном уровне, ищите причину в датчике или в циркуляции. Продолжать движение нельзя, пока не понятно, почему двигатель перегревается.',
        'en': u'Engine overheating is serious, because the cylinder head and gasket cannot take prolonged heat. First stop and let the engine cool; do not open '
              u'the cap while it is hot. Then check the coolant level, the fan operation and the thermostat. If the temperature keeps rising with a normal level, '
              u'look for the cause in the sensor or the circulation. Do not keep driving until the reason for the overheating is clear.',
    },
    'problemy-s-toplivom': {
        'ru': u'Проблемы с топливом — вода в фильтре, воздух в линии или засор, и симптомы похожи: провалы, рывки, трудный запуск. Сначала слейте отстой из '
              u'фильтра и проверьте, нет ли в нём воды, затем ищите подсос воздуха в линии низкого давления. Если двигатель троит или глохнет под нагрузкой, '
              u'остановитесь. Коды топливной системы часто приходят парой, смотрите их вместе.',
        'en': u'Fuel problems — water in the filter, air in the line, or a blockage — give similar symptoms: dips, jerking, hard starting. First drain the '
              u'filter sump and check it for water, then look for an air leak on the low-pressure line. If the engine misfires or stalls under load, stop. '
              u'Fuel-system codes often come as a pair, so read them together.',
    },
    'probuksovyvaet-sceplenie': {
        'ru': u'Пробуксовка сцепления — когда обороты растут, а машина едет медленнее; это признак износа или проблемы с управлением. Сначала проверьте, не управляется '
              u'ли сцепление электроникой, и посмотрите коды трансмиссии. Если пробуксовка появилась резко под нагрузкой, не тяните тяжёлый груз, пока её не '
              u'разобрали. Коды сцепления и выбора передач обычно идут вместе.',
        'en': u'Clutch slip means the revs rise while the truck moves more slowly; it points to wear or a control problem. First check whether the clutch is '
              u'electronically controlled and look at the transmission codes. If the slip appears suddenly under load, do not pull a heavy load until it has '
              u'been checked. Clutch and gear-selection codes usually come together.',
    },
    'propalo-pitanie': {
        'ru': u'Пропало питание — внезапно отключаются блоки, и часто причина одна: обрыв на массе, пробой или сгоревший главный предохранитель. Сначала проверьте '
              u'клеммы аккумулятора и массу двигателя, затем главный предохранитель и реле. Если часть приборов работает, а часть нет, проследите цепь, которая '
              u'питает отсутствующие блоки. Коды электропитания идут группой, разбирайте их по порядку.',
        'en': u'Lost power means several units shut off at once, often from one cause: a broken earth, a short, or a blown main fuse. First check the battery '
              u'terminals and the engine earth, then the main fuse and the relays. If some units work and others do not, trace the circuit that feeds the missing '
              u'units. Power supply codes come as a group, so work through them in order.',
    },
    'siniy-dym': {
        'ru': u'Синий дым означает, что в камеру сгорания попадает масло: чаще всего это изношенные поршневые кольца, направляющие клапанов или сальники. Сначала '
              u'проверьте уровень масла и не вспенивается ли оно в картере, затем состояние воздушного фильтра и вентиляцию картера. Синий дым отличается от белого: '
              u'белый — пар или топливо, синий — масло. Если дым идёт вместе с падением давления масла, остановитесь.',
        'en': u'Blue smoke means oil is getting into the combustion chamber, most often through worn piston rings, valve guides or seals. First check the oil level and '
              u'whether the oil is foaming in the sump, then the air filter and the crankcase breather. Blue smoke is not the same as white smoke: white is steam or fuel, '
              u'blue is oil. If the smoke comes with falling oil pressure, stop.',
    },
    'stoyanochnyy-tormoz': {
        'ru': u'Стояночный тормоз удерживает машину на месте без водителя, и его коды касаются давления и электроники. Сначала проверьте давление в пневмосистеме и '
              u'положение рычага или кнопки, затем коды тормозов. Если стояночный тормоз не отпускается или не держит, не трогайтесь, пока не разберётесь. Коды '
              u'тормозной системы разбирайте вместе, а не по одному.',
        'en': u'The parking brake holds the truck in place without the driver, and its codes concern pressure and electronics. First check the air pressure in the '
              u'system and the position of the lever or switch, then the brake codes. If the parking brake will not release or will not hold, do not move off until '
              u'it is sorted. Read the brake-system codes together, not one at a time.',
    },
    'troit-dvigatel': {
        'ru': u'Троение двигателя — пропуски в одном или нескольких цилиндрах, и ощущается оно как дёргание на холостом ходу. Сначала по кодам и описанию определите, '
              u'один цилиндр или несколько работают плохо. Затем смотрите топливо: форсунки, фильтр, давление. Если троение появилось под нагрузкой и растёт, '
              u'остановитесь, пока не повредился катализатор. Коды топливной системы и синхронизации часто идут группой.',
        'en': u'A misfire means one or more cylinders are not firing; it is felt as a stumble at idle. First use the codes and their description to find out whether '
              u'one cylinder or several are affected. Then look at the fuel side: injectors, filter and pressure. If the misfire starts under load and gets worse, stop '
              u'before the catalytic converter is damaged. Fuel and timing codes often come as a group.',
    },
    'zabit-sazhevyy-filtr': {
        'ru': u'Забитый сажевый фильтр — следствие коротких поездок и неудачных регенераций. Сначала проверьте, давала ли машина длительную поездку на скорости, затем '
              u'коды давления на фильтре. Если засор растёт и появилось ограничение мощности, не откладывайте сервис и не продолжайте ездить с нарастающим засором.',
        'en': u'A blocked particulate filter is usually the result of short trips and failed regenerations. First check whether the truck has had a long run at speed, '
              u'then the pressure codes across the filter. If the blockage keeps growing and a power limit has appeared, do not put off the service and do not keep '
              u'driving with a growing blockage.',
    },
}


# ---------------------------------------------------------------------
# Дописанные страницы (образцы, 26.10). Только эти три страницы получают
# блоки из EXTRA_BLOCKS; остальные страницы этот словарь не читают.
# Ключ: 'brand:<марка>' (ru), 'problem:<slug>' (ru), 'code-en:<SPN>' (en).
# 'head' ставится сразу после вводного блока, 'tail' - в конец страницы.
# Элемент раздела: строка - абзац; список строк - маркированный список.
# [[адрес|текст]] - ссылка на страницу сайта. Числа, напряжения, моменты
# затяжки и цены здесь не указаны: только то, что верно для любого
# грузовика; конкретное значение - по руководству на машину.
EXTRA_BLOCKS = {
    'brand:wabco': {
        'head': [
            (u'Что это за система', [
                u'WABCO - поставщик тормозной электроники для большинства европейских и российских тягачей и прицепов. '
                u'Система ABS не даёт колёсам блокироваться при торможении, а ESC и ASR помогают удерживать машину на '
                u'дороге и трогаться без пробуксовки. Все эти функции держит один электронный блок, датчики и клапаны.',
                u'Коды в этом разделе относятся к блоку управления, датчикам колёс, модуляторам давления, реле и сети '
                u'между блоками. Тормозной механизм (колодки, барабаны, диски) в электронных кодах обычно не отражается, '
                u'поэтому код ABS не равен износу колодок.',
            ]),
            (u'Где стоит', [
                u'Блок управления обычно закреплён на раме или в кабине рядом с осью, на которой стоит модулятор. '
                u'Датчики колёс установлены у ступиц: каждое колесо имеет свой датчик, он считывает скорость вращения по '
                u'зубчатому кольцу (реластору) на ступице или валу. Модуляторы стоят на пневмолиниях у осей и открывают или '
                u'закрывают давление в каждом тормозном канале.',
                u'На прицепе связь с тягачом идёт через разъём ISO 7638 (с несколькими контактами). Через него прицеп '
                u'получает питание для своего блока ABS и обменивается сигналами с тягачом. Загрязнённый или окисленный '
                u'разъём на прицепе часто даёт коды, которые выглядят как поломка колеса.',
            ]),
            (u'Как работает', [
                u'Блок сравнивает скорость всех колёс. Если одно колесо начинает тормозить резче остальных и готово '
                u'заблокироваться, блок через модулятор сбрасывает давление в его тормозной камере, затем возвращает. '
                u'Так колесо остаётся на грани сцепления. Когда датчик или клапан выходит из строя, блок записывает код '
                u'и отключает ту часть, которую не может контролировать.',
                u'При отказе ABS обычное пневматическое торможение остаётся: педаль работает, но защиты от блокировки '
                u'колёс уже нет. ESC и ASR при этом обычно тоже отключаются, и машина становится менее устойчивой на '
                u'скользкой дороге или в повороте.',
            ]),
            (u'Типовые причины и признаки', [
                [u'Повреждённый датчик колеса: обрыв провода, попадание грязи или воды, трещина корпуса.',
                 u'Повреждённое зубчатое кольцо: сколы, налипший металл, биение. Датчик исправен, а сигнал пропадает.',
                 u'Жгут и разъёмы: перетёртый провод рядом с колодкой, окисленные контакты, плохая масса.',
                 u'Модулятор, который залип или не отвечает на команду блока.',
                 u'Питание блока: низкое напряжение бортовой сети или плохой контакт на клемме даёт сразу несколько кодов.',
                 u'Сеть CAN (J1939): если блок перестал видеть двигатель или приборную панель, в считывании появляется '
                 u'код сети вместе с кодами ABS. Тогда ищите причину в сети, а не в колёсах.'],
                u'Признаки для водителя: горит жёлтая лампа ABS, иногда лампа ESC или ASR, на приборах может мигать '
                u'значок отключения. Если рядом горит красная лампа тормозов, это уже не только ABS.',
            ]),
            (u'Порядок проверки', [
                u'1. Считайте все коды сканером, включая кадр стоп-данных (условия, при которых код записался). '
                u'Запишите коды целиком, с SPN и FMI. Коды питания и сети проверяются раньше датчиков.',
                u'2. Проверьте напряжение аккумуляторов и массу блока под нагрузкой. Просадка питания часто даёт '
                u'несколько кодов сразу.',
                u'3. Осмотрите разъёмы блока, датчиков и модуляторов, жгут у оси и у рамы. Перетёртые и окисленные места '
                u'найдутся быстрее, чем тестером.',
                u'4. Датчик колеса проверяется по руководству на эту ось: сопротивление обмотки, зазор до кольца и '
                u'сигнал при вращении. Конкретные значения в справочнике не приводятся, берите их из руководства на машину.',
                u'5. Для прицепа отдельно проверьте разъём ISO 7638 и контакты в нём. Затем очистите коды и проверьте '
                u'через две-три поездки в обычном режиме, не полагаясь на один запуск.',
            ]),
            (u'Что делать водителю в рейсе', [
                u'Если горит только жёлтая лампа ABS, а тормоза держат как обычно, можно доехать до сервиса, но '
                u'аккуратнее: на мокром или скользком покрытии не рассчитывайте на защиту от блокировки. Если горит красная '
                u'лампа тормозов, давление падает или педаль ведёт себя необычно, остановитесь в безопасном месте.',
                u'По таблице этого справочника коды датчиков и модуляторов колёс отнесены к тем, с которыми ехать нельзя. '
                u'Это не диагноз, а предупреждение: без проверки на месте такую машину в рейс лучше не пускать. '
                u'Не сбрасывайте коды несколько раз подряд, пока не нашли причину.',
            ]),
            (u'Что делать мастеру в сервисе', [
                u'Сначала проверьте питание, массу и разъёмы, и только потом меняйте датчики или модуляторы. Заменённый '
                u'датчик без устранения причины в жгуте даёт тот же код через неделю. После замены датчика или блока часто '
                u'нужна калибровка или обучение системы, это указано в руководстве производителя на конкретную машину.',
                u'Сверьте коды, записанные на машине: код сети CAN, код питания и код конкретного колеса вместе говорят о '
                u'корневой причине. По одному коду колеса деталь ставить не стоит. Связанные коды ниже помогут разобрать такой набор.',
            ]),
            (u'Связанные коды и страницы', [
                [u'[[/kody/spn-627.html|SPN 627 - источник питания]]',
                 u'[[/kody/spn-629.html|SPN 629 - контроллер №1]]',
                 u'[[/kody/spn-639.html|SPN 639 - сеть J1939 №1]]',
                 u'[[/kody/spn-789.html|SPN 789 - датчик колеса ABS, ось 1, слева]]',
                 u'[[/kody/spn-806.html|SPN 806 - клапан ASR, дифференциал 1]]'],
                u'Если жёлтая лампа ABS горит без кодов колёс, см. [[/problemy/gorit-lampa-abs.html|разбор лампы ABS]].',
            ]),
        ],
        'tail': [
            (u'Вопросы и ответы', [
                (u'Можно ли ехать с горящей лампой ABS?',
                 u'Если тормоза работают обычно и красной лампы нет, можно доехать до сервиса с осторожностью. Защиты от '
                 u'блокировки и ESC при этом может не быть. Если код относится к колёсам, по таблице справочника такую '
                 u'машину лучше не пускать в рейс без проверки.'),
                (u'Почему ошибка ABS появилась только с прицепом?',
                 u'Чаще всего это разъём ISO 7638, его контакты или питание прицепа, а тягач при этом исправен. Проверьте '
                 u'разъём на прицепе и тягаче, прежде чем менять датчики.'),
                (u'Код остался после замены датчика, что делать?',
                 u'Проверьте жгут и разъём этого датчика, зубчатое кольцо и зазор. Если всё исправно, нужна калибровка или '
                 u'обучение системы по руководству. Иначе код вернётся.'),
                (u'Нужно ли сразу менять блок ABS?',
                 u'Нет. Блок меняют, когда исключены питание, масса, сеть и проводка и когда сам блок подтверждён '
                 u'диагностикой по руководству производителя.'),
            ]),
        ],
    },
    'problem:datchik-nox': {
        'head': [
            (u'Что это за датчик', [
                u'Датчик NOx - керамический датчик в выхлопе, который измеряет окислы азота. Система SCR по этим данным '
                u'понимает, насколько хорошо работает нейтрализатор и правильно ли дозируется AdBlue. Поэтому датчик часто '
                u'стоит до и после SCR-нейтрализатора: один показывает, что пришло, другой - что ушло.',
                u'Ошибка по датчику не всегда означает, что машина сильно загрязняет воздух. Чаще датчик даёт неверный '
                u'сигнал из-за своей цепи, нагрева, копоти или из-за показаний, искажённых дозированием. Поэтому разбирайте '
                u'коды по порядку, а не меняйте датчик сразу.',
            ]),
            (u'Где стоит и как устроен', [
                u'Датчик ввинчен в выпускную трубу или корпус нейтрализатора и работает при высокой температуре. Внутри есть '
                u'нагреватель, который выводит датчик на рабочий режим. Пока он не прогрет, показания не считаются надёжными, '
                u'поэтому коды часто появляются при холодном запуске или сразу после него.',
                u'Разъём и жгут идут близко к выпускной трубе, где проводка греется, вибрирует и может натираться. Многие '
                u'обрывы и плохие контакты находятся именно здесь, а не в самом датчике.',
            ]),
            (u'Типовые причины и признаки', [
                [u'Повреждение жгута или разъёма у выпускной трубы: перегрев изоляции, перетёртый провод, влага.',
                 u'Неисправность нагревателя датчика: датчик не выходит на рабочий режим.',
                 u'Загрязнение керамики копотью, маслом или отложениями, в том числе после сбоев в дозировании AdBlue.',
                 u'Протечка в выхлопе до датчика: подсос воздуха искажает показания.',
                 u'Неисправность AdBlue: пустой бак, некачественный реагент, засорённая форсунка или насос дозирования '
                 u'(см. [[/problemy/oshibka-adblue.html|разбор ошибки AdBlue]] и [[/problemy/nasos-adblue.html|разбор насоса AdBlue]]).',
                 u'Старый датчик: со временем показания уходят, и система начинает считать их недостоверными.'],
                u'Признаки для водителя: лампа Check Engine или значок AdBlue/SCR, на приборах может появиться '
                u'предупреждение о снижении мощности. Часто ошибка появляется после длительной стоянки или при холодном запуске.',
            ]),
            (u'Порядок проверки', [
                u'1. Считайте коды с кадром стоп-данных: температуру выхлопа, режим работы, время после запуска. Если ошибка '
                u'появляется только на холоде, это признак нагревателя или проводки.',
                u'2. Осмотрите разъём датчика и жгут у выпускной трубы: натирание, копоть, влага. Разъём должен быть сухим и '
                u'плотно сидеть.',
                u'3. Проверьте, нет ли протечек выхлопа до датчика. Подсос воздуха даёт ложные показания без всякой поломки '
                u'самого датчика.',
                u'4. Проверьте уровень и качество AdBlue, работу дозатора и отсутствие засора. Коды SCR обычно идут вместе '
                u'с датчиком, поэтому разбирайте их по порядку.',
                u'5. Питание и сигнал датчика проверяйте по схеме и значениям из руководства на конкретный двигатель. '
                u'Общих цифр здесь нет, потому что они зависят от производителя датчика.',
                u'6. Датчик меняйте, когда проводка и AdBlue исключены и датчик подтверждён диагностикой. После замены во '
                u'многих машинах нужно обучение или калибровка.',
            ]),
            (u'Что делать водителю в рейсе', [
                u'Если горит только значок AdBlue или SCR без других ошибок, можно ехать к сервису, но не откладывайте визит: '
                u'при длительной ошибке система может ограничить мощность. Проверьте уровень AdBlue в баке.',
                u'Если горит красная лампа, мощность заметно упала или машина перешла в режим ограничения, остановитесь, '
                u'когда это безопасно, и вызовите помощь. Если код в таблице справочника отнесён к «ехать нельзя», решение '
                u'принимает мастер по коду, а не по цвету лампы.',
            ]),
            (u'Что делать мастеру в сервисе', [
                u'Сначала прочитайте стоп-данные и историю ошибок. Посмотрите, идёт ли ошибка вместе с кодами AdBlue, '
                u'дозирования и температуры. Если да, искать причину нужно в системе дозирования, а не в датчике.',
                u'Датчик и проводку проверяйте по схеме на конкретную марку и двигатель. Удаление датчика, отключение SCR '
                u'или стирание кодов без поиска причины не решают проблему: ошибка вернётся, а выбросы будут выше нормы, что '
                u'может стать проблемой на техосмотре.',
            ]),
            (u'Связанные страницы', [
                u'[[/problemy/oshibka-adblue.html|Ошибка AdBlue]] - если в считывании есть коды бака и дозирования.',
                u'[[/problemy/ne-idet-regeneratsiya.html|Не идёт регенерация]] - если датчик связан с сажевым фильтром.',
                u'[[/problemy/zabit-sazhevyy-filtr.html|Забит сажевый фильтр]] - если давление и температура фильтра влияют на показания.',
            ]),
        ],
        'tail': [
            (u'Вопросы и ответы', [
                (u'Сразу ли менять датчик NOx?',
                 u'Нет. Сначала проверьте разъём, жгут, протечки выхлопа и AdBlue. Датчик меняют, когда эти причины исключены.'),
                (u'Можно ли ехать с ошибкой датчика NOx?',
                 u'Если лампа не красная и мощность не падает, можно доехать до сервиса. При красной лампе или сильном '
                 u'ограничении мощности остановитесь и вызовите помощь.'),
                (u'Почему ошибка появляется только зимой?',
                 u'Датчик выходит на рабочий режим не сразу, а конденсат и холодный выхлоп дают искажения. Если ошибка уходит '
                 u'после прогрева, проверьте нагреватель датчика и разъём, который может намокать.'),
                (u'Можно ли отключить датчик, чтобы ошибка не мешала?',
                 u'Нет. Отключение датчика или системы SCR без законной причины нарушает требования к выбросам и ведёт к '
                 u'проблемам на техосмотре. Ошибка при этом не исчезает, а причина остаётся.'),
            ]),
        ],
    },
    'code-en:97': {
        'head': [
            (u'What this code means', [
                u'SPN 97 is the water-in-fuel indicator. A sensor sits in the water separator (the sedimenter of the coarse '
                u'fuel filter) and tells the engine computer when water collects at the bottom of the bowl. The engine '
                u'computer then turns on a warning, and on some engines it reduces power.',
                u'Water is the enemy of the fuel system. It does not burn, so it causes poor combustion, rust inside the fuel '
                u'pump and injectors, and it can feed microbial growth in the tank that clogs the filters. This is why the '
                u'code should be taken seriously even when the engine runs normally.',
                u'The second half of the code, the FMI, tells you what the sensor reports. FMI 3 and FMI 4 point to a problem '
                u'in the sensor circuit (voltage too high or too low). FMI 15 to 18 mean that water has been detected, from the '
                u'least serious level to the most serious. The table below shows the exact wording for each make.',
            ]),
            (u'What to do on the road', [
                u'If the light comes on while the engine runs normally, drain the separator at the first safe stop, provided '
                u'you have a drain valve, a clear container and the right tools. Water settles at the bottom, so drain until '
                u'clean fuel comes out, not just a few drops.',
                u'If the engine loses power, stumbles or starts badly, stop as soon as it is safe and call for help. Note where '
                u'you last refuelled. If the code comes back after draining, or the water returns within a day or two, do not '
                u'keep driving on that fuel: go to a service point.',
            ]),
            (u'What to check in the workshop', [
                u'Check the sensor connector and the wiring first, using the wiring diagram for the make. Corrosion at the '
                u'connector at the bottom of the filter is a common cause. Clean the sensor electrodes; a dirty sensor can give '
                u'a false reading.',
                u'Drain the separator and the tank sediment, then inspect the bowl for cracks. Check the tank breather and the '
                u'filler cap: a damaged cap or breather lets in water through condensation as the temperature changes. Ask where '
                u'the fuel was bought, because many water cases come from one bad delivery.',
                u'Replace the filter element as the service schedule says, not only when a code appears. In winter the water in '
                u'the bowl can freeze and block the drain: warm it up, and do not replace the sensor just because the reading is wrong.',
                u'Replace the sensor only after the connector, the wiring and the separator are confirmed good, and check the '
                u'manufacturer manual for any reset or calibration after replacement.',
            ]),
            (u'Related codes and pages', [
                u'[[/en/kody/spn-94.html|SPN 94 - Fuel delivery pressure]] - if the fuel supply is also weak.',
                u'[[/en/kody/spn-95.html|SPN 95 - Fuel Filter Differential Pressure]] - if the filter is clogged after water or dirt.',
                u'[[/en/problemy/problemy-s-toplivom.html|Fuel problems: symptoms and what to check]]',
            ]),
        ],
        'tail': [
            (u'Questions and answers', [
                (u'Can I keep driving with SPN 97 on?',
                 u'If the engine runs normally and there is no red lamp or power loss, you can drive to a service point, but '
                 u'drain the separator first if you can. If the engine loses power or stumbles, stop.'),
                (u'The light goes off after draining. Is the fuel fine now?',
                 u'Not necessarily. Water often comes back from the tank, so check the tank sediment and the breather, and '
                 u'refuel at a trusted station.'),
                (u'Do I need a new sensor?',
                 u'Usually not first. Check the connector, the wiring and the separator bowl. Replace the sensor only when they are good.'),
                (u'Why does the code appear in winter?',
                 u'Water in the bowl can freeze and block the drain, and the sensor can read wrongly while it is cold. Warm the '
                 u'bowl and check the drain before changing parts.'),
            ]),
        ],
    },
}
