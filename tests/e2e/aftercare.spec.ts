import { test, expect } from '@playwright/test';

for (const lang of ['en', 'zh-hans', 'zh-hant'] as const) {
  test(`/${lang}/ortho-k/ shows the aftercare lists and the practice's flyer`, async ({ page }) => {
    await page.goto(`/${lang}/ortho-k/`);
    const sec = page.locator('#aftercare');
    await expect(sec.locator('h2')).toHaveCount(1);
    await expect(sec.locator('h3')).toHaveCount(2);
    await expect(sec.locator('.c-service').nth(0).locator(':scope > ul > li')).toHaveCount(6);
    await expect(sec.locator('.c-service').nth(1).locator(':scope > ul > li')).toHaveCount(9);
    const img = sec.locator('.c-flyer img');
    await expect(img).toHaveAttribute('alt', /.+/);
    await img.scrollIntoViewIfNeeded();
    await expect.poll(() => img.evaluate((i: HTMLImageElement) => i.naturalWidth)).toBeGreaterThan(0);
  });
}

test('the 404 page speaks all three languages and links each home page', async ({ page }) => {
  await page.goto('/404.html');
  await expect(page.locator('h1')).toHaveCount(1);
  for (const href of ['/en/', '/zh-hans/', '/zh-hant/']) await expect(page.locator(`a[href="${href}"]`)).toHaveCount(1);
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex');
});
