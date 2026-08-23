export async function onRequestPost({ request, env }) {
  try {
    const body = await request.json();
    const id = 'lead-' + Date.now();
    await env.CSOAI_LEADS.put(id, JSON.stringify({
      ...body, ts: new Date().toISOString(),
      remark: 'Council of AI - attenstation-as-a-service lead'
    }));
    return new Response(JSON.stringify({ ok: true, id }), {
      headers: { 'content-type': 'application/json' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: String(e) }), {
      status: 500, headers: { 'content-type': 'application/json' }
    });
  }
}
