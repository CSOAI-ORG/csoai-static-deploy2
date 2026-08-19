// /api/receipts/latest — the flagship claim made machine-demonstrable:
// one full signed artifact a stranger can verify against did:web:csoai.org offline.
const REPO_RAW = 'https://raw.githubusercontent.com/CSOAI-ORG/csoai-static-deploy2/main/SOVOS/boards-signed/';
const PINNED = 'board_swarm-candidates-v2b.signed.json'; // pinned 2026-08-19; LATEST.json supersedes when present

export async function onRequestGet() {
  let doc = null, srcName = PINNED;
  try {
    const ptrRes = await fetch(REPO_RAW + 'LATEST.json', { cf: { cacheTtl: 120 } });
    if (ptrRes.ok) {
      const ptr = JSON.parse(await ptrRes.text());
      if (ptr.file) srcName = ptr.file;
    }
  } catch (_) { /* pinned fallback */ }
  try {
    const r = await fetch(REPO_RAW + srcName, { cf: { cacheTtl: 120 } });
    if (!r.ok) throw new Error('raw ' + r.status);
    doc = JSON.parse(await r.text());
  } catch (e) {
    return new Response(JSON.stringify({ error: 'receipt fetch failed', detail: String(e) }),
      { status: 502, headers: { 'content-type': 'application/json' } });
  }
  return new Response(JSON.stringify({
    kind: 'csoai-receipt-envelope-v1',
    receipt: doc,
    source: REPO_RAW + srcName,
    how_to_verify_offline: [
      'curl https://csoai.org/.well-known/did.json -> take publicKeyJwk.x of the kid named in receipt.signatures[0].protected (base64url)',
      'recompute: sha256(json of receipt minus signatures, sort_keys, compact separators, utf-8) -> lowercase hex -> ascii bytes',
      'ed25519_verify(pubkey_bytes, content_id_bytes, base64url_decode(receipt.signatures[0].signature))',
    ],
    verify_in_browser: 'https://councilof.ai/verify',
    verify_via_mcp: 'https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp (tool: verify)',
  }, null, 2), { headers: { 'content-type': 'application/json', 'cache-control': 'public, max-age=120' } });
}
