/**
 * /api/receipts — signed agent-payment settlement receipts (AXIS-27 / INT-14).
 *
 * Honest framing is load-bearing here. A receipt asserts WHAT was settled, for
 * how much, with whom, on what rail, at what time — sworn by a signer. It is
 * NEVER "we earned $X": the receiver is a counter-party wallet, not CSOAI
 * revenue. We measure + sign the settlement event; we do not book it.
 *
 *   GET /api/receipts → { receipts:[...], honest_note }
 *
 * Measurement, not certification. R8: regulators + anything ranked free forever;
 * this is the machine-rail index feed (commercial data, never a score).
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from './signlib.js';

// The settled money-in receipt recorded by the fleet (verified VALID, from the
// evidence tree on feat/sandbox-arena-seam). Destination: a counter-party wallet.
const RECEIPTS = [
  {
    card_id: 'card-csoai-revenue-001',
    spec: 'csoai-x402-receipt-0.1',
    kind: 'measurement-card',
    network: 'base',
    asset: 'USDC',
    amount_units: 5000000,
    fee_bps: 100,
    receiver: '0x212686404A7D1E1fD88F35eD6200c3aF7A78ae31',
    signer: 'sov33-owem-micro',
    ts: '2026-08-25T03:44:25Z',
    verify: 'VALID',
    verify_url: 'https://csoai-verify.pages.dev/verify',
    // Honest reading, not a revenue claim:
    reading: 'signed measured settlement event — the machine-rail moves money, the receipt is stranger-verifiable. The receiver is a counter-party wallet, not a CSOAI revenue figure.',
  },
];

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers });

  try {
    const claim = {
      schema: 'csoai.settlement-receipts/0.1',
      record_type: 'measured-current-state',
      not_a_certification: true,
      endorsement: 'none',
      authored_by: 'did:web:csoai-gspc.pages.dev',
      basis: 'agent-payment settlement receipts measured + signed on the machine rail (x402/Base)',
      honest_note: 'A receipt asserts what settled, with whom, and at what time. It is never a revenue claim: the receiver is a counter-party wallet. We measure + sign the event; the authority/insurer decides what it means.',
      witnessed_at: new Date().toISOString(),
      receipts: RECEIPTS,
      count: RECEIPTS.length,
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
