#!/usr/bin/env node
// MEOK products E2E — functional assertions against the LIVE estate (not just HTTP 200).
// Run: node test/e2e-products.mjs [baseURL]   (default https://os.meok.ai)
const BASE = process.argv[2] || 'https://os.meok.ai';
let pass = 0, fail = 0; const fails = [];
const ck = (name, cond, extra = '') => { if (cond) { pass++; console.log('  ok   ' + name); } else { fail++; fails.push(name); console.log('  FAIL ' + name + (extra ? '  → ' + extra : '')); } };
const gj = async (u, opt) => { const r = await fetch(BASE + u, opt); return { s: r.status, j: await r.json().catch(() => ({})) }; };
const post = (u, b) => gj(u, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(b) });

console.log('E2E products @ ' + BASE + '\n');

// ── governance lookup ──
let r = await gj('/api/govern?q=I%20run%20a%20bank');
ck('govern: bank → finance + DORA', r.j.industry === 'finance' && r.j.frameworks.some(f => f.name === 'DORA'));
r = await gj('/api/govern?q=healthcare%20clinic');
ck('govern: healthcare → HIPAA', r.j.frameworks.some(f => f.name === 'HIPAA'));
r = await gj('/api/govern?q=zxq-nonsense');
ck('govern: unknown → general fallback', r.j.industry === 'general');

// ── legacy bridges (real validation) ──
r = await post('/api/bridge', { message: 'GB33BUKB20201555555555' });
ck('bridge: valid IBAN passes mod-97', r.j.detected === 'iban' && r.j.result?.valid === true);
r = await post('/api/bridge', { message: 'GB00BUKB20201555555555' });
ck('bridge: bad IBAN fails', r.j.result?.valid === false);
r = await gj('/api/bridge?sample=hl7');
ck('bridge: HL7 MSH parses (ADT)', r.j.detected === 'hl7' && /ADT/.test(r.j.result?.messageType || ''));
r = await gj('/api/bridge?sample=iso20022');
ck('bridge: ISO 20022 pain.001 valid', r.j.result?.valid === true && /pain\./.test(r.j.result?.scheme || ''));
r = await gj('/api/bridge?sample=swift-mt');
ck('bridge: SWIFT MT103 parses', r.j.result?.valid === true && r.j.result?.mt === '103');

// ── Ed25519 sign → verify (the moat) ──
r = await post('/api/sign', { action: { do: 'approve-loan', amount: 5000, ts: 'fixed' } });
const canon = r.j.canonical, sig = r.j.signature, pub = r.j.publicKey;
ck('sign: returns ed25519 sig + pubkey', r.j.ok && r.j.alg === 'ed25519' && /^[0-9a-f]+$/.test(sig));
let v = await post('/api/verify', { message: canon, signature: sig, publicKey: pub });
ck('verify: honest signature valid', v.j.valid === true);
v = await post('/api/verify', { message: canon.replace('5000', '9999'), signature: sig, publicKey: pub });
ck('verify: tampered message REJECTED', v.j.valid === false);

// ── canonical node graph ──
r = await gj('/api/nodes');
ck('nodes: 12 hubs, London governed', r.j.count === 12 && r.j.nodes?.find(n=>n.id==="london")?.status === 'governed');

// ── live world knowledge ──
r = await gj('/api/knowledge?q=London');
ck('knowledge: live population fact', r.j.facts && r.j.facts.population > 1000000);

// ── governed brain ──
r = await post('/api/chat', { message: 'say ok', register: 'plain' });
ck('chat: governed brain replies', typeof r.j.response === 'string' && r.j.response.length > 0, r.j.model);

// ── supporting product endpoints ──
for (const [n, u] of [['social networks', '/api/social?action=networks'], ['media (CC)', '/api/media?q=sea&n=1'], ['badge svg', '/api/badge'], ['avatar svg', '/api/avatar?queen_id=queen-care']]) {
  const rr = await fetch(BASE + u); ck('reachable: ' + n, rr.status === 200);
}

console.log('\n' + (fail === 0 ? '✅ PASS' : '❌ FAIL') + ' — ' + pass + ' passed, ' + fail + ' failed' + (fails.length ? '  [' + fails.join(', ') + ']' : ''));
process.exit(fail ? 1 : 0);
