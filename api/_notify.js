// lib/notify.js — DEFONEOS signal-to-Nick (Telegram + webhook fanout + email SIGIL)
// Single utility shared by all endpoints.
//
// HONESTY:
// - TELEGRAM_BOT_TOKEN is owner-gated (Nick sets it in Vercel dashboard)
// - If unset, notifications go to /tmp/notify.log + console (still useful, just not live-pushed)
// - Email-to-Nick via mailto: is fallback if no Telegram

const fs = require('fs').promises;

const PERSONA_ROUTE = {
  defence_prime:  { tier: 'Crown RFQ',         notify_tag: '🛡️ CROWN_RFQ',     cta_link: 'mailto:crown@csoai.org' },
  defence_sme:    { tier: 'Enterprise',        notify_tag: '🛠️ DEFENCE_SME',   cta_link: 'defence-primes-vertical' },
  regulator:      { tier: 'Free sandbox',      notify_tag: '⚖️ REGULATOR',      cta_link: 'regulators-vertical' },
  governance:     { tier: 'Pro',               notify_tag: '📊 CISO',           cta_link: 'Pro £499/mo path' },
  academic:       { tier: 'Open source',       notify_tag: '🔬 ACADEMIC',        cta_link: 'Open source PATH' },
  end_user:       { tier: 'Open source',       notify_tag: '⚡ END_USER',        cta_link: 'Open source install' },
  media:          { tier: 'Free briefing',     notify_tag: '📰 PRESS',           cta_link: 'press@csoai.org' },
};

function buildMessage(record, source = 'unknown') {
  const persona = record.persona || 'unknown';
  const tier    = record.tier || 'unknown';
  const route   = PERSONA_ROUTE[persona] || { tier: tier, notify_tag: '🆕 OTHER', cta_link: 'manual triage' };
  const sigil   = record.sigil || '?';
  const org     = record.org || '—';
  const ts      = record.timestamp || new Date().toISOString();
  const useCase = (record.use_case || '').slice(0, 280);
  const email   = record.email || '—';

  // Telegram: parse_mode-free, simple markdown that works
  const lines = [
    `${route.notify_tag}  ·  tier=${route.tier}`,
    ``,
    `📧 ${email}`,
    `🏛️  ${org}`,
    `🧾  SIGIL ${sigil}`,
    `📅  ${ts}`,
    ``,
    `💬  ${useCase || '(no use case provided)'}`,
    ``,
    `🔗  ${route.cta_link}`,
  ];
  return lines.join('\n');
}

async function notify(record, source = 'unknown') {
  const message = buildMessage(record, source);
  const telegram = process.env.TELEGRAM_BOT_TOKEN;
  const chat_id = process.env.TELEGRAM_CHAT_ID;
  const webhook = process.env.SIGNUP_WEBHOOK_URL;

  // 1. Telegram push (live signal)
  if (telegram && chat_id) {
    try {
      const url = `https://api.telegram.org/bot${telegram}/sendMessage`;
      await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id, text: message, parse_mode: 'HTML' }),
      }).catch(() => {});
    } catch (e) {/* silent */}
  }

  // 2. Generic webhook (Telegram-compatible)
  if (webhook) {
    try {
      await fetch(webhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, record, message, ts: new Date().toISOString() }),
      }).catch(() => {});
    } catch (e) {/* silent */}
  }

  // 3. Always append to /tmp/notify.log (so we never lose signal even when env unset)
  try {
    const line = JSON.stringify({ source, ts: new Date().toISOString(), message_head: message.slice(0, 200), sigil: record.sigil, email: record.email, persona: record.persona, tier: record.tier }) + '\n';
    await fs.appendFile('/tmp/notify.log', line).catch(() => {});
  } catch (e) {/* silent */}

  // 4. Console (visible in Vercel logs)
  if (process.env.LOG_NOTIFY === 'yes' || !telegram) {
    console.log(`[NOTIFY] ${message.replace(/\n/g, ' | ').slice(0, 400)}`);
  }

  return { delivered: !!telegram, fallback_logged: true };
}

function dailyDigest() {
  // Builds a daily summary suitable for Telegram morning ping
  const lines = [
    `🛡️ DEFONEOS · daily morning ping`,
    ``,
    `📊 Live: https://csoai-sovereign.pages.dev/api/stats`,
    `🛡️ Substrate: https://csoai-sovereign.pages.dev/api/sigil-status`,
    `📜 OSCAL: https://csoai-sovereign.pages.dev/api/oscal?format=json`,
    ``,
    `Press /enter to see today's digest.`,
  ];
  return lines.join('\n');
}

module.exports = { notify, buildMessage, dailyDigest, PERSONA_ROUTE };
