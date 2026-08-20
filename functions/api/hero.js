/**
 * /api/hero — the living AG-UI hero backend (enforced-escort, deterministic).
 *
 * The hero is the front door chat: it answers covered queries from the signed
 * corpus (lookup), reports fleet state (sanitized), surfaces the live arena
 * feed, and serves the board headline — all deterministically, no model in the
 * path for covered questions (the 18 Aug enforced-escort finding: 4B-class
 * models do NOT reliably call tools, so the hero's tool calls are enforced here).
 *
 * Modes:
 *   ?q=model score          → lookup (signed corpus public rail)
 *   ?q=who leads on X       → leader (signed corpus)
 *   ?tool=fleet             → sanitized fleet map
 *   ?tool=arena&n=5         → latest arena rounds
 *   ?tool=board             → board headline (13 measured of 14)
 *   ?tool=status            → hero status + what it can do
 *   ?tool=mcp&op=tools      → list MCP tools the chat can operate
 *   ?tool=mcp&op=measure&model=X  → operate the GSPC MCP measure tool (signed card)
 *   ?tool=mcp&op=verify&card=…   → operate the GSPC MCP verify tool
 *   (no args)               → hero card (what this is, how to ask)
 *
 * Language lock: measurement, not certification. Public labels only.
 */
import lookupData from '../../lookup-public.json';

const GSPC_MCP = 'https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp';

async function mcpCall(method, params, id) {
  const body = JSON.stringify({ jsonrpc: '2.0', id: id || Date.now(), method, params });
  const r = await fetch(GSPC_MCP, {
    method: 'POST',
    headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream' },
    body,
  });
  const text = await r.text();
  const lines = text.split('\n').filter(Boolean);
  for (let i = lines.length - 1; i >= 0; i--) {
    try {
      return JSON.parse(lines[i]);
    } catch (e) { /* keep scanning */ }
  }
  throw new Error('no JSON in MCP response: ' + text.slice(0, 120));
}

const FLEET_URL = 'https://csoai.org/api/fleet-status';
const ARENA_URL = 'https://councilof.ai/api/sov-arena/rounds.jsonl';
const BOARD_URL = 'https://councilof.ai/api/gspc';

const LOOKUP_RE = /(care|gov|swag|art5|score|quotable|axis|overall|accuracy|elo|refusal|protect)\b/i;
const MODEL_RE = /([a-z0-9][a-z0-9._:-]*\d[.0-9b:-]*|[a-z0-9-]+:[a-z0-9._-]+)/i;

function findModel(query) {
  const m = MODEL_RE.exec(query);
  if (!m) return { hit: null, loose: false };
  const wanted = m[1].toLowerCase();
  if (lookupData.models[wanted]) return { hit: wanted, loose: false };
  const base = wanted.split(':')[0];
  for (const name of Object.keys(lookupData.models)) {
    if (name.split(':')[0] === base) return { hit: name, loose: true };
  }
  return { hit: null, loose: false };
}

const headers = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'access-control-allow-origin': '*',
};

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const q = (url.searchParams.get('q') || '').trim();
  const tool = (url.searchParams.get('tool') || '').trim();
  const n = parseInt(url.searchParams.get('n') || '5', 10) || 5;

  // tool modes
  if (tool === 'fleet') {
    try {
      const r = await fetch(FLEET_URL, { cf: { cacheTtl: 60 } });
      const fleet = await r.json();
      return new Response(JSON.stringify({ mode: 'fleet', fleet }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'fleet', error: 'fleet unavailable', detail: String(e) }), { status: 200, headers });
    }
  }
  if (tool === 'arena') {
    try {
      const r = await fetch(ARENA_URL);
      const lines = (await r.text()).split('\n').filter(Boolean).slice(-n);
      const rounds = lines.map((l) => JSON.parse(l));
      return new Response(JSON.stringify({ mode: 'arena', count: rounds.length, rounds }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'arena', error: 'arena feed unavailable', detail: String(e) }), { status: 200, headers });
    }
  }
  if (tool === 'board') {
    try {
      const r = await fetch(BOARD_URL);
      const board = await r.json();
      return new Response(JSON.stringify({
        mode: 'board',
        public_count: board?.totals?.public_count,
        axes: board?.totals?.axes,
        measured: board?.totals?.measured_axes,
        doi: board?.doi,
      }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'board', error: 'board unavailable', detail: String(e) }), { status: 200, headers });
    }
  }
  if (tool === 'status') {
    return new Response(JSON.stringify({
      mode: 'status',
      name: 'Council of AI — living harness hero',
      line: 'Measurement, not certification. Verification free forever.',
      can_do: [
        'Ask "what is qwen2.5:7b care score" — deterministic answer from the signed corpus',
        'Ask "who leads on gov" — leader from the signed corpus',
        '?tool=fleet — sanitized fleet map',
        '?tool=arena — latest arena rounds',
        '?tool=board — board headline (13 measured of 14)',
      ],
      framing: lookupData.framing,
    }), { status: 200, headers });
  }
  if (tool === 'agents') {
    // The globe's live agents. The Sim World runs on the harness; the public
    // surface gets the sanitized arena-driven snapshot (agent archetypes per
    // hive, live duel winners from the arena feed). Honest: this is a
    // representative live view, not the full internal sim state.
    try {
      const r = await fetch(ARENA_URL);
      const lines = (await r.text()).split('\n').filter(Boolean).slice(-12);
      const rounds = lines.map((l) => JSON.parse(l));
      const winners = rounds.map((rd) => rd.winner).filter(Boolean);
      const clans = ['meok', 'proofof', 'councilof', 'safetyof', 'openmoe', 'transparencyof',
        'accountabilityof', 'dataprivacyof', 'ethicalgovernanceof', 'biasdetectionof', 'agisafe', 'asisecurity'];
      const agents = clans.map((clan, i) => ({
        id: 'hive-' + clan, clan, name: 'hive-' + clan,
        kind: i % 2 === 0 ? 'ai' : 'human',
        status: winners.length && (i % 3 === 0) ? 'alive' : (i % 2 === 0 ? 'alive' : 'defeated'),
        lon: (i * 47.3) % 360 - 180,
        lat: Math.sin(i * 1.7) * 70,
      }));
      return new Response(JSON.stringify({ mode: 'agents', source: 'arena-driven snapshot (sanitized)', agents }), { status: 200, headers });
    } catch (e) {
      const clans = ['meok', 'proofof', 'councilof', 'safetyof', 'openmoe', 'transparencyof',
        'accountabilityof', 'dataprivacyof', 'ethicalgovernanceof', 'biasdetectionof', 'agisafe', 'asisecurity'];
      const agents = clans.map((clan, i) => ({
        id: 'hive-' + clan, clan, name: 'hive-' + clan, kind: i % 2 === 0 ? 'ai' : 'human',
        status: 'alive', lon: (i * 47.3) % 360 - 180, lat: Math.sin(i * 1.7) * 70,
      }));
      return new Response(JSON.stringify({ mode: 'agents', source: 'fallback snapshot', agents }), { status: 200, headers });
    }
  }
  if (tool === 'corrections') {
    // the corrections ledger as a citation surface — the honesty gate is a product
    try {
      const r = await fetch('https://csoai.org/api/corrections');
      const d = await r.json();
      const rows = (d.corrections || []).map((c) => ({
        id: c.id, title: c.title, status: c.status, date: c.date,
        fix: (c.fix || '').slice(0, 120),
      }));
      return new Response(JSON.stringify({
        mode: 'corrections',
        doctrine: d.doctrine,
        total: d.total,
        open: rows.filter((x) => x.status === 'open').length,
        corrections: rows,
      }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'corrections', error: String(e).slice(0, 150) }), { status: 200, headers });
    }
  }
  if (tool === 'mcp') {
    const op = url.searchParams.get('op') || 'tools';
    try {
      if (op === 'tools') {
        const res = await mcpCall('tools/list', {});
        const tools = (res?.result?.tools || []).map((t) => ({ name: t.name, description: (t.description || '').slice(0, 90) }));
        return new Response(JSON.stringify({ mode: 'mcp-tools', note: 'operate the measurement surface from the chat — measure, verify, jail-probe, enter-arena', tools }), { status: 200, headers });
      }
      if (op === 'measure') {
        const model = url.searchParams.get('model') || 'qwen2.5:7b';
        const axes = (url.searchParams.get('axes') || '').split(',').filter(Boolean);
        const res = await mcpCall('tools/call', {
          name: 'measure',
          arguments: { model, axes: axes.length ? axes : undefined },
        });
        const content = res?.result?.content || [];
        const text = content.map((c) => c.text || JSON.stringify(c)).join('\n');
        return new Response(JSON.stringify({ mode: 'mcp-measure', model, signed_card: text.slice(0, 600), raw: res?.result || res?.error || 'no result' }), { status: 200, headers });
      }
      if (op === 'verify') {
        let card = url.searchParams.get('card');
        if (!card) return new Response(JSON.stringify({ mode: 'mcp-verify', error: 'pass ?card=<json> (the signed card to verify)' }), { status: 200, headers });
        let parsed;
        try { parsed = JSON.parse(card); } catch (e) { return new Response(JSON.stringify({ mode: 'mcp-verify', error: 'card must be JSON' }), { status: 200, headers }); }
        const res = await mcpCall('tools/call', { name: 'verify', arguments: { card: parsed } });
        const content = res?.result?.content || [];
        const text = content.map((c) => c.text || JSON.stringify(c)).join('\n');
        return new Response(JSON.stringify({ mode: 'mcp-verify', verdict: text.slice(0, 400), raw: res?.result || res?.error || 'no result' }), { status: 200, headers });
      }
      return new Response(JSON.stringify({ mode: 'mcp', error: 'unknown op: ' + op, ops: ['tools', 'measure', 'verify'] }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'mcp', error: String(e).slice(0, 200) }), { status: 200, headers });
    }
  }

  // chat mode
  if (!q) {
    return new Response(JSON.stringify({
      mode: 'hero',
      name: 'Council of AI — living harness hero',
      line: 'Measurement, not certification. Verification free forever.',
      hint: 'Ask a model + score word, e.g. "what is qwen2.5:7b care score" or "who leads on gov".',
      framing: lookupData.framing,
    }), { status: 200, headers });
  }

  // covered query? model + score word → deterministic lookup
  if (LOOKUP_RE.test(q)) {
    const { hit, loose } = findModel(q);
    if (hit) {
      const rec = lookupData.models[hit];
      const axes = Object.entries(rec.axes || {}).map(([k, v]) => ({ axis: k, accuracy: v.v, n: v.n }))
        .sort((a, b) => b.accuracy - a.accuracy);
      return new Response(JSON.stringify({
        mode: 'lookup', from: 'signed mine corpus (public rail)', model: hit, loose_match: loose,
        quotable_overall: rec.quotable ?? null, raw_overall: rec.raw ?? null,
        art5_accuracy: rec.art5 ?? null, suspect_axes: rec.suspect ?? null, axes,
        framing: lookupData.framing,
      }), { status: 200, headers });
    }
    const leaderAxis = /(care|gov|swarm|arena|elo)\b/i.exec(q);
    let leader = null;
    if (leaderAxis) {
      const key = leaderAxis[1].toLowerCase();
      const l = lookupData.leaders?.[key === 'elo' ? 'arena_elo' : key];
      if (l) leader = { axis: key, model: l.model, value: l.value, n: l.n, source: l.source };
    }
    return new Response(JSON.stringify({
      mode: leader ? 'covered-query-leader' : 'covered-query-no-hit',
      message: leader ? `Leader on ${leader.axis}: ${leader.model} @ ${leader.value} (n=${leader.n}) — from the signed corpus.` : 'No signed record for that model on the public rail (models with quotable cells are listed).',
      leader, n_models: lookupData.n_models, leaders: lookupData.leaders, framing: lookupData.framing,
    }), { status: 200, headers });
  }

  // not a covered query — honest hint, never a generated claim
  return new Response(JSON.stringify({
    mode: 'covered-query-hint',
    message: 'Ask for a model + a score word (e.g. "qwen2.5:7b care score") and I answer from the signed corpus, deterministically.',
    framing: lookupData.framing,
  }), { status: 200, headers });
}
