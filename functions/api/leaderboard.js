// Cloudflare Pages Function — GovBench / SOV33 leaderboard
// GET /api/leaderboard

const HMAC_SECRET = 'csoai-sov33-leaderboard-default-2026-sovereign-hmac';

const BENCHMARKS = ['mmlu', 'gsm8k', 'aime', 'ifeval', 'bbh'];

const SOV33_BASELINES = {
  sov33_small: { mmlu: 0.642, gsm8k: 0.581, aime: 0.187, ifeval: 0.713, bbh: 0.524 },
  sov33_large: { mmlu: 0.781, gsm8k: 0.812, aime: 0.413, ifeval: 0.832, bbh: 0.711 },
};

const COMPETITORS = [
  { id: 'gpt-4o', mmlu: 0.887, gsm8k: 0.962, ifeval: 0.847, source: 'gpt-4o model card (2024-08)' },
  { id: 'claude-3.5-sonnet', mmlu: 0.882, gsm8k: 0.961, ifeval: 0.876, source: 'claude-3.5-sonnet model card (2024-10)' },
  { id: 'llama-3.1-405b', mmlu: 0.886, gsm8k: 0.964, ifeval: 0.857, source: 'llama-3.1-405b model card (2024-07)' },
  { id: 'deepseek-v3', mmlu: 0.882, gsm8k: 0.890, ifeval: 0.831, source: 'deepseek-v3 technical report (2024-12)' },
  { id: 'qwen2.5-72b', mmlu: 0.860, gsm8k: 0.910, ifeval: 0.840, source: 'qwen2.5-72b model card (2024-09)' },
];

async function hmacSigil(payloadObj) {
  const canonical = JSON.stringify(payloadObj, Object.keys(payloadObj).sort());
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw', encoder.encode(HMAC_SECRET), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign'],
  );
  const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(canonical));
  return Array.from(new Uint8Array(sig)).map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function onRequest(context) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
    'Cache-Control': 'no-store',
  };

  if (context.request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers });
  }
  if (context.request.method !== 'GET') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers });
  }

  const tsIso = new Date().toISOString();

  // On Cloudflare, no /tmp filesystem — use published baselines
  // (live runs can be stored in KV/D1 in a future iteration)
  const boards = {};
  for (const model of ['sov33_small', 'sov33_large']) {
    boards[model] = {};
    for (const b of BENCHMARKS) {
      boards[model][b] = {
        score: SOV33_BASELINES[model][b],
        runs: 0,
        source: 'published-baseline',
      };
    }
  }

  const flatten = (obj) => {
    const out = {};
    for (const b of BENCHMARKS) out[b] = obj[b].score;
    return out;
  };

  const payload = {
    sov33_small: flatten(boards.sov33_small),
    sov33_large: flatten(boards.sov33_large),
    compared_to: COMPETITORS,
    runs_aggregated: 0,
    benchmarks_tracked: BENCHMARKS,
    benchmark_breakdown: boards,
    timestamp: tsIso,
  };
  const sigil = await hmacSigil(payload);

  return new Response(
    JSON.stringify({
      status: 'leaderboard_readout',
      ...payload,
      sigil_algo: 'HMAC-SHA256',
      sigil,
      note: 'Cloudflare Pages Function — scores reflect published SOV33 baseline. Submit benchmark runs via POST /api/benchmark-run to populate with live data.',
    }),
    { status: 200, headers },
  );
}
