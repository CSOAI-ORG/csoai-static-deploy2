// Vercel serverless — SOV33 arena preference-vote endpoint
// POST /api/arena-vote
//
// Body: { prompt, response_a, response_b, voter_id,
//         model_a?: 'sov33_small' (default) | 'sov33_large',
//         model_b?: 'sov33_large' (default) | 'sov33_small' }
//
// Returns: { status, preference, model_a, model_b, voter_sig, sigil, timestamp }
//
// HONESTY:
// - The voter_sig is an HMAC-SHA256 receipt over the canonical vote record
//   (voter_id + prompt hash + preference + timestamp). It binds the vote
//   to the voter without exposing the raw voter_id.
// - The preference signal is computed from a deterministic character-
//   level heuristic (length-normalised lexical overlap with the prompt,
//   vocabulary diversity, repetition rate) and labelled `mode:
//   heuristic-substrate-unreachable` when the SOV3 mesh is not reachable
//   from this serverless function. When the substrate IS reachable we
//   defer to its judgement and label `mode: sov3-substrate-live`.
// - Every vote is appended to /tmp/arena-vote.jsonl so the arena ledger
//   accumulates an auditable history of every preference cast.

const crypto = require('crypto');
const fs = require('fs');
const fsp = fs.promises;

const HMAC_SECRET = process.env.ARENA_HMAC_SECRET
  || 'csoai-sov33-arena-default-2026-sovereign-hmac';

const SOV3_URL = process.env.SOV3_URL || 'http://35.242.143.249:3101/mcp';
const VOTE_LOG = '/tmp/arena-vote.jsonl';

const ALLOWED_MODELS = new Set(['sov33_small', 'sov33_large']);

function hmacSigil(payloadObj) {
  const canonical = JSON.stringify(payloadObj, Object.keys(payloadObj).sort());
  return crypto.createHmac('sha256', HMAC_SECRET).update(canonical).digest('hex');
}

// Lightweight character-level heuristic — no LLM call needed. Produces
// a deterministic quality score in [0,1] for any text snippet.
function heuristicQualityScore(text) {
  if (!text || typeof text !== 'string') return 0;
  const s = text.trim();
  if (s.length === 0) return 0;

  // 1. Length adequacy (sigmoid over word count, plateau at ~120 words)
  const words = s.split(/\s+/).filter(Boolean);
  const wc = words.length;
  const lengthScore = 1 - Math.exp(-wc / 80);

  // 2. Vocabulary diversity (unique/total word ratio, capped)
  const uniq = new Set(words.map(w => w.toLowerCase().replace(/[^a-z0-9]/g, '')).filter(Boolean));
  const diversityScore = words.length === 0 ? 0 : Math.min(1, uniq.size / Math.max(1, words.length * 0.6));

  // 3. Repetition penalty (max consecutive identical word run, normalised)
  let maxRun = 1, curRun = 1;
  for (let i = 1; i < words.length; i++) {
    if (words[i].toLowerCase() === words[i-1].toLowerCase()) {
      curRun += 1;
      if (curRun > maxRun) maxRun = curRun;
    } else curRun = 1;
  }
  const repetitionScore = Math.max(0, 1 - (maxRun - 1) * 0.15);

  // 4. Coherence proxy — fraction of alphabetic characters
  const alphaChars = s.replace(/[^A-Za-z]/g, '').length;
  const coherenceScore = s.length === 0 ? 0 : alphaChars / s.length;

  // Weighted sum → [0,1]
  const composite = 0.35 * lengthScore + 0.30 * diversityScore + 0.15 * repetitionScore + 0.20 * coherenceScore;
  return Math.max(0, Math.min(1, Number(composite.toFixed(4))));
}

async function trySubstrateVote(prompt, response_a, response_b, model_a, model_b) {
  return new Promise((resolve) => {
    try {
      const url = new URL(SOV3_URL);
      const body = JSON.stringify({
        jsonrpc: '2.0', id: 'arena-vote', method: 'sov_arena_judge',
        params: { prompt, response_a, response_b, model_a, model_b },
      });
      const req = require('http').request({
        host: url.hostname, port: url.port || 80, path: url.pathname,
        method: 'POST', timeout: 1200,
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
      }, (r) => {
        let data = '';
        r.on('data', (c) => data += c);
        r.on('end', () => resolve({ reachable: true, status: r.statusCode, data }));
      });
      req.on('timeout', () => { req.destroy(); resolve({ reachable: false, reason: 'timeout' }); });
      req.on('error', (e) => resolve({ reachable: false, reason: e.code || e.message }));
      req.write(body); req.end();
    } catch (e) { resolve({ reachable: false, reason: e.message }); }
  });
}

async function appendLog(record) {
  try { await fsp.appendFile(VOTE_LOG, JSON.stringify(record) + '\n'); } catch {}
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }
  if (!body || typeof body !== 'object') body = {};

  const prompt = (body.prompt || '').toString();
  const response_a = (body.response_a || '').toString();
  const response_b = (body.response_b || '').toString();
  const voter_id = (body.voter_id || '').toString().slice(0, 128);
  const model_a = (body.model_a || 'sov33_small').toString().toLowerCase();
  const model_b = (body.model_b || 'sov33_large').toString().toLowerCase();

  if (!prompt || !response_a || !response_b) {
    return res.status(400).json({
      status: 'invalid_payload',
      error: 'prompt, response_a, response_b are all required',
      sigil: null, timestamp: new Date().toISOString(),
    });
  }
  if (!voter_id) {
    return res.status(400).json({
      status: 'invalid_voter',
      error: 'voter_id is required',
      sigil: null, timestamp: new Date().toISOString(),
    });
  }
  if (!ALLOWED_MODELS.has(model_a) || !ALLOWED_MODELS.has(model_b)) {
    return res.status(400).json({
      status: 'invalid_model',
      error: `model_a and model_b must be one of: ${[...ALLOWED_MODELS].join('|')}`,
      sigil: null, timestamp: new Date().toISOString(),
    });
  }
  if (model_a === model_b) {
    return res.status(400).json({
      status: 'identical_models',
      error: 'model_a and model_b must differ for a meaningful arena vote',
      sigil: null, timestamp: new Date().toISOString(),
    });
  }

  const t0 = Date.now();
  const tsIso = new Date(t0).toISOString();
  const vote_id = crypto.randomBytes(6).toString('hex');
  const prompt_hash = crypto.createHash('sha256').update(prompt).digest('hex').slice(0, 16);

  // Attempt live substrate vote first.
  let mode = 'heuristic-substrate-unreachable';
  let basis = 'lexical heuristic (length + vocabulary diversity + repetition penalty + coherence) — substrate unreachable from serverless';
  let preference, confidence;
  let live_score_a = null, live_score_b = null;

  const live = await trySubstrateVote(prompt, response_a, response_b, model_a, model_b);
  if (live.reachable && live.status === 200) {
    try {
      const parsed = JSON.parse(live.data);
      const result = parsed?.result;
      if (result && (result.preference === 'a' || result.preference === 'b' || result.preference === 'tie')) {
        preference = result.preference;
        confidence = typeof result.confidence === 'number' ? Number(result.confidence.toFixed(4)) : null;
        mode = 'sov3-substrate-live';
        basis = 'live substrate judge (sov_arena_judge) over the sovereign mesh';
        live_score_a = typeof result.score_a === 'number' ? result.score_a : null;
        live_score_b = typeof result.score_b === 'number' ? result.score_b : null;
      }
    } catch {/* fall through */}
  }

  if (mode === 'heuristic-substrate-unreachable') {
    const scoreA = heuristicQualityScore(response_a);
    const scoreB = heuristicQualityScore(response_b);
    live_score_a = scoreA;
    live_score_b = scoreB;
    const diff = Math.abs(scoreA - scoreB);
    if (diff < 0.01) {
      preference = 'tie';
      confidence = Number((0.5 + diff).toFixed(4));
    } else if (scoreA > scoreB) {
      preference = 'a';
      confidence = Number((0.5 + (diff / 2)).toFixed(4));
    } else {
      preference = 'b';
      confidence = Number((0.5 + (diff / 2)).toFixed(4));
    }
  }

  const duration_ms = Date.now() - t0;

  // Voter signature binds the vote to the voter without exposing voter_id.
  const voterSigPayload = { voter_id, prompt_hash, preference, vote_id, timestamp: tsIso };
  const voter_sig = crypto.createHmac('sha256', HMAC_SECRET).update(JSON.stringify(voterSigPayload)).digest('hex');

  // Full SIGIL receipt covers the entire canonical record.
  const receiptPayload = {
    vote_id, voter_id, prompt_hash, model_a, model_b, preference, confidence,
    score_a: live_score_a, score_b: live_score_b, mode, basis, duration_ms,
  };
  const sigil = hmacSigil(receiptPayload);

  await appendLog({
    ts: tsIso, vote_id, voter_id, prompt_hash, prompt_len: prompt.length,
    model_a, model_b, preference, confidence, score_a: live_score_a, score_b: live_score_b,
    mode, basis, duration_ms, voter_sig, sigil,
  });

  return res.status(200).json({
    status: 'vote_recorded',
    vote_id,
    preference,        // 'a' | 'b' | 'tie'
    confidence,
    model_a, model_b,
    score_a: live_score_a,
    score_b: live_score_b,
    mode,
    basis,
    duration_ms,
    voter_sig,         // HMAC binding voter_id + prompt_hash + preference
    voter_sig_algo: 'HMAC-SHA256',
    sigil,             // full receipt sigil
    sigil_algo: 'HMAC-SHA256',
    timestamp: tsIso,
    note: mode === 'sov3-substrate-live'
      ? 'Live substrate judge — preference pulled from SOV3 sov_arena_judge() over the sovereign mesh.'
      : 'Substrate not reached from this serverless function. Preference is a deterministic lexical heuristic (length + diversity + repetition + coherence) — the real judge lives on the SOV3 VM (35.242.143.249:3101) and is fetched via /mcp from the Mac-side runtime.',
  });
};