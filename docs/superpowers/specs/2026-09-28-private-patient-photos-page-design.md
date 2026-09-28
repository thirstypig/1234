# Private patient-photos page — design

Date: 2026-09-28
Status: approved in chat; awaiting spec review

## Purpose

Dr. Woo and the practice staff need one place to see the patient photos
that are **held back from the public site**, understand **why** (HIPAA and
California medical-privacy rules, children in the photos), and **download a
photo-release form** to use with families. Nothing here is linked from, or
built with, the public site.

Success looks like: staff open a link, type one password, see every
held-back photo with a number, read a short plain-English explanation, and
download a trilingual release form they can print and have families sign.

## Constraints

- `thirstypig/1234` is a **public** repo and the preview site is public. No
  patient photo, the password, or the page's content may go into either.
- The review site's password gate is client-side (localStorage). That is not
  acceptable here: the check must happen **on the server**, so images and the
  PDF are never served without it.
- `pasadenaworks.com` DNS is hosted on Google Cloud DNS, not Cloudflare, so a
  Worker cannot take a custom subdomain without moving DNS. The page uses the
  Worker's `*.workers.dev` URL.
- Form wording is a generic draft. It must be reviewed by the practice's
  attorney or HIPAA compliance contact before anyone signs it. Chinese text is
  a draft for the practice to check (same client-copy rule as the site).

## Architecture

```
browser ──► Cloudflare Worker "1234-patient-photos" (workers.dev)
              │  GET /            → password form (no content) or the page
              │  POST /login      → compare to secret, set cookie
              │  GET /img/<n>     → R2 object, only with valid cookie
              │  GET /release.pdf → R2 object, only with valid cookie
              ▼
           R2 bucket "1234-patient-photos" (private, no public URL)
```

- **Worker** — one TypeScript file, same toolchain as `workers/comments/`.
  Lives in its own directory **outside** this repo (a new private GitHub repo,
  `thirstypig/1234-patient-photos`, or local-only if preferred). Only this
  spec lives in the public repo.
- **Password** — a two-word password stored with `wrangler secret put
  PAGE_PASSWORD`. Never in code, config, git, or this spec.
- **Session** — on a correct password the Worker sets an `HttpOnly; Secure;
  SameSite=Strict` cookie holding an HMAC-signed expiry (12 hours), signed
  with a second secret `SESSION_KEY`. No server-side session store needed.
- **Brute-force limit** — failed logins counted per IP in a small KV
  namespace; after 10 failures in 15 minutes, `/login` returns 429.
- **Every response** carries `X-Robots-Tag: noindex, nofollow`,
  `Cache-Control: private, no-store`, and `Referrer-Policy: no-referrer`.
- **R2** — photos and the PDF are uploaded from the Mac with
  `wrangler r2 object put`. The bucket has no public access or r2.dev URL.

## Page content

1. **Why these photos aren't on the website** — a short plain-English note:
   - The photos show patients, most of them children, in the clinic. A
     patient's image taken during care is health information.
   - HIPAA requires a patient's written authorization before a practice uses
     it in marketing (website, social media, print, testimonials).
     California's Confidentiality of Medical Information Act adds its own
     written-authorization rules.
   - For anyone under 18, a parent or legal guardian signs.
   - One photo shows a lens record card with visit dates and prescription
     values; that card must be blurred or the photo left out even with a
     signed release.
   - Once a family signs, send the form's photo numbers and we'll add the
     photo to the site.
2. **The photos** — a numbered grid (P-01 … P-23): the 9 client photos from
   2026-09-28 and the 14 old-site photos tagged `patient-photo`. Numbers are
   what staff write on the form.
3. **Download the release form** — button for `release.pdf`.

## Release form (PDF)

One printable form, English + 繁體 + 简体, Letter size, 2 pages max:

- Practice name and address (1234 Ortho-K Vision Care, 1234 S. Garfield
  Ave. #105, Alhambra, CA 91801).
- Patient name; photo number(s) covered.
- Uses, each ticked separately: practice website · social media · print
  materials · testimonial quote shown with the photo.
- Standard authorization terms: what is disclosed and to whom, purpose,
  expiry (default: 5 years or until revoked), right to revoke in writing,
  treatment not conditioned on signing, info may be re-shared once public,
  no payment.
- Signatures: parent/guardian (required under 18) with relationship; patient
  signature (18+) or optional assent line for a minor; date.
- Footer: "Draft — have this reviewed by the practice's legal/HIPAA contact
  before use."

Generated from an HTML template with Playwright's `page.pdf()` (already a dev
dependency here), so the three languages render with system CJK fonts.

## Testing

- Worker unit tests (vitest calling the fetch handler with fake R2/KV bindings, as in `workers/comments/`):
  - No cookie → `/`, `/img/1`, `/release.pdf` return the login form or 401,
    never content.
  - Wrong password → 401; correct → 303 with cookie; expired or tampered
    cookie → rejected.
  - 11th failed login within the window → 429.
  - Headers (`noindex`, `no-store`) on every response.
- Manual: open the workers.dev URL in a private window, check the login flow,
  the grid, the PDF download, and that `/img/1` fails without the cookie.
- The public repo's existing guard tests keep passing; no new images in it.

## Out of scope

- Per-person logins, audit logs, or uploads from the page.
- Tracking which families have signed.
- Adding released photos to the site (done later, one photo at a time, via
  the existing catalog/guard process).
