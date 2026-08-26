/**
 * /api/report/benchmark-integrity — the annual Benchmark Integrity Report (revenue Play #2).
 *
 * Grounds the "rating the raters" + corrections-ledger assets as a sponsorable,
 * signed, doctrine-compliant report. This is the State-of-X sponsorship model: the
 * report is free + signed (the trust engine); sponsor slots are the paid layer.
 *
 * It is honest about what it is and is not:
 *   - It reports which benchmark publishers publish a corrections register and which do not.
 *   - It does NOT certify, rate, or recommend any vendor. It measures a public fact
 *     (does a publisher keep an append-only record of its own errors?).
 *   - Every claim in the corpus resolves to the signed corrections register + methodology.
 *
 *   GET /api/report/benchmark-integrity → signed report shell
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from './signlib.js';

const REPORT = {
  schema: 'csoai.benchmark-integrity-report/0.1',
  title: 'Benchmark Integrity Report',
  edition: '2026',
  honesty_basis: 'A benchmark you can trust must (a) publish its methodology, (b) publish intervals + a separation rule, and (c) keep an append-only record of its own corrections. We score these as public, observable facts — never as a quality verdict.',
  findings: [
    { measure: 'methodology published', observed: 'most benchmark publishers publish a methodology document', basis: 'public methodology pages' },
    { measure: 'confidence intervals + separation rule', observed: 'rare — most report point estimates with no interval or significance test', basis: 'published benchmark results' },
    { measure: 'append-only corrections register', observed: 'a minority keep a public corrections record; many correct silently', basis: 'publisher corrections pages / git history' },
  ],
  our_own_audit: {
    corrections_register_entries: 15,
    policy: 'Appended, never edited or deleted. Each entry: what was wrong, how it was caught, the fix.',
    signatory: 'Each entry signed + time-anchored; the register is itself the honesty proof.',
  },
  our_statistical_discipline: {
    intervals: 'Wilson 95% CI (avoids Wald failure near 0/1)',
    separation: 'conservative overlap rule + McNemar paired test (overlapping CIs != non-significance)',
    never: ['a rating', 'a recommendation', 'investment advice', 'a certification'],
  },
  sponsor_slots: {
    note: 'The report is free + signed. Paid sponsorship funds the audit; sponsors do not influence the methodology or any finding. The list is a sponsored slot, never an endorsement.',
    slots: {
      headline: 1,
      section: 4,
      recommended_resource: 3,
    },
    boundary: 'no sponsor affects a measurement; the trust engine is free forever (R-free for regulators).',
  },
  never: ['a certification', 'a rating', 'investment advice', 'an endorsement'],
  witnessed_at: null,
};

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers });

  const claim = {
    schema: REPORT.schema,
    record_type: 'measured-current-state',
    not_a_certification: true,
    endorsement: 'none',
    authored_by: 'did:web:csoai-gspc.pages.dev',
    basis: 'the annual Benchmark Integrity Report — free + signed (trust engine); sponsors fund the audit but never influence a finding',
    report: REPORT,
    witnessed_at: new Date().toISOString(),
  };
  const content_id = await sha256hex(canon(claim));
  const pair = await getKey(context.env);
  const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
  const pub = pair.rawPubHex ? hexToBytes(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
  const out = { ...claim, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
  if (pair.kid) { out.key_id = pair.kid; out.verification_method = pair.did + '#gspc'; out.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }
  return new Response(JSON.stringify(out), { status: 200, headers });
}
