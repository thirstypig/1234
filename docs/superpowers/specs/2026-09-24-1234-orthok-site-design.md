# 1234 Ortho-K Site — Project Setup & Design Concept Review

## Context

Replacing 1234orthok.com (Wix-based site for Dr. Paul T. Woo's Ortho-K
optometry practice, clinics in Alhambra and Walnut, CA) with a new
marketing site. Five design concepts (A–E) were built in Claude Design
and exported as a static bundle (`orthok-design-concepts.zip`). The
client hasn't picked a concept yet. Final site will be trilingual
(English, Simplified Chinese, Traditional Chinese) as separate URL
paths — that work starts only after a concept is chosen; out of scope
here.

This spec covers two things: (1) standing up the actual site repo and
project structure, and (2) a temporary internal review site that lets
the client leave dated feedback on each of the five concepts.

## Scope

### 1. Repo & scaffold
- New GitHub repo `thirstypig/1234`, public.
- Astro + TypeScript, no starter theme.
- Feature module isolation:
  ```
  src/
    features/
      home/
      services/
      testimonials/
      scheduling/
      contact/
    layouts/       (shared page shell only)
    components/     (shared, cross-feature UI only)
    pages/          (thin route files importing from features/)
  ```
  No feature folder imports from another feature folder directly;
  shared code only comes from `layouts/` or `components/`. This
  applies to the eventual real site; the concept-review material in
  (2) is intentionally kept outside this structure since it's
  reference material, not app code.

### 2. Design concepts import
- Branch `design/concepts-import` off `main`.
- Copy `orthok-design-concepts.zip` contents unchanged into
  `design/concepts/` (`README.md`, `index.html`, `concepts/`,
  `generator/`). No edits to design tokens, CSS, or copy.
- `.gitignore` inside `design/concepts/generator/` for `out/`,
  `shots/`, `__pycache__/`, `*.ttf`.
- Verify locally (`npx serve design/concepts`) and screenshot each
  concept's EN desktop homepage and zh-Hant mobile homepage with
  Playwright at 1280px/390px (20 screenshots total) into
  `design/concepts/_qa/` (gitignored). Report any broken CSS, missing
  fonts, horizontal scroll, or overlap — don't fix, just report.
- **Stop and show the user** after verification, before touching
  CLAUDE.md, filing issues, or opening the PR.
- Then: document the rules in CLAUDE.md, file one GitHub issue per
  open item from the export's README (label `design`), commit in two
  logical commits (import; docs+gitignore), open PR to `main`
  (not merged).

### 3. Review-site feedback features (new, on top of imported concepts)
- **Comments sidebar**: right-hand sidebar on each concept page.
  Plain text field + submit. List of existing comments shown
  newest-first, each with a date stamp. Visible to all viewers of the
  page (shared, not per-visitor).
- **Password gate**: client-side check for a fixed phrase,
  `purplelantern`. Not real auth — a casual-visitor deterrent only,
  per explicit requirement ("no login, just a simple gate"). Sets a
  cookie/localStorage flag on success so it doesn't re-prompt every
  page.
- **Backend**: Cloudflare Worker + KV, deployed separately from the
  GitHub Pages static hosting. Two endpoints:
  - `POST /comments` — `{ concept, page, text }` → stores with
    server-generated timestamp.
  - `GET /comments?concept=X&page=Y` — returns stored comments for
    that page, newest-first.
  No auth on the Worker beyond CORS restricted to the review site's
  origin — acceptable given this is low-stakes internal client
  feedback, not user data.

### 4. Hosting
- `design/concepts/` (plus the sidebar/gate additions) built and
  deployed via **GitHub Pages** from the `1234` repo.
- Custom domain `1234.pasadenaworks.com`, DNS CNAME added in
  Cloudflare (same pattern as the existing `pasadenaworks.com` GitHub
  Pages setup).
- Comments Worker deployed to Cloudflare under its own route/subdomain
  (e.g. `1234-comments.pasadenaworks.workers.dev` or a mapped
  subdomain — exact naming decided during implementation).
- A link to `1234.pasadenaworks.com` (with a note that the password is
  `purplelantern`) added to the `ops-panel` project
  (`~/Projects/property-page/ops-panel`) so it's discoverable from
  `ops.pasadenaworks.com`.

## Out of scope (explicitly deferred)

- Any visual/content design work — concepts come from Claude Design,
  not this process.
- Picking a concept, building the real site's pages/theme from a
  chosen concept, or trilingual routing — happens only after the
  client picks a direction, in a separate spec.
- Real authentication for the review site or the comments API — the
  password gate is intentionally simple/client-side, per requirement.
- Scheduling API integration — noted as a likely future feature
  (`features/scheduling/` reserved for it) but not designed or built
  here.

## Testing / verification

- Playwright screenshots per concept (see step 2) confirm the raw
  import renders correctly before any review-site code touches it.
- Manual check of comments sidebar (submit, reload, see it persisted
  and dated) and password gate (wrong phrase blocks, correct phrase
  unlocks and persists across page loads) before considering the
  review site done.

## Open items carried into implementation planning

- Exact Worker route/subdomain naming.
- Whether KV is sufficient long-term or a cap on comment volume/size
  is needed (unlikely to matter at this scale — internal review only).
