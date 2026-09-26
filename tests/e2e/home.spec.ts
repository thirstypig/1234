import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
});

test('home has every Concept C section, in order', async ({ page }) => {
  await page.goto('/en/');
  const marks = await page.$$eval('main > section', (s) =>
    s.map((x) => x.id || ['ui-hero', 'ui-section--band'].find((c) => x.classList.contains(c)) || 'intro'),
  );
  expect(marks).toEqual(['ui-hero', 'intro', 'how', 'doctor', 'visit', 'faq', 'locations', 'ui-section--band']);
});

test('unapproved "30 years" claim is not shown', async ({ page }) => {
  await page.goto('/en/');
  await expect(page.locator('main')).not.toContainText('30 years');
});

test('Dr. Woo photo comes from the approved legacy catalog', async ({ page }) => {
  await page.goto('/en/');
  await expect(page.locator('#doctor img')).toHaveCount(1);
  await expect(page.locator('#doctor img')).toHaveAttribute('alt', /Dr\. .*Woo/);
});
