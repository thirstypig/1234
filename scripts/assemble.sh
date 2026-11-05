#!/usr/bin/env bash
# Builds a GitHub Pages artifact in dist/. Two copies of the same site:
#
#   SITE_MODE=production (default) — the live site, https://www.1234orthok.com (this repo's Pages):
#     /                          Astro site, indexable, no review overlay
#     /<old-page>.html, /<old-page>/   redirects from the old Web.com site's URLs
#     /robots.txt, /sitemap.xml
#
#   SITE_MODE=review — the practice's review copy, https://1234.pasadenaworks.com
#   (thirstypig/1234-review builds this from main):
#     /                          Astro site behind the password gate, with feedback sidebar + pins, noindex
#     /concepts/<X>/...          the five concepts, at the same URLs the client already has
#     /concepts/                 the concept gallery (links made root-relative in this copy only)
#     /concepts/legacy-images/   legacy image catalog
#     /_review/                  review gate + comments scripts
#
# Nothing under design/concepts/ is modified.
set -euo pipefail
MODE="${SITE_MODE:-production}"
export SITE_MODE="$MODE"
case "$MODE" in production|review) ;; *) echo "SITE_MODE must be production or review" >&2; exit 1 ;; esac

npm run build
node --import tsx scripts/site-files.mjs "$MODE"

if [ "$MODE" = production ]; then
  rm -rf dist/_review   # copied from public/; the live site never loads it
  echo "www.1234orthok.com" > dist/CNAME
  exit 0
fi

mkdir -p dist/concepts dist/_review
cp -R design/concepts/concepts/. dist/concepts/
sed 's#href="concepts/#href="/concepts/#g' design/concepts/index.html > dist/concepts/index.html
cp design/concepts/_review/*.js dist/_review/
rm -f dist/_review/*.test.mjs dist/_review/test-setup.mjs
rm -rf dist/concepts/legacy-images
mkdir -p dist/concepts/legacy-images/img
cp design/legacy-catalog/index.html dist/concepts/legacy-images/
cp assets/legacy/site/* dist/concepts/legacy-images/img/   # cleared images only
cp design/concepts/CNAME dist/CNAME
