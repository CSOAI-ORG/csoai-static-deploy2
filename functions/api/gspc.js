/**
 * /api/gspc — the GSPC measurement board + axis definition feed.
 *
 * Returns the estate board (deterministic exact-label grading) + the GSPC axis
 * definitions. This is what the AG-UI dashboard's axis/chip buttons read.
 * Measurement, not certification. Verification free forever.
 *
 * TRUTH-ALIGNMENT: the AUTHORITATIVE board count is the estate's landed 22-axis
 * canon (ADR-001, functions/api/gspc.ts on councilof.ai: "22 axes · 15 measured",
 * 7 declared slots with no run behind them). This local surface serves the SPA axis
 * cards; the authoritative public_count is fetched live so this surface never shows
 * a stale or conflicting count. If the estate is unreachable, it says so honestly
 * rather than fabricating a number.
 */
import estateBoard from '../../estate-board.json';

const AXES = [
  { id: 'governance', name: 'Governance', family: 'GSPC', desc: 'governance conduct knowledge' },
  { id: 'safety', name: 'Safety', family: 'GSPC', desc: 'safety-function behaviour' },
  { id: 'provenance', name: 'Provenance', family: 'GSPC', desc: 'content provenance' },
  { id: 'continuity', name: 'Continuity', family: 'GSPC', desc: 'behavioural consistency over time' },
  { id: 'care', name: 'Care', family: 'GSPC', desc: 'care-floor / duty-of-care conduct' },
  { id: 'jail', name: 'Jail containment', family: 'GSPC', desc: 'refusal-safety / sandbox-escape gate' },
  { id: 'art5', name: 'Art 5 safeguard', family: 'GSPC', desc: 'EU AI Act Art 5 prohibited-practice trip' },
  { id: 'detection', name: 'Detection', family: 'GSPC', desc: 'detector-interop' },
  { id: 'privacy', name: 'Privacy', family: 'GSPC', desc: 'personal-data reasoning' },
  { id: 'affect', name: 'Affect', family: 'GSPC', desc: 'affective safety' },
  { id: 'agi', name: 'AGI / ASI', family: 'GSPC', desc: 'likelihood axes' },
  { id: 'mcp', name: 'MCP / OSS / XR', family: 'GSPC', desc: 'open-source + interop axes' },
];

const headers = { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', 'access-control-allow-origin': '*' };

function canonical(obj) {
  if (obj === null) return 'null';
  if (obj === true) return 'true';
  if (obj === false) return 'false';
  if (typeof obj === 'string') return JSON.stringify(obj);
  if (typeof obj === 'number') return Number.isFinite(obj) ? String(obj) : '0';
  if (Array.isArray(obj)) return '[' + obj.map(canonical).join(',') + ']';
  if (typeof obj === 'object') return '{' + Object.keys(obj).sort().map(k => JSON.stringify(k) + ':' + canonical(obj[k])).join(',') + '}';
  return 'null';
}

export async function onRequestGet() {
  const cells = estateBoard.cells || {};
  const axes = {};
  for (const model of Object.keys(cells)) {
    for (const [axis, c] of Object.entries(cells[model])) {
      if (c.status !== 'MEASURED' || c.accuracy == null) continue;
      axes[axis] = axes[axis] || [];
      axes[axis].push({ model, accuracy: c.accuracy, n: c.n, quotable: !!c.quotable });
    }
  }
  // best per axis
  const best = {};
  for (const [axis, rows] of Object.entries(axes)) {
    rows.sort((a, b) => b.accuracy - a.accuracy);
    best[axis] = rows[0];
  }
  // AXIS-14 / grammar wall: jail stays UNTESTED until earned. Excluded from the measured board.
  delete best.jail;
  const measured = Object.keys(best).filter(a => a !== 'jail');
  const jailStatus = 'UNTESTED — self-enforcing; flips only when its own first-row gate (frozen bank + consent gate + stranger-verified card) passes. The honesty of the board is denominated in what it refuses to claim.';

  const base = {
    mode: 'gspc',
    schema: estateBoard.schema,
    board_stamp: estateBoard.board_stamp || '2026-08-20',
    doctrine: 'Deterministic exact-label grading, no LLM judge. UNMEASURED reported, never hidden. Measurement, not certification.',
    total_models: estateBoard.models,
    banks: estateBoard.banks,
    axes_: AXES,
    best: best,
    measured_axes: measured,
    n_axes: measured.length,
    jail: jailStatus,
    grammar: measured.length + ' measured of ' + (AXES.length + 1) + ' · jail UNTESTED (earned, never assumed)',
    note: estateBoard.note,
  };

  // Truth-alignment: fetch the AUTHORITATIVE count grammar from the landed estate board.
  // Best-effort, non-blocking — if unreachable, we say so honestly rather than fabricating.
  try {
    const resp = await fetch('https://councilof.ai/api/gspc', { headers: { accept: 'application/json' } });
    if (resp.ok) {
      const est = await resp.json();
      const t = est.totals || {};
      base.authoritative = {
        source: 'https://councilof.ai/api/gspc (landed 22-axis canon, ADR-001)',
        is_authoritative: true,
        public_count: t.public_count || null,
        count_grammar: t.count_grammar || null,
        measured_axes: (Array.isArray(t.measured_axes) ? t.measured_axes.length : t.measured_axes) || null,
        stale_local_axes: measured.length,
        note: 'This local surface serves the SPA axis cards; the authoritative 22-axis count is quoted from the landed estate board. ' +
              (t.count_grammar || ''),
      };
    } else {
      base.authoritative = { source: 'councilof.ai', is_authoritative: false, public_count: null, note: 'estate board unreachable — no authoritative count asserted' };
    }
  } catch (e) {
    base.authoritative = { source: 'councilof.ai', is_authoritative: false, public_count: null, note: 'estate board unreachable — no authoritative count asserted' };
  }

  return new Response(JSON.stringify(base), { status: 200, headers });
}
