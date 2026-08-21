export async function onRequestGet({ env }) {
  const v = env.SOV_ARENA_STATE ? await env.SOV_ARENA_STATE.get("fresh-test-key") : "NO_BINDING";
  return new Response(JSON.stringify({ freshKey: v }), { headers: { "content-type": "application/json" } });
}
