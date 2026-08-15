# Advisories — corrections, revocations, anomaly notices (v1, 2026-08-15)

**CVE-style citable IDs for measurement findings.** IDs make corrections
citable — cheap and compounding (pattern: AI Incident Database sequential
IDs 1→746+; OSV JSON schema).

## ID scheme

`COAI-2026-NNNN` — sequential, per-year, never reused.

## Advisory types

| Type | Trigger | Schema base |
|---|---|---|
| `correction` | A published card was superseded (error, drift) | OSV JSON shape |
| `revocation` | Revocation ladder step 4 or immediate | OSV + REVOCATION_LADDER |
| `anomaly` | Surveillance hit (drift ring, key exposure) | OSV + event refs |
| `security` | Security finding from VDP program | OSV + GHSA shape |

## File layout

```
advisories/
├── README.md             (this file)
├── COAI-2026-0001.json   (signed advisory)
└── COAI-2026-0001.md     (human-readable companion)
```

## OSV-style shape (JSON)

```json
{
  "schema_version": "1.4.0",
  "id": "COAI-2026-0001",
  "summary": "Card COAI-2026-0001 superseded — probe-set drift",
  "details": "...",
  "affected": [{"card": "COAI-2026-0001", "family": "gspc-jail"}],
  "date_published": "2026-08-15T12:00:00Z",
  "digest": "...",
  "signature": "..."
}
```

## Rules

- Every advisory is signed (Ed25519, estate spine)
- Every advisory maps to a ledger event (`card.revoked`, `card.corrected`)
- Revoked cards STAY in the register, marked revoked — never deleted
- Advisories are part of the error statistics: the metric counts the
  corrections we published ourselves before anyone else could

## Sign-off

CISO seat reviews; CEO approves; the advisory is a signed commit in the
public advisories repo.