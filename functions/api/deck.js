// Cloudflare Pages Function — GET /api/deck (Wave-3 visual-mind surface)
// Serves the J-space deck + C-space fold as JSON. Data ships via the
// build allowlist (jspace_deck.json + c_space_card.json in _site/), this
// function reads the built copies at the site root.
// Honest: the deck is a deterministic fold of the KB facts (no synthetic
// "model DNA"); the sigil SVGs are pure functions of card hashes.

export async function onRequest(context) {
  const { env, request } = context;
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json',
    'Cache-Control': 'public, max-age=300',
  };
  const url = new URL(request.url);
  const want = url.searchParams.get('view') || 'deck';

  // Static files ship at _site/{jspace_deck,c_space_card}.json via the
  // build allowlist; this function reads them from the site origin.
  const deckResp = await fetch(new URL('/jspace_deck.json', url.origin)).catch(() => null);
  const ccardResp = await fetch(new URL('/c_space_card.json', url.origin)).catch(() => null);

  if (want === 'c-card') {
    if (!ccardResp || !ccardResp.ok) return new Response(JSON.stringify({error:'C-card not found'}), {status:404, headers});
    const c = await ccardResp.json();
    return new Response(JSON.stringify(c), {status:200, headers});
  }
  // default: full deck
  if (!deckResp || !deckResp.ok) return new Response(JSON.stringify({error:'deck not found'}), {status:404, headers});
  const d = await deckResp.json();
  return new Response(JSON.stringify(d), {status:200, headers});
}
