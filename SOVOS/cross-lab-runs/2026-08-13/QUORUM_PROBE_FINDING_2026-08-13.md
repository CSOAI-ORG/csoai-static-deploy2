# QUORUM PROBE — BFTQuorum verification finding (2026-08-13)

**Result: FALSIFIED — `BFTQuorum` does not provide the Byzantine fault tolerance it claims.**

## What was probed
`sovos-world/src/sovos_world/bft_quorum.py` (143 lines) — a "Byzantine Fault Tolerant" cross-clan voting module, the one domain the estate flagged as **under-verified**. Both documented code paths were probed with their exact schemas:

1. `vote()` — `swarm_results {family: {best: {confidence, counter_strategy:{primary}, strengths, weaknesses}}}`
2. `vote_from_cspace()` — `master_cspace {clan_contributions: {clan: {total_confidence, count}}}`

## What the probe did
For **each** path, ran a coherent 5-clan vote AND a canary-run with one injected **rogue** clan scoring `confidence: 0.99` with a divergent strategy ("rogue-flip").

## Honest findings
| Path | Coherent vote | Rogue injected | Rogue captured? |
|---|---|---|---|
| `vote()` | quorum_reached **true** | quorum_reached **true** | **YES** — winning_strategy stays coherent, but rogue is in alliance |
| `vote_from_cspace()` | quorum_reached **true** | quorum_reached **true** | **YES** — rogue (conf 0.99) becomes top-weighted |

**The module does not implement Byzantine Fault Tolerance.** `quorum_reached = best["confidence"] >= threshold` — it is a **single-candidate confidence check**, not a supermajority of independent agreement. A rogue voter that reports high confidence captures the decision. There is no `(2/3)+1` vote-count, no leader-equivocation handling, no accountability for faulty voters.

## Why this matters
- The docstring and threshold comment ("BFT threshold (2/3 + 1)") overclaim. It is **maximum-confidence selection**, not BFT quorum.
- Any downstream that treats `quorum_reached=True` as "consensus among N independent voters" (§-level strategies, the 29-voter/200-voter council framing) inherits a **false safety guarantee**.

## Recommended fix (not applied — this is a finding, not a change without owner nod)
Two honest options:
1. **Rename to `MaxConfidenceVote` / `WeightedVote`** — honest about what it does (single-dimension selection), or
2. **Actually implement BFT**: require a genuine `(2/3)+1` of voters to agree on the winning strategy (group by strategy, sum weights, enforce 2/3 supermajority), and treat divergent/rogue voters as faults.

## Evidence
Signed probe: `benchmark-results/quorum_probe/quorum_probe_v2_20260813_*.json` (Ed25519, A100 key).
- Path 1: honest_consensus true, with_rogue_captured true
- Path 2: honest_consensus true, with_rogue_captured true

One probe caveat: I fed a *synthetic* coherent vote; this proves the threshold logic is structural, not a specific-input artifact.

---

*This is the value of the quotable probe: the domain WAS under-verified, and the probe replaced "it exists" with "it does not do what it claims."*