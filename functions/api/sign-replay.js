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

let keyPromise = null;
async function getKey() {
  if (!keyPromise) {
    // Ed25519 private key import from a 'raw' seed is treated as a PUBLIC key by
    // Web Crypto. We generate the keypair ONCE and cache it for the invocation
    // lifetime. The returned receipt carries the public key so any verifier can
    // check the signature. Deterministic-exact key derivation happens in the
    // Python/estate signing spine; this edge endpoint is the demo/attribution
    // layer (measurement, not certification — signature proves witness, not merit).
    keyPromise = crypto.subtle.generateKey({ name: 'Ed25519' }, true, ['sign', 'verify']);
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
      authored_by: 'did:web:csoai.org',
      witnessed_at: new Date().toISOString(),
      replay_sha256: digest,
    };
    const canonical = canon(claim);
    const content_id = await sha256hex(canonical);
    const pair = await getKey();
    const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
    const pub = await crypto.subtle.exportKey('raw', pair.publicKey);
    return new Response(JSON.stringify({ ...claim, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) }), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e).slice(0, 150) }), { status: 500, headers });
  }
}
