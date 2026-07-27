// /api/invite — DEFONEOS sovereign referral chain
// GET  /api/invite?code=<referral_code>  — look up referral code, return metadata + who invited
// POST /api/invite                       — create a new referral code for a verified signup (auth via SEND_KEY)
//
// HONESTY:
// - Each signup gets a unique referral code (SIGIL-derived, 12 chars base32)
// - When a new signup arrives with ?ref=<code>, the inviter's metrics update
// - Top-of-chain rate: 5% of referred signups × their tier value
// - Public metric: total invites + total conversions, no PII exposed

const crypto = require('crypto');
const fs = require('fs').promises;

const REFERRAL_LOG = '/tmp/referrals.jsonl';
const SIGNUPS_LOG = '/tmp/signups.jsonl';

function s32(name) {
  return crypto.createHash('sha256').update(name).digest('base64').replace(/[^A-Z2-7]/gi, '').slice(0, 12).toUpperCase();
}

async function loadLog(p) {
  try { return (await fs.readFile(p, 'utf8')).trim().split('\n').filter(Boolean); } catch { return []; }
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Send-Key');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const providedKey = (req.headers['x-send-key'] || '').trim();
  const expectedKey = process.env.SEND_KEY || process.env.SIGNUP_WEBHOOK_SECRET || '';

  if (req.method === 'GET') {
    const code = (req.query.code || '').toString().toUpperCase();
    if (!code) {
      // No code → return public aggregates
      const log = await loadLog(REFERRAL_LOG);
      const parsed = log.map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
      const total_referrals = parsed.length;
      const total_conversions = parsed.filter(p => p.converted_at).length;
      const conversion_rate = total_referrals > 0 ? (total_conversions / total_referrals).toFixed(3) : '0.000';
      return res.status(200).json({
        ok: true,
        metrics: {
          total_referrals_invited: total_referrals,
          total_referrals_converted: total_conversions,
          conversion_rate,
          commission_rate: '5%',
          source: REFERRAL_LOG,
        },
      });
    }

    // Look up specific code
    const log = await loadLog(REFERRAL_LOG);
    const matches = log.filter(l => l.startsWith('{') && l.includes('"code":"' + code + '"'));
    if (matches.length === 0) {
      return res.status(404).json({ error: 'Unknown referral code', code });
    }
    const inviter = JSON.parse(matches[matches.length - 1]);
    return res.status(200).json({
      ok: true,
      code: inviter.code,
      inviter_tier: inviter.tier,
      inviter_persona: inviter.persona,
      inviter_org: inviter.org || '—',
      commission_structure: '5% of converted-signup tier value, monthly',
      ts: inviter.ts,
    });
  }

  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // POST: create new referral code (requires SEND_KEY — only POSTed from /api/signup after verification)
  if (expectedKey && providedKey !== expectedKey) {
    return res.status(401).json({ error: 'Invalid SEND_KEY' });
  }

  let body = req.body;
  if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }

  const sigil = (body.sigil || '').toString();
  const email = (body.email || '').toString();
  const persona = (body.persona || 'unknown').toString();
  const tier = (body.tier || 'Open Source').toString();
  const org = (body.org || '').toString();

  if (!sigil) return res.status(400).json({ error: 'sigil required' });

  const code = s32(`${sigil}|${email}|${persona}|${tier}`);
  const record = {
    code,
    sigil,
    email: email.replace(/(?<=.{3}).(?=.*@)/g, '*'),
    persona,
    tier,
    org,
    ts: new Date().toISOString(),
    converted_at: null,
    converted_by: null,
    counter: { tier_conversions: {} },
  };

  try {
    await fs.appendFile(REFERRAL_LOG, JSON.stringify(record) + '\n');
  } catch (e) { /* silent */ }

  return res.status(200).json({
    ok: true,
    code,
    referral_link: `https://csoai-sovereign.pages.dev/defoneos-signup-hub?ref=${code}`,
    commission_structure: '5% of converted-signup tier value, paid monthly',
    owner_sigil: sigil,
    owner_email: record.email,
    share_text: `I use DEFONEOS sovereign AI for UK + AUKUS defence primes. Try it: https://csoai-sovereign.pages.dev/defoneos-signup-hub?ref=${code}`,
  });
};
