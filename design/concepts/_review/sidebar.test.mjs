import { test } from 'node:test';
import assert from 'node:assert';
import { formatDate, renderSidebar, positionFromClick, renderPins } from './sidebar.js';

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

test('renderSidebar marks pinned comments distinctly from general ones', () => {
  const container = document.createElement('div');
  renderSidebar(container, [
    { text: 'Pinned one', createdAt: '2026-09-24T10:00:00.000Z', xPercent: 10, yPercent: 10 },
    { text: 'General one', createdAt: '2026-09-24T11:00:00.000Z' },
  ]);
  const items = container.querySelectorAll('.review-comment');
  assert.strictEqual(items.length, 2);
  assert.ok(items[0].querySelector('.review-comment-pin-badge'));
  assert.strictEqual(items[1].querySelector('.review-comment-pin-badge'), null);
});

test('renderPins wires a click handler that receives the comment', () => {
  const container = document.createElement('div');
  let clicked = null;
  renderPins(container, [
    { text: 'Move this down', createdAt: '2026-09-24T10:00:00.000Z', xPercent: 50, yPercent: 20 },
  ], (comment) => { clicked = comment; });
  container.querySelector('.review-pin').dispatchEvent(new Event('click', { bubbles: true }));
  assert.strictEqual(clicked.text, 'Move this down');
});

test('positionFromClick converts a click point to page-relative percentages', () => {
  const pos = positionFromClick({
    pageX: 300,
    pageY: 900,
    fullWidth: 1200,
    fullHeight: 3000,
  });
  assert.strictEqual(pos.xPercent, 25);
  assert.strictEqual(pos.yPercent, 30);
});

test('positionFromClick clamps to 0-100 even with a click at the very edge', () => {
  const pos = positionFromClick({ pageX: 1200, pageY: 0, fullWidth: 1200, fullHeight: 3000 });
  assert.strictEqual(pos.xPercent, 100);
  assert.strictEqual(pos.yPercent, 0);
});

test('renderPins places one pin element per comment that has a position', () => {
  const container = document.createElement('div');
  renderPins(container, [
    { text: 'Move this down', createdAt: '2026-09-24T10:00:00.000Z', xPercent: 50, yPercent: 20 },
    { text: 'No position on this one', createdAt: '2026-09-24T11:00:00.000Z' },
  ]);
  const pins = container.querySelectorAll('.review-pin');
  assert.strictEqual(pins.length, 1);
  assert.strictEqual(pins[0].style.left, '50%');
  assert.strictEqual(pins[0].style.top, '20%');
});
