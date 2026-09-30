import { test, expect } from '@playwright/test';
import en from '../../src/content/copy/en.json' with { type: 'json' };

// Old-site claims the owner approved (2026-09-29, src/content/approved-claims.json) are exempt.
const APPROVED = [...Object.values(en.claims).filter((v) => v !== en.claims.credentialsLabel), en.doctor.years];

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
    let text = await page.locator('main').evaluate((m) => {
      const c = m.cloneNode(true) as HTMLElement;
      c.querySelectorAll('blockquote.c-quote').forEach((q) => q.remove());
      return c.innerText;
    });
    for (const claim of APPROVED) text = text.replaceAll(claim, '');
    expect(text).not.toMatch(/\d+\s*%|success rate|most \w+|\bbest\b|\bfinest\b|\d[\d,]* patients/i);
  });
}

test('testimonials are shown as quotes', async ({ page }) => {
  await page.goto('/en/testimonials/');
  expect(await page.locator('main blockquote').count()).toBeGreaterThanOrEqual(3);
});

for (const l of ['en', 'zh-hans', 'zh-hant']) {
  test(`/${l}/testimonials/ shows the 12 public reviews and the results note`, async ({ page }) => {
    await page.goto(`/${l}/testimonials/`);
    await expect(page.locator('main blockquote.c-quote')).toHaveCount(12);
    await expect(page.locator('main blockquote.c-quote[lang="en"]')).toHaveCount(12);
    await expect(page.locator('main .c-disclaimer')).toHaveCount(1);
    await expect(page.locator('main blockquote.c-quote').filter({ hasText: 'saving my vision' })).toHaveCount(1);
  });
}

for (const l of ['en', 'zh-hans', 'zh-hant']) {
  test(`/${l}/community/ shows the 14 public community photos, each described and captioned`, async ({ page }) => {
    await page.goto(`/${l}/community/`);
    await expect(page.locator('h1')).toHaveCount(1);
    const imgs = page.locator('main .c-events img');
    await expect(imgs).toHaveCount(14);
    for (const alt of await imgs.evaluateAll((els) => els.map((e) => e.getAttribute('alt') ?? ''))) expect(alt.trim()).not.toBe('');
    await expect(page.locator('main .c-events figure figcaption')).toHaveCount(14);
  });

  test(`/${l}/testimonials/ shows the 23 cleared patient photos, each described`, async ({ page }) => {
    await page.goto(`/${l}/testimonials/`);
    const imgs = page.locator('main .c-gallery img');
    await expect(imgs).toHaveCount(23);
    for (const alt of await imgs.evaluateAll((els) => els.map((e) => e.getAttribute('alt') ?? ''))) expect(alt.trim()).not.toBe('');
  });

  test(`/${l}/ links to the Community page from the footer`, async ({ page }) => {
    await page.goto(`/${l}/`);
    await expect(page.locator(`footer a[href="/${l}/community/"]`)).toHaveCount(1);
  });
}

test('every review is attributed to its author, as on the old site', async ({ page }) => {
  await page.goto('/en/testimonials/');
  await expect(page.locator('main figure.c-review figcaption')).toHaveCount(12);
  const martin = page.locator('main figure.c-review').filter({ hasText: 'saving my vision' });
  await expect(martin.locator('figcaption')).toHaveText(/Martin M\./);
  const johnny = page.locator('main figure.c-review').filter({ hasText: 'Dr. Woo then explained the technology' });
  await expect(johnny.locator('figcaption')).toHaveText(/Johnny C\./);
  const colin = page.locator('main figure.c-review').filter({ hasText: 'laboratory work' });
  await expect(colin.locator('figcaption')).toHaveText(/Colin C\./);
  await expect(page.locator('main figure.c-review').filter({ hasText: 'VIPOK' })).toHaveCount(0);
});

test('the About gallery includes the two remaining practice photos', async ({ page }) => {
  await page.goto('/en/about/');
  await expect(page.locator('main .c-gallery img')).toHaveCount(10);
});

const OLD_PAGES = {
  'eye-exams': { en: 'Why does my child need dilating eye drops?', 'zh-hans': '为什么要做散瞳检查？', 'zh-hant': '為什麼要做散瞳檢查？' },
  'eye-surface': { en: 'Eye stones, also called conjunctival stones', 'zh-hans': '眼结石也称为结膜结石', 'zh-hant': '眼結石也稱為結膜結石' },
} as const;
const HTML_LANG = { en: 'en', 'zh-hans': 'zh-Hans', 'zh-hant': 'zh-Hant' } as const;
for (const l of ['en', 'zh-hans', 'zh-hant'] as const) {
  for (const slug of ['eye-exams', 'eye-surface'] as const) {
    test(`/${l}/ortho-k/${slug}/ is translated and sits under How it works`, async ({ page }) => {
      await page.goto(`/${l}/ortho-k/${slug}/`);
      await expect(page.locator('h1')).toHaveCount(1);
      await expect(page.locator(`main [lang="${HTML_LANG[l]}"]`).filter({ hasText: OLD_PAGES[slug][l] }).first()).toBeVisible();
      await expect(page.locator(`header nav a[href*="${slug}"]`)).toHaveCount(0);
      await expect(page.locator(`header nav a[href="/${l}/ortho-k/"]`)).toHaveAttribute('aria-current', 'page');
    });
  }
  test(`/${l}/ortho-k/ links to both other-eye-care pages`, async ({ page }) => {
    await page.goto(`/${l}/ortho-k/`);
    for (const slug of ['eye-exams', 'eye-surface']) await expect(page.locator(`main a[href="/${l}/ortho-k/${slug}/"]`)).toHaveCount(1);
  });
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

for (const l of ['en', 'zh-hans', 'zh-hant']) {
  test(`/${l}/contact/ offers Call to book above the form`, async ({ page }) => {
    await page.goto(`/${l}/contact/`);
    await expect(page.locator('#call a[data-call][href="tel:+16262825388"]')).toBeVisible();
    await expect(page.locator('#book form[data-booking]')).toHaveCount(1);
  });

  test(`/${l}/ footer links to all five required notices`, async ({ page }) => {
    await page.goto(`/${l}/`);
    for (const slug of ['privacy', 'notice-of-privacy-practices', 'accessibility', 'terms', 'nondiscrimination']) {
      await expect(page.locator(`footer a[href="/${l}/${slug}/"]`)).toHaveCount(1);
    }
    await expect(page.locator('footer [aria-disabled="true"]')).toHaveCount(0);
  });

  for (const slug of ['privacy', 'notice-of-privacy-practices', 'accessibility', 'terms', 'nondiscrimination']) {
    test(`/${l}/${slug}/ has real content`, async ({ page }) => {
      await page.goto(`/${l}/${slug}/`);
      await expect(page.locator('h1')).toHaveCount(1);
      expect((await page.locator('main article').innerText()).length).toBeGreaterThan(800);
      expect(await page.locator('main').innerText()).not.toMatch(/待提供|placeholder/i);
    });
  }
}

for (const path of ['/en/', '/en/ortho-k/']) {
  test(`${path} answers "Is ortho-k safe for kids?" with real safety guidance`, async ({ page }) => {
    await page.goto(path);
    const faq = page.locator('#faq');
    await expect(faq).toContainText('infection');
    await expect(faq).toContainText('(626) 282-5388');
  });
}

for (const l of ['en', 'zh-hans', 'zh-hant']) {
  test(`/${l}/ortho-k/ shows the VIPOK logo with Dr. Woo's ownership disclosed`, async ({ page }) => {
    await page.goto(`/${l}/ortho-k/`);
    const s = page.locator('#lenses');
    await expect(s.locator('img')).toHaveCount(1);
    await expect(s).toContainText('VIPOK');
    await expect(s.locator('[data-disclosure]')).toHaveCount(1);
  });
}

for (const l of ['en', 'zh-hant']) {
  test(`/${l}/ every Call to book button shows a phone icon`, async ({ page }) => {
    await page.goto(`/${l}/`);
    const buttons = page.locator('[data-cta="message"]');
    expect(await buttons.count()).toBeGreaterThan(0);
    await expect(page.locator('[data-cta="message"] svg[data-icon="phone"]')).toHaveCount(await buttons.count());
  });
}
