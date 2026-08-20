/**
 * /api/evidence — the insurer minimum product: signed per-agent evidence reports,
 * queryable. Underwriting evidence, never underwriting. We measure and sign what
 * the agent did; we never underwrite, never advise on premium, never name insurers
 * on the public surface (FCA Art 33B-safe).
 *
 * Query params:
 *   ?agent=qwen2.5:7b  → one agent's report
 *   ?axis=gov          → filter cells by axis
 *   (none)             → all reports (the feed)
 */
import reports from '../../evidence-reports.json';

const headers = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'access-control-allow-origin': '*',
};

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const agent = url.searchParams.get('agent');
  const axis = url.searchParams.get('axis');

  let rows = reports.reports;
  if (agent) rows = rows.filter((r) => r.agent.toLowerCase() === agent.toLowerCase());
  if (axis) {
    rows = rows.map((r) => ({ ...r, cells: r.cells.filter((c) => c.axis === axis) }))
      .filter((r) => r.cells.length);
  }

  return new Response(JSON.stringify({
    schema: reports.schema,
    doctrine: reports.doctrine,
    generated: reports.generated,
    total: reports.reports.length,
    returned: rows.length,
    reports: rows,
  }), { status: 200, headers });
}
