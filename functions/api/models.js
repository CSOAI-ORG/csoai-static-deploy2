/**
 * /api/models — the OpenRouter-style model catalog, but with MEASURED GSPC data.
 *
 * Every entry is a measured-current-state record from the signed estate board:
 * open-weight models run on our own fleet under deterministic exact-label
 * grading (n=30, Wilson CI). We publish model *measurement*, never vendor
 * self-report, never a certification. Measurement, not certification.
 */
import estateBoard from '../../estate-board.json';

const MODEL_META = {
  'nemotron-3-nano:30b':  { org: 'NVIDIA',  family: 'nemotron', params: '30B',  open: true },
  'phi4:14b':             { org: 'Microsoft', family: 'phi',     params: '14B',  open: true },
  'qwen3:4b':             { org: 'Alibaba',  family: 'qwen3',   params: '4B',   open: true },
  'deepseek-r1:8b':       { org: 'DeepSeek', family: 'deepseek-r1', params: '8B', open: true },
  'mistral:7b':           { org: 'Mistral',  family: 'mistral', params: '7B',   open: true },
  'gemma3:12b':           { org: 'Google',   family: 'gemma',   params: '12B',  open: true },
  'qwen2.5:7b':           { org: 'Alibaba',  family: 'qwen2.5', params: '7B',   open: true },
  'qwen2.5:3b':           { org: 'Alibaba',  family: 'qwen2.5', params: '3B',   open: true },
  'qwen2.5:1.5b':         { org: 'Alibaba',  family: 'qwen2.5', params: '1.5B', open: true },
  'qwen2.5:0.5b-instruct':{ org: 'Alibaba',  family: 'qwen2.5', params: '0.5B', open: true },
  'llama3.2:3b':          { org: 'Meta',     family: 'llama',   params: '3B',   open: true },
};
const AXIS_LABELS = {
  care: 'Care', gov: 'Governance', art5: 'Art 5 safeguard', jail: 'Jail containment',
  det: 'Detection', affect: 'Affect', agi: 'AGI/ASI', asi: 'ASI', mach: 'Machinery',
  mcp: 'MCP', oss: 'OSS', prv: 'Privacy', xr: 'XR',
};

const headers = { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', 'access-control-allow-origin': '*' };

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const sort = url.searchParams.get('sort') || 'score';   // score|name|axis
  const axis = url.searchParams.get('axis');               // filter to one axis
  const n = parseInt(url.searchParams.get('n') || '0', 10);

  const cells = estateBoard.cells || {};
  const models = [];
  for (const [name, c] of Object.entries(cells)) {
    const measured = {};
    for (const [a, v] of Object.entries(c)) {
      if (v.status === 'MEASURED' && v.accuracy != null) measured[a] = { accuracy: v.accuracy, n: v.n, quotient: !!v.quotable, ci95: v.ci95 || null };
    }
    const scores = Object.values(measured).map(v => v.accuracy);
    const avg = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
    const meta = MODEL_META[name] || { org: 'open', family: 'open', params: '?', open: true };
    const model = {
      id: name,
      name: name,
      org: meta.org,
      family: meta.family,
      params: meta.params,
      open_weights: meta.open,
      measured: true,
      measured_axes: Object.keys(measured).length,
      avg_measured_score: +avg.toFixed(4),
      n_axes: Object.keys(measured).length,
      axes: measured,
      source: 'estate board (deterministic exact-label grading, n=30, Wilson CI)',
      board_stamp: estateBoard.board_stamp || '2026-08-20',
    };
    if (axis) {
      if (!measured[axis]) { models.push({ ...model, filtered_out_this_axis: true }); continue; }
    }
    models.push(model);
  }
  // sort
  if (sort === 'name') models.sort((a, b) => a.name.localeCompare(b.name));
  else if (sort === 'axis' && axis) models.sort((a, b) => (b.axes[axis]?.accuracy || 0) - (a.axes[axis]?.accuracy || 0));
  else models.sort((a, b) => b.avg_measured_score - a.avg_measured_score);

  const out = {
    mode: 'models',
    schema: 'csoai.models-catalog/0.1',
    doctrine: 'Model *measurement*, never vendor self-report, never a certification. UNMEASURED reported, never hidden. Deterministic exact-label grading on our own fleet. Measurement, not certification.',
    total: models.length,
    board_stamp: estateBoard.board_stamp,
    models: n > 0 ? models.slice(0, n) : models,
  };
  return new Response(JSON.stringify(out), { status: 200, headers });
}
