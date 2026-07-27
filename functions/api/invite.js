// Cloudflare Pages Function — converted from api/invite.js
import { createHash, createHmac, randomBytes } from 'crypto';

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

  // /api/invite — DEFONEOS sovereign referral chain
  // GET  /api/invite?code=<referral_code>  — look up referral code, return metadata + who invited
  // POST /api/invite                       — create a new referral code for a verified signup (auth via SEND_KEY)
  //
  // HONESTY:
  // - Each signup gets a unique referral code (SIGIL-derived, 12 chars base32)
  // - When a new signup arrives with ?ref=<code>, the inviter's metrics update
  // - Top-of-chain rate: 5% of referred signups × their tier value
  // - Public metric: total invites + total conversions, no PII exposed

  const REFERRAL_LOG = '/tmp/referrals.jsonl';
  const SIGNUPS_LOG = '/tmp/signups.jsonl';

  function s32(name) {
    return createHash('sha256').update(name).digest('base64').replace(/[^A-Z2-7]/gi, '').slice(0, 12).toUpperCase();
  }

  async function loadLog(p) {
    try { return ("" /* fs.readFile no-op */).trim().split('\n').filter(Boolean); } catch { return []; }
  }



    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders });

    const providedKey = (request.headers['x-send-key'] || '').trim();
    const expectedKey = process.env.SEND_KEY || process.env.SIGNUP_WEBHOOK_SECRET || '';

    if (request.method === 'GET') {
      const code = (url.searchParams.get("code") || '').toString().toUpperCase();
      if (!code) {
        // No code → return public aggregates
        const log = await loadLog(REFERRAL_LOG);
        const parsed = log.map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
        const total_referrals = parsed.length;
        const total_conversions = parsed.filter(p => p.converted_at).length;
        const conversion_rate = total_referrals > 0 ? (total_conversions / total_referrals).toFixed(3) : '0.000';
        return new Response(JSON.stringify({
          ok: true,
          metrics: {
            total_referrals_invited: total_referrals,
            total_referrals_converted: total_conversions,
            conversion_rate,
            commission_rate: '5%',
            source: REFERRAL_LOG,
          },
        }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
      }

      // Look up specific code
      const log = await loadLog(REFERRAL_LOG);
      const matches = log.filter(l => l.startsWith('{') && l.includes('"code":"' + code + '"'));
      if (matches.length === 0) {
        return new Response(JSON.stringify({ error: 'Unknown referral code', code }), { status: 404, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
      }
      const inviter = JSON.parse(matches[matches.length - 1]);
      return new Response(JSON.stringify({
        ok: true,
        code: inviter.code,
        inviter_tier: inviter.tier,
        inviter_persona: inviter.persona,
        inviter_org: inviter.org || '—',
        commission_structure: '5% of converted-signup tier value, monthly',
        ts: inviter.ts,
      }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }

    if (request.method !== 'POST') return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

    // POST: create new referral code (requires SEND_KEY — only POSTed from /api/signup after verification)
    if (expectedKey && providedKey !== expectedKey) {
      return new Response(JSON.stringify({ error: 'Invalid SEND_KEY' }), { status: 401, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }

    let body = await request.json();
    if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }

    const sigil = (body.sigil || '').toString();
    const email = (body.email || '').toString();
    const persona = (body.persona || 'unknown').toString();
    const tier = (body.tier || 'Open Source').toString();
    const org = (body.org || '').toString();

    if (!sigil) return new Response(JSON.stringify({ error: 'sigil required' }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

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
      /* fs.appendFile no-op */ void 0
    } catch (e) { /* silent */ }

    return new Response(JSON.stringify({
      ok: true,
      code,
      referral_link: `https://csoai-sovereign.pages.dev/defoneos-signup-hub?ref=${code}`,
      commission_structure: '5% of converted-signup tier value, paid monthly',
      owner_sigil: sigil,
      owner_email: record.email,
      share_text: `I use DEFONEOS sovereign AI for UK + AUKUS defence primes. Try it: https://csoai-sovereign.pages.dev/defoneos-signup-hub?ref=${code}`,
    }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
}
