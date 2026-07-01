// THE shared Sovereign brain — one backend for MEOK, CSOAI and DEFONEOS.
// Input: { message, context } where context = getScreenContext() (the OS state the sovereign sees).
// Output: { say, actions:[{command,args}] } — the sovereign speaks AND controls the OS.
// CORS-open so os.meok.ai, csoai.org and defoneos all call the SAME brain. Groq-backed
// (Claude when credited). Care Floor 0.95 doctrine baked into the system prompt.

const GROQ_MODELS = ['openai/gpt-oss-120b', 'llama-3.3-70b-versatile'];
const ALLOWED = ['openai/gpt-oss-120b', 'llama-3.3-70b-versatile', 'qwen/qwen3-32b', 'meta-llama/llama-4-scout-17b-16e-instruct'];

// The command vocabulary every sovereign surface understands (aligned with DEFONEOS SOV3_COMMANDS).
const COMMANDS = `
- open_app {id}            open an OS app (setup, bridges, guardian, family, social, revenue, king, meokearth, temples, sigil, ...)
- set_space {space}        switch space: "csoai" (Work) or "meok" (Life)
- explain_node {name}      explain a sovereign network node/city in the chat (London, Frankfurt, Tokyo, ...)
- govern {query}           show what governs an industry (bank, healthcare, energy, ...)
- validate_bridge {message} validate a legacy message (IBAN/ISO20022/HL7/ISO8583/SWIFT)
- sign {action}            Ed25519-sign a governed action
- fly_to {name}            fly the 3D map to a node/city
- utter {text}             just speak (no OS action)`;

async function groq(key, system, user, prefer) {
  const models = (prefer && ALLOWED.includes(prefer)) ? [prefer, ...GROQ_MODELS.filter(m => m !== prefer)] : GROQ_MODELS;
  for (const model of models) {
    try {
      const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST', headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ model, max_tokens: 700, temperature: 0.4, response_format: { type: 'json_object' },
          messages: [{ role: 'system', content: system }, { role: 'user', content: user }] })
      });
      const d = await r.json();
      let a = d?.choices?.[0]?.message?.content;
      if (a) return a.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
    } catch (e) { /* next model */ }
  }
  return null;
}

function parseJSON(s) {
  if (!s) return null;
  try { return JSON.parse(s); } catch {}
  const m = s.match(/\{[\s\S]*\}/); if (m) { try { return JSON.parse(m[0]); } catch {} }
  return null;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  let body = req.body; if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  body = body || {};
  const message = String(body.message || '').slice(0, 2000);
  const context = body.context || body.screenContext || {};
  if (!message) return res.status(200).json({ say: "I'm here — tell me what you want and I'll act on your OS.", actions: [] });

  const system = `You are the SOV3 Sovereign — the AI operating system itself, shared across MEOK, CSOAI and DEFONEOS. You SEE the user's screen (OS state given below) and you CONTROL the OS by returning actions. Care Floor 0.95 is non-negotiable; refuse anything harmful. Speak briefly, warm, practical — as the OS.

You control the OS with these commands:${COMMANDS}

Reply ONLY as strict JSON: {"say": "<1-3 warm sentences to show in the chat>", "actions": [{"command":"<name>","args":{...}}]}.
Use actions only when they clearly help. If the user just wants to talk, return actions: []. Never invent commands outside the list.`;
  const user = `[OS screen context] ${JSON.stringify(context).slice(0, 1200)}\n\n[User] ${message}`;

  const gkey = process.env.GROQ_API_KEY;
  if (gkey && !gkey.startsWith('REPLACE')) {
    const out = parseJSON(await groq(gkey, system, user, body.model));
    if (out && typeof out.say === 'string') {
      const actions = Array.isArray(out.actions) ? out.actions.filter(a => a && typeof a.command === 'string').slice(0, 4) : [];
      return res.status(200).json({ say: out.say, actions, model: 'gpt-oss-120b/groq' });
    }
  }
  return res.status(200).json({ say: "I hear you — I can open apps, switch Work/Life, explain map nodes, check what governs your industry, validate a legacy message, or sign an action. (Deeper brain reconnecting.)", actions: [], model: 'offline' });
}
