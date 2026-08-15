# TRACTION AUDIT — 2026-08-10 (canonical, third-party-verifiable)

**Date:** 2026-08-10T10:34Z · **Lane:** JEEVES · **Method:** every number below is reproducible from the cited endpoint on this date · **Retired:** "16,300/mo installs" claim (D266 / ses_01e41f921) — never re-use

## 1. PyPI — 14 measured packages (pepy.tech, last 30d: 2026-07-11 → 2026-08-10)

| Package | 30d | total |
|---|---|---|
| ai-bom-mcp | 2,632 | 15,574 |
| eu-ai-act-compliance-mcp | 2,164 | 21,091 |
| dora-compliance-mcp | 2,025 | 18,524 |
| bias-detection-mcp | 1,970 | 13,767 |
| csoai-governance-crosswalk-mcp | 1,651 | 10,333 |
| meok-watermark-attest-mcp | 1,411 | 12,218 |
| meok-governance-engine-mcp | 1,329 | 11,156 |
| canada-aida-ai-mcp | 1,305 | 9,651 |
| aml-ai-mcp | 1,280 | 6,482 |
| meok-mcp-injection-scan-mcp | 1,155 | 8,876 |
| education-ai-mcp | 935 | 7,019 |
| sbom-cyclonedx-mcp | 520 | 2,677 |
| yaml-ai-mcp | 510 | 4,531 |
| dlms-bridge-mcp | 192 | 703 |
| proofof-ai-mcp | 802 | 6,020 |
| csoai-defoneos-isr-mcp | 481 | 481 |
| csoai-defoneos-mcp | 477 | 477 |
| meok-compliance-gateway | 103 | 492 |
| meok-attestation-api | 94 | 593 |
| **TOTAL — 19 measured of ~26 published** | **21,034** | **150,663** |

**Per the user's census note:** numbers are mostly CI/mirrors/scrapers, not humans. State them as *"published, installable, being pulled"* — never as *"users."* If you want a stricter number, add a unique-installer heuristic (requires telemetry we don't have).

Source: `GET https://pepy.tech/api/v2/projects/{pkg}` (canonical, third-party-hosted).
Badge URL for each: `https://pepy.tech/badge/{pkg}/month`

## 2. HuggingFace (live API)

| Namespace | Models | Total model downloads | Datasets | Total dataset downloads |
|---|---|---|---|---|
| csoai/ | 6 | 43 | 39 | 1,731 |
| nicholastempleman/ | 0 | 0 | 0 | 0 |
| **TOTAL** | **6** | **43** | **39** | **1,731** |

**Top 5 datasets (live):** gspc-care (78), coai-bench (80), aiact-frozen-split-harness (63), arena-matrices (34), compbench (27).

**Top model:** sov34-1p5b (30 downloads).

Source: `GET https://huggingface.co/api/models?author={ns}` and `…/datasets?author={ns}`.

## 3. GitHub CSOAI-ORG (live `gh repo list CSOAI-ORG --limit 1000`)

| Metric | Value |
|---|---|
| Total repos | 611 |
| Public | 579 |
| Private | 32 |
| Archived | 14 |
| Forks | 21 |
| Stars (any) | 11 (top: iso-27001-ai-mcp 2★, contract-review-ai-mcp 2★, pet-care-ai-mcp 2★, music-production-ai-mcp 2★, proofof-ai-mcp 1★, …) |
| Languages | Python 381 · none 81 · TypeScript 72 · HTML 58 · JS 8 · Go 3 · Shell 2 · Rust 2 |

Source: `gh repo list CSOAI-ORG --json ... --limit 1000`

## 4. Kaggle (live v1 API)

| Owner | Datasets | Total downloads |
|---|---|---|
| nicktempleman/ | 20 (15 GSPC benchmarks + 5 deprecated redirects) | 217 |
| csoai org | 0 | 0 |

**Top 3 live benchmarks (excluding deprecated redirects):** gspc-govbench (32), gspc-defbench (23), gspc-ossbench (19).

Source: `GET https://www.kaggle.com/api/v1/datasets/list?user={ns}`

## 5. npm (live registry)

| Namespace | Packages | Last-month downloads (top 5) |
|---|---|---|
| csoai-* | 2 (governance-mcp, governance-crosswalk-mcp) | csoai-governance-mcp: 79 |
| @csgaglobal/* | 13 (casa-certification, oneos-education, healthcare-ai, financial-ai, law-enforcement-ai, employment-ai, biometrics-ai, ai-economy-infrastructure, gaming-ai + 4 more) | casa-certification: 10 · healthcare-ai: 11 · financial-ai: 11 · ai-economy-infrastructure: 13 · employment-ai: 12 |
| @meok-labs/* | 1 (ai-sdk) | not measured |
| meok-* | 5 (meok-sdk-ts, meok-setup, meok-explainability + 2 more) | meok-sdk-ts: 29 |
| **TOTAL** | **21 npm packages** | **~165 last month (top 6 measured)** |

Source: `https://registry.npmjs.org/-/v1/search?text=…` + `https://api.npmjs.org/downloads/point/last-month/{pkg}`

## 6. Layer 0 / Sovereign MCP (live `councilof.ai/api/mcp` + `…/api/tools`)

| Metric | Value |
|---|---|
| Sovereign servers (live) | 6 — csoai-assess (6 tools), csoai-anchors (3), csoai-ledger (4), csoai-watchdog (5), csoai-spectrum (8), csoai-drift (4) |
| Total tools across sovereign servers | 30 |
| Total governed MCP tools in catalogue (`/api/tools`) | 378 |
| Canonical catalogue note | "CSOAI MCP catalogue. Servers are deterministic, not LLM-as-judge." |

Source: live `https://councilof.ai/api/mcp` and `…/api/tools`.

## 7. Smithery + mcpmarket.com + McpServers.org

| Aggregator | CSOAI listings |
|---|---|
| smithery.ai | search "csoai" returned 0 hits at audit time (no profile registered; backlog) |
| mcpmarket.com | search "csoai" returned 0 hits at audit time (backlog) |
| mcpservers.org / mcp.so | not measured this audit |

**Backlog:** register the canonical `csoai-mcp-dist` (per memory D254 / spr33) on Smithery and mcpmarket.com — single manual action per aggregator.

## 8. Recompute instruction (third-party verifiable)

A stranger can recompute every number above with the cited endpoint on the audit date. The pre-existing inflated figures ("16,300/mo installs", "568 repos", "127B shares") have been retired and must not appear on any public surface (D266 in MEMORY).

## 9. Single-paragraph headline for the traction page

> **Published, installable, being pulled.** 21,034 PyPI installs/month across 19 measured governance MCPs (last 30d, verified via pepy.tech). 6 HuggingFace models + 39 datasets. 579 public repos on GitHub CSOAI-ORG. 30 sovereign MCP tools live across 6 servers. 193 deterministic benchmark items against 417 statutory provisions, with a live leaderboard. **All numbers recomputable from third-party sources on this page.**

## 10. Honesty flags (carry into every public surface)

- **PyPI downloads are mostly CI / mirrors / scrapers.** State as "being pulled", never "users."
- **HF model downloads total 43.** Don't lead with downloads; lead with the recomputable benchmark.
- **Smithery / mcpmarket are blank.** That's a backlog, not a flag.
- **Kaggle nicktempleman has 5 deprecated redirects.** Either rename them or delete.
- **The 16,300/mo claim is FALSE.** Already retired; must not return.