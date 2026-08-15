# Methodology Change + Cessation Policy (v1, 2026-08-15)

Adapted from: IOSCO Benchmark Principles + EU BMR (2016/1011) + FTSE Russell
rebalance consultations.

## Why this exists

No one trusts a benchmark that can change arbitrarily or that can't say how it
dies. BMR/IOSCO discipline (consultation, error policy, cessation policy) is
what separates a *benchmark* from a *leaderboard*. The bright line stays:
**"research statistic, not for use as a financial benchmark"** on every card
until this governance file is real — and now it is.

## Methodology changes

1. **Advance public consultation** — any material methodology change
   (axis definitions, probe sets, scoring rules, index construction) is
   announced with a comment window (minimum 30 days) BEFORE change.
2. **Change log** — the methodology is versioned; every change is a dated,
   signed entry in `METHODOLOGY_CHANGELOG.md`.
3. **Transition** — cards issued under the old method remain valid under
   their own scope block until natural expiry (ISO 20022-style coexistence
   windows; reject-on-invalid validation in the verifier).
4. **Impact notice** — every card family potentially affected gets a
   machine-readable notice 14 days before the change lands.

## Error policy

1. On a discovered error, the artifact is **superseded** by a compensating
   signed entry — never silently rewritten.
2. The correction gets a citable ID (`COAI-2026-NNNN`).
3. Error statistics are published per ERROR_STATISTICS_FORMAT.md.

## Cessation policy (a benchmark must say how it dies)

1. The index/methodology has a named **administrator of last resort**.
2. **Cessation triggers** (pre-committed):
   - Funder termination without successor within 90 days
   - Loss of measurement fabric (no fresh data) for 2 consecutive index cycles
   - Regulatory order (if ever applicable)
3. On cessation: 6-month public wind-down notice; final archive (raw
   measurements + cards + index history) exported to Zenodo + Software
   Heritage; the index's last value published with a `ceased` marker and a
   pointer to the archive.
4. **No silent vanishing.** Users must be able to plan around the end.

## Consultation calendar

The index methodology-change calendar is public and pre-committed (fast-entry
rule for major model launches: a GPT-6-class launch enters the index within a
pre-committed N days).