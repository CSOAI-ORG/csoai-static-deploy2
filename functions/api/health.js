export async function onRequest(context) {
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
  if (context.request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }
  return new Response(JSON.stringify({
    status: 'ok',
    project: 'csoai-static-deploy2',
    pages: 752,
    phase: 100,
    sigil: 'tick-180',
    deployed: new Date().toISOString(),
  }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
}
