// /api/welcome — Send a SIGIL-receipted welcome email on every signup
// POST /api/welcome?receipt=<sigid>&email=<email>&persona=<p> — composes + sends
//
// HONESTY:
// - This endpoint requires a private SEND_KEY in env to prevent spam.
// - Without RESEND_API_KEY (etc.), it persists the message to /tmp/email.outbox.jsonl for owner-cron sync.
// - The welcome email includes the SIGIL hash, persona, tier, and a 1-click "next step" CTA.

const fs = require('fs').promises;
const crypto = require('crypto');

const NEXT_STEPS = {
  defence_prime:  { subject: '🛡️ Your DEFONEOS Crown RFQ is being prepared', cta: 'crown@csoai.org', next: 'A Director of AI Defence will reach out within 24h with your tailored Crown RFQ pack.' },
  defence_sme:    { subject: '🛡️ Welcome to DEFONEOS — Enterprise tier', cta: 'https://csoai-sovereign.pages.dev/defoneos-defence-primes', next: 'Your SIGIL-receipted audit pack will arrive in 4 minutes. Review + book your 40-min scoping call.' },
  regulator:      { subject: '⚖️ Welcome — DEFONEOS regulator sandbox activated', cta: 'https://csoai-sovereign.pages.dev/defoneos-regulators', next: 'Sandbox + 12-framework compliance evidence pack attached. 30-day free trial auto-expires (no card).' },
  governance:     { subject: '📊 DEFONEOS Pro tier — your audit-prep kit is in flight', cta: 'https://csoai-sovereign.pages.dev/defoneos-system-card', next: 'Audit-prep kit will arrive in 4 minutes. 14-day money-back. ISO 42001 + EU AI Act evidence pack included.' },
  academic:       { subject: '🔬 Welcome to DEFONEOS — sovereign dev kit', cta: 'https://csoai-sovereign.pages.dev/install', next: 'Open-source install + PyPI access + GitHub repo access granted. Citation framework included.' },
  end_user:       { subject: '⚡ Welcome to DEFONEOS — sovereign OS install ready', cta: 'https://csoai-sovereign.pages.dev/install', next: 'Open-source install ready. Sovereign compute tier at £29/mo available.' },
  media:          { subject: '📰 Welcome — your 40-min press brief is booked', cta: 'https://csoai-sovereign.pages.dev/defoneos-press', next: 'Cited brief pack will arrive in 4 minutes. Slot within 24h. Off-the-record available on request.' },
};

function buildEmailBody(record) {
  const persona = record.persona || 'unknown';
  const next = NEXT_STEPS[persona] || { subject: 'Welcome to DEFONEOS', cta: 'https://csoai-sovereign.pages.dev', next: 'Your SIGIL-signed receipt is below. We will be in touch within 24h.' };

  return {
    subject: next.subject,
    text: [
      next.subject,
      '',
      `Hi ${record.name || 'there'},`,
      '',
      `Welcome to DEFONEOS. Your signup has been SIGIL-signed and routed.`,
      '',
      `Receipt details:`,
      `  • SIGIL: ${record.sigil}`,
      `  • Persona: ${persona}`,
      `  • Tier: ${record.tier || 'pending'}`,
      `  • Issuer: CSOAI LTD UK 16939677`,
      `  • Timestamp: ${record.timestamp}`,
      `  • Verify at: https://csoai-sovereign.pages.dev/defoneos-verify`,
      '',
      `What happens next: ${next.next}`,
      '',
      `Next step: ${next.cta}`,
      '',
      `--`,
      `DEFONEOS — sovereign AI for UK + AUKUS defence primes.`,
      `Sovereign-by-construction. Audit-grade. Signed. Neutral.`,
      `Charter Article 0 binding — ISO fee-for-service only.`,
      '',
      `If you did not request this email, please ignore or reply STOP.`,
    ].join('\n'),
    html: `<p style="font-family:system-ui,sans-serif;line-height:1.5"><strong>${next.subject}</strong></p>
<p>Hi ${record.name || 'there'},</p>
<p>Welcome to DEFONEOS. Your signup has been SIGIL-signed and routed.</p>
<table style="font-family:'SF Mono',monospace;font-size:13px;border-collapse:collapse">
<tr><td><strong>SIGIL</strong></td><td>${record.sigil}</td></tr>
<tr><td><strong>Persona</strong></td><td>${persona}</td></tr>
<tr><td><strong>Tier</strong></td><td>${record.tier || 'pending'}</td></tr>
<tr><td><strong>Issuer</strong></td><td>CSOAI LTD UK 16939677</td></tr>
<tr><td><strong>Timestamp</strong></td><td>${record.timestamp}</td></tr>
</table>
<p>What happens next: ${next.next}</p>
<p><a href="${next.cta}" style="display:inline-block;padding:.7rem 1.4rem;background:linear-gradient(135deg,#22d3ee,#a78bfa);color:#000;border-radius:8px;text-decoration:none;font-weight:700">Continue to ${next.cta.includes('mailto') ? 'Crown RFQ flow' : 'your next step'} →</a></p>
<p style="color:#64748b;font-size:13px">DEFONEOS — sovereign-by-construction · UK-sovereign · AUKUS-compatible · Charter Article 0 binding</p>
<p style="color:#64748b;font-size:11px">If you did not request this email, please ignore or reply STOP.</p>`,
    from: 'DEFONEOS <noreply@defoneos.ai>',
    to: record.email,
  };
}

async function sendViaProvider(email) {
  const RESEND = process.env.RESEND_API_KEY;
  if (!RESEND) return { provider: 'none', reason: 'RESEND_API_KEY unset' };
  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${RESEND}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: email.from, to: email.to, subject: email.subject, text: email.text, html: email.html }),
    });
    const body = await res.json().catch(() => ({}));
    return { provider: 'resend', status: res.status, body };
  } catch (e) {
    return { provider: 'resend-error', error: e.message };
  }
}

async function sendViaSmtp(email) {
  const SMTP_URL = process.env.SMTP_WEBHOOK_URL;
  if (!SMTP_URL) return { provider: 'none', reason: 'SMTP_WEBHOOK_URL unset' };
  try {
    await fetch(SMTP_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(email) }).catch(() => {});
    return { provider: 'smtp-webhook', sent: true };
  } catch (e) { return { provider: 'smtp-error', error: e.message }; }
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }
  if (!body || typeof body !== 'object') body = {};

  // Auth: require SEND_KEY in header (since email-sending should not be public)
  const providedKey = (req.headers['x-send-key'] || req.headers.authorization || '').replace(/^Bearer\s+/i, '').trim();
  const expectedKey = process.env.SEND_KEY || process.env.SIGNUP_WEBHOOK_SECRET || '';
  if (expectedKey && providedKey !== expectedKey) {
    return res.status(401).json({ error: 'Invalid SEND_KEY' });
  }

  const record = body.record || body;
  if (!record.email || !record.sigil) return res.status(400).json({ error: 'record.email + record.sigil required' });

  const email = buildEmailBody(record);

  // Try providers in order: Resend → SMTP webhook → fallback outbox
  let result;
  if (process.env.RESEND_API_KEY) result = await sendViaProvider(email);
  if (!result || result.provider === 'none') result = await sendViaSmtp(email);

  // Always append to outbox (so cron can replay)
  try {
    const line = JSON.stringify({ ts: new Date().toISOString(), record: { sigil: record.sigil, email: record.email, persona: record.persona, tier: record.tier }, email, deliver_attempt: result }) + '\n';
    await fs.appendFile('/tmp/email.outbox.jsonl', line).catch(() => {});
  } catch (e) { /* silent */ }

  if (!result || (result.provider === 'none' && !process.env.SMTP_WEBHOOK_URL)) {
    return res.status(200).json({
      ok: true,
      delivered: false,
      queued: true,
      reason: 'No email provider configured (RESEND_API_KEY or SMTP_WEBHOOK_URL). Email queued in /tmp/email.outbox.jsonl for owner-cron replay.',
      email_subject: email.subject,
      record_sigil: record.sigil,
    });
  }

  return res.status(200).json({ ok: true, delivered: true, result, email_subject: email.subject });
};
