// /api/arena/rounds.jsonl — the clean alias of the live arena evidence feed.
// Same KV source as the legacy path; this is the canonical public URL going forward.
export async function onRequestGet({ env }) {
  if (!env.SOV_ARENA_STATE) {
    return new Response(JSON.stringify({ error: 'no live rounds', label: 'DESIGN',
      detail: 'KV binding SOV_ARENA_STATE not visible to this function' }),
      { status: 503, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
  }
  const body = await env.SOV_ARENA_STATE.get('rounds.jsonl', { cacheTtl: 60 });
  if (!body) {
    return new Response(JSON.stringify({ error: 'no live rounds', label: 'DESIGN',
      detail: 'KV bound but empty — the fleet arena has not synced yet' }),
      { status: 503, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
  }
  return new Response(body, {
    headers: { 'content-type': 'application/x-ndjson', 'cache-control': 'public, max-age=30',
               'x-arena-source': 'fleet arena (oracle) — every round real' },
  });
}
