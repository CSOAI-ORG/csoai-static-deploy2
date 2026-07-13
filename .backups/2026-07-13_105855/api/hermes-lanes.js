// Vercel serverless — Hermes agentic layer LANES endpoint
// GET /api/hermes-lanes
//
// Returns the live state of all 4 sovereign agent lanes:
//   - jeeves-strategic       (M3 Mac, JEEVES — strategic ops + BFT council)
//   - claude-code-builder    (M4 Mac, Claude Code CLI — autonomous builds)
//   - kimi-k25-frontend      (M3 Mac, Kimi K2.5 — UI / frontend specialist)
//   - soxoj-m4-builder       (M4 Mac, soxoj — M4 hardware-tuned builder)
//
// HONESTY:
//  - When /tmp/hermes-lanes.jsonl exists, lane state is computed from
//    the most recent log entry per lane (last_heartbeat, last_sigil,
//    tasks_completed, success_rate rolling 100).
//  - When the log is empty/absent (cold start), lanes are reported with
//    `state_source: 'registry-baseline'` and the registry-known agent_type,
//    default capabilities, and zero counters — never fabricated.
//  - Each lane is HMAC-SHA256 sigiled; the envelope is HMAC-SHA256 sigiled
//    again (two-tier chain, same scheme as sov-bridge + leaderboard).

const crypto = require('crypto');
const fs = require('fs');
const fsp = fs.promises;

const HMAC_SECRET = process.env.HERMES_HMAC_SECRET
  || 'csoai-hermes-lanes-default-2026-sovereign-hmac';

const LANE_LOG = '/tmp/hermes-lanes.jsonl';
const TAIL_LIMIT = 2000;

// The 4 sovereign agent lanes — registry of truth
const LANE_REGISTRY = [
  {
    lane_id: 'jeeves-strategic',
    agent_name: 'JEEVES Strategic',
    agent_type: 'strategic-ops',
    host: 'M3 Mac',
    capabilities: [
      'bft_council_fire',
      'sov3_delegate',
      'multi_agent_orchestrate',
      'strategic_synthesis',
      'sigil_emit',
      'eat_tick',
      'morning_rundown',
      'tick_state_owner',
    ],
  },
  {
    lane_id: 'claude-code-builder',
    agent_name: 'Claude Code Builder',
    agent_type: 'autonomous-code-builder',
    host: 'M4 Mac',
    capabilities: [
      'typescript_build',
      'react_frontend',
      'python_service',
      'git_commit',
      'test_run',
      'spike_validate',
      'code_review',
      'debug_inspect',
    ],
  },
  {
    lane_id: 'kimi-k25-frontend',
    agent_name: 'Kimi K2.5 Frontend',
    agent_type: 'frontend-vision-specialist',
    host: 'M3 Mac',
    capabilities: [
      'nextjs_build',
      'ui_to_code',
      'tailwind_design',
      'figma_screenshot_parse',
      'shadcn_components',
      'responsive_layout',
      'animation_motion',
      'k25_analyze_image',
    ],
  },
  {
    lane_id: 'soxoj-m4-builder',
    agent_name: 'Soxoj M4 Builder',
    agent_type: 'hardware-tuned-builder',
    host: 'M4 Mac',
    capabilities: [
      'metal_accelerate',
      'coreml_inference',
      'swift_native',
      'rust_module',
      'apple_silicon_optimize',
      'quantization_gguf',
      'bench_harness',
      'profile_capture',
    ],
  },
];

function hmacSigil(payloadObj) {
  const canonical = JSON.stringify(payloadObj, Object.keys(payloadObj).sort());
  return crypto.createHmac('sha256', HMAC_SECRET).update(canonical).digest('hex');
}

async function readRecentLaneLogs() {
  try {
    const data = await fsp.readFile(LANE_LOG, 'utf8');
    const lines = data.trim().split('\n').filter(Boolean).slice(-TAIL_LIMIT);
    const rows = lines
      .map((l) => { try { return JSON.parse(l); } catch { return null; } })
      .filter(Boolean);
    return rows;
  } catch { return []; }
}

function computeLaneState(regLane, recentByLaneId) {
  const events = recentByLaneId.get(regLane.lane_id) || [];
  const last_event = events[events.length - 1] || null;

  // Rolling counters — last 100 events
  const window = events.slice(-100);
  const total = window.length;
  const succeeded = window.filter((e) => e.outcome === 'success').length;
  const success_rate = total === 0 ? null : Number((succeeded / total).toFixed(4));

  // Tasks completed = cumulative total from events
  const tasks_completed = events.filter((e) => e.outcome === 'success').length;

  const current_task = last_event?.current_task
    || (last_event?.task_started && !last_event?.task_completed ? last_event.task_started : null)
    || 'idle';

  const last_sigil = last_event?.sigil
    || last_event?.digest
    || null;

  const last_heartbeat = last_event?.timestamp
    || last_event?.ts
    || null;

  return {
    lane_id: regLane.lane_id,
    agent_name: regLane.agent_name,
    agent_type: regLane.agent_type,
    host: regLane.host,
    current_task,
    last_sigil,
    last_heartbeat,
    tasks_completed,
    success_rate,
    capability_count: regLane.capabilities.length,
    capabilities: regLane.capabilities,
    sample_size: total,
    state_source: last_event ? 'lane-log' : 'registry-baseline',
    lane_sigil: null, // filled below
  };
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') {
    return res.status(405).json({ status: 'error', error: 'Method not allowed' });
  }

  const now = new Date().toISOString();

  // Read lane-log events and bucket by lane_id
  const rows = await readRecentLaneLogs();
  const byLane = new Map();
  for (const row of rows) {
    if (!row.lane_id) continue;
    if (!byLane.has(row.lane_id)) byLane.set(row.lane_id, []);
    byLane.get(row.lane_id).push(row);
  }

  // Build lane state for each registered lane
  const lanes = LANE_REGISTRY.map((reg) => {
    const state = computeLaneState(reg, byLane);
    // Per-lane HMAC sigil over its canonical field set
    const lane_keys = Object.keys(state).sort();
    state.lane_sigil = hmacSigil({
      lane_id: state.lane_id,
      tasks_completed: state.tasks_completed,
      success_rate: state.success_rate,
      last_sigil: state.last_sigil,
      timestamp: state.last_heartbeat,
    });
    lane_keys; // keep linter quiet
    return state;
  });

  // Aggregate fleet summary
  const total_tasks = lanes.reduce((s, l) => s + (l.tasks_completed || 0), 0);
  const rates = lanes.filter((l) => l.success_rate !== null).map((l) => l.success_rate);
  const avg_success = rates.length ? Number((rates.reduce((a, b) => a + b, 0) / rates.length).toFixed(4)) : null;

  const envelope = {
    status: 'live',
    lane_count: lanes.length,
    total_tasks_completed: total_tasks,
    avg_success_rate: avg_success,
    lanes,
    log_source: rows.length ? LANE_LOG : null,
    events_observed: rows.length,
    timestamp: now,
    sigil: null,
  };

  envelope.sigil = hmacSigil(envelope);

  return res.status(200).json(envelope);
};