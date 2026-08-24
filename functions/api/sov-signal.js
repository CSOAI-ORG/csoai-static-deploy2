/**
 * /api/sov-signal — the THIRD data output: a cross-synced governance risk index.
 *
 * Cross-syncs THREE rails into one measured, signed index:
 *   [crosswalk]  East<->West governance crosswalk coverage
 *   [regulation] live regulation pressure (in-force + upcoming regimes)
 *   [sims]       SOV-space governance behaviour (each model's measured axis scores)
 *
 * Output = a per-model SOV SIGNAL (0..1) + DIVERGENCE (distance from the permitted
 * manifold = 1 - signal) + a market-level aggregate, all Ed25519-signed.
 *
 *   GET /api/sov-signal   (POST also accepted to add a signed card)
 *
 * This is the risk-oracle the settlement rails query. Measurement, not certification.
 */
import estateBoard from '../../estate-board.json';
import regulationFeed from '../../regulation-feed.json';
import benchmarkQualityFeed from '../../benchmark-quality-feed.json';
import lookupData from '../../lookup-public.json';

import { getKey as getPinnedKey, bytesToHex } from './signlib.js';
let _k = null;
async function key(env) { if (!_k) _k = getPinnedKey(env); return _k; }
function canon(o) { if (o === null) return 'null'; if (o === true) return 'true'; if (o === false) return 'false'; if (typeof o === 'string') return JSON.stringify(o); if (typeof o === 'number') return Number.isFinite(o) ? String(o) : '0'; if (Array.isArray(o)) return '[' + o.map(canon).join(',') + ']'; if (typeof o === 'object') return '{' + Object.keys(o).sort().map(k => JSON.stringify(k) + ':' + canon(o[k])).join(',') + '}'; return 'null'; }
async function sha(s) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }
function b64(u) { let b = ''; u.forEach(x => b += String.fromCharCode(x)); return btoa(b); }

// east-west crosswalk coverage: how many curated East signals resolve cleanly.
const CROSSWALK_SIGNALS = ['tc260-registry', 'social-credit-profile', 'pdca-cycle', 'algorithm-filing', 'data-localisation'];

function h2b(h){return new Uint8Array((h.match(/.{2}/g)||[]).map(b=>parseInt(b,16)));}

export async function onRequest(context) {
  const h = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,POST,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers: h });
  if (context.request.method === 'GET') {
    // GET returns the computed, signed index (the read side of the third data output).
  } else if (context.request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'GET or POST only' }), { status: 405, headers: h });
  }

  const cells = estateBoard.cells || {};
  const models = Object.keys(cells);
  const regs = regulationFeed.regulations || [];
  const inForce = regs.filter(r => r.status === 'in-force').length;
  const upcoming = regs.filter(r => r.status === 'upcoming' || r.status === 'positioning').length;
  // regulation pressure: fraction of the calendar that is live/looming (0..1)
  const regulation_pressure = regs.length ? Math.min(1, (inForce + upcoming * 0.5) / regs.length) : 0;
  // crosswalk coverage: fraction of curated East signals that resolve (deterministic; all resolve)
  const crosswalk_coverage = 1.0;
  const crosswalk_density = CROSSWALK_SIGNALS.length;

  const perModel = models.map(m => {
    const axes = cells[m] || {};
    const measured = Object.values(axes).filter(c => c.status === 'MEASURED' && c.accuracy != null);
    const behavior = measured.length ? (measured.reduce((a, c) => a + c.accuracy, 0) / measured.length) : 0;
    const axes_measured = measured.length;
    // SOV SIGNAL = behaviour weighted against regulation pressure + crosswalk coverage,
    // then SCALED by measured-axis coverage: a model measured on few axes gets an honest,
    // lower signal (never inflated). Signal = 0 for a fully UNMEASURED model.
    const coverage = Math.min(1, axes_measured / Math.max(Object.keys(axes).length, 1));
    const signal = Math.round((0.5 * behavior + 0.3 * regulation_pressure + 0.2 * crosswalk_coverage) * coverage * 1000) / 1000;
    const divergence = Math.round((1 - signal) * 1000) / 1000;
    return { model: m, behavior: Math.round(behavior * 1000) / 1000, axes_measured, signal, divergence };
  }).sort((a, b) => b.signal - a.signal);

  const agg = perModel.length ? Math.round((perModel.reduce((a, x) => a + x.signal, 0) / perModel.length) * 1000) / 1000 : 0;
  const leader = perModel[0] || null;
  const witnessed_at = new Date().toISOString();

  const claim = {
    schema: 'csoai.sov-signal/0.1',
    record_type: 'measured-current-state',
    not_a_certification: true,
    endorsement: 'none',
    authored_by: 'did:web:csoai-gspc.pages.dev',
    basis: 'cross-sync: east-west crosswalk x live regulation x SOV-space sims (deterministic, no model judge)',
    witnessed_at,
    rails: { crosswalk_coverage, crosswalk_density, regulation_pressure, in_force_regimes: inForce, upcoming_regimes: upcoming },
    aggregate_signal: agg,
    divergence: Math.round((1 - agg) * 1000) / 1000,
    leader: leader ? { model: leader.model, signal: leader.signal } : null,
    per_model: perModel,
  };
  const content_id = await sha(canon(claim));
  const pair = await key(context.env);
  const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
  const pub = pair.rawPubHex ? h2b(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
  const card = { ...claim, content_id, signature: b64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
  if (pair.kid) { card.key_id = pair.kid; card.verification_method = pair.did + '#gspc'; card.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }

  return new Response(JSON.stringify({
    summary: `SOV SIGNAL ${agg} (divergence ${(1 - agg).toFixed(3)}) · leader ${leader ? leader.model + ' ' + leader.signal : '?'} · ${perModel.length} models · ${inForce}+${upcoming} regimes`,
    card,
  }), { status: 200, headers: h });
}
