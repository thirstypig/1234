import { defineConfig } from '@playwright/test';

// Tests the assembled review copy (SITE_MODE=review): Astro site + archived concepts + review scripts.
// The live build (the default) is covered by tests/e2e/launch.spec.ts and scripts/site-files.test.mjs.
export default defineConfig({
  testDir: 'tests/e2e',
  testMatch: ['deploy.spec.ts'],
  webServer: {
    command: 'SITE_MODE=review bash scripts/assemble.sh && node scripts/serve-dist.mjs 4330',
    port: 4330,
    reuseExistingServer: false,
    timeout: 180_000,
  },
  use: { baseURL: 'http://localhost:4330' },
});
