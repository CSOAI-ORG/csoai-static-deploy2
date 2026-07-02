// smoke test — sign → verify → tamper → verify-false → content re-bind. No deps.
const { signArtifact, verifyReceipt, callTool, FINGERPRINT } = require('./server.js');
let pass = 0, fail = 0;
function t(name, ok) { console.log((ok ? '✅' : '❌') + ' ' + name); ok ? pass++ : fail++; }

const output = 'Boltz-2 predicts binding affinity ΔG = -9.4 kcal/mol for ligand X to target Y.';
const r = signArtifact({ kind: 'finding', subject: 'binding affinity ligand X / target Y', output, method: 'Boltz-2 via BioNeMo; seed 42; env boltz@2.1', inputs: ['PDB:1ABC', 'SMILES:CC(=O)O'] });
const sc = r.defoneos_signed_contact;

t('receipt shape (defoneos_signed_contact + message + sig + pub)', !!(sc && sc.message && sc.signature_ed25519 && sc.public_key_ed25519));
t('message is exactly {i,ts,action,detail,prev}', JSON.stringify(Object.keys(sc.message).sort()) === JSON.stringify(['action','detail','i','prev','ts']));
t('signature is 128-hex (raw Ed25519)', /^[0-9a-f]{128}$/.test(sc.signature_ed25519));
t('public key is 64-hex (raw Ed25519)', /^[0-9a-f]{64}$/.test(sc.public_key_ed25519));
t('fingerprint present + stable', sc.fingerprint === FINGERPRINT && /^SOV:/.test(sc.fingerprint));
t('provenance records method + output hash + care-floor', !!(sc.provenance.method && sc.provenance.output_sha256 && sc.provenance.care_floor === 0.95));

const v = verifyReceipt(r);
t('valid receipt verifies TRUE', v.valid === true);

const bad = JSON.parse(JSON.stringify(r)); bad.defoneos_signed_contact.message.detail = bad.defoneos_signed_contact.message.detail.replace('ligand X', 'ligand Z');
t('tampered receipt (detail changed) verifies FALSE', verifyReceipt(bad).valid === false);
const bad2 = JSON.parse(JSON.stringify(r)); bad2.defoneos_signed_contact.message.ts = new Date().toISOString();
t('tampered receipt (timestamp changed) verifies FALSE', verifyReceipt(bad2).valid === false);

t('content re-bind TRUE for original output', verifyReceipt(Object.assign({}, sc, { output })).content_match === true);
t('content re-bind FALSE for altered output', verifyReceipt(Object.assign({}, sc, { output: output + ' (edited)' })).content_match === false);

const pk = callTool('defoneos_public_key', {});
t('public_key tool returns key + fingerprint', /^[0-9a-f]{64}$/.test(pk.public_key_ed25519) && /^SOV:/.test(pk.fingerprint));

// System Card
const { signSystemCard } = require('./server.js');
const cardR = signSystemCard({ name: 'ER-Triage Assistant', version: '2.1', provider: 'Acme Health', purpose: 'prioritise ED patients from vitals+notes', risk_tier: 'high', high_risk: true, rationale: 'EU AI Act Annex III — medical triage', frameworks: ['EU AI Act', 'ISO 42001', 'JSP 936'], limitations: 'decision-support only; clinician confirms' });
const csc = cardR.defoneos_signed_contact;
t('system card: signed receipt shape', !!(csc && csc.message && csc.signature_ed25519 && csc.system_card));
t('system card: action = system-card:<name>', csc.message.action === 'system-card:ER-Triage Assistant');
t('system card: records risk tier + frameworks + controls', csc.system_card.classification.risk_tier === 'high' && csc.system_card.frameworks.length >= 3 && !!csc.system_card.controls.human_oversight);
t('system card: invariant honesty note (attestation NOT certification)', /NOT certification|not certif/i.test(csc.note));
t('system card: signature verifies TRUE', verifyReceipt(cardR).valid === true);
const cbad = JSON.parse(JSON.stringify(cardR)); cbad.defoneos_signed_contact.message.detail = cbad.defoneos_signed_contact.message.detail.replace('"high"', '"minimal"');
t('system card: downgraded risk tier verifies FALSE (tamper-evident)', verifyReceipt(cbad).valid === false);

// OSCAL export
const { signOscal } = require('./server.js');
const oR = signOscal({ title: 'Acme AI — Governance Posture' });
const osc = oR.defoneos_signed_contact;
t('oscal: signed receipt + .oscal doc present', !!(osc && osc.message && osc.signature_ed25519 && osc.oscal));
t('oscal: valid OSCAL 1.1.2 component-definition', osc.oscal['component-definition'].metadata['oscal-version'] === '1.1.2' && Array.isArray(osc.oscal['component-definition'].components));
t('oscal: has implemented-requirements (controls)', osc.oscal['component-definition'].components[0]['control-implementations'][0]['implemented-requirements'].length >= 6);
t('oscal: signature verifies TRUE', verifyReceipt(oR).valid === true);
const crypto2 = require('crypto');
const recomputed = crypto2.createHash('sha256').update(JSON.stringify(osc.oscal)).digest('hex');
t('oscal: doc bound by sha256 (recompute matches + in signed message)', osc.doc_sha256 === recomputed && osc.message.detail.indexOf(recomputed) >= 0);
const obad = JSON.parse(JSON.stringify(oR)); obad.defoneos_signed_contact.message.detail = obad.defoneos_signed_contact.message.detail.replace(/sha256:[0-9a-f]{6}/, 'sha256:000000');
t('oscal: altered hash in message verifies FALSE', verifyReceipt(obad).valid === false);

// print a receipt to eyeball + to feed into verify.html
console.log('\n--- sample receipt (feed into verify.html) ---');
console.log(JSON.stringify(r));
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
