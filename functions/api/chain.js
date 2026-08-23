/**
 * /api/chain — read the SOVOS engine-axis attestation ledger (persistent chain).
 *
 * Walks the signed chain backward from the head, returning each attestation's
 * content_id, sector, summary and prev link — the auditable, append-only ledger
 * the risk-oracle writes to. Requires the SOVOS_CHAIN KV binding; if absent it
 * returns a graceful message (a single-card chain from one manual card).
 *
 *   GET /api/chain?head=<content_id>&n=10
 *
 * Measurement, not certification. Every link is Ed25519-signed.
 */

const GENESIS_SCHEMA = 'csoai.engine-axis-attestation/0.1';

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS', 'access-control-allow-headers': 'Content-Type' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });

  const kv = context.env && context.env.SOVOS_CHAIN;
  const url = new URL(context.request.url);
  const head = url.searchParams.get('head');
  const n = Math.min(Math.max(parseInt(url.searchParams.get('n') || '10', 10) || 10, 1), 50);

  if (!kv) {
    return new Response(JSON.stringify({
      mode: 'chain',
      error: 'SOVOS_CHAIN KV binding not attached — attach b4eb1252766040d68bf6b10e6470ab57 to the csoai-gspc Pages project to persist the ledger.',
      not_a_certification: true,
    }), { status: 200, headers });
  }

  let cursor = head || (await kv.get('sovos-chain-head')) || null;
  if (!cursor) {
    return new Response(JSON.stringify({ mode: 'chain', error: 'empty chain — mint an attestation first', head: null, length: 0 }), { status: 200, headers });
  }

  const cards = [];
  let steps = 0;
  while (cursor && steps < n) {
    const card = await kv.get('card:' + cursor);
    if (!card) break;
    const c = JSON.parse(card);
    cards.push({
      content_id: c.content_id,
      sector: c.sector,
      subject: (c.object && c.object.subject) || '',
      composite: (c.risk && c.risk.composite) || 0,
      measured_axes: (c.risk && c.risk.measured_axes) || 0,
      prev: c.prev,
      witnessed_at: c.witnessed_at,
    });
    cursor = c.prev || null;
    steps++;
  }

  return new Response(JSON.stringify({
    mode: 'chain',
    head: head || (await kv.get('sovos-chain-head')),
    length: cards.length,
    cards,
    not_a_certification: true,
  }), { status: 200, headers });
}
