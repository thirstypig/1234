import { test } from 'node:test';
import assert from 'node:assert';
import { isUnlocked, tryUnlock } from './gate.js';

test('tryUnlock returns false for wrong phrase', () => {
  localStorage.clear();
  assert.strictEqual(tryUnlock('wrong phrase'), false);
  assert.strictEqual(isUnlocked(), false);
});

test('tryUnlock returns true for correct phrase and persists', () => {
  localStorage.clear();
  assert.strictEqual(tryUnlock('purplelantern'), true);
  assert.strictEqual(isUnlocked(), true);
});

test('tryUnlock is case-insensitive and trims whitespace', () => {
  localStorage.clear();
  assert.strictEqual(tryUnlock('  PurpleLantern  '), true);
});
