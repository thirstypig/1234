import { test } from 'node:test';
import assert from 'node:assert';
import { formatDate, renderSidebar } from './sidebar.js';

test('formatDate renders a readable date', () => {
  assert.strictEqual(formatDate('2026-09-24T10:00:00.000Z'), new Date('2026-09-24T10:00:00.000Z').toLocaleString());
});

test('renderSidebar shows each comment with its date', () => {
  const container = document.createElement('div');
  renderSidebar(container, [
    { text: 'Love this one', createdAt: '2026-09-24T10:00:00.000Z' },
  ]);
  assert.ok(container.textContent.includes('Love this one'));
  assert.ok(container.textContent.includes(formatDate('2026-09-24T10:00:00.000Z')));
});

test('renderSidebar shows a placeholder when there are no comments', () => {
  const container = document.createElement('div');
  renderSidebar(container, []);
  assert.ok(container.textContent.includes('No comments yet'));
});
