/**
 * /api/methodology — the statistical + governance methodology, published as a signed artifact.
 *
 * Per the benchmarking research (2026-08-25): no incumbent on-chain attester (Moody's
 * TIE, S&P via Chainlink, Particula, Credora/RedStone) publicly discloses confidence-interval
 * methodology, statistical-separation testing, or third-party audit of its scoring statistics.
 * Publishing THIS is GSPC's clearest differentiation lane — a hidden internal function turned
 * into a citable, stranger-verifiable governance asset.
 *
 * The methodology is itself a signed, did:web-resolvable payload so a stranger can recompute
 * content_id and verify the Ed25519 signature. It states the deliberate conservatism of the
 * separation rule (overlapping CIs ≠ non-significance) and cites the field-standard anchors.
 *
 *   GET /api/methodology → signed methodology artifact
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from './signlib.js';

const METHODOLOGY = {
  schema: 'csoai.measurement-methodology/0.1',
  title: 'GSPC statistical + governance methodology',
  confidence_interval: {
    method: 'Wilson score 95% interval',
    why: 'avoids the Wald interval failure near p=0 and p=1; the de-facto standard for accuracy/pass-rate proportion metrics in LLM evals',
    reference: 'Wilson (1927); Evan Miller, "Adding Error Bars to Evals," arXiv:2411.00640 (Anthropic, 2024)',
    formula: 'z=1.96; denom=1+z^2/n; center=(p+z^2/(2n))/denom; margin=z*sqrt((p(1-p)/n+z^2/(4n^2)))/denom',
  },
  separation_rule: {
    rule: 'we declare a leader only when that axis leader\'s Wilson interval does NOT overlap the fleet mean interval',
    deliberate_conservatism: 'true',
    why: 'overlapping confidence intervals do NOT by themselves prove non-significance; this rule errs toward NOT overclaiming, and is deliberately conservative + audit-friendly',
    paired_test: {
      method: 'McNemar chi^2 (df=1, continuity-corrected) on the frozen paired bank, p=erfc(sqrt(chi/2))',
      why: 'closes the one methodological criticism of CI-overlap: two estimates can have overlapping CIs yet differ significantly under a paired test. A head-to-head leader-vs-runner-up claim requires this paired test, not interval overlap alone.',
      example: { aOnly: 30, bOnly: 10, chi: 9.025, p: 0.0027, significant: true },
      refuse_when: 'no discordant pairs (b+c=0) — the test is not run and the caller is told so, not given a fake number',
    },
    gateway_note: 'head-to-head leader-vs-runner-up claims require the McNemar paired test (implemented); interval overlap alone is deliberately treated as NOT establishing a difference.',
  },
  governance_anchor: {
    framework: 'NIST AI RMF MEASURE function — "rigorous software testing and performance evaluation procedures with accompanying measurements of uncertainty, comparisons to performance benchmarks, and structured reporting"',
    contrast: 'MLPerf/MLCommons reports point estimates with no confidence intervals or significance testing on rankings; this methodology publishes intervals + a separation rule',
    human_baselines: 'GPQA-Diamond (Rein et al. 2023: PhD experts 65%, non-expert validators 34%); HLE (calibrated cautiously per FutureHouse 2025 correction-on-answers finding)',
  },
  independence: {
    mode: 'UNSOLICITED + PERMISSIONLESS',
    meaning: 'attached to the public record without issuer opt-in and without issuer payment',
    anti_touting: 'non-issuer-paid per asset by construction; methodology published; anti-touting/anti-fraud safe (contrast: SEC 2019 ICO-Rating enforcement for undisclosed issuer payment)',
    outside_taxonomy: 'a pure signed-opinion model — no token issuance, no custody, no synthetic exposure — sits outside the SEC Jan-2026 Statement on Tokenized Securities taxonomy; opinion-framing (not a rating, not investment advice) applies',
  },
  never: ['a rating', 'a recommendation to buy/hold/sell', 'investment advice', 'suitability opinion', 'a certification', 'a compliance determination', 'a quality/safety verdict'],
  witnessed_at: null, // set at request time
};

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers });

  try {
    const claim = {
      schema: METHODOLOGY.schema,
      record_type: 'measured-current-state',
      not_a_certification: true,
      endorsement: 'none',
      authored_by: 'did:web:csoai-gspc.pages.dev',
      basis: 'the statistical + governance methodology behind every measured card, published as a signed artifact so the discipline is auditable, not hidden',
      methodology: METHODOLOGY,
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
