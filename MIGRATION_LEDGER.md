# MIGRATION LEDGER (M7)

State at: $(date -u +%Y-%m-%dT%H:%M:%SZ)

| source | dest | size | status |
|---|---|---|---|
| ~/clawd/oowm-v8-e2e | /workspace/mac-backup/oowm-v8-e2e | 270M partial | in-flight |
| ~/clawd/sov33-oowm | /workspace/mac-backup/sov33-oowm | 144K | DONE |
| ~/clawd/sov-os | /workspace/mac-backup/sov-os | 361M partial | partial |
| ~/clawd/sovereign-charters | /workspace/mac-backup/sovereign-charters | 225M | queued |
| ~/clawd/sovereign-temple-public | /workspace/mac-backup/sovereign-temple-public | 253M | queued |
| Sibling dirs (mcp-marketplace, meok-oneos, csoai-dashboard, etc.) | /workspace/mac-backup/<same> | n/a | sibling-owned, untouched |

**Mac disk before:** $(df -h / | tail -1 | awk '{print $4}') free.

**Notes**
- Migration is PAUSED (sibling lane active on /workspace; reclaims deferred to avoid volume starvation).
- No deletes on Mac; copy-only via `rsync --partial` (resumable).
- Champion weights (v12 q8): pod-canonical md5 add16859…; Mac partial persisted.
- Migration scripts: `~/clawd/migrate_to_pod.sh`, `~/clawd/migrate_pending.sh` (both --partial, --append).
- **M3 BLOCKED 2026-08-09**: pod vol 100% full (118M free); cannot move ~/Downloads (613M) without starving the volume. Defer until: sibling rsyncs idle OR v12 merged model (3.1G, regenerable from adapter) is reclaimed. Mac retains ~/Downloads in the meantime (per "MOVE not delete").
