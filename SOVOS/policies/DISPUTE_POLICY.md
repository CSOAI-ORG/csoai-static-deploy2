# Dispute / Appeal Policy (v1, 2026-08-15)

Adapted from: NRSRO bounded appeal (S&P/Fitch rating-committee dissent rules).

## Principles

1. The measured org gets a **fact-check window** before public index
   publication (48h for card-level: factual errors only, not preference).
2. **Appeal only on new evidence or material misinterpretation** — not on
   "we don't like the result."
3. **Appeal is bounded**: delay-tactic appeals are rejected.
4. **Watch status** during appeal: the card shows `status: watch`, stays
   published, and downstream citation continues (no deletion).
5. **Decision is final** after review; the decision memo is public.

## Flow

```
Dispute filed (measured org, within N days of publication)
    │
    ▼
Fact-check window (48h): org may correct factual errors
    │
    ▼
Watch status set; independent review (>= 2 scorer configurations concur,
dissent => automatic re-run with fresh config — the committee rule)
    │
    ▼
Decision: uphold / correct / revoke
    │
    ▼
Decision memo published; card updated (superseding entry, never silent rewrite)
```

## The committee rule (high-stakes cards)

For cards above a risk tier: card issues only when **>=2 independent scorer
configurations concur**. Dissent triggers an automatic re-run with a fresh
configuration — mirroring Fitch's mandatory appeal with a new committee.

## What we never accept

- An appeal that is actually a request to improve a result ("re-measure until
  we pass")
- An appeal on grounds of commercial damage without new evidence
- An anonymous appeal (except through the confidential self-report intake —
  NASA-ASRS pattern — which has its own cure window, not an appeal)