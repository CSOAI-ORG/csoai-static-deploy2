# E2E Audit & Alignment — MEOK Policy Lab / DORA Experiment

**Date:** 2026-06-22  
**Scope:** All changes made in this session from `meok_policy_lab.docx` intake through live A/B run, report generation, and public artifact publication.  
**Auditor:** JEEVES (Kimi Code CLI)

---

## 1. What was delivered

| Workstream | Deliverable | Location |
|---|---|---|
| Intake | Policy Lab alignment doc | `p0_aqua/docs/MEOK_POLICY_LAB_INTAKE.md` |
| Real-data policies | `DORAAutomatedPolicy`, `DORAManualPolicy` in `BUILT_IN` | `p0_aqua/benchmark/policy.py` |
| Experiment registry | First experiment JSON | `p0_aqua/experiments/dora_finance.json` |
| Experiment CLI | `vote`, `spawn --live`, `status`, `report` | `p0_aqua/policy_lab.py` |
| Live A/B run | Attested treatment + control runs | manifests in `p0_aqua/benchmark_runs/` |
| Regulator view | Static, aggregate-only HTML | `proofof-site/sovereign-town/experiments/dora-finance.html` |
| White paper | Full methodology & results | `proofof-site/sovereign-town/experiments/dora-finance-reports/dora_finance_001_whitepaper.md` |
| Regulatory brief | Executive summary (MD + DOCX) | `proofof-site/sovereign-town/experiments/dora-finance-reports/dora_finance_001_regulatory_brief.*` |
| Outreach draft | EU compliance officer email | `proofof-site/sovereign-town/experiments/dora-finance-reports/dora_finance_001_outreach_email.md` |
| Gap/roadmap tracking | Updated `AUDIT_GAPS.md` + `ROADMAP_13DAY.md` | `p0_aqua/` |

---

## 2. Final experiment results (14-day DORA window)

| Metric | Automated (treatment) | Manual (control) |
|---|---|---|
| Mean detection time | **1.0 h** | 8.2 h |
| Detection rate | **100%** | 38.9% |
| Missed incidents | **0** | 219 |
| False positive rate | 0.0% | 0.0% |
| Cost index (sim units) | **3,070** | 22,392 |
| Final trust | **0.5** | 0.0 |
| Status | **PROVEN** | — |

- **Treatment run id:** `984b99f4e513740e`
- **Control run id:** `f65c8a32a5310f8b`
- **Report generated:** 2026-06-22T06:29:27Z

---

## 3. Inconsistencies found and fixed during audit

| # | Issue | Fix |
|---|---|---|
| 1 | `DORAAutomatedPolicy` / `DORAManualPolicy` were defined but not added to `BUILT_IN`, so `load_policy()` rejected them | Added both classes to `BUILT_IN` in `benchmark/policy.py` |
| 2 | `policy_lab.py` did not request signed manifests, so `spawn --live` stored `run_id: None` | Added `"sign": True` to harness payload and extracted `manifest.id` |
| 3 | `policy_lab.py report` failed on a sanitized experiment because raw payloads were stripped | Added fallback to reuse embedded `exp["report"]` when payloads are absent |
| 4 | `experiments/dora_finance.json` had `duration_sim_days: 14` but the `dora_incident_deadline` scenario ran 21 days | Added `"DAYS": 14` to the scenario and re-ran the experiment |
| 5 | `policy_lab.py` module docstring listed only `vote`/`spawn`/`status` | Updated docstring to include `report` |
| 6 | README test count still said 34/selftest | Updated to 44/44 (see §5) |

---

## 4. Security & privacy review

| Check | Result |
|---|---|
| No API keys/secrets in new files | ✅ Only `config.API_TOKEN` references, no values |
| No raw ledger in public artifacts | ✅ Aggregate tables only |
| No agent names/PII in public artifacts | ✅ Verified via grep |
| Experiment JSON sanitized | ✅ `tick_states` removed; only summaries and metrics retained |
| Public regulator view has CSP + `frame-ancestors 'none'` | ✅ |
| Outreach draft requires opt-in before send | ✅ Note added at bottom |
| Live harness uses signed manifests | ✅ Both runs saved to `benchmark_runs/` |
| `policy_lab.py spawn` supports `SOV_TOWN_API_TOKEN` | ✅ Bearer header added when token configured |

---

## 5. Test surface

Run with `p0_aqua/.venv/bin/python`:

```bash
cd p0_aqua
PYTHON=/Users/nicholas/clawd/sovereign-town/p0_aqua/.venv/bin/python ./check.sh
```

Results:

- `selftest.py`: **44/44 passed**
- `e2e_test.py`: **58/58 passed**
- `browser_test.py`: **5/5 passed**

`README.md` test badge updated to reflect 44 selftest passes.

---

## 6. Alignment with `AUDIT_GAPS.md` / `ROADMAP_13DAY.md`

| Gap ID | Status | Note |
|---|---|---|
| PL-1 | ✅ Closed | Experiment registry + CLI landed |
| PL-2 | ✅ Closed | `spawn --live` wired to `/harness/run` with signed manifests |
| PL-3 | ✅ Closed | Deterministic BFT vote + unit test |
| PL-4 | 🟡 Partial | Static regulator view live; dynamic leaderboard widget still queued for Day 6 |
| PL-5 | ⏳ Open | Auto-spawn on new regulation → Day 10 |
| PL-6 | 🟡 Partial | Regulatory brief + whitepaper generated; deeper `report.py` integration queued |
| PL-7 | ⏳ Open | Per-experiment outcome aggregation → Day 10 |

Roadmap updates:
- Day 4: all scaffold items complete
- Day 5: live A/B run complete
- Day 6: static regulator view complete; dynamic widget open
- Day 11: first experiment report + brief complete

---

## 7. Operational notes

- The harness process on `:3941` was restarted twice during this work to pick up new policies and scenario changes.
- A local `.venv` was created under `p0_aqua/.venv` to run tests; it is not tracked in git.
- Old manifests from the 21-day pilot run remain in `p0_aqua/benchmark_runs/` but are no longer referenced by the experiment JSON.

---

## 8. Remaining risks / next actions

1. **Dynamic widget:** Add an experiment comparison card to the workbench/leaderboard (PL-4).
2. **Auto-spawn:** Hook new regulation detection to `policy_lab.py spawn` (PL-5).
3. **Outcome aggregation:** Feed experiment results into `distribution_events_state.json` / content factory (PL-7).
4. **Send gate:** The outreach email is a draft only — do not send without Nick's explicit review and consent.

---

**Conclusion:** The Policy Lab intake, real-data DORA policies, live A/B run, and public artifacts are aligned, tested, and secure. All P0/P1 items in scope are closed; remaining work is P2 roadmap follow-up.
