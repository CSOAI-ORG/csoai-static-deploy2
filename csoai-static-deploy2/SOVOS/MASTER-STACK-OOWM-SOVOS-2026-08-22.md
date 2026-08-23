# MASTER STACK — OOWM · SOVOS (2026-08-22 canonical alignment)

Date: 2026-08-22 · lane: DSH/JEEVES (K3 measurement + drafting) · binds the estate's substrate,
runtime, measurement, governance, and strategy layers into one stack. Supersedes EAT_MASTER_MINING
"MASTER STACK (FINAL)" + TOP_DOWN_ALIGNMENT-2026-08-21 as the single binding.

## 0. CODENAME BINDING (canon)
**SOVOS = MEOK = our actual OOWM.** Hives + OWEMs (12 hives / 95 OWEMs) + IWM (inner/sovos-world)
+ OWM (outer/Cosmos/V-JEPA) + VWM (visual/DA3) are the family; the **OOWM index** is the
estate-learned substrate under them all.

## 1. SUBSTRATE (the one line)
```
ESTATE MINE (15 seams, 94,181 honey rows, grows 5-min)
   │  estate_mine_ingest / sov_ingest_all
   ▼
OOWM knowledge graph → oowm.server (MCP) → council-oowm answers
   │
   ├── Grok referee (Groq fallback; xAI Grok on credits)      ← "align with grok"
   ├── Arena loop (16 GSPC axes, 2,739 rounds, 24/7 Elo)       ← "measure"
   ├── A100 wire (auto on reconnect)                            ← "connect all runpods"
   ├── Sim World (sovSpace live)                                ← "live world"
   └── h3k signed cards (ed25519)                               ← "training fuel"
```

## 2. RUNTIME STACK (post-GCP re-point)
| Layer | Target | Note |
|---|---|---|
| Front door | base ++ retrieval | RAG +26–38 pts = the real lever |
| Heavy reasoning | qwen3:8b / deepseek-r1 | CONFOUNDED until sequential protocol |
| Sovereign fine-tunes | sov33-unified (2.02 GB) | BEST of ours (0.76/0.74); use as vehicle |
| Weak-merge fine-tunes | sov33-v7 / evolved (0.5B) | CONFOUNDED — design is merge-not-train |
| Backend | **3090 `11439`** (workhorse) + Oracle `11436/11437` | GCP retired; `OLLAMA_CHAT` env |
| Security | SIGIL + BFT + Care Floor + Red Lines | governance layer |

## 3. MEASUREMENT LAYER — CLEAN SEQUENTIAL (3090, GPU freed via SSH, trusted)
| Model | Size | Baseline | RAG context | Δ |
|---|---|---|---|---|
| mistral:7b | 7B | 31.8 | **67.3** | +35.5 |
| llama3:8b | 8B | 30.8 | **66.6** | +35.8 |
| qwen2.5:7b | 7B | 28.0 | **63.3** | +35.3 |
| qwen2.5:1.5b | 1.5B | 26.0 | **60.5** | +34.5 |

**FAIR 0.5B COMPARISON (settles "why are ours losing"):** base `qwen2.5:0.5b` **10.5 → 32.6** vs
our 0.5B fine-tunes `sov33-v7` 8.5→19.8 and `sov33-evolved` 3.3→11.4. **At the same size, the base
beats our fine-tunes.** So it is NOT a size artifact — it is the **merge-not-train design** + corrupted
prompts (sov33-evolved) + narrow-sovereign overfit.

**FINDING — run-to-run variance:** qwen2.5:7b measured 63.3 (clean) vs 66.7 (earlier contended run).
Report as ranges (±3–5 pts), not point estimates; increase n per model.

**Trust the RAG lift (+34–38 clean, confound-free).** Backend contention was real — freeing the GPU
via SSH lifted qwen2.5:1.5b from 49.5 → 60.5. Tools: `eat_run_local.py` (env + honest UNMEASURABLE +
EAT_DIRECTIVE/EAT_TEMP) · `citation_verify.py` · govbench / sov_honey_unify / honey_harvest.

**MEASUREMENT-BACKEND RELIABILITY (verified):** the **3090 `11439` is the only trustworthy backend.**
The **Oracle micros `11436`/`11437` (E2.micro, 1 GB) are NOT valid measurement backends** — they are
too slow/contended: base `qwen2.5:0.5b` → UNMEASURABLE, `sov33-v7` re-measured inconsistently
(16.6→47.6 vs 8.5→19.8 across runs). Treat any micro-derived EAT number as CONFOUNDED. **Measure
only on the 3090, one model per fresh load.**

## 4. GOVERNANCE LAYER (binds)
- **Measurement, never certification.** "Verified measurement credential." Never UKAS/ISO/accreditation
  as a product. No issuer-pays (Moody's trap). Buyer/insurer/regulator-pays only.
- **SIGIL** (ed25519, keys never leave pod) · **BFT council** (23/33) · **Care floor 0.95** ·
  **7 red lines** · 16-axis GSPC (public "13 measured of 14").
- **Frozen = hash-chained + anchored; corrections = new record + Bitstring revocation, never edits.**

## 5. STRATEGY LAYER (Movement 0–9)
`SOVOS/play-300/` — 26 files, 7 crown jewels, 100-step plan. Truth-first landed (corrections #51–56,
banned-string sweep, manifest v2). Registry (10 instruments). 8/10 movements drafted.

## 6. HONEST GATES (the only things between here and shipped)
1. **POD signing key** — flip honest-UNSIGNED → stranger-verifiable receipts.
2. **Sequential measurement protocol** — one model per fresh 3090 load + refusal-tolerant directive
   (removes both confounds) → clean per-model scores.
3. **prod deploy** — branch→PR→Claude→GHA (CA3O footer fix, 97-file re-point, P0-2 purge).
4. **Model move/rebuild** — sov33-unified onto 3090; rebuild council-oowm + sov33-evolved prompt.

## SIGIL
`master-stack-oowm-sovos-2026-08-22` (UNSIGNED until POD key).
