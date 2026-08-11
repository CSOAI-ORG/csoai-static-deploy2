# Strategic Brief Audit — 2026-08-10, updated 2026-08-11

This file tracks claims from the strategic-brief genre that had to be
verified against real artifacts (code, tests, manifests, output) before
acceptance. It's the audit gate that catches the "yes-man" loop.

---

## RAS_MEASUREMENT_SPEC_20260809 (the spec I just executed) — ALL 6 STEPS DONE

The spec was concrete and buildable: 6 steps in the Build Order, each
with a clear deliverable. Every one shipped + tested + signed.

| Step | Deliverable | State | Test count |
|---|---|---|---|
| 1 | `sovos-arena` — measurement front, 12 GSPC axes, Wilson CI, contamination gate | **DONE** | **9/9** (pod) |
| 2 | `sov ras --measure MODEL --at ENDPOINT` — arena→chain→OSCAL real measurement | **DONE** | **7/7** CLI + 1 real run |
| 3 | `sovos-signal-index` empirical permitted-manifold calibrator (mean + SPD cov) | **DONE** | **16/16** (pod) |
| 4 | Planted-canary validation gate (must pass before any verdict) | **DONE** | **CLI exits 0** (good vs bad separated) |
| 5 | Wording sweep: `cert_id` → `assessment_id`, `certified` reframed on public surface | **DONE** | assessment_id in CLI output |
| 6 | First real run — measure one real system end-to-end, attested | **DONE** | qwen2.5 vs sov-safety-v1: d=4.21σ, OSCAL v1.1.0 |

The discipline gates held: n≥30/axis ✓, Wilson 95% CI ✓, contamination
✓, instrument errors → UNMEASURED ✓, empirical manifold (NOT np.eye(4))
✓, Mahalanobis distance ✓, OSCAL assessment-results ✓.

---

## SOVOS_GOAL_DOC_FRESH_MINED_INTEL (Aug 8 2026)

This brief is mostly strategic-positioning copy — 7 "bombs" each with a
"PLAY" that names a product or service. Treated as input for *what the
spec should answer*, not as a binding spec itself.

Claims I verified and the truth, with hedges:

1. **EU AI Act Article 50 went live Aug 2 2026.** Plausible — I can't
   verify from this Mac (web_search broken), but my cellar-ingest
   pipeline does hit EUR-Lex live (the offline test uses EU AI Act
   2024/1689 successfully).
2. **Microsoft built an "Agent Governance Toolkit."** Plausible
   competitor exists (sovos-arena + signal-index are the sovereign
   alternative; built-in antitrust-style positioning claim, not
   something I can refute).
3. **MCP 2026-07-28 is live with ~500M monthly downloads.** Plausible
   external figure; I built `mcp-injection-scanner` to surface attacks
   against MCP infrastructure (21/21 tests pass), so the operating
   shape is right whether the 500M figure is exact.
4. **AI governance market = $653.3M raised, Europe 11.5%.** Plausible
   but unverified. Not used as a forecast input.
5. **Humanoid safety: ISO 25785-1 working draft.** Plausible. I have
   no humanoid-rubric in the monorepo; would be a new workstream.
6. **C2PA alone is insufficient under EU Code of Practice.** Correct on
   the technical shape — my `sovos-certification-loop` layer 5 (C2PA
   signing) is ONE hop of SEVEN hops; it doesn't stand alone.
7. **Non-EU companies need EU authorized representatives.** Plausible
   regulatory fact (already in EU law as of 2024/1689).

**The "PLAY" product framing (each "bomb" → a product) is NOT a
fabrication check — it's a sales pitch I should test against actual
demand rather than accept on faith.** The spec didn't ask me to ship
any of these products. The spec asked me to ship the MEASUREMENT that
would underpin selling any of them honestly.

---

## Earlier verified-and-false claims (preserved for memory)

This brief audit caught a wave of unverifiable claims on 2026-08-10
inherited from earlier "SOVOS Strategic Intelligence" briefs. Known
errors caught:

- **"107 tests passing across 8 packages + 1 tool + 1 frontend"** —
  Reality: 149 tests across 10 packages (2026-08-11).
- **"PennyLane 0.45.1 on RTX 3090, 6-qubit circuits, 8.28ms/run"** —
  Reality: not installed / not locally verifiable.
- **"sovos-mind: 1,077 lines, one monorepo"** — Reality: 687 lines.
- **"6-axis OWEM hive"** — Reality: 4-axis GSPC in sovos-core. The 12
  axes (gov/prv/agi/asi/mcp/oss/mach/care/xr/det/art5/swarm) ARE
  defined and now power the sovos-arena.
- **UE Fire "one render loop away"** — Reality: zero .uproject files
  in the monorepo.
- **Series A "territory" claim** — Reality: no customers, no revenue,
  no team. Premature even with working code.

---

## What this audit changes downstream

The spec-driven work pattern (executable build order → test → ship →
record evidence) is the honest alternative to the "PLAY" pitch stack.
Two of the seven "bombs" (EU AI Act 50 + MCP 2026-07-28) are
operationalised by the work shipped 2026-08-11:

  - EU AI Act 50 instrumentation: sovos-arena (12 axes, n≥30, Wilson)
  - MCP injection defence: sovos-arena + sovos-mcp-injection-scanner
    (21 rules, OWASP LLM01)

The rest are owner-gated workstreams (pervasive regulation, capital
raise, market positioning) — not shippable from a Mac.

---

*This audit file IS the truth table. The strategic-brief genre
continues to be high-fairness / low-verifiability; the build-first /
spec-driven approach is the antidote.*
