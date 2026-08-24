/**
 * /api/gspc — the GSPC measurement board + axis definition feed.
 *
 * Returns the estate board (deterministic exact-label grading) + the GSPC axis
 * definitions. This is what the AG-UI dashboard's axis/chip buttons read.
 * Measurement, not certification. Verification free forever.
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
  // AXIS-14 / grammar wall: jail stays UNTESTED until earned. Exclude it from the
  // measured board and n_axes so the board honestly renders "N measured of M"
  // with jail as the empty chair. It is never rendered as measured, never implied.
  delete best.jail;
  const measured = Object.keys(best).filter(a => a !== 'jail');
  const jailStatus = 'UNTESTED — self-enforcing; flips only when its own first-row gate (frozen bank + consent gate + stranger-verified card) passes. The honesty of the board is denominated in what it refuses to claim.';
  return new Response(JSON.stringify({
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
  }), { status: 200, headers });
}
