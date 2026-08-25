/**
 * /api/mcnemar — paired (McNemar) head-to-head significance test, as a signed endpoint.
 *
 * The benchmarking research (2026-08-25) is explicit: overlapping Wilson CIs do NOT
 * prove non-significance — two estimates can overlap yet differ significantly under
 * a paired test. This is the one methodological criticism a sophisticated reviewer
 * could raise against a CI-overlap-only separation rule. This endpoint closes it:
 * caller supplies the paired contingency counts on a frozen bank, and we return the
 * McNemar chi^2 (df=1, continuity-corrected) + p-value + a signed verdict object.
 *
 *   POST /api/mcnemar {"agreeBoth":40,"aOnly":30,"bOnly":10,"agreeNeither":20}
 *   GET  → schema
 *
 * Honest boundary: if there are no discordant pairs (b+c=0) the test is not run and
 * the caller is told so — we never hand back a fabricated significance number.
 * The verdict is a signed measurement of a difference; it is never a ranking, a
 * recommendation, or investment advice.
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from './signlib.js';

function erfc(x) {
  const t = 1 / (1 + 0.3275911 * Math.abs(x));
  const y = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))));
  return (x >= 0) ? y * Math.exp(-x * x) : 2 - y * Math.exp(-x * x);
}

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,POST,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method === 'GET') {
    return new Response(JSON.stringify({ schema: 'csoai.mcnemar-test/0.1', example: 'POST {"agreeBoth":40,"aOnly":30,"bOnly":10,"agreeNeither":20}', not_a_certification: true }), { status: 200, headers });
  }
  if (context.request.method !== 'POST') return new Response(JSON.stringify({ error: 'POST or GET only' }), { status: 405, headers });

  let b;
  try { b = await context.request.json(); } catch (e) { return new Response(JSON.stringify({ error: 'bad json' }), { status: 400, headers }); }
  const agreeBoth = Number(b.agreeBoth) || 0, aOnly = Number(b.aOnly) || 0, bOnly = Number(b.bOnly) || 0, agreeNeither = Number(b.agreeNeither) || 0;
  const n = agreeBoth + aOnly + bOnly + agreeNeither;
  let result;
  if (aOnly + bOnly === 0) {
    result = { valid: false, why: 'no discordant pairs (b+c=0) — the paired test cannot be run; no significance number is fabricated', n };
  } else {
    const chi = Math.pow(Math.abs(aOnly - bOnly) - 1, 2) / (aOnly + bOnly);
    const p = Math.min(1, erfc(Math.sqrt(chi / 2)));
    result = { valid: true, n, agreeBoth, aOnly, bOnly, agreeNeither, chi: +chi.toFixed(4), p: +p.toFixed(4), significant: p < 0.05, interpretation: p < 0.05 ? 'statistically significant difference (alpha=0.05)' : 'no significant difference (alpha=0.05)' };
  }

  try {
    const claim = {
      schema: 'csoai.mcnemar-test/0.1',
      record_type: 'measured-current-state',
      not_a_certification: true,
      endorsement: 'none',
      authored_by: 'did:web:csoai-gspc.pages.dev',
      basis: 'paired McNemar test (chi^2 df=1, continuity-corrected, p=erfc(sqrt(chi/2))). Closes the overlapping-CI != non-significance criticism.',
      witnessed_at: new Date().toISOString(),
      result,
      never: ['a ranking', 'a recommendation', 'investment advice', 'a certification'],
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
