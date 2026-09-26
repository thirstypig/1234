import { mkdir, writeFile } from 'node:fs/promises';
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
const escapeRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

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
    const tag = html.match(new RegExp(`<img[^>]*${escapeRe(file)}[^>]*>`, 'i'))?.[0] || '';
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
    if (r.ok && (r.headers.get('content-type') || '').startsWith('image/')) {
      assets.set(u, { sourcePages: new Set(), alt: '', context: '' });
      orphans.push(u);
      break;
    }
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
