import { test } from 'node:test';
import assert from 'node:assert';
import { pathFor, LOCALES, PAGES } from './locales.ts';
import { makeT, checkParity } from './t.ts';

test('pathFor builds language-prefixed paths', () => {
  assert.strictEqual(pathFor('en', 'home'), '/en/');
  assert.strictEqual(pathFor('zh-hans', 'contact'), '/zh-hans/contact/');
});
test('every locale x page has a path', () => {
  assert.strictEqual(LOCALES.flatMap((l) => PAGES.map((p) => pathFor(l, p))).length, 15);
});
test('t throws on a missing key', () => {
  const t = makeT('en');
  assert.throws(() => t('no.such.key'), /Missing copy key "no.such.key" for en/);
});
test('all locales have the same keys as en', () => {
  assert.deepStrictEqual(checkParity(), []);
});
