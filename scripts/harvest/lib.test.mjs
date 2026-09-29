import { test } from 'node:test';
import assert from 'node:assert';
import { extractPageLinks, extractAssetUrls, findNumberGaps } from './lib.mjs';

const PAGE = 'https://1234orthok.com/about.html';

test('page links: same-domain html only, normalized, deduped', () => {
  const html = `<a href="../www.1234orthok.com/contact-us.html">c</a>
    <a href="contact-us.html#x">c2</a><a href="https://other.com/a.html">x</a>
    <a href="mailto:a@b.c">m</a><a href="images/1234orthok-com-053.png">img</a>`;
  assert.deepStrictEqual(extractPageLinks(html, PAGE), ['https://1234orthok.com/contact-us.html']);
});

test('asset urls: relative and absolute to the same file collapse to one', () => {
  const html = `<img src="images/1234orthok-com-027.png">
    <img src="https://1234orthok.com/images/1234orthok-com-027.png">
    <img srcset="images/a.jpg 1x, images/b.jpg 2x">
    <div style="background-image:url('images/c.webp')"></div>
    <a href="https://storage.googleapis.com/x/files/book.pdf">pdf</a>`;
  assert.deepStrictEqual(extractAssetUrls(html, PAGE).sort(), [
    'https://1234orthok.com/images/1234orthok-com-027.png',
    'https://1234orthok.com/images/a.jpg',
    'https://1234orthok.com/images/b.jpg',
    'https://1234orthok.com/images/c.webp',
    'https://storage.googleapis.com/x/files/book.pdf',
  ]);
});

test('number gaps: reports missing numbers in the observed range', () => {
  const files = ['1234orthok-com-001.png', '1234orthok-com-003.jpg', '1234orthok-com-005.png', 'other.png'];
  assert.deepStrictEqual(findNumberGaps(files), ['002', '004']);
});

import { suggestTag } from './lib.mjs';

test('suggestTag: small files are decorative', () => {
  assert.strictEqual(suggestTag({ bytes: 1500, width: 32, height: 32, alt: '', context: '', file: 'x.png' }), 'decorative');
});
test('suggestTag: pdf is needs-review', () => {
  assert.strictEqual(suggestTag({ bytes: 900000, file: 'book.pdf', alt: '', context: '' }), 'needs-review');
});
test('suggestTag: logo words suggest third-party-logo', () => {
  assert.strictEqual(suggestTag({ bytes: 20000, width: 300, height: 100, alt: 'Paragon CRT logo', context: '', file: 'a.png' }), 'third-party-logo');
});
test('suggestTag: never guesses practice-photo', () => {
  const t = suggestTag({ bytes: 200000, width: 1200, height: 800, alt: 'Dr. Woo in office', context: '', file: 'a.jpg' });
  assert.strictEqual(t, 'needs-review');
});
