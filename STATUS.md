# STATUS — 1234

**Last updated:** 2026-11-18

## One-line description
Website in three languages (EN / 简体 / 繁體) for 1234 Eye Care Clinic & Optometric Center, an optometry practice in Alhambra and Walnut, CA. Built from design Concept C ("Picture Book").

## Scope / positioning
- Replaces the old Web.com site; old URLs redirect to the new pages.
- 13 pages × 3 locales.
- Client copy only and no new claims; image and patient-photo rules are enforced by tests.
- The repo is public.

## Stack & hosting
- Astro 7, Node ≥ 22.12; Playwright + axe tests.
- Live site: GitHub Pages, deployed by `deploy-site.yml` on every push to `main`.
- Review copy: built by the separate repo `thirstypig/1234-review`.
- Cloudflare Worker + KV (`workers/comments/`): review comments; booking route off.
- DNS at Squarespace. Google Analytics 4 on the live site only.

## URLs
- Live: https://www.1234orthok.com
- Review (password-gated): https://1234.pasadenaworks.com

## Shipped (last 60 days)
- Concept C built in three languages; old-site images behind build-time publish guards.
- Patient photos, old-site reviews and approved claims published; owner copy rounds 10-09, 10-27, 11-07.
- Amblyopia poster, treatment steps, aftercare flyer, 404 page.
- Launched 2026-11-04; www became the main address; GA4 added.
- Language audit; self-hosted Chinese font subset; Walnut call-only; booking form hidden; notices rewritten for phone-only booking; booking endpoint off (N-24, #37–#40).
- Attorney PDFs rebuilt (stale since 2026-09-28).
- New practice name on all pages and notices (#42).

## In progress
- Attorney PDFs rebuilt with the new name but not uploaded to R2; private Worker not redeployed.
- Most `docs/copy-review.md` items await practice or attorney sign-off; the site launched with Claude-drafted notices, Chinese copy and FAQ answer (N-18).

## Open bugs / known issues
- No online booking until the practice names a service covered by a BAA.
- Google profile (2026-11-18): two old review replies to replace (one discusses a patient's payment); no Walnut listing; a duplicate "Paul T. Woo, OD" listing.
- Name spelling unconfirmed: site and Google say "Eye Care"; logo and permit checklist say "Eyecare"; a photographed sign says "1234 Ortho-K Vision Care". Photo release forms keep the old name.
- Abiliti logo file not yet supplied (N-13).
- Amblyopia threshold (0.8 vs 0.7) waiting on the practice to confirm (N-17).
- Attorney questions: VIPOK disclosure (N-7), testimonials (T-1).

## Next phases (in order)
  1. Attorney review; apply changes on the live site.
  2. Pick a booking service covered by a BAA; re-enable the form and Worker, restore the notices' form wording and name the service.
  3. A separate FAQ page for SEO ("planned later").

## Decisions changed recently
- Chinese font self-hosted as a subset; English still loads Quicksand from Google Fonts (2026-11-07).
- Opening hours, placeholder copy and unanswered FAQs removed (2026-11-07).
- Practice name "1234 Ortho-K Vision Care" → "1234 Eye Care Clinic & Optometric Center" (matches Google); Chinese name unchanged (2026-11-18).
- Walnut no longer "Opening soon"; booking form disabled (2026-11-07); notices rewritten for phone-only booking rather than waiting for a booking service (2026-11-18).
