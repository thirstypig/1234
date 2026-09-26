import { test } from 'node:test';
import assert from 'node:assert';
import { isApproved } from './claims.ts';

test('a claim id is approved only when listed', () => {
  assert.strictEqual(isApproved('F-home-1', ['F-about-2']), false);
  assert.strictEqual(isApproved('F-home-1', ['F-home-1']), true);
});
