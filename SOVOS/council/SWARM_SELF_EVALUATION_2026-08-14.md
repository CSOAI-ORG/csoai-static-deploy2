# Council self-evaluation against the gspc-swarm protocol bank

The estate measuring its own council. Every answer is derived from the code as
committed (wave8, `SOVOS/council/`), not from intent. Runtime properties not yet
exercised are marked UNMEASURED — the doctrine's word, not a euphemism.

Format: swarm-id — answer — evidence.

- swarm-001 fault_tolerance (f crashes) — **HOLDS (design)** — quorum 2-of-3 completes with one crashed voter; abstain path is code, tested in selftest.
- swarm-002 convergence — **HOLDS** — no iterative protocol; one collection pass terminates by construction.
- swarm-007 byzantine_tolerance — **HOLDS for 1 adversarial voter, given 2 honest + trusted collector** — 2-of-3 outvotes one bad vote. NOT claimed beyond that; two colluding voters defeat it (stated in README).
- swarm-008 sybil_resistance — **PARTIAL** — voters are identified by implementation+host string, not cryptographic identity. Sybil resistance awaits per-pod Ed25519 lane DIDs (v2). Stated as the known gap.
- swarm-009 quorum_integrity — **ENFORCED by the collector** (`promotion_council.py decide()`), not by distributed protocol. The collector is trusted — stated.
- swarm-010 liveness — **HOLDS** — abstaining voters never block a decision; quorum counts non-abstaining votes.
- swarm-011 partition_tolerance — **N/A by design** — centralized collection means no voter-to-voter network; documented as the deliberate simplification, not overlooked.
- swarm-012 auditability — **REPLAYABLE** — every vote carries `rows_sha256`; rows are re-graded by anyone with the frozen probes; the certificate is signed and verifiable offline.
- swarm-013 message_provenance — **PARTIAL** — votes hash-committed at source, signed at collection. Full per-voter signatures = v2 (lane DIDs).
- swarm-014 replay_resistance — **HOLDS** — each run is timestamped and content-hashed; a replayed old verdict carries a stale rows hash that won't match the candidate under evaluation.
- swarm-015 identity_attestation — **PARTIAL** — implementation + host attested in each verdict; not yet a hardware/code attestation.
- swarm-016 disagreement_logging — **PRESERVED** — ALL votes ride in the certificate, including dissent and abstention, with per-voter deltas.
- swarm-021 human_escalation — **DECLARED** — a REJECTED certificate halts promotion; the human reads it. The stop is the default.
- swarm-026 graceful_degradation — **REFUSES** — below quorum the council issues REJECTED, never a reduced-confidence promotion.
- swarm-030 unmeasured_disclosure — **DISCLOSED** — this document is the practice: PARTIAL and UNMEASURED appear wherever the code doesn't yet prove the property.

Remaining items (003–006, 017–020, 022–025, 027–029): **UNMEASURED** — they
describe runtime adversarial exercises (fork handling, leader censoring,
collusion measurement, rollback under attack) that require a live multi-cycle
council history. They become measured when the council has run enough cycles to
attack honestly.

Verdict: the council as built satisfies the safety-critical swarm properties by
construction, declares its two real gaps (Sybil identity, per-voter signatures),
and marks everything unexercised UNMEASURED. It would not pass a hostile reading
that required v2 features — and it says so on its face.
