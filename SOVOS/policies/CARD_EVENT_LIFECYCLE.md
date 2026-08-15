# Card-Event Lifecycle Schema — the registry's Consolidated Audit Trail (v1, 2026-08-15)

Adapted from: SEC Rule 613 Consolidated Audit Trail (full lifecycle logging,
stable IDs, replayable) + DTC corporate actions processing.

## The event types

| Event | Meaning | Emitter |
|---|---|---|
| `card.issued` | Card created, signed, time-anchored | measurement pipeline |
| `card.verified` | External verifier confirmed digest+signature | verify endpoint / csoai_verify.py |
| `card.re_attested` | Re-measurement confirmed the claim still holds | re-attestation cron |
| `card.watch` | Dispute filed or drift detected; stays published | dispute intake |
| `card.corrected` | Superseding entry (never silent rewrite) | correction step |
| `card.suspended` | Family suspended pending cure | revocation ladder step 3 |
| `card.revoked` | Revoked but RETAINED, marked revoked | ladder step 4/immediate |
| `card.ceased` | Index/methodology cessation | cessation policy |

## Event schema (machine-readable, signed)

```json
{
  "event": "card.revoked",
  "card_id": "COAI-2026-0017",
  "family": "gspc-jail",
  "ts": "2026-08-15T14:02:11.000Z",
  "actor": "CISO",
  "reason_ref": "COAI-2026-0003",
  "payload_hash": "sha256:...",
  "supersedes": null,
  "signature": "ed25519:...",
  "anchor": "ots:...|scitt:..."
}
```

## Append-only + replayable

- Every event appends to the lifecycle log (JSONL in the public register repo)
- Stable IDs (`COAI-YYYY-NNNN`) — IDs make corrections citable
- Sync-synced timestamps (UTC ISO-8601)
- Derived views (per-card timeline, per-family stats) are recomputed from the
  log — the log is truth, views are derived
- EOD close: a signed end-of-day root hash over the day's events (daily
  reconciliation analog)

## The invariants

1. **No deletion.** A revoked card stays in the log and the register, marked
   revoked, linked to its revocation notice.
2. **No silent rewrites.** Corrections are new events with `supersedes`
   pointers; the original event remains.
3. **Reconciliation.** Registry ledger vs public verify API vs transparency
   log must agree; unresolved breaks stop index publication.