# EVERY EVAL EVER (EEE) SCHEMA-COMPAT SKETCH — K3 (19 Aug 2026)
**Task:** TODAY plan Stage-2 #5 (K3). Receipt as an EEE provenance block.

## Facts (HS.3, arXiv:2606.14516)
- EEE = 22,235 models · 2,273 benchmarks · converters for Inspect / lm-eval / HELM
- Cheapest distribution into the eval-science community = our receipt schema as an EEE provenance block

## The mapping (receipt → EEE block)
| Our receipt field | EEE provenance block field |
|---|---|
| `issuer` (did:web:csoai.org) | provenance.issuer |
| `subject_card` (agent/model id) | provenance.subject |
| `claims[].type` = measurement | provenance.claim_type |
| `evidence_sha256` (log hash) | provenance.evidence_hash |
| `content_id` (RFC 8785 sha256) | provenance.content_id |
| `signature` (Ed25519) | provenance.signature |
| `issued_at` | provenance.timestamp |
| supersession `prev` link | provenance.previous_claim (our J-space chain) |

## What this buys
1. **Distribution**: every EEE consumer sees signed measurement as a first-class field — no format war, just a block.
2. **Community trust**: EEE is the eval-science index; receipts become part of the scholarly record.
3. **The governance gap**: EEE has the catalog, we have the signing — complementary, zero conflict.

## Deliverable (agent-doable)
- [ ] Draft the JSON-LD/JSON Schema for `provenance` block matching EEE's converter output shape
- [ ] Validate against one real receipt (my RFC 8785 converter output) — schema-compat proof
- [ ] Submit as an issue/PR to EEE repo (coordinate-first, owner nod for external)

## Firewalls
- One genuine contribution · never claim EEE endorsement · measurement-not-certification

*Drafted by JEEVES (K3), 19 Aug 2026. Schema + validation next; external submission = owner GO.*
