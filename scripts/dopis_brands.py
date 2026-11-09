# -*- coding: utf-8 -*-
# Dopisyvanie 09.11.2026: марки deutz, wabco, allison.
# ru: ключ 'brand:<марка>+' - добавка ПОСЛЕ прежних блоков 'brand:<марка>' (они остаются).
# en: ключ 'brand-en:<марка>' (раньше английских текстов у этих марок не было).

BLOCKS = {

'brand:deutz+': {'tail': [
    (u'Чем коды Deutz отличаются от других марок', [
        u'Двигатели Deutz чаще встречаются на строительной, сельскохозяйственной и складской технике, генераторах и автобусах, а не на магистральных тягачах. '
        u'Поэтому коды приходят не только с лампы грузовика, но и с пульта самой машины. Блок управления EMR (Electronic Motor Regelung, «электронное регулирование двигателя») '
        u'записывает неисправности и в формате J1939 (SPN.FMI через точку), и собственными номерами Deutz выше 516000. Диагностику у производителя делают программой SerDia.',
        u'Это важно при чтении: запись 100.0 - стандартный SPN 100 (давление масла) с FMI 0, а запись 516408.31 - уже внутренний номер Deutz, которого нет в таблицах J1939.',
    ]),
    (u'Как читать FMI в записях Deutz', [
        [u'**FMI 0, 15, 16** - значение выше нормы (0 - самый тяжёлый уровень). Для температуры и давления это перегрев или избыточное давление.',
         u'**FMI 1, 17, 18** - значение ниже нормы (1 - самый тяжёлый).',
         u'**FMI 3 и 4** - напряжение в цепи выше или ниже нормы: чаще всего обрыв или замыкание.',
         u'**FMI 5 и 6** - обрыв цепи и замыкание на массу по току.',
         u'**FMI 2** - недостоверные данные (в записях AdBlue встречается постоянно).',
         u'**FMI 11 и 31** - причина не определена или условие существует: нужен разбор по руководству.'],
        u'Расшифровка FMI дана по SAE J1939-73; страницы Deutz в разделе выше показывают, как формулирует каждую запись завод.',
    ]),
    (u'Типичные причины по убыванию', [
        [u'Разъёмы и жгут: влага и вибрация на внедорожной технике, потёртости о кронштейны.',
         u'Качество реагента и состояние датчиков в системе AdBlue/SCR (коды 3031.2, 4334.2, 516201.11).',
         u'Топливо: вода и загрязнения вызывают пропуски зажигания и ошибки форсунок.',
         u'Масло: уровень, вязкость, датчик давления (код 100.0).',
         u'Питание блока EMR: аккумулятор, масса и клеммы - дают несколько кодов сразу.',
         u'Блок управления - в последнюю очередь.'],
    ]),
    (u'Когда можно ехать (или работать)', [
        u'Записи о критическом давлении или температуре масла (100.0, 175.0) требуют остановки двигателя. Коды цепей датчиков (FMI 3, 4, 5, 6) сами по себе не грозят двигателю, '
        u'но защита по этому параметру перестаёт работать: следите за приборами. Если двигатель дёргается, теряет мощность или горят красные лампы, остановитесь.',
    ]),
    (u'Вопросы и ответы', [
        (u'Что делать, если в записи Deutz номер больше 516000?',
         u'Это собственный номер Deutz, в J1939 его нет. Читайте его по описанию на странице, а точное значение подтверждайте по руководству на свой двигатель.'),
        (u'Код 100.0 и двигатель работает ровно. Можно ли продолжать работу?',
         u'Нет. По странице это критическое давление масла. Остановитесь, проверьте уровень масла и давление манометром.'),
    ]),
]},

'brand:wabco+': {'tail': [
    (u'Как коды WABCO связаны с тем, что вы видите на машине', [
        u'WABCO (с 2020 года часть группы ZF) - один из основных поставщиков тормозной электроники для европейских и многих российских тягачей и прицепов. '
        u'Коды ABS и EBS читаются сканером по CAN. На приборной панели жёлтая лампа ABS говорит, что антиблокировка отключена полностью или частично; '
        u'прицеп своим блоком подаёт отдельную лампу через разъём ISO 7638.',
        u'Обычные тормоза при этом сохраняются: пневматика работает независимо от электроники. Исчезает только защита от блокировки и связанные функции (ASR, ESC).',
    ]),
    (u'Типичные значения FMI в кодах WABCO', [
        [u'**FMI 3 и 4** - напряжение в цепи выше или ниже нормы: датчик, клапан или питание.',
         u'**FMI 5 и 6** - обрыв или замыкание на массу в цепи клапана-модулятора.',
         u'**FMI 1, 2, 7, 8, 10** - у датчика колеса: слабый, неровный или пропадающий сигнал; ищите зазор, зубчатое кольцо и подшипник ступицы.',
         u'**FMI 9** - пропала связь по CAN с другим блоком.',
         u'**FMI 12** - неисправное интеллектуальное устройство: сам блок. К этому выводу приходят в последнюю очередь.'],
    ]),
    (u'Причины по убыванию', [
        [u'Датчик колеса и его кабель, особенно на передней оси, где кабель гнётся при поворотах руля.',
         u'Зубчатое кольцо: грязь, повреждённые зубья, ржавчина.',
         u'Разъёмы модуляторов и жгут вдоль рамы: окисление, потёртость, влага.',
         u'Питание и масса блока: просадка напряжения даёт несколько кодов разных осей.',
         u'Разъём ISO 7638 между тягачом и прицепом: окисленные контакты дают «мнимые» неисправности колеса.',
         u'Сам модулятор или блок - после всего.'],
    ]),
    (u'Порядок проверки (кратко)', [
        u'1. Считайте коды и кадр стоп-данных. 2. Проверьте питание и массу. 3. Осмотрите разъёмы, начиная с ISO 7638 на прицепе. 4. Мерьте сопротивление датчика колеса: для датчика WABCO порядок 0,9-1,3 кОм, '
        u'сравнивайте с датчиком того же моста. 5. Мерьте катушку модулятора и прозвоните провода. 6. Меняйте деталь только после этого.',
    ]),
    (u'Вопросы и ответы', [
        (u'Лампа ABS горит. Можно ли ехать?',
         u'Тормоза работают, но без защиты от блокировки. Ехать можно осторожно и недолго, затем устранить.'),
        (u'Код есть, а датчик и клапаны целые. Что ещё?',
         u'Питание и масса блока, разъём ISO 7638 и сеть CAN. Сначала это, затем блок.'),
        (u'Какая разница между WABCO ABS и EBS?',
         u'ABS только не даёт колёсам блокироваться. EBS ещё управляет торможением электроникой и обменивается данными с прицепом по CAN.'),
    ]),
]},

'brand:allison+': {'tail': [
    (u'Что важно знать об автоматической коробке Allison', [
        u'Allison - автоматическая коробка с гидротрансформатором для грузовиков, автобусов и спецтехники (семейства 1000, 2000, 3000, 4000 и другие). Её блок управления TCM '
        u'записывает неисправности, зажигает лампу CHECK TRANS и при серьёзной неисправности переводит коробку в защитный режим: ограничивает передачи или фиксирует одну. '
        u'Читать коды можно сканером по CAN, а производитель предлагает свою диагностическую программу Allison DOC.',
        u'На странице выше сочетаются короткие номера и коды P0xxx; первое, что надо понимать: код может быть активным (неисправность есть сейчас) или записанным в прошлом.',
    ]),
    (u'Масло - первое, что проверяют', [
        u'Многие жалобы на «плохо переключает» объясняются не электроникой, а уровнем и состоянием масла. Уровень проверяют по щупу на прогретой коробке на нейтрали при работающем двигателе, '
        u'в диапазоне температур масла примерно 71-93 °C (160-200 °F), как указано в руководстве Allison. Применяют масло стандарта TES 295 или TES 668 (синтетика), если иное не указано для вашей модели. '
        u'Перегрев, пена или потемнение масла - повод искать причину до ремонта электрики.',
    ]),
    (u'Как читать коды по группам', [
        [u'**Соленоиды и давление (P0962, P0776, P2724, P0975 и др.)** - сначала разъём и жгут соленоида, затем гидравлика.',
         u'**Датчики скорости и давления (P0717, P0847, P1714)** - разъём, сигнал, посторонние металлические частицы на датчике.',
         u'**Тормоз и ретардер (P0703, C1312)** - выключатель тормоза и сигнал запроса ретардера.',
         u'**Двигатель и CAN (P1779, U0010)** - связь с блоком двигателя и состояние шины, а не только коробка.'],
    ]),
    (u'Когда можно ехать', [
        u'Если коробка в защитном режиме, не переключается или горит CHECK TRANS вместе с признаками проскальзывания, остановитесь: проскальзывание быстро перегревает фрикционы. '
        u'Если коробка работает как обычно, а код записан в прошлом, доезжайте до сервиса и сотрите код после проверки.',
        u'Нельзя буксировать грузовик с автоматической коробкой на ведущих колёсах без отсоединения карданного вала: смазка при неработающей коробке отсутствует.',
    ]),
    (u'Вопросы и ответы', [
        (u'Коробка переключает не на все передачи. Что это?',
         u'Либо защитный режим по неисправности соленоида, либо проблема с маслом. Начните с уровня масла и считывания кодов.'),
        (u'Горит CHECK TRANS, но коробка работает. Что делать?',
         u'Прочитайте коды и отметьте, активны ли они. Лампа говорит, что TCM записал неисправность, которую нужно проверить.'),
    ]),
]},

'brand-en:deutz': {'tail': [
    (u'About these Deutz codes', [
        u'Deutz engines power construction machines, farm tractors, forklifts, generator sets and some buses far more often than long-haul tractors, so many of these codes come '
        u'from the machine\'s own display rather than a truck dashboard. The engine computer (EMR, Electronic Motor Regelung) stores faults in two forms: J1939 style SPN.FMI separated by a dot, '
        u'and Deutz-specific numbers above 516000. The manufacturer reads them with its SerDia diagnostic software.',
        u'The difference matters when reading: 100.0 is the standard SPN 100 (engine oil pressure) with FMI 0, while 516408.31 is an internal Deutz number that does not exist in the J1939 tables.',
    ]),
    (u'Reading the FMI part', [
        [u'**FMI 0, 15, 16** - above normal (0 is the most severe): overheating or excess pressure.',
         u'**FMI 1, 17, 18** - below normal (1 is the most severe).',
         u'**FMI 3 and 4** - circuit voltage high or low, usually an open circuit or a short.',
         u'**FMI 5 and 6** - current below normal (open) and current above normal (short to ground).',
         u'**FMI 2** - erratic or implausible data; AdBlue sensor entries show it often.',
         u'**FMI 11 and 31** - cause not known or condition exists: use the engine manual.'],
        u'FMI meanings follow SAE J1939-73; the tables above give the factory wording of each Deutz entry.',
    ]),
    (u'Common causes, most frequent first', [
        [u'Connectors and harness: moisture and vibration on off-highway machines, chafing against brackets.',
         u'AdBlue/SCR system: reagent quality and sensors (codes such as 3031.2, 4334.2, 516201.11).',
         u'Fuel: water and dirt cause misfires and injector faults.',
         u'Oil: level, viscosity, pressure sensor (code 100.0).',
         u'Supply to the EMR unit: battery, ground and terminals can produce several codes at once.',
         u'The control unit itself, last.'],
    ]),
    (u'Can you keep working?', [
        u'Entries for critical oil pressure or oil temperature (100.0, 175.0) mean stop the engine. Sensor-circuit codes (FMI 3, 4, 5, 6) do not endanger the engine directly, '
        u'but protection based on that parameter no longer works, so watch the gauges. If the engine hesitates, loses power or a red lamp comes on, stop.',
    ]),
    (u'Questions and answers', [
        (u'What does a number above 516000 mean?',
         u'It is a Deutz-specific number, not in J1939. Read the description on this page and confirm it in the manual for your engine.'),
        (u'Code 100.0 and the engine runs smoothly. Can I carry on?',
         u'No. The page lists it as critical oil pressure. Stop, check the oil level and measure the pressure with a gauge.'),
        (u'AdBlue sensor reports implausible data. Replace it?',
         u'First check the reagent quality, the tank and the connector; replace the sensor only if those are fine.'),
    ]),
]},

'brand-en:wabco': {'tail': [
    (u'What WABCO codes mean on the truck', [
        u'WABCO (part of the ZF group since 2020) supplies brake electronics for most European and many other tractors and trailers. ABS and EBS faults are read with a scan tool over CAN. '
        u'The amber ABS lamp means anti-lock is partly or fully disabled; the trailer reports its own lamp through the ISO 7638 connector.',
        u'The air brakes themselves keep working because the pneumatics are independent of the electronics. What you lose is anti-lock protection and related functions such as ASR and ESC.',
    ]),
    (u'Typical FMI values in WABCO codes', [
        [u'**FMI 3 and 4** - circuit voltage high or low: sensor, valve or supply.',
         u'**FMI 5 and 6** - open circuit or short to ground in a modulator valve circuit.',
         u'**FMI 1, 2, 7, 8, 10** - at a wheel speed sensor: weak, uneven or vanishing signal. Look at the gap, the tone ring and the wheel bearing.',
         u'**FMI 9** - lost communication on CAN with another unit.',
         u'**FMI 12** - bad intelligent device, i.e. the unit itself. Conclude this last.'],
    ]),
    (u'Causes, most frequent first', [
        [u'Wheel speed sensor and its cable, especially on the front axle where the cable bends with steering.',
         u'Tone ring: dirt, damaged teeth or rust.',
         u'Modulator connectors and harness along the chassis: corrosion, chafing, water.',
         u'Supply and ground of the ABS unit: a voltage drop produces codes for several axles at once.',
         u'The ISO 7638 trailer connector: corroded pins create "phantom" wheel faults.',
         u'The modulator or the unit itself, after everything else.'],
    ]),
    (u'Short check procedure', [
        u'1. Read codes and freeze-frame data. 2. Check supply and ground. 3. Inspect connectors, starting with the ISO 7638 plug on the trailer. 4. Measure the wheel sensor: a WABCO sensor is typically around 0.9-1.3 kOhm; '
        u'compare with the sensor on the same axle. 5. Measure the modulator coil and test the wiring. 6. Replace parts only after that.',
    ]),
    (u'Can you keep driving?', [
        u'Yes, carefully and not for long: the brakes work but without anti-lock. On a slippery road a wheel can lock. Keep extra distance and have the fault repaired.',
    ]),
    (u'Questions and answers', [
        (u'The lamp is on but the sensor and valves test fine. What else?',
         u'Supply and ground of the ABS unit, the ISO 7638 plug and the CAN network. Check those before the unit.'),
        (u'What is the difference between ABS and EBS?',
         u'ABS only prevents wheel lock. EBS also controls braking electronically and exchanges data with the trailer over CAN.'),
        (u'Why do front axle sensors fail more often?',
         u'Their cables flex every time the wheels turn, and they are exposed to spray from the tyre.'),
    ]),
]},

'brand-en:allison': {'tail': [
    (u'About the Allison automatic', [
        u'Allison makes torque-converter automatic transmissions for trucks, buses and special vehicles (the 1000, 2000, 3000, 4000 series and others). Its control unit (TCM) stores faults, '
        u'lights the CHECK TRANS lamp and, for serious faults, puts the transmission into a protective mode: it limits the gears or holds one. Codes can be read with a scan tool over CAN, '
        u'and the manufacturer offers its own diagnostic software, Allison DOC.',
        u'The list above mixes short numbers and P0xxx-style codes. The first thing to know is whether a code is active (the fault exists now) or stored from the past.',
    ]),
    (u'Check the fluid first', [
        u'Many complaints about poor shifting come from the fluid, not the electronics. The level is checked with the dipstick on a warm transmission in neutral with the engine idling, '
        u'with the sump fluid at roughly 71-93 C (160-200 F), as the Allison manual describes. The fluid is normally a TES 295 or TES 668 synthetic unless your model says otherwise. '
        u'Overheated, foamy or dark fluid is a reason to find the cause before repairing electrics.',
    ]),
    (u'Reading codes by group', [
        [u'**Solenoids and pressure (P0962, P0776, P2724, P0975 and others)** - the connector and harness first, then hydraulics.',
         u'**Speed and pressure sensors (P0717, P0847, P1714)** - the connector, the signal, and metal debris on the sensor.',
         u'**Brake and retarder (P0703, C1312)** - the brake switch and the retarder request signal.',
         u'**Engine and CAN (P1779, U0010)** - the link to the engine controller and the state of the bus, not only the transmission.'],
    ]),
    (u'Can you keep driving?', [
        u'If the transmission is in protective mode, will not shift, or CHECK TRANS comes on with slipping, stop: slip overheats the clutches quickly. '
        u'If it shifts normally and the code is only stored, drive to a workshop and clear the code after the check.',
        u'Never tow a truck with an automatic on its drive wheels without disconnecting the driveshaft: there is no lubrication when the transmission is not running.',
    ]),
    (u'Questions and answers', [
        (u'It will not shift into all gears. What does that mean?',
         u'Either a protective mode after a solenoid fault or a fluid problem. Start with the fluid level and read the codes.'),
        (u'CHECK TRANS is on but the transmission works. What should I do?',
         u'Read the codes and note whether they are active. The lamp means the TCM stored a fault that needs checking.'),
        (u'What is code P0703 on a refuse truck?',
         u'It is the brake switch signal. The page notes that on refuse trucks it blocks N-D shifting; check the switch and its signal.'),
    ]),
]},

}
