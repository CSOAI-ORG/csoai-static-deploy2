export async function onRequestGet() {
  return new Response(JSON.stringify({ probe: "nested-function-alive", v: 1 }), {
    headers: { 'content-type': 'application/json' } });
}
