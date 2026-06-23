# MEOK Policy Lab — Intake & Alignment

**Source:** `/Users/nicholas/Downloads/meok_policy_lab.docx` (20,530 bytes, Word 2007+)  
**Ingested:** 2026-06-22  
**Owner:** JEEVES (strategic alignment)  

---

## 1. What the document says

The Policy Lab reframes Sovereign Town from a *governed-vs-ungoverned simulation* into a **policy-experiment platform**:

| Concept | Meaning in our codebase |
|---|---|
| **Town** | Experiment container (treatment vs control) |
| **Industry / Hive** | Compliance testbed (DORA, EU AI Act, NIS2, GDPR, etc.) |
| **Civilization** | Governance-model variant (parliamentary, technocratic, federal, etc.) |
| **"Go Fund Us"** | BFT Council votes to fund experiments; proven ones auto-scale |
| **Regulator View** | Public dashboard + downloadable audit trail / white paper |
| **Data Moat** | Every experiment adds behavioral outcomes; uncopyable dataset |

The immediate ask is **Hour 1**: start the first experiment — *DORA Finance Compliance, automated vs manual incident reporting* — with a treatment town, a control town, live metrics, and a public dashboard.

---

## 2. Alignment with current architecture

What already exists and maps cleanly:

| Policy Lab idea | Existing Sovereign Town piece | Gap |
|---|---|---|
| Run two policies head-to-head | `benchmark/server.py` `/harness/run` + `/harness/leaderboard` | No explicit treatment/control pairing |
| Signed, attestable outcomes | `sign_lib.py`, signed run manifests, `verify_chain.py` | Experiments are not yet first-class signed artifacts |
| Live dashboard | `dashboard_server.py`, `dashboard.html`, `town3d.html` | No experiment-specific view |
| Public leaderboard | `proofof-site/sovereign-town/leaderboard.html` | No experiment filter / comparison page |
| BFT Council / voting | `common.py` personas, 12-around-1 council concept | No programmatic vote/spawn loop |
| Auto-scaling proven policies | `flywheel_forever.py`, `train_all_hives.py` | No experiment-to-flywire bridge |
| Regulator-ready white paper | `report.py` → MEOK Labs index | No experiment-specific report generator |

---

## 3. New gaps surfaced by the intake

These are added to `AUDIT_GAPS.md` and scheduled in `ROADMAP_13DAY.md`.

| ID | Priority | Finding | Suggested Fix | Roadmap Day |
|---|---|---|---|---|
| PL-1 | P1 | No experiment registry or JSON schema | Create `experiments/` directory + `policy_lab.py` CLI | Day 4 |
| PL-2 | P1 | No treatment/control pairing in harness | Extend `policy_lab.py` to call `/harness/run` twice and link run IDs | Day 4 |
| PL-3 | P1 | No BFT Council vote simulation | Add deterministic council vote to `policy_lab.py vote` | Day 4 |
| PL-4 | P2 | No experiment-specific dashboard | Add `/experiments/<id>` view or filter on leaderboard | Day 6 |
| PL-5 | P2 | No auto-experiment spawning on new regulation | Hook regulation parser → `policy_lab.py spawn` | Day 10 |
| PL-6 | P2 | No experiment white-paper / regulator brief export | Extend `report.py` with experiment template | Day 11 |
| PL-7 | P2 | No "data moat" aggregation per experiment | Append experiment outcomes to `distribution_events_state.json` / content factory | Day 10 |

---

## 4. Concrete artifacts created

- `experiments/dora_finance.json` — first proposed experiment (DORA automated vs manual) using real DORA policy classes.
- `benchmark/policy.py` — added `DORAAutomatedPolicy` and `DORAManualPolicy` grounded in Regulation (EU) 2022/2554 Arts. 12 & 14.
- `policy_lab.py` — CLI for `vote`, `spawn`, and `status`.
- `proofof-site/sovereign-town/experiments/dora-finance.html` — safe, static, aggregate-only regulator view.
- First live A/B run executed (`policy_lab.py spawn --live`):
  - Treatment `dora_automated`: 1.0 h mean detection, 100% detection rate, 0 missed.
  - Control `dora_manual`: 8.0 h mean detection, 38.2% detection rate, 370 missed.
  - Experiment status: **PROVEN**.
- `policy_lab.py report` computes DORA metrics, sanitizes the experiment JSON, regenerates the regulator HTML, and exports:
  - White paper (`dora_finance_001_whitepaper.md`)
  - Regulatory advisory brief (`dora_finance_001_regulatory_brief.md` + `.docx`)
  - Outreach email draft (`dora_finance_001_outreach_email.md`)
- This intake document.

---

## 5. Recommended execution order

1. **Day 4 (today/tomorrow):** land `policy_lab.py` + `experiments/dora_finance.json`, add unit test for vote logic.
2. **Day 5:** wire `spawn` to the harness with API-token support and run a dry-run A/B pair.
3. **Day 6:** add experiment comparison widget to the public leaderboard / workbench.
4. **Day 10:** build regulation→experiment trigger and auto-archive logic.
5. **Day 11:** generate regulator brief / white-paper from experiment results.

---

## 6. Decisions

### Real data only
The first experiment uses **real DORA policies**, not `sovereign_gate`/`ungoverned` proxies. `benchmark/policy.py` now exposes:
- `dora_automated` — auto-classifies and reports critical/major ICT incidents under DORA Arts. 12 & 14.
- `dora_manual` — models a human business-hours desk that misses off-hours and end-of-day incidents.

### Regulator-view safety & security
**Recommendation implemented:** keep the detailed, live experiment dashboard **local and bearer-token authenticated**; publish only a **static, aggregate-only, signed-snapshot regulator view** under `proofof-site/sovereign-town/experiments/`. This mirrors the existing `fleet-status.html` pattern and preserves the bright lines:
- No raw ledger, no agent identities, no PII.
- No live control surface or API exposed to the public.
- CSP + `frame-ancestors 'none'` + no external scripts.
- Every number is explicitly labelled **SIMULATION / PREDICTION**.

## 7. Open questions for Nick

- Which civilizations should be modeled first? The document proposes 12; the sim currently has 28 hives/districts.
- Should the regulator view auto-refresh from a sanitized export job, or remain a manually updated static snapshot until the experiment is proven?
