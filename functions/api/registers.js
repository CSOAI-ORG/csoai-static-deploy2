/**
 * /api/registers — the estate's signed register rollup (CAT F6 close).
 *
 * Serves the register counts as ONE signed, did:web-resolvable payload so a
 * stranger can recompute content_id and verify the Ed25519 signature without
 * trusting us. Register counts are claims about N signed artifacts; they render
 * only as counts, each backed by the /api/chain ledger for per-row proof.
 *
 *   GET /api/registers  → { schema, generated, doctrine, registers, content_id,
 *                           signature, pubkey, key_id, verification_method }
 *
 * Measurement, not certification. Every register count is a N-computed claim,
 * never a verdict. Ground truth for per-row proof is /api/chain.
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from './signlib.js';

const REGISTER_DATA = {
  schema: 'csoai.registers/0.1',
  generated: '2026-08-22T09:40:00Z',
  doctrine: 'Signed registers, Ed25519, measured-current-state, never certified. Measurement, not certification.',
  registers: {
    benchmark: 5,
    'regulator-deadlines': 14,
    'regulator-clarity': 12,
    'orbital-ai': 6,
    'platform-artifacts': 24,
    documentation: 7,
    'embodied-transparency': 14,
    'estate-board': 11,
    'arena-duels': 3052,
    'chain-cards': 3500,
  },
};

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers });

  try {
    const claim = {
      schema: REGISTER_DATA.schema,
      record_type: 'measured-current-state',
      not_a_certification: true,
      endorsement: 'none',
      authored_by: 'did:web:csoai-gspc.pages.dev',
      basis: 'register rollup — counts are N-computed claims, per-row proof is /api/chain',
      generated: REGISTER_DATA.generated,
      doctrine: REGISTER_DATA.doctrine,
      registers: REGISTER_DATA.registers,
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
