# Confidential Self-Report Intake (v1, 2026-08-15)

**The NASA ASRS pattern applied to measurement.** A measured org can
self-report a card error within N days and get CORRECTION (not revocation),
with the intake run under third-party custody if volume ever justifies it.

## The problem it solves

Punitive channels provably suppress data. If a measured org's only option
when it finds a card error is to dispute publicly, it will hide errors. The
confidential intake fixes the incentive: report early, get correction; hide,
get caught by surveillance later (worse).

## The rule (ASRS 10-day analog)

1. A measured org (or attestor) self-reports a card error within **10 days**
   of learning of it.
2. If inadvertent + non-criminal (fabrication is NEVER eligible) + no
   third-party harm claim pending:
   → the error is **corrected** (superseding entry), not revoked
   → reported as `correction` in error stats (the credibility moat — mixed
     news is the trust signal)
   → no immediate enforcement action from THIS report alone
3. Eligibility bar (NASA analog): the self-report must be submitted within
   the window; deliberate concealment discovered later is a revocation
   trigger, not a correction.

## What the intake looks like

```
report (signed, but custody-isolated)
    │
    ▼
intake review (CISO seat)
    │
    ├─ eligible → correction path (supersede card, COAI advisory, stats)
    │
    └─ ineligible → escalate to revocation ladder (normal due process)
```

## Custody

- At current volume, the intake is a signed intake file into the ledger
  (the report is kept; the reporter's identity is separated and
  access-controlled)
- If volume justifies it: the intake is administered by a third party (e.g.
  an auditor or a university) — NASA runs ASRS, not the FAA, precisely so
  the FAA never sees identities

## What never converts into a self-report

- Fabricated measurement
- Collusion rings
- Key compromise
These are immediate-revocation triggers (REVOCATION_LADDER.md), always.

## The honest framing for partners

"We'd rather you tell us a card is wrong than find out later. Report within
10 days, we correct it publicly (superseded entry — here's the advisory),
and it's counted as a correction — which is exactly what our error stats
show. The data is more valuable than the score.