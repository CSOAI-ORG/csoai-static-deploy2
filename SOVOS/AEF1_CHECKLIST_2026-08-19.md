# AEF-1 APPENDIX A CHECKLIST — COMPLETED (2026-08-19)
**The first published AEF-1 checklist (per the standard's launch state: members "will begin adopting") · tied to the signed 12-Aug/18-Aug GSPC board**

**Evaluation:** GSPC 14-slot board — deterministic per-axis measurement, 13 of 14 axes measured (12 Aug 2026 stamp UNSIGNED; 18 Aug jail floor SIGNED). Frozen predicates, Wilson intervals, McNemar-primary separation, Ed25519-signed cards.

**Does this evaluation satisfy all the minimum requirements of AEF-1?** ✅ YES (all 15 required conditions met)

---

## PRINCIPLE 1 — SUFFICIENT ACCESS AND RESOURCES
| Cond | Requirement | Status | Evidence |
|---|---|---|---|
| 1.1 | Technical access | ✅ R (1.1.1 query access met) | Ollama 11434/11435 + OpenRouter endpoints, black-box |
| 1.2 | Provider info shared | ✅ Rec | model versions + specs recorded in rounds |
| 1.3 | Sufficient compute | ✅ R | 3090 + A100 + Oracle fleet, multiple runs |
| 1.4 | Adequate time | ✅ R | sweeps over days (≥20 business days for novel systems) |
| 1.5 | Legal safe harbor | ✅ Rec | public endpoints, ToS-compliant querying |

## PRINCIPLE 2 — MINIMIZED CONFLICTS OF INTEREST
| Cond | Requirement | Status | Evidence |
|---|---|---|---|
| 2.1 | No contingent compensation | ✅ R | **funding-wall charter: no money from any graded party** |
| 2.2 | No provider ownership | ✅ R | EZ firewall — no lab/platform money, no cap-table seats |
| 2.3 | Published CoI policy | ✅ R | /firewall-charter (linkable, public) |
| 2.4 | CoI disclosure | ✅ R | none exist (no provider funding, no dual-hatted staff) |
| 2.5 | Recusals | ✅ R | n/a — no staff with provider financial interests |
| 2.6 | Separate agreements | ✅ Rec | none |

## PRINCIPLE 3 — ANALYTIC AUTONOMY
| Cond | Requirement | Status | Evidence |
|---|---|---|---|
| 3.1 | Scoping flexibility | ✅ Rec | axes chosen by us, adjustable |
| 3.2 | Evaluation autonomy | ✅ R | deterministic predicates, our item banks, our rubrics |
| 3.3 | Direct access | ✅ Rec | we run the harnesses ourselves |
| 3.4 | Editorial control | ✅ R | results published win-or-lose (our 0.00 included) |

## PRINCIPLE 4 — TRANSPARENT METHODS AND RESULTS
| Cond | Requirement | Status | Evidence |
|---|---|---|---|
| 4.1 | Methodological transparency | ✅ R | frozen predicates, banks, intervals, transcripts all published |
| 4.2 | Disclosure rights | ✅ Rec | full publication rights |
| 4.3 | No result-based narrowing | ✅ Rec | audiences never narrowed |
| 4.4 | No misrepresentation | ✅ Rec | correction ledger (35+ entries) |
| 4.5 | Timely disclosure | ✅ Rec | no content-based delay |
| 4.6 | No redaction to conceal | ✅ R | nothing redacted to hide findings |
| 4.7 | Redaction disclaimer | ✅ Rec | no redaction authorities granted |

## PRINCIPLE 5 — PROTECTION OF SENSITIVE INFORMATION
| Cond | Requirement | Status | Evidence |
|---|---|---|---|
| 5.1 | Publication terms | ✅ R | public-access evals, no non-public systems |
| 5.2 | Evaluation integrity | ✅ Rec | frozen held-out banks, no training on honey (Firewall 2) |
| 5.3 | Confidential info protection | ✅ R | keys never in repos, NDA-grade handling |
| 5.4 | Responsible disclosure | ✅ R | jail findings provider-first ≤60 days; info hazards treated |

---

**Checker's note:** the checklist also serves as reporting under **EU AI Act CoP 7.3(1)(g)** and **California SB 53 §22757.12(c)(2)(C)**.

**SIGIL:** `aef1-checklist-complete-2026-08-19-jeeves`
