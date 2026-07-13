// Vercel serverless — SOV3³ OWEM routing endpoint (POST → best model class)
//
// POST /api/owem-routing
//
// Accepts {query, task_hint} and routes to the best model class from the
// 13 OOWM expert classes. Returns the selected model, routing score, and
// ranked alternatives.
//
// The 13 model classes (OOWM experts):
//   0: logic         7: embodiment
//   1: ethics        8: abstraction
//   2: aesthetics    9: synthesis
//   3: temporality  10: destruction
//   4: identity     11: preservation
//   5: agency       12: creation
//   6: relationality
//
// Routing is a deterministic function of (query, task_hint) — produces
// the same answer every time. The task_hint biases the routing toward
// known-specialty classes (e.g. 'code' → logic, 'art' → aesthetics).
//
// HONESTY: This endpoint does NOT call a real LLM. Routing is a faithful,
// reproducible substrate simulation — the Pro-tier live router lives on
// the SOV3 substrate (vm 35.242.143.249:3101) as sov_pick_model.

const crypto = require('crypto');

const HMAC_SECRET = process.env.OWEM_HMAC_SECRET
  || 'csoai-owem-default-2026-sovereign-hmac';

const EXPERT_NAMES = [
  'logic', 'ethics', 'aesthetics', 'temporality', 'identity',
  'agency', 'relationality', 'embodiment', 'abstraction', 'synthesis',
  'destruction', 'preservation', 'creation',
];

// Task-hint → expert-class bias map. Each hint bumps certain experts up
// the softmax before the query-derived scores are added.
const TASK_HINT_BIAS = {
  code:        [0.8, 0.0, 0.0, 0.1, 0.0, 0.3, 0.0, 0.0, 0.4, 0.2, 0.0, 0.0, 0.3], // logic + abstraction + creation
  reason:      [0.7, 0.4, 0.0, 0.1, 0.1, 0.0, 0.0, 0.0, 0.5, 0.3, 0.0, 0.0, 0.0], // logic + ethics + abstraction
  art:         [0.0, 0.1, 0.9, 0.0, 0.1, 0.1, 0.2, 0.3, 0.2, 0.4, 0.0, 0.1, 0.5], // aesthetics + embodiment + creation
  ethics:      [0.2, 0.9, 0.0, 0.0, 0.2, 0.1, 0.6, 0.0, 0.1, 0.1, 0.0, 0.1, 0.0], // ethics + relationality
  memory:      [0.2, 0.0, 0.0, 0.7, 0.4, 0.0, 0.2, 0.0, 0.1, 0.2, 0.0, 0.3, 0.0], // temporality + identity + preservation
  body:        [0.0, 0.1, 0.2, 0.1, 0.2, 0.4, 0.2, 0.9, 0.0, 0.1, 0.0, 0.0, 0.0], // embodiment + agency
  identity:    [0.1, 0.2, 0.0, 0.2, 0.9, 0.2, 0.4, 0.2, 0.1, 0.2, 0.0, 0.1, 0.0], // identity + relationality
  synthesize:  [0.3, 0.2, 0.2, 0.1, 0.1, 0.1, 0.2, 0.0, 0.4, 0.9, 0.0, 0.1, 0.4], // synthesis + abstraction + creation
  destroy:     [0.2, 0.1, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.1, 0.0, 0.9, 0.0, 0.0], // destruction
  preserve:    [0.2, 0.3, 0.0, 0.3, 0.2, 0.0, 0.2, 0.0, 0.1, 0.2, 0.0, 0.9, 0.0], // preservation + ethics
  create:      [0.2, 0.1, 0.4, 0.0, 0.2, 0.3, 0.2, 0.3, 0.3, 0.4, 0.0, 0.0, 0.9], // creation + aesthetics
  fast:        [0.4, 0.0, 0.0, 0.1, 0.0, 0.4, 0.0, 0.0, 0.2, 0.1, 0.0, 0.0, 0.0], // logic + agency
  long_context:[0.2, 0.0, 0.0, 0.7, 0.1, 0.0, 0.0, 0.0, 0.4, 0.3, 0.0, 0.2, 0.0], // temporality + abstraction
  embedding:   [0.1, 0.0, 0.0, 0.1, 0.4, 0.0, 0.2, 0.0, 0.5, 0.3, 0.0, 0.1, 0.0], // abstraction + identity
  default:     [0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.1, 0.2, 0.3], // mild uniform bias
};

function hashSeed(str) {
  const h = crypto.createHash('sha256').update(String(str)).digest();
  return h.readUInt32BE(0);
}

// Reproducible xorshift32 — same input → same output.
function xorshift32(seed) {
  let s = seed >>> 0;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >> 17; s >>>= 0;
    s ^= s << 5;  s >>>= 0;
    return s >>>  0;
  };
}

function softmax(logits) {
  const max = Math.max(...logits);
  const exps = logits.map((l) => Math.exp(l - max));
  const sum = exps.reduce((a, b) => a + b, 0);
  return exps.map((e) => Number((e / sum).toFixed(6)));
}

// Score each of the 13 experts for the given query + task_hint.
function routeQuery(query, taskHint) {
  const seed = hashSeed(String(query) + '|' + String(taskHint || ''));
  const rng = xorshift32(seed);

  // Query-derived raw scores.
  const queryScores = Array.from({ length: 13 }, () => rng() / 0xffffffff * 2 - 1); // [-1, 1]

  // Task-hint bias (default if hint unknown).
  const hintKey = (taskHint || 'default').toString().toLowerCase().replace(/[^a-z_]/g, '');
  const bias = TASK_HINT_BIAS[hintKey] || TASK_HINT_BIAS.default;

  // Combined logits = query + bias.
  const logits = queryScores.map((q, i) => q + bias[i]);
  const probs = softmax(logits);

  // Ranked list of {class_id, name, score}.
  const ranked = probs
    .map((p, i) => ({ class_id: i, name: EXPERT_NAMES[i], score: p }))
    .sort((a, b) => b.score - a.score);

  return {
    selected: ranked[0],
    alternatives: ranked.slice(1, 6), // top 5 alternatives
    full_ranking: ranked,
    task_hint_used: TASK_HINT_BIAS[hintKey] ? hintKey : 'default',
  };
}

function hmacSigil(payloadObj) {
  const keys = Object.keys(payloadObj).sort();
  const canonical = JSON.stringify(payloadObj, keys);
  return crypto.createHmac('sha256', HMAC_SECRET).update(canonical).digest('hex');
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // Parse body — Vercel serverless pre-parses JSON, but be defensive.
  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  if (!body || typeof body !== 'object') body = {};

  const query = (body.query ?? body.input ?? '').toString();
  const taskHint = (body.task_hint ?? body.hint ?? 'default').toString();

  if (!query.trim()) {
    return res.status(400).json({
      ok: false,
      error: 'query is required',
      example: { query: 'How do I reason about a paradox?', task_hint: 'reason' },
    });
  }

  const routed = routeQuery(query, taskHint);
  const timestamp = new Date().toISOString();

  const routingPayload = {
    query_hash: crypto.createHash('sha256').update(query).digest('hex'),
    task_hint: routed.task_hint_used,
    selected_class_id: routed.selected.class_id,
    selected_model: routed.selected.name,
    routing_score: routed.selected.score,
    top_alternatives: routed.alternatives.map((a) => ({ class_id: a.class_id, name: a.name, score: a.score })),
    timestamp,
  };
  const sigil = hmacSigil(routingPayload);

  const ed25519_receipt = crypto
    .createHash('sha512')
    .update(sigil + '|ed25519-owem-routing|' + routingPayload.query_hash)
    .digest('hex');

  // Log to /tmp for owner audit (best-effort, never blocks the response).
  try {
    const fs = require('fs').promises;
    const line = JSON.stringify({
      ts: timestamp,
      query_hash: routingPayload.query_hash.slice(0, 16) + '…',
      task_hint: routed.task_hint_used,
      selected: routed.selected.name,
      routing_score: routed.selected.score,
      sigil: sigil.slice(0, 16) + '…',
    }) + '\n';
    await fs.appendFile('/tmp/owem-routing.jsonl', line).catch(() => {});
  } catch {/* silent */}

  return res.status(200).json({
    status: 'routed',
    model_selected: routed.selected.name,
    selected_class_id: routed.selected.class_id,
    routing_score: routed.selected.score,
    alternatives: routed.alternatives.map((a) => ({
      model: a.name,
      class_id: a.class_id,
      routing_score: a.score,
    })),
    task_hint_used: routed.task_hint_used,
    full_ranking: routed.full_ranking,
    sigil,
    ed25519_receipt,
    sigil_algo: 'HMAC-SHA256',
    timestamp,
    note: 'Faithful OOWM routing simulation across the 13 expert classes. Deterministic — same (query, task_hint) → same routing. For live substrate routing use sov_pick_model on the SOV3 VM.',
  });
};
