/**
 * /api/benchmark-quality — the signed register rating THIRD-PARTY benchmark quality.
 *
 * Deterministic predicates from public artifacts only — never an LLM judge.
 * Records are measured-current-state, Ed25519-signed, chained, offline-verifiable.
 * The impartiality firewall: CSOAI's own boards are NEVER scored here
 * (ISO/IEC 17020/17025 — a body must not assess its own work).
 *
 * Query params:
 *   (none)          → full feed summary
 *   ?benchmark=NAME → one record
 *   ?top=3          → highest-scoring records
 */
import feed from '../../benchmark-quality-feed.json';

const headers = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'access-control-allow-origin': '*',
};

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const name = url.searchParams.get('benchmark');
  const top = parseInt(url.searchParams.get('top') || '0', 10);

  if (name) {
    const rec = (feed.records || []).find(r => r.benchmark.toLowerCase() === name.toLowerCase());
    return new Response(JSON.stringify(rec || { error: 'no record for ' + name, records_available: (feed.records || []).map(r => r.benchmark) }), { status: 200, headers });
  }

  const summary = (feed.records || []).map(r => ({
    benchmark: r.benchmark,
    owner: r.owner,
    score: r.score,
    max_score: r.max_score,
    score_pct: r.score_pct,
    content_id: r.content_id,
    as_of: r.as_of,
  })).sort((a, b) => b.score - a.score);

  let out = {
    mode: 'benchmark-quality',
    doctrine: feed.doctrine,
    generated: feed.generated,
    max_score: feed.max_score,
    records: summary,
  };
  if (top > 0) out.top = summary.slice(0, top);
  return new Response(JSON.stringify(out), { status: 200, headers });
}
