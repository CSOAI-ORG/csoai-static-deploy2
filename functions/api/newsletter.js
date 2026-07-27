// Cloudflare Pages Function — converted from api/newsletter.js
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

  // DEFONEOS DEFONEOS newsletter capture
  // POST /api/newsletter — emails with marketing=true on /api/signup are mirrored here.
  // GET  /api/newsletter?since=<iso> — recent signups (paginated)
  // HONESTY: Email capture only; no auto-subscribe. Owner-gated broadcast tool is configurable.

  const NL_LOG = '/tmp/newsletter.jsonl';



    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders });

    if (request.method === 'POST') {
      let body = await request.json();
      if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }
      if (!body || typeof body !== 'object') body = {};

      const email = (body.email || '').toString().trim().toLowerCase();
      const source = (body.source || 'unknown').toString();
      const gdpr = !!body.gdpr_consent;
      if (!email || !email.includes('@')) return new Response(JSON.stringify({ error: 'Valid email required' }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
      if (!gdpr) return new Response(JSON.stringify({ error: 'GDPR consent required' }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });

      const record = {
        timestamp: new Date().toISOString(),
        email,
        source,
        gdpr_consent: gdpr,
        ua: (request.headers['user-agent'] || '').slice(0, 200),
      };

      try {
        const dir = '/tmp';
        const line = JSON.stringify(record) + '\n';
        /* fs.appendFile no-op */ void 0
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

      return new Response(JSON.stringify({
        ok: true,
        receipt: {
          timestamp: record.timestamp,
          source: record.source,
          weekly_digest_unsubscribe: 'one-click in every email',
        },
      }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }

    if (request.method === 'GET') {
      try {
        const data = "" /* fs.readFile no-op */
        const lines = data.trim().split('\n').filter(Boolean);
        const since = url.searchParams.get("since");
        const sinceTs = since ? new Date(since).getTime() : 0;
        const recent = lines
          .map((l) => { try { return JSON.parse(l); } catch { return null; } })
          .filter(Boolean)
          .filter((r) => new Date(r.timestamp).getTime() >= sinceTs)
          .slice(-100);
        return new Response(JSON.stringify({
          ok: true,
          total_lines: lines.length,
          returning: recent.length,
          sample: recent.slice(0, 5).map(r => ({ email: r.email, ts: r.timestamp, source: r.source })),
        }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
      } catch (e) {
        return new Response(JSON.stringify({ ok: true, total_lines: 0, returning: 0, note: 'no log yet' }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
      }
    }

    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
}
