import { test } from 'node:test';
import assert from 'node:assert';
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

// The repo is public: only images cleared for the site may be tracked in git.
test('only practice-photo or approved legacy images are tracked in git', () => {
  const catalog = JSON.parse(readFileSync('assets/legacy/catalog.json', 'utf8'));
  const ok = new Set(catalog.filter((e) => e.tag === 'practice-photo' || e.approved).map((e) => e.file));
  const tracked = execSync('git ls-files assets/legacy design/legacy-catalog', { encoding: 'utf8' })
    .split('\n').filter((f) => /\.(png|jpe?g|gif|webp|pdf)$/i.test(f));
  assert.deepStrictEqual(tracked.filter((f) => !ok.has(basename(f))), []);
});

// Client-supplied photos: every tracked image must be listed as a staff or office photo.
test('only listed staff or office photos are tracked in assets/practice', () => {
  const list = JSON.parse(readFileSync('assets/practice/photos.json', 'utf8'));
  const ok = new Set(list.filter((e) => ['staff', 'office'].includes(e.subject)).map((e) => e.file));
  const tracked = execSync('git ls-files --cached --others --exclude-standard assets/practice', { encoding: 'utf8' })
    .split('\n').filter((f) => /\.(png|jpe?g|gif|webp|heic)$/i.test(f));
  assert.deepStrictEqual(tracked.filter((f) => !ok.has(basename(f))), []);
});
