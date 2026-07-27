// Cloudflare Pages Function — converted from api/cascade.js
import { createHash, createHmac, randomBytes } from 'crypto';

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  // DEFONEOS SOV3³ Cascade clan routing endpoint
  //
  // POST /api/cascade
  //
  // Routes through the 10/90 cascade topology:
  //   LEFT brain (small fast) handles 90% of traffic
  //   RIGHT brain (large deep) handles 10% escalations

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
    return createHmac('sha256', HMAC_SECRET).update(JSON.stringify(obj, Object.keys(obj).sort())).digest('hex');
  }
    corsHeaders['Cache-Control'] = 'no-store';
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders });
    if (request.method !== 'POST') return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

    let body = await request.json();
    if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
    if (!body || typeof body !== 'object') body = {};

    const message = (body.message ?? body.query ?? '').toString();
    if (!message.trim()) return new Response(JSON.stringify({ ok: false, error: 'message required' }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

    const ts = new Date().toISOString();
    const diff = estimateDifficulty(message);
    const escalated = diff.difficulty > DIFFICULTY_THRESHOLD;

    const sigil = hmacSigil({
      message_hash: createHash('sha256').update(message).digest('hex').slice(0, 16),
      decision: escalated ? 'RIGHT' : 'LEFT',
      difficulty: diff.difficulty,
      timestamp: ts,
    });

    return new Response(JSON.stringify({
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
    }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
}
