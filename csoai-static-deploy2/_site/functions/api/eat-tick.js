// Cloudflare Pages Function — EAT cycle tick
// POST /api/eat-tick with { task: 'verify|status' }
// GET  /api/eat-tick lists available tasks

const TASKS = {
  verify: async (env) => {
    // Hit /api/daily-golden on the same deployment
    const baseUrl = env?.SITE_URL || 'https://csoai-sovereign.pages.dev';
    try {
      const r = await fetch(`${baseUrl}/api/daily-golden`, { signal: AbortSignal.timeout(15000) });
      const j = await r.json();
      return {
        task: 'verify',
        started_at: new Date().toISOString(),
        golden: j.pass + '/' + (j.pass + j.fail) + ' ok',
        pass: j.pass,
        fail: j.fail,
        total_ms: j.total_ms,
      };
    } catch (e) {
      return { task: 'verify', started_at: new Date().toISOString(), error: e.message };
    }
  },
  status: async (env) => {
    const baseUrl = env?.SITE_URL || 'https://csoai-sovereign.pages.dev';
    try {
      const r = await fetch(`${baseUrl}/api/eat-status`, { signal: AbortSignal.timeout(10000) });
      return await r.json();
    } catch (e) {
      return { task: 'status', started_at: new Date().toISOString(), error: e.message };
    }
  },
};

export async function onRequest(context) {
  const { request, env } = context;
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Send-Key',
    'Content-Type': 'application/json',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers });
  }

  // Auth check
  const provided = (request.headers.get('x-send-key') || '').trim();
  const expected = env?.SEND_KEY || env?.SIGNUP_WEBHOOK_SECRET || '';
  if (expected && provided !== expected) {
    return new Response(JSON.stringify({ error: 'Invalid X-Send-Key' }), { status: 401, headers });
  }

  if (request.method === 'GET') {
    return new Response(
      JSON.stringify({
        ok: true,
        available_tasks: Object.keys(TASKS),
        usage: 'POST /api/eat-tick with body { task: "verify" } or X-Send-Key header for auth',
      }),
      { status: 200, headers },
    );
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers });
  }

  let body = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const taskName = (body.task || 'verify').toString();
  const fn = TASKS[taskName];
  if (!fn) {
    return new Response(
      JSON.stringify({ error: 'unknown task', available: Object.keys(TASKS) }),
      { status: 400, headers },
    );
  }

  const t0 = Date.now();
  let result;
  try {
    result = await fn(env);
  } catch (e) {
    result = { error: e.message };
  }
  const ms = Date.now() - t0;

  // Build tick record with hash
  const tick_record = {
    tick_id: 'eat_' + crypto.randomUUID().replace(/-/g, '').slice(0, 16),
    task: taskName,
    started_at: new Date(t0).toISOString(),
    elapsed_ms: ms,
    result,
  };

  // Hash the record
  const encoder = new TextEncoder();
  const hashBuffer = await crypto.subtle.digest('SHA-512', encoder.encode(JSON.stringify(tick_record)));
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  tick_record.sigil_chain_hash = hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');

  return new Response(JSON.stringify({ ok: true, tick: tick_record }), { status: 200, headers });
}
