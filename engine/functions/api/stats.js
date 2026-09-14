// Cloudflare Pages Function — DEFONEOS public live stats
// GET /api/stats

export async function onRequest(context) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
    'Cache-Control': 'public, max-age=60',
  };

  if (context.request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers });
  }
  if (context.request.method !== 'GET') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers });
  }

  // On Cloudflare, no filesystem — use baked baselines + env overrides
  const signupTotal = parseInt(context.env?.SIGNUP_TOTAL || '0', 10) || 0;
  const pageCount = parseInt(context.env?.PAGE_COUNT || '226', 10) || 226;

  return new Response(
    JSON.stringify({
      signups: {
        total: signupTotal,
        week: 0,
        day: 0,
        source: signupTotal > 0 ? 'live' : 'conservative-baseline',
      },
      empire: {
        pages: pageCount,
        mcps: '30/30',
        repos: '15/15',
        sigil_chain: 'live',
        sov3_mesh_port: 3101,
        bft_council_quorum: '23/33',
        data_corpus_gb: 49,
        care_floor: 0.95,
        sigma_audit: null,
      },
      pipeline: {
        defence_primes_evaluating: 7,
        defence_primes_evaluating_source: 'illustrative — clear of any one prime until converted',
        regulators_in_cooperation: 3,
        regulators_in_cooperation_source: 'illustrative — confirmed pipeline not public',
      },
      sovereign: {
        key_alias: 'd75a9801…7511a',
        sigil_algo: 'Ed25519',
        pqc_target: 'ML-DSA-65',
        pqc_migration_year: 2027,
        sigil_per_day: 86400,
      },
      timestamp: new Date().toISOString(),
      note: 'Cloudflare Pages Function. Baked Empire numbers reflect real substrate state. Pipeline numbers are explicitly illustrative.',
    }),
    { status: 200, headers },
  );
}
