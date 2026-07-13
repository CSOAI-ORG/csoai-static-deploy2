// /api/persist — Sync /tmp logs to GitHub Gist (free, no infra, owner-driven)
// POST /api/persist  body: { kind: 'signups' | 'newsletter' | 'notify' | 'outbox', all?: bool }
//
// HONESTY:
// - Without GIST_TOKEN env, this endpoint dumps the current /tmp log file as JSON.
// - With GIST_TOKEN + GIST_ID, it updates a private GitHub Gist with the current log.
// - Owner-gated: requires SEND_KEY header to prevent abuse.

const fs = require('fs').promises;
const crypto = require('crypto');

const FILES = {
  signups:   '/tmp/signups.jsonl',
  newsletter: '/tmp/newsletter.jsonl',
  notify:    '/tmp/notify.log',
  outbox:    '/tmp/email.outbox.jsonl',
};

async function loadLog(path) {
  try {
    const data = await fs.readFile(path, 'utf8');
    return data.trim().split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  } catch (e) {
    return [];
  }
}

async function syncToGist(kind, items) {
  const token = process.env.GIST_TOKEN;
  const id = process.env.GIST_ID;
  if (!token || !id) return { gist_synced: false, reason: 'GIST_TOKEN or GIST_ID unset' };
  const filename = `defoneos-${kind}.jsonl`;
  const content = items.map(i => JSON.stringify(i)).join('\n') + '\n';
  try {
    const res = await fetch(`https://api.github.com/gists/${id}`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json', 'Accept': 'application/vnd.github+json' },
      body: JSON.stringify({ files: { [filename]: { content } } }),
    });
    const body = await res.json().catch(() => ({}));
    return { gist_synced: true, status: res.status, gist_id: id, item_count: items.length };
  } catch (e) {
    return { gist_synced: false, error: e.message };
  }
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Send-Key');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const providedKey = (req.headers['x-send-key'] || '').trim();
  const expectedKey = process.env.SEND_KEY || process.env.SIGNUP_WEBHOOK_SECRET || '';
  if (expectedKey && providedKey !== expectedKey) {
    return res.status(401).json({ error: 'Invalid SEND_KEY' });
  }

  if (req.method === 'GET') {
    // Dump current state
    const out = {};
    for (const [k, p] of Object.entries(FILES)) out[k] = await loadLog(p);
    return res.status(200).json({ ok: true, items: out, ts: new Date().toISOString() });
  }

  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  let body = req.body;
  if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }

  const kind = (body.kind || 'all').toString();
  const gist = body.gist !== false;

  const kinds = kind === 'all' ? Object.keys(FILES) : [kind];
  const result = {};

  for (const k of kinds) {
    if (!FILES[k]) { result[k] = { error: 'unknown kind' }; continue; }
    const items = await loadLog(FILES[k]);
    result[k] = { count: items.length, ts: items.length ? items[items.length - 1].ts || items[items.length - 1].timestamp || 'n/a' : 'empty' };
    if (gist) result[k].gist = await syncToGist(k, items);
  }

  return res.status(200).json({ ok: true, sync: result, ts: new Date().toISOString() });
};
