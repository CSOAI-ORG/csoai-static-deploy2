// Cloudflare Pages Function — EAT cycle tick
// POST /api/eat-tick with { task: 'verify|status' }
// GET  /api/eat-tick lists available tasks

let OOWM_SEED = [];  // hydrated from EAT_OWEM KV in onRequest (issue #8: the 14MB literal exceeded the 3MiB worker cap; seed = 75,087 entries at KV key 'owem_seed')

const TASKS = {
  // v8: OOWM neutral scoring parity with Python oowm/eat_oowm.py
  // Receipt shape mirrors the Python eat_score() (score / aligned_source / topic).
  oowm_score: async (env, body) => {
    const topic = (body.topic || '').toString().trim();
    if (!topic) return { error: 'topic required', receipt_kind: 'living-substrate-scoring' };
    // Small built-in OOWM seed (subset of v7 60-doc MMR seed) — topic ~ doc via token overlap
    // SEED hoisted to module scope as OOWM_SEED
    const toks = topic.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
    // Score against full doc text (60-doc seed: { s, d, t })
    let best = null, bestScore = 0;
    for (const doc of OOWM_SEED) {
      const textToks = (doc.t || '').toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
      const overlap = toks.filter(x => textToks.includes(x)).length;
      if (overlap > bestScore) { bestScore = overlap; best = doc; }
    }
    return {
      receipt_kind: 'living-substrate-scoring',
      version: '7.0',
      topic,
      score: best ? Number((bestScore / Math.max(toks.length, 1)).toFixed(4)) : 0,
      aligned_source: best ? best.s : null,
      aligned_doc: best ? { text: best.t, domain: best.d } : null,
      sigil: 'ed25519+ml_dsa_65',
    };
  },
  // v11: top-N-by-topic — return the N highest-overlap docs for a topic (for globe viz)
  oowm_topn: async (env, body) => {
    const topic = (body.topic || '').toString().trim();
    const topn = Math.min(parseInt(body.top_n || '5', 10) || 5, OOWM_SEED.length);
    if (!topic) return { error: 'topic required', receipt_kind: 'living-substrate-topn' };
    const toks = topic.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
    const scored = OOWM_SEED.map((doc) => {
      const textToks = (doc.t || '').toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
      const overlap = toks.filter(x => textToks.includes(x)).length;
      return { source: doc.s, domain: doc.d, text: doc.t,
               score: Number((overlap / Math.max(toks.length, 1)).toFixed(4)) };
    }).filter(d => d.score > 0).sort((a, b) => b.score - a.score).slice(0, topn);
    return { receipt_kind: 'living-substrate-topn', version: '11.0', topic,
             count: scored.length, results: scored, sigil: 'ed25519+ml_dsa_65' };
  },
  verify: async (env) => {
    // Hit /api/daily-golden on the same deployment
    const baseUrl = env?.SITE_URL || 'https://csoai-neutral.pages.dev';
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
    const baseUrl = env?.SITE_URL || 'https://csoai-neutral.pages.dev';
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

  // issue #8: seed hydrated from KV (was 14MB inlined literal)
  OOWM_SEED = (await env.EAT_OWEM.get('owem_seed', 'json')) || [];
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
    result = await fn(env, body);
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
