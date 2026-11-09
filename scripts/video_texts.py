# -*- coding: utf-8 -*-
"""
Тексты роликов для блока «Видеоразбор» (video_block.py), 09.11.2026.
Ключ = ключ в video_razbory.json. ru - озвучка в читаемом виде (без призывов и рекламной концовки,
факты те же), en - перевод по смыслу; topic_en/name_en - подпись и название для англ. страницы.
Абзацы разделяются пустой строкой (\n\n).
Источники: scenario.json / tekst.txt роликов, где они сохранились; иначе - описание из карточки
публикации (tiktok-codetruck/publish/cards), написанное по озвучке.
"""
TEXTS = {
    'spn-97': {
        'ru': u'На КАМАЗе загорелся значок воды в топливе. Можно ли ехать? Код SPN 97. Датчик стоит в отстойнике фильтра грубой очистки. Обычно ехать можно, но код покажите на ближайшем ТО.\n\nСлейте отстой из фильтра-сепаратора в прозрачную ёмкость. Зимой вода в стакане замерзает: отогрейте его, а не меняйте датчик.',
        'en': u'A water-in-fuel icon came on in a KAMAZ. Can you keep driving? The code is SPN 97. The sensor sits in the sump of the primary fuel filter. You can usually keep driving, but show the code at the next service.\n\nDrain the sump of the filter-separator into a clear container. In winter the water in the bowl freezes: thaw it out rather than replacing the sensor.',
        'topic_en': u'KAMAZ SPN 97 - water in fuel',
        'name_en': u'KAMAZ SPN 97: water in fuel - what happens in the filter'},
    'planar-13': {
        'ru': u'Планар не заводится. Две вспышки на пульте — это код 13: не запустился за две попытки. Свеча раскаляется, а пламени нет. ПУ-5 мигает два раза, на экранном пульте — число 13.\n\nПервое: топливо — уровень, сезон, топливопровод, насос. Второе: прочистите воздухозабор и выхлоп. Третье: свеча — прочистите отверстие и сетку — и напряжение.',
        'en': u'The Planar will not start. Two flashes on the controller mean code 13: it failed to start in two attempts. The glow plug heats up, but there is no flame. The PU-5 blinks twice; on a display controller it shows 13.\n\nFirst: the fuel - level, season, fuel line, pump. Second: clean the air intake and the exhaust. Third: the glow plug - clean the hole and the screen - and the voltage.',
        'topic_en': u'Planar code 13 - does not start, 2 blinks on PU-5',
        'name_en': u'Planar will not start: code 13 and 2 blinks on PU-5 - what to check'},
    'eberspacher-011': {
        'ru': u'Eberspächer погас, на пульте AF и 011. Это код 011 — пониженное напряжение: напряжение на блоке управления ниже нормы дольше двадцати секунд, и отопитель отключается. Проверьте заряд аккумулятора и клеммы. Затем — предохранитель отопителя, при необходимости замените его. Не помогло — в мастерскую.',
        'en': u'The Eberspächer went out and the controller shows AF and 011. This is code 011, low voltage: the voltage at the control unit stayed below normal for more than twenty seconds, so the heater shut down. Check the battery charge and the terminals. Then check the heater fuse and replace it if needed. If that does not help, take it to a workshop.',
        'topic_en': u'Eberspächer error 011 - low voltage',
        'name_en': u'Eberspächer error 011: low voltage - why the heater shuts off'},
    'spn-107': {
        'ru': u'Можно ли ехать? SPN 107 — Мерседес ругается на воздушный фильтр. Датчик сравнивает давление до фильтра и после него: чем грязнее фильтр, тем больше разница. FMI 0 — разница выше нормы, фильтр забит. FMI 3 и 4 — неисправна цепь датчика: провод, разъём или сам датчик. Проверьте сами, когда меняли фильтр, нет ли грязи и влаги в трубках датчика, не окислился ли разъём. Забитый фильтр — тяга может падать. Решение о поездке — за вами; сомневаетесь — остановитесь и проверьте фильтр.',
        'en': u'Can you keep driving? SPN 107 - the Mercedes is complaining about the air filter. The sensor compares the pressure before and after the filter: the dirtier the filter, the bigger the difference. FMI 0 - the difference is above normal, the filter is clogged. FMI 3 and 4 - the sensor circuit is faulty: wire, connector or the sensor itself. Check for yourself when the filter was last changed, whether there is dirt or moisture in the sensor tubes, and whether the connector is oxidised. A clogged filter can reduce engine power. The decision to drive is yours; if in doubt, stop and check the filter.',
        'topic_en': u'Mercedes SPN 107 - air filter differential pressure',
        'name_en': u'Mercedes SPN 107: air filter differential pressure - what to check'},
    'webasto-f01': {
        'ru': u'Webasto, F01 — отопитель не запускается. Можно ли ехать? Ехать можно: это отопитель, а не двигатель. Код значит: нет запуска, пламя не появилось даже после повторной попытки. Это по таблице завода для Air Top 2000 ST и Thermo Top Evo. Сначала один раз выключите и включите отопитель. Не помогло — проверьте топливо: есть ли оно в баке, не забиты ли линии. Дальше — горелка: прочистите её и проверьте свечу накаливания. На дизельном Air Top дальше датчик перегрева или блок управления. F02 — срыв пламени: огонь был, но погас.',
        'en': u'Webasto, F01 - the heater does not start. Can you keep driving? Yes: this is the heater, not the engine. The code means no start: no flame appeared even after a repeat attempt. This follows the factory table for the Air Top 2000 ST and Thermo Top Evo. First switch the heater off and on once. If that does not help, check the fuel: is there any in the tank, are the lines blocked. Next is the burner: clean it and check the glow plug. On the diesel Air Top the next suspects are the overheat sensor or the control unit. F02 is flame-out: there was a flame, but it went out.',
        'topic_en': u'Webasto F01 and F02 - no start and flame-out',
        'name_en': u'Webasto F01 and F02: no start and flame-out - what to check'},
    'webasto-f02': {
        'ru': u'Webasto: код F02 — срыв пламени: огонь был, но погас. Код F01 — нет запуска: после двух попыток пламени нет. Что проверить самому: топливо (бак не пустой, трубки не забиты), выход тёплого воздуха, предохранитель и разъёмы. Сначала один раз выключите и включите отопитель. Не помогло — горелка и свеча накаливания. Ехать можно: это отопитель, а не двигатель.',
        'en': u'Webasto: code F02 is flame-out: there was a flame, but it went out. Code F01 is no start: no flame after two attempts. What to check yourself: the fuel (the tank is not empty, the lines are not blocked), the warm-air outlet, the fuse and the connectors. First switch the heater off and on once. If that does not help, look at the burner and the glow plug. You can keep driving: this is the heater, not the engine.',
        'topic_en': u'Webasto F01 and F02 - no start and flame-out',
        'name_en': u'Webasto F01 and F02: no start and flame-out - what to check'},
    'spn-3719': {
        'ru': u'SPN 3719 — сажевый фильтр копит сажу и забивается. Три ступени: FMI 15, 16 и 0. Лампа горит ровно, потом мигает, потом становится красной. Пока лампа ровная и мощность не упала, доедьте и дайте фильтру регенерацию. Если лампа мигает или красная, либо мощность упала, остановитесь, сделайте стояночную регенерацию по инструкции производителя и не прерывайте её. Не помогло — в сервис: золу регенерация не выжигает. Решение о поездке — за водителем.',
        'en': u'SPN 3719 - the particulate filter is accumulating soot and clogging. There are three levels: FMI 15, 16 and 0. The lamp first stays on steadily, then flashes, then turns red. While the lamp is steady and power has not dropped, finish the trip and let the filter regenerate. If the lamp flashes or is red, or power has dropped, stop, run a parked regeneration following the manufacturer instructions and do not interrupt it. If that does not help, go to a workshop: regeneration does not burn off ash. The decision to drive is the driver\'s.',
        'topic_en': u'SPN 3719 - clogged particulate filter',
        'name_en': u'SPN 3719: clogged particulate filter - what the driver should do'},
    'webasto-f03': {
        'ru': u'Webasto, код F03. Что это? Напряжение пониженное или повышенное. Air Top 2000 ST, 12 В: ниже 10,5 В дольше 20 секунд или выше 16 В дольше 6 секунд.\n\nСначала зарядите аккумулятор. Осмотрите клеммы и провода: окисление, плохие контакты. Проверьте предохранитель и разъёмы. Потом выключите отопитель и включите снова. Не помогло — сервис.',
        'en': u'Webasto, code F03. What is it? The voltage is too low or too high. Air Top 2000 ST, 12 V: below 10.5 V for more than 20 seconds or above 16 V for more than 6 seconds.\n\nFirst charge the battery. Inspect the terminals and wires: oxidation, poor contacts. Check the fuse and the connectors. Then switch the heater off and on again. If that does not help, go to a workshop.',
        'topic_en': u'Webasto F03 - low or high voltage',
        'name_en': u'Webasto F03: low or high voltage - what to do'},
    'webasto-f10': {
        'ru': u'Webasto, код F10. Что это? Перегрев: сработала блокировка, отопитель перегрелся. Это Air Top 2000 ST; у других моделей F10 значит другое.\n\nСначала проверьте воздухозаборник и выхлоп: нет ли снега, льда, грязи, не смята ли труба. Выход тёплого воздуха в салон не должен быть закрыт. Осмотрите топливную систему: нет ли подтёков. Если воздух и выхлоп свободны, а перегрев повторяется — сервис: чистка теплообменника, проверка датчика перегрева.',
        'en': u'Webasto, code F10. What is it? Overheating: the lock-out has triggered, the heater overheated. This is the Air Top 2000 ST; on other models F10 means something else.\n\nFirst check the air intake and the exhaust: no snow, ice or dirt, and the pipe is not crushed. The warm-air outlet into the cab must not be blocked. Inspect the fuel system for leaks. If the air and exhaust are clear but the overheating repeats, go to a workshop: heat exchanger cleaning and a check of the overheat sensor.',
        'topic_en': u'Webasto F10 - overheating',
        'name_en': u'Webasto F10: overheating - what to do'},
    'spn-100': {
        'ru': u'SPN 100 — давление масла в двигателе. FMI 1 и 18: давление ниже нормы, ехать нельзя. Сразу заглушите двигатель: без давления масла вал и вкладыши изнашиваются за считаные минуты. Потом проверьте уровень масла по щупу, на ровном месте. FMI 3 и 4 — это не давление, а цепь датчика: проверьте разъём и проводку. Пока не поставили механический манометр, считайте давление настоящим.',
        'en': u'SPN 100 - engine oil pressure. FMI 1 and 18: pressure below normal, do not drive. Shut the engine off at once: without oil pressure the crankshaft and bearings wear out within minutes. Then check the oil level with the dipstick on level ground. FMI 3 and 4 are not about pressure but about the sensor circuit: check the connector and the wiring. Until a mechanical gauge is fitted, treat the pressure reading as real.',
        'topic_en': u'SPN 100 - low oil pressure',
        'name_en': u'SPN 100: low oil pressure - do not drive'},
    'spn-110': {
        'ru': u'SPN 110. Двигатель перегрелся. Что делать? Это температура охлаждающей жидкости. FMI 0, 15 и 16 — выше нормы. Ехать нельзя: остановитесь и дайте двигателю остыть. Крышку бачка не открывайте.\n\nПотом проверьте уровень жидкости, радиатор и ремень вентилятора. FMI 3 и 4 — цепь датчика: проверьте разъём и проводку.',
        'en': u'SPN 110. The engine has overheated. What to do? This is the engine coolant temperature. FMI 0, 15 and 16 mean above normal. Do not drive: stop and let the engine cool down. Do not open the coolant tank cap.\n\nThen check the coolant level, the radiator and the fan belt. FMI 3 and 4 point to the sensor circuit: check the connector and the wiring.',
        'topic_en': u'SPN 110 - engine overheating',
        'name_en': u'SPN 110: engine overheating - do not drive'},
    'spn-1761': {
        'ru': u'SPN 1761: мочевина на исходе. Что делать? Это уровень мочевины в баке. FMI 17 и 18 — ниже нормы. Ехать можно, но долейте мочевину: дальше двигатель ограничит мощность, а потом и скорость. Когда именно, зависит от производителя, не ждите.\n\nFMI 3 и 4 — цепь датчика. Проверьте разъём: на нём бывают кристаллы. Если бак полный, а код есть — виноват датчик.',
        'en': u'SPN 1761: the urea is running low. What to do? This is the urea level in the tank. FMI 17 and 18 mean below normal. You can keep driving, but top up the urea: later the engine will limit power, and then speed. Exactly when depends on the manufacturer, so do not wait.\n\nFMI 3 and 4 point to the sensor circuit. Check the connector: crystals can form on it. If the tank is full but the code is there, the sensor is at fault.',
        'topic_en': u'SPN 1761 - low urea (AdBlue) level',
        'name_en': u'SPN 1761: urea (AdBlue) running low - you can drive, but top up'},
    'planar-29': {
        'ru': u'Планар гаснет при работе, три вспышки — это код 29. Код 29: срыв пламени при работе, топлива не хватает, пламя гаснет. Для Планар 2Д, 4Д, 8Д и 9Д: на ПУ-5 три вспышки, на ПУ-22 число 29.\n\nПричины: мало топлива, насос, индикатор пламени. Проверьте топливопровод — утечки, засор, хомуты. Потом воздухозабор и выхлоп. Если отопитель запускается, подозрение на индикатор пламени. Если повторяется — сервис.',
        'en': u'The Planar goes out while running, three flashes - this is code 29. Code 29: flame-out during operation, not enough fuel, the flame goes out. For Planar 2D, 4D, 8D and 9D: three flashes on the PU-5, the number 29 on the PU-22.\n\nCauses: too little fuel, the pump, the flame indicator. Check the fuel line - leaks, blockage, clamps. Then the air intake and the exhaust. If the heater starts, the flame indicator is the suspect. If it repeats, go to a workshop.',
        'topic_en': u'Planar code 29 - flame-out during operation',
        'name_en': u'Planar: code 29 - flame-out during operation'},
    'spn-102': {
        'ru': u'SPN 102 — давление наддува. Можно ли ехать? Это давление воздуха во впускном коллекторе. FMI 16 — наддув выше нормы, FMI 18 — ниже нормы. Ехать можно, но недалеко: у ряда двигателей блок сам ограничивает мощность. Свист, дым или масло на патрубках — остановитесь.\n\nПроверьте патрубки, хомуты, интеркулер и воздушный фильтр. FMI 2, 3 и 4 — датчик давления: смотрите разъём.',
        'en': u'SPN 102 - boost pressure. Can you keep driving? This is the air pressure in the intake manifold. FMI 16 - boost above normal, FMI 18 - below normal. You can drive, but not far: on a number of engines the ECU limits power by itself. Whistling, smoke or oil on the hoses - stop.\n\nCheck the hoses, clamps, intercooler and air filter. FMI 2, 3 and 4 - the pressure sensor: look at the connector.',
        'topic_en': u'SPN 102 - boost pressure',
        'name_en': u'SPN 102: boost pressure - you can drive, but not far'},
    'spn-789': {
        'ru': u'SPN 789 — горит АБС. Можно ли ехать? Это датчик скорости колеса (передняя ось, левое). Лампа АБС горит — на АБС не рассчитывайте: тормоза работают, но колесо может заблокироваться, тормозной путь длиннее. На скользкой дороге это опаснее всего. Ехать можно, но осторожно, чините скоро. Датчик читает зубья кольца АБС: грязь, ржавчина или большой зазор — и сигнала нет. Ещё виноваты провод у поворотного кулака и люфт подшипника. Причина — зазор, грязь или ржавчина на кольце, обрыв или замыкание провода.',
        'en': u'SPN 789 - the ABS lamp is on. Can you keep driving? This is a wheel speed sensor (front axle, left). With the ABS lamp on, do not count on ABS: the brakes work, but the wheel can lock up and the braking distance is longer. This is most dangerous on a slippery road. You can drive, but carefully, and have it repaired soon. The sensor reads the teeth of the ABS ring: dirt, rust or a large gap and there is no signal. The wire near the steering knuckle and bearing play are also common culprits. The cause is a gap, dirt or rust on the ring, or a broken or shorted wire.',
        'topic_en': u'SPN 789 - ABS wheel speed sensor',
        'name_en': u'SPN 789: ABS sensor - the brakes work, but do not count on ABS'},
    'planar-dlinny': {
        'ru': u'Две вспышки на пульте ПУ-5 и код 13 на экране — это одно и то же. А 13 вспышек — совсем другая неисправность. В ролике разобраны все коды ошибок воздушного отопителя Планар и мигания пульта ПУ-5: что значит каждый код, что проверить самому и когда ехать в сервис.\n\nГлавы: 0:00 — две вспышки и 13 вспышек не одно и то же; 0:17 — две системы: номер кода и мигания ПУ-5; 1:21 — первые проверки при любом коде; 2:08 — пуск и срыв пламени, коды 13, 29, 08, 78; 4:05 — напряжение, коды 12 и 15; 4:40 — свеча и топливный насос, коды 09, 17, 07; 5:12 — нагнетатель воздуха, коды 10, 27, 28; 5:48 — перегрев и датчики, коды 01, 02, 05, 04, 06, 16; 6:56 — связь пульта с блоком, коды 20 и 30; 7:24 — только Планар 8Д, коды 31–36; 7:57 — шпаргалка: вспышки ПУ-5 от 1 до 12; 9:01 — три правила, чтобы не ловить ошибки; 9:25 — когда нужен сервис.\n\nИсточник — заводские руководства по ремонту и эксплуатации воздушных отопителей (таблица кодов ремонта и таблица «код — мигания ПУ-5»). Часть кодов относится только к моделям 8Д.',
        'en': u'Two flashes on the PU-5 controller and code 13 on the display mean the same thing. But 13 flashes is a completely different fault. The video goes through all fault codes of the Planar air heater and the PU-5 controller blinks: what each code means, what to check yourself and when to go to a workshop.\n\nChapters: 0:00 - two flashes and 13 flashes are not the same; 0:17 - two systems: the code number and the PU-5 blinks; 1:21 - first checks for any code; 2:08 - starting and flame-out, codes 13, 29, 08, 78; 4:05 - voltage, codes 12 and 15; 4:40 - glow plug and fuel pump, codes 09, 17, 07; 5:12 - air blower, codes 10, 27, 28; 5:48 - overheating and sensors, codes 01, 02, 05, 04, 06, 16; 6:56 - controller-to-unit link, codes 20 and 30; 7:24 - Planar 8D only, codes 31-36; 7:57 - cheat sheet: PU-5 flashes from 1 to 12; 9:01 - three rules to avoid faults; 9:25 - when you need a workshop.\n\nSource: the factory repair and operating manuals of the air heaters (the repair code table and the "code - PU-5 blinks" table). Some codes apply to the 8D models only.',
        'topic_en': u'Planar - all fault codes and PU-5 blinks',
        'name_en': u'Planar: all fault codes and PU-5 blinks - what they mean and what to do',
        'h2': u'Видео: все коды Планара и мигания ПУ-5',
        'h2_en': u'Video: all Planar codes and PU-5 blinks'},
}
