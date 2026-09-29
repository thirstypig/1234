// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://1234.pasadenaworks.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
