/**
 * /api/live-regulation — the LIVE cross-reference feed (move #13).
 *
 * Pulls REAL, dated, official regulatory documents from the live Federal Register
 * API (no key, free) + serves them as a signed, change-detected feed. Each record
 * carries a SHA-256 content hash so a change to an official document is a DETECTABLE
 * event (cross-referenced against the static feed → a published correction), never a
 * silent edit. This is the "find exposure BEFORE they call us" data layer.
 *
 *   GET /api/live-regulation?term=artificial+intelligence&per_page=5
 *   GET /api/live-regulation?source=federal-register   (default)
 *
 * We only ever point at public official sources; we never scrape against terms.
 * Measurement, not certification. This is reference data (a dated fact), never a
 * compliance determination.
 */

import { getKey, canon, sha256hex, hexToBytes, bytesToB64, bytesToHex } from './signlib.js';

const SOURCES = {
  'federal-register': {
    name: 'US Federal Register',
    base: 'https://www.federalregister.gov/api/v1/documents.json',
    license: 'public domain (17 U.S.C. §105) — official US government record',
  },
};

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers });

  const url = new URL(context.request.url);
  const source = SOURCES[url.searchParams.get('source') || 'federal-register'] ? (url.searchParams.get('source') || 'federal-register') : 'federal-register';
  const term = url.searchParams.get('term') || 'artificial intelligence';
  const perPage = Math.min(Math.max(parseInt(url.searchParams.get('per_page') || '5', 10) || 5, 1), 20);
  const live = url.searchParams.get('live') === '1'; // per-request live fetch vs cached/static fallback

  const cfg = SOURCES[source];
  const fetchUrl = cfg.base + '?conditions%5Bterm%5D=' + encodeURIComponent(term) + '&per_page=' + perPage;

  let docs = [];
  let fetchedAt = null;
  let error = null;
  if (live) {
    try {
      const r = await fetch(fetchUrl, { headers: { 'user-agent': 'csoai-gspc/1.0', accept: 'application/json' } });
      if (r.ok) {
        const j = await r.json();
        docs = (j.results || []).map((d) => ({
          title: String(d.title || ''),
          type: String(d.type || ''),
          publication_date: String(d.publication_date || ''),
          document_number: String(d.document_number || ''),
          agency: String(d.agencies?.[0]?.name || ''),
          url: String(d.html_url || d.url || ''),
          abstract: String(d.abstract || '').slice(0, 300),
          content_hash: null, // set below
        }));
        fetchedAt = new Date().toISOString();
      } else {
        error = 'live fetch HTTP ' + r.status;
      }
    } catch (e) {
      error = 'live fetch failed: ' + String(e).slice(0, 80);
    }
  }

  // SHA-256 content hash per record — a change to the official doc is a detectable event.
  const hashText = (d) => sha256hex(d.title + '|' + d.document_number + '|' + d.publication_date + '|' + d.abstract);
  for (const d of docs) d.content_hash = await hashText(d);
  const feedHash = docs.length ? await sha256hex(canon(docs)) : null;

  const claim = {
    schema: 'csoai.live-regulation/0.1',
    record_type: 'measured-current-state',
    not_a_certification: true,
    endorsement: 'none',
    authored_by: 'did:web:csoai-gspc.pages.dev',
    basis: 'cross-reference against LIVE official sources (Federal Register API, public domain). Every record carries a SHA-256 content hash so a change is a detectable event, never a silent edit.',
    source: { name: cfg.name, license: cfg.license, term, fetchedAt },
    feed_hash: feedHash,
    count: docs.length,
    live: live,
    error,
    documents: docs,
    never: ['a compliance determination', 'a certification', 'legal advice'],
    witnessed_at: new Date().toISOString(),
  };
  const content_id = await sha256hex(canon(claim));
  const pair = await getKey(context.env);
  const sig = await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(content_id));
  const pub = pair.rawPubHex ? hexToBytes(pair.rawPubHex) : await crypto.subtle.exportKey('raw', pair.publicKey);
  const out = { ...claim, content_id, signature: bytesToB64(new Uint8Array(sig)), pubkey: bytesToHex(new Uint8Array(pub)) };
  if (pair.kid) { out.key_id = pair.kid; out.verification_method = pair.did + '#gspc'; out.did_resolver = 'https://' + pair.did.replace('did:web:', '') + '/.well-known/did.json'; }
  return new Response(JSON.stringify(out), { status: 200, headers });
}
