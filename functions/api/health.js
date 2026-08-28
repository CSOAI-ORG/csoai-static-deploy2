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

  // Health must not freeze a tick/phase that drifts from reality (the "tick-180" /
  // "phase 100" / "pages 752" values were hardcoded and went stale). Everything
  // here derives live: deployed = now, board = the AUTHORITATIVE 22-axis count.
  let board = 'unreachable';
  try {
    const r = await fetch('https://councilof.ai/api/gspc', { headers: { accept: 'application/json' }, signal: AbortSignal.timeout(8000) });
    if (r.ok) {
      const d = await r.json();
      board = (d.totals && d.totals.public_count) || 'unknown';
    }
  } catch (e) { /* board stays 'unreachable' — honest */ }

  return new Response(
    JSON.stringify({
      status: 'ok',
      platform: 'cloudflare-pages',
      project: 'csoai-static-deploy2',
      board_public_count: board,
      deployed: new Date().toISOString(),
    }),
    { status: 200, headers },
  );
}
