# ESTATE INVENTORY — EVERYTHING WE HAVE (2026-08-15)

## THE 15 AXES (the measurement fabric)

14 measured + 1: **gov, prv, agi, asi, mcp, oss, mach, care, xr, det, art5,
swarm, affect, jail** (14 measured, all with n≥30) + **human-vs-AI** (the 15th
dimension — the Escape Room / co-development bench, DPIA-gated).

## MEASUREMENT FABRIC (the "what")

| Asset | Count | Detail |
|---|---|---|
| Signed packages | 58 | `SOVOS/packages/` — csoai-core, oscal, arena, league, chain, fisher-rao, gprobe, etc. |
| Migrated csoai-* | 55/55 | `councilof-ai-monorepo` live on GitHub |
| Release proofs | 16 | 15 signed cards + index, Ed25519, in-browser verify |
| Board cards | 14 | all MEASURED, usable_n≥30, Wilson CIs |
| Honey strata | 4,896 rows | 2,693 signed (card_type=sovos-honey-stratum-v1, OTS anchor) |
| Agents/scripts | 37 | rotator, scorer-signer, framework-signer, verify, release-gen |
| MCP servers | 8 | incl. ai-bom, governance-crosswalk, eu-ai-act, injection-scanner |
| DOIs | 6 | C1 (zenodo.21914702), WMH, ProvBench + preprints |
| IP inventory | 42 components | 5 CRITICAL provisionals queued (signal-index/arena/chain/sheaf/world-OWEM) |

## OPERATIONS FABRIC (the "how")

| Surface | Detail |
|---|---|
| GSPC MCP worker | measure / verify / jail-probe tools, live on Cloudflare |
| Verify | `csoai_verify.py` stdlib-only, tamper-proven; in-browser on releases page |
| Sites | csoai.org + councilof.ai (582 pages), releases page, blog, escape-room |
| Workers | csoai-gspc-mcp + attest-verify |
| CI | G4 claim-linter + firewall-lint (Firewall 2) + schema gates |

## COMPUTE FABRIC (the "where")

| Tier | Resource | Cost | Role |
|---|---|---|---|
| Frontier | A100 80GB (RunPod) | $1.19/h | board runs, heavy probes |
| Mid | RTX 3090 (RunPod) | $0.22/h | 24x7 arena loop |
| Burst | K3 serverless (2TB vol) | pay-per-inference | FlashBoot mid-size probes |
| Free | 2× Oracle E2.Micro | £0 | city report, verify health, fabric |
| Free | A1.Flex (hunting) | £0 (2 OCPU/12GB) | model rotator (~5-6 models/hr) |
| Free | RunPod budget | $82 remaining | primary paid compute |

## DISTRIBUTION FABRIC (the "reach")

| Channel | Status |
|---|---|
| GitHub CSOAI-ORG | LIVE (monorepo + 15 repos) |
| PyPI `csoai` 0.2.0 | LIVE |
| npm `@meok-labs/csoai` | LIVE |
| Kaggle `csoai-signed-measurement-cards` | LIVE (pending public visibility) |
| Hugging Face | bundle ready (token refresh needed) |
| Zenodo | C1 DOI live; batch DOI pending deposit |
| MCP registry | `io.github.CSOAI-ORG/gspc` live |

## AUTHORITY FABRIC (the "trust")

| Asset | Status |
|---|---|
| C2PA Contributor Member | SIGNED (LF, docusign 7C9592DB) — Adobe/MS/BBC/Sony/Google co-members |
| OIN 2.0 + LOT Network | SIGNED (defensive patents) |
| BSI ART/1 seat | pending (owner action, £0, ISO/IEC SC 42 room) |
| AI TAP (Singapore) | EOI drafted |
| IETF agentproto | -00 draft written (BoF 17 Aug) |
| DEFONEOS compartments | meok-defoneos / csoai-defoneos / dagon (never mixed) |

## INSTRUMENTS (the "how we monetize without selling neutrality")

| Instrument | Status |
|---|---|
| Reliance tooling (BitSight×CFC) | spec'd — insurers get feed access |
| Regulator mapping packs | spec'd — legal teams push the format |
| Co-development bench | spec'd — partner corpus → joint DOI |
| Give-to-get benchmark barter | spec'd |
| Collison attestation | spec'd (live demo in room) |
| Compute credits | tracker live (~$18-20k £0 this month) |
| Press pack | 15 signed releases + journalist targets |
| Design-partner bootstrap | releases page + verify + offer |

## FIREWALL (the moat — never cross)

1. Measure, never certify/endorse
2. Analyse outcomes, never train a shipped champion model
3. No PII leakage; licence hygiene (MIT/Apache only in shippable paths)
4. No rating-for-listing reciprocity, no referral fees tied to ratings
5. DEFONEOS hard stops (kinetic, surveillance, DSEI, defonos.io trap)

---

*Canonical inventory. Updated 2026-08-15. Used as the estate baseline for the
playbook synthesis.*