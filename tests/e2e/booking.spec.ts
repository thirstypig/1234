import { test, expect, type Page } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('1234-review-unlocked', 'true'));
});

async function fill(page: Page) {
  await page.goto('/en/contact/');
  await page.fill('[name=parentName]', 'Ann Lee');
  await page.fill('[name=phone]', '6265550100');
  await page.check('[name=location][value=alhambra]', { force: true });
}

test('form has no free-text notes field', async ({ page }) => {
  await page.goto('/en/contact/');
  await expect(page.locator('#book textarea')).toHaveCount(0);
});

test('successful submit shows inline confirmation', async ({ page }) => {
  await page.route('**/booking', (r) => r.fulfill({ status: 201, body: '{"ok":true}' }));
  await fill(page);
  await page.click('#book [type=submit]');
  await expect(page.locator('#book [role=status]')).toContainText(/thank/i);
});

test('network failure shows error, re-enables, keeps values', async ({ page }) => {
  await page.route('**/booking', (r) => r.abort());
  await fill(page);
  const submit = page.locator('#book [type=submit]');
  await submit.click();
  await expect(page.locator('#book [role=alert]')).toBeVisible();
  await expect(submit).toBeEnabled();
  await expect(page.locator('[name=parentName]')).toHaveValue('Ann Lee');
});

test('double click sends one request', async ({ page }) => {
  let n = 0;
  await page.route('**/booking', async (r) => {
    n++;
    await new Promise((x) => setTimeout(x, 300));
    await r.fulfill({ status: 201, body: '{"ok":true}' });
  });
  await fill(page);
  await page.locator('#book [type=submit]').dblclick();
  await expect(page.locator('#book [role=status]')).toContainText(/thank/i);
  expect(n).toBe(1);
});

test('server field errors mark the fields', async ({ page }) => {
  await page.route('**/booking', (r) => r.fulfill({ status: 400, body: '{"error":"x","fields":["phone"]}' }));
  await fill(page);
  await page.click('#book [type=submit]');
  await expect(page.locator('[name=phone]')).toHaveAttribute('aria-invalid', 'true');
});

test('error box is not shown before any submit', async ({ page }) => {
  await page.goto('/en/contact/');
  await expect(page.locator('#book [role=alert]')).toBeHidden();
});
