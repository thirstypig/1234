// Writes the files that differ between the live site and the review copy into dist/.
//   node --import tsx scripts/site-files.mjs production|review
// production: redirects from the old 1234orthok.com URLs, robots.txt allowing crawlers, sitemap.xml.
// review: robots.txt disallowing everything (pages also carry noindex).
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { LOCALES, PAGES, pathFor } from '../src/i18n/locales.ts';

export const PRODUCTION_ORIGIN = 'https://www.1234orthok.com';

// Old Web.com site (archived 2026-11-04 in the private thirstypig/1234orthok-old-site) -> new page.
// It served each page both as /name.html and /name/. consultant and therapy were Chinese-only pages.
export const OLD_PAGES = {
  index: '/en/',
  about: '/en/about/',
  'contact-us': '/en/contact/',
  ortho: '/en/ortho-k/',
  testimonials: '/en/testimonials/',
  memories: '/en/community/',
  consultant: '/zh-hant/ortho-k/eye-exams/',
  therapy: '/zh-hant/ortho-k/eye-surface/',
};

// [file path relative to dist, target path]
export function redirectFiles() {
  const out = [];
  for (const [name, to] of Object.entries(OLD_PAGES)) {
    out.push([`${name}.html`, to]);
    if (name !== 'index') out.push([`${name}/index.html`, to]);
  }
  return out;
}

const escapeAttr = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;');

export function redirectHtml(to, origin = PRODUCTION_ORIGIN) {
  const href = escapeAttr(to);
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url=${href}" />
    <link rel="canonical" href="${escapeAttr(origin + to)}" />
    <title>1234 Ortho-K Vision Care</title>
  </head>
  <body><a href="${href}">1234 Ortho-K Vision Care</a></body>
</html>
`;
}

export function sitemapXml(origin = PRODUCTION_ORIGIN) {
  const urls = LOCALES.flatMap((l) => PAGES.map((p) => `  <url><loc>${origin}${pathFor(l, p)}</loc></url>`));
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join('\n')}
</urlset>
`;
}

export function robotsTxt(mode, origin = PRODUCTION_ORIGIN) {
  return mode === 'production'
    ? `User-agent: *\nAllow: /\n\nSitemap: ${origin}/sitemap.xml\n`
    : 'User-agent: *\nDisallow: /\n';
}

async function write(dist, rel, text) {
  const f = join(dist, rel);
  await mkdir(dirname(f), { recursive: true });
  await writeFile(f, text);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const mode = process.argv[2];
  if (!['production', 'review'].includes(mode)) throw new Error('usage: site-files.mjs production|review');
  const dist = 'dist';
  await write(dist, 'robots.txt', robotsTxt(mode));
  if (mode === 'production') {
    await write(dist, 'sitemap.xml', sitemapXml());
    for (const [rel, to] of redirectFiles()) await write(dist, rel, redirectHtml(to));
  }
}
