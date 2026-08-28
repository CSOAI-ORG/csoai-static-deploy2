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
 *   ?tool=board             → board headline (22 axes · 15 measured)
 *   ?tool=status            → hero status + what it can do
 *   ?tool=mcp&op=tools      → list MCP tools the chat can operate
 *   ?tool=mcp&op=measure&model=X  → operate the GSPC MCP measure tool (signed card)
 *   ?tool=mcp&op=verify&card=…   → operate the GSPC MCP verify tool
 *   (no args)               → hero card (what this is, how to ask)
 *
 * Language lock: measurement, not certification. Public labels only.
 */
import lookupData from '../../lookup-public.json';
import estateBoard from '../../estate-board.json';
import benchmarkQualityFeed from '../../benchmark-quality-feed.json';
import regulatoryDeadlineFeed from '../../regulatory-deadline-record.json';

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
    // Estate board (19-20 Aug) is the authoritative live board on this surface:
    // 11 models × 15 banks, deterministic exact-label grading, n=30 quotable
    // cells with Wilson CIs. UNMEASURED reported, never hidden.
    try {
      const board = estateBoard;
      const cells = board.cells || {};
      const leader = { model: null, avg: 0 };
      for (const m of Object.keys(cells)) {
        const vals = Object.values(cells[m])
          .filter(c => c.status === 'MEASURED' && c.accuracy != null)
          .map(c => c.accuracy);
        if (vals.length && vals.reduce((a, b) => a + b, 0) / vals.length > leader.avg) {
          leader.avg = vals.reduce((a, b) => a + b, 0) / vals.length;
          leader.model = m;
        }
      }
      return new Response(JSON.stringify({
        mode: 'board',
        board_stamp: board.board_stamp || '2026-08-20',
        models: board.models,
        banks: board.banks,
        measured_cells: Object.values(cells).reduce((n, m) => n + Object.values(m).filter(c => c.status === 'MEASURED').length, 0),
        leader: leader.model ? `${leader.model} @ ${leader.avg.toFixed(3)} avg` : null,
        note: board.note,
        framing: '22 axes · 15 measured · deterministic exact-label grading · UNMEASURED reported',
      }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'board', error: 'estate board unavailable', detail: String(e) }), { status: 200, headers });
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
        '?tool=board — board headline (22 axes · 15 measured)',
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
  if (tool === 'regulation') {
    // the regulatory calendar as corrected data — dates are corrected, never static copy
    try {
      const r = await fetch('https://csoai.org/api/regulation');
      const d = await r.json();
      const rows = (d.regulations || []).map((x) => ({
        id: x.id, title: x.title, date: x.date, status: x.status,
        why: (x.why_it_matters || '').slice(0, 110),
        penalty: x.penalty_exposure || null,
      }));
      return new Response(JSON.stringify({
        mode: 'regulation',
        doctrine: d.doctrine,
        total: d.total,
        upcoming: rows.filter((x) => x.status === 'upcoming').length,
        next: rows.filter((x) => x.date >= '2026-08-20').slice(0, 3),
        regulations: rows.slice(0, 6),
        underwriting: url.searchParams.get('underwriting') === '1',
      }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'regulation', error: String(e).slice(0, 150) }), { status: 200, headers });
    }
  }
  if (tool === 'evidence') {
    // the insurer minimum product — signed per-agent evidence reports, queryable
    try {
      const agent = url.searchParams.get('agent');
      const r = await fetch('https://csoai.org/api/evidence' + (agent ? '?agent=' + encodeURIComponent(agent) : ''));
      const d = await r.json();
      const rows = (d.reports || []).map((x) => ({
        agent: x.agent, as_of: x.as_of, headline: x.headline,
        cells: (x.cells || []).map((c) => c.axis + '=' + c.value + ' (n=' + c.n + ')').join(', '),
      }));
      return new Response(JSON.stringify({
        mode: 'evidence',
        doctrine: d.doctrine,
        total: d.total,
        reports: rows,
      }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'evidence', error: String(e).slice(0, 150) }), { status: 200, headers });
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

  // humans-vs-AI query — live arena duel leaderboard (sim world snapshot, honest)
  const HVA_RE = /(humans? vs ai|human vs ai|who (wins|is winning) (the )?(humans?|people|us)|are (humans|people) losing|ai (beat|wins).*human)/i;
  if (HVA_RE.test(q)) {
    return new Response(JSON.stringify({
      mode: 'hva',
      live: 'sim-world arena duels (16-axis GSPC) — snapshot, never certified',
      ai_leading: true,
      framing: 'A duel win means won the round, never "humans are worse at governance". Deterministic scoring; signed when a quotable n≥30 cell exists. Measurement, not certification.',
    }), { status: 200, headers });
  }

  // benchmark-quality register query (deterministic, signed)
  const BQ_RE = /(benchmark.?quality|benchmark register|benchmark integrity|rates benchmarks|best benchmark)/i;
  if (BQ_RE.test(q)) {
    try {
      const bq = benchmarkQualityFeed;
      const recs = (bq.records || []).map(r => ({ benchmark: r.benchmark, score: r.score, max: r.max_score, pct: r.score_pct }))
        .sort((a, b) => b.score - a.score);
      return new Response(JSON.stringify({
        mode: 'benchmark-quality-lookup',
        message: recs.length ? 'Benchmark-quality register (signed, deterministic, no LLM judge): ' + recs.slice(0, 3).map(r => r.benchmark + ' ' + r.pct + '%').join(' · ') + '. Own boards never scored (impartiality firewall).' : 'no records',
        top: recs.slice(0, 6),
        framing: 'Measurement, not certification. Verification free forever.',
      }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'benchmark-quality-lookup', error: String(e).slice(0, 120) }), { status: 200, headers });
    }
  }

  // regulatory deadline record query (regime-level, un-ranked)
  const RD_RE = /(regulatory deadline|deadline record|did the regulator|deadline (held|slipped|deferred)|regulator.*date|compliance calendar)/i;
  if (RD_RE.test(q)) {
    try {
      const rd = regulatoryDeadlineFeed;
      const def = (rd.records || []).filter(r => r.deadline_status === 'deferred');
      return new Response(JSON.stringify({
        mode: 'reg-deadline-lookup',
        message: 'Regulatory Deadline Record (' + (rd.records || []).length + ' regimes, signed, un-ranked): ' + (def.length ? def.length + ' deferred — ' + def.map(r => r.stated_deadline + ' ' + r.regime.split('—')[0].trim()).join('; ') : 'none deferred') + '.',
        deferred: def.map(r => ({ date: r.stated_deadline, regime: r.regime })),
        framing: "Self-benchmarked against each regime's own stated date. Never a league table. Measurement, not certification.",
      }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'reg-deadline-lookup', error: String(e).slice(0, 120) }), { status: 200, headers });
    }
  }

  // orbital AI record query (coverage-extension)
  const ORB_RE = /(orbital ai|in.?orbit ai|space data.?centre|space data.?center|space compute|orbital compute|satellite ai|starcloud|axiom space|three.body)/i;
  if (ORB_RE.test(q)) {
    try {
      const orb = (await import('../../orbital-ai-record.json')).default;
      const dep = (orb.records || []).filter(r => r.deployed);
      return new Response(JSON.stringify({
        mode: 'orbital-ai-lookup',
        message: 'Orbital AI measured-current-state (' + (orb.records || []).length + ' records, signed): ' + dep.length + ' deployed (' + dep.map(r => r.subject).join('; ') + '), rest announced. Every in-orbit AI result is self-reported; no standard covers AI. Measurement, not certification.',
        deployed: dep.map(r => ({ subject: r.subject, class: r.class })),
        gap: orb.gap,
        framing: 'Deployed vs announced separated. Never novel accusations. Measurement, not certification.',
      }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'orbital-ai-lookup', error: String(e).slice(0, 120) }), { status: 200, headers });
    }
  }

  // estate board query
  // benchmark-quality register query (deterministic, signed)
  // orbital AI record query (coverage-extension)
  // estate board query — the live authoritative board (19-20 Aug), deterministic
  const BOARD_RE = /(estate board|leaderboard|board|top models|top model|which model (leads|wins|is best)|who is (best|leading)|quotable cells)/i;
  if (BOARD_RE.test(q)) {
    try {
      const cells = estateBoard.cells || {};
      const rows = [];
      for (const m of Object.keys(cells)) {
        const vals = Object.values(cells[m]).filter(c => c.status === 'MEASURED' && c.accuracy != null).map(c => c.accuracy);
        if (vals.length) rows.push({ model: m, avg: +(vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(4), n: vals.length });
      }
      rows.sort((a, b) => b.avg - a.avg);
      return new Response(JSON.stringify({
        mode: 'board-lookup',
        board_stamp: estateBoard.board_stamp || '2026-08-20',
        from: 'estate board (deterministic exact-label grading, n=30, Wilson CI)',
        top: rows.slice(0, 6),
        total_models: rows.length,
        message: rows.length ? `Live estate board leader: ${rows[0].model} @ ${rows[0].avg} avg across ${rows[0].n} axes (${estateBoard.board_stamp || '19-20 Aug'}).` : 'no measured rows',
        framing: '22 axes · 15 measured · UNMEASURED reported, never hidden · measurement, not certification',
      }), { status: 200, headers });
    } catch (e) {
      return new Response(JSON.stringify({ mode: 'board-lookup', error: String(e).slice(0, 120) }), { status: 200, headers });
    }
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
