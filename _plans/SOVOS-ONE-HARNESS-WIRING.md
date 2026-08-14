# SOVOS — one harness, one SOV signal (wiring plan)

**Goal:** every measurement piece wired into ONE spine so the SOV signal is real, fresh, signed,
and externally verifiable. **The reconciliation** ("all inside SOVOS" vs "layer-not-monorepo"):
monorepo the **measurement** pieces INTO the neutral spine; keep client / fix / payment code
(CobolBridge, Stripe, x402 billing) as SEPARATE verticals that *consume* the spine. Folding a
fix/seller into the neutral core poisons neutrality — the one asset every market buys.

```
                        ┌──────────────  THE NEUTRAL SPINE (monorepo this)  ──────────────┐
   corpus-watch ──drift──▶ gspc_flywheel + fix_loop ──▶ citation_verify.verdict ──▶ sign.py /
   (EU AI Act CELLAR,      (measure + self-improve)      (CORRECTNESS GATE ✅ done)     card_issuer
    UK statute; fail-                                                                    (Ed25519 +
    closed)                                                                              timestamp)
                                        │                                                    │
                                        ▼                                                    ▼
                              aggregate_sov_signal  ◀───────────────────────────────  signed 3KB cards
                              (THE SOV SIGNAL — index of measured governance)          (externally verifiable)
   └───────────────────────────────────────────────────────────────────────────────────────────────┘
        ▲ consume, never merge ▲
   ┌────┴─────────┬──────────────┬───────────────┬─────────────────┬──────────────────┐
   crosswalk-mcp  ai-bom-mcp     injection-       watermark-attest  compliance-gateway  CobolBridge
   (→frameworks,   (supply-chain  scanner         (Art 50 mark)     (AWS/Azure/Smithery (COBOL fix —
    M2 evidence pack) provenance)  (agent security)                   + x402 pay)         SEPARATE)
```

## Status of the 4 missing pieces
| # | Piece | State | Gate |
|---|-------|-------|------|
| 1 | **Correctness gate** (3-state verdict) | ✅ **DONE** — built, tested, committed `31387e03` | none (in-lane) |
| 2 | **Externally-verifiable signer** | **Issuance WIRED** — real card via MeasureService → MinIO, content_id recomputed off-box & matched (moat gap closed, demo-able). Remaining: signer *identity* still resolves "unknown" externally | split |
| 3 | **GSPC-as-A2A-skill** | Not wired — `sovos-a2a-swarm` is surface only | none (in-lane) |
| 4 | **Real timestamping** | Aspirational — "OTS Bitcoin proof" is ~1 code ref | none (in-lane) |

## Build order (in-lane first, gated flagged)
1. **✅ Correctness gate** — done. Every SOV-signal input now passes the gate; ungrounded ≠ verified.
2. **GSPC-as-A2A-skill** *(in-lane)* — wrap `gspc_flywheel.measure` as an A2A skill + MCP tool:
   agent presents its card → live-measured on the axes → `card_issuer` signs a **measurement**
   credential (never "certified") it carries into the A2A directory. Grabs the empty signed-card slot.
3. **Real timestamping** *(in-lane)* — add an RFC-3161 TSA / OpenTimestamps anchor to `card_issuer`
   so every card carries a verifiable time proof. Kills the aspirational "OTS" claim; strengthens
   every card. Then delete the OTS overclaim from the CobolBridge charter.
4. **corpus-watch → re-measure trigger** *(in-lane)* — a drift event (statute changed) triggers a
   re-measure + re-sign, so the SOV signal has a freshness guarantee, not a stale snapshot.
5. **crosswalk-mcp evidence pack** *(in-lane)* — GSPC board → crosswalk (5,013 LOC; maps to
   regulatory frameworks — note only 4 framework control-sets are on disk today, the "~30" is a
   named target, not evidenced) → signed **EU AI Act evidence pack**. The showable M2 artifact
   (`evidence_pack.py`, built; covers the 6 mandated EU AI Act obligations).
6. **ai-bom + injection-scanner as axis inputs** *(in-lane)* — fold supply-chain provenance and
   agent-security into the board so the SOV signal covers them.
7. **Externally-verifiable signer** *(SPLIT)* — in-lane: embed pubkey in every card + one-command
   `csoai verify`. **GATED (owner/counsel/cost):** C2PA trust-list membership / a recognised CA so
   verifiers report the signer as *known*.
8. **compliance-gateway + x402** *(GATED — deploy + payments)* — the go-to-market/monetization rail.

## Hard firewalls (do not cross without counsel)
- **Measurement, not certification.** Never "certified/compliant" — only "measured". The A2A card
  is a *measurement credential*. CobolBridge's charter "we certify"/"CMKC"/"ISO fee-for-service"
  language must be scrubbed before any public surface uses it.
- **Do not call the SOV signal an "index"/"benchmark" publicly** until the IOSCO / EU Benchmark
  Regulation boundary is legally scoped (dated exposure, owner+counsel gate).
- **Layer-protocol, not mono-repo of the fix.** CobolBridge/client/payment code stays a separate
  consumer. Mine its 49GB data moat; never merge its seller code into the neutral spine.
- **The 49GB data moat grounds correctness** — wire it as the retrieval corpus behind the gate, so
  "grounded" means grounded against real statute text, not just the hand-checked registry.
- **affect stays DRAFT / UNMEASURED** until Sep 11 + one owner word (27a06946 was a lane flip, not a
  sign-off). Do not let any lane re-flip it.
- **Keep improvement DIRECTIONAL.** fix_loop now runs an even/odd holdout and `flywheel.selftest()`
  is 19/19 on the pod — the loop gates both ways and memorization is engineered out — but the
  magnitude stays "directional (~+1 pt)". Do not upgrade the number in any public surface.
