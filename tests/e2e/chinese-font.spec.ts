import { test, expect } from '@playwright/test';

// The self-hosted Chinese font (scripts/fonts/subset.mjs) must draw every Chinese character on the page,
// in one file, with real bold (see "Chinese font" in CLAUDE.md).
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
});

for (const l of ['zh-hans', 'zh-hant']) {
  test(`/${l}/ loads one self-hosted Chinese font file and nothing from Google for Chinese`, async ({ page }) => {
    const fonts: string[] = [];
    page.on('request', (r) => { if (r.resourceType() === 'font') fonts.push(r.url()); });
    await page.goto(`/${l}/`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    expect(fonts.filter((u) => /chiron-goround-tc\.[\w-]+\.woff2$/.test(u))).toHaveLength(1);
    expect(fonts.filter((u) => u.includes('gstatic'))).toHaveLength(fonts.filter((u) => /quicksand/i.test(u)).length);
    expect(await page.evaluate(() => document.fonts.check('700 20px "Chiron GoRound TC"', '視视'))).toBe(true);
  });

  test(`/${l}/ bold Chinese really is bolder than regular`, async ({ page }) => {
    await page.goto(`/${l}/`);
    await page.evaluate(() => document.fonts.load('400 40px "Chiron GoRound TC"', '增'));
    const ink = await page.evaluate(async () => {
      const count = async (w: number) => {
        await document.fonts.load(`${w} 80px "Chiron GoRound TC"`, '增視');
        const c = document.createElement('canvas'); c.width = 200; c.height = 100;
        const x = c.getContext('2d')!; x.font = `${w} 80px "Chiron GoRound TC"`; x.fillText('增視', 0, 80);
        return x.getImageData(0, 0, 200, 100).data.filter((v, i) => i % 4 === 3 && v > 128).length;
      };
      return { regular: await count(400), medium: await count(500), bold: await count(700) };
    });
    expect(ink.medium).toBeGreaterThan(ink.regular * 1.05);
    expect(ink.bold).toBeGreaterThan(ink.regular * 1.25);
  });
}
