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
    // Word-for-word patient reviews are exempt (owner decision 2026-09-28); everything else is checked.
    const text = await page.locator('main').evaluate((m) => {
      const c = m.cloneNode(true) as HTMLElement;
      c.querySelectorAll('blockquote.c-quote').forEach((q) => q.remove());
      return c.innerText;
    });
    expect(text).not.toMatch(/\d+\s*%|success rate|most \w+|\bbest\b|\bfinest\b|\d[\d,]* patients/i);
  });
}

test('testimonials are shown as quotes', async ({ page }) => {
  await page.goto('/en/testimonials/');
  expect(await page.locator('main blockquote').count()).toBeGreaterThanOrEqual(3);
});

for (const l of ['en', 'zh-hans', 'zh-hant']) {
  test(`/${l}/testimonials/ shows all 21 old-site reviews in their own language`, async ({ page }) => {
    await page.goto(`/${l}/testimonials/`);
    await expect(page.locator('main blockquote.c-quote')).toHaveCount(21);
    await expect(page.locator('main blockquote.c-quote[lang="en"]')).toHaveCount(18);
    await expect(page.locator('main blockquote.c-quote[lang^="zh"]')).toHaveCount(3);
    await expect(page.locator('main blockquote.c-quote').filter({ hasText: 'saving my vision' })).toHaveCount(1);
  });
}

for (const l of ['en', 'zh-hans', 'zh-hant']) {
  test(`/${l}/community/ shows the 9 event photos, each described`, async ({ page }) => {
    await page.goto(`/${l}/community/`);
    await expect(page.locator('h1')).toHaveCount(1);
    const imgs = page.locator('main .c-events img');
    await expect(imgs).toHaveCount(9);
    for (const alt of await imgs.evaluateAll((els) => els.map((e) => e.getAttribute('alt') ?? ''))) expect(alt.trim()).not.toBe('');
  });

  test(`/${l}/ links to the Community page from the footer`, async ({ page }) => {
    await page.goto(`/${l}/`);
    await expect(page.locator(`footer a[href="/${l}/community/"]`)).toHaveCount(1);
  });
}
