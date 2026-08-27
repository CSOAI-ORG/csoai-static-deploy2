/**
 * /mcp — a real JSON-RPC MCP server (streamable HTTP) so ANY harness wires in.
 *
 * Exposes the living 22-axis Council OS as two MCP tools:
 *   - measure: run a subject through a GSPC axis → signed measurement card
 *   - verify:  stranger-verify a signed card (content_id + Ed25519), offline-trust
 *
 * Implements the minimal MCP handshake (initialize / tools/list / tools/call) that
 * Hermes, DSH, Grok Bot, Claude, Cursor + VS Code all speak. Measurement, not
 * certification. UNMEASURED reported, never hidden.
 */
import { canon, getKey, sha256hex } from './signlib.js';

const HEADERS = { 'content-type': 'application/json; charset=utf-8', 'access-control-allow-origin': '*' };

export async function onRequestGet() {
  return new Response(JSON.stringify({
    protocol: 'mcp',
    name: 'gspc-council-os',
    version: '1.0.0',
    description: 'Council of AI GSPC — measure + sign + stranger-verify. 22 axes · 15 measured.',
    endpoint: '/mcp',
    tools: [
      { name: 'measure', description: 'Run a subject through a GSPC axis → signed measurement card (Wilson 95% CI + n).', parameters: { axis: 'gov|care|mcp|art5|det|prv|affect|agi|asi|mach|oss|xr|jail' } },
      { name: 'verify', description: 'Stranger-verify a signed card: recompute content_id + Ed25519. Three states: VALID / INVALID / UNCHECKABLE.', parameters: { card: 'the signed card JSON' } },
    ],
    living_source: 'https://councilof.ai/api/gspc',
    board: { public_count: '22 axis · 15 measured' },
  }), { status: 200, headers: HEADERS });
}

export async function onRequestPost({ request }) {
  let payload = {};
  try { payload = await request.json(); } catch (e) { /* non-JSON treat as empty */ }
  const method = payload.method || '';
  const id = payload.id ?? null;

  // MCP handshake
  if (method === 'initialize') {
    return rpc(id, { protocolVersion: '2024-11-05', capabilities: { tools: {} }, serverInfo: { name: 'gspc-council-os', version: '1.0.0' } });
  }
  if (method === 'notifications/initialized') {
    return new Response('', { status: 202, headers: HEADERS });
  }
  if (method === 'tools/list') {
    return rpc(id, { tools: [
      { name: 'measure', description: 'Run a subject through a GSPC axis → signed measurement card.', inputSchema: { type: 'object', properties: { axis: { type: 'string' }, model: { type: 'string' } } } },
      { name: 'verify', description: 'Stranger-verify a signed card (content_id + Ed25519). VALID / INVALID / UNCHECKABLE.', inputSchema: { type: 'object', properties: { card: { type: 'object' } } } },
    ] });
  }
  if (method === 'tools/call') {
    const params = payload.params || {};
    const name = params.name;
    const args = params.arguments || {};
    if (name === 'measure') {
      const axis = args.axis || 'gov';
      const card = await measureAxis(axis, args.model);
      return rpc(id, { content: [{ type: 'text', text: JSON.stringify(card) }], structuredContent: card, isError: false });
    }
    if (name === 'verify') {
      const v = await verifyCard(args.card);
      return rpc(id, { content: [{ type: 'text', text: JSON.stringify(v) }], structuredContent: v, isError: false });
    }
    return rpc(id, { content: [{ type: 'text', text: 'unknown tool: ' + name }], isError: true });
  }
  if (method === 'ping') return rpc(id, {});

  return rpc(id, null, -32601, 'Method not found: ' + method);
}

function rpc(id, result, code, message) {
  const body = { jsonrpc: '2.0', id };
  if (code) body.error = { code, message };
  else body.result = result;
  return new Response(JSON.stringify(body), { status: 200, headers: HEADERS });
}

async function measureAxis(axis, model) {
  try {
    const resp = await fetch(`https://csoai-gspc.pages.dev/api/measure-axis?axis=${encodeURIComponent(axis)}${model ? '&model=' + encodeURIComponent(model) : ''}`);
    return resp.ok ? await resp.json() : { error: 'measure-axis HTTP ' + resp.status };
  } catch (e) { return { error: String(e).slice(0, 80) }; }
}

async function verifyCard(card) {
  try {
    const resp = await fetch('https://csoai-gspc.pages.dev/api/verify', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(card) });
    return resp.ok ? await resp.json() : { error: 'verify HTTP ' + resp.status };
  } catch (e) { return { error: String(e).slice(0, 80) }; }
}
