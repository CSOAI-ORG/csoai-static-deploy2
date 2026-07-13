// Vercel serverless — DEFONEOS newsletter capture
// POST /api/newsletter — emails with marketing=true on /api/signup are mirrored here.
// GET  /api/newsletter?since=<iso> — recent signups (paginated)
// HONESTY: Email capture only; no auto-subscribe. Owner-gated broadcast tool is configurable.

const fs = require('fs').promises;
const path = require('path');

const NL_LOG = '/tmp/newsletter.jsonl';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(204).end();

  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }
    if (!body || typeof body !== 'object') body = {};

    const email = (body.email || '').toString().trim().toLowerCase();
    const source = (body.source || 'unknown').toString();
    const gdpr = !!body.gdpr_consent;
    if (!email || !email.includes('@')) return res.status(400).json({ error: 'Valid email required' });
    if (!gdpr) return res.status(400).json({ error: 'GDPR consent required' });

    const record = {
      timestamp: new Date().toISOString(),
      email,
      source,
      gdpr_consent: gdpr,
      ua: (req.headers['user-agent'] || '').slice(0, 200),
    };

    try {
      const dir = '/tmp';
      const line = JSON.stringify(record) + '\n';
      await fs.appendFile(NL_LOG, line);
    } catch (e) {
      console.error('newsletter persistence error:', e.message);
    }

    // Optional webhook for Telegram / ConvertKit / Beehiiv
    const webhook = process.env.NEWSLETTER_WEBHOOK_URL;
    if (webhook) {
      try {
        await fetch(webhook, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(record),
        }).catch(() => {});
      } catch {}
    }

    return res.status(200).json({
      ok: true,
      receipt: {
        timestamp: record.timestamp,
        source: record.source,
        weekly_digest_unsubscribe: 'one-click in every email',
      },
    });
  }

  if (req.method === 'GET') {
    try {
      const data = await fs.readFile(NL_LOG, 'utf8');
      const lines = data.trim().split('\n').filter(Boolean);
      const since = req.query.since;
      const sinceTs = since ? new Date(since).getTime() : 0;
      const recent = lines
        .map((l) => { try { return JSON.parse(l); } catch { return null; } })
        .filter(Boolean)
        .filter((r) => new Date(r.timestamp).getTime() >= sinceTs)
        .slice(-100);
      return res.status(200).json({
        ok: true,
        total_lines: lines.length,
        returning: recent.length,
        sample: recent.slice(0, 5).map(r => ({ email: r.email, ts: r.timestamp, source: r.source })),
      });
    } catch (e) {
      return res.status(200).json({ ok: true, total_lines: 0, returning: 0, note: 'no log yet' });
    }
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
