// Cloudflare Pages Function — SOV measured results readout
// GET /api/leaderboard
//
// Register law: measurement/attestation language only. Every figure below is
// from a completed, archived run with a published harness. Benchmarks we have
// not run are listed as not-measured, never estimated.

const HMAC_SECRET = 'csoai-Council-leaderboard-default-2026-neutral-hmac';

// ─── Measured: official-format lm-eval-harness runs (2026-08-03, validated) ──
// Validated lane: lm_eval --model hf + GGUF (transformers 4.44), full splits,
// after the 2026-08-03 llama-server lane invalidation (disclosed: HF
// csoai/lmeval-official-format INVALIDATED.md). Near-random on general-
// knowledge MC is the specialization profile of a governance-tuned model —
// disclosed, not hidden, and now measured through a validated instrument.
const OFFICIAL_FORMAT = {
  model: 'csoai/Council-unified',
  harness: 'lm-eval-harness 0.4.12 (official format, reproducible; hf+GGUF validated lane)',
  results: {
    arc_easy: { acc: 0.2534, ci95: 0.0089, n: 'full split' },
    arc_challenge: { acc: 0.221, ci95: 0.0121, n: 'full split' },
    hellaswag: { acc: 0.259, ci95: 0.0044, n: 'full split' },
  },
  note: 'General-knowledge trivia is not the target domain; see frozen_split_governance for the measured specialization. Prior llama-server numbers quarantined 2026-08-03 as instrument fault.',
};

// ─── Measured: frozen-split governance battery (2026-08-02) ─────────────────
// 170 held-out scenarios, BCa n=2000. Harness + raw logs:
// HF dataset csoai/aiact-frozen-split-harness. DOI 10.5281/zenodo.21755656.
const FROZEN_SPLIT = {
  harness: 'aiact-frozen-split-harness (published, recomputable)',
  n_scenarios: 170,
  results: [
    { id: 'grok-4.5', score: 0.368, ci95: [0.331, 0.408] },
    { id: 'opus-4.1', score: 0.323, ci95: null },
    { id: 'Council-unified', score: 0.2508, ci95: [0.221, 0.283], note: 'identical-170 re-run 2026-08-03; statistical tie with sonnet-4.5 and gpt-5 on governance scenarios' },
    { id: 'sonnet-4.5', score: 0.243, ci95: null },
    { id: 'gpt-5', score: 0.243, ci95: null },
    { id: 'llama-4-maverick', score: 0.220, ci95: null },
    { id: 'gemini-2.5-pro', score: 0.217, ci95: null },
    { id: 'mistral-large', score: 0.209, ci95: null },
    { id: 'qwen3-235b', score: 0.199, ci95: null },
    { id: 'sov34-1.5b-lora', score: 0.1975, ci95: [0.169, 0.226], note: 'dual-gate candidate 2026-08-03: generality gate PASS (arc_easy 0.7504, matches own base), frozen-split gate FAIL vs 0.2508 — no successor claims; published with failures included' },
    { id: 'qwen2.5-1.5b-base', score: 0.1767, ci95: [0.151, 0.205], note: 'control: sov34 base weights' },
  ],
  excluded: [
    { id: 'deepseek-v3.2', reason: '94/170 unparseable under strict parser — instrument/format fault, score withheld rather than folded in as zero' },
    { id: 'kimi-k2.6', reason: 'instrument fault: thinking-only responses exhausted token budget (142/170 empty) — excluded, not scored' },
  ],
};

// ─── Measured: GovBench 15-dimension composite (2026-07-28) ─────────────────
const GOVBENCH_15D = {
  dimensions: 15,
  note: 'score_band is a descriptive range of the measured composite — measurement, not certification. Scores from other dimension counts are not comparable.',
  results: [
    { id: 'Council-dist-c3', composite: 57.0, score_band: 'bronze' },
    { id: 'Council-evolved', composite: 57.0, score_band: 'bronze' },
    { id: 'Council-dist-c2', composite: 54.6, score_band: 'bronze' },
    { id: 'Council-dist-c1', composite: 49.2, score_band: 'below band threshold' },
    { id: 'qwen2.5-0.5b', composite: 43.3, score_band: 'below band threshold' },
    { id: 'neutral-v4', composite: 42.9, score_band: 'below band threshold' },
  ],
};

// ─── Not measured — listed so absence is explicit, never implied ────────────
const NOT_MEASURED = ['mmlu', 'gsm8k', 'aime', 'ifeval', 'bbh'];

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

  const payload = {
    register: 'measurement_attestation_only',
    official_format_lm_eval: OFFICIAL_FORMAT,
    frozen_split_governance: FROZEN_SPLIT,
    govbench_15d_composite: GOVBENCH_15D,
    not_measured: NOT_MEASURED,
    artifacts: {
      harness_dataset: 'https://huggingface.co/datasets/csoai/aiact-frozen-split-harness',
      model: 'https://huggingface.co/csoai/Council-unified',
      doi: '10.5281/zenodo.21755656',
    },
    timestamp: new Date().toISOString(),
  };
  const sigil = await hmacSigil(payload);

  return new Response(
    JSON.stringify({
      status: 'measured_results_readout',
      ...payload,
      sigil_algo: 'HMAC-SHA256',
      sigil,
      note: 'Every score above is from a completed archived run with a published harness. Unmeasured benchmarks are listed explicitly and never estimated.',
    }),
    { status: 200, headers },
  );
}
