// Cuts Chiron GoRound TC down to the characters the site uses (scripts/fonts/chars.mjs) and writes
// src/assets/fonts/chiron-goround-tc.woff2, keeping the weight axis (one file serves 400, 500 and 700).
//
// Why: Google Fonts served this font in ~100 slices, 3.8–7.3 MB per Chinese page. On a phone, characters
// whose slice hadn't arrived showed in the system font, so a sentence mixed two fonts (some characters
// looked bold). One small preloaded file swaps all at once.
//
// Run after changing Chinese copy: `npm run fonts`. The unit test fails if any character is missing.
// The source (51 MB) is downloaded from google/fonts at a pinned commit and is not committed.
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import subsetFont from 'subset-font';
import { siteChars } from './chars.mjs';

const COMMIT = 'acff8706bac584c3149c630864fe0d3c07e34561';
const URL = `https://github.com/google/fonts/raw/${COMMIT}/ofl/chirongoroundtc/ChironGoRoundTC%5Bwght%5D.ttf`;
const SHA256 = '47cd5ff5153799d4c0d05bcc64da849e13b8eb842e46728a66bf2d52c480231f';
const CACHE = 'node_modules/.cache/fonts/ChironGoRoundTC[wght].ttf';
const OUT = 'src/assets/fonts/chiron-goround-tc.woff2';

let source = existsSync(CACHE) ? readFileSync(CACHE) : null;
if (!source) {
  console.log('Downloading Chiron GoRound TC…');
  const res = await fetch(URL);
  if (!res.ok) throw new Error(`download failed: ${res.status}`);
  source = Buffer.from(await res.arrayBuffer());
  mkdirSync('node_modules/.cache/fonts', { recursive: true });
  writeFileSync(CACHE, source);
}
const sum = createHash('sha256').update(source).digest('hex');
if (sum !== SHA256) throw new Error(`source font checksum mismatch: ${sum}`);

const text = [...siteChars()].join('');
// Keep the full weight axis: limiting it with `variationAxes` silently dropped the glyph variations
// (gvar), so every weight rendered as regular. subset.test.mjs checks bold really is bolder.
const out = await subsetFont(source, text, { targetFormat: 'woff2' });
writeFileSync(OUT, out);
console.log(`${OUT}: ${[...text].length} characters, ${Math.round(out.length / 1024)} KB`);
