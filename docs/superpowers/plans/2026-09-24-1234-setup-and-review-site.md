# 1234 Site Setup & Design Concept Review — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the `thirstypig/1234` repo with an Astro feature-module scaffold, import the five Claude-Design concept exports unchanged, and add a password-gated, commentable review site at `1234.pasadenaworks.com` so the client can leave dated feedback on each concept.

**Architecture:** The real site (Astro, feature modules) and the throwaway review site (static concept HTML + a small vanilla-JS gate/sidebar layer + a Cloudflare Worker for comment storage) are separate concerns living in the same repo. GitHub Pages serves both; the Worker is deployed independently to Cloudflare and called over `fetch` from the static pages.

**Tech Stack:** Astro + TypeScript, vanilla JS (no framework) for the gate/sidebar overlay, Cloudflare Workers + KV for the comments API, GitHub Actions for Pages deploy, Playwright for verification screenshots.

**Spec:** `docs/superpowers/specs/2026-09-24-1234-orthok-site-design.md`

## Global Constraints

- Repo: `thirstypig/1234`, public.
- Feature module isolation: no folder under `src/features/*` imports from
  another `src/features/*` folder; shared code only from `src/layouts/`
  or `src/components/`.
- Design concept files copied from the export are **never edited** —
  no touching tokens, CSS, or copy inside `design/concepts/concepts/`.
- Password gate value is exactly `purplelantern`, client-side only, no
  accounts.
- Comments are shared across all viewers (not per-browser) and each
  one carries a server-generated timestamp.
- Stop after the import-verification step (Task 3) and show the user
  before continuing to docs/issues/PR (Task 8+).

## Review Focus

- Missing/renamed concept preview path (e.g. a concept's homepage file
  isn't at the expected `preview/Homepage desktop EN/preview.html`) —
  the verification step must report this instead of silently skipping it.
- Empty comment text submitted — the API must reject it rather than
  storing a blank, dateless-looking entry.
- Two people viewing the same concept page at once — the sidebar must
  show both viewers' comments, not just the local submitter's.
- Wrong password entered — the gate must not unlock, and must not leak
  the real content into the page DOM before the check passes.
- Worker called from an unexpected origin — CORS must restrict to the
  review site's own origin, not `*`.

---

## Task 1: Scaffold Astro project with feature-module structure

**Files:**
- Create: `package.json`, `astro.config.mjs`, `tsconfig.json` (via `npm create astro@latest`)
- Create: `src/features/home/.gitkeep`, `src/features/services/.gitkeep`, `src/features/testimonials/.gitkeep`, `src/features/scheduling/.gitkeep`, `src/features/contact/.gitkeep`
- Create: `src/layouts/BaseLayout.astro`
- Create: `src/components/.gitkeep`
- Create: `src/pages/index.astro`
- Modify: `.gitignore` (Astro default + `dist/`, `.astro/`, `node_modules/`)

**Interfaces:**
- Produces: `src/layouts/BaseLayout.astro` — an Astro layout component accepting a `title: string` prop via frontmatter, rendering `<slot />` in `<body>`. Later tasks (real site pages, once built in a future plan) will import this; nothing in this plan consumes it yet beyond `index.astro`.

- [ ] **Step 1: Scaffold Astro**

```bash
cd /Users/jameschang/Projects/1234
npm create astro@latest . -- --template minimal --typescript strict --no-install --no-git
npm install
```

- [ ] **Step 2: Create feature module folders**

```bash
mkdir -p src/features/{home,services,testimonials,scheduling,contact}
touch src/features/home/.gitkeep src/features/services/.gitkeep \
      src/features/testimonials/.gitkeep src/features/scheduling/.gitkeep \
      src/features/contact/.gitkeep
mkdir -p src/components
touch src/components/.gitkeep
```

- [ ] **Step 3: Add a minimal shared layout**

Create `src/layouts/BaseLayout.astro`:

```astro
---
interface Props {
  title: string;
}
const { title } = Astro.props;
---
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <title>{title}</title>
  </head>
  <body>
    <slot />
  </body>
</html>
```

- [ ] **Step 4: Update the default index page to use the layout**

Replace `src/pages/index.astro` with:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---
<BaseLayout title="1234 Ortho-K Vision Care">
  <h1>1234 Ortho-K Vision Care — site under construction</h1>
</BaseLayout>
```

- [ ] **Step 5: Verify the build works**

```bash
npm run build
```
Expected: build succeeds, `dist/index.html` exists and contains "site under construction".

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "Scaffold Astro project with feature-module structure

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

## Task 2: Create GitHub repo and push

**Files:** none (repo/remote operation only)

- [ ] **Step 1: Create the repo under thirstypig**

```bash
gh repo create thirstypig/1234 --public --source=. --remote=origin
```

- [ ] **Step 2: Push main**

```bash
git branch -M main
git push -u origin main
```

- [ ] **Step 3: Verify**

```bash
gh repo view thirstypig/1234 --web=false
```
Expected: shows the repo with the commit from Task 1.

---

## Task 3: Import design concepts and verify (STOP POINT)

**Files:**
- Create: `design/concepts/` (entire unzipped contents of `orthok-design-concepts.zip`)
- Create: `design/concepts/generator/.gitignore`
- Create (gitignored): `design/concepts/_qa/*.png`

**Interfaces:**
- Consumes: nothing from Task 1/2 code — this is a parallel, independent folder tree.
- Produces: `design/concepts/concepts/<A-E>/preview/...` paths that Task 4-6 will overlay the gate/sidebar onto without modifying.

- [ ] **Step 1: Branch**

```bash
git status   # must be clean
git pull origin main
git checkout -b design/concepts-import
```

- [ ] **Step 2: Unzip and copy in unchanged**

```bash
mkdir -p /tmp/orthok-design-concepts
unzip -q ~/Downloads/orthok-design-concepts.zip -d /tmp/orthok-design-concepts
mkdir -p design/concepts
cp -R /tmp/orthok-design-concepts/. design/concepts/
```

Confirm nothing was altered:
```bash
diff -rq /tmp/orthok-design-concepts design/concepts
```
Expected: no output (identical).

- [ ] **Step 3: Add generator gitignore**

Create `design/concepts/generator/.gitignore`:
```
out/
shots/
__pycache__/
*.ttf
```

- [ ] **Step 4: Gitignore the QA screenshots folder**

Add to root `.gitignore`:
```
design/concepts/_qa/
```

- [ ] **Step 5: Read the export's README**

```bash
cat design/concepts/README.md
```
Note the folder layout, regeneration steps, per-concept rules, and the
"Open issues" list — Task 8 needs the open issues list verbatim.

- [ ] **Step 6: Serve locally**

```bash
npx serve design/concepts -l 4321 &
```

- [ ] **Step 7: Screenshot each concept with Playwright**

Create `/tmp/screenshot-concepts.mjs`:

```javascript
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';

const concepts = ['A', 'B', 'C', 'D', 'E'];
const pages = [
  { name: 'Homepage desktop EN', width: 1280, path: 'Homepage desktop EN' },
  { name: 'Homepage Traditional Chinese mobile', width: 390, path: 'Homepage Traditional Chinese mobile' },
];

mkdirSync('design/concepts/_qa', { recursive: true });

const browser = await chromium.launch();
const issues = [];

for (const concept of concepts) {
  for (const page of pages) {
    const ctx = await browser.newContext({ viewport: { width: page.width, height: 900 } });
    const tab = await ctx.newPage();
    const url = `http://localhost:4321/concepts/${concept}/preview/${encodeURIComponent(page.path)}/preview.html`;
    const consoleErrors = [];
    tab.on('console', (msg) => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });

    const response = await tab.goto(url).catch((e) => null);
    if (!response || !response.ok()) {
      issues.push(`${concept} / ${page.name}: page failed to load (${response ? response.status() : 'no response'})`);
      await ctx.close();
      continue;
    }

    const hasHorizontalScroll = await tab.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
    if (hasHorizontalScroll) issues.push(`${concept} / ${page.name}: horizontal scroll detected`);
    if (consoleErrors.length) issues.push(`${concept} / ${page.name}: console errors: ${consoleErrors.join('; ')}`);

    await tab.screenshot({ path: `design/concepts/_qa/${concept}-${page.name.replace(/\s+/g, '-')}.png`, fullPage: true });
    await ctx.close();
  }
}

await browser.close();
console.log(issues.length ? issues.join('\n') : 'No issues found.');
```

Run it:
```bash
node /tmp/screenshot-concepts.mjs
```

- [ ] **Step 8: Stop the local server**

```bash
kill %1
```

- [ ] **Step 9: STOP — report to user**

Show the console output from Step 7 (issues found, or "No issues
found"), list the 10 screenshots saved under `design/concepts/_qa/`,
and **wait for the user's go-ahead** before Task 4 onward.

---

## Task 4: Password gate (client-side)

**Files:**
- Create: `design/concepts/_review/gate.js`
- Test: `design/concepts/_review/gate.test.mjs`

**Interfaces:**
- Produces: `isUnlocked(): boolean`, `tryUnlock(phrase: string): boolean`, `installGate(rootDocument: Document): void` — exported from `gate.js`. Task 6 calls `installGate(document)` from each concept preview page.

- [ ] **Step 1: Write the failing tests**

Create `design/concepts/_review/gate.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert';
import { isUnlocked, tryUnlock } from './gate.js';

test('tryUnlock returns false for wrong phrase', () => {
  localStorage.clear();
  assert.strictEqual(tryUnlock('wrong phrase'), false);
  assert.strictEqual(isUnlocked(), false);
});

test('tryUnlock returns true for correct phrase and persists', () => {
  localStorage.clear();
  assert.strictEqual(tryUnlock('purplelantern'), true);
  assert.strictEqual(isUnlocked(), true);
});

test('tryUnlock is case-insensitive and trims whitespace', () => {
  localStorage.clear();
  assert.strictEqual(tryUnlock('  PurpleLantern  '), true);
});
```

This test file needs a `localStorage` global; run it under a browser-like
environment. Add a dev dependency:

```bash
npm install -D happy-dom
```

Add `design/concepts/_review/test-setup.mjs`:
```javascript
import { Window } from 'happy-dom';
const window = new Window();
globalThis.localStorage = window.localStorage;
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
node --import ./design/concepts/_review/test-setup.mjs --test design/concepts/_review/gate.test.mjs
```
Expected: FAIL — `gate.js` does not exist yet.

- [ ] **Step 3: Implement the gate**

Create `design/concepts/_review/gate.js`:

```javascript
const STORAGE_KEY = '1234-review-unlocked';
const PASSPHRASE = 'purplelantern';

export function isUnlocked() {
  return localStorage.getItem(STORAGE_KEY) === 'true';
}

export function tryUnlock(phrase) {
  const normalized = phrase.trim().toLowerCase().replace(/\s+/g, '');
  if (normalized === PASSPHRASE) {
    localStorage.setItem(STORAGE_KEY, 'true');
    return true;
  }
  return false;
}

export function installGate(rootDocument) {
  if (isUnlocked()) return;

  const overlay = rootDocument.createElement('div');
  overlay.id = 'review-gate-overlay';
  overlay.style.cssText = 'position:fixed;inset:0;background:#111;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:99999;font-family:sans-serif;gap:12px;';
  overlay.innerHTML = `
    <p>Enter the review password</p>
    <input type="password" id="review-gate-input" style="padding:8px;font-size:16px;" />
    <button id="review-gate-submit" style="padding:8px 16px;">Enter</button>
    <p id="review-gate-error" style="color:#f88;display:none;">Incorrect password.</p>
  `;
  rootDocument.body.style.overflow = 'hidden';
  rootDocument.body.appendChild(overlay);

  const submit = () => {
    const input = rootDocument.getElementById('review-gate-input');
    if (tryUnlock(input.value)) {
      overlay.remove();
      rootDocument.body.style.overflow = '';
    } else {
      rootDocument.getElementById('review-gate-error').style.display = 'block';
    }
  };

  rootDocument.getElementById('review-gate-submit').addEventListener('click', submit);
  rootDocument.getElementById('review-gate-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') submit();
  });
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
node --import ./design/concepts/_review/test-setup.mjs --test design/concepts/_review/gate.test.mjs
```
Expected: all 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add design/concepts/_review/gate.js design/concepts/_review/gate.test.mjs \
        design/concepts/_review/test-setup.mjs package.json package-lock.json
git commit -m "Add client-side password gate for review site

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

## Task 5: Comments Worker API (Cloudflare Worker + KV)

**Files:**
- Create: `workers/comments/src/index.ts`
- Create: `workers/comments/wrangler.toml`
- Test: `workers/comments/src/index.test.ts`
- Create: `workers/comments/package.json`, `workers/comments/tsconfig.json`

**Interfaces:**
- Produces: `POST /comments` accepting `{ concept: string, page: string, text: string }`, returns `201` with the stored `{ concept, page, text, createdAt }` on success, `400` if `text` is empty/whitespace-only or `concept`/`page` missing. `GET /comments?concept=X&page=Y` returns `200` with `{ comments: Array<{ text: string, createdAt: string }> }` sorted newest-first. Task 6's sidebar JS calls both.

- [ ] **Step 1: Scaffold the Worker project**

```bash
mkdir -p workers/comments/src
cd workers/comments
npm init -y
npm install -D wrangler typescript @cloudflare/workers-types vitest
```

Create `workers/comments/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2021",
    "module": "ES2022",
    "moduleResolution": "Bundler",
    "types": ["@cloudflare/workers-types"],
    "strict": true
  }
}
```

Create `workers/comments/wrangler.toml`:
```toml
name = "1234-review-comments"
main = "src/index.ts"
compatibility_date = "2026-09-24"

kv_namespaces = [
  { binding = "COMMENTS_KV", id = "REPLACE_WITH_REAL_KV_ID" }
]

[vars]
ALLOWED_ORIGIN = "https://1234.pasadenaworks.com"
```

- [ ] **Step 2: Write the failing tests**

Create `workers/comments/src/index.test.ts`:

```typescript
import { describe, it, expect, vi } from 'vitest';
import worker from './index';

function makeKvMock(initial: Record<string, string> = {}) {
  const store = { ...initial };
  return {
    get: vi.fn(async (key: string) => store[key] ?? null),
    put: vi.fn(async (key: string, value: string) => { store[key] = value; }),
  } as unknown as KVNamespace;
}

const env = (kv: KVNamespace) => ({ COMMENTS_KV: kv, ALLOWED_ORIGIN: 'https://1234.pasadenaworks.com' });

describe('POST /comments', () => {
  it('rejects empty text with 400', async () => {
    const kv = makeKvMock();
    const req = new Request('https://worker/comments', {
      method: 'POST',
      body: JSON.stringify({ concept: 'A', page: 'home', text: '   ' }),
    });
    const res = await worker.fetch(req, env(kv), {} as ExecutionContext);
    expect(res.status).toBe(400);
  });

  it('stores a valid comment with a timestamp', async () => {
    const kv = makeKvMock();
    const req = new Request('https://worker/comments', {
      method: 'POST',
      body: JSON.stringify({ concept: 'A', page: 'home', text: 'Looks great' }),
    });
    const res = await worker.fetch(req, env(kv), {} as ExecutionContext);
    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body.text).toBe('Looks great');
    expect(typeof body.createdAt).toBe('string');
    expect(kv.put).toHaveBeenCalled();
  });
});

describe('GET /comments', () => {
  it('returns comments newest-first', async () => {
    const stored = JSON.stringify([
      { text: 'first', createdAt: '2026-09-24T10:00:00.000Z' },
      { text: 'second', createdAt: '2026-09-24T11:00:00.000Z' },
    ]);
    const kv = makeKvMock({ 'A:home': stored });
    const req = new Request('https://worker/comments?concept=A&page=home');
    const res = await worker.fetch(req, env(kv), {} as ExecutionContext);
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.comments.map((c: any) => c.text)).toEqual(['second', 'first']);
  });
});
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
npx vitest run
```
Expected: FAIL — `./index` does not exist yet.

- [ ] **Step 4: Implement the Worker**

Create `workers/comments/src/index.ts`:

```typescript
export interface Env {
  COMMENTS_KV: KVNamespace;
  ALLOWED_ORIGIN: string;
}

interface Comment {
  text: string;
  createdAt: string;
}

function corsHeaders(origin: string) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const headers = corsHeaders(env.ALLOWED_ORIGIN);

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers });
    }

    const url = new URL(request.url);

    if (request.method === 'POST' && url.pathname === '/comments') {
      const body = await request.json<{ concept?: string; page?: string; text?: string }>();
      const concept = body.concept?.trim();
      const page = body.page?.trim();
      const text = body.text?.trim();

      if (!concept || !page || !text) {
        return new Response(JSON.stringify({ error: 'concept, page, and text are required' }), {
          status: 400,
          headers: { ...headers, 'Content-Type': 'application/json' },
        });
      }

      const key = `${concept}:${page}`;
      const existingRaw = await env.COMMENTS_KV.get(key);
      const existing: Comment[] = existingRaw ? JSON.parse(existingRaw) : [];
      const comment: Comment = { text, createdAt: new Date().toISOString() };
      existing.push(comment);
      await env.COMMENTS_KV.put(key, JSON.stringify(existing));

      return new Response(JSON.stringify(comment), {
        status: 201,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }

    if (request.method === 'GET' && url.pathname === '/comments') {
      const concept = url.searchParams.get('concept');
      const page = url.searchParams.get('page');
      if (!concept || !page) {
        return new Response(JSON.stringify({ error: 'concept and page query params are required' }), {
          status: 400,
          headers: { ...headers, 'Content-Type': 'application/json' },
        });
      }
      const key = `${concept}:${page}`;
      const raw = await env.COMMENTS_KV.get(key);
      const comments: Comment[] = raw ? JSON.parse(raw) : [];
      comments.sort((a, b) => b.createdAt.localeCompare(a.createdAt));

      return new Response(JSON.stringify({ comments }), {
        status: 200,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }

    return new Response('Not found', { status: 404, headers });
  },
};
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
npx vitest run
```
Expected: all tests PASS.

- [ ] **Step 6: Commit**

```bash
cd /Users/jameschang/Projects/1234
git add workers/comments
git commit -m "Add Cloudflare Worker + KV comments API

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

## Task 6: Comments sidebar (client-side) and wiring into concept pages

**Files:**
- Create: `design/concepts/_review/sidebar.js`
- Test: `design/concepts/_review/sidebar.test.mjs`
- Create: `design/concepts/_review/inject.js` (small script tag added to each preview page)
- Modify: each `design/concepts/concepts/<A-E>/preview/*/preview.html` — add one `<script type="module" src="/_review/inject.js"></script>` line before `</body>` (structural addition only, not a content/design edit)

**Interfaces:**
- Consumes: `installGate` from `gate.js` (Task 4); Worker endpoints from Task 5.
- Produces: `renderSidebar(container: HTMLElement, comments: Array<{text: string, createdAt: string}>): void`, `formatDate(iso: string): string` — exported from `sidebar.js`.

- [ ] **Step 1: Write the failing tests**

Create `design/concepts/_review/sidebar.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert';
import { formatDate, renderSidebar } from './sidebar.js';

test('formatDate renders a readable date', () => {
  assert.strictEqual(formatDate('2026-09-24T10:00:00.000Z'), new Date('2026-09-24T10:00:00.000Z').toLocaleString());
});

test('renderSidebar shows each comment with its date', () => {
  const container = document.createElement('div');
  renderSidebar(container, [
    { text: 'Love this one', createdAt: '2026-09-24T10:00:00.000Z' },
  ]);
  assert.ok(container.textContent.includes('Love this one'));
  assert.ok(container.textContent.includes(formatDate('2026-09-24T10:00:00.000Z')));
});

test('renderSidebar shows a placeholder when there are no comments', () => {
  const container = document.createElement('div');
  renderSidebar(container, []);
  assert.ok(container.textContent.includes('No comments yet'));
});
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
node --import ./design/concepts/_review/test-setup.mjs --test design/concepts/_review/sidebar.test.mjs
```
Expected: FAIL — `sidebar.js` does not exist yet.

(Note: `test-setup.mjs` from Task 4 uses happy-dom's `Window`, which
provides `document` too — no changes needed there.)

- [ ] **Step 3: Implement the sidebar**

Create `design/concepts/_review/sidebar.js`:

```javascript
export function formatDate(iso) {
  return new Date(iso).toLocaleString();
}

export function renderSidebar(container, comments) {
  container.innerHTML = '';
  if (comments.length === 0) {
    const empty = document.createElement('p');
    empty.textContent = 'No comments yet.';
    container.appendChild(empty);
    return;
  }
  for (const comment of comments) {
    const item = document.createElement('div');
    item.className = 'review-comment';
    const date = document.createElement('div');
    date.className = 'review-comment-date';
    date.textContent = formatDate(comment.createdAt);
    const text = document.createElement('div');
    text.className = 'review-comment-text';
    text.textContent = comment.text;
    item.appendChild(date);
    item.appendChild(text);
    container.appendChild(item);
  }
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
node --import ./design/concepts/_review/test-setup.mjs --test design/concepts/_review/sidebar.test.mjs
```
Expected: all 3 tests PASS.

- [ ] **Step 5: Write the injector that ties gate + sidebar + API together**

Create `design/concepts/_review/inject.js`:

```javascript
import { installGate } from './gate.js';
import { renderSidebar } from './sidebar.js';

const API_BASE = 'https://1234-review-comments.pasadenaworks.workers.dev';

function currentConceptAndPage() {
  const match = window.location.pathname.match(/\/concepts\/([A-E])\/preview\/([^/]+)\//);
  return match ? { concept: match[1], page: match[2] } : { concept: 'unknown', page: 'unknown' };
}

async function loadComments(concept, page) {
  const res = await fetch(`${API_BASE}/comments?concept=${encodeURIComponent(concept)}&page=${encodeURIComponent(page)}`);
  const body = await res.json();
  return body.comments ?? [];
}

async function submitComment(concept, page, text) {
  await fetch(`${API_BASE}/comments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ concept, page, text }),
  });
}

function buildSidebarShell() {
  const aside = document.createElement('aside');
  aside.id = 'review-sidebar';
  aside.style.cssText = 'position:fixed;top:0;right:0;width:320px;height:100vh;overflow-y:auto;background:#fafafa;border-left:1px solid #ddd;padding:16px;box-sizing:border-box;font-family:sans-serif;z-index:9998;';
  aside.innerHTML = `
    <h3>Feedback</h3>
    <div id="review-comment-list"></div>
    <textarea id="review-comment-input" style="width:100%;height:80px;margin-top:12px;"></textarea>
    <button id="review-comment-submit" style="margin-top:8px;">Add comment</button>
  `;
  document.body.appendChild(aside);
  return aside;
}

async function init() {
  installGate(document);
  const { concept, page } = currentConceptAndPage();
  const aside = buildSidebarShell();
  const list = aside.querySelector('#review-comment-list');

  const refresh = async () => renderSidebar(list, await loadComments(concept, page));
  await refresh();

  aside.querySelector('#review-comment-submit').addEventListener('click', async () => {
    const input = aside.querySelector('#review-comment-input');
    if (!input.value.trim()) return;
    await submitComment(concept, page, input.value);
    input.value = '';
    await refresh();
  });
}

init();
```

- [ ] **Step 6: Inject the script tag into every concept preview page**

```bash
find design/concepts/concepts -name preview.html -print0 | \
  xargs -0 sed -i '' 's#</body>#<script type="module" src="/_review/inject.js"></script></body>#'
```

Verify only the closing-body line changed, not design content:
```bash
git diff --stat design/concepts/concepts
```
Expected: every changed file shows `1 file changed, 1 insertion(+)` (or similar — one line added per file, nothing removed).

- [ ] **Step 7: Manual verification**

```bash
npx serve design/concepts -l 4321 &
```
Open `http://localhost:4321/concepts/A/preview/Homepage%20desktop%20EN/preview.html`
in a browser: confirm the gate overlay appears, wrong password shows the
error message and doesn't unlock, `purplelantern` unlocks and the
sidebar appears with "No comments yet." (Worker isn't deployed yet, so
the fetch will fail — confirm it fails gracefully, i.e. sidebar still
renders the shell without crashing the page; if it throws, wrap
`loadComments`'s fetch in try/catch returning `[]`.)

```bash
kill %1
```

- [ ] **Step 8: Commit**

```bash
git add design/concepts
git commit -m "Add comments sidebar and wire gate+sidebar into concept previews

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

## Task 7: Deploy Worker and hosting

**Files:** none (deploy/config operations)

- [ ] **Step 1: Create the KV namespace**

```bash
cd workers/comments
npx wrangler kv namespace create COMMENTS_KV
```
Copy the returned `id` into `wrangler.toml`'s `REPLACE_WITH_REAL_KV_ID`.

- [ ] **Step 2: Deploy the Worker**

```bash
npx wrangler deploy
```
Expected output includes the deployed URL, e.g.
`https://1234-review-comments.<subdomain>.workers.dev`. If it differs
from the `API_BASE` hardcoded in `design/concepts/_review/inject.js`,
update that constant to match and commit the fix.

- [ ] **Step 3: Add GitHub Pages workflow for the review site**

Create `.github/workflows/deploy-review-site.yml`:

```yaml
name: Deploy review site to GitHub Pages

on:
  push:
    branches: [design/concepts-import, main]
    paths:
      - 'design/concepts/**'

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: design/concepts
      - id: deployment
        uses: actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e # v4
```

- [ ] **Step 4: Enable Pages and set the custom domain**

```bash
gh api repos/thirstypig/1234/pages -X POST -f "build_type=workflow" \
  -f "source[branch]=main" -f "source[path]=/"
echo "1234.pasadenaworks.com" > design/concepts/CNAME
git add design/concepts/CNAME .github/workflows/deploy-review-site.yml
git commit -m "Deploy review site to GitHub Pages with custom domain

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 5: Add the Cloudflare DNS record**

Add a CNAME record in the Cloudflare dashboard for `pasadenaworks.com`:
`1234` → `thirstypig.github.io`, proxy status DNS-only (matching how
the apex `pasadenaworks.com` A-records are set up, per
`~/projects/pasadenaworks/README.md`'s DNS section). This is a manual
dashboard step — no CLI access to that Cloudflare account has been
established in this session; do it yourself and confirm here once done.

- [ ] **Step 6: Verify end-to-end**

Once DNS propagates, visit `https://1234.pasadenaworks.com/concepts/A/preview/Homepage%20desktop%20EN/preview.html`,
confirm the gate, submit a comment, reload, confirm it persists and
shows a date.

---

## Task 8: Docs, issues, PR (only after Task 3's stop point is cleared by the user)

**Files:**
- Create/Modify: `CLAUDE.md`

- [ ] **Step 1: Add the CLAUDE.md section**

Append to `CLAUDE.md` (create if missing):

```markdown
## Design concepts

Design concepts live in `design/concepts/`; each concept's source of
truth is `concepts/<X>/project/` (`tokens.json`, `README.md`,
`components/bundle.css`, component READMEs).

Rules:
- EN / 简体 / 繁體 as separate pages with the switcher always visible.
- Chinese body >= 17px, line height >= 1.7.
- No logo (plain-text name).
- Use only client-provided copy.
- Never add statistics, success rates, patient counts, or
  "best/most effective" claims.
- All text WCAG AA.
- "Book a consultation" in the first screen and at the bottom.
- Mobile sticky Book/Message bar.

Treat everything in `design/concepts/` as reference until the client
picks a direction. Don't build pages from it without asking first.

The review site (`design/concepts/_review/`) overlays a password gate
and a comments sidebar on top of the concepts for client feedback; the
concepts themselves are never edited by it.
```

- [ ] **Step 2: File one issue per open item**

```bash
gh label create design --description "Design concept review" --color FBCA04 || true
# Repeat the following per line in design/concepts/README.md's "Open issues" section:
gh issue create --repo thirstypig/1234 --title "<short title from open issue>" \
  --body "<plain-English restatement>" --label design
```

- [ ] **Step 3: Commit docs**

```bash
git add CLAUDE.md
git commit -m "Document design concepts folder and review-site rules

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step 4: Push and open the PR**

```bash
git push -u origin design/concepts-import
gh pr create --repo thirstypig/1234 --title "Import website design concepts A-E" \
  --body "Imports the five Claude-Design concept exports unchanged into design/concepts/, plus a password-gated comments review site at 1234.pasadenaworks.com.

## What's in it
- design/concepts/ — unmodified export (concepts A-E, generator, README)
- design/concepts/_review/ — client-side password gate + comments sidebar
- workers/comments/ — Cloudflare Worker + KV backing the comments API
- .github/workflows/deploy-review-site.yml — GitHub Pages deploy

## View locally
npx serve design/concepts, then open a concept's preview.html

## Issues filed
<list the issue links from Step 2>

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

Do not merge.

---

## Task 9: Add link to ops-panel

**Files:**
- Modify: a markdown/data file in `~/Projects/property-page/ops-panel` that lists panel links (locate it first — inspect that repo's structure before editing, since its exact link-list format isn't known yet from this plan).

- [ ] **Step 1: Inspect the ops-panel repo to find where links are defined**

```bash
cd ~/Projects/property-page/ops-panel
grep -ril "pasadenaworks.com" . | grep -v node_modules
```

- [ ] **Step 2: Add the entry**

Follow whatever pattern the existing entries use (likely a markdown
table or JSON/YAML list) to add:
- Name: `1234 — design concept review`
- URL: `https://1234.pasadenaworks.com`
- Note: `Password: purplelantern`

- [ ] **Step 3: Commit in that repo**

```bash
git add -A
git commit -m "Add link to 1234 design concept review site

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

Push per that repo's normal workflow (check if it auto-deploys via
Railway on push, per MASTER-PORTS.md — if so, a plain push is enough).
