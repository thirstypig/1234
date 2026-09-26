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
