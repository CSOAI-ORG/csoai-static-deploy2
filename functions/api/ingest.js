/**
 * /api/ingest — automatic trace-ingest hook (DESIGN -> working stub, labeled stub).
 *
 * Every OpenRouter / local-clan routing event should be captured, evaluated, and
 * appended to the signed proof chain. This endpoint accepts one event, signs it,
 * and appends to the SOVOS_CHAIN ledger (KV) if bound. It is a STUB labeled STUB:
 * the live hook (post-call → arena eval → append) lives behind the route layer.
 *
 *   POST {model, route, route_type:"openrouter"|"local-clan"|"eunomia", prompt, response_ref}
 *
 * Measurement, not certification. The signature asserts witness, never merit.
 */
import { getKey as getPinnedKey, bytesToHex } from './signlib.js';
let _k = null;
async function key(env) { if (!_k) _k = getPinnedKey(env); return _k; }
function canon(o) { if (o === null) return 'null'; if (o === true) return 'true'; if (o === false) return 'false'; if (typeof o === 'string') return JSON.stringify(o); if (typeof o === 'number') return Number.isFinite(o) ? String(o) : '0'; if (Array.isArray(o)) return '[' + o.map(canon).join(',') + ']'; if (typeof o === 'object') return '{' + Object.keys(o).sort().map(k => JSON.stringify(k) + ':' + canon(o[k])).join(',') + '}'; return 'null'; }
async function sha(s) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }
function b64(u) { let b = ''; u.forEach(x => b += String.fromCharCode(x)); return btoa(b); }
function h2b(h){return new Uint8Array((h.match(/.{2}/g)||[]).map(b=>parseInt(b,16)));}

export async function onRequest(context) {
  const h = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,POST,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers: h });
  if (context.request.method === 'GET') return new Response(JSON.stringify({ schema: 'csoai.trace-ingest/0.1', status: 'STUB', example: 'POST {"model":"qwen2.5:7b","route_type":"openrouter","prompt":"...","response_ref":"..."}', not_a_certification: true }), { status: 200, headers: h });
  if (context.request.method !== 'POST') return new Response(JSON.stringify({ error: 'POST only' }), { status: 405, headers: h });
  let b; try { b = await context.request.json(); } catch (e) { return new Response(JSON.stringify({ error: 'bad json' }), { status: 400, headers: h }); }
  const witnessed_at = new Date().toISOString();
  const claim = { schema: 'csoai.trace-ingest/0.1', record_type: 'measured-current-state', not_a_certification: true, endorsement: 'none', authored_by: 'did:web:csoai-gspc.pages.dev', basis: 'trace ingest hook (stub — labeled STUB)', witnessed_at, stub: true, event: { model: String(b.model || '?').slice(0, 60), route_type: String(b.route_type || 'eunomia').slice(0, 40), prompt_hash: await sha(String(b.prompt || '')), response_ref: String(b.response_ref || '').slice(0, 80) } };
  const content_id = await sha(canon(claim));
  const pair = await key(context.env);
  const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
  const pub = pair.rawPubHex ? h2b(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
  const card = { ...claim, content_id, signature: b64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
  if (pair.kid) { card.key_id = pair.kid; card.verification_method = pair.did + '#gspc'; card.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }
  // append to proof chain if SOVOS_CHAIN bound
  let chained = false;
  const kv = context.env && context.env.SOVOS_CHAIN;
  if (kv) { try { await kv.put('sovos-chain-head', card.content_id); await kv.put('card:' + card.content_id, JSON.stringify(card)); chained = true; } catch (e) {} }
  return new Response(JSON.stringify({ note: 'Trace-ingest STUB (labeled stub). Attach SOVOS_CHAIN KV for persistence. Verify at /api/verify. Measurement, not certification.', chained, card }), { status: 200, headers: h });
}
