# 🏛 CSOAI Backend — consolidation master (2026-06-25) · EAT all, no drift

## 1. The fleet — RECONCILED (kills the drift)
`~/clawd/mcp-marketplace`: **347** `*-mcp` dirs · **347 have pyproject** (publishable) · **335 have server.json** (registry-ready).
- ⚠️ Drift killed: old notes said "233 / 294 / 300." Reality: **347 built-publishable, 335 registry-ready.** Gap = **built ≫ published.**
- Canonical: "347 governance/compliance MCPs built (335 registry-ready); **live-PyPI count = VERIFY** before any deck — distribution is the lever, not build."

## 2. COBOL Bridge — the enterprise wedge (lead product)
- **cobol-bridge-mcp** — "COBOL Bridge (Legacy Modernization) MCP", `io.github.CSOAI-ORG/cobol-bridge-mcp`, **scorecard 86/100**, PyPI `cobol_bridge_mcp`, full prod kit (server.py/json, cosign-sign, codeql, tests, smithery).
- Product surface: `cobolbridge/`, `-deploy`, `-site`, landing, **sales plan**, press release, brand guidelines, Terranova/CSGA deck.
- Why: banks/insurers/gov run COBOL → a *governed* legacy→AI bridge = enterprise wedge nobody sovereign-grade offers. Pair with DORA/NIS2 + audit/attestation MCPs.

## 3. Governance core (the CSOAI moat)
eu-ai-act · gdpr · csoai-governance-crosswalk · bft-governance · agent-audit-logger · ai-self-audit · firmware-attestation · a2a-governance-bridge · dora · dora-nis2-crosswalk · cra · csrd · healthcare-ai · hipaa · cqc · insurance-verification · construction-iso-19650 · haulage-uk · drone-airspace.
→ The backend the OS/SOV3 calls; every governed action (incl. the OS self-modifications, Ed25519-signed) routes here.

## 4. Align (to everything built this session)
OS dock → meok-one bridge + SOV3 /chat → governance MCPs · self-improve loop signs onto a ledger (same moat the fleet sells) · CSOAI Map+Dome gap = embed god-eye + meok-town-view · Revenue = A2A £499/mo + compliance packs + COBOL Bridge enterprise SKU.

## 5. Execute (honest next)
1. Verify live PyPI count → publish the registry-ready long tail (335 ready).
2. COBOL Bridge to market (86/100 + sales plan + site) — lead enterprise push.
3. Wire OS "CSOAI-governed posting" → governance MCPs (signed posts).
4. Embed Map+Dome into csoai-org.
5. Owner-gated: publish keys, DNS, twine, outreach.

## 6. 🔴 CRITICAL INFRA (found 2026-06-25)
**Data volume 100% FULL** — 228Gi, 199Gi used, ~347Mi free (after I truncated a 135MB crash-loop log). Ties to the launchd-sprawl/overheat. Big non-essential hogs: /tmp/chrome-profile-copy 924M, /tmp/roboto_origin 568M, /tmp/keystone-venv 141M (verify before clearing). **Free disk + tame the crash-loop before more backend work** — writes are failing (ENOSPC).
