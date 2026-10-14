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
 *  3. Ввод: длина кода <= 12, допустимые символы (буквы, цифры, дефис, либо
 *     вид «100.1» с точкой), марка только из KNOWN_PCODE_BRANDS -> иначе 400.
 *     Неверный ввод до лимитов не доходит и суточный счётчик не трогает.
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

function norm(code) {
  var c = code.toUpperCase().replace(/\s+/g, '');
  return DOT_CODE_RE.test(c) ? canonDot(c) : c;
}

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
 * дополненную нулями до пяти знаков. Точное совпадение выигрывает, дополнение -
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
  if (/^\d{1,4}$/.test(c)) {
    var padded = ('00000' + c).slice(-5);
    if (out.indexOf(padded) < 0) out.push(padded);
  }
  return out;
}

function kvKey(brand, code) {
  return 'pcode:' + brand + ':' + norm(code);
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
  var found = Object.create(null); // марка -> вариант написания (приоритет по порядку)
  for (var v = 0; v < variants.length; v++) {
    var code = variants[v];
    var raw = await env.PCODE_KV.get(shardKey(code));
    if (raw === null) return null;
    var shard = JSON.parse(raw);
    if (!Object.prototype.hasOwnProperty.call(shard, code)) continue;
    var list = shard[code];
    for (var j = 0; j < list.length; j++) {
      if (!(list[j] in found)) found[list[j]] = code;
    }
  }

  var brands = Object.keys(found).sort(function (a, b) {
    return KNOWN_PCODE_BRANDS.indexOf(a) - KNOWN_PCODE_BRANDS.indexOf(b);
  });
  var results = await Promise.all(brands.map(async function (b) {
    var raw2 = await env.PCODE_KV.get(kvKey(b, found[b]));
    if (!raw2) return null;
    return { brand: b, code: found[b], text: pickText(JSON.parse(raw2), lang) };
  }));
  return results.filter(Boolean);
}

/**
 * Запасной путь: перебор таблиц марок. Нужен, пока индекс не залит, и для
 * поиска с выбранной маркой (там индекс не нужен - одна марка).
 */
async function searchBruteForce(env, brands, variants, lang) {
  var results = await Promise.all(brands.map(async function (b) {
    for (var i = 0; i < variants.length; i++) {
      var raw = await env.PCODE_KV.get(kvKey(b, variants[i]));
      if (raw) {
        var entry = JSON.parse(raw);
        return { brand: b, code: variants[i], text: pickText(entry, lang) };
      }
    }
    return null;
  }));
  return results.filter(Boolean);
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
  var up = code.toUpperCase();
  var shapeOk = (code.length <= MAX_CODE_LEN && CODE_RE.test(up)) ||
                DOT_CODE_RE.test(up) || MID_CODE_RE.test(up) || SLASH_CODE_RE.test(up);
  if (!shapeOk) {
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

  var variants = codeVariants(code);
  var hits = null;
  try {
    if (!brand) hits = await searchByIndex(env, variants, lang);
    if (hits === null) {
      hits = await searchBruteForce(env, brand ? [brand] : KNOWN_PCODE_BRANDS, variants, lang);
    }
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

export default {
  async fetch(request, env) {
    var url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: Object.assign(baseHeaders(), corsHeaders(request)) });
    }
    if (request.method !== 'GET') {
      return json(request, 405, { error: 'method_not_allowed' });
    }
    if (url.pathname !== '/pcode') {
      return json(request, 404, { error: 'not_found' });
    }
    var src = sourceOf(request);
    if (!uaAllowed(request) || src === null) {
      return json(request, 403, { error: 'forbidden' });
    }

    // Ключ. Сайт работает без него (по IP). Приложения - только с ключом.
    // Если сайт прислал ключ, он проверяется так же, как у приложения.
    var key = (request.headers.get('X-Codetruck-Key') || '').trim();
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
