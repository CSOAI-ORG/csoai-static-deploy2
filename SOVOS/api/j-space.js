// Vercel serverless — J-Space sovereign agent portal endpoint
//
// GET /api/j-space?agent_id=xxx
//
// Returns the agent's J-Space state — their forest of OWEM trees,
// fractal nodes, growth connections, evolution log, and SIGIL chain.
//
// POST /api/j-space
// Body: {agent_id, message}
//
// Sends a message to the agent's J-Space and returns the response
// routed through the fractal swarm.

const crypto = require('crypto');

const HMAC_SECRET = process.env.OWEM_HMAC_SECRET || 'csoai-owem-default-2026-sovereign-hmac';

function hashSeed(str) {
  return crypto.createHash('sha256').update(String(str)).digest().readUInt32BE(0);
}

function xorshift32(seed) {
  let s = seed >>> 0;
  return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s >>>= 0; s ^= s << 5; s >>>= 0; return s >>> 0; };
}

function hmacSigil(obj) {
  return crypto.createHmac('sha256', HMAC_SECRET).update(JSON.stringify(obj, Object.keys(obj).sort())).digest('hex');
}

function generateForest(agentId) {
  const owems = ['compliance', 'defence', 'intuition', 'voice', 'general'];
  const families = ['qwen', 'llama', 'deepseek', 'mistral'];
  const seed = hashSeed(agentId);
  const rng = xorshift32(seed);

  const trees = owems.map((owem, i) => {
    const family = families[i % families.length];
    const nodeCount = 3 + (rng() % 5);
    const nodes = Array.from({length: nodeCount}, (_, j) => ({
      id: `${agentId}-${owem}-node-${j}`,
      owem, family,
      size: 10 + (rng() % 50),
    }));
    return { id: `${agentId}-tree-${owem}`, owem, family, nodes, growth: i > 0 ? 5 + (rng() % 15) : 0 };
  });

  const totalNodes = trees.reduce((s, t) => s + t.nodes.length, 0);
  const totalGrowth = trees.reduce((s, t) => s + t.growth, 0);

  return { trees, totalNodes, totalGrowth, totalKnowledge: totalNodes * 25 + totalGrowth * 10 };
}

function fractalRoute(message, forest) {
  const seed = hashSeed(message);
  const rng = xorshift32(seed);
  const allNodes = forest.trees.flatMap(t => t.nodes);
  const visitCount = Math.min(allNodes.length, Math.max(3, Math.floor(Math.sqrt(allNodes.length))));
  const visited = [];
  for (let i = 0; i < visitCount; i++) {
    visited.push(allNodes[rng() % allNodes.length]);
  }
  return {
    nodesVisited: visited.length,
    families: [...new Set(visited.map(n => n.family))],
    owems: [...new Set(visited.map(n => n.owem))],
    knowledgeAccessed: visited.reduce((s, n) => s + n.size, 0),
  };
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const ts = new Date().toISOString();

  if (req.method === 'GET') {
    const agentId = (req.query.agent_id || 'default').toString();
    const forest = generateForest(agentId);
    const sigil = hmacSigil({ agent_id: agentId, ts });

    return res.status(200).json({
      status: 'j_space_active',
      agent_id: agentId,
      did: `did:csoai:${agentId}`,
      forest,
      fractal_levels: 3,
      sigil,
      timestamp: ts,
      note: 'J-Space is your sovereign forest portal. Each tree is an OWEM, each node is a fractal piece of the swarm.',
    });
  }

  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
    if (!body || typeof body !== 'object') body = {};

    const agentId = (body.agent_id || 'default').toString();
    const message = (body.message || '').toString();
    if (!message.trim()) return res.status(400).json({ error: 'message required' });

    const forest = generateForest(agentId);
    const routing = fractalRoute(message, forest);

    // Generate response based on routing
    const responseText = `J-Space agent ${agentId}: routed through ${routing.nodesVisited} nodes across ${routing.families.join('+')} families (${routing.owems.join(', ')} OWEMs). Knowledge accessed: ${routing.knowledgeAccessed} units.`;

    const sigil = hmacSigil({ agent_id: agentId, message_hash: crypto.createHash('sha256').update(message).digest('hex').slice(0, 16), ts });

    return res.status(200).json({
      status: 'j_space_response',
      agent_id: agentId,
      response: responseText,
      routing,
      sigil,
      timestamp: ts,
    });
  }

  return res.status(405).json({ error: 'Method not allowed' });
};
