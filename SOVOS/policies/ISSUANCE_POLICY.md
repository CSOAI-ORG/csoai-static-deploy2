# Issuance Policy — when a card may be issued (v1, 2026-08-15)

Adapted from: NYSE continued-listing standards + ISO/IEC 17025 scope discipline.

## The issuance bar (all must hold)

1. **Measured on a named axis set** — the card lists exactly which axes,
   which probes, which model version, which date range. Outside scope is
   unmeasured, full stop.
2. **usable_n >= 30** per quoted cell (or an explicit UNMEASURED marker).
3. **Quotable quotient** — every public number carries its Wilson 95% CI.
4. **No transport error / no unparsed row** in the underlying run.
5. **Signed + time-anchored** — Ed25519 signature and a transparency anchor
   (OpenTimestamps / SCITT receipt) per card.
6. **Not infra-tainted** — the run's artifacts (GGUF, weights, harness) are
   verified clean; the `?????` signature is recorded as a revoked artifact
   class, not silently re-labeled.
7. **In-scope** — the card's method is within published methodology. Work
   outside the scope block cannot be represented as issued.

## Scope-of-accreditation discipline (17025 analog)

Every card carries an explicit **scope block**:

```json
"scope": {
  "axes": ["gov","prv","mcp","jail"],
  "probeset": "board_v2@2026-08-01",
  "model": "qwen2.5:0.5b-instruct",
  "valid_from": "2026-08-01T00:00:00Z",
  "valid_to": "2026-08-31T23:59:59Z"
}
```

Anything outside scope is **UNMEASURED**, never zero, never implied.

## Continued-listing (attestation) bar

For an org/model to KEEP quoted cards, it must pass the continuing bar:

- Re-attestation on a published cadence (quarterly for quoted models)
- No unremedied deficiency notice
- No un-disclosed weights/lab update since last attestation
- (Anomaly ladder: see REVOCATION_LADDER.md)

## The honest marker

Every card prints: **"verified measurement credential"** — per ISO CASCO,
we are a measurement/attestation body, not a certification body. The word
"certified" never appears on an issued card.