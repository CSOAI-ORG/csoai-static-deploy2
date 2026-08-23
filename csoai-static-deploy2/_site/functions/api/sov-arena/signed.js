// Cloudflare Pages Function — /api/sov-arena/signed.jsonl
// GET — returns the signed_card ledger from /signed_rounds.jsonl
//
// Source: spine_v2.py signs every arena-round and writes to signed_rounds.jsonl
// (committed to the repo). This function serves the file directly.
// External verifiers can recompute any card's CID and check the Ed25519 sig.

export async function onRequestGet({ env }) {
  // Try KV first (live feed from Mac cron sync)
  if (env.SOV_SIGNED_CARDS) {
    const body = await env.SOV_SIGNED_CARDS.get('latest.jsonl');
    if (body) {
      return new Response(body, {
        status: 200,
        headers: { 'content-type': 'application/x-ndjson', 'cache-control': 'no-store' },
      });
    }
  }
  // Fallback: serve the static file shipped with the deploy
  // The wrangler static assets include /api/sov-arena/signed.jsonl
  return new Response(JSON.stringify({
    error: 'no signed cards yet',
    detail: 'SOV_SIGNED_CARDS KV not bound AND no static fallback. Run the spine-mcp signing pipeline first.',
    label: 'DESIGN',
  }), {
    status: 503,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });
}
