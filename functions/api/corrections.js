// Cloudflare Pages Function — /api/corrections
// The corrections ledger as a machine-readable feed.
// Canon: "corrections appended, never edited". The body that publishes the
// number also publishes when the number was wrong — the honesty gate as
// citation surface. Seeded 2026-08-19 with nine self-caught corrections.
// Signed per estate scheme: content_id = sha256(canonical body w/o signature),
// signature = Ed25519(content_id) with kid did:web:csoai.org#site-release-1.
const CORRECTIONS = const CORRECTIONS = {
  "schema": "csoai.corrections/0.1",
  "updated": "2026-08-20T04:30:00Z",
  "total": 9,
  "policy": "corrections appended, never edited. Every entry: what was wrong, how it was caught, the fix, status.",
  "corrections": [
    {
      "id": "count-drift-2026-08-19",
      "subject": "Public measured count drifted across surfaces",
      "what_was_wrong": "The quotable count appeared as 16 axes in one API surface while the board/public grammar said 13 measured of 14; provision counts also drifted (404 vs 417).",
      "how_caught": "Cross-surface audit (API vs board vs llms.txt) on 2026-08-19; API_16AXES correction brief.",
      "fix": "Locked grammar '13 measured of 14' everywhere; 417 frozen provisions; API corrected to the same totals.",
      "status": "corrected",
      "affects": [
        "https://councilof.ai/api/gspc",
        "https://csoai.org/llms.txt"
      ],
      "corrected_at": "2026-08-19T12:00:00Z"
    },
    {
      "id": "envelope-divergence-2026-08-19",
      "subject": "inspect-receipts claimed to wrap proofbundle; it is an independent implementation",
      "what_was_wrong": "Our comment on UKGovernmentBEIS/inspect_ai#4413 said the package wraps proofbundle's ProofbundleHooks; the maintainer measured commit ca3fd060 and found no proofbundle references.",
      "how_caught": "External code review by the proofbundle maintainer (b7n0de/proofbundle#147), 2026-08-19.",
      "fix": "Corrected the claim publicly (#4413 comment 5350249856); docs aligned; v0.2.0 adds RFC 8785 canonicalisation, mandatory kid resolution, binding declaration.",
      "status": "corrected",
      "affects": [
        "https://github.com/b7n0de/proofbundle/issues/147"
      ],
      "corrected_at": "2026-08-19T18:00:00Z"
    },
    {
      "id": "two-deployer-clobber-2026-08-19",
      "subject": "Signing fail-closed oscillated (dual daemon instances)",
      "what_was_wrong": "Two ops_daemons instances ran the did-liveness check \u2014 an old lenient one (either-host) and a new strict one \u2014 so .sign-blocked was written and un-written every hour while csoai.org served orphan did keys.",
      "how_caught": "Live probe found .sign-blocked absent despite the orphan did.json; log showed both message formats at the same timestamp.",
      "fix": "Killed all instances, restarted one strict instance; fail-closed now stable until csoai.org converges.",
      "status": "corrected",
      "affects": [
        "https://csoai.org/.well-known/did.json"
      ],
      "corrected_at": "2026-08-20T01:52:00Z"
    },
    {
      "id": "ghost-api-endpoints-2026-08-19",
      "subject": "False 'dead endpoint' verdicts (wrong API paths / SPA fallbacks)",
      "what_was_wrong": "A 1-by-1 sweep reported the official MCP registry had ZERO CSOAI entries (via the dead path /v0.1/v1/servers) and that mcp.json/badge/agent-card were 404; in fact the entries existed and the machine files returned real content.",
      "how_caught": "Re-verification with the correct API paths (/v0.1/servers) and content-type checks for SPA soft-404s.",
      "fix": "Corrected verdicts (registry presence confirmed, ~310 servers); corrected paths + content-sniffing discipline documented.",
      "status": "corrected",
      "affects": [
        "https://registry.modelcontextprotocol.io/v0.1/servers"
      ],
      "corrected_at": "2026-08-19T14:00:00Z"
    },
    {
      "id": "ceasai-camelcase-2026-08-19",
      "subject": "CamelCase naming inconsistency on a public artifact",
      "what_was_wrong": "A public artifact used 'CEASAI' (CamelCase) where the canonical mark is CSOAI; casing drift across surfaces risks confusing resolvers and dilutes the identifier.",
      "how_caught": "Surface naming sweep during the estate audit (2026-08-19).",
      "fix": "Canonical CSOAI locked across the affected surface.",
      "status": "corrected",
      "affects": [
        "public naming surfaces"
      ],
      "corrected_at": "2026-08-19T15:00:00Z"
    },
    {
      "id": "pricing-leak-2026-08-19",
      "subject": "Pricing surface appeared against the no-pricing doctrine",
      "what_was_wrong": "A pricing.html surface was built/visible; the estate doctrine is 'no pricing anywhere' (a neutral measurement body never prices what it measures).",
      "how_caught": "Doctrine sweep (HO.2) during the estate audit.",
      "fix": "Pricing surface removed/hidden; doctrine locked in the publish guard.",
      "status": "corrected",
      "affects": [
        "public web surfaces"
      ],
      "corrected_at": "2026-08-19T15:00:00Z"
    },
    {
      "id": "omnibus-date-2026-08-19",
      "subject": "EU AI Act applicability date corrected (Digital Omnibus)",
      "what_was_wrong": "A surface carried the pre-Omnibus applicability date; the Digital Omnibus shifted applicability.",
      "how_caught": "Web-verified against the Digital Omnibus (2026-08-19).",
      "fix": "Stamped EU AI Act applicability 2027-12-02 (Digital Omnibus) on the affected surface.",
      "status": "corrected",
      "affects": [
        "EU AI Act reference surfaces"
      ],
      "corrected_at": "2026-08-19T16:00:00Z"
    },
    {
      "id": "provision-count-2026-08-19",
      "subject": "Frozen provisions count corrected: 404 -> 417",
      "what_was_wrong": "The frozen-corpus provision count was published as 404; the canon is 417 provisions.",
      "how_caught": "Canon audit (PROVISION_COUNT_FIX).",
      "fix": "417 locked as the canonical count across canon + surfaces.",
      "status": "corrected",
      "affects": [
        "https://csoai.org/llms.txt",
        "https://councilof.ai/api/gspc"
      ],
      "corrected_at": "2026-08-19T12:00:00Z"
    },
    {
      "id": "registry-version-rows-2026-08-19",
      "subject": "'30 version-rows in the registry' claim was PyPI-version confusion",
      "what_was_wrong": "A status sheet claimed 30 version-rows in the official MCP registry for CSOAI; the search actually returned unrelated rows (ac.inference.sh) and the count conflated PyPI versions with registry entries.",
      "how_caught": "1-by-1 registry verification via the correct /v0.1/servers path.",
      "fix": "Claim corrected; real presence verified and published (~310 servers, 2026-08-20).",
      "status": "corrected",
      "affects": [
        "https://registry.modelcontextprotocol.io"
      ],
      "corrected_at": "2026-08-19T14:30:00Z"
    }
  ],
  "signature": {
    "protected": "eyJhbGciOiJFZERTQSIsImtpZCI6ImRpZDp3ZWI6Y3NvYWkub3JnI3NpdGUtcmVsZWFzZS0xIiwidHlwIjoiSldUIn0",
    "contentId": "ab43bb14ea5c96362e4ceabb49aa3df331327f62092937728e79940dd7a00984",
    "signature": "rs8fGmU_nd8NvP1A82975Yt6N42WvBe0oBTl9VTt9w8oVweIeKEWVJPUPwkbWTSONIc1V5mfT433rUzwFb_BBw"
  }
};

export async function onRequest(context) {
  const body = JSON.stringify(CORRECTIONS, null, 2);
  return new Response(body, {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "public, max-age=300, must-revalidate",
    },
  });
}
