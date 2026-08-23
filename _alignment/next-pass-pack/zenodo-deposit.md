# Zenodo carder-card deposit — fire-ready
- Target: csoai community on Zenodo (create if not exists; ZENODO_TOKEN pod-side)
- Payload: latest signed h3k cards (ed25519, body_sha256-verified)
  - ~/sim-world-data/cards/h3k-2026-08-19T1146.json (7,428 B, 25 rec)
  - ~/sim-world-data/cards/h3k-2026-08-19T1148.json (7,453 B, 25 rec)
  - ~/sim-world-data/cards/h3k-2026-08-19T1151.json (11,913 B, 40 rec)
  - ~/sim-world-data/cards/h3k-2026-08-19T1155.json (14,670 B, 50 rec)
  - ~/sim-world-data/cards/h3k-2026-08-19T1159.json (28,810 B, 100 rec, MAX)
  - Total: 5 cards / 240 signed records
- Existing DOI: 10.5281/zenodo.21991104 (issuer CSOAI Ltd 16939677)
- Licence: CC-BY-4.0 (matches carder gate)
- API: POST https://zenodo.org/api/deposit/depositions (Bearer ZENODO_TOKEN)
- NOTE 2026-08-19 13:50: zenodo.org unreachable from K3's Mac (both v4/v6 time out at edge, 0 bytes).
  Deposit to run from pod (ZENODO_TOKEN lives there) or next session.
- Community check: not verifiable from here — run `curl -4 "https://zenodo.org/api/communities?q=csoai"` on pod.
