# ALL-LANE BUILD REGISTER (2026-08-23) — the master consolidation

Everything built across all lanes, consolidated. Canon = `SOVOS/canon/SOVOS-MASTER-PART-A/B`.
This is the one register of what's BUILT + what's RUNNING + what's RECEIVABLE.

## 1. VERIFICATION / MEASUREMENT BODY (my lane — LIVE)
- **LIVE:** `https://csoai-verify.pages.dev/verify` (Cloudflare, HTTP 200, browser-verifiable WebCrypto).
- **Signed evidence:** 15 Ed25519-signed verdicts + `evidence-index.json` (pubkey
  `bWbk52E47J6EkY4+pu0H…`), all VALID + hash-matched + tamper-sensitive.
- **Portable verifier:** `verify_signature.py` (cryptography lib). **PR:** `SOVOS/evidence/DEPLOY-PR-CLAUDE.md`.
- **Clean measurement (3090, RAG):** mistral:7b 67.3 · llama3:8b 66.6 · qwen2.5:7b 63.3 · 1.5b 60.5.
  Fair-0.5B: base 32.6 > sov33-v7 19.8 > sov33-evolved 11.4.

## 2. GTM PRODUCT LAYER (dorado-bench lane — BUILT)
| Product | What it is | Code |
|---|---|---|
| **Council Ledger** (codename Dorado) | signed provision-conformance receipts + market/human/AI context | `dorado-bench/council_ledger.py` |
| **Dorado Bench** | East↔West live regulation-vs-market pair measurement | `dorado-bench/dorado_bench.py`, `dorado_mcp.py` |
| **Claimguard** | signed claim-evidence guard | `dorado-bench/claimguard.py`, `claimguard_mcp.py`, `claimguard_pkg/` |
| **Art 50 receipt spec** | Article 50 signed conformity receipt (Mosaic × Munich Re aiSure pilot) | `dorado-bench/art50_demo.py` |
| **Insurer pilot v2** | Mosaic × Munich Re; reframed as measurement-not-prediction | `dorado-bench/INSURER_PILOT_v2_2026-08-21.md` |

All registers: MEASURED / REPORTED / UNMEASURED. Never fused regulation+market; measurement, not prediction.

## 3. RUNPOD RUNNING STATE (actual, verified on 3090)
| Process | Purpose |
|---|---|
| `arena_loop_keeper.py` | 16-axis GSPC Elo loop (2,739+ rounds) |
| `arena_pickup.py` | arena round pickup |
| `arena-git-sync.sh` | arena git sync |

## 4. MODELS / BUILD (actual)
- 3090 (`11439`) workhorse: base models (qwen3:8b, llama3:8b, mistral:7b, qwen2.5:7b, 1.5b) + corrupted
  council-oowm rebuilt → **council-oowm-clean** (397 MB).
- Oracle micros (`11436`/`11437`): the 150+ sovereign fleet (sov33-*).
- **sov33-unified** (3.2B llama q4): transfer to 3090 in-flight (~63%) → watcher auto-fires
  create→clean-measure→sign.

## 5. HONEST GATES (the only un-built)
POD/owner gates: publish to `councilof.ai` (GHA merge — repo 1100-commit divergence + LFS) · `COUNCIL_SIGN_KEY`
(optional — signing works on-node) · social/arXiv (Nick/Claude).

## Master one-liner
The measurement body is now: **signed, stranger-verifiable measurement credentials (LIVE)** +
**built GTM products (Council Ledger/Dorado/Claimguard)** + **live arena measurement on the 3090**, all
hash-anchored and Ed25519-signed (key never left the node). The remaining moves are publish + the
sov33-unified build close-out.
