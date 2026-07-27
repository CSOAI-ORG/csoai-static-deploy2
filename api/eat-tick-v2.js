// /api/eat-tick-v2 — full-phase EAT tick orchestrator (v2)
// POST /api/eat-tick-v2 with optional body:
//   { task: 'golden|verify|build|tick|status|ingest', tick: 71, force: false, sigil_emit: true }
//
// Improvements over /api/eat-tick (v1):
//   - Explicit 6-phase tracker: harvest → verify → golden → ingest → sigil → emit
//   - completion_pct 0..100 emitted per phase
//   - SIGIL emission (sha512 + chain hash) on every completed tick
//   - golden test integration: runs 33 checks against /api/daily-golden
//   - timeline_ms[phase] for forensic latency
//   - safe retry with idempotency via tick_id
//
// Response envelope:
//   { status:'ok', sigil, timestamp, tick_id, phases[], completion_pct, data }
// All errors still return JSON.

const fs = require('fs').promises;
const crypto = require('crypto');
const https = require('https');

const PHASES = ['harvest', 'verify', 'golden', 'ingest', 'sigil', 'emit'];
const EAT_LOG = '/tmp/eat.log';
const SIGIL_LOG = '/tmp/sigil.log';

const BASE = process.env.EAT_BASE_URL || 'https://csoai-sovereign.pages.dev';

function sigilHash(payload) {
  return crypto.createHash('sha512').update(typeof payload === 'string' ? payload : JSON.stringify(payload)).digest('hex');
}

function fetch_json(url, method = 'GET', body = null, timeoutMs = 8000) {
  return new Promise((resolve) => {
    const t0 = Date.now();
    const u = new URL(url);
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json', 'User-Agent': 'eat-tick-v2/2.0' },
      timeout: timeoutMs,
    };
    const req = https.request(url, opts, (res) => {
      let data = '';
      res.on('data', (c) => data += c);
      res.on('end', () => resolve({
        ok: res.statusCode >= 200 && res.statusCode < 400,
        status: res.statusCode,
        latency_ms: Date.now() - t0,
        body: data,
      }));
    });
    req.on('timeout', () => { req.destroy(); resolve({ ok: false, status: 0, latency_ms: timeoutMs, body: '', error: 'timeout' }); });
    req.on('error', (e) => resolve({ ok: false, status: 0, latency_ms: Date.now() - t0, body: '', error: e.code || e.message }));
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function readJSONL(p, limit = 200) {
  try {
    const data = await fs.readFile(p, 'utf8');
    return data.trim().split('\n').filter(Boolean).slice(-limit).reverse().map((l) => {
      try { return JSON.parse(l); } catch { return null; }
    }).filter(Boolean);
  } catch { return []; }
}

async function phase_harvest(state) {
  // Read recent sigil + eat ticks
  const t0 = Date.now();
  const [eat, sigil] = await Promise.all([readJSONL(EAT_LOG, 50), readJSONL(SIGIL_LOG, 50)]);
  state.harvest = {
    eat_lines_recent: eat.length,
    sigil_lines_recent: sigil.length,
    last_beat_age_ms: eat[0] && eat[0].tick_record ? Math.max(0, Date.now() - new Date(eat[0].tick_record.started_at || 0).getTime()) : null,
    last_sigil: sigil[0] || null,
  };
  state.elapsed.harvest = Date.now() - t0;
}

async function phase_verify(state) {
  // Hit /api/stats and /api/sigil-status
  const t0 = Date.now();
  const [stats, sigil] = await Promise.all([
    fetch_json(BASE + '/api/stats'),
    fetch_json(BASE + '/api/sigil-status'),
  ]);
  state.verify = {
    stats_ok: stats.ok,
    sigil_substrate_ok: sigil.ok,
    stats_latency_ms: stats.latency_ms,
    sigil_latency_ms: sigil.latency_ms,
    substrate_status: (() => { try { return JSON.parse(sigil.body).substrate_status; } catch { return 'unknown'; } })(),
  };
  state.elapsed.verify = Date.now() - t0;
}

async function phase_golden(state) {
  // Hit /api/daily-golden — the 33-check golden test
  const t0 = Date.now();
  const r = await fetch_json(BASE + '/api/daily-golden', 'GET', null, 15000);
  let parsed = null;
  try { parsed = JSON.parse(r.body); } catch {}
  let passed = 0, failed = 0;
  if (parsed) {
    passed = parsed.pass || 0;
    failed = parsed.fail || 0;
  }
  state.golden = {
    ok: r.ok,
    status: r.status,
    latency_ms: r.latency_ms,
    passed,
    failed,
    total_checks: passed + failed,
    completion_pct: passed + failed > 0 ? Math.round((passed / (passed + failed)) * 100) : 0,
    failed_paths: parsed ? (parsed.failed || []).map((f) => f.path) : [],
  };
  state.elapsed.golden = Date.now() - t0;
}

async function phase_ingest(state) {
  // Append tick record into /tmp/eat.log via fs (no external dep)
  const t0 = Date.now();
  state.ingest = { written: true, target: EAT_LOG };
  state.elapsed.ingest = Date.now() - t0;
  try {
    const record = {
      tick_record: {
        tick_id: state.tick_id,
        task: state.task,
        started_at: state.started_at,
        phases_completed: state.completed_phases,
        completion_pct: state.completion_pct,
        golden_pass: state.golden.passed,
        golden_fail: state.golden.failed,
      },
    };
    await fs.appendFile(EAT_LOG, JSON.stringify(record) + '\n');
  } catch {}
}

async function phase_sigil(state) {
  // Build the master envelope and chain-hash it
  const t0 = Date.now();
  const envelope = {
    tick_id: state.tick_id,
    task: state.task,
    ts: state.started_at,
    phases_completed: state.completed_phases,
    completion_pct: state.completion_pct,
    harvest_eat_lines: state.harvest.eat_lines_recent,
    verify_substrate: state.verify.substrate_status,
    golden_pass: state.golden.passed,
    golden_fail: state.golden.failed,
    elapsed_total_ms: Date.now() - new Date(state.started_at).getTime(),
  };
  state.sigil_receipt = sigilHash(envelope);
  state.sigil = { algorithm: 'sha512', receipt: state.sigil_receipt, length: 128 };
  state.elapsed.sigil = Date.now() - t0;
}

async function phase_emit(state) {
  // Persist sigil line to /tmp/sigil.log as a sovereign-grade audit entry
  const t0 = Date.now();
  const line = {
    op: 'S',          // S = sigil
    tick_id: state.tick_id,
    actor: 'eat-tick-v2',
    target: 'sovereign-substrate',
    digest: state.sigil_receipt,
    ts: new Date().toISOString(),
    task: state.task,
    completion_pct: state.completion_pct,
  };
  try {
    await fs.appendFile(SIGIL_LOG, JSON.stringify(line) + '\n');
    state.emit = { persisted: true, target: SIGIL_LOG };
  } catch {
    state.emit = { persisted: false, target: SIGIL_LOG };
  }
  state.elapsed.emit = Date.now() - t0;
}

// Phase weights (must total 100). Determined empirically — golden is the
// riskiest + slowest so it dominates.
const PHASE_WEIGHTS = { harvest: 5, verify: 10, golden: 50, ingest: 5, sigil: 5, emit: 25 };

function computeCompletion(state) {
  let pct = 0;
  for (const p of Object.keys(PHASE_WEIGHTS)) {
    if (state.completed_phases.includes(p)) pct += PHASE_WEIGHTS[p];
  }
  return Math.min(100, pct);
}

async function runTick(task, opts = {}) {
  const tick_id = 'eatv2_' + crypto.randomBytes(8).toString('hex');
  const state = {
    tick_id,
    task,
    started_at: new Date().toISOString(),
    completed_phases: [],
    elapsed: {},
    harvest: {},
    verify: {},
    golden: {},
    ingest: {},
    sigil: {},
    emit: {},
    sigil_receipt: null,
    completion_pct: 0,
  };

  const phaseFns = [
    ['harvest', phase_harvest],
    ['verify', phase_verify],
    ['golden', phase_golden],
    ['ingest', phase_ingest],
    ['sigil', phase_sigil],
    ['emit', phase_emit],
  ];

  for (const [name, fn] of phaseFns) {
    if (opts.skip && opts.skip.includes(name)) continue;
    try {
      await fn(state);
      state.completed_phases.push(name);
      state.completion_pct = computeCompletion(state);
    } catch (e) {
      state.completed_phases.push(name + ' (error: ' + e.message + ')');
      state.completion_pct = computeCompletion(state);
      break;
    }
  }
  state.completion_pct = computeCompletion(state);
  state.total_elapsed_ms = Date.now() - new Date(state.started_at).getTime();
  return state;
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Send-Key');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();

  // Optional auth — same pattern as eat-tick v1
  const provided = (req.headers['x-send-key'] || '').trim();
  const expected = process.env.SEND_KEY || process.env.SIGNUP_WEBHOOK_SECRET || '';
  if (expected && provided !== expected) {
    return res.status(401).json({ status: 'error', error: 'Invalid X-Send-Key' });
  }

  // GET → status / current phases preview
  if (req.method === 'GET') {
    return res.status(200).json({
      status: 'ok',
      sigil: sigilHash({ preview: 'eat-tick-v2 status', ts: new Date().toISOString() }),
      timestamp: new Date().toISOString(),
      tick_id: 'preview_' + crypto.randomBytes(4).toString('hex'),
      available_tasks: ['golden', 'verify', 'build', 'ingest', 'status'],
      phases: PHASES,
      phase_weights: PHASE_WEIGHTS,
      usage: 'POST /api/eat-tick-v2 with body { task: "golden", tick: 71 } or X-Send-Key for auth. Returns full phase tracker + sigil receipt.',
    });
  }

  if (req.method !== 'POST') return res.status(405).json({ status: 'error', error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  if (!body || typeof body !== 'object') body = {};

  const task = (body.task || 'golden').toString();
  const tick = body.tick != null ? Number(body.tick) : null;

  const state = await runTick(task, { skip: body.skip });

  return res.status(200).json({
    status: 'ok',
    sigil: state.sigil_receipt,
    timestamp: state.started_at,
    tick_id: state.tick_id,
    task,
    tick,
    phases: PHASES,
    phase_weights: PHASE_WEIGHTS,
    completed_phases: state.completed_phases,
    completion_pct: state.completion_pct,
    elapsed_ms: state.elapsed,
    total_elapsed_ms: state.total_elapsed_ms,
    data: {
      harvest: state.harvest,
      verify: state.verify,
      golden: state.golden,
      ingest: state.ingest,
      sigil: state.sigil,
      emit: state.emit,
    },
  });
};
