// Cloudflare Pages Function — /api/sov-town/state.jsonl
// GET — live SOV Town sim state (STAGING, DESIGN-labelled).
//
// Source: the MicropolisJ headless engine ticking on oracle-micro-2 every 5 min
// (cron every-5-min, sov_town_cron.sh). A Mac-side cron rsyncs state_live.jsonl
// and puts it into the SOV_TOWN_STATE KV namespace; this function serves the
// latest value.
//
// Honesty discipline (same as corpus-watch): if KV is empty or unbound, the
// function answers 503 with a plain statement — a staging lab page says "no
// live state" rather than rendering a fabricated city. The sim output itself
// carries "label":"DESIGN".
//
// Migrated 2026-08-08 from councilof-ai/functions/api/sov-town/state.jsonl.ts
// to the live apex repo (csoai-static-deploy2). The councilof-ai copy stays
// as the development source of truth.

export async function onRequestGet({ env }) {
  if (!env.SOV_TOWN_STATE) {
    return new Response(
      JSON.stringify({
        error: 'no live state',
        detail: 'KV binding SOV_TOWN_STATE is not visible to this function (deployment config)',
        label: 'DESIGN',
      }),
      { status: 503, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } },
    );
  }
  const body = await env.SOV_TOWN_STATE.get('state.jsonl');
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
      'x-sov-town-source': 'oracle-micro-2 micropolisj, 5-min tick, DESIGN LAB',
    },
  });
}
