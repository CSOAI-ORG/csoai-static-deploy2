# Attestor / Delegated-Measurement Program (v1, 2026-08-15)

**The FAA ODA → Lloyd's coverholder pattern applied to AI measurement.**
An institution signs ITS OWN framework with ITS OWN Ed25519 key against OUR
13-axis methodology; we operate the rails: the canonical method, the
transparency ledger, and the oversight/audit. This is how one tiny referee
scales trust across thousands of entities **without becoming a player** in
the market they measure.

## The delegation mechanic (cryptographic FAA ODA)

| FAA ODA element | Our analog |
|---|---|
| Signed procedures manual | Attestor signs the published methodology + scope + liability wording |
| Scoped grant (organizations, not blanket endorsement) | Grant = limited axis-scope + probe-set + model-version + validity window |
| Dedicated oversight (annual assessment + 2-yr inspection) | Annual re-attestation review; ad-hoc spot re-measurement without notice |
| Bounded: ODA cannot issue an original type certificate | Self-signing attestor CANNOT mint the method, confer standing, or alter the axes |
| Certificate holders have an affirmative duty to report (21.3) | Attestor has a re-attestation duty + anomaly self-report within N days |

## What an attestor gets

1. **Their own signing key** (we never hold it — Firewall 1)
2. **A scoped grant** document (machine-readable, signed)
3. **The rails**: methodology spec, card schema, reference implementation,
   transparency-service endpoints
4. **Public registry listing** — verified-measurement credential, not a
   certification claim
5. **Surveillance economics** option: their re-attestation feed becomes
   procurement evidence (Reliance tooling)

## What the Council gets

- **Scale without hiring** — each attestor extends verification reach
- **A cited reference** — their cards reference OUR method (the citation
  flywheel)
- **Re-attestation revenue** — recurring verification infra, never a score
- **The ODA-style oversight game** — we audit the attestors, they audit
  nothing for us (the grader role)

## Attestor lifecycle

```
1. Application → scope request (axes, models, region, use-case)
2. Authorisation → signed procedures manual + granted scope + Ed25519 key
   registration (their key, their identity)
3. First issuance → reference re-run, spot-checked by us (committee rule)
4. Surveillance → monthly signed data report (bordereaux-style); escalation
   = more frequent reporting before suspension
5. Annual review → business plan vs filed measurement plan; under-performers
   lose scope (Lloyd's PMD / Decile-10 exit pattern)
6. Exit → clean wind-down; retained history; no deletion
```

## Scope-bounded grant example

```json
{
  "attestor_id": "att-2026-0001",
  "scope": {
    "axes": ["gov","prv","mcp"],
    "probeset": "board_v2@2026-08-01",
    "model_family_limits": ["qwen*","llama*"],
    "valid_from": "2026-09-01",
    "valid_to": "2027-08-31"
  },
  "grants": [
    "self-sign their own measurement cards per methodology v4",
    "reference the Council methodology in their card metadata"
  ],
  "forbidden": [
    "certify or endorse any model (Firewall 1)",
    "alter the axes or scoring method (delegation is bounded)",
    "train a champion on their collected data (Firewall 2)"
  ]
}
```

## The bordereaux
Monthly signed data report (escalation = weekly): cards issued, corrections,
disputes, authorisation breaches. The reporting frequency itself is the
early-warning sanction.

## Why this is the revenue unlock

The attestor program is what design partners ask for when they mean
"give us your measurement rails." It's the same deal as the runways in sign
your own framework (the free wedge) turned into a structured, payable,
recurring program. It also directly misstages us for the Workday Agent
Passport + AI Verify + insurance-evidence plays (the DO moves 68-73).