# SOV*/33-AGENT PURGE LIST — councilof-ai (19 Aug 2026, JEEVES scan)
Canon gate (Part B (8) §419): "purge SOV* strings, reconcile to ONE verified fleet number, before any PR catapult." Kill-list: "BFT/33-agent" never in display copy.
Owner: Claude lane (deploy-lock). This is the grep target list.

## Scale: 71 files under client/src/
Counts by file: App.tsx:2 · SovereignDock:1 · GlobalSearch:4 · CouncilVisualization:1 · globeDrive:1 · EarlyAccessLanding:1 · PDCASimulator:5 (+ ~60 more)

## The strings to purge (canon kill-list)
- "33-Agent" / "33-agent" / "33 Agent" / "33-agent council" / "33-agent consensus"
- "SOVOS" / "SOV-" / "sov-space" / "Sovereign AI platform" (HM Government collision — VERIFIED)
- "BFT-33" / "33-seat" / "33-voter"

## Replacement language (measurement, not BFT)
- "33-Agent Council" → "the measurement council" / "the GSPC council"
- "33-agent consensus model" → "cross-lineage consensus (East-West, measured)"
- "Sovereign AI platform" → "independent measurement body" / "Council of AI"

## Command for the lane
grep -rln "33-Agent\|33-agent\|33 Agent\|SOVOS\|sov-space\|Sovereign AI platform" client/src/ | xargs sed -i '' -e 's/33-Agent Council/the measurement council/g; ...'
Verify: grep -rc returns 0 across client/src, then the persona-gauntlet CI stays green.
