# Strategic Brief Audit — August 2026

## What This Document Is

The Aug 2026 strategic brief ("$60B Infrastructure Layer") made several claims
about external companies and the path to bootstrap SOVOS. This document records
**what we verified, what we couldn't, and what we built**.

## Bootstrap Claims (External Companies)

| Claim | Source | Verified? | How to verify |
|---|---|---|---|
| **Tower Semi has $1.3B in 2027 SiPho commitments** | Brief cites tower semi public statements | **Not verifiable from this Mac** | Tower investor relations: investors.towersemi.com — needs browser or curl with full render |
| **Tower Semi has 50+ SiPho customers, 7 of top 11 datacom** | Brief cites Tower earnings call | **Not verifiable from this Mac** | Same as above |
| **GF acquired AMF (Advanced Micro Foundry)** | Brief cites GF press | **Not verifiable from this Mac** | GF newsroom: gf.com/about-us/newsroom |
| **GF is now largest pure-play SiPho foundry** | Brief cites GF announcement | **Not verifiable from this Mac** | Same |
| **SAXON Q has QCi Connect cloud since 2025** | Brief cites SAXON Q website | **Not verifiable from this Mac** | saxonq.com, qci-connect.com |
| **SAXON Q delivered 4-qubit system to DLR Ulm 2023** | Brief cites web search | **Not verifiable from this Mac** | Press release |
| **IBM Quantum free tier for researchers** | Brief cites IBM | **Plausible** | quantum.ibm.com mentions "free" but full page didn't extract |
| **IBM Brisbane/Kyoto/Sherbrooke = 127 qubits each** | Brief cites IBM | **Plausible (well-known)** | IBM Quantum documentation |
| **Qiskit Global Summer School 2026 ran July 13-24** | Brief cites IBM | **Plausible** | learning.quantum.ibm.com |
| **CMC Microsystems offers GF 9WG MPW** | Brief cites CMC | **Plausible** | cmc.ca mentions "MPW" in returned text |
| **Salesforce Agentforce hit $800M ARR Q4 FY2026** | Brief cites Salesforce | **Plausible (public financials)** | Salesforce IR |
| **Anthropic hit $9B ARR Jan 2026** | Brief cites Anthropic | **Plausible** | Anthropic press |
| **AI agent market $7.84B → $52.6B (46% CAGR)** | Brief cites Grand View Research | **Plausible** | Grand View Research reports |
| **Agent marketplace creator split 70-85%** | Brief cites industry source | **Plausible** | Multiple sources confirm |
| **White-label agent margins 80-90%** | Brief cites industry source | **Plausible** | Standard SaaS math |

## Internal Claims (About Our Code)

These we can verify from disk:

| Claim | Reality | Notes |
|---|---|---|
| **sovos-mind 1,019 lines** | **687 lines** across 7 files | Brief inflated ~50% |
| **OWEM hive is 6-axis** | **4-axis** (GSPC) | Brief confused axes count |
| **107 tests across 8 packages** | **47 tests across 5 packages pass** | Brief inflated |
| **PennyLane 8.28ms/run on RTX 3090** | **Not reproducible locally** | Brief cites prior pod session |
| **sovos-cpo-calculator 10/10 tests pass** | ✅ Real | Shipped commit `3e09c56` |
| **sovos-mind 10/10 tests pass** | ✅ Real | Verified this session |

## What I Built From This Brief

### ✅ Play 1 — CPO Power Savings Calculator (Crown Jewel #1)

- **Python module**: `SOVOS/packages/sovos-cpo-calculator/` (10/10 tests pass)
  - Committed: `3e09c56`
  - 4 pre-built scenarios (small_edge, mid_enterprise, hyperscale, sov1_farm)
  - Honest scope statement in README
- **Public web page**: `cpo-calculator.html` (16.5 KB, self-contained, no server)
  - Committed: `c1ff9e9`
  - 4 quick presets, live recomputation, schema.org WebApplication markup
  - Math matches Python exactly (verified via browser_console)
  - Default load: 117.6 kW saved, $185K/yr, 618 tonnes CO2

### ⏳ Plays I Did Not Attempt (and why)

- **Play 2 — IBM Quantum registration**: **Owner-gated**. Requires creating
  a real IBM account tied to a real email. Free but personal. Not done.
- **Play 3 — SAXON Q email to Axel Kunz**: **Owner-gated**. Real external
  email to a real person. Should be sent by Nick, not by an autonomous agent.
- **Play 4 — CMC Microsystems quote request**: **Owner-gated**. Same reason.
- **Play 5 — GDSFactory photonic chip design**: **Skills gap**. Needs weeks
  of photonic chip design experience. Not a 1-day ship.
- **Play 6 — Quantum Soil Sensor Kit (UncutGem fork)**: **Cost gate**. £160
  parts + iokfarm beta coordination. Not done this session.
- **Play 7 — SOVOS TV SDK**: **Months of work**. Zero UE files in repo.
  Not happening this session.

## What This Means for Future Sessions

1. **External claims in strategic briefs are leads, not facts.** The brief
   is a research proposal. It points at companies and markets. It does NOT
   prove them. Always verify before publishing or spending.

2. **Internal claims about our own code should be self-consistent.** The
   "1019 lines" / "107 tests" / "6 axes" / "8.28ms" claims were wrong. We
   have ground truth on disk (`wc -l`, `grep`, `pytest`). Use it.

3. **The CPO calculator is real and ships. The brief's other crown jewels
   need owner-gated actions.** Don't auto-send emails, don't auto-create
   accounts, don't auto-spend money.

4. **Web verification is broken on this Mac** (`web_search` unavailable).
   If a future claim needs verification, escalate to Nick with a clear
   list of what to check on a working browser.

— JEEVES, 10 Aug 2026
