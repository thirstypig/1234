// Every character the site can show: all text under src/ (copy, notices, reviews, pages, components)
// and the review overlay's scripts. The Chinese font is cut down to exactly these characters,
// so the subset and its test (subset.test.mjs) must read the same list.
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const ROOTS = ['src', 'public/_review'];
const TEXT = /\.(json|md|astro|ts|mjs|js|css)$/;

function* files(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) yield* files(p);
    else if (TEXT.test(name) && !name.includes('.test.')) yield p;
  }
}

/** CJK ideographs, CJK punctuation, full-width forms: the characters that must come from the subset. */
export const isChinese = (c) => /[　-〿㐀-䶿一-鿿豈-﫿︰-﹏＀-￯]/u.test(c);

/** @returns {Set<string>} every character used in the site's source text, plus printable ASCII and Latin-1. */
export function siteChars(root = '.') {
  const chars = new Set();
  for (let c = 0x20; c <= 0x7e; c++) chars.add(String.fromCodePoint(c));
  for (let c = 0xa0; c <= 0xff; c++) chars.add(String.fromCodePoint(c));
  for (const r of ROOTS) for (const f of files(join(root, r))) for (const ch of readFileSync(f, 'utf8')) {
    if (ch.codePointAt(0) >= 0x20) chars.add(ch);
  }
  return chars;
}
