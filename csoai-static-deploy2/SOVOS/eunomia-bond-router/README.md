# eunomia-bond-router

The **Venturi throat** that turns the $130T COBOL bond market into A2A flow.
One repo today. Not five. The proof of weave.

> Measurement, not certification. Every routed object is Ed25519-signed,
> RFC 9943 (SCITT)-aligned COSE receipt, chain-linked, `not_a_certification:true`.

## The one-paragraph thesis
Banks spent ~$3T on COBOL replacement since 2000 — **85% failed**. You don't
replace the meal; you change *when and how it's processed*. This repo **wraps**
a COBOL batch job and emits a routable, attested, settlement-ready A2A object.
The `cobol-parser` is the atomic unit: **reads one COPYBOOK → emits one JSON.**

## The weaving
```
COBOL MAINFRAME (stomach, batch)          A2A (bloodstream, real-time)
│  overnight batch job 11pm                │  agents react in ms
│  → 50,000 settlement instructions        │  → T+0 atomic DvP
        │                                          │
        └──── EUNOMIA WRAPPER (stomach lining) ─────┘
                 │
                 ├── cobol-parser     COPYBOOK → JSON schema      ← THE PROOF
                 ├── a2a-agent-cards financial agent identity + DID
                 ├── atomic-settlement smart-contract atomic DvP
                 └── compliance-bridge ISO 42001 + MiCA + MiFID
```

## The proof of weave (100 lines)
`cobol-parser/copybook_schema.py` reads one COPYBOOK and emits one JSON schema:
```
$ python3 cobol-parser/copybook_schema.py
parsed 5 fields
  SETTLE-DATE  string   X(8)
  NOTIONAL     number   9(12)V99
  ...
{'$schema': 'https://json-schema.org/draft/2020-12/schema', ...}
```
Every field is a routable `eunomia://` node; every route is crosswalked; the whole
batch can be signed + chained by the live engine-axis (`/api/attest`).

## Route (live, on csoai-gspc)
```
POST https://csoai-gspc.pages.dev/api/cobol   {copybook}
  → { fields:[...], schema:{...}, route:"eunomia://bridge/cobol" }
```
