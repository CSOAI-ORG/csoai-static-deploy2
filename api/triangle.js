// Vercel serverless — SOV3³ Triangle clan routing endpoint
//
// POST /api/triangle
//
// Routes a message through the 3-around-1 triangle topology:
//   3 small OWEMs at vertices (different families)
//   + 1 general OWEM at center (queen/governor)
//
// The triangle computes rho (lineage decorrelation) and decides
// whether to commit locally or escalate to center.

const crypto = require('crypto');

const HMAC_SECRET = process.env.OWEM_HMAC_SECRET || 'csoai-owem-default-2026-sovereign-hmac';

const TRIANGLE_VERTICES = [
  { position: 0, family: 'qwen',     owem: 'compliance' },
  { position: 1, family: 'llama',    owem: 'defence' },
  { position: 2, family: 'deepseek', owem: 'intuition' },
];
const TRIANGLE_CENTER = { family: 'qwen', owem: 'general' };

function hashSeed(str) {
  return crypto.createHash('sha256').update(String(str)).digest().readUInt32BE(0);
}

function xorshift32(seed) {
  let s = seed >>> 0;
  return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s >>>= 0; s ^= s << 5; s >>>= 0; return s >>> 0; };
}

function estimateDifficulty(message) {
  const signals = {};
  signals.length = Math.min(1.0, message.length / 200);
  const techTerms = ['article','regulation','compliance','framework','conformity','assessment','governance','sovereign','bft','sigil'];
  signals.technical_density = Math.min(1.0, techTerms.filter(t => message.toLowerCase().includes(t)).length / 4);
  const regimes = ['eu ai act','gdpr','iso 42001','uk aisi','ncsc','aukus','nato'];
  signals.regulatory_cross_ref = Math.min(1.0, regimes.filter(r => message.toLowerCase().includes(r)).length / 3);
  const weights = { length: 0.2, technical_density: 0.35, regulatory_cross_ref: 0.45 };
  const difficulty = Object.keys(weights).reduce((s, k) => s + (signals[k] || 0) * weights[k], 0);
  return { difficulty: Number(difficulty.toFixed(3)), signals, verdict: difficulty > 0.6 ? 'HARD' : difficulty > 0.3 ? 'MEDIUM' : 'EASY' };
}

function computeRho(message, vertices) {
  const seed = hashSeed(message + '|rho');
  const rng = xorshift32(seed);
  const sim = (rng() / 0xffffffff) * 0.6 + 0.1;
  return { rho: Number((1 - sim).toFixed(4)), avg_similarity: Number(sim.toFixed(4)), source: 'deterministic-hash-seeded' };
}

function hmacSigil(obj) {
  return crypto.createHmac('sha256', HMAC_SECRET).update(JSON.stringify(obj, Object.keys(obj).sort())).digest('hex');
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  if (!body || typeof body !== 'object') body = {};

  const message = (body.message ?? body.query ?? '').toString();
  const lane = (body.lane ?? '').toString() || null;
  const difficultyOverride = body.difficulty != null ? Number(body.difficulty) : null;

  if (!message.trim()) return res.status(400).json({ ok: false, error: 'message required' });

  const ts = new Date().toISOString();
  const diff = estimateDifficulty(message);
  if (difficultyOverride !== null) {
    diff.difficulty = difficultyOverride;
    diff.verdict = difficultyOverride > 0.6 ? 'HARD' : difficultyOverride > 0.3 ? 'MEDIUM' : 'EASY';
  }

  const rho = computeRho(message, TRIANGLE_VERTICES);
  const shouldEscalate = diff.difficulty > 0.5 || rho.rho < 0.7;
  const nEff = Number((3 * rho.rho).toFixed(2));

  const vertices = TRIANGLE_VERTICES.map(v => ({
    name: `sov33-${v.family}-${v.owem}`,
    family: v.family,
    owem: v.owem,
    in_lane: lane ? v.owem === lane : true,
    local: 'ALLOW',
    verdict: 'ALLOW',
  }));

  const sigil = hmacSigil({ message_hash: crypto.createHash('sha256').update(message).digest('hex').slice(0, 16), ruling: shouldEscalate ? 'ESCALATED' : 'COMMITTED_LOCAL', rho: rho.rho, timestamp: ts });

  return res.status(200).json({
    status: 'triangle_routed',
    ruling: shouldEscalate ? 'ESCALATED' : 'COMMITTED_LOCAL',
    message_preview: message.slice(0, 80),
    lane,
    difficulty: diff,
    vertices,
    center: { model: `sov33-${TRIANGLE_CENTER.family}-${TRIANGLE_CENTER.owem}`, family: TRIANGLE_CENTER.family, escalated_to: shouldEscalate },
    rho,
    n_eff_votes: nEff,
    small_owems: vertices,
    sigil,
    sigil_algo: 'HMAC-SHA256',
    timestamp: ts,
    note: 'Deterministic triangle routing simulation. For live substrate routing use sov33_triangle_v2.py locally.',
  });
};
