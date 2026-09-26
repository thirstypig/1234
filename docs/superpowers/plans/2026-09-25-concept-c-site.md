# Concept C Site + Legacy Image Harvest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harvest every image from 1234orthok.com into a tagged catalog, and build the Concept C site (5 pages × EN/简体/繁體) deployed at `1234.pasadenaworks.com` with the five concepts archived under `/concepts/`.

**Architecture:** Node scripts in `scripts/` produce `assets/legacy/` (originals + `catalog.json`) and `src/content/copy/en.json`. The Astro app renders every page from `[lang]` routes, one component per Concept C component, all strings from per-language JSON, and styles imported unmodified from the concept folder. The existing Cloudflare Worker gains a `POST /booking` route. One GitHub Pages workflow builds Astro and copies the concepts in.

**Tech Stack:** Astro 7 (Node ≥ 22.12), `node:test` for script units, Vitest for the Worker, `@playwright/test` + `@axe-core/playwright` for page rules.

**Spec:** `docs/superpowers/specs/2026-09-25-concept-c-site-design.md`

## Global Constraints

- Locales: `en`, `zh-hans`, `zh-hant`. Pages: `home`, `about`, `ortho-k`, `contact`, `testimonials`. Switcher always visible and links to the same page in the other language.
- Chinese body text ≥ 17px, line-height ≥ 1.7.
- No logo — plain-text name `1234 Ortho-K Vision Care` (zh pages add `1234兒童視力矯正中心` beneath, per Concept C README).
- Only client-provided copy. Never add statistics, success rates, patient counts, or "best/most effective" claims. Flagged sentences render nothing until approved in `docs/copy-review.md`.
- All text WCAG AA.
- "Book a consultation" in the first screen and at the bottom of every page. Mobile sticky Book/Message bar.
- Chinese body copy is placeholder until the client supplies it: zh-hant `〔中文內容待提供〕`, zh-hans `〔中文内容待提供〕`.
- Contact facts come from the client brief as reflected in Concept C (Alhambra: 1234 S. Garfield Ave., #105, Alhambra, CA 91801 · Tue & Fri 12–6 pm, Sat 12–4 pm; Walnut: address and hours "coming soon"; phones (800) 991-8881 · (626) 282-5388). Where the old site differs (Rowland Heights, Mon–Wed hours), list it in `docs/copy-review.md`; don't publish it.
- Design files under `design/concepts/` are never edited.
- Legacy images appear on pages only via `src/lib/images.ts`; the build fails otherwise.
- No `window.alert()` / `window.prompt()` / `confirm()` anywhere.
- Whole preview site: review-password gate + `<meta name="robots" content="noindex">`.
- Commits end with `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.

## Review Focus

1. **Language switcher on non-home pages** — clicking 简体 on `/en/contact/` must land on `/zh-hans/contact/`, not `/zh-hans/`. Pinned by the e2e test in Task 6.
2. **Booking form double-submit / network failure** — the button disables while sending; a failed request shows an inline error and re-enables, with the typed values kept. Pinned in Task 10.
3. **Relative image URLs on crawled pages** — `images/x.png` on `/about.html` and `https://1234orthok.com/images/x.png` are the same file and must download once. Pinned in Task 1.
4. **Missing copy key** — a key present in `en.json` but absent from a zh file must fail the build, not render `undefined`. Pinned in Task 4.
5. **Moved concepts still gated and commentable** — `/concepts/concepts/C-picture-book/ConceptC-PictureBook-homepage-EN.html` must still load `/_review/inject.js`. Pinned in Task 12.

---

## File Structure

```
scripts/harvest/lib.mjs            pure helpers: URL extraction, gap finding, tagging heuristics
scripts/harvest/lib.test.mjs
scripts/harvest/crawl.mjs          CLI: crawl + download + write catalog.json
scripts/harvest/review-page.mjs    CLI: catalog.json → design/legacy-catalog/index.html
scripts/copy/claims.mjs            flagClaims(sentence)
scripts/copy/claims.test.mjs
scripts/copy/extract.mjs           CLI: old-site text → en.json draft + docs/copy-review.md
assets/legacy/originals/*          downloaded files (committed)
assets/legacy/catalog.json
design/legacy-catalog/index.html   generated review grid
src/i18n/locales.ts                LOCALES, PAGES, pathFor(), alternates()
src/i18n/t.ts                      makeT(lang) with strict missing-key error
src/i18n/i18n.test.mjs
src/content/copy/{en,zh-hans,zh-hant}.json
src/content/approved-claims.json   ids of flagged sentences approved by the user
src/lib/images.ts                  legacyImage(filename) guard
src/lib/images.test.mjs
src/styles/site.css                imports concept tokens + bundle
src/layouts/BaseLayout.astro       (modify) html lang, css, hreflang, noindex, gate, chrome
src/components/*.astro             one per Concept C component
src/features/{home,about,ortho-k,contact,testimonials}/Page.astro
src/features/contact/booking.js    form submit client
src/pages/index.astro              (modify) redirect → /en/
src/pages/[lang]/index.astro, about.astro, ortho-k.astro, contact.astro, testimonials.astro
tests/e2e/rules.spec.ts            CLAUDE.md rules + axe over all 15 pages
tests/e2e/booking.spec.ts
tests/e2e/deploy.spec.ts
playwright.config.ts
workers/comments/src/booking.ts    booking handler
workers/comments/src/booking.test.ts
workers/comments/src/index.ts      (modify) route /booking
.github/workflows/deploy-site.yml  replaces deploy-review-site.yml
```

---

### Task 1: Harvest crawler

**Files:**
- Create: `scripts/harvest/lib.mjs`, `scripts/harvest/lib.test.mjs`, `scripts/harvest/crawl.mjs`
- Modify: `package.json` (scripts)

**Interfaces:**
- Produces: `extractPageLinks(html, pageUrl) → string[]`, `extractAssetUrls(html, pageUrl) → string[]`, `findNumberGaps(filenames) → string[]` (from lib.mjs); `assets/legacy/originals/<basename>`; `assets/legacy/catalog.json` = `Array<{file, url, sourcePages: string[], bytes, width, height, alt, context, tag: null, approved: false, orphan: boolean}>`.

- [ ] **Step 1: Write the failing tests**

```js
// scripts/harvest/lib.test.mjs
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
```

- [ ] **Step 2: Run to verify failure**

Run: `node --test scripts/harvest/lib.test.mjs`
Expected: FAIL — `Cannot find module './lib.mjs'`.

- [ ] **Step 3: Implement `lib.mjs`**

```js
// scripts/harvest/lib.mjs
const SITE_HOST = '1234orthok.com';
const ASSET_EXT = /\.(png|jpe?g|gif|webp|svg|pdf)(\?|#|$)/i;

function resolve(raw, base) {
  // Mirror-tool links look like ../www.1234orthok.com/x.html — strip the fake host folder.
  const cleaned = raw.trim().replace(/^(\.\.\/)*www\.1234orthok\.com\//, '/');
  try {
    const u = new URL(cleaned, base);
    u.hash = '';
    if (u.hostname === `www.${SITE_HOST}`) u.hostname = SITE_HOST;
    return u;
  } catch { return null; }
}

export function extractPageLinks(html, pageUrl) {
  const out = new Set();
  for (const [, href] of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/gi)) {
    const u = resolve(href, pageUrl);
    if (!u || u.hostname !== SITE_HOST || !/^https?:$/.test(u.protocol)) continue;
    if (ASSET_EXT.test(u.pathname)) continue;
    if (!/(\.html?|\/)$/.test(u.pathname)) continue;
    out.add(u.href);
  }
  return [...out];
}

export function extractAssetUrls(html, pageUrl) {
  const raws = [];
  for (const [, v] of html.matchAll(/\b(?:src|data-src)="([^"]+)"/gi)) raws.push(v);
  for (const [, v] of html.matchAll(/\bsrcset="([^"]+)"/gi)) raws.push(...v.split(',').map((s) => s.trim().split(/\s+/)[0]));
  for (const [, v] of html.matchAll(/url\(\s*['"]?([^'")]+)['"]?\s*\)/gi)) raws.push(v);
  for (const [, v] of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/gi)) raws.push(v);
  const out = new Set();
  for (const raw of raws) {
    const u = resolve(raw, pageUrl);
    if (u && ASSET_EXT.test(u.pathname)) out.add(u.href);
  }
  return [...out];
}

export function findNumberGaps(filenames) {
  const nums = filenames
    .map((f) => f.match(/^1234orthok-com-(\d{3})\./)?.[1])
    .filter(Boolean)
    .map(Number);
  if (!nums.length) return [];
  const have = new Set(nums);
  const gaps = [];
  for (let n = Math.min(...nums); n <= Math.max(...nums); n++) {
    if (!have.has(n)) gaps.push(String(n).padStart(3, '0'));
  }
  return gaps;
}
```

- [ ] **Step 4: Run tests — expect PASS**

Run: `node --test scripts/harvest/lib.test.mjs`

- [ ] **Step 5: Write the crawler CLI**

```js
// scripts/harvest/crawl.mjs
import { mkdir, writeFile, readdir } from 'node:fs/promises';
import { basename, join } from 'node:path';
import { imageSize } from 'image-size';
import { extractPageLinks, extractAssetUrls, findNumberGaps } from './lib.mjs';

const START = 'https://1234orthok.com/';
const OUT = 'assets/legacy/originals';
const CATALOG = 'assets/legacy/catalog.json';
await mkdir(OUT, { recursive: true });

const seen = new Set();
const queue = [START];
const assets = new Map(); // url -> {sourcePages:Set, alt, context}

while (queue.length) {
  const url = queue.shift();
  if (seen.has(url)) continue;
  seen.add(url);
  const res = await fetch(url);
  if (!res.ok || !(res.headers.get('content-type') || '').includes('html')) continue;
  const html = await res.text();
  for (const link of extractPageLinks(html, url)) if (!seen.has(link)) queue.push(link);
  for (const a of extractAssetUrls(html, url)) {
    const entry = assets.get(a) || { sourcePages: new Set(), alt: '', context: '' };
    entry.sourcePages.add(url);
    const file = basename(new URL(a).pathname);
    const tag = html.match(new RegExp(`<img[^>]*${file.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[^>]*>`, 'i'))?.[0] || '';
    entry.alt ||= tag.match(/\balt="([^"]*)"/i)?.[1] || '';
    const at = html.indexOf(file);
    entry.context ||= at < 0 ? '' : html.slice(Math.max(0, at - 600), at + 600)
      .replace(/<(script|style)[\s\S]*?<\/\1>/gi, ' ').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 300);
    assets.set(a, entry);
  }
}
console.log(`crawled ${seen.size} pages, found ${assets.size} assets`);

// Probe unlinked numbered files.
const names = [...assets.keys()].map((u) => basename(new URL(u).pathname));
const orphans = [];
for (const n of findNumberGaps(names)) {
  for (const ext of ['png', 'jpg']) {
    const u = `https://1234orthok.com/images/1234orthok-com-${n}.${ext}`;
    const r = await fetch(u, { method: 'HEAD' });
    if (r.ok) { assets.set(u, { sourcePages: new Set(), alt: '', context: '' }); orphans.push(u); break; }
  }
}
console.log(`orphans found by gap probe: ${orphans.length}`);

const catalog = [];
for (const [url, e] of assets) {
  const res = await fetch(url);
  if (!res.ok) { console.warn('skip', res.status, url); continue; }
  const buf = Buffer.from(await res.arrayBuffer());
  const file = basename(new URL(url).pathname);
  await writeFile(join(OUT, file), buf);
  let dims = {};
  try { dims = imageSize(buf); } catch {}
  catalog.push({
    file, url, sourcePages: [...e.sourcePages].sort(), bytes: buf.length,
    width: dims.width ?? null, height: dims.height ?? null, alt: e.alt, context: e.context,
    tag: null, approved: false, orphan: e.sourcePages.size === 0,
  });
}
catalog.sort((a, b) => a.file.localeCompare(b.file));
await writeFile(CATALOG, JSON.stringify(catalog, null, 2) + '\n');
const total = catalog.reduce((s, c) => s + c.bytes, 0);
console.log(`wrote ${catalog.length} files, ${(total / 1e6).toFixed(1)} MB`);
```

Add to `package.json` scripts: `"harvest": "node scripts/harvest/crawl.mjs"`, `"test:unit": "node --test scripts/**/*.test.mjs src/**/*.test.mjs"`. Install: `npm i -D image-size`.

- [ ] **Step 6: Run it and check the size**

Run: `npm run harvest`
Expected: prints pages crawled (≥ 12), assets found (≥ 25), orphans, and total MB. **If total > 50 MB, stop and report to the user before committing** (spec: LFS/untracked if large).

- [ ] **Step 7: Commit**

```bash
git add scripts/harvest package.json package-lock.json assets/legacy
git commit -m "Harvest all images from 1234orthok.com into assets/legacy"
```

---

### Task 2: Tagging + catalog review page

**Files:**
- Modify: `scripts/harvest/lib.mjs`, `scripts/harvest/lib.test.mjs`, `assets/legacy/catalog.json`
- Create: `scripts/harvest/tag.mjs`, `scripts/harvest/review-page.mjs`, `design/legacy-catalog/index.html`

**Interfaces:**
- Consumes: `catalog.json` from Task 1.
- Produces: `suggestTag(entry) → 'practice-photo'|'likely-stock'|'third-party-logo'|'patient-photo'|'decorative'|'needs-review'`; every catalog entry has a non-null `tag`.

- [ ] **Step 1: Failing tests for `suggestTag`**

```js
// append to scripts/harvest/lib.test.mjs
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
```

- [ ] **Step 2: Run — expect FAIL** (`suggestTag` is not exported). `node --test scripts/harvest/lib.test.mjs`

- [ ] **Step 3: Implement**

```js
// append to scripts/harvest/lib.mjs
export function suggestTag({ bytes = 0, width, height, alt = '', context = '', file = '' }) {
  if (/\.pdf$/i.test(file)) return 'needs-review';
  if (bytes < 5000 || (width && height && width * height < 80 * 80)) return 'decorative';
  if (/\blogo\b|certif|paragon|euclid|bausch|menicon|fda|aoa|association/i.test(`${alt} ${context}`)) return 'third-party-logo';
  // Practice vs patient vs stock requires eyes on the image — never guessed.
  return 'needs-review';
}
```

- [ ] **Step 4: Run — expect PASS.**

- [ ] **Step 5: Apply heuristics, then tag by eye**

`scripts/harvest/tag.mjs`: reads catalog, sets `tag = suggestTag(e)` only where `tag === null`, writes it back. Run `node scripts/harvest/tag.mjs`.

Then open each non-decorative image with the Read tool (it displays images) and set `tag` by hand in `catalog.json`:
- Dr. Woo, staff, clinic interior/exterior, equipment → `practice-photo`
- Identifiable child or parent → `patient-photo` (even if it's also in the office)
- Generic polished photo / clip art / watermark / reverse-image-plausible stock → `likely-stock`
- Brand or certifying-body mark → `third-party-logo`
- Unsure → leave `needs-review`

- [ ] **Step 6: Generate the review page**

```js
// scripts/harvest/review-page.mjs
import { readFile, writeFile, mkdir, cp } from 'node:fs/promises';
const catalog = JSON.parse(await readFile('assets/legacy/catalog.json', 'utf8'));
await mkdir('design/legacy-catalog/img', { recursive: true });
for (const c of catalog) await cp(`assets/legacy/originals/${c.file}`, `design/legacy-catalog/img/${c.file}`);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[ch]);
const tags = [...new Set(catalog.map((c) => c.tag))].sort();
const cards = catalog.map((c) => `
  <figure class="card" data-tag="${esc(c.tag)}">
    ${/\.pdf$/i.test(c.file) ? `<a href="img/${esc(c.file)}">PDF: ${esc(c.file)}</a>` : `<img loading="lazy" src="img/${esc(c.file)}" alt="${esc(c.alt)}">`}
    <figcaption><b>${esc(c.file)}</b> · <span class="tag">${esc(c.tag)}</span>${c.orphan ? ' · orphan' : ''}<br>
    ${c.width ?? '?'}×${c.height ?? '?'} · ${(c.bytes / 1024).toFixed(0)} KB<br>
    <small>${c.sourcePages.map((p) => esc(new URL(p).pathname)).join(', ') || 'not linked'}</small></figcaption>
  </figure>`).join('');
await writeFile('design/legacy-catalog/index.html', `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Legacy images — 1234 Ortho-K</title>
<style>body{font:16px/1.5 system-ui;margin:16px;background:#fff;color:#222}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.card{margin:0;border:1px solid #ddd;border-radius:8px;padding:8px}.card img{width:100%;height:160px;object-fit:contain;background:#f4f4f4}
.tag{font-weight:600}button[aria-pressed=true]{background:#1F3563;color:#fff}</style></head><body>
<h1>Images from 1234orthok.com (${catalog.length})</h1>
<p>Only <b>practice-photo</b> images are used on the new site automatically. Everything else needs sign-off.</p>
<p>${['all', ...tags].map((t) => `<button data-f="${esc(t)}" aria-pressed="${t === 'all'}">${esc(t)}</button>`).join(' ')}</p>
<div class="grid">${cards}</div>
<script>document.querySelectorAll('button[data-f]').forEach(b=>b.onclick=()=>{document.querySelectorAll('button[data-f]').forEach(x=>x.setAttribute('aria-pressed',x===b));
document.querySelectorAll('.card').forEach(c=>c.hidden=b.dataset.f!=='all'&&c.dataset.tag!==b.dataset.f)});</script>
<script type="module" src="/_review/gate-only.js"></script></body></html>\n`);
console.log('wrote design/legacy-catalog/index.html');
```

Note: `design/legacy-catalog/` is new and generated, so it is not a concept file. The gate script `/_review/gate-only.js` is created in Task 12.

Run: `node scripts/harvest/review-page.mjs`, then open the file and confirm filters work.

- [ ] **Step 7: Commit**

```bash
git add scripts/harvest assets/legacy/catalog.json design/legacy-catalog
git commit -m "Tag legacy images and generate the catalog review page"
```

---

### Task 3: Copy extraction + claims flagger

**Files:**
- Create: `scripts/copy/claims.mjs`, `scripts/copy/claims.test.mjs`, `scripts/copy/extract.mjs`, `docs/copy-review.md`, `docs/legacy-copy/*.txt`

**Interfaces:**
- Produces: `flagClaims(sentence) → string[]` (reasons; empty = clean). `docs/legacy-copy/<page>.txt`: clean sentences, one per line, for Task 7/8 authors to draw from. `docs/copy-review.md`: flagged sentences with stable ids `F-<page>-<n>`.

- [ ] **Step 1: Failing tests**

```js
// scripts/copy/claims.test.mjs
import { test } from 'node:test';
import assert from 'node:assert';
import { flagClaims } from './claims.mjs';

test('clean sentence passes', () => {
  assert.deepStrictEqual(flagClaims('Lenses are worn while your child sleeps.'), []);
});
test('percent and success rate', () => {
  assert.ok(flagClaims('Ortho-K has a 95% success rate.').includes('statistic'));
  assert.ok(flagClaims('Ortho-K has a 95% success rate.').includes('success-rate'));
});
test('superlatives', () => {
  assert.ok(flagClaims('The most effective treatment for myopia.').includes('superlative'));
  assert.ok(flagClaims('We are the best clinic in the San Gabriel Valley.').includes('superlative'));
  assert.ok(flagClaims('A leading Ortho-K provider.').includes('superlative'));
});
test('patient counts and guarantees', () => {
  assert.ok(flagClaims('Over 5,000 children treated.').includes('patient-count'));
  assert.ok(flagClaims('Results are guaranteed.').includes('guarantee'));
});
test('years of experience is flagged for review, not auto-cut', () => {
  assert.ok(flagClaims('Dr. Woo has 30 years of experience.').includes('number'));
});
```

- [ ] **Step 2: Run — expect FAIL.** `node --test scripts/copy/claims.test.mjs`

- [ ] **Step 3: Implement**

```js
// scripts/copy/claims.mjs
const RULES = [
  ['statistic', /\d+(\.\d+)?\s*%|\bpercent\b/i],
  ['success-rate', /success\s+rate|effective(ness)?\s+rate|\bcure[sd]?\b/i],
  ['superlative', /\b(best|most\s+effective|most\s+advanced|leading|top|#\s?1|number\s+one|premier|unmatched)\b/i],
  ['patient-count', /\b\d[\d,]*\+?\s+(patients|children|kids|families|cases|eyes)\b|\b(thousands|hundreds)\s+of\s+(patients|children|families)/i],
  ['guarantee', /\bguarantee[sd]?\b|\bpermanent(ly)?\b|\b100\s*%/i],
  ['number', /\d/],
];
export function flagClaims(sentence) {
  return RULES.filter(([, re]) => re.test(sentence)).map(([name]) => name);
}
```

- [ ] **Step 4: Run — expect PASS.**

- [ ] **Step 5: Extraction CLI**

```js
// scripts/copy/extract.mjs
import { writeFile, mkdir } from 'node:fs/promises';
import { flagClaims } from './claims.mjs';

const PAGES = { home: '', about: 'about.html', 'ortho-k': 'ortho.html', contact: 'contact-us.html', testimonials: 'testimonials.html' };
const HAN = /\p{Script=Han}/u;
await mkdir('docs/legacy-copy', { recursive: true });
let review = `# Copy review\n\nSentences from the old site that break the CLAUDE.md copy rules.\nMark each: **keep** (add its id to \`src/content/approved-claims.json\`), **cut**, or **rewrite** (write the new text under it).\n\n`;
review += `## Facts that differ from the client brief\n\n- Old site lists **Rowland Heights**; brief and Concept C say **Walnut**. Using Walnut.\n- Old site hours (Mon–Wed 12–6 …) differ from Concept C (Tue & Fri 12–6, Sat 12–4). Using Concept C.\n\n`;

for (const [page, path] of Object.entries(PAGES)) {
  const html = await (await fetch(`https://1234orthok.com/${path}`)).text();
  const text = html.replace(/<(script|style|nav|header|footer)[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<br\s*\/?>|<\/(p|div|h\d|li)>/gi, '\n').replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&#39;|&rsquo;/g, "'").replace(/&quot;/g, '"');
  const sentences = text.split(/\n|(?<=[.!?])\s+/).map((s) => s.replace(/\s+/g, ' ').trim())
    .filter((s) => s.length > 20 && !HAN.test(s));
  const zh = text.split('\n').map((s) => s.trim()).filter((s) => HAN.test(s));
  const clean = [];
  const flagged = [];
  for (const s of [...new Set(sentences)]) (flagClaims(s).length ? flagged : clean).push(s);
  await writeFile(`docs/legacy-copy/${page}.txt`, clean.join('\n') + '\n');
  if (zh.length) await writeFile(`docs/legacy-copy/${page}.zh-Hant.reference.txt`, zh.join('\n') + '\n');
  review += `## ${page}\n\n`;
  flagged.forEach((s, i) => { review += `- [ ] **F-${page}-${i + 1}** (${flagClaims(s).join(', ')}): ${s}\n`; });
  if (!flagged.length) review += '_Nothing flagged._\n';
  review += '\n';
}
await writeFile('docs/copy-review.md', review);
await writeFile('src/content/approved-claims.json', '[]\n');
console.log('wrote docs/copy-review.md and docs/legacy-copy/');
```

Run: `mkdir -p src/content && node scripts/copy/extract.mjs`. Open `docs/copy-review.md` and check the flags are sensible (spot-check 5 clean lines too).

- [ ] **Step 6: Commit**

```bash
git add scripts/copy docs/copy-review.md docs/legacy-copy src/content/approved-claims.json
git commit -m "Extract old-site copy and flag claims for review"
```

---

### Task 4: i18n foundation, layout, styles, routes

**Files:**
- Create: `src/i18n/locales.ts`, `src/i18n/t.ts`, `src/i18n/i18n.test.mjs`, `src/content/copy/{en,zh-hans,zh-hant}.json`, `src/styles/site.css`, `src/pages/[lang]/{index,about,ortho-k,contact,testimonials}.astro`, `src/features/*/Page.astro` (stub)
- Modify: `astro.config.mjs`, `src/layouts/BaseLayout.astro`, `src/pages/index.astro`, `package.json`

**Interfaces:**
- Produces:
  - `LOCALES = ['en','zh-hans','zh-hant'] as const`, `type Lang`, `PAGES = ['home','about','ortho-k','contact','testimonials'] as const`, `type PageId`
  - `pathFor(lang: Lang, page: PageId): string` → `/en/`, `/zh-hans/about/` …
  - `HTML_LANG: Record<Lang,string>` → `en`, `zh-Hans`, `zh-Hant`
  - `makeT(lang: Lang): (key: string) => string` — throws `Missing copy key "<key>" for <lang>`
  - `getLangStaticPaths()` → `LOCALES.map(lang => ({ params: { lang } }))`
  - `BaseLayout` props: `{ lang: Lang; page: PageId; title: string }`

- [ ] **Step 1: Failing tests**

```js
// src/i18n/i18n.test.mjs  (run through tsx so .ts imports work)
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
```

- [ ] **Step 2: Run — expect FAIL.** Install `npm i -D tsx`; set `"test:unit": "node --import tsx --test \"scripts/**/*.test.mjs\" \"src/**/*.test.mjs\""`. Run `npm run test:unit`.

- [ ] **Step 3: Implement i18n**

```ts
// src/i18n/locales.ts
export const LOCALES = ['en', 'zh-hans', 'zh-hant'] as const;
export type Lang = (typeof LOCALES)[number];
export const PAGES = ['home', 'about', 'ortho-k', 'contact', 'testimonials'] as const;
export type PageId = (typeof PAGES)[number];
export const HTML_LANG: Record<Lang, string> = { en: 'en', 'zh-hans': 'zh-Hans', 'zh-hant': 'zh-Hant' };
export const SWITCHER_LABEL: Record<Lang, string> = { en: 'EN', 'zh-hans': '简体', 'zh-hant': '繁體' };

export function pathFor(lang: Lang, page: PageId): string {
  return page === 'home' ? `/${lang}/` : `/${lang}/${page}/`;
}
export function getLangStaticPaths() {
  return LOCALES.map((lang) => ({ params: { lang } }));
}
```

```ts
// src/i18n/t.ts
import en from '../content/copy/en.json';
import zhHans from '../content/copy/zh-hans.json';
import zhHant from '../content/copy/zh-hant.json';
import type { Lang } from './locales';

type Dict = { [k: string]: string | Dict };
const DICTS: Record<Lang, Dict> = { en, 'zh-hans': zhHans, 'zh-hant': zhHant };

function lookup(d: Dict, key: string): string | undefined {
  const v = key.split('.').reduce<unknown>((o, k) => (o && typeof o === 'object' ? (o as Dict)[k] : undefined), d);
  return typeof v === 'string' ? v : undefined;
}
function keys(d: Dict, prefix = ''): string[] {
  return Object.entries(d).flatMap(([k, v]) => (typeof v === 'string' ? [prefix + k] : keys(v, `${prefix}${k}.`)));
}
export function makeT(lang: Lang) {
  return (key: string): string => {
    const v = lookup(DICTS[lang], key);
    if (v === undefined) throw new Error(`Missing copy key "${key}" for ${lang}`);
    return v;
  };
}
/** Returns "<lang>: <key>" for every en key missing elsewhere (and extra keys). */
export function checkParity(): string[] {
  const base = new Set(keys(DICTS.en));
  const out: string[] = [];
  for (const lang of ['zh-hans', 'zh-hant'] as const) {
    const ks = new Set(keys(DICTS[lang]));
    for (const k of base) if (!ks.has(k)) out.push(`${lang}: missing ${k}`);
    for (const k of ks) if (!base.has(k)) out.push(`${lang}: extra ${k}`);
  }
  return out;
}
```

Seed the three JSON files with the shared chrome keys (English from the Concept C EN mockup, lines 362–368 and 475–480; zh-hant chrome labels from `ConceptC-PictureBook-homepage-zh-Hant.html` same lines; zh-hans chrome labels = the English labels until the client supplies them):

```json
{
  "site": { "name": "1234 Ortho-K Vision Care", "nameZh": "1234兒童視力矯正中心" },
  "nav": { "home": "Home", "about": "About", "orthok": "Ortho-K", "testimonials": "Stories", "contact": "Contact", "menu": "Menu", "close": "Close" },
  "cta": { "book": "Book a consultation", "message": "Message us", "call": "Call" },
  "footer": { "copyright": "© 2026 1234 Ortho-K Vision Care", "privacy": "Privacy policy" },
  "meta": { "home": "1234 Ortho-K Vision Care", "about": "About", "ortho-k": "Ortho-K", "contact": "Contact", "testimonials": "Stories" }
}
```

(Use the mockup's exact label text where it differs from the above — the mockup is the source.)

- [ ] **Step 4: Run — expect PASS.**

- [ ] **Step 5: Styles, layout, routes**

```css
/* src/styles/site.css — Concept C, imported unmodified */
@import '../../design/concepts/concepts/C-picture-book/tokens.local.css';
@import '../../design/concepts/concepts/C-picture-book/project/components/bundle.css';
html, body { margin: 0; background: var(--background); }
/* CLAUDE.md floor for Chinese body text */
:lang(zh) .ui-body, :lang(zh) .ui-lead, :lang(zh) p { font-size: max(17px, 1em); line-height: 1.8; }
```

```astro
---
// src/layouts/BaseLayout.astro
import '../styles/site.css';
import { LOCALES, HTML_LANG, pathFor, type Lang, type PageId } from '../i18n/locales';
interface Props { lang: Lang; page: PageId; title: string }
const { lang, page, title } = Astro.props;
const site = 'https://1234.pasadenaworks.com';
---
<!doctype html>
<html lang={HTML_LANG[lang]}>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="robots" content="noindex" />
    <title>{title}</title>
    {LOCALES.map((l) => <link rel="alternate" hreflang={HTML_LANG[l]} href={site + pathFor(l, page)} />)}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Chiron+GoRound+TC:wght@400;500;700&display=swap" rel="stylesheet" />
    <script type="module" src="/_review/gate-only.js"></script>
  </head>
  <body>
    <slot />
  </body>
</html>
```

```astro
---
// src/pages/[lang]/about.astro  (same shape for index/ortho-k/contact/testimonials, changing PageId and feature import)
import { getLangStaticPaths, type Lang } from '../../i18n/locales';
import Page from '../../features/about/Page.astro';
export const getStaticPaths = getLangStaticPaths;
const lang = Astro.params.lang as Lang;
---
<Page lang={lang} />
```

```astro
---
// src/features/about/Page.astro — stub, filled in Task 8
import BaseLayout from '../../layouts/BaseLayout.astro';
import { makeT } from '../../i18n/t';
import type { Lang } from '../../i18n/locales';
const { lang } = Astro.props as { lang: Lang };
const t = makeT(lang);
---
<BaseLayout lang={lang} page="about" title={t('meta.about')}><main><h1>{t('meta.about')}</h1></main></BaseLayout>
```

```astro
---
// src/pages/index.astro
---
<meta http-equiv="refresh" content="0; url=/en/" /><link rel="canonical" href="/en/" /><a href="/en/">Continue</a>
```

`astro.config.mjs`: `export default defineConfig({ site: 'https://1234.pasadenaworks.com', trailingSlash: 'always', build: { format: 'directory' }, vite: { server: { fs: { allow: ['.'] } } } });`

- [ ] **Step 6: Build**

Run: `npx astro build && ls dist/en dist/zh-hans/about`
Expected: build succeeds; 15 `index.html` files under `dist/{en,zh-hans,zh-hant}/`.

- [ ] **Step 7: Commit**

```bash
git add src astro.config.mjs package.json package-lock.json
git commit -m "Add i18n routing, strict copy lookup, and Concept C styles"
```

---

### Task 5: Legacy image guard

**Files:**
- Create: `src/lib/images-guard.ts`, `src/lib/images.ts`, `src/lib/images.test.mjs`

**Interfaces:**
- Consumes: `assets/legacy/catalog.json`.
- Produces: `assertUsable(file: string, catalog: Entry[]): void` (throws), `legacyImage(file: string): ImageMetadata` (for `<Image src={...}>`).

- [ ] **Step 1: Failing tests**

```js
// src/lib/images.test.mjs
import { test } from 'node:test';
import assert from 'node:assert';
import { assertUsable } from './images-guard.ts';

const cat = [
  { file: 'dr.jpg', tag: 'practice-photo', approved: false },
  { file: 'kid.jpg', tag: 'patient-photo', approved: false },
  { file: 'kid-ok.jpg', tag: 'patient-photo', approved: true },
];
test('practice photo is usable', () => assert.doesNotThrow(() => assertUsable('dr.jpg', cat)));
test('patient photo is blocked', () => assert.throws(() => assertUsable('kid.jpg', cat), /kid\.jpg.*patient-photo.*not approved/));
test('approved patient photo is usable', () => assert.doesNotThrow(() => assertUsable('kid-ok.jpg', cat)));
test('unknown file is blocked', () => assert.throws(() => assertUsable('nope.jpg', cat), /not in the legacy catalog/));
```

- [ ] **Step 2: Run — expect FAIL.** `npm run test:unit`

- [ ] **Step 3: Implement** (guard split out so the test doesn't need Vite's `import.meta.glob`)

```ts
// src/lib/images-guard.ts
export interface Entry { file: string; tag: string | null; approved: boolean }
export function assertUsable(file: string, catalog: Entry[]): void {
  const e = catalog.find((c) => c.file === file);
  if (!e) throw new Error(`Image "${file}" is not in the legacy catalog`);
  if (e.tag !== 'practice-photo' && !e.approved) {
    throw new Error(`Image "${file}" is tagged ${e.tag} and not approved — set approved:true in assets/legacy/catalog.json after sign-off`);
  }
}
```

```ts
// src/lib/images.ts
import type { ImageMetadata } from 'astro';
import catalog from '../../assets/legacy/catalog.json';
import { assertUsable, type Entry } from './images-guard';
const files = import.meta.glob<{ default: ImageMetadata }>('../../assets/legacy/originals/*.{png,jpg,jpeg,webp,gif}', { eager: true });
export function legacyImage(file: string): ImageMetadata {
  assertUsable(file, catalog as Entry[]);
  const mod = files[`../../assets/legacy/originals/${file}`];
  if (!mod) throw new Error(`Image "${file}" is catalogued but missing from assets/legacy/originals`);
  return mod.default;
}
```

- [ ] **Step 4: Run — expect PASS.**
- [ ] **Step 5: Commit** — `git add src/lib && git commit -m "Guard legacy image use behind the catalog tags"`

---

### Task 6: Shared chrome components + rules test harness

**Files:**
- Create: `src/components/{LanguageSwitcher,SiteHeader,SiteFooter,StickyBar,Button,Icon}.astro`, `playwright.config.ts`, `tests/e2e/rules.spec.ts`
- Modify: `src/layouts/BaseLayout.astro` (render chrome around `<slot/>`), `package.json`

**Interfaces:**
- Consumes: `pathFor`, `LOCALES`, `SWITCHER_LABEL`, `makeT`, `Lang`, `PageId`.
- Produces: `<Button href variant="primary|secondary" size?="sm" block? icon?>`; `<Icon name="calendar|chat|phone|pin|clock|…">`; BaseLayout renders `LanguageSwitcher` (utility bar), `SiteHeader`, `<slot/>`, `SiteFooter`, `StickyBar`.

- [ ] **Step 1: Test harness and the failing rules test**

`npm i -D @playwright/test @axe-core/playwright && npx playwright install chromium`

```ts
// playwright.config.ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: 'tests/e2e',
  webServer: { command: 'npx astro build && npx astro preview --port 4321', port: 4321, reuseExistingServer: true, timeout: 180_000 },
  use: { baseURL: 'http://localhost:4321' },
});
```

```ts
// tests/e2e/rules.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
const LOCALES = ['en', 'zh-hans', 'zh-hant'];
const PAGES = ['', 'about/', 'ortho-k/', 'contact/', 'testimonials/'];
const ALL = LOCALES.flatMap((l) => PAGES.map((p) => `/${l}/${p}`));

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
});

for (const path of ALL) {
  test.describe(path, () => {
    test('switcher links to the same page in each language', async ({ page }) => {
      await page.goto(path);
      const sub = path.split('/').slice(2).join('/');
      for (const l of LOCALES) {
        await expect(page.locator(`.ui-lang a[href="/${l}/${sub}"]`).first()).toBeAttached();
      }
    });
    test('Book a consultation in first screen and at bottom', async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto(path);
      const book = page.locator('[data-cta="book"]');
      await expect(book.first()).toBeInViewport();
      await expect(page.locator('footer [data-cta="book"], [data-cta-bottom] [data-cta="book"]').first()).toBeAttached();
    });
    test('no logo image in header', async ({ page }) => {
      await page.goto(path);
      await expect(page.locator('header img, header svg.logo')).toHaveCount(0);
    });
    test('WCAG AA (axe)', async ({ page }) => {
      await page.goto(path);
      const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
      expect(r.violations.map((v) => `${v.id}: ${v.nodes.length}`)).toEqual([]);
    });
    if (path.startsWith('/zh')) {
      test('Chinese body >= 17px, line-height >= 1.7', async ({ page }) => {
        await page.goto(path);
        const bad = await page.$$eval('main p', (ps) => ps.map((p) => {
          const s = getComputedStyle(p); const fs = parseFloat(s.fontSize);
          const lh = s.lineHeight === 'normal' ? 1.2 : parseFloat(s.lineHeight) / fs;
          return fs < 17 || lh < 1.7 ? `${p.textContent?.slice(0, 20)} ${fs}px/${lh.toFixed(2)}` : null;
        }).filter(Boolean));
        expect(bad).toEqual([]);
      });
    }
    test('mobile sticky Book/Message bar', async ({ page }) => {
      await page.setViewportSize({ width: 390, height: 844 });
      await page.goto(path);
      await page.mouse.wheel(0, 3000);
      await expect(page.locator('[data-sticky-bar] [data-cta="book"]')).toBeInViewport();
      await expect(page.locator('[data-sticky-bar] [data-cta="message"]')).toBeInViewport();
    });
  });
}
```

Add scripts: `"test:e2e": "playwright test"`, `"test": "npm run test:unit && npm run test:e2e"`.

- [ ] **Step 2: Run — expect FAIL** (no switcher/header/CTA yet). `npx playwright test tests/e2e/rules.spec.ts`

- [ ] **Step 3: Build the components by porting mockup markup**

Source: `design/concepts/concepts/C-picture-book/ConceptC-PictureBook-homepage-EN.html`. Copy markup **verbatim**, then make only these changes: text → `t('…')`, `href="#"` → real paths, add `data-cta` attributes.
- `LanguageSwitcher.astro` ← line 362 (`div.ui-utility` → `nav.ui-lang`). Each link: `href={pathFor(l, page)}`, `hreflang={HTML_LANG[l]}`, `lang={HTML_LANG[l]}`, `aria-current={l === lang ? 'page' : undefined}`, text `SWITCHER_LABEL[l]`.
- `SiteHeader.astro` ← lines 363–368 (header, `ui-brand`, `ui-nav`, mobile sheet with its two block buttons). Brand: `t('site.name')`; on zh pages also `<span lang="zh-Hant" class="ui-footer-zh">{t('site.nameZh')}</span>` as the README specifies. Nav links → `pathFor(lang, …)` for the five pages, `aria-current` on the active one. Header Book button gets `data-cta="book"` and `href={pathFor(lang,'contact') + '#book'}`.
- `SiteFooter.astro` ← lines 475–480. Includes its Book button (`data-cta="book"`) and a second switcher. Leave "Notice of privacy practices" / "Privacy policy" links as `aria-disabled` spans until the client provides URLs (don't fake a page).
- Mobile menu script ← line 481, moved into `SiteHeader.astro` as `<script>` (Astro bundles it).
- `Button.astro`: renders `<a class={['ui-btn', `ui-btn--${variant}`, size && `ui-btn--${size}`, block && 'ui-btn--block']} href data-cta>` with the icon SVG + `<slot/>`.
- `Icon.astro`: move each inline `<svg class="ui-ico c-ico">` from the mockup into a `name → path data` map (one entry per distinct icon); render the same `<svg>` wrapper.
- `StickyBar.astro` (new): `<div class="ui-sticky" data-sticky-bar>` with Book (`data-cta="book"`, primary) and Message (`data-cta="message"`, secondary, `href="tel:+18009918881"`). Style with Concept C tokens only:

```css
.ui-sticky{position:fixed;inset:auto 0 0 0;display:none;gap:var(--space-1);padding:var(--space-1) var(--gutter-mobile) calc(var(--space-1) + env(safe-area-inset-bottom));background:var(--surface);box-shadow:var(--shadow-float);z-index:50}
.ui-sticky .ui-btn{flex:1}
@media (max-width: 767px){.ui-sticky{display:flex}body{padding-bottom:84px}}
```

Wire all of them into `BaseLayout.astro` around `<slot />`.

- [ ] **Step 4: Run — expect PASS for everything except page-specific axe issues from stub bodies.** Fix any axe violation in chrome components before moving on.
- [ ] **Step 5: Commit** — `git add -A src playwright.config.ts tests package.json package-lock.json && git commit -m "Add Concept C site chrome and the CLAUDE.md rules test suite"`

---

### Task 7: Home page

**Files:**
- Create: `src/components/{Hero,StoryScenes,HowItWorks,DoctorCard,PhotoFrame,FaqAccordion,LocationCard,BookingBand}.astro`
- Modify: `src/features/home/Page.astro`, `src/content/copy/*.json`

**Interfaces:**
- Consumes: `Button`, `Icon`, `makeT`, `pathFor`, `legacyImage`.
- Produces: `<PhotoFrame image?={ImageMetadata} alt placeholder>` (renders the mockup's labeled placeholder when `image` is absent); `<LocationCard name address hours phones mapHref? disabledLabel?>`; `<BookingBand lang>` (has `data-cta-bottom` wrapper, Book button `data-cta="book"`) — reused by every page.

- [ ] **Step 1: Test** — add to `tests/e2e/rules.spec.ts`:

```ts
test('home has every Concept C section, in order', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
  await page.goto('/en/');
  const order = await page.$$eval('main > section', (s) => s.map((x) => x.id || x.className));
  expect(order.map((o) => o.split(' ').find((c) => ['ui-hero', 'how', 'doctor', 'visit', 'faq', 'locations', 'ui-section--band'].includes(c)) ?? o))
    .toEqual(expect.arrayContaining(['ui-hero', 'how', 'doctor', 'visit', 'faq', 'locations', 'ui-section--band']));
});
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Port sections from the EN mockup, verbatim markup, text → keys under `home.*`**
  - `Hero` ← lines 369–397. The "trust chip" (Dr. Woo · 30 years) contains a number → keep it only if `F-…` for the equivalent old-site sentence is approved; otherwise render just "Dr. Paul T. Woo, OD".
  - The intro paper section + `StoryScenes` ← lines 397–426. Keep the illustration SVGs/labeled placeholders exactly as the mockup has them (spec: illustrations don't exist yet).
  - `HowItWorks` ← the `.how` section. `DoctorCard` + `PhotoFrame` ← lines 427–432; pass `legacyImage(<the practice-photo of Dr. Woo from the catalog>)` if one exists, else keep the placeholder.
  - `visit` section ← lines 433–448 (ordered steps). `FaqAccordion` ← `.faq` section (`<details>` ×4; answers stay as the mockup's placeholder text until the client writes them).
  - `LocationCard` ×2 ← `.locations` section. Walnut keeps "Address coming soon" and the disabled "Opening soon" button.
  - `BookingBand` ← lines 449–474.
  - English text: use the mockup's EN text (written from the client brief). Where the old site says the same thing in more detail, you may substitute a line from `docs/legacy-copy/home.txt` — never a flagged one. zh files: every `home.*` key = the placeholder string for that locale.
- [ ] **Step 4: Run all e2e — expect PASS.** Also compare visually: screenshot `/en/` at 1280 and 390 wide next to `design/concepts/_qa/C-picture-book-Homepage-desktop-EN.png`. Differences should be limited to real content.
- [ ] **Step 5: Commit** — `git commit -am "Build the Concept C homepage"` (after `git add src`).

---

### Task 8: About, Ortho-K, Testimonials pages

**Files:**
- Modify: `src/features/{about,ortho-k,testimonials}/Page.astro`, `src/content/copy/*.json`

**Interfaces:**
- Consumes: all Task 6–7 components. Every page ends with `<BookingBand lang>`; every page's first screen has a Book button (`data-cta="book"`) in its hero.

- [ ] **Step 1: Test** — add to rules.spec: each of these pages has exactly one `h1`, and its `main` text contains none of `/\d+\s*%|success rate|most effective|\bbest\b/i`.

```ts
for (const p of ['about/', 'ortho-k/', 'testimonials/']) {
  test(`/en/${p} has one h1 and no banned claims`, async ({ page }) => {
    await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
    await page.goto(`/en/${p}`);
    await expect(page.locator('h1')).toHaveCount(1);
    expect(await page.locator('main').innerText()).not.toMatch(/\d+\s*%|success rate|most effective|\bbest\b/i);
  });
}
```

- [ ] **Step 2: Run — expect FAIL** (stubs have no hero Book button).
- [ ] **Step 3: Compose each page from existing components only** (no new visual patterns):
  - **About:** a short night-band hero (reuse `Hero` with `variant="short"` — a boolean prop that drops the scene art and hills), `DoctorCard` (full bio from `docs/legacy-copy/about.txt`), a `ui-section c-paper` with the practice story paragraphs, `BookingBand`.
  - **Ortho-K:** short hero, intro paragraphs, `HowItWorks`, `StoryScenes`, `FaqAccordion` (questions from `docs/legacy-copy/ortho-k.txt` where present), `BookingBand`.
  - **Testimonials:** short hero, a `ui-grid` of quote cards (`<blockquote class="ui-card">`), only clean sentences, attributed only as they were on the old site (first name/initial) — no photos unless the catalog entry is approved. `BookingBand`.
  - Copy: English from the matching `docs/legacy-copy/*.txt`, or from `docs/copy-review.md` entries whose id is in `approved-claims.json`. zh: placeholder strings.
- [ ] **Step 4: Run all tests — expect PASS.**
- [ ] **Step 5: Commit** — `git add src && git commit -m "Build About, Ortho-K and Testimonials pages"`

---

### Task 9: Worker `POST /booking`

**Files:**
- Create: `workers/comments/src/booking.ts`, `workers/comments/src/booking.test.ts`
- Modify: `workers/comments/src/index.ts`, `workers/comments/package.json` (`"test": "vitest run"`)

**Interfaces:**
- Produces: `POST /booking` JSON `{ parentName, phone, location: 'alhambra'|'walnut', preferredTime, website }` → `201 {ok:true}` | `400 {error, fields: string[]}` | `429 {error}`. KV keys: `booking:<iso>:<uuid>` (TTL 30 days), `rl:<ip>` (TTL 1 hour).

- [ ] **Step 1: Failing tests**

```ts
// workers/comments/src/booking.test.ts
import { describe, it, expect, vi } from 'vitest';
import worker from './index';

function kv(initial: Record<string, string> = {}) {
  const store: Record<string, string> = { ...initial };
  return { store, get: vi.fn(async (k: string) => store[k] ?? null), put: vi.fn(async (k: string, v: string) => { store[k] = v; }) } as any;
}
const env = (k: any) => ({ COMMENTS_KV: k, ALLOWED_ORIGIN: 'https://1234.pasadenaworks.com' });
const post = (body: unknown, ip = '1.1.1.1') => new Request('https://w/booking', {
  method: 'POST', body: JSON.stringify(body), headers: { 'CF-Connecting-IP': ip, 'Content-Type': 'application/json' },
});
const good = { parentName: 'Ann Lee', phone: '(626) 555-0100', location: 'alhambra', preferredTime: 'Tue afternoon', website: '' };

describe('POST /booking', () => {
  it('stores a valid request with a 30-day TTL', async () => {
    const k = kv();
    const res = await worker.fetch(post(good), env(k));
    expect(res.status).toBe(201);
    const [key, , opts] = k.put.mock.calls.find((c: any[]) => c[0].startsWith('booking:'));
    expect(key).toMatch(/^booking:/);
    expect(opts).toEqual({ expirationTtl: 60 * 60 * 24 * 30 });
  });
  it('rejects bad fields and names them', async () => {
    const res = await worker.fetch(post({ ...good, phone: '12', location: 'pasadena', parentName: '' }), env(kv()));
    expect(res.status).toBe(400);
    expect((await res.json() as any).fields.sort()).toEqual(['location', 'parentName', 'phone']);
  });
  it('silently accepts but does not store honeypot submissions', async () => {
    const k = kv();
    const res = await worker.fetch(post({ ...good, website: 'spam.com' }), env(k));
    expect(res.status).toBe(201);
    expect(k.put.mock.calls.some((c: any[]) => c[0].startsWith('booking:'))).toBe(false);
  });
  it('rate limits after 5 per hour per IP', async () => {
    const k = kv({ 'rl:9.9.9.9': '5' });
    const res = await worker.fetch(post(good, '9.9.9.9'), env(k));
    expect(res.status).toBe(429);
  });
  it('ignores unknown fields such as free-text notes', async () => {
    const k = kv();
    await worker.fetch(post({ ...good, notes: 'my child has keratoconus' }), env(k));
    const stored = Object.entries(k.store).find(([key]) => key.startsWith('booking:'))![1] as string;
    expect(stored).not.toContain('keratoconus');
  });
});
```

- [ ] **Step 2: Run — expect FAIL.** `cd workers/comments && npx vitest run src/booking.test.ts`
- [ ] **Step 3: Implement**

```ts
// workers/comments/src/booking.ts
import type { Env } from './index';
const TTL_30D = 60 * 60 * 24 * 30;
const LOCATIONS = ['alhambra', 'walnut'];

export async function handleBooking(request: Request, env: Env, headers: Record<string, string>): Promise<Response> {
  const json = (status: number, body: unknown) =>
    new Response(JSON.stringify(body), { status, headers: { ...headers, 'Content-Type': 'application/json' } });

  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const rlKey = `rl:${ip}`;
  const count = Number((await env.COMMENTS_KV.get(rlKey)) || 0);
  if (count >= 5) return json(429, { error: 'Too many requests. Please call the office.' });

  let body: Record<string, unknown>;
  try { body = await request.json(); } catch { return json(400, { error: 'Invalid JSON', fields: [] }); }
  if (typeof body.website === 'string' && body.website.trim() !== '') return json(201, { ok: true });

  const parentName = String(body.parentName ?? '').trim();
  const phone = String(body.phone ?? '').trim();
  const location = String(body.location ?? '').trim();
  const preferredTime = String(body.preferredTime ?? '').trim();
  const fields: string[] = [];
  if (parentName.length < 1 || parentName.length > 100) fields.push('parentName');
  const digits = phone.replace(/\D/g, '');
  if (digits.length < 10 || digits.length > 15) fields.push('phone');
  if (!LOCATIONS.includes(location)) fields.push('location');
  if (preferredTime.length > 100) fields.push('preferredTime');
  if (fields.length) return json(400, { error: 'Please check the highlighted fields.', fields });

  const createdAt = new Date().toISOString();
  await env.COMMENTS_KV.put(`booking:${createdAt}:${crypto.randomUUID()}`,
    JSON.stringify({ parentName, phone, location, preferredTime, createdAt }), { expirationTtl: TTL_30D });
  await env.COMMENTS_KV.put(rlKey, String(count + 1), { expirationTtl: 3600 });
  return json(201, { ok: true });
}
```

In `index.ts`: `import { handleBooking } from './booking';` and before the 404: `if (request.method === 'POST' && url.pathname === '/booking') return handleBooking(request, env, headers);`

- [ ] **Step 4: Run the whole Worker suite — expect PASS** (existing comment tests too). `npx vitest run`
- [ ] **Step 5: Commit** — `git add workers/comments && git commit -m "Add booking request endpoint to the Worker"`
- [ ] **Step 6: Deploy** — ask the user before `npx wrangler deploy` (it's a live service).

---

### Task 10: Contact page + booking form

**Files:**
- Modify: `src/features/contact/Page.astro`, `src/content/copy/*.json`
- Create: `src/features/contact/booking.js`, `src/components/FormField.astro`, `tests/e2e/booking.spec.ts`

**Interfaces:**
- Consumes: `POST {API}/booking` from Task 9; `API` = `https://1234-review-comments.jimmyc316.workers.dev` (same as `API_BASE` in `design/concepts/_review/inject.js`).
- Produces: `<form id="book" data-booking>` with inputs `parentName`, `phone`, `location` (radio), `preferredTime`, hidden-from-humans `website`.

- [ ] **Step 1: Failing e2e**

```ts
// tests/e2e/booking.spec.ts
import { test, expect } from '@playwright/test';
test.beforeEach(async ({ page }) => page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true')));

test('successful submit shows inline confirmation', async ({ page }) => {
  await page.route('**/booking', (r) => r.fulfill({ status: 201, body: '{"ok":true}' }));
  await page.goto('/en/contact/');
  await page.fill('[name=parentName]', 'Ann Lee');
  await page.fill('[name=phone]', '6265550100');
  await page.check('[name=location][value=alhambra]');
  await page.click('#book [type=submit]');
  await expect(page.locator('#book [role=status]')).toContainText(/thank/i);
});

test('network failure shows error, re-enables, keeps values', async ({ page }) => {
  await page.route('**/booking', (r) => r.abort());
  await page.goto('/en/contact/');
  await page.fill('[name=parentName]', 'Ann Lee');
  await page.fill('[name=phone]', '6265550100');
  await page.check('[name=location][value=alhambra]');
  const submit = page.locator('#book [type=submit]');
  await submit.click();
  await expect(page.locator('#book [role=alert]')).toBeVisible();
  await expect(submit).toBeEnabled();
  await expect(page.locator('[name=parentName]')).toHaveValue('Ann Lee');
});

test('double click sends one request', async ({ page }) => {
  let n = 0;
  await page.route('**/booking', async (r) => { n++; await new Promise((x) => setTimeout(x, 300)); r.fulfill({ status: 201, body: '{"ok":true}' }); });
  await page.goto('/en/contact/');
  await page.fill('[name=parentName]', 'Ann Lee');
  await page.fill('[name=phone]', '6265550100');
  await page.check('[name=location][value=alhambra]');
  await page.locator('#book [type=submit]').dblclick();
  await expect(page.locator('#book [role=status]')).toContainText(/thank/i);
  expect(n).toBe(1);
});

test('server field errors mark the fields', async ({ page }) => {
  await page.route('**/booking', (r) => r.fulfill({ status: 400, body: '{"error":"x","fields":["phone"]}' }));
  await page.goto('/en/contact/');
  await page.fill('[name=parentName]', 'Ann Lee');
  await page.fill('[name=phone]', '6265550100');
  await page.check('[name=location][value=alhambra]');
  await page.click('#book [type=submit]');
  await expect(page.locator('[name=phone]')).toHaveAttribute('aria-invalid', 'true');
});
```

- [ ] **Step 2: Run — expect FAIL.**
- [ ] **Step 3: Build the page**
  - Short hero; two `LocationCard`s + `Contact row` component (phones as `tel:` links); the form section `id="book"` built from `FormField.astro` (port the Concept C "Form field set" component preview markup); `BookingBand` at the bottom.
  - A "Preview — requests are not yet sent to the office" notice above the submit button (`copy.contact.previewNotice`), per spec.
  - No free-text/notes field.
  - `website` honeypot: `<div hidden aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>`.

```js
// src/features/contact/booking.js
const API = 'https://1234-review-comments.jimmyc316.workers.dev'; // same Worker as inject.js API_BASE
const form = document.querySelector('[data-booking]');
if (form) {
  const btn = form.querySelector('[type=submit]');
  const status = form.querySelector('[role=status]');
  const alert = form.querySelector('[role=alert]');
  let sending = false;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (sending) return;
    sending = true; btn.disabled = true; alert.hidden = true; status.textContent = '';
    form.querySelectorAll('[aria-invalid]').forEach((el) => el.removeAttribute('aria-invalid'));
    const data = Object.fromEntries(new FormData(form));
    try {
      const res = await fetch(`${API}/booking`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
      const body = await res.json().catch(() => ({}));
      if (res.ok) { form.reset(); status.textContent = form.dataset.success; return; }
      (body.fields || []).forEach((f) => form.querySelector(`[name=${f}]`)?.setAttribute('aria-invalid', 'true'));
      alert.textContent = res.status === 429 ? form.dataset.ratelimited : form.dataset.invalid;
      alert.hidden = false;
    } catch {
      alert.textContent = form.dataset.network; alert.hidden = false;
    } finally { sending = false; btn.disabled = false; }
  });
}
```

Messages come from `data-success`, `data-invalid`, `data-ratelimited`, `data-network` attributes filled with `t('contact.form.*')`; the network message includes the office phone number.

- [ ] **Step 4: Run all e2e — expect PASS.**
- [ ] **Step 5: Commit** — `git add src tests && git commit -m "Build Contact page with booking request form"`

---

### Task 11: Message button target

**Files:** Modify `src/components/StickyBar.astro`, `src/content/copy/*.json`

- [ ] **Step 1:** Keep `tel:+18009918881` as the Message target (spec: `sms:` only after the client confirms the number takes texts). Add a code comment pointing to that open question.
- [ ] **Step 2:** Test — add to rules.spec: `await expect(page.locator('[data-sticky-bar] [data-cta="message"]')).toHaveAttribute('href', /^(tel|sms):/)`. Run — PASS.
- [ ] **Step 3: Commit.**

---

### Task 12: Deploy workflow + concept move

**Files:**
- Create: `.github/workflows/deploy-site.yml`, `public/_review/gate-only.js` (see below), `tests/e2e/deploy.spec.ts`
- Delete: `.github/workflows/deploy-review-site.yml`

**Interfaces:**
- Produces: deployed layout — `/` site, `/concepts/…` = `design/concepts/` verbatim, `/_review/…` = `design/concepts/_review/` (the concept homepages load `/_review/inject.js` by absolute path), `/concepts/legacy-images/` = `design/legacy-catalog/`.

- [ ] **Step 1: Gate-only script** — the new site pages need the password overlay but not the comments sidebar:

```js
// public/_review/gate-only.js — served at /_review/gate-only.js next to the copied review scripts
import { installGate } from './gate.js';
installGate(document);
```

During dev, `/_review/gate.js` must also resolve: add a tiny Astro integration step or simply copy `design/concepts/_review/gate.js` into `public/_review/` in a `prebuild`/`predev` npm script: `"predev": "node scripts/sync-review.mjs"`, `"prebuild": "node scripts/sync-review.mjs"` where `sync-review.mjs` copies `design/concepts/_review/*.js` (not tests) into `public/_review/`. Add `public/_review/*` except `gate-only.js` to `.gitignore`.

- [ ] **Step 2: Failing deploy test**

```ts
// tests/e2e/deploy.spec.ts — runs against the assembled dist via `npx serve dist`
import { test, expect } from '@playwright/test';
test('moved concept homepage still loads the review script and gate', async ({ page }) => {
  await page.goto('http://localhost:4322/concepts/concepts/C-picture-book/ConceptC-PictureBook-homepage-EN.html');
  await expect(page.locator('#review-gate-overlay')).toBeVisible();
});
test('legacy catalog is gated', async ({ page }) => {
  await page.goto('http://localhost:4322/concepts/legacy-images/');
  await expect(page.locator('#review-gate-overlay')).toBeVisible();
});
test('site root redirects to /en/ and is gated', async ({ page }) => {
  await page.goto('http://localhost:4322/');
  await expect(page).toHaveURL(/\/en\/$/);
  await expect(page.locator('#review-gate-overlay')).toBeVisible();
});
```

Add `scripts/assemble.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
npx astro build
mkdir -p dist/concepts dist/_review
cp -R design/concepts/. dist/concepts/
cp design/concepts/_review/*.js dist/_review/
rm -f dist/_review/*.test.mjs dist/_review/test-setup.mjs
rm -rf dist/concepts/legacy-images && cp -R design/legacy-catalog dist/concepts/legacy-images
cp design/concepts/CNAME dist/CNAME
```

Run: `bash scripts/assemble.sh && (npx serve dist -l 4322 &) && npx playwright test tests/e2e/deploy.spec.ts` — expect FAIL before the script exists, PASS after.

- [ ] **Step 3: Workflow**

```yaml
# .github/workflows/deploy-site.yml
name: Deploy site to GitHub Pages
on:
  push:
    branches: [site/concept-c, design/concepts-import, main]
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: pages, cancel-in-progress: true }
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: '${{ steps.deployment.outputs.page_url }}' }
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run test:unit
      - run: bash scripts/assemble.sh
      - uses: actions/upload-pages-artifact@v3
        with: { path: dist }
      - id: deployment
        uses: actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e # v4
```

`git rm .github/workflows/deploy-review-site.yml`.

- [ ] **Step 4: Commit** — `git add -A .github scripts public .gitignore tests package.json && git commit -m "Deploy Astro site with concepts archived under /concepts/"`
- [ ] **Step 5: Push and verify** — ask the user before pushing (it deploys to the live review domain). After push: watch the Actions run; load `https://1234.pasadenaworks.com/en/`, `/concepts/`, one concept homepage (check an existing comment still shows), `/concepts/legacy-images/`. If HTTPS breaks, clear and re-set `cname` via `gh api` (known quirk).

---

## Final check (before reporting done)

- `npm test` green; `cd workers/comments && npx vitest run` green.
- Screenshots of `/en/`, `/zh-hant/`, `/en/contact/` at 1280 and 390 wide.
- Report to the user: catalog link, count by tag, `docs/copy-review.md` item count, open client questions (office email + sending mechanism, whether the number takes texts, privacy-policy URLs, illustrations, Chinese copy).
