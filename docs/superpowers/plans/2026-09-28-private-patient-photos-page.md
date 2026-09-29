# Private Patient-Photos Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A password-protected page on a standalone Cloudflare Worker where the practice sees the 23 held-back patient photos, reads why they can't be published, and downloads a photo-release form in English, 繁體 or 简体.

**Architecture:** One Cloudflare Worker (`1234-patient-photos`, served on `*.workers.dev`) checks a password on the server, sets an HMAC-signed 12-hour cookie, and only then serves the HTML page, the photos and the PDFs from a private R2 bucket. Failed logins are counted per IP in KV. Photos and PDFs are prepared on the Mac and uploaded with wrangler; none of them enter git.

**Tech Stack:** TypeScript Worker (wrangler 4, `@cloudflare/workers-types`), vitest, R2, KV, Python 3 + Pillow (photo prep), Playwright Chromium `page.pdf()` (release forms), exiftool / pdfinfo / pdftotext (checks).

**Spec:** `docs/superpowers/specs/2026-09-28-private-patient-photos-page-design.md`

## Global Constraints

- Project lives at `~/Projects/1234-patient-photos/` — **outside** the public `thirstypig/1234` repo. Nothing from this plan except the spec and this plan file goes into `thirstypig/1234`.
- No photo, PDF, password or session key is ever committed anywhere. `upload/` is git-ignored.
- Password check happens in the Worker. The password lives only in `wrangler secret put PAGE_PASSWORD`; the signing key only in `wrangler secret put SESSION_KEY`.
- Cookie: `session=<expiry>.<hex hmac>; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=43200`.
- Every response has `X-Robots-Tag: noindex, nofollow`, `Cache-Control: private, no-store`, `Referrer-Policy: no-referrer`.
- Rate limit: 10 failed logins per IP per 15 minutes; the next attempt gets 429.
- Photos are numbered `P-01` … `P-23`; R2 keys are `photos/P-NN.jpg`.
- Release PDFs: `release-en.pdf`, `release-zh-hant.pdf`, `release-zh-hans.pdf`, Letter size, every font size ≥ 14 pt, footer marks them as a draft for legal review.
- Patient-photo metadata (GPS, dates, camera) is stripped; images are re-encoded at ≤ 1600 px on the long side.

## Review Focus

- A staff member types the two-word password on a phone auto-capitalized and with a space between the words → they should get in. Pinned in Task 4 (`passwordMatches` normalizes case and spaces) and Task 4's router test.
- Someone forwards a direct photo link (`/img/P-05`) to a person without the cookie → 401, no image bytes. Pinned in Task 4.
- A hand-typed or crafted path (`/img/P-99`, `/img/..%2Frelease-en.pdf`, `/img/P-1`) → 404 for logged-in users and 401 for others, never an arbitrary R2 key. Pinned in Task 4.
- A photo is listed in the manifest but missing from R2 (upload skipped one) → 404, not a 500 or a broken page. Pinned in Task 4.
- The Worker is deployed before the secrets are set → a clear 500 "not configured", never a login that accepts an empty password. Pinned in Task 4.

---

## File structure (new project `~/Projects/1234-patient-photos/`)

| File | Responsibility |
|---|---|
| `package.json`, `tsconfig.json`, `wrangler.toml`, `.gitignore` | Toolchain and bindings (`PHOTOS_BUCKET` R2, `LOGIN_KV` KV) |
| `src/session.ts` | Cookie read, token create/verify (HMAC-SHA-256), password compare |
| `src/ratelimit.ts` | Per-IP failed-login counter in KV |
| `src/photos.json` | Manifest: id, source file, origin, alt text, optional note |
| `src/photos.ts` | Typed access to the manifest, R2 key for a photo |
| `src/pages.ts` | HTML for the login page and the photos page |
| `src/index.ts` | Router: login, page, `/img/P-NN`, `/release-<lang>.pdf`, headers |
| `src/*.test.ts` | vitest tests per module |
| `scripts/prepare_photos.py` | Re-encode sources → `upload/photos/P-NN.jpg`, metadata stripped |
| `form/text.json`, `form/template.html`, `scripts/build-pdfs.mjs` | Release form text (3 languages), layout, PDF build + 14 pt check |
| `scripts/upload.sh` | Put photos and PDFs into R2 |

---

### Task 1: Scaffold the project and the session module

**Files:**
- Create: `~/Projects/1234-patient-photos/package.json`, `tsconfig.json`, `wrangler.toml`, `.gitignore`
- Create: `src/session.ts`
- Test: `src/session.test.ts`

**Interfaces:**
- Produces:
  - `readCookie(request: Request, name: string): string | null`
  - `createSessionToken(key: string, now: number, ttlMs: number): Promise<string>`
  - `verifySessionToken(token: string | null, key: string, now: number): Promise<boolean>`
  - `normalizePassword(input: string): string`
  - `passwordMatches(input: string, secret: string): Promise<boolean>`

- [ ] **Step 1: Create the project files**

```bash
mkdir -p ~/Projects/1234-patient-photos/{src,scripts,form,upload/photos} && cd ~/Projects/1234-patient-photos && git init -q
```

`package.json`:
```json
{
  "name": "1234-patient-photos",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "vitest run",
    "typecheck": "tsc --noEmit",
    "photos": "python3 scripts/prepare_photos.py",
    "pdfs": "node scripts/build-pdfs.mjs",
    "upload": "bash scripts/upload.sh",
    "deploy": "wrangler deploy"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^5.20260924.1",
    "playwright": "^1.63.0",
    "typescript": "^7.0.2",
    "vitest": "^5.0.1",
    "wrangler": "^4.143.0"
  }
}
```

`tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "Bundler",
    "types": ["@cloudflare/workers-types"],
    "resolveJsonModule": true,
    "strict": true
  },
  "include": ["src"]
}
```

`wrangler.toml` (the KV id is filled in during Task 7):
```toml
name = "1234-patient-photos"
main = "src/index.ts"
compatibility_date = "2026-09-28"
workers_dev = true

r2_buckets = [
  { binding = "PHOTOS_BUCKET", bucket_name = "1234-patient-photos" }
]

kv_namespaces = [
  { binding = "LOGIN_KV", id = "REPLACED_IN_TASK_7" }
]
```

`.gitignore`:
```
node_modules/
.wrangler/
upload/
.dev.vars
```

Run: `npm install`
Expected: installs without errors.

- [ ] **Step 2: Write the failing tests** — `src/session.test.ts`

```ts
import { describe, it, expect } from 'vitest';
import { readCookie, createSessionToken, verifySessionToken, normalizePassword, passwordMatches } from './session';

const KEY = 'test-signing-key';
const HOUR = 60 * 60 * 1000;

describe('readCookie', () => {
  it('finds a cookie among several', () => {
    const r = new Request('https://x/', { headers: { Cookie: 'a=1; session=abc.def; b=2' } });
    expect(readCookie(r, 'session')).toBe('abc.def');
  });
  it('returns null when absent', () => {
    expect(readCookie(new Request('https://x/'), 'session')).toBeNull();
  });
});

describe('session tokens', () => {
  it('accepts a fresh token', async () => {
    const t = await createSessionToken(KEY, 1_000, 12 * HOUR);
    expect(await verifySessionToken(t, KEY, 1_000 + HOUR)).toBe(true);
  });
  it('rejects an expired token', async () => {
    const t = await createSessionToken(KEY, 1_000, 12 * HOUR);
    expect(await verifySessionToken(t, KEY, 1_000 + 12 * HOUR)).toBe(false);
  });
  it('rejects a token with an edited expiry', async () => {
    const t = await createSessionToken(KEY, 1_000, 12 * HOUR);
    const [, sig] = t.split('.');
    expect(await verifySessionToken(`${Number.MAX_SAFE_INTEGER}.${sig}`, KEY, 2_000)).toBe(false);
  });
  it('rejects a token signed with another key', async () => {
    const t = await createSessionToken('other-key', 1_000, 12 * HOUR);
    expect(await verifySessionToken(t, KEY, 2_000)).toBe(false);
  });
  it('rejects null and malformed tokens', async () => {
    for (const bad of [null, '', 'abc', '123', '123.', '.abc', '1.2.3']) {
      expect(await verifySessionToken(bad, KEY, 0)).toBe(false);
    }
  });
});

describe('passwords', () => {
  it('normalizes case and spaces', () => {
    expect(normalizePassword('  Maple Cloud ')).toBe('maplecloud');
  });
  it('matches regardless of case and spacing', async () => {
    expect(await passwordMatches('Maple Cloud', 'maplecloud')).toBe(true);
  });
  it('rejects a wrong or empty password', async () => {
    expect(await passwordMatches('maplecloudy', 'maplecloud')).toBe(false);
    expect(await passwordMatches('', 'maplecloud')).toBe(false);
  });
});
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `npx vitest run src/session.test.ts`
Expected: FAIL — cannot resolve `./session`.

- [ ] **Step 4: Implement** — `src/session.ts`

```ts
const enc = new TextEncoder();

const hex = (buf: ArrayBuffer) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');

async function hmac(key: string, data: string): Promise<string> {
  const k = await crypto.subtle.importKey('raw', enc.encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return hex(await crypto.subtle.sign('HMAC', k, enc.encode(data)));
}

const sha256 = async (s: string) => hex(await crypto.subtle.digest('SHA-256', enc.encode(s)));

/** Equal-length strings compared without an early exit. */
function safeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

export function readCookie(request: Request, name: string): string | null {
  for (const part of (request.headers.get('Cookie') ?? '').split(';')) {
    const [k, ...v] = part.trim().split('=');
    if (k === name) return v.join('=');
  }
  return null;
}

export async function createSessionToken(key: string, now: number, ttlMs: number): Promise<string> {
  const exp = String(now + ttlMs);
  return `${exp}.${await hmac(key, exp)}`;
}

export async function verifySessionToken(token: string | null, key: string, now: number): Promise<boolean> {
  if (!token) return false;
  const parts = token.split('.');
  if (parts.length !== 2) return false;
  const [exp, sig] = parts;
  if (!/^\d+$/.test(exp) || !sig) return false;
  if (Number(exp) <= now) return false;
  return safeEqual(sig, await hmac(key, exp));
}

/** "Maple Cloud" and "maplecloud" are the same password. */
export function normalizePassword(input: string): string {
  return input.toLowerCase().replace(/\s+/g, '');
}

export async function passwordMatches(input: string, secret: string): Promise<boolean> {
  // Hashing both sides makes the comparison length-independent.
  const [a, b] = await Promise.all([sha256(normalizePassword(input)), sha256(normalizePassword(secret))]);
  return normalizePassword(input).length > 0 && safeEqual(a, b);
}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `npx vitest run src/session.test.ts`
Expected: PASS (10 tests).

- [ ] **Step 6: Commit**

```bash
git add package.json package-lock.json tsconfig.json wrangler.toml .gitignore src/session.ts src/session.test.ts
git commit -m "Add session tokens and password check for the patient-photos Worker"
```

---

### Task 2: Failed-login rate limit

**Files:**
- Create: `src/ratelimit.ts`, `src/test-helpers.ts`
- Test: `src/ratelimit.test.ts`

**Interfaces:**
- Produces:
  - `MAX_FAILURES = 10`, `WINDOW_MS = 15 * 60 * 1000`
  - `isLocked(kv: KVNamespace, ip: string, now: number): Promise<boolean>`
  - `recordFailure(kv: KVNamespace, ip: string, now: number): Promise<void>`

- [ ] **Step 1: Write the shared fake KV** — `src/test-helpers.ts` (a plain module, so importing it doesn't re-run any tests)

```ts
import { vi } from 'vitest';

export function makeKv() {
  const store: Record<string, string> = {};
  return {
    store,
    get: vi.fn(async (k: string, type?: string) => (k in store ? (type === 'json' ? JSON.parse(store[k]) : store[k]) : null)),
    put: vi.fn(async (k: string, v: string) => { store[k] = v; }),
  } as unknown as KVNamespace & { store: Record<string, string> };
}
```

- [ ] **Step 1b: Write the failing tests** — `src/ratelimit.test.ts`

```ts
import { describe, it, expect } from 'vitest';
import { isLocked, recordFailure, MAX_FAILURES, WINDOW_MS } from './ratelimit';
import { makeKv } from './test-helpers';

describe('rate limit', () => {
  it('is not locked with no failures', async () => {
    expect(await isLocked(makeKv(), '1.2.3.4', 0)).toBe(false);
  });
  it('locks after MAX_FAILURES failures inside the window', async () => {
    const kv = makeKv();
    for (let i = 0; i < MAX_FAILURES - 1; i++) await recordFailure(kv, '1.2.3.4', i * 1000);
    expect(await isLocked(kv, '1.2.3.4', 10_000)).toBe(false);
    await recordFailure(kv, '1.2.3.4', 11_000);
    expect(await isLocked(kv, '1.2.3.4', 12_000)).toBe(true);
  });
  it('unlocks once the window has passed', async () => {
    const kv = makeKv();
    for (let i = 0; i < MAX_FAILURES; i++) await recordFailure(kv, '1.2.3.4', 0);
    expect(await isLocked(kv, '1.2.3.4', WINDOW_MS + 1)).toBe(false);
  });
  it('counts each IP separately', async () => {
    const kv = makeKv();
    for (let i = 0; i < MAX_FAILURES; i++) await recordFailure(kv, '1.1.1.1', 0);
    expect(await isLocked(kv, '2.2.2.2', 1)).toBe(false);
  });
  it('starts a fresh count after the window', async () => {
    const kv = makeKv();
    for (let i = 0; i < MAX_FAILURES; i++) await recordFailure(kv, '1.2.3.4', 0);
    await recordFailure(kv, '1.2.3.4', WINDOW_MS + 5);
    expect(JSON.parse(kv.store['fail:1.2.3.4']).count).toBe(1);
  });
});
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `npx vitest run src/ratelimit.test.ts`
Expected: FAIL — cannot resolve `./ratelimit`.

- [ ] **Step 3: Implement** — `src/ratelimit.ts`

```ts
export const MAX_FAILURES = 10;
export const WINDOW_MS = 15 * 60 * 1000;

interface Failures { count: number; first: number }
const key = (ip: string) => `fail:${ip}`;

async function current(kv: KVNamespace, ip: string, now: number): Promise<Failures | null> {
  const r = await kv.get<Failures>(key(ip), 'json');
  return r && now - r.first < WINDOW_MS ? r : null;
}

export async function isLocked(kv: KVNamespace, ip: string, now: number): Promise<boolean> {
  const r = await current(kv, ip, now);
  return !!r && r.count >= MAX_FAILURES;
}

export async function recordFailure(kv: KVNamespace, ip: string, now: number): Promise<void> {
  const r = await current(kv, ip, now);
  const next: Failures = r ? { count: r.count + 1, first: r.first } : { count: 1, first: now };
  await kv.put(key(ip), JSON.stringify(next), { expirationTtl: WINDOW_MS / 1000 });
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `npx vitest run src/ratelimit.test.ts`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add src/ratelimit.ts src/ratelimit.test.ts src/test-helpers.ts
git commit -m "Limit failed logins to 10 per IP per 15 minutes"
```

---

### Task 3: Photo manifest and the two HTML pages

**Files:**
- Create: `src/photos.json`, `src/photos.ts`, `src/pages.ts`
- Test: `src/pages.test.ts`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces:
  - `interface Photo { id: string; file: string; origin: string; alt: string; note?: string }`
  - `PHOTOS: Photo[]`, `findPhoto(id: string): Photo | undefined`, `photoKey(id: string): string` → `photos/<id>.jpg`
  - `LANGS = ['en', 'zh-hant', 'zh-hans'] as const`, `type Lang`
  - `loginPage(error?: string): string`, `photosPage(photos: Photo[]): string`

- [ ] **Step 1: Write the manifest** — `src/photos.json`

```json
[
  { "id": "P-01", "file": "~/Downloads/IMG_2347.jpeg", "origin": "Sent 2026-09-28", "alt": "Girl holding her lens record card in the clinic", "note": "The record card shows visit dates and prescription values. Blur the card before any use, even with a signed release." },
  { "id": "P-02", "file": "~/Downloads/fwd/3aa3b5e82f4b86d858dd20f30f22fd.jpeg", "origin": "Sent 2026-09-28", "alt": "Young man at the lens-training desk giving two thumbs up" },
  { "id": "P-03", "file": "~/Downloads/fwd/39c31b1259f56c3e637451f7df5f7b_livephoto.jpeg", "origin": "Sent 2026-09-28", "alt": "Staff member checking a patient's eyes at the training desk" },
  { "id": "P-04", "file": "~/Downloads/fwd/d91f7a0eb577c3c527b55b09378b0d.jpeg", "origin": "Sent 2026-09-28", "alt": "Young woman with green hair holding the 1234 sign" },
  { "id": "P-05", "file": "~/Downloads/fwd/0d760cd46a29e016879e6be039fa7c.jpeg", "origin": "Sent 2026-09-28", "alt": "Child putting in an ortho-k lens" },
  { "id": "P-06", "file": "~/Downloads/fwd/ae397ebd85ef0050b958edf8ad8fa9.jpeg", "origin": "Sent 2026-09-28", "alt": "Two children at the exam machines with staff and a parent" },
  { "id": "P-07", "file": "~/Downloads/fwd/62bd9ea175ffa0ec4ed30a77c43efb.jpeg", "origin": "Sent 2026-09-28", "alt": "Patient putting in a lens", "note": "Phone screenshot with black bars. Crop before any use." },
  { "id": "P-08", "file": "~/Downloads/fwd/010512fc547a59b45a8a090049d78c.jpeg", "origin": "Sent 2026-09-28", "alt": "Young man holding the 1234 sign", "note": "Phone screenshot with Edit/Done buttons. Crop before any use." },
  { "id": "P-09", "file": "~/Downloads/fwd/IMG_0916.jpeg", "origin": "Sent 2026-09-28", "alt": "Boy standing by the clinic window" },
  { "id": "P-10", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-002.jpg", "origin": "Old website", "alt": "Patient photo from the old website (002)" },
  { "id": "P-11", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-013.jpg", "origin": "Old website", "alt": "Patient photo from the old website (013)" },
  { "id": "P-12", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-016.jpg", "origin": "Old website", "alt": "Patient photo from the old website (016)" },
  { "id": "P-13", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-026.jpg", "origin": "Old website", "alt": "Patient photo from the old website (026)" },
  { "id": "P-14", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-028.jpg", "origin": "Old website", "alt": "Patient photo from the old website (028)" },
  { "id": "P-15", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-031.jpg", "origin": "Old website", "alt": "Patient photo from the old website (031)" },
  { "id": "P-16", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-042.jpg", "origin": "Old website", "alt": "Patient photo from the old website (042)" },
  { "id": "P-17", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-045.jpg", "origin": "Old website", "alt": "Patient photo from the old website (045)" },
  { "id": "P-18", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-050.jpg", "origin": "Old website", "alt": "Patient photo from the old website (050)" },
  { "id": "P-19", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-062.jpg", "origin": "Old website", "alt": "Patient photo from the old website (062)" },
  { "id": "P-20", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-063.jpg", "origin": "Old website", "alt": "Patient photo from the old website (063)" },
  { "id": "P-21", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-064.jpg", "origin": "Old website", "alt": "Patient photo from the old website (064)" },
  { "id": "P-22", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-067.jpg", "origin": "Old website", "alt": "Patient photo from the old website (067)" },
  { "id": "P-23", "file": "~/Projects/1234/assets/legacy/originals/1234orthok-com-068.jpg", "origin": "Old website", "alt": "Patient photo from the old website (068)" }
]
```

`src/photos.ts`:
```ts
import list from './photos.json';

export interface Photo { id: string; file: string; origin: string; alt: string; note?: string }

export const PHOTOS: Photo[] = list;
export const findPhoto = (id: string): Photo | undefined => PHOTOS.find((p) => p.id === id);
export const photoKey = (id: string): string => `photos/${id}.jpg`;

export const LANGS = ['en', 'zh-hant', 'zh-hans'] as const;
export type Lang = (typeof LANGS)[number];
```

- [ ] **Step 2: Write the failing tests** — `src/pages.test.ts`

```ts
import { describe, it, expect } from 'vitest';
import { loginPage, photosPage } from './pages';
import { PHOTOS } from './photos';

describe('loginPage', () => {
  it('posts a password field to /login and is not indexed', () => {
    const h = loginPage();
    expect(h).toContain('method="post" action="/login"');
    expect(h).toContain('type="password" name="password"');
    expect(h).toContain('autocapitalize="none"');
    expect(h).toContain('<meta name="robots" content="noindex, nofollow">');
  });
  it('shows an error, escaped', () => {
    expect(loginPage('<b>no</b>')).toContain('&lt;b&gt;no&lt;/b&gt;');
  });
  it('reveals no photo or form content', () => {
    const h = loginPage();
    expect(h).not.toContain('/img/');
    expect(h).not.toContain('release-');
  });
});

describe('photosPage', () => {
  const h = photosPage(PHOTOS);
  it('lists all 23 photos with their numbers', () => {
    expect(PHOTOS).toHaveLength(23);
    for (const p of PHOTOS) {
      expect(h).toContain(`src="/img/${p.id}"`);
      expect(h).toContain(`>${p.id}<`);
    }
  });
  it('links all three release forms', () => {
    for (const l of ['en', 'zh-hant', 'zh-hans']) expect(h).toContain(`href="/release-${l}.pdf"`);
  });
  it('explains the reason in plain words', () => {
    expect(h).toContain('HIPAA');
    expect(h).toContain('parent or legal guardian');
    expect(h).toContain('Confidentiality of Medical Information Act');
  });
  it('shows notes and escapes text', () => {
    expect(h).toContain('Blur the card before any use');
    expect(photosPage([{ id: 'P-01', file: '', origin: 'x', alt: 'a "quoted" <alt>' }])).toContain('alt="a &quot;quoted&quot; &lt;alt&gt;"');
  });
  it('never exposes source file paths', () => {
    expect(h).not.toContain('Downloads');
    expect(h).not.toContain('originals');
  });
});
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `npx vitest run src/pages.test.ts`
Expected: FAIL — cannot resolve `./pages`.

- [ ] **Step 4: Implement** — `src/pages.ts`

```ts
import type { Photo } from './photos';

const esc = (s: string) =>
  s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

const CSS = `
  :root { --ink:#1f2a44; --muted:#4a5568; --line:#e2dccf; --bg:#fbf7ef; --card:#fff; --accent:#1f3a68; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:17px/1.6 -apple-system, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif; }
  main { max-width: 1080px; margin: 0 auto; padding: 32px 16px 64px; }
  h1 { font-size: 28px; margin: 0 0 8px; } h2 { font-size: 21px; margin: 32px 0 8px; }
  p, li { max-width: 68ch; } .muted { color: var(--muted); }
  .box { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 20px; }
  .grid { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
  .grid li { background: var(--card); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
  .grid img { display: block; width: 100%; aspect-ratio: 4/3; object-fit: cover; background: #eee; }
  .grid .cap { padding: 10px 12px; font-size: 15px; }
  .id { font-weight: 700; } .note { color: #8a2a0a; }
  .btns { display: flex; flex-wrap: wrap; gap: 12px; }
  .btn { display: inline-block; background: var(--accent); color: #fff; text-decoration: none; padding: 10px 16px; border-radius: 999px; }
  form { display: grid; gap: 12px; max-width: 360px; }
  input { font: inherit; padding: 10px 12px; border: 1px solid var(--muted); border-radius: 8px; }
  button { font: inherit; padding: 10px 16px; border: 0; border-radius: 999px; background: var(--accent); color: #fff; }
  .err { color: #8a2a0a; }
`;

const shell = (title: string, body: string) => `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>${esc(title)}</title><style>${CSS}</style></head>
<body><main>${body}</main></body></html>`;

export function loginPage(error?: string): string {
  return shell('1234 — private', `
    <h1>1234 Ortho-K Vision Care — private page</h1>
    <p class="muted">For Dr. Woo and the practice team.</p>
    <form method="post" action="/login">
      <label for="pw">Password</label>
      <input id="pw" type="password" name="password" autocomplete="current-password" autocapitalize="none" autocorrect="off" spellcheck="false" required>
      ${error ? `<p class="err" role="alert">${esc(error)}</p>` : ''}
      <button type="submit">Open</button>
    </form>`);
}

const FORMS: [string, string][] = [['en', 'English'], ['zh-hant', '繁體中文'], ['zh-hans', '简体中文']];

export function photosPage(photos: Photo[]): string {
  const cards = photos.map((p) => `
      <li>
        <img src="/img/${esc(p.id)}" alt="${esc(p.alt)}" loading="lazy">
        <div class="cap"><span class="id">${esc(p.id)}</span> · ${esc(p.origin)}${p.note ? `<br><span class="note">${esc(p.note)}</span>` : ''}</div>
      </li>`).join('');
  return shell('Patient photos — held back', `
    <h1>Patient photos we are holding back</h1>
    <p class="muted">Private page for the 1234 Ortho-K Vision Care team. Please don't share the link or password outside the practice.</p>

    <section class="box">
      <h2 style="margin-top:0">Why these photos aren't on the website</h2>
      <ul>
        <li>These photos show patients, most of them children, at the clinic. A patient's picture taken during their care counts as health information.</li>
        <li>Under HIPAA, the practice needs the patient's written authorization before using that information in marketing — the website, social media, printed materials, or testimonials.</li>
        <li>California's Confidentiality of Medical Information Act adds its own rules for that written authorization.</li>
        <li>For anyone under 18, a parent or legal guardian signs. Children can also sign to show they agree.</li>
        <li>Photo P-01 also shows a lens record card with visit dates and prescription values. That card has to be blurred before the photo is used, even with a signed release.</li>
      </ul>
      <p><strong>Once a family signs:</strong> send us the photo number(s) written on the form, and we'll add those photos to the website.</p>
    </section>

    <h2>Release form</h2>
    <p>Print the version in the family's language. Each one is the same form. Have the practice's legal or HIPAA contact review it before first use.</p>
    <p class="btns">${FORMS.map(([l, name]) => `<a class="btn" href="/release-${l}.pdf">${name} (PDF)</a>`).join('')}</p>

    <h2>The photos (${photos.length})</h2>
    <p class="muted">Write the photo number (for example P-05) on the family's form.</p>
    <ul class="grid">${cards}
    </ul>`);
}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `npx vitest run src/pages.test.ts`
Expected: PASS (8 tests).

- [ ] **Step 6: Commit**

```bash
git add src/photos.json src/photos.ts src/pages.ts src/pages.test.ts
git commit -m "Add the photo manifest, login page and photos page"
```

---

### Task 4: The Worker router

**Files:**
- Create: `src/index.ts`
- Test: `src/index.test.ts`

**Interfaces:**
- Consumes: everything produced in Tasks 1–3 (exact names above).
- Produces: `default { fetch(request: Request, env: Env): Promise<Response> }`, `interface Env { PHOTOS_BUCKET: R2Bucket; LOGIN_KV: KVNamespace; PAGE_PASSWORD: string; SESSION_KEY: string }`, `SESSION_MS = 43_200_000`.

- [ ] **Step 1: Write the failing tests** — `src/index.test.ts`

```ts
import { describe, it, expect, vi } from 'vitest';
import worker, { type Env } from './index';
import { makeKv } from './test-helpers';

function makeBucket(keys: string[]) {
  return {
    get: vi.fn(async (k: string) => (keys.includes(k) ? { body: `bytes:${k}` } : null)),
  } as unknown as R2Bucket;
}

const baseEnv = (over: Partial<Env> = {}): Env => ({
  PHOTOS_BUCKET: makeBucket(['photos/P-01.jpg', 'release-en.pdf', 'release-zh-hant.pdf', 'release-zh-hans.pdf']),
  LOGIN_KV: makeKv(),
  PAGE_PASSWORD: 'maplecloud',
  SESSION_KEY: 'k'.repeat(64),
  ...over,
});

const get = (path: string, cookie?: string) =>
  new Request(`https://w.example${path}`, { headers: cookie ? { Cookie: cookie } : {} });

const login = (password: string, ip = '1.2.3.4') =>
  new Request('https://w.example/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'CF-Connecting-IP': ip },
    body: new URLSearchParams({ password }),
  });

async function sessionCookie(env: Env): Promise<string> {
  const res = await worker.fetch(login('maplecloud'), env);
  return res.headers.get('Set-Cookie')!.split(';')[0];
}

describe('without a session', () => {
  it('GET / shows the login form only', async () => {
    const res = await worker.fetch(get('/'), baseEnv());
    const body = await res.text();
    expect(res.status).toBe(200);
    expect(body).toContain('name="password"');
    expect(body).not.toContain('/img/');
  });
  it.each(['/img/P-01', '/img/P-99', '/release-en.pdf', '/img/..%2Frelease-en.pdf', '/anything'])('%s is 401', async (p) => {
    const env = baseEnv();
    const res = await worker.fetch(get(p), env);
    expect(res.status).toBe(401);
    expect(env.PHOTOS_BUCKET.get).not.toHaveBeenCalled();
  });
  it('rejects a forged cookie', async () => {
    const res = await worker.fetch(get('/img/P-01', `session=${Date.now() + 1e9}.deadbeef`), baseEnv());
    expect(res.status).toBe(401);
  });
});

describe('login', () => {
  it('sets a 12-hour Lax cookie and redirects on the right password', async () => {
    const res = await worker.fetch(login('maplecloud'), baseEnv());
    expect(res.status).toBe(303);
    expect(res.headers.get('Location')).toBe('/');
    const c = res.headers.get('Set-Cookie')!;
    for (const part of ['HttpOnly', 'Secure', 'SameSite=Lax', 'Path=/', 'Max-Age=43200']) expect(c).toContain(part);
  });
  it('accepts the password typed as "Maple Cloud"', async () => {
    const res = await worker.fetch(login('Maple Cloud'), baseEnv());
    expect(res.status).toBe(303);
  });
  it('rejects a wrong password with 401 and no cookie', async () => {
    const res = await worker.fetch(login('maplecloudy'), baseEnv());
    expect(res.status).toBe(401);
    expect(res.headers.get('Set-Cookie')).toBeNull();
    expect(await res.text()).toContain('didn’t match');
  });
  it('returns 429 on the 11th try after 10 failures, even with the right password', async () => {
    const env = baseEnv();
    for (let i = 0; i < 10; i++) await worker.fetch(login('wrong'), env);
    const res = await worker.fetch(login('maplecloud'), env);
    expect(res.status).toBe(429);
  });
  it('GET /login shows the form instead of an error', async () => {
    const res = await worker.fetch(get('/login'), baseEnv());
    expect(res.status).toBe(200);
    expect(await res.text()).toContain('name="password"');
  });
});

describe('with a session', () => {
  it('GET / shows the photos page', async () => {
    const env = baseEnv();
    const res = await worker.fetch(get('/', await sessionCookie(env)), env);
    const body = await res.text();
    expect(body).toContain('src="/img/P-23"');
    expect(body).toContain('href="/release-zh-hans.pdf"');
  });
  it('serves a photo as JPEG', async () => {
    const env = baseEnv();
    const res = await worker.fetch(get('/img/P-01', await sessionCookie(env)), env);
    expect(res.status).toBe(200);
    expect(res.headers.get('Content-Type')).toBe('image/jpeg');
    expect(await res.text()).toBe('bytes:photos/P-01.jpg');
  });
  it('serves each release form as a PDF download', async () => {
    const env = baseEnv();
    const cookie = await sessionCookie(env);
    for (const l of ['en', 'zh-hant', 'zh-hans']) {
      const res = await worker.fetch(get(`/release-${l}.pdf`, cookie), env);
      expect(res.status).toBe(200);
      expect(res.headers.get('Content-Type')).toBe('application/pdf');
      expect(res.headers.get('Content-Disposition')).toBe(`attachment; filename="1234-photo-release-${l}.pdf"`);
    }
  });
  it('404s an unknown photo, a bad id and a traversal attempt without reading R2', async () => {
    const env = baseEnv();
    const cookie = await sessionCookie(env);
    for (const p of ['/img/P-99', '/img/P-1', '/img/..%2Frelease-en.pdf', '/release-fr.pdf']) {
      const res = await worker.fetch(get(p, cookie), env);
      expect(res.status).toBe(404);
    }
    expect(env.PHOTOS_BUCKET.get).not.toHaveBeenCalled();
  });
  it('404s a listed photo that is missing from R2', async () => {
    const env = baseEnv();
    const res = await worker.fetch(get('/img/P-02', await sessionCookie(env)), env);
    expect(res.status).toBe(404);
  });
});

describe('every response', () => {
  it.each(['/', '/img/P-01', '/nope'])('%s carries noindex and no-store', async (p) => {
    const res = await worker.fetch(get(p), baseEnv());
    expect(res.headers.get('X-Robots-Tag')).toBe('noindex, nofollow');
    expect(res.headers.get('Cache-Control')).toBe('private, no-store');
    expect(res.headers.get('Referrer-Policy')).toBe('no-referrer');
  });
});

describe('misconfiguration', () => {
  it('returns 500 and never logs in when secrets are missing', async () => {
    const env = baseEnv({ PAGE_PASSWORD: '' });
    const res = await worker.fetch(login(''), env);
    expect(res.status).toBe(500);
    expect(res.headers.get('Set-Cookie')).toBeNull();
  });
});
```

The encoded-slash path `/img/..%2Frelease-en.pdf` stays as-is in `URL.pathname` (the parser doesn't decode `%2F` or treat it as a dot segment), so it must fail the `P-\d{2}` pattern rather than reach the release-form route.

- [ ] **Step 2: Run the tests to verify they fail**

Run: `npx vitest run src/index.test.ts`
Expected: FAIL — cannot resolve `./index`.

- [ ] **Step 3: Implement** — `src/index.ts`

```ts
import { createSessionToken, verifySessionToken, readCookie, passwordMatches } from './session';
import { isLocked, recordFailure } from './ratelimit';
import { loginPage, photosPage } from './pages';
import { PHOTOS, findPhoto, photoKey, LANGS, type Lang } from './photos';

export interface Env {
  PHOTOS_BUCKET: R2Bucket;
  LOGIN_KV: KVNamespace;
  PAGE_PASSWORD: string;
  SESSION_KEY: string;
}

const COOKIE = 'session';
export const SESSION_MS = 12 * 60 * 60 * 1000;

const BASE_HEADERS: Record<string, string> = {
  'X-Robots-Tag': 'noindex, nofollow',
  'Cache-Control': 'private, no-store',
  'Referrer-Policy': 'no-referrer',
  'X-Content-Type-Options': 'nosniff',
};

function respond(body: BodyInit | null, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(body, { status, headers: { ...BASE_HEADERS, ...headers } });
}
const html = (s: string, status = 200) => respond(s, status, { 'Content-Type': 'text/html; charset=utf-8' });
const notFound = () => respond('Not found', 404);

async function fromBucket(env: Env, key: string, type: string, download?: string): Promise<Response> {
  const obj = await env.PHOTOS_BUCKET.get(key);
  if (!obj) return notFound();
  const headers: Record<string, string> = { 'Content-Type': type };
  if (download) headers['Content-Disposition'] = `attachment; filename="${download}"`;
  return respond(obj.body, 200, headers);
}

async function login(request: Request, env: Env, now: number): Promise<Response> {
  const ip = request.headers.get('CF-Connecting-IP') ?? 'unknown';
  if (await isLocked(env.LOGIN_KV, ip, now)) {
    return html(loginPage('Too many tries. Please wait 15 minutes and try again.'), 429);
  }
  const form = await request.formData().catch(() => null);
  const input = String(form?.get('password') ?? '');
  if (!(await passwordMatches(input, env.PAGE_PASSWORD))) {
    await recordFailure(env.LOGIN_KV, ip, now);
    return html(loginPage('That password didn’t match. Please try again.'), 401);
  }
  const token = await createSessionToken(env.SESSION_KEY, now, SESSION_MS);
  return respond(null, 303, {
    Location: '/',
    'Set-Cookie': `${COOKIE}=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_MS / 1000}`,
  });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (!env.PAGE_PASSWORD || !env.SESSION_KEY) return respond('Not configured', 500);
    const url = new URL(request.url);
    const now = Date.now();

    if (url.pathname === '/login' && request.method === 'POST') return login(request, env, now);

    const authed = await verifySessionToken(readCookie(request, COOKIE), env.SESSION_KEY, now);
    if (url.pathname === '/' || url.pathname === '/login') {
      if (request.method !== 'GET' && request.method !== 'HEAD') return respond('Method not allowed', 405);
      return html(authed ? photosPage(PHOTOS) : loginPage());
    }
    if (!authed) return respond('Unauthorized', 401);

    const img = url.pathname.match(/^\/img\/(P-\d{2})$/);
    if (img) {
      const photo = findPhoto(img[1]);
      return photo ? fromBucket(env, photoKey(photo.id), 'image/jpeg') : notFound();
    }
    const pdf = url.pathname.match(/^\/release-([a-z-]+)\.pdf$/);
    if (pdf && (LANGS as readonly string[]).includes(pdf[1])) {
      const lang = pdf[1] as Lang;
      return fromBucket(env, `release-${lang}.pdf`, 'application/pdf', `1234-photo-release-${lang}.pdf`);
    }
    return notFound();
  },
};
```

- [ ] **Step 4: Run all tests and the type check**

Run: `npm test && npm run typecheck`
Expected: every test file PASSES with 0 failures; `tsc` reports no errors.

- [ ] **Step 5: Commit**

```bash
git add src/index.ts src/index.test.ts
git commit -m "Route login, the photos page, photos and release forms behind the session"
```

---

### Task 5: Prepare the photos (metadata stripped, resized)

**Files:**
- Create: `scripts/prepare_photos.py`
- Output (git-ignored): `upload/photos/P-01.jpg` … `P-23.jpg`

**Interfaces:**
- Consumes: `src/photos.json` (`id`, `file`).
- Produces: 23 JPEGs named `<id>.jpg` in `upload/photos/`, for Task 7's upload.

- [ ] **Step 1: Write the script** — `scripts/prepare_photos.py`

```python
"""Re-encode every photo in src/photos.json into upload/photos/<id>.jpg.

Re-encoding with Pillow drops all metadata (GPS, dates, camera). Images are
rotated upright first, then shrunk to at most 1600 px on the long side.
Multi-picture iPhone files (MPO) are reduced to their first frame.
"""
import json
import os
import sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "upload", "photos")
MAX = 1600

def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(ROOT, "src", "photos.json"), encoding="utf-8") as f:
        photos = json.load(f)
    missing = [p["file"] for p in photos if not os.path.exists(os.path.expanduser(p["file"]))]
    if missing:
        print("Missing source files:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 1
    for p in photos:
        with Image.open(os.path.expanduser(p["file"])) as im:
            im.seek(0)
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((MAX, MAX))
            dest = os.path.join(OUT, f"{p['id']}.jpg")
            im.save(dest, "JPEG", quality=85, optimize=True)
            print(p["id"], im.size)
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run it**

Run: `npm run photos`
Expected: 23 lines `P-01 (w, h)` … `P-23 (w, h)`, exit 0.

- [ ] **Step 3: Verify no metadata survived and the count is right**

Run:
```bash
ls upload/photos/*.jpg | wc -l
exiftool -q -s -GPSPosition -DateTimeOriginal -Make -Model -Orientation upload/photos/*.jpg | grep -v '^========' | wc -l
```
Expected: `23`, then `0`.

- [ ] **Step 4: Look at P-01, P-07 and P-08** (Read the images) and confirm they are upright and match their alt text in `src/photos.json`. Fix any alt text that doesn't match.

- [ ] **Step 5: Commit** (script only — `upload/` is ignored)

```bash
git status --short upload   # expect no output
git add scripts/prepare_photos.py src/photos.json
git commit -m "Prepare patient photos without metadata for private upload"
```

---

### Task 6: Release forms (three 14 pt PDFs)

**Files:**
- Create: `form/text.json`, `form/template.html`, `scripts/build-pdfs.mjs`
- Output (git-ignored): `upload/release-en.pdf`, `upload/release-zh-hant.pdf`, `upload/release-zh-hans.pdf`

**Interfaces:**
- Produces: the three PDFs for Task 7's upload. File names must match `release-<lang>.pdf` with `<lang>` in `LANGS`.

- [ ] **Step 1: Write the text** — `form/text.json`

```json
{
  "en": {
    "lang": "en",
    "title": "Patient Photo Release and Authorization",
    "practice": "1234 Ortho-K Vision Care · 1234 S. Garfield Ave. #105, Alhambra, CA 91801 · (626) 282-5388",
    "fields": ["Patient name", "Date of birth", "Photo number(s), e.g. P-05"],
    "sections": [
      ["What this covers", "I allow 1234 Ortho-K Vision Care to use the photo(s) listed above, which show the patient at the clinic. The photos may show the patient's face. No medical record or eye prescription will be shown with them."],
      ["Where it may be used", "Tick each one you agree to:"],
      ["Why", "To show other families what a visit to the clinic looks like. This is marketing by the practice."],
      ["How long", "This permission lasts 5 years from the date it is signed, unless I cancel it sooner."],
      ["Cancelling", "I can cancel this at any time by writing to the practice at the address above. After that, the practice will stop new uses and remove the photos from its own website and social media accounts. It cannot recall printed materials already handed out, or copies other people have already made."],
      ["Your choice", "Signing is voluntary. Saying no will not affect the patient's treatment, payment, or eligibility for care."],
      ["Once it is public", "Once a photo is posted publicly, other people may copy or share it, and it may no longer be protected by privacy laws."],
      ["No payment", "No payment is given for this permission. I will receive a copy of this signed form."]
    ],
    "uses": ["Practice website (1234orthok.com)", "Social media (for example WeChat, Instagram, Facebook, Yelp)", "Printed materials (brochures, posters)", "Testimonial: the photo shown with our own words about our visit"],
    "minorTitle": "If the patient is under 18",
    "minorFields": ["Parent or legal guardian signature", "Printed name", "Relationship to patient", "Date"],
    "assentTitle": "Child's agreement (optional)",
    "assentText": "I know my photo may be shown, and that's OK with me.",
    "assentFields": ["Child's signature", "Date"],
    "adultTitle": "If the patient is 18 or older",
    "adultFields": ["Patient signature", "Date"],
    "officeTitle": "Office use",
    "officeFields": ["Received by", "Date", "Photo numbers recorded"],
    "footer": "DRAFT — have the practice's legal or HIPAA contact review this form before use."
  },
  "zh-hant": {
    "lang": "zh-Hant",
    "title": "病人照片使用授權書",
    "practice": "1234 Ortho-K Vision Care · 1234 S. Garfield Ave. #105, Alhambra, CA 91801 · (626) 282-5388",
    "fields": ["病人姓名", "出生日期", "照片編號（例如 P-05）"],
    "sections": [
      ["授權範圍", "本人同意 1234 Ortho-K Vision Care 使用上列照片。照片為病人在診所拍攝，可能顯示病人面部。照片旁不會顯示病歷或眼睛度數。"],
      ["使用範圍", "請勾選您同意的項目："],
      ["用途", "讓其他家庭了解到診所看診的情形。這屬於診所的宣傳用途。"],
      ["有效期限", "本授權自簽署日起五年內有效，除非本人提前撤銷。"],
      ["撤銷授權", "本人可隨時以書面方式寄至上述地址撤銷本授權。撤銷後，診所將停止新的使用，並從診所自己的網站及社交媒體帳號移除照片；但已派發的印刷品或他人已複製的內容無法收回。"],
      ["自願簽署", "簽署與否完全自願。不簽署不會影響病人的治療、付款或就診資格。"],
      ["公開之後", "照片公開後，他人可能複製或轉發，且可能不再受隱私法律保護。"],
      ["不涉及報酬", "本授權不涉及任何報酬。本人將獲得一份已簽署的副本。"]
    ],
    "uses": ["診所網站（1234orthok.com）", "社交媒體（例如微信、Instagram、Facebook、Yelp）", "印刷品（小冊子、海報）", "見證分享：照片配上我們對看診經驗的文字"],
    "minorTitle": "病人未滿 18 歲",
    "minorFields": ["家長或法定監護人簽名", "正楷姓名", "與病人關係", "日期"],
    "assentTitle": "孩子同意（可選）",
    "assentText": "我知道我的照片可能會被展示，我同意。",
    "assentFields": ["孩子簽名", "日期"],
    "adultTitle": "病人年滿 18 歲",
    "adultFields": ["病人簽名", "日期"],
    "officeTitle": "診所填寫",
    "officeFields": ["經手人", "日期", "已登記照片編號"],
    "footer": "草稿 — 使用前請由診所的法律或 HIPAA 負責人審閱。中文為草擬譯文，請診所核對。"
  },
  "zh-hans": {
    "lang": "zh-Hans",
    "title": "病人照片使用授权书",
    "practice": "1234 Ortho-K Vision Care · 1234 S. Garfield Ave. #105, Alhambra, CA 91801 · (626) 282-5388",
    "fields": ["病人姓名", "出生日期", "照片编号（例如 P-05）"],
    "sections": [
      ["授权范围", "本人同意 1234 Ortho-K Vision Care 使用上列照片。照片为病人在诊所拍摄，可能显示病人面部。照片旁不会显示病历或眼睛度数。"],
      ["使用范围", "请勾选您同意的项目："],
      ["用途", "让其他家庭了解到诊所看诊的情形。这属于诊所的宣传用途。"],
      ["有效期限", "本授权自签署日起五年内有效，除非本人提前撤销。"],
      ["撤销授权", "本人可随时以书面方式寄至上述地址撤销本授权。撤销后，诊所将停止新的使用，并从诊所自己的网站及社交媒体账号移除照片；但已派发的印刷品或他人已复制的内容无法收回。"],
      ["自愿签署", "签署与否完全自愿。不签署不会影响病人的治疗、付款或就诊资格。"],
      ["公开之后", "照片公开后，他人可能复制或转发，且可能不再受隐私法律保护。"],
      ["不涉及报酬", "本授权不涉及任何报酬。本人将获得一份已签署的副本。"]
    ],
    "uses": ["诊所网站（1234orthok.com）", "社交媒体（例如微信、Instagram、Facebook、Yelp）", "印刷品（小册子、海报）", "见证分享：照片配上我们对看诊经验的文字"],
    "minorTitle": "病人未满 18 岁",
    "minorFields": ["家长或法定监护人签名", "正楷姓名", "与病人关系", "日期"],
    "assentTitle": "孩子同意（可选）",
    "assentText": "我知道我的照片可能会被展示，我同意。",
    "assentFields": ["孩子签名", "日期"],
    "adultTitle": "病人年满 18 岁",
    "adultFields": ["病人签名", "日期"],
    "officeTitle": "诊所填写",
    "officeFields": ["经手人", "日期", "已登记照片编号"],
    "footer": "草稿 — 使用前请由诊所的法律或 HIPAA 负责人审阅。中文为草拟译文，请诊所核对。"
  }
}
```

- [ ] **Step 2: Write the layout** — `form/template.html` (every font size is ≥ 14pt; the build checks this)

```html
<!doctype html>
<html><head><meta charset="utf-8">
<style>
  @page { size: Letter; margin: 0.6in 0.7in 0.8in; }
  body { font-family: -apple-system, "Helvetica Neue", "PingFang TC", "PingFang SC", sans-serif; font-size: 14pt; line-height: 1.45; color: #111; }
  html[lang="zh-Hans"] body { font-family: -apple-system, "PingFang SC", sans-serif; }
  h1 { font-size: 20pt; margin: 0 0 4pt; }
  h2 { font-size: 15pt; margin: 14pt 0 4pt; }
  p { margin: 0 0 6pt; }
  .practice { font-size: 14pt; color: #333; margin-bottom: 12pt; }
  .field { display: flex; gap: 8pt; align-items: flex-end; margin: 10pt 0; }
  .field span { white-space: nowrap; }
  .field i { flex: 1; border-bottom: 1pt solid #111; height: 18pt; }
  .use { display: flex; gap: 10pt; margin: 6pt 0; }
  .use b { flex: none; width: 14pt; height: 14pt; border: 1.5pt solid #111; margin-top: 3pt; }
  .sign { break-inside: avoid; border: 1pt solid #999; padding: 8pt 12pt; margin-top: 12pt; }
  .footer { font-size: 14pt; margin-top: 16pt; border-top: 1pt solid #999; padding-top: 6pt; }
</style></head>
<body>
  <h1 id="title"></h1>
  <p class="practice" id="practice"></p>
  <div id="fields"></div>
  <div id="sections"></div>
  <div class="sign" id="minor"></div>
  <div class="sign" id="assent"></div>
  <div class="sign" id="adult"></div>
  <div class="sign" id="office"></div>
  <p class="footer" id="footer"></p>
</body></html>
```

- [ ] **Step 3: Write the build** — `scripts/build-pdfs.mjs`

```js
import { chromium } from 'playwright';
import { readFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const text = JSON.parse(readFileSync(`${root}form/text.json`, 'utf8'));
const template = readFileSync(`${root}form/template.html`, 'utf8');

// CMIA §56.11: printed authorizations must use type no smaller than 14 point.
const sizes = [...template.matchAll(/font-size:\s*([\d.]+)(pt|px)/g)].map(([, n, u]) => (u === 'px' ? Number(n) * 0.75 : Number(n)));
const small = sizes.filter((pt) => pt < 14);
if (small.length) throw new Error(`Font sizes under 14pt in form/template.html: ${small.join(', ')}`);

mkdirSync(`${root}upload`, { recursive: true });
const browser = await chromium.launch();
for (const [key, t] of Object.entries(text)) {
  const page = await browser.newPage();
  await page.setContent(template);
  await page.evaluate((t) => {
    const $ = (id) => document.getElementById(id);
    const el = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt) e.textContent = txt; return e; };
    const field = (label) => { const f = el('div', 'field'); f.append(el('span', '', label), el('i')); return f; };
    const block = (id, title, fields, lead) => { const b = $(id); b.append(el('h2', '', title)); if (lead) b.append(el('p', '', lead)); fields.forEach((f) => b.append(field(f))); };
    document.documentElement.lang = t.lang;
    $('title').textContent = t.title;
    $('practice').textContent = t.practice;
    t.fields.forEach((f) => $('fields').append(field(f)));
    t.sections.forEach(([h, p], i) => {
      $('sections').append(el('h2', '', `${i + 1}. ${h}`), el('p', '', p));
      if (i === 1) t.uses.forEach((u) => { const r = el('div', 'use'); r.append(el('b'), el('span', '', u)); $('sections').append(r); });
    });
    block('minor', t.minorTitle, t.minorFields);
    block('assent', t.assentTitle, t.assentFields, t.assentText);
    block('adult', t.adultTitle, t.adultFields);
    block('office', t.officeTitle, t.officeFields);
    $('footer').textContent = t.footer;
  }, t);
  const out = `${root}upload/release-${key}.pdf`;
  await page.pdf({ path: out, format: 'Letter', printBackground: true, displayHeaderFooter: false });
  const pages = execFileSync('pdfinfo', [out], { encoding: 'utf8' }).match(/Pages:\s+(\d+)/)[1];
  console.log(`release-${key}.pdf  ${pages} pages`);
}
await browser.close();
```

- [ ] **Step 4: Build**

Run: `npx playwright install chromium && npm run pdfs`
Expected: three lines `release-en.pdf  N pages` (N is 2–4); no "Font sizes under 14pt" error.

- [ ] **Step 5: Verify the text rendered (no missing CJK glyphs) and the draft notice is there**

Run:
```bash
pdftotext upload/release-en.pdf - | grep -c -e "Parent or legal guardian" -e "DRAFT"
pdftotext upload/release-zh-hant.pdf - | grep -c -e "家長或法定監護人" -e "草稿"
pdftotext upload/release-zh-hans.pdf - | grep -c -e "家长或法定监护人" -e "草稿"
```
Expected: `2` for each.

- [ ] **Step 6: Look at page 1 of each PDF** (`pdftocairo -png -r 50 -f 1 -l 1 upload/release-zh-hant.pdf /tmp/zh` in the session scratchpad, then Read the PNG) and check that checkboxes, signature lines and Chinese text look right.

- [ ] **Step 7: Commit** (sources only)

```bash
git add form/text.json form/template.html scripts/build-pdfs.mjs
git commit -m "Build 14pt photo-release forms in English, Traditional and Simplified Chinese"
```

---

### Task 7: Cloud setup, upload, deploy, verify

This task changes the user's Cloudflare account. Confirm with the user before Step 1.

**Files:**
- Modify: `wrangler.toml` (KV id)
- Create: `scripts/upload.sh`

**Interfaces:**
- Consumes: `upload/photos/*.jpg` (Task 5), `upload/release-*.pdf` (Task 6), the Worker (Task 4).

- [ ] **Step 1: Create the bucket and KV namespace**

```bash
npx wrangler r2 bucket create 1234-patient-photos
npx wrangler kv namespace create LOGIN_KV
```
Expected: bucket created; the KV command prints an `id`. Put that id in `wrangler.toml` in place of `REPLACED_IN_TASK_7`.

- [ ] **Step 2: Confirm the bucket has no public access**

Run: `npx wrangler r2 bucket dev-url get 1234-patient-photos`
Expected: says the r2.dev URL is disabled. If enabled, run `npx wrangler r2 bucket dev-url disable 1234-patient-photos`.

- [ ] **Step 3: Write the upload script** — `scripts/upload.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
BUCKET=1234-patient-photos
for f in upload/photos/P-*.jpg; do
  npx wrangler r2 object put "$BUCKET/photos/$(basename "$f")" --file "$f" --content-type image/jpeg --remote
done
for lang in en zh-hant zh-hans; do
  npx wrangler r2 object put "$BUCKET/release-$lang.pdf" --file "upload/release-$lang.pdf" --content-type application/pdf --remote
done
echo "Uploaded $(ls upload/photos/P-*.jpg | wc -l | tr -d ' ') photos and 3 forms."
```

Run: `npm run upload`
Expected: ends with `Uploaded 23 photos and 3 forms.`

- [ ] **Step 4: Set the secrets.** The password is the two-word one agreed with the user in chat. It must never be written into any file, including this plan; pass it through an environment variable set only in the shell that runs this step.

```bash
printf '%s' "$PAGE_PASSWORD" | npx wrangler secret put PAGE_PASSWORD
openssl rand -hex 32 | tr -d '\n' | npx wrangler secret put SESSION_KEY
```
Expected: both report success. (Wrangler may ask to create the Worker first; answer yes.)

- [ ] **Step 5: Deploy**

Run: `npm run deploy`
Expected: prints the URL `https://1234-patient-photos.<account-subdomain>.workers.dev`.

- [ ] **Step 6: Verify the live Worker** (set `U` to the printed URL)

```bash
U=https://1234-patient-photos.<subdomain>.workers.dev
curl -s -o /dev/null -w '%{http_code}\n' "$U/img/P-01"            # 401
curl -s -o /dev/null -w '%{http_code}\n' "$U/release-en.pdf"      # 401
curl -sI "$U/" | grep -i -e x-robots-tag -e cache-control           # noindex, no-store
curl -s -o /dev/null -w '%{http_code}\n' -d password=wrong "$U/login"   # 401
J=$(mktemp); curl -s -c "$J" -o /dev/null -w '%{http_code}\n' --data-urlencode "password=$PAGE_PASSWORD" "$U/login"   # 303
curl -s -b "$J" -o /dev/null -w '%{http_code} %{content_type}\n' "$U/img/P-01"      # 200 image/jpeg
curl -s -b "$J" -o /dev/null -w '%{http_code} %{content_type}\n' "$U/release-zh-hant.pdf"  # 200 application/pdf
rm "$J"
```
Expected: the codes in the comments.

- [ ] **Step 7: Check the page in a real browser** — open `$U` in a private window: login form → password → page with the explanation, three form buttons, 23 photos all loading. Screenshot it at 390 px and 1280 px wide.

- [ ] **Step 8: Commit**

```bash
git add wrangler.toml scripts/upload.sh
git commit -m "Deploy the patient-photos Worker with a private R2 bucket"
```

---

### Task 8: Private GitHub repo

Creating a repo on the user's GitHub account is outward-facing. Ask the user before Step 1; if they prefer local-only, skip this task.

- [ ] **Step 1: Confirm nothing sensitive is tracked**

Run: `git ls-files | grep -E '\.(jpe?g|png|pdf|heic)$|^upload/|\.dev\.vars' ; echo "exit=$?"`
Expected: no file names, `exit=1`.

- [ ] **Step 2: Create the private repo and push**

```bash
gh repo create thirstypig/1234-patient-photos --private --source . --push
gh repo view thirstypig/1234-patient-photos --json visibility -q .visibility
```
Expected: `PRIVATE`.

---

### Task 9: Hand-off note in the public repo

**Files:**
- Modify: `~/Projects/1234/docs/copy-review.md` (item P-2)

- [ ] **Step 1: Point P-2 at the private page** — replace P-2's last sentence ("Patient photos would be hosted outside the public code repository.") with:

```
The photos, the reason they're held back, and the release form (English, 繁體, 简体) are on the private patient-photos page; ask Jimmy for the link and password.
```

- [ ] **Step 2: Confirm the password and the account's Worker URL are not in the public repo**

Run (same shell as Task 7, so `$PAGE_PASSWORD` and `$U` are set): `cd ~/Projects/1234 && git grep -n -i -F -e "$PAGE_PASSWORD" -e "$U"; echo "exit=$?"`
Expected: no matches, `exit=1`.

- [ ] **Step 3: Commit**

```bash
git add docs/copy-review.md
git commit -m "Point the photo-release item at the private patient-photos page"
```
