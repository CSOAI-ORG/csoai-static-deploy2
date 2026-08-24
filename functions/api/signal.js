/**
 * /api/signal — SOV SIGNAL INDEX (the composed third output).
 *
 * Composes (does not fuse, does not add a claim):
 *   regulation_obligation  (live regulation: what the law requires + penalty)
 *   crosswalk_predicates   (east-west framework crosswalk map)
 *   measured_ai            (what models actually score, GSPC board)
 *   sim_evidence           (Council Space / arena round + clan trace)   [PARTIAL]
 *
 * Output: a divergence statement per axis/jurisdiction, Ed25519-signed.
 * "divergence stated, not certified."
 */
import regulationFeed from '../../regulation-feed.json';
import estateBoard from '../../estate-board.json';
import lookupData from '../../lookup-public.json';

import { getKey as getPinnedKey, bytesToHex } from './signlib.js';
let _k = null;
async function getKey(env) { if (!_k) _k = getPinnedKey(env); return _k; }
function canon(o) { if (o === null) return 'null'; if (o === true) return 'true'; if (o === false) return 'false'; if (typeof o === 'string') return JSON.stringify(o); if (typeof o === 'number') return Number.isFinite(o) ? String(o) : '0'; if (Array.isArray(o)) return '[' + o.map(canon).join(',') + ']'; if (typeof o === 'object') return '{' + Object.keys(o).sort().map(k => JSON.stringify(k) + ':' + canon(o[k])).join(',') + '}'; return 'null'; }
async function sha(s) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }
function b64(u) { let b = ''; u.forEach(x => b += String.fromCharCode(x)); return btoa(b); }

const PREDICATES = { 'eu-ai-act': ['ISO-42001-AIMS', 'NIST-AI-RMF-MAP'], 'dora': ['DORA-ICT', 'NIST-CSF'], 'fda': ['ISO-13485', 'MDR-2024'], 'fca': ['ISO-42001-AIMS', 'PSD2'], 'illinois': ['SB-315-AUDIT'], 'none': ['NIST-AI-RMF-GOVERN'] };
function h2b(h){return new Uint8Array((h.match(/.{2}/g)||[]).map(b=>parseInt(b,16)));}

export async function onRequest(context) {
  const h = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers: h });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers: h });
  try {
  const url = new URL(context.request.url);
  const axis = url.searchParams.get('axis') || 'gov';
  const jurisdiction = url.searchParams.get('jurisdiction') || 'EU';

  const regs = regulationFeed.regulations || [];
  const cells = estateBoard.cells || {};
  const models = Object.keys(cells);
  const perModel = models.map(m => {
    const axes = cells[m] || {}; const measured = Object.values(axes).filter(c => c.status === 'MEASURED' && c.accuracy != null);
    const behavior = measured.length ? measured.reduce((a, c) => a + c.accuracy, 0) / measured.length : 0;
    return { model: m, accuracy: Math.round(behavior * 1000) / 1000, n: measured.length };
  }).filter(m => m.n > 0).sort((a, b) => b.accuracy - a.accuracy);
  const leader = perModel[0] || null;
  const axisScore = leader ? leader.accuracy : null;

  // regulation obligation for this jurisdiction (the live-reg leg)
  const regFor = regs.find(r => String(r.celex || '').toUpperCase().includes(jurisdiction.toUpperCase())) || regs[0] || null;
  const key = (regFor && regFor.celex && regFor.celex.toLowerCase()) || 'none';
  const predicates = PREDICATES[key] || PREDICATES['none'];
  const divergence = axisScore != null ? Math.round((1 - axisScore) * 1000) / 1000 : null;

  const witnessed_at = new Date().toISOString();
  const claim = {
    schema: 'csoai.sov-signal-index/0.1',
    record_type: 'measured-current-state',
    not_a_certification: true,
    endorsement: 'none',
    authored_by: 'did:web:csoai-gspc.pages.dev',
    basis: 'composes regulation x crosswalk x measured-AI — computes only, adds no new claim',
    witnessed_at,
    axis, jurisdiction,
    regulation_obligation: regFor ? { regime: regFor.title || regFor.id, celex: regFor.celex, effective: regFor.date, status: regFor.status, penalty: regFor.penalty_exposure } : null,
    crosswalk_predicates: predicates,
    measured_ai: { leader: leader ? leader.model : null, accuracy: axisScore, models: perModel.length, separation: 'SEPARATED' },
    sim_evidence: { status: 'PARTIAL', note: 'Council Space sim leg not ingested as a fourth leg yet' },
    signal: divergence != null ? 'divergence stated, not certified' : 'unmeasured',
    divergence,
  };
  const content_id = await sha(canon(claim));
  const pair = await getKey(context.env);
  const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
  const pub = pair.rawPubHex ? h2b(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
  const card = { ...claim, content_id, signature: b64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
  if (pair.kid) { card.key_id = pair.kid; card.verification_method = pair.did + '#gspc'; card.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }
  return new Response(JSON.stringify({ summary: `SOV SIGNAL [${axis} / ${jurisdiction}] divergence ${divergence} · leader ${leader ? leader.model + ' ' + leader.accuracy : 'unmeasured'} · ${card.crosswalk_predicates.join(',')}`, card }), { status: 200, headers: h });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e).slice(0, 300) }), { status: 200, headers: h });
  }
}
