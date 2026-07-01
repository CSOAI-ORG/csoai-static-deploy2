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

// SYNTHETIC defence-AI system card — structured to JSP 936 assurance domains + the Turing
// "System Card" template. Nothing operational; a public, safe demonstration instance.
const CARD = {
  schema: 'defoneos.systemcard.v1',
  classification: 'UNCLASSIFIED · SYNTHETIC DEMONSTRATION',
  system: {
    name: 'ISR Image-Triage Decision Support (SYNTHETIC)',
    version: '1.4.0',
    owner: 'DEFONEOS Assurance (demo)',
    supplier: 'Illustrative Prime Ltd (synthetic)',
    issued: '2026-07-01',
    purpose: 'Rank incoming ISR imagery for human analyst review. Decision-SUPPORT only.',
  },
  intended_use: 'Cue a human analyst to frames likely to contain items of interest.',
  out_of_scope: [
    'No autonomous targeting or engagement of any kind',
    'No identification of individuals',
    'Not a sole basis for any lethal or coercive decision',
  ],
  data: { provenance: 'Synthetic + open ISR-like imagery (demo)', pii: 'none', residency: 'UK-sovereign (demo)' },
  model: { type: 'vision classifier (demo)', updates: 'change-controlled; each retrain re-issues a signed card' },
  risk: { framework: 'JSP 936-aligned', classification: 'high-impact human-in-the-loop', bias_tested: true, robustness_tested: true },
  evaluation: { top1_synthetic: 0.94, false_negative_rate_synthetic: 0.03, adversarial_robustness: 'tested (demo)', last_evaluated: '2026-06-28' },
  human_oversight: 'Human-in-the-loop mandatory; analyst confirms every cue; system cannot act.',
  hard_stops: ['no kinetic targeting', 'no individual surveillance', 'no unvoted autonomy'],
  governance: {
    care_floor: 0.95,
    council: 'BFT quorum recorded',
    decisions: ['deployment gated on human-oversight control present', 'kinetic autonomy permanently disabled'],
  },
  limitations: ['degrades in unseen sensor conditions', 'not validated outside demo distribution'],
  assurance_statement: 'Governed and recorded per JSP 936-aligned lifecycle assurance. This card is independently verifiable offline; tampering invalidates the signature.',
};

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();
  try {
    // Allow a caller to sign THEIR OWN card fields (POST {card}); default = the demo card.
    let body = req.body; if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
    const card = (body && body.card && typeof body.card === 'object') ? body.card : CARD;
    const { priv, pubHex } = keypair();
    const message = canonical(card).slice(0, 8000);
    const signature = crypto.sign(null, Buffer.from(message), priv).toString('hex');
    const digest = crypto.createHash('sha256').update(message).digest('hex');
    return res.status(200).json({
      ok: true, alg: 'ed25519', card, canonical: message, sha256: digest, signature, publicKey: pubHex,
      seeded: !!process.env.SIGIL_SEED,
      verify: { endpoint: '/api/verify', body: { message, signature, publicKey: pubHex }, page: '/verify.html' },
      note: 'Independently verifiable offline — POST {message, signature, publicKey} to /api/verify. Tampering with any field invalidates the signature. Card data is SYNTHETIC.',
    });
  } catch (e) { return res.status(500).json({ ok: false, error: String(e.message || e) }); }
}
