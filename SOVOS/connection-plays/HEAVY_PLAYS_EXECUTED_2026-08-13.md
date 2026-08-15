# HEAVY PLAYS EXECUTED — OSCAL + Crosswalk + ProvBench, real runs on the A100 (2026-08-13)

Owner directive: "point the plays at their real execution — run anything heavy
on the pod." All three executed against real data, not stubs.

## 1. OSCAL exporter — REAL export (FedRAMP signature-gap play)
- Executed `sovos-oscal` against the **verified ProvBench measurement**
  (18/105 survival, rate 0.1714 from `benchmark-results/provbench-15asset-2026-07-30.json`).
- Emitted a **genuine OSCAL v1.1.0** assessment-results document:
  - path `evidence/harness/oscal/provbench-oscar.json` (3,895 bytes)
  - chain-id `372de11c8752ac1aca0ebdef`
  - 2 findings (1 satisfied / 1 not-satisfied), OSCAL version 1.1.0
  - honest: survival 17.1% < 30% floor → `is_permitted = false` (reports
    "not adequate," does not claim otherwise)
- Applies to: the OSCAL signature-gap / FedRAMP RFC-0024 30-Sep-2026 play — a
  real OSCAL artifact, not a stub. (Note: this is a measurement export; the
  Ed25519 receipt wiring to it is the next layer.)

## 2. DSIT crosswalk — REAL execution
- `sovos-crosswalk` ran (12/12 tests) + live assess:
  - **26 EU-AI-Atlas rows** crosswalked against **ISO-42001 / NIST-AI-RMF**
  - `iso_shared_ratio 0.6923`, `vendor_shared_ratio 0.3846`
  - `iso_obstructed 4`, `vendor_obstructed 8`
  - `align_cost_eu_iso 0.3077`
- Applies to: the DSIT £11m bid + the EU-AI compliance crosswalk — real
  obstruction/alignment numbers, not theory.

## 3. ProvBench reframe — real anchor
- Verified from disk: 18/105 = 17.14% survival, CI present, 15 assets × 7
  transforms, PQ COSE-ML-DSA-65 binding.
- The wedge preprint (`SOVOS/preprints/PROVBENCH_WEDGE_2026-08-13.md`) is the
  reframe; the OSCAL export above now gives it a machine-readable companion.

## Honesty register
- **REAL:** OSCAL 1.1.0 export from verified data; crosswalk obstruction/align
  numbers; 18/105 survival with CI.
- **THEORY/not-run:** a *third-party* live model-vs-model sandbox duel (the
  seam runs local/contained only); FedRAMP certification itself (authority
  stays with FedRAMP); DSIT award likelihood. No overclaim.
