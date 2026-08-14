# Chain A2 — HF dataset upload (fires after owner token rotation)

Built 2026-08-14T03:37:09.119543+00:00 UTC. 12 board cards, honest register.
Upload ONE command per board once the rotated HF token is set:

```bash
huggingface-cli upload csoai/gspc-affect SOVOS/boards-hf-cards/2026-08-14/affect.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_affect.json --repo-type=dataset
huggingface-cli upload csoai/gspc-art5 SOVOS/boards-hf-cards/2026-08-14/art5.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_art5.json --repo-type=dataset
huggingface-cli upload csoai/gspc-care SOVOS/boards-hf-cards/2026-08-14/care.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_care.json --repo-type=dataset
huggingface-cli upload csoai/gspc-det SOVOS/boards-hf-cards/2026-08-14/det.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_det.json --repo-type=dataset
huggingface-cli upload csoai/gspc-gov SOVOS/boards-hf-cards/2026-08-14/gov.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_gov.json --repo-type=dataset
huggingface-cli upload csoai/gspc-gspc_jail SOVOS/boards-hf-cards/2026-08-14/gspc_jail.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_gspc_jail.json --repo-type=dataset
huggingface-cli upload csoai/gspc-mach SOVOS/boards-hf-cards/2026-08-14/mach.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_mach.json --repo-type=dataset
huggingface-cli upload csoai/gspc-mcp SOVOS/boards-hf-cards/2026-08-14/mcp.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_mcp.json --repo-type=dataset
huggingface-cli upload csoai/gspc-oss SOVOS/boards-hf-cards/2026-08-14/oss.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_oss.json --repo-type=dataset
huggingface-cli upload csoai/gspc-prv SOVOS/boards-hf-cards/2026-08-14/prv.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_prv.json --repo-type=dataset
huggingface-cli upload csoai/gspc-swarm SOVOS/boards-hf-cards/2026-08-14/swarm.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_swarm.json --repo-type=dataset
huggingface-cli upload csoai/gspc-xr SOVOS/boards-hf-cards/2026-08-14/xr.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_xr.json --repo-type=dataset
```

Board .json (raw evidence) stays GATED — do NOT upload to the public dataset. 
Each README carries the measurement-not-certification banner; GATE3 conflation is blocked in code.