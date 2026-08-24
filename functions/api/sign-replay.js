/**
 * /api/sign-replay — sign an arbitrary game replay digest with the estate key.
 *
 * Cloudflare Pages Function → Web Crypto (crypto.subtle), no Node requires.
 * Ed25519 signatures are supported natively. The client sends its WebCrypto
 * SHA-256 digest of a finished game; we sign the digest + canonical claim so
 * the replay is cryptographically attributable.
 *
 * Language lock: measurement, not certification. The signature asserts
 * "this exact replay was witnessed at time T", never that the play was good.
 */

import { getKey as getPinnedKey } from './signlib.js';
let keyPromise = null;
async function getKey(env) {
  if (!keyPromise) {
    // Pinned did:web key (GSPC_SIGNER_PRIV) when present, ephemeral fallback otherwise.
    // The returned receipt carries the public key so any verifier can resolve the DID.
    keyPromise = getPinnedKey(env);
  }
  return keyPromise;
}

function canon(obj) {
  if (obj === null) return 'null';
  if (obj === true) return 'true';
  if (obj === false) return 'false';
  if (typeof obj === 'string') return JSON.stringify(obj);
  if (typeof obj === 'number') return Number.isFinite(obj) ? String(obj) : '0';
  if (Array.isArray(obj)) return '[' + obj.map(canon).join(',') + ']';
  if (typeof obj === 'object') {
    return '{' + Object.keys(obj).sort().map(k => JSON.stringify(k) + ':' + canon(obj[k])).join(',') + '}';
  }
  return 'null';
}
async function sha256hex(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
}
function hexToBytes(hex) {
  return new Uint8Array((hex.match(/.{2}/g) || []).map(b => parseInt(b, 16)));
}
function bytesToHex(u8) {
  return [...u8].map(b => b.toString(16).padStart(2, '0')).join('');
}
function bytesToB64(u8) {
  let bin = ''; u8.forEach(b => bin += String.fromCharCode(b));
  return btoa(bin);
}

function h2b(h){return new Uint8Array((h.match(/.{2}/g)||[]).map(b=>parseInt(b,16)));}

export async function onRequestPost({ request }) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*' };
  try {
    const body = await request.json();
    const digest = body.digest || body.content_id || null;
    if (!digest) return new Response(JSON.stringify({ error: 'no digest' }), { status: 400, headers });

    const claim = {
      schema: 'csoai.game-replay-receipt/0.1',
      record_type: 'measured-current-state',
      not_a_certification: true,
      endorsement: 'none',
      authored_by: 'did:web:csoai-gspc.pages.dev',
      witnessed_at: new Date().toISOString(),
      replay_sha256: digest,
    };
    const canonical = canon(claim);
    const content_id = await sha256hex(canonical);
    const pair = await getKey(context.env);
    const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
    const pub = pair.rawPubHex ? h2b(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
    const out = { ...claim, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
    if (pair.kid) { out.key_id = pair.kid; out.verification_method = pair.did + '#gspc'; out.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }
    return new Response(JSON.stringify(out), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e).slice(0, 150) }), { status: 500, headers });
  }
}
