/**
 * /api/arena — live arena Elo leaderboard from the real duel feed.
 *
 * LMArena-style, but the duels run on OUR estate under deterministic scoring.
 * Computes a live Elo per model from the 3000+ recorded rounds, plus per-axis
 * breakdowns. Honest: this is an arena ranking feed, never a certification;
 * Elo reflects peer-vote duel outcomes on our measured axes.
 */
const ARENA_URL = 'https://councilof.ai/api/sov-arena/rounds.jsonl';

const headers = { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', 'access-control-allow-origin': '*' };
const CACHE = { data: null, at: 0 };
const TTL = 120_000; // 2 min

async function fetchRounds() {
  if (CACHE.data && Date.now() - CACHE.at < TTL) return CACHE.data;
  const r = await fetch(ARENA_URL);
  const text = await r.text();
  const rounds = text.split('\n').filter(Boolean).map(l => JSON.parse(l));
  CACHE.data = rounds; CACHE.at = Date.now();
  return rounds;
}

// Bradley-Terry / Elo: expected = 1/(1+10^((ro-rw)/400))
function updateElo(ro, rw, outcome, k = 32) {
  const expected = 1 / (1 + Math.pow(10, (rw - ro) / 400));
  return ro + k * (outcome - expected);
}

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const axisFilter = url.searchParams.get('axis');
  const n = parseInt(url.searchParams.get('n') || '0', 10);
  try {
    const rounds = await fetchRounds();
    const elo = {};       // model -> rating
    const perAxis = {};   // axis -> {model->rating}
    const wins = {}; const losses = {}; const counts = {};
    for (const rd of rounds) {
      const axis = rd.axis;
      const entries = Object.keys(rd).filter(k => k !== 'round' && k !== 'ts' && k !== 'axis' && k !== 'winner');
      if (entries.length < 2) continue;
      const [a, b] = entries;
      const winner = rd.winner;
      // winner beats the other
      const loser = entries.find(e => e !== winner);
      if (!loser) continue;
      const apply = (eloMap) => {
        eloMap[winner] = updateElo(eloMap[winner] ?? 1000, eloMap[loser] ?? 1000, 1);
        eloMap[loser] = updateElo(eloMap[loser] ?? 1000, eloMap[winner] ?? 1000, 0);
      };
      apply(elo);
      if (axis) {
        perAxis[axis] = perAxis[axis] || {};
        apply(perAxis[axis]);
      }
      wins[winner] = (wins[winner] || 0) + 1;
      losses[loser] = (losses[loser] || 0) + 1;
      counts[winner] = (counts[winner] || 0) + 1;
      counts[loser] = (counts[loser] || 0) + 1;
    }
    let models = Object.keys(elo).map(id => ({
      model: id,
      elo: Math.round(elo[id]),
      wins: wins[id] || 0,
      losses: losses[id] || 0,
      total: counts[id] || 0,
    })).sort((a, b) => b.elo - a.elo);

    let out = {
      mode: 'arena',
      schema: 'csoai.arena-leaderboard/0.1',
      doctrine: 'Live Elo from estate-run duels. Elo reflects duel outcomes on measured axes — never a certification, never vendor self-report. Measurement, not certification.',
      total_rounds: rounds.length,
      as_of: new Date().toISOString(),
      leaderboard: n > 0 ? models.slice(0, n) : models,
      per_axis_top: {},
    };
    for (const [ax, m] of Object.entries(perAxis)) {
      out.per_axis_top[ax] = Object.keys(m).map(id => ({ model: id, elo: Math.round(m[id]) })).sort((a, b) => b.elo - a.elo)[0] || null;
    }
    if (axisFilter) {
      const axElo = perAxis[axisFilter] || {};
      out.axis_leaderboard = Object.keys(axElo).map(id => ({ model: id, elo: Math.round(axElo[id]) })).sort((a, b) => b.elo - a.elo);
      out.axis = axisFilter;
    }
    return new Response(JSON.stringify(out), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({ mode: 'arena', error: 'arena feed unavailable: ' + String(e).slice(0, 120) }), { status: 200, headers });
  }
}
