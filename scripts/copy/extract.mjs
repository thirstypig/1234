import { writeFile, mkdir } from 'node:fs/promises';
import { flagClaims, splitSentences } from './claims.mjs';

const PAGES = { home: '', about: 'about.html', 'ortho-k': 'ortho.html', contact: 'contact-us.html', testimonials: 'testimonials.html' };
const HAN = /\p{Script=Han}/u;
await mkdir('docs/legacy-copy', { recursive: true });
await mkdir('src/content', { recursive: true });
let review = `# Copy review\n\nSentences from the old site that break the CLAUDE.md copy rules.\nMark each: **keep** (add its id to \`src/content/approved-claims.json\`), **cut**, or **rewrite** (write the new text under it).\n\n`;
review += `## Facts that differ from the client brief\n\n- Old site lists **Rowland Heights**; brief and Concept C say **Walnut**. Using Walnut.\n- Old site hours (Mon–Wed 12–6 …) differ from Concept C (Tue & Fri 12–6, Sat 12–4). Using Concept C.\n- Some testimonials may be copied from Yelp or Google reviews. Confirm the practice may republish them, and whether to show reviewers' names.\n\n`;

for (const [page, path] of Object.entries(PAGES)) {
  const html = await (await fetch(`https://1234orthok.com/${path}`)).text();
  const text = html.replace(/<(script|style|nav|header|footer)[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<br\s*\/?>|<\/(p|div|h\d|li)>/gi, '\n').replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&#39;|&rsquo;/g, "'").replace(/&quot;/g, '"');
  const sentences = splitSentences(text)
    .filter((s) => s.length > 20 && !HAN.test(s));
  const zh = [...new Set(text.split('\n').map((s) => s.replace(/\s+/g, ' ').trim()).filter((s) => HAN.test(s)))];
  const clean = [];
  const flagged = [];
  for (const s of [...new Set(sentences)]) (flagClaims(s).length ? flagged : clean).push(s);
  await writeFile(`docs/legacy-copy/${page}.txt`, clean.join('\n') + '\n');
  if (zh.length) await writeFile(`docs/legacy-copy/${page}.zh-Hant.reference.txt`, zh.join('\n') + '\n');
  if (page === 'testimonials') {
    // Keep each review whole; mark reviews containing any flagged sentence.
    const paras = [...new Set(text.split('\n').map((s) => s.replace(/\s+/g, ' ').trim()).filter((s) => s.length > 40 && !HAN.test(s)))];
    // A bare number ("my son, 9") isn't a claim in a personal review; the other rules still block.
    const reasons = (p) => [...new Set(splitSentences(p).flatMap(flagClaims))].filter((r) => r !== 'number');
    const out = paras.map((p) => (reasons(p).length ? `[FLAGGED: ${reasons(p).join(', ')}] ${p}` : p));
    await writeFile('docs/legacy-copy/testimonials.reviews.txt', out.join('\n\n') + '\n');
  }
  review += `## ${page}\n\n`;
  flagged.forEach((s, i) => { review += `- [ ] **F-${page}-${i + 1}** (${flagClaims(s).join(', ')}): ${s}\n`; });
  if (!flagged.length) review += '_Nothing flagged._\n';
  review += '\n';
  console.log(page, 'clean', clean.length, 'flagged', flagged.length, 'zh lines', zh.length);
}
await writeFile('docs/copy-review.md', review);
await writeFile('src/content/approved-claims.json', '[]\n');
console.log('wrote docs/copy-review.md and docs/legacy-copy/');
