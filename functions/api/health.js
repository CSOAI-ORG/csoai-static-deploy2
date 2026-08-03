// Cloudflare Pages Function — Health check
// GET /api/health
// Honest liveness only: no invented page counts, phases, or tickers.

export async function onRequest(context) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };

  if (context.request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers });
  }

  return new Response(
    JSON.stringify({
      status: 'ok',
      platform: 'cloudflare-pages',
      project: 'csoai-org',
      timestamp: new Date().toISOString(),
      note: 'liveness check only — no usage or content metrics are reported here',
    }),
    { status: 200, headers },
  );
}
