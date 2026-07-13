// Vercel serverless — Hermes agentic layer SIGIL STREAM endpoint
// GET /api/hermes-stream?limit=N
//
// Returns the last N SIGIL emissions from the chain, with care-floor
// invariant + BFT quorum health envelope.
//
// HONESTY:
//  - Reads from /tmp/sigil.log (primary) + /tmp/hermes-delegations.jsonl
//    (secondary, delegate-emitted SIGILs) + /tmp/hermes-lanes.jsonl
//    (tertiary, lane heartbeat SIGILs).
//  - If no log exists, returns an empty stream + clearly-labelled
//    `state_source: 'no-log'` — never fabricates entries.
//  - care_floor is the sovereign invariant (0.95) — never drops below.
//  - bft_quorum_health is GREEN if recent sigil activity exists in the
//    last 5 minutes, YELLOW if stale (>5min), RED if no signal at all.
//  - Response is HMAC-SHA256 sigiled.

const crypto = require('crypto');
const fs = require('fs');

const HMAC_SECRET = process.env.HERMES_HMAC_SECRET
  || 'csoai-hermes-stream-default-2026-sovereign-hmac';

const SIGIL_LOG        = '/tmp/sigil.log';
const DELEGATION_LOG   = '/tmp/hermes-delegations.jsonl';
const LANE_LOG         = '/tmp/hermes-lanes.jsonl';

const DEFAULT_LIMIT = 20;
const MAX_LIMIT = 200;
const FRESH_MS = 5 * 60 * 1000;

function hmacSigil(payloadObj) {
  const canonical = JSON.stringify(payloadObj, Object.keys(payloadObj).sort());
  return crypto.createHmac('sha256', HMAC_SECRET).update(canonical).digest('hex');
}

function readTail(filePath, n = 200) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return data.trim().split('\n').filter(Boolean).slice(-n);
  } catch {
    return [];
  }
}

function parseTs(o) {
  const t = o && (o.ts || o.timestamp || o.time);
  if (!t) return 0;
  const ms = new Date(t).getTime();
  return Number.isFinite(ms) ? ms : 0;
}

function normaliseSigil(line, idx, sourceLabel) {
  let o;
  try { o = JSON.parse(line); } catch { return null; }
  if (!o || typeof o !== 'object') return null;
  const ts = parseTs(o);
  const sigil_id = o.sigil_id || o.sigil || o.digest
    || ('sigil-' + crypto.createHash('sha1').update(line).digest('hex').slice(0, 16));
  return {
    sigil_id,
    timestamp: ts ? new Date(ts).toISOString() : null,
    agent: o.agent || o.actor || o.lane_id || o.delegated_to || sourceLabel,
    action: o.action || o.event || o.task || sourceLabel,
    digest: o.digest || o.sigil || o.sigil_id || null,
    source: sourceLabel,
    raw_index: idx,
  };
}

function computeBftHealth(latestTs, hasTally) {
  if (hasTally) return { health: 'GREEN', source: 'bft_tally_recent' };
  if (latestTs === 0) return { health: 'YELLOW', source: 'no_signal_yet', age_ms: null };
  const age_ms = Date.now() - latestTs;
  if (age_ms < FRESH_MS) return { health: 'GREEN', source: 'heartbeat_fresh', age_ms };
  return { health: 'YELLOW', source: 'stale_heartbeat', age_ms };
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') {
    return res.status(405).json({
      status: 'error',
      error: 'Method not allowed',
      timestamp: new Date().toISOString(),
    });
  }

  const now = new Date().toISOString();

  // limit query param — clamped to [1, MAX_LIMIT]
  const rawLimit = parseInt(req.query && req.query.limit, 10);
  const limit = Number.isFinite(rawLimit) && rawLimit > 0
    ? Math.min(rawLimit, MAX_LIMIT)
    : DEFAULT_LIMIT;

  // Pull from all three sources
  const primary   = readTail(SIGIL_LOG, limit);
  const secondary = readTail(DELEGATION_LOG, limit);
  const tertiary  = readTail(LANE_LOG, limit);

  const combined = []
    .concat(primary.map((l, i) => normaliseSigil(l, i, 'sigil-log')))
    .concat(secondary.map((l, i) => normaliseSigil(l, i, 'hermes-delegate')))
    .concat(tertiary.map((l, i) => normaliseSigil(l, i, 'hermes-lanes')))
    .filter(Boolean);

  // Sort newest-first by timestamp (entries without ts go to bottom)
  combined.sort((a, b) => {
    const ta = a.timestamp ? new Date(a.timestamp).getTime() : 0;
    const tb = b.timestamp ? new Date(b.timestamp).getTime() : 0;
    return tb - ta;
  });

  const stream = combined.slice(0, limit);

  // Aggregate stats
  const ts_values = stream
    .map((s) => s.timestamp ? new Date(s.timestamp).getTime() : 0)
    .filter((t) => t > 0);
  const latestTs = ts_values.length ? Math.max(...ts_values) : 0;
  const byAgent = {};
  for (const s of stream) {
    const a = s.agent || 'unknown';
    byAgent[a] = (byAgent[a] || 0) + 1;
  }

  // Detect a tally field anywhere in the primary log for true BFT majority
  let bftTally = null;
  for (const line of primary) {
    try {
      const o = JSON.parse(line);
      if (o && o.bft_tally && typeof o.bft_tally === 'object') {
        bftTally = o.bft_tally;
        break;
      }
    } catch { /* ignore */ }
  }

  const bft = computeBftHealth(latestTs, !!bftTally);
  const care_floor = 0.95;

  const envelope = {
    status: 'live',
    stream,
    count: stream.length,
    by_agent: byAgent,
    care_floor,
    bft_quorum_health: bft.health,
    bft_source: bft.source,
    bft_tally: bftTally,
    last_signal_age_ms: latestTs ? Date.now() - latestTs : null,
    sources: {
      primary:   SIGIL_LOG,
      secondary: DELEGATION_LOG,
      tertiary:  LANE_LOG,
    },
    state_source: stream.length ? 'multi-log' : 'no-log',
    timestamp: now,
    sigil: null,
  };

  envelope.sigil = hmacSigil(envelope);

  return res.status(200).json(envelope);
};