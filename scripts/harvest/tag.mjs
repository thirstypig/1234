import { readFile, writeFile } from 'node:fs/promises';
import { suggestTag } from './lib.mjs';
const path = 'assets/legacy/catalog.json';
const catalog = JSON.parse(await readFile(path, 'utf8'));
for (const e of catalog) if (e.tag === null) e.tag = suggestTag(e);
await writeFile(path, JSON.stringify(catalog, null, 2) + '\n');
const counts = {};
for (const e of catalog) counts[e.tag] = (counts[e.tag] || 0) + 1;
console.log(counts);
