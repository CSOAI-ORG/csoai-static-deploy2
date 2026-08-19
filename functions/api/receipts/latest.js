// /api/receipts/latest — the flagship claim made machine-demonstrable:
// returns one full signed artifact (latest signed measurement board) that any
// stranger can verify against did:web:csoai.org with three offline steps.
const REPO_RAW = 'https://raw.githubusercontent.com/CSOAI-ORG/csoai-static-deploy2/main/SOVOS/boards-signed/';

export async function onRequestGet() {
  try {
    const listRes = await fetch(
      'https://api.github.com/repos/CSOAI-ORG/csoai-static-deploy2/contents/SOVOS/boards-signed',
      { headers: { 'Accept': 'application/vnd.github+json', 'User-Agent': 'csoai-receipts-endpoint' } });
    if (!listRes.ok) throw new Error('gh ' + listRes.status);
    const files = (await listRes.json())
      .filter(f => f.name.endsWith('.signed.json'))
      .sort((a, b) => b.name.localeCompare(a.name));
    if (!files.length) throw new Error('no signed boards');
    const latest = files.find(f => f.name.includes('fleetv2')) || files[0];
    const doc = JSON.parse(await (await fetch(latest.download_url)).text());
    return new Response(JSON.stringify({
      kind: 'csoai-receipt-envelope-v1',
      receipt: doc,
      source: REPO_RAW + latest.name,
      how_to_verify_offline: [
        'curl https://csoai.org/.well-known/did.json  -> take publicKeyJwk.x of the kid named in receipt.signatures[0].protected (base64url)',
        'recompute: sha256(json.dumps(receipt minus signatures, sort_keys, compact, utf-8)) -> hex -> ascii bytes',
        'ed25519_verify(pubkey, content_id_bytes, base64url_decode(receipt.signatures[0].signature))',
      ],
      verify_in_browser: 'https://councilof.ai/verify',
      verify_via_mcp: 'https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp (tool: verify)',
    }, null, 2), { headers: { 'content-type': 'application/json', 'cache-control': 'public, max-age=300' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: 'receipt fetch failed', detail: String(e) }),
      { status: 502, headers: { 'content-type': 'application/json' } });
  }
}
