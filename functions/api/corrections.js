/**
 * /api/corrections — the corrections ledger as a machine-readable feed.
 *
 * The compounding move: a body that publishes the number AND publishes when the
 * number was wrong is the only kind a relying party can depend on. This feed is
 * the honesty gate turned into a citation surface — append-only, each entry with
 * what was wrong / how it was caught / the fix / status / evidence.
 *
 * Language lock: measurement, not certification. Corrections are assets, not
 * admissions. A wrong date here becomes a published correction, never a hidden edit.
 *
 * Query params:
 *   (none)         → full feed (this file's seed + generated entries)
 *   ?status=open   → only open items
 *   ?axis=care     → filter by axis/tag
 *   ?count=5       → latest N
 */
import corrections from '../../corrections-feed.json';

const headers = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'access-control-allow-origin': '*',
};

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const status = url.searchParams.get('status');
  const axis = url.searchParams.get('axis');
  const count = parseInt(url.searchParams.get('count') || '0', 10);

  let rows = corrections.corrections;
  if (status) rows = rows.filter((c) => (c.status || '').toLowerCase() === status.toLowerCase());
  if (axis) rows = rows.filter((c) => (c.tags || []).some((t) => t.toLowerCase() === axis.toLowerCase()));
  if (count > 0) rows = rows.slice(-count);

  return new Response(JSON.stringify({
    schema: 'csoai.corrections-feed/0.1',
    note: corrections.note,
    doctrine: corrections.doctrine,
    total: corrections.corrections.length,
    returned: rows.length,
    corrections: rows,
  }, null, 0), { status: 200, headers });
}
