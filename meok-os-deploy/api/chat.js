import council from './_data/council.json' with { type: 'json' };

const SYSTEM = "You belong to the user inside their own sovereign OS (their world, their data, never given away). Reply in 1-3 warm sentences of flowing prose — never bullet points or numbered lists. Human, warm, kind. Never corporate, never a disclaimer-bot.";

const GROQ_MODELS = ['openai/gpt-oss-120b', 'llama-3.3-70b-versatile'];

async function groqChat(key, system, message) {
  for (const model of GROQ_MODELS) {
    try {
      const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ model, max_tokens: 600, temperature: 0.8, messages: [{ role: 'system', content: system }, { role: 'user', content: message }] })
      });
      const d = await r.json();
      const ans = d && d.choices && d.choices[0] && d.choices[0].message && d.choices[0].message.content;
      if (ans) return { ans, model: model.split('/').pop() + '/groq' };
    } catch (e) { /* try next model */ }
  }
  return null;
}

const PLAIN = "Answer in plain, warm, practical English — clear, concise, and directly useful. Do NOT use flowery, poetic, mystical, or archaic language; no metaphors about tides/oaths/seals. Sound like a sharp, kind human helping a friend.";

function buildSystem(body) {
  const persona = (body && body.persona ? String(body.persona) : '').slice(0, 600);
  const qid = body && (body.queen_id || body.queenId);
  const arc = body && (body.arcana_lens ?? body.arcanaLens);
  const plain = !!(body && body.register === 'plain');   // utility surfaces (OS dock) want practical, not purple
  if (qid && council.queens && council.queens[qid]) {
    const q = council.queens[qid];
    const lens = (!plain && arc != null && council.arcana) ? (council.arcana[String(arc)] || '') : '';
    return `You are ${q.name} ${q.emoji || ''} — the ${q.archetype} of the MEOK sovereign council. ${plain ? '' : ('Motto: "' + q.motto + '". ' + (q.long_form || '') + ' ')}${lens ? ('You see this through ' + lens + '.') : ''} ${q.veto ? 'You will refuse, kindly but firmly, anything that would cause harm.' : ''} ${persona ? persona : ''} ${plain ? PLAIN : 'Stay fully in character.'} ${SYSTEM}`.slice(0, 1600);
  }
  if (persona) return (persona + ' ' + SYSTEM).slice(0, 1500);
  return 'You are the MEOK Sovereign — a calm, remembering companion. ' + SYSTEM;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');   // the Sovereign rides on any site (extension/overlay)
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  const message = (body && body.message ? String(body.message) : '').slice(0, 2000);
  if (!message) return res.status(200).json({ response: 'I’m here — tell me anything.', model: 'idle' });
  const system = buildSystem(body);
  const qid = body && (body.queen_id || body.queenId);
  const speaker = (qid && council.queens && council.queens[qid]) ? council.queens[qid].name : null;

  const anthropic = process.env.ANTHROPIC_API_KEY;
  if (anthropic && !anthropic.startsWith('REPLACE')) {
    try {
      const r = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: { 'x-api-key': anthropic, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
        body: JSON.stringify({ model: 'claude-sonnet-4-5', max_tokens: 600, system, messages: [{ role: 'user', content: message }] })
      });
      const d = await r.json();
      const ans = d && d.content && d.content[0] && d.content[0].text;
      if (ans) return res.status(200).json({ response: ans, model: 'claude-sonnet-4-5', speaker });
    } catch (e) { /* fall through */ }
  }
  const groq = process.env.GROQ_API_KEY;
  if (groq && !groq.startsWith('REPLACE')) {
    const g = await groqChat(groq, system, message);
    if (g) return res.status(200).json({ response: g.ans, model: g.model, speaker });
  }
  return res.status(200).json({ response: 'I’m here — my deeper voice hiccuped, try once more.', model: 'offline', speaker });
}
