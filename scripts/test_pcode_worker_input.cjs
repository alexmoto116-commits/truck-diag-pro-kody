#!/usr/bin/env node
'use strict';
// Regression guard: actual Worker input normalization, no KV data.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const src = fs.readFileSync(path.join(__dirname, '..', 'worker', 'pcode-api.js'), 'utf8');
const runnable = src.replace(/\bexport\s+default\s*\{/g, 'var workerDefault = {')
  .replace(/\bexport\s+(?=class\s|function\s)/g, '');
const sandbox = { TextEncoder, URL, URLSearchParams, console };
vm.createContext(sandbox);
vm.runInContext(runnable, sandbox, { timeout: 1500 });
for (const [input, expected] of [['abc123','ABC123'], ['p0105-01','P0105-01'], ['m128-p100.1','M128-P100.1'], ['fc 415','415']]) {
  const plan = sandbox.planSearch(input);
  assert(plan && Array.from(plan.forms).includes(expected), 'Failed for ' + input);
}
assert.equal(sandbox.planSearch('invalid!code'), null);
console.log('PASS: lowercase input normalized using actual Worker code');
console.log('NOTE: Actual Cummins ISX code format cases require private local testing.');
