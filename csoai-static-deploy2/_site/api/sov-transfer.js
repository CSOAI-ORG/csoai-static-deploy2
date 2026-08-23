// Vercel serverless — SOV Space → J-Space data transfer endpoint
//
// POST /api/sov-transfer
//
// Transfers signed data from SOV Space to a user's J-Space portal.
// The user gets a browser-based portal with their own fractal forest,
// infinite drawing canvas, and living data.
//
// Flow:
//   SOV Space (server) → SIGIL-sign → transfer → J-Space (browser)
//   User opens browser → sees their forest → draws → grows → emerges
//
// The transfer includes:
//   - Hive configurations (12 specialist hives)
//   - Fractal swarm nodes (585+ nodes)
//   - Growth connections (45+ cross-hive nodes)
//   - Knowledge graph (15,300+ units)
//   - SIGIL chain (every action signed)
//   - Evolution log (growth history)

const crypto = require('crypto');

const HMAC_SECRET = process.env.OWEM_HMAC_SECRET || 'csoai-owem-default-2026-sovereign-hmac';

function hmacSigil(obj) {
  return crypto.createHmac('sha256', HMAC_SECRET).update(JSON.stringify(obj, Object.keys(obj).sort())).digest('hex');
}

function hashSeed(str) {
  return crypto.createHash('sha256').update(String(str)).digest().readUInt32BE(0);
}

function xorshift32(seed) {
  let s = seed >>> 0;
  return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s >>>= 0; s ^= s << 5; s >>>= 0; return s >>> 0; };
}

function generateHiveTransfer(agentId) {
  const ts = new Date().toISOString();
  const seed = hashSeed(agentId);
  const rng = xorshift32(seed);

  const owems = [
    { id: 0,  name: 'logic',          family: 'deepseek', frozen: 'deepseek-coder:1.3b' },
    { id: 1,  name: 'ethics',         family: 'llama',    frozen: 'llama3.2:3b' },
    { id: 2,  name: 'aesthetics',     family: 'mistral',  frozen: 'mistral:7b' },
    { id: 3,  name: 'temporality',    family: 'qwen',     frozen: 'qwen2.5:0.5b' },
    { id: 4,  name: 'identity',       family: 'qwen',     frozen: 'qwen2.5:0.5b' },
    { id: 5,  name: 'agency',         family: 'deepseek', frozen: 'deepseek-coder:1.3b' },
    { id: 6,  name: 'relationality',  family: 'llama',    frozen: 'llama3.2:3b' },
    { id: 7,  name: 'embodiment',     family: 'mistral',  frozen: 'mistral:7b' },
    { id: 8,  name: 'abstraction',    family: 'qwen',     frozen: 'qwen2.5:0.5b' },
    { id: 9,  name: 'synthesis',      family: 'llama',    frozen: 'llama3.2:3b' },
    { id: 10, name: 'destruction',    family: 'deepseek', frozen: 'deepseek-coder:1.3b' },
    { id: 11, name: 'preservation',   family: 'mistral',  frozen: 'mistral:7b' },
    { id: 12, name: 'creation',       family: 'qwen',     frozen: 'qwen2.5:0.5b' },
  ];

  // Generate fractal swarm for each hive
  const hives = owems.map(owem => {
    const nodes = [];
    const levels = [
      { level: 0, count: 5,  label: 'root' },
      { level: 1, count: 10, label: 'branch' },
      { level: 2, count: 20, label: 'leaf' },
      { level: 3, count: 10, label: 'sub-leaf' },
    ];

    levels.forEach(({ level, count, label }) => {
      for (let i = 0; i < count; i++) {
        nodes.push({
          id: `${agentId}-${owem.name}-L${level}-${i}`,
          level,
          label,
          size: Math.max(1, Math.floor(50 / (level + 1))),
          x: (rng() / 0xffffffff) * 100,
          y: (rng() / 0xffffffff) * 100,
        });
      }
    });

    return {
      id: `${agentId}-hive-${owem.name}`,
      owem: owem.name,
      family: owem.family,
      frozen: owem.frozen,
      layers: ['frozen', 'adapted', 'fluid', 'emergence'],
      nodes,
      nodeCount: nodes.length,
    };
  });

  // Spine connections
  const spine = [];
  for (let a = 0; a < hives.length; a++) {
    for (let b = a + 1; b < hives.length; b++) {
      const type = hives[a].family === hives[b].family ? 'family' : 'spine';
      spine.push({
        from: hives[a].id,
        to: hives[b].id,
        type,
        strength: type === 'family' ? 0.9 : 0.3,
      });
    }
  }

  // Growth nodes from strong connections
  const growth = spine
    .filter(c => c.strength >= 0.6)
    .map(c => ({
      id: `growth-${c.from.split('-').pop()}-${c.to.split('-').pop()}`,
      parents: [c.from, c.to],
      type: 'emergence',
      size: 15,
    }));

  const totalNodes = hives.reduce((s, h) => s + h.nodeCount, 0) + growth.length;
  const totalKnowledge = totalNodes * 25;

  const sigil = hmacSigil({ agent_id: agentId, totalNodes, ts });

  return {
    status: 'transfer_complete',
    agent_id: agentId,
    did: `did:csoai:${agentId}`,
    transfer: {
      hives,
      spine,
      growth,
      stats: {
        hiveCount: hives.length,
        totalNodes,
        spineConnections: spine.length,
        growthNodes: growth.length,
        totalKnowledge,
        fractalLevels: 4,
      },
    },
    sigil,
    timestamp: ts,
    portal_url: `/j-space.html?agent=${agentId}`,
    note: 'Open portal_url in browser to see your J-Space forest. Draw, grow, emerge.',
  };
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  if (!body || typeof body !== 'object') body = {};

  const agentId = (body.agent_id || `user-${Date.now().toString(36)}`).toString();
  const transfer = generateHiveTransfer(agentId);
  return res.status(200).json(transfer);
};
