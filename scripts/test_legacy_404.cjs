#!/usr/bin/env node
'use strict';
// Static regression: old language routes are genuine 404s, with no cross-site
// migration script or cross-domain canonical redirect.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, '..', '404.html'), 'utf8');
assert(!/dieselcodes(?:\.com)?/i.test(html), 'CodeTruck 404 must not link to other site');
assert(/<meta\s+name="robots"\s+content="noindex"/i.test(html), '404 must stay noindex');
assert(!/Old translated paths are retired/i.test(html), 'Old relocation script returned');
assert(/<form\b/i.test(html), '404 must retain its search form');
console.log('PASS: standalone CodeTruck 404 with local navigation and no cross-site notice');
