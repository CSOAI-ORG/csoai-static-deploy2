// Cloudflare Pages Function — OpenAI-compatible chat completions bridge
// POST /api/council-bridge with OpenAI-format messages
// Routes to Ollama (localhost:11434) or returns a mock response

const OLLAMA_URL = 'http://localhost:11434';

function mockChatResponse(messages) {
  const last = messages[messages.length - 1];
  const content = last?.content || 'No input provided.';
  return {
    id: `chatcmpl-mock-${Date.now()}`,
    object: 'chat.completion',
    created: Math.floor(Date.now() / 1000),
    model: 'Council-bridge-mock',
    choices: [
      {
        index: 0,
        message: {
          role: 'assistant',
          content: `[SOV Bridge Mock] Received ${messages.length} message(s). Last: "${content.slice(0, 120)}". Ollama is not reachable from this environment — deploy to a worker with local Ollama access for live responses.`,
        },
        finish_reason: 'stop',
      },
    ],
    usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 },
  };
}

export async function onRequest(context) {
  const { request, env } = context;
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Content-Type': 'application/json',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers });
  }
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed — use POST' }), { status: 405, headers });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), { status: 400, headers });
  }

  const messages = body.messages || [];
  const model = body.model || 'Council-master-v2:latest';
  const ollamaUrl = env?.OLLAMA_URL || OLLAMA_URL;

  // Try Ollama
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);

    const r = await fetch(`${ollamaUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        messages: messages.map((m) => ({ role: m.role, content: m.content })),
        stream: false,
      }),
      signal: controller.signal,
    });
    clearTimeout(timeout);

    if (r.ok) {
      const data = await r.json();
      const reply = data.message?.content || '';
      return new Response(
        JSON.stringify({
          id: `chatcmpl-council-${Date.now()}`,
          object: 'chat.completion',
          created: Math.floor(Date.now() / 1000),
          model: data.model || model,
          choices: [
            {
              index: 0,
              message: { role: 'assistant', content: reply },
              finish_reason: 'stop',
            },
          ],
          usage: {
            prompt_tokens: data.prompt_eval_count || 0,
            completion_tokens: data.eval_count || 0,
            total_tokens: (data.prompt_eval_count || 0) + (data.eval_count || 0),
          },
          ollama_total_duration_ms: data.total_duration ? Math.round(data.total_duration / 1e6) : null,
        }),
        { status: 200, headers },
      );
    }
  } catch {
    // Ollama not reachable — fall through to mock
  }

  // Mock fallback
  return new Response(JSON.stringify(mockChatResponse(messages)), { status: 200, headers });
}
