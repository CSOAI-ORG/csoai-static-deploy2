#!/usr/bin/env node
// eunomia-gateway-v2.cjs — OpenRouter-school gateway: provider abstraction + fallback chains.
// provider = runpod:<endpoint> | local:<ollama-model> ; model aliases route primary->secondary->...
// Usage/prices surfaces: GET /api/v1/usage, /api/v1/prices. Billing ledger per call (commission log).
const http = require('node:http');
const https = require('node:https');
const fs = require('node:fs');
const os = require('node:os');
const { URL } = require('node:url');

const ENV = fs.readFileSync(os.homedir() + '/.dsh/.env', 'utf8');
const RUNPOD_KEY = (ENV.match(/RUNPOD_API_KEY=(\S+)/) || [])[1] || '';
const PORT = process.env.PORT || 8878;
const LEDGER = os.homedir() + '/eunomia-ledger.jsonl';
const LOCAL = 'http://localhost:11434'; // Mac ollama (policy teachers; healthy)

// model alias -> provider chain (primary first); local twins only where weights family matches
const ROUTES = {
  'sov4-mistral-7b':      [ 'runpod:cwfrc0a4w4mfjl', 'local:mistral:7b' ],
  'sov4-qwen25-7b':       [ 'runpod:2nvfnpy2jvhtqj', 'local:qwen2.5:7b' ],
  'sov6-deepseek-r1-671b':[ 'runpod:yco6asrwhsppeh' ],
  'sov6-qwen3-235b':      [ 'runpod:izwlg5ea4abx7r' ],
  'sov6-kimi-k3-2tb':     [ 'runpod:c22oxi45hjf9rc' ],
  'sov6-gpt-oss-120b':    [ 'runpod:uyqf1r2nk6ois4' ],
  'sov4-llama33-70b':     [ 'runpod:xlg0t4v6zii8lw' ],
  'sov4-qwen38-27b':      [ 'runpod:smq8l6p9cqq3d6' ],
  'sov4-deepseek-r1-7b':  [ 'runpod:ghocankokw6r78' ],
  'sov4-qwen25-7b-local': [ 'local:qwen2.5:7b' ],
  'sov4-mistral-7b-local':[ 'local:mistral:7b' ],
};
// honest price table (USD per 1M tokens, our published rates; 0 = free / unmeasured)
const PRICES = {
  'sov4-mistral-7b': { in: 0.20, out: 0.20 }, 'sov4-qwen25-7b': { in: 0.20, out: 0.20 },
  'sov4-llama33-70b': { in: 0.80, out: 0.80 }, 'sov4-qwen38-27b': { in: 0.80, out: 0.80 },
  'sov4-deepseek-r1-7b': { in: 0.80, out: 0.80 }, 'sov6-qwen3-235b': { in: 2.00, out: 2.00 },
  'sov6-deepseek-r1-671b': { in: 2.00, out: 2.00 }, 'sov6-kimi-k3-2tb': { in: 2.00, out: 2.00 },
  'sov6-gpt-oss-120b': { in: 1.00, out: 1.00 },
};

function callProvider(provider, body, model, timeoutMs = 300000) {
  return new Promise((resolve) => {
    let u;
    if (provider.startsWith('runpod:')) u = `https://api.runpod.ai/v2/${provider.slice(7)}/openai/v1/chat/completions`;
    else if (provider.startsWith('local:')) u = `${LOCAL}/v1/chat/completions`;
    else return resolve({ status: 502, body: JSON.stringify({ error: `unknown provider ${provider}` }) });
    const headers = provider.startsWith('runpod:')
      ? { 'Authorization': `Bearer ${RUNPOD_KEY}`, 'Content-Type': 'application/json' }
      : { 'Content-Type': 'application/json' };
    const preq = https.request(new URL(u), { method: 'POST', headers, timeout: timeoutMs }, (pres) => {
      let out = ''; pres.on('data', c => out += c);
      pres.on('end', () => resolve({ status: pres.statusCode, body: out || '{"error":"empty"}' }));
    });
    preq.on('error', (e) => resolve({ status: 502, body: JSON.stringify({ error: 'upstream', message: String(e) }) }));
    preq.setTimeout(timeoutMs, () => { preq.destroy(); resolve({ status: 504, body: JSON.stringify({ error: 'timeout' }) }); });
    preq.end(JSON.stringify(body));
  });
}

function readLedger(n = 500) {
  if (!fs.existsSync(LEDGER)) return [];
  return fs.readFileSync(LEDGER, 'utf8').trim().split('\n').filter(Boolean).slice(-n).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
}

const server = http.createServer((req, res) => {
  let body = ''; req.on('data', c => body += c);
  req.on('end', async () => {
    const send = (code, obj) => { res.writeHead(code, { 'content-type': 'application/json' }); res.end(JSON.stringify(obj)); };
    if (req.method === 'GET' && req.url.startsWith('/v1/models')) {
      const catalog = Object.entries(ROUTES).map(([id, chain]) => ({ id, object: 'model', owned_by: 'eunomia-runpod', providers: chain, primary: chain[0] }));
      return send(200, { object: 'list', data: catalog });
    }
    if (req.method === 'GET' && req.url.startsWith('/api/v1/prices')) return send(200, { object: 'list', data: PRICES });
    if (req.method === 'GET' && req.url.startsWith('/api/v1/usage')) {
      const rows = readLedger(2000);
      const agg = {};
      let calls = 0, tokens = 0;
      for (const r of rows) { if (!agg[r.model]) agg[r.model] = { calls: 0, tokens: 0 }; agg[r.model].calls++; agg[r.model].tokens += r.tokens || 0; calls++; tokens += r.tokens || 0; }
      return send(200, { calls, tokens, by_model: agg, note: 'commission ledger aggregation; UNMEASURED columns omitted when absent' });
    }
    if (req.method === 'GET' && req.url.startsWith('/ledger')) return send(200, { calls: readLedger().length, last: readLedger(20) });
    if (req.method !== 'POST' || !req.url.startsWith('/v1/chat/completions')) return send(404, { error: 'not found' });
    let data; try { data = JSON.parse(body); } catch { return send(400, { error: 'bad json' }); }
    const model = data.model || 'sov4-mistral-7b';
    const chain = ROUTES[model];
    if (!chain) return send(400, { error: `unknown model ${model}; known: ${Object.keys(ROUTES).join(', ')}` });
    const t0 = Date.now();
    // fallback chain: each provider gets a bounded budget; first success (<500) wins
    const budget = chain.length > 1 ? 45000 : 300000;
    let last = null;
    for (let i = 0; i < chain.length; i++) {
      last = await callProvider(chain[i], data, model, budget);
      if (last.status >= 200 && last.status < 500) break;
    }
    const used = (() => { try { return JSON.parse(last.body)?.usage || {}; } catch { return {}; } })();
    fs.appendFileSync(LEDGER, JSON.stringify({
      t: new Date().toISOString(), model, provider: chain.find(p => p === last?.provider) || chain[0], status: last.status,
      tokens: used.total_tokens || 0, latency_ms: Date.now() - t0, fallback_used: chain.length > 1, tier: 'commission-log',
    }) + '\n');
    res.writeHead(last.status || 502, { 'content-type': 'application/json' });
    res.end(last.body);
  });
});
server.listen(PORT, () => console.log(`EUNOMIA v2 on :${PORT} (${Object.keys(ROUTES).length} aliases, fallback chains) — POST /v1/chat/completions`));
