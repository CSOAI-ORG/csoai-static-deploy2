# GSPC HF Space — "Run a signed assessment" CTA (L2 Patronus move, staged)

**Date:** 2026-08-12 · **Status:** STAGED — blocked on O2 (HF token rotation gate)

## The move
The 15 HF Spaces (13 GSPC axis cards + oowm-router-demo + oowm-routing-matrix)
are static interactive demos but none links to the **live signed assessment**.
The Patronus-move CTA makes every card's primary action a signed run, not a link.

## The patch (applied to /tmp/gspc_gov_index.html, the gov card)
Added as the primary button (before "The dataset"):
```html
<a class="btn" href="https://councilof.ai/assess"
   style="background:#4338ca;border-color:#4338ca;font-weight:600">
  Run a signed assessment →
</a>
```
plus the honest line: "Every assessment returns an Ed25519 signature you can
verify offline — measurement you can prove, not just read."

## Apply to all 13 axis Spaces when the HF token gate clears
For each space in `csoai/gspc-{gov,agi,asi,prv,xr,det,art5,care,mcp,oss,mach,swarm,affect}`:
1. fetch `https://huggingface.co/spaces/csoai/{space}/raw/main/index.html`
2. apply the same button patch (keep the dataset link; promote the assess CTA)
3. upload via `huggingface_hub.upload_file` with the rotated token
4. verify: `curl -s https://csoai-gspc-gov.hf.space | grep "signed assessment"`

## Honest boundary
This is staged, not shipped — the HF token rotation (O2, owner gate, post-breach
posture) blocks every re-push. The minute the token lands, this is a ~20 min
batch across all 13 cards.

## Verified facts (this pass)
- 15 Spaces exist under csoai org, all runtime RUNNING, all static sdk
- gspc-gov Space is a **real interactive GovBench runner** (24 items, Art 5 +
  Annex III anchors, deterministic grading) — not just a card
- councilof.ai/assess → HTTP 200 (the live signed-assessment surface exists)
- councilof.ai/sign → 200 · councilof.ai/system-card → 200
- **HF collection "GSPC Governance Benchmark Suite" exists** but holds only 4
  domain benches (coai/poai/asisec/agisafe-bench). The 13 GSPC axis banks
  (gspc-gov/agi/asi/prv/xr/det/art5/care/mcp/oss/mach/swarm/affect) are NOT in
  it — the suite should contain the governance suite. STAGED: add all 13 when
  the O2 HF token clears (same batch as the Space CTA).
- arena page links to HF + Kaggle (K5 surface present); the 13 banks are all
  live on HF (200), so the "every item set is public on HF" claim is now true
  for the GSPC suite.
