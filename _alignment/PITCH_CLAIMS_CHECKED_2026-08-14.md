# CSOAI pitch — claims-checked (canonical; supersedes prior decks)

**Rule:** every claim below is tagged and traceable. Do not restate a claim in a deck, site,
card, or model card in a stronger form than its tag here. The counter-canon gate
(`check_counters.py`) now enforces the worst offenders in CI — a deck that overclaims and a gate
that blocks overclaims cannot both ship.

Legend: ✅ VERIFIED (code/artifact ref) · ⚠️ HONEST-FORM (was overclaimed; use this wording) ·
🚧 ROADMAP (not built — say "planned") · ❓ UNVERIFIED (do not use until grounded)

---

## What we are
- ✅ **A measurement body, not a certifier.** We measure; we never certify or issue certificates.
  (`sov_whole.py`, site firewall; enforced by the "measurement not certification" discipline.)
- ✅ **Deterministic — 0 models in the verdict path.** Grading is rule-based; results recompute
  bit-for-bit. (`gspc_flywheel.py` — no judge model.)
- ✅ **Signed, content-verifiable cards.** Every measurement is Ed25519-signed; anyone recomputes
  the `content_id` and confirms it offline. (`measure_api.MeasureService.verify`, `card_issuer.py`.)
- ✅ **RFC-3161 time-anchored.** Real third-party timestamp token (verified live: 6,180 B from a
  public TSA). (`sov_timestamp.py`.)
- ⚠️ **"Verify without trusting us" — content only, today.** The card *content* verifies offline.
  The **signer identity still resolves as unknown** to an outside verifier (private root). Say:
  *"content-verifiable today; signer-identity attestation via a recognised CA is in progress."*
  (Owner-gate console item; C2PA conformance → CA.)

## What we measure
- ⚠️ **9 axes, not 14.** governance, safety, provenance, continuity, conformance, openness, care,
  mach, art5. (`gspc_flywheel.AXES` — literally 9.) Never say "14 dimensions."
- ✅ **UNMEASURED is first-class.** An axis we can't measure is reported UNMEASURED, never 0.
- ⚠️ **Model count — publish the measured number, do not claim 19.** The gate marks "19 signed
  agents" unevidenced (largest registry export holds 7). Say the count the registry actually shows.
- ⚠️ **Frameworks — 4 control-sets on disk, not 30.** The crosswalk *names* ~30; only 4 have
  control-sets. Gate blocks "30 frameworks." Say *"crosswalk maps to EU AI Act, NIST, ISO 42001,
  DORA … (4 control-sets on disk today; more in progress)."*

## The spine (all built + tested this session)
- ✅ **Correctness gate** — a wrong answer cannot carry a clean receipt; ungrounded ≠ verified.
  (`citation_verify.verdict`, `correctness_gate.py`, wired in `sov_whole` + `measure_api._emit_card`.)
- ✅ **Drift-triggered re-attestation** — regulation change → stale cards → re-measure queue,
  fail-closed on UNKNOWN. (`drift_reattest.py` + `corpus-watch`.)
- ✅ **A2A measurement skill** — agent presents a target → live-measured → signed *measurement
  credential* (never a certificate). (`GSPCMeasureAgent`.)
- ✅ **Self-improving loop** — gates on held-out generalisation; has reverted its own overfits.
  Keep the magnitude **directional (~+1 pt)** — do not upgrade. (`fix_loop.py`.)

## Post-quantum (the correction that matters most)
- ⚠️ **We MEASURE PQC migration-readiness; we do NOT sign with ML-DSA-65.** 0 ML-DSA sign calls in
  the codebase; signatures are Ed25519. Say: *"PQCBench — the neutral score of whether a signing
  chain survives a PQC migration, honest enough to fail our own chain first."* That is a real,
  unique wedge. **Never** say "we already sign with ML-DSA-65." (`pqcbench.py`.)
- 🚧 **ML-DSA-65 signing** — roadmap. COSE identifiers referenced; no ML-DSA signer built.

## Provenance / identity plumbing
- ⚠️ **SCITT** — partial (3 files reference it); not an end-to-end transparency-receipt flow yet.
- 🚧 **COSE Sign1 signed statements** — not built (0 files). Roadmap.
- 🚧 **did:web identity** — not built (0 files). Roadmap.

## The commercial thesis
- ✅ **The gap is real:** the indices (Anthropic Economic Index, OECD.AI, Stanford HAI) made their
  data *callable* via MCP but not *verifiable/signed*. We can wrap any MCP index output in a
  signed, time-anchored, drift-bound card. **This is the sellable protocol.** (Built next: `sign_mcp_output.py`.)
- ✅ **Three deadline-driven buyers** — AI-liability underwriting (score the underwriter prices
  against), PQC migration-readiness (the neutral score), A2A agent-card measurement (fill the empty
  signed-slot). All reachable with the spine.
- ⚠️ **Business-model analogies (MSCI, "95% recurring, 56% margin", "index")** — do NOT publish the
  word "index"/"benchmark" for the SOV signal until the IOSCO / EU-BMR boundary is legally scoped
  (owner-gate). Internally fine; publicly gated.

## Do-not-use-until-grounded
- ❓ **J-Space / Poincaré / Procrustes "signed distance index", "10/10, 8/8 on hardware"** — not
  verified that the geometric code emits a *signed* distance or that those pass-counts are current.
  Ground it (does `Procrustes`/`Fisher-Rao` code produce a signed artifact?) before any pitch use.

## The moat, stated truthfully
Neutrality (we measure, never fix or certify) · **self-refutation** (we publish our own resolution
limits — the one thing a regulator trusts) · **content-verifiable signatures** (an underwriter can
check a score without trusting us — with the signer-identity CA caveat above). All three are real
today except the CA leg, which is in progress and stated as such.
