/**
 * /api/verify — verify a signed record/feed/receipt against its embedded pubkey.
 *
 * The AG-UI "verify backbone" button. Takes a { signature, pubkey, content_id,
 * body } (or a full signed record) and verifies offline-consistent:
 *   recompute content_id = sha256(canonical body, RFC 8785)
 *   check Ed25519 signature over content_id with the pubkey.
 * Verification is free, loginless, and never an endorsement — measurement,
 * not certification.
 */

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
async function verifySig(sigB64, pubkeyHex, contentId) {
  const key = await crypto.subtle.importKey('raw', hexToBytes(pubkeyHex), { name: 'Ed25519' }, false, ['verify']);
  const sigBytes = Uint8Array.from(atob(sigB64), c => c.charCodeAt(0));
  return crypto.subtle.verify('Ed25519', key, sigBytes, new TextEncoder().encode(contentId));
}

const headers = { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', 'access-control-allow-origin': '*' };

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const contentId = url.searchParams.get('content_id') || url.searchParams.get('contentId');
  const sig = url.searchParams.get('signature');
  const pubkey = url.searchParams.get('pubkey');
  if (!contentId || !sig || !pubkey) {
    return new Response(JSON.stringify({ mode: 'verify', error: 'need content_id, signature, pubkey' }), { status: 400, headers });
  }
  try {
    const ok = await verifySig(sig, pubkey, contentId);
    return new Response(JSON.stringify({ mode: 'verify', content_id: contentId, valid: ok, not_a_certification: true, endorsement: 'none' }), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({ mode: 'verify', error: String(e).slice(0, 150) }), { status: 200, headers });
  }
}

export async function onRequestPost({ request }) {
  try {
    const body = await request.json();
    const r = body;
    // full signed record → verify content_id recompute + signature.
    // Strip every server/meta field that is NOT part of the canonical claim body
    // (incl. the JB-D1 pinned-key fields) so content_id recomputes identically.
    const fields = ['content_id', 'signature', 'prev', 'pubkey', 'key_id', 'verification_method', 'did_resolver'];
    const payload = {};
    for (const k of Object.keys(r)) if (!fields.includes(k)) payload[k] = r[k];
    const recomputed = await sha256hex(canon(payload));
    const cidMatch = recomputed === r.content_id;
    let sigOk = false;
    try { sigOk = await verifySig(r.signature, r.pubkey, r.content_id); } catch (e) { sigOk = false; }
    return new Response(JSON.stringify({ mode: 'verify', content_id: r.content_id, recomputed: recomputed, content_id_match: cidMatch, signature_valid: sigOk, valid: cidMatch && sigOk, not_a_certification: true, endorsement: 'none' }), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({ mode: 'verify', error: String(e).slice(0, 150) }), { status: 200, headers });
  }
}
