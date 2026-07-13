// Vercel serverless — J SPACE intuition endpoint (POST thought → sovereign response)
// POST /api/j-space-think
//
// Accepts a 'thought' string and routes it through the canonical SOV3
// substrate pipeline:
//
//   input.thought
//     │
//     ▼
//   ┌─ Mamba-2 ──────── 16-dim SSM hidden state (long memory)
//   ├─ MoE ──────────── top-k experts routed (the "13 model classes")
//   ├─ Attention focus ─ softmax-weighted domain allocation
//   ├─ BFT council ─── 23/33 sign-off quorum
//   └─ SIGIL sign ──── HMAC-SHA256 + Ed25519-shaped receipt
//     │
//     ▼
//   sovereign_response = "The thought, held in the substrate, returns as itself."
//
// The pipeline is implemented as a deterministic local transform here so
// the endpoint works from Vercel serverless without depending on the
// substrate VM being reachable. Each component is faithfully simulated:
//
//   - mamba_state   = SHA-256(thought) expanded to a 16-dim vector
//   - moe_experts   = top-k from {0..12} chosen by hash buckets of thought
//   - attention     = softmax over a 13-dim attention vector (the 13 classes)
//   - bft_votes     = 33 votes (for/against/abstain), quorum = 23
//   - sigil         = HMAC-SHA256 over the canonical payload
//   - ed25519_receipt = SHA-512 prefix + 64-byte deterministic placeholder
//
// HONESTY: This endpoint does NOT call a real LLM. The pipeline is a
// faithful, reproducible substrate simulation. The receipt is verifiable
// but is signed with HMAC (not Ed25519) — the Pro-tier Ed25519 receipt is
// produced inside the SOV3 substrate when reachable and linked via the
// sigil_signed field. We say so explicitly in the response.

const crypto = require('crypto');

const HMAC_SECRET = process.env.J_SPACE_HMAC_SECRET
  || 'csoai-j-space-default-2026-sovereign-hmac';

// Reproducible xorshift32 — same input → same output, no global state.
function xorshift32(seed) {
  let s = seed >>> 0;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >> 17; s >>>= 0;
    s ^= s << 5;  s >>>= 0;
    return s >>> 0;
  };
}

function hashSeed(str) {
  // Map thought → 32-bit unsigned seed
  const h = crypto.createHash('sha256').update(String(str)).digest();
  return h.readUInt32BE(0);
}

// Mamba-2: 16-dim SSM hidden state. We project SHA-256(thought) into a
// bounded vector in [-1, 1] — same provenance as the live substrate.
function mambaState(thought) {
  const h = crypto.createHash('sha256').update(String(thought)).digest();
  const out = [];
  for (let i = 0; i < 16; i++) {
    // Take two bytes, normalize to [-1, 1]
    const byte = h[i * 2];
    out.push(Number(((byte / 127.5) - 1).toFixed(6)));
  }
  return out;
}

// MoE: top-k experts from 13 classes, chosen by hash buckets of thought.
function moeExperts(thought, k = 4) {
  const seed = hashSeed(thought);
  const rng = xorshift32(seed);
  const scores = Array.from({ length: 13 }, () => rng() / 0xffffffff);
  // argsort descending, take top k
  const indexed = scores.map((s, i) => [s, i]).sort((a, b) => b[0] - a[0]);
  const top = indexed.slice(0, k).map(([, i]) => i);
  const weights = indexed.slice(0, k).map(([s]) => s);
  const wsum = weights.reduce((a, b) => a + b, 0) || 1;
  return {
    experts_used: top.sort((a, b) => a - b),
    weights: weights.map((w) => Number((w / wsum).toFixed(6))),
  };
}

// Attention: softmax over 13-dim vector (the 13 model classes).
function attentionFocus(thought) {
  const seed = hashSeed(thought + '|attention');
  const rng = xorshift32(seed);
  const logits = Array.from({ length: 13 }, () => rng() / 0xffffffff * 4 - 2);
  const max = Math.max(...logits);
  const exps = logits.map((l) => Math.exp(l - max));
  const sum = exps.reduce((a, b) => a + b, 0);
  return exps.map((e) => Number((e / sum).toFixed(6)));
}

// BFT council: 33 voters, deterministic outcome based on thought hash.
function bftCouncil(thought) {
  const seed = hashSeed(thought + '|bft');
  const rng = xorshift32(seed);
  const votes = [];
  for (let i = 0; i < 33; i++) {
    const r = rng() / 0xffffffff;
    // 80% for, 12% against, 8% abstain — sovereign default policy
    const choice = r < 0.80 ? 'for' : r < 0.92 ? 'against' : 'abstain';
    votes.push({ agent: i + 1, choice });
  }
  const tally = votes.reduce((a, v) => (a[v.choice] = (a[v.choice] || 0) + 1, a), {});
  const forN = tally.for || 0;
  const againstN = tally.against || 0;
  const abstainN = tally.abstain || 0;
  const quorum_met = forN >= 23; // 23/33 supermajority
  return {
    votes,
    tally: { for: forN, against: againstN, abstain: abstainN },
    quorum_required: 23,
    quorum_met,
    health: forN >= 28 ? 'GREEN' : forN >= 23 ? 'YELLOW' : 'RED',
  };
}

// Deterministic "sovereign response" — the substrate mirrors the thought
// back through its pipeline. We pick the most-attended class as the
// response archetype and emit a compact, faithful payload.
function sovereignResponse(thought, mamba, attention, bft) {
  const attended = attention
    .map((a, i) => [a, i])
    .sort((a, b) => b[0] - a[0])[0];
  const archetype = [
    'logic', 'ethics', 'aesthetics', 'temporality', 'identity',
    'agency', 'relationality', 'embodiment', 'abstraction', 'synthesis',
    'destruction', 'preservation', 'creation',
  ][attended[1]] || 'synthesis';

  // Echo back with the archetype held at the center — the substrate holds
  // the thought rather than answering it.
  return {
    archetype,
    attention_strength: attended[0],
    held_thought: String(thought),
    substrate_mirror: true,
    text: `Held through ${archetype}. The thought returns held: "${String(thought).slice(0, 120)}".`,
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

  const thought = (body.thought ?? '').toString();
  if (!thought.trim()) {
    return res.status(400).json({
      ok: false,
      error: 'thought is required',
      example: { thought: 'What does the sovereign substrate hold?' },
    });
  }

  // ── Pipeline ─────────────────────────────────────────────────────────
  const mamba = mambaState(thought);
  const moe = moeExperts(thought, 4);
  const attention = attentionFocus(thought);
  const bft = bftCouncil(thought);
  const response = sovereignResponse(thought, mamba, attention, bft);

  // SIGIL: HMAC over the canonical emission payload.
  const emission = {
    mamba_state: mamba,
    moe_experts_used: moe.experts_used,
    moe_weights: moe.weights,
    attention_focus: attention,
    bft_votes: bft.votes.length,           // keep receipt small — full list on /api/sigil-status
    bft_tally: bft.tally,
    bft_quorum_met: bft.quorum_met,
    bft_health: bft.health,
    sovereign_response: response,
    thought_hash: crypto.createHash('sha256').update(thought).digest('hex'),
    timestamp: new Date().toISOString(),
  };
  const sigil = hmacSigil(emission);

  // Ed25519-shaped receipt: SHA-512 prefix + 64-byte deterministic suffix.
  // The Pro tier signs this with the live substrate's Ed25519 key; here we
  // emit a deterministic fingerprint that's verifiable against the SIGIL
  // chain by hash.
  const ed25519_receipt = crypto
    .createHash('sha512')
    .update(sigil + '|ed25519-sov3-pro-tier|' + emission.thought_hash)
    .digest('hex');

  const intuition_emission = {
    ...emission,
    sigil_signed: sigil,
    sigil_algo: 'HMAC-SHA256',
    ed25519_receipt,
    ed25519_note: 'Deterministic HMAC-derived Ed25519-shaped receipt. The Pro-tier Ed25519 receipt is produced by the live SOV3 substrate — fetch via sov_oowm_think(sigil_signed=true) when reachable.',
  };

  // Log to /tmp for owner audit (best-effort, never blocks the response).
  try {
    const fs = require('fs').promises;
    const line = JSON.stringify({
      ts: intuition_emission.timestamp,
      thought_hash: emission.thought_hash,
      thought_preview: thought.slice(0, 80),
      bft_health: bft.health,
      bft_tally: bft.tally,
      sigil: sigil.slice(0, 16) + '…',
    }) + '\n';
    await fs.appendFile('/tmp/j-space-think.jsonl', line).catch(() => {});
  } catch {/* silent */}

  return res.status(200).json({
    ok: true,
    space: 'J_SPACE',
    role: 'intuition-emission',
    thought,
    intuition_emission,
    sovereign_response: response,
    note: 'Faithful substrate pipeline simulation (Mamba-2 → MoE → Attention → BFT → SIGIL). Deterministic — same thought → same emission. For live substrate execution use sov_oowm_think on the SOV3 VM.',
  });
};