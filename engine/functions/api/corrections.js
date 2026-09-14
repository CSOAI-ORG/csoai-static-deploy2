// Cloudflare Pages Function — /api/corrections (CORR-010 added 2026-08-20)
const CORRECTIONS = {
  "schema": "csoai.corrections/0.1",
  "updated": "2026-08-20T04:20:00Z",
  "total": 10,
  "policy": "corrections appended, never edited. The body that publishes the number publishes when the number was wrong.",
  "corrections": [
    {
      "id": "CORR-001",
      "subject": "",
      "what_was_wrong": "An internal signed artifact carried '16 axes'; the live API served totals.axes=17 and items=966 while canon is 14-slot / 13 measured / 819 items.",
      "how_caught": "End-user probe of councilof.ai/api/gspc against the canon register (GR.2 reconciliation); cross-checked badge (13 of 14) vs API totals.",
      "fix": "Public copy holds 13-of-14 everywhere; the 16-axis artifact is internal-only and never publishes; the councilof-ai lane reconciled the API to axes=14 / measured=13 / DOI 21991104.",
      "status": "resolved"
    },
    {
      "id": "CORR-002",
      "subject": "",
      "what_was_wrong": "The published agent-card.json carried kid did:web:csoai.org#site-release-1 which is absent from the DID document; the card did not verify against either published key (corrections #27 / HN.0).",
      "how_caught": "Offline verification of the served card against the DID doc keys (recomputed id + Ed25519 check).",
      "fix": "Byte-identical restore of the machine surface while the signing-chain fix is owned by the kernel/identity lane (Rekor v2 + RFC 3161 TSA). No new A2A publicity until it verifies.",
      "status": "open"
    },
    {
      "id": "CORR-003",
      "subject": "",
      "what_was_wrong": "A full _site build deployed to the shared csoai-site project replaced its content, dropping K3's untracked machine-surface files (agent-card.json, banks-manifest.json, verification.schema.json, CANONICAL-DOIS.md, badge/axes.json).",
      "how_caught": "Post-deploy machine-path probe: 5 of 12 paths 404'd on the new hash (csoai.org still showed 200 via edge cache \u2014 the cache masked it).",
      "fix": "Restored the authoritative files from the prior deployment, added a never-drop allowlist rule to build_site.py, redeployed; all machine paths verified 200 cache-busted.",
      "status": "resolved"
    },
    {
      "id": "CORR-004",
      "subject": "",
      "what_was_wrong": "The documented arena feed path councilof.ai/api/sov-arena/rounds.jsonl returned 404 while the live data served at /sov-arena/rounds.jsonl.",
      "how_caught": "End-user probe of both paths against the harness map's documented surface.",
      "fix": "Flagged to the K3 lane; the live feed serves at the working path and the KV-backed feed continues.",
      "status": "open"
    },
    {
      "id": "CORR-005",
      "subject": "",
      "what_was_wrong": "An internal codename appeared with a CamelCase variant on public surfaces, violating the case-locked kill-list (ceasai vs CEASAI).",
      "how_caught": "Case-sensitive sweep of public HTML for kill-list tokens (the sweep that also caught the BFT pages).",
      "fix": "Purged the variant from public copy; the kill-list sweep is now part of the acceptance battery.",
      "status": "resolved"
    },
    {
      "id": "CORR-006",
      "subject": "",
      "what_was_wrong": "Public surfaces carried SaaS pricing tiers (\u00a3199/mo re-attestation, \u00a3999/\u00a31,999) \u2014 the single most dangerous sentence on the estate: it reads as pay-to-stay-measured.",
      "how_caught": "Canon sweep (HO.2 ruling: all pricing removed; verification free forever).",
      "fix": "All pricing removed; the free-rail posture line replaces it; any future pricing surface requires an owner ruling.",
      "status": "resolved"
    },
    {
      "id": "CORR-007",
      "subject": "",
      "what_was_wrong": "The Annex III high-risk date needed to be 2 Dec 2027 (Digital Omnibus Reg (EU) 2026/1744 deferral), not 2 Aug 2026 \u2014 serving the dead date would be a credibility wound.",
      "how_caught": "Reg-calendar research + date sweep of shipped pages for wrong pairings of '2 Aug 2026' with Annex III.",
      "fix": "Verified no wrong pairing shipped (the 2 Aug 2026 refs are Article 50, correct); the reg-feed treats dates as corrected data, not static copy.",
      "status": "resolved"
    },
    {
      "id": "CORR-008",
      "subject": "",
      "what_was_wrong": "tools/bft-council.html ('CSOAI Designed 33-Agent Council \u2014 Sovereign Governance') and tools/bft-vote-log.html shipped to production and sat in the sitemap \u2014 BFT/33/Sovereign are kill-listed.",
      "how_caught": "Kill-list sweep of shipped _site (the ramp's 'last 33-Agent string' valuation-hygiene item).",
      "fix": "NEVER_HTML exclusion (DIRS loop), _redirects 308 \u2192 honest desks, sitemap cleanup. Verified: routes 308, zero bft in sitemap, machine paths + hero intact.",
      "status": "resolved"
    },
    {
      "id": "CORR-009",
      "subject": "",
      "what_was_wrong": "CARE 0.895/F1 0.8976 was claimed as 'key verified' but it is an in-lane harness figure (tuned specialist on an internal bank); the public board number is care leader 0.535 (n=199).",
      "how_caught": "Probe of the live signed board against the claimed figure (deterministic grader, 15,580 rows).",
      "fix": "Rule: never cite 0.895/0.8976 as the CARE board figure; public = 0.535 (n=199). Internal harness numbers stay internal-only.",
      "status": "resolved"
    },
    {
      "id": "CORR-010",
      "subject": "Reg feed signature was stale (underwriting substrate must verify)",
      "what_was_wrong": "/api/regulation's signature block (sigil scheme) no longer verified \u2014 the feed had been edited after signing / signed with a non-estate key; contentId mismatch.",
      "how_caught": "Verification pass on the live feed (2026-08-20): recomputed canonical vs stored id/signer.",
      "fix": "Re-signed with did:web:csoai.org#site-release-1 (card scheme); corrected payload staged for the councilof-ai repo (site lane handoff).",
      "status": "corrected"
    }
  ],
  "signature": {
    "protected": "eyJhbGciOiJFZERTQSIsImtpZCI6ImRpZDp3ZWI6Y3NvYWkub3JnI3NpdGUtcmVsZWFzZS0xIiwidHlwIjoiSldUIn0",
    "contentId": "10bdfac58a255187ef5c8a09ec43292d410fbfd01a2e46fc42f02544831f112f",
    "signature": "oDgIZcUyUTOImk7xBD3lpZpInhgoAQxNs_o9ARKlymbL87yyQ7fvtJd9U5BdA1cwW5jtVNahdOebjdPxyzltBg"
  }
};

export async function onRequest(context) {
  return new Response(JSON.stringify(CORRECTIONS, null, 2), {
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "public, max-age=300, must-revalidate" },
  });
}
