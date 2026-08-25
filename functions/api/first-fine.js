/**
 * /api/first-fine — the First-Fine Watch as a signed, stranger-verifiable feed.
 *
 * The public-proof engine (J-D5 / EXE-259): enforcement facts rendered not as
 * static copy but as ONE signed, did:web-resolvable payload. A stranger resolves
 * did:web:csoai-gspc.pages.dev, recomputes content_id, verifies the Ed25519
 * signature — no trust in us. Every fine figure is a dated public-record fact,
 * never a verdict. Regulators free forever (R8).
 *
 *   GET /api/first-fine → signed watch feed
 *
 * Measurement, not certification. A fine number is EITHER a collected fact
 * (dated, sourced, an authority's determination) or an honest €0.
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from './signlib.js';

const FACTS = [
  { event: 'EU AI Act enforcement powers LIVE', date: '2026-08-02', scope: 'Art 101 up to €35M or 7% global turnover; Art 5(1)(da) prohibition; Art 50(2) marking grace opens', status: 'in-force' },
  { event: 'EU AI Act fines collected', date: '2026-08-02', amount: '€0', note: 'First-Fine Watch — enforcement Live 0 days; no fine collected yet. Honest zero, not a lack of power.', status: 'watch' },
  { event: 'Texas AI consumer-protection portal', date: '2026-09-01', scope: 'deployer reporting window', status: 'upcoming' },
  { event: 'DRCF response window', date: '2026-09-02', scope: 'Digital Regulators Cooperation Forum', status: 'upcoming' },
  { event: 'Art 50(2) marking grace ends', date: '2026-12-02', scope: 'prohibited-practice + marking obligations bite', status: 'upcoming' },
  { event: 'Korea AI Framework Act', date: '2027-01-22', scope: 'national AI law enters', status: 'upcoming' },
  { event: 'Illinois SB 315 audits', date: '2028-01-01', scope: 'automated-decision audits', status: 'upcoming' },
  { event: 'Clearview AI cumulative penalties', date: '2026', amount: '>€100M', note: 'cumulative across EU/UK orders; cited as field precedent', status: 'collected' },
  { event: 'OpenAI EU fine annulled', date: '2026-03', amount: '€15M', note: 'annulled in March — a correction is a new signed row, never a hidden edit', status: 'corrected' },
  { event: 'FTC consumer-protection record', date: '2026', amount: '~$85M', note: 'US federal action on deceptive claims', status: 'collected' },
];

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers });

  try {
    const claim = {
      schema: 'csoai.first-fine-watch/0.1',
      record_type: 'measured-current-state',
      not_a_certification: true,
      endorsement: 'none',
      authored_by: 'did:web:csoai-gspc.pages.dev',
      basis: 'systematic signed coverage of the public enforcement record — dated facts, an authority determines any violation, we only report the record',
      witnessed_at: new Date().toISOString(),
      grammar: 'a fine is either a dated collected fact or an honest €0; corrections are appended, never edited',
      facts: FACTS,
      first_fine: '€0 — the watch. Enforcement is live; the first fine is a dated record when it lands.',
    };
    const content_id = await sha256hex(canon(claim));
    const pair = await getKey(context.env);
    const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
    const pub = pair.rawPubHex ? hexToBytes(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
    const out = { ...claim, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
    if (pair.kid) { out.key_id = pair.kid; out.verification_method = pair.did + '#gspc'; out.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }
    return new Response(JSON.stringify(out), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e).slice(0, 150) }), { status: 500, headers });
  }
}
