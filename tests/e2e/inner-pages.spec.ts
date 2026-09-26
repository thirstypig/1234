import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
});

for (const p of ['about/', 'ortho-k/', 'testimonials/']) {
  test(`/en/${p} has one h1, real content, and no banned claims`, async ({ page }) => {
    await page.goto(`/en/${p}`);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('main > section')).toHaveCount(await page.locator('main > section').count());
    expect(await page.locator('main > section').count()).toBeGreaterThanOrEqual(3);
    expect(await page.locator('main').innerText()).not.toMatch(/\d+\s*%|success rate|most \w+|\bbest\b|\bfinest\b|\d[\d,]* patients/i);
  });
}

test('testimonials are shown as quotes', async ({ page }) => {
  await page.goto('/en/testimonials/');
  expect(await page.locator('main blockquote').count()).toBeGreaterThanOrEqual(3);
});
