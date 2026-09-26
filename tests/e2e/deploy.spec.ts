import { test, expect } from '@playwright/test';

test('concept homepage keeps its old URL and still loads the review script and gate', async ({ page }) => {
  await page.goto('/concepts/C-picture-book/ConceptC-PictureBook-homepage-EN.html');
  await expect(page.locator('#review-gate-overlay')).toBeVisible();
});

test('concept gallery is served under /concepts/ and its links work', async ({ page, request }) => {
  const res = await page.goto('/concepts/');
  expect(res?.status()).toBe(200);
  const hrefs = await page.$$eval('a[href]', (as) => as.map((a) => (a as HTMLAnchorElement).href).filter((h) => h.startsWith(location.origin)));
  expect(hrefs.length).toBeGreaterThan(10);
  for (const h of hrefs.slice(0, 5)) expect((await request.get(h)).status(), h).toBe(200);
});

test('legacy catalog is gated, shows images, and filters by tag', async ({ page }) => {
  await page.goto('/concepts/legacy-images/');
  await expect(page.locator('#review-gate-overlay')).toBeVisible();
  await page.evaluate(() => localStorage.setItem('1234-review-unlocked', 'true'));
  await page.reload();
  const first = page.locator('.card img').first();
  await expect(first).toBeVisible();
  expect(await first.evaluate((img: HTMLImageElement) => img.naturalWidth)).toBeGreaterThan(0);
  await page.click('button[data-f="practice-photo"]');
  await expect(page.locator('.card:visible')).toHaveCount(12);
});

test('site root redirects to /en/ and is gated', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveURL(/\/en\/$/);
  await expect(page.locator('#review-gate-overlay')).toBeVisible();
});
