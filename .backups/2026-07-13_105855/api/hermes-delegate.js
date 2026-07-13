// Vercel serverless — Hermes agentic layer DELEGATE endpoint
// POST /api/hermes-delegate
//
// Body: { task: string, capability_required: string|string[],
//         lane_preference?: 'jeeves-strategic' | 'claude-code-builder' |
//                          'kimi-k25-frontend' | 'soxoj-m4-builder' }
//
// Returns: { status, delegated_to, task_id, eta_seconds,
//            capability_match, sigil, timestamp }
//
// HONESTY:
//  - This endpoint performs SIMULATED delegation. From a Vercel
//    serverless function we cannot reach the sovereign substrate VM
//    directly (cross-VPC blocked), so we simulate the dispatch:
//      1. Capability matching: score each of the 4 lanes against the
//         requested capability and pick the highest match (or the
//         explicitly-preferred lane if requested and capable).
//      2. task_id is a UUID-like hash of (task + lane + timestamp).
//      3. eta_seconds is derived from a per-lane base latency profile
//         (declared in code) — not fabricated measurements.
//  - Each delegation is appended to /tmp/hermes-delegations.jsonl so
//    downstream consumers (BFT council, audit trail) can replay.
//  - The response is HMAC-SHA256 sigiled over the canonical envelope.

const crypto = require('crypto');
const fs = require('fs');
const fsp = fs.promises;

const HMAC_SECRET = process.env.HERMES_HMAC_SECRET
  || 'csoai-hermes-delegate-default-2026-sovereign-hmac';

const DELEGATION_LOG = '/tmp/hermes-delegations.jsonl';

// Per-lane base ETA profile (seconds). These are the declared
// dispatch latencies for each lane type — strategic reasoning is
// slower than a typed build, etc.
const LANE_PROFILE = {
  'jeeves-strategic':       { base_eta: 4.2, priority: 1 },
  'claude-code-builder':    { base_eta: 6.8, priority: 2 },
  'kimi-k25-frontend':      { base_eta: 5.5, priority: 3 },
  'soxoj-m4-builder':       { base_eta: 7.4, priority: 4 },
};

// Lane capability registry — same as hermes-lanes.js. Keep these
// in sync; the delegated_to + capability_match depends on this.
const LANE_CAPABILITIES = {
  'jeeves-strategic': [
    'bft_council_fire', 'sov3_delegate', 'multi_agent_orchestrate',
    'strategic_synthesis', 'sigil_emit', 'eat_tick', 'morning_rundown',
    'tick_state_owner', 'sigil_chain', 'audit_trail', 'governance',
    'bft_vote', 'routing_decision',
  ],
  'claude-code-builder': [
    'typescript_build', 'react_frontend', 'python_service', 'git_commit',
    'test_run', 'spike_validate', 'code_review', 'debug_inspect',
    'node_server', 'cli_tool', 'refactor', 'typescript', 'javascript',
    'python', 'code', 'build', 'debug',
  ],
  'kimi-k25-frontend': [
    'nextjs_build', 'ui_to_code', 'tailwind_design', 'figma_screenshot_parse',
    'shadcn_components', 'responsive_layout', 'animation_motion',
    'k25_analyze_image', 'react', 'nextjs', 'frontend', 'css', 'tailwind',
    'design', 'ui', 'ux', 'vision',
  ],
  'soxoj-m4-builder': [
    'metal_accelerate', 'coreml_inference', 'swift_native', 'rust_module',
    'apple_silicon_optimize', 'quantization_gguf', 'bench_harness',
    'profile_capture', 'swift', 'rust', 'metal', 'coreml', 'quantization',
    'apple_silicon', 'm4', 'native', 'gpu',
  ],
};

function hmacSigil(payloadObj) {
  const canonical = JSON.stringify(payloadObj, Object.keys(payloadObj).sort());
  return crypto.createHmac('sha256', HMAC_SECRET).update(canonical).digest('hex');
}

function scoreLane(laneId, capability) {
  const caps = LANE_CAPABILITIES[laneId] || [];
  const required = Array.isArray(capability) ? capability : [capability];
  const lowerCaps = caps.map((c) => c.toLowerCase());
  const matches = required.filter((r) => {
    const lr = String(r).toLowerCase();
    if (lowerCaps.includes(lr)) return true;
    // Token overlap fallback: any token in the requested cap also appears in any lane cap
    const tokens = lr.split(/[^a-z0-9]+/).filter(Boolean);
    return tokens.some((tok) =>
      lowerCaps.some((lc) => lc.includes(tok) || tok.includes(lc.split('_')[0]))
    );
  });
  return {
    matched: matches.length,
    requested: required.length,
    score: Number((matches.length / Math.max(required.length, 1)).toFixed(4)),
    matched_capabilities: matches,
  };
}

function pickLane(capability, preference) {
  // If preference is supplied AND it has any capability match, honor it.
  if (preference && LANE_CAPABILITIES[preference]) {
    const prefScore = scoreLane(preference, capability);
    if (prefScore.matched > 0) {
      return { lane: preference, score: prefScore.score, reason: 'lane_preference_honored' };
    }
  }
  // Otherwise score every lane, pick highest
  let best = null;
  for (const laneId of Object.keys(LANE_CAPABILITIES)) {
    const s = scoreLane(laneId, capability);
    if (!best || s.score > best.score || (s.score === best.score && s.matched > best.matched)) {
      best = { lane: laneId, score: s.score, matched: s.matched, reason: 'capability_match' };
    }
  }
  return best;
}

function generateTaskId(task, lane, ts) {
  const h = crypto.createHash('sha256');
  h.update(String(task || ''));
  h.update('|');
  h.update(String(lane || ''));
  h.update('|');
  h.update(String(ts || ''));
  return 'task-' + h.digest('hex').slice(0, 16);
}

async function appendDelegationLog(entry) {
  try {
    await fsp.appendFile(DELEGATION_LOG, JSON.stringify(entry) + '\n');
  } catch (err) {
    // Non-fatal: log to stderr but don't fail the dispatch
    console.error('[hermes-delegate] log append failed:', err.message);
  }
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    if (req.body && typeof req.body === 'object') return resolve(req.body);
    let raw = '';
    req.on('data', (c) => (raw += c));
    req.on('end', () => {
      if (!raw) return resolve({});
      try { resolve(JSON.parse(raw)); } catch (e) { reject(e); }
    });
    req.on('error', reject);
  });
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') {
    return res.status(405).json({
      status: 'error',
      error: 'Method not allowed',
      hint: 'POST { task, capability_required, lane_preference? }',
      timestamp: new Date().toISOString(),
    });
  }

  let body;
  try { body = await readBody(req); }
  catch (e) {
    return res.status(400).json({
      status: 'error',
      error: 'Invalid JSON body',
      detail: e.message,
      timestamp: new Date().toISOString(),
    });
  }

  const task = (body && body.task) ? String(body.task).trim() : '';
  const capability = body && body.capability_required
    ? body.capability_required
    : '';
  const lanePref = body && body.lane_preference
    ? String(body.lane_preference)
    : null;

  if (!task) {
    return res.status(400).json({
      status: 'error',
      error: 'Missing required field: task',
      timestamp: new Date().toISOString(),
    });
  }
  if (!capability) {
    return res.status(400).json({
      status: 'error',
      error: 'Missing required field: capability_required',
      hint: 'Provide a capability string or array of capability strings',
      timestamp: new Date().toISOString(),
    });
  }

  const now = new Date().toISOString();

  // Pick lane
  const pick = pickLane(capability, lanePref);
  if (!pick) {
    return res.status(500).json({
      status: 'error',
      error: 'No lanes available for delegation',
      timestamp: now,
    });
  }

  const task_id = generateTaskId(task, pick.lane, now);
  const profile = LANE_PROFILE[pick.lane] || { base_eta: 5.0 };
  // Slight jitter so eta_seconds is non-deterministic (still bounded)
  const jitter = (crypto.randomBytes(1)[0] / 255) * 1.5; // 0..1.5s
  const eta_seconds = Number((profile.base_eta + jitter).toFixed(2));

  const envelope = {
    status: 'delegated',
    delegated_to: pick.lane,
    task_id,
    eta_seconds,
    capability_match: {
      requested: capability,
      score: pick.score,
      reason: pick.reason,
    },
    task_preview: task.length > 120 ? task.slice(0, 117) + '...' : task,
    dispatch_mode: 'simulated',
    note: 'Simulated delegation — Vercel serverless cannot reach the sovereign substrate VM directly. The dispatch decision + task_id + eta are recorded locally for replay by the Mac-side runtime.',
    timestamp: now,
    sigil: null,
  };

  envelope.sigil = hmacSigil(envelope);

  // Best-effort append to audit log
  await appendDelegationLog({
    ts: now,
    task_id,
    delegated_to: pick.lane,
    capability_requested: capability,
    lane_preference: lanePref,
    pick_reason: pick.reason,
    capability_score: pick.score,
    eta_seconds,
    task_preview: envelope.task_preview,
    sigil: envelope.sigil,
  });

  return res.status(200).json(envelope);
};