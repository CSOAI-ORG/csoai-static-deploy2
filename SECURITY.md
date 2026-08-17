# Security Policy

## Reporting a vulnerability
Email security@csoai.org (or nicholas@csoai.org). We acknowledge within 72h.

## Scope
- The signed-card chain (Ed25519 over SHA-256 canonical JSON)
- The verify path at csoai.org/verify and `verify_offline.py`
- The gspc MCP server (io.github.CSOAI-ORG/gspc)

## What we care most about
- Signature forgery or chain breaks
- Any path that lets a card claim a measurement that didn't happen
- Key-handling weaknesses

## Our own doctrine
Signing keys live only on the signing pod / hardware keystone; public surfaces serve public keys only. No HMAC fallback card ever ships. See SOVOS/KEY-CONTINUITY.md for the two-identity rule.
