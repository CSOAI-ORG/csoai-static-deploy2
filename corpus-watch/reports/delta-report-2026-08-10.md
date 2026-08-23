# Corpus-Watch Delta Report

Generated: 2026-08-10 05:25 UTC · normaliser `norm-v2` · watcher last-run `2026-08-10T05:25:09.835205+00:00`

Instruments watched: **8** · provisions under hash: **787** · drift events to date: **3**

Detection is a SHA-256 compare over the normalised consolidated text of each act (act-level — the honest coarse signal; provision-level slicing is a later refinement). A failed fetch records UNKNOWN, never 'unchanged'.

## Drift events

### UK GDPR (retained Regulation (EU) 2016/679) — act-level change detected 2026-08-09T05:53:56.892423+00:00

- Source: `legislation.gov.uk:eur/2016/679` · normaliser `norm-v2`
- Hash: `000351d3370db500…` → `d4f149166c5fa5caf208b65b49fc0fffc8d0cf8ed2dc29a9bcfa1127664bebe5…`
- Provisions potentially affected: **99** (act-level detection — the changed provisions are inside this act)
- **Action:** any evidence pack citing UK-GDPR needs review against the current text.

### Digital Markets, Competition and Consumers Act 2024 (incl. pricing-transparency guidance) — act-level change detected 2026-08-09T05:53:56.892423+00:00

- Source: `legislation.gov.uk:ukpga/2024/13` · normaliser `norm-v2`
- Hash: `68f03a76a1b63605…` → `488b4c713e4b53fd03aa7f0caca17dfa895ae959626bc32cb67cc63bedebc5da…`
- Provisions potentially affected: **386** (act-level detection — the changed provisions are inside this act)
- **Action:** any evidence pack citing UK-DMCCA needs review against the current text.

### NY GBS §349-a (algorithmic pricing disclosure, in force 2025-11) — act-level change detected 2026-08-09T05:53:56.892423+00:00

- Source: `web:None` · normaliser `norm-v2`
- Hash: `76c4d402f7a5c18f…` → `7fcb1d6b667787cc6ad0d5b49c7417e56d3d3ba587baf7c5bbfc345ab503425e…`
- Provisions potentially affected: **1** (act-level detection — the changed provisions are inside this act)
- **Action:** any evidence pack citing US-NY-349A needs review against the current text.


---
Signed: Ed25519, corpus-watch key (raw public key hex: `6bb1a649666d7b8bcf976509ed213db4084bebdb7fdf0a45f75068499b5f4e0e`). Verify: `openssl pkeyutl -verify -pubin -inkey keys/corpus-watch-ed25519.pub -rawin -in <this-file> -sigfile <this-file>.sig`
