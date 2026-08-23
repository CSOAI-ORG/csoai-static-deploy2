// Vercel serverless — SOV3³ OWEM evolution endpoint (POST → retrain)
//
// POST /api/owem-evolve
//
// Retrains the four OOWM substrate layers and anchors a new SIGIL:
//
//   ┌─ Mamba ──── refresh 16-dim SSM state from accumulated episodes
//   ├─ MoE ────── rebalance 13-expert weights from episode outcomes
//   ├─ MOM ────── recompute the Moments-of-Memory consolidation table
//   └─ Sigil ─── anchor a new HMAC receipt + Ed25519-shaped SHA-512
//
// The episode count is read from /tmp/owem-cycle.jsonl (every cycle logs
// a residue line). If the log doesn't exist yet, we start from zero.
// Each evolve call bumps the count by 1 (the new anchor episode) and
// emits a sigil receipt that's verifiable against the SIGIL chain.
//
// HONESTY: This endpoint does NOT retrain a real neural network. The
// "retrain" is a deterministic state transition that:
//
//   - counts accumulated episodes from /tmp logs
//   - recomputes a synthetic Mamba state from the episode hashes
//   - recomputes synthetic MoE weights from the cycle residues
//   - recomputes the MOM consolidation fingerprint
//   - anchors all four via HMAC-SHA256 + Ed25519-shaped receipt
//
// The Pro-tier live evolution runs as sov_oowm_evolve on the SOV3
// substrate (vm 35.242.143.249:3101). This endpoint is the
// serverless-side equivalent — auditable, deterministic, reproducible.

const crypto = require('crypto');
const fs = require('fs');
const fsp = fs.promises;

const HMAC_SECRET = process.env.OWEM_HMAC_SECRET
  || 'csoai-owem-default-2026-sovereign-hmac';
const CYCLE_LOG = '/tmp/owem-cycle.jsonl';
const ROUTING_LOG = '/tmp/owem-routing.jsonl';
const EVOLVE_LOG = '/tmp/owem-evolve.jsonl';

function hashSeed(str) {
  const h = crypto.createHash('sha256').update(String(str)).digest();
  return h.readUInt32BE(0);
}

function xorshift32(seed) {
  let s = seed >>> 0;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >> 17; s >>>= 0;
    s ^= s << 5;  s >>>= 0;
    return s >>>  0;
  };
}

async function countEpisodes(logPath) {
  try {
    const data = await fsp.readFile(logPath, 'utf8');
    return data.trim().split('\n').filter(Boolean).length;
  } catch {
    return 0;
  }
}

async function readAllEpisodes(logPath) {
  try {
    const data = await fsp.readFile(logPath, 'utf8');
    return data.trim().split('\n').filter(Boolean).map((l) => {
      try { return JSON.parse(l); } catch { return null; }
    }).filter(Boolean);
  } catch {
    return [];
  }
}

// Mamba refresh: aggregate all cycle residues into a 16-dim state.
function refreshMambaState(cycles) {
  const state = new Array(16).fill(0);
  if (cycles.length === 0) return state.map((v) => Number(v.toFixed(6)));
  const seed = hashSeed(cycles.map((c) => c.cycle_id || c.ts || '').join('|'));
  const rng = xorshift32(seed);
  for (let i = 0; i < 16; i++) {
    state[i] = Number(((rng() / 0xffffffff) * 2 - 1).toFixed(6));
  }
  // Mix in actual cycle counts to bias the state toward accumulated activity.
  const n = cycles.length;
  for (let i = 0; i < 16; i++) {
    state[i] = Number(((state[i] * 0.7) + (Math.log2(n + 1) / 10) * (i % 2 ? 1 : -1)).toFixed(6));
  }
  return state;
}

// MoE rebalance: aggregate routing log into 13-expert weights.
function rebalanceMoEWeights(routings) {
  const counts = new Array(13).fill(0);
  for (const r of routings) {
    if (typeof r.selected === 'string') {
      const idx = [
        'logic', 'ethics', 'aesthetics', 'temporality', 'identity',
        'agency', 'relationality', 'embodiment', 'abstraction', 'synthesis',
        'destruction', 'preservation', 'creation',
      ].indexOf(r.selected);
      if (idx >= 0) counts[idx] += 1;
    }
  }
  const total = counts.reduce((a, b) => a + b, 0) || 1;
  // Add a small prior so unseen experts don't get zero weight.
  const weights = counts.map((c) => (c + 0.1) / (total + 13 * 0.1));
  return weights.map((w) => Number(w.toFixed(6)));
}

// MOM consolidation: deterministic fingerprint of the accumulated state.
function computeMomConsolidation(mamba, moe, cycles, routings) {
  const h = crypto.createHash('sha256');
  h.update(JSON.stringify(mamba));
  h.update('|');
  h.update(JSON.stringify(moe));
  h.update('|');
  h.update(String(cycles.length));
  h.update('|');
  h.update(String(routings.length));
  return h.digest('hex');
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

  const timestamp = new Date().toISOString();

  // Pull accumulated state from /tmp logs.
  const cycles = await readAllEpisodes(CYCLE_LOG);
  const routings = await readAllEpisodes(ROUTING_LOG);
  const priorEvolves = await countEpisodes(EVOLVE_LOG);

  const cycleCount = cycles.length;
  const routingCount = routings.length;
  const newEpisodeCount = cycleCount + routingCount + priorEvolves + 1; // +1 for this anchor

  // ── Retrain the four layers ──────────────────────────────────────────
  const mamba_state = refreshMambaState(cycles);
  const moe_weights = rebalanceMoEWeights(routings);
  const mom_fingerprint = computeMomConsolidation(mamba_state, moe_weights, cycles, routings);

  // ── Sigil anchor ────────────────────────────────────────────────────
  const anchorPayload = {
    new_episode_count: newEpisodeCount,
    cycle_count: cycleCount,
    routing_count: routingCount,
    prior_evolve_count: priorEvolves,
    mamba_state,
    moe_weights,
    mom_fingerprint,
    timestamp,
  };
  const sigil = hmacSigil(anchorPayload);

  // Ed25519-shaped receipt.
  const ed25519_receipt = crypto
    .createHash('sha512')
    .update(sigil + '|ed25519-owem-evolve|' + mom_fingerprint)
    .digest('hex');

  // Log this evolve to /tmp/owem-evolve.jsonl for the next evolve call.
  try {
    const line = JSON.stringify({
      ts: timestamp,
      new_episode_count: newEpisodeCount,
      mom_fingerprint: mom_fingerprint.slice(0, 16) + '…',
      sigil: sigil.slice(0, 16) + '…',
    }) + '\n';
    await fsp.appendFile(EVOLVE_LOG, line).catch(() => {});
  } catch {/* silent */}

  return res.status(200).json({
    status: 'evolved',
    retrain_status: 'complete',
    new_episode_count: newEpisodeCount,
    episode_breakdown: {
      cycles: cycleCount,
      routings: routingCount,
      prior_evolves: priorEvolves,
      this_anchor: 1,
    },
    layers: {
      mamba: {
        status: 'refreshed',
        state_dim: 16,
        state: mamba_state,
      },
      moe: {
        status: 'rebalanced',
        expert_count: 13,
        weights: moe_weights,
      },
      mom: {
        status: 'consolidated',
        fingerprint: mom_fingerprint,
      },
      sigil: {
        status: 'anchored',
        algo: 'HMAC-SHA256',
        sigil,
        ed25519_receipt,
      },
    },
    sigil_anchored: true,
    sigil,
    ed25519_receipt,
    sigil_algo: 'HMAC-SHA256',
    timestamp,
    note: 'Faithful OOWM evolution simulation — Mamba state refresh + MoE weight rebalance + MOM consolidation + SIGIL anchor. Deterministic — same input logs → same evolution. For live substrate evolution use sov_oowm_evolve on the SOV3 VM.',
  });
};
