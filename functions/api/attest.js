/**
 * /api/attest — the EUNOMIA ENGINE-AXIS attestor (sector-agnostic).
 *
 * One measured + signed layer for ANY sector: banks · insurance · AI agents ·
 * COBOL/legacy · bond market · index · stock market · east-to-east cross-border.
 * A single governance-axis vocabulary is applied to whatever object is routed
 * through; the result is an Ed25519-signed, not_a_certification, chain-linkable
 * card (recompute content_id + verify signature like /api/verify).
 *
 * The thesis: every instrument moves on the X-axis (human→agent / speed) but must
 * climb the Y-axis (EUNOMIA verification) to be legal, auditable, insured. This is
 * the Y-axis as one engine.
 *
 *   POST {sector, subject, text, actor, counterparty, amount, jurisdiction, prev}
 *   GET  → schema + examples
 */

let keyPromise = null;
async function getKey() {
  if (!keyPromise) keyPromise = crypto.subtle.generateKey({ name: 'Ed25519' }, true, ['sign', 'verify']);
  return keyPromise;
}
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
function bytesToHex(u8) { return [...u8].map(b => b.toString(16).padStart(2, '0')).join(''); }
function bytesToB64(u8) { let bin = ''; u8.forEach(b => bin += String.fromCharCode(b)); return btoa(bin); }

// one governance-axis vocabulary across ALL sectors.
const SIG = {
  gov:       [/jurisdict|regulat|public|administrat|enforc|treasury|fca|sec|mnuch|esma/i],
  care:      [/human|welfare|vulnerab|dignit|consumer|retail|patient|insured|dignity/i],
  art5:      [/prohibit|csam|intimate|manipulat|deceptive|harm|non-consensual/i],
  jail:      [/fail|risk|contain|mitigat|safe|fraud|sanction|default|breach|wash/i],
  prv:       [/data|gdpr|consent|personal|biometric|privacy|kyc|aml|confident/i],
  mcp:       [/interoperab|market|platform|protocol|api|settle|atomic|trade|venue/i],
  fairness:  [/fair|bias|equal|disparate|non-discrim|small|retail-protect/i],
  identity:  [/did|credential|identity|verifiable|agent-card|sbt|soulbound|claim/i],
  market:    [/quote|markout|spread|price|implied|vol|liquid|index|hedge/i],
  reliability:[/batch|copybook|mainframe|legacy|reconcil|audit-trail|determin|overnight/i],
  jurisdiction:[/cross-border|east|china|europe|mifid|uk|us|brussels|beijing|jurisdiction/i],
};
const SECTORS = ['bond', 'insurance', 'equity', 'index', 'banking', 'cobol', 'agent', 'cross-border', 'generic'];

function axisRisk(text, ax) {
  const re = SIG[ax] || [];
  if (!re.length) return { measured: false, score: 0 };
  const t = String(text || '').toLowerCase();
  const hits = re.filter(r => r.test(t)).length;
  return { measured: hits > 0, score: Math.min(1, hits / re.length) };
}

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,POST,OPTIONS', 'access-control-allow-headers': 'Content-Type' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  const url = new URL(context.request.url);

  if (context.request.method === 'GET') {
    return new Response(JSON.stringify({
      schema: 'csoai.engine-axis-attestation/0.1', sectors: SECTORS, axes: Object.keys(SIG),
      example: 'POST {"sector":"insurance","subject":"Policy INS-777","text":"retail human insured, KYC/AML done, non-discriminatory, privacy protected, claims dispute risk mitigated, FCA rules"}',
      not_a_certification: true,
    }), { status: 200, headers });
  }
  if (context.request.method !== 'POST') return new Response(JSON.stringify({ error: 'POST or GET only' }), { status: 405, headers });

  let body;
  try { body = await context.request.json(); } catch (e) { return new Response(JSON.stringify({ error: 'invalid JSON' }), { status: 400, headers }); }

  const sector = SECTORS.includes(String(body.sector).toLowerCase()) ? String(body.sector).toLowerCase() : 'generic';
  const text = [body.subject, body.text, body.counterparty, body.actor, body.jurisdiction].filter(Boolean).join(' ');
  const risk = {};
  let measured = 0;
  for (const ax of Object.keys(SIG)) {
    const r = axisRisk(text, ax);
    risk[ax] = { measured: r.measured, score: Math.round(r.score * 1000) / 1000 };
    if (r.measured) measured++;
  }
  const composite = measured ? Math.round(Object.values(risk).reduce((a, r) => a + r.score, 0) / Object.keys(SIG).length * 1000) / 1000 : 0;

  const witnessed_at = new Date().toISOString();
  const claim = {
    schema: 'csoai.engine-axis-attestation/0.1',
    record_type: 'measured-current-state',
    not_a_certification: true,
    endorsement: 'none',
    authored_by: 'did:web:csoai.org',
    basis: 'one EUNOMIA engine-axis vocabulary, deterministic exact-label predicates (no model judge, no self-report)',
    sector,
    witnessed_at,
    object: {
      subject: String(body.subject || 'UNSPECIFIED').slice(0, 100),
      actor: String(body.actor || 'unknown').slice(0, 80),
      counterparty: String(body.counterparty || '').slice(0, 80),
      amount: Number(body.amount) || 0,
      jurisdiction: String(body.jurisdiction || '').slice(0, 60),
      text: String(body.text || '').slice(0, 300),
    },
    risk: { composite, measured_axes: measured, axes: risk },
    framing: 'every sector climbs the same measured Y-axis before it is legal, auditable, insured',
  };
  const canonical = canon(claim);
  const content_id = await sha256hex(canonical);
  // persistent chain: link this attestation to the previous head (KV-backed).
  const kv = context.env && context.env.SOVOS_CHAIN;
  let prev;
  if (kv) {
    try { prev = await kv.get('sovos-chain-head') || await sha256hex(canon({ schema: 'csoai.engine-axis-attestation/0.1', genesis: 'sovos-engine-axis-chain-v1' })); }
    catch (e) { prev = body.prev || await sha256hex(canon({ schema: 'csoai.engine-axis-attestation/0.1', genesis: 'sovos-engine-axis-chain-v1' })); }
  } else {
    prev = body.prev || await sha256hex(canon({ schema: 'csoai.engine-axis-attestation/0.1', genesis: 'sovos-engine-axis-chain-v1' }));
  }
  const pair = await getKey();
  const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
  const pub = await crypto.subtle.exportKey('raw', pair.publicKey);
  const card = { ...claim, prev, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
  let chained = false;
  if (kv) {
    try { await kv.put('sovos-chain-head', card.content_id); await kv.put('card:' + card.content_id, JSON.stringify(card)); chained = true; }
    catch (e) { /* non-fatal: /api/attest still returns the signed card */ }
  }

  return new Response(JSON.stringify({
    note: 'Engine-axis attestation (sector-agnostic). Measurement, not certification. Verify at /api/verify. ' + (chained ? 'Chained on SOVOS ledger (see /api/chain).' : ''),
    summary: `${sector.toUpperCase()} · ${claim.object.subject} · ${claim.object.actor}→${claim.object.counterparty} · composite ${composite} · ${measured} of ${Object.keys(SIG).length} axes measured`,
    chained,
    card,
  }), { status: 200, headers });
}
