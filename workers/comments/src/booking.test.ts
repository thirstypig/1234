import { describe, it, expect, vi } from 'vitest';
import worker from './index';

function kv(initial: Record<string, string> = {}) {
  const store: Record<string, string> = { ...initial };
  return {
    store,
    get: vi.fn(async (k: string) => store[k] ?? null),
    put: vi.fn(async (k: string, v: string) => { store[k] = v; }),
  } as any;
}
const env = (k: any) => ({ COMMENTS_KV: k, ALLOWED_ORIGIN: 'https://1234.pasadenaworks.com' });
const post = (body: unknown, ip = '1.1.1.1') =>
  new Request('https://w/booking', {
    method: 'POST',
    body: JSON.stringify(body),
    headers: { 'CF-Connecting-IP': ip, 'Content-Type': 'application/json' },
  });
const good = { parentName: 'Ann Lee', phone: '(626) 555-0100', location: 'alhambra', preferredTime: 'Tue afternoon', website: '' };

describe('POST /booking', () => {
  it('stores a valid request with a 30-day TTL', async () => {
    const k = kv();
    const res = await worker.fetch(post(good), env(k));
    expect(res.status).toBe(201);
    const call = k.put.mock.calls.find((c: any[]) => c[0].startsWith('booking:'));
    expect(call).toBeTruthy();
    expect(call[2]).toEqual({ expirationTtl: 60 * 60 * 24 * 30 });
  });

  it('rejects bad fields and names them', async () => {
    const res = await worker.fetch(post({ ...good, phone: '12', location: 'pasadena', parentName: '' }), env(kv()));
    expect(res.status).toBe(400);
    expect(((await res.json()) as any).fields.sort()).toEqual(['location', 'parentName', 'phone']);
  });

  it('silently accepts but does not store honeypot submissions', async () => {
    const k = kv();
    const res = await worker.fetch(post({ ...good, website: 'spam.com' }), env(k));
    expect(res.status).toBe(201);
    expect(k.put.mock.calls.some((c: any[]) => c[0].startsWith('booking:'))).toBe(false);
  });

  it('rate limits after 5 per hour per IP', async () => {
    const res = await worker.fetch(post(good, '9.9.9.9'), env(kv({ 'rl:9.9.9.9': '5' })));
    expect(res.status).toBe(429);
  });

  it('ignores unknown fields such as free-text notes', async () => {
    const k = kv();
    await worker.fetch(post({ ...good, notes: 'my child has keratoconus' }), env(k));
    const stored = Object.entries(k.store).find(([key]) => key.startsWith('booking:'))![1] as string;
    expect(stored).not.toContain('keratoconus');
  });

  it('rejects malformed JSON with 400', async () => {
    const req = new Request('https://w/booking', { method: 'POST', body: '{nope' });
    expect((await worker.fetch(req, env(kv()))).status).toBe(400);
  });
});
