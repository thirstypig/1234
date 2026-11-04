// Which copy of the site this build is.
//   production (default) — https://1234orthok.com: indexable, no review overlay.
//   review (SITE_MODE=review) — https://1234.pasadenaworks.com: noindex, password gate and the
//   feedback sidebar/pins for the practice, plus the archived concepts (scripts/assemble.sh).
export const REVIEW = process.env.SITE_MODE === 'review';
export const PRODUCTION_ORIGIN = 'https://1234orthok.com';
export const REVIEW_ORIGIN = 'https://1234.pasadenaworks.com';
export const SITE_ORIGIN = REVIEW ? REVIEW_ORIGIN : PRODUCTION_ORIGIN;
