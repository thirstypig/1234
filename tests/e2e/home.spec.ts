import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
});

test('home has every Concept C section, in order', async ({ page }) => {
  await page.goto('/en/');
  const marks = await page.$$eval('main > section', (s) =>
    s.map((x) => x.id || ['ui-hero', 'ui-section--band'].find((c) => x.classList.contains(c)) || 'intro'),
  );
  expect(marks).toEqual(['ui-hero', 'intro', 'how', 'doctor', 'visit', 'locations', 'ui-section--band']);
});

test('approved credentials are shown on the doctor card', async ({ page }) => {
  await page.goto('/en/');
  await expect(page.locator('#doctor')).toContainText('Over 30 years');
  await expect(page.locator('#doctor')).toContainText('Global Orthokeratology');
});

test('Dr. Woo photo comes from the approved legacy catalog', async ({ page }) => {
  await page.goto('/en/');
  await expect(page.locator('#doctor img')).toHaveCount(1);
  await expect(page.locator('#doctor img')).toHaveAttribute('alt', /Dr\. .*Woo/);
});

test('the Walnut card shows its address and the clinic sign photo', async ({ page }) => {
  await page.goto('/en/');
  const walnut = page.locator('#locations .ui-loc').nth(1);
  await expect(walnut).toContainText('20265 Valley Blvd., #E');
  await expect(walnut).toContainText('Walnut, CA 91789');
  await expect(walnut.locator('img')).toHaveCount(1);
});
