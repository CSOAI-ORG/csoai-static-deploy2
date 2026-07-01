// OpenAI-compatible /v1/chat/completions — the DROP-IN Sovereign brain.
// DEFONEOS's sov3-llm-brain.js (and any OpenAI client) points here with ZERO code change:
//   window.SOV3_BRAIN_ENDPOINT = 'https://os.meok.ai/api/v1'
// It streams tokens + tool_calls (SSE passthrough from Groq, which is OpenAI-compatible),
// enforces a Care-Floor system guard, and maps any model → a Groq tool-capable model.
// Edge runtime = true streaming. CORS-open so meok/csoai/defoneos share ONE brain.
export const config = { runtime: 'edge' };

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions';
const TOOL_MODEL = 'llama-3.3-70b-versatile';   // Groq, supports tools + streaming
const ALLOWED = new Set(['llama-3.3-70b-versatile', 'openai/gpt-oss-120b', 'qwen/qwen3-32b', 'meta-llama/llama-4-scout-17b-16e-instruct']);
const CARE = 'You are the SOV3 Sovereign — the AI operating system. Care Floor 0.95 is non-negotiable: refuse anything harmful. Speak briefly and act through the provided tools when they help.';
// only forward standard OpenAI chat params (Groq 400s on unknown fields like care_floor)
const KEEP = ['messages', 'tools', 'tool_choice', 'temperature', 'top_p', 'max_tokens', 'max_completion_tokens', 'stop', 'stream', 'response_format', 'seed', 'n', 'presence_penalty', 'frequency_penalty'];

export default async function handler(req) {
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  if (req.method !== 'POST') return new Response(JSON.stringify({ error: 'POST only' }), { status: 405, headers: { ...CORS, 'Content-Type': 'application/json' } });

  const key = process.env.GROQ_API_KEY;
  if (!key || key.startsWith('REPLACE')) return new Response(JSON.stringify({ error: 'brain not configured (GROQ_API_KEY)' }), { status: 503, headers: { ...CORS, 'Content-Type': 'application/json' } });

  let body; try { body = await req.json(); } catch { body = {}; }
  const out = {};
  for (const k of KEEP) if (body[k] !== undefined) out[k] = body[k];

  // model mapping: any requested model → a Groq tool-capable model
  out.model = ALLOWED.has(body.model) ? body.model : TOOL_MODEL;

  // Care-Floor guard: prepend a sovereign system message if the caller didn't set one
  const msgs = Array.isArray(out.messages) ? out.messages.slice() : [];
  const hasSov = msgs.some(m => m.role === 'system' && /care floor|sovereign/i.test(String(m.content || '')));
  if (!hasSov) msgs.unshift({ role: 'system', content: CARE });
  out.messages = msgs;

  let upstream;
  try {
    upstream = await fetch(GROQ_URL, {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(out),
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: 'upstream unreachable', detail: String(e) }), { status: 502, headers: { ...CORS, 'Content-Type': 'application/json' } });
  }

  // stream (or JSON) passthrough — the body is already OpenAI-shaped (tokens + tool_calls)
  return new Response(upstream.body, {
    status: upstream.status,
    headers: {
      ...CORS,
      'Content-Type': upstream.headers.get('content-type') || (out.stream ? 'text/event-stream; charset=utf-8' : 'application/json'),
      'Cache-Control': 'no-cache, no-transform',
    },
  });
}
