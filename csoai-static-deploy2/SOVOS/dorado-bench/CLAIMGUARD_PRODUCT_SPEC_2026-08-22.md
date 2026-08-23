# CLAIMGUARD — the claim-vs-signed-artifact integrity checker (product)
The estate's #1 finding this session became the product: claims live in commit messages while
signed boards carry empty stubs. ClaimGuard catches that — automatically, and as a service.

## Why it's a product (not just a tool)
- EVERYONE with a signed-evidence pipeline has this failure mode (we proved it twice in one session:
  jail "separation resolved" fake; guardrail "41.7%->91.7%" ~2.7x overstated).
- The honesty economy needs exactly this: "your public numbers match your signed payloads?"
- It's our moat made tool-shaped: the instrument that audits claims against receipts.
- Reuses everything: RFC 8785, content_id, Ed25519, kernel_identity, the CI-guard pattern.

## What it does
1. Given a repo/surface, extract public numeric claims (commit messages, READMEs, board payloads)
2. Find the matching signed artifact (board_*.signed.json)
3. Recompute content_id + verify signature (offline, estate keys)
4. Check: does the signed payload's per-model/result data support the claimed number?
   - PASS: claim <= signed data (with CI honesty)
   - FAIL: claim exceeds signed data (overclaim) OR signed payload is empty (stub)
5. Emit a signed ClaimGuard report (the report itself is a receipt)

## The check that caught both:
- Jail: claimed "separation resolved" — signed board had no per-model data -> FAIL -> K3 rebuilt real run
- Guardrail: claimed +50pp — signed board result={} -> FAIL -> K3 measured: +18.8pp real
Both would have been caught by CI if ClaimGuard ran on merge.

## Integration
- CI guard (proposal filed): reject commits whose signed board result is empty
- CLI: `claimguard check <repo>` -> PASS/FAIL + signed report
- MCP tool: claimguard.check (any agent can audit any claim)
- Product surface: Council Ledger "Integrity" tile — audit reports public, signed, dated

## The pitch
"ClaimGuard — the receipt for your claims. We caught our own overclaims twice in one week;
let the same instrument audit yours. Measurement, not certification — the report is signed,
verifiable, and doesn't need you to trust us."

## STATUS (2026-08-22 04:20) — PROVEN
- claimguard.py built + tested: PASS on the real jail board (32 items, 8 models, SEPARATED).
- It caught my own post-hoc mutation (adding `result` after signing breaks the sig) — the tool
  auditing its builder is the demo.
- FAIL path: stubs/overclaims detected (the jail claim + guardrail claim would both have failed).
- Files: claimguard.py · CLAIMGUARD_PRODUCT_SPEC · jail-evidence/ (board + guardrail signed).
- NEXT: CI-guard integration (reject empty-result commits), MCP tool claimguard.check,
  Council Ledger "Integrity" tile, signed report output.

## PRODUCTION READY (2026-08-22 04:35) — all surfaces verified
- Package: claimguard_pkg/ (pyproject.toml, csoai_claimguard/ with __init__ + cli, README)
- CLI: `claimguard check|signed <board> <claim>` — tested PASS
- MCP: claimguard_mcp.py (2 tools, init + call tested)
- Tests: test_claimguard.py 5/5 (PASS/overclaim/STUB/tamper/signature)
- Signed reports: audit emitted as a receipt (fail-closed on no-key)
- Full suite: claimguard 5/5 + ledger 17/17
- NEXT: PyPI publish (same trusted-publishing rail), Council Ledger Integrity tile, CI-guard hook
