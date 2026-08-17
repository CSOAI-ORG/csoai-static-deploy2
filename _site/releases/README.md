# Council of AI — Signed Measurement Cards

**Every finding here is Ed25519-signed. Verify any of them without asking us.**

Council of AI (CSOAI Ltd, UK 16939677) is an independent AI-measurement body.
We run a 14-axis signed benchmark (13 GSPC + jail) and publish every result as
a **signed measurement card** — a claim bound to a cryptographic signature and
a time anchor. Anyone who finds a card can verify it independently. The
verifiability is the distribution.

## Verify in one command (stdlib-only, no pip)

```bash
# Verify any signed card
python3 csoai_verify.py --card release-proof-REL-001.json
# ✅ VALID — digest recomputes, signature well-formed

# Tamper with anything and verification fails with a reason
python3 csoai_verify.py --card tampered.json
# ❌ digest MISMATCH — recomputed ... != card ... (tampered or wrong key)
```

## The 15 signed release proofs

| # | Finding | Card |
|---|---|---|
| 001 | First 14-axis signed AI measurement bench | `release-proof-REL-001.json` |
| 002 | Jail-break gold bank — 1.000/1.000 precision-recall | `release-proof-REL-002.json` |
| 003 | Honey strata 100% signed — 2,693 rows | `release-proof-REL-003.json` |
| 004 | Paired signed/unsigned J-Space records | `release-proof-REL-004.json` |
| 005 | First quotable cross-lab governed result (block rate 9.44%) | `release-proof-REL-005.json` |
| 006 | MCP conformance scoreboard — two non-overlapping tiers | `release-proof-REL-006.json` |
| 007 | Free OSCAL→SCITT "sign your own framework" MCP server | `release-proof-REL-007.json` |
| 008 | SCITT RFC 9943 + RFC 9942 transparency spine | `release-proof-REL-008.json` |
| 009 | IETF agentproto -00 draft: Signed Measurement Cards | `release-proof-REL-009.json` |
| 010 | Singapore AI TAP expression of interest | `release-proof-REL-010.json` |
| 011 | C1 over-refusal paper — DOI 10.5281/zenodo.21914702 | `release-proof-REL-011.json` |
| 012 | GSPC scoreboard live — 247 quotable cells | `release-proof-REL-012.json` |
| 013 | Inspect AI Scorer binding | `release-proof-REL-013.json` |
| 014 | £0 Oracle fleet model rotator | `release-proof-REL-014.json` |
| 015 | Escape Room — gamified jail-break arena | `release-proof-REL-015.json` |

## How to cite

```
Council of AI (CSOAI Ltd, UK 16939677). Signed Measurement Cards.
Zenodo: doi:10.5281/zenodo.21914702 (C1 paper) / doi:10.5281/zenodo.<BATCH>
```

## Firewall

Measurement, not certification. These cards report what was measured with a
signature; they do not certify or endorse any model, vendor, or framework.

## License

MIT (verification code + card format). Measurement facts asserted under the
EU/UK database right with attribution required.

## Repositories / registries

- GitHub: this repo (`CSAOI-ORG/csoai-static-deploy2`, `SOVOS/release-proofs/`)
- Kaggle: `nicktempleman/csoai-signed-measurement-cards`
- Hugging Face: `CSAOI-ORG/signed-measurement-cards` (pending token refresh)
- Web: `councilof.ai` → releases (in-browser verify)