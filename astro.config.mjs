// @ts-check
import { defineConfig } from 'astro/config';

// SITE_MODE=review builds the password-gated review copy; anything else is the live site.
// Keep in step with src/lib/site-mode.ts.
const site = process.env.SITE_MODE === 'review' ? 'https://1234.pasadenaworks.com' : 'https://www.1234orthok.com';

// https://astro.build/config
export default defineConfig({
  site,
  trailingSlash: 'always',
  build: { format: 'directory' },
});
