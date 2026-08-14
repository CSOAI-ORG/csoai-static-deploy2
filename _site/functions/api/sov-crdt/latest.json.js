// Cloudflare Pages Function — /api/sov-crdt/latest.json
// GET — latest cross-micro convergence digest (CRDT).
//
// Source: the Mac-side CRDT heartbeat observer (sov_crdt_heartbeat.py) records
// per-cycle convergence of the two Oracle micros (independently computed Merkle
// digests over replicated honey + all three CRDT axioms). sync-sov-crdt-kv.sh
// pushes the latest record to the SOV_CRDT_STATE KV namespace; this serves it.
//
// Honesty discipline: 503 + plain statement on empty/unbound. The digest
// carries overall + merkle_match so a consumer can show "converged / diverged".

export async function onRequestGet({ env }) {
  if (!env.SOV_CRDT_STATE) {
    return new Response(
      JSON.stringify({
        error: 'no convergence digest',
        detail: 'KV binding SOV_CRDT_STATE is not visible to this function',
        label: 'DESIGN',
      }),
      { status: 503, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } },
    );
  }
  const body = await env.SOV_CRDT_STATE.get('latest.json');
  if (!body) {
    return new Response(
      JSON.stringify({
        error: 'no convergence digest',
        detail: 'KV bound but key latest.json empty — the CRDT heartbeat has not synced yet',
        label: 'DESIGN',
      }),
      { status: 503, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } },
    );
  }
  return new Response(body, {
    headers: {
      'content-type': 'application/json',
      'cache-control': 'public, max-age=30',
      'x-sov-crdt-source': 'mac observer + oracle-micro/micro-2, DESIGN LAB',
    },
  });
}