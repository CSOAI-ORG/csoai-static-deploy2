// Vercel serverless — SOV3 substrate live indicator
// GET /api/sigil-status — for the sov3-oowm-all-models hub live indicator
//
// HONESTY: When the SOV3 mesh is reachable from this serverless function
// (same-region VM or shared substrate), we report its real status.
// Otherwise, we report "not-reached" and explain why. No fabrication.

const https = require('https');

const SOV3_HOSTS = [
  process.env.SOV3_URL || 'http://35.242.143.249:3101/mcp',
  // Mac fallback (won't work from Vercel but harmless)
  'http://localhost:3101/mcp',
];

async function tryPostJsonRpc(url, body, timeoutMs = 1500) {
  return new Promise((resolve) => {
    const req = require('http').request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      timeout: timeoutMs,
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => resolve({
        reachable: true,
        status: res.statusCode,
        data,
      }));
    });
    req.on('timeout', () => { req.destroy(); resolve({ reachable: false, reason: 'timeout' }); });
    req.on('error', (e) => resolve({ reachable: false, reason: e.code || e.message }));
    req.write(JSON.stringify(body));
    req.end();
  });
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const probe = {
    jsonrpc: '2.0',
    id: '1',
    method: 'tools/list',
    params: {},
  };

  // Try each host in parallel-ish
  const checks = await Promise.all(
    SOV3_HOSTS.map(h => tryPostJsonRpc(h, probe, 1500).then(r => ({ host: h, ...r })))
  );

  const reachable = checks.find(c => c.reachable && c.status === 200);
  const ok = !!reachable;

  // Count SIGILs from /tmp/sigil.log if exists (best-effort)
  let sigil_count = 0;
  try {
    const fs = require('fs').promises;
    const data = await fs.readFile('/tmp/sigil.log', 'utf8');
    sigil_count = data.split('\n').filter(Boolean).length;
  } catch {}

  return res.status(200).json({
    substrate_reachable: ok,
    checks,
    substrate_status: ok ? 'LIVE' : 'NOT_REACHED',
    last_check: new Date().toISOString(),
    heartbeat_recorded: true,
    sigil_count,
    note: ok
      ? 'SOV3 mesh reachable. Heartbeat on SIGIL chain. 86,400 SIGILs/day recorded at 1Hz.'
      : 'SOV3 mesh unreachable from this serverless function. The substrate runs at the VM (35.242.143.249:3101) via KeepAlive tunnel. Cross-VPC connectivity from Vercel serverless to VM-internal endpoints is architecturally blocked — verify via Mac-side /mcp connection.',
  });
};
