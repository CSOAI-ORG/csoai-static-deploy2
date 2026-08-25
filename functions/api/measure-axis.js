/**
 * /api/measure-axis — the AXIS-BOOTSTRAP-EAT per-axis signed measurement card.
 *
 * Takes an axis (and optional model), reads the live board bank, computes the
 * Wilson 95% interval from the real n, and emits ONE signed Ed25519 card. This is
 * the "first signed row" for an axis: a stranger resolves did:web, recomputes
 * content_id, verifies the signature, and sees a real interval — never a claim.
 *
 *   GET /api/measure-axis?axis=gov[&model=phi4:14b]
 *
 * Measurement, not certification. The card states a measured accuracy + interval
 * on a frozen bank; it never says the model is good, safe, legal, or compliant.
 * An axis with no measured bank renders as UNMEASURED — the honest zero IS the
 * artifact (jail is UNTESTED until earned; it is never rendered as measured).
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from './signlib.js';

// Wilson score 95% interval for a binomial proportion.
function wilson95(acc, n) {
  const p = acc;
  const z = 1.96;
  const z2 = z * z;
  const denom = 1 + z2 / n;
  const center = (p + z2 / (2 * n)) / denom;
  const margin = (z * Math.sqrt((p * (1 - p) / n + z2 / (4 * n * n)))) / denom;
  return { low: round3(Math.max(0, center - margin)), high: round3(Math.min(1, center + margin)) };
}
function round3(x) { return Math.round(x * 1000) / 1000; }

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers });

  const url = new URL(context.request.url);
  const axis = String(url.searchParams.get('axis') || 'gov');
  const model = url.searchParams.get('model') || null;

  try {
    // Read the live board bank (same source /api/gspc uses).
    const board = await (await fetch('https://csoai-gspc.pages.dev/api/gspc')).json();
    const best = board.best || {};
    const axes_ = board.axes_ || [];
    const isKnownAxis = best[axis] || axes_.includes(axis);

    if (!isKnownAxis) {
      // Honest zero / unknown axis — sign a UNMEASURED row, never a claim.
      const claim = {
        schema: 'csoai.axis-measurement/0.1',
        record_type: 'unmeasured-current-state',
        not_a_certification: true,
        endorsement: 'none',
        authored_by: 'did:web:csoai-gspc.pages.dev',
        axis,
        status: 'UNMEASURED',
        basis: 'no measured bank for this axis; honest zero, never a claim (JL.5)',
        witnessed_at: new Date().toISOString(),
        grammar: 'this axis stays unmeasured until a signed card lands; the index counts what was measured',
      };
      const content_id = await sha256hex(canon(claim));
      const pair = await getKey(context.env);
      const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
      const pub = pair.rawPubHex ? hexToBytes(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
      const out = { ...claim, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
      if (pair.kid) { out.key_id = pair.kid; out.verification_method = pair.did + '#gspc'; out.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }
      return new Response(JSON.stringify(out), { status: 200, headers });
    }

    const entry = best[axis];
    const m = model ? { model, ...(board.cells && board.cells[model] && board.cells[model][axis] ? board.cells[model][axis] : {}) } : entry;
    const acc = Number(m.accuracy);
    const n = Number(m.n);
    const measured = Number.isFinite(acc) && n > 0;
    const interval = measured ? wilson95(acc, n) : null;

    const claim = {
      schema: 'csoai.axis-measurement/0.1',
      record_type: 'measured-current-state',
      not_a_certification: true,
      endorsement: 'none',
      authored_by: 'did:web:csoai-gspc.pages.dev',
      basis: 'deterministic exact-label grading on a frozen bank; no LLM judge, no vendor self-report',
      axis,
      model: m.model || null,
      measured: measured ? round3(acc) : null,
      n: measured ? n : 0,
      wilson95: interval,
      bank: board.banks ? board.banks[axis] || board.banks : 'frozen bank (see /api/gspc banks)',
      never: ['a quality verdict', 'a safety verdict', 'a compliance determination', 'a certification'],
      opinion_framing: 'a statement of opinion expressed as of the witnessed_at date — not a statement of fact, not a rating, not a recommendation to buy/hold/sell, not investment advice, and it does not address suitability. Unsolicited and permissionless: attached to the public record without issuer opt-in or payment (anti-touting safe by construction: non-issuer-paid, methodology-published).',
      witnessed_at: new Date().toISOString(),
    };
    const content_id = await sha256hex(canon(claim));
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
