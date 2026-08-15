// Cloudflare Pages Function — /api/sov-openttd/state.jsonl
// GET — live SOV City / OpenTTD substrate state (STAGING, DESIGN-labelled).
//
// Source: the headless OpenTTD 15.3 dedicated server on oracle-micro-2
// (admin-port 4517), ticked every 60s by ~/sov-openttd/tick_loop.sh.
// A Mac-side sync cron (sync-sov-openttd-kv.sh) pushes /tmp/sov_openttd_state.jsonl
// into the SOV_OPENTTD_STATE KV namespace; this function serves the latest value.
//
// Honesty discipline (same as sov-town): if KV is empty or unbound, answer 503
// with a plain statement — a staging lab answers "no live state" rather than
// rendering a fabricated sim. Output carries "label":"DESIGN".

export async function onRequestGet({ env }) {
  if (!env.SOV_OPENTTD_STATE) {
    return new Response(
      JSON.stringify({
        error: 'no live state',
        detail: 'KV binding SOV_OPENTTD_STATE is not visible to this function (deployment config)',
        label: 'DESIGN',
      }),
      { status: 503, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } },
    );
  }
  const body = await env.SOV_OPENTTD_STATE.get('state.jsonl');
  if (!body) {
    return new Response(
      JSON.stringify({
        error: 'no live state',
        detail: 'KV bound but key state.jsonl is empty — the oracle tick has not synced yet',
        label: 'DESIGN',
      }),
      { status: 503, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } },
    );
  }
  return new Response(body, {
    headers: {
      'content-type': 'application/x-ndjson',
      'cache-control': 'public, max-age=60',
      'x-sov-openttd-source': 'oracle-micro-2 openttd-15.3 admin-port, 60s tick, DESIGN LAB',
    },
  });
}