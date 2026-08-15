# SOVOS-MASTER — True Master Stack Runbook (Part BH)

**Date:** 2026-08-12
**Goal achieved so far:** A blue-pod MinIO master is live on the A100; Mac + A100 clients read-write to it. Cross-pod (3090) and the 800GB volume remain pending the A100-restart decision below.

## What is LIVE right now (real, verified)

| Item | State |
|---|---|
| **MinIO server** | A100 `1dldzposn7ssuu` (104.255.9.187:11737), `RELEASE.2025-09-07`, on `:9000` (health 200) + console `:9001` |
| **Data dir** | `/runpod/sovos-master` on the A100's 100GB persistent volume |
| **Root creds** | `/root/.sovos-master/credentials.env` on A100 (mode 600) |
| **Buckets** | `models` `merges` `datasets` `evidence` `signed-cards` `corpus` (6, created) |
| **Users** | `a100-rw` (key `a100rw-GDiniQ`/`7e6JL5UXbD5XD5tS`) · `gpu3090-rw` (key `gpu3090rw-11lvAw`/`hZTqfLQnmWGWR6yx`), policy `sovos-rw` attached to both |
| **Mac client** | rclone remote `sovos:` via SSH tunnel `Mac→A100:9000` (mac localhost:9000). ✅ list+write+read verified |
| **A100 self-client** | rclone remote `sovos:` (localhost:9000). ✅ buckets + seeded `evidence/a100-inventory.json` |
| **3090 client** | NOT yet wired (needs :9000 reachable across DCs) |

## Buckets seeded so far
- `evidence/sovos-test.txt` (Mac heartbeat)
- `evidence/a100-inventory.json` (A100 manifest)

## The one blocking decision — A100 restart

**Why it's needed:** the A100's public IP only exposes `8888` + `22`. MinIO binds `:9000` but RunPod does not forward it to the public IP. The 3090 is in a **different datacenter** (no shared private VPC), so it can only reach A100:9000 via the **public IP**. Exposing :9000 on an existing pod = **restart**.

**What the restart drops:** the sibling lane's `run_all.py` in `/workspace/banks` — currently building the **sov6 all-12-axis board** (board_asi.json done, others in progress). Also the ouroboros/Season runs.

**Alternative (no restart):** keep the master A100-local + Mac only (proven working). The 3090 + 800GB volume get wired whenever Nick next restarts either pod anyway.

## Replication / "never lose a piece" layer (proposed)

```
A100 MinIO (master, /runpod 100GB)     ← source of truth
  ├── Mirror bucket `corpus-backup/`   ← mc mirror (live second copy)
  ├── Nightly `rclone sync` → Mac      ← third copy (off-box)
  └── (future) 800GB volume attach     ← durable backing when DC/port resolved
```

## Creds note (security)
The service-account secrets above are printed in this runbook for operational
use; rotate if this doc is shared. MinIO runs on the A100 with a 600-mode env
file; expose publicly only with the `gpu3090-rw` least-access user.

## Next (owner-gated)
1. **A100 restart to expose :9000** = full cross-pod (3090 + Mac + future volumes).
2. OR keep A100-local + Mac now, defer cross-pod.
3. Whatever is chosen: stand up `mc mirror corpus → corpus-backup` + a nightly   rclone-sync cron to the Mac so the "never lose a piece" guarantee is actually true.

## ✅ DURABILITY CONFIRMED — 3 copies live (12 Aug 09:30 UTC)

| Copy | Location | State |
|---|---|---|
| **1. Master** | A100 MinIO `evidence/` bucket | ✅ verified |
| **2. Mirror** | same host `corpus-backup/` bucket (mc mirror) | ✅ verified |
| **3. Off-box** | Mac `~/sovos-master-backup/` (nightly LaunchAgent + persistent tunnel) | ✅ verified |

Round-trip proof: `durab-check.txt` present in all 3, content intact.

## Persistent agents (Mac, no A100 restart)
- `com.csoai.sovos-master-tunnel` LaunchAgent — keepalive `ssh -L 9000:localhost:9000` → A100, **running/active**.
- `com.csoai.sovos-master-backup` LaunchAgent — nightly 02:10 `rclone copy sovos: ~/sovos-master-backup/`, loaded.

## Remaining (documented honestly)
- **3090 cross-pod** not yet wired — requires A100 :9000 public exposure (A100 restart) OR a later pod restart. Runbook has the exact create flags for a dedicated master pod if Nick wants one without touching the A100.
- The two CPU-master attempts (ubuntu:22.04 + minio/minio CPU pods) both failed to boot (RUNNING but uptime 0, runtime empty) — a documented RunPod CPU-pod quirk on this account; both deleted, $0.06/hr each, no data loss. Recording so future sessions don't repeat the attempt.
   rclone-sync cron to the Mac so the "never lose a piece" guarantee is actually true.
