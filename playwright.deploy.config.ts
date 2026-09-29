import { defineConfig } from '@playwright/test';

// Tests the assembled GitHub Pages output: Astro site + archived concepts + review scripts.
export default defineConfig({
  testDir: 'tests/e2e',
  testMatch: ['deploy.spec.ts'],
  webServer: {
    command: 'bash scripts/assemble.sh && node scripts/serve-dist.mjs 4330',
    port: 4330,
    reuseExistingServer: false,
    timeout: 180_000,
  },
  use: { baseURL: 'http://localhost:4330' },
});
