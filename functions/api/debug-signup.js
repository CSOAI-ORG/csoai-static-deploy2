// Cloudflare Pages Function — converted from api/debug-signup.js
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




  if (request.method === 'GET') {
  return new Response(JSON.stringify({
  endpoint: 'debug',
  deployed_at: '2026-07-07',
  note: 'Inspect deployed signup.js by triggering an OPTIONS request and looking at logs'
  }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
  }

  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders });

  let body = await request.json();
  if (typeof body === 'string') {
  try { body = JSON.parse(body); } catch (e) { return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }); }
  }
  if (!body || typeof body !== 'object') body = {};

  // Echo what we received
  return new Response(JSON.stringify({
  received_keys: Object.keys(body),
  email: body.email,
  email_type: typeof body.email,
  email_stringified: String(body.email || ''),
  email_after_trim_lowercase: String(body.email || '').trim().toLowerCase(),
  email_includes_at: String(body.email || '').trim().toLowerCase().includes('@'),
  }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
}
