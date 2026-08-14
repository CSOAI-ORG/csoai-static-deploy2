# HF + Kaggle 13-Axis Estate Plan — 2026-08-12

**Scope:** everything that must happen on Hugging Face and Kaggle to take all 13 GSPC axes to quotable, correctly-named, signed, DOI'd public artifacts — plus the exposures found in this pass that must be killed first.
**Method:** live web-index verification of HF + Kaggle public surfaces (HF API unreachable from sandbox; search-index and page fetches used). Every inventory row below is REAL (observed 2026-08-12) unless marked.

---

## 1. Verified estate inventory (REAL, observed 2026-08-12)

### Hugging Face — `csoai` org

| Asset | Type | State observed | Problem |
|---|---|---|---|
| gspc-gov | dataset | Live; arena page says n=237 re-measured, sov34 acc 0.515 Wilson [0.451, 0.578] (2026-08-05) | Card carries **"sov34"** name publicly |
| gspc-care | dataset | Live; card at 200 (100/100) after 63→200 fix | 200-vs-201 board reconciliation still **OWED** |
| gspc-affect | dataset | Live; 34 public + 1 canary; 13/10/11; severity v2 sha 4ed69ea | Newest axis — page/product not yet built |
| gspc-mach | dataset | Live; measured board added 2026-08-11 (RunPod 3090); expanded measured bank n=33 (2026-08-05 board) | Closest to quotable after gov |
| gspc-xr | dataset | Live | Kaggle title-edit gate now confirmed relevant (Kaggle copy exists) |
| gspc-prv | dataset | Live; C2PA manifest-survival bank; canary GSPC-CANARY-GUID present | No model comparison yet (clean board re-running) |
| gspc-papers | dataset | Live; regulatory-clock content | **TITLE BLEED: "GSPC / SOVOS — Papers, Methods & Roadmap" — SOVOS on a public card** |
| gspc-arena-results | dataset | Live | **MAJOR NAMING BLEED: "SOV3 arena", "sovereign model relay", "sov34_board.json", "sovereign_family_map.json — ~30 trained sovereign variants" all on the public card** |
| gspc-normalized | dataset | Live (518 rows shown in index) | Audit card vs board numbers (set-naming) |
| gspc-boards | dataset | Live; updated today | Confirm it carries hashes, not just numbers |
| gspc-swarm | dataset | Live; SwarmBench protocol v0.1, honesty clause, n_eff retraction story | Gold standard card — template for all others |
| coai-bench / poai-bench / asisec-bench / agisafe-bench / omai-bench / mcp-scoreboard | datasets | Live (pre-GSPC naming generation) | Naming-generation drift: two naming eras coexisting |
| **csoai/sov-compliance-art5** | **model** | Live; GGUF, served via vLLM/Ollama/LM Studio widgets | **sov-* name on a public model + GGUF = CVE-2026-5760 untrusted-code class** |

### Kaggle — `nicktempleman` personal account

| Asset | State observed | Problem |
|---|---|---|
| gspc-defbench | **LIVE** (DefBench — Refusal & Robustness) | AUDIT CORRECTION: Kaggle presence is not zero — it exists under the personal account |
| gspc-mcpbench | Live, marked "DEPRECATED — use gspc-mcp" | Deprecation pointer text says **"the full sovereign…"** — sovereign-class wording on Kaggle |
| other gspc-* sets | Not found | councilof.ai/arena publicly claims "Every item set is public on Hugging Face **and Kaggle**" — **claim ahead of reality for most sets** |

**Canon correction to the 2026-08-12 audit:** "Kaggle all-404 / absent" → **Kaggle presence is partial under nicktempleman, inconsistently named, with one deprecated duplicate.** Old verdict replaced.

---

## 2. Exposure kills — do these FIRST (before any new publishing)

| # | Kill | Where | Gate |
|---|---|---|---|
| K1 | Retitle gspc-papers — remove "SOVOS" from the public card title | HF | lane can execute; no owner gate (text edit) |
| K2 | Rewrite gspc-arena-results card — SOV3→public arena name, "sovereign model relay"→relay, rename sov34_board.json / sovereign_family_map.json references or regenerate files with clean names | HF | lane; file renames inside the repo need a re-push |
| K3 | Rename or delist csoai/sov-compliance-art5 model; if kept, card must carry GGUF-untrusted-code notice and no sovereign-class language | HF | **OWNER** (model disposition = weights surface) |
| K4 | Fix Kaggle gspc-mcpbench deprecation text ("sovereign" wording) | Kaggle | lane (account holder = owner login — likely **OWNER** for credentials) |
| K5 | Either mirror every public item set to Kaggle or edit councilof.ai/arena to "public on Hugging Face, Kaggle mirrors rolling out" — the current sentence is an overclaim | Kaggle + site | lane |
| K6 | HF token rotation (post-breach posture) — blast radius covers every push below | HF | **OWNER** |

Naming canon (binding, all public surfaces): `csoai/gspc-<axis>` datasets, `csoai/<public-line-name>` models only. Never: SOVOS, SOV OS, SOV<n>, sov-*, "sovereign" as product/weights language. Names are free, numbers are earned — and sovereign-class names are internal only.

---

## 3. The Quotable Card Standard (every axis, one schema)

Template = gspc-swarm (honesty clause) + gspc-affect (severity v2 + canary) + arena-results (CIs). Mandatory sections:

| Section | Rule |
|---|---|
| Set-named counts | Every number names its set: public split / held-out split / board bank. Never interchangeable (the 201/63/200 lesson) |
| Split policy | Public items + held-out items + exactly 1 canary per bank; held-out count disclosed, items withheld |
| Measurement block | n, Wilson 95% CI, judge hash, aggregator version — the signed triple (gold + rows + aggregator version) |
| Honesty clause | Binding register: measurement vocabulary only; UNMEASURED never scored wrong; ties called ties |
| Provenance | Board sha, run date, host class (e.g. "RunPod 3090"), code commit |
| Law anchors | Where applicable: Art 5 / Art 50 / Annex III mapping (affect, art5, gov) |
| Severity | severity 1–5 + severity_basis where the axis grades harm (affect v2 schema) |
| License + citation | License field populated; Zenodo DOI once minted |
| Labels | SIMULATED where items are synthetic; COUNSEL-PENDING where legal labels await blessing |

---

## 4. The 13-axis matrix — status → next action

Axis identities below are REAL (observed in public artifacts). The **canonical 13-name registry export from code (GSPC_AXES) is OWED** — the numbers registry (Stage 0, A4) owns the authoritative list; this matrix is built from public evidence and must be reconciled against it.

| Axis (public name) | Public asset | n (set-named) | Measured? | Next action |
|---|---|---|---|---|
| gov (risk tiering) | gspc-gov + GovBench | 237 public arena set | YES — sov34 0.515 [0.451, 0.578], 2026-08-05 | Rename sov34 ref in card; mint signed triple; Zenodo DOI; Kaggle mirror |
| mach | gspc-mach | 33 measured bank (2026-08-05 board) + 2026-08-11 board | YES | Wilson + judge hash on the 08-11 board → quotable candidate #2 |
| care | gspc-care | 200 public card (100/100); 201 board claim unreconciled | Board exists | Reconcile 200-vs-201; then n≥30 Wilson run |
| affect (13th) | gspc-affect | 34 public + 15 held-out (49 full); 13/10/11 | Bank published; measurement owed after re-bolt | Counsel blessing (labels + severity basis) → measure → Emotional Safety Card v1 |
| xr | gspc-xr | 32 (per arena-results starved note) | Starved (<60 note) | Author items to n≥60 → train/eval split → measure |
| prv (C2PA) | gspc-prv | 32 + canary | Clean board re-running | Complete re-run; ProvBench model comparison |
| asi | gspc-asi (agisafe-bench legacy) | 33 | Starved note says needs authored items | Author → n≥60 → measure |
| def (refusal) | DefBench; Kaggle copy | 14 arena set | 17-model v1 comparison (retired) | Grow bank; re-measure at n≥30; fix Kaggle text |
| pqc (continuity) | PQCBench | 33 arena set | Board n=33 best 0.606 (sov6-logic) recovered post-incident | Wilson + judge hash → quotable candidate #3; rename sov6-logic ref publicly |
| mcp | gspc-mcp + MCPBench | 11 arena set | 17-model v1 (retired) | Grow bank (11→≥30); Kaggle deprecation already pointed here |
| oss (licence) | OSSBench | 16 arena set | — | Grow to ≥30 |
| swarm | gspc-swarm | 6 protocol items | Protocol only — by design | Keep as protocol; first measured uplift/n_eff run when fleet exists |
| art5 (prohibitions) | gspc-art5 gold bank + sov-compliance-art5 model | Gold seed published | v1-row provenance cleanup owed | Cleanup → counsel blessing → measure; model disposition (K3) |

**Register: axis names REAL from public artifacts · canonical 13-list OWED from code registry · "six arena axes" (gov/def/prv/pqc/mcp/oss) is the arena subset, not the suite.**

---

## 5. Per-axis publish pipeline (the assembly line)

```
bank → item_gate (ACCEPT/ADJUDICATE/REJECT, Blind-Spot Rule)
     → usable_n ≥ 30 → Wilson intervals → ratified judge hash
     → signed triple (gold + rows + aggregator version) [+ Sigsum receipt once owner enables]
     → HF card (§3 schema) → Zenodo DOI → Kaggle mirror → arena link-back
     → Delta Note entry if numbers change
```

Gates that block axes today: counsel blessing (art5, affect labels + severity basis) · JUDGE.lock re-bolt (owner) · item authoring for starved banks (xr/asi/def/mcp/oss) · 200-vs-201 reconciliation (care) · Sigsum on net-capable host (owner).

---

## 6. Kaggle strategy (decision + execution)

**Decision (OWNER):** keep publishing under `nicktempleman` or create a Kaggle org/team identity. Recommendation: create the org identity now — the estate is a measurement body; a personal account holding the public mirrors is the same class of problem as the GitHub drift. Until decided, all Kaggle edits are owner-login.

Execution either way:
1. Fix gspc-mcpbench deprecation text (K4).
2. Mirror every public HF split in §4 order of readiness (gov first — it's the quotable flagship).
3. Every Kaggle dataset: same card schema as §3, DOI backlink to Zenodo, link to HF as source of truth.
4. Kill duplicate/deprecated copies once mirrors land (one canonical name per axis).
5. Only then is the arena page's "HF and Kaggle" sentence true — or apply K5 first.

---

## 7. Ordering vs the E2E stage plan

| Stage | Adds |
|---|---|
| 0 (ungated, now) | K1, K2, K5-edit; canonical 13-axis registry export; gspc-art5 provenance cleanup; 200-vs-201 reconciliation; secrets scan before any re-push |
| 1 (owner batch) | K3 model disposition, K4 Kaggle login work, K6 token rotation, Kaggle org decision, JUDGE.lock re-bolt, counsel blessing, Sigsum host |
| 5 (publish wave 1) | gov signed card + DOI → Kaggle mirror; mach + pqc quotable candidates; affect page after measurement; Delta Note #1 covers all card edits |
| 6 (productization) | Emotional Safety Card v1 (affect), Art 50 evidence pack (gov + art5 + xr) — 92-day clock |

**Standing rules in force on every push:** naming canon · set-named counts · no sovereign-class strings publicly · GGUF = untrusted code · killed claims never recur · durable copies on independent failure domains before any destructive rename.
