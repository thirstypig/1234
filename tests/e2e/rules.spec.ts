import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const LOCALES = ['en', 'zh-hans', 'zh-hant'];
const PAGES = ['', 'about/', 'ortho-k/', 'contact/', 'testimonials/'];
const ALL = LOCALES.flatMap((l) => PAGES.map((p) => `/${l}/${p}`));

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
});

for (const path of ALL) {
  test.describe(path, () => {
    test('switcher links to the same page in each language', async ({ page }) => {
      await page.goto(path);
      const sub = path.split('/').slice(2).join('/');
      for (const l of LOCALES) {
        await expect(page.locator(`.ui-lang a[href="/${l}/${sub}"]`).first()).toBeVisible();
      }
    });

    test('Book a consultation in first screen and at bottom', async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto(path);
      await expect(page.locator('[data-cta="book"]').first()).toBeInViewport();
      await expect(page.locator('[data-cta-bottom] [data-cta="book"]').first()).toBeAttached();
    });

    test('no logo image in header', async ({ page }) => {
      await page.goto(path);
      await expect(page.locator('header img, header svg.logo')).toHaveCount(0);
    });

    test('WCAG AA (axe)', async ({ page }) => {
      await page.goto(path);
      const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
      expect(r.violations.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).join(', ')}`)).toEqual([]);
    });

    if (path.startsWith('/zh')) {
      test('Chinese body >= 17px, line-height >= 1.7', async ({ page }) => {
        await page.goto(path);
        const bad = await page.$$eval('main p', (ps) =>
          ps
            .map((p) => {
              const s = getComputedStyle(p);
              const fs = parseFloat(s.fontSize);
              const lh = s.lineHeight === 'normal' ? 1.2 : parseFloat(s.lineHeight) / fs;
              return fs < 17 || lh < 1.7 ? `${p.textContent?.slice(0, 20)} ${fs}px/${lh.toFixed(2)}` : null;
            })
            .filter(Boolean),
        );
        expect(bad).toEqual([]);
      });
    }

    test('mobile sticky Book/Message bar', async ({ page }) => {
      await page.setViewportSize({ width: 390, height: 844 });
      await page.goto(path);
      await page.mouse.wheel(0, 3000);
      await expect(page.locator('[data-sticky-bar] [data-cta="book"]')).toBeInViewport();
      await expect(page.locator('[data-sticky-bar] [data-cta="message"]')).toBeInViewport();
      await expect(page.locator('[data-sticky-bar] [data-cta="message"]')).toHaveAttribute('href', /^(tel|sms):/);
    });
  });
}
