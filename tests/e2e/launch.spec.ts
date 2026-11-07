import { test, expect } from '@playwright/test';

// The default build is the live site (1234orthok.com): indexable, no review overlay.
test('live pages have no noindex, no review overlay, and a canonical on www.1234orthok.com', async ({ page }) => {
  await page.goto('/en/about/');
  await expect(page.locator('meta[name="robots"]')).toHaveCount(0);
  await expect(page.locator('script[src*="_review"]')).toHaveCount(0);
  await expect(page.locator('#review-gate-overlay')).toHaveCount(0);
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', 'https://www.1234orthok.com/en/about/');
});

test('hreflang alternates point at the live domain', async ({ page }) => {
  await page.goto('/zh-hant/');
  const hrefs = await page.$$eval('link[rel="alternate"]', (ls) => ls.map((l) => (l as HTMLLinkElement).href));
  expect(hrefs).toHaveLength(3);
  for (const h of hrefs) expect(h.startsWith('https://www.1234orthok.com/')).toBe(true);
});

test('live pages load Google Analytics with Google signals off', async ({ page }) => {
  await page.goto('/en/');
  await expect(page.locator('script[src="https://www.googletagmanager.com/gtag/js?id=G-ZS9T686F3W"]')).toHaveCount(1);
  const inline = await page.locator('script:not([src])').allTextContents();
  expect(inline.some((t) => t.includes('allow_google_signals: false') && t.includes('allow_ad_personalization_signals: false'))).toBe(true);
});

test('"/" forwards straight to the English home without showing a link page', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveURL(/\/en\/$/);
  await expect(page.locator('h1')).toHaveCount(1);
});
