# Publish runbook — GSPC fleet board — 20 models (owner, after token rotation)

Everything in this folder is generated + honest. To publish (needs the rotated HF token):

```bash
# 1. HF dataset (board + card + JSON-LD) — PUBLIC artifacts only.
#    board.json is the RAW SIGNED EVIDENCE and may contain internal model
#    codenames; it is NOT auto-published. Upload only the clean files:
huggingface-cli upload csoai/gspc-fleet-board dist/fleet-board/scorecard.html dist/fleet-board/README.md dist/fleet-board/dataset.jsonld --repo-type=dataset

# 2. scorecard page → the site (Cloudflare Pages), then IndexNow ping
cp dist/fleet-board/scorecard.html <site>/boards/gspc-fleet-board.html

# 3. raw signed board.json → GATED location (not the public dataset), e.g. a
#    private/org-only repo OR strip codenames first. Never push it to the
#    public HF dataset as-is.
```
Nothing here is a certification. The scorecard carries the "measurement, not
certification" banner and reports ties as ties.
