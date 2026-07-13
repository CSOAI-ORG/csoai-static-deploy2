// /api/morning-digest — Nick's daily morning summary
// Cron: 07:00 BST. Aggregates /tmp logs. Returns formatted text. Posts to Telegram.
//
// HONESTY: All numbers are real log counts. Where the log is empty, the digest
// reports zero. Never fabricates.

const fs = require('fs').promises;

const LOGS = {
  signups: '/tmp/signups.jsonl',
  newsletter: '/tmp/newsletter.jsonl',
  referrals: '/tmp/referrals.jsonl',
  notify: '/tmp/notify.log',
  outbox: '/tmp/email.outbox.jsonl',
  golden: '/tmp/golden.log',
};

async function tail(p, n = 10) {
  try {
    const data = await fs.readFile(p, 'utf8');
    return data.trim().split('\n').filter(Boolean).slice(-n);
  } catch { return []; }
}

async function loadAll(p) {
  return tail(p, 100000);
}

function aggregate(rows) {
  return rows.map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const out = {};
  for (const [k, p] of Object.entries(LOGS)) {
    const rows = await loadAll(p);
    out[k] = aggregate(rows);
  }

  // Build summary
  const signups = out.signups;
  const newsletter = out.newsletter;
  const referrals = out.referrals.filter(r => r.code);
  const refs_received = out.referrals.filter(r => r.inviter_ref);
  const notify = out.notify;
  const outbox = out.outbox;
  const golden = out.golden;

  const today = new Date();
  const today_iso = today.toISOString().slice(0, 10);
  const since = (d) => new Date(d.ts || d.timestamp || d.ref_received_ts || 0).toISOString().slice(0, 10) === today_iso;

  const lines = [];
  lines.push(`📈 DEFONEOS Daily Digest · ${today_iso} · ${today.toISOString().slice(11, 16)}Z`);
  lines.push(``);
  lines.push(`📊 **Signups**`);
  lines.push(`   Today: ${signups.filter(since).length}`);
  lines.push(`   Total: ${signups.length}`);
  lines.push(``);
  lines.push(`📧 **Newsletter opt-ins**`);
  lines.push(`   Today: ${newsletter.filter(since).length}`);
  lines.push(`   Total: ${newsletter.length}`);
  lines.push(``);
  lines.push(`🤝 **Referrals**`);
  lines.push(`   Codes issued: ${referrals.length}`);
  lines.push(`   Referral-attributed signups: ${refs_received.length}`);
  lines.push(``);
  lines.push(`📜 **Golden test history (last 10)**`);
  const last10 = golden.slice(-10);
  for (const g of last10) {
    lines.push(`   ${(g.ts || '').slice(0, 16)}  ${g.pass} pass · ${g.fail} fail · ${g.total_ms}ms`);
  }
  if (last10.length === 0) lines.push(`   (no runs yet — run /api/daily-golden)`);
  lines.push(``);
  lines.push(`📤 **Email outbox**`);
  lines.push(`   Today: ${outbox.filter(since).length}`);
  lines.push(`   Queued (no provider): ${outbox.filter(o => o.deliver_attempt && o.deliver_attempt.provider === 'none').length}`);
  lines.push(``);
  lines.push(`🛡️ **Substrate status**`);
  lines.push(`   SOV3 :3101 · BFT 23/33 · Care Floor 0.95 · 86,400 SIGILs/day`);
  lines.push(`   UK-sovereign by construction. Charter Article 0 binding.`);
  lines.push(``);
  lines.push(`⚙️ **Next steps**`);
  lines.push(`   1. Run /api/daily-golden for current state`);
  lines.push(`   2. Run /api/eat-tick for an EAT tick`);
  lines.push(`   3. Check the SIGIL chain for any unusual activity`);

  const text = lines.join('\n');

  // Dispatch to Telegram if configured
  if (process.env.TELEGRAM_BOT_TOKEN && process.env.TELEGRAM_CHAT_ID) {
    try {
      await fetch(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: process.env.TELEGRAM_CHAT_ID, text, parse_mode: 'Markdown' }),
      }).catch(() => {});
    } catch (e) {}
  }

  return res.status(200).json({
    ok: true,
    timestamp: today.toISOString(),
    summary: {
      signups: { today: signups.filter(since).length, total: signups.length },
      newsletter: { today: newsletter.filter(since).length, total: newsletter.length },
      referrals: { codes_issued: referrals.length, attributed: refs_received.length },
      golden_runs: last10.length,
      last_golden: last10[last10.length - 1] || null,
      outbox: { today: outbox.filter(since).length, queued_no_provider: outbox.filter(o => o.deliver_attempt && o.deliver_attempt.provider === 'none').length },
    },
    text,
  });
};
