import { test, expect } from '@playwright/test';
import { BOOKING_FORM_ENABLED } from '../../src/lib/cta';

// The owner's comments of 2026-11-07 (docs/copy-review.md, N-23).
const LANGS = ['en', 'zh-hans', 'zh-hant'] as const;
const PAGES = ['', 'about/', 'ortho-k/', 'contact/', 'testimonials/', 'community/'];

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
});

for (const l of LANGS) {
  for (const p of PAGES) {
    test(`/${l}/${p} shows no hours, placeholder copy, insurance list or exact patient count`, async ({ page }) => {
      await page.goto(`/${l}/${p}`);
      const text = await page.locator('body').innerText();
      expect(text).not.toMatch(/12–6|12 點|12点|coming soon|即將公布|即将公布/i);
      expect(text).not.toMatch(/placeholder|暫定|暂定/i);
      expect(text).not.toMatch(/EyeMed|MES Vision|Allied Physicians/);
      expect(text).not.toContain('41,879');
      // Contact's booking form carries a "Preview" label while it is shown.
      if (p !== 'contact/' || !BOOKING_FORM_ENABLED) await expect(page.locator('.ui-draft')).toHaveCount(0);
    });
  }

  test(`/${l}/ortho-k/ keeps only the answered parent question`, async ({ page }) => {
    await page.goto(`/${l}/ortho-k/`);
    await expect(page.locator('#faq details')).toHaveCount(1);
  });
}

test('About says over 40,000 patients', async ({ page }) => {
  await page.goto('/en/about/');
  await expect(page.locator('main')).toContainText('over 40,000 patients');
});

test('Ortho-K lenses are described as semi-hard in all three languages', async ({ page }) => {
  for (const [l, word] of [['en', 'semi-hard'], ['zh-hans', '半硬式'], ['zh-hant', '半硬式']]) {
    await page.goto(`/${l}/ortho-k/`);
    await expect(page.locator('main')).toContainText(word);
    expect(await page.locator('main').innerText()).not.toMatch(/semi-soft|半軟|半软/);
  }
});
