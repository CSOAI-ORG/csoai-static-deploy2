# csoai-claimguard — the receipt for your claims

**Claim-vs-signed-artifact integrity checker.** Given a signed board and a public claim,
ClaimGuard verifies: (1) signature valid, (2) payload non-empty, (3) claim supported by data.
Deterministic — never a model opinion. MEASURED register.

It caught CSOAI's own overclaims twice in one week (a fake jail "separation resolved" and a
~2.7x-overstated guardrail lift). Let the same instrument audit yours.

## CLI
```bash
pip install csoai-claimguard
claimguard check board.signed.json '{"refusal_rate": 0.633}'
claimguard signed board.signed.json '{"separation": "SEPARATED"}'   # needs CLAIMGUARD_KEY
```

## MCP
Tools: claimguard.check · claimguard.signed (any agent can audit any claim).

## Honesty
- Measurement, not certification. The report is signed and verifiable without trusting us.
- Fail-closed: no key -> report unsigned-labelled; empty payload -> STUB flagged.
- RFC 8785 + Ed25519 + did:web:csoai.org trust root.

## License: CC-BY-4.0. Issuer: CSOAI Ltd (UK 16939677).

## Install
```bash
python3 -m venv .venv && .venv/bin/pip install csoai-claimguard
claimguard check board.signed.json '{"refusal_rate": 0.633}'
```
(Once published to PyPI, `pip install csoai-claimguard` works from any Python; in a venv or
`--user` — the macOS system Python is PEP-668-locked.)

## The honest pitch
"We caught our own overclaims twice in one week. Let the same instrument audit yours."
