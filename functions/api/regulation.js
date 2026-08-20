/**
 * /api/regulation — the regulatory calendar as a machine-readable feed.
 *
 * The compounding move (empty-chair #2): a verified, cited, signed regulation feed,
 * quarterly re-verified, is the first estate product a relying party might actually
 * pay to depend on. Dates are corrected data — a wrong date becomes a published
 * correction (see /api/corrections), never a hidden edit.
 *
 * Query params:
 *   (none)          → full feed
 *   ?status=upcoming|in-force|positioning
 *   ?tag=us|eu|uk|demand-creating|correction
 *   ?from=YYYY-MM-DD  → only dates >= from
 *   ?count=5          → latest N by date
 */
import regs from '../../regulation-feed.json';

const headers = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'access-control-allow-origin': '*',
};

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const status = url.searchParams.get('status');
  const tag = url.searchParams.get('tag');
  const from = url.searchParams.get('from');
  const count = parseInt(url.searchParams.get('count') || '0', 10);

  let rows = regs.regulations;
  if (status) rows = rows.filter((r) => r.status === status);
  if (tag) rows = rows.filter((r) => (r.tags || []).includes(tag));
  if (from) rows = rows.filter((r) => r.date >= from);
  rows = rows.slice().sort((a, b) => a.date.localeCompare(b.date));
  if (count > 0) rows = rows.slice(-count);

  return new Response(JSON.stringify({
    schema: regs.schema,
    doctrine: regs.doctrine,
    generated: regs.generated,
    total: regs.regulations.length,
    returned: rows.length,
    regulations: rows,
  }), { status: 200, headers });
}
