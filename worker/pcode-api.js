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
                          'eaton', 'hyundai', 'haldex', 'allison', 'weichai', 'kenworth', 'volkswagen'];
var ALLOWED_ORIGINS = ['https://codetruck.ru'];

function norm(code) {
  return code.toUpperCase().replace(/\s+/g, '');
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

  var results;
  try {
    results = await Promise.all(brandsToCheck.map(async function (b) {
      var raw = await env.PCODE_KV.get(kvKey(b, code));
      if (!raw) return null;
      var entry = JSON.parse(raw);
      return { brand: b, text: pickText(entry, lang) };
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
