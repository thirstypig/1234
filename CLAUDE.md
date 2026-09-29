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
- Use only client-provided copy.
- Never add statistics, success rates, patient counts, or
  "best/most effective" claims. Exception (owner decision,
  2026-09-28): the old site's patient reviews appear word for word on
  the Stories page (`src/content/reviews.json`), claims included.
- Every image is accounted for in `docs/photo-inventory.md` (a test
  enforces it). Patient photos live only on the private patient-photos
  page, never in this repo.
- All text WCAG AA.
- "Book a consultation" in the first screen and at the bottom.
- Mobile sticky Book/Message bar.

Treat everything in `design/concepts/` as reference until the client
picks a direction. Don't build pages from it without asking first.

The review site (`design/concepts/_review/`) overlays a password gate
and a comments/pin system on top of the five homepage mockups
(`Concept*-homepage-EN.html` in each concept folder) for client
feedback — never on the design-system component preview pages. The
concepts themselves are never edited by it. It's deployed via GitHub
Pages at `1234.pasadenaworks.com`; comments are stored by a small
Cloudflare Worker + KV API (`workers/comments/`), kept separate from
the page hosting itself so the site stays static.
