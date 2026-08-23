# cobol-a2a-bridge-mcp

The atomic unit (Open 1) — **the Rosetta stone** between COBOL legacy (fed state:
batch, high-entropy, T+2) and A2A agents (fasted state: stream, low-entropy, T+0).
EUNOMIA is the metabolic boundary. This wraps COBOL — it never replaces it.

> Measurement, not certification. Every attestation is Ed25519-signed,
> RFC 9943 (SCITT)-aligned COSE receipt, chain-linked, `not_a_certification:true`.

## The parasitic symbiosis
```
COBOL MAINFRAME (honey)              EUNOMIA WRAPPER (water-pipe)        A2A AGENT LAYER (steam)
│  batch job runs 11pm               │  reads batch output to disk        │  verified, attested, scored
│  → 50,000 settlement instructions  │  → C2PA attestation in real-time   │  → negotiate in milliseconds
│                                    │  → COBOL user-id → DID mapping      │  → smart contract T+0 DvP
```

## Structure
```
cobol-a2a-bridge-mcp
├── parsers/           COBOL COPYBOOK → JSON schema (copybook_schema.py)
├── attestations/      C2PA / Ed25519 attestation generation (c2pa_attest.py)
├── identity/          mainframe user-id → DID mapping (did_mapping.py)
├── compliance/        ISO 42001 + EU AI Act probe for batch jobs (iso42001_probe.py)
└── tests/             live COBOL test environment
```

## Fit (one engine-axis)
- parse the COPYBOOK (schema) → the batch becomes a routable `eunomia://bridge/<proto>` object
- attest it (C2PA) → the overnight report becomes a real-time signed attestation
- map the identity (DID) → permissionless trust, no 10-year relationship
- probe compliance (ISO 42001 + EU AI Act + the regime crosswalk) → one signed card

## Route
Every bridge is resolvable on the live router:
```
eunomia://bridge/cobol        → cobolbridge.ai
eunomia://bridge/cics         → cics-bridge-mcp   (SOX + PCI-DSS + DORA)
eunomia://bridge/iso20022     → iso20022-bridge-mcp (PSD2 + DORA + AML)
eunomia://a2a/batch-job       → bft-progress-council-mcp
```
