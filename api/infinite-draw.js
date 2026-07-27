// Vercel serverless — Infinite Drawing API endpoint
//
// POST /api/infinite-draw
//
// The core API for the infinite drawing engine.
// Accepts drawing operations and returns graph state.
//
// Operations:
//   draw: Add a memory node at (x, y)
//   grow: Grow from a node in a direction
//   zoom: Fractal zoom into a node
//   route: Route through the graph
//   memory: Retrieve memories
//   ingest: Ingest docstore entries
//   state: Get full graph state

const crypto = require('crypto');
const fs = require('fs').promises;
const path = require('path');

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

// In-memory graph store (per serverless instance)
const graphs = new Map();

function getGraph(agentId) {
  if (!graphs.has(agentId)) {
    graphs.set(agentId, {
      nodes: new Map(),
      drawPoints: [],
      growth: [],
      sigils: [],
      generation: 0,
    });
  }
  return graphs.get(agentId);
}

function initHives(graph) {
  const owems = [
    {name:'logic',family:'deepseek'},{name:'ethics',family:'llama'},{name:'aesthetics',family:'mistral'},
    {name:'temporality',family:'qwen'},{name:'identity',family:'qwen'},{name:'agency',family:'deepseek'},
    {name:'relationality',family:'llama'},{name:'embodiment',family:'mistral'},{name:'abstraction',family:'qwen'},
    {name:'synthesis',family:'llama'},{name:'destruction',family:'deepseek'},{name:'preservation',family:'mistral'},
    {name:'creation',family:'qwen'},
  ];

  owems.forEach((o, i) => {
    const angle = (Math.PI * 2 / owems.length) * i;
    const cx = 600 + Math.cos(angle) * 300;
    const cy = 500 + Math.sin(angle) * 300;

    graph.nodes.set(`hive-${o.name}`, {
      id: `hive-${o.name}`, x: cx, y: cy,
      hive: o.name, family: o.family, level: 0, size: 8,
      knowledge: Array.from({length: 10}, (_, k) => ({q: `${o.name} Q${k}`, a: `Sovereign ${o.name}`})),
      connections: [],
    });

    // Fractal swarm
    [{l:1,n:10,r:40},{l:2,n:20,r:25},{l:3,n:10,r:15}].forEach(({l,n,r}) => {
      for (let j = 0; j < n; j++) {
        const a = (Math.PI * 2 / n) * j + l * 0.3;
        const nx = cx + Math.cos(a) * r * (1 + l * 0.5);
        const ny = cy + Math.sin(a) * r * (1 + l * 0.5);
        const nodeId = `${o.name}-L${l}-${j}`;
        graph.nodes.set(nodeId, {
          id: nodeId, x: nx, y: ny,
          hive: o.name, family: o.family, level: l, size: Math.max(2, 8 - l * 2),
          knowledge: [{q: `${nodeId} Q0`, a: `Knowledge`}],
          connections: [`hive-${o.name}`],
        });
        graph.nodes.get(`hive-${o.name}`).connections.push(nodeId);
      }
    });
  });
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

  const agentId = (body.agent_id || 'default').toString();
  const op = (body.op || 'state').toString();
  const ts = new Date().toISOString();

  const graph = getGraph(agentId);
  if (graph.nodes.size === 0) initHives(graph);

  let result = {};

  if (op === 'draw') {
    const x = Number(body.x) || 0;
    const y = Number(body.y) || 0;
    const data = (body.data || '').toString();
    const drawId = `draw-${graph.drawPoints.length}`;
    graph.nodes.set(drawId, {
      id: drawId, x, y, hive: 'user', family: 'user', level: 0, size: 5,
      knowledge: [{q: data || `draw-${x}-${y}`, a: 'user memory'}],
      connections: [],
    });
    // Connect to nearest
    let nearest = null, minDist = Infinity;
    graph.nodes.forEach((n, id) => {
      if (id === drawId) return;
      const d = Math.sqrt((n.x - x)**2 + (n.y - y)**2);
      if (d < minDist) { minDist = d; nearest = n; }
    });
    if (nearest) {
      graph.nodes.get(drawId).connections.push(nearest.id);
      nearest.connections.push(drawId);
    }
    graph.drawPoints.push({x, y, ts});
    result = {status: 'drawn', node: drawId, connected_to: nearest?.id, total_nodes: graph.nodes.size};

  } else if (op === 'grow') {
    const nodeId = (body.node_id || '').toString();
    const direction = (body.direction || 'auto').toString();
    const parent = graph.nodes.get(nodeId);
    if (!parent) return res.status(400).json({error: `Node ${nodeId} not found`});

    graph.generation++;
    const rng = xorshift32(hashSeed(`${nodeId}-${graph.generation}`));
    const dirs = ['forward', 'backward', 'downward', 'lateral'];
    const dir = direction === 'auto' ? dirs[rng() % 4] : direction;
    const angle = (rng() / 0xFFFFFFFF) * Math.PI * 2;
    const dist = 20 + (rng() % 30);

    let nx, ny;
    if (dir === 'backward') {
      nx = parent.x - dist; ny = parent.y;
    } else if (dir === 'downward') {
      nx = parent.x + Math.cos(angle) * dist * 0.5;
      ny = parent.y + Math.sin(angle) * dist * 0.5;
    } else {
      nx = parent.x + Math.cos(angle) * dist;
      ny = parent.y + Math.sin(angle) * dist;
    }

    const newId = `${parent.hive}-${dir}-${graph.generation}`;
    graph.nodes.set(newId, {
      id: newId, x: nx, y: ny,
      hive: parent.hive, family: parent.family,
      level: dir === 'downward' ? parent.level + 1 : parent.level,
      size: Math.max(2, parent.size - 1),
      knowledge: [{q: `${dir}-growth`, a: `grown from ${nodeId}`}],
      connections: [nodeId],
    });
    parent.connections.push(newId);

    // Backward connection
    let nearest = null, minDist = Infinity;
    graph.nodes.forEach((n, id) => {
      if (id === newId) return;
      const d = Math.sqrt((n.x - nx)**2 + (n.y - ny)**2);
      if (d < minDist) { minDist = d; nearest = n; }
    });
    if (nearest) {
      graph.nodes.get(newId).connections.push(nearest.id);
      nearest.connections.push(newId);
    }

    graph.growth.push({id: newId, parent: nodeId, direction: dir});
    result = {status: 'grown', node: newId, direction: dir, backward_connection: nearest?.id, total_nodes: graph.nodes.size};

  } else if (op === 'route') {
    const query = (body.query || '').toString();
    const seed = hashSeed(query);
    const rng = xorshift32(seed);
    const allNodes = Array.from(graph.nodes.values());
    const count = Math.min(allNodes.length, Math.max(3, Math.floor(query.length / 10)));
    const visited = [];
    for (let i = 0; i < count; i++) visited.push(allNodes[rng() % allNodes.length]);

    const knowledge = new Set();
    visited.forEach(n => (n.knowledge || []).forEach(k => knowledge.add(k.q)));
    const families = [...new Set(visited.map(n => n.family))];
    const hives = [...new Set(visited.map(n => n.hive))];

    result = {nodes_visited: visited.length, families, hives, knowledge_accessed: knowledge.size, path: visited.map(n => n.id)};

  } else if (op === 'memory') {
    const query = (body.query || '').toString();
    const seed = hashSeed(query);
    const rng = xorshift32(seed);
    const allNodes = Array.from(graph.nodes.values());
    const visited = [];
    for (let i = 0; i < Math.min(5, allNodes.length); i++) visited.push(allNodes[rng() % allNodes.length]);
    const details = [];
    visited.forEach(n => (n.knowledge || []).forEach(k => details.push({node: n.id, q: k.q, a: k.a})));
    result = {query, memories_recalled: visited.length, knowledge_details: details.slice(0, 20)};

  } else if (op === 'state') {
    let totalConns = 0, totalKnowledge = 0;
    graph.nodes.forEach(n => {
      totalConns += (n.connections || []).length;
      totalKnowledge += (n.knowledge || []).length;
    });
    result = {
      agent_id: agentId, nodes: graph.nodes.size, connections: totalConns,
      knowledge: totalKnowledge, draw_points: graph.drawPoints.length,
      growth: graph.growth.length, sigils: graph.sigils.length, generation: graph.generation,
    };
  }

  const sigil = hmacSigil({op, agent_id: agentId, ts});
  graph.sigils.push({hash: sigil, ts, op});

  return res.status(200).json({status: 'ok', op, ...result, sigil, timestamp: ts});
};
