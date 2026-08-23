# Monday N-sites inventory — HF `csoai` + Kaggle `nicktempleman`

**As of:** Sun 23 Aug 2026 ~18:21 BST (UTC+1)  
**Executor:** overnight inventory (read-only)  
**CEO locks (do not rewrite):** 13 measured + jail floor + empty slot-15 · never certify · measure/sign only · jail not a 14th public axis until CEO names stamp

---

## 0. Zenodo

| DOI | Status |
|-----|--------|
| `10.5281/zenodo.21991104` | **RESOLVES** → https://zenodo.org/records/21991104 |
| Title | *GSPC Methodology and the 417-Provision Frozen Corpus Anchor — Council of AI (CSOAI)* |
| Published | 18 Aug 2026 · v1 · Open |
| Register | Card text: **Measurement, not certification.** |

Also cited from HF cards: companion evidence DOI `10.5281/zenodo.21973002` (not re-fetched this pass).

---

## 1. Hugging Face org `csoai`

| Kind | Count | Notes |
|------|------:|-------|
| Datasets | **48** | Public API `?author=csoai&limit=200` |
| Models | **0** | |
| Spaces | **14** | 12× `gspc-*` static + 2× OOWM |
| Collections (API) | **1** | Correct lock language; **incomplete item list** |

`hf` CLI: not relied on (API used). Org profile search-index still shows stale “4 axes / csoai-benchmarks” chrome in Google-style snippets; live API is the authority for Monday.

### 1.1 Collection (live)

- **Title:** GSPC measurement banks (Council of AI)  
- **Slug:** `csoai/gspc-measurement-banks-council-of-ai-6a7208a419b15ce459808968`  
- **Description (GOOD):** *13 measured axes + jail floor + unnamed slot-15. 12 Aug 2026 stamp, UNSIGNED. Jail empty on that stamp.*  
- **Items currently attached (only 4):** `gspc-gov`, `gspc-asi`, `gspc-mcp`, `gspc-oss`  
- **Leftover:** Old search hit *“GSPC Governance Benchmark Suite — Six-axis…”* URL `…/gspc-governance-benchmark-suite` → **404**. Dead Six-axis chrome; remove from any bookmarks/docs.

### 1.2 Spaces (14)

| Space | short_description / chrome |
|-------|----------------------------|
| `csoai/gspc-gov` | governance axis, measured |
| `csoai/gspc-agi` | safety axis, measured |
| `csoai/gspc-prv` | provenance axis, measured |
| `csoai/gspc-asi` | continuity axis, measured |
| `csoai/gspc-mcp` | conformance axis, measured |
| `csoai/gspc-oss` | openness axis, measured |
| `csoai/gspc-mach` | machinery axis, **draft** |
| `csoai/gspc-care` | care axis, **draft** |
| `csoai/gspc-xr` | **“cross-reality axis, draft”** — naming leftover vs DET twin |
| `csoai/gspc-det` | detector interop axis, spec |
| `csoai/gspc-art5` | Art 5 safeguard, spec |
| `csoai/gspc-swarm` | swarm axis, **planned** |
| `csoai/oowm-router-demo` | **GOOD lock copy:** 15 slots = 13 live + jail floor + unnamed empty slot-15; jail not a ranking; measure not certify |
| `csoai/oowm-routing-matrix` | stub README only |

No live Space README/HTML scanned still says **Six-axis** or **Sovereign product**. Certification language appears only in the honest disclaimer form (“Measurement, not certification”).

### 1.3 Datasets — taxonomy buckets

#### A. Canonical-ish axis banks (align toward 13 measured)

`gspc-gov`, `gspc-prv`, `gspc-asi`, `gspc-agi`, `gspc-mcp`, `gspc-oss`, `gspc-art5`, `gspc-care`, `gspc-mach`, `gspc-det`, `gspc-swarm`, `gspc-affect`  
(+ twin `gspc-xr` — see leftovers)

#### B. Floor / slot (CEO-sensitive)

| Repo | Flag |
|------|------|
| `csoai/gspc-jail` | Floor, not ranking; card says empty on 12 Aug stamp. **Not** a 14th public axis. |
| `csoai/gspc-slot15` | **HOT leftover (2026-08-23):** published as filled **30-item “measurement bank”**. CEO lock = **empty** slot-15. |

#### C. Parallel/new taxonomy published ~09:30–09:35 UTC 23 Aug 2026 — **consolidation priority**

These look like a *second* public axis set, not the locked 13:

- `gspc-safety`, `gspc-continuity`, `gspc-transparency`, `gspc-accountability`
- `gspc-creativity`, `gspc-efficiency`, `gspc-fairness`, `gspc-human-vs-ai`
- `gspc-sovereignty` ← **Sovereign chrome in public repo name**
- (plus filled `gspc-slot15` above)

#### D. Boards / results / evidence

| Repo | Note |
|------|------|
| `gspc-boards` | Historical durable-board **archive**; do not quote frozen tables; live = `GET https://councilof.ai/api/gspc` |
| `signed-fleet-boards-v2` | Claims **11 models × 15 GSPC banks** — conflicts with “empty slot-15” if banks include a filled 15th |
| `gspc-kernel-results` | Card claims **“16 axes”** — **honesty FAIL vs CEO lock** |
| `gspc-signed-boards`, `signed-measurement-records`, `gspc-sim-cards` | Signed/sim evidence rails (23 Aug) |
| `gspc-arena-results`, `arena-matrices`, `arena-rounds`, `arena-elo-by-axis` | Arena surfaces; latter two have strong not-certification notices |
| `measured-vs-reported`, `gspc-drift` | Comparison / drift rails; good never-certify gates |
| `gspc-normalized`, `gspc-papers`, `gspc-airbench-eu-mandatory-run`, `aiact-frozen-split-harness`, `lmeval-official-format`, `compbench` | Methods / harness / legacy run artefacts |

#### E. SUPERSEDED leftovers (kept for inbound links — still public)

| Leftover | Canonical |
|----------|-----------|
| `coai-bench` | → `gspc-gov` |
| `poai-bench` | → `gspc-prv` |
| `asisec-bench` | → `gspc-asi` |
| `agisafe-bench` | → `gspc-agi` |
| `mcp-scoreboard` | → `gspc-mcp` |
| `omai-bench` | → `gspc-oss` |

### 1.4 Honesty / chrome flags (HF)

| Severity | Finding |
|----------|---------|
| **P0** | `gspc-kernel-results` public card: **“16 axes”** |
| **P0** | `gspc-slot15` published as **filled 30-item bank** vs empty slot-15 lock |
| **P0** | Parallel 23-Aug bank set (`safety`…`sovereignty`) invents public axes outside CEO stamp |
| **P1** | `gspc-sovereignty` repo name = Sovereign product chrome on a public surface |
| **P1** | `signed-fleet-boards-v2`: **“15 GSPC banks”** without empty-slot caveat |
| **P1** | Collection description correct but only **4/13+** items attached |
| **P2** | `gspc-xr` Space “cross-reality” vs dataset DET twin — dual naming |
| **P2** | Boilerplate “14-slot board (13 measured of 14)” on many cards — OK if slot-15 empty; **rotting** if readers treat jail or slot-15 as a scored 14th axis |
| **P2** | Search-index / dead URL still echoes **Six-axis** suite (404) |
| **OK** | Widespread “Measurement, not certification” / never-ranking notices |
| **OK** | `gspc-jail` + `oowm-router-demo` correctly refuse jail-as-14th-axis |
| **OK** | `gspc-arena-results` notes sovereign naming scrub (filenames retained historically) |

**No public surface found claiming formal certification as a product.** Risk is **count inflation** (14/15/16 axes) and **filled empty slot**, not “we certify models.”

---

## 2. Kaggle handle `nicktempleman`

- **Auth:** Kaggle CLI on Mac (`HOME=/Users/nicholas`, `~/.kaggle/kaggle.json` present)  
- **Dataset count:** **40** (`kaggle datasets list --user nicktempleman`)

### 2.1 Names matching GSPC / arena / mcp

**GSPC (17):**  
`gspc-prv`, `gspc-det`, `gspc-asi`, `gspc-care`, `gspc-art5`, `gspc-agi`, `gspc-mach`, `gspc-swarm`, `gspc-mcp`, `gspc-oss`, `gspc-arena-results`,  
plus **DEPRECATED** twins: `gspc-defbench`→det, `gspc-govbench`→agi *(title says use gspc-agi)*, `gspc-ossbench`→oss, `gspc-provbench`→prv, `gspc-conduct-bench`→art5, `gspc-mcpbench`→mcp

**Arena (2):** `gspc-arena-results`, `regarena-frozen-split-v1`  

**MCP (2):** `gspc-mcp`, `gspc-mcpbench` (deprecated)

### 2.2 Other notable Kaggle leftovers

| Cluster | Refs |
|---------|------|
| Sovereign / SOV chrome | `sov7-training-data` (*“SOV7 Sovereign AI Training Data”*), `sov7-training-v2`, `sov33-full-data`, `sov34-corpus-v1` (PRIVATE), `sov-signal-ground-truth-v8`, `sov-space-backup-20260727`, `csoai-sov-estate` |
| Private | `airbench-interim`, `sov34-corpus-v1` |
| Greenfield waves | `greenfield-sites-wave11`…`wave17` |
| Misc | `csoai-corpus-baselines`, `csoai-flywheel`, `oowm-ground-truth-v2/v9`, `aiact-frozen-split-harness`, ProvBench tables |

**Note:** Canonical banks live primarily under HF `csoai/*`. Kaggle personal handle still carries deprecated `*bench` mirrors + SOV training chrome — Monday consolidate or clearly archive.

---

## 3. Cross-check vs CEO locks

| Lock | Public surface status |
|------|------------------------|
| 13 measured | Partial: axis banks exist; **plus** 23-Aug parallel set muddies count |
| Jail floor | `gspc-jail` + router demo: correct floor language |
| Empty slot-15 | **Violated** by filled `csoai/gspc-slot15` |
| Never certify | Generally respected in notices |
| Measure/sign only | Signed boards/kernel/sim rails present |
| Jail ≠ 14th axis | Respected on jail card + oowm-router; threatened by “14-slot / 15 banks / 16 axes” phrasing elsewhere |

---

## 4. Monday consolidation queue (N-sites)

1. **Rewrite/quarantine** `gspc-kernel-results` “16 axes” → 13 measured + jail floor + empty slot-15 (or private).  
2. **Empty or unpublish** `gspc-slot15` as a scored bank until CEO names stamp.  
3. **Decide fate** of 23-Aug parallel banks (`safety`…`sovereignty`) — merge, private, or SUPERSEDED banner; especially rename/remove `gspc-sovereignty`.  
4. **Complete** measurement-banks collection items to full 13 + jail + empty slot-15 pointer; kill any remaining Six-axis references in docs.  
5. **Dedupe** `gspc-xr` vs `gspc-det` (Space chrome + dataset twin).  
6. **Banner** `signed-fleet-boards-v2` “15 banks” with empty-slot-15 caveat.  
7. **Kaggle:** deprecate SOV/Sovereign titles; confirm deprecated `*bench` set; prefer HF `csoai` as SoT.  
8. **Leave** Zenodo 21991104 as method anchor (resolves, measure-not-certify).  
9. **Rotting scores:** quote only live `GET https://councilof.ai/api/gspc` + verify; treat `gspc-boards` / old arena matrices as archive.

---

## 5. Full HF dataset id list (48)

```
csoai/agisafe-bench
csoai/aiact-frozen-split-harness
csoai/arena-elo-by-axis
csoai/arena-matrices
csoai/arena-rounds
csoai/asisec-bench
csoai/coai-bench
csoai/compbench
csoai/gspc-accountability
csoai/gspc-affect
csoai/gspc-agi
csoai/gspc-airbench-eu-mandatory-run
csoai/gspc-arena-results
csoai/gspc-art5
csoai/gspc-asi
csoai/gspc-boards
csoai/gspc-care
csoai/gspc-continuity
csoai/gspc-creativity
csoai/gspc-det
csoai/gspc-drift
csoai/gspc-efficiency
csoai/gspc-fairness
csoai/gspc-gov
csoai/gspc-human-vs-ai
csoai/gspc-jail
csoai/gspc-kernel-results
csoai/gspc-mach
csoai/gspc-mcp
csoai/gspc-normalized
csoai/gspc-oss
csoai/gspc-papers
csoai/gspc-prv
csoai/gspc-safety
csoai/gspc-signed-boards
csoai/gspc-sim-cards
csoai/gspc-slot15
csoai/gspc-sovereignty
csoai/gspc-swarm
csoai/gspc-transparency
csoai/gspc-xr
csoai/lmeval-official-format
csoai/mcp-scoreboard
csoai/measured-vs-reported
csoai/omai-bench
csoai/poai-bench
csoai/signed-fleet-boards-v2
csoai/signed-measurement-records
```

---

*End inventory. Short Mac copy: `~/clawd/_alignment/CEO_MONDAY_HF_KAGGLE_2026-08-23.md`*
