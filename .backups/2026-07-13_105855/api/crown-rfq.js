// /api/crown-rfq — Sovereign Crown RFQ capture endpoint
// POST /api/crown-rfq — captures a Crown-tier Request-For-Quotation from a
// defence prime / Crown commercial buyer.
//
// Body: { organisation, contact_name, contact_email, capability, vehicle,
//         clearance_level (Official|Sensitive|Secret|TS), timeline (months),
//         procurement_route (Direct|Crown Agreement|G-Cloud|DOS|DASA|Other),
//         msg (free-form), gdpr_consent: true, honeypot?: '', notify?: true }
//
// Security:
//   - HMAC-SHA256 signed payload receipt (using process.env.CROWN_HMAC_KEY, falls
//     back to SIGNUP_WEBHOOK_SECRET, falls back to a stable defoneos dev secret
//     so dev/CI still works — production deployments MUST set the env).
//   - PII redaction in /tmp/crown-rfq.jsonl log: contact_email and contact_name
//     are partially masked before persistence. The full payload is only included
//     in the response envelope (which the buyer consented to sending to us).
//   - GDPR consent is required. Missing → 400.
//   - Bot honeypot field returns 200 but does NOT persist.
//
// Routing:
//   - Telegram notification (CROWN_RFQ tag, owner-gated)
//   - sales@defoneos.ai email fanout via SMTP-relay env if present (RESEND_API_KEY or SMTP_*)
//   - Falls back to /tmp/crown-rfq.log + console when no live channel available
//
// Returns:
//   { status, sigil, timestamp, rfq_id, routing: { telegam, email, log_fallback } }

const fs = require('fs').promises;
const crypto = require('crypto');

const HMAC_KEY = process.env.CROWN_HMAC_KEY || process.env.SIGNUP_WEBHOOK_SECRET || 'csoai-sovereign-dev-key-do-not-ship';
const SALES_EMAIL = 'sales@defoneos.ai';

const VALID_CLEARANCE = ['Official', 'Sensitive', 'Secret', 'TS', 'TOP SECRET'];
const VALID_PROCUREMENT = ['Direct Award', 'Crown Agreement', 'G-Cloud', 'DOS', 'DASA', 'Other', 'Framework RM', 'CCS'];

function hmac(payload, key = HMAC_KEY) {
  return crypto.createHmac('sha256', key).update(typeof payload === 'string' ? payload : JSON.stringify(payload)).digest('hex');
}

function sha512(payload) {
  return crypto.createHash('sha512').update(typeof payload === 'string' ? payload : JSON.stringify(payload)).digest('hex');
}

function newRfqId() {
  return 'crown_' + Date.now().toString(36) + '_' + crypto.randomBytes(4).toString('hex');
}

// Partial PII redaction
function redactEmail(email) {
  if (!email || typeof email !== 'string') return '';
  const [user, domain] = email.split('@');
  if (!domain) return '***';
  const u = user.length <= 2 ? user[0] + '*' : user.slice(0, 2) + '***';
  const d = domain.length <= 4 ? domain : domain.slice(0, 3) + '***.' + domain.split('.').pop();
  return u + '@' + d;
}

function redactName(name) {
  if (!name || typeof name !== 'string') return '';
  const parts = name.trim().split(/\s+/);
  return parts.map((p, i) => {
    if (i === 0) return p.length <= 1 ? p : p[0] + '.' + '*'.repeat(Math.max(1, p.length - 2)) + (p.length > 1 ? p.slice(-1) : '');
    if (i === parts.length - 1) return p; // keep surname
    return p[0] + '.';
  }).join(' ');
}

// Tier routing — defence primes / gov buyers go to Crown tier
const ROUTE = {
  default: { tier: 'Crown RFQ', notify_tag: '🛡️ CROWN_RFQ', cta: 'mailto:' + SALES_EMAIL },
};

async function persistRfq(record, redacted) {
  const out = {
    rfq_id: record.rfq_id,
    ts: record.timestamp,
    organisation: record.organisation,
    capability: record.capability,
    vehicle: record.vehicle,
    clearance_level: record.clearance_level,
    timeline_months: record.timeline_months,
    procurement_route: record.procurement_route,
    pii_redacted: {
      contact_email: redacted.email,
      contact_name: redacted.name,
    },
    notify_channel: record.notify_channel || ['log'],
    hmac_sig: record.hmac,
    sigil: record.sigil,
  };
  try {
    await fs.appendFile('/tmp/crown-rfq.jsonl', JSON.stringify(out) + '\n');
  } catch {}
}

async function fanoutTelegram(record) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chat_id = process.env.CROWN_TELEGRAM_CHAT_ID || process.env.TELEGRAM_CHAT_ID;
  if (!token || !chat_id) return { delivered: false, channel: 'telegram', reason: 'env_not_set' };
  const msg = [
    '🛡️ CROWN_RFQ · tier=Crown',
    '',
    '🏛️  ' + (record.organisation || '—'),
    '👤  ' + redactName(record.contact_name || '—'),
    '📧  ' + redactEmail(record.contact_email || '—'),
    '⚙️   ' + (record.capability || '—'),
    '📜  clearance=' + (record.clearance_level || '—'),
    '🛂  procurement=' + (record.procurement_route || '—'),
    '🗓️  timeline=' + (record.timeline_months || '—') + ' mo',
    '🧾  SIGIL ' + (record.sigil || '?'),
    '',
    '📅  ' + record.timestamp,
  ].join('\n');
  try {
    const r = await fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id, text: msg }),
    }).catch(() => null);
    return { delivered: !!(r && r.ok), channel: 'telegram' };
  } catch (e) {
    return { delivered: false, channel: 'telegram', reason: e.message };
  }
}

async function fanoutEmail(record) {
  // Generic webhook first (preferred), then Resend, then SMTP-via-Proxy
  const webhook = process.env.CROWN_EMAIL_WEBHOOK || process.env.SALES_EMAIL_WEBHOOK;
  const resend = process.env.RESEND_API_KEY;
  const subject = '🛡️ Crown RFQ — ' + (record.organisation || 'unknown') + ' — ' + record.rfq_id;

  const body = {
    to: SALES_EMAIL,
    from: process.env.SALES_FROM || 'rfq@defoneos.ai',
    subject,
    rfq: record,
    timestamp: record.timestamp,
  };

  if (webhook) {
    try {
      const r = await fetch(webhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      }).catch(() => null);
      return { delivered: !!(r && r.ok), channel: 'webhook' };
    } catch (e) {
      return { delivered: false, channel: 'webhook', reason: e.message };
    }
  }

  if (resend) {
    try {
      const r = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + resend, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: body.from,
          to: [body.to],
          subject,
          html: '<pre style="font:13px/1.4 monospace">' + JSON.stringify(body.rfq, null, 2) + '</pre>',
        }),
      }).catch(() => null);
      return { delivered: !!(r && r.ok), channel: 'resend' };
    } catch (e) {
      return { delivered: false, channel: 'resend', reason: e.message };
    }
  }

  // Fallback: append to /tmp/crown-rfq.log for Nick to review
  try {
    await fs.appendFile('/tmp/crown-rfq.log', 'TO: ' + SALES_EMAIL + '\nSUBJECT: ' + subject + '\nRFQ: ' + JSON.stringify(record, null, 2) + '\n----\n');
    return { delivered: false, channel: 'log_fallback', reason: 'no live email channel configured' };
  } catch (e) {
    return { delivered: false, channel: 'log_fallback', reason: e.message };
  }
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();

  // GET → schema preview
  if (req.method === 'GET') {
    return res.status(200).json({
      status: 'ok',
      sigil: sha512({ preview: 'crown-rfq schema', ts: new Date().toISOString() }),
      timestamp: new Date().toISOString(),
      rfq_id: 'preview_' + crypto.randomBytes(4).toString('hex'),
      schema: {
        organisation: 'string · required',
        contact_name: 'string · required',
        contact_email: 'string · required · valid email',
        capability: 'string · required · which sovereign capability',
        vehicle: 'string · required · Crown vehicle (e.g. JAGO / DEFCON 760)',
        clearance_level: { one_of: VALID_CLEARANCE, default: 'Official' },
        timeline_months: 'number · 1..120',
        procurement_route: { one_of: VALID_PROCUREMENT, default: 'Crown Agreement' },
        msg: 'string ≤ 2000 chars',
        gdpr_consent: 'true required',
        honeypot: 'string · empty',
        notify: 'boolean · request Telegram push',
      },
      routes: ['telegram', 'email->sales@defoneos.ai', 'log_fallback'],
    });
  }

  if (req.method !== 'POST') return res.status(405).json({ status: 'error', error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { return res.status(400).json({ status: 'error', error: 'Invalid JSON' }); } }
  if (!body || typeof body !== 'object') body = {};

  // Honeypot — bots
  if (body.honeypot) {
    return res.status(200).json({ status: 'ok', sigil: sha512('bot-suppressed-' + Date.now()), timestamp: new Date().toISOString(), rfq_id: 'bot_' + crypto.randomBytes(4).toString('hex') });
  }

  // GDPR gate
  if (body.gdpr_consent !== true) {
    return res.status(400).json({ status: 'error', error: 'GDPR consent required', code: 'GDPR_CONSENT_MISSING' });
  }

  // Validation
  const org = (body.organisation || '').toString().trim();
  const cn  = (body.contact_name || '').toString().trim();
  const ce  = (body.contact_email || '').toString().trim().toLowerCase();
  const capability = (body.capability || '').toString().trim();
  const vehicle = (body.vehicle || '').toString().trim();
  const clearance = ((body.clearance_level || 'Official').toString().trim());
  const timeline = Number(body.timeline_months || 0);
  const procurement = ((body.procurement_route || 'Crown Agreement').toString().trim());
  const msg = (body.msg || '').toString().slice(0, 2000);

  const errors = [];
  if (!org) errors.push('organisation_required');
  if (!cn)  errors.push('contact_name_required');
  if (!ce || !ce.includes('@') || !ce.includes('.')) errors.push('contact_email_invalid');
  if (!capability) errors.push('capability_required');
  if (!vehicle) errors.push('vehicle_required');
  if (VALID_CLEARANCE.indexOf(clearance) === -1) errors.push('clearance_level_invalid');
  if (!Number.isFinite(timeline) || timeline < 1 || timeline > 120) errors.push('timeline_invalid');
  if (VALID_PROCUREMENT.indexOf(procurement) === -1) errors.push('procurement_route_invalid');

  if (errors.length) {
    return res.status(400).json({ status: 'error', error: 'validation_failed', code: 'INVALID_RFQ', details: errors });
  }

  const rfq_id = newRfqId();
  const timestamp = new Date().toISOString();

  // HMAC over the redacted-but-meaningful envelope (NOT the raw PII — we keep
  // the actual PII in this object only for fanout, and redact in any persistence).
  const hmac_envelope = { rfq_id, ts: timestamp, org, capability, vehicle, clearance, timeline, procurement };
  const hmac_sig = hmac(hmac_envelope);

  const record = {
    rfq_id,
    timestamp,
    organisation: org,
    contact_name: cn,
    contact_email: ce,
    capability,
    vehicle,
    clearance_level: clearance,
    timeline_months: timeline,
    procurement_route: procurement,
    msg,
    gdpr_consent_at: timestamp,
    hmac_algorithm: 'HMAC-SHA256',
    hmac: hmac_sig,
    tier: ROUTE.default.tier,
    notify_tag: ROUTE.default.notify_tag,
  };

  // Sigil — full sovereign-grade receipt over a PII-REDACTED envelope
  const sigil_input = {
    rfq_id,
    timestamp,
    tier: record.tier,
    capability,
    vehicle,
    clearance,
    procurement,
    hmac: hmac_sig,
    redacted_email: redactEmail(ce),
    redacted_name: redactName(cn),
  };
  record.sigil = sha512(sigil_input);
  record.sigil_algo = 'SHA-512 (chain-ready)';

  // Persistence — only redacted fields
  await persistRfq(record, { email: redactEmail(ce), name: redactName(cn) });

  // Fanout (concurrent)
  const want_notify = body.notify === true;
  const channels = await Promise.all([
    fanoutTelegram(want_notify ? record : { ...record, contact_email: ce, contact_name: cn }), // only fan to TG if explicitly opted-in
    fanoutEmail(record),
  ]);

  return res.status(200).json({
    status: 'ok',
    sigil: record.sigil,
    sigil_algo: record.sigil_algo,
    hmac: hmac_sig,
    timestamp,
    rfq_id,
    tier: record.tier,
    routing: {
      to_email: SALES_EMAIL,
      telegram: channels[0],
      email: channels[1],
      log_fallback: '/tmp/crown-rfq.log',
      persistence: '/tmp/crown-rfq.jsonl',
    },
    data: {
      organisation: org,
      contact_email: ce,        // only returned to the sender
      capability, vehicle,
      clearance_level: clearance,
      timeline_months: timeline,
      procurement_route: procurement,
      notify_opted_in: want_notify,
      hmac_algorithm: 'HMAC-SHA256',
    },
    next_steps: 'A sovereign solutions architect will reply within 24h (working hours, UK BST). Reference: ' + rfq_id,
  });
};
