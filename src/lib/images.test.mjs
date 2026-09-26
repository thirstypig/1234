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
