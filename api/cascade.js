// Vercel serverless — SOV3³ Cascade clan routing endpoint
//
// POST /api/cascade
//
// Routes through the 10/90 cascade topology:
//   LEFT brain (small fast) handles 90% of traffic
//   RIGHT brain (large deep) handles 10% escalations

const crypto = require('crypto');

const HMAC_SECRET = process.env.OWEM_HMAC_SECRET || 'csoai-owem-default-2026-sovereign-hmac';
const LEFT_MODEL = 'sov33-qwen-general';
const RIGHT_MODEL = 'sov33-mistral-general';
const DIFFICULTY_THRESHOLD = 0.5;

function estimateDifficulty(message) {
  const signals = {};
  signals.length = Math.min(1.0, message.length / 200);
  const techTerms = ['article','regulation','compliance','framework','conformity','assessment','governance','sovereign','bft','sigil','quorum','annex','directive','statutory'];
  signals.technical_density = Math.min(1.0, techTerms.filter(t => message.toLowerCase().includes(t)).length / 4);
  const regimes = ['eu ai act','gdpr','iso 42001','uk aisi','ncsc','caf','cra','aukus','nato','dasa','jsp 936','nist','ieee'];
  signals.regulatory_cross_ref = Math.min(1.0, regimes.filter(r => message.toLowerCase().includes(r)).length / 3);
  const openWords = ['why','how does','explain','compare','analyze','evaluate','discuss','implications'];
  signals.open_endedness = Math.min(1.0, openWords.filter(w => message.toLowerCase().includes(w)).length / 2);
  const weights = { length: 0.15, technical_density: 0.30, regulatory_cross_ref: 0.30, open_endedness: 0.25 };
  const difficulty = Object.keys(weights).reduce((s, k) => s + (signals[k] || 0) * weights[k], 0);
  return { difficulty: Number(difficulty.toFixed(3)), signals, verdict: difficulty > 0.6 ? 'HARD' : difficulty > 0.3 ? 'MEDIUM' : 'EASY' };
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
  if (!message.trim()) return res.status(400).json({ ok: false, error: 'message required' });

  const ts = new Date().toISOString();
  const diff = estimateDifficulty(message);
  const escalated = diff.difficulty > DIFFICULTY_THRESHOLD;

  const sigil = hmacSigil({
    message_hash: crypto.createHash('sha256').update(message).digest('hex').slice(0, 16),
    decision: escalated ? 'RIGHT' : 'LEFT',
    difficulty: diff.difficulty,
    timestamp: ts,
  });

  return res.status(200).json({
    status: 'cascade_routed',
    decision: escalated ? 'RIGHT' : 'LEFT',
    difficulty: diff,
    left: { model: LEFT_MODEL, family: 'qwen', role: 'fast (90%)', ok: true },
    right: escalated ? { model: RIGHT_MODEL, family: 'mistral', role: 'deep (10%)', ok: true } : null,
    escalated_to_right: escalated,
    rationale: escalated
      ? `Difficulty ${diff.difficulty} > ${DIFFICULTY_THRESHOLD} → escalated to RIGHT (${RIGHT_MODEL})`
      : `Difficulty ${diff.difficulty} ≤ ${DIFFICULTY_THRESHOLD} → handled by LEFT (${LEFT_MODEL})`,
    sigil,
    sigil_algo: 'HMAC-SHA256',
    timestamp: ts,
    note: 'Deterministic cascade routing simulation. For live substrate routing use sov33_cascade_v2.py locally.',
  });
};
