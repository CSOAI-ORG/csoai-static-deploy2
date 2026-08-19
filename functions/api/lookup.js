/**
 * /api/lookup — the enforced-escort front door on the site (move 27).
 *
 * Deterministic, zero-model covered-query answers from the signed mine corpus
 * (public rail only: trusted axes with usable n≥30; UNMEASURED is never
 * fabricated). Mirrors the enforced-escort finding of 18 Aug 2026: 4B-class
 * models do NOT reliably call lookup tools, so the front door ENFORCES the
 * lookup deterministically — no model in the path for covered queries.
 *
 * Covered query = a model name + a score-intent word (care/gov/swag/art5/
 * score/axis/quotable/overall/accuracy/elo). Anything else answers a
 * non-committal "covered-query" hint, never a generated claim.
 *
 * Data: lookup-public.json (built from mine-learnt.json by the mine lane,
 * public rail only — verified signature on the source corpus).
 */
import lookupData from '../../lookup-public.json';

const LOOKUP_RE = /(care|gov|swag|art5|score|quotable|axis|overall|accuracy|elo|refusal|protect)\b/i;
const MODEL_RE = /([a-z0-9][a-z0-9._:-]*\d[.0-9b:-]*|[a-z0-9-]+:[a-z0-9._-]+)/i;

function findModel(query) {
  const m = MODEL_RE.exec(query);
  if (!m) return { hit: null, loose: false };
  const wanted = m[1].toLowerCase();
  const exact = lookupData.models[wanted];
  if (exact) return { hit: wanted, loose: false };
  // loose: same base family (before ":")
  const base = wanted.split(':')[0];
  for (const name of Object.keys(lookupData.models)) {
    if (name.split(':')[0] === base) return { hit: name, loose: true };
  }
  return { hit: null, loose: false };
}

export async function onRequestGet({ request, params, waitUntil, next, data }) {
  const url = new URL(request.url);
  const q = (url.searchParams.get('q') || '').trim();
  const headers = {
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store',
  };
  if (!q) {
    return new Response(JSON.stringify({ error: 'q required' }), { status: 400, headers });
  }
  if (!LOOKUP_RE.test(q)) {
    return new Response(JSON.stringify({
      mode: 'covered-query-hint',
      message: 'Ask for a model + a score word (e.g. "qwen2.5:7b care score") and I answer from the signed corpus, deterministically.',
      framing: lookupData.framing,
    }), { status: 200, headers });
  }
  const { hit, loose } = findModel(q);
  if (!hit) {
    return new Response(JSON.stringify({
      mode: 'covered-query-no-hit',
      message: 'No signed record for that model on the public rail (models with quotable cells are listed).',
      n_models: lookupData.n_models,
      leaders: lookupData.leaders,
      framing: lookupData.framing,
    }), { status: 200, headers });
  }
  const rec = lookupData.models[hit];
  const axes = Object.entries(rec.axes || {}).map(([k, v]) => ({
    axis: k, accuracy: v.v, n: v.n,
  })).sort((a, b) => b.accuracy - a.accuracy);
  return new Response(JSON.stringify({
    mode: 'lookup',
    from: 'signed mine corpus (public rail)',
    model: hit,
    loose_match: loose,
    quotable_overall: rec.quotable ?? null,
    raw_overall: rec.raw ?? null,
    art5_accuracy: rec.art5 ?? null,
    suspect_axes: rec.suspect ?? null,
    axes,
    framing: lookupData.framing,
    leaders: lookupData.leaders,
  }), { status: 200, headers });
}
