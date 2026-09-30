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

test('patient photos are not published', async ({ request }) => {
  const res = await request.get('/concepts/legacy-images/img/1234orthok-com-016.jpg');
  expect(res.status()).toBe(404);
});

test('site pages stay gated and, once unlocked, have the feedback sidebar with pins', async ({ page }) => {
  // Never touch the real comments Worker from tests.
  const posted: any[] = [];
  await page.route('https://1234-review-comments.jimmyc316.workers.dev/**', async (route) => {
    const req = route.request();
    if (req.method() === 'POST') posted.push(req.postDataJSON());
    await route.fulfill({ json: req.method() === 'POST' ? {} : { comments: [] } });
  });

  await page.goto('/en/about/');
  await expect(page.locator('#review-gate-overlay')).toBeVisible();
  await page.evaluate(() => localStorage.setItem('1234-review-unlocked', 'true'));
  await page.reload();
  await expect(page.locator('#review-gate-overlay')).toHaveCount(0);

  await page.click('#review-sidebar-toggle');
  await expect(page.locator('#review-sidebar')).toBeVisible();
  await page.fill('#review-comment-input', 'General note');
  await page.click('#review-comment-submit');
  await expect.poll(() => posted.length).toBe(1);
  expect(posted[0]).toMatchObject({ concept: 'C-site', text: 'General note' });

  // Placing a pin on a link must not follow the link.
  await page.click('#review-pin-button');
  await page.locator('header a').first().click();
  await expect(page).toHaveURL(/\/en\/about\/$/);
  await expect(page.locator('.review-pin-composer')).toBeVisible();
});
