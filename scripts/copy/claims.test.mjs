import { test } from 'node:test';
import assert from 'node:assert';
import { flagClaims } from './claims.mjs';

test('clean sentence passes', () => {
  assert.deepStrictEqual(flagClaims('Lenses are worn while your child sleeps.'), []);
});
test('percent and success rate', () => {
  assert.ok(flagClaims('Ortho-K has a 95% success rate.').includes('statistic'));
  assert.ok(flagClaims('Ortho-K has a 95% success rate.').includes('success-rate'));
});
test('superlatives', () => {
  assert.ok(flagClaims('The most effective treatment for myopia.').includes('superlative'));
  assert.ok(flagClaims('We are the best clinic in the San Gabriel Valley.').includes('superlative'));
  assert.ok(flagClaims('A leading Ortho-K provider.').includes('superlative'));
});
test('patient counts and guarantees', () => {
  assert.ok(flagClaims('Over 5,000 children treated.').includes('patient-count'));
  assert.ok(flagClaims('Results are guaranteed.').includes('guarantee'));
});
test('years of experience is flagged for review, not auto-cut', () => {
  assert.ok(flagClaims('Dr. Woo has 30 years of experience.').includes('number'));
});

import { splitSentences } from './claims.mjs';

test('any "most <adjective>" and "finest/first" superlatives are flagged', () => {
  assert.ok(flagClaims('He is one of the most experienced doctors in the United States.').includes('superlative'));
  assert.ok(flagClaims('We use the finest equipment.').includes('superlative'));
  assert.ok(flagClaims('First Asian doctor to lecture at the conference.').includes('superlative'));
});
test('splitSentences keeps titles like Dr. attached', () => {
  assert.deepStrictEqual(splitSentences('Children have been treated by Dr. Woo. He opened in 1988.\nNext line here'),
    ['Children have been treated by Dr. Woo.', 'He opened in 1988.', 'Next line here']);
});
