#!/usr/bin/env node
'use strict';
// Exercise the existing legacy-language 404 script without browser dependencies.
// Never connects to the network or touches private Cloudflare KV data.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const html = fs.readFileSync(path.join(__dirname, '..', '404.html'), 'utf8');
const anchor = '/* Old translated paths are retired:';
const start = html.indexOf(anchor);
assert(start >= 0, 'Legacy language notice script missing');
const end = html.indexOf('</script>', start);
assert(end > start, 'Legacy language notice script not terminated');
const code = html.slice(start, end);

function element(tag) {
  return {
    tag, children: [], style: {}, attrs: {},
    setAttribute(k, v) { this.attrs[k] = v; },
    appendChild(child) { this.children.push(child); return child; }
  };
}
function descendants(node, tag) {
  return (node.tag === tag ? [node] : []).concat(
    ...(node.children || []).map(x => descendants(x, tag))
  );
}
function run(urlPath) {
  const root = element('body');
  const doc = {
    title: 'Page not found',
    documentElement: { lang: 'ru' },
    body: root,
    createElement: element
  };
  vm.runInNewContext(code, { location: { pathname: urlPath }, document: doc }, { timeout: 1000 });
  return { doc, root };
}
const languages = ['en','pl','de','fr','es','it','pt','cs','sk','ro','hu','nl','tr','uk','bg','sr','hr','lt','lv','et','fi','sv','no','da'];
for (const lang of languages) {
  for (const suffix of ['', '/', '/kody/spn-91.html']) {
    const { doc, root } = run('/' + lang + suffix);
    const links = descendants(root, 'a');
    assert(links.some(link => link.href === 'https://dieselcodes.com/'),
      `Missing visible DieselCodes link on /${lang}${suffix}`);
    assert(links.some(link => link.href === 'https://codetruck.ru/'),
      `Missing Russian fallback on /${lang}${suffix}`);
    assert.equal(doc.documentElement.lang, lang);
    assert(descendants(root, 'h1').some(h => typeof h.textContent === 'string' && h.textContent.length > 0),
      'Missing notice heading');
  }
}
for (const input of ['/', '/kody/spn-91.html', '/engine', '/english/page', '/planother']) {
  const { root, doc } = run(input);
  assert.equal(root.children.length, 0, 'Unexpected relocation notice on ' + input);
  assert.equal(doc.documentElement.lang, 'ru');
}
console.log('PASS: 24 legacy language paths render a clickable DieselCodes notice; normal routes unaffected.');
