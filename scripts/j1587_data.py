# -*- coding: utf-8 -*-
"""
Раздел «Коды J1587/J1708: MID / PID / SID / FMI» (09.11.2026).

Данные страниц: PAGES (одна страница = блок MID + PID или SID, с набором FMI). Построение страниц - novye_kody.py,
источники и расхождения - novye_kody_istochniki.md (рядом).
Названия PID/SID и общий смысл FMI - стандарт SAE J1587 (ред. 02.2002). Набор FMI для узла - таблицы Volvo
(MID 128, 130, 136, 140, 144). Закрытые дилерские базы не использовались.
Поля: fmis - какие FMI у узла перечислены в таблице Volvo (для MID 136 таблица не даёт FMI по строкам: None).
lvl: calm - ехать можно, warn - ехать осторожно и проверить, now - остановиться.
"""

DATE = '2026-11-09'

MIDS = [  # (MID, по стандарту SAE J1587 ru, en, как у Volvo)
    (128, u'Двигатель №1', u'Engine #1', u'ЭБУ двигателя', u'Engine ECU'),
    (130, u'Коробка передач', u'Transmission', u'ЭБУ коробки передач', u'Transmission ECU'),
    (136, u'Тормоза тягача', u'Brakes, power unit', u'ЭБУ тормозов (ABS)', u'Brake ECU (ABS)'),
    (140, u'Приборная панель', u'Instrument cluster', u'Приборная панель', u'Instrument cluster'),
    (144, u'Круиз-контроль', u'Cruise control', u'ЭБУ автомобиля (VECU)', u'Vehicle ECU (VECU)'),
]

# источники: ключ -> (название, адрес)
SRC = {
    'sae': (u'SAE J1587, ред. февраль 2002 (таблицы MID, SID, FMI, список PID; открытая копия документа)',
            u'SAE J1587 (rev. Feb 2002): MID, SID, FMI tables and PID list (public copy of the document)',
            'https://cdn.hackaday.io/files/18651797964384/SAE%20J1587%20(2002%20Standard).pdf'),
    'volvo': (u'Таблицы кодов Volvo MID 128, 130, 136, 140, 144 (PID, PSID, SID, FMI)',
              u'Volvo fault code tables MID 128, 130, 136, 140, 144 (PID, PSID, SID, FMI)',
              'https://pdfcoffee.com/codigo-de-error-volvo-pdf-free.html'),
    'tsi': (u'Volvo, сервисное руководство TSI: MID 144 SID 231 SAE J1939 Control Link, стр. 233',
            u'Volvo TSI service manual: MID 144 SID 231 SAE J1939 Control Link, p. 233',
            'https://manualslib.com/manual/1921428/Volvo-Tsi.html?page=233'),
    'vnl': (u'Volvo VNL, руководство: список MID и PID с текстовыми сообщениями, стр. 148',
            u'Volvo VNL manual: list of MIDs and PIDs with text messages, p. 148',
            'https://www.manualslib.com/manual/822061/Volvo-Vnl.html?page=148'),
}

FMI = {  # по SAE J1587, табл. 7
    0: (u'Значение в норме по цепи, но выше рабочего диапазона', u'Data valid but above normal operational range'),
    1: (u'Значение в норме по цепи, но ниже рабочего диапазона', u'Data valid but below normal operational range'),
    2: (u'Данные нестабильные, прерывистые или неверные', u'Data erratic, intermittent or incorrect'),
    3: (u'Напряжение выше нормы или замыкание на плюс', u'Voltage above normal or shorted high'),
    4: (u'Напряжение ниже нормы или замыкание на массу', u'Voltage below normal or shorted low'),
    5: (u'Ток ниже нормы или обрыв цепи', u'Current below normal or open circuit'),
    6: (u'Ток выше нормы или замыкание цепи на массу', u'Current above normal or grounded circuit'),
    7: (u'Механическая система не отвечает как нужно', u'Mechanical system not responding properly'),
    8: (u'Неверная частота, ширина импульса или период', u'Abnormal frequency, pulse width or period'),
    9: (u'Неверная частота обновления данных (в таблицах Volvo: ошибка связи)',
        u'Abnormal update rate (in Volvo tables: communication fault)'),
    10: (u'Слишком быстрое изменение значения', u'Abnormal rate of change'),
    11: (u'Вид отказа не определён', u'Failure mode not identifiable'),
    12: (u'Неисправен блок или компонент', u'Bad intelligent device or component'),
    13: (u'Вне калибровки', u'Out of calibration'),
    14: (u'Особые указания (смотреть руководство производителя)', u'Special instructions (see manufacturer manual)'),
}

# ---------------------------------------------------------------------------------------------------------------
PAGES = []


def add(**kw):
    PAGES.append(kw)


# ---- MID 130 / 128 / 140 / 144 / 136: SID 231 -------------------------------------------------------------------
add(slug='mid-128-sid-231', mid=128, kind='SID', num='231', label='SID 231', fmis=[2], lvl='warn',
    src=['sae', 'volvo', 'tsi'], nm_ru=u'канал J1939 у ЭБУ двигателя', nm_en=u'J1939 link at the engine ECU',
    title_ru=u'MID 128 SID 231 FMI 2: связь J1939 двигателя — ехать ли',
    title_en=u'MID 128 SID 231 FMI 2: engine J1939 link fault - can you drive',
    ru=dict(
        short=u'SID 231 по стандарту SAE J1587 — канал связи SAE J1939 (CAN). MID 128 — двигатель. FMI 2 — данные прерывистые или неверные: '
              u'блок двигателя не получил подтверждения своих сообщений по CAN. По таблице Volvo это «SAE J1939 Control Link».',
        badge=u'Ехать можно, но осторожно', verdict=u'Обычно ехать можно: код ставит жёлтую лампу, а при потере CAN связь между блоками '
              u'часто идёт запасным каналом J1587/J1708. Остановиться стоит, если двигатель сбросил мощность, глохнет, '
              u'горит красная лампа или пропала часть приборов.',
        checks=[u'Выключите зажигание, откройте разъёмы блока двигателя и других блоков на шине J1939: ищите окисление, влагу, отогнутые и вытянутые контакты.',
                u'Осмотрите жгут J1939 (витая пара, обычно жёлтый и зелёный провода) на протёртость и места изгиба; шевелите жгут при включённом зажигании и смотрите, пропадает ли код.',
                u'Проверьте заряд и клеммы аккумулятора и массы: просадка напряжения даёт ложные ошибки связи.',
                u'Сопротивление между линиями CAN High и CAN Low при выключенном питании должно быть около 60 Ом (два терминатора по 120 Ом); сильно другое значение — обрыв или лишний терминатор. Это работа с мультиметром.',
                u'Если код вернулся после ремонта жгута, проверяйте блоки, которые подключены к J1939, по одному, отключая их: так находят блок, который «роняет» шину.'],
        service=u'Если код появляется вместе с потерей мощности, ошибками коробки или тормозов, или контакты и жгут целы, а код держится, нужна диагностика шины сканером производителя.',
        faq=[(u'Что значит MID 128 SID 231 FMI 2?', u'Блок двигателя (MID 128) не получил подтверждения сообщений по каналу J1939 (SID 231); FMI 2 — данные прерывистые или неверные. Чаще это плохой контакт или обрыв в проводах J1939.'),
             (u'Можно ли с этим ехать?', u'Обычно да, если нет потери мощности и красной лампы. Но причину нужно искать: пропадающая связь может отключить круиз, коробку или ABS на ходу.')]),
    en=dict(
        short=u'SID 231 in SAE J1587 is the SAE J1939 (CAN) data link. MID 128 is the engine. FMI 2 means erratic, intermittent or incorrect data: '
              u'the engine ECU got no confirmation of its messages on the CAN link. Volvo calls it "SAE J1939 Control Link".',
        badge=u'You can drive, carefully', verdict=u'Usually you can drive: the code turns on the yellow lamp and, when CAN drops out, '
              u'control often continues over the backup J1587/J1708 link. Stop if the engine derates, stalls, '
              u'the red lamp comes on or part of the instruments goes dead.',
        checks=[u'Switch the ignition off and open the engine ECU connector and the other J1939 connectors: look for corrosion, moisture, bent or pushed-out pins.',
                u'Inspect the J1939 harness (twisted pair, usually yellow and green) for chafing and bend points; wiggle it with the ignition on and watch whether the code goes away.',
                u'Check battery charge and the battery and ground terminals: a voltage dip causes false link errors.',
                u'With power off, resistance between CAN High and CAN Low should be about 60 ohm (two 120 ohm terminators); a very different value means an open circuit or an extra terminator. This needs a multimeter.',
                u'If the code returns after the harness repair, disconnect the units on J1939 one at a time: that is how the unit that pulls the bus down is found.'],
        service=u'See a workshop if the code appears with power loss, gearbox or brake faults, or if the connectors and harness are fine and the code stays: the bus needs diagnosis with the manufacturer tool.',
        faq=[(u'What does MID 128 SID 231 FMI 2 mean?', u'The engine ECU (MID 128) did not get confirmation for messages on the J1939 link (SID 231); FMI 2 is intermittent or incorrect data. Most often a poor contact or an open wire in the J1939 harness.'),
             (u'Can I drive with it?', u'Usually yes if there is no power loss and no red lamp. But find the cause: a dropping link can disable cruise, the gearbox or ABS on the road.')]))

add(slug='mid-130-sid-231', mid=130, kind='SID', num='231', label='SID 231', fmis=[2], lvl='warn',
    src=['sae', 'volvo', 'tsi'], nm_ru=u'канал J1939 у ЭБУ коробки передач', nm_en=u'J1939 link at the transmission ECU',
    title_ru=u'MID 130 SID 231 FMI 2: связь J1939 коробки — ехать ли',
    title_en=u'MID 130 SID 231 FMI 2: transmission J1939 link - can you drive',
    ru=dict(
        short=u'MID 130 — коробка передач, SID 231 — канал связи SAE J1939, FMI 2 — данные прерывистые или неверные. Типичный случай на тягачах с J1939: '
              u'блок коробки теряет связь с остальными блоками по CAN. Сам по себе он не говорит, что сломана коробка.',
        badge=u'Ехать можно, но осторожно', verdict=u'Если коробка переключается нормально, ехать можно с осторожностью. Если пошла в аварийный режим '
              u'(застряла на одной передаче, не переключается, красная лампа), доезжайте до безопасного места и вызывайте сервис.',
        checks=[u'Посмотрите, нет ли рядом других кодов связи: MID 130 PSID 200/201/204 (потеря связи с двигателем, ЭБУ автомобиля, тормозами), MID 128 SID 231, MID 144 SID 231. Если их несколько — причина общая, в шине J1939, а не в коробке.',
                u'Осмотрите разъём ЭБУ коробки и разъёмы на шине J1939: влага, окисление, вытянутые контакты.',
                u'Проверьте жгут J1939 по всей длине: протёртости, пережатие, следы ремонта; пошевелите жгут при включённом зажигании.',
                u'Проверьте массу и напряжение питания блока коробки и аккумулятор.',
                u'Проверьте сопротивление между CAN High и CAN Low при выключенном питании (около 60 Ом).',
                u'Сотрите код и проверьте, вернётся ли он: разовая запись при пропадании питания — не неисправность.'],
        service=u'Код возвращается сразу после стирания, коробка работает в аварийном режиме или стоит несколько кодов связи — нужна диагностика шины в сервисе.',
        faq=[(u'MID 130 SID 231 FMI 2 — коробка сломана?', u'Не обязательно. Код говорит о связи блока коробки по J1939. Сначала проверяют разъёмы, жгут и питание.'),
             (u'Какие ещё коды смотреть?', u'MID 128 SID 231, MID 140 SID 231, MID 144 SID 231 и PSID «Data Link Error J1939» у MID 130: так видно, у одного ли блока пропала связь или у всей шины.')]),
    en=dict(
        short=u'MID 130 is the transmission, SID 231 is the SAE J1939 data link, FMI 2 is erratic, intermittent or incorrect data. A typical case on trucks with J1939: '
              u'the transmission ECU loses contact with the other units on CAN. By itself it does not say the gearbox is broken.',
        badge=u'You can drive, carefully', verdict=u'If the gearbox shifts normally you can drive with care. If it has gone into limp mode '
              u'(stuck in one gear, will not shift, red lamp), get to a safe place and call a workshop.',
        checks=[u'Look for other link codes: MID 130 PSID 200/201/204 (lost contact with engine, vehicle ECU, brakes), MID 128 SID 231, MID 144 SID 231. Several of them mean the cause is the J1939 bus, not the gearbox.',
                u'Inspect the transmission ECU connector and the J1939 connectors: moisture, corrosion, pushed-out pins.',
                u'Check the J1939 harness along its length: chafing, pinching, signs of earlier repairs; wiggle it with the ignition on.',
                u'Check ground and supply voltage at the transmission ECU, and the battery.',
                u'Check resistance between CAN High and CAN Low with power off (about 60 ohm).',
                u'Clear the code and see whether it returns: a one-off entry during a supply dip is not a fault.'],
        service=u'The code returns right after clearing, the gearbox runs in limp mode, or several link codes are stored: the bus needs diagnosis in a workshop.',
        faq=[(u'Is the gearbox broken with MID 130 SID 231 FMI 2?', u'Not necessarily. The code is about the gearbox ECU link on J1939. Check connectors, harness and supply first.'),
             (u'Which other codes should I look at?', u'MID 128 SID 231, MID 140 SID 231, MID 144 SID 231 and the "Data Link Error J1939" PSIDs under MID 130: they show whether one unit lost the link or the whole bus.')]))

add(slug='mid-140-sid-231', mid=140, kind='SID', num='231', label='SID 231', fmis=[2], lvl='calm',
    src=['sae', 'volvo'], nm_ru=u'канал J1939 у приборной панели', nm_en=u'J1939 link at the instrument cluster',
    title_ru=u'MID 140 SID 231 FMI 2: связь J1939 панели приборов',
    title_en=u'MID 140 SID 231 FMI 2: instrument cluster J1939 link fault',
    ru=dict(
        short=u'MID 140 — приборная панель, SID 231 — канал SAE J1939, FMI 2 — данные прерывистые или неверные. Панель получает по CAN скорость, обороты, температуры; код значит, что связь по J1939 нестабильна.',
        badge=u'Ехать можно', verdict=u'Обычно ехать можно, но следите за приборами: при потере связи показания могут пропадать или замирать (спидометр, давление, температура). Если приборам не доверяете, остановитесь и проверьте уровни и давление по факту.',
        checks=[u'Отметьте, что именно пропадает на панели: скорость, обороты, температуры. Это показывает, какой блок не доходит до панели.',
                u'Проверьте разъём панели и массу панели.',
                u'Осмотрите жгут J1939 за панелью и под рулевой колонкой: частое место обрыва — перегиб при движении.',
                u'Проверьте питание панели и аккумулятор.',
                u'Сравните с MID 128 SID 231 и MID 130 SID 231: если те же коды есть у других блоков, причина общая — шина.'],
        service=u'Показания пропадают регулярно, нет уверенности в давлении масла и температуре — в сервис, не откладывая.',
        faq=[(u'Что означает MID 140 SID 231 FMI 2?', u'Приборная панель (MID 140) теряет данные на шине J1939 (SID 231): сообщения приходят прерывисто или неверно.'),
             (u'Из-за чего пропадают показания приборов?', u'Чаще из-за плохого контакта разъёма панели или обрыва в жгуте J1939, реже из-за самой панели.')]),
    en=dict(
        short=u'MID 140 is the instrument cluster, SID 231 is the SAE J1939 link, FMI 2 is erratic, intermittent or incorrect data. The cluster gets speed, rpm and temperatures over CAN; the code means the J1939 link is unstable.',
        badge=u'You can drive', verdict=u'You can usually drive, but watch the gauges: when the link is lost, readings may drop out or freeze (speed, pressure, temperature). If you do not trust the gauges, stop and check levels and pressure directly.',
        checks=[u'Note what exactly drops out on the cluster: speed, rpm, temperatures. It shows which unit is not reaching the cluster.',
                u'Check the cluster connector and the cluster ground.',
                u'Inspect the J1939 harness behind the cluster and under the steering column: a common break point is a bend that flexes while driving.',
                u'Check the cluster supply and the battery.',
                u'Compare with MID 128 SID 231 and MID 130 SID 231: the same codes on other units mean a common cause, the bus.'],
        service=u'Readings drop out regularly and you cannot trust oil pressure and temperature: see a workshop without delay.',
        faq=[(u'What does MID 140 SID 231 FMI 2 mean?', u'The instrument cluster (MID 140) loses data on the J1939 link (SID 231): messages arrive intermittently or incorrectly.'),
             (u'Why do the gauges drop out?', u'Most often a poor cluster connector contact or a break in the J1939 harness, less often the cluster itself.')]))

add(slug='mid-144-sid-231', mid=144, kind='SID', num='231', label='SID 231', fmis=[2, 12], lvl='warn',
    src=['sae', 'volvo', 'tsi', 'vnl'], nm_ru=u'канал J1939 у ЭБУ автомобиля (VECU)', nm_en=u'J1939 link at the vehicle ECU (VECU)',
    title_ru=u'MID 144 SID 231 FMI 2 и 12: связь J1939 ЭБУ автомобиля',
    title_en=u'MID 144 SID 231 FMI 2 and 12: vehicle ECU J1939 link fault',
    ru=dict(
        short=u'SID 231 — канал SAE J1939 (по стандарту), MID 144 — у Volvo ЭБУ автомобиля (VECU), по стандарту SAE — круиз-контроль. '
              u'Руководство Volvo описывает «SAE J1939 Control Link»: быстрая связь блоков, по которой управляется машина; при отказе запасным каналом служит J1587/J1708.',
        badge=u'Ехать можно, но осторожно', verdict=u'Руководство Volvo: при коде ставится жёлтая лампа. Ехать можно, но возможны отключённый круиз-контроль, ограничения коробки и других систем. '
              u'Красная лампа, потеря мощности или остановка двигателя — остановиться.',
        checks=[u'FMI 2: ЭБУ не получает подтверждения сообщений по J1939. Руководство Volvo называет причины: плохое соединение, обрыв провода J1939, сопротивление и окисление контактов.',
                u'FMI 12: от какого-то блока на шине не приходят ожидаемые сообщения. Причины те же: обрыв провода, окисление контактов.',
                u'Откройте и осмотрите разъёмы блоков на шине J1939, особенно ЭБУ автомобиля, двигателя, коробки, тормозов.',
                u'Прозвоните жгут J1939 и проверьте сопротивление между CAN High и CAN Low (около 60 Ом при выключенном питании).',
                u'Посмотрите коды MID 144 PSID 200–214: «Communication Error, J1939» с номером блока показывает, какой именно блок пропал.'],
        service=u'Блок связи не определился или код возвращается после чистки контактов — диагностика шины в сервисе (Volvo: проверка по процедуре «SAE J1939 Control Link, Check»).',
        faq=[(u'MID 144 у Volvo — это круиз-контроль?', u'По стандарту SAE J1587 MID 144 — круиз-контроль. В таблицах Volvo этот блок — ЭБУ автомобиля (VECU), в руководстве VNL подписан «Cab Controller». Берите описание по марке вашей машины.'),
             (u'В чём разница между FMI 2 и FMI 12 у SID 231?', u'FMI 2 — ЭБУ не получает подтверждения своих сообщений. FMI 12 — не приходят ожидаемые сообщения от какого-то блока на шине.')]),
    en=dict(
        short=u'SID 231 is the SAE J1939 link (by the standard); MID 144 is the Vehicle ECU (VECU) at Volvo and cruise control in the SAE standard. '
              u'The Volvo manual describes "SAE J1939 Control Link": the fast link between units that controls the truck; if it fails, J1587/J1708 serves as the backup.',
        badge=u'You can drive, carefully', verdict=u'Volvo manual: the code turns on the yellow lamp. You can drive, but cruise control, gearbox and other functions may be limited. '
              u'A red lamp, power loss or an engine stop means stopping.',
        checks=[u'FMI 2: the ECU gets no confirmation for messages on J1939. The Volvo manual lists the causes: a loose connection, an open J1939 wire, contact resistance and oxidation.',
                u'FMI 12: expected messages from some unit on the bus are missing. The same causes: an open wire, contact oxidation.',
                u'Open and inspect the connectors of the units on J1939, especially the vehicle ECU, engine, gearbox and brake ECU.',
                u'Test the J1939 harness continuity and the resistance between CAN High and CAN Low (about 60 ohm with power off).',
                u'Look at MID 144 PSID 200-214: "Communication Error, J1939" with a unit number shows which unit dropped out.'],
        service=u'You cannot find the unit or the code returns after cleaning the contacts: bus diagnosis in a workshop (Volvo: the "SAE J1939 Control Link, Check" procedure).',
        faq=[(u'Is MID 144 at Volvo cruise control?', u'In the SAE J1587 standard MID 144 is cruise control. In Volvo tables the unit is the Vehicle ECU (VECU), and the VNL manual labels it "Cab Controller". Use the description for your make.'),
             (u'What is the difference between FMI 2 and FMI 12 for SID 231?', u'FMI 2: the ECU gets no confirmation of its own messages. FMI 12: expected messages from some unit on the bus do not arrive.')]))

add(slug='mid-136-sid-231', mid=136, kind='SID', num='231', label='SID 231', fmis=None, lvl='warn',
    src=['sae', 'volvo', 'vnl'], nm_ru=u'нет связи J1939 у ЭБУ тормозов (ABS)', nm_en=u'J1939 not communicating at the brake ECU (ABS)',
    title_ru=u'MID 136 SID 231: ABS не связывается по J1939 — ехать ли',
    title_en=u'MID 136 SID 231: ABS J1939 not communicating - can you drive',
    ru=dict(
        short=u'MID 136 — тормоза тягача (ЭБУ ABS), SID 231 — канал SAE J1939. В таблице Volvo строка называется «J1939 Not Communicating»; FMI по этой строке в нашем источнике не приведён, значение FMI смотрите по общей таблице ниже.',
        badge=u'Ехать осторожно, не быстро', verdict=u'Рабочие тормоза остаются, но блок ABS мог потерять связь с машиной, и ABS и противобуксовочные функции могут быть недоступны. Ехать можно только медленно, с большой дистанцией, без спешки, и сразу в сервис.',
        checks=[u'Посмотрите, горит ли лампа ABS и есть ли другие коды связи (MID 128 или 130 SID 231): общая причина — шина J1939.',
                u'Осмотрите разъём блока ABS и разъём на шине рядом: влага, окисление, вытянутые контакты.',
                u'Проверьте жгут J1939 у рамы и у тормозных узлов: там чаще всего протирается.',
                u'Проверьте питание блока ABS: предохранитель, клеммы, массу.',
                u'После ремонта сотрите код и проедьте несколько километров: убедитесь, что лампа ABS гаснет.'],
        service=u'Лампа ABS горит после проверки разъёмов и питания — диагностика блока ABS и шины в сервисе. С прицепом и в скользких условиях ехать не стоит.',
        faq=[(u'Работают ли тормоза с кодом MID 136 SID 231?', u'Обычные тормоза работают, но не рассчитывайте на то, что ABS вмешается. Дистанцию увеличивайте, скорость снижайте.'),
             (u'Чем отличается MID 136 SID 231 от SID 254?', u'SID 231 — нет связи по J1939 (канал), SID 254 — «ЭБУ не отвечает» (сам блок). Первое чаще лечится жгутом и разъёмами, второе — питанием и самим блоком.')]),
    en=dict(
        short=u'MID 136 is the power unit brakes (ABS ECU), SID 231 is the SAE J1939 link. In the Volvo table the row is called "J1939 Not Communicating"; the FMI for this row is not given in our source, so read the FMI from the general table below.',
        badge=u'Drive carefully and slowly', verdict=u'The service brakes remain, but the ABS unit may have lost contact with the truck and ABS and traction functions may be unavailable. Drive slowly with a large gap, no rush, and go straight to a workshop.',
        checks=[u'See whether the ABS lamp is on and whether other link codes exist (MID 128 or 130 SID 231): a common cause means the J1939 bus.',
                u'Inspect the ABS ECU connector and the nearby bus connector: moisture, corrosion, pushed-out pins.',
                u'Check the J1939 harness near the frame and the brake units: it chafes there most often.',
                u'Check ABS ECU supply: fuse, terminals, ground.',
                u'After repair clear the code and drive a few kilometres: make sure the ABS lamp goes out.'],
        service=u'The ABS lamp stays on after the connectors and supply check: diagnose the ABS unit and the bus in a workshop. Do not drive with a trailer or on slippery roads.',
        faq=[(u'Do the brakes work with MID 136 SID 231?', u'The ordinary brakes work, but do not count on ABS stepping in. Increase the gap and lower the speed.'),
             (u'How does MID 136 SID 231 differ from SID 254?', u'SID 231 is no communication on J1939 (the link); SID 254 is "ECU not communicating" (the unit itself). The first is more often a harness or connector issue, the second a supply or the unit.')]))

# ---- Двигатель MID 128: PID ------------------------------------------------------------------------------------
add(slug='mid-128-pid-100', mid=128, kind='PID', num='100', label='PID 100', fmis=[1, 3, 5], lvl='now',
    src=['sae', 'volvo'], nm_ru=u'давление масла двигателя', nm_en=u'engine oil pressure',
    title_ru=u'MID 128 PID 100: давление масла — FMI 1, 3, 5, ехать ли',
    title_en=u'MID 128 PID 100: engine oil pressure - FMI 1, 3, 5, can you drive',
    ru=dict(
        short=u'PID 100 по стандарту SAE J1587 — давление масла двигателя, MID 128 — двигатель. По таблице Volvo у этого параметра бывают FMI 1 (ниже нормы), 3 (замыкание на плюс) и 5 (обрыв).',
        badge=u'FMI 1: остановиться', verdict=u'FMI 1 — давление масла ниже допустимого: двигатель заглушите, ехать нельзя, пока не проверите уровень масла. '
              u'FMI 3 и 5 — неисправность цепи датчика: давление может быть нормальным, но проверьте его механическим манометром, пока не убедитесь.',
        checks=[u'Остановитесь, заглушите двигатель и подождите несколько минут. Проверьте уровень масла по щупу.',
                u'Нет подтёков масла под двигателем и на фильтре.',
                u'FMI 3 и 5: осмотрите разъём датчика давления, провод, ищите замыкание или обрыв; плохой контакт также даёт эти коды.',
                u'Если уровень в норме, а FMI 1 остаётся, давление проверяют манометром в сервисе до дальнейшей работы двигателя.',
                u'С FMI 3 или 5 допустимо доехать до сервиса, если на панели давление по факту в норме, нет красной лампы и стука.'],
        service=u'FMI 1 с красной лампой или стуком — эвакуатор: работа двигателя без давления масла разрушает его за минуты. Электрические FMI 3 и 5 — диагностика датчика и цепи.',
        faq=[(u'Что значит MID 128 PID 100 FMI 1?', u'Давление масла ниже рабочего диапазона. Это настоящая причина остановиться и проверить уровень и давление.'),
             (u'MID 128 PID 100 FMI 3 или 5 — опасно?', u'Это ошибки цепи датчика (замыкание на плюс или обрыв). Двигатель при этом может работать нормально, но подтвердите давление независимо от показаний.')]),
    en=dict(
        short=u'PID 100 in SAE J1587 is engine oil pressure, MID 128 is the engine. The Volvo table lists FMI 1 (below normal), 3 (shorted high) and 5 (open circuit) for it.',
        badge=u'FMI 1: stop', verdict=u'FMI 1 means oil pressure below the allowed range: shut the engine down and do not drive until you have checked the oil level. '
              u'FMI 3 and 5 are sensor circuit faults: the pressure may be normal, but confirm it with a mechanical gauge before relying on it.',
        checks=[u'Stop, shut the engine down and wait a few minutes. Check the oil level on the dipstick.',
                u'Look for oil leaks under the engine and at the filter.',
                u'FMI 3 and 5: inspect the pressure sensor connector and wire for a short or an open circuit; a poor contact also gives these codes.',
                u'If the level is right and FMI 1 stays, the pressure must be checked with a gauge in a workshop before the engine runs again.',
                u'With FMI 3 or 5 you can reach a workshop if the real pressure is normal, there is no red lamp and no knocking.'],
        service=u'FMI 1 with a red lamp or knocking: call a tow; running without oil pressure destroys the engine in minutes. Electrical FMI 3 and 5: diagnose the sensor and circuit.',
        faq=[(u'What does MID 128 PID 100 FMI 1 mean?', u'Oil pressure is below the operating range. It is a real reason to stop and check level and pressure.'),
             (u'Is MID 128 PID 100 FMI 3 or 5 dangerous?', u'They are sensor circuit faults (shorted high or open). The engine may run normally, but confirm the pressure independently of the reading.')]))

add(slug='mid-128-pid-110', mid=128, kind='PID', num='110', label='PID 110', fmis=[0, 2, 4, 5, 10], lvl='now',
    src=['sae', 'volvo'], nm_ru=u'температура охлаждающей жидкости', nm_en=u'engine coolant temperature',
    title_ru=u'MID 128 PID 110: температура охлаждающей жидкости — FMI',
    title_en=u'MID 128 PID 110: coolant temperature - FMI 0, 2, 4, 5, 10',
    ru=dict(
        short=u'PID 110 по SAE J1587 — температура охлаждающей жидкости двигателя, MID 128 — двигатель. Таблица Volvo даёт FMI 0, 2, 4, 5, 10.',
        badge=u'FMI 0: остановиться', verdict=u'FMI 0 — температура выше допустимой: заглушите двигатель, дайте остыть, проверьте уровень охлаждающей жидкости. Ехать с перегревом нельзя. '
              u'Остальные FMI — датчик или цепь: можно доехать осторожно, сверяя температуру со стрелкой.',
        checks=[u'При FMI 0 остановитесь, снизьте обороты и заглушите двигатель после короткой работы на холостом ходу. Не открывайте крышку бачка горячей.',
                u'Проверьте уровень охлаждающей жидкости, подтёки, натяжение и целость ремня привода вентилятора и помпы.',
                u'Включается ли вентилятор (муфта) при нагреве; не забиты ли соты радиатора.',
                u'FMI 2, 4, 5, 10: проверьте разъём и провод датчика, ищите окисление, обрыв, замыкание; сравните показание стрелки с ощущением (сильно горячий верхний патрубок при холодной стрелке — датчик).',
                u'Не продолжайте поездку, если температура растёт вместе с ошибкой.'],
        service=u'Перегрев подтверждён или повторяется — сервис: возможна прокладка ГБЦ, помпа, термостат. Электрические FMI — замена датчика и проверка цепи.',
        faq=[(u'Что значит MID 128 PID 110 FMI 0?', u'Температура охлаждающей жидкости выше рабочего диапазона — вероятный перегрев.'),
             (u'А FMI 4 и 5?', u'Это обрыв и замыкание в цепи датчика температуры: показание теряется, блок двигателя может ограничивать работу.')]),
    en=dict(
        short=u'PID 110 in SAE J1587 is engine coolant temperature, MID 128 is the engine. The Volvo table lists FMI 0, 2, 4, 5, 10.',
        badge=u'FMI 0: stop', verdict=u'FMI 0 means temperature above the allowed range: shut the engine down, let it cool and check the coolant level. Do not drive while overheating. '
              u'The other FMIs are the sensor or its circuit: you can drive carefully, checking the gauge.',
        checks=[u'With FMI 0, stop, lower rpm and shut down after a short idle. Do not open the expansion tank cap hot.',
                u'Check the coolant level, leaks, the tension and condition of the fan and water pump drive belt.',
                u'Does the fan (clutch) engage when hot; are the radiator cores blocked.',
                u'FMI 2, 4, 5, 10: check the sensor connector and wire for corrosion, an open circuit or a short; compare the gauge with reality (a very hot upper hose with a cold gauge points at the sensor).',
                u'Do not continue the trip if the temperature climbs together with the code.'],
        service=u'Overheating is confirmed or repeats: workshop; a head gasket, water pump or thermostat may be the cause. Electrical FMIs: replace the sensor and check the circuit.',
        faq=[(u'What does MID 128 PID 110 FMI 0 mean?', u'Coolant temperature is above the operating range: probable overheating.'),
             (u'And FMI 4 and 5?', u'An open circuit and a short in the temperature sensor circuit: the reading is lost, and the engine ECU may limit operation.')]))

add(slug='mid-128-pid-102', mid=128, kind='PID', num='102', label='PID 102', fmis=[0, 1, 2, 3, 5, 11], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'давление наддува (во впускном коллекторе)', nm_en=u'boost (intake manifold) pressure',
    title_ru=u'MID 128 PID 102: давление наддува — FMI, ехать ли',
    title_en=u'MID 128 PID 102: boost pressure - FMI 0, 1, 2, 3, 5, 11',
    ru=dict(
        short=u'PID 102 по SAE J1587 — давление наддува (Boost Pressure), в таблице Volvo — давление во впускном коллекторе. MID 128 — двигатель. FMI по Volvo: 0, 1, 2, 3, 5, 11.',
        badge=u'Ехать осторожно', verdict=u'Обычно ехать можно на сниженной мощности до сервиса. Остановиться, если из выхлопа валит чёрный или белый дым, слышен свист и вой турбины или температура растёт.',
        checks=[u'FMI 0 и 1: давление выше или ниже нормы. Проверьте шланги наддува и хомуты: трещины, соскочивший патрубок, масло в патрубках.',
                u'Проверьте воздушный фильтр: забитый даёт падение давления.',
                u'Осмотрите интеркулер и его патрубки на подтёки масла и трещины.',
                u'FMI 3 и 5: разъём и провод датчика давления, замыкание на плюс или обрыв.',
                u'Нет ли других кодов турбины (PSID 98 Boost Air Pressure System, SID 27 VGT) и пропусков выхлопа.'],
        service=u'Если сниженная мощность не уходит после осмотра патрубков и фильтра — сервис: проверка турбины, привода регулирования, датчика.',
        faq=[(u'Можно ли ехать с MID 128 PID 102?', u'Обычно да, на сниженной мощности, если нет дыма, свиста и роста температуры. Дольше затягивать не стоит: утечка наддува перегружает двигатель.'),
             (u'FMI 0 или 1 — датчик или турбина?', u'Сначала шланги, фильтр и патрубки, потом датчик и турбина. Датчик ошибочно винят чаще всего.')]),
    en=dict(
        short=u'PID 102 in SAE J1587 is boost pressure; the Volvo table gives it as intake manifold pressure. MID 128 is the engine. Volvo FMIs: 0, 1, 2, 3, 5, 11.',
        badge=u'Drive carefully', verdict=u'Usually you can drive at reduced power to a workshop. Stop if black or white smoke pours from the exhaust, you hear a whistle or turbo howl, or temperature climbs.',
        checks=[u'FMI 0 and 1: pressure above or below normal. Check the boost hoses and clamps: cracks, a pipe that came off, oil in the pipes.',
                u'Check the air filter: a blocked one drops the pressure.',
                u'Inspect the intercooler and its pipes for oil seepage and cracks.',
                u'FMI 3 and 5: the pressure sensor connector and wire, a short high or an open circuit.',
                u'Look for other turbo codes (PSID 98 Boost Air Pressure System, SID 27 VGT) and exhaust leaks.'],
        service=u'If the power loss stays after checking pipes and filter: workshop, to test the turbo, its actuator and the sensor.',
        faq=[(u'Can I drive with MID 128 PID 102?', u'Usually yes, at reduced power, if there is no smoke, whistle or temperature rise. Do not stretch it: a boost leak overloads the engine.'),
             (u'FMI 0 or 1: sensor or turbo?', u'Hoses, filter and pipes first, then the sensor and the turbo. The sensor is blamed wrongly most often.')]))

add(slug='mid-128-pid-105', mid=128, kind='PID', num='105', label='PID 105', fmis=[0, 1, 2, 4, 5, 10], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'температура воздуха во впускном коллекторе', nm_en=u'intake manifold temperature',
    title_ru=u'MID 128 PID 105: температура воздуха на впуске — FMI',
    title_en=u'MID 128 PID 105: intake manifold temperature - FMI list',
    ru=dict(
        short=u'PID 105 по SAE J1587 — температура воздуха во впускном коллекторе. MID 128 — двигатель. Таблица Volvo: FMI 0, 1, 2, 4, 5, 10.',
        badge=u'Ехать осторожно', verdict=u'Обычно ехать можно: блок двигателя при потере показаний подставляет запасное значение и может немного снизить мощность. Остановиться, если мощность упала резко или вырос расход, пошёл дым.',
        checks=[u'FMI 0: температура выше нормы. Проверьте интеркулер: грязь на сотах, подтёки масла, неплотный патрубок.',
                u'Нет ли перегрева двигателя и забитого радиатора рядом с интеркулером.',
                u'FMI 4 и 5: проверьте разъём и провод датчика (замыкание на массу или обрыв).',
                u'FMI 2 и 10: нестабильные показания — плохой контакт датчика, окисление разъёма.',
                u'Сверьте с другими кодами наддува (PID 102).'],
        service=u'Код не уходит после чистки интеркулера и разъёма — замена датчика и проверка цепи в сервисе.',
        faq=[(u'Чем опасен MID 128 PID 105 FMI 0?', u'Горячий воздух на впуске снижает мощность и перегружает двигатель, если причина — забитый интеркулер.'),
             (u'Датчик температуры воздуха на впуске дорогой?', u'Обычно простой датчик; сначала проверьте разъём и провод, потом меняйте.')]),
    en=dict(
        short=u'PID 105 in SAE J1587 is intake manifold temperature. MID 128 is the engine. Volvo table: FMI 0, 1, 2, 4, 5, 10.',
        badge=u'Drive carefully', verdict=u'You can usually drive: when the reading is lost, the engine ECU substitutes a fallback value and may reduce power a little. Stop if power drops sharply, consumption jumps or smoke appears.',
        checks=[u'FMI 0: temperature above normal. Check the intercooler: dirt on the cores, oil seepage, a loose pipe.',
                u'Check the engine is not overheating and the radiator next to the intercooler is not blocked.',
                u'FMI 4 and 5: check the sensor connector and wire (short to ground or an open circuit).',
                u'FMI 2 and 10: unstable readings point to a poor sensor contact or corroded connector.',
                u'Compare with other boost codes (PID 102).'],
        service=u'The code stays after cleaning the intercooler and connector: replace the sensor and check the circuit in a workshop.',
        faq=[(u'Why is MID 128 PID 105 FMI 0 harmful?', u'Hot intake air lowers power and overloads the engine if the cause is a blocked intercooler.'),
             (u'Is the intake air temperature sensor expensive?', u'It is usually a simple sensor; check the connector and wire first, then replace.')]))

add(slug='mid-128-pid-111', mid=128, kind='PID', num='111', label='PID 111', fmis=[1, 3, 4, 5], lvl='now',
    src=['sae', 'volvo'], nm_ru=u'уровень охлаждающей жидкости', nm_en=u'coolant level',
    title_ru=u'MID 128 PID 111: уровень охлаждающей жидкости — FMI 1, 3, 4, 5',
    title_en=u'MID 128 PID 111: coolant level - FMI 1, 3, 4, 5',
    ru=dict(
        short=u'PID 111 по SAE J1587 — уровень охлаждающей жидкости. MID 128 — двигатель. Таблица Volvo: FMI 1 (низкий уровень), 3, 4, 5 (цепь датчика).',
        badge=u'FMI 1: остановиться', verdict=u'FMI 1 — уровень низкий: не ехать, пока не проверите бачок остывшего двигателя и не долили жидкость. FMI 3, 4, 5 — датчик уровня или его цепь: проверьте уровень вручную.',
        checks=[u'Остановитесь, дайте двигателю остыть, проверьте уровень в расширительном бачке (на холодном двигателе).',
                u'Осмотрите шланги, радиатор, помпу и крышку бачка на подтёки и белые следы засохшей жидкости.',
                u'Нет ли масла в охлаждающей жидкости и жидкости на щупе: признак прокладки ГБЦ.',
                u'FMI 3, 4, 5: разъём и провод датчика уровня в бачке.',
                u'Доливайте только жидкость нужной спецификации, смешивайте только совместимые.'],
        service=u'Уровень падает снова — сервис: течь, прокладка, радиатор. Электрические FMI — датчик уровня.',
        faq=[(u'Что значит MID 128 PID 111 FMI 1?', u'Уровень охлаждающей жидкости ниже нормы.'),
             (u'Можно ли долить воду?', u'Как временное решение — да, но потом жидкость нужно заменить на правильную смесь, и найти причину утечки.')]),
    en=dict(
        short=u'PID 111 in SAE J1587 is coolant level. MID 128 is the engine. Volvo table: FMI 1 (low level), 3, 4, 5 (sensor circuit).',
        badge=u'FMI 1: stop', verdict=u'FMI 1 means low level: do not drive until you have checked the cold expansion tank and topped up. FMI 3, 4, 5 are the level sensor or its circuit: check the level by hand.',
        checks=[u'Stop, let the engine cool and check the level in the expansion tank (cold engine).',
                u'Inspect hoses, radiator, water pump and cap for leaks and white traces of dried coolant.',
                u'Look for oil in the coolant and coolant on the dipstick: a head gasket sign.',
                u'FMI 3, 4, 5: the level sensor connector and wire in the tank.',
                u'Top up only with the right specification; mix only compatible coolants.'],
        service=u'The level drops again: workshop, for a leak, head gasket or radiator. Electrical FMIs: the level sensor.',
        faq=[(u'What does MID 128 PID 111 FMI 1 mean?', u'The coolant level is below normal.'),
             (u'Can I top up with water?', u'As a temporary measure yes, but replace it later with the right mixture and find the cause of the leak.')]))

add(slug='mid-128-pid-175', mid=128, kind='PID', num='175', label='PID 175', fmis=[0, 2, 4, 5], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'температура масла двигателя', nm_en=u'engine oil temperature',
    title_ru=u'MID 128 PID 175: температура масла двигателя — FMI 0, 2, 4, 5',
    title_en=u'MID 128 PID 175: engine oil temperature - FMI 0, 2, 4, 5',
    ru=dict(
        short=u'PID 175 по SAE J1587 — температура масла двигателя. MID 128 — двигатель. Таблица Volvo: FMI 0, 2, 4, 5.',
        badge=u'FMI 0: остановиться', verdict=u'FMI 0 — масло слишком горячее: снизьте нагрузку, остановитесь, проверьте охлаждение и уровень масла. FMI 2, 4, 5 — датчик или цепь: ехать можно осторожно, сверяя с температурой охлаждающей жидкости.',
        checks=[u'При FMI 0 проверьте охлаждающую жидкость и уровень масла, температуру двигателя по стрелке.',
                u'Осмотрите масляный радиатор или теплообменник и их патрубки, соты радиатора.',
                u'FMI 4 и 5: разъём и провод датчика температуры масла.',
                u'FMI 2: нестабильный сигнал — контакты датчика и жгут.',
                u'Сравните с другими кодами по перегреву: PID 110 (охлаждающая жидкость).'],
        service=u'Масло перегревается без видимой причины — сервис: теплообменник, насос, перегруз.',
        faq=[(u'MID 128 PID 175 FMI 0 — это перегрев двигателя?', u'Не обязательно, но связано: горячее масло теряет вязкость. Проверьте охлаждение двигателя.'),
             (u'Отличается ли PID 175 от PID 100?', u'Да: PID 175 — температура масла, PID 100 — давление масла.')]),
    en=dict(
        short=u'PID 175 in SAE J1587 is engine oil temperature. MID 128 is the engine. Volvo table: FMI 0, 2, 4, 5.',
        badge=u'FMI 0: stop', verdict=u'FMI 0 means the oil is too hot: reduce load, stop, check cooling and oil level. FMI 2, 4, 5 are the sensor or circuit: you can drive carefully, comparing with the coolant temperature.',
        checks=[u'With FMI 0 check the coolant and the oil level, and engine temperature on the gauge.',
                u'Inspect the oil cooler or heat exchanger and its pipes, and the radiator cores.',
                u'FMI 4 and 5: the oil temperature sensor connector and wire.',
                u'FMI 2: unstable signal; the sensor contacts and harness.',
                u'Compare with other overheating codes: PID 110 (coolant).'],
        service=u'The oil overheats without an obvious cause: workshop, for the heat exchanger, pump or overload.',
        faq=[(u'Is MID 128 PID 175 FMI 0 engine overheating?', u'Not necessarily, but related: hot oil loses viscosity. Check engine cooling.'),
             (u'Does PID 175 differ from PID 100?', u'Yes: PID 175 is oil temperature, PID 100 is oil pressure.')]))

add(slug='mid-128-pid-94', mid=128, kind='PID', num='94', label='PID 94', fmis=[1, 3, 5, 7], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'давление подачи топлива', nm_en=u'fuel delivery pressure',
    title_ru=u'MID 128 PID 94: давление топлива в магистрали — FMI 1, 3, 5, 7',
    title_en=u'MID 128 PID 94: fuel delivery pressure - FMI 1, 3, 5, 7',
    ru=dict(
        short=u'PID 94 по SAE J1587 — давление подачи топлива (Fuel Delivery Pressure). MID 128 — двигатель. Таблица Volvo: FMI 1, 3, 5, 7.',
        badge=u'Ехать осторожно', verdict=u'Низкое давление топлива (FMI 1, 7) грозит потерей мощности и остановкой двигателя под нагрузкой: ехать можно только недалеко и без обгонов, лучше сразу в сервис. FMI 3 и 5 — датчик: давление может быть нормальным.',
        checks=[u'Проверьте топливо в баке и подтёки на магистралях, подсос воздуха в соединениях.',
                u'Замените или осмотрите топливные фильтры: забитый фильтр — частая причина падения давления.',
                u'Проверьте отстойник и слив воды (см. PID 97).',
                u'FMI 3 и 5: разъём и провод датчика давления топлива.',
                u'Подкачивающий насос: слышна ли его работа при включении зажигания.'],
        service=u'Давление падает под нагрузкой или двигатель глохнет — сервис: насос подкачки, регулятор, форсунки. Работа на «голодном» топливе повреждает насос.',
        faq=[(u'Почему падает давление топлива?', u'Чаще всего забит фильтр или подсасывает воздух. Реже — износ насоса.'),
             (u'FMI 7 — это что?', u'Механическая часть не отвечает: давление не такое, как команда блока. Смотрят насос и регулятор.')]),
    en=dict(
        short=u'PID 94 in SAE J1587 is fuel delivery pressure. MID 128 is the engine. Volvo table: FMI 1, 3, 5, 7.',
        badge=u'Drive carefully', verdict=u'Low fuel pressure (FMI 1, 7) threatens power loss and a stall under load: drive only a short way and without overtaking, better go straight to a workshop. FMI 3 and 5 are the sensor: the pressure may be fine.',
        checks=[u'Check the fuel in the tank, leaks on the lines and air intake at the joints.',
                u'Inspect or replace the fuel filters: a blocked filter is a common cause of low pressure.',
                u'Check the water separator and drain (see PID 97).',
                u'FMI 3 and 5: the fuel pressure sensor connector and wire.',
                u'The lift pump: can you hear it when the ignition comes on.'],
        service=u'Pressure drops under load or the engine stalls: workshop, for the lift pump, regulator or injectors. Running on starved fuel damages the pump.',
        faq=[(u'Why does fuel pressure drop?', u'Most often a blocked filter or air getting in. Less often a worn pump.'),
             (u'What is FMI 7?', u'The mechanical part does not respond: the pressure is not what the ECU commands. The pump and regulator are checked.')]))

add(slug='mid-128-pid-97', mid=128, kind='PID', num='97', label='PID 97', fmis=[3, 4], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'вода в топливе', nm_en=u'water in fuel indicator',
    title_ru=u'MID 128 PID 97: вода в топливе — датчик, FMI 3 и 4',
    title_en=u'MID 128 PID 97: water in fuel indicator - FMI 3 and 4',
    ru=dict(
        short=u'PID 97 по SAE J1587 — индикатор воды в топливе (Water in Fuel Indicator). MID 128 — двигатель. Таблица Volvo: FMI 3 и 4 — электрика цепи датчика.',
        badge=u'Ехать осторожно', verdict=u'Сначала слейте воду из отстойника: вода в топливе губит насос и форсунки. Если воды нет, а код остаётся — это датчик или провод, ехать можно в сервис.',
        checks=[u'Слейте отстойник топливного фильтра до чистого топлива; на стоянке после дождя, у заправки с сомнительным топливом это делают в первую очередь.',
                u'Осмотрите разъём датчика в отстойнике и провод: замыкание на плюс (FMI 3) или на массу (FMI 4).',
                u'Проверьте, не залипла ли вода в бачке при морозе (лёд в магистрали).',
                u'Замените фильтр, если загрязнён.',
                u'Не заправляйтесь на подозрительной станции, пока причина не найдена.'],
        service=u'Вода возвращается — сервис: вычистить бак и магистрали, проверить насос и форсунки.',
        faq=[(u'MID 128 PID 97 — это неисправность датчика?', u'Оба варианта: может быть реальная вода (лампа и код) или неисправная цепь датчика (FMI 3, 4). Начните со слива отстойника.'),
             (u'Что будет, если не сливать воду?', u'Вода разрушает смазку топливной аппаратуры и ведёт к ремонту насоса и форсунок.')]),
    en=dict(
        short=u'PID 97 in SAE J1587 is the water in fuel indicator. MID 128 is the engine. Volvo table: FMI 3 and 4, the circuit electrics of the sensor.',
        badge=u'Drive carefully', verdict=u'First drain the water from the separator: water in fuel ruins the pump and injectors. If there is no water and the code stays, it is the sensor or wire, and you can drive to a workshop.',
        checks=[u'Drain the fuel filter separator until clean fuel comes out; do it first after rain or after fuel of doubtful quality.',
                u'Inspect the separator sensor connector and wire: a short high (FMI 3) or low (FMI 4).',
                u'Check whether water froze in the tank or line in frost (ice in the line).',
                u'Replace the filter if it is dirty.',
                u'Do not refuel at a suspicious station until the cause is found.'],
        service=u'Water returns: workshop, to clean the tank and lines and check the pump and injectors.',
        faq=[(u'Is MID 128 PID 97 a sensor fault?', u'It can be either: real water (lamp and code) or a faulty sensor circuit (FMI 3, 4). Start by draining the separator.'),
             (u'What happens if I do not drain the water?', u'Water destroys the lubrication of the fuel system and leads to pump and injector repair.')]))

add(slug='mid-128-sid-1-6', mid=128, kind='SID', num='1-6', label='SID 1-6', fmis=[3, 5, 7, 12], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'форсунки цилиндров 1-6', nm_en=u'injectors of cylinders 1-6',
    title_ru=u'MID 128 SID 1-6: форсунка цилиндра — FMI 3, 5, 7, 12',
    title_en=u'MID 128 SID 1-6: injector cylinder 1-6 - FMI 3, 5, 7, 12',
    ru=dict(
        short=u'SID 1–6 по SAE J1587 — форсунки цилиндров №1–№6 (Injector Cylinder). MID 128 — двигатель. Номер SID равен номеру цилиндра. По Volvo: FMI 3 — замыкание на плюс низкой стороны, 5 — обрыв цепи, 7 — механическая часть не отвечает, 12 — слишком большое сопротивление.',
        badge=u'Ехать осторожно, недалеко', verdict=u'С одним отказавшим цилиндром двигатель работает неровно и со сниженной мощностью, остальные цилиндры нагружаются сильнее. Ехать можно недалеко, без нагрузки, до сервиса. При вибрации, стуке или дыме — остановиться.',
        checks=[u'Определите цилиндр: номер SID — номер цилиндра (SID 3 — цилиндр 3).',
                u'Осмотрите разъём форсунки (или насос-форсунки) и жгут на клапанной крышке: окисление, масло в разъёме, перетёртые провода.',
                u'FMI 3 и 5: замыкание или обрыв цепи форсунки; FMI 12: слишком большое сопротивление (плохой контакт или сама форсунка).',
                u'FMI 7: форсунка не отвечает механически — клапан или привод; проверка в сервисе.',
                u'Не пытайтесь заводить двигатель многократно при стуке: можно повредить поршень.'],
        service=u'Любой код форсунки подтверждается в сервисе: замер сопротивления, тест отключением цилиндра, замена форсунки.',
        faq=[(u'Как понять, какой цилиндр по SID?', u'SID 1 — цилиндр 1, SID 2 — цилиндр 2 и так далее до SID 6.'),
             (u'Можно ли доехать с кодом форсунки?', u'Обычно да, недалеко и с малой нагрузкой, пока нет сильной тряски и дыма.')]),
    en=dict(
        short=u'SID 1-6 in SAE J1587 are the injectors of cylinders 1-6 (Injector Cylinder). MID 128 is the engine. The SID number equals the cylinder number. Volvo: FMI 3 is low side shorted to battery, 5 is an open circuit, 7 is the mechanical part not responding, 12 is too high resistance.',
        badge=u'Drive carefully, only a short way', verdict=u'With one failed cylinder the engine runs rough with reduced power, and the other cylinders work harder. You can drive a short way, without load, to a workshop. Stop for vibration, knocking or smoke.',
        checks=[u'Identify the cylinder: the SID number is the cylinder number (SID 3 is cylinder 3).',
                u'Inspect the injector (or unit injector) connector and the harness under the valve cover: corrosion, oil in the connector, chafed wires.',
                u'FMI 3 and 5: a short or an open circuit in the injector circuit; FMI 12: too high resistance (a poor contact or the injector itself).',
                u'FMI 7: the injector does not respond mechanically; the valve or drive; test in a workshop.',
                u'Do not crank the engine repeatedly if it knocks: you can damage a piston.'],
        service=u'Any injector code is confirmed in a workshop: resistance measurement, cylinder cut-out test, injector replacement.',
        faq=[(u'How do I tell the cylinder from the SID?', u'SID 1 is cylinder 1, SID 2 is cylinder 2 and so on up to SID 6.'),
             (u'Can I drive with an injector code?', u'Usually yes, a short way at light load, unless there is heavy shaking or smoke.')]))

add(slug='mid-128-sid-22', mid=128, kind='SID', num='22', label='SID 22', fmis=[2, 3, 8], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'датчик оборотов (маховик, Timing Sensor)', nm_en=u'engine speed (flywheel) sensor, timing sensor',
    title_ru=u'MID 128 SID 22: датчик оборотов на маховике — FMI 2, 3, 8',
    title_en=u'MID 128 SID 22: flywheel speed sensor - FMI 2, 3, 8',
    ru=dict(
        short=u'SID 22 по SAE J1587 — датчик синхронизации (Timing Sensor); у Volvo — частота вращения, датчик на маховике. MID 128 — двигатель. Таблица Volvo: FMI 2, 3, 8.',
        badge=u'Ехать осторожно', verdict=u'Блок двигателя может использовать второй датчик (распредвал) и продолжать работу, но двигатель может не завестись заново. Ехать можно до сервиса; не глушите двигатель без необходимости.',
        checks=[u'Осмотрите разъём датчика на картере маховика, провод и экран провода: часто там протирается или попадает масло.',
                u'Проверьте зазор и крепление датчика, металлическую стружку на торце.',
                u'FMI 8: неверная частота — загрязнён датчик или повреждены зубья маховика.',
                u'FMI 3: замыкание на плюс; FMI 2: нестабильный сигнал.',
                u'Сравните с кодом датчика распредвала SID 21.'],
        service=u'Двигатель с перебоями, не заводится или глохнет — сервис. Замена датчика обычно проста, но сначала проверка проводки.',
        faq=[(u'Что произойдёт, если откажет датчик оборотов?', u'Блок двигателя может работать по датчику распредвала, но при пропадании обоих двигатель остановится и не заведётся.'),
             (u'SID 22 и SID 21 — одно и то же?', u'Нет: SID 21 — положение двигателя (распредвал), SID 22 — синхронизация по маховику.')]),
    en=dict(
        short=u'SID 22 in SAE J1587 is the timing sensor; at Volvo it is the engine speed sensor on the flywheel. MID 128 is the engine. Volvo table: FMI 2, 3, 8.',
        badge=u'Drive carefully', verdict=u'The engine ECU may use the second sensor (camshaft) and keep running, but the engine may not restart. You can drive to a workshop; do not shut the engine down unless you must.',
        checks=[u'Inspect the sensor connector on the flywheel housing, the wire and its shield: oil gets in and it chafes there.',
                u'Check the sensor gap and mounting and metal swarf on its tip.',
                u'FMI 8: abnormal frequency; the sensor is dirty or the flywheel teeth are damaged.',
                u'FMI 3: short to positive; FMI 2: an unstable signal.',
                u'Compare with the camshaft sensor code SID 21.'],
        service=u'Misfire, no start or stalling: workshop. Replacing the sensor is usually simple, but check the wiring first.',
        faq=[(u'What happens if the speed sensor fails?', u'The engine ECU may run on the camshaft sensor, but if both drop out the engine stops and will not start.'),
             (u'Are SID 22 and SID 21 the same?', u'No: SID 21 is engine position (camshaft), SID 22 is timing from the flywheel.')]))

add(slug='mid-128-sid-21', mid=128, kind='SID', num='21', label='SID 21', fmis=[3, 8], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'датчик положения двигателя (распредвал)', nm_en=u'engine position (camshaft) sensor',
    title_ru=u'MID 128 SID 21: датчик распредвала — FMI 3 и 8, ехать ли',
    title_en=u'MID 128 SID 21: camshaft position sensor - FMI 3 and 8',
    ru=dict(
        short=u'SID 21 по SAE J1587 — датчик положения двигателя (Engine Position Sensor); у Volvo — датчик распредвала. MID 128 — двигатель. Таблица Volvo: FMI 3 и 8.',
        badge=u'Ехать осторожно', verdict=u'Двигатель обычно работает по датчику маховика, но запуск может стать долгим. Ехать можно до сервиса без нужды не глуша двигатель; при потере и датчика маховика двигатель встанет.',
        checks=[u'Осмотрите разъём и провод датчика на корпусе у распредвала: масло, окисление, перетёртость.',
                u'Проверьте крепление и зазор датчика.',
                u'FMI 3: замыкание на плюс; FMI 8: неверная частота — грязь на датчике, повреждение зуба распределительной шестерни.',
                u'Посмотрите код датчика маховика SID 22: два кода сразу — общий жгут или питание датчиков.',
                u'Проверьте питание датчиков (5 В): SID 232.'],
        service=u'Двигатель долго заводится, теряет мощность или глохнет — сервис.',
        faq=[(u'Можно ли ехать с MID 128 SID 21?', u'Обычно да, до сервиса. Но при отказе второго датчика двигатель остановится.'),
             (u'Чем SID 21 отличается от SID 22?', u'SID 21 — положение по распредвалу, SID 22 — синхронизация по маховику; блок использует оба.')]),
    en=dict(
        short=u'SID 21 in SAE J1587 is the engine position sensor; at Volvo it is the camshaft sensor. MID 128 is the engine. Volvo table: FMI 3 and 8.',
        badge=u'Drive carefully', verdict=u'The engine usually runs on the flywheel sensor, but starting can become slow. You can drive to a workshop, avoiding shutting down; if the flywheel sensor also drops out, the engine stops.',
        checks=[u'Inspect the sensor connector and wire at the camshaft housing: oil, corrosion, chafing.',
                u'Check the sensor mounting and gap.',
                u'FMI 3: short to positive; FMI 8: abnormal frequency, dirt on the sensor or a damaged gear tooth.',
                u'Look at the flywheel sensor code SID 22: two codes together mean a shared harness or sensor supply.',
                u'Check the sensor supply (5 V): SID 232.'],
        service=u'The engine is slow to start, loses power or stalls: workshop.',
        faq=[(u'Can I drive with MID 128 SID 21?', u'Usually yes, to a workshop. If the second sensor fails the engine stops.'),
             (u'How does SID 21 differ from SID 22?', u'SID 21 is position from the camshaft, SID 22 is timing from the flywheel; the ECU uses both.')]))

add(slug='mid-128-sid-254', mid=128, kind='SID', num='254', label='SID 254', fmis=[3, 8, 12], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'блок управления двигателем (EECU)', nm_en=u'engine electronic control unit (EECU)',
    title_ru=u'MID 128 SID 254: блок управления двигателем — FMI 3, 8, 12',
    title_en=u'MID 128 SID 254: engine control unit fault - FMI 3, 8, 12',
    ru=dict(
        short=u'SID 254 по SAE J1587 — «контроллер №1» (Controller #1); у Volvo — электронный блок управления двигателем (EECU). MID 128 — двигатель. Таблица Volvo: FMI 3, 8, 12.',
        badge=u'Ехать осторожно, лучше не ехать', verdict=u'Если блок двигателя нестабилен, возможны потеря мощности и внезапная остановка двигателя. Если двигатель работает ровно, ехать можно до ближайшего сервиса; при перебоях — остановиться.',
        checks=[u'Проверьте аккумулятор, клеммы и массу двигателя: просадка питания блока даёт такие коды.',
                u'Осмотрите предохранители и реле питания блока.',
                u'Откройте разъёмы блока двигателя: вода, окисление, согнутые контакты.',
                u'FMI 12 — неисправен сам блок или компонент; FMI 3 — напряжение выше нормы; FMI 8 — неверная частота сигнала.',
                u'Не стирайте код, не проверив питание: он вернётся.'],
        service=u'Код остаётся после проверки питания и разъёмов — диагностика и, возможно, перепрошивка или замена блока в сервисе.',
        faq=[(u'MID 128 SID 254 — блок двигателя сломан?', u'Сначала питание и разъёмы: большинство «отказов» блока — это просадка или плохая масса.'),
             (u'Можно ли менять блок самому?', u'Новый блок нужно прописать под машину (VIN, параметры); без сервисного оборудования это не делают.')]),
    en=dict(
        short=u'SID 254 in SAE J1587 is "Controller #1"; at Volvo it is the engine electronic control unit (EECU). MID 128 is the engine. Volvo table: FMI 3, 8, 12.',
        badge=u'Drive carefully, better not at all', verdict=u'If the engine ECU is unstable, power loss and a sudden engine stop are possible. If the engine runs smoothly you can drive to the nearest workshop; with misfires, stop.',
        checks=[u'Check the battery, terminals and engine ground: a supply dip gives these codes.',
                u'Inspect the fuses and the ECU supply relays.',
                u'Open the ECU connectors: water, corrosion, bent pins.',
                u'FMI 12 is a bad unit or component; FMI 3 is voltage above normal; FMI 8 is an abnormal signal frequency.',
                u'Do not clear the code without checking supply: it will return.'],
        service=u'The code stays after the supply and connector check: diagnosis and possibly reflashing or replacing the unit in a workshop.',
        faq=[(u'Is the engine ECU broken with MID 128 SID 254?', u'Check supply and connectors first: most unit "failures" are a supply dip or a poor ground.'),
             (u'Can I replace the unit myself?', u'A new unit must be programmed to the truck (VIN, parameters); it is not done without workshop equipment.')]))

add(slug='mid-128-sid-253', mid=128, kind='SID', num='253', label='SID 253', fmis=[2, 12, 13], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'память калибровок блока двигателя', nm_en=u'engine ECU calibration memory',
    title_ru=u'MID 128 SID 253: память блока двигателя — FMI 2, 12, 13',
    title_en=u'MID 128 SID 253: engine ECU calibration memory - FMI 2, 12, 13',
    ru=dict(
        short=u'SID 253 по SAE J1587 — память калибровок (Calibration Memory); у Volvo — память данных EEPROM. MID 128 — двигатель. Таблица Volvo: FMI 2, 12, 13.',
        badge=u'Ехать осторожно', verdict=u'Это внутренняя ошибка памяти блока, а не датчик или провод. Двигатель может работать на запасных настройках и с потерей мощности. Ехать можно до сервиса, если работает ровно.',
        checks=[u'Проверьте аккумулятор и напряжение: сбой записи памяти бывает при просадке питания при пуске.',
                u'Сотрите код и посмотрите, вернётся ли он.',
                u'Проверьте массу блока двигателя.',
                u'FMI 13 — вне калибровки: блок нужно перенастроить или перепрошить в сервисе.',
                u'Нет ли вместе с ним SID 254 (блок).'],
        service=u'Код возвращается — сервис: перепрошивка, запись параметров, при FMI 12 — замена блока.',
        faq=[(u'Можно ли исправить SID 253 самому?', u'Нет: калибровки записываются только сервисным оборудованием.'),
             (u'Почему код появляется после разряженной батареи?', u'Просадка напряжения при пуске могла прервать запись в память.')]),
    en=dict(
        short=u'SID 253 in SAE J1587 is calibration memory; at Volvo it is the EEPROM data set memory. MID 128 is the engine. Volvo table: FMI 2, 12, 13.',
        badge=u'Drive carefully', verdict=u'This is an internal memory error of the unit, not a sensor or wire. The engine may run on fallback settings with some power loss. You can drive to a workshop if it runs smoothly.',
        checks=[u'Check the battery and voltage: a memory write error can come from a supply dip on cranking.',
                u'Clear the code and see whether it returns.',
                u'Check the engine ECU ground.',
                u'FMI 13 is out of calibration: the unit must be reconfigured or reflashed in a workshop.',
                u'Look for SID 254 (the unit) alongside it.'],
        service=u'The code returns: workshop, for reflashing, writing parameters or, with FMI 12, replacing the unit.',
        faq=[(u'Can I fix SID 253 myself?', u'No: calibrations are written only with workshop equipment.'),
             (u'Why does the code appear after a flat battery?', u'A voltage dip on cranking may have interrupted a memory write.')]))

# ---- MID 130 ---------------------------------------------------------------------------------------------------
add(slug='mid-130-sid-250', mid=130, kind='SID', num='250', label='SID 250', fmis=[9], lvl='calm',
    src=['sae', 'volvo'], nm_ru=u'канал J1587/J1708 у коробки передач', nm_en=u'J1587/J1708 link at the transmission',
    title_ru=u'MID 130 SID 250 FMI 9: связь J1587 коробки передач',
    title_en=u'MID 130 SID 250 FMI 9: transmission J1587 link fault',
    ru=dict(
        short=u'SID 250 по SAE J1587 — канал данных SAE J1708 (J1587). MID 130 — коробка передач. Таблица Volvo даёт FMI 9: по Volvo «ошибка связи», по стандарту SAE — неверная частота обновления данных.',
        badge=u'Ехать можно', verdict=u'Это запасной, медленный канал; основная связь идёт по J1939. Ехать можно, если нет других кодов связи и коробка работает нормально.',
        checks=[u'Проверьте разъём диагностики и разъём ЭБУ коробки: влага и окисление.',
                u'Осмотрите двухпроводный жгут J1708 (витая пара) на обрыв и замыкание.',
                u'Посмотрите, нет ли одновременно MID 130 SID 231 (J1939): тогда оба канала нестабильны, причина общая.',
                u'Сотрите код и проверьте, вернётся ли он.'],
        service=u'Код возвращается или связь пропадает вместе с J1939 — диагностика шин в сервисе.',
        faq=[(u'Чем J1708 отличается от J1939?', u'J1708 (с протоколом J1587) — старая медленная шина, J1939 — быстрая CAN. На многих машинах обе шины идут рядом, и J1708 служит запасной.'),
             (u'Почему у FMI 9 два толкования?', u'В стандарте SAE FMI 9 — неверная частота обновления данных, в таблицах Volvo — ошибка связи. По смыслу это потеря сообщений.')]),
    en=dict(
        short=u'SID 250 in SAE J1587 is the SAE J1708 (J1587) data link. MID 130 is the transmission. The Volvo table gives FMI 9: Volvo calls it a "communication fault", the SAE standard calls it an abnormal update rate.',
        badge=u'You can drive', verdict=u'This is the backup, slow link; the main link runs on J1939. You can drive if there are no other link codes and the gearbox works normally.',
        checks=[u'Check the diagnostic connector and the transmission ECU connector: moisture and corrosion.',
                u'Inspect the two-wire J1708 harness (twisted pair) for opens and shorts.',
                u'See whether MID 130 SID 231 (J1939) appears at the same time: then both links are unstable and the cause is common.',
                u'Clear the code and see whether it returns.'],
        service=u'The code returns or the link drops together with J1939: bus diagnosis in a workshop.',
        faq=[(u'How does J1708 differ from J1939?', u'J1708 (with the J1587 protocol) is the older slow bus, J1939 is fast CAN. On many trucks both run side by side and J1708 serves as the backup.'),
             (u'Why does FMI 9 have two readings?', u'In the SAE standard FMI 9 is an abnormal update rate; in Volvo tables it is a communication fault. In practice it is lost messages.')]))

add(slug='mid-130-pid-177', mid=130, kind='PID', num='177', label='PID 177', fmis=[0, 4, 5], lvl='now',
    src=['sae', 'volvo'], nm_ru=u'температура масла коробки передач', nm_en=u'transmission oil temperature',
    title_ru=u'MID 130 PID 177: температура масла коробки — FMI 0, 4, 5',
    title_en=u'MID 130 PID 177: transmission oil temperature - FMI 0, 4, 5',
    ru=dict(
        short=u'PID 177 по SAE J1587 — температура масла коробки передач (Transmission #1 Oil Temperature). MID 130 — коробка. Таблица Volvo: FMI 0 (выше нормы), 4 и 5 (цепь датчика).',
        badge=u'FMI 0: остановиться', verdict=u'FMI 0 — масло в коробке перегрето: остановитесь, дайте коробке остыть на нейтрали, проверьте уровень. Дальше ехать с перегревом нельзя. FMI 4 и 5 — датчик или цепь: ехать можно осторожно.',
        checks=[u'Остановитесь на ровной площадке, дайте двигателю поработать на холостом ходу в нейтрали несколько минут и заглушите.',
                u'Проверьте уровень масла в коробке и нет ли подтёков.',
                u'Не работали ли вы на высокой нагрузке, с прицепом в гору, с пробуксовкой сцепления.',
                u'FMI 4 и 5: разъём и провод датчика температуры, замыкание на массу и обрыв.',
                u'Не ставьте рядом коды перегрева двигателя: общий перегрев влияет и на коробку.'],
        service=u'Масло перегревается снова — сервис: уровень, масло, радиатор масла коробки, пробуксовка.',
        faq=[(u'Что значит MID 130 PID 177 FMI 0?', u'Температура масла коробки выше рабочего диапазона.'),
             (u'Можно ли ехать дальше, дав остыть?', u'Да, но не продолжайте работу на той же нагрузке, пока причина не найдена.')]),
    en=dict(
        short=u'PID 177 in SAE J1587 is transmission oil temperature (Transmission #1 Oil Temperature). MID 130 is the gearbox. Volvo table: FMI 0 (above normal), 4 and 5 (sensor circuit).',
        badge=u'FMI 0: stop', verdict=u'FMI 0 means the gearbox oil is overheated: stop, let it cool in neutral and check the level. Do not drive on while overheating. FMI 4 and 5 are the sensor or circuit: you can drive carefully.',
        checks=[u'Stop on level ground, idle in neutral for a few minutes and shut down.',
                u'Check the gearbox oil level and look for leaks.',
                u'Think whether you worked under heavy load, climbing with a trailer, or with clutch slip.',
                u'FMI 4 and 5: the temperature sensor connector and wire, short to ground and open circuit.',
                u'Check whether engine overheating codes are present: general overheating also affects the gearbox.'],
        service=u'The oil overheats again: workshop, for level, oil, the gearbox oil cooler and clutch slip.',
        faq=[(u'What does MID 130 PID 177 FMI 0 mean?', u'Gearbox oil temperature is above the operating range.'),
             (u'Can I continue after it cools?', u'Yes, but do not continue the same load until the cause is found.')]))

add(slug='mid-130-pid-160', mid=130, kind='PID', num='160', label='PID 160', fmis=[1, 2, 3, 4, 5], lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'частота вращения главного вала коробки', nm_en=u'main shaft speed',
    title_ru=u'MID 130 PID 160: скорость главного вала — FMI 1, 2, 3, 4, 5',
    title_en=u'MID 130 PID 160: gearbox main shaft speed - FMI 1, 2, 3, 4, 5',
    ru=dict(
        short=u'PID 160 по SAE J1587 — частота вращения главного вала (Main Shaft Speed). MID 130 — коробка. Таблица Volvo: FMI 1, 2, 3, 4, 5.',
        badge=u'Ехать осторожно', verdict=u'Блок коробки без этого датчика может переключать хуже, перейти в аварийный режим или потерять часть передач. Ехать можно осторожно, не нагружая коробку, до сервиса.',
        checks=[u'Осмотрите разъём датчика на корпусе коробки и провод: масло, окисление, перетёртость, металлическая стружка на датчике.',
                u'FMI 3, 4, 5: замыкание на плюс, на массу, обрыв.',
                u'FMI 1 и 2: сигнал ниже нормы или нестабильный: зазор датчика, повреждённое зубчатое колесо.',
                u'Проверьте уровень масла в коробке.',
                u'Сравните с датчиком входного вала PID 161.'],
        service=u'Коробка не переключается нормально — сервис: замена датчика и проверка проводки.',
        faq=[(u'Работает ли коробка с кодом по PID 160?', u'Как правило, да, но со сбоями переключения; полностью аварийный режим возможен.'),
             (u'PID 160 и PID 161 — в чём разница?', u'PID 160 — главный вал, PID 161 — входной вал; блок сравнивает их для определения проскальзывания и передачи.')]),
    en=dict(
        short=u'PID 160 in SAE J1587 is main shaft speed. MID 130 is the gearbox. Volvo table: FMI 1, 2, 3, 4, 5.',
        badge=u'Drive carefully', verdict=u'Without this sensor the gearbox ECU may shift poorly, go into limp mode or lose some gears. You can drive carefully, without stressing the gearbox, to a workshop.',
        checks=[u'Inspect the sensor connector on the gearbox housing and its wire: oil, corrosion, chafing, metal swarf on the sensor.',
                u'FMI 3, 4, 5: short to positive, short to ground, open circuit.',
                u'FMI 1 and 2: signal below normal or unstable: the sensor gap, or a damaged tone wheel.',
                u'Check the gearbox oil level.',
                u'Compare with the input shaft sensor PID 161.'],
        service=u'The gearbox does not shift normally: workshop, to replace the sensor and check the wiring.',
        faq=[(u'Does the gearbox work with a PID 160 code?', u'As a rule yes, but with shift faults; full limp mode is possible.'),
             (u'PID 160 or PID 161: what is the difference?', u'PID 160 is the main shaft, PID 161 the input shaft; the ECU compares them to detect slip and gear.')]))

# ---- MID 136 ---------------------------------------------------------------------------------------------------
add(slug='mid-136-sid-1-6', mid=136, kind='SID', num='1-6', label='SID 1-6', fmis=None, lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'датчики скорости колёс ABS', nm_en=u'ABS wheel speed sensors',
    title_ru=u'MID 136 SID 1-6: датчик скорости колеса ABS — какой и что делать',
    title_en=u'MID 136 SID 1-6: ABS wheel speed sensor - which wheel, what to do',
    ru=dict(
        short=u'MID 136 — тормоза тягача (ЭБУ ABS). По таблице Volvo SID 1–6 — датчики скорости колёс ABS: 1 и 2 — передняя ось слева и справа, 3 и 4 — первый ведущий мост (передние колёса моста) слева и справа, 5 и 6 — задние колёса моста слева и справа. '
              u'FMI по этим строкам в нашем источнике не приведены: значение FMI смотрите по общей таблице ниже (чаще всего 3, 4, 5 — цепь датчика).',
        badge=u'Ехать осторожно, не быстро', verdict=u'Тормоза работают, но ABS на этом колесе, скорее всего, отключена: колесо может заблокироваться при резком торможении. Ехать можно медленно, с большой дистанцией, без прицепа и скользкой дороги, до сервиса.',
        checks=[u'По номеру SID определите колесо (SID 1 — передняя ось слева, SID 2 — справа и так далее по таблице выше).',
                u'Осмотрите разъём датчика и провод у ступицы: частое место обрыва — перетёртый провод, окисление, масло.',
                u'Проверьте, не загрязнён ли датчик и зубчатое кольцо (реактор): металлическая пыль, трещина кольца.',
                u'Проверьте зазор датчика и его посадку во втулке.',
                u'После ремонта сотрите код и проедьте: лампа ABS должна погаснуть после начала движения.'],
        service=u'Лампа ABS не гаснет после чистки и проверки разъёма — сервис: замена датчика, ремонт жгута.',
        faq=[(u'Как узнать колесо по MID 136 SID?', u'SID 1 — передняя ось слева, SID 2 — справа; следующие номера — колёса ведущих мостов (3 и 4, 5 и 6) по таблице Volvo.'),
             (u'Можно ли ехать без ABS?', u'Рабочие тормоза остаются, но блокировка колёс не контролируется. Нельзя ехать быстро, с прицепом и на скользкой дороге.')]),
    en=dict(
        short=u'MID 136 is the power unit brakes (ABS ECU). In the Volvo table SID 1-6 are the ABS wheel speed sensors: 1 and 2 front axle left and right, 3 and 4 front wheels of the first drive axle left and right, 5 and 6 rear wheels of the axle left and right. '
              u'The FMIs for these rows are not given in our source: read the FMI from the general table below (most often 3, 4, 5, the sensor circuit).',
        badge=u'Drive carefully and slowly', verdict=u'The brakes work, but ABS on this wheel is probably off: the wheel may lock under hard braking. You can drive slowly with a large gap, without a trailer and not on slippery roads, to a workshop.',
        checks=[u'Identify the wheel from the SID (SID 1 is front axle left, SID 2 right, and so on per the table above).',
                u'Inspect the sensor connector and wire at the hub: a chafed wire, corrosion or oil is the usual break point.',
                u'Check whether the sensor and the tone ring are dirty: metal dust, a cracked ring.',
                u'Check the sensor gap and its seating in the bushing.',
                u'After repair clear the code and drive: the ABS lamp should go out after you start moving.'],
        service=u'The ABS lamp stays on after cleaning and the connector check: workshop, to replace the sensor or repair the harness.',
        faq=[(u'How do I find the wheel from MID 136 SID?', u'SID 1 is front axle left, SID 2 right; the next numbers are the drive axle wheels (3 and 4, 5 and 6) per the Volvo table.'),
             (u'Can I drive without ABS?', u'The service brakes remain, but wheel lock is not controlled. Do not drive fast, with a trailer or on slippery roads.')]))

add(slug='mid-136-sid-254', mid=136, kind='SID', num='254', label='SID 254', fmis=None, lvl='warn',
    src=['sae', 'volvo'], nm_ru=u'блок ABS не отвечает', nm_en=u'ABS ECU not communicating',
    title_ru=u'MID 136 SID 254: ЭБУ ABS не отвечает — можно ли ехать',
    title_en=u'MID 136 SID 254: ABS ECU not communicating - can you drive',
    ru=dict(
        short=u'MID 136 — тормоза тягача (ЭБУ ABS). SID 254 по SAE J1587 — «контроллер №1»; в таблице Volvo строка называется «ECU Not Communicating» (блок не отвечает). FMI по строке в нашем источнике не приведены.',
        badge=u'Ехать осторожно, не быстро', verdict=u'Блок ABS не выходит на связь: ABS и связанные функции, скорее всего, не работают. Рабочие тормоза остаются. Ехать можно медленно и с запасом дистанции, без прицепа на скользкой дороге, и сразу в сервис.',
        checks=[u'Проверьте предохранитель и реле питания блока ABS, клеммы аккумулятора, массу.',
                u'Осмотрите разъём блока ABS и жгут у него: влага, окисление.',
                u'Проверьте, нет ли кода SID 251 (питание) вместе с ним; если есть, питание блока ниже нормы.',
                u'Проверьте, нет ли кода MID 136 SID 231: связь по J1939 может быть нарушена отдельно.',
                u'Сотрите код и убедитесь, что лампа ABS гаснет после начала движения.'],
        service=u'Блок не появляется на связи после проверки питания и разъёма — сервис: диагностика, замена блока ABS.',
        faq=[(u'Что значит MID 136 SID 254?', u'Блок ABS не отвечает по диагностической связи: нет питания, плохой разъём или сам блок.'),
             (u'Будут ли работать тормоза?', u'Обычная тормозная система да, но ABS нет; не рассчитывайте на неё.')]),
    en=dict(
        short=u'MID 136 is the power unit brakes (ABS ECU). SID 254 in SAE J1587 is "Controller #1"; in the Volvo table the row is called "ECU Not Communicating". The FMIs for this row are not given in our source.',
        badge=u'Drive carefully and slowly', verdict=u'The ABS unit does not respond: ABS and related functions are probably off. The service brakes remain. You can drive slowly with a large gap, without a trailer on slippery roads, and go to a workshop at once.',
        checks=[u'Check the ABS ECU fuse and supply relay, the battery terminals and the ground.',
                u'Inspect the ABS ECU connector and the harness next to it: moisture, corrosion.',
                u'Look for SID 251 (supply) with it; if it is there, the unit supply is below normal.',
                u'Look for MID 136 SID 231: the J1939 link can fail separately.',
                u'Clear the code and make sure the ABS lamp goes out after you start moving.'],
        service=u'The unit does not appear on the link after the supply and connector check: workshop, for diagnosis and replacing the ABS unit.',
        faq=[(u'What does MID 136 SID 254 mean?', u'The ABS unit does not answer on diagnostic communication: no supply, a bad connector or the unit itself.'),
             (u'Will the brakes work?', u'The ordinary brake system yes, but ABS not; do not rely on it.')]))

# ---- MID 140 ---------------------------------------------------------------------------------------------------
add(slug='mid-140-sid-250', mid=140, kind='SID', num='250', label='SID 250', fmis=[3, 4, 9, 12], lvl='calm',
    src=['sae', 'volvo'], nm_ru=u'канал J1587/J1708 у приборной панели', nm_en=u'J1587/J1708 link at the instrument cluster',
    title_ru=u'MID 140 SID 250: связь J1587/J1708 панели — FMI 3, 4, 9, 12',
    title_en=u'MID 140 SID 250: cluster J1587/J1708 link - FMI 3, 4, 9, 12',
    ru=dict(
        short=u'SID 250 по SAE J1587 — канал данных J1708/J1587. MID 140 — приборная панель. Таблица Volvo: FMI 3 и 4 (замыкание на плюс, на массу), 9 (ошибка связи), 12 (неисправен блок).',
        badge=u'Ехать можно', verdict=u'Это запасная шина; основная работает по J1939. Ехать можно, если панель показывает всё и других кодов связи нет. Если панель погасла или показания пропали — проверьте давление и температуру другими способами и вызывайте сервис.',
        checks=[u'FMI 3 и 4: замыкание линии J1708 на плюс или на массу: осмотрите двухпроводную линию и разъём панели.',
                u'FMI 9: потеря сообщений по шине: проверьте разъёмы блоков, включая диагностический разъём.',
                u'FMI 12: неисправен блок на шине или сама панель; отключайте дополнительные устройства, подключённые к диагностическому разъёму (трекеры, регистраторы): они часто «роняют» J1708.',
                u'Проверьте питание панели и массу.',
                u'Сравните с MID 140 SID 231.'],
        service=u'Код не уходит после отключения дополнительных устройств — диагностика в сервисе.',
        faq=[(u'Почему J1708 «падает» после установки трекера?', u'Устройства, подключённые к шине J1708/J1587 через диагностический разъём, нагружают её или замыкают; отключите устройство и проверьте.'),
             (u'Опасен ли код для движения?', u'Сам по себе нет, если J1939 работает.')]),
    en=dict(
        short=u'SID 250 in SAE J1587 is the J1708/J1587 data link. MID 140 is the instrument cluster. Volvo table: FMI 3 and 4 (short high, short low), 9 (communication fault), 12 (bad unit).',
        badge=u'You can drive', verdict=u'This is the backup bus; the main one runs on J1939. You can drive if the cluster shows everything and no other link codes exist. If the cluster goes dark or readings drop out, check pressure and temperature by other means and call a workshop.',
        checks=[u'FMI 3 and 4: the J1708 line shorted to positive or ground: inspect the two-wire line and the cluster connector.',
                u'FMI 9: messages lost on the bus: check the unit connectors, including the diagnostic connector.',
                u'FMI 12: a bad unit on the bus or the cluster itself; disconnect add-on devices on the diagnostic connector (trackers, recorders): they often pull J1708 down.',
                u'Check the cluster supply and ground.',
                u'Compare with MID 140 SID 231.'],
        service=u'The code stays after unplugging add-on devices: diagnosis in a workshop.',
        faq=[(u'Why does J1708 fail after a tracker is installed?', u'Devices connected to J1708/J1587 through the diagnostic connector load or short the bus; unplug the device and check.'),
             (u'Is the code dangerous for driving?', u'By itself no, if J1939 works.')]))

add(slug='mid-140-pid-96', mid=140, kind='PID', num='96', label='PID 96', fmis=[3, 4], lvl='calm',
    src=['sae', 'volvo'], nm_ru=u'уровень топлива (датчик в баке)', nm_en=u'fuel level (tank sender)',
    title_ru=u'MID 140 PID 96: датчик уровня топлива — FMI 3 и 4',
    title_en=u'MID 140 PID 96: fuel level sender - FMI 3 and 4',
    ru=dict(
        short=u'PID 96 по SAE J1587 — уровень топлива (Fuel Level). MID 140 — приборная панель. Таблица Volvo: FMI 3 (замыкание на плюс) и FMI 4 (замыкание на массу).',
        badge=u'Ехать можно', verdict=u'Ехать можно: двигатель не зависит от этого датчика. Но показание уровня может быть неверным — следите за пробегом и дозаправляйтесь заранее, чтобы не остаться с пустым баком.',
        checks=[u'FMI 3: замыкание на плюс, обычно обрыв массы датчика: осмотрите разъём и провод датчика в баке.',
                u'FMI 4: замыкание на массу: поиск перетёртого провода на пути от бака к панели.',
                u'Проверьте разъём панели приборов.',
                u'Если показания «прыгают» — датчик в баке или его контакты (поплавок, дорожка).',
                u'Оцените остаток по пробегу и расходу.'],
        service=u'Датчик уровня заменяют вместе с узлом в баке; в сервис — при пустом показании без причины.',
        faq=[(u'Влияет ли неисправный датчик уровня на двигатель?', u'Нет: это только показание на панели.'),
             (u'Почему указатель показывает пустой бак?', u'Замыкание в цепи датчика, плохая масса или неисправный поплавок.')]),
    en=dict(
        short=u'PID 96 in SAE J1587 is fuel level. MID 140 is the instrument cluster. Volvo table: FMI 3 (short high) and FMI 4 (short low).',
        badge=u'You can drive', verdict=u'You can drive: the engine does not depend on this sender. But the level reading may be wrong, so watch mileage and refuel early to avoid an empty tank.',
        checks=[u'FMI 3: shorted high, often an open sender ground: inspect the connector and wire of the tank sender.',
                u'FMI 4: shorted to ground: look for a chafed wire between the tank and the cluster.',
                u'Check the instrument cluster connector.',
                u'If the readings jump, it is the tank sender or its contacts (float, track).',
                u'Estimate the remainder from mileage and consumption.'],
        service=u'The sender is replaced with the tank unit; go to a workshop if the gauge reads empty for no reason.',
        faq=[(u'Does a faulty fuel level sender affect the engine?', u'No: it is only a reading on the cluster.'),
             (u'Why does the gauge show an empty tank?', u'A short in the sender circuit, a poor ground or a faulty float.')]))

# ---- MID 144 ---------------------------------------------------------------------------------------------------
add(slug='mid-144-sid-250', mid=144, kind='SID', num='250', label='SID 250', fmis=[2], lvl='calm',
    src=['sae', 'volvo'], nm_ru=u'канал J1587/J1708 у ЭБУ автомобиля', nm_en=u'J1587/J1708 link at the vehicle ECU',
    title_ru=u'MID 144 SID 250 FMI 2: связь J1587/J1708 ЭБУ автомобиля',
    title_en=u'MID 144 SID 250 FMI 2: vehicle ECU J1587/J1708 link',
    ru=dict(
        short=u'SID 250 по SAE J1587 — канал данных J1708/J1587. MID 144 — ЭБУ автомобиля у Volvo (по стандарту SAE — круиз-контроль). Таблица Volvo: FMI 2 — данные прерывистые или неверные.',
        badge=u'Ехать можно', verdict=u'Запасная шина нестабильна; основная связь по J1939. Ехать можно, если нет кодов J1939 (SID 231) и всё работает.',
        checks=[u'Проверьте разъёмы ЭБУ автомобиля и диагностический разъём.',
                u'Отключите дополнительные устройства на диагностическом разъёме (трекеры, регистраторы) и проверьте, исчезнет ли код.',
                u'Осмотрите линию J1708: обрывы, перетёртость.',
                u'Проверьте массу и питание ЭБУ автомобиля.',
                u'Сравните с MID 144 SID 231.'],
        service=u'Код остаётся без дополнительных устройств — диагностика шины в сервисе.',
        faq=[(u'MID 144 SID 250 FMI 2 опасен?', u'Сам по себе нет: J1708 — запасная шина.'),
             (u'Какие устройства чаще мешают?', u'Трекеры и регистраторы, подключённые к диагностическому разъёму.')]),
    en=dict(
        short=u'SID 250 in SAE J1587 is the J1708/J1587 data link. MID 144 is the vehicle ECU at Volvo (cruise control in the SAE standard). Volvo table: FMI 2, erratic, intermittent or incorrect data.',
        badge=u'You can drive', verdict=u'The backup bus is unstable; the main link runs on J1939. You can drive if there are no J1939 (SID 231) codes and everything works.',
        checks=[u'Check the vehicle ECU connectors and the diagnostic connector.',
                u'Unplug add-on devices on the diagnostic connector (trackers, recorders) and see whether the code goes.',
                u'Inspect the J1708 line: opens, chafing.',
                u'Check ground and supply at the vehicle ECU.',
                u'Compare with MID 144 SID 231.'],
        service=u'The code stays with no add-on devices: bus diagnosis in a workshop.',
        faq=[(u'Is MID 144 SID 250 FMI 2 dangerous?', u'By itself no: J1708 is the backup bus.'),
             (u'Which devices interfere most often?', u'Trackers and recorders connected to the diagnostic connector.')]))

add(slug='mid-144-pid-91', mid=144, kind='PID', num='91', label='PID 91', fmis=[3, 4, 5, 6, 14], lvl='now',
    src=['sae', 'volvo'], nm_ru=u'положение педали акселератора', nm_en=u'accelerator pedal position',
    title_ru=u'MID 144 PID 91: педаль акселератора — FMI 3, 4, 5, 6, 14',
    title_en=u'MID 144 PID 91: accelerator pedal position - FMI 3, 4, 5, 6, 14',
    ru=dict(
        short=u'PID 91 по SAE J1587 — положение педали акселератора в процентах (Percent Accelerator Pedal Position). MID 144 — ЭБУ автомобиля у Volvo. Таблица Volvo: FMI 3, 4, 5, 6, 14.',
        badge=u'Ехать нельзя без проверки', verdict=u'При отказе педали двигатель может остаться на холостых, ограничить обороты или не реагировать на газ: на дороге это опасно. Если педаль даёт рывки или вы не можете поддерживать скорость, не ехать, а звать сервис. При нормальной реакции педали — до сервиса с осторожностью.',
        checks=[u'Проверьте, нормально ли реагирует двигатель на педаль на месте (холостые, плавный набор оборотов).',
                u'Осмотрите разъём педали и провода: окисление, перетёртость, мокрый разъём.',
                u'FMI 3, 4: замыкание на плюс или массу; FMI 5, 6: обрыв или замыкание цепи; FMI 14 — особые указания (смотреть руководство производителя).',
                u'Проверьте питание датчика педали (PPID 73 — второй датчик педали, питание) и массу.',
                u'Проверьте, не мешает ли коврик или предмет ходу педали.'],
        service=u'Реакция педали нестабильна — не ехать: ремонт педали в сервисе.',
        faq=[(u'Почему двигатель на холостых после кода по педали?', u'Блок не доверяет сигналу педали и оставляет холостые, чтобы исключить неуправляемый разгон.'),
             (u'В чём разница между MID 128 PID 91 и MID 144 PID 91?', u'Это одно и то же положение педали, но данные идут от разных блоков: MID 128 — двигатель, MID 144 — ЭБУ автомобиля.')]),
    en=dict(
        short=u'PID 91 in SAE J1587 is percent accelerator pedal position. MID 144 is the vehicle ECU at Volvo. Volvo table: FMI 3, 4, 5, 6, 14.',
        badge=u'Do not drive without a check', verdict=u'With a failed pedal the engine may stay at idle, limit rpm or not respond to the throttle: on the road that is dangerous. If the pedal jerks or you cannot hold speed, do not drive; call a workshop. If the pedal responds normally, drive carefully to a workshop.',
        checks=[u'Check that the engine responds to the pedal while parked (idle, smooth rpm rise).',
                u'Inspect the pedal connector and wires: corrosion, chafing, a wet connector.',
                u'FMI 3, 4: short to positive or ground; FMI 5, 6: open or grounded circuit; FMI 14: special instructions (see the manufacturer manual).',
                u'Check the pedal sensor supply (PPID 73, second pedal sensor supply) and ground.',
                u'Check that a mat or object does not obstruct the pedal travel.'],
        service=u'The pedal response is unstable: do not drive; repair the pedal in a workshop.',
        faq=[(u'Why is the engine at idle after a pedal code?', u'The ECU does not trust the pedal signal and holds idle to rule out uncontrolled acceleration.'),
             (u'How does MID 128 PID 91 differ from MID 144 PID 91?', u'It is the same pedal position, but the data come from different units: MID 128 the engine, MID 144 the vehicle ECU.')]))
