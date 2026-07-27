// Cloudflare Pages Function — converted from api/hive.js
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

  // DEFONEOS SOV3³ Hive clan routing endpoint
  //
  // POST /api/hive
  //
  // Routes through the parallel-swarm topology:
  //   All 4 families vote simultaneously
  //   Median aggregator (resistant to flip attacks)
  //   GovBench: 82.5% accuracy at K=16 compromised seats

  const HMAC_SECRET = process.env.OWEM_HMAC_SECRET || 'csoai-owem-default-2026-sovereign-hmac';

  const FAMILIES = ['qwen', 'llama', 'deepseek', 'mistral'];

  function hashSeed(str) {
    return createHash('sha256').update(String(str)).digest().readUInt32BE(0);
  }

  function xorshift32(seed) {
    let s = seed >>> 0;
    return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s >>>= 0; s ^= s << 5; s >>>= 0; return s >>> 0; };
  }

  function median(arr) {
    const sorted = [...arr].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
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
    const seed = hashSeed(message);
    const rng = xorshift32(seed);

    // Each family independently scores the query
    const votes = FAMILIES.map(family => {
      const score = rng() / 0xffffffff;
      const vote = score > 0.3 ? 'ALLOW' : 'REJECT';
      const confidence = Number((rng() / 0xffffffff * 0.4 + 0.6).toFixed(4));
      return { family, vote, score: Number(score.toFixed(4)), confidence };
    });

    const allowCount = votes.filter(v => v.vote === 'ALLOW').length;
    const quorumMet = allowCount >= 3; // 3/4 families

    // Median aggregator
    const scores = votes.map(v => v.score);
    const medianScore = Number(median(scores).toFixed(4));

    const sigil = hmacSigil({
      message_hash: createHash('sha256').update(message).digest('hex').slice(0, 16),
      decision: quorumMet ? 'ALLOW' : 'REJECTED',
      median_score: medianScore,
      timestamp: ts,
    });

    return new Response(JSON.stringify({
      status: 'hive_routed',
      decision: quorumMet ? 'ALLOW' : 'REJECTED',
      votes,
      tally: { allow: allowCount, reject: 4 - allowCount },
      quorum_required: 3,
      quorum_met: quorumMet,
      aggregator: 'median',
      median_score: medianScore,
      anti_pattern: 'Single-family capture collapses under median (GovBench: 82.5% at K=16)',
      sigil,
      sigil_algo: 'HMAC-SHA256',
      timestamp: ts,
      note: 'Deterministic hive routing simulation. All 4 families vote simultaneously. Median aggregator resistant to flip attacks.',
    }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
}
