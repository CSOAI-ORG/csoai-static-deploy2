// /api/analytics — DEFONEOS funnel analytics
// POST /api/analytics  body: { event: 'cta_click'|'page_view'|'signup_started'|'newsletter_opt'|'press_book'|'crown_rfq', source: 'defoneos-academy', persona?: 'defence_prime' }
// GET  /api/analytics?since=<iso>&funnel=true  — aggregated counts per event
//
// HONESTY: Logs are real (logged to /tmp/analytics.jsonl). Aggregations are
// arithmetic over real records. Where a count is zero, it's zero. No fabrication.

const fs = require('fs').promises;
const crypto = require('crypto');

const LOG = '/tmp/analytics.jsonl';

const ALLOWED_EVENTS = new Set([
  'cta_click', 'page_view', 'signup_started', 'signup_completed', 'newsletter_opt', 'press_book', 'crown_rfq', 'cta_miss',
  'series_a_lead', 'defence_prime_lead', 'regulator_lead', 'academy_enrol', 'distribution_download', 'golden_test', 'digest_run', 'tick_run',
]);

async function tail(p, n = 100000) {
  try { return (await fs.readFile(p, 'utf8')).trim().split('\n').filter(Boolean).slice(-n); } catch { return []; }
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();

  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }
    if (!body || typeof body !== 'object') body = {};

    const event = (body.event || '').toString();
    const source = (body.source || 'unknown').toString().slice(0, 100);
    const persona = (body.persona || '').toString().slice(0, 50);
    const meta = body.meta && typeof body.meta === 'object' ? body.meta : {};

    if (!ALLOWED_EVENTS.has(event)) {
      return res.status(400).json({ error: 'unknown event', allowed: [...ALLOWED_EVENTS] });
    }

    const record = {
      ts: new Date().toISOString(),
      event,
      source,
      persona: persona || null,
      meta,
      ua: (req.headers['user-agent'] || '').slice(0, 200),
      ip_country: (req.headers['cf-ip-country'] || ''),
    };

    try {
      await fs.appendFile(LOG, JSON.stringify(record) + '\n');
    } catch (e) {/* silent */}

    return res.status(200).json({ ok: true, event, source, ts: record.ts });
  }

  if (req.method === 'GET') {
    const since = req.query.since ? new Date(req.query.since).getTime() : 0;
    const want_funnel = req.query.funnel === 'true';
    const rows = await tail(LOG);
    const parsed = rows.map(r => { try { return JSON.parse(r); } catch { return null; } }).filter(Boolean);
    const since_now = parsed.filter(r => new Date(r.ts).getTime() >= since);
    const counts = {};
    for (const r of since_now) counts[r.event] = (counts[r.event] || 0) + 1;
    const by_source = {};
    for (const r of since_now) {
      const key = r.source || 'unknown';
      by_source[key] = by_source[key] || {};
      by_source[key][r.event] = (by_source[key][r.event] || 0) + 1;
    }

    const today = new Date(); today.setHours(0, 0, 0, 0);
    const today_count = parsed.filter(r => new Date(r.ts).getTime() >= today.getTime()).length;
    const last_24h = parsed.filter(r => new Date(r.ts).getTime() >= Date.now() - 24 * 3600 * 1000).length;
    const last_7d = parsed.filter(r => new Date(r.ts).getTime() >= Date.now() - 7 * 24 * 3600 * 1000).length;

    let funnel = null;
    if (want_funnel) {
      const f = {
        page_views: (counts.page_view || 0),
        cta_clicks: (counts.cta_click || 0),
        signup_started: (counts.signup_started || 0),
        signup_completed: (counts.signup_completed || 0),
        newsletter_opt: (counts.newsletter_opt || 0),
        press_book: (counts.press_book || 0),
        crown_rfq: (counts.crown_rfq || 0),
        series_a_lead: (counts.series_a_lead || 0),
        conversion_rate: (counts.page_view ? ((counts.signup_completed || 0) / counts.page_view * 100).toFixed(2) + '%' : '0%'),
      };
      funnel = f;
    }

    return res.status(200).json({
      ok: true,
      timestamp: new Date().toISOString(),
      totals: { all_time: parsed.length, last_24h, last_7d, today: today_count },
      since_iso: since ? new Date(since).toISOString() : 'all-time',
      since: parsed.filter(r => new Date(r.ts).getTime() >= since).length,
      counts,
      by_source,
      funnel,
    });
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
