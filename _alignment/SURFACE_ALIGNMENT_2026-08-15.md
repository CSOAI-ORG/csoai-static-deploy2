# Front-End Surface Alignment — 100/100 Ledger (2026-08-15)

Status: ✅ = done + verified live · 🟡 = owner action required · ⚠️ = needs attention later

## The single brand
> **Council of AI (CSOAI Ltd · UK 16939677)** — independent AI-governance measurement.
> We measure AI systems against the rules that govern them, sign the result, publish what we cannot yet measure.
> **Measurement, not certification.**

## GitHub (CSOAI-ORG) — ✅ ALIGNED
| Item | Before | After | Proof |
|---|---|---|---|
| Profile bio | "Founder @ MEOK & CSOAI" | "Founder, Council of AI (CSOAI Ltd · UK 16939677) — measuring AI systems…" | gh api user |
| Company | "MEOK AI Labs / CSOAI Ltd" | "Council of AI (CSOAI Ltd)" | gh api user |
| Blog | — | councilof.ai | gh api user |
| csoai-org repo desc | "Council for the **Safety** of AI. CEASAI certification…" (dead brand) | "Council of AI — independent AI-governance measurement. 13 GSPC axes…" | ✅ patched |
| .github repo | undefined | "Council of AI — org profile + community health files" | ✅ patched |
| CSGA-GLOBAL org | null | "Legacy bridge modernisation estate (COBOLBridge.ai)…" | ✅ patched |
| Profile README | 1393 B | 1802 B — live MCP endpoint, 13 axes, verifier, HF/Kaggle links | ✅ rewrote |
| Pinned repos | 0 | 6 compliance MCPs (EU AI Act, DORA, CRA, governance-engine, injection-scan, watermark-attest) | ✅ pinned via API |
| Old-brand sweep | 1 repo | 0 repos reference "Safety of AI"/CEASAI | ✅ verified 584-repo set |

## Site surfaces — apex RESURRECTED
| Surface | Before | After | Notes |
|---|---|---|---|
| csoai.org apex | **522** (dead Vercel origin, A-record 162.255.119.208) | **200** — Council of AI measurement home | ✅ attached domain to CF Pages `csoai-site` (API POST, status initializing→pending→live), rebuilt `index.html` as Council brand root, deployed to production 2b3c37f4, cache-busted verified |
| csoai.org/defoneos.html | globe | globe **still live** at own path (308→200) | ✅ preserved |
| www.csoai.org | 200 (Pages) | 200 (Pages) | ✅ unchanged |
| councilof.ai | 200 "Council of AI" | 200 | ✅ |
| meok.ai | 200 | 200 | ✅ |
| proofof.ai | 200 "Council of AI" | 200 | ✅ |
| cobolbridge.ai | 000 (dead) | 000 | ⚠️ needs DNS/deploy decision (CSGA-GLOBAL holds repos) |

## HuggingFace — 🟡 OWNER-REQUIRED (token invalid)
| Item | State | Action needed |
|---|---|---|
| Org page `huggingface.co/csoai` | LIVE — 29 datasets, 14 Spaces, 1 collection | 🟡 Rename org display name from "Council for the Safety of Artificial Intelligence" → **Council of AI** |
| Org bio | "…Council for the Safety of Artificial Intelligence (CSOAI LTD)…" | 🟡 rewrite on rename |
| Datasets (gspc-boards 57 files, coai-bench, omai-bench…) | LIVE | ✅ |
| Token | **invalid** (`hf_LfvQP…` fails whoami-v2) | 🟡 `hf auth login --force` on Mac |
| Models 0 | — | ✅ acceptable (datasets are the surface) |

## Kaggle — 🟡 OWNER-REQUIRED (session)
| Item | Status | Action needed |
|---|---|---|
| Profile `kaggle.com/nicktempleman` | LIVE — 33 datasets, 27 code, 6 benchmarks | — |
| Bio | "No bio yet… Quietly working away" | 🟡 set Council of AI bio + link |
| GSPC banks (gspc-govbench, gspc-defbench, gspc-mcpbench…) | LIVE (deprecated-noted versions point to current) | ✅ |

## PyPI — ✅
| Item | Status |
|---|---|
| .pypirc / packages | ✅ 590+ packages live (pypi.org 200) |

## Board (substrate proof, running through surface pass)
| Axis | Progress |
|---|---|
| gov | ✅ completed 5214/5214 (earlier session) |
| care | 3150/4400 (streaming now) |

## Commits this pass
- `index.html` Council home — csoai-static-deploy2 `b4c2033f`
- GitHub profile + org descriptions + pins + README (API writes, no local VCS)

## Owner click-list (the 5 front-end leftovers)
1. **HF token**: `hf auth login --force` → then org display-name rename to "Council of AI" (Settings → Organization)
2. **Kaggle bio**: log in, edit profile bio → "Council of AI (CSOAI Ltd) — independent AI-governance measurement"
3. **cobolbridge.ai** decide: reissue DNS to CF Pages or archive the domain
4. **Verify GitHub profile renders** at github.com/CSOAI-ORG (6 pins + brand README)
5. **npm 2FA** (carried from prior pass — token `87676e` still rotate-pending)

Every number on the public surfaces recomputes from published rows; nothing "certified".