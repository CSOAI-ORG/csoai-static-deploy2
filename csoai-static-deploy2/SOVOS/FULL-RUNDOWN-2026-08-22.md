# FULL ALIGNMENT & RUNDOWN — 2026-08-22 (authoritative)

Lane: DSH/JEEVES · console: this is the single consolidated rundown of the estate as of 2026-08-22.
Source-of-truth chain: `SOVOS/canon/SOVOS-MASTER-PART-A/B` (3-weeks knowledge) → `ESTATE-STATE` →
this rundown. Everything is hash-anchored; the canonical artifacts are Ed25519-signed (see §6).

## 1. SUBSTRATE & BACKENDS (post-GCP)
- **Mine** → OOWM knowledge graph → council-oowm → 16-axis arena (2,739 rounds) → Sim World → h3k cards.
- **Inference:** RunPod **3090 `11439`** (workhorse) + Oracle micros (`11436`/`11437`). GCP retired.
- **SSH access:** working — `runpodctl` resolves the 3090; Oracle micros via `id_ed25519`. Bridge honors
  `OLLAMA_CHAT` (re-point from stale `11434`).

## 2. MEASUREMENT (clean sequential, 3090, confound-free RAG lift)
| Model | baseline → RAG |
|---|---|
| mistral:7b | 31.8 → **67.3** |
| llama3:8b | 30.8 → **66.6** |
| qwen2.5:7b | 28.0 → **63.3** |
| qwen2.5:1.5b | 26.0 → **60.5** |

**Fair 0.5B:** base `qwen2.5:0.5b` (32.6) > sov33-v7 (19.8) > sov33-evolved (11.4). **Design flaw
(merge-not-train + corrupted prompt), not a size artifact.** RAG = +34–38 pts (retrieved >> trained).

## 3. MODELS
- **Base (healthy):** qwen3:8b, llama3:8b, mistral:7b, qwen2.5:7b, qwen2.5:1.5b, qwen2.5:0.5b-instruct.
- **Ours (sov33-*):** sov33-unified (3.2B llama q4, on micro, needs 3090) · sov33-v7/evolved (0.5B, weak).
- **Corrupted:** council-oowm (rebuilt → **council-oowm-clean** 397MB) · muse-glimmer (18GB, hangs).
- **Rebuild done this session:** `council-oowm-clean` (from clean qwen2.5:0.5b-instruct + sovereign prompt).

## 4. REGISTRY & STRATEGY (done)
- `registry/instruments-2026-08-22.json` — 10 instrument rows (SB 315, Vietnam, KI-MIG, transparency code, …).
- `play-300/` — strategy-layer files (note: MOST mirror the canon; 4 are genuinely new spec).
- `NEXT-100-STEPS.md` — 100-step plan (Phase A–F).

## 5. WHAT'S GENUINELY NOT-DONE (the real actions, not docs)
| Item | Type |
|---|---|
| Deploy the verification product (verify.html + evidence → councilof.ai) | Claude→GHA |
| Pull `sov33-unified` → 3090 + measure clean | LANE/pod |
| Rebuild `sov33-evolved` full prompt | LANE/pod |
| Persistent sequential-measurement protocol | LANE |
| Intel filesystem deadlock (host-FS, 95% full) | SYS |
| `COUNCIL_SIGN_KEY` in harness (optional — signing works via on-node `sign.py`) | NICK |

## 6. VERIFIABLE EVIDENCE (the milestone — signed on the node, key never leaves)
- `SOVOS/evidence/signed/` — **14 Ed25519-signed artifacts** (12 state/strategy + evidence-index + verify-page).
- `verify_signature.py` — portable verifier (cryptography lib).
- `verify.html` — **browser-verifiable** (WebCrypto) deploy-ready page.
- **All 12/12 VALID + 12/12 hash-MATCH + tamper-sensitive.**
- Pubkey: `bWbk52E47J6EkY4+pu0Hh/B1l1175AZoZsDEBr0EfWA=` (did:web:csoai.org trust root).

## 7. THE ONE-LINE STATE
The estate's measurement + registry + strategy are now **cryptographically attested and independently
verifiable** (browser or python), the measurement is **clean and confound-free**, and the models'
relative ranking is **proven** (base > our 0.5B fine-tunes; merge-not-train is the flaw). The remaining
work is **deploy + model-pull + the gate clearances** — all honest, none hidden.

## SIGIL
`full-alignment-rundown-2026-08-22` (UNSIGNED pending on-node signing; see §6).
