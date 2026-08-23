#!/usr/bin/env node
// eunomia-gateway.mjs — OpenAI-compatible gateway over the RunPod serverless endpoints.
// "Run open-source models on OURS": one API, one key; models run on the RunPod fleet.
// Billing/commission hook: every call is logged (usage -> commission ledger).
const http = require('node:http');

const https = require('node:https');
const fs = require('node:fs');
const os = require('node:os');
const { URL } = require('node:url');

const KEY = fs.readFileSync(os.homedir() + '/.dsh/.env', 'utf8')
  .split('\n').find(l => l.startsWith('RUNPOD_API_KEY='))?.split('=').slice(1).join('=').trim() || '';
const PORT = process.env.PORT || 8877;

// model -> RunPod serverless endpoint id (verified via API this session)
const ROUTES = {
  'sov6-deepseek-r1-671b': 'yco6asrwhsppeh',
  'sov6-qwen3-235b': 'izwlg5ea4abx7r',
  'sov6-kimi-k3-2tb': 'c22oxi45hjf9rc',
  'sov6-gpt-oss-120b': 'uyqf1r2nk6ois4',
  'sov4-llama33-70b': 'xlg0t4v6zii8lw',
  'sov4-qwen38-27b': 'smq8l6p9cqq3d6',
  'sov4-mistral-7b': 'cwfrc0a4w4mfjl',
  'sov4-deepseek-r1-7b': 'ghocankokw6r78',
  'sov4-qwen25-7b': '2nvfnpy2jvhtqj',
};

function proxied(m) {
  const ep = ROUTES[m];
  if (!ep) return { error: true, message: `unknown model ${m}; known: ${Object.keys(ROUTES).join(', ')}` };
  return { ep };
}

const server = http.createServer((req, res) => {
  // only POST /v1/chat/completions (OpenAI-compat)
  let body = '';
  req.on('data', c => body += c);
  req.on('end', () => {
    // billing/models surfaces (the 'rentable' catalog + commission ledger view)
    if (req.method === 'GET' && req.url.startsWith('/v1/models')) {
      res.writeHead(200, {'content-type':'application/json'});
      res.end(JSON.stringify({object:'list', data:Object.keys(ROUTES).map(id=>({id, object:'model', owned_by:'eunomia-runpod'}))}));
      return;
    }
    if (req.method === 'GET' && req.url.startsWith('/ledger')) {
      const rows = fs.existsSync(os.homedir() + '/eunomia-ledger.jsonl')
        ? fs.readFileSync(os.homedir() + '/eunomia-ledger.jsonl','utf8').trim().split('\n').filter(Boolean).slice(-20)
        : [];
      res.writeHead(200, {'content-type':'application/json'});
      res.end(JSON.stringify({calls: rows.length, last: rows.map(r=>JSON.parse(r))}));
      return;
    }
    if (req.method !== 'POST' || !req.url.startsWith('/v1/chat/completions')) {
      res.writeHead(404, {'content-type':'application/json'}); res.end(JSON.stringify({error:'not found'})); return;
    }
    let data; try { data = JSON.parse(body); } catch { res.writeHead(400); res.end('bad json'); return; }
    const model = data.model || 'sov4-mistral-7b';
    const r = proxied(model);
    if (r.error) { res.writeHead(400, {'content-type':'application/json'}); res.end(JSON.stringify(r)); return; }
    // proxy to RunPod serverless OpenAI-compat endpoint
    const u = `https://api.runpod.ai/v2/${r.ep}/openai/v1/chat/completions`;
    const preq = https.request(new URL(u), {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      timeout: 300000,
    }, (pres) => {
      let out = ''; pres.on('data', c => out += c);
      pres.on('end', () => {
        // BILLING/COMMISSION LEDGER
        try {
          const used = JSON.parse(out)?.usage || {};
          fs.appendFileSync(os.homedir() + '/eunomia-ledger.jsonl', JSON.stringify({
            t: new Date().toISOString(), model, endpoint: r.ep, status: pres.statusCode,
            tokens: used.total_tokens || 0, tier: 'commission-log'
          }) + '\n');
        } catch {}
        res.writeHead(pres.statusCode || 502, {'content-type':'application/json'});
        res.end(out || '{"error":"empty upstream"}');
      });
    });
    preq.on('error', e => { res.writeHead(502); res.end(JSON.stringify({error:'upstream', message: String(e)})); });
    preq.end(body);
  });
});
server.listen(PORT, () => console.log(`EUNOMIA gateway on :${PORT} (${Object.keys(ROUTES).length} rentable models) — POST /v1/chat/completions`));
