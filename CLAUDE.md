# 1234 Ortho-K Vision Care — project notes

## Design concepts

Design concepts live in `design/concepts/`; each concept's source of
truth is `concepts/<X>/project/` (`tokens.json`, `README.md`,
`components/bundle.css`, component READMEs).

Rules:
- EN / 简体 / 繁體 as separate pages with the switcher always visible.
- Chinese body >= 17px, line height >= 1.7.
- Header logo: the old-site PNG (`1234orthok-com-051.png`) until the
  client supplies a vector file; the footer keeps the plain-text name.
- Use only client-provided copy. Exception (owner direction,
  2026-09-28): Claude drafted the Chinese translations of all site copy,
  the English and Simplified versions of the two eye-care pages, the
  safety FAQ answer and the five required notices (`src/content/legal/`).
  All are drafts for the practice (and its attorney, for the notices)
  to approve; see `docs/copy-review.md`.
- Never add statistics, success rates, patient counts, or
  "best/most effective" claims. Exceptions (owner decisions,
  2026-09-28), kept word for word from the old site, claims included:
  all 21 patient reviews with their names on the Stories page
  (`src/content/reviews.json`; the owner approved the 9 once held back,
  2026-09-29), and the statistics on the Eye Surface
  Therapy page. That page and Children's Eye Exams
  (`src/content/old-pages.json`) sit under How it works
  (`/<lang>/ortho-k/...`); their Traditional Chinese was cleaned up and
  the English and Simplified versions are drafts for the practice to check.
  Also (owner, 2026-09-29): the old-site claims listed in
  `src/content/approved-claims.json`, shown on the Home doctor card and
  About. The clinic opened in 1998; Dr. Woo has over 30 years of
  experience (he practiced in Taiwan before that). Also (owner's review
  comments, 2026-10-27; `docs/copy-review.md`, N-16): the Home hero
  ("30 years", "prescription does not increase", "highly effective",
  "best option", ages 5–45) and About's "over 40,000 patients" (owner,
  2026-11-07, N-23; it was 41,879, and 9,000 before that). Add no new claims. The two age ranges are deliberate (owner,
  2026-10-28): Home says 5–45 (children and adults), and How it works
  keeps "Ortho-K for children, ages 7–18" (`ortho.title`); don't align them.
- Every image is accounted for in `docs/photo-inventory.md` (a test
  enforces it). Only patient photos P-01 to P-27 may be published
  (owner confirmed permission 2026-09-29, and 2026-10-10 for
  P-27): prepared, metadata-free copies
  in `assets/patients/`, on Stories (P-01 to P-23, P-27) and Community (P-24 to
  P-26) via `patientPhoto()`. The owner took P-09, P-11, P-14, P-21 and
  P-22 off Stories on 2026-10-27; their files were deleted. All
  other patient photos stay on the private patient-photos page.
  Drawings from the practice's amblyopia poster (owner, 2026-10-28:
  the practice owns its poster and flyer artwork) live in
  `assets/client/`, listed in `art.json`, used via `clientArt()`.
- Wording the owner set on 2026-10-09 (`docs/copy-review.md`, N-11 to
  N-15): write "Ortho-K", never "ortho-k", except inside patient
  reviews, which stay word for word. Dr. Woo is "Dr. Paul T. Woo,
  Optometrist", never "OD", including in the notices. He speaks English,
  Mandarin and Cantonese. The English Eye Surface Therapy page says
  "calcium deposits", not "eye stones"; the Chinese pages keep 眼結石.
- Parent questions (the FAQ) are on How it works only, not Home.
- Lens brands named: VIPOK, CRT, Abiliti. The VIPOK and Paragon CRT
  logos are approved in the catalog and shown; the Abiliti logo waits
  on a file from the practice. The owner removed the sentence "Dr. Woo is
  an owner of VIPOK Inc." from How it works on 2026-10-10 (`docs/copy-review.md`,
  N-7, still open for the attorney): don't put it back unasked.
- Walnut: 20265 Valley Blvd., #E, Walnut, CA 91789, shown with the
  Alhambra sign photo; the card still says "Opening soon".
- No opening hours anywhere, for either clinic (owner, 2026-11-07, N-23).
- No placeholder copy and no unanswered questions on the site (owner,
  2026-11-07): the FAQ shows only answered questions. A separate FAQ page
  for SEO is planned later. Ortho-K lenses are "semi-hard" (半硬式).
  The insurance/payment-plan sentence was removed; don't put it back unasked.
- All text WCAG AA.
- "Book a consultation" in the first screen and at the bottom.
- Mobile sticky Book/Message bar.

The client chose **Concept C (Picture Book)** on 2026-09-25. The other
concepts stay as reference. Never edit anything in `design/concepts/`:
the site imports Concept C's `tokens.local.css` and `bundle.css` from
there unmodified.

## The site (`src/`)

Astro, 13 pages × 3 locales from `src/pages/[lang]/` (the two eye-care pages nest under `ortho-k/`; the five notices come from `src/content/legal/`). All text lives in
`src/content/copy/{en,zh-hans,zh-hant}.json`; pages hold no literal
copy, and a key missing from any locale fails the build. The Chinese
copy is Claude's draft translation awaiting the client's approval
(`docs/copy-review.md`, N-2).

Copy from the old site that makes a claim is held in
`docs/copy-review.md` (ids `F-…`, mockup changes `M-…`). It renders
only once its id is in `src/content/approved-claims.json`
(`isApproved()` in `src/lib/claims.ts`). Don't re-run
`scripts/copy/extract.mjs` after the client has signed items off: it
resets both files.

## Images — the repo is PUBLIC

`thirstypig/1234` is public. Old-site originals, including photos of
child patients, stay git-ignored in `assets/legacy/originals/`. Only
images tagged `practice-photo` or marked `approved: true` in
`assets/legacy/catalog.json` may be committed. They live in
`assets/legacy/site/`, regenerated by
`node scripts/harvest/review-page.mjs`. Pages use them only through
`legacyImage()` (`src/lib/images.ts`), which fails the build for
anything else. A unit test fails if any other image is tracked.
Never commit any other patient photo; git history is permanent once
pushed. Patient photos P-01 to P-27 are the exception: they live in
`assets/patients/`, listed in `photos.json` (a unit test enforces it),
with the P-01 record card blurred and P-07/P-08 cropped.

## Live site, review copy and deploy

One build, two copies (`scripts/assemble.sh`, `SITE_MODE`; `src/lib/site-mode.ts`):
- **Live: `https://www.1234orthok.com`** (launched 2026-11-04; default `SITE_MODE=production`; `1234orthok.com` redirects to www).
  This repo's GitHub Pages, `.github/workflows/deploy-site.yml` on push to `main`.
  Indexable, no review overlay, canonical/hreflang on 1234orthok.com, `robots.txt` +
  `sitemap.xml`, and redirect pages for the old Web.com URLs (`/about.html`, `/ortho/`, …;
  `scripts/site-files.mjs`). DNS is Squarespace (nameservers stay there): four `@` A
  records to GitHub, `www` CNAME `thirstypig.github.io`; `mail`, `webmail`, MX and SPF
  are the practice's email: never touch them. The Pages custom domain is set in repo
  settings (a workflow deploy ignores the CNAME file). It is `www.1234orthok.com`, not the bare domain: GitHub's HTTPS certificate for the bare domain stuck in `authorized` for a day (Let's Encrypt had issued it; resets and recreating the Pages site didn't help), and switching to www (2026-11-05) started a fresh request. Don't switch back.
- **Review: `https://1234.pasadenaworks.com`** (`SITE_MODE=review`), for Dr. Woo and
  Elaine's comments: the same pages behind the review password, `noindex`, with:
  - `/concepts/<X>/…` — the five concepts, at their original URLs
  - `/concepts/` — concept gallery; `/concepts/legacy-images/` — image catalog
  - `/_review/` — gate + comments scripts, copied from `design/concepts/_review/`
  It is built from `main` by the separate repo `thirstypig/1234-review` (GitHub allows
  one Pages site per repo).

The old site is archived in the private repo `thirstypig/1234orthok-old-site`
(local `~/Projects/1234orthok-old-site`; patient photos inside: keep it private).

The review overlay (password gate + comments/pins) runs on the five
homepage mockups (`Concept*-homepage-EN.html`, via `inject.js`) and on
every page of the Concept C site (`public/_review/site-review.js`, loaded
by `BaseLayout.astro`; threads use concept `C-site`, keyed by
`site-key.js`), never on the component preview pages, and only in the
review copy: the live build leaves out `site-review.js`, the `noindex` tag and
`dist/_review/` (`tests/e2e/launch.spec.ts`). Google Analytics 4 (`G-ZS9T686F3W`, `src/components/Analytics.astro`) runs on the live site only, with Google signals and ad personalization off; the privacy notice describes it (N-21), so change both together. The gate is a browser-side overlay and its password is in
the public `gate.js`, so anything deployed is effectively public.
`public/_review/*` is git-ignored except for named `!` exceptions, so a
new script there is silently left out of the deploy until you add one.
`gate-only.js` stays: the legacy image catalog still loads it. Comments
don't load on localhost: the Worker's CORS allows only the preview
origin.

`workers/comments/` (Cloudflare Worker + KV) serves `/comments` (keys
`<concept>:<page>`, concept must start A–E) and `/booking` (booking
requests, 30-day TTL; name, phone, location and preferred time only).
Nothing reads `/booking` back: requests sit in KV, the office never sees
them, and no alert goes out. Before launch they must reach the office
through a service covered by a BAA (the practice has to name it; question 2
in the private page's `src/email.ts`), and the privacy notice, which
currently names Cloudflare, must name that service too.
Deploying it (`npx wrangler deploy`) and pushing to a deploy branch are
production actions: ask first.

Working through the owner's feedback: read each thread with
`curl -G <Worker>/comments --data-urlencode concept=C-site --data-urlencode page=<lang>[/<path>]`
(39 pages; curl is not subject to the CORS limit). The Worker has no
delete route, so a thread is cleared by deleting its KV key from
`workers/comments/`: `npx wrangler kv key delete "C-site:<page>"
--namespace-id <id in wrangler.toml> --remote`. A pin left on one
language usually means all three.

`main` is production: a merge deploys 1234orthok.com, so new work goes on a
branch and a PR into `main`.

A separate private Worker (private repo `thirstypig/1234-patient-photos`,
server-side password) holds what stays off this repo: the Admin section
with the pre-launch email to the practice (`src/email.ts`, Copy buttons),
the attorney-review packet and checklist, the release forms, and the
unlicensed stock images and other organizations' logos. Since 2026-09-30
every patient and event photo and every review is on the public site, so
the private page no longer lists them. Deploying it is a production
action: ask first.

Moving patient photos or reviews into this repo, or publishing them,
trips Claude Code's auto-mode classifier even with the owner's go-ahead.
Settle how that step will be approved (`/permissions`, or the user runs
it) before starting, not halfway through. On 2026-10-10 (P-27) it
blocked `git commit` and `gh pr create` but not `git push`: give the user
those two commands to run with `!`.

The only long-lived branch is `main` (`site/concept-c` was deleted
2026-11-06). The auto-mode classifier blocks `git push --delete`: the user
runs it with `!`. Since 2026-10-28 it also blocks `gh pr merge` into `main`
("Production Deploy"), even when the user said to merge: open the PR, then
give the user `! gh pr merge <n> --merge --delete-branch`, and check the
deploy run after.
Stacked PRs: merging the bottom one with `--delete-branch` closes the PR
stacked on it, and a closed PR can't be retargeted; open a new PR from
the same branch.

## Tests

- `npm run test:unit`: scripts, i18n parity, image guards
- `npm run test:e2e`: Playwright + axe over all 39 pages. Stop any
  `astro dev` first (`npx astro dev stop`): Playwright reuses whatever is
  on port 4321, and the dev toolbar's shadow DOM adds extra `h1`s that
  fail the one-h1 tests. (serves `dist/`
  via `scripts/serve-dist.mjs`; `astro preview` detaches in Astro 7).
  A rare `page.goto` timeout is Google Fonts, not the site: rerun.
  The full run takes about 11 minutes (`npx playwright test --workers=4`),
  longer than a foreground command may run: start it in the background
  and write the output to a file rather than piping it to `tail`.
  `npx playwright test home inner-pages` (66 tests, about a minute)
  covers page content.
  Includes a no-sideways-scroll check at 390px on every page (long URLs
  in the notices once made them 295px too wide).
  Images lazy-load: a Playwright element screenshot of a long gallery
  shows blank tiles unless you scroll through the page first.
- `npm run test:deploy`: the assembled review copy (old concept URLs,
  gate, patient photos 404); the live build is covered by
  `tests/e2e/launch.spec.ts` and `scripts/site-files.test.mjs`
- `cd workers/comments && npx vitest run`: Worker
