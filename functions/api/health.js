// Cloudflare Pages Function — Health check
// GET /api/health

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
      project: 'csoai-static-deploy2',
      pages: parseInt(context.env?.PAGE_COUNT || '752', 10),
      phase: 100,
      sigil: 'tick-180',
      deployed: new Date().toISOString(),
    }),
    { status: 200, headers },
  );
}
