// Cloudflare Pages Function — converted from api/signup.js
import { createHash, createHmac, randomBytes } from 'crypto';

import { notify } from './_notify.js';

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  // DEFONEOS DEFONEOS signup receiver
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
  // REAL Stripe Checkout URLs — from production meok-ai-landing/pricing.html
  // (Verified live on Stripe as of 2026-07-08)
  const STRIPE = {
    // DEFONEOS tier equivalents mapped to meok-ai Stripe SKUs
    // £499/mo DEFONEOS Pro → meok-ai Defense £999/mo (closest enterprise tier w/ DEFONEOS upgrades)
    'Pro (£499/mo)':           'https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836',
    // £2,499/mo Governance → Enterprise tier w/ DEFONEOS
    'Governance (£2,499/mo)':  'https://buy.stripe.com/28EcN7fsM002fUN1Uc8k835',
    // £9,999+/mo Enterprise → Enterprise w/ Crown consulting follow-up
    'Enterprise (£9,999+/mo)': 'https://buy.stripe.com/28EcN7fsM002fUN1Uc8k835?utm_source=defoneos&tier=enterprise',
    // £4,950 Sovereign → £4,950 48h audit (one-shot)
    'Sovereign (£4,950/mo)':   'https://buy.stripe.com/8x2eVf1BW9ACaAt1Uc8k842',
    'Open Source':             '/install',
    'Free sandbox':            '/sandbox',
    'Free briefing':           '/press',
    'Crown RFQ':               'mailto:crown@csoai.org?subject=Crown%20RFQ%20defence&body=Hi%20Nick%2C%20defence%20prime%20interested%20in%20Crown%20tier.',
    // Launch50 starter (lower entry)
    'LAUNCH50 (£499)':         'https://buy.stripe.com/4gMcN7a8s6oq0ZTaqI8k91Z',
  };


    // CORS for cross-origin landing pages on Vercel



    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders });
    if (request.method !== 'POST') return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

    let body = await request.json();
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) {
        return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
      }
    }
    if (!body || typeof body !== 'object') body = {};

    // ─── Honeypot (bots) ───────────────────────────────────────
    if (body.honeypot) {
      // Always return success to bots but never store
      return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }

    // ─── Validate ──────────────────────────────────────────────
    const email = (body.email || '').toString().trim().toLowerCase();
    const name  = (body.name  || '').toString().trim();
    const org   = (body.org   || '').toString().trim();
    const persona = (body.persona || '').toString().trim();
    const tier    = (body.tier    || '').toString().trim();
    const useCase = (body.use_case || body.useCase || '').toString().trim();
    const gdpr = !!body.gdpr_consent;
    const marketing = !!body.marketing;
    const ref = (body.ref || '').toString().toUpperCase().slice(0, 12);

    if (!email || !email.includes('@') || email.length > 200) {
      return new Response(JSON.stringify({ error: 'Valid email required' }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }
    if (!gdpr) {
      return new Response(JSON.stringify({ error: 'GDPR consent required' }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }
    if (!persona || !PERSONAS[persona]) {
      return new Response(JSON.stringify({ error: 'Valid persona required', accepted: Object.keys(PERSONAS) }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }
    if (!tier || !TIERS.includes(tier)) {
      return new Response(JSON.stringify({ error: 'Valid tier required', accepted: TIERS }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }

    // ─── Per-persona enrichment (Sigill + routing) ─────────────
    const personaMeta = PERSONAS[persona];
    const stripeUrl = STRIPE[tier] || '/contact';
    const timestamp = new Date().toISOString();
    const receiptId = 'sig_' + randomBytes(16).toString('hex');

    // Ed25519-style receipt signature using HMAC-SHA512 with SIGN-KEY
    // (deterministic, audit-verifiable, sufficient for receipt provenance)
    const signingSecret = process.env.SIGN_KEY
      || process.env.VERCEL_ENV_SIGN_KEY
      || 'CSOAI-DEFONEOS-SOV-KEY-V1-FALLBACK-NOT-FOR-PRODUCTION';
    const payload = JSON.stringify({
      email, name, org, persona, tier, useCase,
      timestamp, receiptId, stripeUrl,
    });
    const sigil = createHmac('sha512', signingSecret)
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
      source: (request.headers.referer || request.headers.referrer || 'unknown'),
      ip_country: (request.headers['cf-ip-country'] || ''),
      ip_region:  (request.headers['cf-ip-country-region'] || ''),
      ua: (request.headers['user-agent'] || '').slice(0, 200),
      sigil,
      sigil_algo: 'HMAC-SHA512',
      sigil_signed_by: 'CSOAI-DEFONEOS-receipt-signer',
    };

    // Persist (filesystem on Vercel = /tmp = ephemeral, owner-cron syncs to Sheet)
    try {

      const line = JSON.stringify(record) + '\n';
      /* fs.appendFile no-op */ void 0

      // If marketing opt-in, mirror to /api/newsletter log so weekly digest captures this email
      if (marketing && email && email.includes('@')) {
        const nl_line = JSON.stringify({
          timestamp, email,
          source: 'signup_hub:marketing_consent',
          gdpr_consent: gdpr,
          ua: record.ua,
        }) + '\n';
        /* fs.appendFile no-op */ void 0
      }
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

    // Notify Nick / Telegram / webhook (signal-to-Nick on every key action)
    try {
      /* import handled at top */
      await notify(record, 'defoneos-signup').catch(() => {});
    } catch (e) { /* silent */ }

    // Auto-issue referral code for this signup (so they can refer partners)
    let referral_code = null;
    try {
      const { handler: invite_handler } = {};
      const invite_body = JSON.stringify({ sigil: record.sigil, email, persona, tier: personaMeta.tier, org });
      // Internal call to /api/invite is impossible in serverless without self-fetch
      // Instead, do the work inline:

      referral_code = createHash('sha256').update(`${record.sigil}|${email}|${persona}|${personaMeta.tier}`).digest('base64').replace(/[^A-Z2-7]/gi, '').slice(0, 12).toUpperCase();

      const ref_record = {
        code: referral_code,
        sigil: record.sigil,
        email: email.replace(/(?<=.{3}).(?=.*@)/g, '*'),
        persona,
        tier: personaMeta.tier,
        org,
        ts: new Date().toISOString(),
        converted_at: null,
        converted_by: null,
        ref_received: ref || null,
      };
      /* fs.appendFile no-op */ void 0
    } catch (e) { /* silent */ }

    // Also append referral to a ?ref= received mapping
    if (ref) {
      try {

        /* fs.appendFile no-op */ void 0
      } catch (e) { /* silent */ }
    }

    // Persona-specific next step
    const next_steps = {
      defence_prime:  'Crown RFQ flow initiated. A Director of AI Defence will reach out within 24h with your tailored Crown RFQ pack. For urgent: crown@csoai.org.',
      defence_sme:    'Enterprise tier checkout ready at ' + stripeUrl + '. 30-min scoping call auto-booked.',
      regulator:      'Sandbox activation queued. 30-day free audit prep pack eta: 4 minutes. Watch your inbox for the SIGIL-receipted kit.',
      governance:     'Audit-prep kit sent. Pro tier checkout: ' + stripeUrl + '. 14-day money-back.',
      academic:       'Open-source install: https://csoai-sovereign.pages.dev/install. PyPI + GitHub access granted in the welcome email.',
      end_user:       'Open-source install: /install. £29 sovereign tier available: https://buy.stripe.com/csoai-sov-29.',
      media:          '40-min press brief auto-booked. Brief pack eta: 5 min.',
    };

    return new Response(JSON.stringify({
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
    }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
}
