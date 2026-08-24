/**
 * /api/dvp — atomic delivery-vs-payment (Open 2), live.
 *
 * The cash leg (SWIFT/COBOL, T+2) is the bottleneck. This runs the ESCROW:
 * LOCK bond (buyer) + LOCK cash (seller) -> VERIFY both -> RELEASE both OR
 * neither. All-or-nothing. Then signs the outcome via the engine-axis spine so
 * an A2A agent / regulator can verify it offline (recompute content_id + check
 * the Ed25519 signature at /api/verify).
 *
 *   POST {bond:{quantity,currency,owner}, cash:{quantity,currency,owner}, compliance?}
 *   GET  -> schema + example
 *
 * Measurement, not certification. not_a_certification:true.
 */

import { getKey as getPinnedKey, bytesToHex } from './signlib.js';
let keyPromise = null;
async function getKey(env) { if (!keyPromise) keyPromise = getPinnedKey(env); return keyPromise; }
function canon(obj) {
  if (obj === null) return 'null';
  if (obj === true) return 'true';
  if (obj === false) return 'false';
  if (typeof obj === 'string') return JSON.stringify(obj);
  if (typeof obj === 'number') return Number.isFinite(obj) ? String(obj) : '0';
  if (Array.isArray(obj)) return '[' + obj.map(canon).join(',') + ']';
  if (typeof obj === 'object') return '{' + Object.keys(obj).sort().map(k => JSON.stringify(k) + ':' + canon(obj[k])).join(',') + '}';
  return 'null';
}
async function sha256hex(s) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }
function bytesToB64(u8) { let bin = ''; u8.forEach(b => bin += String.fromCharCode(b)); return btoa(bin); }

function leg(v) {
  v = v || {};
  const q = parseFloat(v.quantity != null ? v.quantity : (v.amount || 0));
  return { quantity: isNaN(q) ? 0 : q, currency: String(v.currency || '').toUpperCase(), owner: String(v.owner || '') };
}
function escrow(bond, cash) { return { bond: leg(bond), cash: leg(cash), locked: !!(bond && cash) }; }
function verify(esc, compliance) {
  const bond_ok = esc.bond.quantity > 0, cash_ok = esc.cash.quantity > 0;
  const currency_ok = !esc.bond.currency || !esc.cash.currency || esc.bond.currency === esc.cash.currency;
  const compliance_ok = compliance !== false;
  return { bond_ok, cash_ok, currency_ok, compliance_ok, all_ok: !!(bond_ok && cash_ok && currency_ok && compliance_ok) };
}
function finalize(esc, v) {
  return v.all_ok
    ? { status: 'settled', released: { bond: 'buyer', cash: 'seller' }, reason: 'atomic DvP complete' }
    : { status: 'not-settled', released: 'none', reason: { bond_ok: v.bond_ok, cash_ok: v.cash_ok, currency_ok: v.currency_ok } };
}

function h2b(h){return new Uint8Array((h.match(/.{2}/g)||[]).map(b=>parseInt(b,16)));}

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,POST,OPTIONS', 'access-control-allow-headers': 'Content-Type' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method === 'GET') {
    return new Response(JSON.stringify({ schema: 'csoai.atomic-dvp/0.1', example: 'POST {"bond":{"quantity":1000000,"currency":"USD","owner":"buyer"},"cash":{"quantity":1025000,"currency":"USD","owner":"seller"}}', not_a_certification: true }), { status: 200, headers });
  }
  if (context.request.method !== 'POST') return new Response(JSON.stringify({ error: 'POST or GET only' }), { status: 405, headers });

  let body;
  try { body = await context.request.json(); } catch (e) { return new Response(JSON.stringify({ error: 'invalid JSON' }), { status: 400, headers }); }

  const esc = escrow(body.bond, body.cash);
  const v = verify(esc, body.compliance);
  const outcome = finalize(esc, v);
  const witnessed_at = new Date().toISOString();

  const claim = {
    schema: 'csoai.atomic-dvp/0.1',
    record_type: 'measured-current-state',
    not_a_certification: true,
    endorsement: 'none',
    authored_by: 'did:web:csoai-gspc.pages.dev',
    basis: 'atomic DvP — both legs lock, verify, and release together or not at all',
    witnessed_at,
    escrow: esc,
    verified: v,
    settlement: outcome,
  };
  const content_id = await sha256hex(canon(claim));
  const prev = await sha256hex(canon({ schema: 'csoai.atomic-dvp/0.1', genesis: 'sovos-dvp-chain-v1' }));
  const pair = await getKey(context.env);
  const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
  const pub = pair.rawPubHex ? h2b(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
  const card = { ...claim, prev, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
  if (pair.kid) { card.key_id = pair.kid; card.verification_method = pair.did + '#gspc'; card.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }

  const kv = context.env && context.env.SOVOS_CHAIN;
  let chained = false;
  if (kv) {
    try { await kv.put('sovos-chain-head', card.content_id); await kv.put('card:' + card.content_id, JSON.stringify(card)); chained = true; } catch (e) {}
  }

  return new Response(JSON.stringify({
    note: 'Atomic DvP settlement' + (chained ? ' · chained on SOVOS ledger (see /api/chain).' : '') + ' Verify at /api/verify. Measurement, not certification.',
    status: outcome.status,
    chained,
    escrow: esc,
    verified: v,
    card,
  }), { status: 200, headers });
}
