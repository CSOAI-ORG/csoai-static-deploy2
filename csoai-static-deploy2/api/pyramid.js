// Vercel serverless — SOV3³ Pyramid clan routing endpoint
//
// POST /api/pyramid
//
// Routes through the 4-level hierarchy:
//   L0: Cache (<1ms)
//   L1: Local OWEM (1-5s, single-family specialist)
//   L2: Cross-family council (3-10s, 3-family BFT vote)
//   L3: Frontier oracle (2-30s, Groq/OpenRouter)

const crypto = require('crypto');

const HMAC_SECRET = process.env.OWEM_HMAC_SECRET || 'csoai-owem-default-2026-sovereign-hmac';

const LANE_MODELS = {
  compliance: 'sov33-qwen-compliance',
  defence: 'sov33-llama-defence',
  intuition: 'sov33-deepseek-intuition',
  voice: 'sov33-qwen-voice',
  general: 'sov33-qwen-general',
};

const COUNCIL_MODELS = ['sov33-qwen-general', 'sov33-llama-general', 'sov33-mistral-general'];

function classifyLane(message) {
  const laneSignals = {
    compliance: ['eu ai act','gdpr','iso 42001','compliance','regulation','article','deadline','fine'],
    defence: ['aukus','nato','dasa','mod','defence','military','jsp','ncsc'],
    intuition: ['market','strategy','moat','forecast','trend','adoption','pipeline'],
    voice: ['who are you','what can you do','article 0','invariants','care floor','identity'],
    general: ['what is','capital of','derivative','chemical','math','calculate'],
  };
  let best = 'general', bestScore = 0;
  for (const [lane, keywords] of Object.entries(laneSignals)) {
    const score = keywords.filter(kw => message.toLowerCase().includes(kw)).length;
    if (score > bestScore) { bestScore = score; best = lane; }
  }
  return bestScore > 0 ? best : 'general';
}

function estimateDifficulty(message) {
  const techTerms = ['article','regulation','compliance','framework','conformity','assessment','governance','sovereign','bft','sigil'];
  const regimes = ['eu ai act','gdpr','iso 42001','uk aisi','ncsc','aukus','nato'];
  const openWords = ['why','explain','compare','analyze','evaluate','discuss'];
  const signals = {
    length: Math.min(1.0, message.length / 200),
    technical_density: Math.min(1.0, techTerms.filter(t => message.toLowerCase().includes(t)).length / 4),
    regulatory_cross_ref: Math.min(1.0, regimes.filter(r => message.toLowerCase().includes(r)).length / 3),
    open_endedness: Math.min(1.0, openWords.filter(w => message.toLowerCase().includes(w)).length / 2),
  };
  const w = { length: 0.15, technical_density: 0.30, regulatory_cross_ref: 0.30, open_endedness: 0.25 };
  return Number(Object.keys(w).reduce((s, k) => s + (signals[k] || 0) * w[k], 0).toFixed(3));
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
  const laneOverride = (body.lane ?? '').toString() || null;
  if (!message.trim()) return res.status(400).json({ ok: false, error: 'message required' });

  const ts = new Date().toISOString();
  const lane = laneOverride || classifyLane(message);
  const difficulty = estimateDifficulty(message);

  // Simulate pyramid routing — determine final level
  const path = [];
  let finalLevel = 0;

  // L0: Cache (always miss in serverless)
  path.push({ level: 0, name: 'cache', result: 'MISS' });

  // L1: Local OWEM
  if (difficulty <= 0.5) {
    finalLevel = 1;
    path.push({ level: 1, name: 'local_owem', model: LANE_MODELS[lane] || LANE_MODELS.general, lane, result: 'OK' });
  } else {
    path.push({ level: 1, name: 'local_owem', result: 'ESCALATED', reason: 'high_difficulty' });

    // L2: Cross-family council
    if (difficulty <= 0.8) {
      finalLevel = 2;
      path.push({ level: 2, name: 'cross_family_council', models: COUNCIL_MODELS, result: 'ALLOW' });
    } else {
      path.push({ level: 2, name: 'cross_family_council', result: 'ESCALATED', reason: 'very_high_difficulty' });
      finalLevel = 3;
      path.push({ level: 3, name: 'frontier_oracle', result: 'REACHED', note: 'Requires OPENROUTER_API_KEY' });
    }
  }

  const sigil = hmacSigil({ level: finalLevel, lane, difficulty, ts });

  return res.status(200).json({
    status: 'pyramid_routed',
    final_level: finalLevel,
    level_name: ['cache', 'local_owem', 'cross_family_council', 'frontier_oracle'][finalLevel],
    lane,
    difficulty,
    path,
    escalation_triggers: {
      L0_to_L1: 'cache_miss',
      L1_to_L2: 'confidence < 0.7 OR care_score < 0.95',
      L2_to_L3: 'bft_vote FAILS quorum OR difficulty > 0.8',
    },
    sigil,
    sigil_algo: 'HMAC-SHA256',
    timestamp: ts,
    note: 'Deterministic pyramid routing simulation. For live substrate routing use sov33_pyramid_clan.py locally.',
  });
};
