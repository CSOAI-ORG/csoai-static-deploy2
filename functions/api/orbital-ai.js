/**
 * /api/orbital-ai — orbital AI measured-current-state records.
 *
 * Coverage-extension of the signed measurement spine to in-orbit AI.
 * The core fact: every in-orbit AI result is self-reported; no standard
 * (ECSS/NASA/DO-178C) covers AI; no independent body measures on-board AI
 * behaviour. We record public claims + verifiable facts with deterministic
 * predicates. Never novel accusations. Measurement, not certification.
 */
import feed from '../../orbital-ai-record.json';

const headers = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'access-control-allow-origin': '*',
};

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const cls = url.searchParams.get('class'); // orbital-data-centre | orbital-computing-constellation | announced
  let records = feed.records || [];
  if (cls) records = records.filter(r => r.class === cls);
  return new Response(JSON.stringify({
    mode: 'orbital-ai',
    doctrine: feed.doctrine,
    gap: feed.gap,
    generated: feed.generated,
    total: records.length,
    records: records.map(r => ({
      subject: r.subject, class: r.class, deployed: r.deployed,
      claim: r.claim.slice(0, 160), orbit_km: r.orbit_km,
      predicates: r.predicates, content_id: r.content_id,
    })),
  }), { status: 200, headers });
}
