# Error Statistics Format (v1, 2026-08-15)

Adapted from: NRSRO Exhibit 1 (transition-and-default matrices) + IOSCO
annual independent assurance. **The self-published error stats are the
credibility moat** — a measurement body that publishes its own error rate is
one you can trust.

## The published metrics (aggregated from the ledger, per family)

| Metric | Definition | Why it matters |
|---|---|---|
| **Revocation rate** | revoked cards / cards issued (per period) | Honest account of failures |
| **Correction rate** | superseded-or-corrected cards / cards issued | Process accountability |
| **Drift rate** | cards whose claims diverged from re-measurement beyond CI bounds | The re-attestation signal |
| **Dispute outcomes** | upheld / corrected / rejected / pending | Due-process transparency |
| **Verifier success** | verifications that passed / total verifications attempted | Ecosystem trust reach |

## Publication format (machine-readable)

```json
{
  "period": "2026-Q3",
  "family": "gspc-board",
  "cards_issued": 421,
  "revoked": 2,
  "revocation_rate": 0.0047,
  "corrected": 5,
  "correction_rate": 0.0119,
  "drifted": 1,
  "drift_rate": 0.0024,
  "disputes": {"filed": 3, "upheld": 0, "rejected": 2, "open": 1},
  "verifications": {"attempted": 4122, "passed": 4111, "failed": 11}
}
```

The JSON is signed (Ed25519) and posted to the public register — same
discipline as cards.

## Cadence

- **Quarterly**: full error statistics
- **Monthly**: availability + index timeliness (status page)
- **Annual**: the full Transparency Report (measurements, revocations,
  disputes, funding sources — Cloudflare/GitHub cadence)

## The honest rule

Mixed news is the trust signal — GitHub's monthly availability reports keep
publishing missed targets, and that candor is WHY they're believed. We report
our own errors before anyone else can report them for us.