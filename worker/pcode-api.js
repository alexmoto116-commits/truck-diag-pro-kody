/**
 * codetruck.ru — API дилерских кодов (Volvo/Mercedes/Scania и др.).
 *
 * Отдаёт по одному коду за раз вместо публикации всей таблицы целиком в
 * assets/dtc.enc.js / dtc.en.js. Данные заливаются в PCODE_KV скриптом
 * scripts/build_pcode.py (см. pcode-source/kv-bulk.json + `wrangler kv
 * bulk put`).
 *
 * Защита (порядок проверок):
 *  1. User-Agent: пустой или известный бот/библиотека -> 403.
 *  2. Источник: Origin или Referer должны вести на https://codetruck.ru -> 403.
 *     Это отсекает простые скрипты. Браузер с сайта такие заголовки шлёт сам,
 *     но подделать их скрипту ничего не стоит - поэтому дальше ещё лимит.
 *  3. Ввод: длина кода <= 12, допустимые символы, марка только из
 *     KNOWN_PCODE_BRANDS -> иначе 400.
 *  4. Лимит частоты по IP (CF-Connecting-IP) через привязку Workers Rate
 *     Limiting PCODE_RL: 20 запросов в минуту. Запрос без марки стоит 3
 *     единицы лимита (он проходит все таблицы сразу). Превышение -> 429.
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
var ALLOWED_ORIGINS = ['https://codetruck.ru'];

// Подстроки User-Agent (в нижнем регистре), по которым отсекаем ботов и библиотеки.
var BLOCKED_UA = ['curl', 'wget', 'python-requests', 'python-urllib', 'go-http-client', 'java', 'okhttp',
                  'scrapy', 'headlesschrome', 'phantomjs', 'gptbot', 'claudebot', 'claude-web', 'ccbot', 'bytespider',
                  'perplexitybot', 'amazonbot', 'dataforseobot', 'ahrefsbot', 'semrushbot', 'mj12bot'];

var LIMIT_PER_MINUTE = 20;
var COST_NO_BRAND = 3;       // запрос без марки проверяет все таблицы сразу
var MAX_CODE_LEN = 12;
var CODE_RE = /^[A-Za-z0-9-]+$/;

function norm(code) {
  return code.toUpperCase().replace(/\s+/g, '');
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
    'Access-Control-Allow-Headers': 'Content-Type',
  };
  if (ALLOWED_ORIGINS.indexOf(origin) >= 0) headers['Access-Control-Allow-Origin'] = origin;
  return headers;
}

function json(request, status, body, extra) {
  var headers = Object.assign({ 'Content-Type': 'application/json; charset=utf-8' },
                              baseHeaders(), corsHeaders(request), extra || {});
  return new Response(JSON.stringify(body), { status: status, headers: headers });
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

// Запрос пришёл с сайта codetruck.ru: по Origin или по Referer.
function sourceAllowed(request) {
  var origin = request.headers.get('Origin');
  if (origin) return ALLOWED_ORIGINS.indexOf(origin) >= 0;
  var referer = request.headers.get('Referer') || '';
  return referer === 'https://codetruck.ru' || referer.indexOf('https://codetruck.ru/') === 0;
}

async function handlePcode(request, env, url) {
  var code = (url.searchParams.get('code') || '').trim();
  var lang = url.searchParams.get('lang') || 'ru';
  var brand = url.searchParams.get('brand') || '';

  if (!code) return json(request, 400, { error: 'missing_code' });
  if (code.length > MAX_CODE_LEN || !CODE_RE.test(code)) {
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

  var brandsToCheck = brand ? [brand] : KNOWN_PCODE_BRANDS;
  var variants = codeVariants(code);

  var results;
  try {
    results = await Promise.all(brandsToCheck.map(async function (b) {
      for (var i = 0; i < variants.length; i++) {
        var raw = await env.PCODE_KV.get(kvKey(b, variants[i]));
        if (raw) {
          var entry = JSON.parse(raw);
          return { brand: b, code: variants[i], text: pickText(entry, lang) };
        }
      }
      return null;
    }));
  } catch (e) {
    return json(request, 502, { error: 'kv_unavailable' });
  }

  return json(request, 200, { hits: results.filter(Boolean) });
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
    if (!uaAllowed(request) || !sourceAllowed(request)) {
      return json(request, 403, { error: 'forbidden' });
    }
    return handlePcode(request, env, url);
  },
};
