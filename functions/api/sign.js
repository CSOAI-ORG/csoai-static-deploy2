/**
 * /api/sign — sign an arbitrary replay/statement digest with the estate key.
 *
 * Stranger-verification (JB-D1): when the Pages secret GSPC_SIGNER_PRIV is
 * present we sign with ONE pinned Ed25519 key whose public half is published at
 * did:web:csoai-gspc.pages.dev (/.well-known/did.json). A stranger can resolve
 * the DID, match the key, recompute content_id, and verify without trusting us.
 * Without the secret we fall back to an ephemeral per-invocation key (signed,
 * self-consistent, but not did:web-pinnable).
 *
 * Language lock: measurement, not certification. The signature asserts "this
 * exact replay was witnessed at time T by the pinned key", never that it was good.
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from './signlib.js';

export async function onRequestPost({ request, env }) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*' };
  try {
    const body = await request.json();
    const digest = body.digest || body.content_id || null;
    if (!digest) return new Response(JSON.stringify({ error: 'no digest' }), { status: 400, headers });

    const claim = {
      schema: 'csoai.signed-statement/0.1',
      record_type: 'measured-current-state',
      not_a_certification: true,
      endorsement: 'none',
      authored_by: 'did:web:csoai-gspc.pages.dev',
      witnessed_at: new Date().toISOString(),
      replay_sha256: digest,
    };
    const canonical = canon(claim);
    const content_id = await sha256hex(canonical);
    const pair = await getKey(env);
    const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
    const pub = pair.rawPubHex ? hexToBytes(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
    const out = { ...claim, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
    if (pair.kid) { out.key_id = pair.kid; out.verification_method = pair.did + '#gspc'; out.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }
    return new Response(JSON.stringify(out), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e).slice(0, 150) }), { status: 500, headers });
  }
}
