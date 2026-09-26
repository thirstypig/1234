import { readFile, writeFile, mkdir, cp, rm } from 'node:fs/promises';
const catalog = JSON.parse(await readFile('assets/legacy/catalog.json', 'utf8'));
// The repo and the preview site are public: only cleared images leave this machine.
const cleared = (c) => c.tag === 'practice-photo' || c.approved;
await rm('assets/legacy/site', { recursive: true, force: true });
await mkdir('assets/legacy/site', { recursive: true });
for (const c of catalog.filter(cleared)) await cp(`assets/legacy/originals/${c.file}`, `assets/legacy/site/${c.file}`);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[ch]);
const tags = [...new Set(catalog.map((c) => c.tag))].sort();
const cards = catalog.map((c) => `
  <figure class="card" data-tag="${esc(c.tag)}">
    ${!cleared(c) ? `<div class="held">Not published online.<br>Open <code>assets/legacy/originals/${esc(c.file)}</code> locally.</div>`
      : /\.pdf$/i.test(c.file) ? `<a class="pdf" href="img/${esc(c.file)}">PDF: ${esc(c.file)}</a>`
      : `<img loading="lazy" src="img/${esc(c.file)}" alt="${esc(c.alt || c.note || c.file)}">`}
    <figcaption><b>${esc(c.file)}</b> · <span class="tag">${esc(c.tag)}</span>${c.orphan ? ' · orphan' : ''}<br>
    ${c.note ? `<i>${esc(c.note)}</i><br>` : ''}${c.width ?? '?'}×${c.height ?? '?'} · ${(c.bytes / 1024).toFixed(0)} KB<br>
    <small>${c.sourcePages.map((p) => esc(new URL(p).pathname)).join(', ') || 'not linked from any page'}</small></figcaption>
  </figure>`).join('');
await writeFile('design/legacy-catalog/index.html', `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Legacy images — 1234 Ortho-K</title>
<style>body{font:16px/1.5 system-ui;margin:16px;background:#fff;color:#222}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.card{margin:0;border:1px solid #ddd;border-radius:8px;padding:8px}.card img{width:100%;height:160px;object-fit:contain;background:#f4f4f4}
.pdf,.held{display:flex;height:160px;align-items:center;justify-content:center;text-align:center;background:#f4f4f4;padding:8px}
.tag{font-weight:600}button{font:inherit;padding:4px 10px;margin:2px}button[aria-pressed=true]{background:#1F3563;color:#fff}</style></head><body>
<h1>Images from 1234orthok.com (${catalog.length})</h1>
<p>Only <b>practice-photo</b> images are used on the new site automatically. Everything else needs sign-off before it can appear.</p>\n<p>Patient photos and images still under review are <b>not published online</b>; their thumbnails are shown only on the local copy of this catalog.</p>
<p>${['all', ...tags].map((t) => `<button type="button" data-f="${esc(t)}" aria-pressed="${t === 'all'}">${esc(t)} (${t === 'all' ? catalog.length : catalog.filter((c) => c.tag === t).length})</button>`).join(' ')}</p>
<div class="grid">${cards}</div>
<script>document.querySelectorAll('button[data-f]').forEach(b=>b.onclick=()=>{document.querySelectorAll('button[data-f]').forEach(x=>x.setAttribute('aria-pressed',x===b));
document.querySelectorAll('.card').forEach(c=>c.hidden=b.dataset.f!=='all'&&c.dataset.tag!==b.dataset.f)});</script>
<script type="module" src="/_review/gate-only.js"></script></body></html>\n`);
console.log('wrote design/legacy-catalog/index.html');
