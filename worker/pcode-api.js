/**
 * codetruck.ru — API дилерских кодов (Volvo/Mercedes/Scania и др.).
 *
 * Отдаёт по одному коду за раз вместо публикации всей таблицы целиком в
 * assets/dtc.enc.js / dtc.en.js. Данные заливаются в PCODE_KV скриптом
 * scripts/build_pcode.py (см. pcode-source/kv-bulk.json + `wrangler kv
 * bulk put`, а также индекс pcode-source/kv-idx.json - см. ниже).
 *
 * Защита (порядок проверок):
 *  1. User-Agent: пустой или известный бот/библиотека -> 403.
 *  2. Источник: Origin или Referer должны вести на один из адресов
 *     РАЗРЕШЁННЫЕ_ИСТОЧНИКИ (сайт codetruck.ru и локальное приложение на
 *     localhost:8765 / 127.0.0.1:8765) -> иначе 403.
 *     Это отсекает простые скрипты. Браузер с сайта такие заголовки шлёт сам,
 *     но подделать их скрипту ничего не стоит - поэтому дальше ещё лимиты.
 *  3. Ввод: сначала нормализуется (пробелы, кириллические двойники, префиксы
 *     модулей, запятая как точка - см. planSearch), потом проверяется форма
 *     (буквы, цифры, дефис/слеш/точка по шаблонам). Марка только из
 *     KNOWN_PCODE_BRANDS -> иначе 400. Неверный ввод до лимитов не доходит и
 *     суточный счётчик не трогает.
 *  4. Лимит частоты по IP (CF-Connecting-IP) через привязку Workers Rate
 *     Limiting PCODE_RL: 20 запросов в минуту. Запрос без марки стоит 3
 *     единицы лимита (он проходит все таблицы сразу). Превышение -> 429.
 *  5. Лимит на сутки: каждый поиск (с маркой или без) - один. Считает Durable
 *     Object DailyLimit. Сайт без ключа - по IP, DAILY_LIMIT_PER_DAY в сутки
 *     (UTC). Приложение - по ключу (объект key:<ключ>), лимит из записи ключа
 *     (по умолчанию DAILY_LIMIT_PER_DAY). Превышение -> 429 с {error:
 *     'daily_limit', limit} и Retry-After до полуночи UTC. Почему не KV: у
 *     бесплатного KV всего 1 000 записей в сутки, на счётчик их уйдёт много.
 *  6. Ключ приложений (заголовок X-Codetruck-Key, формат ct_ + 24 символа):
 *     обязателен для всех разрешённых адресов, кроме сайта codetruck.ru.
 *     Запись в KV: apikey:<ключ> -> {имя, лимит, до, активен, создан}. Нет
 *     ключа -> 401 need_key; неверный или отключён -> 403 bad_key; срок прошёл
 *     -> 403 key_expired. При успехе - заголовок X-Remaining (поисков осталось
 *     сегодня). Ключи выдаёт worker/ключи.py.
 *
 * Поиск без марки идёт по индексу (ключи pcode:_idx:XX, см. shardKey): один
 * шард на вариант написания вместо чтения всех марок. Пока индекс не залит,
 * шарда нет - тогда работает запасной путь, перебор всех марок.
 *
 * Пакеты моделей КАМАЗ: GET /pack?model=<модель> с ключом (X-Codetruck-Key, для всех
 * источников, сайт тоже). Модель должна быть в записи ключа (поле "модели": одна модель,
 * или ["*"] для служебного). Лимит 20 пакетов в сутки на ключ. Пакет лежит в KV pack:<модель>,
 * на выдаче в него вшивается метка ключа (блок «Пакеты моделей» ниже).
 *
 * Все ответы: Cache-Control: no-store и X-Robots-Tag: noindex.
 */

// Держать в согласии с KNOWN_PCODE_BRANDS/top-level ключами
// pcode-source/pcode.json в scripts/build_pcode.py.
var KNOWN_PCODE_BRANDS = ['volvo', 'mercedes', 'scania', 'shacman', 'tata', 'ashokleyland', 'howo', 'faw', 'jac', 'international', 'powerstroke',
                          'cumminsisb', 'cumminsislisc', 'cumminsism', 'cumminsisx', 'paccarmx13', 'hino', 'renault', 'caterpillar',
                          'mahindra', 'deutz', 'fuso', 'thermoking', 'carrier',
                          'planar', 'webasto', 'eberspacher', 'daewoo', 'cumminsisf',
                          'eaton', 'hyundai', 'haldex', 'allison', 'weichai', 'volkswagen', 'mwm', 'isuzu', 'baw',
                          'ivecoedc', 'ivecoeurotronic', 'iveco', 'daf', 'manzbr2', 'manebs', 'man', 'mack', 'yamz', 'volvomid', 'jingwei', 'gaz'];
// Адреса, с которых пускаем запросы (Origin / Referer): сайт и локальное
// приложение «Каталог 3D». Точное совпадение, без слеша в конце. Чтобы добавить
// адрес выкладки приложения - дописать сюда и развернуть воркер.
var РАЗРЕШЁННЫЕ_ИСТОЧНИКИ = ['https://codetruck.ru', 'http://localhost:8765', 'http://127.0.0.1:8765'];
var ALLOWED_ORIGINS = РАЗРЕШЁННЫЕ_ИСТОЧНИКИ;
// Сайт: для него ключ не нужен (лимит по IP). Все остальные разрешённые адреса -
// приложения, им нужен ключ в заголовке X-Codetruck-Key.
var SITE_ORIGIN = 'https://codetruck.ru';
// Формат ключа: ct_ + 24 символа [a-z0-9] (генерирует worker/ключи.py).
var KEY_RE = /^ct_[a-z0-9]{24}$/;
// Запись ключа (KV apikey:<ключ>) кэшируется в памяти изолята на 60 с.
var KEY_CACHE_MS = 60000;
var keyCache = new Map(); // ключ -> { t: время проверки, rec: запись или null }

// Подстроки User-Agent (в нижнем регистре), по которым отсекаем ботов и библиотеки.
var BLOCKED_UA = ['curl', 'wget', 'python-requests', 'python-urllib', 'go-http-client', 'java', 'okhttp',
                  'scrapy', 'headlesschrome', 'phantomjs', 'gptbot', 'claudebot', 'claude-web', 'ccbot', 'bytespider',
                  'perplexitybot', 'amazonbot', 'dataforseobot', 'ahrefsbot', 'semrushbot', 'mj12bot'];

var LIMIT_PER_MINUTE = 20;
var COST_NO_BRAND = 3;       // запрос без марки проверяет все таблицы сразу
var DAILY_LIMIT_PER_DAY = 50; // поисков в сутки (UTC) с одного адреса
var MAX_CODE_LEN = 12;
// Буквы кириллицей - в двух кодах Mercedes (2E050Б, EE0A0З): так записаны в базе.
// Проверяем верхний регистр (см. handlePcode), поэтому строчные сюда не нужны.
var CODE_RE = /^[A-Z0-9\u0400-\u042F\u0401-]+$/;
// Дилерский код вида «100.1» (Deutz, Caterpillar, Daewoo, Iveco EDC): цифры,
// точка, цифры. Точка в прочих форматах не разрешена - P-коды, MID/PID,
// Volvo B000101 и пары SPN-FMI с дефисом проверяются по CODE_RE, как раньше.
var DOT_CODE_RE = /^[0-9]{1,7}\.[0-9]{1,2}$/;
// Код Volvo MID/PID из таблицы volvomid: M128-P100.1, M128-PP270.12 (1 407 ключей).
// Длина до 14 символов, поэтому проверяется по шаблону, а не по MAX_CODE_LEN.
var MID_CODE_RE = /^M[0-9]{1,3}-[PS]{1,2}[0-9]{1,4}\.[0-9]{1,2}$/;
// Код Volkswagen с косой чертой: 0027/04 (589 ключей). Дефисная форма 1045-02
// проходит CODE_RE.
var SLASH_CODE_RE = /^[0-9]{3,4}\/[0-9]{2}$/;

// Число шардов индекса без марки. Держать в согласии с SHARDS в
// scripts/build_pcode.py: там же строится pcode-source/kv-idx.json.
var INDEX_SHARDS = 64;

// Кириллические двойники латинских букв (верхний регистр). Держать в согласии с
// homoglyphs в scripts/build_pcode.py: ключи KV и индекс строятся тем же norm.
var CYR_HOMO = 'АВСЕНКМОРТХУ'; // А В С Е Н К М О Р Т Х У
var LAT_HOMO = 'ABCEHKMOPTXY';

function homoglyphs(s) {
  return s.replace(/[АВСЕНКМОРТХУ]/g,
                   function (ch) { return LAT_HOMO.charAt(CYR_HOMO.indexOf(ch)); });
}

/**
 * Нормализация ключа (и введённого кода без разделителей): пробелы убираем,
 * заглавные, кириллические двойники -> латиница, у «100.01» ведущие нули
 * дробной части убираем. Так же строится ключ KV в build_pcode.py (norm).
 */
function norm(code) {
  var c = homoglyphs(code.toUpperCase().replace(/\s+/g, ''));
  return DOT_CODE_RE.test(c) ? canonDot(c) : c;
}

/**
 * Очистка ввода: пробелы схлопнуть до одного, заглавные, кириллические
 * двойники -> латиница, запятая как точка («100,1» -> «100.1»).
 */
function cleanInput(raw) {
  var s = homoglyphs(String(raw).trim().replace(/\s+/g, ' ').toUpperCase());
  if (/^[0-9]{1,7},[0-9]{1,2}$/.test(s)) s = s.replace(',', '.');
  return s;
}

// Код, который может лежать в KV (проверка формы ввода). Длина считается без пробелов.
function shapeOk(form) {
  return (form.length <= MAX_CODE_LEN && CODE_RE.test(form)) ||
         DOT_CODE_RE.test(form) || MID_CODE_RE.test(form) || SLASH_CODE_RE.test(form);
}

// Префиксы, которые сканер или документация пишут перед номером.
// Модули Scania (acu.su): ключ - только номер, модуль отбрасывается.
var SCANIA_MODULE_RE = /^(EMS|BMS|GMS|COO|LAS|EEC|SMS|VIS|ICL|AHS|TCO|RET|APS|BWS|CCS)[ -]?([0-9]{1,6})$/;
// Cummins FC 415 -> 415: ищем во всех Cummins-таблицах.
var CUMMINS_FC_RE = /^FC[ -]?([0-9]{1,6})$/;
var CUMMINS_BRANDS = ['cumminsisb', 'cumminsisf', 'cumminsislisc', 'cumminsism', 'cumminsisx'];
// Отопители: Webasto F09 -> ключ «F09» (F-код таймера; F9 -> F09), Eberspächer E-05 -> ключ «005».
// Ключи «00»…«AB» у Webasto - служебные ПК-коды программы, это ДРУГОЙ смысл: F03 на них
// не откатываем (раньше F03 отдавал ПК-код 03). ПК-код ищется вводом без буквы: «03», «0A».
var WEBASTO_RE = /^F[ -]?([0-9]{1,2})$/;
var EBERSPACHER_DASH_RE = /^E[ -]([0-9]{2,3})$/;
// E05 без разделителя: сначала ключ Jingwei E05 (он существует), затем Eberspächer.
var EBERSPACHER_PLAIN_RE = /^E([0-9]{2})$/;

/**
 * Каноническая запись дилерского кода с точкой: ведущие нули дробной части
 * убираем («100.01» -> «100.1»), последняя цифра остаётся. В базе таких нулей
 * нет ни у одного кода (проверено по pcode.json), так что канон совпадает с
 * ключом KV. «100.0» и «100.00» дают «100.0».
 */
function canonDot(c) {
  var parts = c.split('.');
  return parts[0] + '.' + parts[1].replace(/^0+(?=[0-9])/, '');
}

/**
 * Варианты записи одного и того же номера для чисто цифровых дилерских кодов.
 *
 * Зачем. 2176 ключей в базе записаны с ведущими нулями до пяти знаков -
 * manebs 1380, man 372, manzbr2 221, mercedes 316, iveco 80, eberspacher 74 и
 * ещё по мелочи. Так их печатает заводская документация, так собраны наши
 * таблицы. Но сканеры и часть источников показывают тот же номер без нулей
 * («3051», «597»), и человек вводит ровно то, что видит на экране. Поиск идёт
 * по точному совпадению ключа, поэтому такой ввод не находил ничего.
 *
 * Что делаем. Для чисто цифрового ввода пробуем две записи: как ввели и
 * дополненную нулями до четырёх и до пяти знаков (Iveco «0111» при вводе «111»).
 * Точное совпадение выигрывает, дополнение -
 * запасной ход. Для всего остального (P-коды, семизначные UDS Volvo, коды с
 * дефисом) вариант ровно один, лишних чтений KV не появляется.
 *
 * ПОЧЕМУ ТОЛЬКО ДОПОЛНЕНИЕ, А НЕ ОБРАТНОЕ ПРЕОБРАЗОВАНИЕ. Раздевать ввод от
 * нулей («03051» -> «3051») технически так же просто, но это шумит: короткие
 * номера заняты сразу у нескольких марок (1, 2, 3 есть у planar, shacman,
 * thermoking, carrier), и запрос без выбранной марки начинал бы возвращать
 * пачку чужих ответов. По базе посчитано: одно дополнение добавляет лишние
 * марки 933 кодам, дополнение вместе с раздеванием - уже 1865. Раздевание
 * при этом никому не нужно: люди вводят то, что видят на экране, а на экране
 * короткая форма, не длинная.
 */
function codeVariants(code) {
  var c = norm(code);
  var out = [c];
  // До четырёх знаков: Iveco «0111» при вводе «111».
  if (/^\d{1,3}$/.test(c)) {
    var p4 = ('0000' + c).slice(-4);
    if (out.indexOf(p4) < 0) out.push(p4);
  }
  if (/^\d{1,4}$/.test(c)) {
    var padded = ('00000' + c).slice(-5);
    if (out.indexOf(padded) < 0) out.push(padded);
  }
  return out;
}

/**
 * Вторая очередь вариантов: короткий цифровой код дополняем нулями до двух и до
 * трёх знаков («1» -> «01», «001»; «0» -> «00», «000»; «34» -> «034»). В частях
 * «NN/NN» и «NN-NN» дополняем каждую часть: VW «27/04» -> «0027/04». Такие
 * варианты пробуются только тогда, когда основные ничего не дали (см. runSearch),
 * поэтому уже найденные коды не меняются.
 */
function padVariantsOf(c) {
  var out = [];
  var m;
  if (/^[0-9]{1,2}$/.test(c)) {
    if (c.length < 2) out.push(('00' + c).slice(-2));
    out.push(('000' + c).slice(-3));
    return out;
  }
  if ((m = /^([0-9]{1,4})([-\/])([0-9]{1,2})$/.exec(c))) {
    var aParts = [m[1]];
    for (var len = m[1].length + 1; len <= 4; len++) aParts.push(('0000' + m[1]).slice(-len));
    var bParts = [m[3]];
    if (m[3].length < 2) bParts.push(('00' + m[3]).slice(-2));
    var seps = [m[2], m[2] === '/' ? '-' : '/'];
    for (var s = 0; s < seps.length; s++) {
      for (var a = 0; a < aParts.length; a++) {
        for (var b = 0; b < bParts.length; b++) {
          var f = aParts[a] + seps[s] + bParts[b];
          if (f !== c && shapeOk(f) && out.indexOf(f) < 0) out.push(f);
        }
      }
    }
  }
  return out;
}

/**
 * Варианты записи введённого кода с разделителями. Ключи в базе пишутся по-разному:
 * VW «0027/04», MWM «P0105-01», Mercedes «MR 0101» (с пробелом), DAF «84-9».
 * Человек вводит то же самое своими словами: «0027-04», «0027 04», «MR-0101»,
 * «P0105 01». Берём введённую форму (пробелы убраны) и, если в ней был пробел,
 * его заменой на «-», «/», «.»; если разделитель есть - также форму без него и
 * с заменённым «-»/«/». Форма, не похожая на код, в список не попадает.
 */
function candidateForms(s) {
  var nospace = s.replace(/ /g, '');
  var forms = [];
  // «100 1», «1 32» - пара SPN/FMI (вторая группа 1-2 знака): слитно («1001») не
  // склеиваем, дало бы чужие коды. «10 004» (вторая группа 3+ знака) - номер Scania.
  if (!/[0-9] [0-9]{1,2}$/.test(s)) forms.push(nospace);
  if (s.indexOf(' ') >= 0) {
    forms.push(s.replace(/ /g, '-'), s.replace(/ /g, '/'), s.replace(/ /g, '.'));
  }
  if (/[-\/]/.test(nospace)) {
    // Дефис после букв («MR-0101», «P-0121») - разделитель, его убираем.
    // Между цифрами («84-9», «1-32») дефис - это SPN-FMI, его не трогаем.
    if (/^[A-Z]+[-\/][0-9]/.test(nospace)) {
      forms.push(nospace.replace(/^([A-Z]+)[-\/]/, '$1')); // P-0105-01 -> P0105-01
      forms.push(nospace.replace(/[-\/]/g, ''));           // P-0105-01 -> P010501 (прежняя форма)
    }
    forms.push(nospace.replace(/-/g, '/'), nospace.replace(/\//g, '-'));
  }
  var out = [];
  for (var i = 0; i < forms.length; i++) {
    if (shapeOk(forms[i]) && out.indexOf(forms[i]) < 0) out.push(forms[i]);
  }
  return out;
}

/**
 * Варианты для поиска: ввод (с его разделительными формами) через codeVariants.
 * Дубли отбрасываются, порядок сохраняется (точное совпадение первым).
 */
function searchForms(forms) {
  var out = [];
  for (var i = 0; i < forms.length; i++) {
    var vs = codeVariants(forms[i]);
    for (var j = 0; j < vs.length; j++) {
      if (out.indexOf(vs[j]) < 0) out.push(vs[j]);
    }
  }
  return out;
}

function pad3(digits) {
  return ('000' + digits).slice(-3);
}

/**
 * План поиска по вводу (raw - как пришёл с сайта, уже без лишних пробелов по краям).
 * Возвращает { forms, brands, fallback, pads } или null, если форма ввода не подходит.
 *  forms    - варианты ключа для поиска (по порядку);
 *  brands   - если задано, поиск только по этим маркам (префиксы модулей/FC/отопителей);
 *  fallback - запасной поиск {forms, brands}, если основной ничего не дал (только без марки);
 *  pads     - вторая очередь: дополнения нулями (см. padVariantsOf), если и она пуста.
 */
function planSearch(raw) {
  var s = cleanInput(raw);
  var m;
  if ((m = SCANIA_MODULE_RE.exec(s))) {
    return { forms: searchForms([m[2]]), brands: ['scania'], fallback: null, pads: [] };
  }
  if ((m = CUMMINS_FC_RE.exec(s))) {
    return { forms: searchForms([m[1]]), brands: CUMMINS_BRANDS, fallback: null, pads: [] };
  }
  if ((m = WEBASTO_RE.exec(s))) {
    // Ключ F + две цифры; без отката на hex-ключ и без дополнения нулями (pads пуст).
    return { forms: ['F' + ('0' + m[1]).slice(-2)], brands: ['webasto'], fallback: null, pads: [] };
  }
  if ((m = EBERSPACHER_DASH_RE.exec(s))) {
    // E-05: Eberspächer пишет 005, SITRAK (jingwei) - E05. Ищем обе формы в обеих марках.
    var dforms = [pad3(m[1])];
    if (m[1].length === 2) dforms.push('E' + m[1]);
    return { forms: searchForms(dforms), brands: ['eberspacher', 'jingwei'], fallback: null, pads: [] };
  }
  var cand = candidateForms(s);
  if (!cand.length) return null;
  var fallback = null;
  if ((m = EBERSPACHER_PLAIN_RE.exec(s))) {
    fallback = { forms: searchForms([pad3(m[1])]), brands: ['eberspacher'] };
  }
  var forms = searchForms(cand);
  var pads = [];
  for (var c = 0; c < cand.length; c++) {
    var pv = padVariantsOf(cand[c]);
    for (var q = 0; q < pv.length; q++) {
      if (forms.indexOf(pv[q]) < 0 && pads.indexOf(pv[q]) < 0) pads.push(pv[q]);
    }
  }
  return { forms: forms, brands: null, fallback: fallback, pads: pads };
}

function kvKey(brand, code) {
  return 'pcode:' + brand + ':' + norm(code);
}

// Блинк-алиас: номер мигающего кода -> список ключей марки (см. build_pcode.py).
function aliasKey(brand, form) {
  return 'pcode:_alias:' + brand + ':' + norm(form);
}

/**
 * Ключ шарда индекса для нормализованного кода: FNV-1a по UTF-8 байтам, mod
 * INDEX_SHARDS, две hex-цифры. Та же функция стоит в scripts/build_pcode.py
 * (shard_of) - менять только вместе, иначе индекс не найдёт ни одного кода.
 */
function shardKey(code) {
  var h = 0x811c9dc5;
  var bytes = new TextEncoder().encode(code);
  for (var i = 0; i < bytes.length; i++) {
    h = Math.imul(h ^ bytes[i], 0x01000193) >>> 0;
  }
  return 'pcode:_idx:' + (h % INDEX_SHARDS).toString(16).padStart(2, '0');
}

function pickText(entry, lang) {
  if (lang !== 'ru' && entry.en) return entry.en;
  return entry.ru;
}

// Заголовки, которые ставим на каждый ответ.
function baseHeaders() {
  return {
    'Cache-Control': 'no-store',
    'X-Robots-Tag': 'noindex',
  };
}

function corsHeaders(request) {
  var origin = request.headers.get('Origin');
  var headers = {
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Codetruck-Key',
    'Access-Control-Expose-Headers': 'X-Remaining, X-Plan',
    // Ответ зависит от Origin: кэш не должен отдать один источник другому.
    'Vary': 'Origin',
  };
  if (ALLOWED_ORIGINS.indexOf(origin) >= 0) headers['Access-Control-Allow-Origin'] = origin;
  return headers;
}

function json(request, status, body, extra) {
  var headers = Object.assign({ 'Content-Type': 'application/json; charset=utf-8' },
                              baseHeaders(), corsHeaders(request), extra || {});
  return new Response(JSON.stringify(body), { status: status, headers: headers });
}

// Календарный день по UTC в виде YYYY-MM-DD.
function utcDay() {
  return new Date().toISOString().slice(0, 10);
}

// Секунд до ближайшей полуночи UTC (не меньше 1).
function secondsToMidnightUtc() {
  var now = new Date();
  var next = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + 1);
  return Math.max(1, Math.ceil((next - now.getTime()) / 1000));
}

// Проверка User-Agent: пустой или из чёрного списка -> false.
function uaAllowed(request) {
  var ua = (request.headers.get('User-Agent') || '').trim().toLowerCase();
  if (!ua) return false;
  for (var i = 0; i < BLOCKED_UA.length; i++) {
    if (ua.indexOf(BLOCKED_UA[i]) >= 0) return false;
  }
  return true;
}

// Источник запроса (один из ALLOWED_ORIGINS) по Origin или по Referer, иначе null.
function sourceOf(request) {
  var origin = request.headers.get('Origin');
  if (origin) return ALLOWED_ORIGINS.indexOf(origin) >= 0 ? origin : null;
  var referer = request.headers.get('Referer') || '';
  for (var i = 0; i < ALLOWED_ORIGINS.length; i++) {
    var o = ALLOWED_ORIGINS[i];
    if (referer === o || referer.indexOf(o + '/') === 0) return o;
  }
  return null;
}

/**
 * Проверка ключа приложения. Возвращает { rec } для верного ключа или
 * { error, status } для отказа. Запись читается из KV (apikey:<ключ>) и
 * кэшируется в памяти изолята на KEY_CACHE_MS. Ошибку чтения KV не глотаем:
 * она уходит наверх и даёт 503.
 */
async function checkKey(env, key) {
  if (!KEY_RE.test(key)) return { error: 'bad_key', status: 403 };
  var now = Date.now();
  var c = keyCache.get(key);
  var rec;
  if (c && now - c.t < KEY_CACHE_MS) {
    rec = c.rec;
  } else {
    var raw = await env.PCODE_KV.get('apikey:' + key);
    rec = null;
    if (raw) {
      try { rec = JSON.parse(raw); } catch (e) { rec = null; }
    }
    keyCache.set(key, { t: now, rec: rec });
  }
  if (!rec || rec['активен'] === false) return { error: 'bad_key', status: 403 };
  if (rec['до'] && rec['до'] < utcDay()) return { error: 'key_expired', status: 403 };
  var lim = parseInt(rec['лимит'], 10);
  if (!(lim > 0)) lim = DAILY_LIMIT_PER_DAY;
  // Тариф: 'демо' (рекламный) или 'платный' (по умолчанию). Пока на поиск не влияет.
  var plan = rec['тариф'] === 'демо' ? 'demo' : 'platnyi';
  return { rec: rec, limit: lim, plan: plan };
}

/**
 * Поиск без марки по индексу. Читаем шард для каждого варианта написания и
 * берём только те марки, которые в нём есть (обычно 1-3), затем по одному
 * чтению на марку - за текстом. Для варианта, которого нет ни в одной марке,
 * чтение не делаем вовсе.
 *
 * Возвращает null, если шарда нет (индекс ещё не залит) - тогда вызывающий
 * идёт запасным путём. Пустой шард - это настоящий ответ «ничего нет».
 */
async function searchByIndex(env, variants, lang) {
  // Записи шарда: «марка» - прямой ключ; «марка>ключ» - блинк-алиас (см. build_pcode.py).
  var direct = Object.create(null); // марка -> ключ (первый вариант написания по порядку)
  var alias = Object.create(null);  // марка -> [ключи, на которые указывает блинк]
  for (var v = 0; v < variants.length; v++) {
    var code = variants[v];
    var raw = await env.PCODE_KV.get(shardKey(code));
    if (raw === null) return null;
    var shard = JSON.parse(raw);
    if (!Object.prototype.hasOwnProperty.call(shard, code)) continue;
    var list = shard[code];
    for (var j = 0; j < list.length; j++) {
      var item = list[j];
      var gt = item.indexOf('>');
      if (gt < 0) {
        if (!(item in direct)) direct[item] = code;
      } else {
        var ab = item.slice(0, gt);
        (alias[ab] = alias[ab] || []).push(item.slice(gt + 1));
      }
    }
  }

  // Блинк-алиас учитываем, только если у марки нет прямого ключа на этот номер.
  var pairs = [];
  Object.keys(direct).forEach(function (b) { pairs.push([b, direct[b]]); });
  Object.keys(alias).forEach(function (b) {
    if (b in direct) return;
    alias[b].forEach(function (k) { pairs.push([b, k]); });
  });
  pairs.sort(function (x, y) {
    var d = KNOWN_PCODE_BRANDS.indexOf(x[0]) - KNOWN_PCODE_BRANDS.indexOf(y[0]);
    if (d !== 0) return d;
    return x[1] < y[1] ? -1 : (x[1] > y[1] ? 1 : 0);
  });
  // Один ключ мог прийти с двух вариантов написания (21 и 2-1): оставляем один.
  pairs = pairs.filter(function (p, i) {
    return i === 0 || p[0] !== pairs[i - 1][0] || p[1] !== pairs[i - 1][1];
  });

  var results = await Promise.all(pairs.map(async function (p) {
    var raw2 = await env.PCODE_KV.get(kvKey(p[0], p[1]));
    if (!raw2) return null;
    return { brand: p[0], code: p[1], text: pickText(JSON.parse(raw2), lang) };
  }));
  return results.filter(Boolean);
}

/**
 * Запасной путь: перебор таблиц марок. Нужен, пока индекс не залит, и для
 * поиска с выбранной маркой (там индекс не нужен - одна марка).
 */
async function searchBruteForce(env, brands, variants, lang) {
  var per = await Promise.all(brands.map(async function (b) {
    // Прямой ключ важнее блинк-алиаса; внутри марки первый вариант написания.
    for (var i = 0; i < variants.length; i++) {
      var raw = await env.PCODE_KV.get(kvKey(b, variants[i]));
      if (raw) {
        var entry = JSON.parse(raw);
        return [{ brand: b, code: variants[i], text: pickText(entry, lang) }];
      }
    }
    for (var a = 0; a < variants.length; a++) {
      var araw = await env.PCODE_KV.get(aliasKey(b, variants[a]));
      if (!araw) continue;
      var targets = JSON.parse(araw);
      var hits = await Promise.all(targets.map(async function (t) {
        var traw = await env.PCODE_KV.get(kvKey(b, t));
        if (!traw) return null;
        return { brand: b, code: t, text: pickText(JSON.parse(traw), lang) };
      }));
      return hits.filter(Boolean);
    }
    return [];
  }));
  return [].concat.apply([], per);
}

/**
 * Поиск по плану planSearch. Явная марка - только её таблица. Префикс (модули
 * Scania, FC, отопители) - только таблицы его марок. Без марки и без префикса -
 * индекс; если индекс не залит - перебор всех марок. Запасной ход (E05 -> Eberspächer)
 * только если без марки ничего не нашлось.
 */
async function runSearch(env, plan, brand, lang) {
  var fb = plan.fallback;
  var pads = plan.pads || [];
  if (brand) {
    var own = await searchBruteForce(env, [brand], plan.forms, lang);
    if (own.length === 0 && fb && fb.brands.indexOf(brand) >= 0) {
      own = await searchBruteForce(env, [brand], fb.forms, lang);
    }
    if (own.length === 0 && pads.length) own = await searchBruteForce(env, [brand], pads, lang);
    return own;
  }
  if (plan.brands) {
    var pb = await searchBruteForce(env, plan.brands, plan.forms, lang);
    if (pb.length === 0 && pads.length) pb = await searchBruteForce(env, plan.brands, pads, lang);
    return pb;
  }
  var hits = await searchByIndex(env, plan.forms, lang);
  if (hits === null) hits = await searchBruteForce(env, KNOWN_PCODE_BRANDS, plan.forms, lang);
  if (hits.length === 0 && fb) {
    hits = await searchBruteForce(env, fb.brands, fb.forms, lang);
  }
  if (hits.length === 0 && pads.length) {
    var ph = await searchByIndex(env, pads, lang);
    hits = ph === null ? await searchBruteForce(env, KNOWN_PCODE_BRANDS, pads, lang) : ph;
  }
  return hits;
}

/**
 * who - кто платит за поиск: { daily: имя объекта DailyLimit, limit: лимит в
 * сутки }. Для сайта без ключа это IP и DAILY_LIMIT_PER_DAY, для приложения -
 * ключ (key:<ключ>) и лимит из его записи.
 */
async function handlePcode(request, env, url, who) {
  var code = (url.searchParams.get('code') || '').trim();
  var lang = url.searchParams.get('lang') || 'ru';
  var brand = url.searchParams.get('brand') || '';

  if (!code) return json(request, 400, { error: 'missing_code' });
  // Сначала нормализуем ввод (пробелы, кириллица, префиксы), потом проверяем форму.
  // Неверный ввод отвечает 400 {error:'bad_code'} до лимитов.
  var plan = code.length <= 40 ? planSearch(code) : null;
  if (!plan) {
    return json(request, 400, { error: 'bad_code' });
  }
  if (brand && KNOWN_PCODE_BRANDS.indexOf(brand) < 0) {
    return json(request, 400, { error: 'unknown_brand' });
  }

  // Лимит по IP. Без марки запрос тяжелее: он проходит все таблицы.
  var ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  var cost = brand ? 1 : COST_NO_BRAND;
  var limited = false;
  if (env.PCODE_RL) {
    for (var k = 0; k < cost; k++) {
      var rl = await env.PCODE_RL.limit({ key: ip });
      if (!rl.success) { limited = true; break; }
    }
  }
  if (limited) {
    return json(request, 429, { error: 'rate_limited' }, { 'Retry-After': '60' });
  }

  // Лимит на сутки: каждый поиск, прошедший проверки выше, - один.
  // Если объект лимита недоступен, поиск не отдаём (лимит - защита).
  var remaining = null;
  if (env.DAILY_LIMIT) {
    var verdict;
    try {
      var stub = env.DAILY_LIMIT.get(env.DAILY_LIMIT.idFromName(who.daily));
      var resp = await stub.fetch('https://daily-limit/take?day=' + utcDay() +
                                  '&limit=' + who.limit);
      verdict = await resp.json();
    } catch (e) {
      return json(request, 503, { error: 'limit_unavailable' });
    }
    if (!verdict.allowed) {
      return json(request, 429, { error: 'daily_limit', limit: who.limit },
                  { 'Retry-After': String(secondsToMidnightUtc()) });
    }
    remaining = Math.max(0, who.limit - verdict.count);
  }

  var hits = null;
  try {
    hits = await runSearch(env, plan, brand, lang);
  } catch (e) {
    return json(request, 502, { error: 'kv_unavailable' });
  }

  var extra = {};
  if (remaining !== null) extra['X-Remaining'] = String(remaining);
  if (who.plan) extra['X-Plan'] = who.plan;
  return json(request, 200, { hits: hits }, extra);
}

/**
 * Счётчик поисков одного адреса за сутки. Один объект на адрес (idFromName),
 * хранилище SQLite: одна строка на день. Весь метод синхронный (без await),
 * поэтому проверка и увеличение счётчика выполняются атомарно даже при
 * параллельных запросах с одного адреса.
 */
export class DailyLimit {
  constructor(state) {
    this.sql = state.storage.sql;
    this.sql.exec('CREATE TABLE IF NOT EXISTS daily (day TEXT PRIMARY KEY, n INTEGER NOT NULL)');
  }

  fetch(request) {
    var url = new URL(request.url);
    var day = url.searchParams.get('day') || '';
    var limit = parseInt(url.searchParams.get('limit'), 10);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(day) || !(limit > 0)) {
      return new Response('bad_request', { status: 400 });
    }
    // Прошедшие сутки не нужны: держим одну строку - за текущий день.
    this.sql.exec('DELETE FROM daily WHERE day < ?', day);
    var row = this.sql.exec('SELECT n FROM daily WHERE day = ?', day).toArray()[0];
    var n = row ? row.n : 0;
    if (n >= limit) {
      return new Response(JSON.stringify({ allowed: false, count: n }),
                          { headers: { 'Content-Type': 'application/json' } });
    }
    this.sql.exec('INSERT INTO daily (day, n) VALUES (?, 1) ON CONFLICT(day) DO UPDATE SET n = n + 1', day);
    return new Response(JSON.stringify({ allowed: true, count: n + 1 }),
                        { headers: { 'Content-Type': 'application/json' } });
  }
}

// ---- Пакеты моделей (/pack) ----
// Пакет - данные одной модели (каталог, предохранители, щиток, ТО), лежит в KV pack:<модель>.
// Выдаётся только по ключу, где модель есть (поле "модели"). Каждая выдача несёт метку ключа:
//  - верхнее поле "_выдано": {"м": модель, "к": первые 12 hex SHA-256 от ключа, "д": дата UTC};
//  - скрытая метка: 8 единиц из "единицы" (выбраны по хешу ключа) получают в конце названия "т"
//    по четыре невидимых символа (U+200B = 0, U+200C = 1): 32 бита отпечатка ключа.
var MODEL_RE = /^[A-Za-z0-9]{1,16}$/;
var PACK_LIMIT_PER_DAY = 20;
var PACK_CACHE_S = 300;   // чтение пакета из KV кэшируется на 5 минут
var PACK_MARK_UNITS = 8;  // единиц с меткой (по 4 бита)
var ZW0 = '​';
var ZW1 = '‌';

function modelsOf(rec) {
  var m = rec ? rec['модели'] : null;
  return Array.isArray(m) ? m : [];
}

async function keyHash(key) {
  var buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(key));
  return new Uint8Array(buf);
}

function hexOf(bytes, n) {
  var s = '';
  for (var i = 0; i < n; i++) s += bytes[i].toString(16).padStart(2, '0');
  return s;
}

// 32 бита отпечатка: первые 4 байта хеша.
function fingerprint32(hash) {
  return ((hash[0] << 24) | (hash[1] << 16) | (hash[2] << 8) | hash[3]) >>> 0;
}

// Номера единиц с меткой, по возрастанию, выбраны по хешу (ЛКГ от байтов 4..7).
// null, если подходящих единиц меньше восьми: тогда только поле _выдано.
function pickMarkUnits(hash, units) {
  var eligible = [];
  for (var i = 0; i < units.length; i++) {
    if (units[i] && typeof units[i]['т'] === 'string') eligible.push(i);
  }
  if (eligible.length < PACK_MARK_UNITS) return null;
  var seed = ((hash[4] << 24) | (hash[5] << 16) | (hash[6] << 8) | hash[7]) >>> 0;
  var chosen = [];
  while (chosen.length < PACK_MARK_UNITS) {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    var idx = eligible[seed % eligible.length];
    if (chosen.indexOf(idx) < 0) chosen.push(idx);
  }
  return chosen.sort(function (a, b) { return a - b; });
}

function nibbleMark(n) {
  var s = '';
  for (var b = 3; b >= 0; b--) s += ((n >> b) & 1) ? ZW1 : ZW0;
  return s;
}

function stampUnits(pack, hash) {
  var units = pack['единицы'];
  if (!Array.isArray(units)) return;
  var idxs = pickMarkUnits(hash, units);
  if (!idxs) return;
  var fp = fingerprint32(hash);
  for (var j = 0; j < PACK_MARK_UNITS; j++) {
    var u = units[idxs[j]];
    u['т'] = u['т'] + nibbleMark((fp >>> (28 - 4 * j)) & 0xF);
  }
}

// Метка пакета: поле _выдано и скрытые биты (8 hex, или null, если меток меньше восьми).
export function извлечьМетку(пакет) {
  var выдано = (пакет && пакет['_выдано']) || null;
  var units = (пакет && Array.isArray(пакет['единицы'])) ? пакет['единицы'] : [];
  var tails = [];
  for (var i = 0; i < units.length; i++) {
    var t = units[i] && units[i]['т'];
    if (typeof t !== 'string' || t.length < 4) continue;
    var tail = t.slice(-4);
    if (/^[​‌]{4}$/.test(tail)) tails.push(tail);
  }
  var скрыто = null;
  if (tails.length >= PACK_MARK_UNITS) {
    var v = 0;
    for (var j = 0; j < PACK_MARK_UNITS; j++) {
      var n = 0;
      for (var c = 0; c < 4; c++) n = (n << 1) | (tails[j].charAt(c) === ZW1 ? 1 : 0);
      v = (v << 4) | n;
    }
    скрыто = (v >>> 0).toString(16).padStart(8, '0');
  }
  return { выдано: выдано, скрыто: скрыто, помечено: tails.length };
}

// Пакет из KV с меткой ключа.
async function stampPack(raw, model, key) {
  var pack = JSON.parse(raw);
  var hash = await keyHash(key);
  pack['_выдано'] = { 'м': model, 'к': hexOf(hash, 6), 'д': utcDay() };
  stampUnits(pack, hash);
  return JSON.stringify(pack);
}

/**
 * Выдача пакета. check - результат checkKey (ключ верный). Порядок ответов:
 * bad_model 400 -> model_not_in_key 403 -> лимит IP -> no_pack 404 -> pack_limit 429 -> 200.
 * Счётчик pack:<ключ> растёт только при выдаче (404 и ошибки ввода его не трогают).
 */
async function handlePack(request, env, url, key, check) {
  var model = (url.searchParams.get('model') || '').trim();
  if (!MODEL_RE.test(model)) return json(request, 400, { error: 'bad_model' });
  var models = modelsOf(check.rec);
  if (models.indexOf('*') < 0 && models.indexOf(model) < 0) {
    return json(request, 403, { error: 'model_not_in_key' });
  }
  var ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  if (env.PCODE_RL) {
    var rl = await env.PCODE_RL.limit({ key: ip });
    if (!rl.success) return json(request, 429, { error: 'rate_limited' }, { 'Retry-After': '60' });
  }
  var raw;
  try {
    raw = await env.PCODE_KV.get('pack:' + model, { cacheTtl: PACK_CACHE_S });
  } catch (e) {
    return json(request, 503, { error: 'kv_unavailable' });
  }
  if (raw === null || raw === undefined) return json(request, 404, { error: 'no_pack' });
  // Лимит пакетов в сутки. Без объекта лимита пакет не отдаём (лимит - защита).
  if (!env.DAILY_LIMIT) return json(request, 503, { error: 'limit_unavailable' });
  var verdict;
  try {
    var stub = env.DAILY_LIMIT.get(env.DAILY_LIMIT.idFromName('pack:' + key));
    var resp = await stub.fetch('https://daily-limit/take?day=' + utcDay() +
                                '&limit=' + PACK_LIMIT_PER_DAY);
    verdict = await resp.json();
  } catch (e) {
    return json(request, 503, { error: 'limit_unavailable' });
  }
  if (!verdict.allowed) {
    return json(request, 429, { error: 'pack_limit', limit: PACK_LIMIT_PER_DAY },
                { 'Retry-After': String(secondsToMidnightUtc()) });
  }
  var body;
  try {
    body = await stampPack(raw, model, key);
  } catch (e) {
    return json(request, 502, { error: 'bad_pack' });
  }
  var headers = Object.assign({ 'Content-Type': 'application/json; charset=utf-8' },
                              baseHeaders(), corsHeaders(request), { 'X-Plan': check.plan });
  return new Response(body, { status: 200, headers: headers });
}

export default {
  async fetch(request, env) {
    var url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: Object.assign(baseHeaders(), corsHeaders(request)) });
    }
    if (request.method !== 'GET') {
      return json(request, 405, { error: 'method_not_allowed' });
    }
    if (url.pathname !== '/pcode' && url.pathname !== '/pack') {
      return json(request, 404, { error: 'not_found' });
    }
    var src = sourceOf(request);
    if (!uaAllowed(request) || src === null) {
      return json(request, 403, { error: 'forbidden' });
    }

    // Ключ. Сайт работает без него (по IP). Приложения - только с ключом.
    // Если сайт прислал ключ, он проверяется так же, как у приложения.
    var key = (request.headers.get('X-Codetruck-Key') || '').trim();
    if (url.pathname === '/pack') {
      if (!key) return json(request, 401, { error: 'need_key' });
      var pcheck;
      try {
        pcheck = await checkKey(env, key);
      } catch (e) {
        return json(request, 503, { error: 'kv_unavailable' });
      }
      if (pcheck.error) return json(request, pcheck.status, { error: pcheck.error });
      return handlePack(request, env, url, key, pcheck);
    }
    var who;
    if (!key && src === SITE_ORIGIN) {
      who = { daily: request.headers.get('CF-Connecting-IP') || 'unknown', limit: DAILY_LIMIT_PER_DAY };
    } else {
      if (!key) return json(request, 401, { error: 'need_key' });
      var check;
      try {
        check = await checkKey(env, key);
      } catch (e) {
        return json(request, 503, { error: 'kv_unavailable' });
      }
      if (check.error) return json(request, check.status, { error: check.error });
      who = { daily: 'key:' + key, limit: check.limit, plan: check.plan };
    }
    return handlePcode(request, env, url, who);
  },
};
