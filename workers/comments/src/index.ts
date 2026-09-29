import { handleBooking } from './booking';

export interface Env {
  COMMENTS_KV: KVNamespace;
  ALLOWED_ORIGIN: string;
}

interface Comment {
  text: string;
  createdAt: string;
  xPercent?: number;
  yPercent?: number;
}

// Comment keys are `<concept folder>:<page>`; concept folders start with A–E. Anything else
// (e.g. the booking and rate-limit keys, which share this KV namespace) is off-limits here.
const CONCEPT = /^[A-E][^:/]*$/;

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
      const body = await request.json<{
        concept?: string;
        page?: string;
        text?: string;
        xPercent?: number;
        yPercent?: number;
      }>();
      const concept = body.concept?.trim();
      const page = body.page?.trim();
      const text = body.text?.trim();

      if (!concept || !page || !text || !CONCEPT.test(concept)) {
        return new Response(JSON.stringify({ error: 'concept, page, and text are required' }), {
          status: 400,
          headers: { ...headers, 'Content-Type': 'application/json' },
        });
      }

      const key = `${concept}:${page}`;
      const existingRaw = await env.COMMENTS_KV.get(key);
      const existing: Comment[] = existingRaw ? JSON.parse(existingRaw) : [];
      const comment: Comment = { text, createdAt: new Date().toISOString() };
      if (typeof body.xPercent === 'number' && typeof body.yPercent === 'number') {
        comment.xPercent = body.xPercent;
        comment.yPercent = body.yPercent;
      }
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
      if (!concept || !page || !CONCEPT.test(concept)) {
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

    if (request.method === 'POST' && url.pathname === '/booking') {
      return handleBooking(request, env, headers);
    }

    return new Response('Not found', { status: 404, headers });
  },
};
