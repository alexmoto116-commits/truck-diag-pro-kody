(function(){
  'use strict';

  var sel   = document.getElementById('pf-brand');
  var midSel = document.getElementById('pf-mid');
  var std   = document.getElementById('pf-standard');
  var input = document.getElementById('pf-code');
  var go    = document.getElementById('pf-go');
  var out   = document.getElementById('pf-out');
  var langSelect = document.getElementById('pf-lang');
  var dataNote   = document.getElementById('pf-datanote');

  var DB = null, loading = null;

  /* Freightliner/Mack/Detroit Diesel не влезают в двухчастный SPN.FMI:
     их код - тройка MID (модуль) + PID/SID (параметр) + FMI. Вместо
     переделки describe()/analyze() под трёхчастный ключ кодируем MID
     и параметр одной строкой "M<mid>-<P|S><num>" и кладём её на место
     spn - вся остальная логика (describe, Гирлянда, build_pages.py)
     работает со строкой как есть, потому что нигде не предполагает,
     что spn обязательно число. build_pages.py уже отбрасывает нечисловые
     первые части ключа, так что SEO-страницы под эти марки просто не
     генерятся - осознанный пробел, не баг.

     У Detroit Diesel MID из источника фактически один и тот же (128,
     блок двигателя DDEC), поэтому для него выбор модуля не показываем -
     он зашивается в код напрямую. */
  /* Western Star - алиас к Detroit Diesel (см. BRAND_ALIAS ниже), а у
     того коды не SPN.FMI, а MID/PID/SID. Значит и вводить их надо так
     же, иначе марка есть, а поиск по ней не работает. */
  var MID_BRANDS = {freightliner:1, mack:1, detroitdiesel:1, westernstar:1, volvomid:1};
  var MID_FIXED  = {detroitdiesel:'128', westernstar:'128'};

  /* MID-марка, чья таблица лежит не в бесплатной базе, а в дилерской (KV).
     Отличие только в том, куда уходит собранный код: у Freightliner и Mack
     это ключ бесплатной таблицы brands.<марка>["M128-P100.4"], а у Volvo -
     тот же по виду ключ, но спрашиваемый у pcode-API. Таблица большая
     (1407 кодов заводского мануала), в assets её класть нельзя - это
     дилерские данные, и вес файла для всех посетителей. */
  var MID_PCODE_BRANDS = {volvomid:1};

  /* Навесное оборудование нумерует свои коды просто числом: у Thermo
     King это 00-137, у Carrier 1-249, у Планара 1-78, у Eberspacher
     000-085, у Webasto 00-99, у Daewoo это код мигания лампы вида
     "4.4". Автоопределение формата (parseAuto) чисто цифровой ввод
     трактует как SPN - и правильно делает, для грузовика это почти
     всегда SPN. Но у этих марок SPN-таблицы нет вообще, есть только
     дилерская, поэтому "61" от них надо искать как дилерский код, а
     не как SPN 61.

     Kenworth (свой 4-значный код шасси, "0700") и Volkswagen
     Caminhões/Constellation (свой формат "код/подкод" или "код-подкод",
     не всегда совпадает по смыслу с реальным SAE FMI даже когда выглядит
     похоже) - по той же причине здесь же: без этого списка одиночный
     код без слова FMI уходит в ветку SPN без FMI и просто не находится,
     даже когда дилерские данные уже в KV.

     Подмену снимают два случая: явно выбранный в строке стандарта
     "J1939 - SPN/FMI" и слово FMI в самом вводе. И то и другое значит,
     что человек всё-таки вводит SPN - например, чтобы получить общую
     J1939-расшифровку, она работает для любой марки. Спорить с прямо
     высказанным намерением не надо. */
  /* Закрытые базы: марки, чьи дилерские коды ищутся на воркере (pcode-api).
     Список совпадает с KNOWN_PCODE_BRANDS в worker/pcode-api.js - менять вместе.
     КамАЗ сюда не входит: у него свой реестр блоков (blockHits), хотя один из
     его доноров - Mercedes.

     Номер или пара «номер-номер» у такой марки почти всегда дилерский код, а не
     SPN/FMI: у Scania «100» - дилерский, у DAF «84-9» тоже. Поэтому сначала
     спрашиваем закрытую базу, а стандарт J1939 показываем ниже с подписью. */
  var CLOSED_BRANDS = {volvo:1, mercedes:1, scania:1, shacman:1, tata:1, ashokleyland:1, howo:1, faw:1, jac:1,
    international:1, powerstroke:1, cumminsisb:1, cumminsislisc:1, cumminsism:1, cumminsisx:1, paccarmx13:1,
    hino:1, renault:1, caterpillar:1, mahindra:1, deutz:1, fuso:1, thermoking:1, carrier:1, planar:1, webasto:1,
    eberspacher:1, daewoo:1, cumminsisf:1, eaton:1, hyundai:1, haldex:1, allison:1, weichai:1, volkswagen:1,
    mwm:1, isuzu:1, baw:1, ivecoedc:1, ivecoeurotronic:1, iveco:1, daf:1, manzbr2:1, manebs:1, man:1, mack:1,
    yamz:1, volvomid:1, jingwei:1, gaz:1};
  /* Марка с закрытой базой - напрямую или через свой алиас (см. BRAND_ALIAS). */
  function isClosedBrand(brand){
    return !!brand && brand !== 'kamaz' && donorsOf(brand).some(function(d){ return !!CLOSED_BRANDS[d]; });
  }

  /* Марки с блинк-кодами (код вспышек мигающей лампы): «2-1», «2-4-3», «21»,
     «131». Такой ввод - не SPN/FMI: в J1939 он не уходит и срочности не получает.
     Если кода нет ни в открытом словаре, ни в закрытой базе - «не найден». */
  var BLINK_BRANDS = {isuzu:1, maz:1, yamz:1, shacman:1, weichai:1, ivecoedc:1, iveco:1, kamaz:1};
  /* Марки со своей нумерацией FMI (не стандарт J1939): подсказку берём из
     раздела fmiBrand словаря, срочность по FMI не считаем. У MAN легенда из
     SD 812a; у Renault легенды нет - пишем номер со ссылкой на таблицу марки. */
  var OWN_FMI = {man:'man', manebs:'man', manzbr2:'man', renault:'renault'};

  /* Марки, у которых дилерский номер записан САМИМ СЛОВОМ "SPN" плюс число.

     У Renault Trucks 85 из 91 дилерского кода лежат под ключами вида
     "SPN16", "SPN597" - так их печатает заводская документация, и значат
     они там своё: SPN16 у Renault - это "реле обмотки 1, замыкание на плюс
     или обрыв", а вовсе не перепад давления на топливном фильтре, как SPN
     16 по стандарту J1939.

     Беда в том, что parseAuto нарочно отменяет дилерскую ветку, когда во
     вводе есть слово SPN (иначе "SPN16" и "97FMI3" уезжали бы в марочные
     коды вместо стандарта). Правило верное, но именно на Renault оно
     срабатывало против нас: весь заводской справочник марки был недостижим
     в автоопределении, а ответ приходил чужой - и не пустой, а
     правдоподобный, что хуже.

     Лечим тем же приёмом, что и DAF выше: марка выбрана человеком, значит
     сначала спрашиваем её заводскую таблицу ("SPN" + число), и только если
     там пусто - идём в стандарт тем же run(true). Чужих марок не касается:
     ветка включается только по этому списку. */
  var SPN_PCODE_BRANDS = {renault:1};

  /* Марки, у которых дилерские коды бывают короткими hex-кодами из одного-трёх
     знаков с буквой A-F («9A», «A7», «C0»): это ключи их таблицы, а не SPN.
     Такой ввод уходит в дилерскую базу, как и буквенно-цифровой код. */
  var HEX_KEY_BRANDS = {haldex:1};

  var NUM_PCODE_BRANDS = {thermoking:1, carrier:1, planar:1, webasto:1,
                          eberspacher:1, daewoo:1, eaton:1, volkswagen:1,
                          /* Подсистемы Iveco: у ivecoedc код мигания
                             пишется как "4.5" и неотличим от SPN 4 / FMI 5,
                             у ivecoeurotronic это голое число ("38"). Своей
                             таблицы SPN ни у той, ни у другой нет, так что
                             увести числовой ввод в дилерскую ветку здесь
                             ничего не ломает. */
                          ivecoedc:1, ivecoeurotronic:1};

  /* МАРКИ-АЛИАСЫ.

     Половина грузовиков мира - это чужой двигатель под своим шильдиком.
     Kenworth и Peterbilt - это PACCAR MX-13, ГАЗель Next - это Cummins
     ISF, Урал и КрАЗ - это ЯМЗ. Своей таблицы кодов у таких марок нет и
     быть не может: коды выдаёт блок управления двигателем, а он чужой.

     Раньше это значило, что человек, ищущий "ошибка 3712 ГАЗель", не
     находил ничего - хотя ровно эти коды лежат у нас под именем
     "Cummins ISF". Теперь марка есть в списке, а данные берутся у
     донора. Порядок доноров важен: первым идёт самый вероятный.

     Обманывать при этом не нужно: в ответе показывается имя ДОНОРА, а
     не алиаса ("заводская таблица Cummins ISF"), чтобы механик понимал,
     по какому блоку он читает код, и не искал у себя несуществующую
     "фирменную таблицу ГАЗа". */
  var BRAND_ALIAS = {
    gaz:         ['gaz', 'cumminsisf', 'yamz'],
    /* Отопитель Jingwei стоит на SITRAK штатно: код E13 с выбранной маркой
       SITRAK ищем и в его таблице. */
    sitrak:      ['sitrak', 'jingwei'],
    maz:         ['maz', 'yamz', 'mercedes', 'deutz'],
    /* КамАЗ 5490 - это мерседесовский силовой агрегат под своим шильдиком
       (OM457LA, блоки PLD/MR2 + ADM3 + SCR), и коды у него мерседесовские:
       из 364 внутренних кодов таблицы 5490 282 слово в слово совпали с
       нашей таблицей Mercedes. Классический КамАЗ 65115/4308 идёт на
       Cummins ISB. Своя таблица КамАЗа стоит первой и ничего не теряет. */
    /* wabco в конце списка: ABS на шасси КамАЗа вабковский (сканер так и
       подписывает систему - "КАМАЗ - Шасси - Wabco ABS-E4/E8 (CAN)"), и
       тормозных кодов вроде 791.5 нет ни в своей таблице, ни у доноров
       двигателя - ответ выходил общий по J1939 вместо заводского. Ставим
       последним, чтобы четыре пересечения по шине CAN (630.2, 630.12,
       639.2, 639.12) по-прежнему отвечали своей таблицей КамАЗа. */
    /* КамАЗ с реестром блоков (DB.blocks) ищется по блокам, см. blockHits().
       Этот список - запасной путь для базы без реестра. */
    kamaz:       ['kamaz', 'mercedes', 'cumminsisb', 'wabco'],
    ural:        ['yamz', 'kamaz'],
    kraz:        ['yamz'],
    /* Своей таблицы у Kenworth нет: то, что лежало здесь под видом 939
       кодов, оказалось перечнем номеров ПРОВОДОВ из электросхемы
       ("ORIGINAL CIRCUIT WIRING KEY", C17SR = компонент + цепь 17 +
       стартер), а не кодами неисправностей - выброшено 27.08. Остаётся
       двигатель PACCAR MX-13, он у Kenworth и стоит. */
    kenworth:    ['paccarmx13'],
    peterbilt:   ['paccarmx13'],
    westernstar: ['detroitdiesel'],
    bharatbenz:  ['mercedes', 'fuso'],
    ram:         ['cumminsisb'],
    dodge:       ['cumminsisb'],
    fordcargo:   ['cumminsisb', 'cumminsislisc', 'mwm'],
    agrale:      ['cumminsisf', 'mwm'],
    udtrucks:    ['volvo'],
    teplostar:   ['planar'],
    beiben:      ['mercedes'],
    hongyan:     ['iveco'],
    /* Shacman: своя дилерская таблица - это внутренние коды Weichai
       (1..335, флэш-коды EDC7), а ABS на нём вабковская. Официальный
       импортёр публикует "общую таблицу кодов ошибок Shacman" -
       и это ровно наша таблица WABCO: 96 пар SPN.FMI (789-802, 627,
       630, 639) совпали до единой, а в самих описаниях источник
       ссылается на требования компании WABCO. Без этой строки ввод
       "789.1" у Shacman уходил в общую J1939-расшифровку, где SPN 789
       значит совсем другое. */
    shacman:     ['shacman', 'wabco'],
    // Foton: своя таблица SPN/FMI мелкая (27 строк), а реальные коды
    // выдаёт двигатель. Тяжёлый Auman - Weichai WD615/WP10 (флэш-коды
    // той же таблицы EDC7 публикуются прямо под именем Foton BJ3251),
    // лёгкие Aumark/Ollin - Cummins ISF совместного завода Foton
    // Cummins. Обе строчки подписаны именем донора, так что механик
    // видит, по какому блоку читает код.
    foton:       ['foton', 'weichai', 'cumminsisf']
  };

  /* Марка -> список таблиц, в которых её искать. Для обычной марки это
     она сама, для алиаса - его доноры. */
  function donorsOf(brand){
    if(!brand) return [];
    return BRAND_ALIAS[brand] || [brand];
  }
  /* Подпись ответа: своя таблица марки - «фирменная таблица»; таблица донора
     (блок того же поставщика, например КамАЗ -> Mercedes-Benz) - отдельная строка. */
  function donorSrc(donor, brand){
    return donor === brand ? t('factorySource', {brand: brandName(donor)})
                           : t('donorDecoding', {brand: brandName(donor)});
  }
  function donorStep(donor, brand){
    return donor !== brand ? t('donorDecoding', {brand: brandName(donor)}) : t('stepDecoding');
  }
  var MID_LIST = {
    freightliner: [
      {v:'128', ru:'128 — Двигатель',                 en:'128 — Engine'},
      {v:'130', ru:'130 — Автоматическая трансмиссия', en:'130 — Automatic transmission'},
      {v:'136', ru:'136 — Тормоза (ABS)',              en:'136 — Brakes (ABS)'},
      {v:'140', ru:'140 — Панель, левая',              en:'140 — Panel, left'},
      {v:'142', ru:'142 — Панель, правая №1',          en:'142 — Panel, right #1'},
      {v:'164', ru:'164 — Бортовой блок (BHM)',        en:'164 — Bulkhead module (BHM)'},
      {v:'172', ru:'172 — Диагностическая система',    en:'172 — Diagnostic system'},
      {v:'179', ru:'179 — Чёрный ящик',                en:'179 — Black box'},
      {v:'181', ru:'181 — Спутниковая система',        en:'181 — Satellite system'},
      {v:'190', ru:'190 — Кондиционер',                en:'190 — Air conditioner'},
      {v:'219', ru:'219 — Радар',                      en:'219 — Radar'},
      {v:'231', ru:'231 — Сотовая связь',              en:'231 — Cellular'},
      {v:'234', ru:'234 — Панель, правая №2',          en:'234 — Panel, right #2'}
    ],
    mack: [
      {v:'128', ru:'128 — Двигатель (EECU)',        en:'128 — Engine (EECU)'},
      {v:'142', ru:'142 — Приборка/шасси (VECU)',   en:'142 — Dash/chassis (VECU)'},
      {v:'143', ru:'143 — Двигатель, доп. блок',    en:'143 — Engine, secondary'}
    ],
    /* Volvo FH/FM/FL/NH 3 серии - 24 блока заводского мануала. Названия
       блоков взяты с оглавления источника, а не придуманы. */
    volvomid: [
      {v:'128', ru:'128 — Двигатель (EECU)',            en:'128 — Engine (EECU)'},
      {v:'130', ru:'130 — Коробка передач',             en:'130 — Transmission'},
      {v:'136', ru:'136 — Тормоза (ABS, EBS)',          en:'136 — Brakes (ABS, EBS)'},
      {v:'140', ru:'140 — Приборная панель',            en:'140 — Instrument cluster'},
      {v:'141', ru:'141 — Dynafleet',                   en:'141 — Dynafleet'},
      {v:'144', ru:'144 — Блок автомобиля (VECU)',      en:'144 — Vehicle unit (VECU)'},
      {v:'146', ru:'146 — Микроклимат кабины',          en:'146 — Cab climate control'},
      {v:'150', ru:'150 — Пневмоподвеска (ECS)',        en:'150 — Air suspension (ECS)'},
      {v:'163', ru:'163 — Блокиратор запуска',          en:'163 — Immobiliser'},
      {v:'166', ru:'166 — Давление в шинах',            en:'166 — Tyre pressure monitoring'},
      {v:'179', ru:'179 — Шлюз FMS',                    en:'179 — FMS gateway'},
      {v:'184', ru:'184 — Управляемая задняя ось',      en:'184 — Steered rear axle'},
      {v:'185', ru:'185 — Воздухоосушитель (APM)',      en:'185 — Air dryer (APM)'},
      {v:'206', ru:'206 — Магнитола (радио, CD)',       en:'206 — Radio/CD player'},
      {v:'214', ru:'214 — Охранная система',            en:'214 — Alarm system'},
      {v:'216', ru:'216 — Наружное освещение (LCM)',    en:'216 — Exterior lighting (LCM)'},
      {v:'219', ru:'219 — Адаптивный круиз-контроль',   en:'219 — Adaptive cruise control'},
      {v:'220', ru:'220 — Тахограф',                    en:'220 — Tachograph'},
      {v:'222', ru:'222 — Замедлитель (ретардер)',      en:'222 — Retarder'},
      {v:'223', ru:'223 — Селектор передач',            en:'223 — Gear selector'},
      {v:'231', ru:'231 — Мобильный телефон',           en:'231 — Mobile phone'},
      {v:'232', ru:'232 — Подушки безопасности (SRS)',  en:'232 — Airbags (SRS)'},
      {v:'249', ru:'249 — Дополнительное оборудование (BBM)', en:'249 — Bodybuilder module (BBM)'},
      {v:'250', ru:'250 — Модуль на руле',              en:'250 — Steering wheel module'}
    ]
  };

  /* Freightliner не имеет готовых построчных описаний кодов - только
     справочные таблицы имён компонентов (см. Америка-DTC/01-Freightliner.md).
     Вместо тысяч вручную набитых строк describe() собирает текст на лету:
     имя MID + имя PID/SID + текст FMI. Покрыты MID128 (двигатель), MID136
     (ABS), MID190 (кондиционер) и MID219 (радар VORAD) целиком, плюс общий
     диапазон SID 151-254, который встречается на многих модулях. Остальные
     MID (130/140/172/179/181/231/234) не имеют своих SID-таблиц уже у
     самого источника (truck-manuals.net) - не пробел в сборе данных, а
     ограничение первоисточника. Для них выдаётся "модуль + FMI" без имени
     параметра, это лучше, чем ничего. */
  var FL_PID = {"51":["Положение педали газа","Throttle pedal position"],"52":["Температура интеркулера","Intercooler temperature"],"53":["Синхронизатор сцепления","Clutch synchronizer"],"54":["Синхронизатор тормоза","Brake synchronizer"],"55":["Положение вилки переключения передач","Shift fork position"],"56":["Статус диапазона","Range status"],"57":["Статус активатора №2 (трансмиссия)","Actuator #2 status (transmission)"],"58":["Статус контроллера вилки переключения","Shift fork controller status"],"59":["Статус мотора переключения передач","Shift motor status"],"60":["Положение рейки переключения передач","Shift rail position"],"61":["Статус активатора стояночного тормоза","Parking brake actuator status"],"62":["Статус моторного тормоза (Retarder Inhibit)","Retarder inhibit status"],"63":["Статус активатора №1 (трансмиссия)","Actuator #1 status (transmission)"],"64":["Статус переключателя направления","Direction switch status"],"65":["Статус переключателя рабочего тормоза","Service brake switch status"],"66":["Статус компонента разрешения движения","Vehicle enabling component status"],"67":["Статус переключателя запроса переключения","Shift request switch status"],"68":["Коэффициент ограничения крутящего момента","Torque limiting factor"],"69":["Статус переключателя двухскоростного моста","Two-speed axle switch status"],"70":["Переключатель стояночного тормоза","Parking brake switch"],"71":["Таймер отключения на холостом ходу","Idle shutdown timer"],"72":["Положение байпасного клапана кондиционера","A/C bypass valve position"],"73":["Давление вспомогательного насоса","Auxiliary pump pressure"],"74":["Максимальная скорость движения","Max road speed"],"75":["Температура масла переднего моста","Front axle oil temperature"],"76":["Давление подъёма/опускания моста","Axle lift air pressure"],"77":["Температура масла среднего моста","Forward drive axle oil temperature"],"78":["Температура масла заднего моста","Rear drive axle oil temperature"],"79":["Температура дорожного покрытия","Road surface temperature"],"80":["Уровень жидкости омывателя","Washer fluid level"],"81":["Давление в сажевом фильтре","Particulate trap inlet pressure"],"82":["Давление пневмостартера","Air starter pressure"],"83":["Статус ограничения скорости движения","Road speed limit status"],"84":["Скорость движения","Road speed"],"85":["Переключатель круиз-контроля","Cruise control switch"],"86":["Круиз Set Speed","Cruise set speed"],"87":["Круиз High-Set","Cruise high-set"],"88":["Круиз Low-Set","Cruise low-set"],"89":["Статус коробки отбора мощности (PTO)","PTO status"],"90":["Температура масла PTO","PTO oil temperature"],"91":["Положение педали газа (% полного хода)","Accelerator pedal position (%)"],"92":["Процент нагрузки двигателя","Engine load %"],"93":["Выходной крутящий момент","Output torque"],"94":["Давление топлива впрыска","Fuel delivery pressure"],"95":["Перепад давления на топливном фильтре","Fuel filter differential pressure"],"96":["Уровень топлива","Fuel level"],"97":["Индикатор воды в топливе","Water in fuel indicator"],"98":["Уровень масла в двигателе","Engine oil level"],"99":["Перепад давления масляного фильтра","Oil filter differential pressure"],"100":["Давление масла","Oil pressure"],"101":["Давление газов в картере","Crankcase pressure"],"102":["Давление наддува турбокомпрессора","Boost pressure"],"103":["Обороты турбокомпрессора","Turbo speed"],"104":["Давление масла в турбокомпрессоре","Turbo oil pressure"],"105":["Температура во впускном коллекторе","Intake manifold temperature"],"106":["Давление воздуха на входе воздушного фильтра","Air inlet pressure"],"107":["Перепад давления на воздушном фильтре","Air filter differential pressure"],"108":["Барометрическое давление","Barometric pressure"],"109":["Давление охлаждающей жидкости","Coolant pressure"],"110":["Температура охлаждающей жидкости","Coolant temperature"],"111":["Уровень охлаждающей жидкости","Coolant level"],"112":["Перепад давления на фильтре антифриза","Coolant filter differential pressure"],"113":["Диапазон регулятора компрессора","Governor droop"],"114":["Ток аккумуляторной батареи","Net battery current"],"115":["Ток генератора","Alternator current"],"116":["Рабочее давление тормозов","Brake application pressure"],"117":["Давление в 1-м ресивере","Primary reservoir pressure"],"118":["Давление во 2-м ресивере","Secondary reservoir pressure"],"119":["Давление гидравлического ретардера","Hydraulic retarder pressure"],"120":["Температура масла гидравлического ретардера","Hydraulic retarder oil temperature"],"121":["Статус моторного тормоза","Engine retarder status"],"122":["Процент моторного тормоза","Engine retarder %"],"123":["Давление сцепления","Clutch pressure"],"124":["Уровень масла в коробке передач","Transmission oil level"],"125":["Индикатор уровня масла в трансмиссии","Transmission oil level indicator (Hi/Lo)"],"126":["Перепад давления масляного фильтра трансмиссии","Transmission oil filter differential pressure"],"127":["Давление масла (трансмиссия)","Transmission oil pressure"],"154":["Статус доп. вход/выход №2","Auxiliary input/output #2 status"],"155":["Статус доп. вход/выход №1","Auxiliary input/output #1 status"],"156":["Общее давление системы форсунок (время впрыска)","Injector metering rail pressure (timing)"],"157":["Общее давление системы подачи форсунок","Injector metering rail pressure"],"158":["Коммутируемое напряжение батарей","Switched battery voltage"],"159":["Давление подачи газа (не дизель)","Gas supply pressure (non-diesel)"],"160":["Обороты вторичного вала","Mainshaft speed"],"161":["Обороты входного вала","Input shaft speed"],"162":["Переключатель Range коробки передач (выбрано)","Transmission range selected"],"163":["Range достигнут","Range attained"],"164":["Давление управления впрыском","Injection control pressure"],"165":["Компас","Compass bearing"],"166":["Номинальная мощность двигателя","Rated engine power"],"167":["Напряжение генератора","Alternator voltage"],"168":["Напряжение аккумуляторов","Battery voltage"],"169":["Температура внутри кузова","Cargo ambient temperature"],"170":["Температура в кабине","Cab interior temperature"],"171":["Температура наружного воздуха","Ambient air temperature"],"172":["Температура воздуха на впуске","Air inlet temperature"],"173":["Температура выхлопных газов","Exhaust gas temperature"],"174":["Температура топлива","Fuel temperature"],"175":["Температура масла в двигателе","Engine oil temperature"],"176":["Температура масла в турбокомпрессоре","Turbo oil temperature"],"177":["Температура масла трансмиссии","Transmission oil temperature"],"178":["Нагрузка на передний мост","Front axle weight"],"179":["Нагрузка на задний мост","Rear axle weight"],"180":["Вес прицепа","Trailer weight"],"181":["Вес груза","Cargo weight"],"182":["Расход топлива за поездку","Trip fuel"],"183":["Расход топлива","Fuel rate"],"184":["Мгновенный расход топлива","Instant fuel economy"],"185":["Средний расход топлива","Average fuel economy"],"186":["Обороты PTO","PTO speed"],"187":["Ограниченные обороты PTO","PTO set speed"],"188":["Обороты холостого хода","Idle engine speed"],"189":["Номинальные обороты двигателя","Rated engine speed"],"190":["Обороты двигателя","Engine speed"],"191":["Выходная скорость трансмиссии","Transmission output speed"],"232":["Коррекция DGPS","DGPS correction"],"233":["Заводская настройка (Power Unit №)","Power unit number"],"234":["Версия ПО блока управления","Software identification"],"235":["Общее время на холостом ходу","Total idle hours"],"236":["Общий расход топлива на холостом ходу","Total idle fuel"],"237":["VIN","VIN"],"238":["Направление вектора скорости движения","Velocity vector direction"],"239":["Положение машины (GPS)","Vehicle position (GPS)"],"240":["Заводской код настройки (Change Ref №)","Change reference number"],"241":["Давление в шинах","Tire pressure"],"242":["Температура колеса/шины","Tire temperature"],"243":["ID компонента","Component ID"],"244":["Пробег за поездку (TRIP)","Trip distance"],"245":["Общий пробег","Total vehicle distance"],"246":["Общее время работы машины","Total vehicle hours"],"247":["Общее время работы двигателя","Total engine hours"],"248":["Общее время работы PTO","Total PTO hours"],"249":["Общее число оборотов двигателя","Total engine revolutions"],"250":["Общий расход топлива","Total fuel used"],"251":["Часы (Clock)","Clock"],"252":["Дата","Date"],"253":["Общее время (Elapsed Time)","Elapsed time"]};
  var FL_SID = {'128':{"1":["Форсунка цилиндра №1","Injector cylinder #1"],"2":["Форсунка цилиндра №2","Injector cylinder #2"],"3":["Форсунка цилиндра №3","Injector cylinder #3"],"4":["Форсунка цилиндра №4","Injector cylinder #4"],"5":["Форсунка цилиндра №5","Injector cylinder #5"],"6":["Форсунка цилиндра №6","Injector cylinder #6"],"7":["Форсунка цилиндра №7","Injector cylinder #7"],"8":["Форсунка цилиндра №8","Injector cylinder #8"],"9":["Форсунка цилиндра №9","Injector cylinder #9"],"10":["Форсунка цилиндра №10","Injector cylinder #10"],"11":["Форсунка цилиндра №11","Injector cylinder #11"],"12":["Форсунка цилиндра №12","Injector cylinder #12"],"13":["Форсунка цилиндра №13","Injector cylinder #13"],"14":["Форсунка цилиндра №14","Injector cylinder #14"],"15":["Форсунка цилиндра №15","Injector cylinder #15"],"16":["Форсунка цилиндра №16","Injector cylinder #16"],"17":["Главный запорный клапан подачи топлива","Fuel shutoff main valve"],"18":["Клапан управления подачей топлива","Fuel control valve"],"19":["Байпасный клапан дросселя","Throttle bypass valve"],"20":["Механизм управления распределением","Timing actuator"],"21":["Датчик положения коленвала","Crankshaft position sensor"],"22":["Датчик распределения","Timing sensor"],"23":["Механизм топливной рейки","Fuel rack actuator"],"24":["Датчик положения топливной рейки","Fuel rack position sensor"],"25":["Сигнал внешней защиты двигателя","External engine protect signal"],"26":["Вспомогательный драйвер №1","Auxiliary output driver #1"],"27":["Привод турбокомпрессора №1","Turbo actuator #1"],"28":["Привод турбокомпрессора №2","Turbo actuator #2"],"29":["Входной сигнал топливной системы","External fuel input signal"],"30":["Входной сигнал скорости","External speed input signal"],"31":["Сигнал тахометра","Tachometer signal"],"32":["Привод байпасного клапана турбины (wastegate)","Wastegate driver"],"33":["Пневмоуправление муфтой вентилятора","Fan clutch drive"],"34":["Датчик давления выхлопа","Exhaust pressure sensor"],"35":["Соленоид регулировки давления выхлопа","Exhaust pressure control solenoid"],"36":["Лампа свечей накаливания","Glow plug lamp"],"37":["Силовое реле","Power relay"],"38":["Реле системы свечей накаливания","Glow plug system relay"],"39":["Реле стартера","Starter relay"],"40":["Вспомогательный драйвер №2","Auxiliary output driver #2"],"41":["Питание ECM 8В","ECM 8-volt power supply"],"42":["Регулятор давления форсунок","Injector pressure regulator"],"43":["Управление высокой передачей автопереключения","Auto-shift high gear control"],"44":["Управление низкой передачей автопереключения","Auto-shift low gear control"],"45":["Управление нейтралью автопереключения","Auto-shift neutral control"],"46":["Общая цепь минус автопереключения","Auto-shift common ground circuit"],"47":["Форсунка цилиндра №17","Injector cylinder #17"],"48":["Форсунка цилиндра №18","Injector cylinder #18"],"49":["Форсунка цилиндра №19","Injector cylinder #19"],"50":["Форсунка цилиндра №20","Injector cylinder #20"],"51":["Дополнительный вход/драйвер №3","Auxiliary output driver #3"],"52":["Дополнительный вход/драйвер №4","Auxiliary output driver #4"],"53":["Вспомогательный драйвер №5","Auxiliary output driver #5"],"54":["Вспомогательный драйвер №6","Auxiliary output driver #6"],"55":["Вспомогательный драйвер №7","Auxiliary output driver #7"],"56":["Дополнительный вход/драйвер №8","Auxiliary output driver #8"],"57":["Дополнительный ШИМ-драйвер №1","Auxiliary PWM driver #1"],"58":["Дополнительный ШИМ-драйвер №2","Auxiliary PWM driver #2"],"59":["Дополнительный ШИМ-драйвер №3","Auxiliary PWM driver #3"],"60":["Дополнительный ШИМ-драйвер №4","Auxiliary PWM driver #4"],"61":["Клапан смесеобразования (Swirl Valve)","Variable swirl valve"],"62":["Датчик преднасоса","Prestroke sensor"],"63":["Привод преднасоса","Prestroke actuator"],"64":["Датчик оборотов двигателя №2","Engine speed sensor #2"],"65":["Датчик кислорода","Oxygen sensor"],"66":["Сигнал режима сгорания","Ignition mode signal"],"67":["Сигнал момента зажигания","Ignition timing signal"],"68":["Давление во впуске 2-го турбокомпрессора","Turbo #2 inlet pressure"],"69":["Температура интеркулера (ACOC)","Intercooler temperature (ACOC)"],"70":["Подогрев впускного воздуха №1","Intake air heater #1"],"71":["Подогрев впускного воздуха №2","Intake air heater #2"],"72":["Форсунка цилиндра №21","Injector cylinder #21"],"73":["Форсунка цилиндра №22","Injector cylinder #22"],"74":["Форсунка цилиндра №23","Injector cylinder #23"],"75":["Форсунка цилиндра №24","Injector cylinder #24"],"76":["Датчик детонации","Knock sensor"],"77":["Клапан подачи газа","Gas metering valve"],"78":["Контроллер топливного насоса","Fuel pump controller"]},'136':{"1":["Датчик ABS, ось 1, левый","ABS sensor, axle 1, left"],"2":["Датчик ABS, ось 1, правый","ABS sensor, axle 1, right"],"3":["Датчик ABS, ось 2, левый","ABS sensor, axle 2, left"],"4":["Датчик ABS, ось 2, правый","ABS sensor, axle 2, right"],"5":["Датчик ABS, ось 3, левый","ABS sensor, axle 3, left"],"6":["Датчик ABS, ось 3, правый","ABS sensor, axle 3, right"],"7":["Модулятор ABS, ось 1, левый","ABS modulator, axle 1, left"],"8":["Модулятор ABS, ось 1, правый","ABS modulator, axle 1, right"],"9":["Модулятор ABS, ось 2, левый","ABS modulator, axle 2, left"],"10":["Модулятор ABS, ось 2, правый","ABS modulator, axle 2, right"],"11":["Модулятор ABS, ось 3, левый","ABS modulator, axle 3, left"],"12":["Модулятор ABS, ось 3, правый","ABS modulator, axle 3, right"],"13":["Реле моторного тормоза","Retarder control relay"],"14":["Реле диагонали №1","Diagonal relay 1"],"15":["Реле диагонали №2","Diagonal relay 2"],"16":["Переключатель ABS","ABS mode switch"],"17":["Переключатель ASR","ASR mode switch"],"18":["Клапан DIF 1-ASR","ASR diff valve 1"],"19":["Клапан DIF 2-ASR","ASR diff valve 2"],"20":["Пневмоуправление двигателем","Pneumatic engine control"],"21":["Электроуправление двигателем","Electric engine control"],"22":["Датчик спидометра","Speedometer sensor signal input"],"23":["Лампа ABS","ABS warning lamp"],"24":["Лампа ASR","ASR warning lamp"],"25":["Средняя скорость датчиков ABS оси 1","Axle 1 ABS sensor average speed"],"26":["Средняя скорость датчиков ABS оси 2","Axle 2 ABS sensor average speed"],"27":["Средняя скорость датчиков ABS оси 3","Axle 3 ABS sensor average speed"],"28":["Модулятор клапана ABS для мостов трансмиссии","Drive axle ABS modulator valve"],"29":["Датчик давления клапана ABS для мостов трансмиссии","Drive axle ABS pressure transducer"],"30":["Главное реле","Master relay"],"31":["Тормоз передней тележки прицепа, левый — регулировка неверна","Front trailer bogie, left brake, adjustment wrong"],"32":["Тормоз передней тележки прицепа, правый — регулировка неверна","Front trailer bogie, right brake, adjustment wrong"],"33":["Тормоз задней тележки прицепа, левый — регулировка неверна","Rear trailer bogie, left brake, adjustment wrong"],"34":["Тормоз задней тележки прицепа, правый — регулировка неверна","Rear trailer bogie, right brake, adjustment wrong"],"35":["Тормоз переднего моста тягача, левый — регулировка неверна","Tractor front axle, left brake, adjustment wrong"],"36":["Тормоз переднего моста тягача, правый — регулировка неверна","Tractor front axle, right brake, adjustment wrong"],"37":["Тормоз переднего моста-редуктора тягача, левый — регулировка неверна","Tractor front drive axle, left brake, adjustment wrong"],"38":["Тормоз переднего моста-редуктора тягача, правый — регулировка неверна","Tractor front drive axle, right brake, adjustment wrong"],"39":["Тормоз заднего моста-редуктора тягача, левый — регулировка неверна","Tractor rear drive axle, left brake, adjustment wrong"],"40":["Тормоз заднего моста-редуктора тягача, правый — регулировка неверна","Tractor rear drive axle, right brake, adjustment wrong"],"41":["Реле пневмоподвески по высоте","Suspension height relay"],"42":["Соленоид удерживающего клапана, ось 1, левый","Holding valve solenoid, axle 1, left"],"43":["Соленоид удерживающего клапана, ось 1, правый","Holding valve solenoid, axle 1, right"],"44":["Соленоид удерживающего клапана, ось 2, левый","Holding valve solenoid, axle 2, left"],"45":["Соленоид удерживающего клапана, ось 2, правый","Holding valve solenoid, axle 2, right"],"46":["Соленоид удерживающего клапана, ось 3, левый","Holding valve solenoid, axle 3, left"],"47":["Соленоид удерживающего клапана, ось 3, правый","Holding valve solenoid, axle 3, right"],"48":["Соленоид сброса клапана, ось 1, левый","Release valve solenoid, axle 1, left"],"49":["Соленоид сброса клапана, ось 1, правый","Release valve solenoid, axle 1, right"],"50":["Соленоид сброса клапана, ось 2, левый","Release valve solenoid, axle 2, left"],"51":["Соленоид сброса клапана, ось 2, правый","Release valve solenoid, axle 2, right"],"52":["Соленоид сброса клапана, ось 3, левый","Release valve solenoid, axle 3, left"],"53":["Соленоид сброса клапана, ось 3, правый","Release valve solenoid, axle 3, right"],"54":["Мотор гидронасоса","Hydraulic pump motor"],"55":["Переключатель стоп-сигнала №1","Brake light switch 1"],"56":["Переключатель стоп-сигнала №2","Brake light switch 2"],"57":["Электроконтроль давления тормозов, ось 1","Electric pressure control, axle 1"],"58":["Контроль давления резервной системы, ось 1","Spare system pressure monitoring, axle 1"],"59":["Давление тормозов, ось 1","Brake pressure, axle 1"],"60":["Электроконтроль давления тормозов, ось 2","Electric pressure control, axle 2"],"61":["Контроль давления резервной системы, ось 2","Spare system pressure control, axle 2"],"62":["Давление тормозов, ось 2","Brake pressure, axle 2"],"63":["Электрорегулировка тормоза, ось 3","Electric brake adjustment, axle 3"],"64":["Электроконтроль давления тормозов, ось 3","Electric pressure control, axle 3"],"65":["Давление тормозов, ось 3","Brake pressure, axle 3"],"66":["Электрорегулировка тормоза, прицеп","Electric brake adjustment, trailer"],"67":["Пневмоконтроль тормозов, прицеп","Pneumatic brake control, trailer"],"68":["Давление тормозов, прицеп","Brake pressure, trailer"],"69":["Датчик нагрузки на оси","Load sensor on axles"],"70":["Датчик толщины накладок, ось 1, левый","Lining thickness sensor, axle 1, left"],"71":["Датчик толщины накладок, ось 1, правый","Lining thickness sensor, axle 1, right"],"72":["Датчик толщины накладок, ось 2, левый","Lining thickness sensor, axle 2, left"],"73":["Датчик толщины накладок, ось 2, правый","Lining thickness sensor, axle 2, right"],"74":["Датчик толщины накладок, ось 3, левый","Lining thickness sensor, axle 3, left"],"75":["Датчик толщины накладок, ось 3, правый","Lining thickness sensor, axle 3, right"],"76":["Датчик сигнала торможения","Brake signal transmitter"],"77":["Сигнал датчика торможения №1","Brake sensor signal #1"],"78":["Сигнал датчика торможения №2","Brake sensor signal #2"],"79":["Размер колеса","Wheel size"],"80":["Управление торможением машины","Vehicle brake control"]},'190':{"1":["Уровень фреона","Freon level"],"2":["Влажность фреона","Moisture level in freon"],"3":["Неконденсируемый газ во фреоне","Non-condensing gas in freon"],"4":["Соленоид управления потоком фреона","Solenoid controlling freon flow"],"5":["Датчик низкого давления фреона","Low freon pressure sensor"],"6":["Цепь управления компрессором кондиционера","Freon compressor control circuit"],"7":["Цепь термостата радиатора кондиционера","A/C radiator thermostat circuit"]},'219':{"1":["Передняя антенна","Front antenna"],"2":["Электроника антенн","Antenna electronics"],"3":["Монитор тормозной системы","Brake system monitor"],"4":["Монитор динамики движения","Dynamics monitor"],"5":["Монитор положения органов управления","Control position monitor"],"6":["Монитор спидометра","Speedometer monitor"],"7":["Монитор бокового радара (правый угол)","Right-angle monitor"],"8":["Монитор поворота налево","Left turn monitor"],"9":["Дисплей","Display"],"10":["Датчик правой стороны","Right side sensor"],"11":["Датчик левой стороны","Left side sensor"],"12":["Задний датчик","Rear sensor"]}};
  var FL_SID_COMMON = {"151":["Диагностический код системы №1","System diagnostic code #1"],"152":["Диагностический код системы №2","System diagnostic code #2"],"153":["Диагностический код системы №3","System diagnostic code #3"],"154":["Диагностический код системы №4","System diagnostic code #4"],"155":["Диагностический код системы №5","System diagnostic code #5"],"219":["Индикатор сгорания","Combustion indicator"],"220":["Электрическое соединение тягач/прицеп (ISO 11992)","Tractor/trailer electrical connection (ISO 11992)"],"221":["Напряжение питания датчиков","Sensor supply voltage"],"222":["Лампа PROTECT","Protect lamp"],"223":["Датчик яркости","Brightness sensor"],"224":["Сигнализация","Alarms"],"225":["Жёлтая лампа","Yellow lamp"],"226":["Датчик трансмиссии","Transmission sensor"],"227":["Доп. вход №1","Auxiliary input #1"],"228":["Переключатель высокого давления","High pressure switch"],"229":["Переключатель Kickdown","Kickdown switch"],"230":["Переключатель подтверждения холостого хода","Idle validation switch"],"231":["Цепь SAE J1939","SAE J1939 link"],"232":["Питание 5В","5-volt DC supply"],"233":["Драйвер №2","Driver #2"],"234":["Механизм включения стояночного тормоза","Parking brake ON mechanism"],"235":["Механизм выключения стояночного тормоза","Parking brake OFF mechanism"],"236":["Устройство соединения питания","Power connection device"],"237":["Устройство соединения прикуривателя","Cigar lighter connection device"],"238":["Диагностическая лампа — красная","Diagnostic lamp — red"],"239":["Диагностическая лампа — жёлтая","Diagnostic lamp — yellow"],"240":["Память","Memory"],"242":["Переключатель Resume круиза","Cruise resume switch"],"243":["Переключатель Set круиза","Cruise set switch"],"244":["Переключатель Enable круиза","Cruise enable switch"],"245":["Переключатель №1 педали сцепления","Clutch pedal switch #1"],"246":["Переключатель №1 педали тормоза","Brake pedal switch #1"],"247":["Переключатель №2 педали тормоза","Brake pedal switch #2"],"248":["Диагностическая цепь OME","OEM diagnostic circuit"],"249":["Цепь SAE J1922","SAE J1922 link"],"250":["Цепь SAE J1708 (J1587)","SAE J1708 (J1587) link"],"251":["Питание","Power supply"],"252":["Модуль калибровки","Calibration module"],"253":["Память калибровки","Calibration memory"],"254":["Контроллер №1","Controller #1"]};
  var FL_MID_NAME = {ru:{"128": "Двигатель", "130": "Трансмиссия", "136": "ABS", "140": "Панель, левая", "142": "Панель, правая", "172": "Диагностическая система", "179": "Чёрный ящик", "181": "Спутниковая система", "190": "Кондиционер", "219": "Радар", "231": "Сотовая связь", "234": "Панель, правая #2"}, en:{"128": "Engine", "130": "Transmission", "136": "ABS", "140": "Panel, left", "142": "Panel, right", "172": "Diagnostic system", "179": "Black box", "181": "Satellite system", "190": "Air conditioner", "219": "Radar", "231": "Cellular", "234": "Panel, right #2"}};

  function composeFreightlinerText(mid, letter, num){
    var lang = currentLang === 'ru' ? 0 : 1;
    var entry = letter === 'P' ? FL_PID[num] : ((FL_SID[mid] && FL_SID[mid][num]) || FL_SID_COMMON[num]);
    if(!entry) return null;
    var modName = FL_MID_NAME[currentLang === 'ru' ? 'ru' : 'en'][mid] || ('MID ' + mid);
    return modName + ' — ' + entry[lang];
  }

  function midName(item){
    return (currentLang === 'ru' ? item.ru : item.en) || item.ru;
  }

  function fillMid(){
    if(!midSel) return;
    var brand = sel.value;
    var list = MID_LIST[brand];
    while(midSel.options.length > 1) midSel.removeChild(midSel.lastChild);
    if(list){
      list.forEach(function(item){
        var o = document.createElement('option');
        o.value = item.v; o.textContent = midName(item);
        midSel.appendChild(o);
      });
    }
    /* Строка "Модуль" - только когда её правда нужно выбирать (Freightliner/
       Mack). У Detroit Diesel модуль зашит в код (MID_FIXED), выбора нет,
       и своя строка стандарта им обеим ни к чему - формат диктует марка. */
    midSel.style.display = list ? '' : 'none';
    if(std) std.style.display = MID_BRANDS[brand] ? 'none' : '';
    if(input) input.placeholder = MID_BRANDS[brand] ? 'P100 FMI 4' : 'SPN 100 FMI 1';
    /* Выбор стандарта и подсказка поля зависят и от режима: эта функция
       вызывается при старте уже после applyLang, и без повторного
       applyModeUi отопитель и тахограф получали бы пример SPN/FMI и
       выбор стандарта. */
    applyModeUi();
  }

  /* Свободный ввод для этих марок - не SPN, а PID/SID: "P100 FMI 4"
     или "S1 FMI 4" (P/S не указан - считаем PID, он чаще встречается
     в источниках). MID берём из выбора выше (или из MID_FIXED). */
  /* Код OBD-II во вводе MID-марки: буква и четыре знака, без FMI
     ("P0016", "P02CD", "U0100"). PID/SID так не записывают, так что
     совпадение однозначно значит дилерскую таблицу марки. */
  function midObdCode(raw){
    var up = normCode(raw);
    if(/FMI/.test(up)) return null;
    /* Пробел или дефис после буквы допускаем: «P 0016», «P-040A» - так Mack
       и пишут на приборке. В ответ уходит слитная запись «P0016». */
    var m = up.match(/\b([PUBC])\s*-?\s*([0-9A-F]{4})\b/);
    return m ? m[1] + m[2] : null;
  }

  /* Volvo пишет коды четырьмя семействами: PID и SID - это стандарт
     J1587, PPID и PSID - собственная нумерация Volvo поверх него, и
     номера в них не пересекаются по смыслу (PSID 42 у MID128 - это
     прерывание дозирования мочевины, а PID 42 - совсем другое). В
     ключе семейство сжимается до P/S/PP/PS. Длинные имена разбираем
     ПЕРВЫМИ: иначе "PSID42" развалится на букву и число неправильно. */
  var MID_FAMILY = {PID:'P', SID:'S', PPID:'PP', PSID:'PS'};

  /* MID-код по частям: модуль (MID) в начале, внутри или через дефис -
     "MID 144 PID 97 FMI 2", "M128-P100.1", "128-100-1". */
  function midSplit(up){
    /* «M 128-P100.1», «M-128-P100.1» - пробел и дефис после M допустимы;
       между номером параметра и FMI может стоять просто пробел («P100 1»). */
    var m = /^M?\s*-?\s*(\d{3})\s*[-\/]\s*((?:(?:PPID|PSID|PID|SID|PP|PS|P|S)\s*)?\d{1,4}(?:\s*[.\-\/,]\s*|\s+)\d{1,2})$/.exec(up);
    if(m) return {mid:m[1], body:m[2]};
    m = /\bMID\s*(\d{3})\b\s*[-\/,]?\s*/.exec(up);
    if(m) return {mid:m[1], body:(up.slice(0, m.index) + ' ' + up.slice(m.index + m[0].length)).trim()};
    return {mid:null, body:up};
  }
  /* Тело кода: «PID 97 FMI 2», «SID 1-6 FMI 5» (диапазон - берём первый номер),
     «PID 100.1», «P100 FMI 4», «100 1», «100 FMI 1». Без семейства - PID. */
  function parseMidBody(body){
    var F = 'PPID|PSID|PID|SID|PP|PS|P|S';
    var m = new RegExp('\\b(' + F + ')\\s*(\\d{1,4})(?:\\s*-\\s*\\d{1,4})?\\D{0,20}?FMI\\s*[:\\-]?\\s*(\\d{1,2})(?!\\d)').exec(body);
    if(!m) m = new RegExp('\\b(' + F + ')\\s*(\\d{1,4})(?:\\s*-\\s*\\d{1,4})?(?:\\s*[.\\-\\/,]\\s*|\\s+)(\\d{1,2})(?!\\d)').exec(body);
    if(!m) m = /^()(\d{1,4})\s*(?:FMI\s*[:\-]?\s*|[.\-\/,]\s*|\s+)(\d{1,2})$/.exec(body);
    if(!m) return null;
    return {letter: MID_FAMILY[m[1]] || m[1] || 'P', num: m[2], fmi: parseInt(m[3], 10)};
  }
  function parseMidCode(t, mid, brand){
    var b = parseMidBody(midSplit(normCode(t)).body);
    if(!b){
      /* FMI нет вовсе, но код похож на OBD-II ("P0016") - дилерская таблица марки. */
      var obd = midObdCode(t);
      return obd ? {pcode:obd} : {bad:true};
    }
    if(MID_PCODE_BRANDS[brand]) return {pcode:'M' + mid + '-' + b.letter + b.num + '.' + b.fmi};
    return {spn:'M' + mid + '-' + b.letter + b.num, fmi:b.fmi};
  }

  function parseAllMid(raw, mid){
    var up = normCode(raw), out = [], seen = {}, m;
    var re = /\b(PPID|PSID|PID|SID|PP|PS|P|S)\s*(\d{1,4})\D{0,20}FMI\s*[:\-]?\s*(\d{1,2})(?!\d)/g;
    while((m = re.exec(up))){
      var spn = 'M' + mid + '-' + (MID_FAMILY[m[1]] || m[1]) + m[2],
          fmi = parseInt(m[3], 10), k = spn + '.' + fmi;
      if(!seen[k]){ seen[k] = 1; out.push({spn:spn, fmi:fmi}); }
    }
    return out;
  }

  /* Дилерские таблицы (pcode) больше не публикуются целиком в
     assets/dtc.enc.js / dtc.en.js - см. worker/pcode-api.js и
     scripts/build_pcode.py. Один код ищем по сети, а не в памяти. */
  var PCODE_API = 'https://codetruck-pcode-api.alexdiag116.workers.dev';

  /* ---------- перевод интерфейса ----------
     База (названия SPN, заводские таблицы) остаётся русской - там
     тысячи строк, перевести их некому и незачем. А вот стандартные
     расшифровки FMI по J1939 - фиксированный список из 23 значений,
     их перевести можно и нужно: это половина каждого ответа. */
  var I18N = {
    ru: {
      pageTitle: 'Код неисправности грузовика — SPN/FMI и дилерские коды',
      langOffer: 'Эта страница есть на русском',
      metaDescription: 'Бесплатная расшифровка кодов неисправностей грузовиков: стандарт J1939 (SPN/FMI) и заводские таблицы 80+ марок. Введите код со сканера или с приборной панели.',
      h1: 'Загорелась лампа <em>Check&nbsp;Engine</em> — что означает код?',
      purposeStats: '39 000+ кодов неисправностей по 80+ маркам техники и агрегатов',
      purposeDo: 'Введите код — или сразу весь список ошибок, как есть: через запятую, пробел или столбиком. Одна поломка тянет за собой пять-шесть кодов — покажем, какой из них причина, а какие пришли следом, и скажем, можно ли ехать.',
      goBtn: 'Разобрать',
      modeGroup: 'Режим поиска',
      modeMotor: 'Мотор и блоки',
      modeHeater: 'Отопитель',
      modeTacho: 'Тахограф',
      heaterHint: 'Код с пульта: 031, E-031, F09',
      heaterEmpty: 'Введите код с пульта отопителя — например <b>031</b>, <b>E-031</b>, <b>F09</b> или <b>12</b>.',
      heaterBadCode: 'Этот код не похож на код отопителя. Введите цифры — например <b>031</b>, <b>E-031</b>, <b>F09</b> или <b>12</b>.',
      heaterNotFound: 'Код не найден в таблицах {list} — проверьте марку отопителя.',
      heaterNotFoundOne: 'Код <b>{code}</b> не найден в таблице {brand} — проверьте марку отопителя.',
      brandGroupHeaters: 'Отопители',
      brandGroupTacho: 'Тахографы',
      tachoHint: 'Код или текст с экрана тахографа',
      tachoPickBrand: 'Выберите марку тахографа в списке выше.',
      tachoNotFound: 'Код не найден в таблице {brand}.',
      tachoNone: 'Не нашли: проверьте марку тахографа или введите текст с экрана',
      codeEmpty: 'Введите код.',
      demoTag: 'пример',
      brandDefault: '— любая марка —',
      brandGroupVehicles: 'Марки техники',
      brandGroupSystems: 'Системы и агрегаты',
      midDefault: '— выберите модуль —',
      needMid: 'У этой марки код состоит из модуля (MID) и параметра. Выберите модуль в списке выше — например «Двигатель» или «ABS» — и введите остаток кода с FMI, например <b>P100 FMI 4</b>.',
      standardAuto: 'Определить автоматически',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: 'Дилерский / OBD-код',
      dataLangNote: '',
      printLabel: 'Распечатать',
      themeDay: 'Дневная тема',
      themeNight: 'Ночная тема',
      footText: 'Справочник показывает, что означает код, а не ставит диагноз — решение всегда за человеком с оборудованием. Вопросы — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>.',
      langAria: 'Язык страницы',
      copyMail: 'Скопировать адрес',
      copied: 'Скопировано',
      emptyPrompt: 'Введите код — например <b>SPN 100 FMI 1</b> или просто <b>100/1</b>.',
      badCode: 'Не удалось разобрать этот код в выбранном стандарте. Попробуйте «Определить автоматически» или формат <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b>.',
      pcodeNotFound: 'Дилерский код <b>{code}</b> в справочнике не найден. Такие коды у каждой марки свои — проверьте написание.',
      pcodeSearching: 'Ищем код…',
      pcodeApiError: 'Нет связи с базой кодов — проверьте интернет и попробуйте ещё раз.',
      dealerBase: 'дилерская база — {brand}',
      dealerOffline: 'дилерская база сейчас недоступна — показан только открытый словарь.',
      dailyLimit: 'Лимит поисков на сегодня исчерпан (50 в сутки). Попробуйте завтра.',
      scanStep: 'номер сканера',
      fmiOwn: 'FMI по таблице производителя блока',
      j1939Caption: 'По стандарту J1939 (двигатели Bosch и другие блоки со стандартной нумерацией)',
      blinkLimit: 'Ограничение', blinkCode: 'блинк {n}',
      blinkNotFound: 'Блинк-код <b>{n}</b> в таблице КамАЗ Евро-3 (Bosch MS 6.1) не найден.',
      cumminsFcLabel: 'Cummins ISB 6.7, код FC {n}',
      scanMany: 'Номер <b>{code}</b> отвечает нескольким кодам на щитке — сверьтесь с тем, что показывает панель.',
      stepCode: 'код', stepDecoding: 'расшифровка',
      donorDecoding: 'Расшифровка по таблице {brand} (блок того же поставщика)',
      factorySource: 'фирменная таблица {brand}', standardSource: 'стандарт J1939',
      blinkNotFoundFor: 'Блинк-код {n} не найден в таблице {brand}.',
      j1939ForBrand: 'По стандарту J1939 — у {brand} номер может значить другое',
      badCodeFor: 'Код не распознан в таблице {brand}, проверьте формат.',
      pcodeServerError: 'База кодов временно недоступна — попробуйте позже.',
      fmiTable: 'FMI {fmi} по таблице {brand}',
      midDefault: 'MID в коде не указан — считаем модулем двигателя, MID 128.',
      midTyped: 'В коде указан MID {mid} — используем его, а не выбранный в списке ({sel}).',
      composedSource: 'собрано из таблиц компонентов {brand}',
      spnNotFound: '<b>SPN {spn}</b> в справочнике не найден — скорее всего, код фирменный. Попробуйте выбрать марку выше или добавьте FMI: например <b>{spn}/1</b>.',
      stepParam: 'параметр', knownFailures: 'известные отказы {brand}',
      stepNeedFmi: 'нужен FMI',
      needFmiText: 'Это вторая половина кода, она говорит <b>что именно</b> с этим параметром не так. Введите её вместе с номером: например <span class="mono">{spn}/1</span>.',
      stepUrgency: 'срочность',
      urgentText: '<span class="crit">Критично</span> — остановиться при первой безопасной возможности, не тянуть.',
      notUrgentText: '<span class="warn">Ехать можно</span> — но показать код на ближайшем ТО.',
      unknownSpnNote: 'Этого SPN нет в справочнике — скорее всего, код фирменный. Попробуйте выбрать марку выше.',
      loadError: 'Не загрузился словарь — обновите страницу.',
      spnTooBig: 'SPN {spn} — такого SPN нет в J1939 (номера бывают до 524287).',
      needSpnFmi: 'Введите SPN и FMI, например <b>100.1</b> или <b>SPN 100 FMI 1</b>.',
      notParsed: 'не разобрали: {items}',
      dealerAtBrands: 'у марок: {brands}',
      brandlessAsk: 'Поискать у марок',
      brandlessNone: 'у марок такого номера нет',
      sysEnginebrake: 'моторный тормоз',
      sourceLabel: 'источник: {src}', fmiNonstandard: 'FMI {fmi}: значение не стандартное — смотрите расшифровку марки',
      commonTitle: 'Частые коды неисправностей',
      bySituation: 'Если номера кода нет',
      byBrand: 'По маркам',
      allCodes: 'Все коды ошибок',
      allBrands: 'Все марки',
      allProblems: 'Все неисправности',
      casCount: 'кодов в разборе: {n}',
      casRoot: 'вероятная первопричина',
      casCons: 'следствия — отдельно не чинятся',
      casSolo: 'не связано с первопричиной',
      casTodo: 'что сделать сейчас',
      casWhyChain: 'Остальные коды в списке обычно приходят следом за этим — сначала устраняют его.',
      casWhySingle: 'Остальное в списке с этим кодом напрямую не связано.',
      vStop: 'Ехать нельзя',
      vStopSub: 'Остановиться при первой безопасной возможности, дальше не тянуть.',
      vWarn: 'Ехать можно',
      vWarnSub: 'Ниже — сколько есть времени и что будет, если тянуть.',
      shareLabel: 'Отослать разбор',
      shareDone: 'Ссылка скопирована',
      sysScr: 'AdBlue / выхлоп', sysOil: 'смазка', sysCool: 'охлаждение',
      sysFuel: 'топливо', sysAir: 'впуск / наддув', sysPower: 'питание',
      sysCan: 'CAN-шина', sysBrake: 'тормоза', sysTrans: 'трансмиссия',
      sysProt: 'защита двигателя', sysOther: 'прочее',
      actScr: 'Долей AdBlue до полного бака. Если бак полный — дело в дозировании или качестве реагента, нужен сканер.',
      actOil: 'Заглуши двигатель. Проверь уровень масла щупом и осмотри низ на течи. Не заводи, пока давление не восстановится.',
      actCool: 'Дай двигателю остыть — пробку расширительного бачка на горячем не открывай. Потом проверь уровень и патрубки.',
      actFuel: 'Проверь топливный фильтр и отстойник, слей воду. На морозе — парафинизация солярки.',
      actAir: 'Осмотри воздушный фильтр и патрубки наддува: подсос и трещины дают именно такие коды.',
      actPower: 'Проверь клеммы АКБ и массу — окисление и слабая затяжка сыплют ложные коды по всей машине. На заведённом норма 27–29 В.',
      actCan: 'Смотри разъёмы и жгут: обрыв витой пары CAN валит связь у всех блоков разом.',
      actBrake: 'Дай накачать пневмосистему до рабочего давления, послушай утечки. С неисправными тормозами не едешь.',
      actDefault: 'Запиши коды и покажи их на сервисе — по этому набору нужен сканер и осмотр на месте.',
      freqOil: "Давление масла",
      freqCool: "Температура ОЖ",
      freqWater: "Вода в топливе",
      freqBoost: "Давление наддува",
      freqVolt: "Напряжение АКБ",
      freqAdblue: "Уровень AdBlue",
      freqDpf: "Сажевый фильтр",
      freqTorque: "Ограничение момента",
      freqCan: "CAN-шина",
      symCheck: "Загорелся Check Engine",
      symAdblue: "Ошибка AdBlue",
      symPower: "Упала мощность",
      symLowOil: "Низкое давление масла",
      symOverheat: "Перегрев двигателя",
      symDpfClog: "Забит сажевый фильтр",
      symWater: "Вода в топливе",
      symAllCodes: "Ошибки по всей машине",
      symNoStart: "Не заводится",
      symStalls: "Глохнет на ходу",
      symMisfire: "Троит двигатель",
      symBlackSmoke: "Чёрный дым",
      symWhiteSmoke: "Белый дым",
      symBlueSmoke: "Синий дым",
      symFuelUse: "Большой расход топлива",
      symNoRegen: "Не идёт регенерация",
      symAdbluePump: "Не качает AdBlue",
      symNox: "Ошибка датчика NOx",
      symAlt: "Не заряжает генератор",
      symAir: "Не набирает воздух",
      symAbsLamp: "Горит лампа ABS",
      symParkBrake: "Не снимается стояночный тормоз",
      symGears: "Не переключаются передачи",
      symClutch: "Пробуксовывает сцепление",
      symRetarder: "Ошибка ретардера",
      symUphill: "Греется в гору",
      symTacho: "Ошибка тахографа",
      symEngineBrake: "Не работает моторный тормоз",
      brandKamazLbl: "КамАЗ",
      brandYamzLbl: "ЯМЗ",
      brandGazLbl: "ГАЗ",
      brandMazLbl: "МАЗ",
      brandKrazLbl: "КрАЗ",
      brandUralLbl: "Урал",
      brandPlanarLbl: "Планар",
      brandTeplostarLbl: "Теплостар"
    },
    en: {
      pageTitle: 'Truck fault code — SPN/FMI and dealer code lookup',
      langOffer: 'This page is available in English',
      metaDescription: 'Free truck fault code lookup: J1939 standard (SPN/FMI) and factory tables for 80+ makes. Enter a code from your scanner or dashboard.',
      h1: 'The <em>Check&nbsp;Engine</em> light is on — what does the code mean?',
      purposeStats: '39,000+ fault codes across 80+ makes and systems',
      purposeDo: 'Enter one code — or the whole fault list exactly as it is: separated by commas, spaces or line breaks. One fault drags five or six codes along — we show which one is the cause and which just followed, and tell you whether it’s safe to drive.',
      goBtn: 'Decode',
      modeGroup: 'Search mode',
      modeMotor: 'Engine & ECUs',
      modeHeater: 'Heater',
      modeTacho: 'Tachograph',
      heaterHint: 'Code from panel: 031, E-031, F09',
      heaterEmpty: 'Enter a heater panel code, e.g. <b>031</b>, <b>E-031</b>, <b>F09</b> or <b>12</b>.',
      heaterBadCode: 'This does not look like a heater code. Enter digits, e.g. <b>031</b>, <b>E-031</b>, <b>F09</b> or <b>12</b>.',
      heaterNotFound: 'Code not found in the {list} tables. Check the heater brand.',
      heaterNotFoundOne: 'Code <b>{code}</b> not found in the {brand} table. Check the heater brand.',
      brandGroupHeaters: 'Heaters',
      brandGroupTacho: 'Tachographs',
      tachoHint: 'Code or text from the tachograph screen',
      tachoNone: 'Not found: check the tachograph brand or enter the text from the screen',
      tachoPickBrand: 'Pick a tachograph brand in the list above.',
      tachoNotFound: 'Code not found in the {brand} table.',
      codeEmpty: 'Enter a code.',
      demoTag: 'example',
      brandDefault: '— any make —',
      brandGroupVehicles: 'Vehicle makes',
      brandGroupSystems: 'Systems & components',
      midDefault: '— select module —',
      needMid: 'For this brand the code is built from a module (MID) and a parameter. Pick the module above — e.g. “Engine” or “ABS” — then enter the rest of the code with FMI, e.g. <b>P100 FMI 4</b>.',
      standardAuto: 'Detect automatically',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: 'Dealer / OBD code',
      dataLangNote: 'Fault names and factory tables in the database are in Russian; the interface and the standard FMI meanings below are translated.',
      printLabel: 'Print',
      themeDay: 'Day theme',
      themeNight: 'Night theme',
      footText: 'This reference explains what a code means — it doesn’t diagnose the truck. The final call is always with a person who has the equipment. Questions — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>.',
      langAria: 'Page language',
      copyMail: 'Copy address',
      copied: 'Copied',
      emptyPrompt: 'Enter a code — for example <b>SPN 100 FMI 1</b> or just <b>100/1</b>.',
      badCode: 'Couldn’t parse this code in the selected standard. Try “Detect automatically” or the format <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b>.',
      pcodeNotFound: 'Dealer code <b>{code}</b> not found in the database. These codes differ by make — double-check the spelling.',
      pcodeSearching: 'Searching…',
      pcodeApiError: 'No connection to the code database — check your internet and try again.',
      dealerBase: 'dealer database — {brand}',
      dealerOffline: 'The dealer database is unavailable right now — only the factory table is shown.',
      dailyLimit: 'Daily search limit reached (50 per day). Please try again tomorrow.',
      scanStep: 'scanner code',
      fmiOwn: 'FMI per the unit maker\'s table',
      j1939Caption: 'Per J1939 standard (Bosch engines and other units with standard numbering)',
      blinkLimit: 'Limit', blinkCode: 'blink {n}',
      blinkNotFound: 'Blink code <b>{n}</b> not found in the KAMAZ Euro-3 (Bosch MS 6.1) table.',
      cumminsFcLabel: 'Cummins ISB 6.7, FC code {n}',
      scanMany: 'Code <b>{code}</b> maps to several dash codes — check which one the cluster shows.',
      stepCode: 'code', stepDecoding: 'meaning',
      donorDecoding: 'From the {brand} table (same supplier unit)',
      factorySource: 'factory table — {brand}', standardSource: 'J1939 standard',
      blinkNotFoundFor: 'Blink code {n} not found in the {brand} table.',
      j1939ForBrand: 'Per J1939 standard — for {brand} this number may mean something else',
      badCodeFor: 'Code not recognised in the {brand} table — check the format.',
      pcodeServerError: 'The code database is temporarily unavailable — try again later.',
      fmiTable: 'FMI {fmi} per the {brand} table',
      midDefault: 'No MID in the code — taking the engine module, MID 128.',
      midTyped: 'The code has MID {mid} — using it instead of the one selected ({sel}).',
      composedSource: 'assembled from {brand} component tables',
      spnNotFound: '<b>SPN {spn}</b> not found in the database — likely a manufacturer-specific code. Try selecting a make above, or add the FMI: e.g. <b>{spn}/1</b>.',
      stepParam: 'parameter', knownFailures: 'known faults — {brand}',
      stepNeedFmi: 'FMI needed',
      needFmiText: 'FMI is the second half of the code — it says <b>exactly what</b> is wrong with this parameter. Enter it together with the number: e.g. <span class="mono">{spn}/1</span>.',
      stepUrgency: 'urgency',
      urgentText: '<span class="crit">Critical</span> — stop as soon as it’s safe to do so, don’t keep driving.',
      notUrgentText: '<span class="warn">Safe to drive</span> — but have the code checked at the next service.',
      unknownSpnNote: 'This SPN isn’t in the database — likely a manufacturer-specific code. Try selecting a make above.',
      loadError: 'The dictionary did not load — refresh the page.',
      spnTooBig: 'SPN {spn} — there is no such SPN in J1939 (numbers go up to 524287).',
      needSpnFmi: 'Enter the SPN and the FMI, for example <b>100.1</b> or <b>SPN 100 FMI 1</b>.',
      notParsed: 'not parsed: {items}',
      dealerAtBrands: 'at makes: {brands}',
      brandlessAsk: 'Search dealer codes',
      brandlessNone: 'no dealer code with this number at the makes',
      sysEnginebrake: 'engine brake',
      sourceLabel: 'source: {src}', fmiNonstandard: 'FMI {fmi}: non-standard value — see the make’s decoding',
      commonTitle: 'Common fault codes',
      bySituation: 'If you don’t have a code number',
      byBrand: 'By make',
      allCodes: 'All fault codes',
      allBrands: 'All makes',
      allProblems: 'All symptoms',
      casCount: 'codes analysed: {n}',
      casRoot: 'likely root cause',
      casCons: 'knock-on codes — not fixed separately',
      casSolo: 'unrelated to the root cause',
      casTodo: 'what to do now',
      casWhyChain: 'The other codes in the list normally follow this one — fix this first.',
      casWhySingle: 'The rest of the list isn’t directly related to this code.',
      vStop: 'Do not drive',
      vStopSub: 'Stop as soon as it’s safe to do so — don’t keep going.',
      vWarn: 'Safe to drive',
      vWarnSub: 'Below — how much time you have and what happens if you keep going.',
      shareLabel: 'Send this report',
      shareDone: 'Link copied',
      sysScr: 'AdBlue / exhaust', sysOil: 'lubrication', sysCool: 'cooling',
      sysFuel: 'fuel', sysAir: 'intake / boost', sysPower: 'power supply',
      sysCan: 'CAN bus', sysBrake: 'brakes', sysTrans: 'transmission',
      sysProt: 'engine protection', sysOther: 'other',
      actScr: 'Fill the AdBlue tank. If it’s already full, the problem is dosing or reductant quality — you need a scanner.',
      actOil: 'Shut the engine down. Check the oil level with the dipstick and look underneath for leaks. Don’t restart until pressure is back.',
      actCool: 'Let the engine cool — never open the expansion tank cap while hot. Then check the level and the hoses.',
      actFuel: 'Check the fuel filter and water trap, drain the water. In cold weather, suspect fuel waxing.',
      actAir: 'Inspect the air filter and charge-air hoses: leaks and cracks produce exactly these codes.',
      actPower: 'Check the battery terminals and earth strap — corrosion and loose clamps throw false codes all over the truck. Running voltage should be 27–29 V.',
      actCan: 'Check connectors and the harness: a broken CAN twisted pair takes out communication for every ECU at once.',
      actBrake: 'Let the air system build to working pressure and listen for leaks. Don’t drive with faulty brakes.',
      actDefault: 'Write the codes down and show them at a workshop — this set needs a scanner and an on-site inspection.',
      freqOil: "Oil pressure",
      freqCool: "Coolant temperature",
      freqWater: "Water in fuel",
      freqBoost: "Boost pressure",
      freqVolt: "Battery voltage",
      freqAdblue: "AdBlue level",
      freqDpf: "Soot filter",
      freqTorque: "Torque limit",
      freqCan: "CAN bus",
      symCheck: "Check Engine light is on",
      symAdblue: "AdBlue error",
      symPower: "Power loss",
      symLowOil: "Low oil pressure",
      symOverheat: "Engine overheating",
      symDpfClog: "Clogged soot filter",
      symWater: "Water in fuel",
      symAllCodes: "Faults all over the truck",
      symNoStart: "Engine won't start",
      symStalls: "Stalls while driving",
      symMisfire: "Engine misfiring",
      symBlackSmoke: "Black exhaust smoke",
      symWhiteSmoke: "White exhaust smoke",
      symBlueSmoke: "Blue exhaust smoke",
      symFuelUse: "High fuel consumption",
      symNoRegen: "DPF regeneration won't start",
      symAdbluePump: "AdBlue pump not dosing",
      symNox: "NOx sensor fault",
      symAlt: "Alternator not charging",
      symAir: "Air pressure won't build up",
      symAbsLamp: "ABS warning light on",
      symParkBrake: "Parking brake won't release",
      symGears: "Gears won't shift",
      symClutch: "Clutch slipping",
      symRetarder: "Retarder fault",
      symUphill: "Overheats on climbs",
      symTacho: "Tachograph fault",
      symEngineBrake: "Engine brake not working",
      brandKamazLbl: "KAMAZ",
      brandYamzLbl: "YaMZ",
      brandGazLbl: "GAZ",
      brandMazLbl: "MAZ",
      brandKrazLbl: "KrAZ",
      brandUralLbl: "Ural",
      brandPlanarLbl: "Planar",
      brandTeplostarLbl: "Teplostar"
    },
    de: {
      pageTitle: 'LKW-Fehlercode — SPN/FMI und Händlercode entschlüsseln',
      langOffer: 'Diese Seite gibt es auf Deutsch',
      metaDescription: 'Kostenlose Entschlüsselung von LKW-Fehlercodes: J1939-Standard (SPN/FMI) und Werkstabellen für 80+ Marken. Code vom Scanner oder Armaturenbrett eingeben.',
      h1: 'Die <em>Check&nbsp;Engine</em>-Leuchte ist an — was bedeutet der Code?',
      purposeStats: '39.000+ Fehlercodes für über 80 Marken und Systeme',
      purposeDo: 'Geben Sie einen Code ein — oder gleich die ganze Fehlerliste, so wie sie ist: getrennt durch Komma, Leerzeichen oder Zeilenumbruch. Ein Defekt zieht fünf bis sechs Codes nach sich — wir zeigen, welcher die Ursache ist und welche nur gefolgt sind, und sagen, ob die Weiterfahrt sicher ist.',
      goBtn: 'Entschlüsseln',
      demoTag: 'Beispiel',
      brandDefault: '— beliebige Marke —',
      brandGroupVehicles: 'Fahrzeugmarken',
      brandGroupSystems: 'Systeme & Komponenten',
      standardAuto: 'Automatisch erkennen',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: 'Händler-/OBD-Code',
      dataLangNote: 'Fehlerbeschreibungen werden auf Englisch angezeigt.',
      printLabel: 'Drucken',
      themeDay: 'Tagmodus',
      themeNight: 'Nachtmodus',
      footText: 'Dieses Nachschlagewerk erklärt, was ein Code bedeutet — es stellt keine Diagnose. Die Entscheidung trifft immer eine Person mit der passenden Ausrüstung. Fragen — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>.',
      langAria: 'Seitensprache',
      copyMail: 'Adresse kopieren',
      copied: 'Kopiert',
      emptyPrompt: 'Code eingeben — zum Beispiel <b>SPN 100 FMI 1</b> oder einfach <b>100/1</b>.',
      badCode: 'Dieser Code konnte im gewählten Standard nicht erkannt werden. Versuchen Sie „Automatisch erkennen“ oder das Format <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b>.',
      pcodeNotFound: 'Händlercode <b>{code}</b> nicht in der Datenbank gefunden. Diese Codes sind je Marke unterschiedlich — Schreibweise prüfen.',
      pcodeSearching: 'Suche läuft…',
      pcodeApiError: 'Händlercode konnte nicht abgerufen werden — Verbindung prüfen und erneut versuchen.',
      dealerBase: 'Händlerdatenbank — {brand}',
      dealerOffline: 'Die Händlerdatenbank ist derzeit nicht erreichbar — nur die Werkstabelle wird angezeigt.',
      dailyLimit: 'Tageslimit für Suchen erreicht (50 pro Tag). Bitte morgen erneut versuchen.',
      scanStep: 'Scanner-Code',
      scanMany: 'Nummer <b>{code}</b> entspricht mehreren Codes im Kombiinstrument — prüfen Sie, welcher angezeigt wird.',
      stepCode: 'Code', stepDecoding: 'Bedeutung',
      factorySource: 'Werkstabelle — {brand}', standardSource: 'J1939-Standard',
      blinkNotFoundFor: 'Blinkcode {n} in der Tabelle {brand} nicht gefunden.',
      j1939ForBrand: 'Nach J1939-Standard — bei {brand} kann diese Nummer etwas anderes bedeuten',
      badCodeFor: 'Code in der Tabelle {brand} nicht erkannt — Format prüfen.',
      pcodeServerError: 'Die Codedatenbank ist vorübergehend nicht verfügbar — später erneut versuchen.',
      fmiTable: 'FMI {fmi} laut Tabelle {brand}',
      midDefault: 'Kein MID im Code — angenommen wird das Motormodul, MID 128.',
      midTyped: 'Der Code enthält MID {mid} — verwendet wird dieser statt der Auswahl ({sel}).',
      spnNotFound: '<b>SPN {spn}</b> nicht in der Datenbank gefunden — vermutlich ein herstellerspezifischer Code. Wählen Sie oben eine Marke, oder ergänzen Sie den FMI: z. B. <b>{spn}/1</b>.',
      stepParam: 'Parameter', knownFailures: 'bekannte Fehler — {brand}',
      stepNeedFmi: 'FMI erforderlich',
      needFmiText: 'Der FMI ist die zweite Hälfte des Codes — er sagt <b>genau</b>, was mit diesem Parameter nicht stimmt. Geben Sie ihn zusammen mit der Nummer ein: z. B. <span class="mono">{spn}/1</span>.',
      stepUrgency: 'Dringlichkeit',
      urgentText: '<span class="crit">Kritisch</span> — bei nächster sicherer Gelegenheit anhalten, nicht weiterfahren.',
      notUrgentText: '<span class="warn">Weiterfahrt möglich</span> — Code aber beim nächsten Service prüfen lassen.',
      unknownSpnNote: 'Dieser SPN ist nicht in der Datenbank — vermutlich ein herstellerspezifischer Code. Wählen Sie oben eine Marke.',
      loadError: 'Das Wörterbuch wurde nicht geladen — bitte Seite neu laden.',
      sourceLabel: 'Quelle: {src}', fmiNonstandard: 'FMI {fmi} (nicht standardisierter Wert)',
      commonTitle: 'Häufige Fehlercodes',
      bySituation: 'Wenn Sie keine Codenummer haben',
      byBrand: 'Nach Marke',
      allCodes: 'Alle Fehlercodes',
      allBrands: 'Alle Marken',
      allProblems: 'Alle Symptome',
      casCount: 'Codes im Befund: {n}',
      casRoot: 'wahrscheinliche Ursache',
      casCons: 'Folgefehler — nicht einzeln reparieren',
      casSolo: 'nicht mit der Ursache verbunden',
      casTodo: 'was jetzt zu tun ist',
      casWhyChain: 'Die übrigen Codes folgen üblicherweise diesem — zuerst diesen beheben.',
      casWhySingle: 'Der Rest der Liste hängt mit diesem Code nicht direkt zusammen.',
      vStop: 'Weiterfahrt nicht möglich',
      vStopSub: 'Anhalten, sobald es sicher möglich ist — nicht weiterfahren.',
      vWarn: 'Weiterfahrt möglich',
      vWarnSub: 'Unten — wie viel Zeit bleibt und was passiert, wenn Sie weiterfahren.',
      shareLabel: 'Auswertung senden',
      shareDone: 'Link kopiert',
      sysScr: 'AdBlue / Abgas', sysOil: 'Schmierung', sysCool: 'Kühlung',
      sysFuel: 'Kraftstoff', sysAir: 'Ansaugung / Ladedruck', sysPower: 'Bordnetz',
      sysCan: 'CAN-Bus', sysBrake: 'Bremsen', sysTrans: 'Getriebe',
      sysProt: 'Motorschutz', sysOther: 'Sonstiges',
      actScr: 'AdBlue-Tank auffüllen. Ist er bereits voll, liegt es an der Dosierung oder der Reagenzqualität — dafür ist ein Diagnosegerät nötig.',
      actOil: 'Motor abstellen. Ölstand mit dem Messstab prüfen und von unten auf Leckagen kontrollieren. Nicht starten, bis der Druck wieder steht.',
      actCool: 'Motor abkühlen lassen — den Deckel des Ausgleichsbehälters niemals im heißen Zustand öffnen. Danach Stand und Schläuche prüfen.',
      actFuel: 'Kraftstofffilter und Wasserabscheider prüfen, Wasser ablassen. Bei Frost an Paraffinausscheidung denken.',
      actAir: 'Luftfilter und Ladeluftschläuche prüfen: Falschluft und Risse erzeugen genau solche Codes.',
      actPower: 'Batteriepole und Masseband prüfen — Korrosion und lose Klemmen erzeugen Fehlercodes im ganzen Fahrzeug. Im Betrieb sind 27–29 V normal.',
      actCan: 'Stecker und Kabelbaum prüfen: eine unterbrochene CAN-Zweidrahtleitung legt die Kommunikation aller Steuergeräte gleichzeitig lahm.',
      actBrake: 'Druckluftanlage auf Betriebsdruck aufbauen lassen und auf Undichtigkeiten hören. Mit defekten Bremsen wird nicht gefahren.',
      actDefault: 'Codes notieren und in der Werkstatt zeigen — dieser Satz erfordert ein Diagnosegerät und eine Sichtprüfung vor Ort.',
      freqOil: "Öldruck",
      freqCool: "Kühlmitteltemperatur",
      freqWater: "Wasser im Kraftstoff",
      freqBoost: "Ladedruck",
      freqVolt: "Batteriespannung",
      freqAdblue: "AdBlue-Füllstand",
      freqDpf: "Partikelfilter",
      freqTorque: "Drehmomentbegrenzung",
      freqCan: "CAN-Bus",
      symCheck: "Check-Engine-Leuchte an",
      symAdblue: "AdBlue-Fehler",
      symPower: "Leistungsverlust",
      symLowOil: "Niedriger Öldruck",
      symOverheat: "Motorüberhitzung",
      symDpfClog: "Verstopfter Partikelfilter",
      symWater: "Wasser im Kraftstoff",
      symAllCodes: "Fehler im ganzen Fahrzeug",
      symNoStart: "Motor startet nicht",
      symStalls: "Geht während der Fahrt aus",
      symMisfire: "Motor läuft unrund",
      symBlackSmoke: "Schwarzer Rauch",
      symWhiteSmoke: "Weißer Rauch",
      symBlueSmoke: "Blauer Rauch",
      symFuelUse: "Hoher Kraftstoffverbrauch",
      symNoRegen: "Keine DPF-Regeneration",
      symAdbluePump: "AdBlue-Pumpe dosiert nicht",
      symNox: "NOx-Sensor-Fehler",
      symAlt: "Lichtmaschine lädt nicht",
      symAir: "Kein Luftdruckaufbau",
      symAbsLamp: "ABS-Leuchte an",
      symParkBrake: "Feststellbremse löst nicht",
      symGears: "Gänge schalten nicht",
      symClutch: "Kupplung rutscht",
      symRetarder: "Retarder-Fehler",
      symUphill: "Überhitzt am Berg",
      symTacho: "Tachograph-Fehler",
      symEngineBrake: "Motorbremse ohne Wirkung",
      brandKamazLbl: "KAMAZ",
      brandYamzLbl: "YaMZ",
      brandGazLbl: "GAZ",
      brandMazLbl: "MAZ",
      brandKrazLbl: "KrAZ",
      brandUralLbl: "Ural",
      brandPlanarLbl: "Planar",
      brandTeplostarLbl: "Teplostar"
    },
    fr: {
      pageTitle: 'Code défaut camion — décodage SPN/FMI et codes constructeur',
      langOffer: 'Cette page existe en français',
      metaDescription: 'Décodage gratuit des codes défaut camion : norme J1939 (SPN/FMI) et tables constructeur pour 80+ marques. Entrez le code du scanner ou du tableau de bord.',
      h1: 'Le voyant <em>Check&nbsp;Engine</em> est allumé — que signifie le code ?',
      purposeStats: '39 000+ codes défaut pour plus de 80 marques et systèmes',
      purposeDo: 'Saisissez un code — ou toute la liste des défauts, telle quelle : séparés par des virgules, des espaces ou des retours à la ligne. Une panne entraîne cinq ou six codes — nous montrons lequel est la cause et lesquels ont suivi, et vous disons si vous pouvez rouler.',
      goBtn: 'Décoder',
      demoTag: 'exemple',
      brandDefault: '— toutes marques —',
      brandGroupVehicles: 'Marques de véhicules',
      brandGroupSystems: 'Systèmes et composants',
      standardAuto: 'Détecter automatiquement',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: 'Code constructeur / OBD',
      dataLangNote: 'Les descriptions des défauts sont affichées en anglais.',
      printLabel: 'Imprimer',
      themeDay: 'Thème clair',
      themeNight: 'Thème sombre',
      footText: 'Ce répertoire explique ce que signifie un code — il ne pose pas de diagnostic. La décision revient toujours à une personne équipée du matériel nécessaire. Questions — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>.',
      langAria: 'Langue de la page',
      copyMail: 'Copier l’adresse',
      copied: 'Copié',
      emptyPrompt: 'Entrez un code — par exemple <b>SPN 100 FMI 1</b> ou simplement <b>100/1</b>.',
      badCode: 'Impossible d’analyser ce code dans la norme sélectionnée. Essayez « Détecter automatiquement » ou le format <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b>.',
      pcodeNotFound: 'Code constructeur <b>{code}</b> introuvable dans la base. Ces codes diffèrent selon la marque — vérifiez l’orthographe.',
      pcodeSearching: 'Recherche en cours…',
      pcodeApiError: 'Impossible de récupérer le code constructeur — vérifiez votre connexion et réessayez.',
      dealerBase: 'base concessionnaire — {brand}',
      dealerOffline: 'La base concessionnaire est indisponible — seule la table constructeur est affichée.',
      dailyLimit: 'Limite quotidienne de recherches atteinte (50 par jour). Réessayez demain.',
      scanStep: 'code de la valise',
      scanMany: 'Le numéro <b>{code}</b> correspond à plusieurs codes au tableau de bord — vérifiez celui qui s’affiche.',
      stepCode: 'code', stepDecoding: 'signification',
      factorySource: 'table constructeur — {brand}', standardSource: 'norme J1939',
      blinkNotFoundFor: 'Code clignotant {n} introuvable dans la table {brand}.',
      j1939ForBrand: 'Selon la norme J1939 — chez {brand} ce numéro peut signifier autre chose',
      badCodeFor: 'Code non reconnu dans la table {brand} — vérifiez le format.',
      pcodeServerError: 'La base de codes est momentanément indisponible — réessayez plus tard.',
      fmiTable: 'FMI {fmi} selon la table {brand}',
      midDefault: 'Aucun MID dans le code — on prend le module moteur, MID 128.',
      midTyped: 'Le code indique MID {mid} — on l’utilise au lieu du choix ({sel}).',
      spnNotFound: '<b>SPN {spn}</b> introuvable dans la base — probablement un code propre au constructeur. Essayez de choisir une marque ci-dessus, ou ajoutez le FMI : par ex. <b>{spn}/1</b>.',
      stepParam: 'paramètre', knownFailures: 'pannes connues — {brand}',
      stepNeedFmi: 'FMI requis',
      needFmiText: 'Le FMI est la seconde moitié du code — il indique <b>précisément</b> ce qui ne va pas avec ce paramètre. Entrez-le avec le numéro : par ex. <span class="mono">{spn}/1</span>.',
      stepUrgency: 'urgence',
      urgentText: '<span class="crit">Critique</span> — arrêtez-vous dès que possible en sécurité, ne continuez pas à rouler.',
      notUrgentText: '<span class="warn">Vous pouvez rouler</span> — mais faites vérifier le code lors du prochain entretien.',
      unknownSpnNote: 'Ce SPN n’est pas dans la base — probablement un code propre au constructeur. Essayez de choisir une marque ci-dessus.',
      loadError: 'Le dictionnaire ne s’est pas chargé — actualisez la page.',
      sourceLabel: 'source : {src}', fmiNonstandard: 'FMI {fmi} (valeur non standard)',
      commonTitle: 'Codes défaut fréquents',
      bySituation: 'Si vous n’avez pas de numéro de code',
      byBrand: 'Par marque',
      allCodes: 'Tous les codes défaut',
      allBrands: 'Toutes les marques',
      allProblems: 'Tous les symptômes',
      casCount: 'codes analysés : {n}',
      casRoot: 'cause probable',
      casCons: 'conséquences — ne se réparent pas séparément',
      casSolo: 'sans lien avec la cause',
      casTodo: 'que faire maintenant',
      casWhyChain: 'Les autres codes suivent habituellement celui-ci — traitez-le en premier.',
      casWhySingle: 'Le reste de la liste n’est pas directement lié à ce code.',
      vStop: 'Ne pas rouler',
      vStopSub: 'Arrêtez-vous dès que c’est possible en sécurité — ne continuez pas.',
      vWarn: 'Vous pouvez rouler',
      vWarnSub: 'Ci-dessous — combien de temps il vous reste et ce qui arrive si vous continuez.',
      shareLabel: 'Envoyer l’analyse',
      shareDone: 'Lien copié',
      sysScr: 'AdBlue / échappement', sysOil: 'lubrification', sysCool: 'refroidissement',
      sysFuel: 'carburant', sysAir: 'admission / suralimentation', sysPower: 'alimentation',
      sysCan: 'bus CAN', sysBrake: 'freins', sysTrans: 'transmission',
      sysProt: 'protection moteur', sysOther: 'divers',
      actScr: 'Faites le plein d’AdBlue. Si le réservoir est déjà plein, le problème vient du dosage ou de la qualité du réactif — une valise est nécessaire.',
      actOil: 'Coupez le moteur. Vérifiez le niveau d’huile à la jauge et inspectez le dessous pour des fuites. Ne redémarrez pas tant que la pression n’est pas rétablie.',
      actCool: 'Laissez refroidir le moteur — n’ouvrez jamais le bouchon du vase d’expansion à chaud. Vérifiez ensuite le niveau et les durites.',
      actFuel: 'Vérifiez le filtre à carburant et le décanteur, purgez l’eau. Par temps froid, pensez à la paraffine dans le gazole.',
      actAir: 'Contrôlez le filtre à air et les durites de suralimentation : les prises d’air et les fissures donnent exactement ces codes.',
      actPower: 'Vérifiez les cosses de batterie et la tresse de masse — la corrosion et un serrage faible génèrent de faux codes dans tout le camion. Moteur tournant, 27–29 V est la norme.',
      actCan: 'Inspectez les connecteurs et le faisceau : une paire torsadée CAN coupée met hors service la communication de tous les calculateurs à la fois.',
      actBrake: 'Laissez le circuit d’air monter à la pression de service et écoutez les fuites. On ne roule pas avec des freins défectueux.',
      actDefault: 'Notez les codes et montrez-les à un atelier — cet ensemble demande une valise et une inspection sur place.',
      freqOil: "Pression d'huile",
      freqCool: "Température du liquide de refroidissement",
      freqWater: "Eau dans le carburant",
      freqBoost: "Pression de suralimentation",
      freqVolt: "Tension de batterie",
      freqAdblue: "Niveau d'AdBlue",
      freqDpf: "Filtre à particules",
      freqTorque: "Limitation de couple",
      freqCan: "Bus CAN",
      symCheck: "Voyant Check Engine allumé",
      symAdblue: "Erreur AdBlue",
      symPower: "Perte de puissance",
      symLowOil: "Pression d'huile basse",
      symOverheat: "Surchauffe moteur",
      symDpfClog: "Filtre à particules colmaté",
      symWater: "Eau dans le carburant",
      symAllCodes: "Défauts sur tout le camion",
      symNoStart: "Le moteur ne démarre pas",
      symStalls: "Cale en roulant",
      symMisfire: "Ratés d'allumage",
      symBlackSmoke: "Fumée noire",
      symWhiteSmoke: "Fumée blanche",
      symBlueSmoke: "Fumée bleue",
      symFuelUse: "Consommation excessive",
      symNoRegen: "Pas de régénération du FAP",
      symAdbluePump: "Pompe AdBlue ne dose pas",
      symNox: "Défaut du capteur NOx",
      symAlt: "L'alternateur ne charge pas",
      symAir: "Pas de montée en pression d'air",
      symAbsLamp: "Témoin ABS allumé",
      symParkBrake: "Frein de stationnement bloqué",
      symGears: "Les vitesses ne passent pas",
      symClutch: "Embrayage qui glisse",
      symRetarder: "Défaut du ralentisseur",
      symUphill: "Surchauffe en côte",
      symTacho: "Défaut du tachygraphe",
      symEngineBrake: "Frein moteur inopérant",
      brandKamazLbl: "KAMAZ",
      brandYamzLbl: "YaMZ",
      brandGazLbl: "GAZ",
      brandMazLbl: "MAZ",
      brandKrazLbl: "KrAZ",
      brandUralLbl: "Ural",
      brandPlanarLbl: "Planar",
      brandTeplostarLbl: "Teplostar"
    },
    es: {
      pageTitle: 'Código de avería de camión — SPN/FMI y códigos de concesionario',
      langOffer: 'Esta página está disponible en español',
      metaDescription: 'Decodificación gratuita de códigos de avería de camiones: norma J1939 (SPN/FMI) y tablas de fábrica de 80+ marcas. Introduce el código del escáner o del salpicadero.',
      h1: 'Se ha encendido el testigo <em>Check&nbsp;Engine</em> — ¿qué significa el código?',
      purposeStats: 'Más de 39.000 códigos de falla en más de 80 marcas y sistemas',
      purposeDo: 'Introduzca un código — o la lista completa de averías, tal cual: separados por comas, espacios o saltos de línea. Una avería arrastra cinco o seis códigos — le mostramos cuál es la causa y cuáles vinieron detrás, y le decimos si puede circular.',
      goBtn: 'Decodificar',
      demoTag: 'ejemplo',
      brandDefault: '— cualquier marca —',
      brandGroupVehicles: 'Marcas de vehículos',
      brandGroupSystems: 'Sistemas y componentes',
      standardAuto: 'Detectar automáticamente',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: 'Código de concesionario / OBD',
      dataLangNote: 'Las descripciones de las averías se muestran en inglés.',
      printLabel: 'Imprimir',
      themeDay: 'Tema claro',
      themeNight: 'Tema oscuro',
      footText: 'Esta referencia explica qué significa un código — no diagnostica el camión. La decisión final siempre corresponde a una persona con el equipo adecuado. Preguntas — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>.',
      langAria: 'Idioma de la página',
      copyMail: 'Copiar dirección',
      copied: 'Copiado',
      emptyPrompt: 'Introduce un código — por ejemplo <b>SPN 100 FMI 1</b> o simplemente <b>100/1</b>.',
      badCode: 'No se pudo interpretar este código en la norma seleccionada. Prueba "Detectar automáticamente" o el formato <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b>.',
      pcodeNotFound: 'Código de concesionario <b>{code}</b> no encontrado en la base de datos. Estos códigos varían según la marca — revisa la escritura.',
      pcodeSearching: 'Buscando…',
      pcodeApiError: 'No se pudo obtener el código de concesionario — comprueba tu conexión e inténtalo de nuevo.',
      dealerBase: 'base de concesionarios — {brand}',
      dealerOffline: 'La base de concesionarios no está disponible — solo se muestra la tabla de fábrica.',
      dailyLimit: 'Se alcanzó el límite diario de búsquedas (50 al día). Inténtalo mañana.',
      scanStep: 'código del escáner',
      scanMany: 'El número <b>{code}</b> corresponde a varios códigos del cuadro — comprueba cuál se muestra.',
      stepCode: 'código', stepDecoding: 'significado',
      factorySource: 'tabla de fábrica — {brand}', standardSource: 'norma J1939',
      blinkNotFoundFor: 'Código de parpadeo {n} no encontrado en la tabla de {brand}.',
      j1939ForBrand: 'Según la norma J1939 — en {brand} este número puede significar otra cosa',
      badCodeFor: 'Código no reconocido en la tabla de {brand} — revisa el formato.',
      pcodeServerError: 'La base de códigos no está disponible ahora — inténtalo más tarde.',
      fmiTable: 'FMI {fmi} según la tabla de {brand}',
      midDefault: 'El código no indica MID — se toma el módulo del motor, MID 128.',
      midTyped: 'El código indica MID {mid} — se usa en lugar del seleccionado ({sel}).',
      spnNotFound: '<b>SPN {spn}</b> no encontrado en la base de datos — probablemente un código específico del fabricante. Prueba a elegir una marca arriba, o añade el FMI: p. ej. <b>{spn}/1</b>.',
      stepParam: 'parámetro', knownFailures: 'averías conocidas — {brand}',
      stepNeedFmi: 'falta el FMI',
      needFmiText: 'El FMI es la segunda mitad del código — indica <b>exactamente qué</b> falla con este parámetro. Introdúcelo junto con el número: p. ej. <span class="mono">{spn}/1</span>.',
      stepUrgency: 'urgencia',
      urgentText: '<span class="crit">Crítico</span> — detente en cuanto sea seguro hacerlo, no sigas conduciendo.',
      notUrgentText: '<span class="warn">Se puede seguir conduciendo</span> — pero revisa el código en el próximo mantenimiento.',
      unknownSpnNote: 'Este SPN no está en la base de datos — probablemente un código específico del fabricante. Prueba a elegir una marca arriba.',
      loadError: 'El diccionario no se ha cargado — actualiza la página.',
      sourceLabel: 'fuente: {src}', fmiNonstandard: 'FMI {fmi} (valor no estándar)',
      commonTitle: 'Códigos de avería frecuentes',
      bySituation: 'Si no tiene el número del código',
      byBrand: 'Por marca',
      allCodes: 'Todos los códigos de avería',
      allBrands: 'Todas las marcas',
      allProblems: 'Todos los síntomas',
      casCount: 'códigos analizados: {n}',
      casRoot: 'causa probable',
      casCons: 'consecuencias — no se reparan por separado',
      casSolo: 'sin relación con la causa',
      casTodo: 'qué hacer ahora',
      casWhyChain: 'Los demás códigos suelen aparecer después de este — resúelvalo primero.',
      casWhySingle: 'El resto de la lista no está directamente relacionado con este código.',
      vStop: 'No circule',
      vStopSub: 'Deténgase en cuanto sea seguro — no siga conduciendo.',
      vWarn: 'Puede circular',
      vWarnSub: 'Abajo — cuánto tiempo tiene y qué pasa si sigue circulando.',
      shareLabel: 'Enviar el informe',
      shareDone: 'Enlace copiado',
      sysScr: 'AdBlue / escape', sysOil: 'lubricación', sysCool: 'refrigeración',
      sysFuel: 'combustible', sysAir: 'admisión / sobrealimentación', sysPower: 'alimentación',
      sysCan: 'bus CAN', sysBrake: 'frenos', sysTrans: 'transmisión',
      sysProt: 'protección del motor', sysOther: 'otros',
      actScr: 'Llene el depósito de AdBlue. Si ya está lleno, el problema es la dosificación o la calidad del reactivo — hace falta un escáner.',
      actOil: 'Pare el motor. Compruebe el nivel de aceite con la varilla y revise los bajos en busca de fugas. No lo arranque hasta que se recupere la presión.',
      actCool: 'Deje enfriar el motor — nunca abra el tapón del depósito de expansión en caliente. Después compruebe el nivel y los manguitos.',
      actFuel: 'Revise el filtro de combustible y el decantador, purgue el agua. Con frío, sospeche de la parafina del gasóleo.',
      actAir: 'Inspeccione el filtro de aire y los manguitos de sobrealimentación: las entradas de aire y las grietas dan exactamente estos códigos.',
      actPower: 'Revise los bornes de la batería y la masa — la corrosión y el apriete flojo generan códigos falsos por todo el camión. Con el motor en marcha, 27–29 V es lo normal.',
      actCan: 'Revise conectores y mazo: un par trenzado CAN cortado deja sin comunicación a todas las centralitas a la vez.',
      actBrake: 'Deje que el circuito neumático alcance la presión de trabajo y escuche si hay fugas. Con los frenos averiados no se circula.',
      actDefault: 'Anote los códigos y muéstrelos en un taller — este conjunto requiere escáner e inspección presencial.',
      freqOil: "Presión de aceite",
      freqCool: "Temperatura del refrigerante",
      freqWater: "Agua en el combustible",
      freqBoost: "Presión de sobrealimentación",
      freqVolt: "Tensión de batería",
      freqAdblue: "Nivel de AdBlue",
      freqDpf: "Filtro de partículas",
      freqTorque: "Limitación de par",
      freqCan: "Bus CAN",
      symCheck: "Testigo Check Engine encendido",
      symAdblue: "Error de AdBlue",
      symPower: "Pérdida de potencia",
      symLowOil: "Presión de aceite baja",
      symOverheat: "Sobrecalentamiento del motor",
      symDpfClog: "Filtro de partículas obstruido",
      symWater: "Agua en el combustible",
      symAllCodes: "Averías en todo el camión",
      symNoStart: "El motor no arranca",
      symStalls: "Se para en marcha",
      symMisfire: "Fallos de encendido",
      symBlackSmoke: "Humo negro",
      symWhiteSmoke: "Humo blanco",
      symBlueSmoke: "Humo azul",
      symFuelUse: "Consumo excesivo de combustible",
      symNoRegen: "No arranca la regeneración del DPF",
      symAdbluePump: "La bomba de AdBlue no dosifica",
      symNox: "Fallo del sensor NOx",
      symAlt: "El alternador no carga",
      symAir: "No sube la presión de aire",
      symAbsLamp: "Testigo ABS encendido",
      symParkBrake: "El freno de estacionamiento no suelta",
      symGears: "No entran las marchas",
      symClutch: "El embrague patina",
      symRetarder: "Fallo del ralentizador",
      symUphill: "Se calienta en subida",
      symTacho: "Fallo del tacógrafo",
      symEngineBrake: "El freno motor no funciona",
      brandKamazLbl: "KAMAZ",
      brandYamzLbl: "YaMZ",
      brandGazLbl: "GAZ",
      brandMazLbl: "MAZ",
      brandKrazLbl: "KrAZ",
      brandUralLbl: "Ural",
      brandPlanarLbl: "Planar",
      brandTeplostarLbl: "Teplostar"
    },
    pt: {
      pageTitle: 'Código de falha de caminhão — SPN/FMI e códigos de concessionária',
      langOffer: 'Esta página está disponível em português',
      metaDescription: 'Decodificação gratuita de códigos de falha de caminhões: norma J1939 (SPN/FMI) e tabelas de fábrica de 80+ marcas. Digite o código do scanner ou do painel.',
      h1: 'A luz de <em>Check&nbsp;Engine</em> acendeu — o que significa o código?',
      purposeStats: 'Mais de 39.000 códigos de falha em mais de 80 marcas e sistemas',
      purposeDo: 'Introduza um código — ou a lista completa de avarias, tal como está: separados por vírgulas, espaços ou quebras de linha. Uma avaria arrasta cinco ou seis códigos — mostramos qual é a causa e quais vieram a seguir, e dizemos se pode circular.',
      goBtn: 'Decodificar',
      demoTag: 'exemplo',
      brandDefault: '— qualquer marca —',
      brandGroupVehicles: 'Marcas de veículos',
      brandGroupSystems: 'Sistemas e componentes',
      standardAuto: 'Detectar automaticamente',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: 'Código de concessionária / OBD',
      dataLangNote: 'As descrições das falhas são apresentadas em inglês.',
      printLabel: 'Imprimir',
      themeDay: 'Tema claro',
      themeNight: 'Tema escuro',
      footText: 'Esta referência explica o que um código significa — não faz diagnóstico do caminhão. A decisão final é sempre de uma pessoa com o equipamento adequado. Dúvidas — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>.',
      langAria: 'Idioma da página',
      copyMail: 'Copiar endereço',
      copied: 'Copiado',
      emptyPrompt: 'Digite um código — por exemplo <b>SPN 100 FMI 1</b> ou apenas <b>100/1</b>.',
      badCode: 'Não foi possível interpretar este código na norma selecionada. Tente "Detectar automaticamente" ou o formato <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b>.',
      pcodeNotFound: 'Código de concessionária <b>{code}</b> não encontrado no banco de dados. Esses códigos variam por marca — verifique a grafia.',
      pcodeSearching: 'Buscando…',
      pcodeApiError: 'Não foi possível obter o código de concessionária — verifique sua conexão e tente novamente.',
      dealerBase: 'base de concessionárias — {brand}',
      dealerOffline: 'A base de concessionárias está indisponível — mostrada apenas a tabela de fábrica.',
      dailyLimit: 'Limite diário de pesquisas atingido (50 por dia). Tente novamente amanhã.',
      scanStep: 'código do scanner',
      scanMany: 'O número <b>{code}</b> corresponde a vários códigos no painel — verifique qual aparece.',
      stepCode: 'código', stepDecoding: 'significado',
      factorySource: 'tabela de fábrica — {brand}', standardSource: 'norma J1939',
      blinkNotFoundFor: 'Código de pisca {n} não encontrado na tabela {brand}.',
      j1939ForBrand: 'Pela norma J1939 — na {brand} este número pode significar outra coisa',
      badCodeFor: 'Código não reconhecido na tabela {brand} — verifique o formato.',
      pcodeServerError: 'A base de códigos está indisponível no momento — tente mais tarde.',
      fmiTable: 'FMI {fmi} conforme a tabela {brand}',
      midDefault: 'O código não indica MID — considera-se o módulo do motor, MID 128.',
      midTyped: 'O código indica MID {mid} — usamos esse em vez do selecionado ({sel}).',
      spnNotFound: '<b>SPN {spn}</b> não encontrado no banco de dados — provavelmente um código específico do fabricante. Tente selecionar uma marca acima, ou adicione o FMI: ex. <b>{spn}/1</b>.',
      stepParam: 'parâmetro', knownFailures: 'falhas conhecidas — {brand}',
      stepNeedFmi: 'falta o FMI',
      needFmiText: 'O FMI é a segunda metade do código — indica <b>exatamente o que</b> está errado com esse parâmetro. Digite-o junto com o número: ex. <span class="mono">{spn}/1</span>.',
      stepUrgency: 'urgência',
      urgentText: '<span class="crit">Crítico</span> — pare assim que for seguro fazê-lo, não continue dirigindo.',
      notUrgentText: '<span class="warn">Pode continuar dirigindo</span> — mas verifique o código na próxima revisão.',
      unknownSpnNote: 'Este SPN não está no banco de dados — provavelmente um código específico do fabricante. Tente selecionar uma marca acima.',
      loadError: 'O dicionário não foi carregado — atualize a página.',
      sourceLabel: 'fonte: {src}', fmiNonstandard: 'FMI {fmi} (valor não padrão)',
      commonTitle: 'Códigos de falha frequentes',
      bySituation: 'Se não tiver o número do código',
      byBrand: 'Por marca',
      allCodes: 'Todos os códigos de falha',
      allBrands: 'Todas as marcas',
      allProblems: 'Todos os sintomas',
      casCount: 'códigos analisados: {n}',
      casRoot: 'causa provável',
      casCons: 'consequências — não se reparam separadamente',
      casSolo: 'sem relação com a causa',
      casTodo: 'o que fazer agora',
      casWhyChain: 'Os outros códigos costumam vir depois deste — resolva-o primeiro.',
      casWhySingle: 'O resto da lista não está diretamente relacionado com este código.',
      vStop: 'Não circule',
      vStopSub: 'Pare assim que for seguro — não continue a conduzir.',
      vWarn: 'Pode circular',
      vWarnSub: 'Abaixo — quanto tempo tem e o que acontece se continuar.',
      shareLabel: 'Enviar a análise',
      shareDone: 'Link copiado',
      sysScr: 'AdBlue / escape', sysOil: 'lubrificação', sysCool: 'arrefecimento',
      sysFuel: 'combustível', sysAir: 'admissão / sobrealimentação', sysPower: 'alimentação',
      sysCan: 'barramento CAN', sysBrake: 'travões', sysTrans: 'transmissão',
      sysProt: 'proteção do motor', sysOther: 'outros',
      actScr: 'Ateşte o depósito de AdBlue. Se já estiver cheio, o problema é a dosagem ou a qualidade do reagente — é preciso um scanner.',
      actOil: 'Desligue o motor. Verifique o nível de óleo com a vareta e inspecione por baixo à procura de fugas. Não arranque até a pressão voltar.',
      actCool: 'Deixe o motor arrefecer — nunca abra o tampão do depósito de expansão a quente. Depois verifique o nível e os tubos.',
      actFuel: 'Verifique o filtro de combustível e o decantador, purgue a água. Com frio, suspeite de parafina no gasóleo.',
      actAir: 'Inspecione o filtro de ar e os tubos de sobrealimentação: entradas de ar e fissuras dão exatamente estes códigos.',
      actPower: 'Verifique os bornes da bateria e a massa — corrosão e aperto fraco geram códigos falsos por todo o camião. Com o motor a trabalhar, 27–29 V é o normal.',
      actCan: 'Verifique conectores e cablagem: um par entrançado CAN partido deixa todas as centralinas sem comunicação ao mesmo tempo.',
      actBrake: 'Deixe o circuito pneumático atingir a pressão de trabalho e ouça se há fugas. Com travões avariados não se circula.',
      actDefault: 'Anote os códigos e mostre-os numa oficina — este conjunto exige scanner e inspeção no local.',
      freqOil: "Pressão do óleo",
      freqCool: "Temperatura do líquido de arrefecimento",
      freqWater: "Água no combustível",
      freqBoost: "Pressão de sobrealimentação",
      freqVolt: "Tensão da bateria",
      freqAdblue: "Nível de AdBlue",
      freqDpf: "Filtro de partículas",
      freqTorque: "Limitação de binário",
      freqCan: "Barramento CAN",
      symCheck: "Luz Check Engine acesa",
      symAdblue: "Erro de AdBlue",
      symPower: "Perda de potência",
      symLowOil: "Pressão de óleo baixa",
      symOverheat: "Sobreaquecimento do motor",
      symDpfClog: "Filtro de partículas entupido",
      symWater: "Água no combustível",
      symAllCodes: "Avarias em toda a viatura",
      symNoStart: "O motor não arranca",
      symStalls: "Morre em andamento",
      symMisfire: "Falhas de ignição",
      symBlackSmoke: "Fumo negro",
      symWhiteSmoke: "Fumo branco",
      symBlueSmoke: "Fumo azul",
      symFuelUse: "Consumo excessivo de combustível",
      symNoRegen: "Sem regeneração do DPF",
      symAdbluePump: "Bomba de AdBlue não doseia",
      symNox: "Falha do sensor NOx",
      symAlt: "O alternador não carrega",
      symAir: "Não sobe a pressão de ar",
      symAbsLamp: "Luz ABS acesa",
      symParkBrake: "Travão de mão não solta",
      symGears: "Não engrena as mudanças",
      symClutch: "Embraiagem a patinar",
      symRetarder: "Falha do retardador",
      symUphill: "Aquece na subida",
      symTacho: "Falha do tacógrafo",
      symEngineBrake: "Travão-motor não funciona",
      brandKamazLbl: "KAMAZ",
      brandYamzLbl: "YaMZ",
      brandGazLbl: "GAZ",
      brandMazLbl: "MAZ",
      brandKrazLbl: "KrAZ",
      brandUralLbl: "Ural",
      brandPlanarLbl: "Planar",
      brandTeplostarLbl: "Teplostar"
    },
    pl: {
      pageTitle: 'Kod usterki ciężarówki — SPN/FMI i kody dealerskie',
      langOffer: 'Ta strona jest dostępna po polsku',
      metaDescription: 'Darmowe rozszyfrowanie kodów usterek ciężarówek: norma J1939 (SPN/FMI) i tabele fabryczne 80+ marek. Wpisz kod ze skanera lub z deski rozdzielczej.',
      h1: 'Zapaliła się kontrolka <em>Check&nbsp;Engine</em> — co oznacza kod?',
      purposeStats: '39 000+ kodów usterek dla ponad 80 marek i systemów',
      purposeDo: 'Wpisz kod — albo od razu całą listę usterek, tak jak jest: oddzielone przecinkami, spacjami lub nowymi wierszami. Jedna usterka ciągnie za sobą pięć-sześć kodów — pokażemy, który jest przyczyną, a które pojawiły się po nim, i powiemy, czy można jechać.',
      goBtn: 'Rozszyfruj',
      demoTag: 'przykład',
      brandDefault: '— dowolna marka —',
      brandGroupVehicles: 'Marki pojazdów',
      brandGroupSystems: 'Systemy i podzespoły',
      standardAuto: 'Wykryj automatycznie',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: 'Kod dealerski / OBD',
      dataLangNote: 'Opisy usterek są wyświetlane w języku angielskim.',
      printLabel: 'Drukuj',
      themeDay: 'Motyw dzienny',
      themeNight: 'Motyw nocny',
      footText: 'Ta baza wyjaśnia, co oznacza kod — nie stawia diagnozy. Ostateczna decyzja zawsze należy do osoby dysponującej odpowiednim sprzętem. Pytania — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>.',
      langAria: 'Język strony',
      copyMail: 'Kopiuj adres',
      copied: 'Skopiowano',
      emptyPrompt: 'Wpisz kod — na przykład <b>SPN 100 FMI 1</b> albo po prostu <b>100/1</b>.',
      badCode: 'Nie udało się rozpoznać tego kodu w wybranym standardzie. Spróbuj „Wykryj automatycznie” lub formatu <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b>.',
      pcodeNotFound: 'Kod dealerski <b>{code}</b> nie znaleziony w bazie. Takie kody różnią się między markami — sprawdź zapis.',
      pcodeSearching: 'Szukam…',
      pcodeApiError: 'Nie udało się pobrać kodu dealerskiego — sprawdź połączenie i spróbuj ponownie.',
      dealerBase: 'baza dealerska — {brand}',
      dealerOffline: 'Baza dealerska jest teraz niedostępna — pokazano tylko tabelę fabryczną.',
      dailyLimit: 'Wyczerpano dzienny limit wyszukiwań (50 dziennie). Spróbuj jutro.',
      scanStep: 'kod ze skanera',
      scanMany: 'Numer <b>{code}</b> odpowiada kilku kodom na zestawie wskaźników — sprawdź, który pokazuje panel.',
      stepCode: 'kod', stepDecoding: 'znaczenie',
      factorySource: 'tabela fabryczna — {brand}', standardSource: 'norma J1939',
      blinkNotFoundFor: 'Kodu migania {n} nie znaleziono w tabeli {brand}.',
      j1939ForBrand: 'Według normy J1939 — u marki {brand} ten numer może znaczyć co innego',
      badCodeFor: 'Kodu nie rozpoznano w tabeli {brand} — sprawdź format.',
      pcodeServerError: 'Baza kodów jest chwilowo niedostępna — spróbuj później.',
      fmiTable: 'FMI {fmi} wg tabeli {brand}',
      midDefault: 'Brak MID w kodzie — przyjęto moduł silnika, MID 128.',
      midTyped: 'Kod zawiera MID {mid} — użyto go zamiast wybranego ({sel}).',
      spnNotFound: '<b>SPN {spn}</b> nie znaleziony w bazie — prawdopodobnie kod producenta. Spróbuj wybrać markę powyżej albo dodaj FMI: np. <b>{spn}/1</b>.',
      stepParam: 'parametr', knownFailures: 'znane usterki — {brand}',
      stepNeedFmi: 'potrzebny FMI',
      needFmiText: 'FMI to druga połowa kodu — mówi <b>dokładnie co</b> jest nie tak z tym parametrem. Wpisz go razem z numerem: np. <span class="mono">{spn}/1</span>.',
      stepUrgency: 'pilność',
      urgentText: '<span class="crit">Krytyczne</span> — zatrzymaj się przy najbliższej bezpiecznej okazji, nie jedź dalej.',
      notUrgentText: '<span class="warn">Można jechać dalej</span> — ale pokaż kod przy najbliższym przeglądzie.',
      unknownSpnNote: 'Tego SPN nie ma w bazie — prawdopodobnie kod producenta. Spróbuj wybrać markę powyżej.',
      loadError: 'Słownik się nie wczytał — odśwież stronę.',
      sourceLabel: 'źródło: {src}', fmiNonstandard: 'FMI {fmi} (wartość niestandardowa)',
      commonTitle: 'Częste kody usterek',
      bySituation: 'Jeśli nie masz numeru kodu',
      byBrand: 'Według marki',
      allCodes: 'Wszystkie kody usterek',
      allBrands: 'Wszystkie marki',
      allProblems: 'Wszystkie objawy',
      casCount: 'przeanalizowanych kodów: {n}',
      casRoot: 'prawdopodobna przyczyna',
      casCons: 'skutki — nie naprawia się ich osobno',
      casSolo: 'bez związku z przyczyną',
      casTodo: 'co zrobić teraz',
      casWhyChain: 'Pozostałe kody zwykle pojawiają się po tym — najpierw usuń ten.',
      casWhySingle: 'Reszta listy nie jest bezpośrednio powiązana z tym kodem.',
      vStop: 'Nie jedź dalej',
      vStopSub: 'Zatrzymaj się, gdy tylko będzie to bezpieczne — nie kontynuuj jazdy.',
      vWarn: 'Można jechać',
      vWarnSub: 'Poniżej — ile masz czasu i co się stanie, jeśli pojedziesz dalej.',
      shareLabel: 'Wyślij analizę',
      shareDone: 'Link skopiowany',
      sysScr: 'AdBlue / wydech', sysOil: 'smarowanie', sysCool: 'układ chłodzenia',
      sysFuel: 'paliwo', sysAir: 'dolot / doładowanie', sysPower: 'zasilanie',
      sysCan: 'magistrala CAN', sysBrake: 'hamulce', sysTrans: 'skrzynia biegów',
      sysProt: 'ochrona silnika', sysOther: 'inne',
      actScr: 'Uzupełnij AdBlue do pełna. Jeśli zbiornik jest pełny, problem leży w dozowaniu lub jakości reagenta — potrzebny jest skaner.',
      actOil: 'Zgaś silnik. Sprawdź poziom oleju bagnetem i obejrzyj spód pod kątem wycieków. Nie uruchamiaj, dopóki ciśnienie nie wróci.',
      actCool: 'Poczekaj, aż silnik ostygnie — nigdy nie otwieraj korka zbiornika wyrównawczego na gorąco. Potem sprawdź poziom i przewody.',
      actFuel: 'Sprawdź filtr paliwa i odstojnik, spuść wodę. Na mrozie podejrzewaj parafinowanie oleju napędowego.',
      actAir: 'Obejrzyj filtr powietrza i przewody doładowania: nieszczelności i pęknięcia dają dokładnie takie kody.',
      actPower: 'Sprawdź klemy akumulatora i masę — korozja i luźne zaciski sypią fałszywymi kodami po całym pojeździe. Na pracującym silniku norma to 27–29 V.',
      actCan: 'Sprawdź złącza i wiązkę: przerwana skrętka CAN pozbawia łączności wszystkie sterowniki naraz.',
      actBrake: 'Pozwól układowi pneumatycznemu nabić ciśnienie robocze i posłuchaj, czy nie ma nieszczelności. Z niesprawnymi hamulcami się nie jedzie.',
      actDefault: 'Zapisz kody i pokaż je w warsztacie — ten zestaw wymaga skanera i oględzin na miejscu.',
      freqOil: "Ciśnienie oleju",
      freqCool: "Temperatura płynu chłodzącego",
      freqWater: "Woda w paliwie",
      freqBoost: "Ciśnienie doładowania",
      freqVolt: "Napięcie akumulatora",
      freqAdblue: "Poziom AdBlue",
      freqDpf: "Filtr cząstek stałych",
      freqTorque: "Ograniczenie momentu",
      freqCan: "Magistrala CAN",
      symCheck: "Zapaliła się kontrolka Check Engine",
      symAdblue: "Błąd AdBlue",
      symPower: "Spadek mocy",
      symLowOil: "Niskie ciśnienie oleju",
      symOverheat: "Przegrzanie silnika",
      symDpfClog: "Zapchany filtr cząstek stałych",
      symWater: "Woda w paliwie",
      symAllCodes: "Usterki w całej ciężarówce",
      symNoStart: "Silnik nie odpala",
      symStalls: "Gaśnie w trakcie jazdy",
      symMisfire: "Silnik pracuje nierówno",
      symBlackSmoke: "Czarny dym",
      symWhiteSmoke: "Biały dym",
      symBlueSmoke: "Niebieski dym",
      symFuelUse: "Duże zużycie paliwa",
      symNoRegen: "Brak regeneracji DPF",
      symAdbluePump: "Pompa AdBlue nie dozuje",
      symNox: "Błąd czujnika NOx",
      symAlt: "Alternator nie ładuje",
      symAir: "Nie nabija powietrza",
      symAbsLamp: "Świeci kontrolka ABS",
      symParkBrake: "Hamulec postojowy nie puszcza",
      symGears: "Biegi się nie przełączają",
      symClutch: "Sprzęgło się ślizga",
      symRetarder: "Błąd retardera",
      symUphill: "Grzeje się na wzniesieniu",
      symTacho: "Błąd tachografu",
      symEngineBrake: "Hamulec silnikowy nie działa",
      brandKamazLbl: "KAMAZ",
      brandYamzLbl: "YaMZ",
      brandGazLbl: "GAZ",
      brandMazLbl: "MAZ",
      brandKrazLbl: "KrAZ",
      brandUralLbl: "Ural",
      brandPlanarLbl: "Planar",
      brandTeplostarLbl: "Teplostar"
    },
    tr: {
      pageTitle: 'Kamyon arıza kodu — SPN/FMI ve bayi kodu çözümleme',
      langOffer: 'Bu sayfa Türkçe olarak da mevcut',
      metaDescription: 'Ücretsiz kamyon arıza kodu çözümleme: J1939 standardı (SPN/FMI) ve 80+ markanın fabrika tabloları. Tarayıcıdan veya gösterge panelinden kodu girin.',
      h1: '<em>Check&nbsp;Engine</em> lambası yandı — kod ne anlama geliyor?',
      purposeStats: '80+ marka ve sistemde 39.000+ arıza kodu',
      purposeDo: 'Bir kod girin — ya da arıza listesinin tamamını olduğu gibi: virgül, boşluk veya alt satır fark etmez. Tek bir arıza beş-altı kodu peşinden sürükler — hangisinin neden olduğunu, hangilerinin ardından geldiğini gösterir ve yola devam edilip edilemeyeceğini söyleriz.',
      goBtn: 'Çöz',
      demoTag: 'örnek',
      brandDefault: '— herhangi bir marka —',
      brandGroupVehicles: 'Araç markaları',
      brandGroupSystems: 'Sistemler ve bileşenler',
      standardAuto: 'Otomatik algıla',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: 'Bayi / OBD kodu',
      dataLangNote: 'Arıza açıklamaları İngilizce olarak gösterilir.',
      printLabel: 'Yazdır',
      themeDay: 'Gündüz teması',
      themeNight: 'Gece teması',
      footText: 'Bu rehber kodun ne anlama geldiğini açıklar — teşhis koymaz. Nihai karar her zaman uygun ekipmana sahip bir kişiye aittir. Sorular — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>.',
      langAria: 'Sayfa dili',
      copyMail: 'Adresi kopyala',
      copied: 'Kopyalandı',
      emptyPrompt: 'Bir kod girin — örneğin <b>SPN 100 FMI 1</b> veya sadece <b>100/1</b>.',
      badCode: 'Bu kod seçilen standartta çözümlenemedi. "Otomatik algıla" seçeneğini veya <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b> biçimini deneyin.',
      pcodeNotFound: 'Bayi kodu <b>{code}</b> veritabanında bulunamadı. Bu kodlar markaya göre farklıdır — yazımı kontrol edin.',
      pcodeSearching: 'Aranıyor…',
      pcodeApiError: 'Bayi kodu alınamadı — bağlantınızı kontrol edip tekrar deneyin.',
      dealerBase: 'bayi veritabanı — {brand}',
      dealerOffline: 'Bayi veritabanı şu an kullanılamıyor — yalnızca fabrika tablosu gösteriliyor.',
      dailyLimit: 'Günlük arama limiti doldu (günde 50). Lütfen yarın tekrar deneyin.',
      scanStep: 'tarayıcı kodu',
      scanMany: '<b>{code}</b> numarası gösterge panelindeki birden fazla koda karşılık gelir — hangisinin göründüğünü kontrol edin.',
      stepCode: 'kod', stepDecoding: 'anlam',
      factorySource: 'fabrika tablosu — {brand}', standardSource: 'J1939 standardı',
      blinkNotFoundFor: '{brand} tablosunda {n} yanıp sönme kodu bulunamadı.',
      j1939ForBrand: 'J1939 standardına göre — {brand} markasında bu numara farklı bir anlam taşıyabilir',
      badCodeFor: '{brand} tablosunda kod tanınmadı — biçimi kontrol edin.',
      pcodeServerError: 'Kod veritabanı geçici olarak kullanılamıyor — daha sonra deneyin.',
      fmiTable: 'FMI {fmi}, {brand} tablosuna göre',
      midDefault: 'Kodda MID yok — motor modülü, MID 128 alındı.',
      midTyped: 'Kodda MID {mid} var — seçilen ({sel}) yerine bu kullanıldı.',
      spnNotFound: '<b>SPN {spn}</b> veritabanında bulunamadı — muhtemelen üreticiye özel bir kod. Yukarıdan bir marka seçin veya FMI ekleyin: örn. <b>{spn}/1</b>.',
      stepParam: 'parametre', knownFailures: 'bilinen arızalar — {brand}',
      stepNeedFmi: 'FMI gerekli',
      needFmiText: 'FMI, kodun ikinci yarısıdır — bu parametrede <b>tam olarak neyin</b> yanlış olduğunu söyler. Numarayla birlikte girin: örn. <span class="mono">{spn}/1</span>.',
      stepUrgency: 'aciliyet',
      urgentText: '<span class="crit">Kritik</span> — güvenli olan ilk fırsatta durun, sürmeye devam etmeyin.',
      notUrgentText: '<span class="warn">Yola devam edilebilir</span> — ancak kodu bir sonraki serviste gösterin.',
      unknownSpnNote: 'Bu SPN veritabanında yok — muhtemelen üreticiye özel bir kod. Yukarıdan bir marka seçmeyi deneyin.',
      loadError: 'Sözlük yüklenemedi — sayfayı yenileyin.',
      sourceLabel: 'kaynak: {src}', fmiNonstandard: 'FMI {fmi} (standart olmayan değer)',
      commonTitle: 'Sık görülen arıza kodları',
      bySituation: 'Kod numarası yoksa',
      byBrand: 'Markaya göre',
      allCodes: 'Tüm arıza kodları',
      allBrands: 'Tüm markalar',
      allProblems: 'Tüm belirtiler',
      casCount: 'incelenen kod: {n}',
      casRoot: 'olası kök neden',
      casCons: 'sonuç kodları — ayrı ayrı onarılmaz',
      casSolo: 'kök nedenle ilgisiz',
      casTodo: 'şimdi ne yapmalı',
      casWhyChain: 'Diğer kodlar genellikle bunun ardından gelir — önce bunu giderin.',
      casWhySingle: 'Listenin geri kalanı bu kodla doğrudan ilgili değil.',
      vStop: 'Yola devam etmeyin',
      vStopSub: 'Güvenli olur olmaz durun — yola devam etmeyin.',
      vWarn: 'Yola devam edilebilir',
      vWarnSub: 'Aşağıda — ne kadar zamanınız var ve devam ederseniz ne olur.',
      shareLabel: 'Raporu gönder',
      shareDone: 'Bağlantı kopyalandı',
      sysScr: 'AdBlue / egzoz', sysOil: 'yağlama', sysCool: 'soğutma',
      sysFuel: 'yakıt', sysAir: 'emme / turbo basıncı', sysPower: 'besleme',
      sysCan: 'CAN hattı', sysBrake: 'frenler', sysTrans: 'şanzıman',
      sysProt: 'motor koruma', sysOther: 'diğer',
      actScr: 'AdBlue deposunu doldurun. Depo zaten doluysa sorun dozajlama veya reaktif kalitesindedir — cihaz gerekir.',
      actOil: 'Motoru durdurun. Yağ seviyesini çubukla kontrol edin ve altını kaçak için gözden geçirin. Basınç geri gelmeden çalıştırmayın.',
      actCool: 'Motorun soğumasını bekleyin — genleşme deposunun kapağını sıcakken asla açmayın. Sonra seviyeyi ve hortumları kontrol edin.',
      actFuel: 'Yakıt filtresini ve su tutucuyu kontrol edin, suyu boşaltın. Soğukta motorinin parafinlenmesinden şüphelenin.',
      actAir: 'Hava filtresini ve turbo hortumlarını inceleyin: kaçaklar ve çatlaklar tam olarak bu kodları verir.',
      actPower: 'Akü kutup başlarını ve şasi bağlantısını kontrol edin — oksitlenme ve gevşek sıkma tüm araçta sahte kod üretir. Motor çalışırken 27–29 V normaldir.',
      actCan: 'Soketleri ve tesisatı kontrol edin: kopmuş bir CAN burgulu çifti tüm beyinlerin haberleşmesini aynı anda keser.',
      actBrake: 'Hava sisteminin çalışma basıncına ulaşmasını bekleyin ve kaçak sesi dinleyin. Arızalı frenle yola çıkılmaz.',
      actDefault: 'Kodları not edin ve serviste gösterin — bu grup için cihaz ve yerinde inceleme gerekir.',
      freqOil: "Yağ basıncı",
      freqCool: "Soğutma suyu sıcaklığı",
      freqWater: "Yakıtta su",
      freqBoost: "Turbo basıncı",
      freqVolt: "Akü voltajı",
      freqAdblue: "AdBlue seviyesi",
      freqDpf: "Partikül filtresi",
      freqTorque: "Tork sınırlama",
      freqCan: "CAN hattı",
      symCheck: "Check Engine lambası yandı",
      symAdblue: "AdBlue hatası",
      symPower: "Güç kaybı",
      symLowOil: "Düşük yağ basıncı",
      symOverheat: "Motor aşırı ısınması",
      symDpfClog: "Tıkalı partikül filtresi",
      symWater: "Yakıtta su",
      symAllCodes: "Kamyonun her yerinde arıza",
      symNoStart: "Motor çalışmıyor",
      symStalls: "Yolda stop ediyor",
      symMisfire: "Motor tekliyor",
      symBlackSmoke: "Siyah duman",
      symWhiteSmoke: "Beyaz duman",
      symBlueSmoke: "Mavi duman",
      symFuelUse: "Yüksek yakıt tüketimi",
      symNoRegen: "DPF rejenerasyonu başlamıyor",
      symAdbluePump: "AdBlue pompası dozlamıyor",
      symNox: "NOx sensörü arızası",
      symAlt: "Alternatör şarj etmiyor",
      symAir: "Hava basıncı yükselmiyor",
      symAbsLamp: "ABS lambası yanıyor",
      symParkBrake: "El freni çözülmüyor",
      symGears: "Vites geçmiyor",
      symClutch: "Debriyaj kayıyor",
      symRetarder: "Retarder arızası",
      symUphill: "Yokuşta ısınıyor",
      symTacho: "Takograf arızası",
      symEngineBrake: "Motor freni çalışmıyor",
      brandKamazLbl: "KAMAZ",
      brandYamzLbl: "YaMZ",
      brandGazLbl: "GAZ",
      brandMazLbl: "MAZ",
      brandKrazLbl: "KrAZ",
      brandUralLbl: "Ural",
      brandPlanarLbl: "Planar",
      brandTeplostarLbl: "Teplostar"
    },
    hi: {
      pageTitle: 'ट्रक फॉल्ट कोड — SPN/FMI और डीलर कोड डिकोडिंग',
      langOffer: 'यह पृष्ठ हिंदी में उपलब्ध है',
      metaDescription: 'ट्रक फॉल्ट कोड की मुफ्त डिकोडिंग: J1939 मानक (SPN/FMI) और 80+ ब्रांड की फैक्ट्री तालिकाएं। स्कैनर या डैशबोर्ड से कोड डालें।',
      h1: '<em>Check&nbsp;Engine</em> लैंप जल गया है — कोड का मतलब क्या है?',
      purposeStats: '80+ ब्रांड और सिस्टम के लिए 39,000+ फॉल्ट कोड',
      purposeDo: 'एक कोड डालें — या खराबियों की पूरी सूची जैसी है वैसी ही: कॉमा, स्पेस या नई लाइन से अलग। एक खराबी पांच-छह कोड अपने साथ लाती है — हम बताएंगे कि कौन सा कारण है और कौन से उसके बाद आए, और यह भी कि गाड़ी चलाना सुरक्षित है या नहीं।',
      goBtn: 'डिकोड करें',
      demoTag: 'उदाहरण',
      brandDefault: '— कोई भी ब्रांड —',
      brandGroupVehicles: 'वाहन ब्रांड',
      brandGroupSystems: 'सिस्टम और घटक',
      standardAuto: 'स्वतः पहचानें',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: 'डीलर / OBD कोड',
      dataLangNote: 'खराबी के विवरण अंग्रेज़ी में दिखाए गए हैं।',
      printLabel: 'प्रिंट करें',
      themeDay: 'दिन वाली थीम',
      themeNight: 'रात वाली थीम',
      footText: 'यह संदर्भ पुस्तिका बताती है कि कोड का मतलब क्या है — यह निदान नहीं करती। अंतिम निर्णय हमेशा उपकरण रखने वाले व्यक्ति का होता है। सवाल — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>.',
      langAria: 'पृष्ठ की भाषा',
      copyMail: 'पता कॉपी करें',
      copied: 'कॉपी हो गया',
      emptyPrompt: 'एक कोड डालें — उदाहरण के लिए <b>SPN 100 FMI 1</b> या सिर्फ <b>100/1</b>.',
      badCode: 'चुने गए मानक में यह कोड समझ नहीं आया। "स्वतः पहचानें" आज़माएं या <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b> प्रारूप का उपयोग करें।',
      pcodeNotFound: 'डीलर कोड <b>{code}</b> डेटाबेस में नहीं मिला। ये कोड हर ब्रांड में अलग होते हैं — वर्तनी जांचें।',
      pcodeSearching: 'खोजा जा रहा है…',
      pcodeApiError: 'डीलर कोड नहीं मिल सका — अपना कनेक्शन जांचें और फिर से कोशिश करें।',
      dealerBase: 'डीलर डेटाबेस — {brand}',
      dealerOffline: 'डीलर डेटाबेस अभी उपलब्ध नहीं है — केवल फैक्ट्री तालिका दिखाई जा रही है।',
      dailyLimit: 'आज की खोज सीमा पूरी हो गई (प्रतिदिन 50)। कृपया कल फिर कोशिश करें।',
      scanStep: 'स्कैनर कोड',
      scanMany: 'नंबर <b>{code}</b> डैश के कई कोड से मेल खाता है — देखें कि पैनल कौन सा दिखा रहा है।',
      stepCode: 'कोड', stepDecoding: 'अर्थ',
      factorySource: 'फैक्ट्री तालिका — {brand}', standardSource: 'J1939 मानक',
      blinkNotFoundFor: '{brand} तालिका में ब्लिंक कोड {n} नहीं मिला।',
      j1939ForBrand: 'J1939 मानक के अनुसार — {brand} में यह संख्या कुछ और अर्थ रख सकती है',
      badCodeFor: '{brand} तालिका में कोड नहीं पहचाना गया — प्रारूप जांचें।',
      pcodeServerError: 'कोड डेटाबेस अस्थायी रूप से उपलब्ध नहीं है — बाद में प्रयास करें।',
      fmiTable: 'FMI {fmi} — {brand} तालिका के अनुसार',
      midDefault: 'कोड में MID नहीं है — इंजन मॉड्यूल, MID 128 लिया गया।',
      midTyped: 'कोड में MID {mid} है — चयनित ({sel}) की जगह यही लिया गया।',
      spnNotFound: '<b>SPN {spn}</b> डेटाबेस में नहीं मिला — संभवतः यह निर्माता-विशिष्ट कोड है। ऊपर ब्रांड चुनें, या FMI जोड़ें: जैसे <b>{spn}/1</b>.',
      stepParam: 'पैरामीटर', knownFailures: 'ज्ञात खराबियां — {brand}',
      stepNeedFmi: 'FMI चाहिए',
      needFmiText: 'FMI कोड का दूसरा हिस्सा है — यह बताता है कि इस पैरामीटर में <b>वास्तव में क्या</b> गड़बड़ है। इसे नंबर के साथ डालें: जैसे <span class="mono">{spn}/1</span>.',
      stepUrgency: 'तात्कालिकता',
      urgentText: '<span class="crit">गंभीर</span> — जैसे ही सुरक्षित हो, रुक जाएं, गाड़ी चलाना जारी न रखें।',
      notUrgentText: '<span class="warn">गाड़ी चलाना सुरक्षित है</span> — लेकिन अगली सर्विस में कोड जरूर दिखाएं।',
      unknownSpnNote: 'यह SPN डेटाबेस में नहीं है — संभवतः यह निर्माता-विशिष्ट कोड है। ऊपर ब्रांड चुनकर देखें।',
      loadError: 'शब्दकोश लोड नहीं हुआ — पेज रीफ़्रेश करें।',
      sourceLabel: 'स्रोत: {src}', fmiNonstandard: 'FMI {fmi} (गैर-मानक मान)',
      commonTitle: 'आम फॉल्ट कोड',
      bySituation: 'अगर कोड नंबर नहीं है',
      byBrand: 'ब्रांड के अनुसार',
      allCodes: 'सभी फॉल्ट कोड',
      allBrands: 'सभी ब्रांड',
      allProblems: 'सभी लक्षण',
      casCount: 'जांचे गए कोड: {n}',
      casRoot: 'संभावित मूल कारण',
      casCons: 'परिणामी कोड — अलग से ठीक नहीं होते',
      casSolo: 'मूल कारण से असंबंधित',
      casTodo: 'अभी क्या करें',
      casWhyChain: 'बाकी कोड आमतौर पर इसी के बाद आते हैं — पहले इसे ठीक करें।',
      casWhySingle: 'सूची के बाकी कोड इससे सीधे जुड़े नहीं हैं।',
      vStop: 'गाड़ी न चलाएं',
      vStopSub: 'जैसे ही सुरक्षित हो, रुक जाएं — आगे न बढ़ें।',
      vWarn: 'गाड़ी चलाना सुरक्षित है',
      vWarnSub: 'नीचे — आपके पास कितना समय है और आगे चलाते रहने पर क्या होगा।',
      shareLabel: 'रिपोर्ट भेजें',
      shareDone: 'लिंक कॉपी हो गया',
      sysScr: 'AdBlue / निकास', sysOil: 'स्नेहन', sysCool: 'शीतलन',
      sysFuel: 'ईंधन', sysAir: 'इनटेक / बूस्ट', sysPower: 'विद्युत आपूर्ति',
      sysCan: 'CAN बस', sysBrake: 'ब्रेक', sysTrans: 'ट्रांसमिशन',
      sysProt: 'इंजन सुरक्षा', sysOther: 'अन्य',
      actScr: 'AdBlue टैंक भरें। अगर टैंक पहले से भरा है तो समस्या डोज़िंग या रीएजेंट की गुणवत्ता में है — स्कैनर चाहिए।',
      actOil: 'इंजन बंद करें। डिपस्टिक से तेल का स्तर जांचें और नीचे रिसाव देखें। दबाव लौटने तक इंजन चालू न करें।',
      actCool: 'इंजन को ठंडा होने दें — गर्म में एक्सपेंशन टैंक का ढक्कन कभी न खोलें। फिर स्तर और पाइप जांचें।',
      actFuel: 'ईंधन फिल्टर और वॉटर ट्रैप जांचें, पानी निकालें। ठंड में डीज़ल के जमने का संदेह करें।',
      actAir: 'एयर फिल्टर और बूस्ट पाइप देखें: रिसाव और दरारें ठीक ऐसे ही कोड देती हैं।',
      actPower: 'बैटरी टर्मिनल और अर्थ जांचें — जंग और ढीली कसावट पूरी गाड़ी में झूठे कोड पैदा करती है। इंजन चालू पर 27–29 V सामान्य है।',
      actCan: 'कनेक्टर और वायरिंग जांचें: टूटी CAN जोड़ी सभी ECU का संपर्क एक साथ खत्म कर देती है।',
      actBrake: 'न्यूमैटिक सिस्टम को काम करने के दबाव तक भरने दें और रिसाव सुनें। खराब ब्रेक के साथ गाड़ी नहीं चलाते।',
      actDefault: 'कोड लिख लें और वर्कशॉप में दिखाएं — इस सेट के लिए स्कैनर और मौके पर जांच चाहिए।',
      freqOil: "तेल का दबाव",
      freqCool: "कूलेंट तापमान",
      freqWater: "ईंधन में पानी",
      freqBoost: "बूस्ट प्रेशर",
      freqVolt: "बैटरी वोल्टेज",
      freqAdblue: "AdBlue स्तर",
      freqDpf: "सूट फ़िल्टर",
      freqTorque: "टॉर्क सीमा",
      freqCan: "CAN बस",
      symCheck: "Check Engine लाइट जली",
      symAdblue: "AdBlue त्रुटि",
      symPower: "पावर लॉस",
      symLowOil: "कम तेल दबाव",
      symOverheat: "इंजन ओवरहीटिंग",
      symDpfClog: "बंद सूट फ़िल्टर",
      symWater: "ईंधन में पानी",
      symAllCodes: "पूरे ट्रक में खराबियां",
      symNoStart: "इंजन स्टार्ट नहीं होता",
      symStalls: "चलते-चलते बंद हो जाता है",
      symMisfire: "इंजन मिसफायर कर रहा है",
      symBlackSmoke: "काला धुआं",
      symWhiteSmoke: "सफेद धुआं",
      symBlueSmoke: "नीला धुआं",
      symFuelUse: "ज्यादा ईंधन खपत",
      symNoRegen: "DPF रीजनरेशन नहीं होता",
      symAdbluePump: "AdBlue पंप डोज़ नहीं कर रहा",
      symNox: "NOx सेंसर खराबी",
      symAlt: "अल्टरनेटर चार्ज नहीं कर रहा",
      symAir: "हवा का प्रेशर नहीं बनता",
      symAbsLamp: "ABS लाइट जली",
      symParkBrake: "पार्किंग ब्रेक नहीं छूटता",
      symGears: "गियर नहीं बदलते",
      symClutch: "क्लच स्लिप कर रहा है",
      symRetarder: "रिटार्डर खराबी",
      symUphill: "चढ़ाई पर गरम होता है",
      symTacho: "टैकोग्राफ खराबी",
      symEngineBrake: "इंजन ब्रेक काम नहीं कर रहा",
      brandKamazLbl: "KAMAZ",
      brandYamzLbl: "YaMZ",
      brandGazLbl: "GAZ",
      brandMazLbl: "MAZ",
      brandKrazLbl: "KrAZ",
      brandUralLbl: "Ural",
      brandPlanarLbl: "Planar",
      brandTeplostarLbl: "Teplostar"
    },
    zh: {
      pageTitle: '卡车故障代码查询 — SPN/FMI 与经销商代码解析',
      langOffer: '本页面有中文版',
      metaDescription: '免费卡车故障代码查询：J1939 标准（SPN/FMI）及80+个品牌的原厂代码表。输入诊断仪或仪表盘显示的代码即可查询。',
      h1: '<em>Check&nbsp;Engine</em>（发动机故障）灯亮了 — 代码是什么意思？',
      purposeStats: '覆盖80+品牌和系统，39,000+条故障代码',
      purposeDo: '输入一个代码 — 或者按原样输入整个故障列表：用逗号、空格或换行分隔。一个故障通常会带出五六个代码 — 我们会指出哪个是根本原因，哪些只是随之而来的，并告诉你是否可以继续行驶。',
      goBtn: '解析',
      demoTag: '示例',
      brandDefault: '— 任意品牌 —',
      brandGroupVehicles: '车辆品牌',
      brandGroupSystems: '系统与部件',
      standardAuto: '自动识别',
      standardSpnFmi: 'J1939 — SPN / FMI',
      standardPcode: '经销商 / OBD 代码',
      dataLangNote: '故障名称以英文显示。',
      printLabel: '打印',
      themeDay: '日间模式',
      themeNight: '夜间模式',
      footText: '本查询工具用于解释代码含义，并不能诊断车辆故障。最终判断应由持有专业设备的技师做出。有问题请联系 — <a href="mailto:alexdiag116@gmail.com" style="color:inherit">alexdiag116@gmail.com</a>。',
      langAria: '页面语言',
      copyMail: '复制地址',
      copied: '已复制',
      emptyPrompt: '请输入代码 — 例如 <b>SPN 100 FMI 1</b> 或直接输入 <b>100/1</b>。',
      badCode: '无法按所选标准解析该代码。请尝试“自动识别”，或使用 <b>SPN 100 FMI 1</b> / <b>100/1</b> / <b>P2BA7</b> 格式。',
      pcodeNotFound: '数据库中未找到经销商代码 <b>{code}</b>。不同品牌的代码不同 — 请检查输入是否正确。',
      pcodeSearching: '正在查询…',
      pcodeApiError: '无法获取经销商代码 — 请检查网络连接后重试。',
      dealerBase: '经销商数据库 — {brand}',
      dealerOffline: '经销商数据库暂时不可用 — 仅显示厂家表。',
      dailyLimit: '今日搜索次数已用完（每天 50 次）。请明天再试。',
      scanStep: '扫描仪代码',
      scanMany: '代码 <b>{code}</b> 对应仪表盘上的多个代码 — 请核对仪表显示的是哪一个。',
      stepCode: '代码', stepDecoding: '含义',
      factorySource: '原厂代码表 — {brand}', standardSource: 'J1939 标准',
      blinkNotFoundFor: '在{brand}表中未找到闪码{n}。',
      j1939ForBrand: '按J1939标准 — {brand}的该编号可能含义不同',
      badCodeFor: '在{brand}表中无法识别该代码 — 请检查格式。',
      pcodeServerError: '代码数据库暂时不可用 — 请稍后再试。',
      fmiTable: 'FMI {fmi}，按{brand}表',
      midDefault: '代码中没有MID — 按发动机模块MID 128处理。',
      midTyped: '代码中的MID为{mid} — 使用它而非所选的({sel})。',
      spnNotFound: '数据库中未找到 <b>SPN {spn}</b> — 可能是厂商专有代码。请在上方选择品牌，或补充 FMI，例如 <b>{spn}/1</b>。',
      stepParam: '参数', knownFailures: '已知故障 — {brand}',
      stepNeedFmi: '需要 FMI',
      needFmiText: 'FMI 是代码的后半部分 — 它准确说明了该参数<b>具体</b>出了什么问题。请与编号一起输入，例如 <span class="mono">{spn}/1</span>。',
      stepUrgency: '紧急程度',
      urgentText: '<span class="crit">紧急</span> — 请在安全的情况下尽快停车，不要继续行驶。',
      notUrgentText: '<span class="warn">可以继续行驶</span> — 但请在下次保养时检查该代码。',
      unknownSpnNote: '数据库中没有该 SPN — 可能是厂商专有代码。请在上方选择品牌后重试。',
      loadError: '词典未能加载 — 请刷新页面。',
      sourceLabel: '来源：{src}', fmiNonstandard: 'FMI {fmi}（非标准值）',
      commonTitle: '常见故障代码',
      bySituation: '如果没有代码编号',
      byBrand: '按品牌查找',
      allCodes: '全部故障代码',
      allBrands: '全部品牌',
      allProblems: '全部故障现象',
      casCount: '已分析代码数：{n}',
      casRoot: '可能的根本原因',
      casCons: '连带产生的代码 — 无需单独处理',
      casSolo: '与根本原因无关',
      casTodo: '现在该怎么做',
      casWhyChain: '列表中的其他代码通常是由此代码引发的 — 请先处理这一个。',
      casWhySingle: '列表中的其余代码与该代码没有直接关联。',
      vStop: '禁止行驶',
      vStopSub: '请在安全的情况下尽快停车 — 不要继续行驶。',
      vWarn: '可以继续行驶',
      vWarnSub: '下方说明您还有多少时间，以及继续行驶会发生什么。',
      shareLabel: '发送此报告',
      shareDone: '链接已复制',
      sysScr: 'AdBlue / 排气', sysOil: '润滑系统', sysCool: '冷却系统',
      sysFuel: '燃油系统', sysAir: '进气 / 增压', sysPower: '电源系统',
      sysCan: 'CAN 总线', sysBrake: '制动系统', sysTrans: '变速箱',
      sysProt: '发动机保护', sysOther: '其他',
      actScr: '请加注 AdBlue（尿素）。如果已加满，问题可能出在喷射系统或尿素质量上 — 需要使用诊断仪检查。',
      actOil: '请立即熄火。用机油尺检查油位，并查看车底是否有渗漏。压力恢复正常前不要重新启动发动机。',
      actCool: '让发动机冷却 — 切勿在高温时打开膨胀水箱盖。冷却后检查冷却液液位和管路。',
      actFuel: '检查燃油滤清器和油水分离器，排出积水。寒冷天气下应考虑柴油结蜡的可能性。',
      actAir: '检查空气滤清器和增压管路：泄漏和裂纹正是导致此类代码的常见原因。',
      actPower: '检查蓄电池接线柱和搭铁线 — 腐蚀或接线松动会在全车范围内引发虚假故障代码。发动机运转时电压应为 27–29 V。',
      actCan: '检查接插件和线束：CAN 双绞线断路会导致全部电控单元同时失去通讯。',
      actBrake: '让气路系统建立到工作气压，并检查是否有漏气声。切勿在制动系统故障的情况下行驶。',
      actDefault: '请记录下所有代码并交给维修厂处理 — 这类故障需要诊断仪和现场检查。',
      freqOil: "机油压力",
      freqCool: "冷却液温度",
      freqWater: "燃油中含水",
      freqBoost: "增压压力",
      freqVolt: "蓄电池电压",
      freqAdblue: "AdBlue 液位",
      freqDpf: "颗粒捕集器（DPF）",
      freqTorque: "扭矩限制",
      freqCan: "CAN 总线",
      symCheck: "Check Engine（发动机故障灯）亮起",
      symAdblue: "AdBlue 故障",
      symPower: "动力下降",
      symLowOil: "机油压力过低",
      symOverheat: "发动机过热",
      symDpfClog: "颗粒捕集器堵塞",
      symWater: "燃油中含水",
      symAllCodes: "全车范围故障",
      symNoStart: "发动机无法启动",
      symStalls: "行驶中熄火",
      symMisfire: "发动机缺缸",
      symBlackSmoke: "排气冒黑烟",
      symWhiteSmoke: "排气冒白烟",
      symBlueSmoke: "排气冒蓝烟",
      symFuelUse: "油耗过高",
      symNoRegen: "颗粒捕集器无法再生",
      symAdbluePump: "AdBlue 泵不喷射",
      symNox: "NOx 传感器故障",
      symAlt: "发电机不充电",
      symAir: "气压上不来",
      symAbsLamp: "ABS 灯亮",
      symParkBrake: "驻车制动无法解除",
      symGears: "无法换挡",
      symClutch: "离合器打滑",
      symRetarder: "缓速器故障",
      symUphill: "爬坡时过热",
      symTacho: "行驶记录仪故障",
      symEngineBrake: "发动机制动不起作用",
      brandKamazLbl: "KAMAZ",
      brandYamzLbl: "YaMZ",
      brandGazLbl: "GAZ",
      brandMazLbl: "MAZ",
      brandKrazLbl: "KrAZ",
      brandUralLbl: "Ural",
      brandPlanarLbl: "Planar",
      brandTeplostarLbl: "Teplostar"
    }
  };

  /* Стандартные расшифровки FMI по J1939 - фиксированные 23
     значения, есть смысл перевести. Русский вариант берём прямо из
     базы (DB.fmi), чтобы не дублировать текст. */
  var FMI_I18N = {
    en: {0:'data above normal range (most severe level)',1:'data below normal range (most severe level)',
      2:'data erratic or intermittent',3:'voltage above normal or shorted high',
      4:'voltage below normal or shorted to ground',5:'current below normal or open circuit',
      6:'current above normal or grounded circuit',7:'mechanical system not responding',
      8:'abnormal frequency or pulse width',9:'abnormal update rate',10:'abnormal rate of change',
      11:'root cause not known',12:'faulty device or component',13:'calibration out of range',
      14:'manufacturer-specific instructions',15:'above normal — low severity',
      16:'above normal — moderate severity',17:'below normal — low severity',
      18:'below normal — moderate severity',19:'error in received network data',
      20:'data drifted high',21:'data drifted low',31:'condition exists (see manufacturer description)'},
    de: {0:'Wert über Normalbereich (höchster Schweregrad)',1:'Wert unter Normalbereich (höchster Schweregrad)',
      2:'Wert instabil oder fehlerhaft',3:'Spannung über Normalwert oder Kurzschluss nach Plus',
      4:'Spannung unter Normalwert oder Kurzschluss nach Masse',5:'Strom unter Normalwert oder Leitungsunterbrechung',
      6:'Strom über Normalwert oder Kurzschluss nach Masse',7:'mechanisches System reagiert nicht',
      8:'anomale Frequenz oder Pulsbreite',9:'anomale Aktualisierungsrate',10:'anomale Änderungsrate',
      11:'Ursache nicht bekannt',12:'defektes Gerät oder Bauteil',13:'Kalibrierung fehlerhaft',
      14:'herstellerspezifische Anweisung',15:'über Normalbereich — geringe Dringlichkeit',
      16:'über Normalbereich — mittlere Dringlichkeit',17:'unter Normalbereich — geringe Dringlichkeit',
      18:'unter Normalbereich — mittlere Dringlichkeit',19:'Fehler in empfangenen Netzwerkdaten',
      20:'Datendrift nach oben',21:'Datendrift nach unten',31:'Zustand liegt vor (siehe Herstellerbeschreibung)'},
    fr: {0:'valeur au-dessus de la normale (niveau le plus sévère)',1:'valeur en dessous de la normale (niveau le plus sévère)',
      2:'valeur instable ou erronée',3:'tension au-dessus de la normale ou court-circuit au plus',
      4:'tension en dessous de la normale ou court-circuit à la masse',5:'courant en dessous de la normale ou circuit ouvert',
      6:'courant au-dessus de la normale ou court-circuit à la masse',7:'système mécanique ne répond pas',
      8:"fréquence ou largeur d'impulsion anormale",9:'taux de mise à jour anormal',10:'taux de variation anormal',
      11:'cause non déterminée',12:'composant ou dispositif défectueux',13:'étalonnage incorrect',
      14:'instruction spécifique du constructeur',15:'au-dessus de la normale — faible gravité',
      16:'au-dessus de la normale — gravité moyenne',17:'en dessous de la normale — faible gravité',
      18:'en dessous de la normale — gravité moyenne',19:'erreur dans les données réseau reçues',
      20:'dérive des données vers le haut',21:'dérive des données vers le bas',31:'condition présente (voir description du constructeur)'},
    hi: {0:'मान सामान्य से अधिक (सबसे गंभीर स्तर)',1:'मान सामान्य से कम (सबसे गंभीर स्तर)',
      2:'मान अस्थिर या गलत',3:'वोल्टेज सामान्य से अधिक या पॉजिटिव से शॉर्ट',
      4:'वोल्टेज सामान्य से कम या ग्राउंड से शॉर्ट',5:'करंट सामान्य से कम या सर्किट टूटा हुआ',
      6:'करंट सामान्य से अधिक या ग्राउंड से शॉर्ट',7:'यांत्रिक प्रणाली प्रतिक्रिया नहीं दे रही',
      8:'असामान्य आवृत्ति या पल्स चौड़ाई',9:'डेटा अपडेट दर असामान्य',10:'डेटा परिवर्तन दर असामान्य',
      11:'कारण स्पष्ट नहीं',12:'खराब उपकरण या घटक',13:'कैलिब्रेशन गलत',
      14:'निर्माता के विशेष निर्देश',15:'सामान्य से अधिक — कम गंभीरता',
      16:'सामान्य से अधिक — मध्यम गंभीरता',17:'सामान्य से कम — कम गंभीरता',
      18:'सामान्य से कम — मध्यम गंभीरता',19:'प्राप्त नेटवर्क डेटा में त्रुटि',
      20:'डेटा ऊपर की ओर खिसका',21:'डेटा नीचे की ओर खिसका',31:'स्थिति मौजूद है (निर्माता विवरण देखें)'},
    es: {0:'valor por encima de lo normal (nivel más grave)',1:'valor por debajo de lo normal (nivel más grave)',
      2:'valor inestable o erróneo',3:'voltaje por encima de lo normal o cortocircuito a positivo',
      4:'voltaje por debajo de lo normal o cortocircuito a masa',5:'corriente por debajo de lo normal o circuito abierto',
      6:'corriente por encima de lo normal o cortocircuito a masa',7:'el sistema mecánico no responde',
      8:'frecuencia o ancho de pulso anómalo',9:'frecuencia de actualización anómala',10:'velocidad de cambio anómala',
      11:'causa no determinada',12:'dispositivo o componente defectuoso',13:'calibración fuera de rango',
      14:'instrucción específica del fabricante',15:'por encima de lo normal — gravedad baja',
      16:'por encima de lo normal — gravedad media',17:'por debajo de lo normal — gravedad baja',
      18:'por debajo de lo normal — gravedad media',19:'error en los datos de red recibidos',
      20:'deriva de datos al alza',21:'deriva de datos a la baja',31:'condición presente (ver descripción del fabricante)'},
    pt: {0:'valor acima do normal (nível mais grave)',1:'valor abaixo do normal (nível mais grave)',
      2:'valor instável ou incorreto',3:'tensão acima do normal ou curto para o positivo',
      4:'tensão abaixo do normal ou curto para a massa',5:'corrente abaixo do normal ou circuito aberto',
      6:'corrente acima do normal ou curto para a massa',7:'sistema mecânico não responde',
      8:'frequência ou largura de pulso anormal',9:'taxa de atualização anormal',10:'taxa de variação anormal',
      11:'causa não determinada',12:'dispositivo ou componente com defeito',13:'calibração fora do intervalo',
      14:'instrução específica do fabricante',15:'acima do normal — baixa gravidade',
      16:'acima do normal — gravidade moderada',17:'abaixo do normal — baixa gravidade',
      18:'abaixo do normal — gravidade moderada',19:'erro nos dados de rede recebidos',
      20:'desvio de dados para cima',21:'desvio de dados para baixo',31:'condição presente (ver descrição do fabricante)'},
    pl: {0:'wartość powyżej normy (najwyższy poziom istotności)',1:'wartość poniżej normy (najwyższy poziom istotności)',
      2:'wartość niestabilna lub błędna',3:'napięcie powyżej normy lub zwarcie do plusa',
      4:'napięcie poniżej normy lub zwarcie do masy',5:'prąd poniżej normy lub przerwany obwód',
      6:'prąd powyżej normy lub zwarcie do masy',7:'układ mechaniczny nie reaguje',
      8:'nieprawidłowa częstotliwość lub szerokość impulsu',9:'nieprawidłowa częstość aktualizacji',10:'nieprawidłowe tempo zmian',
      11:'przyczyna nieznana',12:'uszkodzone urządzenie lub podzespół',13:'kalibracja poza zakresem',
      14:'instrukcja specyficzna dla producenta',15:'powyżej normy — niska pilność',
      16:'powyżej normy — średnia pilność',17:'poniżej normy — niska pilność',
      18:'poniżej normy — średnia pilność',19:'błąd w odebranych danych sieciowych',
      20:'dryf danych w górę',21:'dryf danych w dół',31:'warunek występuje (patrz opis producenta)'},
    tr: {0:'değer normalin üzerinde (en ciddi seviye)',1:'değer normalin altında (en ciddi seviye)',
      2:'değer kararsız veya hatalı',3:'gerilim normalin üzerinde veya artıya kısa devre',
      4:'gerilim normalin altında veya şaseye kısa devre',5:'akım normalin altında veya devre açık',
      6:'akım normalin üzerinde veya şaseye kısa devre',7:'mekanik sistem tepki vermiyor',
      8:'anormal frekans veya darbe genişliği',9:'anormal güncelleme hızı',10:'anormal değişim hızı',
      11:'kök neden bilinmiyor',12:'arızalı cihaz veya bileşen',13:'kalibrasyon aralık dışında',
      14:'üreticiye özel talimat',15:'normalin üzerinde — düşük önem',
      16:'normalin üzerinde — orta önem',17:'normalin altında — düşük önem',
      18:'normalin altında — orta önem',19:'alınan ağ verisinde hata',
      20:'veri yukarı kaydı',21:'veri aşağı kaydı',31:'durum mevcut (üretici açıklamasına bakın)'},
    zh: {0:'数据高于正常范围（最严重级别）',1:'数据低于正常范围（最严重级别）',
      2:'数据异常跳动或时断时续',3:'电压高于正常值或对正极短路',
      4:'电压低于正常值或对地短路',5:'电流低于正常值或电路断路',
      6:'电流高于正常值或电路对地短路',7:'机械系统无响应',
      8:'频率或脉冲宽度异常',9:'更新频率异常',10:'变化速率异常',
      11:'根本原因未知',12:'设备或部件损坏',13:'标定超出范围',
      14:'厂商专用说明',15:'高于正常值 — 轻微',
      16:'高于正常值 — 中等',17:'低于正常值 — 轻微',
      18:'低于正常值 — 中等',19:'接收到的网络数据错误',
      20:'数据向上漂移',21:'数据向下漂移',31:'故障条件存在（参见厂商说明）'}
  };

  /* КамАЗ и ЯМЗ в базе записаны кириллицей - для остальных языков
     переключаем на латинскую транслитерацию, так их узнают на
     любом языке. Остальные марки (Volvo, MAN, DAF...) уже латиницей. */
  var BRAND_OVERRIDE = {kamaz:'KAMAZ', yamz:'YAMZ', planar:'Planar / Teplostar',
                        vdo:'VDO DTCO', shtrih:'Shtrih-TachoRUS', mercury:'Mercury TA-001',
                        kasbi:'KASBI DT-20', atol:'ATOL Drive',
                        gaz:'GAZ', maz:'MAZ', ural:'Ural',
                        kraz:'KrAZ', beiben:'Beiben',
                        volvomid:'Volvo (MID modules)',
                        jingwei:'Jingwei (SITRAK heater)'};

  /* Часть "марок" в базе — не марки техники, а поставщики систем/агрегатов
     (ABS/EBS, двигатели, отопители, рефрижераторы), общие для многих машин.
     В выпадающем списке их выносим в отдельную группу, чтобы не мешались
     с марками при поиске по алфавиту. */
  var BRAND_SYSTEM_KEYS = {bendix:1, carrier:1, caterpillar:1, cumminsisb:1,
    cumminsisf:1, cumminsislisc:1, cumminsism:1, cumminsisx:1, detroitdiesel:1,
    deutz:1, eaton:1, eberspacher:1, powerstroke:1, knorrbremse:1, meritor:1,
    paccarmx13:1, thermoking:1, wabco:1, webasto:1, planar:1, yamz:1, haldex:1,
    zfastronic:1, allison:1, weichai:1, teplostar:1, jingwei:1};

  var LANG_KEY = 'pf-lang';
  /* /en/, /de/ и т.д. - отдельные страницы под hreflang (см. <head>: там
     же canonical и alternate на все версии). Каждая обязана всегда
     открываться на своём языке, иначе поисковик не сможет доверять
     hreflang - он объявляет URL источником истины по языку, а не
     localStorage конкретного браузера. Поэтому здесь язык страницы не
     угадывается: html[data-lock-lang] выставлен в самой генерируемой
     странице (scripts/build_lang_pages.py) и перебивает и localStorage,
     и navigator.languages. Корень тоже закреплён - data-lock-lang="ru"
     проставлен ему в коммите «Главная перестала притворяться английской»:
     до этого главная подстраивалась под язык гостя, и Googlebot, который
     представляется английским, индексировал русский адрес с английским
     заголовком. Гостю с другим языком вместо подмены показываем ссылку
     на его версию - см. offerLang(). */
  var LOCK_LANG = document.documentElement.getAttribute('data-lock-lang');
  function detectBrowserLang(){
    var langs = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || navigator.userLanguage || ''];
    for(var i = 0; i < langs.length; i++){
      var code = String(langs[i] || '').toLowerCase().split('-')[0];
      if(I18N[code]) return code;
    }
    return null;
  }
  function getStoredLang(){
    if(LOCK_LANG && (LOCK_LANG === 'ru' || I18N[LOCK_LANG])) return LOCK_LANG;
    try{
      var v = localStorage.getItem(LANG_KEY);
      if(v && I18N[v]) return v;
    }catch(e){}
    return detectBrowserLang() || 'ru';
  }
  var currentLang = getStoredLang();

  /* Ключи режимов поиска (Мотор и блоки / Отопитель / Тахограф): в языках без
     своего перевода берём английский, а не русский. */
  var EN_FALLBACK = {modeGroup:1, modeMotor:1, modeHeater:1, modeTacho:1, heaterHint:1, heaterEmpty:1,
    heaterBadCode:1, heaterNotFound:1, heaterNotFoundOne:1, brandGroupHeaters:1, brandGroupTacho:1,
    tachoHint:1, tachoPickBrand:1, tachoNotFound:1, tachoNone:1, codeEmpty:1,
    spnTooBig:1, needSpnFmi:1, notParsed:1, dealerAtBrands:1, sysEnginebrake:1,
    brandlessAsk:1, brandlessNone:1, donorDecoding:1};
  function t(key, vars){
    var dict = I18N[currentLang] || I18N.ru;
    var s = dict[key] != null ? dict[key] : (EN_FALLBACK[key] ? I18N.en[key] : I18N.ru[key]);
    if(vars) Object.keys(vars).forEach(function(k){ s = s.split('{' + k + '}').join(vars[k]); });
    return s;
  }
  /* Статические таблицы до загрузки словаря (assets/dtc.enc.js): ключи марок и их
     русские названия как DB.brandNames; тахографы - марки с непустой таблицей в DB.brands.
     Пересоздать, если в словаре появились или сменились марки: декодировать словарь
     так же, как home_counts() в scripts/build_lang_pages.py (base64 -> JSON), взять
     brandNames и непустые brands у тахографных ключей и заменить обе строки ниже.
     Словарь при загрузке fillBrands() всё равно пересобирает список сам. */
  var BRAND_RU_STATIC = {kamaz:"КамАЗ",renault:"Renault Trucks",mercedes:"Mercedes-Benz",isuzu:"Isuzu",man:"MAN",daf:"DAF",yamz:"ЯМЗ",sitrak:"SITRAK",iveco:"Iveco",volvo:"Volvo",scania:"Scania",deutz:"Deutz",tata:"Tata Motors",ashokleyland:"Ashok Leyland",mahindra:"Mahindra",shacman:"Shacman",dongfeng:"Dongfeng",faw:"FAW",foton:"Foton",howo:"HOWO",jac:"JAC",international:"International",detroitdiesel:"Detroit Diesel",freightliner:"Freightliner",mack:"Mack",powerstroke:"Ford PowerStroke",cumminsisb:"Cummins ISB",cumminsislisc:"Cummins ISL/ISC",cumminsism:"Cummins ISM",cumminsisx:"Cummins ISX",paccarmx13:"PACCAR MX-13",hino:"Hino",caterpillar:"Caterpillar",fuso:"Mitsubishi Fuso",thermoking:"Thermo King",carrier:"Carrier Transicold",planar:"Планар",webasto:"Webasto",eberspacher:"Eberspächer",daewoo:"Tata Daewoo",cumminsisf:"Cummins ISF 2.8/3.8",bendix:"Bendix ABS/ESP",wabco:"WABCO ABS/ESC",eaton:"Eaton Fuller",gaz:"ГАЗ",maz:"МАЗ",ural:"Урал",kraz:"КрАЗ",kenworth:"Kenworth",peterbilt:"Peterbilt",westernstar:"Western Star",bharatbenz:"BharatBenz",ram:"RAM",beiben:"Beiben",meritor:"Meritor (ex-WABCO)",knorrbremse:"Knorr-Bremse EBS",hyundai:"Hyundai",hongyan:"SAIC-Iveco Hongyan",haldex:"Haldex ABS",zfastronic:"ZF AS-Tronic",allison:"Allison",weichai:"Weichai/Shaanxi WP10/WP12",ford:"Ford Trucks",dodge:"Dodge",teplostar:"Теплостар",volkswagen:"Volkswagen",fordcargo:"Ford Cargo",agrale:"Agrale",mwm:"MWM",udtrucks:"UD Trucks",baw:"BAW",ivecoedc:"Iveco EDC",ivecoeurotronic:"Iveco EuroTronic",manzbr2:"MAN ZBR2",manebs:"MAN EBS",volvomid:"Volvo (блоки MID)",jingwei:"Jingwei (отопитель SITRAK)",vdo:"VDO DTCO",shtrih:"Штрих-ТахоRUS",mercury:"Меркурий ТА-001",kasbi:"КАСБИ DT-20",atol:"Атол Драйв"};
  var TACHO_STATIC = {vdo:1,atol:1,mercury:1,shtrih:1,kasbi:1};
  function brandName(key){
    if(currentLang !== 'ru' && BRAND_OVERRIDE[key]) return BRAND_OVERRIDE[key];
    return DB ? DB.brandNames[key] : BRAND_RU_STATIC[key];
  }
  function fmiLookup(f){
    var tbl = FMI_I18N[currentLang];
    if(tbl && tbl[f] != null) return tbl[f];
    return DB.fmi[f];
  }
  /* FMI из стандарта и описанный в словаре (0-31). Всё остальное - нестандартное. */
  function fmiKnown(fmi){
    var f = String(fmi);
    if(!fmiOk(f)) return false;
    var f0 = stripZero(f) || f;
    return fmiLookup(f0) != null || fmiLookup(f) != null;
  }
  function fmiText(fmi){
    var f = String(fmi), v = fmiLookup(f);
    if(v != null) return v;
    var f2 = stripZero(f);
    return f2 ? fmiLookup(f2) : v;
  }

  function fillBrands(){
    syncTacho();
    var prevValue = sel.value;
    while(sel.options.length > 1) sel.removeChild(sel.lastChild);
    function byName(a, b){
      return brandLabel(a).localeCompare(brandLabel(b), currentLang === 'ru' ? 'ru' : currentLang);
    }
    var vehicleKeys = [], systemKeys = [];
    modeKeys().forEach(function(k){
      if(MODE === 'main' && BRAND_SYSTEM_KEYS[k]) systemKeys.push(k); else vehicleKeys.push(k);
    });
    vehicleKeys.sort(byName);
    systemKeys.sort(byName);
    function addGroup(label, keys, cls){
      var g = document.createElement('optgroup');
      g.label = label; g.className = cls;
      keys.forEach(function(k){
        var o = document.createElement('option');
        o.value = k; o.textContent = brandLabel(k);
        g.appendChild(o);
      });
      sel.appendChild(g);
    }
    var vLabel = MODE === 'heater' ? t('brandGroupHeaters') :
                 MODE === 'tacho' ? t('brandGroupTacho') : t('brandGroupVehicles');
    addGroup(vLabel, vehicleKeys, 'grp-vehicles');
    if(MODE === 'main') addGroup(t('brandGroupSystems'), systemKeys, 'grp-systems');
    sel.value = prevValue;
  }

  /* ---------- режимы поиска: Мотор и блоки / Отопитель / Тахограф ----------
     Режим меняет список марок, подсказку поля и путь разбора. Отопители
     ушли из «Мотор и блоки» в свой режим: их короткие коды (031, 12) легко
     спутать с кодами других марок. Ссылка ?b=eberspacher (webasto, planar,
     teplostar) сама включает режим «Отопитель». Режим хранится в адресе:
     ?mode=heater, ?mode=tacho; без параметра - «Мотор и блоки». */
  var HEATER_BRANDS = {eberspacher:1, webasto:1, planar:1, teplostar:1};
  /* Таблицы, по которым ищем отопитель без выбранной марки. Teplostar - алиас Planar. */
  var HEATER_TABLES = ['eberspacher', 'webasto', 'planar'];
  /* Разделы тахографов. Список расширяемый: марка появится в выборе, когда её словарь
     появится в DB.brands (пока пуст - кнопка режима скрыта). */
  var TACHO_BRANDS = ['vdo', 'stoneridge', 'atol', 'mercury', 'shtrih', 'kasbi'];
  var MODE_NAMES = {main:1, heater:1, tacho:1};
  var modeBox = document.getElementById('pf-modes');
  var tachoBtn = modeBox ? modeBox.querySelector('[data-mode="tacho"]') : null;
  var cancelDemo = null;

  function initialMode(){
    var m = /[?&]mode=([a-z]+)/.exec(location.search);
    if(m && MODE_NAMES[m[1]]) return m[1];
    var h = /^#(main|heater|tacho)$/.exec(location.hash);
    if(h) return h[1];
    var b = /[?&]b=([a-z0-9]+)/.exec(location.search);
    if(b && HEATER_BRANDS[b[1]]) return 'heater';
    return 'main';
  }
  var MODE = initialMode();
  paintModes();

  function brandLabel(k){ return brandName(k) || k; }
  function tachoHas(k){
    if(!DB) return !!TACHO_STATIC[k];
    var tb = DB.brands && DB.brands[k];
    return !!tb && Object.keys(tb).length > 0;
  }
  function brandKeys(){ return Object.keys(DB ? DB.brandNames : BRAND_RU_STATIC); }
  function modeKeys(){
    if(MODE === 'tacho') return TACHO_BRANDS.filter(tachoHas);
    return brandKeys().filter(function(k){
      return MODE === 'heater' ? !!HEATER_BRANDS[k] : (!HEATER_BRANDS[k] && TACHO_BRANDS.indexOf(k) < 0);
    });
  }
  /* Кнопку «Тахограф» показываем только при наличии хотя бы одного раздела. */
  function syncTacho(){
    var has = TACHO_BRANDS.some(tachoHas);
    if(tachoBtn) tachoBtn.hidden = !has;
    if(!has && MODE === 'tacho') MODE = 'main';
    paintModes();
  }
  function paintModes(){
    if(!modeBox) return;
    Array.prototype.forEach.call(modeBox.querySelectorAll('[data-mode]'), function(b){
      b.setAttribute('aria-pressed', String(b.getAttribute('data-mode') === MODE));
    });
  }
  /* Подсказка поля и видимость выбора стандарта под режим. Вызывается после fillMid. */
  function applyModeUi(){
    if(!input) return;
    if(modeBox) modeBox.setAttribute('aria-label', t('modeGroup'));
    if(MODE === 'heater') input.placeholder = t('heaterHint');
    else if(MODE === 'tacho') input.placeholder = t('tachoHint');
    if(MODE !== 'main' && std) std.style.display = 'none';
  }
  /* Адрес держит режим: ?mode=heater. Выбранная марка и результат при смене сбрасываются,
     поэтому параметры разбора (b, q, c, mid) из адреса тоже убираем. */
  function writeModeUrl(){
    try{
      var p = new URLSearchParams(location.search);
      if(MODE === 'main') p.delete('mode'); else p.set('mode', MODE);
      ['b', 'q', 'c', 'mid'].forEach(function(k){ p.delete(k); });
      var qs = p.toString();
      history.replaceState(null, '', location.pathname + (qs ? '?' + qs : '') + location.hash);
    }catch(e){}
  }
  function setMode(m){
    if(m === 'tacho' && !TACHO_BRANDS.some(tachoHas)) m = 'main';
    if(cancelDemo) cancelDemo();
    MODE = m;
    paintModes();
    sel.value = '';
    fillBrands();
    fillMid();
    applyModeUi();
    out.innerHTML = '';
    writeModeUrl();
  }
  if(modeBox){
    modeBox.addEventListener('click', function(e){
      var btn = e.target.closest && e.target.closest('[data-mode]');
      if(!btn || btn.hidden) return;
      var m = btn.getAttribute('data-mode');
      if(m !== MODE) setMode(m);
    });
  }

  function runMode(){ return MODE === 'heater' ? runHeater() : runTacho(); }

  /* Код с пульта отопителя -> ключ таблицы. Чистая функция: без сети и без
     состояния страницы (её же проверяет самопроверка в scratchpad).
     Префиксы КОД/CODE/ERR, E, E-, F снимаем; кириллические двойники в коде
     переводим в латиницу. eberspacher - три цифры, webasto - два знака
     (hex, заглавные), planar - число без ведущих нулей. */
  function heaterNorm(table, raw){
    var s = String(raw || '').toUpperCase().replace(/\s+/g, '');
    s = s.replace(/^(КОД|CODE|ERROR|ERR)[-:.]?/, '');
    s = s.replace(/[АВЕКМНОРСТХ]/g, function(c){
      return {'А':'A','В':'B','Е':'E','К':'K','М':'M','Н':'H','О':'O','Р':'P','С':'C','Т':'T','Х':'X'}[c];
    });
    /* Префикс снимаем по таблице. Eberspächer пишет E и три цифры. Webasto - либо
       две цифры, либо F и два hex-знака («F09»): «E0», «F0», «EA» у Webasto не код,
       и обрезать первую букву у них нельзя (получалось «00 - Ошибок нет»). */
    if(table === 'eberspacher') s = s.replace(/^E[-:.]?/, '');
    else if(table === 'webasto'){
      if(/^F[-:.]?[0-9A-F]{2}$/.test(s)) s = s.replace(/^F[-:.]?/, '');
    }
    else s = s.replace(/^[EF][-:.]?/, '');
    if(table === 'eberspacher') return /^\d{1,3}$/.test(s) ? ('000' + s).slice(-3) : null;
    if(table === 'webasto') return /^\d{1,2}$/.test(s) ? ('0' + s).slice(-2) : null;
    if(table === 'planar') return /^\d{1,3}$/.test(s) ? String(parseInt(s, 10)) : null;
    return null;
  }

  /* TACHO-PURE-BEGIN - чистые функции тахографа (без DOM и сети); проверяются
     отдельно на настоящем словаре (scratchpad/tacho-wire/test_tacho.js).
     tachoText: ввод и текст экрана приводятся к одной форме - нижний регистр, ё -> е,
     знаки -> пробел; в словах с цифрами (коды «0х1х», «6А 82») кириллические двойники
     (а в е к м н о р с т у х) становятся латиницей. Так «0х1х», «0X1X» и «0x1x» дают
     одну строку; ключи словаря записаны этой же функцией. Слова без цифр не трогаем. */
  var TACHO_CYR = {'а':'a','в':'b','е':'e','к':'k','м':'m','н':'h','о':'o','р':'p','с':'c','т':'t','у':'y','х':'x'};
  function tachoText(s){
    var base = String(s == null ? '' : s).toLowerCase().replace(/ё/g, 'е')
      .replace(/[^a-z0-9а-я]+/g, ' ').replace(/^ | $/g, '');
    return base.split(' ').map(function(tok){
      return /\d/.test(tok) ? tok.replace(/[а-я]/g, function(ch){ return TACHO_CYR[ch] || ch; }) : tok;
    }).join(' ');
  }
  /* Ключ записи словаря: числовой код (VDO - три цифры, Меркурий и Штрих - две,
     КАСБИ Ж.1 - hex «6A82»), иначе «t:» + текст экрана. Алиасы словаря (tachoAlias)
     проверяются раньше: текст экрана, его ядро, номер «x 20», hex «0x0A». */
  function tachoNormKey(brand, raw, alias){
    var t = tachoText(raw);
    if(!t) return '';
    var c = t.split(' ').join('');
    var al = (alias && alias[brand]) || {};
    if(Object.prototype.hasOwnProperty.call(al, t)) return al[t];
    if(Object.prototype.hasOwnProperty.call(al, c)) return al[c];
    if(brand === 'vdo' && /^\d{1,3}$/.test(c)) return ('00' + c).slice(-3);
    if((brand === 'mercury' || brand === 'shtrih') && /^\d{1,2}$/.test(c)) return ('0' + c).slice(-2);
    if(brand === 'kasbi' && /^[0-9a-f][0-9a-fx]{3}$/.test(c)) return c.toUpperCase();
    /* «0x6A82» - hex с приставкой 0x: ключ таблицы тот же, что у «6A82». */
    if(brand === 'kasbi' && /^0x[0-9a-f]{4}$/.test(c)) return c.slice(2).toUpperCase();
    return 't:' + t;
  }
  /* Поиск по словам: каждое слово запроса - начало какого-нибудь слова записи
     (код, текст экрана, смысл). Источник и «Что делать» в поиск не входят. Запрос короче
     трёх знаков не ищем: иначе «5» дало бы случайные совпадения. */
  function tachoSearch(db, brands, q, limit){
    var t = tachoText(q), toks = t ? t.split(' ') : [];
    if(!toks.length || toks.join('').length < 3) return [];
    var out = [];
    brands.forEach(function(b){
      var tbl = (db.brands && db.brands[b]) || {};
      var scr = (db.tachoScreen && db.tachoScreen[b]) || {};
      Object.keys(tbl).forEach(function(k){
        if(out.length >= limit) return;
        var meaning = String(tbl[k]).split(' Что делать:')[0].split(' Источник:')[0];
        var hay = tachoText((k.indexOf('t:') === 0 ? k.slice(2) : k) + ' ' + (scr[k] || '') + ' ' + meaning).split(' ');
        var ok = toks.every(function(tok){
          return hay.some(function(w){ return w.indexOf(tok) === 0; });
        });
        if(ok) out.push({brand: b, key: k, text: tbl[k], screen: scr[k] || ''});
      });
    });
    return out;
  }
  /* TACHO-PURE-END */

  /* Ключ кода тахографа (см. tachoNormKey): алиасы и числовые правила марки. */
  function normTachoKey(brand, raw){
    return tachoNormKey(brand, raw, DB ? DB.tachoAlias : null);
  }

  /* Отопитель: одна таблица - один запрос (лимит воркера); без марки - по всем
     трём таблицам, каждая со своим ключом. */
  function runHeater(){
    var mySeq = ++runSeq;
    var typed = String(input.value || '').trim().replace(/\s+/g, ' ');
    if(!typed){ render(note(t('heaterEmpty'))); return; }
    var brand = sel.value;
    var tables = brand ? donorsOf(brand) : HEATER_TABLES;
    var jobs = [];
    tables.forEach(function(tb){
      var key = heaterNorm(tb, typed);
      if(key !== null) jobs.push({tb: tb, key: key});
    });
    if(!jobs.length){ render(note(t('heaterBadCode'))); return; }
    render(note(t('pcodeSearching')));
    ready().then(function(){
      return Promise.all(jobs.map(function(j){
        return fetchPcodeOne(j.tb, j.key, currentLang).then(function(hits){
          return {j: j, hits: hits};
        }, function(e){ return {j: j, hits: [], err: e}; });
      }));
    }).then(function(res){
      if(mySeq !== runSeq) return;
      var found = res.filter(function(r){ return r.hits.length > 0; });
      if(!found.length){
        var failed = res.filter(function(r){ return r.err && !r.err.badCode; });
        if(failed.length === res.length){ render(pcodeErrorText(failed[0].err, '')); return; }
        render(note(brand
          ? t('heaterNotFoundOne', {code: esc(typed), brand: esc(brandLabel(brand))})
          : t('heaterNotFound', {list: HEATER_TABLES.map(function(k){ return esc(brandLabel(k)); }).join(' / ')})));
        return;
      }
      var steps = [];
      found.forEach(function(r){
        r.hits.forEach(function(h){
          steps.push({st: brandLabel(r.j.tb),
            tx: '<span class="mono">' + esc(r.j.key) + '</span> <b>' + esc(h.text) + '</b>', cls: 'ok'});
        });
      });
      render(chain(steps), true);
    }).catch(function(){ if(mySeq === runSeq) render(note(t('loadError'))); });
  }

  /* Тахограф: только открытый словарь DB.brands, без воркера. Сначала точный ключ
     (с алиасами), не нашлось - поиск по словам. Без марки ищем по всем маркам тахографов. */
  function runTacho(){
    var mySeq = ++runSeq;
    var typed = String(input.value || '').trim();
    if(!typed){ render(note(t('codeEmpty'))); return; }
    var brand = sel.value;
    ready().then(function(){
      if(mySeq !== runSeq) return;
      var brands = brand ? [brand] : TACHO_BRANDS.filter(tachoHas);
      var E = en();
      var hits = [];
      brands.forEach(function(b){
        var key = tachoNormKey(b, typed, DB.tachoAlias);
        var tbl = (DB.brands && DB.brands[b]) || {};
        if(Object.prototype.hasOwnProperty.call(tbl, key)) hits.push({brand: b, key: key, text: tbl[key], screen: ''});
      });
      if(!hits.length) hits = tachoSearch(DB, brands, typed, 8);
      if(!hits.length){ render(note(t('tachoNone'))); return; }
      var steps = hits.slice(0, 8).map(function(h){
        var txt = (E && E.brands && E.brands[h.brand] && E.brands[h.brand][h.key]) || h.text;
        var isText = h.key.indexOf('t:') === 0;
        return {st: brandLabel(h.brand),
          tx: (isText ? '' : '<span class="mono">' + esc(h.key) + '</span> ') + '<b>' + esc(txt) + '</b>',
          cls: 'ok'};
      });
      render(chain(steps), true);
    }).catch(function(){ if(mySeq === runSeq) render(note(t('loadError'))); });
  }

  function applyLang(lang){
    if(!I18N[lang]) lang = 'ru';
    currentLang = lang;
    try{ localStorage.setItem(LANG_KEY, lang); }catch(e){}
    document.documentElement.lang = lang;
    document.title = t('pageTitle');
    var metaDesc = document.querySelector('meta[name="description"]');
    if(metaDesc) metaDesc.setAttribute('content', t('metaDescription'));
    document.querySelectorAll('[data-i18n]').forEach(function(el){
      el.innerHTML = t(el.getAttribute('data-i18n'));
    });
    /* Плашка нужна только там, где описания придут не на языке
       интерфейса: русскому и английскому объяснять нечего. */
    dataNote.style.display = (lang === 'ru' || lang === 'en') ? 'none' : 'block';
    langSelect.value = lang;
    langSelect.setAttribute('aria-label', t('langAria'));
    fillBrands();
    applyModeUi();
    if(input.value.trim()) run();
  }

  /* Ссылка на свою языковую версию для гостя с другим браузерным языком.
     Зачем именно ссылка, а не подмена языка: адрес объявлен источником
     истины по языку (canonical + hreflang), и страница обязана оставаться
     той, за которую себя выдаёт. Заголовок, H1 и canonical здесь не
     трогаются вовсе - меняется только одна строка над первым экраном.

     Адрес берём из hreflang этой же страницы, а не собираем руками: так
     ссылка не может разойтись с реальной версией. Показываем один раз -
     закрытую плашку помним в localStorage. */
  var OFFER_KEY = 'pf-lang-offer';

  function offerLang(){
    var guest = detectBrowserLang();
    if(!guest || guest === currentLang) return;
    var txt = (I18N[guest] || {}).langOffer;
    if(!txt) return;
    var alt = document.querySelector('link[rel="alternate"][hreflang="' + guest + '"]');
    if(!alt) return;
    var href = alt.getAttribute('href');
    if(!href || href === location.href) return;
    try{ if(localStorage.getItem(OFFER_KEY) === guest) return; }catch(e){}

    var box = document.createElement('div');
    box.className = 'lang-offer';
    box.style.cssText = 'display:flex;align-items:center;gap:10px;flex-wrap:wrap;' +
      'margin:0 0 18px;padding:9px 13px;border:1px solid var(--line);border-radius:12px;' +
      /* Фон и рамка - переменными, иначе на дневной теме плашка осталась бы
         тёмной: светлая тема переопределяет ровно эти --line/--line-2. */
      'background:var(--line-2);color:var(--ink);font:500 14px/1.35 var(--sans)';
    var a = document.createElement('a');
    a.href = href; a.hreflang = guest; a.lang = guest;
    a.textContent = txt + ' →';
    a.style.cssText = 'color:var(--signal);text-decoration:none';
    var close = document.createElement('button');
    close.type = 'button';
    close.textContent = '×';
    close.setAttribute('aria-label', 'Close');
    close.style.cssText = 'margin-left:auto;min-width:32px;min-height:32px;cursor:pointer;' +
      'background:none;border:0;color:var(--ink-3);font-size:18px;line-height:1';
    close.addEventListener('click', function(){
      box.parentNode && box.parentNode.removeChild(box);
      try{ localStorage.setItem(OFFER_KEY, guest); }catch(e){}
    });
    box.appendChild(a); box.appendChild(close);
    var host = document.querySelector('.scene .w') || document.body;
    host.insertBefore(box, host.firstChild);
  }

  function load(){
    if(DB) return Promise.resolve(DB);
    if(window.__TDP_DTC){
      DB = window.__TDP_DTC; fillBrands();
      return Promise.resolve(DB);
    }
    if(loading) return loading;
    loading = new Promise(function(resolve, reject){
      var t = document.createElement('script');
      t.src = '/assets/dtc.enc.js'; t.async = true;
      t.onload = function(){
        DB = window.__TDP_DTC;
        if(!DB) return reject(new Error('пустой справочник'));
        fillBrands(); resolve(DB);
      };
      t.onerror = function(){ reject(new Error('не загрузился')); };
      document.head.appendChild(t);
    });
    return loading;
  }
  /* Словарь (dtc.enc.js, ~3 МБ) грузим по первому действию, а не при открытии
     страницы. Список марок до того уже виден из BRAND_RU_STATIC и TACHO_STATIC.
     Сразу грузим, если адрес ведёт в разбор (?q, ?c, ?b) или в режим отопителя
     или тахографа. Фокус при загрузке не считаем: поле получает его автофокусом. */
  fillBrands();
  var warmed = false;
  function warm(){
    if(warmed) return;
    warmed = true;
    load().catch(function(){});
  }
  if(MODE !== 'main' || /[?&](q|c|b)=/.test(location.search)) warm();
  input.addEventListener('pointerdown', warm);
  input.addEventListener('keydown', warm);
  input.addEventListener('input', warm);
  sel.addEventListener('pointerdown', warm);
  sel.addEventListener('keydown', warm);
  sel.addEventListener('change', warm);
  go.addEventListener('pointerdown', warm);

  /* Английские описания лежат отдельным файлом и грузятся только
     когда язык не русский. Основная аудитория русская - незачем
     заставлять её тянуть лишние полмегабайта на обочине с одной
     палкой связи. Не загрузился - молча остаёмся на русском. */
  var DB_EN = null, loadingEn = null;
  function loadEn(){
    if(currentLang === 'ru') return Promise.resolve(null);
    if(DB_EN) return Promise.resolve(DB_EN);
    if(window.__TDP_DTC_EN){ DB_EN = window.__TDP_DTC_EN; return Promise.resolve(DB_EN); }
    if(loadingEn) return loadingEn;
    loadingEn = new Promise(function(resolve){
      var s = document.createElement('script');
      s.src = '/assets/dtc.en.js'; s.async = true;
      s.onload  = function(){ DB_EN = window.__TDP_DTC_EN || null; resolve(DB_EN); };
      s.onerror = function(){ resolve(null); };
      document.head.appendChild(s);
    });
    return loadingEn;
  }
  /* Русский - язык базы и значение по умолчанию. Для всех остальных
     языков сначала смотрим английскую таблицу, а где перевода ещё
     нет - показываем русское описание: неполный ответ лучше пустого. */
  function en(){ return currentLang === 'ru' ? null : DB_EN; }

  /* Нормализация написания: регистр и пробелы (в т.ч. неразрывные,
     двойные, табы) не должны влиять на распознавание кода. */
  function normCode(t){
    var u = t.toUpperCase().replace(/\s+/g, ' ').trim();
    /* Слова СПН/ФМИ по-русски и буквы-двойники латиницы в коде: «Р0340»
       пишут русской Р, а P - это та же буква для сканера. Замена только
       по верхнему регистру уже приведённой строки. */
    u = u.replace(/СПН/g, 'SPN').replace(/ФМИ/g, 'FMI');
    return u.replace(/[РСАЕОХВМТНК]/g, function(c){
      return {'Р':'P','С':'C','А':'A','Е':'E','О':'O','Х':'X','В':'B','М':'M','Т':'T','Н':'H','К':'K'}[c];
    });
  }

  /* SPN/FMI почти всегда чисто десятичные (стандарт J1939), но у
     некоторых марок (Ford F-MAX/Ecotorq) заводская таблица использует
     собственную буквенно-цифровую нумерацию (например "06F", "12DC") -
     это не HEX-запись десятичного SPN (проверено: не совпадает по
     смыслу с универсальной J1939-таблицей), а отдельная система марки.
     Что распознаётся как число - остаётся числом (нулевой риск для
     всех остальных марок); буквенные коды остаются строкой и просто не
     участвуют в группировке по системе/срочности по номеру (там есть
     резервный разбор по словам в тексте) - это лучше, чем не находиться
     вовсе. */
  function codeVal(s){
    // Ведущий ноль в многозначном числе - примета марок вроде Ford,
    // где это несущий часть формата код ("084"), а не десятичное
    // число со стилистическим нулём спереди: parseInt его бы съел
    // ("084" -> 84) и сломал поиск по таблице марки, где ключ хранится
    // как есть. Настоящие J1939 SPN/FMI ведущих нулей не пишут.
    if(/^0\d+$/.test(s)) return s;
    return /^\d+$/.test(s) ? parseInt(s, 10) : s;
  }

  /* На деле приборка почти всегда показывает SPN/FMI с отступом до
     фиксированной ширины ("03043-00" - реальный пример с фото приборной
     панели), и codeVal() выше нарочно хранит такую запись строкой -
     иначе сломалась бы собственная нумерация Ford. Но для любой другой
     марки и для стандартных J1939-таблиц (SPN.FMI в заводских таблицах,
     urgentSpn/urgentFmi, классификация по системе для «гирлянды») это
     просто десятичное число с нулём для красоты - и его тоже нужно
     узнавать, иначе самый обычный код с приборки MAN/Scania/Volvo
     показывает «нет в справочнике» вместо расшифровки. stripZero()
     отдаёт раздетый вид ТОЛЬКО когда есть что снимать: у настоящих
     кодов Ford в записи всегда есть буква ("06F"), чистого "\d+" там не
     бывает, так что под фильтр они не попадают и не путаются с чужим
     десятичным SPN, которому просто не повезло совпасть по цифрам.
     hasNum() - тот же поиск по массиву целых чисел: сначала как есть
     (без стоимости для всех остальных марок), и только если не нашлось -
     в раздетом виде. */
  /* FMI по стандарту J1939 - число 0..31. Больше - это не FMI, а соседнее
     число: в «636 11, 190 2» без этой проверки выходил SPN 11 / FMI 190. */
  function fmiOk(v){ return !/^\d+$/.test(String(v)) || parseInt(v, 10) <= 31; }
  function stripZero(s){
    return (typeof s === 'string' && /^0\d+$/.test(s)) ? String(parseInt(s, 10)) : null;
  }
  function hasNum(arr, v){
    if(arr.indexOf(v) >= 0) return true;
    var s = stripZero(v);
    return s ? arr.indexOf(parseInt(s, 10)) >= 0 : false;
  }

  /* Пара SPN/FMI внутри уже нормализованной строки. Границы чисел соблюдаются:
     «1234567.1» - это число вне диапазона, а не SPN 234567 (раньше пару
     отрезали с середины числа). Число слева от пары («2 100.1») или
     разделитель с числом справа («100.1.1», «1.1.1.1») - не пара, а
     склейка чужих чисел: такой ввод отказом, без догадок. Знаки и слова
     после пары («100.0!!», «12401-20 шт») - лишний хвост, отбрасываем. */
  function pairFind(up){
    var rx = [
      /(^|[^0-9A-F])(?:SPN\s*[:\-]?\s*)?([0-9A-F]{1,10})\D{0,20}FMI\s*[:\-]?\s*([0-9A-F]{1,3})/,
      /(^|[^0-9A-F])([0-9A-F]{1,10})\s*[\/\-.,]\s*([0-9A-F]{1,3})(?![0-9A-F])/,
      /(^|[^0-9A-F])([0-9A-F]{1,10})\s+([0-9A-F]{1,3})$/
    ];
    var m = null;
    for(var i = 0; i < rx.length && !m; i++) m = rx[i].exec(up);
    if(!m || !fmiOk(m[3])) return null;
    if(/\d/.test(up.slice(0, m.index + m[1].length))) return {bad:true};
    if(/^\s*[.\-\/,]\s*\d/.test(up.slice(m.index + m[0].length))) return {bad:true};
    if(/^\d+$/.test(m[2]) && parseInt(m[2], 10) > 524287) return {bigSpn: m[2]};
    return {spn:codeVal(m[2]), fmi:codeVal(m[3])};
  }

  function parseAuto(t){
    /* Знаки восклицания, точка и вопрос в самом конце - хвост («0000!!», «SPN45.»),
       код от него не меняется. Слова после кода обрабатывает разбор ниже. */
    var up = normCode(t).replace(/\s*[!?.;:]+\s*$/, '');
    /* Номер блока КамАЗ-5490 пишут с приставкой ("ADM3 10203", "MR2-12420").
       Приставка - не часть кода в сканере; ищем по цифрам как по обычному
       дилерскому номеру (DB.scan). Без этого "ADM310203" не находилось. */
    var blk = up.match(/^(?:ADM3|MR2)\s*-?\s*(\d{4,6})$/);
    if(blk) return {pcode: blk[1]};
    // Панель показывает код вместе с порядковым номером ошибки
    // ("2 03043-00"), поэтому ищем код с разделителем где угодно
    // в строке, а не только когда это весь ввод целиком. Слово SPN
    // необязательно ("97 FMI 3" пишут чаще, чем полную форму), а
    // между числом и словом FMI допускаем что угодно или ничего -
    // код нередко вводят слитно: "97FMI3".
    // Флэш-код мигающей лампы китайских EDC7 (Weichai WP10/WP12 и всё,
    // что на них собрано - Foton, Shacman, HOWO) пишут тремя группами
    // через дефис: "1-3-2" = три вспышки. SPN/FMI так не пишут никогда
    // (там две группы, не три), поэтому форма однозначная и брать её
    // можно до разбора SPN/FMI, иначе "1-3-2" разобралось бы как
    // SPN 1 / FMI 3. В таблицах код лежит слитно ("132").
    var flash = up.replace(/\s+/g, '').match(/^(\d)-(\d)-(\d)$/);
    if(flash) return {pcode: flash[1] + flash[2] + flash[3]};
    // Заводской код с буквой впереди и дефисом внутри ("P0105-01" у MWM,
    // "P0607-283" у BAW) до этого уезжал в разбор SPN/FMI: регулярка ниже
    // не привязана к началу строки и видела в нём "0105-01" = SPN 105 /
    // FMI 1. Ответ выходил чужой, но правдоподобный - это хуже пустого.
    // Буква в начале - надёжная примета заводского кода, SPN и FMI всегда
    // числа. Слова SPN/FMI в строке правило отменяют: "97FMI3" и "SPN16" -
    // это ввод по стандарту, а не марочный код.
    /* Первый токен с буквой впереди - дилерский код, всё после него (слова,
       точка, «шт», «!!») - хвост от списка или заметок. «P0105-01 Датчик
       давления», «P0105-01.», «P0105/01» (слеш у дефисного кода = дефис)
       читаются одинаково. Токен нужен с цифрой и длиной от четырёх знаков;
       если сразу после него идёт «-число» или «.число», это не конец кода -
       дальше разбираем как SPN/FMI (и там такой ввод отказ). */
    var lead = up.replace(/\s+/g, '');
    var lt = /^([A-Z][A-Z0-9]*(?:[-\/][A-Z0-9]+)*)/.exec(lead);
    if(lt && lt[1].length >= 4 && lt[1].length <= 12 && /\d|[-\/]/.test(lt[1]) &&
       !/SPN|FMI/.test(lead) && !/^[.\-\/,]\d/.test(lead.slice(lt[1].length))){
      return {pcode: lt[1].replace('/', '-')};
    }
    var pm = pairFind(up);
    if(pm) return pm;
    var only = up.match(/^SPN\s*[:\-]?\s*(\d{1,10})$/) || up.match(/^(\d{1,10})$/);
    if(only){
      /* Номер больше 524287 - не SPN. Но и не обязательно обрывок: у марок с
         дилерскими номерами из семи цифр он может быть ключом их таблицы.
         Поэтому это ещё и дилерский код; если его нигде нет - ответ «нет в J1939». */
      if(parseInt(only[1], 10) > 524287) return {pcode: only[1], bigSpn: only[1]};
      return {spn:codeVal(only[1]), fmi:null};
    }
    /* Слово FMI без номера SPN («FMI 1», «100 FMI») - обрывок, а не дилерский код. */
    if(/FMI/.test(up)) return {bad:true, fmiOnly:true};
    // Дилерские коды в справочнике очень разной формы: P2BA7, B000101,
    // 00100, "AA 9999", 9A9A99, P0115-01 (MWM), P1204-1196 (BAW, P-код +
    // внутренний номер Bosch, до 10 символов). Общее у них одно - короткий
    // буквенно-цифровой набор, дефис внутри - тоже часть кода, не
    // разделитель SPN/FMI (буква P впереди туда попасть не даёт). Чисто
    // цифровые сюда не берём: это SPN.
    if(/^[A-Z0-9-]{4,10}$/.test(up.replace(/\s+/g,'')) && /[A-Z]/.test(up)){
      return {pcode:up.replace(/\s+/g,' ')};
    }
    return {bad:true};
  }

  function parse(raw, standard){
    var t = (raw || '').trim();
    if(!t) return null;
    if(standard === 'pcode') return {pcode:normCode(t)};
    if(standard === 'spnfmi'){
      var up = normCode(t);
      var pm = pairFind(up);
      if(pm) return pm;
      var only = up.match(/^SPN\s*[:\-]?\s*(\d{1,10})$/) || up.match(/^(\d{1,10})$/);
      if(only){
        if(parseInt(only[1], 10) > 524287) return {bigSpn: only[1]};
        return {spn:codeVal(only[1]), fmi:null};
      }
      return {bad:true};
    }
    return parseAuto(t);
  }

  var MEANING = ['выше','ниже','превыш','обрыв','замыкан','кз ','кз.','короткое',
                 'недостовер','не поступ','отсутств','нет сигнал','неисправ',
                 'перегрев','малое','низк','высок','больше','меньше','утечк','заклин'];

  /* Подсказка по FMI: своя легенда марки (MAN, Renault) или стандарт J1939. */
  function fmiHintOf(owner, fmi){
    var own = owner && OWN_FMI[owner];
    if(!own) return fmiText(fmi);
    if(own === 'renault') return t('fmiTable', {brand: brandName('renault'), fmi: fmi});
    return ownLegend(own, fmi);
  }
  function ownLegend(key, fmi){
    var E = en();
    var tbl = (E && E.fmiBrand && E.fmiBrand[key]) || (DB.fmiBrand && DB.fmiBrand[key]);
    if(!tbl) return null;
    var v = tbl[String(fmi)];
    if(v == null) v = tbl[stripZero(String(fmi))];
    return v != null ? v : null;
  }
  function withFmiHint(desc, fmi, owner){
    var f = fmiHintOf(owner, fmi);
    if(!f) return desc;
    var low = desc.toLowerCase();
    if(owner && OWN_FMI[owner] && low.indexOf(f.toLowerCase()) >= 0) return desc;
    /* Текст уже называет смысл FMI («данные ниже нормы» в записи и в легенде) -
       второй раз саму фразу не пишем, а хвост легенды («низкая срочность»,
       «наиболее серьёзный уровень») дописываем, если его в тексте ещё нет. */
    var core0 = f.split(/ \(| — |, /)[0];
    if(core0 && low.indexOf(core0.toLowerCase()) >= 0){
      var rest = f.slice(core0.length).replace(/^\s*(—|,)\s*/, '').trim();
      if(!rest || low.indexOf(rest.toLowerCase()) >= 0) return desc;
      return desc + (rest.charAt(0) === '(' ? ' ' : ' — ') + rest;
    }
    if(desc.length > 60 && MEANING.some(function(w){ return low.indexOf(w) >= 0; })) return desc;
    return desc + ' — ' + f;
  }

  /* Имя параметра по SPN - одна лестница источников: заводская
     таблица марки, стандарт J1939, общий справочник. На каждой
     ступени сначала английский (если язык не русский), потом русский. */
  function spnLookup(s, brand){
    var E = en();
    return (E && E.spn[s])
        || (E && brand && E.spnName[brand] && E.spnName[brand][s])
        || (E && E.universal[s])
        || DB.spn[s]
        || (brand && DB.spnNameRu[brand] && DB.spnNameRu[brand][s])
        || (brand && DB.spnNameEn[brand] && DB.spnNameEn[brand][s])
        || DB.universal[s];
  }
  /* Русское имя параметра - та же лестница, что у spnLookup, но без английского:
     по нему определяем систему, и она не должна зависеть от языка страницы. */
  function ruSpnName(spn, brand){
    var s = String(spn), s2 = stripZero(s);
    function one(k){
      return DB.spn[k] || (brand && DB.spnNameRu[brand] && DB.spnNameRu[brand][k]) || DB.universal[k];
    }
    return one(s) || (s2 ? one(s2) : null) || null;
  }
  function spnName(spn, brand){
    var s = String(spn), found = spnLookup(s, brand);
    if(found) return found;
    var s2 = stripZero(s);
    return s2 ? spnLookup(s2, brand) : found;
  }

  /* ============================================================
     БЛОКИ МАШИНЫ

     КамАЗ - это несколько блоков управления под одним шильдиком:
     двигатель (J1939), тормоза EBS3 WABCO, подвеска ECAS, коробка ZF,
     ретардер, а у 5490 ещё старый блок Mercedes по K-line. Каждый
     отдаёт свои коды, и один и тот же SPN.FMI у разных блоков значит
     разное. Поэтому для марки с реестром DB.blocks ищем по всем блокам
     по порядку и показываем ВСЕ попадания, каждое с подписью блока.

     Блоки с ownFmi (свой FMI, таблица производителя блока): номер FMI
     там не стандартный J1939, поэтому подсказку по FMI, срочность по
     urgentSpn/urgentFmi и горизонт по FMI не применяем. Электрику и
     критичность определяем по тексту записи.
     ============================================================ */
  function blockItemIn(lists, id){
    var found = null;
    Object.keys(lists || {}).some(function(b){
      return lists[b].some(function(x){
        if(x.id === id){ found = x; return true; }
        return false;
      });
    });
    return found;
  }
  function blockItem(id){ return blockItemIn(DB.blocks, id); }
  function isBlockId(id){ return !!blockItem(id); }
  /* Реестр марки (список блоков по порядку) или null, если марка без реестра. */
  function blockReg(brand){
    var E = en();
    return (E && E.blocks && E.blocks[brand]) || (DB.blocks && DB.blocks[brand]) || null;
  }
  function blockIds(brand){
    var reg = blockReg(brand);
    return reg ? reg.map(function(b){ return b.id; }) : null;
  }
  function blockLabel(id){
    var E = en();
    var n = (E && E.blockNames && E.blockNames[id]) || (DB.blockNames && DB.blockNames[id]);
    if(n) return n;
    var it = (E && E.blocks && blockItemIn(E.blocks, id)) || blockItem(id);
    return it ? it.label : id;
  }
  function blockText(id, key){
    var E = en();
    return (E && E.brands[id] && E.brands[id][key]) || (DB.brands[id] && DB.brands[id][key]) || null;
  }
  /* Ключи SPN.FMI: точный и без ведущих нулей - как в describe(). */
  function keysOf(spn, fmi){
    var spnS = String(spn), fmiS = String(fmi);
    var spnAlt = stripZero(spnS), fmiAlt = stripZero(fmiS);
    var keys = [spnS + '.' + fmiS];
    if(spnAlt) keys.push(spnAlt + '.' + fmiS);
    if(fmiAlt) keys.push(spnS + '.' + fmiAlt);
    if(spnAlt && fmiAlt) keys.push(spnAlt + '.' + fmiAlt);
    return keys;
  }
  /* Электрика по тексту записи блока с ownFmi: обрыв, КЗ, масса, плюс,
     напряжение, ток (русский и английский текст). */
  var ELEC_TEXT = /обрыв|замыкан|(^|[^а-яё])кз([^а-яё]|$)|на массу|на плюс|напряжен|(^|[^а-яё])ток([^а-яё]|$)|open|short|voltage|current|ground|circuit/;
  /* Критично по тексту записи блока с ownFmi. */
  var CRIT_TEXT = /давление масла слишком низк|перегрев|температур[^.]*высок|oil pressure too low|overheat|temperature[^.]*high/;

  /* Одно попадание в блок. Для блока с ownFmi текст берём как есть,
     без подсказки по FMI; для обычного блока - как раньше. */
  function blockHitOf(id, spn, fmi, ownFmi, keys){
    for(var j = 0; j < keys.length; j++){
      var tx = blockText(id, keys[j]);
      if(!tx) continue;
      var h = {id:id, label:blockLabel(id), k:keys[j], spn:spn, fmi:fmi, ownFmi:!!ownFmi,
               ru:(DB.brands[id] && DB.brands[id][keys[j]]) || tx};
      if(ownFmi){
        var low = tx.toLowerCase();
        h.text = tx;
        h.elec = ELEC_TEXT.test(low);
        h.urgent = (id === 'kamaz5490' && (DB.kamaz5490Urgent || []).indexOf(keys[j]) >= 0) ||
                   CRIT_TEXT.test(low);
      } else {
        h.text = withFmiHint(tx, fmi);
        h.urgent = urgent(spn, fmi, 'kamaz');
      }
      return h;
    }
    return null;
  }
  /* Все попадания по реестру марки; null - марка без реестра. */
  function blockHits(brand, spn, fmi){
    var reg = blockReg(brand);
    if(!reg) return null;
    var keys = keysOf(spn, fmi), out = [];
    reg.forEach(function(b){
      var h = blockHitOf(b.id, spn, fmi, b.ownFmi, keys);
      if(h) out.push(h);
    });
    return out;
  }
  /* Попадание в один конкретный блок (номер сканера знает свой блок). */
  function blockHitOne(id, spn, fmi){
    var it = blockItem(id);
    return blockHitOf(id, spn, fmi, !!(it && it.ownFmi), keysOf(spn, fmi));
  }
  /* Система для анализа и риска: у блока с ownFmi SPN другой, поэтому
     систему определяем только по тексту. */
  function hitSys(h){ return systemOf(h.ownFmi ? null : h.spn, h.ru || h.text); }

  function ownNote(h){
    return h.ownFmi ? '<div class="st" style="margin-top:7px">' + esc(t('fmiOwn')) + '</div>' : '';
  }
  function scanBlockStep(h){
    var bh = blockHitOne(h.brand, h.spn, h.fmi);
    return {st: bh ? bh.label : blockLabel(h.brand),
      tx: '<span class="mono">' + codeLabel(h.spn) + ' · FMI ' + esc(h.fmi) + '</span>' +
          (bh ? ownNote(bh) : '') + '<br><b>' + esc(bh ? bh.text : '') + '</b>', cls:'ok'};
  }

  /* Вывод попаданий: одно - карточка как обычно, подпись блока в источнике;
     несколько - список «подпись блока: текст» и карточка риска на каждое. */
  function blockHitsHtml(spn, fmi, hits, lead){
    var steps = lead ? [lead] : [];
    var multi = hits.length > 1, h0 = hits[0], shown = h0.k.split('.');
    steps.push({st:t('stepCode'), tx:'<span class="mono">' + codeLabel(shown[0]) + ' · FMI ' + shown[1] + '</span>' +
      (multi ? '' : ownNote(h0)), cls:'ok'});
    hits.forEach(function(h){
      if(!multi){
        steps.push({st:t('stepDecoding'), tx:'<b>' + esc(h.text) + '</b>' +
          '<div class="st" style="margin-top:7px">' + esc(t('sourceLabel', {src: h.label})) + '</div>', cls:'ok'});
        steps.push(h.urgent ? {st:t('stepUrgency'), tx:t('urgentText'), cls:'hit'}
                            : {st:t('stepUrgency'), tx:t('notUrgentText')});
      } else {
        steps.push({st:h.label, tx:'<b>' + esc(h.text) + '</b>' + ownNote(h) +
          '<div class="st" style="margin-top:7px">' + (h.urgent ? t('urgentText') : t('notUrgentText')) + '</div>', cls:'ok'});
      }
    });
    var html = chain(steps);
    hits.forEach(function(h){
      html += '<div class="card">' + riskBlock({spn:spn, fmi:fmi, sys:hitSys(h), urgent:h.urgent,
        ownFmi:h.ownFmi, elec:h.elec}, multi ? ' · ' + h.label : '') + '</div>';
    });
    return html;
  }

  /* Дополнительные попадания строки анализа и первопричины. */
  function altHtml(c){
    return (c.alt || []).map(function(h){
      return '<div class="st" style="margin-top:7px">' + esc(h.label) + ': ' + esc(h.text) + '</div>';
    }).join('');
  }
  function codeText(c){
    return (c.label ? '<i>' + esc(c.label) + ':</i> ' : '') + esc(c.text) + altHtml(c);
  }

  /* Особые вводы: FC-номер Cummins («FC 111») и блинк-код КамАЗ Bosch MS 6.1
     («блинк 21»). Это не SPN и не дилерский код, поэтому смотрим их до разбора.
     Только для КамАЗ и без марки. */
  /* Блинк-код: «2-1», «2-4-3», «21», «131», «блинк 21». Нулей в блинк-кодах
     не бывает, поэтому «100» сюда не попадает. dash - разделитель именно «-». */
  function blinkCode(raw){
    var s = String(raw || '').toUpperCase().replace(/\s+/g, ' ').trim();
    var m = /^(БЛИНК|BLINK|МИГАЕТ|МИГАНИЕ|МИГАЮТ|ВСПЫШКИ|ВСПЫШКА)?\s*([1-9])\s*([-.\/,]?)\s*([1-9])(?:\s*([-.\/,]?)\s*([1-9]))?$/.exec(s);
    if(!m) return null;
    return {code: m[2] + m[4] + (m[6] || ''), prefix: !!m[1], dash: m[3] === '-' || m[5] === '-'};
  }
  /* Индекс «марка|блинк-код» -> ключи словаря, строится по тексту записи
     «Мигающий код: 2-4-3» (ru) и «Blink code: 6-6-3» (en). */
  var BLINK_IDX = null;
  function blinkIndex(){
    if(BLINK_IDX) return BLINK_IDX;
    BLINK_IDX = {};
    [DB, DB_EN].forEach(function(D){
      if(!D || !D.brands) return;
      Object.keys(D.brands).forEach(function(b){
        var m = D.brands[b];
        Object.keys(m).forEach(function(k){
          var r = /(?:Мигающий код|Blink code):\s*([0-9][0-9-]*)/.exec(m[k]);
          if(!r) return;
          var id = b + '|' + r[1].replace(/-/g, '');
          var list = BLINK_IDX[id] = BLINK_IDX[id] || [];
          if(list.indexOf(k) < 0) list.push(k);
        });
      });
    });
    return BLINK_IDX;
  }
  /* Ответ из открытого словаря по блинк-коду; null - такого кода в словаре нет. */
  function blinkOpen(brand, code, typed){
    var idx = blinkIndex(), E = en(), hit = null;
    donorsOf(brand).some(function(d){
      var list = idx[d + '|' + code];
      if(!list || !list.length) return false;
      hit = {donor:d, keys:list};
      return true;
    });
    if(!hit) return null;
    var steps = [{st:t('stepCode'), tx:'<span class="mono">' + esc(typed) + '</span>', cls:'ok'}];
    hit.keys.forEach(function(k){
      var txt = (E && E.brands[hit.donor] && E.brands[hit.donor][k]) || (DB.brands[hit.donor] && DB.brands[hit.donor][k]) || '';
      var pr = k.split('.');
      steps.push({st:donorSrc(hit.donor, brand),
        tx:'<span class="mono">' + codeLabel(pr[0]) + ' · FMI ' + esc(pr[1]) + '</span><br><b>' + esc(txt) + '</b>', cls:'ok'});
    });
    return chain(steps);
  }

  /* Особые вводы: FC-номер Cummins («FC 111») и блинк-код КамАЗ Bosch MS 6.1.
     Только для КамАЗ и без марки. Блинк КамАЗ - с «блинк» или через «-». */
  function specialKind(raw, brand){
    var fc = normCode(raw).replace(/\s+/g, '').match(/^(?:FC|FK|ФC|ФK)-?(\d{1,4})$/);
    if(fc) return {kind:'fc', num:fc[1]};
    var bc = blinkCode(raw);
    if(bc && (bc.prefix || (brand === 'kamaz' && bc.dash))) return {kind:'blink', code:bc.code};
    return null;
  }
  /* html, либо null, если в индексе такого номера нет (тогда идём обычным путём). */
  function specialHtml(sp){
    if(sp.kind === 'fc'){
      var keys = ((DB.cumminsFc && DB.cumminsFc[sp.num]) || []).filter(function(k){
        return blockText('cumminsisb', k);
      });
      if(!keys.length) return null;
      var steps = [{st:t('stepCode'), tx:'<span class="mono">FC ' + esc(sp.num) + '</span>', cls:'ok'}];
      keys.forEach(function(k){
        var p = k.split('.');
        steps.push({st:t('cumminsFcLabel', {n: sp.num}),
          tx:'<span class="mono">' + codeLabel(p[0]) + ' · FMI ' + esc(p[1]) + '</span><br><b>' +
             esc(blockText('cumminsisb', k)) + '</b>', cls:'ok'});
      });
      return chain(steps);
    }
    var E = en(), B = (E && E.kamazBlinkMs61) || DB.kamazBlinkMs61;
    var c = B && B.codes && B.codes[sp.code];
    if(!c) return note(t('blinkNotFound', {n: sp.code}));
    return chain([
      {st:t('stepCode'), tx:'<span class="mono">' + esc(t('blinkCode', {n: sp.code})) + '</span>', cls:'ok'},
      {st:B.label, tx:'<b>' + esc(c.description) + '</b>' +
        '<div class="st" style="margin-top:7px">' + esc(t('blinkLimit')) + ': ' + esc(c.limit) + '</div>' +
        (c.source ? '<div class="st" style="margin-top:7px">' + esc(t('sourceLabel', {src: c.source})) + '</div>' : ''),
        cls:'ok'}
    ]);
  }

  /* Для марки с реестром - все попадания по блокам; без реестра - как раньше. */
  function describe(spn, fmi, brand){
    var hits = blockHits(brand, spn, fmi);
    if(hits && hits.length){
      return {text:hits[0].text, src:hits[0].label, k:hits[0].k, hits:hits, ru:hits[0].ru || hits[0].text};
    }
    if(brand && !hits){
      var E = en();
      var spnS = String(spn), fmiS = String(fmi);
      var spnAlt = stripZero(spnS), fmiAlt = stripZero(fmiS);
      /* Точный ключ - первым: у Ford он совпадает сразу же, до
         раздетых вариантов дело не доходит. Раздетые добавляем, только
         если реально есть что раздевать - иначе не плодим одинаковые
         попытки для обычного кода без нулей. */
      var keys = [spnS + '.' + fmiS];
      if(spnAlt) keys.push(spnAlt + '.' + fmiS);
      if(fmiAlt) keys.push(spnS + '.' + fmiAlt);
      if(spnAlt && fmiAlt) keys.push(spnAlt + '.' + fmiAlt);
      /* Ford и др. пишут SPN тремя знаками («084.0», «024.7»): ввод без нуля ищем и в таком виде. */
      if(/^\d{1,2}$/.test(spnS)) keys.push(('00' + spnS).slice(-3) + '.' + fmiS);
      /* По алиасу (см. BRAND_ALIAS) проходим доноров по очереди и
         подписываем ответ именем того, у кого код реально нашёлся. */
      var donors = donorsOf(brand);
      for(var i = 0; i < donors.length; i++){
        var d = donors[i];
        for(var j = 0; j < keys.length; j++){
          var exact = (E && E.brands[d] && E.brands[d][keys[j]])
                   || (DB.brands[d] && DB.brands[d][keys[j]]);
          if(exact) return {text:withFmiHint(exact, fmi, d), src:donorSrc(d, brand), k:keys[j],
                            ru:(DB.brands[d] && DB.brands[d][keys[j]]) || exact};
        }
      }
    }
    return stdDecode(spn, fmi, brand);
  }

  /* Общий смысл по стандарту (SPN из универсальной таблицы + FMI). Так же
     расшифровывается и код без попаданий по блокам. */
  function stdDecode(spn, fmi, brand){
    /* У Freightliner нет заводской построчной таблицы кодов - есть
       только имена компонентов (MID/PID/SID). Готового текста для
       конкретной комбинации нет, но сама комбинация осмысленна -
       собираем расшифровку из трёх имён вместо "код не найден". */
    if(brand === 'freightliner'){
      var mm = /^M(\d+)-([PS])(\d+)$/.exec(spn);
      if(mm){
        var composed = composeFreightlinerText(mm[1], mm[2], mm[3]);
        if(composed) return {text: withFmiHint(composed, fmi), src: t('composedSource', {brand: brandName(brand)})};
      }
    }
    var name = spnName(spn, brand);
    var known = !!name;
    if(!name) name = codeLabel(spn);
    var f = fmiHintOf(brand, fmi) || t('fmiNonstandard', {fmi:fmi});
    return {text:name + ' — ' + f, src:known ? t('standardSource') : null, unknown:!known,
            ru:ruSpnName(spn, brand) || name};
  }
  /* Все попадания - из блоков с ownFmi (свой FMI): общий смысл по J1939 тоже показываем. */
  function onlyOwnFmi(hits){
    return !!hits && hits.length > 0 && hits.every(function(h){ return h.ownFmi; });
  }

  /* Дилерский код ищем через API (worker/pcode-api.js). Ввод уходит почти как
     набран: пробелы и разделители нормализует воркер. */
  function fetchPcodeOne(brand, code, lang){
    var url = PCODE_API + '/pcode?code=' + encodeURIComponent(code) +
              '&lang=' + encodeURIComponent(lang) +
              (brand ? '&brand=' + encodeURIComponent(brand) : '');
    return fetch(url).catch(function(){
      var ne = new Error('pcode network'); ne.network = true; throw ne;
    }).then(function(r){
      if(r.status === 429){
        return r.json().catch(function(){ return {}; }).then(function(body){
          if(body && body.error === 'daily_limit'){
            var lim = new Error('pcode daily limit'); lim.dailyLimit = true; throw lim;
          }
          throw new Error('pcode api 429');
        });
      }
      if(r.status === 400){
        return r.json().catch(function(){ return {}; }).then(function(body){
          if(body && body.error === 'bad_code'){
            var bc = new Error('pcode bad code'); bc.badCode = true; throw bc;
          }
          return {hits: []};   /* unknown_brand и прочие 400 - ответа нет, это не ошибка */
        });
      }
      if(!r.ok) throw new Error('pcode api ' + r.status);
      return r.json();
    }).then(function(data){ return data.hits || []; });
  }
  function isDailyLimit(e){ return !!(e && e.dailyLimit); }

  /* В воркер - только доноры из KNOWN_PCODE_BRANDS. Без марки - один запрос без brand.
     Если закрытых доноров нет - запроса не делаем. */
  function fetchPcode(brand, code, lang){
    if(!brand) return fetchPcodeOne('', code, lang);
    var donors = donorsOf(brand).filter(function(d){ return !!CLOSED_BRANDS[d]; });
    if(!donors.length) return Promise.resolve([]);
    if(donors.length === 1) return fetchPcodeOne(donors[0], code, lang);
    var failed = null, dead = 0, bad = null;
    return Promise.all(donors.map(function(b){
      return fetchPcodeOne(b, code, lang).catch(function(e){
        if(isDailyLimit(e)) throw e;
        if(e.badCode){ bad = bad || e; return []; }
        dead++; failed = failed || e; return [];
      });
    })).then(function(lists){
      if(dead === donors.length) throw failed;
      var out = [], seen = {};
      lists.forEach(function(hits){
        hits.forEach(function(h){
          var k = h.brand + '|' + h.text;
          if(!seen[k]){ seen[k] = 1; out.push(h); }
        });
      });
      if(!out.length && bad) throw bad;
      return out;
    });
  }

  /* Закрытая база по коду: свой индекс номеров сканера (DB.scan) плюс воркер.
     Сеть не обязана отвечать, если свой ответ уже есть. */
  function closedLookup(brand, code){
    return load().then(function(){
      var mine = scanRefs(brand, code);
      var net = (brand === 'kamaz' && mine.length) ? Promise.resolve([]) : Promise.resolve()
        .then(function(){ return fetchPcode(brand, code, currentLang); })
        .catch(function(e){ if(mine.length) return []; throw e; });
      return Promise.all([net, mine.length ? loadEn() : null])
        .then(function(a){ return {net:a[0], mine:mine}; });
    });
  }
  /* Открытый словарь марки по вводу «число-число»: как есть, и без ведущих нулей
     (MAN «00597-05» - ключ 597.5). Ключ и текст - или null. */
  function openPairHit(brand, typed){
    var m = /^(\d{1,7})\s*[-.\/,\s]\s*(\d{1,3})$/.exec(String(typed || '').trim());
    if(!m) return null;
    var E = en(), s = m[1], f = m[2], s0 = stripZero(s), f0 = stripZero(f);
    var keys = [s + '.' + f];
    if(s0) keys.push(s0 + '.' + f);
    if(f0) keys.push(s + '.' + f0);
    if(s0 && f0) keys.push(s0 + '.' + f0);
    var donors = donorsOf(brand);
    for(var i = 0; i < donors.length; i++){
      for(var j = 0; j < keys.length; j++){
        var tx = (E && E.brands[donors[i]] && E.brands[donors[i]][keys[j]]) ||
                 (DB.brands[donors[i]] && DB.brands[donors[i]][keys[j]]);
        if(tx) return {donor: donors[i], key: keys[j], text: tx};
      }
    }
    return null;
  }
  /* Текст открытого словаря первым; ответы закрытой базы и номера сканера - дальше, без повторов. */
  function openFirstHtml(typed, oh, r, brand){
    var pr = oh.key.split('.');
    var steps = [{st:t('stepCode'), tx:'<span class="mono">' + esc(typed) + '</span>', cls:'ok'},
      {st:donorSrc(oh.donor, brand),
       tx:'<span class="mono">' + codeLabel(pr[0]) + ' · FMI ' + esc(pr[1]) + '</span><br><b>' +
          esc(withFmiHint(oh.text, pr[1], oh.donor)) + '</b>', cls:'ok'}];
    if(r){
      r.net.forEach(function(h){
        if(h.text === oh.text) return;
        steps.push({st:t('dealerBase', {brand: brandName(h.brand) || brand}), tx:'<b>' + esc(h.text) + '</b>', cls:'ok'});
      });
      scanStepList(r.mine.filter(function(m){ return m.spn + '.' + m.fmi !== oh.key; }))
        .forEach(function(s){ steps.push(s); });
    }
    return chain(steps);
  }
  function closedHtml(code, r, brand){
    if(!r.net.length) return scanHtml(code, r.mine);
    var pSteps = [{st:t('stepCode'), tx:pcodeStep(code, r.net), cls:'ok'}];
    r.net.forEach(function(h){
      pSteps.push({st: r.net.length > 1 || r.mine.length || !brand ? brandName(h.brand) : donorStep(h.brand, brand),
        tx:'<b>' + esc(h.text) + '</b>', cls:'ok'});
    });
    return chain(pSteps.concat(scanStepList(r.mine)));
  }
  /* Сеть - «нет связи»; 400 bad_code - код не из этой таблицы; прочее - сервер. */
  function pcodeErrorText(e, brand){
    if(e && e.badCode) return note(brand ? t('badCodeFor', {brand: brandName(brand) || brand}) : t('badCode'));
    if(isDailyLimit(e)) return note(t('dailyLimit'));
    if(e && e.network) return note(t('pcodeApiError'));
    return note(t('pcodeServerError'));
  }
  function stLine(s){ return '<div class="st" style="margin:0 0 8px">' + esc(s) + '</div>'; }
  function j1939Caption(brand){ return stLine(t('j1939ForBrand', {brand: brandName(brand) || brand})); }

  /* SPN без FMI с известным именем: параметр и известные отказы марки. */
  function spnOnlyHtml(spn, brand, nm, quiet){
    var known = [], tblBrand = null;
    donorsOf(brand).some(function(d){
      if(DB.brands[d]){ tblBrand = d; return true; }
      return false;
    });
    if(tblBrand){
      Object.keys(DB.brands[tblBrand]).forEach(function(k){
        var pair = k.split('.');
        if(pair[0] === String(spn) && pair.length === 2) known.push(pair[1]);
      });
      known.sort(function(a,b){ return a - b; });
    }
    var sSteps = [{st:t('stepParam'), tx:'<span class="mono">SPN ' + spn + '</span> — <b>' + esc(nm) + '</b>', cls:'ok'}];
    if(known.length){
      sSteps.push({st:t('knownFailures', {brand: brandName(tblBrand)}),
        tx: known.map(function(f){
          var E = en(), bk = spn + '.' + f;
          var txt = (E && E.brands[tblBrand] && E.brands[tblBrand][bk]) || DB.brands[tblBrand][bk];
          return '<span class="mono">' + spn + '/' + f + '</span> — ' + esc(txt);
        }).join('<br>'), cls:'ok'});
    }
    if(!quiet) sSteps.push({st:t('stepNeedFmi'), tx:t('needFmiText', {spn: spn})});
    return chain(sSteps);
  }
  /* Стандарт J1939 под ответом закрытой базы: без срочности и горизонта. */
  function j1939Quiet(raw, brand){
    var p = parse(raw, 'auto');
    if(!p || p.bad || p.pcode) return '';
    var html;
    if(p.fmi == null){
      var nm = spnName(p.spn, brand);
      if(!nm) return '';
      html = spnOnlyHtml(p.spn, brand, nm, true);
    } else {
      html = spnFmiHtml(p.spn, p.fmi, brand, null, true);
    }
    return j1939Caption(brand) + html;
  }
  function safeQuiet(raw, brand){
    try { return j1939Quiet(raw, brand); } catch(e){ return ''; }
  }

  function urgent(spn, fmi, brand){
    if(OWN_FMI[brand]) return hasNum(DB.urgentSpn, spn);
    /* FMI вне 0-31 или не описанный в словаре: по одному SPN «Критично» не ставим -
       значение нестандартное, и смысл его знает только марка. */
    if(!fmiKnown(fmi)) return false;
    if(hasNum(DB.urgentSpn, spn)) return true;
    if(hasNum(DB.urgentFmi, fmi)) return true;
    if(brand !== 'kamaz') return false;
    if(DB.kamazUrgent.indexOf(spn + '.' + fmi) >= 0) return true;
    var spnAlt = stripZero(String(spn)), fmiAlt = stripZero(String(fmi));
    return !!(spnAlt || fmiAlt) &&
      DB.kamazUrgent.indexOf((spnAlt || spn) + '.' + (fmiAlt || fmi)) >= 0;
  }

  /* Полный ответ по паре SPN/FMI: код, расшифровка, «можно ли ехать» и
     горизонт риска. Вынесено из run() отдельной функцией, потому что тем
     же ответом теперь отвечает и номер сканера (см. DB.scan ниже): человек,
     который ввёл "P0513-00" со своей дешёвой китайской коробочки, должен
     получить ту же карточку, что и человек с кодом с приборки, а не сухую
     строчку. lead - необязательный шаг ПЕРЕД «кодом»: им подписывается,
     из чего мы этот код взяли. */
  function spnFmiHtml(spn, fmi, brand, lead, quiet){
    var d = describe(spn, fmi, brand);
    if(d.hits && d.hits.length){
      var bhtml = blockHitsHtml(spn, fmi, d.hits, lead);
      if(onlyOwnFmi(d.hits)){
        var std = stdDecode(spn, fmi, brand);
        bhtml += chain([{st:t('j1939Caption'), tx:'<b>' + esc(std.text) + '</b>', cls:'ok'}]);
      }
      return bhtml;
    }
    /* Срочность - только по известному SPN. Незнакомый код и тихий режим
       (ответ закрытой базы) «критично» не получают. */
    var u = (quiet || d.unknown) ? false : urgent(spn, fmi, brand);
    var shown = d.k ? d.k.split('.') : [spn, fmi];
    var code = codeLabel(shown[0]) + ' · FMI ' + shown[1];
    var steps = lead ? [lead] : [];
    steps.push({st:t('stepCode'), tx:'<span class="mono">' + code + '</span>', cls:'ok'});
    steps.push({st:t('stepDecoding'), tx:'<b>' + esc(d.text) + '</b>' +
      (d.src ? '<div class="st" style="margin-top:7px">' + esc(t('sourceLabel', {src:d.src})) + '</div>' : ''), cls:'ok'});
    if(!quiet && !d.unknown){
      steps.push(u ? {st:t('stepUrgency'), tx:t('urgentText'), cls:'hit'}
                   : {st:t('stepUrgency'), tx:t('notUrgentText')});
    }
    var html = chain(steps);
    if(!quiet && !d.unknown && !OWN_FMI[brand]){
      html += '<div class="card">' + riskBlock({
        spn:spn, fmi:fmi, sys:systemOf(spn, d.ru || d.text), urgent:u
      }) + '</div>';
    }
    if(d.unknown) html += note(t('unknownSpnNote'));
    return html;
  }

  /* ============================================================
     НОМЕР, КОТОРЫЙ ПОКАЗЫВАЕТ СКАНЕР

     На приборке код один (SPN/FMI), а сканер у того же человека
     показывает другой: у КамАЗ-5490 старый прибор по K-line читает
     пятизначный номер блока ADM3/MR2 ("10103"), Ford печатает свою
     нумерацию FODP ("P0513-00"), а на SITRAK/Dongfeng/Foton дешёвая
     коробочка за тысячу рублей выдаёт обычный OBD-P-код ("P023D").

     Эти соответствия мы знаем и печатаем прямо в описании кода. Но
     лежали они ВНУТРИ ТЕКСТА, а поиск идёт по ключам - и 908 номеров
     были написаны на страницах и при этом не находились ничем. Хуже
     того, часть уводила к чужой марке: "P023D" отвечал JAC, потому что
     у JAC такой ключ в дилерской таблице есть, а у SITRAK нет.

     Индекс DB.scan («номер» -> ["марка|SPN.FMI", ...]) собирается на
     сборке из тех же описаний, см. build_scan_index в
     scripts/build_pcode.py. Ищем по нему ДО сети: свой ответ из памяти
     всегда вернее и быстрее чужого по HTTP.

     Марка выбрана - показываем только её (и её доноров): один номер
     занят у нескольких марок сразу, и вываливать человеку с SITRAK
     ответы Dongfeng незачем. Марка не выбрана - показываем все, как это
     делает и дилерский поиск. */
  function scanRefs(brand, code){
    if(!DB || !DB.scan) return [];
    var refs = DB.scan[normCode(code).replace(/\s+/g, '')];
    if(!refs) return [];
    var donors = blockIds(brand) || donorsOf(brand);
    var out = [];
    refs.forEach(function(ref){
      var cut = ref.indexOf('|');
      var b = ref.slice(0, cut), key = ref.slice(cut + 1);
      if(donors.length && donors.indexOf(b) < 0) return;
      var dot = key.lastIndexOf('.');
      out.push({brand:b, spn:codeVal(key.slice(0, dot)), fmi:codeVal(key.slice(dot + 1))});
    });
    return out;
  }

  /* Ответ по номеру сканера. Один код на щитке - обычная карточка с
     подписью, откуда взялось; несколько - список, потому что выбрать за
     человека, какой из них горит именно у него, мы не можем. */
  function scanStepList(hits){
    return hits.map(function(h){
      if(isBlockId(h.brand)) return scanBlockStep(h);
      var E = en(), key = h.spn + '.' + h.fmi;
      var txt = (E && E.brands[h.brand] && E.brands[h.brand][key]) ||
                (DB.brands[h.brand] && DB.brands[h.brand][key]) || '';
      return {st:brandName(h.brand),
        tx:'<span class="mono">' + codeLabel(h.spn) + ' · FMI ' + esc(h.fmi) +
           '</span><br><b>' + esc(txt) + '</b>', cls:'ok'};
    });
  }
  function scanHtml(typed, hits){
    var lead = {st:t('scanStep'),
                tx:'<span class="mono">' + esc(typed) + '</span>', cls:'ok'};
    if(hits.length === 1){
      var bh = isBlockId(hits[0].brand) ? blockHitOne(hits[0].brand, hits[0].spn, hits[0].fmi) : null;
      if(bh) return blockHitsHtml(hits[0].spn, hits[0].fmi, [bh], lead);
      return spnFmiHtml(hits[0].spn, hits[0].fmi, hits[0].brand, lead);
    }
    return chain([lead].concat(scanStepList(hits))) +
           note(t('scanMany', {code: esc(typed)}));
  }

  function esc(t){
    return String(t).replace(/[&<>"]/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];
    });
  }
  function chain(steps){
    var html = '<div class="card"><ol class="chain">';
    steps.forEach(function(s, n){
      html += '<li class="' + (s.cls||'') + '" style="--s:' + n + '"><i></i>' +
              '<div class="st">' + esc(s.st) + '</div><div class="tx">' + s.tx + '</div></li>';
    });
    return html + '</ol></div>';
  }
  function note(t){ return '<div class="miss">' + t + '</div>'; }

  /* Строка «Код» для дилерского ответа.

     2176 ключей в базе записаны с ведущими нулями до пяти знаков (manebs, man,
     manzbr2, mercedes, iveco, eberspacher), а сканер показывает короткую форму
     без нулей. Воркер с недавних пор дополняет чисто цифровой ввод нулями и
     возвращает в поле code ту запись, под которой код реально нашёлся. Если
     она отличается от введённой, показываем обе: иначе выходит, что мы молча
     поправили ввод и отвечаем не на то, что спросили. Марки могут отдать
     разные формы - тогда перечисляем все. */
  function pcodeStep(typed, hits){
    var flat = String(typed).replace(/\s+/g, ''), forms = [];
    hits.forEach(function(h){
      if(h.code && h.code !== flat && forms.indexOf(h.code) < 0) forms.push(h.code);
    });
    var html = '<span class="mono">' + esc(typed) + '</span>';
    if(forms.length) html += ' → <span class="mono">' + esc(forms.join(', ')) + '</span>';
    return html;
  }

  /* ============================================================
     РАЗБОР ГИРЛЯНДЫ

     Машина почти никогда не отдаёт один код. Сканер вываливает
     6-12 штук, но поломка при этом одна, а остальное - её следствия:
     пустой бак AdBlue -> прервано дозирование -> NOx выше нормы ->
     ограничение момента. Человек проверяет коды по одному и получает
     четыре разных страшных ответа вместо одного «долей мочевину».

     Поэтому здесь мы не расшифровываем список построчно, а ищем в нём
     корень. Ниже - то, чем это делается: принадлежность кода к системе
     и известные цепочки «причина -> следствия».
     ============================================================ */

  var SYS_SPN = {
    scr  :[1761,3216,3226,3242,3246,3250,3251,3361,3363,3364,3480,3609,3610,3719,3936,
           4090,4094,4095,4096,4225,4334,4364,4782,4809,5394,5841],
    oil  :[98,100,175,1208],
    cool :[110,111,975,1134,4076,4193],
    fuel :[94,95,97,157,164,174,651,652,653,654,655,656,657,658,1076,1077,1239,1347,1348,1349],
    air  :[102,103,105,106,107,132,411,412,1127,1172,1176,2630,2659,2789,2791,5401,5541],
    power:[158,167,168,620,627,628,629,1079,1080,3509,3510,3511,5006],
    can  :[520,639,1231,1235,1237,2003,2005,2011,523212,523216],
    brake:[46,70,563,597,598,1086,520192],
    trans:[191,522,523,524,560,561,573,574,787],
    prot :[1108,1110,1569,2629,3607,5246]
  };
  /* Если SPN нет в списках - определяем систему по названию: база
     русская и слова в ней устойчивые. */
  /* Английские слова - для текста записи на английском языке: система должна
     быть та же, что по русскому тексту (иначе язык менял уровень риска). */
  var SYS_WORD = {
    scr  :['adblue','мочевин','реаген','nox','scr','сажев','катализат','dpf','выхлоп','отработавш',
           'urea','exhaust','particulate','catalyst'],
    oil  :['масл','смазк','oil','lubric'],
    cool :['охлажд','антифриз','радиатор','вентилятор',' ож','coolant','cooling','radiator','fan'],
    fuel :['топлив','форсунк','рампе','рампы','рампа','тнвд','впрыск','солярк',
           'fuel','injector','injection','rail'],
    air  :['наддув','турбо','воздуш','впуск','интеркул','дроссел',
           'boost','turbo','intake','intercooler','throttle'],
    power:['бортовой сети','аккумул','генерат','питани','реле',
           'battery','alternator','charging','power supply','relay'],
    can  :['can','шина','сообщени','связ'],
    brake:['тормоз','abs','ebs','ресивер','пневмо','brake','air reservoir'],
    trans:['коробк','сцеплен','передач','кпп','трансмисс',
           'gearbox','transmission','clutch','gear'],
    prot :['ограничен','защит','останов двигател','дерейт','protection','derate','shutdown']
  };
  /* Моторный (выхлопной) тормоз и ретардер - не колёсные тормоза: своя система.
     Проверяем раньше SYS_WORD, иначе «тормоз» в тексте уводил их к колёсным. */
  var ENG_BRAKE_RE = /моторн[а-яё]*\s+тормоз|тормоз[а-яё]*\s+двигател|горн[а-яё]*\s+тормоз|ретардер|retarder|engine\s+brake|exhaust\s+brake|compression\s+brake/i;
  /* Слово нашлось, но по случайной подстроке, а не по смыслу - проверено
     на реальных данных всего справочника: «пасса[жи]р» содержит «сажи»
     (счётчик пассажиров попадал в сажевый фильтр), «ожида[ем]ого»
     содержит " ож" (обычный оборот «ток ниже ожидаемого» попадал в
     охлаждение), «гидро[аккумул]ятор» - это гидравлика, не батарея, а
     «срабатывание защит[ы от перегрева]» - формулировка про
     предохранитель в цепи фонарей (наша же, из перевода Iveco), а не
     про защиту двигателя. sysWordExclude - точечные заплатки под
     конкретно найденный брак, а не общий движок границ слова: если у
     совпавшего слова есть запись здесь и её текст ТОЖЕ есть в строке -
     совпадение не считаем. Раньше «сажи» и «бортов» пытались угадывать
     то же самое и чаще ошибались, чем попадали - убраны совсем.

     Отдельная история - голое «напряж» в power. Слово было верным по
     смыслу («напряжение» правда про напряжение), но ловило почти
     исключительно локальные датчики («Датчик педали акселератора -
     низкое напряжение в цепи», «напряжение выше нормы» у любого узла с
     электрическим FMI): 395 из 503 срабатываний оказались не про
     бортовую сеть/аккумулятор, а про конкретную цепь одного датчика -
     тому, кто едет, при таком коде грозит не разряженный аккумулятор,
     а недостоверные показания именно этого датчика. Заменено на точную
     фразу «бортовой сети» - она держит настоящие случаи («Низкое
     напряжение бортовой сети» у Mercedes/Iveco), а локальные датчики
     теперь уходят в other и получают честный электрический фолбэк
     вместо истории про бортовую сеть.

     «пневмо» - слово из той же породы, но выжившее: 12 верных попаданий
     (пневмобаллоны по осям, пневмоканалы, компрессор пневмосистемы,
     пневмоподвеска) против двух видов брака, оба закрыты исключениями -
     «пневмоэлектромагнит КОРОБКИ» это trans, а «пневмоСИГНАЛ» - звуковой
     сигнал, не тормоза. Исключения поэтому стали списком, а не строкой. */
  var SYS_WORD_EXCLUDE = {' ож':['ожида'], 'аккумул':['гидроаккумул'],
                          'защит':['срабатывание защит'],
                          'пневмо':['коробк','сигнал']};
  function systemOf(spn, name){
    var k;
    for(k in SYS_SPN){ if(hasNum(SYS_SPN[k], spn)) return k; }
    if(ENG_BRAKE_RE.test(name || '')) return 'enginebrake';
    var low = (name || '').toLowerCase();
    for(k in SYS_WORD){
      if(SYS_WORD[k].some(function(w){
        if(low.indexOf(w) < 0) return false;
        var bad = SYS_WORD_EXCLUDE[w];
        return !bad || !bad.some(function(b){ return low.indexOf(b) >= 0; });
      })) return k;
    }
    return 'other';
  }

  /* Известные цепочки. Читать так: если в списке есть код из root,
     то встреченные коды из cons - его следствия, а не отдельные
     поломки. Список неполный и намеренно консервативный: лучше
     не связать два кода, чем связать неверно. */
  var CAUSAL = [
    {root:[1761,4096],        cons:[3216,3226,3361,3363,3364,4090,4094,4095,4225,5841,1569,5246], phys:1},
    {root:[5841,3364],        cons:[3226,4090,4094,4225,1569,5246]},
    {root:[3251,3719],        cons:[131,1569,3609,3610,3936,5246], phys:1},
    {root:[100],              cons:[1108,1110,1569,3607], phys:1},
    {root:[110,111],          cons:[975,1108,1110,1569,3607], phys:1},
    {root:[639,1231,1235],    cons:[520,2003,2005,2011]},
    {root:[102,103,1127,5401],cons:[131,1569,2791,3251], phys:1},
    {root:[94,157,1239],      cons:[190,651,652,653,654,655,656,657,658,1569], phys:1},
    {root:[46,1086],          cons:[563,597,598,520192], phys:1}
  ];

  /* Когда явной цепочки нет, порядок всё равно не случаен: просадка
     питания или оборванная шина сыплют ложные коды по всей машине,
     а ограничение момента - это всегда чей-то итог, а не причина.
     Меньше число - ближе к корню. */
  var FMI_RANGE   = [0,1,15,16,17,18];   // величина реально вне нормы
  var FMI_ELEC    = [3,4,5,6];           // электрика самого датчика
  var FMI_DERIVED = [2,9,10,11,19,20,21,31]; // расчётное, производное
  /* Признаки кода. У блока с ownFmi электрику дают тексты записи (c.elec),
     а не номер FMI; физической величиной считаем всё не электрическое. */
  function isElec(c){ return c.ownFmi ? !!c.elec : hasNum(FMI_ELEC, c.fmi); }
  function isPhysFmi(c){ return c.ownFmi ? !c.elec : hasNum(FMI_RANGE, c.fmi); }
  function isDerived(c){ return !c.ownFmi && hasNum(FMI_DERIVED, c.fmi); }
  function rootScore(c){
    if(c.sys === 'prot')  return 90;
    if(c.sys === 'power') return 10;
    if(c.sys === 'can')   return 15;
    if(isPhysFmi(c))   return 30;
    if(isElec(c))      return 50;
    if(isDerived(c))   return 70;
    return 60;
  }

  /* Из строки достаём все пары SPN/FMI подряд - список со сканера
     приходит и через запятую, и в столбик, и с номерами строк. */
  function parseAll(raw){
    var up = normCode(raw), out = [], seen = {}, m;
    var re = /(?:SPN\s*[:\-]?\s*)?([0-9A-F]{1,6})\s*(?:\D{0,12}?FMI\s*[:\-]?\s*|[\/\-.,]\s*|\s+)([0-9A-F]{1,3})(?![0-9A-F])/g;
    while((m = re.exec(up))){
      /* Пара с FMI вне 0..31 не пара: сдвигаемся на символ и ищем дальше
         ("1 636 11" - пара 636/11, а не 1/636). */
      if(!fmiOk(m[2])){ re.lastIndex = m.index + 1; continue; }
      var spn = codeVal(m[1]), fmi = codeVal(m[2]), k = spn + '.' + fmi;
      if(!seen[k]){ seen[k] = 1; out.push({spn:spn, fmi:fmi}); }
    }
    return out;
  }

  var ACT = {scr:'actScr', oil:'actOil', cool:'actCool', fuel:'actFuel',
             air:'actAir', power:'actPower', can:'actCan', brake:'actBrake'};

  function analyze(codes, brand){
    var list = codes.map(function(c){
      var d = describe(c.spn, c.fmi, brand);
      if(d.hits && d.hits.length){
        var h0 = d.hits[0];
        return {spn:c.spn, fmi:c.fmi, text:h0.text, sys:hitSys(h0), urgent:h0.urgent,
                ownFmi:h0.ownFmi, elec:h0.elec, label:h0.label, alt:d.hits.slice(1)};
      }
      return {spn:c.spn, fmi:c.fmi, text:d.text, sys:systemOf(c.spn, d.ru || d.text),
              urgent:urgent(c.spn, c.fmi, brand)};
    });
    var id = function(c){ return c.spn + '.' + c.fmi; };

    var best = null;

    /* Просевшая бортсеть и мёртвая шина идут вне очереди: они сыплют
       ложные коды сразу по всем системам, поэтому любое другое
       объяснение списка будет разбором этих самых ложных кодов.
       Классика - «загорелось всё сразу» от плохой массы. */
    var supply = list.filter(function(c){ return c.sys === 'power' || c.sys === 'can'; })
                     .sort(function(a, b){ return rootScore(a) - rootScore(b); })[0];
    if(supply){
      best = {root:supply, cons:list.filter(function(c){
        return c !== supply && (isElec(c) || isDerived(c));
      })};
    }

    /* Иначе берём правило, объясняющее больше всего кодов: если подходят
       и «пустой бак», и «плохое качество», выигрывает то, под которое
       легла вся гроздь. */
    if(!best){
      CAUSAL.forEach(function(rule){
        var root = null;
        list.forEach(function(c){
          /* Для физических цепочек причиной считаем только реально
             вылезшую за норму величину. Перегрев тянет за собой дерейт,
             а оборванный провод датчика перегрева - нет: это разные
             неисправности, и путать их нельзя. */
          if(root || !hasNum(rule.root, c.spn)) return;
          if(rule.phys && !isPhysFmi(c)) return;
          root = c;
        });
        if(!root) return;
        var cons = list.filter(function(c){
          return c !== root && hasNum(rule.cons, c.spn);
        });
        if(!best || cons.length > best.cons.length) best = {root:root, cons:cons};
      });
    }

    if(!best){
      best = {root:list.slice().sort(function(a, b){
        return rootScore(a) - rootScore(b);
      })[0], cons:[]};
    }

    var used = {};
    used[id(best.root)] = 1;
    best.cons.forEach(function(c){ used[id(c)] = 1; });
    var solo = list.filter(function(c){ return !used[id(c)]; });

    /* Приговор считаем по горизонту риска, а не по голой метке
       «критический». Пустой бак AdBlue помечен серьёзным - и он
       серьёзный, но машина от него не встанет посреди трассы, и
       говорить водителю «ехать нельзя» здесь просто неправда.

       Смягчаем только там, где знаем систему и знаем почему.
       Помеченный критическим код, для которого модели нет, так и
       остаётся запретом: чего мы не понимаем, тем не рискуем. */
    var risks = list.map(function(c){ return {c:c, r:riskOf(c)}; });
    var worst = risks.slice().sort(function(a, b){
      return RISK_RANK[a.r.lvl] - RISK_RANK[b.r.lvl];
    })[0];
    var blind = risks.some(function(x){ return x.r.key === 'genUrgent'; });

    return {root:best.root, cons:best.cons, solo:solo, worst:worst.c,
            stop:worst.r.lvl === 'now' || blind, total:list.length};
  }

  /* "M128-P100" - это не SPN, а закодированные MID+PID/SID
     (см. MID_BRANDS выше): показываем как "MID 128 · P100", а не
     врём, что это SPN. Обычные коды - без изменений. */
  function codeLabel(spn){
    var m = /^M(\d+)-([PS]\d+)$/.exec(spn);
    return m ? ('MID ' + m[1] + ' · ' + m[2]) : ('SPN ' + spn);
  }

  function codeLine(c){
    return '<span class="mono">' + codeLabel(c.spn) + '/' + c.fmi + '</span>' +
           (c.ownFmi ? '<small>' + esc(t('fmiOwn')) + '</small>' : '') +
           '<span>' + codeText(c) + '</span>';
  }
  function group(label, items, cls){
    if(!items.length) return '';
    return '<div class="grp"><div class="st">' + esc(label) + '</div>' +
      '<ul class="cons ' + (cls || '') + '">' +
      items.map(function(c){
        return '<li class="' + (c.urgent ? 'hit' : '') + '">' + codeLine(c) + '</li>';
      }).join('') + '</ul></div>';
  }

  /* ============================================================
     ГОРИЗОНТ РИСКА

     «Ехать нельзя» - это ещё не ответ. На обочине человек решает
     не да/нет, а другое: дотяну до базы или встаю здесь, и что мне
     будет, если всё-таки поеду. Разница между «масло ушло» и
     «оборван провод датчика масла» - это разница между капремонтом
     и спокойным рейсом до ТО, хотя код в обоих случаях про давление
     масла, и оба помечены как серьёзные.

     Поэтому здесь не оценка тяжести, а три вещи: сколько есть
     времени, что произойдёт дальше и чем это кончится.

     Текст держим на русском и английском, как и описания кодов:
     это содержательная часть справочника, а не подписи интерфейса.
     ============================================================ */

  var RISK_RANK = {now:0, short:1, base:2, watch:3, plan:4};
  var RISK_LVL = {
    now  :{tier:'now',  fill:1},
    short:{tier:'warn', fill:2},
    base :{tier:'warn', fill:3},
    watch:{tier:'calm', fill:3},
    plan :{tier:'calm', fill:4}
  };

  /* Куда какой код попадает. elec отделяем только там, где это
     правда меняет решение: оборванный провод датчика масла и
     ушедшее масло - разные поездки. Во всём остальном по умолчанию
     считаем величину настоящей: ошибиться в сторону осторожности
     дешевле, чем наоборот. */
  var RISK_MAP = {
    oil  :{elec:['oilElec','watch'],  any:['oilPhys','now']},
    cool :{elec:['coolElec','watch'], any:['coolPhys','now']},
    brake:{                           any:['brake','now']},
    enginebrake:{                     any:['engBrake','watch']},
    scr  :{                           any:['scr','base']},
    power:{                           any:['power','short']},
    can  :{                           any:['can','base']},
    fuel :{elec:['elecGen','watch'],  any:['fuelPhys','short']},
    air  :{elec:['elecGen','watch'],  any:['airPhys','base']},
    trans:{                           any:['trans','short']},
    prot :{                           any:['prot','base']}
  };

  var RISK_TITLE = {ru:'Что будет, если ехать дальше',
                    en:'What happens if you keep driving'};
  var RISK_H = {
    ru:{now:'Минуты', short:'До ближайшей остановки', base:'Хватит доехать до базы',
        watch:'Ехать можно, следить самому', plan:'До ближайшего ТО'},
    en:{now:'Minutes', short:'To the nearest safe stop', base:'Enough to reach the yard',
        watch:'Drivable, but watch it yourself', plan:'Until the next service'}
  };
  /* Приписка на случай, когда наш спокойный вывод расходится
     с меткой производителя. Молчать об этом расхождении нельзя. */
  var RISK_FLAG = {
    ru:'При этом производитель пометил код как критический — если сомневаешься, надёжнее остановиться и посмотреть на месте.',
    en:'That said, the manufacturer flags this code as critical — if in doubt, it is safer to stop and check on the spot.'
  };

  var RISK_TX = {
    ru:{
      oilPhys:['Масляная плёнка в подшипниках уже рвётся. Каждая минута под нагрузкой — это металл по металлу на шейках коленвала.',
               'Дальше — провёрнутые вкладыши и капитальный ремонт двигателя. Глушить сразу, к обочине катиться накатом, не подгазовывая.'],
      oilElec:['Само давление, скорее всего, в норме: код электрический — обрыв или замыкание в цепи датчика, а не потеря масла.',
               'Ехать можно, но настоящее падение давления приборка теперь не покажет. До ремонта цепи проверяй уровень щупом на каждой остановке.'],
      coolPhys:['Двигатель уже за пределом по температуре. Алюминиевая головка ведёт себя быстро: сначала уходит геометрия, потом прогорает прокладка.',
                'Дальше — пробитая прокладка ГБЦ, повреждённая головка, в худшем случае трещина в блоке. Заглушить и дать остыть; крышку расширительного бачка на горячую не открывать.'],
      coolElec:['Код электрический: врёт датчик или его проводка, а не система охлаждения.',
                'Стрелка температуры теперь ненадёжна, а вентилятор может не включиться вовремя. Следи за уровнем ОЖ и не держи двигатель в нагрузке на затяжном подъёме.'],
      engBrake:['Моторный (выхлопной) тормоз или ретардер не работает: машина едет, но на спуске тормозит только колёсная система. Колёсные тормоза при этом работают штатно.',
                'На длинных спусках держи пониженную передачу и тормози колёсами короткими торможениями, давая им остыть. Привод и пневмоклапан моторного тормоза проверь на ближайшей стоянке.'],
      brake:['Часть тормозного контура или ABS/EBS вышла из работы. Педаль при этом может ощущаться нормально — до первого экстренного торможения или спуска.',
             'Дальше — увеличенный тормозной путь, занос на скользком, отказ на затяжном спуске. Это тот случай, когда «доеду потихоньку» не работает.'],
      scr:['Дозирование мочевины прервано, и блок это считает. Сначала лампа, потом срез момента, потом принудительное ограничение до скорости пешехода — ступени включаются по наработке, а не разом.',
           'Посреди трассы машина не заглохнет, но запас времени тает с каждым часом работы. Планировать ремонт нужно сейчас, а не когда мощности уже не останется: эмулятор и «отключить мочевину» проблему не убирают, коды копятся дальше.'],
      power:['Бортовая сеть не держит напряжение. Пока двигатель работает, всё тянет генератор; заглушишь — можешь не завестись.',
             'Дальше сядет свет, начнут отваливаться блоки и сыпаться ложные коды по всей машине. До места, где есть помощь, лучше доехать не глуша двигатель.'],
      can:['Блоки перестали слышать друг друга по шине. Часть показаний на панели теперь берётся из воздуха, часть функций просто выключена.',
           'Физически ехать можно, но приборке верить нельзя, и остальные коды в списке вполне могут быть ложными: сначала лечится шина, потом всё остальное.'],
      fuelPhys:['Топливо приходит не в том количестве или не под тем давлением. На подъёме и под нагрузкой это вылезет первым.',
                'Скорее всего, заглохнешь на трассе, и не факт, что заведёшься с обочины. Если причина в фильтре или воде в баке — до сервиса дотянуть реально; если в ТНВД — нет.'],
      airPhys:['Наддув не выходит на расчётные значения: турбина, интеркулер или впуск. Двигатель компенсирует это составом смеси и греется сильнее обычного.',
               'Тяги не будет, расход вырастет, на затяжном подъёме добавится перегрев. Если со стороны турбины слышен вой или свист — не тянуть: там разрушается крыльчатка.'],
      trans:['Коробка или сцепление ушли в аварийный режим: часть передач может стать недоступна, робот — перестать переключаться под нагрузкой.',
             'Главный риск — остаться на подъёме без передачи и покатиться назад. Гружёным в горы не идти; до ровного места и сервиса — можно.'],
      prot:['Это не поломка, а реакция на неё: блок сам режет мощность, чтобы защитить двигатель или выхлоп.',
            'Ограничение будут ужесточать, пока причину не устранят. Искать надо не этот код, а тот, из-за которого он появился.'],
      elecGen:['Код электрический: обрыв, замыкание или плохой контакт в цепи датчика. Сама величина, которую он меряет, скорее всего в норме.',
               'Ехать можно. Но пока цепь не восстановят, эта система едет вслепую и о настоящей неисправности предупредить не сможет.'],
      genUrgent:['Код помечен как критический: производитель считает, что продолжать движение без разбора нельзя.',
                 'Что именно откажет дальше, по одному этому коду сказать нельзя — поэтому останавливаться стоит при первой безопасной возможности и смотреть на месте.'],
      gen:['Отдельная неисправность без немедленных последствий для движения.',
           'Показать коды на ближайшем ТО. Если появится второй код по этой же системе — откладывать уже не стоит.']
    },
    en:{
      oilPhys:['The oil film in the bearings is already breaking down. Every minute under load is metal on metal on the crank journals.',
               'Next comes spun bearings and a full engine rebuild. Shut it down now and coast to the shoulder without revving.'],
      oilElec:['The pressure itself is most likely fine: this is an electrical fault — an open or a short in the sensor circuit, not lost oil.',
               'You can drive, but the dash will no longer warn you about a real pressure drop. Until the circuit is repaired, check the level with the dipstick at every stop.'],
      coolPhys:['The engine is already past its temperature limit. An aluminium head goes fast: first the geometry warps, then the gasket burns through.',
                'Next comes a blown head gasket, a damaged head and, at worst, a cracked block. Shut it down and let it cool — never open the expansion tank cap while hot.'],
      coolElec:['This is an electrical fault: the sensor or its wiring is lying, not the cooling system.',
                'The temperature gauge is unreliable now and the fan may not kick in on time. Watch the coolant level and keep the engine off load on long climbs.'],
      engBrake:['The engine (exhaust) brake or retarder is not working: the truck still drives, but on a descent only the wheel brakes slow it. The wheel brakes themselves work normally.',
                'On long descents use a lower gear and short wheel-brake applications to let them cool. Check the engine brake actuator and its air valve at the next stop.'],
      brake:['Part of the brake circuit or ABS/EBS is out of service. The pedal may still feel normal — until the first emergency stop or descent.',
             'Next comes longer stopping distance, a skid on a slick surface, failure on a long downgrade. This is the case where "I will take it slow" does not work.'],
      scr:['Urea dosing is interrupted and the ECU is counting. First the lamp, then a torque cut, then a forced crawl speed — the stages come in by engine hours, not all at once.',
           'The truck will not die mid-highway, but the window shrinks with every running hour. Plan the repair now, not when the power is gone: an emulator or "deleting AdBlue" does not remove the problem, the codes keep stacking.'],
      power:['The electrical system is not holding voltage. While the engine runs the alternator carries it; shut it off and you may not restart.',
             'Next the lights go, then modules start dropping out and false codes appear all over the truck. Get to somewhere with help without shutting the engine down.'],
      can:['The modules have stopped hearing each other on the bus. Some dash readings are now made up and some functions are simply off.',
           'You can physically drive, but do not trust the instruments, and the other codes in the list may well be false: fix the bus first, then look at the rest.'],
      fuelPhys:['Fuel is not arriving in the right amount or at the right pressure. It shows up first on climbs and under load.',
                'You will most likely stall out on the road, and may not restart on the shoulder. A clogged filter or water in the tank you can nurse to a shop; a failing injection pump you cannot.'],
      airPhys:['Boost is not reaching its target: turbo, intercooler or intake. The engine compensates with mixture and runs hotter than usual.',
               'You will lose pull, burn more fuel and add overheating on long climbs. If you hear a whine or a whistle from the turbo, stop — the wheel is breaking up.'],
      trans:['The gearbox or clutch has gone into limp mode: some gears may be unavailable and an automated box may stop shifting under load.',
             'The main risk is being left on a climb with no gear and rolling back. Do not take a loaded truck into the hills; reaching level ground and a shop is fine.'],
      prot:['This is not the fault, it is the reaction to it: the ECU is cutting power to protect the engine or the aftertreatment.',
            'The limit will keep tightening until the cause is fixed. The code to chase is the one that triggered this, not this one.'],
      elecGen:['This is an electrical fault: an open, a short or a bad contact in the sensor circuit. The value it measures is most likely fine.',
               'You can drive. But until the circuit is repaired this system runs blind and cannot warn you about a real failure.'],
      genUrgent:['The code is flagged critical: the manufacturer considers it unsafe to keep driving without checking.',
                 'This code alone cannot say what will fail next, so stop at the first safe opportunity and look at it on the spot.'],
      gen:['A standalone fault with no immediate consequences for driving.',
           'Show the codes at the next service. If a second code from the same system appears, stop putting it off.']
    }
  };

  function riskOf(c){
    var m = RISK_MAP[c.sys], pick;
    /* Для охлаждения «недостоверные данные» (FMI 2 и родственные) - тоже не
       физический перегрев: датчик или вентилятор врут, двигатель не греется.
       Иначе 1639.2 (частота вентилятора) давало «Минуты: перегрев». */
    var elec = isElec(c);
    var nonPhys = elec || (c.sys === 'cool' && isDerived(c));
    if(c.ownFmi && elec) pick = (m && m.elec) ? m.elec : ['elecGen','watch'];
    else if(m) pick = (m.elec && nonPhys) ? m.elec : m.any;
    else if(elec) pick = ['elecGen','watch'];
    else pick = c.urgent ? ['genUrgent','short'] : ['gen','plan'];

    var lvl = pick[1], flag = false;
    /* Метка производителя перевешивает наш спокойный вывод: поднимаем
       горизонт и говорим о расхождении вслух, а не втихую. */
    if(c.urgent && (lvl === 'plan' || lvl === 'watch')){ lvl = 'short'; flag = true; }
    return {key:pick[0], lvl:lvl, flag:flag};
  }

  function riskBlock(c, tag){
    var L = currentLang === 'ru' ? 'ru' : 'en';
    var r = riskOf(c), meta = RISK_LVL[r.lvl], tx = RISK_TX[L][r.key], bars = '';
    for(var i = 0; i < 4; i++) bars += '<i class="' + (i < meta.fill ? 'on' : '') + '"></i>';
    return '<div class="grp"><div class="st">' + esc(RISK_TITLE[L] + (tag || '')) + '</div>' +
      '<div class="risk t-' + meta.tier + '">' +
        '<div class="rkh"><span class="rkb">' + esc(RISK_H[L][r.lvl]) + '</span>' +
          '<span class="rkl" aria-hidden="true">' + bars + '</span></div>' +
        '<p>' + esc(tx[0]) + '</p>' +
        '<p>' + esc(tx[1]) + (r.flag ? ' ' + esc(RISK_FLAG[L]) : '') + '</p>' +
      '</div></div>';
  }

  var MARK_STOP = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8.2 2h7.6L22 8.2v7.6L15.8 22H8.2L2 15.8V8.2L8.2 2Zm2.8 5v7h2V7h-2Zm0 9v2h2v-2h-2Z"/></svg>';
  var MARK_WARN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 23 21H1L12 2Zm-1 7v6h2V9h-2Zm0 8v2h2v-2h-2Z"/></svg>';

  function cascade(a){
    var html = '';
    html += '<div class="verdict ' + (a.stop ? 'stop' : 'warn') + '">' +
              '<span class="vmark">' + (a.stop ? MARK_STOP : MARK_WARN) + '</span>' +
              '<span><span class="vtitle">' + esc(t(a.stop ? 'vStop' : 'vWarn')) + '</span>' +
              '<span class="vsub">' + esc(t(a.stop ? 'vStopSub' : 'vWarnSub')) + '</span></span>' +
              '<span class="vcount">' + esc(t('casCount', {n:a.total})) + '</span>' +
            '</div>';

    html += '<div class="card">';
    html += '<div class="grp" style="margin-top:0"><div class="st">' + esc(t('casRoot')) + '</div>' +
              '<div class="root">' +
                '<div class="rcode"><span class="mono">' + codeLabel(a.root.spn) + '/' + a.root.fmi + '</span>' +
                  '<span class="sys">' + esc(t('sys' + a.root.sys.charAt(0).toUpperCase() + a.root.sys.slice(1))) + '</span></div>' +
                '<div class="rtext">' + codeText(a.root) + '</div>' +
                '<div class="rwhy">' + esc(a.cons.length ? t('casWhyChain') : t('casWhySingle')) + '</div>' +
              '</div></div>';

    html += group(t('casCons'), a.cons);
    html += group(t('casSolo'), a.solo, 'solo');

    /* Обычно срок задаёт первопричина, но не всегда: рядом с гроздью
       от пустого бака может лежать одинокий тормозной код, и жёстче
       именно он. Тогда показываем его и подписываем номером, чтобы
       не выглядело, будто это про корень. */
    html += riskBlock(a.worst, a.worst === a.root ? '' :
                      ' · ' + codeLabel(a.worst.spn) + '/' + a.worst.fmi);

    html += '<div class="grp"><div class="st">' + esc(t('casTodo')) + '</div>' +
              '<ol class="todo"><li>' + esc(t(ACT[a.root.sys] || 'actDefault')) + '</li></ol></div>';

    return html + '</div>';
  }


  /* Ссылка на разбор. Водитель всё равно звонит механику и диктует
     коды голосом - пусть лучше отправит ссылку, по которой тот увидит
     ровно тот же отчёт. Параметр предпросмотра в неё намеренно не
     попадает: получателю уходит обычный адрес сайта. */
  /* Раньше здесь заново разбирали input.value через parseAll() - тот
     же разбор, что и для обычных SPN/FMI. Для дилерских кодов и для
     MID-марок (Freightliner и т.п.) run() ведёт код по другим веткам
     (fetchPcode, parseAllMid) - parseAll() их не понимает и находит
     ноль пар, кнопка молча ничего не делала. Теперь ссылка несёт сырой
     текст поля через ?q= - тот же путь, что уже был у SearchAction -
     и восстановление на другом конце просто повторяет run(), а не
     дублирует его логику вторым парсером. */
  function shareUrl(){
    var val = input.value.trim();
    if(!val) return null;
    var u = location.origin + location.pathname + '?q=' + encodeURIComponent(val);
    if(sel.value) u += '&b=' + encodeURIComponent(sel.value);
    if(MODE !== 'main') u += '&mode=' + MODE;
    if(MID_BRANDS[sel.value] && midSel.value) u += '&mid=' + encodeURIComponent(midSel.value);
    return u;
  }

  var ICON_PRINT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 8V3h10v5"/>' +
    '<rect x="3" y="8" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/></svg>';
  var ICON_SEND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M21 3 10.5 13.5M21 3l-6.5 18-4-8-8-4L21 3Z"/></svg>';

  /* Чем разбор заканчивается: ссылку кидают механику, лист кладут
     к машине. Обе кнопки стоят здесь, в конце ответа, а не иконкой
     в углу - там их на телефоне просто не замечают. */
  function actions(){
    var box = document.createElement('div');
    box.className = 'acts';

    var sh = document.createElement('button');
    sh.type = 'button'; sh.className = 'act act-main';
    sh.innerHTML = ICON_SEND + '<span></span>';
    var lbl = sh.querySelector('span');
    lbl.textContent = t('shareLabel');
    sh.addEventListener('click', function(){
      var u = shareUrl();
      if(!u) return;
      if(navigator.share) return navigator.share({url:u}).catch(function(){});
      /* Без системного «поделиться» кладём в буфер и говорим об этом
         той же кнопкой - лишнее всплывающее окно тут ни к чему. */
      var done = function(){
        lbl.textContent = t('shareDone');
        setTimeout(function(){ lbl.textContent = t('shareLabel'); }, 2200);
      };
      if(navigator.clipboard) navigator.clipboard.writeText(u).then(done, function(){});
      else done();
    });

    box.appendChild(sh);

    var pr = document.createElement('button');
    pr.type = 'button'; pr.className = 'act';
    pr.innerHTML = ICON_PRINT + '<span></span>';
    pr.querySelector('span').textContent = t('printLabel');
    pr.addEventListener('click', function(){ window.print(); });
    box.appendChild(pr);

    out.appendChild(box);
  }

  /* Тема запоминается: человек выставляет её один раз под свой свет
     в кабине, и переспрашивать при каждом заходе незачем. На кнопке
     всегда то, куда она переключит, а не то, что сейчас. */
  var themeBtn = document.getElementById('pf-theme');
  function labelTheme(){
    var lt = document.documentElement.getAttribute('data-theme') === 'light';
    var s = t(lt ? 'themeNight' : 'themeDay');
    themeBtn.title = s;
    themeBtn.setAttribute('aria-label', s);
  }
  themeBtn.addEventListener('click', function(){
    var lt = document.documentElement.getAttribute('data-theme') !== 'light';
    if(lt) document.documentElement.setAttribute('data-theme', 'light');
    else document.documentElement.removeAttribute('data-theme');
    try{ localStorage.setItem('ct-theme', lt ? 'light' : 'dark'); }catch(e){}
    labelTheme();
  });

  langSelect.addEventListener('change', function(){
    if(LOCK_LANG){
      var picked = langSelect.value;
      try{ localStorage.setItem(LANG_KEY, picked); }catch(e){}
      location.href = picked === 'ru' ? '/' : '/' + picked + '/';
      return;
    }
    applyLang(langSelect.value);
    labelTheme();
  });
  applyLang(currentLang);
  labelTheme();
  offerLang();

  /* printable - только для разобранного кода: печатать сообщение
     «код не найден» смысла нет, поэтому кнопка гаснет. */
  function render(html, printable){
    out.innerHTML = html;
    if(printable) actions();
  }

  /* Перед разбором нужны обе базы: основная и, для нерусского
     интерфейса, английские описания. */
  function ready(){ return Promise.all([load(), loadEn()]); }

  /* Номер последнего разбора: дополнительный дилерский блок старого запроса
     не должен лечь поверх нового результата. */
  var runSeq = 0;
  /* Без марки код читается по стандарту, а дилерский номер может значить другое
     у каждой марки. Поэтому дилерскую базу без марки спрашиваем один раз (это
     один запрос к воркеру): если номер известен у марок, их тексты идут блоком
     «у марок: …» под стандартным смыслом. Нет связи - остаётся стандартный ответ. */
  function brandlessAllowed(typed, skip){
    return !skip && /^\d{1,7}(?:[ \-\/.,]\d{1,3})?$/.test(typed);
  }
  /* Кнопка «Поискать у марок» под стандартным ответом. Запрос к воркеру уходит
     только по нажатию: суточный лимит не тратим на каждый ввод без марки. */
  var brandlessCtx = null;
  function brandlessAsk(typed, skip){
    if(!brandlessAllowed(typed, skip)) return '';
    brandlessCtx = {typed: typed};
    return '<div class="brandless"><button type="button" class="brandless-ask">' +
           esc(t('brandlessAsk')) + '</button></div>';
  }
  out.addEventListener('click', function(e){
    var btn = e.target && e.target.closest ? e.target.closest('.brandless-ask') : null;
    if(!btn || !brandlessCtx) return;
    var ctx = brandlessCtx, seq = runSeq, slot = btn.parentNode;
    brandlessCtx = null;
    slot.innerHTML = note(t('pcodeSearching'));
    brandlessRun(ctx.typed).catch(function(err){ return pcodeErrorText(err, ''); }).then(function(h){
      if(seq === runSeq) slot.innerHTML = h;
    });
  });
  function brandlessRun(typed){
    return fetchPcodeOne('', typed, currentLang).then(function(hits){
      if(!hits || !hits.length) return note(t('brandlessNone'));
      var names = [], texts = [];
      hits.forEach(function(h){
        var nm = brandName(h.brand) || h.brand;
        if(names.indexOf(nm) < 0) names.push(nm);
        /* Текст воркера уже начинается с названия марки («Volkswagen — …») - второй раз не пишем. */
        texts.push('<b>' + esc(h.text) + '</b>');
      });
      return chain([{st: t('dealerAtBrands', {brands: esc(names.join(', '))}), tx: texts.join('<br>'), cls:'ok'}]);
    });
  }

  function run(skipDealer, noSpecial, noOpen){
    /* Словарь грузится по первому действию: до его прихода ждём и запускаем
       тот же разбор с теми же аргументами. */
    if(!DB){
      var runArgs = arguments;
      load().then(function(){ run.apply(null, runArgs); }).catch(function(){});
      return;
    }
    /* Отопитель и тахограф - свои пути разбора, SPN/FMI и блинки сюда не идут. */
    if(MODE !== 'main') return runMode();
    var mySeq = ++runSeq;
    /* Хвост из знаков восклицания и точки в конце не влияет на код («0104!!» = «0104»):
       срезаем его здесь, чтобы маршрут (дилерская база, SPN, MID) выбирался по коду. */
    var typed = String(input.value || '').trim().replace(/\s+/g, ' ').replace(/\s*[!?.;:]+$/, '');
    var up = normCode(typed);
    var brand = sel.value;
    var midNote = '';
    /* Volvo: MID, SID, PSID или PPID в коде - таблица модулей (volvomid), а не SPN.
       Без MID берём модуль двигателя 128. */
    /* MID-код Volvo вида «M128-P100.1» (с пробелом или дефисом у M) узнаём по
       шаблону, а не только по слову MID: такой код - MID-код при любой марке
       и без марки. Detroit/Western Star и Mack/Freightliner свою схему держат. */
    var midLike = /^M\s*-?\s*\d{3}\s*[-\/]?\s*(?:PPID|PSID|PID|SID|PP|PS|P|S)\s*\d/.test(up);
    var fromVolvo = (brand === 'volvo' && (/\bMID\s*\d{3}\b/.test(up) || /\b(SID|PSID|PPID)\s*\d/.test(up))) ||
                    (midLike && brand !== 'freightliner' && brand !== 'mack' &&
                     brand !== 'detroitdiesel' && brand !== 'westernstar');
    if(fromVolvo) brand = 'volvomid';
    var midBrand = !!MID_BRANDS[brand];
    /* Detroit/Western Star с явным SPN - обычный SPN/FMI, а не MID/PID.
       Так же и с шестизначным SPN и FMI через точку, дефис или пробел
       («520199.19»): у этих марок такой код - не MID, а SPN/FMI. */
    if(midBrand && MID_FIXED[brand] && (/SPN/.test(up) || /^\d{1,7}\s*[-.\/,\s]\s*\d{1,3}(?![-.\/,\s]\s*\d)(?!\d)/.test(up))) midBrand = false;
    var mid = null;
    if(midBrand){
      var typedMid = midSplit(up).mid;
      var listMid = MID_FIXED[brand] || midSel.value || null;
      mid = typedMid || listMid;
      if(!typedMid && fromVolvo){ mid = '128'; midNote = stLine(t('midDefault')); }
      else if(typedMid && listMid && typedMid !== listMid && !MID_FIXED[brand]){
        midNote = stLine(t('midTyped', {mid: typedMid, sel: listMid}));
      }
    }
    function rnd(h, printable){ render(midNote + h, printable); }

    /* Freightliner/Mack без модуля - код неоднозначен. Исключение: OBD-код. */
    if(midBrand && !mid && (MID_PCODE_BRANDS[brand] || !midObdCode(typed))){
      rnd(note(t('needMid'))); return;
    }

    /* FC Cummins и блинк КамАЗ - свои индексы; нет в индексе - обычный путь. */
    var special = (!midBrand && (brand === 'kamaz' || !brand) && !noSpecial) ? specialKind(typed, brand) : null;
    if(special){
      ready().then(function(){
        var sh = specialHtml(special);
        if(sh === null){ run(skipDealer, true); return; }
        rnd(sh, true);
      }).catch(function(){ rnd(note(t('loadError'))); });
      return;
    }

    /* Закрытая марка и ввод «число-число», которое есть в её открытом словаре
       (ЯМЗ «27.3», Renault «2.5», MAN «00597-05», Isuzu «102.3», Iveco): текст
       словаря показываем первым и всегда, ответ закрытой базы - дополнительно. */
    var openable = !midBrand && !noOpen && brand !== 'kamaz' && isClosedBrand(brand) &&
                   /^\d{1,7}\s*[-.\/,\s]\s*\d{1,3}$/.test(typed);
    if(openable){
      rnd(note(t('pcodeSearching')));
      ready().then(function(){
        var oh = openPairHit(brand, typed);
        if(!oh){ run(skipDealer, noSpecial, true); return; }
        return closedLookup(brand, normCode(typed)).then(function(r){
          if(mySeq === runSeq) rnd(openFirstHtml(typed, oh, r, brand), true);
        }, function(){
          if(mySeq === runSeq) rnd(openFirstHtml(typed, oh, null, brand) +
            stLine(t('dealerOffline', {brand: brandName(brand) || brand})), true);
        });
      }).catch(function(){ if(mySeq === runSeq) rnd(note(t('loadError'))); });
      return;
    }

    /* Блинк-код марки с блинками: сначала открытый словарь, затем закрытая база.
       J1939 здесь не показываем - это не SPN/FMI. */
    var bc = (!midBrand && brand !== 'kamaz' && BLINK_BRANDS[brand]) ? blinkCode(typed) : null;
    if(bc){
      rnd(note(t('pcodeSearching')));
      ready().then(function(){
        var hit = blinkOpen(brand, bc.code, typed);
        if(hit){ rnd(hit, true); return; }
        if(!isClosedBrand(brand)){ rnd(note(t('blinkNotFoundFor', {n: bc.code, brand: brandName(brand) || brand}))); return; }
        return closedLookup(brand, typed).then(function(r){
          if(mySeq !== runSeq) return;
          if(!r.net.length && !r.mine.length){ rnd(note(t('blinkNotFoundFor', {n: bc.code, brand: brandName(brand) || brand}))); return; }
          rnd(closedHtml(typed, r, brand), true);
        });
      }).catch(function(e){ if(mySeq === runSeq) rnd(pcodeErrorText(e, brand)); });
      return;
    }

    /* Список через запятую у марки с закрытой базой (DAF, Volvo, Mercedes, MWM):
       каждый элемент разбираем так же, как одиночный ввод этой марки - дилерская
       база первой, потом стандарт J1939. Элемент, который не разобрали, показываем
       строкой «не разобрали», а не отбрасываем молча. */
    var items = (!midBrand && isClosedBrand(brand) && !skipDealer && std.value !== 'spnfmi' &&
                 !/\b(SPN|FMI)\b/.test(up) && /[,;]/.test(typed)) ? typed.split(/\s*[,;]\s*/).filter(Boolean) : null;
    if(items && items.length >= 2){
      var unparsed = [];
      ready().then(function(){
        return Promise.all(items.map(function(it){
          var ip = parse(it, 'auto');
          if(!ip || ip.bad || ip.bigSpn){ unparsed.push(it); return ''; }
          var code = ip.pcode ? ip.pcode : normCode(it);
          return closedLookup(brand, code).then(function(r){
            if(r.net.length || r.mine.length) return closedHtml(code, r, brand);
            if(ip.pcode) return note(t('pcodeNotFound', {code: esc(code)}));
            /* Нет в дилерской базе - тот же стандартный ответ, что у одиночного ввода. */
            if(ip.fmi == null){
              var nm = spnName(ip.spn, brand);
              return nm ? spnOnlyHtml(ip.spn, brand, nm, false) : note(t('spnNotFound', {spn: esc(ip.spn)}));
            }
            return spnFmiHtml(ip.spn, ip.fmi, brand, null, false);
          }, function(e){ return pcodeErrorText(e, brand); });
        }));
      }).then(function(parts){
        if(mySeq !== runSeq) return;
        var html = parts.join('');
        if(unparsed.length) html += note(t('notParsed', {items: esc(unparsed.join(', '))}));
        rnd(html, true);
      }).catch(function(){ if(mySeq === runSeq) rnd(note(t('loadError'))); });
      return;
    }

    /* Два кода и больше - выгрузка со сканера: разбираем целиком по стандарту. */
    var numPcode = !!NUM_PCODE_BRANDS[brand] && std.value !== 'spnfmi' && !/FMI/.test(up);
    var many = midBrand ? (MID_PCODE_BRANDS[brand] ? [] : parseAllMid(typed, mid))
             : ((std.value === 'pcode' || numPcode) ? [] : parseAll(typed));
    if(many.length >= 2){
      ready().then(function(){
        rnd(cascade(analyze(many, brand)), true);
      }).catch(function(){ rnd(note(t('loadError'))); });
      return;
    }

    /* Номер или пара «номер-номер» у закрытой марки - сначала её база (fallback:
       если там пусто, идём в стандарт J1939 тем же run(true)). Буквенно-цифровые
       коды (E00, F09, EMS 11, P0340) тоже уходят в базу без стандарта. */
    var isNumIn = /^\d{1,7}(?:[ \-\/.,]\d{1,3})?$/.test(typed);
    var isLetterIn = !midBrand && /^[A-Z]{1,4}[ \-]?\d{1,5}$/.test(up) && !/SPN|FMI|MID|SID|PID/.test(up);
    var renSingle = !!SPN_PCODE_BRANDS[brand] && /^\d{1,7}$/.test(typed) && std.value !== 'spnfmi';
    var closed = !midBrand && isClosedBrand(brand) && !skipDealer && std.value !== 'spnfmi' && !renSingle;
    var shortHex = !!HEX_KEY_BRANDS[brand] && /^[0-9A-F]{1,3}$/.test(up) && /[A-F]/.test(up);
    var p;
    if(midBrand) p = parseMidCode(typed, mid, brand);
    else if(numPcode || (closed && (isLetterIn || shortHex))) p = {pcode: normCode(typed)};
    else if(closed && isNumIn) p = {pcode: normCode(typed), fallback: std.value !== 'pcode'};
    else p = parse(typed, std.value);
    if(!p){ rnd(note(t('emptyPrompt'))); return; }
    /* Подпись «по стандарту J1939 - у марки номер может значить другое». */
    var cap = (!midBrand && isClosedBrand(brand) && isNumIn) ? j1939Caption(brand) : '';

    if(p.pcode){
      rnd(note(t('pcodeSearching')));
      closedLookup(brand, p.pcode).then(function(r){
        if(mySeq !== runSeq) return;
        if(!r.net.length && !r.mine.length){
          if(p.bigSpn){ rnd(note(t('spnTooBig', {spn: esc(p.bigSpn)}))); return; }
          if(p.fallback && !parse(typed, 'auto').bad){ run(true); return; }
          rnd(note(t('pcodeNotFound', {code: esc(p.pcode)})));
          return;
        }
        rnd(closedHtml(p.pcode, r, brand) + (p.fallback ? safeQuiet(typed, brand) : ''), true);
      }).catch(function(e){
        if(mySeq !== runSeq) return;
        rnd(pcodeErrorText(e, brand) + (p.fallback ? safeQuiet(typed, brand) : ''));
      });
      return;
    }

    /* Renault: заводской номер записан словом «SPN» плюс число (см. SPN_PCODE_BRANDS).
       Сначала заводская таблица, при промахе - стандарт тем же run(true). */
    if(SPN_PCODE_BRANDS[brand] && !skipDealer && std.value !== 'spnfmi' && p.spn != null && p.fmi == null){
      var rcode = 'SPN' + p.spn;
      rnd(note(t('pcodeSearching')));
      load().then(function(){
        return fetchPcode(brand, rcode, currentLang);
      }).then(function(hits){
        if(mySeq !== runSeq) return;
        if(!hits.length){ run(true); return; }
        var rSteps = [{st:t('stepCode'), tx:pcodeStep(rcode, hits), cls:'ok'}];
        hits.forEach(function(h){
          rSteps.push({
            st: hits.length > 1 ? brandName(h.brand) : donorStep(h.brand, brand),
            tx: '<b>' + esc(h.text) + '</b>', cls:'ok'
          });
        });
        rnd(chain(rSteps), true);
      }).catch(function(){ if(mySeq === runSeq) run(true); });
      return;
    }

    ready().then(function(){
      if(p.bigSpn){ rnd(note(t('spnTooBig', {spn: esc(p.bigSpn)}))); return; }
      if(p.bad){ rnd(note(p.fmiOnly ? t('needSpnFmi') : t('badCode'))); return; }
      /* SPN без FMI: имя параметра, либо дилерская таблица тем же числом. */
      if(p.fmi === null){
        var nm = spnName(p.spn, brand);
        if(!nm){
          var num = String(p.spn);
          var nMine = scanRefs(brand, num);
          if(nMine.length){ rnd(scanHtml(num, nMine), true); return; }
          /* Из run(true) базу уже спрашивали - второй запрос не делаем. */
          if(skipDealer){ rnd(cap + note(t('spnNotFound', {spn: p.spn}))); return; }
          rnd(note(t('pcodeSearching')));
          fetchPcode(brand, num, currentLang).then(function(hits){
            if(mySeq !== runSeq) return;
            if(!hits.length){ rnd(cap + note(t('spnNotFound', {spn: p.spn}))); return; }
            var nSteps = [{st:t('stepCode'), tx:pcodeStep(num, hits), cls:'ok'}];
            hits.forEach(function(h){
              nSteps.push({
                st: hits.length > 1 || !brand ? brandName(h.brand) : donorStep(h.brand, brand),
                tx: '<b>' + esc(h.text) + '</b>', cls:'ok'
              });
            });
            rnd(chain(nSteps), true);
          }).catch(function(e){
            rnd(note(e && e.network ? t('pcodeApiError')
                   : (isDailyLimit(e) ? t('dailyLimit') : t('spnNotFound', {spn: p.spn}))));
          });
          return;
        }
        rnd(cap + spnOnlyHtml(p.spn, brand, nm, false) + brandlessAsk(typed, skipDealer || !!brand), true);
        return;
      }
      /* Кнопку даём только при стандартном ответе: SPN неизвестен - как до правки, без запроса. */
      var stdKnown = !!spnName(p.spn, brand);
      rnd(cap + spnFmiHtml(p.spn, p.fmi, brand, null, false) +
          (stdKnown ? brandlessAsk(typed, skipDealer || !!brand) : ''), true);
    }).catch(function(){
      rnd(note(t('loadError')));
    });
  }

  /* Разбор по ссылке: ?c=100-1,110-3&b=kamaz - по ней механик
     открывает ровно тот же отчёт, что видел водитель. Работает на
     обычном сайте, а не только в предпросмотре: ссылку получает
     человек со стороны, и никаких параметров вида он не ждёт.
     Марку ставим после загрузки справочника - до неё в списке
     марок ещё пусто. */
  var qc = /[?&]c=([0-9A-Fa-f,\-]+)/.exec(location.search);
  if(qc){
    var pairs = qc[1].split(',').filter(function(x){ return /^[0-9A-Fa-f]{1,6}-[0-9A-Fa-f]{1,3}$/.test(x); });
    if(pairs.length){
      ready().then(function(){
        var qb = /[?&]b=([a-z]+)/.exec(location.search);
        if(qb && DB.brandNames[qb[1]]) sel.value = qb[1];
        input.value = pairs.map(function(x){
          var pr = x.split('-');
          return 'SPN ' + pr[0] + ' FMI ' + pr[1];
        }).join(', ');
        run();
      }).catch(function(){});
    }
  } else {
    /* ?b=kenworth без кода - переход с блока «по маркам» на главной.
       Часть марок не имеет своей страницы в разделе (их коды лежат в
       таблице марки-донора), и в списке они стояли серыми надписями:
       человек видел своё название и не мог по нему никуда пойти, хотя
       поиск эту марку читает. Теперь такая ссылка открывает поиск с
       уже выбранной маркой. Марку ставим после загрузки справочника -
       до неё список марок ещё пуст, как и в разборе по ссылке выше. */
    var qb1 = /[?&]b=([a-z0-9]+)/.exec(location.search);
    /* ?q=... - цель SearchAction в JSON-LD на этой странице (см. <head>)
       и формат ссылки «Отослать разбор» из shareUrl() выше: любой текст
       из поля ввода плюс марка и модуль, без привязки к формату кода -
       работает для дилерских и MID-кодов, не только для пар SPN/FMI.
       Проверяем раньше qb1 и, если есть, забираем марку из того же
       location.search сама - иначе оба блока запустили бы run()
       вперемешку. */
    var qq = /[?&]q=([^&]+)/.exec(location.search);
    if(qq){
      ready().then(function(){
        if(qb1 && DB.brandNames[qb1[1]]){
          sel.value = qb1[1];
          fillMid();
          var qmid = /[?&]mid=([0-9]+)/.exec(location.search);
          if(qmid) midSel.value = qmid[1];
        }
        input.value = decodeURIComponent(qq[1].replace(/\+/g, ' '));
        run();
      }).catch(function(){});
    } else if(qb1){
      ready().then(function(){
        if(!DB.brandNames[qb1[1]]) return;
        sel.value = qb1[1];
        var ev;
        try{ ev = new Event('change'); }
        catch(e){ ev = document.createEvent('Event'); ev.initEvent('change', true, true); }
        sel.dispatchEvent(ev);
        input.focus();
      }).catch(function(){});
    }
  }

  /* через обёртку, а не go.addEventListener('click', run): иначе первым
     аргументом run пришло бы событие клика, и оно сработало бы как
     skipDealer - дилерская ветка ниже молча выключилась бы на кнопке. */
  go.addEventListener('click', function(){ run(); });
  input.addEventListener('keydown', function(e){ if(e.key === 'Enter') run(); });
  sel.addEventListener('change', fillMid);
  sel.addEventListener('change', applyModeUi);
  fillMid();

  /* Автодемо на первом экране: пока человек не начал действовать,
     поле по кругу само печатает и стирает пример кода - показывает,
     как им пользоваться. Разбор не запускает, ничего не решает за
     человека - только заполнение. Мгновенно и насовсем отменяется при
     любом реальном взаимодействии с формой - не спорит с человеком. */
  var scannerEl = document.getElementById('pf-scanner');
  function startIntroDemo(){
    if(qc && qc[1]) return;               // пришли по ссылке-разбору - там уже настоящий ввод
    if(MODE !== 'main') return;           // пример SPN/FMI не подходит к отопителю и тахографу
    if(input.value.trim()) return;        // поле не пустое (автозаполнение браузера и т.п.)
    if(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var cancelled = false;
    var cancelEvents = ['input', 'keydown', 'mousedown', 'focus'];
    function cancel(e){
      if(cancelled) return;
      cancelled = true;
      scannerEl.classList.remove('demo');
      /* 'input' - недопечатанный пример уже смешан с настоящим
         символом в value, трогать поздно. На любом более раннем
         событии (клик/фокус/нажатие клавиши ДО вставки символа)
         подчищаем хвост анимации, чтобы реальный ввод не слипся с
         недопечатанным/недостёртым примером (баг, найденный на
         практике: клик и печать во время анимации давали
         "SPN 100 FHELLO"). */
      if(!e || e.type !== 'input') input.value = '';
      cancelEvents.forEach(function(ev){ input.removeEventListener(ev, cancel); });
      sel.removeEventListener('change', cancel);
      std.removeEventListener('change', cancel);
      go.removeEventListener('click', cancel);
    }
    cancelEvents.forEach(function(ev){ input.addEventListener(ev, cancel); });
    sel.addEventListener('change', cancel);
    std.addEventListener('change', cancel);
    go.addEventListener('click', cancel);
    cancelDemo = cancel;

    /* Один пример строкой целиком: полная запись плюс список из двух
       кодов через запятую в короткой записи (точкой и пробелом) -
       показывает и «гирлянду» (несколько кодов сразу), и что
       разделители в запросе не важны - ровно то, что обещано в
       тексте над полем. */
    var DEMO_CODE = 'SPN 100 FMI 1, 100.1, 100 1';
    function typeIn(){
      if(cancelled) return;
      var i = 0;
      (function typeNext(){
        if(cancelled) return;
        if(i > DEMO_CODE.length){ setTimeout(eraseOut, 2200); return; }
        input.value = DEMO_CODE.slice(0, i);
        i++;
        setTimeout(typeNext, 100);
      })();
    }
    function eraseOut(){
      if(cancelled) return;
      var j = DEMO_CODE.length - 1;
      (function eraseNext(){
        if(cancelled) return;
        if(j < 0){ setTimeout(typeIn, 900); return; }
        input.value = DEMO_CODE.slice(0, j);
        j--;
        setTimeout(eraseNext, 60);
      })();
    }
    /* Демо не разбирает код и словарь не читает - только печатает пример,
       поэтому не ждёт загрузки справочника (иначе он качался бы при каждом открытии). */
    Promise.resolve().then(function(){
      if(cancelled) return;
      scannerEl.classList.add('demo');
      typeIn();
    }).catch(function(){});
  }
  setTimeout(startIntroDemo, 1000);

  /* Кнопка «Скопировать адрес» под подвалом: почтовая ссылка не работает
     там, где нет почтовой программы. Делегирование — кнопка может
     появиться в DOM позже. */
  (function(){
    function fallbackCopy(text){
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.top = '-1000px';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch(e) { ok = false; }
      document.body.removeChild(ta);
      return ok;
    }
    function showCopied(btn){
      btn.textContent = t('copied');
      clearTimeout(btn._copyTimer);
      btn._copyTimer = setTimeout(function(){ btn.textContent = t('copyMail'); }, 2000);
    }
    document.addEventListener('click', function(e){
      var btn = e.target.closest && e.target.closest('.copy-mail');
      if(!btn) return;
      var mail = btn.getAttribute('data-mail');
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(mail).then(function(){ showCopied(btn); }, function(){
          if(fallbackCopy(mail)) showCopied(btn);
        });
      } else if(fallbackCopy(mail)) showCopied(btn);
    });
  })();

})();
