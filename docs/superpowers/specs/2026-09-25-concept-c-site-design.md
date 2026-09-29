# Concept C site + legacy image harvest — design

Date: 2026-09-25 · Branch: `site/concept-c` (from `design/concepts-import`)

## Goal

The client chose Concept C ("Picture Book"). Build the real site from it,
reusing images from the current 1234orthok.com, and keep all five concepts
available for reference.

**Done means:** 15 pages (5 pages × EN / 简体 / 繁體) built from Concept C,
passing WCAG AA and the CLAUDE.md rules, deployed at the root of
`1234.pasadenaworks.com` alongside the archived concepts at `/concepts/`,
plus a reviewable catalog of every image from the old site.

## Decisions (from the user)

- Scope: harvest images **and** build the site.
- Launch pages: Home, About, Ortho-K, Contact, Testimonials.
- English copy: carried over from the old site; every sentence with a
  statistic, success rate, patient count, guarantee, or "best/most/leading"
  claim is flagged for review and does not ship until approved.
- Languages: all three built with an always-visible switcher; Chinese pages
  use marked placeholders until the client supplies copy. Old 繁體 text is
  kept in the catalog as reference only.
- Images: download everything, tag each one; only `practice-photo` (or
  explicitly approved) images may appear on pages.
- Book → booking form on Contact page. Message → `tel:`/`sms:` to the
  office number from the old site.
- Keep the five concepts; move them under `/concepts/`.

## Assumptions (not confirmed — flag if wrong)

- Concept C's zh-Hant homepage copy is placeholder, not client-approved.
- Story-scene illustrations don't exist yet. Pages keep Concept C's labeled
  illustration placeholders; old photos go only in photo slots (Doctor card,
  Illustrated photo frame, Location cards).
- The whole preview site stays behind the existing review password and is
  `noindex` until launch on 1234orthok.com (separate, later step).

## 1. Legacy image harvest

- `scripts/harvest/crawl.mjs` (Node, `fetch`): crawls every same-domain page
  on 1234orthok.com, including pages we aren't rebuilding; collects
  `<img src/srcset>`, CSS `background-image`, and linked image/PDF files.
- **Gap probe:** files follow `1234orthok-com-NNN.ext`; probe every missing
  number in the observed range and record orphans.
- Output:
  - `assets/legacy/originals/` — untouched downloads, committed (report
    total size first; switch to LFS/untracked if large).
  - `assets/legacy/catalog.json` — per file: filename, source pages, bytes,
    dimensions, original `alt`, surrounding text, `tag`, `approved: false`.
  - `design/legacy-catalog/index.html` — filterable thumbnail grid, served at
    `/concepts/legacy-images/` behind the review password.
- Tags: `practice-photo`, `likely-stock`, `third-party-logo`,
  `patient-photo`, `decorative`, `needs-review`. Heuristics pre-sort; every
  image is then visually checked. Uncertain → `needs-review`, never
  `practice-photo`.

## 2. Site structure

- Routes: `/{en,zh-hans,zh-hant}/{,about/,ortho-k/,contact/,testimonials/}`;
  `/` redirects to `/en/`. `hreflang` alternates on every page; the switcher
  links to the same page in the other language.
- `src/styles/` imports Concept C's `bundle.css` and tokens directly from
  `design/concepts/concepts/C-picture-book/project/` (no copies).
- `src/components/`: one `.astro` component per Concept C component README
  (nav + mobile menu, language switcher, footer, hero, story scenes,
  3-step, FAQ, doctor card, location card, contact row, booking band,
  illustrated photo frame, buttons, form field set) plus a mobile sticky
  Book/Message bar.
- `src/features/<page>/`: page compositions. `src/content/copy/{en,zh-hans,zh-hant}.json`:
  all page strings; pages hold no literal copy.
- `src/lib/images.ts`: the only way pages import legacy images; **build
  fails** if an image isn't `practice-photo` or `approved: true`.
- `scripts/copy/extract.mjs` pulls old-site English into `en.json` and writes
  `docs/copy-review.md` (flagged sentences with keep/cut/rewrite boxes).
  Flagged strings render as omitted until approved.
- Chinese typography: body ≥ 17px, line-height ≥ 1.7 on zh pages.
- Header shows plain-text name (no logo), per Concept C README.

## 3. Booking form

- Contact page form fields: parent name, phone, preferred location
  (Alhambra / Walnut), preferred day/time. **No free-text medical field** —
  keeps children's health details out of email and KV.
- Posts to a new `POST /booking` route in `workers/comments/` (same Worker,
  same CORS origin). Validation server-side; honeypot field; per-IP rate
  limit via KV.
- Delivery: email to the office. Mechanism (Cloudflare Email Routing
  `send_email` binding vs. a third-party sender) and its cost are verified
  before implementation — not assumed. Until the office address and sender
  are confirmed, submissions are stored in KV with a 30-day TTL and the
  preview shows a clear "preview only" notice.
- Inline success/error states in the page — no `alert()`/`prompt()`.
- Message button: `tel:` everywhere; `sms:` only if the office number
  accepts texts (ask client; landlines often don't).

## 4. Deploy and move

- One GitHub Pages workflow (replaces `deploy-review-site.yml`): `npm ci`,
  `astro build`, copy `design/concepts/` → `dist/concepts/` unchanged, upload
  `dist/`. Triggers on `site/concept-c`, `design/concepts-import`, `main`.
- Existing comments survive: keys are `<concept-folder>:<lang>` and
  `inject.js` matches `/concepts/<X>/…` anywhere in the path (verified).
  Worker `ALLOWED_ORIGIN` is unchanged because the domain is unchanged.
- Gallery `index.html` for the concepts moves to `/concepts/`.
- Custom domain / cert: unchanged. If the cert drops to `null`, clear and
  re-set `cname` (known quirk).

## Testing

- Unit: catalog guard (`images.ts`), claims flagger, booking validation
  (Worker, alongside existing `index.test.ts`).
- Playwright over all 15 pages: axe WCAG AA; switcher present and targets
  the same page; "Book a consultation" in first viewport and at bottom;
  zh body font-size/line-height; mobile sticky bar at 390px width; no
  `<img>` outside the catalog.
- Manual: visual check of Home in each language against the Concept C
  mockup at desktop and mobile widths.

## Out of scope

Therapy, Consultant, Memories and `el-02xx` pages; logo; illustrations;
Chinese copy; switching 1234orthok.com DNS; closing/merging PR #8.
