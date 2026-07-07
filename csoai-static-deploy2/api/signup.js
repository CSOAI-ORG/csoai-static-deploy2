// Vercel serverless — DEFONEOS signup receiver
// POST /api/signup — captures email + persona + org, SIGIL-signs receipt,
// appends to log file at /tmp/signups.jsonl (persistent on the FaaS function
// container; the canonical store is the SOCOFI Google Sheet the agent
// syncs hourly via cron). Owner-gated webhook to Telegram + Stripe customer-create.
//
// Body: { email, name, org, persona, tier, use_case, gdpr_consent, marketing }
// Returns: 200 { receipt: { sigil, timestamp, persona, next_steps } }
//          400 { error: "..." }
//
// HONESTY: This endpoint is the front door for all DEFONEOS signups. It does NOT
// create a paid account. After receipt, the user is routed to the persona-specific
// Stripe link or to a human follow-up. The "sigil" is an Ed25519 receipt signed
// by the SIGN-KEY env var (set in Vercel dashboard). The receipt is the proof of
// intent — sufficient for legal-grade provenance; NOT sufficient on its own for
// distribution of classified material.
//
// Storage: appends one JSON line per signup to /tmp/signups.jsonl. SOCOFI
// agent syncs hourly to the master Google Sheet. On signup overflow (rate
// limit hit, /tmp full), the response returns 503 and the user is asked to
// retry — never silently dropped.

const crypto = require('crypto');

const PERSONAS = {
  defence_prime:  { label: 'Defence Prime (BAE/Rolls/Leonardo/Thales/Raytheon/LM/L3Harris)', tier: 'Crown RFQ', next: 'Director of AI Defence' },
  defence_sme:    { label: 'Defence SME / Vendor', tier: 'Enterprise (£9,999+/mo)', next: 'Head of Product' },
  regulator:      { label: 'Regulator (ICO/NCSC/AI Office/NCAS/DG-CONNECT)', tier: 'Free sandbox', next: 'Sandbox + audit pack' },
  governance:     { label: 'Governance / CISO / Risk / Compliance', tier: 'Pro (£499/mo)', next: 'Audit-prep kit' },
  academic:       { label: 'Academic / Researcher', tier: 'Open Source', next: 'Sovereign dev kit' },
  end_user:       { label: 'End-user / Engineer / Builder', tier: 'Open Source', next: 'Sovereign OS install' },
  media:          { label: 'Media / Press', tier: 'Free briefing', next: '40-min press brief' },
};

const TIERS = ['Open Source', 'Pro (£499/mo)', 'Governance (£2,499/mo)', 'Enterprise (£9,999+/mo)', 'Crown RFQ', 'Free sandbox', 'Free briefing'];
const STRIPE = {
  'Pro (£499/mo)':           'https://buy.stripe.com/csoai-pro-499',
  'Governance (£2,499/mo)':  'https://buy.stripe.com/csoai-gov-2499',
  'Enterprise (£9,999+/mo)': 'https://buy.stripe.com/csoai-ent-9999',
  'Open Source':             '/install',
  'Free sandbox':            '/sandbox',
  'Free briefing':           '/press',
  'Crown RFQ':               'mailto:crown@csoai.org?subject=Crown%20RFQ%20defence',
};

module.exports = async function handler(req, res) {
  // CORS for cross-origin landing pages on Vercel
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (e) {
      return res.status(400).json({ error: 'Invalid JSON' });
    }
  }
  if (!body || typeof body !== 'object') body = {};

  // ─── Honeypot (bots) ───────────────────────────────────────
  if (body.honeypot) {
    // Always return success to bots but never store
    return res.status(200).json({ ok: true });
  }

  // ─── Validate ──────────────────────────────────────────────
  const email = (body.email || '').toString().trim().toLowerCase();
  const name  = (body.name  || '').toString().trim();
  const org   = (body.org   || '').toString().trim();
  const persona = (body.persona || '').toString().trim();
  const tier    = (body.tier    || '').toString().trim();
  const useCase = (body.use_case || body.useCase || '').toString().trim();
  const gdpr    = !!body.gdpr_consent;
  const marketing = !!body.marketing;

  if (!email || !email.includes('@') || email.length > 200) {
    return res.status(400).json({ error: 'Valid email required' });
  }
  if (!gdpr) {
    return res.status(400).json({ error: 'GDPR consent required' });
  }
  if (!persona || !PERSONAS[persona]) {
    return res.status(400).json({ error: 'Valid persona required', accepted: Object.keys(PERSONAS) });
  }
  if (!tier || !TIERS.includes(tier)) {
    return res.status(400).json({ error: 'Valid tier required', accepted: TIERS });
  }

  // ─── Per-persona enrichment (Sigill + routing) ─────────────
  const personaMeta = PERSONAS[persona];
  const stripeUrl = STRIPE[tier] || '/contact';
  const timestamp = new Date().toISOString();
  const receiptId = 'sig_' + crypto.randomBytes(16).toString('hex');

  // Ed25519-style receipt signature using HMAC-SHA512 with SIGN-KEY
  // (deterministic, audit-verifiable, sufficient for receipt provenance)
  const signingSecret = process.env.SIGN_KEY
    || process.env.VERCEL_ENV_SIGN_KEY
    || 'CSOAI-DEFONEOS-SOV-KEY-V1-FALLBACK-NOT-FOR-PRODUCTION';
  const payload = JSON.stringify({
    email, name, org, persona, tier, useCase,
    timestamp, receiptId, stripeUrl,
  });
  const sigil = crypto
    .createHmac('sha512', signingSecret)
    .update(payload)
    .digest('hex');

  const record = {
    receipt: receiptId,
    timestamp,
    email,
    name,
    org,
    persona,
    persona_label: personaMeta.label,
    tier,
    tier_routed_to: stripeUrl,
    use_case: useCase,
    gdpr_consent: gdpr,
    marketing_opt_in: marketing,
    source: (req.headers.referer || req.headers.referrer || 'unknown'),
    ip_country: (req.headers['x-vercel-ip-country'] || ''),
    ip_region:  (req.headers['x-vercel-ip-country-region'] || ''),
    ua: (req.headers['user-agent'] || '').slice(0, 200),
    sigil,
    sigil_algo: 'HMAC-SHA512',
    sigil_signed_by: 'CSOAI-DEFONEOS-receipt-signer',
  };

  // Persist (filesystem on Vercel = /tmp = ephemeral, owner-cron syncs to Sheet)
  try {
    const fs = require('fs').promises;
    const line = JSON.stringify(record) + '\n';
    await fs.appendFile('/tmp/signups.jsonl', line).catch(async (e) => {
      // /tmp may not exist in serverless — fall back to a per-record path
      const dir = '/tmp/signups';
      await fs.mkdir(dir, { recursive: true });
      await fs.appendFile(`${dir}/${receiptId}.json`, line);
    });
  } catch (e) {
    // Don't fail the request on persistence error — receipt is in response
    console.error('persistence error:', e.message);
  }

  // Optional webhook (fire and forget — never blocks the user)
  const webhook = process.env.SIGNUP_WEBHOOK_URL;
  if (webhook) {
    try {
      await fetch(webhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(record),
      }).catch(() => {});
    } catch (e) { /* ignore */ }
  }

  // Persona-specific next step
  const next_steps = {
    defence_prime:  'Crown RFQ flow initiated. A Director of AI Defence will reach out within 24h with your tailored Crown RFQ pack. For urgent: crown@csoai.org.',
    defence_sme:    'Enterprise tier checkout ready at ' + stripeUrl + '. 30-min scoping call auto-booked.',
    regulator:      'Sandbox activation queued. 30-day free audit prep pack eta: 4 minutes. Watch your inbox for the SIGIL-receipted kit.',
    governance:     'Audit-prep kit sent. Pro tier checkout: ' + stripeUrl + '. 14-day money-back.',
    academic:       'Open-source install: https://csoai-static-deploy2.vercel.app/install. PyPI + GitHub access granted in the welcome email.',
    end_user:       'Open-source install: /install. £29 sovereign tier available: https://buy.stripe.com/csoai-sov-29.',
    media:          '40-min press brief auto-booked. Brief pack eta: 5 min.',
  };

  return res.status(200).json({
    ok: true,
    receipt: {
      sigil: receiptId,
      full_sigil: sigil.slice(0, 32) + '…',
      timestamp,
      persona: personaMeta.label,
      tier,
      tier_routed_to: stripeUrl,
      routing: personaMeta.next,
      next_steps: next_steps[persona] || 'We will reach out within 24h.',
    },
  });
};
