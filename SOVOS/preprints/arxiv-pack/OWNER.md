# OWNER — publish runbook (arXiv 2 ticks, expires 2026-08-27)

## Readiness
- Paper draft: `art5_cross_lab_fleet_measurement.md` · 15 sourced claims (all traced to signed artifacts)
- Endorsement route documented in `SOVOS/research/ARXIV_READINESS_BRIEF_2026-08-12.md`
  (need 1 endorsement per cs.* category; REFEREE route is legitimate, paid-endorsement is NOT).

## The 2 ticks (one command each)
1. **arXiv submit** (category cs.AI or cs.CY; needs endorsement):
   `arxiv-submit art5_cross_lab_fleet_measurement.md --category cs.AI`
2. **Zenodo DOI** for the signed sources (freeze the provenance):
   `zenodo upload SOVOS/preprints/arxiv-pack/sources.json --title "Art5 cross-lab fleet measurement"`

## Verify before submit (must all pass)
```bash
for m in SOVOS/boards-v2-2026-08-12/manifests/manifest_*.json; do
  CD sign.py --verify $m | tail -1
done
```
Every manifest must read `VALID`. The day-one sweep json is signed likewise.

## Hard rules
- arXiv expiration: **2026-08-27** — the expiry is the clock, not a preference.
- No paid endorsement service (arXiv forbids; account-suspension risk).
- Do NOT upload raw board.json (may carry internal codenames) — sources.json / cards only.
