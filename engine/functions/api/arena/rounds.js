// /api/arena/rounds — the live measured arena feed.
// KV first; if the binding serves a stale/pinned copy, fall back to the
// hourly-committed snapshot in the repo (raw.githubusercontent — live file,
// not the built copy). Honest either way: the header says which source served.
const RAW = "https://raw.githubusercontent.com/CSOAI-ORG/csoai-static-deploy2/main/public-data/arena-latest.jsonl";

export async function onRequestGet({ env }) {
  if (env.SOV_ARENA_STATE) {
    const body = await env.SOV_ARENA_STATE.get("rounds.jsonl", { cacheTtl: 60 });
    if (body) {
      // freshness guard: KV edge replicas can pin stale copies; if the last
      // round is older than 6h, fall through to the hourly git snapshot.
      try {
        const lastTs = JSON.parse(body.trim().split("\n").pop()).ts;
        if (Date.now() - new Date(lastTs).getTime() < 6 * 3600 * 1000) {
          return new Response(body, { headers: {
            "content-type": "application/x-ndjson", "cache-control": "public, max-age=60",
            "x-arena-source": "kv-live" } });
        }
      } catch (_) { /* fall through */ }
    }
  }
  try {
    const r = await fetch(RAW, { cf: { cacheTtl: 60 } });
    if (r.ok) {
      return new Response(await r.text(), { headers: {
        "content-type": "application/x-ndjson", "cache-control": "public, max-age=60",
        "x-arena-source": "git-hourly-snapshot" } });
    }
  } catch (_) {}
  return new Response(JSON.stringify({ error: "no live rounds", label: "DESIGN",
    detail: "arena feed sources unreachable — KV unbound and git snapshot missing" }),
    { status: 503, headers: { "content-type": "application/json", "cache-control": "no-store" } });
}
