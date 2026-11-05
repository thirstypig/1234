import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { LOCALES, PAGES, pathFor } from '../src/i18n/locales.ts';
import { OLD_PAGES, redirectFiles, redirectHtml, sitemapXml, robotsTxt } from './site-files.mjs';

const realPaths = new Set(LOCALES.flatMap((l) => PAGES.map((p) => pathFor(l, p))));

test('every old 1234orthok.com page redirects to a page that exists', () => {
  for (const [name, to] of Object.entries(OLD_PAGES)) assert.ok(realPaths.has(to), `${name} -> ${to}`);
});

test('old pages are covered in both their .html and folder forms, without clobbering the root', () => {
  const files = redirectFiles().map(([f]) => f);
  for (const n of ['about', 'ortho', 'testimonials', 'therapy', 'consultant', 'memories', 'contact-us']) {
    assert.ok(files.includes(`${n}.html`) && files.includes(`${n}/index.html`), n);
  }
  assert.ok(!files.includes('index/index.html'));
  // New pages live under /en/, /zh-hans/, /zh-hant/, so no redirect can overwrite one.
  assert.ok(files.every((f) => !/^(en|zh-hans|zh-hant)\//.test(f)));
});

test('redirect pages refresh to the new path and name the live URL as canonical', () => {
  const html = redirectHtml('/en/about/');
  assert.match(html, /http-equiv="refresh" content="0; url=\/en\/about\/"/);
  assert.match(html, /rel="canonical" href="https:\/\/www\.1234orthok\.com\/en\/about\/"/);
});

test('sitemap lists every page in every language on the live domain', () => {
  const xml = sitemapXml();
  assert.equal((xml.match(/<url>/g) || []).length, LOCALES.length * PAGES.length);
  assert.ok(xml.includes('<loc>https://www.1234orthok.com/zh-hant/ortho-k/eye-surface/</loc>'));
  assert.ok(!xml.includes('pasadenaworks'));
});

test('robots.txt opens the live site and closes the review copy', () => {
  assert.match(robotsTxt('production'), /Allow: \/\n[\s\S]*Sitemap: https:\/\/www\.1234orthok\.com\/sitemap\.xml/);
  assert.match(robotsTxt('review'), /Disallow: \//);
});

test('the review copy keeps its CNAME file for the review repo', () => {
  assert.ok(existsSync('design/concepts/CNAME'));
});
