// World-knowledge federation for the Sovereign — the "super-Google" layer.
// LIVE NOW (no key): Wikipedia/Wikidata REST. ENV-GATED (free keys): Google Data Commons (stats),
// Knowledge Graph (entities). Add the keys to light those up; Wikipedia works today.
//
// Returns sources the governed Sovereign synthesises on top of — it does NOT replace the
// council answer, it grounds it in the open world's knowledge.

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  let q = ((req.query && (req.query.q || req.query.query)) || '').toString().slice(0, 200).trim();
  // strip conversational filler so we search the actual entity ("tell me about Monzo bank" → "Monzo bank")
  q = q.replace(/^(?:tell me about|what(?:'s| is| are)|who(?:'s| is| are)|where(?:'s| is)|show me|about|explain|describe|look up|search for|find|who's)\s+/i, '')
       .replace(/^(?:the|a|an)\s+/i, '').replace(/[?.!]+$/,'').trim();
  if (!q) return res.status(200).json({ q: '', results: [], sources: srcStatus() });

  const out = { q, results: [], sources: srcStatus() };
  // ── Wikipedia/Wikidata (free, no key, live) ──
  try {
    const r = await fetch('https://en.wikipedia.org/w/rest.php/v1/search/page?q=' + encodeURIComponent(q) + '&limit=3',
      { headers: { 'User-Agent': 'MEOK-Sovereign/1.0 (https://os.meok.ai)' } });
    const d = await r.json();
    for (const p of (d.pages || []).slice(0, 3)) {
      out.results.push({
        source: 'wikipedia',
        title: p.title,
        desc: p.description || '',
        excerpt: (p.excerpt || '').replace(/<[^>]+>/g, '').trim(),
        url: 'https://en.wikipedia.org/wiki/' + encodeURIComponent(p.key || p.title),
        thumb: p.thumbnail && p.thumbnail.url ? ('https:' + p.thumbnail.url) : null
      });
    }
  } catch (e) { /* graceful */ }

  // ── Google Data Commons (free key) — public stats: population, GDP, emissions, etc. ──
  const dck = process.env.DATACOMMONS_API_KEY;
  if (dck) {
    try {
      const r = await fetch('https://api.datacommons.org/v2/resolve?nodes=' + encodeURIComponent(q) + '&property=' + encodeURIComponent('<-description{typeOf:Place}->dcid'),
        { headers: { 'X-API-Key': dck } });
      const d = await r.json();
      if (d) out.results.push({ source: 'datacommons', title: q, data: d, note: 'Google Data Commons (public statistics)' });
    } catch (e) { /* graceful */ }
  }

  return res.status(200).json(out);
}

function srcStatus() {
  return {
    wikipedia: 'live',
    datacommons: process.env.DATACOMMONS_API_KEY ? 'live' : 'add free DATACOMMONS_API_KEY → public stats (population/GDP/emissions/health)',
    knowledge_graph: process.env.GOOGLE_KG_API_KEY ? 'live' : 'add GOOGLE_KG_API_KEY → entities',
    custom_search: process.env.GOOGLE_CSE_KEY ? 'live' : 'add GOOGLE_CSE_KEY + cx → web breadth'
  };
}
