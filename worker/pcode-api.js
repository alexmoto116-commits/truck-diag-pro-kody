/**
 * codetruck.ru — API дилерских кодов (Volvo/Mercedes/Scania).
 *
 * Отдаёт по одному коду за раз вместо публикации всей таблицы целиком в
 * assets/dtc.enc.js / dtc.en.js. Данные заливаются в PCODE_KV скриптом
 * scripts/build_pcode.py (см. pcode-source/kv-bulk.json + `wrangler kv
 * bulk put`).
 *
 * ВАЖНО про CORS ниже: это мягкий барьер, не защита. Он не пускает чужой
 * сайт читать ответ из браузера пользователя, но никак не мешает curl,
 * скрипту или человеку в дев-тулзах — они Origin не проверяют и не
 * ограничены им. Настоящая защита от массового скрейпинга — это
 * авторизация или rate limiting, которых здесь пока нет.
 */

// Держать в согласии с KNOWN_PCODE_BRANDS/top-level ключами
// pcode-source/pcode.json в scripts/build_pcode.py.
var KNOWN_PCODE_BRANDS = ['volvo', 'mercedes', 'scania', 'shacman', 'tata', 'ashokleyland', 'howo', 'faw', 'jac', 'international', 'powerstroke',
                          'cumminsisb', 'cumminsislisc', 'cumminsism', 'cumminsisx', 'paccarmx13', 'hino', 'renault', 'caterpillar',
                          'mahindra', 'deutz', 'fuso', 'thermoking', 'carrier',
                          'planar', 'webasto', 'eberspacher', 'daewoo', 'cumminsisf',
                          'eaton', 'hyundai', 'haldex', 'allison', 'weichai', 'volkswagen', 'mwm', 'isuzu', 'baw',
                          'ivecoedc', 'ivecoeurotronic', 'iveco', 'daf', 'manzbr2', 'manebs', 'man', 'mack', 'yamz'];
var ALLOWED_ORIGINS = ['https://codetruck.ru'];

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

function corsHeaders(request) {
  var origin = request.headers.get('Origin');
  var headers = {
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
  if (ALLOWED_ORIGINS.indexOf(origin) >= 0) headers['Access-Control-Allow-Origin'] = origin;
  return headers;
}

function json(request, status, body) {
  return new Response(JSON.stringify(body), {
    status: status,
    headers: Object.assign({ 'Content-Type': 'application/json; charset=utf-8' }, corsHeaders(request)),
  });
}

async function handlePcode(request, env, url) {
  var code = url.searchParams.get('code');
  var lang = url.searchParams.get('lang') || 'ru';
  var brand = url.searchParams.get('brand') || '';

  if (!code) return json(request, 400, { error: 'missing_code' });

  var brandsToCheck = brand ? [brand].filter(function (b) { return KNOWN_PCODE_BRANDS.indexOf(b) >= 0; }) : KNOWN_PCODE_BRANDS;

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
      return new Response(null, { status: 204, headers: corsHeaders(request) });
    }
    if (request.method !== 'GET') {
      return json(request, 405, { error: 'method_not_allowed' });
    }
    if (url.pathname !== '/pcode') {
      return json(request, 404, { error: 'not_found' });
    }
    return handlePcode(request, env, url);
  },
};
