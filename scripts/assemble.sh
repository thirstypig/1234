#!/usr/bin/env bash
# Builds the GitHub Pages artifact in dist/:
#   /                          Astro site (Concept C)
#   /concepts/<X>/...          the five concepts, at the same URLs the client already has
#   /concepts/                 the concept gallery (links made root-relative in this copy only)
#   /concepts/legacy-images/   legacy image catalog
#   /_review/                  review gate + comments scripts (concept homepages load /_review/inject.js)
# Nothing under design/concepts/ is modified.
set -euo pipefail
npm run build
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
