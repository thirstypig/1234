import { test } from 'node:test';
import assert from 'node:assert';
import { commentKeyFor, SITE_CONCEPT } from '../../public/_review/site-key.js';

// The Worker rejects any concept that doesn't start with A–E, and ':' separates the KV key.
test('every site page maps to a key the comments Worker accepts', () => {
  for (const path of ['/en/', '/zh-hans/', '/zh-hant/ortho-k/eye-exams/', '/en/faq/', '/en/faq']) {
    const { concept, page } = commentKeyFor(path);
    assert.strictEqual(concept, SITE_CONCEPT);
    assert.match(concept, /^[A-E][^:/]*$/);
    assert.ok(page && !page.includes(':'), `${path} -> ${page}`);
  }
});

test('different pages get different threads', () => {
  assert.notStrictEqual(commentKeyFor('/en/').page, commentKeyFor('/en/faq/').page);
});

test('a trailing slash does not split a thread', () => {
  assert.strictEqual(commentKeyFor('/en/faq').page, commentKeyFor('/en/faq/').page);
});

test('each language gets its own thread', () => {
  assert.strictEqual(commentKeyFor('/zh-hant/ortho-k/eye-exams/').page, 'zh-hant/ortho-k/eye-exams');
  assert.notStrictEqual(commentKeyFor('/en/faq/').page, commentKeyFor('/zh-hans/faq/').page);
});
