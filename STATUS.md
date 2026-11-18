# STATUS — 1234

**Last updated:** 2026-11-11

## One-line description
Website in three languages (EN / 简体 / 繁體) for 1234 Ortho-K Vision Care, an optometry practice in Alhambra and Walnut, CA. Built from design Concept C ("Picture Book").

## Scope / positioning
- Replaces the old Web.com site; old URLs redirect to the new pages.
- 13 pages × 3 locales.
- Client copy only and no new claims; image and patient-photo rules are enforced by tests.
- The repo is public.

## Stack & hosting
- Astro 7, Node ≥ 22.12; Playwright + axe tests.
- Live site: GitHub Pages, deployed by `deploy-site.yml` on every push to `main`.
- Review copy: built by the separate repo `thirstypig/1234-review`.
- Cloudflare Worker + KV (`workers/comments/`) for review comments and booking requests.
- DNS at Squarespace. Google Analytics 4 on the live site only.

## URLs
- Live: https://www.1234orthok.com
- Review (password-gated): https://1234.pasadenaworks.com

## Shipped (last 60 days)
The whole project falls in this window (first commit 2026-09-24).
- Five design concepts on a review site with a comments sidebar and pins.
- Concept C site: all pages, two eye-care pages and five legal notices, in three languages.
- Old-site image harvest, with build-time guards on what can be published.
- Cleared patient photos, old-site reviews and approved claims published.
- Owner copy rounds applied (10-09, 10-27, 11-07).
- Amblyopia poster, treatment steps, aftercare flyer, 404 page.
- Launched 2026-11-04; www became the main address; GA4 added.
- Language audit; self-hosted Chinese font subset.
- Walnut made a call-only location; booking form hidden.

## In progress
- Most `docs/copy-review.md` items are still awaiting practice or attorney sign-off.
- Launched with Claude-drafted legal notices, Chinese copy and FAQ answer, before attorney review (N-18).

## Open bugs / known issues
- The booking form stays hidden until the practice names a service covered by a BAA (requests sat unread in KV).
- The legal notices still describe the booking form (N-24).
- Abiliti logo file not yet supplied (N-13).
- Amblyopia threshold (0.8 vs 0.7) waiting on the practice to confirm (N-17).
- Attorney questions: VIPOK disclosure (N-7), testimonials (T-1).

## Next phases (in order)
- Unknown — no roadmap documented. Recorded items:
  1. Attorney review; apply changes on the live site.
  2. Pick a booking service covered by a BAA; re-enable the form and update the notices.
  3. A separate FAQ page for SEO ("planned later").

## Decisions changed recently
- Main address moved from the bare domain to www after the bare-domain certificate got stuck (2026-11-05).
- Privacy notice changed from "no analytics" to GA4 (2026-11-05).
- Google Fonts replaced by a self-hosted Chinese subset (2026-11-07).
- Opening hours, placeholder copy and unanswered FAQs removed (2026-11-07).
- Walnut no longer "Opening soon"; booking form disabled (2026-11-07).
- `main` is now the only long-lived branch, and it is production (2026-11-06).
