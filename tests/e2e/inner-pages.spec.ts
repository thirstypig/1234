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
  test(`/${l}/community/ shows the 17 event and old-site photos, each described and captioned`, async ({ page }) => {
    await page.goto(`/${l}/community/`);
    await expect(page.locator('h1')).toHaveCount(1);
    const imgs = page.locator('main .c-events img');
    await expect(imgs).toHaveCount(17);
    for (const alt of await imgs.evaluateAll((els) => els.map((e) => e.getAttribute('alt') ?? ''))) expect(alt.trim()).not.toBe('');
    await expect(page.locator('main .c-events figure figcaption')).toHaveCount(17);
  });

  test(`/${l}/ links to the Community page from the footer`, async ({ page }) => {
    await page.goto(`/${l}/`);
    await expect(page.locator(`footer a[href="/${l}/community/"]`)).toHaveCount(1);
  });
}

test('every review is attributed to its author, as on the old site', async ({ page }) => {
  await page.goto('/en/testimonials/');
  await expect(page.locator('main figure.c-review figcaption')).toHaveCount(21);
  const martin = page.locator('main figure.c-review').filter({ hasText: 'saving my vision' });
  await expect(martin.locator('figcaption')).toHaveText(/Martin M\./);
  const johnny = page.locator('main figure.c-review').filter({ hasText: 'Dr. Woo then explained the technology' });
  await expect(johnny.locator('figcaption')).toHaveText(/Johnny C\./);
  const fausto = page.locator('main figure.c-review').filter({ hasText: 'VIPOK' });
  await expect(fausto.locator('figcaption')).toHaveText(/Fausto K\./);
});

test('the About gallery includes the two remaining practice photos', async ({ page }) => {
  await page.goto('/en/about/');
  await expect(page.locator('main .c-gallery img')).toHaveCount(10);
});

for (const l of ['en', 'zh-hans', 'zh-hant']) {
  for (const [slug, zh] of [['eye-exams', '兒童視力檢查不良'], ['eye-surface', '眼睛表面有異物的刺激']]) {
    test(`/${l}/${slug}/ shows the old-site Chinese text and is in the main nav`, async ({ page }) => {
      await page.goto(`/${l}/${slug}/`);
      await expect(page.locator('h1')).toHaveCount(1);
      await expect(page.locator('main [lang="zh-Hant"]').filter({ hasText: zh }).first()).toBeVisible();
      await expect(page.locator(`header nav a[href="/${l}/${slug}/"]`)).toHaveCount(1);
    });
  }
}

for (const w of [1024, 1100, 1200, 1280]) {
  for (const l of ['en', 'zh-hant']) {
    test(`/${l}/ header fits at ${w}px with no sideways scroll`, async ({ page }) => {
      await page.setViewportSize({ width: w, height: 800 });
      await page.goto(`/${l}/`);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    });
  }
}
