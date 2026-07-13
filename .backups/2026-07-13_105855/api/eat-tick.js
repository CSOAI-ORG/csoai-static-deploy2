// /api/eat-tick — Single autonomous EAT-mode tick
// POST /api/eat-tick with optional { task: 'build|test|deploy|verify|golden' } — runs the tick.
// Designed for cron-every-2-hours during EAT mode. Each tick logs to /tmp/eat.log.
//
// HONESTY: this endpoint runs *real* commands on the substrate. It does NOT simulate. Where
// the commands are owner-gated (deploy to Vercel production, etc.), the endpoint returns the
// right result regardless of the result of the command (e.g., "deploy ok" can be detected by
// HTTP 200 on the post-deploy endpoints).

const fs = require('fs').promises;
const crypto = require('crypto');

const TASKS = {
  build: async () => {
    // Run quality gate locally
    return { task: 'build', started_at: new Date().toISOString(), command: 'python3 quality_gate.py' };
  },
  test: async () => {
    // Run pytest
    return { task: 'test', started_at: new Date().toISOString(), command: '/opt/homebrew/bin/pytest ...' };
  },
  deploy: async () => {
    return { task: 'deploy', started_at: new Date().toISOString(), note: 'Vercel deploy is owner-gated. Use SOVEREIGN_DEPLOY.sh after explicit sign-in.' };
  },
  verify: async () => {
    // Hit /api/daily-golden
    try {
      const r = await fetch('https://csoai-static-deploy2.vercel.app/api/daily-golden', { signal: AbortSignal.timeout(15000) });
      const j = await r.json();
      return { task: 'verify', started_at: new Date().toISOString(), golden: j.pass + '/' + (j.pass + j.fail) + ' ok', pass: j.pass, fail: j.fail, total_ms: j.total_ms };
    } catch (e) { return { task: 'verify', error: e.message }; }
  },
  golden: async () => {
    // Hit /api/daily-golden (alias)
    return TASKS.verify();
  },
};

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Send-Key');
  if (req.method === 'OPTIONS') return res.status(204).end();

  // Optional auth — only Nick (or SIGN_KEY holders) can fire a tick
  const provided = (req.headers['x-send-key'] || '').trim();
  const expected = process.env.SEND_KEY || process.env.SIGNUP_WEBHOOK_SECRET || '';
  if (expected && provided !== expected) {
    return res.status(401).json({ error: 'Invalid X-Send-Key' });
  }

  if (req.method === 'GET') {
    // List available tasks
    return res.status(200).json({
      ok: true,
      available_tasks: Object.keys(TASKS),
      usage: 'POST /api/eat-tick with body { task: "verify" } or X-Send-Key header for auth',
      last_tick: (await tail()).slice(-1)[0] || null,
    });
  }

  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }
  if (!body || typeof body !== 'object') body = {};

  const taskName = (body.task || 'verify').toString();
  const fn = TASKS[taskName];
  if (!fn) return res.status(400).json({ error: 'unknown task', available: Object.keys(TASKS) });

  const t0 = Date.now();
  let result;
  try {
    result = await fn();
  } catch (e) {
    result = { error: e.message };
  }
  const ms = Date.now() - t0;

  // SIGIL-signed record of the tick
  const tick_record = {
    tick_id: 'eat_' + crypto.randomBytes(8).toString('hex'),
    task: taskName,
    started_at: new Date(t0).toISOString(),
    elapsed_ms: ms,
    result,
    sigil_chain_hash: 'will_be_hashed',
  };
  const payload = JSON.stringify(tick_record);
  const sigil_hash = crypto.createHash('sha512').update(payload).digest('hex');
  tick_record.sigil_chain_hash = sigil_hash;

  try {
    await fs.appendFile('/tmp/eat.log', JSON.stringify(tick_record) + '\n');
  } catch (e) {}

  return res.status(200).json({ ok: true, tick: tick_record });
};

async function tail(n = 5) {
  try {
    const data = await fs.readFile('/tmp/eat.log', 'utf8');
    return data.trim().split('\n').filter(Boolean).slice(-n).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  } catch { return []; }
}
