/**
 * /api/receipts/latest — honest settlement-receipt endpoint (CAT F3 / INT-14).
 *
 * Until the first real payment-settled artifact ↔ signed-measurement receipt
 * exists, this returns an honest UNPUBLISHED signed stub: the absence IS the
 * artifact. It is signed so even "there is nothing yet" is stranger-verifiable
 * (JL.5 — the index advertises what it has NOT measured as loudly as what it has).
 *
 *   GET /api/receipts/latest → signed UNPUBLISHED stub (never a fabricated receipt)
 *
 * Measurement, not certification. A receipt asserts what was bought, measured,
 * and witnessed — never a quality verdict.
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from '../signlib.js';

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers });

  try {
    const claim = {
      schema: 'csoai.settlement-receipt/0.1',
      record_type: 'unpublished-stub',
      not_a_certification: true,
      endorsement: 'none',
      authored_by: 'did:web:csoai-gspc.pages.dev',
      status: 'UNPUBLISHED',
      basis: 'no payment-settled artifact ↔ signed-measurement receipt exists yet (INT-14 gate)',
      witnessed_at: new Date().toISOString(),
      note: 'This endpoint stays honestly UNPUBLISHED until the first real settlement receipt lands. The honest zero IS the product (JL.5).',
    };
    const canonical = canon(claim);
    const content_id = await sha256hex(canonical);
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
