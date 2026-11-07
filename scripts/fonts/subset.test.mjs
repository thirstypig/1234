import { test } from 'node:test';
import assert from 'node:assert';
import { readFileSync, statSync } from 'node:fs';
import * as fontkit from 'fontkit';
import { isChinese, siteChars } from './chars.mjs';

const FONT = 'src/assets/fonts/chiron-goround-tc.woff2';
const font = fontkit.create(readFileSync(FONT));

test('the Chinese font subset has every Chinese character the site uses (run `npm run fonts` if not)', () => {
  const missing = [...siteChars()].filter((c) => isChinese(c) && !font.hasGlyphForCodePoint(c.codePointAt(0)));
  assert.deepStrictEqual(missing, [], `missing from ${FONT}: ${missing.join('')}`);
});

test('the subset keeps the weight axis and its glyph variations (else bold renders as regular)', () => {
  const w = font.variationAxes.wght;
  assert.ok(w && w.min <= 400 && w.max >= 700, JSON.stringify(font.variationAxes));
  assert.ok('gvar' in font.directory.tables, 'gvar table missing: every weight would draw the same outlines');
});

test('the subset stays small (it replaced 2.4–5.5 MB of Google Fonts slices per Chinese page)', () => {
  assert.ok(statSync(FONT).size < 1024 * 1024, `${statSync(FONT).size} bytes`);
});

test('no page loads Chiron GoRound TC from Google Fonts any more', () => {
  for (const f of ['src/layouts/BaseLayout.astro', 'src/pages/404.astro']) {
    assert.doesNotMatch(readFileSync(f, 'utf8'), /Chiron\+GoRound/, f);
  }
});
