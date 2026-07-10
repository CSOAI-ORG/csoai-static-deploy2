// /api/daily-golden — Daily E2E golden test for the entire DEFONEOS surface
// Cron-driven. Hits every page + every endpoint. Returns structured pass/fail. Posts to Telegram if configured.
//
// HONESTY: Results are real (live HTTP requests to csoai-static-deploy2.vercel.app). No fabrication.
// Time budget: <8s end-to-end. Designed to run every 4 hours during EAT mode.

const https = require('https');

const PAGES = [
  '/', '/defoneos-signup-hub', '/defoneos-defence-primes', '/defoneos-regulators', '/defoneos-seriesa',
  '/sov3-oowm-all-models', '/defoneos-system-card', '/defoneos-academy', '/defoneos-press',
  '/defoneos-framing', '/distribution-pack', '/defoneos-healthcare', '/defoneos-finance',
  '/defoneos-cyber', '/defoneos-investor-onepager', '/defoneos-crown-agreement',
  '/defoneos-gap-analysis', '/defoneos-evidence-vault', '/defoneos-33-bft-council',
];

const API_ENDPOINTS = [
  { method: 'GET', path: '/api/stats' },
  { method: 'GET', path: '/api/sigil-status' },
  { method: 'GET', path: '/api/oscal?format=json' },
  { method: 'GET', path: '/api/sovereign-citations' },
  { method: 'GET', path: '/api/framing' },
  { method: 'GET', path: '/api/invite' },
  { method: 'GET', path: '/api/persist' },
  { method: 'POST', path: '/api/signup', body: JSON.stringify({ email: 'golden-test@csoai.org', persona: 'academic', tier: 'Open Source', gdpr_consent: true, honeypot: '' }) },
  { method: 'POST', path: '/api/welcome', body: JSON.stringify({ record: { sigil: 'sig_golden', email: 'golden-test@csoai.org', persona: 'academic', tier: 'Open Source', timestamp: new Date().toISOString() } }) },
  { method: 'POST', path: '/api/newsletter', body: JSON.stringify({ email: 'golden-test@csoai.org', gdpr_consent: true, source: 'golden-test' }) },
];

function fetch_p(url, method = 'GET', body) {
  return new Promise((resolve) => {
    const start = Date.now();
    const u = new URL(url);
    const opts = { method, headers: { 'Content-Type': 'application/json' }, timeout: 5000 };
    const req = https.request(url, opts, (res) => {
      let data = '';
      res.on('data', (c) => data += c);
      res.on('end', () => resolve({
        path: url.replace('https://csoai-static-deploy2.vercel.app', ''),
        method,
        status: res.statusCode,
        latency_ms: Date.now() - start,
        body_len: data.length,
        body_head: data.slice(0, 200),
        ok: res.statusCode >= 200 && res.statusCode < 400,
      }));
    });
    req.on('timeout', () => { req.destroy(); resolve({ path: url, method, status: 0, latency_ms: 5000, ok: false, error: 'timeout' }); });
    req.on('error', (e) => resolve({ path: url, method, status: 0, latency_ms: Date.now() - start, ok: false, error: e.code || e.message }));
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const base = 'https://csoai-static-deploy2.vercel.app';
  const t0 = Date.now();
  const pageResults = await Promise.all(PAGES.map((p) => fetch_p(base + p, 'GET')));
  const apiResults = await Promise.all(API_ENDPOINTS.map((e) => fetch_p(base + e.path, e.method, e.body)));
  const total_ms = Date.now() - t0;

  const all = [...pageResults, ...apiResults];
  const pass = all.filter((r) => r.ok).length;
  const fail = all.length - pass;

  const summary = {
    ok: fail === 0,
    timestamp: new Date().toISOString(),
    total_ms,
    pass,
    fail,
    total_checks: all.length,
    pages: pageResults.map(r => ({ path: r.path, status: r.status, latency_ms: r.latency_ms, ok: r.ok })),
    endpoints: apiResults.map(r => ({ path: r.path, method: r.method, status: r.status, latency_ms: r.latency_ms, ok: r.ok, body_head: r.body_head })),
    failed: all.filter(r => !r.ok).map(r => ({ path: r.path, status: r.status, error: r.error })),
  };

  // Append to /tmp/golden.log
  try {
    const fs = require('fs').promises;
    const line = JSON.stringify({ ts: summary.timestamp, pass, fail, total_ms, total_checks: all.length, failed: summary.failed }) + '\n';
    await fs.appendFile('/tmp/golden.log', line).catch(() => {});
  } catch (e) {}

  // Notify Telegram on failures
  if (fail > 0 && process.env.TELEGRAM_BOT_TOKEN && process.env.TELEGRAM_CHAT_ID) {
    try {
      const txt = `⚠️ DEFONEOS golden test: ${fail} failures\n${summary.failed.map(f => f.path).join('\n')}`;
      await fetch(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: process.env.TELEGRAM_CHAT_ID, text: txt }),
      }).catch(() => {});
    } catch (e) {}
  }

  res.status(fail === 0 ? 200 : 503).json(summary);
};
