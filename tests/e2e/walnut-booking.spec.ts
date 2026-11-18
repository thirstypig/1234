import { test, expect } from '@playwright/test';
import { BOOKING_FORM_ENABLED } from '../../src/lib/cta';

// Owner, 2026-11-07 (N-24): Walnut is a plain location with a number to call, and
// the booking form is hidden until requests reach the office.
const LANGS = ['en', 'zh-hans', 'zh-hant'] as const;

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
});

for (const l of LANGS) {
  test(`/${l}/ Walnut card is a location with a number to call, not "opening soon"`, async ({ page }) => {
    await page.goto(`/${l}/`);
    const walnut = page.locator('#locations .ui-loc').nth(1);
    await expect(walnut.locator('a[href="tel:16262825388"]')).toHaveCount(1);
    await expect(walnut.locator('[aria-disabled="true"]')).toHaveCount(0);
    expect(await page.locator('body').innerText()).not.toMatch(/opening soon|即將開業|即将开业/i);
  });

  for (const slug of ['terms', 'notice-of-privacy-practices']) {
    test(`/${l}/${slug}/ treats Walnut as open`, async ({ page }) => {
      await page.goto(`/${l}/${slug}/`);
      expect(await page.locator('main').innerText()).not.toMatch(/opening soon|when it opens|即將|即将/i);
    });
  }

  test.describe(() => {
    test.skip(BOOKING_FORM_ENABLED, 'only while the form is hidden');

    test(`/${l}/contact/ has no booking form and every Book link goes to Call`, async ({ page }) => {
      await page.goto(`/${l}/contact/`);
      await expect(page.locator('form')).toHaveCount(0);
      await expect(page.locator('#call a[href="tel:+16262825388"]')).toBeVisible();
      await expect(page.locator('a[href$="#book"]')).toHaveCount(0);
      for (const card of await page.locator('#locations .ui-loc').all()) {
        await expect(card.locator('a[href="tel:+16262825388"]')).toHaveCount(1);
      }
    });

    test(`/${l}/ Book a consultation takes you to the Call section`, async ({ page }) => {
      await page.goto(`/${l}/`);
      const book = page.locator('main [data-cta="book"]').first();
      await expect(book).toHaveAttribute('href', `/${l}/contact/#call`);
      await book.click();
      await expect(page.locator('#call')).toBeInViewport();
    });
  });
}
