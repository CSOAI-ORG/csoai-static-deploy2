/**
 * /api/regulatory-deadline — the signed Regulatory Deadline Record.
 *
 * Regime-level process facts (Option 1 of the regulator brief): did each
 * tracked regulator hit the date it set itself? held / stated / deferred.
 * NEVER a ranked league table, never named officials (Derbyshire shield),
 * un-scored, self-benchmarked, Ed25519-signed, offline-verifiable.
 */
import feed from '../../regulatory-deadline-record.json';

const headers = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'access-control-allow-origin': '*',
};

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const status = url.searchParams.get('status'); // held | stated | deferred
  const celex = url.searchParams.get('celex');

  let records = feed.records || [];
  if (status) records = records.filter(r => r.deadline_status === status);
  if (celex) records = records.filter(r => r.celex === celex);

  return new Response(JSON.stringify({
    mode: 'regulatory-deadline',
    doctrine: feed.doctrine,
    generated: feed.generated,
    total: records.length,
    records: records.map(r => ({
      regime: r.regime, instrument: r.instrument, celex: r.celex,
      stated_deadline: r.stated_deadline, deadline_status: r.deadline_status,
      current_status: r.current_status, content_id: r.content_id,
    })),
  }), { status: 200, headers });
}
