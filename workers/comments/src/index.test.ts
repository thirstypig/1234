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
