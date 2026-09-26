const SITE_HOST = '1234orthok.com';
const ASSET_EXT = /\.(png|jpe?g|gif|webp|svg|pdf)(\?|#|$)/i;

function resolve(raw, base) {
  // Mirror-tool links look like ../www.1234orthok.com/x.html — strip the fake host folder.
  const cleaned = raw.trim().replace(/^(\.\.\/)*www\.1234orthok\.com\//, '/');
  try {
    const u = new URL(cleaned, base);
    u.hash = '';
    if (u.hostname === `www.${SITE_HOST}`) u.hostname = SITE_HOST;
    return u;
  } catch { return null; }
}

export function extractPageLinks(html, pageUrl) {
  const out = new Set();
  for (const [, href] of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/gi)) {
    const u = resolve(href, pageUrl);
    if (!u || u.hostname !== SITE_HOST || !/^https?:$/.test(u.protocol)) continue;
    if (ASSET_EXT.test(u.pathname)) continue;
    if (!/(\.html?|\/)$/.test(u.pathname)) continue;
    out.add(u.href);
  }
  return [...out];
}

export function extractAssetUrls(html, pageUrl) {
  const raws = [];
  for (const [, v] of html.matchAll(/\b(?:src|data-src)="([^"]+)"/gi)) raws.push(v);
  for (const [, v] of html.matchAll(/\bsrcset="([^"]+)"/gi)) raws.push(...v.split(',').map((s) => s.trim().split(/\s+/)[0]));
  for (const [, v] of html.matchAll(/url\(\s*['"]?([^'")]+)['"]?\s*\)/gi)) raws.push(v);
  for (const [, v] of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/gi)) raws.push(v);
  const out = new Set();
  for (const raw of raws) {
    const u = resolve(raw, pageUrl);
    if (u && ASSET_EXT.test(u.pathname)) out.add(u.href);
  }
  return [...out];
}

export function findNumberGaps(filenames) {
  const nums = filenames
    .map((f) => f.match(/^1234orthok-com-(\d{3})\./)?.[1])
    .filter(Boolean)
    .map(Number);
  if (!nums.length) return [];
  const have = new Set(nums);
  const gaps = [];
  for (let n = Math.min(...nums); n <= Math.max(...nums); n++) {
    if (!have.has(n)) gaps.push(String(n).padStart(3, '0'));
  }
  return gaps;
}

export function suggestTag({ bytes = 0, width, height, alt = '', context = '', file = '' }) {
  if (/\.pdf$/i.test(file)) return 'needs-review';
  if (bytes < 5000 || (width && height && width * height < 80 * 80)) return 'decorative';
  if (/\blogo\b|certif|paragon|euclid|bausch|menicon|fda|aoa|association/i.test(`${alt} ${context}`)) return 'third-party-logo';
  // Practice vs patient vs stock requires eyes on the image — never guessed.
  return 'needs-review';
}
