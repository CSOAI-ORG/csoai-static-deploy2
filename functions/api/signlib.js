/**
 * signlib.js — shared Ed25519 signing spine for csoai-gspc Functions.
 *
 * STRANGER-VERIFICATION (JB-D1) design:
 *   When the Pages secret GSPC_SIGNER_PRIV is present, we sign with ONE pinned
 *   Ed25519 key (stable across every invocation) whose public key is published
 *   at did:web:csoai-gspc.pages.dev (/.well-known/did.json). A stranger can
 *   then resolve the DID, check the key, recompute content_id, and verify the
 *   signature WITHOUT trusting us. That independent check is what turns a
 *   measurement into a signal instead of a claim.
 *
 *   When the secret is absent we fall back to an ephemeral per-invocation key
 *   (still signed, still self-consistent, but not did:web-pinnable). That keeps
 *   the demo layer honest and non-breaking in an unsealed environment.
 *
 * Language lock: measurement, not certification. A signature proves the card
 * was witnessed at time T by the pinned key — never that the subject is good.
 */

const DID = 'did:web:csoai-gspc.pages.dev';
const KID = DID + '#gspc';
// Public half of the pinned key (public by definition — safe to publish).
const PUB_RAW_HEX = '54bc68205ba96421e355cdf1c320827bf473c2b84bd5ed764c736204c548c78e';

let keyPromise = null;
export async function getKey(env) {
  if (!keyPromise) {
    // Pages Functions expose secrets via context.env; process.env is a local-dev
    // convenience only. Reading both keeps the pinned key working in prod.
    const secret =
      (env && env.GSPC_SIGNER_PRIV) ||
      (typeof process !== 'undefined' && process.env.GSPC_SIGNER_PRIV);
    if (secret) {
      keyPromise = importPinned(secret);
    } else {
      keyPromise = crypto.subtle.generateKey({ name: 'Ed25519' }, true, ['sign', 'verify']);
    }
  }
  return keyPromise;
}

async function importPinned(pkcs8Hex) {
  const pkcs8 = hexToBytes(pkcs8Hex);
  const privateKey = await crypto.subtle.importKey('pkcs8', pkcs8, { name: 'Ed25519' }, true, ['sign']);
  const pubRaw = hexToBytes(PUB_RAW_HEX);
  const pubKey = await crypto.subtle.importKey('raw', pubRaw, { name: 'Ed25519' }, true, ['verify']);
  return { privateKey, publicKey: pubKey, kid: KID, did: DID, rawPubHex: PUB_RAW_HEX, pinned: true };
}

export function canon(obj) {
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

export async function sha256hex(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
}

export function hexToBytes(hex) {
  return new Uint8Array((hex.match(/.{2}/g) || []).map(b => parseInt(b, 16)));
}

export function bytesToHex(u8) {
  return [...u8].map(b => b.toString(16).padStart(2, '0')).join('');
}

export function bytesToB64(u8) {
  let bin = ''; u8.forEach(b => bin += String.fromCharCode(b));
  return btoa(bin);
}

/**
 * Build a signed card for a claim + a digest. Returns the claim augmented with
 * content_id, signature, pubkey, and (when pinned) the did:web kid/did so a
 * verifier can resolve the key from the DID document.
 */
export async function signCard(claim, digest, env) {
  const pair = await getKey(env);
  const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(digest));
  const pub = pair.rawPubHex ? hexToBytes(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
  const out = { ...claim, content_id: digest, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
  if (pair.kid) {
    out.key_id = pair.kid;
    out.verification_method = pair.did + '#gspc';
    out.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json';
  }
  return out;
}
