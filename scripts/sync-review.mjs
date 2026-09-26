// Copies the review gate from the concepts folder so /_review/gate.js resolves in dev and build.
import { cp, readdir } from 'node:fs/promises';
const SRC = 'design/concepts/_review';
for (const f of await readdir(SRC)) {
  if (f.endsWith('.js')) await cp(`${SRC}/${f}`, `public/_review/${f}`);
}
