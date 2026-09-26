import type { Env } from './index';

const TTL_30D = 60 * 60 * 24 * 30;
const LOCATIONS = ['alhambra', 'walnut'];
const MAX_PER_HOUR = 5;

// Only these four fields are ever stored — no free-text health details.
export async function handleBooking(request: Request, env: Env, headers: Record<string, string>): Promise<Response> {
  const json = (status: number, body: unknown) =>
    new Response(JSON.stringify(body), { status, headers: { ...headers, 'Content-Type': 'application/json' } });

  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const rlKey = `rl:${ip}`;
  const count = Number((await env.COMMENTS_KV.get(rlKey)) || 0);
  if (count >= MAX_PER_HOUR) return json(429, { error: 'Too many requests. Please call the office.' });

  let body: Record<string, unknown>;
  try {
    body = await request.json();
  } catch {
    return json(400, { error: 'Invalid JSON', fields: [] });
  }
  if (typeof body.website === 'string' && body.website.trim() !== '') return json(201, { ok: true });

  const parentName = String(body.parentName ?? '').trim();
  const phone = String(body.phone ?? '').trim();
  const location = String(body.location ?? '').trim();
  const preferredTime = String(body.preferredTime ?? '').trim();
  const fields: string[] = [];
  if (parentName.length < 1 || parentName.length > 100) fields.push('parentName');
  const digits = phone.replace(/\D/g, '');
  if (digits.length < 10 || digits.length > 15) fields.push('phone');
  if (!LOCATIONS.includes(location)) fields.push('location');
  if (preferredTime.length > 100) fields.push('preferredTime');
  if (fields.length) return json(400, { error: 'Please check the highlighted fields.', fields });

  const createdAt = new Date().toISOString();
  await env.COMMENTS_KV.put(
    `booking:${createdAt}:${crypto.randomUUID()}`,
    JSON.stringify({ parentName, phone, location, preferredTime, createdAt }),
    { expirationTtl: TTL_30D },
  );
  await env.COMMENTS_KV.put(rlKey, String(count + 1), { expirationTtl: 3600 });
  return json(201, { ok: true });
}
