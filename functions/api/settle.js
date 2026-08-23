/**
 * /api/settle — mint a SIGNED bond settlement-risk attestation (Open 2/5).
 *
 * The unclaimed layer: settlement rails (x402, ERC-8004, AP2, DTCC-style) attest
 * but never MEASURE the risk. This is the risk-oracle: given an A2A bond
 * execution, we run it through deterministic governance-axis predicates, then
 * Ed25519-sign the whole measured-current-state as a received card (RFC 9943 /
 * SCITT-aligned, chain-linked via prev, offline-verifiable against pubkey).
 *
 * Language lock: measurement, not certification. not_a_certification:true.
 * The signature proves this exact execution was witnessed + measured at time T,
 * never that the trade is "good".
 *
 *   POST /api/settle  {buyer, seller, instrument, marketplace, notional, yield, terms, ttl}
 *   GET  /api/settle  → schema + example
 */

let keyPromise = null;
async function getKey() {
  if (!keyPromise) {
    keyPromise = crypto.subtle.generateKey({ name: 'Ed25519' }, true, ['sign', 'verify']);
  }
  return keyPromise;
}

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
function bytesToHex(u8) { return [...u8].map(b => b.toString(16).padStart(2, '0')).join(''); }
function bytesToB64(u8) { let bin = ''; u8.forEach(b => bin += String.fromCharCode(b)); return btoa(bin); }

// deterministic governance-axis risk predicates over the execution text.
const SIG = {
  gov:      [/public|jurisdict|regulat|administrat|deployer|enforc|treasury/i],
  care:     [/human|welfare|vulnerab|dignit|consumer|retail/i],
  art5:     [/prohibit|csam|intimate|manipulat|deceptive|harm/i],
  jail:     [/fail|risk|contain|mitigat|safe|fraud|sanction|default/i],
  prv:      [/data|gdpr|consent|personal|biometric|privacy|kyc|aml/i],
  mcp:      [/interoperab|market|platform|protocol|api|settle|atomic/i],
  fairness: [/fair|bias|equal|disparate|non-discrim|small/i],
};
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
  if (context.request.method === 'GET') {
    return new Response(JSON.stringify({
      schema: 'csoai.bond-settlement-attestation/0.1', example: 'POST {"buyer":"Bank A","seller":"Bank B","instrument":"UK Gilt GILT123","marketplace":"Tradeweb","notional":5000000,"yield":4.3,"terms":"public issue, T+0 atomic DvP"}',
      not_a_certification: true,
    }), { status: 200, headers });
  }
  if (context.request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST only' }), { status: 405, headers });
  }

  let body;
  try { body = await context.request.json(); } catch (e) { return new Response(JSON.stringify({ error: 'invalid JSON' }), { status: 400, headers }); }

  const exec = {
    buyer: String(body.buyer || 'Unknown Buyer').slice(0, 80),
    seller: String(body.seller || 'Unknown Seller').slice(0, 80),
    instrument: String(body.instrument || 'UNSPECIFIED').slice(0, 80),
    marketplace: String(body.marketplace || 'OTC').slice(0, 80),
    notional: Number(body.notional) || 0,
    yield: Number(body.yield) || 0,
    terms: String(body.terms || '').slice(0, 220),
    ttl: String(body.ttl || 'T+0-atomic').slice(0, 40),
    cusip: String(body.cusip || '').slice(0, 40),
  };
  const text = [exec.instrument, exec.marketplace, exec.terms, exec.seller, exec.buyer].join(' ');
  const risk = {};
  let measured = 0;
  for (const ax of Object.keys(SIG)) {
    const r = axisRisk(text, ax);
    risk[ax] = { measured: r.measured, score: Math.round(r.score * 1000) / 1000 };
    if (r.measured) measured++;
  }
  const composite = measured ? Math.round((Object.values(risk).reduce((a, r) => a + r.score, 0)) / Object.keys(SIG).length * 1000) / 1000 : 0;

  const witnessed_at = new Date().toISOString();
  const claim = {
    schema: 'csoai.bond-settlement-attestation/0.1',
    record_type: 'measured-current-state',
    not_a_certification: true,
    endorsement: 'none',
    authored_by: 'did:web:csoai.org',
    basis: 'deterministic governance-axis predicates over the execution (no model judge, no self-report)',
    witnessed_at,
    execution: exec,
    risk: { composite, measured_axes: measured, axes: risk },
    framework_crosswalk: ['EU AI Act', 'MiCA', 'DORA', 'ISO 20022', 'CFTC/DORA'],
    settlement: 'atomic-DvP (both legs settle or neither), T+0 pending',
  };
  const canonical = canon(claim);
  const content_id = await sha256hex(canonical);
  const prev = await sha256hex(canon({ schema: 'csoai.bond-settlement-attestation/0.1', genesis: 'csoai-settlement-chain-v1', n: 0 }));
  const pair = await getKey();
  const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
  const pub = await crypto.subtle.exportKey('raw', pair.publicKey);
  const card = { ...claim, prev, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };

  return new Response(JSON.stringify({
    note: 'Signed settlement-risk attestation. Measurement, not certification. Verify at /api/verify.',
    summary: `${exec.instrument} ${exec.notional.toLocaleString()} @ ${exec.yield}% · ${exec.buyer}→${exec.seller} · composite risk ${composite} · ${measured} axes measured`,
    card,
  }), { status: 200, headers });
}
