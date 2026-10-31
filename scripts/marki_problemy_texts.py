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
        'ru': u'У Ford Trucks и Ecotorq номер записан по собственной схеме, а не как SPN по J1939: до точки — номер '
              u'неисправности, записанный цифрами (ведущие нули есть не у всех), после точки — её вид, цифрами и буквами '
              u'A–F, например 6.1F. Записей {codes}, и все они собраны на одной странице, с заводским описанием у каждого '
              u'номера. Номер, совпавший с SPN на другой странице, означает другое, поэтому ищите код по полному номеру '
              u'из считывания, а не по SPN.',
        'en': u'Ford Trucks and Ecotorq record the number in their own scheme, not as a J1939 SPN: before the dot is the '
              u'fault number in digits (leading zeros are not on every code), after the dot is the fault type in digits '
              u'and letters A–F, for example 6.1F. There are {codes}, all gathered on this page with the factory '
              u'description for each number. A number that matches an SPN on another page means something else, so look '
              u'the code up by its full number from the reading, not by an SPN.',
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
        'ru': u'Eberspächer — автономный отопитель: {dealer}, коды вида 000, 004 и 011 (таблица Airtronic D2/D4; коды Hydronic '
              u'помечены). Чаще всего встречаются свеча накаливания, нагнетатель, напряжение питания и датчики. Многие строки означают «ошибок нет», это нормальное состояние, а не сбой. Ищите строку с '
              u'ненулевым номером.',
        'en': u'Eberspächer is an independent heater: {dealer}, with codes such as 000, 004 and 011 (the Airtronic D2/D4 table; '
              u'Hydronic codes are marked). The most common areas are the glow plug, the blower, the supply voltage and sensors. Many rows mean "no faults", which is a normal state, not a failure. Look for the row '
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
        'ru': u'Planar — отопитель: {dealer}, коды вида 1, 10 и 11. Номер бывает двух систем: код таблицы ремонта или число '
              u'миганий пульта ПУ-5, поэтому в каждой записи указано, какая система. Чаще всего встречаются перегрев, нагнетатель, '
              u'топливный насос, свеча и связь пульта с блоком. Код 1 относится к теплообменнику отопителя, и при нём проблема в самом теплообменнике, а не в двигателе.',
        'en': u'Planar is a heater: {dealer}, with codes such as 1, 10 and 11. A number comes from one of two systems: a repair-table '
              u'code or the blink count of the PU-5 remote, so each entry says which. The most common areas are overheating, the blower, '
              u'the fuel pump, the glow plug and the remote link. Code 1 concerns the heat exchanger of the heater, so the fault is in the heat exchanger, not '
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
        'ru': u'Webasto — отопитель: {dealer}: ПК-коды программы Webasto Thermo Test вида 00, 01 и 02 и F-коды таймера '
              u'F00-F19. Это две разные системы, соответствие между ними указано в каждой записи. Как и у Eberspächer, нулевая строка означает «нет неисправностей», поэтому ищите код с '
              u'ненулевым номером.',
        'en': u'Webasto is a heater: {dealer}: PC codes of the Webasto Thermo Test program such as 00, 01 and 02, and timer F-codes '
              u'F00-F19. These are two different systems; the match between them is given in each entry. As with Eberspächer, the zero row means "no faults", so look for a code with a non-zero '
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
                u'На тягаче блок управления обычно стоит в кабине, на прицепе — на раме, часто вместе с модулятором. '
                u'Датчики колёс установлены у ступиц: каждое колесо имеет свой датчик, он считывает скорость вращения по '
                u'импульсному (зубчатому) кольцу на ступице или валу. Модуляторы стоят на пневмолиниях у осей и открывают или '
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
                u'The second half of the code, the FMI, tells you what the sensor reports. FMI 3 and FMI 4 point to the sensor '
                u'circuit: voltage above normal or shorted high (3), voltage below normal or shorted low (4). When water is actually '
                u'detected, the FMI shows how serious it is, and the exact number depends on the make: for example FMI 15 or 16 on many engines, and FMI 18 (critical level) on some DAF engines. '
                u'The table below shows the exact wording for each make.',
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


# Партия 1: 10 марок и 2 проблемы. Дописывается в marki_problemy_texts.py
# через EXTRA_BLOCKS.update(...). Числа не указаны; ссылки - только на существующие адреса.

EXTRA_BLOCKS.update({

    "brand:kamaz": {
        "head": [
            ("Что здесь разобрано", [
                "Коды КамАЗ на этой странице идут из нескольких источников, и читать их одной таблицей нельзя. Двигатель записан по стандарту J1939: номер узла (SPN) и вид неисправности (FMI) всегда стоят парой. Блок КамАЗ-5490 записан по протоколу K-line, а не по J1939, поэтому его список стоит отдельно. Совпадение номера с SPN из другой таблицы здесь ничего не значит.",
                "Двигатель Cummins ISB 6.7 и тормозная система EBS3 WABCO тоже разнесены по своим блокам. Если код пришёл из одного блока, ищите его в разделе этого блока. Один и тот же номер в другом блоке может означать другое, поэтому общая таблица здесь не помощник.",
            ]),
            ("Тормоза, ретардер и коробка", [
                "Тормозные коды EBS3 разобраны в отдельном блоке, и связаны они одновременно с пневматикой и электроникой. Прежде чем менять блок, проверьте давление в контурах, утечки и разъёмы по схеме. Во многих случаях код появляется из-за воздуха, а не из-за самого блока.",
                "Ретардер ZF Intarder и коробка ZF AS-Tronic тоже стоят отдельно. Отказ коробки не говорит о двигателе, и наоборот: смотрите, какой блок записал код. Если в считывании одновременно есть код стояночного тормоза и код давления воздуха, сначала остановитесь и проверьте тормоза на месте.",
            ]),
            ("Что стоит в начале списка", [
                "В начале разбора двигателя идут коды вентилятора охлаждения, давления воздуха в тормозном контуре, частоты вращения вентилятора, температуры окружающего воздуха и скорости по датчикам. Сами по себе они редко означают серьёзную поломку, но показывают, где искать. Если вентилятор не выходит на заданный режим, смотрите и привод, и датчик оборотов.",
                "Датчик скорости влияет сразу на несколько систем. Его обрыв или загрязнение даёт ложные данные в приборах и в тормозной электронике, поэтому при одном таком коде не спешите менять блоки. Сначала проверьте разъём датчика и жгут до блока.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите каждый код целиком, с SPN, FMI и блоком-источником. Запишите условия, при которых код появился: обороты, температуру, режим движения. Это кадр стоп-данных, без него разбор идёт вслепую.",
                "2. Коды с FMI 3, 4, 5 и 6 почти всегда касаются электрической цепи. Начните с разъёма, жгута и массы у датчика, и только потом меняйте сам датчик.",
                "3. Коды давления воздуха проверяйте по пневматической схеме: утечки в соединениях, осушитель, клапаны. Давление смотрите на прогретой машине и по методике руководства.",
                "4. Блинк-коды Евро-3 с блоком Bosch MS 6.1 считываются миганием лампы и описаны отдельным разделом на этой странице. Миганием не заменяется сканер: результат сверяйте с руководством.",
                "5. Коды K-line и блока КамАЗ-5490 читаются только инструментом с поддержкой этого протокола. Если сканер их не видит, это не значит, что код пропал.",
                "6. Очищайте коды только после устранения причины и проверяйте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "Если горит красная лампа или в считывании есть код из списка «с этими кодами ехать нельзя», не продолжайте движение. На этой странице к таким относятся уровень и давление масла, температура и уровень охлаждающей жидкости, температура масла и стояночный тормоз. Не доливайте жидкости на ходу в надежде доехать.",
                "Жёлтый код вентилятора или датчика скорости обычно позволяет доехать до сервиса. Следите за температурой двигателя: при первом признаке перегрева остановитесь раньше, чем это станет серьёзно.",
            ]),
            ("Мастеру в сервисе", [
                "Работайте блок за блоком. Сначала определите, какой блок записал код, затем читайте таблицу именно этого блока. Замена блока ради одного кода без проверки питания, массы и жгута почти всегда возвращает ту же ошибку.",
                "Для тормозных кодов сверяйте пневматику и электронику вместе. Записывайте результаты замеров при одинаковых условиях: повторяющийся сбой на одном замере не виден, а в записях видно сразу.",
            ]),
            ("Связанные страницы", [
                "[[/marki/wabco.html|Тормозная электроника WABCO - отдельная страница]]",
                "[[/marki/cumminsisb.html|Двигатель Cummins - отдельная страница]]",
                "[[/marki/zfastronic.html|ZF AS-Tronic]]",
                "[[/problemy/ne-zaryazhaet-generator.html|Не заряжает генератор]], [[/problemy/nizkoe-davlenie-masla.html|низкое давление масла]], [[/problemy/peregrev-dvigatelya.html|перегрев двигателя]], [[/problemy/gorit-check-engine.html|горит Check Engine]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Блинк-код не совпадает с кодом из таблицы. Что делать?",
                 "Блинк-коды и SPN/FMI - разные системы записи. Сверяйте блинк-код с его разделом и руководством на машину, а не с таблицей SPN на этой странице."),
                ("Почему код стояночного тормоза стоит в списке «ехать нельзя»?",
                 "В таблице этой страницы такой код отнесён к «ехать нельзя». Это правило справочника: не продолжайте движение, пока мастер не проверит тормоз."),
                ("Код ушёл после чистки. Значит, всё исправно?",
                 "Не обязательно. Если причина осталась, код вернётся. Проверьте повтор на ходу и смотрите кадр стоп-данных при следующей записи."),
                ("Нужно ли менять блок КамАЗ-5490, если код один?",
                 "Нет. Сначала проверьте разъём, питание и массу блока, затем делайте проверку по руководству на конкретный автомобиль."),
            ]),
        ],
    },

    "brand:maz": {
        "head": [
            ("Какие группы на странице", [
                "Коды МАЗ разложены по системам: смазка, охлаждение, топливная система, впуск и наддув, выпуск и AdBlue, электропитание, CAN-шина, тормоза и прочие системы. Самые большие группы здесь топливо, впуск и наддув, а также электропитание. Значит, при неустойчивой работе двигателя проверку лучше начинать с топлива и воздуха, а не с блока.",
                "Общие коды записаны по J1939: номер узла и вид неисправности идут вместе. Если SPN совпадает с кодом из считывания, а FMI другой, это уже другая неисправность. Читайте код целиком.",
            ]),
            ("Что идёт первым в списке", [
                "В начале разбора стоят управление клапаном рециркуляции (EGR), команда привода дроссельной заслонки, положение дроссельной заслонки, температура воздуха во впускном коллекторе и драйвер подогревателя воздуха. Все они связаны с тем, как двигатель дышит: сколько воздуха поступает, как он подогревается на холодном пуске и сколько выхлопа возвращается в цилиндры.",
                "Коды впуска часто означают не поломку датчика, а то, что воздух идёт не так, как задумано. Засорённый фильтр, подсос после турбины и неплотные патрубки дают похожую картину. Проверьте подсос, прежде чем винить датчик.",
            ]),
            ("Топливо и электропитание", [
                "Топливная система - вторая по размеру группа на этой странице. Чаще всего это подача топлива, засорённый фильтр и воздух в линии. Прежде чем менять форсунку или насос, проверьте, нет ли воды в фильтре и не подсасывает ли воздух на всасывающей стороне.",
                "Группа электропитания связана с тем, что многие датчики получают питание от блока. Просевшее напряжение и плохая масса дают сразу несколько кодов. Сначала посмотрите клеммы аккумулятора и массу двигателя, затем предохранители и реле.",
            ]),
            ("Порядок проверки", [
                "1. Запишите кадр стоп-данных и отметьте, работал ли двигатель на холоде или прогретым.",
                "2. Сверьте SPN и FMI с таблицей группы. Если код из группы впуска, начните с воздухозаборника и патрубков.",
                "3. Проверьте разъёмы и жгут датчика. Для кодов с электрическими FMI это первый шаг.",
                "4. Для подогревателя воздуха проверьте работу на холоде по руководству: код драйвера может появиться именно при низкой температуре.",
                "5. Для клапана EGR проверьте, не забит ли он сажей и нет ли подсоса на линии. Очистку и замену делайте по инструкции на машину.",
                "6. После ремонта очистите коды и проверьте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "Если в считывании есть код из списка «ехать нельзя», остановитесь. На этой странице это уровень и давление масла, температура и уровень охлаждающей жидкости, температура масла и обороты двигателя. Такие коды не ждут, пока соберётся сервис.",
                "Если код из топливной или впускной группы, а двигатель работает ровно, можно доехать до сервиса. Записывайте, при каких условиях появился код: это сэкономит мастеру время.",
            ]),
            ("Мастеру в сервисе", [
                "Ищите причину в группе, а не в одном коде. Коды подогревателя, температуры воздуха и дросселя часто приходят вместе в холод. Если на холоде записано сразу несколько кодов впуска, проверьте общий путь воздуха, а не отдельные датчики.",
                "Не меняйте деталь без проверки питания, массы и жгута. Датчик с плохим разъёмом даёт тот же код через короткое время.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/ne-nabiraet-vozduh.html|Не набирает воздух]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]]",
                "[[/problemy/ne-zaryazhaet-generator.html|Не заряжает генератор]], [[/problemy/propalo-pitanie.html|пропало питание]]",
                "[[/problemy/nizkoe-davlenie-masla.html|Низкое давление масла]], [[/problemy/peregrev-dvigatelya.html|перегрев двигателя]]",
                "[[/kody/spn-2791.html|SPN 2791 - управление клапаном EGR]], [[/kody/spn-730.html|SPN 730 - драйвер подогревателя воздуха]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Ошибка впуска появилась только зимой. Почему?",
                 "На холоде работает подогреватель воздуха, и датчики температуры дают другие показания. Проверьте подогреватель и разъёмы при низкой температуре, а не только после прогрева."),
                ("Можно ли почистить EGR, а не менять клапан?",
                 "Часто да, если клапан только забит. Решает состояние клапана и тракта, поэтому после чистки проверьте работу по руководству."),
                ("Код топлива и код воздуха пришли вместе. Что первично?",
                 "Обычно одна система ограничивает другую. Начинайте с того, что проверить проще: подсос воздуха и фильтр."),
                ("Нужно ли сбрасывать код после ремонта?",
                 "Да, но только после устранения причины. Затем проверьте повтор на ходу."),
            ]),
        ],
    },

    "brand:man": {
        "head": [
            ("Два формата на одной странице", [
                "На странице MAN бесплатный разбор в формате J1939: номер узла и вид неисправности. Дилерские коды MAN записаны иначе: пятизначный номер, где сначала стоит модуль, а потом сама неисправность. Таких записей здесь намного больше. Сначала определите формат кода, и только потом читайте расшифровку.",
                "Если код короткий и без SPN, это дилерский формат. Не переносите его в таблицу SPN: один и тот же номер в разных форматах может означать совсем разное.",
            ]),
            ("Тормоза на первом месте", [
                "Тормозные группы на странице самые заметные. В списке «ехать нельзя» стоят выключатель тормоза и датчики колёс ABS по всем осям и сторонам. Если такой код записан, не пробуйте понять состояние тормоза только по лампе: датчик колеса и его разъём проверяются на месте.",
                "Датчик износа накладок на третьей оси тоже стоит в начале списка. Он может показывать реально стёртые накладки, поэтому сначала осмотрите накладки, а потом проверяйте сам датчик и его проводку.",
            ]),
            ("Сеть, трансмиссия и выпуск", [
                "Сеть J1939 №1 (SPN 639) стоит в начале разбора не случайно. Если блоки перестали видеть друг друга, в считывании появляются коды сразу из нескольких систем. Сначала проверьте жгут сети и разъёмы блоков, и только потом сами блоки.",
                "Остальные группы на странице - охлаждение, электропитание и прочие системы. Здесь действует тот же порядок: сначала питание и массы, потом датчик и жгут, потом блок.",
            ]),
            ("Порядок проверки", [
                "1. Определите формат кода и блок, который его записал.",
                "2. Для кодов ABS осмотрите разъёмы датчиков, зазор и состояние зубчатого кольца по руководству. Зазор «на глаз» не меряйте.",
                "3. Для датчика износа проверьте накладки и проводку, затем сам датчик.",
                "4. Для сети J1939 проверьте жгут, разъёмы и оконечные резисторы по схеме.",
                "5. Очистите коды только после ремонта и проверьте на ходу.",
            ]),
            ("Водителю в рейсе", [
                "Если горит красная лампа тормозов или ABS вместе с кодом из списка «ехать нельзя», остановитесь в безопасном месте. Тормоз должен работать ровно: если педаль ведёт себя необычно, не ждите сервиса.",
                "Жёлтая лампа ABS без кодов колёс и без падения тормозного давления позволяет доехать до сервиса. Но на мокрой дороге не рассчитывайте на защиту от блокировки колёс.",
            ]),
            ("Мастеру в сервисе", [
                "Для дилерского кода сначала установите модуль по номеру и сверьте описание. Если модуль указан, проверьте его питание, массу и разъём до замены.",
                "Для тормозных кодов работайте по схеме конкретной машины: тягач и прицеп имеют разные разъёмы и провода. Не смешивайте их в одну проверку.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/gorit-lampa-abs.html|Горит лампа ABS]], [[/problemy/stoyanochnyy-tormoz.html|стояночный тормоз]]",
                "[[/problemy/propalo-pitanie.html|Пропало питание, ошибки по всей машине]]",
                "[[/kody/spn-639.html|SPN 639 - сеть J1939 №1]], [[/kody/spn-789.html|SPN 789 - датчик колеса ABS]], [[/kody/spn-597.html|SPN 597 - выключатель тормоза]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Код датчика ABS одного колеса. Можно ли ехать?",
                 "По таблице этой страницы такие коды отнесены к «ехать нельзя». Проверьте колесо на месте до выезда."),
                ("Датчик износа говорит, что накладки стёрты, а на вид они целые?",
                 "Сначала проверьте сам датчик и проводку, после осмотра накладок. Датчик может ошибаться из-за проводки."),
                ("Что значит модуль в начале дилерского кода?",
                 "Модуль указывает, какой блок сообщил о проблеме. Описание в таблице даёт суть. Ищите код целиком."),
            ]),
        ],
    },

    "brand:scania": {
        "head": [
            ("Как читать эту таблицу", [
                "Коды Scania на этой странице идут из дилерской таблицы. Они короткие, например 1, 10 или 100, и сами по себе ничего не говорят. Смысл дают сокращения модулей в описании: ACC, BWS, COO, CTS, GMS, ICL, RET и другие. Сначала найдите модуль по сокращению, потом читайте описание.",
                "Сокращение до двоеточия — это блок, а текст после него — сама неисправность. Например, «ACC: электродвигатель распределения воздуха» — неисправность в блоке климат-контроля (ACC); «ICL: напряжение питания» — проблема с питанием приборной панели (ICL); «COO: круиз-контроль» — запись координатора, центрального блока (COO); «CTS: активизация дополнительного подогревателя» — блок часов и таймера (CTS), который включает подогреватель по расписанию. GMS — коробка передач, RET — ретардер, BWS — блок кузовных надстроек.",
            ]),
            ("Что встречается чаще всего", [
                "По справочнику чаще всего встречаются шина CAN, выпуск и AdBlue, топливо и электропитание. Для шины CAN начинайте с разъёмов и жгута между блоками: при обрыве блоки перестают видеть друг друга и записывают коды сразу в нескольких местах.",
                "Для напряжения питания и аккумулятора проверьте клеммы и массу до блока. Если модули с напряжениями записаны вместе с другими кодами, питание может быть общим источником проблемы.",
            ]),
            ("Выпуск, AdBlue и топливо", [
                "Группа выпуска и AdBlue на дилерской таблице большая. Если код относится к баку AdBlue, сначала проверьте уровень и качество реагента, затем датчики и разъёмы. Код топлива начинайте с фильтров и воздуха в линии, а не с форсунок.",
                "Не все коды этой группы означают серьёзную поломку. Смотрите на описание и на то, горит ли красная лампа, и не делайте выводов по одному коду.",
            ]),
            ("Порядок разбора", [
                "1. Выпишите номер кода полностью, вместе с описанием.",
                "2. Найдите модуль по сокращению в описании и запишите, к какой системе он относится.",
                "3. Проверьте питание и массу модуля, затем разъём.",
                "4. Если описание ссылается на другой модуль, проверяйте его, а не первый.",
                "5. Очистите коды после ремонта и проверьте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "На этой странице для Scania нет выделенного списка кодов «ехать нельзя». Поэтому решайте по лампе и поведению машины: красная лампа, падение мощности, перегрев или необычный звук - повод остановиться.",
                "Жёлтая лампа с одним понятным кодом, например по круиз-контролю или дополнительному подогревателю, обычно не мешает доехать до сервиса.",
            ]),
            ("Мастеру в сервисе", [
                "Дилерский формат лучше читать вместе с описанием модуля, которое даёт справочник. Для глубокой диагностики используйте сканер или сервис с доступом к данным конкретной машины и руководству.",
                "Не меняйте модуль по одному описанию. Проверяйте питание, массу и разъём, и только потом блок.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/propalo-pitanie.html|Пропало питание, ошибки по всей машине]], [[/problemy/ne-zaryazhaet-generator.html|Не заряжает генератор]]",
                "[[/problemy/oshibka-adblue.html|Ошибка AdBlue]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]], [[/problemy/gorit-check-engine.html|горит Check Engine]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Почему код 1 и код 10 разные?",
                 "Номер короткий, поэтому смысл зависит от модуля. Смотрите сокращение в описании, а не сам номер."),
                ("Что значит ICL в описании?",
                 "ICL — блок приборной панели. Слова после двоеточия, например «напряжение питания», — это суть неисправности. Проверьте питание и массу приборной панели, прежде чем менять её."),
                ("Можно ли искать код Scania по SPN?",
                 "Нет, это дилерский формат. Вводите полный код в поиск на главной."),
            ]),
        ],
    },

    "brand:volvo": {
        "head": [
            ("Два формата", [
                "Volvo на этой странице разобран в двух форматах. В бесплатной таблице есть коды по J1939, у которых SPN совпадает со стандартом: для них работают обычные правила SPN и FMI. Основная часть записей дилерская и выглядит как код вида B000101, где номер собран из нескольких частей.",
                "Дилерский код не переводится в SPN. Одна и та же строка может означать блок, параметр и вид неисправности, поэтому читайте описание рядом с кодом, а не угадывайте стандарт.",
            ]),
            ("Старые грузовики и MID", [
                "Старые грузовики Volvo записывают код через MID (блок) и PID или SID (параметр), плюс FMI. Такие коды разобраны на отдельной странице блоков MID. Если сканер показывает формат MID с PID, переходите туда, а не ищите совпадение в общей таблице.",
                "Номер блока MID и номер параметра нельзя переносить в таблицу SPN: это разные системы записи.",
            ]),
            ("Что проверять в первую очередь", [
                "Для дилерских кодов проверка начинается так же, как для любого грузовика: питание, масса, разъёмы, жгут. Короткие разрывы в жгуте под кабиной и у рамы часто дают код, который выглядит как серьёзная неисправность блока.",
                "Для стандартных J1939-кодов работайте по FMI: вид неисправности подскажет, где цепь, а где сам узел. Электрические FMI начинаются с разъёма.",
            ]),
            ("Порядок проверки", [
                "1. Определите формат кода: J1939, MID с PID или дилерский.",
                "2. Для J1939 сверяйте SPN и FMI по таблице, для MID - по странице блоков MID.",
                "3. Осмотрите разъёмы и жгут блока, который записал код.",
                "4. Проверьте питание и массу блока.",
                "5. Очистите коды после ремонта и проверьте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "В этой части справочника для Volvo нет выделенного списка кодов «ехать нельзя». Главный сигнал здесь - лампа и поведение машины: красная лампа, потеря мощности или перегрев означают остановку.",
                "Если лампа жёлтая, а машина работает ровно, спокойно доезжайте до сервиса, записав код и условия его появления.",
            ]),
            ("Мастеру в сервисе", [
                "Для дилерского кода используйте сканер марки или сервис с доступом к описанию. Справочник даёт смысл строки, а ход диагностики ведите по руководству на конкретный автомобиль.",
                "Не меняйте блок по одной записи. Сначала исключите питание, массу и разъём, потом блок.",
            ]),
            ("Связанные страницы", [
                "[[/marki/volvomid.html|Volvo - блоки MID]]",
                "[[/problemy/gorit-check-engine.html|Горит Check Engine]], [[/problemy/propalo-pitanie.html|пропало питание]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Код B000101 - это SPN?",
                 "Нет. Это дилерский формат, смысл в описании рядом с кодом."),
                ("Сканер показал MID и PID. Где смотреть?",
                 "На отдельной странице блоков MID, а не в общей таблице."),
                ("Почему на Volvo нет списка «ехать нельзя»?",
                 "На этой странице такой список не выделен. Решайте по лампе и поведению машины."),
            ]),
        ],
    },

    "brand:daf": {
        "head": [
            ("Два формата DAF", [
                "DAF на этой странице разобран в двух форматах. Стандартные SPN и FMI записаны по J1939: номер узла и вид неисправности стоят парой. Дилерский разбор использует коды вида 12401-20, где описание прямо говорит, что произошло, например защиту кулисы. Такие коды читают по описанию, а не по таблице SPN.",
                "Дилерских записей на странице больше, чем стандартных. Поэтому у DAF сначала определите формат кода: от него зависит и проверка, и блок.",
            ]),
            ("Что встречается чаще всего", [
                "У DAF чаще всего встречаются шина CAN, выпуск и AdBlue, топливо, электропитание и тормоза. Из стандартных кодов в начале списка стоят NOx на выходе после SCR, температура воздуха на впуске, давление в дозирующей рампе, положение педали газа и наличие воды в топливе.",
                "Код воды в топливе (SPN 97) разобран отдельно, с порядком проверки сепаратора и датчика: [[/kody/spn-97.html|SPN 97 - наличие воды в топливе]]. Сначала слейте отстой, а уже потом меняйте датчик.",
            ]),
            ("Выпуск, AdBlue и дозирование", [
                "Коды NOx и давления в рампе относятся к дозированию AdBlue. Если они идут вместе, сначала проверьте уровень и качество реагента, затем дозатор и линию. Датчик NOx показывает то, что получает от системы, поэтому его проверка начинается с AdBlue и выхлопа.",
                "Педаль газа (SPN 91) стоит в начале списка не случайно: ошибка положения педали часто связана с разъёмом в кабине и с питанием датчика. Проверьте разъём, прежде чем менять педаль.",
            ]),
            ("Порядок проверки", [
                "1. Определите формат кода: SPN/FMI или дилерский.",
                "2. Для воды в топливе слейте отстой из сепаратора и проверьте разъём датчика.",
                "3. Для кодов дозирования проверьте уровень и качество AdBlue, фильтр, линию и дозатор по руководству.",
                "4. Для педали газа проверьте разъём и питание датчика в кабине.",
                "5. После ремонта очистите коды и проверьте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "Из стандартных кодов на странице к «ехать нельзя» относятся давление масла, температура охлаждающей жидкости и обороты двигателя. Такой код - повод остановиться, а не доехать до сервиса.",
                "Если горит только значок AdBlue или SCR, а машина работает без падения мощности, можно доехать до сервиса. Не откладывайте визит: при длительной ошибке система может ограничить мощность.",
            ]),
            ("Мастеру в сервисе", [
                "Для дилерских кодов сверяйте номер с описанием и только потом выбирайте блок. Не делайте выводов по одной строке таблицы.",
                "Связанные разборы помогут собрать набор: [[/problemy/oshibka-adblue.html|ошибка AdBlue]], [[/problemy/nasos-adblue.html|насос AdBlue]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]], [[/problemy/ne-idet-regeneratsiya.html|регенерация]].",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Можно ли ехать с кодом воды в топливе?",
                 "Если мощность не падает и лампа не красная, можно доехать, сливая отстой на остановке. Иначе остановитесь."),
                ("Код педали газа: датчик или разъём?",
                 "Сначала разъём и питание, датчик потом."),
                ("Почему описание дилерского кода не совпадает с тем, что видно на машине?",
                 "Описание даёт смысл записи, но проверку делайте по состоянию машины и руководству."),
            ]),
        ],
    },

    "brand:iveco": {
        "head": [
            ("Почему названия узлов здесь заводские", [
                "У Iveco на странице много кодов по J1939, но стандартного названия узла у большинства нет. Поэтому название берётся из заводской строки рядом с кодом. Читайте её внимательно: именно она говорит, что записал блок.",
                "Дилерские записи на той же странице отдельно. Чаще всего они касаются топлива и выпуска, а расшифровка идёт по описанию в таблице, а не по SPN.",
            ]),
            ("Двигатель и коробка — отдельные страницы", [
                "Для Iveco на сайте две отдельные страницы: [[/marki/ivecoedc.html|Iveco EDC]] — коды двигателя, то есть блока управления двигателем, и [[/marki/ivecoeurotronic.html|Iveco EuroTronic]] — коды автоматизированной коробки передач. Смотрите, какой блок записал код, и открывайте страницу этого блока. Общая страница их не заменяет.",
                "Если не ясно, какой блок записал код, сверяйте по заводской строке. Не угадывайте блок по внешнему виду машины.",
            ]),
            ("Топливо и выпуск", [
                "Топливные и выпускные коды часто приходят вместе. Если в одном разборе есть коды топлива и AdBlue, начинайте с простого: уровень и качество реагента, фильтр, воздух в топливной линии.",
                "Засорённый сажевый фильтр даёт похожую картину: мощность падает, а лампа показывает выпуск. Смотрите [[/problemy/zabit-sazhevyy-filtr.html|разбор засорённого сажевого фильтра]] перед заменой датчиков.",
            ]),
            ("Порядок проверки", [
                "1. Прочитайте заводскую строку и запишите её целиком.",
                "2. Определите блок, который записал код.",
                "3. Проверьте питание и массу, затем разъёмы и жгут.",
                "4. Для топлива и выпуска проверяйте по порядку: реагент, фильтры, линии, датчики.",
                "5. Очистите коды после ремонта и проверьте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "На этой странице список кодов «ехать нельзя» пуст. Поэтому решайте по лампе и поведению машины: красная лампа, падение мощности, дым и перегрев означают остановку.",
                "Жёлтая лампа при ровной работе двигателя позволяет доехать до сервиса. Запишите код и условия, при которых он появился.",
            ]),
            ("Мастеру в сервисе", [
                "Для дилерских записей сначала найдите описание и сверьте его с заводской строкой. Если описания нет, не угадывайте смысл: пользуйтесь руководством.",
                "Не меняйте топливный или выпускной узел по одной записи. Сначала проверьте реагент, фильтры и разъёмы.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/problemy-s-toplivom.html|Проблемы с топливом]], [[/problemy/oshibka-adblue.html|ошибка AdBlue]], [[/problemy/zabit-sazhevyy-filtr.html|засорённый сажевый фильтр]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Какая страница нужна: EDC или EuroTronic?",
                 "EDC — коды блока управления двигателем, EuroTronic — коды автоматизированной коробки передач. Откройте страницу того блока, который записал код."),
                ("На Iveco нет списка «ехать нельзя». Значит, всё безопасно?",
                 "Нет. Решайте по лампе и поведению машины, а не по отсутствию списка."),
                ("Почему дилерская запись без SPN?",
                 "Дилерский формат записан своей системой. Смотрите описание рядом с кодом."),
            ]),
        ],
    },

    "brand:yamz": {
        "head": [
            ("Что разобрано по J1939", [
                "ЯМЗ на этой странице записан по J1939: номер узла и вид неисправности стоят парой. Стандартного названия у большинства номеров нет, поэтому узел виден по заводской строке рядом с кодом. Читайте её целиком, а не только номер.",
                "Отдельно лежат дилерские записи: трёхзначные коды вроде 111 и 112. В описании у них прямо написано, что делать, например заменить блок управления. Такое описание - то, что записал завод, а не готовый план ремонта.",
            ]),
            ("Что в начале списка и почему", [
                "В начале разбора стоят управление клапаном EGR, команда привода дроссельной заслонки, положение дроссельной заслонки, температура воздуха на впуске и драйвер подогревателя воздуха. Эти коды относятся к тому, как двигатель дышит. Если они приходят вместе, сначала проверяйте воздушный тракт.",
                "Код подогревателя воздуха может появиться на холоде, поэтому проверять его удобнее при низкой температуре, а не в тёплом гараже.",
            ]),
            ("Группы на странице", [
                "По группам чаще всего встречаются выпуск и AdBlue, топливная система, впуск и электропитание. Группа CAN-шины тоже заметна: она связывает блоки, поэтому обрыв там даёт коды сразу в нескольких местах.",
                "Охлаждение и смазка - отдельные группы с короткими списками. Здесь важнее всего следить за уровнем и температурой, потому что эти коды входят в список «ехать нельзя».",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код, заводскую строку и условия его появления.",
                "2. Для кодов воздуха начните с фильтра, патрубков и подсоса.",
                "3. Для блока с описанием «заменить» сначала проверьте питание, массу и разъёмы: описание завода не заменяет проверку.",
                "4. Для CAN проверьте жгут и разъёмы блоков по схеме.",
                "5. После ремонта очистите коды и проверьте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "Коды уровня и давления масла, температуры и уровня охлаждающей жидкости, температуры масла и оборотов двигателя относятся к «ехать нельзя». При таком коде остановитесь, не дожидаясь падения мощности.",
                "Коды воздуха и подогревателя при ровной работе двигателя позволяют доехать до сервиса. Следите за температурой и не давайте ей расти.",
            ]),
            ("Мастеру в сервисе", [
                "Дилерская запись с описанием «заменить блок» требует проверки, а не немедленной замены. Исключите питание, массу, разъёмы и жгут, и только потом решайте вопрос о блоке.",
                "Для J1939-кодов сверяйте SPN и FMI с таблицей и не путайте узлы, которые записаны похоже.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/ne-nabiraet-vozduh.html|Не набирает воздух]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]]",
                "[[/problemy/oshibka-adblue.html|Ошибка AdBlue]], [[/problemy/ne-zaryazhaet-generator.html|Не заряжает генератор]], [[/problemy/nizkoe-davlenie-masla.html|низкое давление масла]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Код 111 - это блок?",
                 "Это дилерская запись. Описание в таблице даёт смысл. Проверьте блок и питание до замены."),
                ("Код подогревателя исчез к обеду. Почему?",
                 "Так бывает при смене температуры: подогреватель и датчик работают иначе, когда машина прогрета. Проверьте при низкой температуре."),
                ("Код EGR - значит, клапан менять?",
                 "Нет. Сначала тракт и сажа, потом клапан."),
            ]),
        ],
    },

    "brand:gaz": {
        "head": [
            ("Какой формат у кодов ГАЗ", [
                "На странице ГАЗ дилерская таблица небольшая. Коды записаны в формате OBD-II: буква и четыре цифры или знака вида P0016 или P0087. Такой формат общий для многих машин, поэтому описание в строке уже и есть расшифровка.",
                "В основном коды относятся к воздуху, топливу и охлаждению. Номер короткий, но смысл понятен из описания. Не переводите такой код в SPN: это другая система записи.",
            ]),
            ("Что записано на странице", [
                "Примеры на странице: P0016 - согласование положения коленчатого и распределительного валов; P0087 - давление в топливной рампе слишком низкое; P0106 - датчик абсолютного давления во впускном коллекторе выдаёт сигнал вне диапазона; P003A - привод турбокомпрессора не выходит на заданное положение.",
                "Эти четыре кода — четыре разных направления: фазы газораспределения (P0016), давление топлива в рампе (P0087), датчик давления на впуске (P0106) и управление турбиной (P003A). Проверять их нужно по отдельности.",
            ]),
            ("Воздух и топливо", [
                "Если код касается воздуха на впуске, проверьте фильтр, патрубки и разъём датчика давления. Подсос после фильтра даёт сигнал, похожий на неисправный датчик, поэтому начинайте с тракта.",
                "Если код касается давления топлива, проверьте фильтр и подачу. Низкое давление в рампе бывает и от воздуха в линии, и от засорённого фильтра. Не меняйте насос без проверки линии.",
            ]),
            ("Порядок проверки", [
                "1. Запишите P-код целиком и описание на странице.",
                "2. Осмотрите разъёмы и жгут датчика, который записал код.",
                "3. Для воздуха проверьте фильтр, патрубки и подсос.",
                "4. Для топлива проверьте фильтр, линии, воздух и подачу по руководству.",
                "5. Для турбины и фаз проверьте привод и датчики по методике на конкретный двигатель.",
                "6. Очистите коды после ремонта и проверьте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "В этой дилерской таблице список «ехать нельзя» не выделен. Решайте по лампе и поведению машины: потеря мощности, рывки или перегрев - повод остановиться.",
                "Если двигатель работает ровно, а горит одна лампа с понятным кодом воздуха, можно доехать до сервиса, записав код и условия его появления.",
            ]),
            ("Мастеру в сервисе", [
                "Для таких кодов сначала исключите простое: фильтр, подсос и разъёмы. Заменённый датчик без проверки тракта даст тот же код.",
                "Если код повторяется после ремонта, сверьте записи с условиями появления: холод, нагрузка, режим. Это быстрее, чем менять деталь наугад.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/ne-nabiraet-vozduh.html|Не набирает воздух]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]]",
                "[[/problemy/upala-moshchnost.html|Упала мощность]], [[/problemy/gorit-check-engine.html|горит Check Engine]], [[/problemy/peregrev-dvigatelya.html|перегрев двигателя]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Чем P-код отличается от SPN?",
                 "P-код - формат OBD-II, SPN - J1939. Это разные системы записи, и их нельзя путать."),
                ("Код P0106: менять датчик?",
                 "Сначала разъём, жгут и подсос на впуске. Датчик - после них."),
                ("Почему P0087 появился после заправки?",
                 "Возможны вода или воздух в линии. Проверьте фильтр и линию перед заменой насоса."),
            ]),
        ],
    },

    "brand:sitrak": {
        "head": [
            ("Что на странице", [
                "SITRAK записывает коды по J1939: SPN и FMI идут парой. Большинство кодов разобраны с заводской строкой вместо стандартного названия, поэтому название узла берите оттуда. Групп много: смазка, охлаждение, топливо, впуск и наддув, выпуск и AdBlue, электропитание, CAN-шина, тормоза, трансмиссия и прочие системы.",
                "Самые крупные группы - выпуск и AdBlue, электропитание и прочие системы. Если код из этих групп пришёл вместе с кодом CAN, сначала проверяйте сеть и питание, а потом узел.",
            ]),
            ("AdBlue и бак", [
                "В начале разбора стоят уровень AdBlue в баке (SPN 1761) и температура бака AdBlue (SPN 3031). Реагент на морозе замерзает и меняет показания, поэтому код температуры зимой не всегда означает поломку датчика. Сначала проверьте, прогрелся ли реагент и видно ли его уровень.",
                "Если код уровня горит на тёплой машине, проверьте датчик в баке, его разъём и проводку. Доливать реагент сверх меры, пока датчик не проверен, не стоит: это не решает причину.",
            ]),
            ("Вентилятор и обороты", [
                "Код частоты вращения вентилятора (SPN 1639) и код положения дроссельной заслонки (SPN 51) стоят в начале разбора. Они часто связаны с тем, как двигатель охлаждается и набирает обороты. Проверьте привод вентилятора и датчик, прежде чем менять блок.",
                "Коды электропитания и CAN проверяются отдельно: сначала разъёмы, потом жгут и только затем блоки.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код с SPN, FMI и заводской строкой.",
                "2. Для электрических FMI (с 3 по 6) начинайте с разъёма и цепи.",
                "3. Для AdBlue проверьте реагент, датчики уровня и температуры, затем линии.",
                "4. Для вентилятора проверьте привод и датчик оборотов.",
                "5. Для CAN и питания проверьте жгут, разъёмы и массу.",
                "6. Очистите коды после ремонта и проверьте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "Коды температуры и уровня масла, охлаждающей жидкости, масла КПП, давления масла и выключателя тормоза стоят в списке «ехать нельзя». По ним не продолжайте движение.",
                "Код AdBlue или вентилятора при ровной работе двигателя даёт возможность доехать до сервиса. Записывайте условия появления: холод, нагрузка, стоянка.",
            ]),
            ("Мастеру в сервисе", [
                "Сначала отделите холод от неисправности: код AdBlue на морозе и код на тёплой машине разбирайте по-разному.",
                "Для кодов масла и охлаждения сначала проверьте уровень и датчик, а не блок. Датчики давления и температуры проверяйте по руководству.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/oshibka-adblue.html|Ошибка AdBlue]], [[/problemy/nasos-adblue.html|насос AdBlue]]",
                "[[/problemy/peregrev-dvigatelya.html|Перегрев двигателя]], [[/problemy/nizkoe-davlenie-masla.html|низкое давление масла]], [[/problemy/propalo-pitanie.html|пропало питание]]",
                "[[/kody/spn-1761.html|SPN 1761 - уровень AdBlue]], [[/kody/spn-1639.html|SPN 1639 - вентилятор]], [[/kody/spn-3031.html|SPN 3031 - температура бака AdBlue]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Код AdBlue появился зимой и пропал к обеду. Что это?",
                 "Холод и прогрев меняют показания бака. Проверьте, прогрелся ли реагент, прежде чем менять датчик."),
                ("Можно ли ехать с кодом масла КПП?",
                 "По таблице страницы код температуры масла КПП стоит в списке «ехать нельзя». Остановитесь и проверьте."),
                ("Код ушёл после очистки. Надо ли что-то делать?",
                 "Проверить повтор на ходу. Если код вернулся, причина не устранена."),
            ]),
        ],
    },

    "problem:ne-zaryazhaet-generator": {
        "head": [
            ("Что делает генератор", [
                "Генератор на работающем двигателе отдаёт ток в бортовую сеть и подзаряжает аккумулятор. Регулятор держит напряжение в нужных пределах. Если зарядки нет, аккумулятор постепенно садится, и машина живёт за его счёт.",
                "Связанные коды на этой странице: напряжение генератора (SPN 167), напряжение аккумулятора (SPN 168) и напряжение аккумулятора на замке зажигания (SPN 158). Они показывают, где именно падает напряжение: на выходе генератора, на аккумуляторе или на цепи включения.",
            ]),
            ("Типовые причины", [
                "Ремень: проскальзывание, износ или слабое натяжение. Без вращения генератора зарядки не будет даже при исправном генераторе.",
                "Клеммы и масса: окисление и слабая затяжка на клемме генератора, на аккумуляторе и на массе двигателя. Часто это самая дешёвая и самая частая причина.",
                "Провод от генератора: обрыв или перетёртая изоляция. Чаще всего такое место у рамы и у двигателя, где жгут греется и вибрирует.",
                "Регулятор напряжения или сам генератор: износ щёток, неисправный диодный мост. Это проверяется отдельно, после проверки проводки.",
                "Аккумулятор, который не держит заряд. Если он старый или сульфатирован, даже исправный генератор его не спасёт, и код появится снова.",
            ]),
            ("Признаки", [
                "Горит лампа заряда, свет и приборы тускнеют на холостом ходу, стартер проворачивает медленно. Блоки могут отключаться по одному, и тогда появляются ложные коды по всей машине.",
                "Если генератор греется, шумит или пахнет горелым, это уже опасность, а не только проблема зарядки. Остановитесь и проверьте его, пока аккумулятор не сел.",
            ]),
            ("Порядок проверки", [
                "1. Осмотрите клеммы аккумулятора и генератора и массу двигателя. Зачистите и затяните.",
                "2. Проверьте натяжение и состояние ремня по руководству на машину.",
                "3. На работающем двигателе измерьте напряжение на клеммах аккумулятора и сравните с нормой из руководства. Цифры со страницы не являются нормой для вашей машины.",
                "4. Включите потребители и повторите измерение: если напряжение проседает, смотрите цепь генератора и массу.",
                "5. Проверьте генератор по методике: нагрев, шум, выходной ток. Регулятор и щётки - отдельным шагом.",
                "6. Аккумулятор проверяйте отдельно, нагрузочным тестом по методике, а не по внешнему виду.",
            ]),
            ("Водителю в рейсе", [
                "Если горит лампа заряда, уменьшите нагрузку на аккумулятор: выключите лишние потребители, обогрев сидений и дополнительные фары. Это продлит работу до сервиса.",
                "Не глушите двигатель без нужды: машина может не завестись, если аккумулятор уже сел. Если генератор греется, пахнет горелым или шумит, остановитесь и вызовите помощь.",
            ]),
            ("Мастеру в сервисе", [
                "Проверяйте по порядку: контакты и масса, ремень, проводка, потом генератор и регулятор, и только в конце аккумулятор. Замена генератора без проверки массы и проводки даёт тот же результат.",
                "После ремонта очистите коды и проверьте зарядку на ходу под нагрузкой. Для кодов напряжения сверьте показания блока с измерением мультиметром.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/propalo-pitanie.html|Пропало питание, ошибки по всей машине]], [[/problemy/gorit-check-engine.html|Горит Check Engine]], [[/problemy/ne-zavoditsya.html|Не заводится]]",
                "[[/kody/spn-167.html|SPN 167 - напряжение генератора]], [[/kody/spn-168.html|SPN 168 - напряжение АКБ]], [[/kody/spn-158.html|SPN 158 - напряжение АКБ на замке]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Лампа заряда горит, а напряжение в норме. Что это?",
                 "Сверьте измерение и код. Возможна неисправность цепи лампы или датчика, а не генератора. Проверьте по руководству."),
            ("Можно ли доехать с погасшей зарядкой?",
                 "Недалеко и осторожно, экономя потребители. Чем дальше, тем выше риск остановки."),
            ("Нужно ли менять аккумулятор после замены генератора?",
                 "Если аккумулятор не держит заряд при проверке по методике, да. Сначала проверьте его отдельно."),
        ])],
    },

    "problem:propalo-pitanie": {
        "head": [
            ("Что означает «всё отвалилось сразу»", [
                "Когда ошибки приходят сразу из нескольких систем, почти всегда причина в питании или шине. Один обрыв на массе или сгоревший главный предохранитель гасит целую группу блоков. Остальные блоки продолжают работать, поэтому картина выглядит хаотичной.",
                "В начале списка на странице идут коды напряжения аккумулятора при зажигании (SPN 158) и аккумулятора (SPN 168), источника питания (SPN 627) и контроллера (SPN 629). Дальше идёт питание датчиков по группам: SPN 1079 и 1080, а также 3509, 3510 и 3511. Они показывают, какая линия просела.",
            ]),
            ("Где чаще всего", [
                "Клеммы аккумулятора и массы двигателя: окисление и слабая затяжка дают самые частые случаи. Проверьте их первыми, даже если всё кажется в порядке.",
                "Главный предохранитель и реле: сгоревший предохранитель или подгоревший контакт реле отключают сразу всё, что на них висит. По схеме смотрите, какие блоки стоят на этом предохранителе.",
                "Разъёмы под приборной панелью и в кабине. Влага и окисление здесь дают перебои, которые пропадают и появляются. Такие случаи сложнее всего поймать, поэтому фиксируйте, когда они происходят.",
                "Жгут у рамы и у двигателя: вибрация перетирает изоляцию, и провод касается массы. Это место проверяйте, когда обрыв не виден на разъёме.",
            ]),
            ("Признаки", [
                "Часть приборов работает, а часть нет. Значит, цепь отсутствующих блоков нужно проследить отдельно, а не менять блоки подряд.",
                "Ошибки сразу по нескольким системам, в том числе ложные. Если они пропадают и возвращаются при тряске или при включении фар, ищите перебой питания.",
            ]),
            ("Порядок проверки", [
                "1. Проверьте клеммы аккумулятора и массу двигателя, зачистите и затяните.",
                "2. Проверьте главный предохранитель и реле по схеме: и колодку, и контакты.",
                "3. Для кодов питания датчиков (SPN 1079, 1080, 3509, 3510, 3511) проверьте линии питания по группам, а не один датчик.",
                "4. Проверьте шину CAN: провод без обрыва, разъёмы, оконечные резисторы по схеме.",
                "5. Найдите блок, который не работает, и проследите его цепь от предохранителя до разъёма.",
            ]),
            ("Водителю в рейсе", [
                "Если питание пропало на ходу, двигатель может заглохнуть. Остановитесь в безопасном месте, пока машина ещё управляется, и не спешите запускать мотор снова, если он не заводится.",
                "Если двигатель работает, а часть приборов и блоков отключилась, не глушите его до сервиса без нужды: повторный запуск может не получиться. Сообщите мастеру, какие приборы пропали и когда.",
            ]),
            ("Мастеру в сервисе", [
                "Не меняйте блоки первыми. Сначала массы и питание под нагрузкой, потом предохранители, реле и линии. Блок, который «не видит» сеть, часто исправен, а мешает обрыв.",
                "После ремонта проверьте все группы кодов, а не только те, что были в начале. Убедитесь, что ошибки питания не возвращаются при тряске и при включении мощных потребителей.",
            ]),
            ("Связанные страницы", [
                "[[/kody/spn-158.html|SPN 158]], [[/kody/spn-168.html|SPN 168]], [[/kody/spn-627.html|SPN 627]], [[/kody/spn-629.html|SPN 629]], [[/kody/spn-639.html|SPN 639]], [[/kody/spn-1079.html|SPN 1079]], [[/kody/spn-1080.html|SPN 1080]]",
                "[[/problemy/ne-zaryazhaet-generator.html|Не заряжает генератор]], [[/problemy/gorit-check-engine.html|горит Check Engine]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Пропали часть приборов, а двигатель работает. Что проверить первым?",
                 "Массы и клеммы, затем предохранитель нужной цепи."),
            ("Почему после тряски ошибки появляются снова?",
                 "Перебой в разъёме или обрыв в жгуте. Проверяйте проводку под нагрузкой и при тряске."),
            ("Нужно ли менять блок, который не отвечает?",
                 "Нет, пока не проверены питание, масса и сеть."),
        ])],
    },

})


# Добавки к партии 1: разделы вставляются перед «Связанными страницами».

def _add(key, section):
    head = EXTRA_BLOCKS[key]["head"]
    head.insert(len(head) - 1, section)

_add("brand:daf", ("Почему дилерских записей больше и что с этим делать", [
    "Дилерский разбор DAF составлен по описаниям самого производителя, поэтому в нём много записей с понятным текстом: что именно не в порядке и какой узел или функция затронуты. Это удобно, но есть ловушка: один и тот же смысл может записываться по-разному в разных блоках. Сначала сверяйте, какой блок записал код, и только потом ищите неисправность.",
    "Если описание говорит о функции, которой вы не пользуетесь, не спешите искать поломку. Посмотрите, не срабатывает ли функция из-за положения органов управления, питания или состояния разъёмов. Такие записи часто связаны с тем, в каком положении стоит рычаг или педаль в момент записи.",
]))

_add("brand:gaz", ("Как устроен формат OBD-II на этой странице", [
    "OBD-II - общий набор кодов, который понимают большинство машин с электронным управлением. Буква P означает двигатель и трансмиссию. Вторая цифра 0 означает общий код для всех производителей, а не заводской. Поэтому описание на странице и есть расшифровка. Но общий код не говорит, какой именно датчик или клапан стоит на вашей машине: это уточняется по схеме.",
    "Коды похожего смысла часто приходят вместе, например датчики фаз и давление в рампе. Смотрите, есть ли среди них код, который объясняет остальные, и начинайте с него. Записывайте, когда ошибка появилась: при холодном пуске, на подъёме или после заправки. Один и тот же код в разных условиях может иметь разные причины.",
]))

_add("brand:iveco", ("Что проверять при кодах топлива и выпуска", [
    "Общий стандартный код часто указывает только на систему, а не на деталь. Поэтому заводская строка важнее номера. Два кода с одним номером в разных блоках могут относиться к разным узлам, и это надо учитывать при поиске.",
    "Топливная система дизеля чувствительна к чистоте. Если в разборе есть коды давления и подачи, проверяйте фильтры и воздух в линии раньше форсунок. Слив отстоя и осмотр уплотнений в линии подачи - недорогие шаги, с которых стоит начинать.",
    "Если код дозирования появился после заправки, сначала выясните, каким реагентом заправлена машина и не было ли долива посторонней жидкости. Промывка бака и смена реагента - работа мастера, а не водителя.",
    "Водитель может помочь разбору: запишите, когда появился код, сколько проехали и какое топливо и реагент заливали. Такие записи сокращают работу мастера.",
]))

_add("brand:man", ("Что важно перед заменой", [
    "Перед заменой датчика или накладок проверьте, не вызвала ли код грязь. Грязь, вода и соль на зубчатом кольце дают сбои сигнала. Иногда достаточно очистки и проверки зазора, а не новой детали.",
    "Записывайте, на какой оси и с какой стороны появился код. Для кодов с номером оси разница между левой и правой стороной важна: по ней мастер быстрее найдёт место в проводке.",
    "Если код появился после ремонта тормоза, сравните работу колеса до ремонта и после. Сбой, который не виден на одном замере, в записях видно сразу.",
]))

_add("brand:scania", ("Как искать код по сокращению модуля", [
    "Сокращения модулей короткие, и один и тот же номер может стоять у разных модулей. Поэтому вводите в поиск код целиком вместе с модулем, если сканер его показывает. Сокращение подсказывает систему: блок приборной панели и блок климат-контроля требуют разных проверок.",
    "Если сканер показывает только номер без модуля, сопоставьте код с записями соседних кодов. Группа записей одного модуля обычно говорит, какой блок проверять первым.",
]))

_add("brand:sitrak", ("Выпуск и AdBlue: порядок проверки", [
    "Группа выпуска и AdBlue на SITRAK большая, поэтому проверку лучше вести по порядку. Сначала реагент: уровень, качество, отсутствие примесей. Затем бак и датчики в нём, потом линии подачи и дозатор. Замена блока в этой группе редко решает проблему.",
    "Если код температуры бака AdBlue появился на морозе и пропал при прогреве, это в первую очередь вопрос отогрева и проверки датчика. Если он держится и на тёплой машине, проверяйте датчик и его разъём.",
    "Для электропитания сначала проверяйте разъёмы блоков, которые подключены к питанию, потом массы, потом предохранители. Группа электропитания здесь большая, поэтому не начинайте с замены блоков.",
]))

_add("brand:volvo", ("Что делать с длинным дилерским кодом", [
    "Дилерский код Volvo собран из нескольких частей, и каждая несёт свой смысл. Номер вида B000101 нельзя разбирать по одной цифре: его читают целиком и сверяют с описанием. Если описание непонятно, не подбирайте значение наугад, а уточните у сервиса с доступом к данным марки.",
    "Коды, связанные с сетью между блоками, появляются, когда повреждены кабель или разъём под кабиной. Такие записи часто идут группой сразу из нескольких блоков. Проверяйте разъёмы, жгут и массу до того, как менять блоки.",
]))

_add("brand:yamz", ("Как не путать дилерские записи и J1939", [
    "Трёхзначный номер вроде 111 не является SPN, даже если совпадает с номером из таблицы стандарта. Сравнивать их напрямую нельзя: дилерская запись собрана по собственной системе, а стандартная - по J1939.",
    "Если в считывании одновременно есть трёхзначная запись и код J1939, разбирайте их раздельно: сначала найдите, какой блок записал каждую, затем проверяйте систему, к которой она относится.",
    "Сохраняйте историю записей при ремонте. Если код появился после замены одного узла, это подсказывает, что проверять стоит соседний разъём или жгут, а не только новый узел.",
]))

_add("problem:ne-zaryazhaet-generator", ("Почему зарядка пропадает не сразу", [
    "Зарядка часто падает постепенно: сначала ремень проскальзывает только под нагрузкой, потом контакт греется, и в какой-то момент цепь рвётся. Поэтому машина может ехать несколько дней с плохим контактом, а потом встать. Если код появлялся и пропадал, считайте это предупреждением, а не случайностью.",
    "Для проверки под нагрузкой включайте обычные потребители поочерёдно и смотрите, как меняется напряжение и не горит ли лампа заряда. Так видно, держит ли цепь при реальной работе, а не только на холостом ходу.",
]))

_add("problem:propalo-pitanie", ("Если отказ повторяется", [
    "Если питание пропадает снова и снова, одного ремонта может не хватить. Ищите место, где появляется нагрузка: движение по неровной дороге, работа обогрева, включение мощных потребителей. Место, которое реагирует на нагрузку, и есть искомая точка.",
]))


_add("brand:volvo", ("Порядок работы с журналом", [
    "Если сканер записал несколько кодов из разных групп, не пытайтесь разобрать их все сразу. Выберите код, который записан раньше других или с кадром стоп-данных, и проверьте его систему. Часто после устранения одной причины остальные записи пропадают сами, и тогда видно, какой код был первичным.",
    "Очищая журнал, запишите, какие коды были до очистки. Так при повторном появлении видно, что это тот же набор, а не новая неисправность, и мастер быстрее найдёт место, где всё начиналось.",
]))

_add("brand:iveco", ("Почему не стоит менять узел сразу", [
    "На Iveco много узлов с похожими симптомами: потеря мощности, дым, ограничение оборотов. Поэтому один код редко даёт право на замену. Сначала сравните записи, условия и состояние питания. Если несколько кодов говорят о топливе, решайте вопрос по общей картине, а не по последнему появившемуся коду.",
]))

_add("brand:scania", ("Что записывать для мастера", [
    "Для дилерского формата полезно записать номер кода, сокращение модуля, описание и условия появления. Если код повторяется, отметьте, в какую погоду и на каком режиме он возвращается. Такие записи позволяют мастеру сузить поиск до одного узла.",
]))

_add("brand:yamz", ("Что уточнить до ремонта", [
    "Перед ремонтом уточните, какой блок и какая версия программы стоят на машине. Записи одного и того же номера могут относиться к разным исполнениям, и сверка по заводской строке с конкретной машиной избавит от лишней работы.",
]))

# Партия 2: 12 марок. Дописывается в конец marki_problemy_texts.py.

EXTRA_BLOCKS.update({

    "brand:ford": {
        "head": [
            ("Что разобрано на этой странице", [
                "Здесь собрано 407 кодов Ford Trucks, и почти вся страница - это одна таблица: номер слева, заводское описание справа. Таблица не делится на отдельные разделы, поэтому группу узла приходится определять по тексту строки, а не по месту на странице.",
                "Среди записей заметно выделяются четыре блока. Первый - AdBlue: дозирование, насосный модуль, датчики уровня и качества реагента, дозирующий модуль и его датчики давления. Второй - сообщения J1939 о скорости, тормозах, педали и круиз-контроле. Третий - датчики радара и привод турбины. Четвёртый - иммобилайзер, тахограф и топливная рампа. Остальное - связь CAN между блоками и внутренние ошибки блока EMS.",
            ]),
            ("Как читать номер", [
                "Ищите код так, как его показывает сканер, полностью - вместе с точкой и ведущими нулями. Номер на этой странице - заводской номер Ford Trucks; он не совпадает с SPN из таблицы J1939.",
                "Номер, совпавший с SPN из таблицы J1939, здесь ничего не значит. Записи, помеченные как «Ошибка сигнала J1939», относятся к сообщению, а не к узлу. Если сообщение не пришло или пришло с ошибкой, неисправным может быть блок-отправитель, а не тот, чьё имя стоит в описании.",
                "В части строк стоит ещё одна запись: «Код FODP (сканер)» и P-код, например P0513-00. Это код, который показывает сканер. Записывайте оба, если они есть: заводской номер нужен для раздела на этой странице, а P-код - для поиска в других таблицах.",
            ]),
            ("Основные системы и типовые причины", [
                "AdBlue. В группе много записей с близким смыслом: уровень реагента, его качество, температура бака, насос, отсечной клапан, давление на входе и выходе дозирующего модуля, связь с модулем. Такой набор может идти от одного узла или от одного питания, поэтому не меняйте все детали подряд. Начинайте с того, что записано первым: уровня и качества реагента, затем линии подачи и только потом модуль.",
                "Радар. Записи о внутренней ошибке датчика радара, нарушенной юстировке и загрязнённой антенне на этой странице относятся к одной группе. Первым делом смотрите на чистоту датчика и его крепление. Юстировку без инструкции не делайте: страница её не описывает.",
                "Привод турбины. Коды связи с приводом, положения привода, внутренней температуры и блокировки перемещения стоят рядом. Сначала проверьте, двигается ли привод свободно и получает ли он питание, и только потом решайте, нужен ли новый привод.",
                "Иммобилайзер и ключ. Записи 001 описывают несовместимый ключ, ошибку чтения и ошибку записи кода ключа. Они решаются ключом и блоком, а не датчиками. Перед разбором убедитесь, что используется ключ именно от этой машины.",
                "Тормоза и тахограф. Записи о датчиках давления тормоза описывают обрыв цепи датчика и его питания. Сообщение о тахографе TCO1 или его отсутствии говорит о линии между тахографом и блоком скорости. Сам тахограф проверяйте, когда линия исправна.",
                "Топливо. Группа рампы включает давление выше или ниже нормы, негерметичность, расходомер и регулирующий клапан. На странице есть отдельная запись о засорённом топливном фильтре, поэтому фильтр и линия подачи проверяются раньше рампы.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код полностью, с точкой, и отметьте группу, к которой он относится.",
                "2. Проверьте, какой блок записал код. Для сообщения J1939 ищите отправителя.",
                "3. Для AdBlue проверьте реагент, бак и датчики в нём, затем линии и дозатор.",
                "4. Для записей CAN проверьте разъёмы шины и жгут до блоков.",
                "5. Для радара и привода проверьте чистоту, крепление, питание и свободный ход.",
                "6. Очистите записи только после устранения причины и проверьте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "Списка «ехать нельзя» на этой странице нет. Решайте по лампе на щитке и по поведению машины. Если двигатель теряет мощность, тормоза работают не так, как обычно, или загорелась красная лампа, остановитесь и вызовите сервис.",
                "Запись только по AdBlue, без потери мощности и без изменения работы тормозов, - повод записать условия появления и ехать к сервису без спешки. Записи о радаре и приводе турбины решайте по поведению машины, а не по номеру.",
            ]),
            ("Мастеру в сервисе", [
                "Сначала отделите группы друг от друга: AdBlue, радар, тахограф, тормоза, иммобилайзер. Записи одной группы могут описывать одну причину, а записи из разных групп - разные, даже если идут подряд.",
                "При ремонте сравните считывание до и после работы. Если часть записей ушла, а часть осталась, причина устранена не полностью. Если записи вернулись в том же составе, ищите общий разъём или питание.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/oshibka-adblue.html|Ошибка AdBlue]], [[/problemy/nasos-adblue.html|насос AdBlue]], [[/problemy/datchik-nox.html|датчик NOx]]",
                "[[/problemy/oshibka-tahografa.html|ошибка тахографа]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]], [[/problemy/gorit-lampa-abs.html|горит лампа ABS]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Код AdBlue пропал после заправки. Что делать?",
             "Запишите, чем заправлена машина. Если код вернулся, проверьте качество реагента, а не только датчик уровня."),
            ("Почему на одной машине много похожих записей сразу?",
             "Одна причина, например питание модуля или уровень реагента, может дать несколько записей из одной группы. Ищите первую по времени запись."),
            ("Как понять, что код относится к радару, а не к тормозам?",
             "Смотрите описание: записи радара стоят в своей группе и говорят о самом датчике или его антенне. Записи тормозов относятся к давлению в контуре и датчикам давления."),
        ])],
    },

    "brand:manebs": {
        "head": [
            ("Что разобрано на этой странице", [
                "Страница относится к тормозному модулю MAN EBS. Записи в ней собраны по модулям и колёсам: ножной тормоз, модуляторы давления по мостам и сторонам, датчики скорости колёс, датчики износа накладок, связь CAN с ESP и тахографом, память модуля.",
                "Примеры показывают, как записан каждый код: номер, текст о том, какой модуль и какое колесо затронуты, вид неисправности и цвет лампы STOP. Поэтому, прежде чем менять деталь, определите модуль и сторону, а затем смотрите вид неисправности.",
            ]),
            ("Как читать коды этой страницы", [
                "Формат здесь не J1939. Номер состоит из пяти цифр, после него идёт текст. В тексте иногда стоит FMI, например FMI 5 для замыкания на массу в записи о ножном тормозе, или FMI 0 и FMI 3 в записях, где точный вид сбоя не определён.",
                "Последним в каждой записи на странице указан цвет лампы STOP: горит жёлтым или горит красным. Цвет помогает решить, что делать с машиной прямо сейчас. Номер нужен, чтобы найти место неисправности.",
                "Записи с текстом «неопределённая неисправность» не дают точной причины. По ним проверяйте сам модуль, его разъём и питание, а не сразу деталь.",
            ]),
            ("Основные системы и типовые причины", [
                "Датчики скорости колёс. Записи о слишком большом зазоре датчика или ошибке скорости колеса дают неверный сигнал для всей тормозной электроники. Загрязнённое зубчатое кольцо или повреждённый разъём дают такой же результат, как неисправный датчик, поэтому сначала очистите кольцо и осмотрите разъём.",
                "Модуляторы давления. Записи по переднему, заднему и 2-му заднему мосту, по правой стороне и по подъёмному мосту указывают на конкретный модуль. Не меняйте модуль одной стороны, если запись касается другой: сверяйте сторону и мост из текста.",
                "CAN и связь. Записи о связи с ESP, о канале CAN тормозов и об истёкшем времени ожидания сообщения говорят, что сообщение не пришло. В этом случае первым делом смотрите жгут между модулями и разъёмы под кабиной, а не блок.",
                "Тахограф. Запись о недопустимом сигнале TCO1 относится к скорости, которую модуль получает от тахографа. Проверьте тахограф и линию до модуля, потом остальное.",
                "Накладки. Датчики износа дают записи о разнице толщины накладок между осями или между сторонами одной оси. Сначала проверьте сами накладки и контакт датчика, потом электрическую часть.",
                "Память и конфигурация. Записи о памяти EEPROM и о несовместимом наборе данных модуля связаны с программной настройкой. Такой ремонт не решается заменой колеса или датчика; нужна сверка конфигурации.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код целиком, с модулем, колесом и цветом лампы STOP.",
                "2. Определите мост и сторону по тексту записи и проверьте, что именно там установлено.",
                "3. Проверьте разъём и жгут до модуля, затем питание и массу.",
                "4. Для датчиков скорости и износа проверьте кольцо, зазор и контакт.",
                "5. Для записей CAN проверьте связь между модулями под кабиной.",
                "6. Модуль меняйте после того, как все предыдущие пункты исправны.",
            ]),
            ("Водителю в рейсе", [
                "На странице нет отдельного списка «ехать нельзя». У каждой записи указан цвет лампы STOP, и решать нужно по нему и по поведению тормозов.",
                "Если тормоз работает иначе, чем обычно, или при торможении машина ведёт себя непредсказуемо, остановитесь независимо от цвета лампы. Если тормоз работает нормально, а горит жёлтая лампа, запишите код и цвет и проверьте в сервисе, не откладывая надолго.",
            ]),
            ("Мастеру в сервисе", [
                "Страница даёт сторону и мост прямо в описании. Используйте это: перед заменой модулятора проверьте, есть ли в том же считывании записи о CAN, датчиках скорости или о тахографе, потому что они могут быть причиной.",
                "Для записей о памяти и конфигурации сверяйте программу модуля и настройки с машиной. Записи о накладках без замера износа не решают вопроса о замене: сначала осмотрите накладки.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/gorit-lampa-abs.html|горит лампа ABS]], [[/problemy/oshibka-tahografa.html|ошибка тахографа]], [[/problemy/stoyanochnyy-tormoz.html|стояночный тормоз]]",
                "[[/marki/man.html|MAN]], [[/marki/manzbr2.html|MAN ZBR2]], [[/kody/spn-597.html|SPN 597 - выключатель тормоза]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Лампа STOP горит жёлтым, а тормоз работает. Что делать?",
             "Запишите код и цвет лампы, проверьте датчик и связь, указанные в записи. Решение по машине принимайте по поведению тормоза."),
            ("Код износа накладок появился после замены колодок. Почему?",
             "Датчик износа и накладки связаны по толщине. Проверьте, что накладки и датчик установлены правильно и что разница толщины между сторонами не вызвана перекосом."),
            ("Можно ли сразу менять модуль регулировки давления?",
             "Нет. Сначала проверьте разъём, жгут и питание модуля, затем датчики колеса. Модуль меняют, когда все они исправны."),
        ])],
    },

    "brand:manzbr2": {
        "head": [
            ("Что разобрано на этой странице", [
                "Страница относится к центральному бортовому компьютеру MAN ZBR2. Судя по записям на странице, к нему подключены наружное освещение, подогрев, централизованная смазка, датчики бачков, тахограф и приборная панель. Поэтому записи здесь касаются не одного узла, а всей сети.",
                "В примерах видно, что блок отмечает и неисправности самих подключённых устройств, и проблемы связи по шине, и несовпадение настроек. Перед разбором помните, что код, записанный блоком ZBR2, не всегда означает неисправность самого блока.",
            ]),
            ("Как читать коды этой страницы", [
                "Код состоит из пятизначного номера и текста. Текст иногда перечисляет виды неисправности через FMI: например, FMI 5 - замыкание на массу, FMI 6 - замыкание на плюс аккумулятора, FMI 10 - обрыв цепи. Если такой перечень есть, сопоставьте его с тем, что видно на машине, и не выходите за рамки перечисленного.",
                "Некоторые записи описаны одной строкой, без уточнения. Например, запись о крутящем моменте двигателя на странице не расшифрована. Для таких кодов смысл берите из системы, которую назвал блок, и из других записей того же считывания.",
            ]),
            ("Основные системы и типовые причины", [
                "Наружное освещение. Записи о выключателе мигающего света, о противотуманных фарах и о блокировке проверки освещения относятся к цепям выключателей. Начните с лампы, предохранителя и разъёма выключателя, затем проводку до блока.",
                "Предпусковой подогрев. Записи о электромагнитном клапане предпускового подогрева говорят о цепи самого клапана: короткое замыкание, обрыв, замыкание на плюс. Не путайте клапан с работой подогревателя в целом: сначала проверьте цепь клапана.",
                "Смазка и бачки. Запись о датчике числа ходов насоса централизованной смазки относится к датчику насоса. Запись о датчике уровня промывочной жидкости - к датчику бачка. В обоих случаях сначала проверяйте питание и сигнал датчика, а не блок.",
                "Шина данных. Коды, начинающиеся на 06, описывают отказ приёма или передачи сообщения. Например, на странице есть запись об отсутствии сигнала автомобильного электропитания в сети CAN и запись о сообщении для дисплея приборной панели. Сначала проверьте шину и её разъёмы, потом блоки, которые должны слать сообщение.",
                "Топливо. Запись о датчике уровня второго бака относится к цепи этого датчика. Проверьте разъём и массу, прежде чем менять сам датчик.",
                "Настройки и тахограф. Запись о наборе параметров в ZBR2 или о номере кузова в тахографе означает несоответствие данных. Здесь нужна сверка настроек с машиной, а не ремонт детали.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код с номером, текстом и видом неисправности.",
                "2. Определите, какое устройство записано в тексте: выключатель, датчик, клапан или сообщение шины.",
                "3. Проверьте питание, массу и разъём этого устройства.",
                "4. Если код касается шины, проверьте разъёмы и жгут шины.",
                "5. Если код касается настроек, сверьте их с номером кузова и тахографом.",
                "6. Блок ZBR2 проверяйте последним, после всех подключённых устройств.",
            ]),
            ("Водителю в рейсе", [
                "Списка «ехать нельзя» здесь нет. Смотрите на лампы приборной панели и на то, что работает не так: пропали фары, не работает подогрев, не показывается уровень в бачке. Это вопросы сервиса.",
                "Если при записи появляются аварийные сигналы на приборной панели или машина теряет управляемость, остановитесь. Во всех остальных случаях запишите код, условия появления и вызовите сервис.",
            ]),
            ("Мастеру в сервисе", [
                "Считывайте все записи одним сеансом и сравнивайте их между собой. Код связи с шиной может стоять рядом с настоящей причиной в другом блоке, поэтому не начинайте с ZBR2, если в считывании есть записи подключённых блоков.",
                "При записи о наборе параметров сверьте номер кузова в тахографе и настройки ZBR2 с этой машиной. Если номера не совпадают, замена блока не решит проблему.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/propalo-pitanie.html|пропало питание]], [[/problemy/oshibka-tahografa.html|ошибка тахографа]], [[/problemy/gorit-check-engine.html|горит Check Engine]]",
                "[[/marki/man.html|MAN]], [[/marki/manebs.html|MAN EBS]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Код шины пришёл без других записей. С чего начать?",
             "С разъёмов шины и её жгута. Код связи не всегда означает поломку блока."),
            ("Код о наборе параметров появился после работы с тахографом. Менять блок?",
             "Нет. Сначала сверьте номер кузова и параметры с машиной и тахографом."),
            ("Пропало наружное освещение одного борта. Это ZBR2?",
             "Возможно, но сначала проверьте лампу, предохранитель и выключатель этой цепи. Запись по цепи выключателя указывает на её проверку в первую очередь."),
        ])],
    },

    "brand:powerstroke": {
        "head": [
            ("Что разобрано на этой странице", [
                "Страница относится к дизельным двигателям Ford Power Stroke. Записи здесь все в формате P-кодов: буква P и цифры. Группы в примерах - топливо, воздух и наддув, датчики температуры и давления, форсунки и их цепи, свечи накала, электропитание, трансмиссия.",
                "Коды короткие, поэтому смысл берите из описания рядом. У части записей описание указывает, что вызвало код: проводка, разъём, датчик, трубка или блок управления.",
            ]),
            ("Как читать коды этой страницы", [
                "Формат P-кодов общий для диагностики автомобилей и не привязан к стандарту J1939. Поэтому номер P0107 или P1263 не следует сравнивать с SPN из другой таблицы: смысл одинаков только внутри одной системы кодов.",
                "В тексте упомянуты блоки PCM, IDM и GPCM. PCM - блок управления силовым агрегатом, IDM — блок управления форсунками, GPCM — блок управления свечами накала. Записи с этими блоками сначала сверяйте с их цепями, а не с самим блоком.",
                "Если описания нет, используйте общий смысл P-кода. Если описание есть, оно важнее: например, на странице код датчика давления наддува прямо связан с забитой трубкой или шлангом.",
            ]),
            ("Основные системы и типовые причины", [
                "Форсунки. Записи про цепи форсунок отдельных цилиндров, короткое замыкание или обрыв между высокой и низкой стороной и общие записи по IDM похожи. Разводка жгута, сама форсунка и блок IDM дают похожие записи. Начинайте с разъёма и жгута на этом цилиндре, затем форсунка.",
                "Датчики давления наддува и атмосферного давления. Для датчика наддува на странице прямо указано, что причиной может быть забитая трубка или шланг. Проверяйте трубку и её соединение раньше датчика. Записи о барометрическом датчике относятся к сигналу; сначала проверяйте питание и сигнал датчика.",
                "Питание и заряд. Запись о пониженном напряжении бортовой сети связана с системой заряда и внутренней неисправностью PCM. Проверяйте аккумулятор, заряд и массы, прежде чем судить о блоке. Запись о цепи разрешения IDM указывает на реле, предохранитель или обрыв цепи.",
                "Свечи накала. Запись о цепи свечи накала первого цилиндра указывает на проводку, разъём, свечу, блок GPCM и PCM. Проверяйте по порядку: разъём и проводку, затем свечу.",
                "Температура и термостат. Запись о температуре масла вне диапазона для самодиагностики связана с тем, что двигатель слишком холодный или слишком горячий, и с термостатом. Сначала проверьте, как двигатель прогревается.",
                "Коробка. Записи о датчике положения селектора и соленоидах переключения передач относятся к трансмиссии. Сначала проверяйте датчик положения селектора и его цепь, затем соленоид.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код полностью и условия, при которых он появился: холод, нагрузка, пуск.",
                "2. Прочтите описание и определите, что записано: проводка, датчик, свеча, форсунка или блок.",
                "3. Для форсунок проверьте разъём и жгут на нужном цилиндре.",
                "4. Для датчиков давления проверьте трубку, шланг и разъём, затем питание и сигнал.",
                "5. Для питания проверьте аккумулятор, заряд и массы.",
                "6. Блок PCM, IDM или GPCM меняйте только после проверки всех цепей.",
            ]),
            ("Водителю в рейсе", [
                "Списка «ехать нельзя» на странице нет. Решайте по лампе двигателя и по поведению машины. Если мощность падает, двигатель глохнет, пропускает или загорелся сигнал давления, остановитесь.",
                "Если код касается датчика или одного цилиндра, а работа двигателя не меняется, запишите условия появления и езжайте к сервису. Настройки на ходу не меняйте.",
            ]),
            ("Мастеру в сервисе", [
                "Сравнивайте код с номером цилиндра и видом неисправности в описании. Для записей с IDM и PCM сначала проверяйте питание и массы блоков, а уже потом цепи форсунок.",
                "Записывайте, при каких условиях появился код: холодный пуск, нагрузка, подъём. Одинаковый код при разных условиях указывает на разные места проверки.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/ne-zavoditsya.html|не заводится]], [[/problemy/upala-moshchnost.html|упала мощность]], [[/problemy/glohnet-na-hodu.html|глохнет на ходу]]",
                "[[/problemy/gorit-check-engine.html|горит Check Engine]], [[/problemy/propalo-pitanie.html|пропало питание]], [[/problemy/ne-zaryazhaet-generator.html|не заряжает генератор]], [[/marki/ford.html|Ford Trucks]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Код форсунки пришёл один раз и пропал. Что делать?",
             "Пропавший код не значит, что причины нет. Проверьте разъём и жгут на этом цилиндре и наблюдайте за повтором."),
            ("Что проверить, если код датчика наддува появился после мойки двигателя?",
             "Проверить разъёмы и трубки датчика: влага и грязь в них дают неверные показания. Затем убедитесь, что соединения сухие и затянуты."),
            ("Нужно ли менять PCM, если горит код питания?",
             "Нет. Сначала проверьте аккумулятор, заряд и массы. Блок меняют, когда питание и сеть проверены."),
        ])],
    },

    "brand:international": {
        "head": [
            ("Что разобрано на этой странице", [
                "На странице два формата кодов International. Первый - стандарт J1939 с SPN и FMI: большинство записей разобрано по нему, и вверху вынесены коды, с которыми страница прямо говорит не ехать. Второй - дилерский формат, где номер короткий и стоит без SPN, а описание начинается после двоеточия.",
                "Для стандартных кодов страница группирует записи по системам: смазка, охлаждение, топливо, электропитание, CAN-шина, тормоза и прочие системы. Названия узлов взяты из заводской строки, поэтому доверяйте описанию на странице, а не общему названию из стандарта.",
            ]),
            ("Как читать коды этой страницы", [
                "SPN - что именно не в порядке: датчик, узел или параметр. FMI - вид неисправности: значение вне нормы, обрыв, замыкание, недостоверные данные. Страница прямо говорит, что «SPN без FMI» - это ещё не диагноз. Записывайте код полностью, с FMI.",
                "В дилерском формате запись выглядит так: номер, сокращение, двоеточие и описание. Всё, что стоит до двоеточия, - это блок или датчик, к которому относится запись. Всё, что после двоеточия, - сама неисправность. Например, запись ECM указывает на блок управления двигателем, а IDM — на блок управления форсунками.",
                "Сокращения MAP, MAT, CKP и INJ в записях означают датчики и цепи, которые описаны на странице. Другие сокращения, например EWPS, AMS, EBP или IPR, здесь не расшифровываются: смысл берите из описания рядом с номером.",
            ]),
            ("Основные системы и типовые причины", [
                "Топливо. SPN 97 - наличие воды в топливе. Сначала слейте отстой и проверьте фильтр, потом датчик воды. SPN 94 - давление топлива в системе подачи, SPN 1382 - перепад давления на топливном фильтре со стороны всасывания. Перепад давления на фильтре показывает, что фильтр и линия до насоса проверяются раньше остального.",
                "Электропитание. SPN 158 - напряжение аккумулятора на замке зажигания, SPN 168 - напряжение аккумулятора. SPN 1079 и SPN 1043 относятся к питанию датчиков, SPN 1089 - к питанию дополнительного оборудования. Питание датчиков проверяйте раньше самих датчиков.",
                "CAN-шина. SPN 639 - сеть J1939 номер один, SPN 1231 - сеть номер два, SPN 625 - проприетарная линия связи. Если запись касается сети, начинайте с разъёмов шины, потом с блоков на линии.",
                "Тормоза. SPN 70 - выключатель стояночного тормоза, SPN 597 - выключатель тормоза, SPN 1087 - давление воздуха рабочего тормоза, контур номер один. Пневматику и выключатели проверяйте до электроники: выключатель может быть исправен, а давление в контуре нет.",
                "Охлаждение и смазка. SPN 986 - запрошенная частота вращения вентилятора, SPN 175 - температура масла, SPN 177 - температура масла КПП. SPN 1378 - интервал замены масла - напоминание о плановой замене, на странице оно стоит отдельно от аварийных кодов смазки. Температурные записи проверяйте по самому маслу и уровню.",
            ]),
            ("Порядок проверки", [
                "1. Сначала проверьте коды из списка «ехать нельзя» на странице.",
                "2. Затем питание: аккумулятор, массы, предохранители, напряжение под нагрузкой.",
                "3. Потом датчик или выключатель, который записан в коде.",
                "4. Жгут и разъём до блока.",
                "5. Блок - только после того, как все пункты выше проверены.",
            ]),
            ("Водителю в рейсе", [
                "На странице прямо указаны коды, с которыми ехать нельзя: SPN 70, SPN 175, SPN 177, SPN 597, SPN 986 и SPN 1087. По ним остановитесь и не продолжайте движение, пока причина не проверена в сервисе. SPN 1378 (интервал замены масла) в этот список не входит: это напоминание о плановой замене, с ним можно доехать до сервиса. Проверьте уровень и давление масла и запланируйте замену.",
                "Остальные записи решайте по лампе и поведению машины. Если машина ведёт себя неровно, запись о воде в топливе или о напряжении питания - повод остановиться до проверки.",
            ]),
            ("Мастеру в сервисе", [
                "Для дилерского формата сверяйте, какой блок записал код: ECM, IDM, CKP и другие сокращения стоят перед двоеточием и показывают, куда смотреть. Номер сверяйте с полным описанием.",
                "При записях CAN сравните коды сразу нескольких блоков. Если сеть отказывает, часть блоков пишет ошибку связи, а сама причина может быть в одном из них или в разъёме.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/nizkoe-davlenie-masla.html|низкое давление масла]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]], [[/problemy/ne-zaryazhaet-generator.html|не заряжает генератор]]",
                "[[/problemy/oshibka-adblue.html|ошибка AdBlue]], [[/problemy/stoyanochnyy-tormoz.html|стояночный тормоз]], [[/kody/spn-168.html|SPN 168]], [[/kody/spn-70.html|SPN 70]], [[/kody/spn-639.html|SPN 639]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Код воды в топливе появился после заправки. Что делать?",
             "Сначала слейте отстой и проверьте фильтр, затем датчик воды. Если код остался, проверьте разъём датчика."),
            ("Можно ли ехать с SPN 70?",
             "По странице это код из списка «ехать нельзя». Остановитесь и проверьте выключатель стояночного тормоза."),
            ("Дилерский код 111 без ошибок - это авария?",
             "Страница пишет, что это только код мигания, без ошибки. Смысл записи - в её описании."),
        ])],
    },

    "brand:ivecoedc": {
        "head": [
            ("Что разобрано на этой странице", [
                "Страница относится к блоку управления двигателем Iveco EDC. Записи дилерские, номера короткие и записываются парой цифр через точку. В примерах видны сигналы скорости и сцепления, датчики температуры и давления воздуха, датчик оборотов турбины, форсунки, свечи накала, клапан моторного тормоза, связь с блоком тормозов EBS и иммобилайзер.",
                "Часть записей на странице отмечена как встречающаяся на старых моделях Iveco, например EuroTech и EuroStar. Это указание страницы, и его стоит сверять с типом вашей машины.",
            ]),
            ("Как читать коды этой страницы", [
                "Коды записываются парой цифр через точку, например 1.1 или 5.3. Структуру «первая цифра - узел, вторая - вид» страница не объясняет, поэтому её не выводите из номера. Смысл берите из текста рядом: в описании сказано, какой узел и что с ним не так.",
                "Некоторые записи содержат указание, что страдает вместе с узлом. Например, при коде 1.1 не работают тахограф и круиз-контроль. Эту часть описания полезно передать сервису вместе с заявкой.",
            ]),
            ("Основные системы и типовые причины", [
                "Скорость и сцепление. Код 1.1 означает, что сигнал скорости вышел за границы, возможно из-за замыкания в проводке. Код 1.5 - недостоверный сигнал выключателя или датчика давления сцепления; круиз-контроль и отбор мощности при нём не работают.",
                "Холодный пуск. Код 2.9 относится к реле свечей накала. Если питания на свечах нет, на странице указан тяжёлый холодный пуск и дым при запуске. Если питание подаётся постоянно, свечи выходят из строя, а аккумулятор садится. Проверяйте реле и цепь свечей.",
                "Датчики воздуха и давления. Код 2.2 - датчик температуры воздуха на впуске, код 2.5 - датчик атмосферного давления, который стоит внутри блока управления. Для обоих на странице указаны замыкание на плюс, на массу или обрыв. Сначала проверьте разъём и цепь, а блок - в последнюю очередь.",
                "Форсунки. Коды 5.3 и 5.6 относятся к электрической части форсунок третьего и шестого цилиндров. На странице сказано, что двигатель работает на пяти цилиндрах, поэтому запись заметна водителю. Для гаек проводов форсунок страница указывает проверить затяжку; величину берите из руководства на машину, а не из этой страницы.",
                "Моторный тормоз. Код 4.6 относится к электромагнитному клапану моторного тормоза: тормоз не работает или остаётся включённым на высоких оборотах. Проверяйте цепь клапана и разъём.",
                "Сеть и связь. Код 7.4 - обмен с блоком управления тормозами EBS. Код 7.7 - превышено время ожидания при обмене с другими блоками. Записи связи сначала проверяйте разъёмами и жгутом, потом блоками.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код с описанием и отметьте, что страдает вместе с узлом.",
                "2. Проверьте питание и массы блока.",
                "3. Проверьте разъём и цепь датчика или клапана, на который указывает код.",
                "4. Для форсунок проверьте затяжку и изоляцию проводов по руководству.",
                "5. Для связи проверьте жгут и разъёмы до блока EBS и других блоков.",
                "6. Блок EDC меняйте только после проверки всех пунктов выше.",
            ]),
            ("Водителю в рейсе", [
                "Списка «ехать нельзя» здесь нет. Решайте по лампе диагностики и по поведению двигателя. Если двигатель теряет мощность, плохо запускается на холодную или моторный тормоз остаётся включённым, остановитесь.",
                "Записи о скорости и сцеплении в дороге проверяйте по работе тахографа и круиз-контроля. Если они не работают, запишите код и условия появления и ведите машину, не полагаясь на эти функции.",
            ]),
            ("Мастеру в сервисе", [
                "Коды связи 7.4 и 7.7 могут означать проблему не в EDC, а в блоке-партнёре, поэтому читайте записи всех блоков сразу.",
                "Для кодов датчиков сравните, какой разъём и какая цепь записаны, и не меняйте датчик, пока цепь на замыкание не проверена. Для форсунок сверяйте номер цилиндра в записи.",
            ]),
            ("Связанные страницы", [
                "[[/marki/iveco.html|Iveco]], [[/marki/ivecoeurotronic.html|Iveco EuroTronic]], [[/problemy/oshibka-tahografa.html|ошибка тахографа]]",
                "[[/problemy/ne-rabotaet-motornyy-tormoz.html|не работает моторный тормоз]], [[/problemy/ne-zavoditsya.html|не заводится]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Код 1.1 пропал, но тахограф по-прежнему не работает. Почему?",
             "Пропавший код не означает, что тахограф восстановлен. Проверьте проводку сигнала скорости и разъёмы."),
            ("Почему двигатель тяжело заводится на холодную?",
             "По странице при коде реле свечей накала без питания на свечах будет тяжёлый холодный пуск. Проверьте реле и питание свечей."),
            ("Можно ли менять блок EDC по одному коду?",
             "Нет. Блок меняют после проверки питания, масс и разъёмов по всем записям."),
        ])],
    },

    "brand:ivecoeurotronic": {
        "head": [
            ("Что разобрано на этой странице", [
                "Страница относится к автоматизированной коробке Iveco EuroTronic. Коды на ней короткие, например 02 и 07, и в основном описывают электроклапаны, датчики положения, реле, линию связи с дисплеем и питание коробки.",
                "Группы, которые видны в примерах: клапаны переключения, делитель, инерционный и моторный тормоз, датчики положения, механизм переключения передач, сцепление, сигнал ASR и питание. Выбирайте запись по её описанию, потому что короткий номер сам по себе ничего не объясняет.",
            ]),
            ("Как читать коды этой страницы", [
                "Номер двух или трёхзначный, после него текст. В тексте указано, что сломано и как: клапан с замыканием на массу, обрыв цепи, замыкание на плюс, неисправность датчика или механизма.",
                "Буквенные обозначения в описаниях - это клапаны и датчики, которые страница называет по их обозначению на схеме: например, Y2 - клапан управления делителем, B4 - датчик положения включения передач, B7 - датчик положения делителя. Сверяйте обозначение с вашей схемой, а не с общим списком.",
            ]),
            ("Основные системы и типовые причины", [
                "Электроклапаны. Записи о замыкании на массу или на плюс у клапанов Y1, Y2 и Y5 говорят о проводке и разъёме клапанного блока. Прежде чем менять клапан, проверьте жгут и разъём клапанного блока на всём пути.",
                "Реле моторного тормоза. Записи о замыкании и обрыве цепи реле отключения моторного тормоза относятся к реле и его проводке. Если тормоз не отключается или не включается, проверяйте реле и цепь до блока коробки.",
                "Питание. Запись 57 о неверном напряжении питания переводит коробку в аварийный режим по описанию страницы. Запись 105 о слишком низком напряжении сопровождается лампой СТОП. Питание коробки проверяйте до того, как искать механику.",
                "Механика. Коды о самокалибровке датчика положения включения передач, о механизме, который не переходит в новое положение, и о сцеплении, которое не включается, связаны с механикой. Датчик может быть исправен, а механизм стоит. Проверяйте механизм на месте и его привод.",
                "Дисплей и связь. Запись о линии связи с дисплеем и о сигнале ASR относится к проводке. Проверяйте разъём и жгут до блока.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код с номером и текстом и отметьте, какой элемент записан: клапан, датчик, реле, механизм или связь.",
                "2. Проверьте питание коробки и массы, если в записи есть напряжение.",
                "3. Для клапанов и реле проверьте разъём клапанного блока и жгут.",
                "4. Для датчиков положения проверьте разъём и самокалибровку по инструкции.",
                "5. Для механики проверьте ход механизма на месте.",
                "6. Блок коробки меняйте только после проверки всех пунктов.",
            ]),
            ("Водителю в рейсе", [
                "На странице сказано, что при кодах 57, 93, 105 и 119 загорается лампа СТОП и звучит зуммер. Это указание страницы: при свечении СТОП остановитесь, проверьте машину и только потом решайте, ехать ли дальше.",
                "По остальным записям списка «ехать нельзя» на странице нет. Смотрите на поведение коробки: если она переходит в аварийный режим или не переключает передачи, остановитесь. Если поведение обычное, запишите код и проверьте в сервисе.",
            ]),
            ("Мастеру в сервисе", [
                "Перед заменой клапана проверьте жгут и разъём клапанного блока. Запись о замыкании на массу может идти от повреждённой изоляции, а не от клапана, поэтому смотрите проводку.",
                "Для механики сравнивайте работу механизма с записью о датчике. Если датчик показывает одно, а механизм стоит, не заменяйте датчик: сначала проверьте ход механизма.",
            ]),
            ("Связанные страницы", [
                "[[/marki/iveco.html|Iveco]], [[/marki/ivecoedc.html|Iveco EDC]], [[/problemy/propalo-pitanie.html|пропало питание]]",
                "[[/problemy/ne-pereklyuchayutsya-peredachi.html|не переключаются передачи]], [[/problemy/ne-rabotaet-motornyy-tormoz.html|не работает моторный тормоз]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Код 02 появился сразу после замены клапана. Почему?",
             "Возможно, виноваты жгут или разъём, а не сам клапан. Проверьте, не замкнута ли проводка на массу после установки."),
            ("Почему загорелся СТОП и звучит зуммер?",
             "По странице это коды 57, 93, 105 и 119. Проверьте, какой из них записан, остановитесь и проверьте питание и узел из записи."),
            ("Коробка переключает не все передачи. Это код?",
             "Смотрите записи про механизм переключения и датчик положения. Механику проверяйте на месте, не только электрику."),
        ])],
    },

    "brand:webasto": {
        "head": [
            ("Что разобрано на этой странице", [
                "Webasto — производитель отопителей; эта страница — про коды отопителя, а не двигателя или коробки. Коды на странице короткие, например 00, 02, 0A и 9A. Они описывают запуск отопителя, пламя, перегрев, свечу накаливания, вентилятор, топливный насос, датчики температуры и пламени, шину W-Bus и кодировку блока управления.",
                "Отопитель записан на странице отдельно от двигателя, поэтому разбор ведётся по нему самому. Эти записи не относятся к двигателю или трансмиссии.",
            ]),
            ("Как читать коды этой страницы", [
                "Код 00 на странице означает «ошибок нет», поэтому ищите запись с ненулевым номером. Коды бывают цифровыми, например 04 или 17, и с буквой, например 0A или 1B. Ищите код целиком: 1B и 17 - разные записи.",
                "Водитель на таймере видит F-код (F00-F19), а программа Webasto Thermo Test показывает ПК-код. Это разные числа: например, F03 на таймере - это ПК-коды 04 и 84, а ПК-код 03 на таймере выглядит как F02. Одному F-коду отвечает несколько ПК-кодов, а у разных моделей (Air Top 2000 ST, Thermo Top Evo, Air Top Evo 40/55, Thermo Pro 90) он может значить разное: смотрите страницу нужного F-кода.",
                "У Eberspächer, как сказано на странице, нулевая строка тоже означает отсутствие неисправностей. Это удобно при сравнении отопителей, но описания кодов одного производителя нельзя переносить на другого.",
            ]),
            ("Основные системы и типовые причины", [
                "Запуск и пламя. Код 02 - неудачный запуск, код 82 - неудачный запуск в тестовом режиме. Код 19 - короткое замыкание цепи свечи накаливания, 0A - короткое замыкание свечи или датчика пламени (в таблице Thermo Top Evo), 9A - обрыв цепи датчика пламени. Сначала проверьте свечу и разъём, затем датчик пламени.",
                "Топливо. Код 88 - обрыв цепи топливного насоса. Проверьте разъём насоса и цепь, потом сам насос.",
                "Перегрев. Код 17 - превышен градиент нарастания температуры, код 1B - короткое замыкание датчика перегрева. Перегрев - вопрос безопасности, поэтому отопитель с такой записью не эксплуатируйте, пока причина не найдена.",
                "Вентилятор. Код 09 - короткое замыкание вентилятора. Проверяйте разъём вентилятора и его цепь.",
                "Напряжение и связь. Код 04 - напряжение питания слишком высокое, код 12 - ошибка шины W-Bus, код 11 - неверная кодировка блока управления, код 91 - блок закодирован нейтрально. Кодировку выделяем отдельно: перед заменой блока сверьте её по инструкции.",
                "Температурный датчик. Код 94 - обрыв цепи датчика температуры. Проверяйте разъём датчика и провод до блока.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код целиком и отметьте, что он говорит: запуск, пламя, перегрев или связь.",
                "2. Перед любой работой отключите отопитель и дайте ему остыть по инструкции.",
                "3. Проверьте разъёмы, предохранители и питание.",
                "4. Для пламени и свечи проверьте свечу и датчик пламени.",
                "5. Для перегрева проверьте датчик температуры и вентилятор.",
                "6. Блок управления меняйте только после проверки кодировки.",
            ]),
            ("Водителю в рейсе", [
                "Списка «ехать нельзя» для отопителя на странице нет: он записан отдельно от движения. Решайте по его поведению и по безопасности в кабине.",
                "Если в кабине появился запах гари, выхлопа или топлива, выключите отопитель, проветрите кабину и вызовите сервис. Не пользуйтесь отопителем, пока причина не установлена.",
            ]),
            ("Мастеру в сервисе", [
                "Перед диагностикой отключите отопитель, проверьте топливо и линии, выхлоп и вентиляцию. Работы с выхлопом и топливом ведите по инструкции изготовителя и не оставляйте утечек без проверки.",
                "Для кодов перегрева и пламени сначала проверьте вентиляцию и выхлоп, потом электрику. Записи о кодировке и шине W-Bus сверяйте с блоком управления отопителя.",
            ]),
            ("Связанные страницы", [
                "[[/marki/webasto.html|Webasto]], [[/marki/eberspacher.html|Eberspächer]], [[/otopiteli/#webasto|отопители: раздел Webasto]]",
                "[[/problemy/propalo-pitanie.html|пропало питание]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Код 00 - это ошибка?",
             "Нет. На странице 00 означает «ошибок нет»."),
            ("Отопитель не запускается. Что проверить первым?",
             "Топливо, свечу и датчик пламени по записям 02, 9A и 0A. Не вскрывайте отопитель на ходу."),
            ("Можно ли пользоваться отопителем с записью о перегреве?",
             "Нет, пока перегрев не проверен. Коды 17 и 1B на странице относятся к температуре."),
        ])],
    },

    "brand:allison": {
        "head": [
            ("Что разобрано на этой странице", [
                "Страница относится к автоматической коробке Allison. Записи смешанного формата: короткие номера вроде 11 и 12 и коды вида P0121, C1312 и U0010. Почти все записи про трансмиссию: соленоиды, датчики давления и скорости, блокировку гидротрансформатора, ретардер и сеть CAN.",
                "Страница отдельно отмечает, что коробка, двигатель и приборы могут записывать похожие по смыслу коды с разными номерами. Поэтому перед разбором определите, из какого блока пришёл код.",
            ]),
            ("Как читать коды этой страницы", [
                "В описаниях есть указание, что делает коробка в ответ на неисправность: диагностика активна, соленоиды отключены, активен аварийный режим, блокировка гидротрансформатора запрещена. Эти фразы говорят о поведении коробки и важнее номера.",
                "Некоторые записи на странице сопровождаются лампой CHECK TRANS, которая загорается при них. Лампа - ещё один признак, что запись влияет на работу коробки, и её стоит учитывать при разборе.",
            ]),
            ("Основные системы и типовые причины", [
                "Соленоиды и гидравлика. Код P0962 - низкое напряжение цепи соленоида регулирования давления: соленоиды при нём отключены, а гидравлическое управление активно. Коды P0776 и P2724 относятся к гидравлическим цепям соленоидов PCS2 и PCS1, при них активен аварийный режим. Код P0975 - обрыв цепи соленоида SS2: на семиступенчатой коробке отключаются переключения с первой по седьмую. Начинайте с разъёма и жгута соленоида, а гидравлику проверяйте после.",
                "Датчики давления и скорости. Код P0847 - низкое напряжение датчика давления PS2. Код P0717 - нет сигнала датчика скорости турбины: коробка блокируется на текущей передаче. Код P1714 - датчик давления заднего хода заклинил во включённом положении.",
                "Тормоз и ретардер. Код P0703 - проблема с сигналом выключателя тормоза. На мусоровозах при нём блокируется переключение N-D, а работа ретардера запрещена. Код C1312 - низкое напряжение сигнала запроса ретардера, ретардер отключён.",
                "Двигатель и CAN. Код P1779 - крутящий момент двигателя, переданный в ECM, недостоверен. Код U0010 - переполнение счётчика шины CAN; тогда используются значения по умолчанию, а управление моментом при переключении отключено.",
                "Опции автомобиля. Код P0610 - ошибка аппаратной части опций автомобиля. Используются калибровочные данные из модуля TID. Перед заменой модуля проверьте, что опции записаны верно.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите код и отметьте, что делает коробка: аварийный режим, блокировка, отключённые соленоиды.",
                "2. Определите, какой блок записал код: коробка, двигатель или приборы.",
                "3. Для соленоидов проверьте разъём, жгут и питание цепи.",
                "4. Для датчиков давления и скорости проверьте разъём и сигнал.",
                "5. Для тормоза и ретардера проверьте выключатель и его сигнал.",
                "6. Для CAN проверьте разъёмы сети. Модуль коробки меняйте после проверки всех пунктов.",
            ]),
            ("Водителю в рейсе", [
                "Списка «ехать нельзя» на странице нет. Решайте по лампе CHECK TRANS, если она загорелась, и по поведению коробки.",
                "Если коробка в аварийном режиме или блокирована на текущей передаче, остановитесь и вызовите сервис. Если коробка работает как обычно, запишите код и условия и проверьте на стоянке.",
            ]),
            ("Мастеру в сервисе", [
                "Сверяйте, какой модуль записал код: коробка, ECM или приборы. Для P0703 учтите тип машины: страница отмечает, что на мусоровозах при нём блокируется переключение N-D.",
                "Для кодов соленоидов сначала проверьте электрику, потом гидравлику. Для P1779 и U0010 сверьте связь с двигателем по CAN, а не только коробку.",
            ]),
            ("Связанные страницы", [
                "[[/marki/allison.html|Allison]], [[/problemy/ne-pereklyuchayutsya-peredachi.html|не переключаются передачи]], [[/problemy/upala-moshchnost.html|упала мощность]]",
                "[[/problemy/oshibka-retardera.html|ошибка ретардера]], [[/problemy/stoyanochnyy-tormoz.html|стояночный тормоз]], [[/problemy/gorit-check-engine.html|горит Check Engine]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Коробка работает не на всех передачах. Что это?",
             "Смотрите записи про соленоиды и аварийный режим. Страница описывает отключение переключений при коде SS2 на семиступенчатой коробке. Проверьте соленоид и его жгут."),
            ("Код P0703 появился на мусоровозе. Почему не включается N-D?",
             "По странице на мусоровозах при этом коде переключение N-D блокируется. Проверьте выключатель тормоза и его сигнал."),
            ("Ретардер не работает, код C1312. Что делать?",
             "Код говорит о низком напряжении сигнала запроса ретардера. Проверьте сигнал и разъём, затем блок ретардера."),
        ])],
    },

    "brand:fuso": {
        "head": [
            ("Что разобрано на этой странице", [
                "Страница относится к грузовикам Mitsubishi Fuso. Записи здесь в формате P-кодов, например P0016, P0101 и P2102. Группы в примерах: воздух и датчик массового расхода, педаль газа, рециркуляция отработавших газов, фильтр сажи DPF, шина CAN, опорное напряжение датчиков, дроссельная заслонка, блок ECU и вспомогательный тормоз.",
                "Часть записей содержит мигающий код - номер, который видно по миганию лампы. Он указан отдельно от P-кода и нужен для сверки.",
            ]),
            ("Как читать коды этой страницы", [
                "Смысл записан в той же строке, что и номер. Общие P-коды OBD-II используйте, только когда описания нет. Описание важнее общего смысла, потому что страница иногда уточняет узел: например, для датчика давления DPF указано, что это датчик перепада давления.",
                "В записях с пометкой «двигатель 4M50» указано, что описание относится к этому двигателю. Записи без такой пометки страница к этому двигателю не привязывает.",
                "Мигающий код и P-код - разные вещи. Мигающий код сверяйте с миганием лампы, P-код - со строкой описания. Одна и та же неисправность может быть записана обоими способами.",
            ]),
            ("Основные системы и типовые причины", [
                "Воздух и педаль газа. Записи о датчике массового расхода воздуха и о датчике оборотов двигателя относятся к сигналу. Записи о датчиках положения педали газа с мигающими кодами указывают на проводку и разъём педали. Сначала проверяйте разъёмы и провода датчиков.",
                "Фильтр сажи. Запись о датчике перепада давления DPF относится к датчику и его трубкам. Перед выводом о засоре фильтра проверьте трубки и разъём датчика.",
                "Рециркуляция и форсунки. Запись о недостаточном потоке EGR относится к рециркуляции, а запись о низком уровне сигнала форсунки номер два - к её цепи. Проверяйте форсунку вместе с жгутом на её цилиндре.",
                "Вспомогательный тормоз. Запись про электромагнитный клапан вспомогательного тормоза относится к клапану и его цепи. Проверяйте разъём и провод клапана.",
                "Блок ECU и сеть. Запись о программном обеспечении блока ECU не решается заменой блока без проверки программы. Запись о шине CAN относится к обмену данными между блоками; сначала разъёмы и жгут.",
                "Дроссель и атмосферное давление. Запись о приводе дроссельной заслонки с коротким замыканием относится к приводу и его проводке. Запись о датчике атмосферного давления с недостоверным сигналом относится к самому датчику.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите P-код и мигающий код отдельно, если оба есть.",
                "2. Прочтите описание и определите, что записано: датчик, цепь, клапан, блок или сеть.",
                "3. Проверьте разъёмы и жгуты на этом узле.",
                "4. Для датчиков проверьте сигнал и питание по инструкции.",
                "5. Для сети проверьте разъёмы и жгут между блоками.",
                "6. Блок ECU меняйте только после проверки питания, масс и программы.",
            ]),
            ("Водителю в рейсе", [
                "Списка «ехать нельзя» на этой странице нет. Решайте по лампе и поведению машины. Если двигатель теряет мощность, глохнет или не набирает тягу, остановитесь.",
                "Если запись касается одного датчика и двигатель работает без изменений, запишите мигающий код и условия появления и вызовите сервис.",
            ]),
            ("Мастеру в сервисе", [
                "Для записей с мигающими кодами сначала сверьте мигание с кодом на странице: это два разных списка, номера из них не путайте.",
                "Для педали газа и датчиков давления проверяйте сигнал и питание, а не только запись. Блок ECU не меняйте из-за одной записи о программе без проверки самой программы.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/zabit-sazhevyy-filtr.html|забитый сажевый фильтр]], [[/problemy/ne-idet-regeneratsiya.html|не идёт регенерация]], [[/problemy/datchik-nox.html|датчик NOx]]",
                "[[/problemy/upala-moshchnost.html|упала мощность]], [[/problemy/glohnet-na-hodu.html|глохнет на ходу]], [[/problemy/ne-rabotaet-motornyy-tormoz.html|не работает моторный тормоз]], [[/marki/fuso.html|Mitsubishi Fuso]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Что значит мигающий код в записи?",
             "Это номер, который видно по миганию лампы. Страница указывает его отдельно от P-кода. Сверяйте его по миганию, а не по P-коду."),
            ("Код P0600 без других записей. Что делать?",
             "Проверьте сеть CAN: разъёмы и жгут между блоками. Блок меняйте только после проверки питания."),
            ("Датчик перепада давления DPF показывает ошибку. Менять его сразу?",
             "Нет. Проверьте трубки и разъём датчика, затем сам датчик."),
        ])],
    },

    "brand:caterpillar": {
        "head": [
            ("Что разобрано на этой странице", [
                "Страница относится к дилерским кодам Caterpillar. Номера записаны парой чисел через точку, например 1.11 или 100.11. Группы в примерах: топливо и форсунки, впуск и турбонаддув, давление масла, охлаждение, выпуск и SCR, очистка выхлопа, педаль тормоза, скорость двигателя и дроссельная заслонка.",
                "Таблица Caterpillar собрана по собственной системе. Соленоиды форсунок и датчики расписаны по цилиндрам, поэтому номер цилиндра стоит в описании, а не в номере кода.",
            ]),
            ("Как читать коды этой страницы", [
                "Номер через точку состоит из двух частей: номер узла по системе Caterpillar и вид неисправности. Номер узла не совпадает с SPN из J1939, поэтому сравнивать его с таблицами SPN нельзя. Вид неисправности описан на странице словами - ориентируйтесь на описание.",
                "Описание указывает узел и вид сбоя: ток ниже нормы, напряжение выше нормы, короткое замыкание, очень низкое давление, вне калибровки. Эта часть записи важнее самого номера.",
                "Одинаковая вторая часть встречается у разных узлов. Например, 1.11 относится к соленоиду форсунки, 32.11 - к соленоиду перепускной заслонки турбины, а 100.11 - к датчику давления масла. Поэтому по одному окончанию номера узел не определяйте.",
            ]),
            ("Основные системы и типовые причины", [
                "Давление масла. Запись 100.11 - датчик давления масла, очень низкое давление масла. Сначала проверяйте само давление масла и его уровень, потом датчик. Датчик без проверки давления не даёт права считать, что давление в норме.",
                "Охлаждение. Запись 111.1 относится к датчику уровня охлаждающей жидкости, уровень ниже нормы. Сначала проверьте уровень в системе, затем датчик и его разъём.",
                "Впуск и турбина. Запись 32.11 относится к соленоиду перепускной заслонки турбины, 70.5 - к впускному обогревателю, 105.3 - к датчику температуры впускного коллектора. Для каждой записи проверяйте свой элемент: соленоид, обогреватель или датчик.",
                "Топливо и форсунки. Запись 1.11 - соленоид форсунки первого цилиндра, ток ниже нормы или открыт. Запись 164.3 относится к датчику давления срабатывания впрыска, напряжение выше нормы. Проверяйте разъём и цепь до датчика.",
                "Выпуск и SCR. Записи 315.2, 320.0 и 324.3 касаются температуры и перепада давления в системе очистки выхлопа. Записи 334.5 и 349.1 касаются привода подачи топлива и давления продувочного воздуха. Здесь проверяйте привод и датчик, а не сам блок.",
                "Педаль и дроссель. Запись 247.11 - переключатель второй педали тормоза не отвечает. Запись 91.13 - положение дроссельной заслонки вне калибровки: проверьте калибровку, а не только механику.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите номер и описание полностью, отметьте узел.",
                "2. Для давления масла сначала проверьте уровень и давление, потом датчик.",
                "3. Для охлаждения проверьте уровень жидкости.",
                "4. Для форсунок и датчиков давления проверьте разъём и цепь.",
                "5. Для выпуска и SCR проверьте привод и датчик по инструкции.",
                "6. Блок меняйте только после проверки всех пунктов.",
            ]),
            ("Водителю в рейсе", [
                "Списка «ехать нельзя» здесь нет, поэтому смотрите на лампу и на поведение двигателя.",
                "Запись о низком давлении масла при работе двигателя требует остановки: проверьте уровень и давление масла, а не только датчик. Записи о температуре и SCR решайте по поведению двигателя: если он теряет мощность или греется, остановитесь.",
            ]),
            ("Мастеру в сервисе", [
                "Записи с одинаковым окончанием номера относятся к разным узлам. Сверяйте описание для каждого номера, а не общий смысл.",
                "Для записей SCR и очистки выхлопа сравните показания датчиков и приводов при холодном и тёплом двигателе. Записывайте, при каких условиях код появляется.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/nizkoe-davlenie-masla.html|низкое давление масла]], [[/problemy/peregrev-dvigatelya.html|перегрев двигателя]], [[/problemy/troit-dvigatel.html|троит двигатель]]",
                "[[/problemy/oshibka-adblue.html|ошибка AdBlue]], [[/problemy/datchik-nox.html|датчик NOx]], [[/marki/caterpillar.html|Caterpillar]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Датчик давления масла показывает очень низкое давление. Что первое?",
             "Проверить давление масла и его уровень. Датчик проверяйте после этого."),
            ("Что значит 1.11?",
             "По описанию это соленоид форсунки первого цилиндра: ток ниже нормы или открыт. Проверьте разъём и цепь этой форсунки."),
            ("Записи системы очистки пропадают на ходу. Что делать?",
             "Записать условия появления, проверить разъёмы датчиков и приводов при вибрации и отдать записи в сервис."),
        ])],
    },

    "brand:deutz": {
        "head": [
            ("Что разобрано на этой странице", [
                "Страница относится к дилерским кодам Deutz. По системам это в основном выпуск и AdBlue (SCR), топливо и воздух. В записях есть номера с точкой, например 100.0 и 3031.2, описание, а у части записей - блинк-код и код, записанный рядом.",
                "Группы в примерах: давление и температура масла, форсунки и пропуски зажигания, воздушный отопитель, датчики AdBlue и SCR, датчики педали газа, датчики частоты вращения, клапан рециркуляции и клапан подачи масла на охлаждение поршней.",
            ]),
            ("Как читать коды этой страницы", [
                "Номер с точкой - это SPN и FMI по J1939: первая часть - узел, вторая - вид неисправности. Например, 100.0 - давление масла (SPN 100) с критическим превышением. Номера больше 516000, например 516408 или 516201, - собственные номера Deutz: в общей таблице J1939 их нет, смысл - только в описании на странице.",
                "Блинк-код - число, которое выводит мигание лампы. На странице он указан рядом с записью отдельно от номера. Код, записанный рядом, тоже указан отдельно. Сверяйте номер, блинк-код и описание, а не один из них.",
                "В части описаний встречается префикс EMR3. EMR3 - это блок управления двигателем Deutz; префикс показывает, что запись сделал он. В записи FMI 11 сказано, что характер неисправности не определён.",
            ]),
            ("Основные системы и типовые причины", [
                "Масло. Код 100.0 - критическое превышение давления масла. Код 175.0 - критический перегрев масла, при котором на странице указана реакция системы. Код 4812.11 относится к клапану подачи масла на охлаждение поршней, электрическая неисправность.",
                "Форсунки и зажигание. Код 653.11 - короткое замыкание одиночного инжектора третьего цилиндра. Код 516408.31 - форсунка восьмого цилиндра, не удалась коррекция малых подач по напряжению. Код 1323.12 - пропуск зажигания в первом цилиндре, неисправное устройство.",
                "Воздушный отопитель. Код 730.5 - магнитный клапан воздушного отопителя, обрыв или короткое замыкание кабеля.",
                "AdBlue и SCR. Код 3031.2 - датчик температуры бака AdBlue, недостоверные данные. Код 4334.2 - датчик давления AdBlue в системе SCR, недостоверные данные. Код 516201.11 - датчик NH3, ошибка сопротивления. Сначала проверяйте реагент и разъёмы датчиков, потом сами датчики.",
                "Педаль и датчики. Код 516098.14 - датчик педали газа 2, ошибка массы. Код 516572.3 - многопозиционный переключатель, замыкание на плюс. Код 516819.31 - датчики частоты вращения, слишком большая разница фазовых углов. Код 102.30 - датчик давления во впускном коллекторе, замыкание на массу или обрыв.",
                "Рециркуляция. Код 27.11 - привод клапана EGR, причина не определена. Проверяйте привод, его разъём и механику.",
            ]),
            ("Порядок проверки", [
                "1. Выпишите номер, блинк-код и описание, отметьте систему.",
                "2. Для масла сначала проверьте уровень и давление, потом датчики.",
                "3. Для AdBlue проверьте реагент и бак, потом датчики и разъёмы.",
                "4. Для форсунок и зажигания проверьте разъёмы и жгут на нужном цилиндре.",
                "5. Для педали и датчиков частоты проверьте массы и разъёмы.",
                "6. Блок управления меняйте после проверки всех пунктов.",
            ]),
            ("Водителю в рейсе", [
                "Списка «ехать нельзя» на странице нет. Записи, которые на странице названы критическими, требуют остановки: это код 100.0 о превышении давления масла и код 175.0 о критическом перегреве масла.",
                "Остальные записи решайте по лампе и поведению двигателя. Если двигатель теряет мощность, пропускает или работает неровно, остановитесь.",
            ]),
            ("Мастеру в сервисе", [
                "Сверяйте номер, блинк-код и код, записанный рядом. Они стоят в записи как дополнительные обозначения, и без сверки номера легко перепутать узлы.",
                "Для кодов AdBlue начинайте с реагента и бака. Для кодов масла проверяйте давление и температуру до того, как менять датчик.",
            ]),
            ("Связанные страницы", [
                "[[/kody/spn-100.html|SPN 100 - давление масла]], [[/problemy/nizkoe-davlenie-masla.html|низкое давление масла]], [[/problemy/peregrev-dvigatelya.html|перегрев двигателя]]",
                "[[/problemy/oshibka-adblue.html|ошибка AdBlue]], [[/problemy/datchik-nox.html|датчик NOx]], [[/marki/deutz.html|Deutz]]",
            ]),
        ],
        "tail": [("Вопросы и ответы", [
            ("Код 100.0 - это давление масла?",
             "Да, по странице 100.0 - критическое превышение давления масла. Остановитесь и проверьте уровень и давление масла."),
            ("Что такое блинк-код?",
             "Число, которое выводит мигание лампы. Страница указывает его отдельно от номера записи. Сверяйте его с записью, а не с номером с точкой."),
            ("Датчик AdBlue выдаёт недостоверные данные. Менять его?",
             "Сначала проверьте реагент и разъём датчика, затем сам датчик."),
        ])],
    },

})


# ---------------------------------------------------------------------
# Партия 3 (31.10.2026): шесть марок, русские тексты (ключ brand:<марка>) и
# английские (ключ brand-en:<марка>, их читает build_en_marki_problemy.py).
# Источники и проверка - _мозг/черновики/партия-3-марки/istochniki.md.
EXTRA_BLOCKS.update({
    "brand:bendix": {
        "head": [
            ("Что разобрано на этой странице", [
                "Bendix - поставщик тормозной электроники: блоки ABS, ATC и ESP для тягачей, грузовиков и прицепов. Страница относится к этой электронике, а не к двигателю и не к самим тормозным механизмам. Коды записаны по J1939: номер узла (SPN) и вид неисправности (FMI) идут парой.",
                "У Bendix есть и второй способ чтения: блинк-коды. Лампа ABS на приборах выдаёт серию вспышек, и каждый код состоит из двух групп (первая и вторая цифры). В таблицах Bendix каждому блинк-коду соответствуют одновременно номер J1587 (SID), SPN и FMI. Это одна и та же неисправность, записанная тремя способами, а не три разные.",
            ]),
            ("Как читать коды этой страницы", [
                "SPN называет узел, FMI называет вид отказа. Например, в таблице Bendix у датчиков скорости колёс стоят SPN с 789 по 794 (по одному на колесо), а блок управления записан под SPN 629. Общий список FMI одинаков для всех марок: 3 - напряжение выше нормы, 4 - ниже нормы, 2 - данные недостоверны, 9 - аномальная частота обновления.",
                "Блинк-код нельзя сравнивать с SPN напрямую: это номер, который собирается из числа вспышек. Двузначный блинк-код сначала переводится по таблице Bendix в SPN и FMI и только потом сверяется со страницей. Обратная ошибка тоже встречается: двузначное число принимают за SPN.",
                "Буквы в описаниях Bendix означают расположение: SA, DA и AA - оси (рулевая, ведущая и дополнительная), Left и Right - сторона. Для кодов колёс это важно: левая и правая стороны одной оси дают разные номера.",
            ]),
            ("Как получить блинк-коды", [
                "По руководству Bendix, режим включается кнопкой диагностики: одно нажатие - активные коды, два - неактивные (записанные раньше), три - стирание активных кодов. Другие нажатия включают проверку конфигурации системы, режим стенда и перенастройку блока. Перед нажатием подождите не менее двух секунд после включения зажигания.",
                "Блок не входит в режим блинк-кодов, если по датчикам колёс машина движется, а при начале движения выходит из режима. Вспышки идут по полсекунды, пауза между цифрами кода 1,5 секунды, между сообщениями 2,5 секунды, в конце лампа горит 5 секунд. Всё это - из сводки Bendix к блоку EC-60, схема для других блоков может отличаться, поэтому сверяйтесь с листом данных на вашу модель.",
            ]),
            ("Что проверить при кодах", [
                [
                    "Датчики скорости колёс: зазор до зубчатого кольца, загрязнение, обрыв провода, повреждение разъёма. В таблице Bendix для датчиков колеса есть отдельные записи по зазору и по выходному сигналу при трогании.",
                    "Клапаны давления (модуляторы): короткое замыкание на массу или на плюс и обрыв цепи записываются отдельными кодами для каждого клапана.",
                    "Питание: код низкого напряжения аккумулятора идёт отдельной записью. Проверяйте клеммы, массу и предохранитель раньше датчиков.",
                    "Сеть J1939: у ESP есть записи о недостоверных сообщениях от других блоков. Они указывают на сеть или на соседний блок, а не на тормоза.",
                    "Датчики ESP: угол поворота руля, скорость рыскания, поперечное ускорение. Для датчика угла в таблице есть запись о незавершённой калибровке, она устраняется калибровкой, а не заменой.",
                ],
                "Загрязнённое зубчатое кольцо или окисленный разъём дают код датчика колеса при исправном датчике. Сначала осмотр и очистка, потом замена.",
            ]),
            ("Порядок проверки", [
                "1. Запишите все коды целиком, с SPN и FMI. Если читаете миганием, запишите число вспышек каждой группы и переведите их по таблице на вашу модель блока.",
                "2. Отдельно отметьте активные и неактивные коды. Неактивный код - это неисправность, которая была, но сейчас не видна.",
                "3. Проверьте питание и массу блока, затем разъёмы и жгут у оси.",
                "4. Для датчика колеса осмотрите кольцо и зазор по руководству на ось. Значения в справочнике не приводятся.",
                "5. После устранения стирайте коды. По руководству Bendix активные коды стираются выключением и включением зажигания, а коды датчиков скорости - только после того, как блок снова видит корректную скорость всех колёс.",
                "6. Проверьте повтор в обычной поездке. Один запуск без повтора ничего не доказывает.",
            ]),
            ("Водителю в рейсе", [
                "Горящая лампа ABS означает, что антиблокировка не работает, даже если тормоза в целом тормозят. Обычное пневматическое торможение при этом остаётся, но защиты от блокировки колёс нет. На мокрой и скользкой дороге увеличивайте дистанцию и не рассчитывайте на защиту.",
                "Если вместе с лампой ABS горит красная лампа тормозов или давление воздуха падает, остановитесь в безопасном месте. Одна жёлтая лампа ABS обычно позволяет доехать до сервиса, но откладывать разбор не стоит.",
            ]),
            ("Мастеру в сервисе", [
                "Блинк-коды заменяют сканер только тогда, когда его нет под рукой. Полную таблицу, неактивные коды и историю событий лучше читать диагностическим прибором. Не переводите блинк-код по таблице другой модели блока: нумерация зависит от серии (EC-60, EC-80 и т. д.).",
                "Не меняйте блок ради одного кода. Сначала питание, масса, разъёмы и жгут. После замены датчика, блока или модулятора может потребоваться калибровка или перенастройка, это указано в листе данных на модель.",
            ]),
            ("Связанные страницы", [
                "[[/marki/wabco.html|WABCO - другая тормозная электроника]], [[/problemy/gorit-lampa-abs.html|горит лампа ABS]]",
                "[[/kody/spn-629.html|SPN 629 - контроллер №1]], [[/kody/spn-639.html|SPN 639 - сеть J1939 №1]], [[/kody/spn-627.html|SPN 627 - источник питания]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Лампа мигнула два раза, пауза, потом семь раз. Это SPN 2 или 7?", "Нет. Блинк-код - это группы вспышек, а не SPN. Его переводят по таблице Bendix в SPN и FMI. Число из вспышек не является SPN."),
                ("Лампа ABS горит, а тормоза работают. Это нормально?", "Тормоза остаются, но защиты от блокировки колёс нет. Ехать можно осторожно до сервиса, не откладывая разбор."),
                ("Код датчика колеса. Менять датчик?", "Сначала осмотрите зубчатое кольцо, зазор, разъём и провод. Загрязнение и окисленный контакт дают тот же код при исправном датчике."),
                ("Код пропал после выключения зажигания. Всё исправно?", "Не обязательно. Активные коды так стираются, а причина остаётся. Посмотрите неактивные коды и проверьте повтор в поездке."),
            ]),
        ],
    },
    "brand-en:bendix": {
        "head": [
            ("What this page covers", [
                "Bendix supplies brake electronics: ABS, ATC and ESP controllers for tractors, trucks and trailers. The page covers this electronics, not the engine and not the brake mechanisms themselves. The codes follow J1939: a component number (SPN) and a failure mode (FMI) come as a pair.",
                "Bendix has a second way to read them: blink codes. The ABS lamp in the cluster flashes a sequence, and each code has two groups (a first and a second digit). In Bendix tables each blink code is matched at once to a J1587 number (SID), an SPN and an FMI. It is one fault written three ways, not three different faults.",
            ]),
            ("How to read the codes on this page", [
                "The SPN names the component and the FMI names the failure type. For example, in the Bendix table the wheel speed sensors use SPN 789 to 794 (one per wheel) and the controller is recorded under SPN 629. The FMI list is the same for every make: 3 is voltage above normal, 4 is below normal, 2 is erratic data, 9 is an abnormal update rate.",
                "A blink code cannot be compared with an SPN directly: it is a number built from a count of flashes. A two-digit blink code is first translated through the Bendix table into SPN and FMI, and only then matched to the page. The reverse mistake also happens: a two-digit number taken for an SPN.",
                "The letters in Bendix descriptions mean position: SA, DA and AA are axles (steer, drive and additional), Left and Right are the side. This matters for wheel codes: the left and right sides of one axle have different numbers.",
            ]),
            ("How to get blink codes", [
                "According to the Bendix guide, the mode is entered with the diagnostic switch: one press for active codes, two for inactive (stored) codes, three to clear active codes. Other presses start a system configuration check, the dynamometer mode and ECU reconfiguration. Wait at least two seconds after ignition on before pressing.",
                "The controller does not enter blink code mode if the wheel speed sensors show the vehicle moving, and it leaves the mode when motion starts. Flashes last half a second, the pause between digits is 1.5 seconds, between messages 2.5 seconds, and the lamp stays on for 5 seconds at the end. This is from the Bendix summary for the EC-60 controller; other controllers may differ, so check the service data sheet for your model.",
            ]),
            ("What to check for these codes", [
                [
                    "Wheel speed sensors: the gap to the tone ring, dirt, a broken wire, a damaged connector. The Bendix table has separate entries for the gap and for low output at drive-off.",
                    "Pressure modulator valves: a short to ground, a short to voltage and an open circuit are logged as separate codes for each valve.",
                    "Power supply: a low battery voltage code is a separate entry. Check the terminals, ground and fuse before the sensors.",
                    "J1939 network: ESP has entries for invalid messages from other controllers. They point to the network or a neighbouring controller, not the brakes.",
                    "ESP sensors: steering angle, yaw rate, lateral acceleration. For the steering angle sensor the table has an entry for calibration in progress; it is cleared by calibration, not by replacement.",
                ],
                "A dirty tone ring or a corroded connector gives a wheel sensor code with a good sensor. Inspect and clean first, replace after.",
            ]),
            ("Order of checks", [
                "1. Write down every code in full, with SPN and FMI. If you read by flashes, write down the count in each group and translate it using the table for your controller model.",
                "2. Mark active and inactive codes separately. An inactive code is a fault that happened but is not present now.",
                "3. Check the controller power and ground, then the connectors and the harness at the axle.",
                "4. For a wheel sensor, inspect the ring and the gap against the manual for that axle. The guide gives no values.",
                "5. Clear the codes after the repair. According to the Bendix guide, active codes clear by cycling the ignition, and wheel speed sensor codes only once the controller again sees valid speed from all wheels.",
                "6. Check for a repeat on a normal trip. One start without a repeat proves nothing.",
            ]),
            ("For the driver on the road", [
                "A lit ABS lamp means anti-lock braking is not working, even if the brakes still stop the truck. Ordinary air braking remains, but there is no protection against wheel lock. On wet or slippery roads, increase your following distance and do not count on that protection.",
                "If the red brake lamp is lit with the ABS lamp, or air pressure is falling, stop in a safe place. A yellow ABS lamp alone usually lets you reach a workshop, but do not put off the check.",
            ]),
            ("For the technician", [
                "Blink codes replace a scan tool only when none is at hand. Read the full table, inactive codes and event history with a diagnostic tool. Do not translate a blink code through the table of another controller model: numbering depends on the series (EC-60, EC-80 and so on).",
                "Do not replace the controller for one code. Power, ground, connectors and harness first. After a sensor, controller or modulator is replaced, calibration or reconfiguration may be needed; the data sheet for the model says so.",
            ]),
            ("Related pages", [
                "[[/en/marki/wabco.html|WABCO - other brake electronics]], [[/en/problemy/gorit-lampa-abs.html|ABS lamp is on]]",
                "[[/en/kody/spn-629.html|SPN 629 - controller #1]], [[/en/kody/spn-639.html|SPN 639 - J1939 network #1]], [[/en/kody/spn-627.html|SPN 627 - power supply]]",
            ]),
        ],
        "tail": [
            ("Questions and answers", [
                ("The lamp flashed twice, paused, then flashed seven times. Is that SPN 2 or 7?", "No. A blink code is groups of flashes, not an SPN. It is translated through the Bendix table into an SPN and an FMI. A number of flashes is not an SPN."),
                ("The ABS lamp is on but the brakes work. Is that normal?", "The brakes remain, but there is no protection against wheel lock. You can drive carefully to a workshop, but do not put off the check."),
                ("A wheel sensor code. Replace the sensor?", "First inspect the tone ring, the gap, the connector and the wire. Dirt and a corroded contact give the same code with a good sensor."),
                ("The code went away after switching the ignition off. Is everything fine?", "Not necessarily. Active codes clear that way, but the cause remains. Look at the inactive codes and check for a repeat on a trip."),
            ]),
        ],
    },
    "brand:eberspacher": {
        "head": [
            ("Что это за страница", [
                "Eberspächer - производитель автономных отопителей кабины и двигателя. Эта страница про коды отопителя, а не двигателя, коробки или тормозов. Коды трёхзначные: 000, 011, 020 и так далее. Они относятся к блоку управления отопителя, и блок записывает их сам.",
                "Основная таблица на странице - Airtronic D2 и D4 (воздушные отопители); коды водяных отопителей Hydronic помечены. Это существенно: у Airtronic и Hydronic номера частично совпадают, а смысл у совпавших номеров бывает разный.",
            ]),
            ("Один номер, два отопителя", [
                "Самый частый источник ошибок - сравнение номеров разных линеек. По заводским руководствам, код 020 у Airtronic - обрыв цепи свечи накаливания, а у Hydronic 16-35 - обрыв цепи блока зажигания. Код 021 у Airtronic - короткое замыкание свечи накаливания, а у Hydronic 16-35 - замыкание на массу в цепи блока зажигания. Код 015 у Airtronic выводится, если после кода 017 (перегрев) отопитель включили снова, а у Hydronic 16-35 - после трёх подряд срабатываний кода 012.",
                "Поэтому первым делом определите модель отопителя по шильдику. Таблицу сопоставляйте именно с этой моделью. Если модель неизвестна, описание кода считайте подсказкой, а не диагнозом.",
            ]),
            ("Как получить код", [
                "Блок управления Airtronic хранит до пяти неисправностей. Прочитать их можно диагностическим прибором, прибором EDiTH, таймером или пультом (по руководству это модульный таймер, радиопульт TP5 и пульты EasyStart). Текущая неисправность выводится как AF и записывается в ячейку F1, предыдущие сдвигаются в F2 - F5. В примере руководства на дисплее показан код 64, а в таблице он записан как 064: ведущий ноль на дисплее может не показываться.",
                "Строка 000 в таблице означает «неисправностей нет». Это нормальное состояние, а не сбой.",
                "Порядок подключения прибора важен. Если нарушить последовательность действий, описанную в руководстве, отопитель запишет ошибку 062 (обрыв в цепи элемента управления) и перейдёт в аварийный режим. Такую запись поэтому нельзя считать причиной проблемы, если она появилась во время диагностики.",
            ]),
            ("Основные группы кодов Airtronic", [
                "Питание. 010 - перенапряжение, отключение; 011 - пониженное напряжение, отключение. При 011 и 099 руководство рекомендует проверить предохранители, питающие провода, минус и клемму плюса на аккумуляторе.",
                "Перегрев. 012 - перегрев на датчике перегрева, 013 - на датчике пламени, 014 - слишком большая разница температур между ними, 017 - перегрев. После 017 повторное включение даёт 015 (блокировка). Руководство советует проверить воздуховоды горячего воздуха на засор.",
                "Свеча накаливания. 018 - слишком малая энергия запуска, 019 - слишком малая энергия поджига, 020 - обрыв, 021 - короткое замыкание, перегрузка или замыкание на минус.",
                "Нагнетатель воздуха. 031 - обрыв, 032 и далее - короткие замыкания и остановка.",
                "Дозирующий насос. 047, 048, 049 - короткое замыкание, обрыв и выход на плюс.",
                "Запуск и пламя. 050 - слишком много неудачных запусков (блокировка), 051 - пламя при включении, 052 - превышено время безопасности, 053 - 057 - срыв пламени на разных ступенях мощности. При 052 - 057 руководство предлагает проверить выхлопную трубу и подачу воздуха и топлива.",
                "Датчики. 060 и 061 - наружный температурный датчик, 064 и 065 - датчик пламени, 071 и 072 - датчик перегрева.",
                "Блок управления. 090 - 099: внутренние неисправности, ошибки памяти, помехи по напряжению. При 091 руководство советует убрать помехи (слабый аккумулятор, зарядное устройство).",
                "Пометка со звёздочкой в заводской таблице означает, что код действует только для блока управления нового поколения.",
            ]),
            ("Порядок проверки", [
                "1. Определите модель отопителя и найдите таблицу под неё.",
                "2. Считайте память неисправностей целиком (до пяти записей) и определите, какая запись текущая.",
                "3. Проверьте питание: предохранители, провода, масса, клемма плюса, состояние аккумулятора.",
                "4. Для кодов перегрева проверьте воздуховоды и вентиляцию на засор, потом датчики.",
                "5. Для кодов пламени и запуска проверьте выхлоп, подачу воздуха и топлива, потом свечу и датчик пламени.",
                "6. Блок управления меняйте только после проверок и по таблице завода. Если код блокировки (015, 050), блокировка снимается стиранием памяти неисправностей, по руководству пультом, таймером или прибором.",
            ]),
            ("Водителю в рейсе", [
                "Неисправность отопителя не влияет на работу двигателя и тормозов машины. Если появился запах гари, выхлопа или топлива, выключите отопитель, проветрите кабину и не включайте его до проверки.",
                "Перегрев (012, 013, 014, 017) и блокировка (015, 050) - это защита, а не поломка кабины. Не пытайтесь «обмануть» блокировку повторными включениями: по руководству так и получается код 015.",
            ]),
            ("Мастеру в сервисе", [
                "Перед диагностикой убедитесь, что порядок подключения прибора соответствует руководству: нарушение порядка записывает 062. Ориентируйтесь на заводские страницы с пометкой «Remedial action» для своего номера.",
                "Не принимайте одинаковые номера у разных моделей за одну неисправность. Для Hydronic D4W SC и D5W S таблица ближе к Airtronic, но не идентична ей.",
            ]),
            ("Связанные страницы", [
                "[[/otopiteli/eberspacher-000.html|Eberspächer 000 - ошибок нет]], [[/otopiteli/eberspacher-011.html|011]], [[/otopiteli/eberspacher-012.html|012]], [[/otopiteli/eberspacher-020.html|020]], [[/otopiteli/eberspacher-021.html|021]]",
                "[[/marki/webasto.html|Webasto]], [[/marki/planar.html|Планар]], [[/problemy/propalo-pitanie.html|пропало питание]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Код 000 - это ошибка?", "Нет. В заводской таблице 000 означает «неисправностей нет»."),
                ("На дисплее 64, а в таблице 064. Это разные коды?", "Это один код. В примере руководства на дисплее показано 64, в таблице записано 064."),
                ("Код 020 есть у Airtronic и у Hydronic. Это одна неисправность?", "Нет. У Airtronic 020 - обрыв цепи свечи накаливания, у Hydronic 16-35 - обрыв цепи блока зажигания. Сверяйте с таблицей своей модели."),
                ("После диагностики отопитель показал 062. Он сломан?", "Не обязательно. По руководству 062 записывается, если нарушить порядок подключения диагностического прибора. Повторите диагностику строго по инструкции."),
            ]),
        ],
    },
    "brand-en:eberspacher": {
        "head": [
            ("What this page is", [
                "Eberspächer makes independent cab and engine heaters. This page is about heater codes, not engine, gearbox or brake codes. The codes have three digits: 000, 011, 020 and so on. They belong to the heater's control box, which records them itself.",
                "The main table on the page is Airtronic D2 and D4 (air heaters); codes for the Hydronic water heaters are marked. This matters: Airtronic and Hydronic numbers partly coincide, and the coinciding numbers can mean different things.",
            ]),
            ("One number, two heaters", [
                "The commonest source of mistakes is comparing numbers across heater lines. According to the factory manuals, code 020 on the Airtronic is an open glow plug circuit, while on the Hydronic 16-35 it is an open circuit of the ignition unit. Code 021 on the Airtronic is a short circuit of the glow plug, while on the Hydronic 16-35 it is an earth short in the ignition unit circuit. Code 015 on the Airtronic is shown if the heater was switched on again after code 017 (overheating), while on the Hydronic 16-35 it follows three consecutive occurrences of code 012.",
                "So first identify the heater model from its rating plate and match the table to that model. If the model is unknown, treat a code description as a hint, not a diagnosis.",
            ]),
            ("How to get the code", [
                "The Airtronic control box stores up to five faults. They can be read with a diagnostic unit, the EDiTH tool, a timer or a remote (in the manual these are the module timer, the TP5 radio remote and the EasyStart controls). The current fault is shown as AF and written to slot F1; earlier ones move to F2 to F5. In the manual's example the display shows code 64 while the table writes it as 064: a leading zero may not be displayed.",
                "Row 000 in the table means \"no faults\". It is a normal state, not a failure.",
                "The order of connecting the tool matters. If the sequence described in the manual is not followed, the heater records error 062 (control unit interruption) and goes into emergency operation. Such an entry should therefore not be taken as the cause of the problem if it appeared during diagnosis.",
            ]),
            ("Main groups of Airtronic codes", [
                "Power. 010 is overvoltage cut-off; 011 is undervoltage cut-off. For 011 and 099 the manual recommends checking the fuses, the supply wires, the ground and the positive terminal on the battery.",
                "Overheating. 012 is overheating at the overheating sensor, 013 at the flame sensor, 014 a too large temperature difference between them, 017 overheating. After 017 a restart gives 015 (lock-out). The manual advises checking the hot air ducts for blockage.",
                "Glow plug. 018 is too low starting energy, 019 too low ignition energy, 020 an open circuit, 021 a short circuit, overload or short to negative.",
                "Blower. 031 is an open circuit; 032 and onward are shorts and stalling.",
                "Metering pump. 047, 048, 049: short circuit, open circuit and short to positive.",
                "Start and flame. 050 is too many failed start attempts (lock-out), 051 flame detected on switch-on, 052 safety time exceeded, 053 to 057 flame cut-out at different power stages. For 052 to 057 the manual suggests checking the exhaust pipe and the air and fuel supply.",
                "Sensors. 060 and 061: the external temperature sensor; 064 and 065: the flame sensor; 071 and 072: the overheating sensor.",
                "Control box. 090 to 099: internal faults, memory errors, voltage interference. For 091 the manual advises removing the interference (a weak battery, a charger).",
                "An asterisk in the factory table means the code applies only to the new-generation control box.",
            ]),
            ("Order of checks", [
                "1. Identify the heater model and find the table for it.",
                "2. Read the whole fault memory (up to five entries) and determine which entry is current.",
                "3. Check power: fuses, wires, ground, positive terminal, battery condition.",
                "4. For overheating codes, check the air ducts and ventilation for blockage, then the sensors.",
                "5. For flame and start codes, check the exhaust and the air and fuel supply, then the plug and the flame sensor.",
                "6. Replace the control box only after these checks and according to the factory table. A lock-out code (015, 050) is cleared by erasing the fault memory, per the manual with a remote, timer or tool.",
            ]),
            ("For the driver on the road", [
                "A heater fault does not affect the work of the engine or the brakes of the vehicle. If you smell burning, exhaust or fuel, switch the heater off, ventilate the cab and do not switch it on until it is checked.",
                "Overheating (012, 013, 014, 017) and lock-out (015, 050) are protection, not a cab fault. Do not try to \"trick\" the lock-out with repeated restarts: that is exactly how code 015 arises according to the manual.",
            ]),
            ("For the technician", [
                "Before diagnosis make sure the order of connecting the tool matches the manual: breaking the order records 062. Use the factory pages with \"Remedial action\" for your number.",
                "Do not take equal numbers on different models for one fault. For the Hydronic D4W SC and D5W S the table is closer to the Airtronic but not identical.",
            ]),
            ("Related pages", [
                "[[/en/otopiteli/eberspacher-000.html|Eberspächer 000 - no faults]], [[/en/otopiteli/eberspacher-011.html|011]], [[/en/otopiteli/eberspacher-012.html|012]], [[/en/otopiteli/eberspacher-020.html|020]], [[/en/otopiteli/eberspacher-021.html|021]]",
                "[[/en/marki/webasto.html|Webasto]], [[/en/marki/planar.html|Planar]], [[/en/problemy/propalo-pitanie.html|power lost]]",
            ]),
        ],
        "tail": [
            ("Questions and answers", [
                ("Is code 000 an error?", "No. In the factory table 000 means \"no faults\"."),
                ("The display shows 64 and the table says 064. Are these different codes?", "It is one code. The manual's example shows 64 on the display and writes 064 in the table."),
                ("Code 020 exists on the Airtronic and on the Hydronic. Is it the same fault?", "No. On the Airtronic 020 is an open glow plug circuit; on the Hydronic 16-35 it is an open ignition unit circuit. Match it to the table of your model."),
                ("After diagnosis the heater shows 062. Is it broken?", "Not necessarily. According to the manual, 062 is recorded if the order of connecting the diagnostic tool is not followed. Repeat the diagnosis strictly following the instructions."),
            ]),
        ],
    },
    "brand:tata": {
        "head": [
            ("Что разобрано на этой странице", [
                "Tata Motors записывает коды двигателя в формате OBD-II: буква P, четыре символа и через дефис ещё два, например P0192-00. На сайте тот же код может быть записан слитно, без дефиса (P019200). Всё вместе - один код: первые пять символов называют неисправность, последние два уточняют её вид.",
                "Подтверждено официальным руководством Tata Motors по диагностике двигателя 3.3L NGE BS-VI с блоком управления MD1CS018 (версия 1.0 от 15.08.2019, 545 страниц): в нём каждая запись оформлена именно так, с описанием, возможными причинами и последствием для машины. Для других двигателей Tata подтверждения формата мы не нашли, поэтому не переносите описания без проверки.",
            ]),
            ("Как читать коды этой страницы", [
                "Основа P0192 и суффикс -00 вместе - один код. Одна и та же основа с разными суффиксами - разные неисправности. В руководстве Tata, например, у датчика температуры топлива есть четыре записи: P0180-11 (короткое замыкание сигнала на массу), P0180-12 (короткое замыкание на плюс или обрыв), P0180-1C (сигнал с недопустимым градиентом, то есть скачет) и P0180-1F (сигнал недостоверен).",
                "Суффиксы повторяются от узла к узлу: -11 стоит у записей о замыкании на массу, -12 - о замыкании на плюс, -13 - об обрыве цепи (например, P0627-11, P0627-12 и P0627-13 для реле топливного насоса). Это закономерность по руководству, а не таблица стандарта, поэтому смысл каждого суффикса сверяйте с записью, а не с памятью.",
                "Код -00 у большинства записей. Нулевой суффикс означает, что тип не уточняется: смысл записан только в описании.",
                "Коды на букву U относятся к связи между блоками. В руководстве Tata U0102-00 назван общим отключением от шины CAN (Overall disconnection to CAN bus), а причиной указан внутренний отказ электроники блока управления. По общему стандарту SAE тот же номер U0102 означает потерю связи с блоком раздаточной коробки, поэтому читайте описание из руководства, а не по памяти.",
            ]),
            ("Основные системы и типовые причины", [
                "Рампа и подача топлива. Датчик давления в рампе: P0192-00 - замыкание на массу, P0193-00 - замыкание на плюс или обрыв. При P0192-00 в руководстве указано снижение крутящего момента, лампа MIL включена. Отдельные записи есть для отклонений давления в рампе (P0087-00, P0088-00).",
                "Воздух и наддув. Датчик массового расхода воздуха, датчик давления во впускном коллекторе, датчик температуры воздуха, привод наддува. Здесь много записей по разным контурам одного узла, и важно отличать цепь питания от сигнальной цепи.",
                "Впрыск. Отдельные записи для обрыва цепи форсунки по цилиндрам (P0201-00 - первый цилиндр, дальше по порядку) и для короткого замыкания верхнего и нижнего плеча каждой форсунки (серия P1201-00 и далее). Номер цилиндра входит в код.",
                "Рециркуляция выхлопа (EGR) и очистка выхлопа. Клапан EGR, его датчик положения, охлаждение, температуры до и после катализатора и сажевого фильтра.",
                "Датчики вала. P0335-00 - обрыв датчика коленчатого вала, P0340-00 - нет сигнала датчика распределительного вала.",
            ]),
            ("Порядок проверки", [
                "1. Запишите код целиком, с суффиксом. Без суффикса запись неполная.",
                "2. Сверьте с описанием в руководстве: узел, цепь (питание, сигнал, масса) и вид отказа.",
                "3. Начните с напряжения аккумулятора, потом разъёма и штырей датчика с обеих сторон. В руководстве Tata типовая последовательность такая: напряжение питания, соединитель, штыри, затем непрерывность сигнальных проводов.",
                "4. Для коротких замыканий на массу и на плюс проверьте жгут на трение и влагу, затем датчик.",
                "5. Заменяйте датчик, когда цепь исправна. Заменённый датчик без устранения причины в жгуте даёт тот же код.",
                "6. Стирайте коды после ремонта и проверяйте повтор в поездке.",
            ]),
            ("Водителю в рейсе", [
                "В руководстве Tata последствие для машины записано отдельной строкой. У части кодов это снижение крутящего момента (P0192-00), у P0001-00 указан аварийный режим limp-home, у кодов сети (U0102-00) - ступенчатое ограничение: на низком уровне снижение момента, на жёстком режим ползучей скорости. У ряда датчиков температуры последствие не указано (NA), горит только лампа MIL. Если мощность упала или лампа MIL горит вместе с другими лампами, остановитесь и обратитесь в сервис.",
                "Коды рампы, форсунок и датчиков вала не оставляйте без внимания: езда с ними может вести к потере мощности и остановке двигателя.",
            ]),
            ("Мастеру в сервисе", [
                "Работайте по руководству на свой двигатель и версию блока. Основа кода одна, а проверки у разных двигателей Tata различаются. Не подставляйте описание из таблицы другого двигателя.",
                "Записывайте вместе с кодом кадр стоп-данных и число повторов.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/gorit-check-engine.html|горит Check Engine]], [[/problemy/upala-moshchnost.html|упала мощность]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]]",
                "[[/problemy/oshibka-adblue.html|ошибка AdBlue]], [[/problemy/datchik-nox.html|датчик NOx]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("P0192-00 и P0192 - это одно и то же?", "Первые пять символов называют неисправность, суффикс уточняет вид. В руководстве Tata кодом считается запись целиком, например P0192-00."),
                ("P0180-11 и P0180-12 - один и тот же датчик?", "Да, датчик температуры топлива, но неисправности разные: замыкание на массу и замыкание на плюс или обрыв."),
                ("Что означает U0102-00 в руководстве Tata?", "В руководстве Tata он назван общим отключением от шины CAN, причина - внутренний отказ электроники блока управления. Руководство советует осмотреть блок на повреждения; при устойчивой ошибке блок меняют, затем стирают код и проверяют заново."),
            ]),
        ],
    },
    "brand-en:tata": {
        "head": [
            ("What this page covers", [
                "Tata Motors records engine codes in an OBD-II style format: the letter P, four characters and, after a hyphen, two more, for example P0192-00. On the site the same code may be written without the hyphen (P019200). Together they are one code: the first five characters name the fault and the last two refine its type.",
                "This is confirmed by Tata Motors' official diagnostic manual for the 3.3L NGE BS-VI engine with the MD1CS018 control unit (version 1.0 of 15 Aug 2019, 545 pages), in which every entry is laid out this way, with a description, probable causes and the effect on the vehicle. We found no confirmation of the format for other Tata engines, so do not carry descriptions across without checking.",
            ]),
            ("How to read the codes on this page", [
                "The base P0192 and the suffix -00 together are one code. The same base with different suffixes is a different fault. In the Tata manual, for example, the fuel temperature sensor has four entries: P0180-11 (signal shorted to ground), P0180-12 (shorted to battery or open), P0180-1C (signal with an implausible gradient, that is, jumping) and P0180-1F (implausible signal).",
                "The suffixes repeat from component to component: -11 appears in entries for a short to ground, -12 for a short to battery, -13 for an open circuit (for example, P0627-11, P0627-12 and P0627-13 for the fuel pump relay). This is a pattern in the manual, not a table from a standard, so check the meaning of each suffix against the entry and not from memory.",
                "Most entries end in -00. A zero suffix means the type is not specified: the meaning is only in the description.",
                "Codes beginning with the letter U concern the link between controllers. In the Tata manual U0102-00 is named an overall disconnection from the CAN bus (Overall disconnection to CAN bus), and the cause given is an internal failure of the control unit electronics. In the general SAE standard the same number U0102 means lost communication with the transfer case control module, so read the description from the manual, not from memory.",
            ]),
            ("Main systems and typical causes", [
                "Rail and fuel supply. Rail pressure sensor: P0192-00 is a short to ground, P0193-00 is a short to battery or an open circuit. For P0192-00 the manual lists a torque reduction and the MIL on. There are separate entries for rail pressure deviations (P0087-00, P0088-00).",
                "Air and boost. Mass air flow sensor, manifold pressure sensor, air temperature sensor, boost actuator. There are many entries for different circuits of one component, and it matters to tell the supply circuit from the signal circuit.",
                "Injection. Separate entries for an open injector circuit by cylinder (P0201-00 is cylinder 1, then in order) and for a short on the high and low side of each injector (the P1201-00 series onward). The cylinder number is part of the code.",
                "Exhaust gas recirculation (EGR) and exhaust aftertreatment. The EGR valve, its position sensor, cooling, and the temperatures before and after the catalyst and the particulate filter.",
                "Shaft sensors. P0335-00 is an open crankshaft sensor, P0340-00 is no camshaft signal.",
            ]),
            ("Order of checks", [
                "1. Write the code down in full, with the suffix. Without the suffix the entry is incomplete.",
                "2. Match it with the description in the manual: the component, the circuit (supply, signal, ground) and the failure type.",
                "3. Start with the battery voltage, then the sensor connector and pins on both sides. In the Tata manual the typical sequence is: supply voltage, connector, pins, then continuity of the signal wires.",
                "4. For shorts to ground and to battery, inspect the harness for chafing and moisture, then the sensor.",
                "5. Replace a sensor when the circuit is good. A new sensor without fixing the harness gives the same code.",
                "6. Clear the codes after the repair and check for a repeat on a trip.",
            ]),
            ("For the driver on the road", [
                "In the Tata manual the effect on the vehicle is a separate line. For some codes it is a torque reduction (P0192-00), P0001-00 lists limp-home mode, and network codes (U0102-00) have a staged restriction: torque reduction at the low level and creep mode at the severe level. For a number of temperature sensors no effect is given (NA) and only the MIL is lit. If power has dropped or the MIL is lit together with other lamps, stop and contact a workshop.",
                "Do not ignore rail, injector and shaft sensor codes: driving with them can lead to loss of power and engine stall.",
            ]),
            ("For the technician", [
                "Work from the manual for your engine and module version. The base of the code is the same, but the checks differ between Tata engines. Do not use a description from another engine's table.",
                "Record the freeze-frame and the occurrence count with the code.",
            ]),
            ("Related pages", [
                "[[/en/problemy/gorit-check-engine.html|Check Engine is on]], [[/en/problemy/upala-moshchnost.html|loss of power]], [[/en/problemy/problemy-s-toplivom.html|fuel problems]]",
                "[[/en/problemy/oshibka-adblue.html|AdBlue fault]], [[/en/problemy/datchik-nox.html|NOx sensor]]",
            ]),
        ],
        "tail": [
            ("Questions and answers", [
                ("Are P0192-00 and P0192 the same thing?", "The first five characters name the fault and the suffix refines the type. In the Tata manual the code is the whole entry, for example P0192-00."),
                ("Are P0180-11 and P0180-12 the same sensor?", "Yes, the fuel temperature sensor, but the faults differ: a short to ground and a short to battery or open circuit."),
                ("What does U0102-00 mean in the Tata manual?", "The Tata manual names it an overall disconnection from the CAN bus, with an internal failure of the control unit electronics as the cause. It advises inspecting the unit for damage; if the error persists, the unit is replaced, then the code is cleared and checked again."),
            ]),
        ],
    },
    "brand:cumminsisf": {
        "head": [
            ("Что разобрано на этой странице", [
                "Cummins ISF - это дизели ISF 2.8 и ISF 3.8 для лёгких грузовиков и фургонов. Их серийно выпускает совместное предприятие Cummins и Foton, поэтому двигатель встречается на машинах разных марок. Страница относится к двигателю, а не к кузовным системам машины.",
                "Коды на странице записаны собственной нумерацией Cummins: короткие номера вроде 111. Это не SPN. Рядом с таким номером в таблицах Cummins всегда стоит пара J1939 (SPN и FMI) и цвет лампы.",
            ]),
            ("Как читать коды этой страницы", [
                "В таблице Cummins у каждой неисправности три значения: собственный номер, SPN и FMI. Они стоят в разных столбцах, и перепутать их легко. Неисправность 111 - это критический внутренний отказ блока управления (SPN 629, FMI 12, красная лампа). А SPN 111 в стандарте - это датчик уровня охлаждающей жидкости.",
                "Поэтому не вводите номер 111 в поиск по SPN: вы получите совсем другой узел. Вводите его там, где ищут коды ISF, или переводите в SPN по таблице Cummins.",
                "Цвет лампы входит в запись. По руководству Cummins жёлтая лампа (Check Engine) требует сервиса при первой возможности, красная лампа Stop Engine - остановки, как только это безопасно.",
            ]),
            ("Что есть и чего нет в руководстве по ремонту", [
                "Руководство по ремонту двигателя ISF3.8 CM2220 (бюллетень 4021704) прямо сообщает, что оно не содержит электронной диагностики топливной системы, и предлагает пользоваться деревьями поиска неисправностей, только когда электронных кодов нет. Для кодов нужен отдельный документ Cummins по неисправностям той же версии блока управления.",
                "Практический вывод: код ISF нельзя «расшифровать» по общему справочнику ремонта. Нужен номер Cummins, SPN, FMI и версия блока (для 3.8 это CM2220). Две версии блока одного двигателя могут иметь разные пороги и перечень кодов.",
            ]),
            ("Порядок проверки", [
                "1. Запишите номер Cummins, SPN, FMI и цвет лампы. Отметьте, активен код или записан в прошлом.",
                "2. Если рядом в записи стоит слово ECM или «внутренний отказ», код сообщает о блоке управления, а не о датчике. Сначала питание, масса, предохранитель и разъёмы блока.",
                "3. Для кодов питания (например, потеря питания при включённом зажигании) осмотрите клеммы аккумулятора, массу двигателя и реле главного питания. Просевшее питание приводит к нескольким кодам подряд.",
                "4. Для кодов с электрическим FMI (3, 4, 5) начинайте с разъёма и жгута датчика.",
                "5. Стирайте коды после ремонта и проверяйте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "Красная лампа Stop Engine - остановка, как только это безопасно, без попыток доехать. Жёлтая лампа - обращение в сервис при первой возможности. Лампа MIL (контроль выбросов) вместе с красной лампой тоже означает остановку.",
                "Не сбрасывайте коды отключением аккумулятора перед сервисом: стёртая история лишает мастера подсказки, в каких условиях код появился.",
            ]),
            ("Мастеру в сервисе", [
                "Сверяйте версию блока управления. Для ISF 3.8 это CM2220 по руководству Cummins. Номера неисправностей одного семейства Cummins в целом совпадают у разных двигателей, но не каждый номер есть у каждого двигателя.",
                "Не меняйте блок ради одного кода внутреннего отказа без проверки питания и массы блока: после замены такая запись часто возвращается.",
            ]),
            ("Связанные страницы", [
                "[[/marki/cumminsisb.html|Cummins ISB]], [[/marki/cumminsism.html|Cummins ISM]], [[/marki/cumminsisx.html|Cummins ISX]]",
                "[[/kody/spn-629.html|SPN 629 - контроллер №1]], [[/kody/spn-111.html|SPN 111 - уровень охлаждающей жидкости]], [[/kody/spn-627.html|SPN 627 - источник питания]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Код 111 на ISF - это SPN 111?", "Нет. Неисправность Cummins 111 - внутренний отказ блока управления (SPN 629, FMI 12). SPN 111 в стандарте - датчик уровня охлаждающей жидкости."),
                ("Горит красная лампа. Можно ли доехать?", "Красная лампа означает остановку, как только это безопасно. Доезжать до сервиса на своём ходу не следует."),
            ]),
        ],
    },
    "brand-en:cumminsisf": {
        "head": [
            ("What this page covers", [
                "Cummins ISF means the ISF 2.8 and ISF 3.8 diesels for light trucks and vans. They are built in series by the Cummins and Foton joint venture, so the engine appears on vehicles of different makes. The page covers the engine, not the body systems of the vehicle.",
                "The codes on the page use Cummins' own numbering: short numbers such as 111. These are not SPNs. Next to such a number, Cummins tables always give a J1939 pair (SPN and FMI) and a lamp colour.",
            ]),
            ("How to read the codes on this page", [
                "In a Cummins table every fault has three values: its own number, an SPN and an FMI. They sit in separate columns and are easy to mix up. Fault 111 is a critical internal failure of the control module (SPN 629, FMI 12, red lamp). And SPN 111 in the standard is the coolant level sensor.",
                "So do not type 111 into an SPN search: you will get a completely different component. Enter it where ISF codes are searched, or translate it to an SPN with the Cummins table.",
                "The lamp colour is part of the entry. According to Cummins, the amber lamp (Check Engine) calls for service at the first opportunity, and the red Stop Engine lamp calls for a stop as soon as it is safe.",
            ]),
            ("What the repair manual does and does not contain", [
                "The ISF3.8 CM2220 service manual (bulletin 4021704) states that it does not contain electronic troubleshooting of the fuel system, and tells the reader to use its troubleshooting trees only when there are no electronic codes. For codes you need a separate Cummins fault code document for the same control module version.",
                "In practice, an ISF code cannot be decoded from a general repair guide. You need the Cummins number, the SPN, the FMI and the module version (for the 3.8 it is CM2220). Two module versions of the same engine can have different thresholds and different lists of codes.",
            ]),
            ("Order of checks", [
                "1. Write down the Cummins number, SPN, FMI and lamp colour. Note whether the code is active or stored.",
                "2. If the entry mentions the ECM or an internal failure, the code reports on the control module, not on a sensor. Power, ground, fuse and the module connectors first.",
                "3. For power codes (for example, power lost with the ignition on), inspect the battery terminals, the engine ground and the main power relay. Sagging power produces several codes in a row.",
                "4. For codes with an electrical FMI (3, 4, 5), start with the sensor connector and harness.",
                "5. Clear the codes after the repair and check for a repeat on the road.",
            ]),
            ("For the driver on the road", [
                "The red Stop Engine lamp means stop as soon as it is safe, with no attempt to reach the destination. The amber lamp means a workshop visit at the first opportunity. The MIL (emissions) lamp together with the red lamp also means stop.",
                "Do not clear codes by disconnecting the battery before the workshop: erased history takes away the technician's clue as to the conditions in which the code appeared.",
            ]),
            ("For the technician", [
                "Check the control module version. For the ISF 3.8 it is CM2220 according to Cummins. Fault numbers within one Cummins family generally match across engines, but not every number exists on every engine.",
                "Do not replace the module for a single internal-failure code without checking its power and ground: after replacement such an entry often returns.",
            ]),
            ("Related pages", [
                "[[/en/marki/cumminsisb.html|Cummins ISB]], [[/en/marki/cumminsism.html|Cummins ISM]], [[/en/marki/cumminsisx.html|Cummins ISX]]",
                "[[/en/kody/spn-629.html|SPN 629 - controller #1]], [[/en/kody/spn-111.html|SPN 111 - coolant level]], [[/en/kody/spn-627.html|SPN 627 - power supply]]",
            ]),
        ],
        "tail": [
            ("Questions and answers", [
                ("Is code 111 on an ISF the same as SPN 111?", "No. Cummins fault 111 is an internal failure of the control module (SPN 629, FMI 12). SPN 111 in the standard is the coolant level sensor."),
                ("The red lamp is on. Can I make it to the workshop?", "The red lamp means stop as soon as it is safe. Do not continue under your own power to the workshop."),
            ]),
        ],
    },
    "brand:cumminsisb": {
        "head": [
            ("Что разобрано на этой странице", [
                "Это раздел двигателя Cummins ISB. Он выделен отдельным блоком, потому что у Cummins своя система записи: рядом с парой J1939 (SPN и FMI) стоит собственный номер неисправности и цвет лампы. На странице КамАЗ этот двигатель тоже упомянут отдельно: его коды разнесены по своему блоку, а не смешаны с кодами самой машины.",
                "Код двигателя и код машины могут прийти из разных блоков. Если сканер показывает источник кода, запишите его: один и тот же номер в другом блоке может означать другое.",
            ]),
            ("Номер Cummins и SPN - два разных номера", [
                "В таблице Cummins каждая строка содержит собственный номер неисправности, SPN, FMI, цвет лампы и описание. Примеры: неисправность 111 - критический внутренний отказ блока управления, она записана под SPN 629 и FMI 12 с красной лампой; неисправность 343 - внутренний отказ блока управления, предупреждающего уровня, тоже под SPN 629 и FMI 12. Один SPN может скрывать несколько разных номеров Cummins, поэтому по SPN и FMI вы можете выйти не на ту строку.",
                "И наоборот, одинаковые цифры не говорят об одной неисправности. Номер Cummins 111 и SPN 111 (уровень охлаждающей жидкости) никак не связаны.",
            ]),
            ("Общие номера у разных двигателей Cummins", [
                "Номера неисправностей у Cummins общие для нескольких семейств двигателей: в сводной таблице Cummins по промышленным двигателям серии Q для строки 111 отмечены сразу все двигатели таблицы (QSB 6.7, QSL 9, QSX 15, QSB 4.5, QSF 3.8, QSG12). Это показывает принцип; для дорожного ISB нужна таблица именно вашего двигателя. Но у других строк отметки стоят только у части двигателей. Поэтому код, найденный для ISB, не обязан существовать у соседнего двигателя, и наоборот.",
                "Практический вывод: ищите код именно по своему двигателю и версии блока. Таблица соседнего двигателя годится как подсказка, но не как подтверждение.",
            ]),
            ("Порядок проверки", [
                "1. Запишите номер Cummins, SPN, FMI, цвет лампы и состояние кода (активен или записан).",
                "2. Электрические FMI (3, 4, 5): разъём, жгут, масса у датчика. Только после этого датчик.",
                "3. Данные недостоверны (FMI 2) или частота обновления аномальна (FMI 9): подозревайте сеть J1939 и питание, а не датчик.",
                "4. Внутренний отказ блока управления: питание, масса, предохранитель, разъёмы блока. Замена блока без этого часто возвращает запись.",
                "5. Стирайте коды после ремонта и проверяйте повтор на ходу.",
            ]),
            ("Водителю в рейсе", [
                "По руководству Cummins, жёлтая лампа означает обслуживание при первой возможности, красная лампа Stop Engine - остановку, как только это безопасно. Лампа MIL вместе с красной лампой Stop Engine тоже означает остановку и обращение к специалистам.",
                "Если лампа красная, не пытайтесь дотянуть до сервиса: продолжение движения может усугубить поломку.",
            ]),
            ("Мастеру в сервисе", [
                "Сверяйте номер Cummins со SPN в одной строке одной таблицы. Не переносите описание из таблицы другого двигателя без проверки отметки двигателя.",
                "Записывайте вместе с кодом кадр стоп-данных и число повторов. Повторяющийся код при тех же условиях указывает на причину, а единичный - на случайный сбой.",
            ]),
            ("Связанные страницы", [
                "[[/marki/kamaz.html|КамАЗ]], [[/marki/cumminsisf.html|Cummins ISF]], [[/marki/cumminsisx.html|Cummins ISX]]",
                "[[/kody/spn-629.html|SPN 629 - контроллер №1]], [[/kody/spn-639.html|SPN 639 - сеть J1939 №1]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Номер Cummins и SPN - это одно и то же?", "Нет. Номер Cummins собственный, SPN из J1939. В таблице Cummins они стоят в разных столбцах рядом с FMI и цветом лампы."),
                ("Один SPN, а номеров Cummins несколько. Как выбрать?", "Смотрите FMI и описание в строке. Например, SPN 629 с FMI 12 встречается у разных неисправностей блока управления, и различает их именно номер Cummins."),
                ("Код нашёл в таблице другого двигателя Cummins. Можно доверять?", "Как подсказке - да. Как подтверждению - нет: у части строк отметки есть не у всех двигателей."),
            ]),
        ],
    },
    "brand-en:cumminsisb": {
        "head": [
            ("What this page covers", [
                "This section covers the Cummins ISB engine. It is a separate block because Cummins has its own recording system: next to the J1939 pair (SPN and FMI) there is its own fault number and a lamp colour. On the KAMAZ page this engine is also mentioned separately: its codes are kept in their own block rather than mixed with the codes of the truck itself.",
                "An engine code and a truck code can come from different controllers. If the scan tool shows the source of the code, write it down: the same number in another block can mean something else.",
            ]),
            ("The Cummins number and the SPN are two different numbers", [
                "In a Cummins table each row holds its own fault number, an SPN, an FMI, a lamp colour and a description. Examples: fault 111 is a critical internal failure of the control module, recorded under SPN 629 and FMI 12 with a red lamp; fault 343 is a warning-level internal failure of the control module, also under SPN 629 and FMI 12. One SPN can hide several Cummins numbers, so going by SPN and FMI alone may land you on the wrong row.",
                "And the other way round: equal digits do not mean the same fault. Cummins number 111 and SPN 111 (coolant level) are unrelated.",
            ]),
            ("Shared numbers across Cummins engines", [
                "Cummins fault numbers are shared by several engine families: in the Cummins summary table for industrial Q-series engines, row 111 is marked for every engine in the table (QSB 6.7, QSL 9, QSX 15, QSB 4.5, QSF 3.8, QSG12). This shows the principle; for a road ISB you need the table for your own engine. Other rows, however, are marked for only some of the engines. So a code found for the ISB does not have to exist on a neighbouring engine, and the reverse.",
                "In practice: look the code up for your own engine and module version. A neighbouring engine's table works as a hint, not as confirmation.",
            ]),
            ("Order of checks", [
                "1. Write down the Cummins number, SPN, FMI, lamp colour and code state (active or stored).",
                "2. Electrical FMI (3, 4, 5): connector, harness, ground at the sensor. The sensor only after that.",
                "3. Data erratic (FMI 2) or an abnormal update rate (FMI 9): suspect the J1939 network and the power supply, not the sensor.",
                "4. Internal failure of the control module: power, ground, fuse, module connectors. Replacing the module without this often brings the entry back.",
                "5. Clear the codes after the repair and check for a repeat on the road.",
            ]),
            ("For the driver on the road", [
                "According to Cummins, the amber lamp means service at the first opportunity and the red Stop Engine lamp means stop as soon as it is safe. The MIL lamp together with the red Stop Engine lamp also means stop and contact specialists.",
                "If the lamp is red, do not try to limp to the workshop: continuing to drive can make the damage worse.",
            ]),
            ("For the technician", [
                "Match the Cummins number with the SPN in one row of one table. Do not carry a description over from another engine's table without checking the engine mark.",
                "Record the freeze-frame and the occurrence count with the code. A code that repeats under the same conditions points to a cause; a one-off points to a random glitch.",
            ]),
            ("Related pages", [
                "[[/en/marki/kamaz.html|KAMAZ]], [[/en/marki/cumminsisf.html|Cummins ISF]], [[/en/marki/cumminsisx.html|Cummins ISX]]",
                "[[/en/kody/spn-629.html|SPN 629 - controller #1]], [[/en/kody/spn-639.html|SPN 639 - J1939 network #1]]",
            ]),
        ],
        "tail": [
            ("Questions and answers", [
                ("Are the Cummins number and the SPN the same thing?", "No. The Cummins number is its own; the SPN is from J1939. In a Cummins table they sit in separate columns next to the FMI and the lamp colour."),
                ("One SPN but several Cummins numbers. How do I choose?", "Look at the FMI and the description in the row. For example, SPN 629 with FMI 12 occurs for different control module faults, and it is the Cummins number that tells them apart."),
                ("I found the code in another Cummins engine's table. Can I trust it?", "As a hint, yes. As confirmation, no: some rows are marked for only some engines."),
            ]),
        ],
    },
    "brand:weichai": {
        "head": [
            ("Что разобрано на этой странице", [
                "Weichai - производитель дизелей, которые ставят на китайские тяжёлые грузовики. Страница относится к двигателям WP10 и WP12. Для WP10 нам удалось найти руководство производителя (серия Landking, Евро-3): двигатель с электронно управляемой топливной системой Common Rail фирмы Bosch. Что формат записи кодов у WP12 и более поздних версий совпадает, мы не подтвердили, поэтому проверяйте его по своей машине.",
                "По этому руководству коды двигателя Weichai бывают трёхзначными: например, 114 (сигнал датчика коленчатого вала ненормален), 134 (открыт клапан ограничения давления в рампе), 242 (слишком высокая температура охлаждающей жидкости). Это не SPN: номер из трёх цифр записан по собственной системе двигателя.",
            ]),
            ("Как читать коды этой страницы", [
                "Трёхзначный код читается миганием лампы диагностики. Лампа даёт серию вспышек каждый раз, когда выключатель диагностики посылает импульс, и между цифрами кода проходит секунда. В руководстве трёхзначный код показан на примере 321; как именно считать вспышки, берите из руководства. Блок хранит в памяти до десяти ошибок.",
                "Тот же код можно прочитать диагностическим оборудованием. Руководство называет два способа: диагностический прибор или лампа с кодом вспышек.",
                "Для сброса вручную в руководстве указано удержание выключателя диагностики при включённом зажигании в течение 4-8 секунд. Те коды, которые остались после сброса, - текущие неисправности. Аппаратные неисправности нужно устранять до очистки памяти блока.",
                "Не путайте число из трёх цифр с SPN: SPN называет узел по стандарту J1939 и идёт в паре с FMI. Если на странице встретилась пара SPN и FMI, это другой способ записи, и сверять номер из трёх цифр с ним напрямую нельзя.",
            ]),
            ("Примеры из руководства", [
                [
                    "114 - сигнал датчика вращения коленчатого вала ненормален; 112 - то же из-за ослабленного разъёма датчика (случай из практики в руководстве).",
                    "134 - открыт клапан ограничения давления в рампе. Руководство разбирает случаи, когда причина оказывалась не в самом клапане.",
                    "143 - обрыв цепи форсунки третьего цилиндра. Номер цилиндра входит в код.",
                    "221 - ненормальный сигнал педали акселератора.",
                    "242 - слишком высокая температура охлаждающей жидкости; 324 - неисправность сигнала частоты вращения.",
                ],
                "Примеры иллюстрируют формат. Полный перечень с причинами и действиями смотрите в руководстве на свой двигатель.",
            ]),
            ("Порядок проверки", [
                "1. Считайте все коды, запишите их по порядку появления и отметьте, какие остались после сброса.",
                "2. Начните с питания и разъёмов: в разобранных случаях руководства причиной не раз оказывались неплотный разъём или жгут.",
                "3. Для кодов датчика коленчатого вала и частоты вращения проверьте разъём, зазор и состояние зубчатого венца по руководству.",
                "4. Для кодов давления в рампе не меняйте клапан сразу: проверьте топливо, фильтр и подачу, потом клапан.",
                "5. После ремонта сбросьте память и проверьте повтор.",
            ]),
            ("Водителю в рейсе", [
                "Записи о температуре охлаждающей жидкости и давлении топлива не откладывайте. Если двигатель теряет мощность, глохнет или перегревается, остановитесь. Одну только запись из таблицы с неясным описанием за повод ехать дальше не считайте.",
            ]),
            ("Связанные страницы", [
                "[[/problemy/peregrev-dvigatelya.html|перегрев двигателя]], [[/problemy/problemy-s-toplivom.html|проблемы с топливом]], [[/problemy/glohnet-na-hodu.html|глохнет на ходу]]",
            ]),
        ],
        "tail": [
            ("Вопросы и ответы", [
                ("Код 114 - это SPN 114?", "Нет. Это трёхзначный код двигателя Weichai. SPN идёт в паре с FMI в формате J1939."),
                ("Как прочитать код без сканера?", "По руководству WP10 - миганием лампы диагностики: три цифры, между ними секунда. Подробности процедуры берите из руководства на свою машину."),
                ("Очистил память, код вернулся. Что это значит?", "Неисправность осталась. Руководство советует устранить аппаратную причину до очистки памяти."),
            ]),
        ],
    },
    "brand-en:weichai": {
        "head": [
            ("What this page covers", [
                "Weichai makes diesels fitted to Chinese heavy trucks. The page covers the WP10 and WP12 engines. For the WP10 we found the manufacturer's manual (Landking series, Euro III): an engine with an electronically controlled Bosch common rail fuel system. We did not confirm that the code format of the WP12 and later versions is the same, so check it on your own truck.",
                "According to this manual, Weichai engine codes can be three digits: for example, 114 (crankshaft sensor signal abnormal), 134 (rail pressure limiting valve open), 242 (coolant temperature too high). These are not SPNs: the three-digit number follows the engine's own system.",
            ]),
            ("How to read the codes on this page", [
                "A three-digit code is read from the diagnostic lamp flashes. The lamp gives a sequence of flashes each time the diagnostic switch sends a pulse, and there is a one-second pause between the digits of a code. The manual shows a three-digit code with the example 321; take the way to count the flashes from the manual. The controller keeps up to ten errors in memory.",
                "The same code can be read with diagnostic equipment. The manual names two ways: a diagnostic tool or the lamp with the flash code.",
                "For a manual reset the manual says to hold the diagnostic switch with the ignition on for 4 to 8 seconds. Codes that remain after the reset are current faults. Hardware faults should be fixed before the controller memory is cleared.",
                "Do not confuse a three-digit number with an SPN: the SPN names the component under J1939 and comes paired with an FMI. If the page shows an SPN and FMI pair, that is a different way of recording and a three-digit number cannot be compared with it directly.",
            ]),
            ("Examples from the manual", [
                [
                    "114 - crankshaft rotation sensor signal abnormal; 112 - the same because of a loose sensor connector (a case in the manual).",
                    "134 - rail pressure limiting valve open. The manual works through cases where the cause turned out not to be the valve itself.",
                    "143 - open circuit of the cylinder 3 injector. The cylinder number is part of the code.",
                    "221 - abnormal accelerator pedal signal.",
                    "242 - coolant temperature too high; 324 - speed signal fault.",
                ],
                "The examples illustrate the format. For the full list with causes and actions see the manual for your engine.",
            ]),
            ("Order of checks", [
                "1. Read all the codes, write them down in order of appearance and note which remained after the reset.",
                "2. Start with power and connectors: in the cases analysed in the manual the cause more than once turned out to be a loose connector or harness.",
                "3. For crankshaft sensor and speed codes, check the connector, the gap and the condition of the tone wheel according to the manual.",
                "4. For rail pressure codes, do not replace the valve at once: check the fuel, the filter and the supply, then the valve.",
                "5. After the repair, reset the memory and check for a repeat.",
            ]),
            ("For the driver on the road", [
                "Do not put off entries about coolant temperature and fuel pressure. If the engine loses power, stalls or overheats, stop. Do not treat a lone entry with an unclear description as a reason to keep driving.",
            ]),
            ("Related pages", [
                "[[/en/problemy/peregrev-dvigatelya.html|engine overheating]], [[/en/problemy/problemy-s-toplivom.html|fuel problems]], [[/en/problemy/glohnet-na-hodu.html|engine stalls while driving]]",
            ]),
        ],
        "tail": [
            ("Questions and answers", [
                ("Is code 114 the same as SPN 114?", "No. It is a three-digit Weichai engine code. The SPN comes paired with an FMI in the J1939 format."),
                ("How do I read a code without a scan tool?", "According to the WP10 manual, from the diagnostic lamp flashes: three digits with a one-second pause between them. Take the procedure details from the manual for your truck."),
                ("I cleared the memory and the code came back. What does that mean?", "The fault is still there. The manual advises fixing the hardware cause before clearing the memory."),
            ]),
        ],
    },
})
