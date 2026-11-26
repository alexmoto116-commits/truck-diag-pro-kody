#!/usr/bin/env node
'use strict';
// Regression guard for URLSearchParams-based restoration of shared searches.
// Does not load site data or contact Cloudflare.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const src = fs.readFileSync(path.join(__dirname, '..', 'assets', 'app.js'), 'utf8');
const expected = "input.value = new URLSearchParams(location.search).get('q') || '';";
assert(src.includes(expected), 'Search query restore must use URLSearchParams');
assert(!src.includes("decodeURIComponent(qq[1].replace(/\\+/g, ' '))"),
  'Fragile raw decodeURIComponent search restoration returned');
const inputs = [
  ['?q=SPN+100+FMI+1', 'SPN 100 FMI 1'],
  ['?q=SPN%20100%20FMI%201', 'SPN 100 FMI 1'],
  ['?b=man&q=P0105-01&mid=128', 'P0105-01'],
  ['?q=%D0%9E%D1%88%D0%B8%D0%B1%D0%BA%D0%B0', 'Ошибка'],
  ['?q=100%25+FMI+1', '100% FMI 1'],
  ['?q=bad%ZZ+input', 'bad%ZZ input'],
  ['?q=%E0%A4%A', '\uFFFD%A'],
  ['?q=', '']
];
for (const [query, want] of inputs) {
  const actual = new URLSearchParams(query).get('q') || '';
  assert.equal(actual, want, query);
}
console.log('PASS: shared search recovery handles normal and malformed URL encoding');
