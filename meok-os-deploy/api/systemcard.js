// DEFONEOS Assurance — a cryptographically-signed AI System Card. This is the primitive the
// UK MOD's JSP 936 needs and the Alan Turing Institute named as missing: an INDEPENDENT,
// OFFLINE-VERIFIABLE record that a defence-AI system was governed. Anyone (vendor, MOD, auditor)
// can verify it with the public key — no account, no trusting our dashboard.
// The card below is SYNTHETIC / DEMONSTRATION data. Signing is real (Ed25519, seed-stable).
import crypto from 'crypto';

function canonical(v) {
  if (typeof v === 'string') return v;
  const sort = (x) => Array.isArray(x) ? x.map(sort)
    : (x && typeof x === 'object') ? Object.keys(x).sort().reduce((o, k) => (o[k] = sort(x[k]), o), {}) : x;
  return JSON.stringify(sort(v));
}
function keypair() {
  const seed = crypto.createHash('sha256').update(process.env.SIGIL_SEED || 'meok-sovereign-demo-key-2026').digest();
  const pkcs8 = Buffer.concat([Buffer.from('302e020100300506032b657004220420', 'hex'), seed]);
  const priv = crypto.createPrivateKey({ key: pkcs8, format: 'der', type: 'pkcs8' });
  const pub = crypto.createPublicKey(priv);
  return { priv, pubHex: pub.export({ type: 'spki', format: 'der' }).toString('hex') };
}

// SYNTHETIC defence-AI system card — structured 1:1 to the UK Defence AI Centre (DAIC) /
// Alan Turing Institute System Card template: six sections (Overview, Concept of use, System
// detail, Security, Safety, Iterative requirements), each with a decision log, SRO-owned, and
// explicitly supporting adherence to JSP 936. Nothing operational; a public demonstration.
const CARD = {
  schema: 'defoneos.systemcard.v1 · DAIC/ATI template',
  classification: 'UNCLASSIFIED · SYNTHETIC DEMONSTRATION',
  senior_responsible_owner: 'SRO (demo) — accountable for keeping this card current',
  issued: '2026-07-01',
  version: '1.4.0',
  overview: {
    name: 'ISR Image-Triage Decision Support (SYNTHETIC)',
    supplier: 'Illustrative Prime Ltd (synthetic)',
    summary: 'Ranks incoming ISR imagery to cue human analyst review. Decision-SUPPORT only.',
    mission_risk: 'high-impact, human-in-the-loop',
  },
  concept_of_use: {
    intended_use: 'Cue an analyst to frames likely to contain items of interest.',
    out_of_scope: ['No autonomous targeting/engagement', 'No identification of individuals', 'Not a sole basis for any lethal or coercive decision'],
    human_oversight: 'Human-in-the-loop mandatory; analyst confirms every cue; the system cannot act.',
  },
  system_detail: {
    model: 'vision classifier (demo)',
    data_provenance: 'Synthetic + open ISR-like imagery (demo)',
    evaluation: { top1_synthetic: 0.94, false_negative_rate_synthetic: 0.03, last_evaluated: '2026-06-28' },
    limitations: ['degrades in unseen sensor conditions', 'not validated outside demo distribution'],
  },
  security: {
    pii: 'none', data_residency: 'UK-sovereign (demo)', supply_chain: 'all components + suppliers documented',
    integrity: 'this card is Ed25519-signed; tampering invalidates it',
  },
  safety: {
    hard_stops: ['no kinetic targeting', 'no individual surveillance', 'no unvoted autonomy'],
    care_floor: 0.95,
    failure_modes_reviewed: true,
    council: 'BFT quorum recorded',
  },
  iterative_requirements: {
    change_control: 'each retrain re-issues a new signed card; version history preserved',
    review_cadence: 'reviewed each release + on incident',
    incident_route: 'incidents logged and trigger re-assurance',
  },
  decision_logs: [
    { date: '2026-06-20', decision: 'Deployment gated on human-oversight control present', by: 'SRO (demo)' },
    { date: '2026-06-20', decision: 'Kinetic autonomy permanently disabled', by: 'SRO (demo)' },
    { date: '2026-06-28', decision: 'Evaluation refreshed; card re-signed', by: 'Assurance (demo)' },
  ],
  jsp936: 'This card supports adherence to JSP 936 (Dependable AI in Defence) — governance, development and assurance across the lifecycle.',
  assurance_statement: 'Recorded per a JSP 936-aligned lifecycle. Independently verifiable OFFLINE with the public key — no account, no trusting our dashboard. Any change to any field invalidates the signature.',
};

// SYNTHETIC Model Card — structured to the DAIC Model Card template (40+ fields / 10 sections).
// The finer-grained companion to the System Card: documents the MODEL, not the whole system.
const MODEL = {
  schema: 'defoneos.modelcard.v1 · DAIC template',
  classification: 'UNCLASSIFIED · SYNTHETIC DEMONSTRATION',
  model_details: { name: 'ISR-Triage Vision Classifier (SYNTHETIC)', version: '1.4.0', type: 'CNN image classifier (demo)', owner: 'Model owner (demo)', developer: 'Illustrative Prime Ltd (synthetic)', date: '2026-07-01', license: 'Crown / sovereign (demo)' },
  intended_use: { primary: 'Rank ISR frames to cue analyst review (decision-support only)', users: 'Cleared image analysts', out_of_scope: ['autonomous targeting', 'individual identification', 'sole basis for coercive action'] },
  factors: { relevant: ['sensor type', 'weather/illumination', 'altitude'], evaluation_factors: ['day/night', 'cloud cover'], groups: 'no individuals; scene-level only' },
  metrics: { performance: ['top-1 accuracy', 'false-negative rate'], thresholds: 'cue-recall prioritised over precision', decision: 'analyst confirms every cue' },
  evaluation_data: { datasets: 'Synthetic + open ISR-like (demo)', motivation: 'representative of demo distribution', preprocessing: 'standardised tiling (demo)' },
  training_data: { datasets: 'Synthetic (demo)', provenance: 'documented; no PII', residency: 'UK-sovereign (demo)' },
  quantitative_analysis: { top1_synthetic: 0.94, false_negative_rate_synthetic: 0.03, disaggregated: 'by day/night (demo)', last_evaluated: '2026-06-28' },
  ethical_considerations: { risks: 'over-reliance on cues', mitigations: 'mandatory human confirmation; hard-stops', hard_stops: ['no kinetic targeting', 'no individual surveillance', 'no unvoted autonomy'] },
  caveats_recommendations: { caveats: ['degrades on unseen sensors', 'not validated beyond demo distribution'], recommendations: ['re-evaluate before any new theatre', 're-issue signed card on retrain'] },
  ownership_governance: { sro: 'SRO (demo)', change_control: 'each retrain re-issues a signed model card', care_floor: 0.95, council: 'BFT quorum recorded' },
  jsp936: 'This model card supports adherence to JSP 936 (Dependable AI in Defence).',
  assurance_statement: 'Independently verifiable OFFLINE with the public key. Any change to any field invalidates the signature.',
};

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();
  try {
    // Allow a caller to sign THEIR OWN card fields (POST {card}); default = the demo card.
    // ?type=model (or POST {type:'model'}) returns the signed Model Card instead.
    let body = req.body; if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
    const type = ((req.query && req.query.type) || (body && body.type) || 'system').toString().toLowerCase();
    const base = type === 'model' ? MODEL : CARD;
    const card = (body && body.card && typeof body.card === 'object') ? body.card : base;
    const { priv, pubHex } = keypair();
    const message = canonical(card).slice(0, 8000);
    const signature = crypto.sign(null, Buffer.from(message), priv).toString('hex');
    const digest = crypto.createHash('sha256').update(message).digest('hex');
    const fingerprint = 'SOV:' + crypto.createHash('sha256').update(pubHex).digest('hex').slice(0, 32).match(/.{1,4}/g).join('-').toUpperCase();
    return res.status(200).json({
      ok: true, cardType: type, alg: 'ed25519', card, canonical: message, sha256: digest, signature, publicKey: pubHex,
      fingerprint, seeded: !!process.env.SIGIL_SEED,
      verify: { endpoint: '/api/verify', body: { message, signature, publicKey: pubHex }, page: '/verify.html' },
      note: 'Independently verifiable offline — POST {message, signature, publicKey} to /api/verify. Tampering with any field invalidates the signature. Card data is SYNTHETIC.',
    });
  } catch (e) { return res.status(500).json({ ok: false, error: String(e.message || e) }); }
}
