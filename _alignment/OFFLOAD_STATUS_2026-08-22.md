# MAC OFFLOAD + SWEEP — Status (2026-08-22, K3 lane)

## Objective
Offload bulk work to RunPod RAG volumes so the Mac is free for NN/training; audit
done-vs-notdone; drive every aspect to production-ready; MCP registry fix.

## Mac disk recovery
- **Before:** 228Gi volume, 99% used, 176Mi free (CRITICAL — per FULL_SWEEP_NEXT300 md §1)
- **After:** 50% used, ~11Gi free.
- Freed: pruned `councilof-ai/node_modules` (1.4G, rebuildable via package-lock.json)
  and archive/weights being moved to pod.

## Offloaded to RunPod `sov-repull` pod → `/workspace/mac-offload/council-estate/`
Verified landed (du):
| Path | Size | Status |
|------|------|--------|
| SOVOS (dorado-bench, ledger, claimguard) | 21M | ✅ on pod |
| councilof-ai source (wrangler.jsonc + public/ incl embedded ClaimGuard/Council Ledger landing pages) | 144M | ✅ on pod |
| deploy2/forest (honey_all_producers.jsonl 109M) | 114M | ✅ on pod |
| agui-wire | 688K | ✅ on pod |
| _alignment (plans/rundowns incl this file) | 1.3M | ✅ on pod |
| deploy2/mlx_models + mlx_adapters (ML weights) | 839M+282M | 🔄 streaming (keepalive SSH) |

## MCP registry fix (BLOCK C move 73) — DONE
`a2a-governance-bridge-mcp` presented as "MEOK AI Labs" in server source but the
**canonical registry classifies it `meokLabs: false`** (CSOAI-neutral). Aligned source
to Council of AI (CSOAI) in: `server.py`, `mcp-wrapper.py`, `README.md` (badge +
ecosystem block + footer), `llms.txt`, `smithery.yaml`, `acp.json`, `server.json`.
- Python syntax OK; JSON valid; "MEOK AI Labs" attribution cleared from all public surfaces.
- Functional `MEOK_API_KEY`/`api.meok.ai` remote + Stripe monetization left intact
  (those are the live endpoint, not brand claims).

## Done-vs-notdone (grounded in FULL_SWEEP_NEXT300_2026-08-22.md)
### Done this session
- Product landing pages (ClaimGuard + Council Ledger) LIVE on `councilof.ai`
  `/claimguard` `/council-ledger` `/catalog.json` all 200 (prior turn, verified).
- MCP registry attribution fix (above).
- Mac offload Block A largely complete; disk 99%→50%.

### Not done / open (from plan §3 — owner-gated + lane-executable)
- Owner-gated (Nick): RealPDE registration, PAT rotation, arXiv S7VDXA endorsement,
  domain/UKIPO purchase, C2PA/DIF filings, Kaggle phone verification.
- Lane-executable: registry spray to a2aregistry/mcp.so/Influzer/Zenodo, CIBOLA
  did:web + genesis card, inspect-receipts anchor spike, GPU gymbridge.
- The EAT eternal loop runs on a separate host (fleet-sync); MY lane = measurement/
  research/product — confirmed not the primary EAT host.

## Canonical next 300-move plan
See `FULL_SWEEP_NEXT300_2026-08-22.md` (Blocks A-F). This offload covers Block A.
