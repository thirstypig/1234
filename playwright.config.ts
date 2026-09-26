import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: 'tests/e2e',
  testIgnore: ['**/deploy.spec.ts'],
  webServer: {
    command: 'npm run build && node scripts/serve-dist.mjs 4321',
    port: 4321,
    reuseExistingServer: !process.env.CI,
    timeout: 180_000,
  },
  use: { baseURL: 'http://localhost:4321' },
});
