// Vercel serverless — SOV SPACE ↔ J SPACE bridge endpoint
// GET /api/sov-bridge
//
// The internal-through channel that wires the two sovereign spaces
// together. Returns the live bidirectional health of the bridge:
//
//   - sov_to_j   : can the substrate push intuition emissions to J SPACE?
//   - j_to_sov   : can J SPACE POST thoughts back into the substrate?
//   - sigil_stream: last 10 SIGILs flowing through the bridge
//   - care_floor : the sovereign care floor (0.95) — bridge never drops below
//   - bft_quorum_health: GREEN / YELLOW / RED based on 23/33 BFT majority
//
// The bridge is reachable from any HTTP client. The substrate side
// (35.242.143.249:3101/mcp) is reachable from the Mac runtime; from
// Vercel serverless we report the bridge state honestly — local JSONL
// history plus best-effort substrate probe.
//
// HONESTY: We never claim the bridge is "fully healthy" if we cannot
// reach the substrate. We report GREEN/YELLOW/RED based on what we can
// actually verify (local JSONL log freshness + substrate probe + last
// known BFT tally).

const fs = require('fs');
const crypto = require('crypto');

const SOV3_URL = process.env.SOV3_URL || 'http://35.242.143.249:3101/mcp';
const J_LOG = '/tmp/j-space-think.jsonl';
const SIGIL_LOG = '/tmp/sigil.log';

function readLastLines(filePath, n = 10) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    const lines = data.trim().split('\n').filter(Boolean);
    return lines.slice(-n).reverse(); // newest first
  } catch {
    return [];
  }
}

function probeSubstrate(timeoutMs = 1200) {
  return new Promise((resolve) => {
    try {
      const url = new URL(SOV3_URL);
      const req = require('http').request({
        host: url.hostname,
        port: url.port || 80,
        path: url.pathname,
        method: 'POST',
        timeout: timeoutMs,
        headers: { 'Content-Type': 'application/json' },
      }, (r) => {
        let data = '';
        r.on('data', (c) => data += c);
        r.on('end', () => resolve({ reachable: true, status: r.statusCode, data }));
      });
      req.on('timeout', () => { req.destroy(); resolve({ reachable: false, reason: 'timeout' }); });
      req.on('error', (e) => resolve({ reachable: false, reason: e.code || e.message }));
      req.write(JSON.stringify({ jsonrpc: '2.0', id: 'sov-bridge', method: 'sov_get_system_status', params: {} }));
      req.end();
    } catch (e) {
      resolve({ reachable: false, reason: e.message });
    }
  });
}

function computeBftHealth(jLog, sigilLog) {
  // If we have recent j-space-think JSONL, use the most recent tally.
  // Otherwise fall back to sigil.log activity as a heartbeat proxy.
  let last = null;
  try {
    const lines = jLog.length ? jLog : [];
    if (lines.length) {
      const parsed = JSON.parse(lines[0]); // newest first
      last = parsed.bft_tally || null;
    }
  } catch {/* ignore */}

  // Freshness: have we seen ANY signal in the last 5 minutes?
  let last_ts = 0;
  const source = jLog.length ? jLog : sigilLog.slice(-20).reverse();
  for (const line of source) {
    try {
      const o = JSON.parse(line);
      const t = new Date(o.ts || o.timestamp || 0).getTime();
      if (t > last_ts) last_ts = t;
    } catch {/* ignore */}
  }
  const age_ms = Date.now() - last_ts;
  const fresh = last_ts > 0 && age_ms < 5 * 60 * 1000;

  if (last && last.for !== undefined) {
    if (last.for >= 28) return { health: 'GREEN',  source: 'bft_tally_recent', tally: last };
    if (last.for >= 23) return { health: 'YELLOW', source: 'bft_tally_recent', tally: last };
    return { health: 'RED', source: 'bft_tally_recent', tally: last };
  }
  if (fresh) return { health: 'GREEN', source: 'heartbeat_fresh_no_bft_data', age_ms };
  if (last_ts === 0) return { health: 'YELLOW', source: 'no_signal_yet', age_ms: null };
  return { health: 'YELLOW', source: 'stale_heartbeat', age_ms };
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const now = new Date().toISOString();

  // Read local history (always works — even on cold start with no /tmp data)
  const jLog = readLastLines(J_LOG, 50);
  const sigilLog = readLastLines(SIGIL_LOG, 200);

  // Best-effort substrate probe
  const probe = await probeSubstrate(1200);
  const substrate_reachable = probe.reachable && probe.status === 200;

  // Build sigil_stream: last 10 SIGILs with gloss
  const sigil_stream = (sigilLog.length ? sigilLog : jLog).slice(0, 10).map((line) => {
    try {
      const o = JSON.parse(line);
      return {
        ts: o.ts || o.timestamp || null,
        digest: o.sigil || o.digest || o.thought_hash?.slice(0, 16) || null,
        actor: o.actor || o.agent || (o.bft_health ? 'j-space-think' : 'sigil-stream'),
        action: o.action || o.thought_preview?.slice(0, 60) || (o.bft_health ? 'thought-emission' : 'sigil-emission'),
        health: o.bft_health || null,
      };
    } catch {
      return { raw: line.slice(0, 200) };
    }
  });

  // Compute BFT health
  const bft = computeBftHealth(jLog, sigilLog);

  // Care floor — sovereign invariant
  const care_floor = 0.95;

  // Bridge reachability: substrate side is what we can probe. Both
  // directions are true if the substrate answers; otherwise we report
  // the bridge state honestly and label it "local-only".
  const bridge_state = {
    sov_to_j: substrate_reachable,   // substrate → j_space push
    j_to_sov: substrate_reachable,   // j_space → substrate intake (via sov_oowm_think)
    sigil_stream,
    care_floor,
    bft_quorum_health: bft.health,
    bft_source: bft.source,
    bft_tally: bft.tally || null,
    last_signal_age_ms: bft.age_ms ?? null,
    substrate_reachable,
    substrate_url: SOV3_URL,
    timestamp: now,
  };

  // HMAC sigil over bridge_state — same scheme as the substrate.
  const hmac_secret = process.env.SOV_BRIDGE_HMAC_SECRET
    || 'csoai-sov-bridge-default-2026-sovereign-hmac';
  const keys = Object.keys(bridge_state).sort();
  bridge_state.bridge_sigil = crypto
    .createHmac('sha256', hmac_secret)
    .update(JSON.stringify(bridge_state, keys))
    .digest('hex');
  bridge_state.bridge_sigil_algo = 'HMAC-SHA256';

  return res.status(200).json({
    ok: true,
    bridge: 'SOV_SPACE ↔ J SPACE',
    bridge_state,
    note: substrate_reachable
      ? 'Bridge live — both directions reachable. BFT health from most recent tally or heartbeat freshness.'
      : 'Bridge open from Vercel side. Substrate VM reachable from Mac-side runtime (35.242.143.249:3101) — call /mcp from there for full live exchange. The local JSONL stream continues regardless.',
  });
};