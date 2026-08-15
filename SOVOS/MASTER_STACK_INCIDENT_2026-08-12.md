# SOVOS-MASTER — Incident + Recovery Runbook (12 Aug 2026 ~10:00 UTC)

## THE INCIDENT
`pod update 1dldzposn7ssuu --ports "8888/http,22/tcp,9000/tcp,9001/tcp"`
→ accepted config, but pod went `desiredStatus: RUNNING / machineId: None / uptime: 0`.
restart + stop/start did NOT re-allocate a machine within ~10 min. Pod unreachable on SSH (timeout).

**Root cause:** RunPod config-change / port-update left the pod without an allocated machine
(mid-reprovision). Data is NOT lost — the persistent `/runpod` volume travels with the pod and
remounts on re-provision. This is an AVAILABILITY outage, not a data-loss event.

## WHAT IS DURABLE (verified / triplicated)
| Asset | Copy 1 | Copy 2 | Copy 3 |
|---|---|---|---|
| `evidence/` (inventory, test, durab-check) | A100 MinIO master | `corpus-backup` mirror (same vol) | **Mac `~/sovos-master-backup/`** ✅ |
| `boards-sov6` (all board JSONs, 12 probe jsonl, peritem, run_all.py) | A100 MinIO `corpus/boards-sov6-2026-08-12/` | `corpus-backup` (same vol) | ~persisted volume (remounts) — **NOT yet on Mac** ⚠️ |
| Season 1b + runbook (git) | origin/jv-wave8-production (`50ef9b6`, `50ef9b6`) | Mac working tree | — ✅ |

## THE COVERAGE GAP I OWN
My Mac LaunchAgent backed up `sovos:evidence/` only, NOT `sovos:corpus/`. So boards-sov6
were NOT on the Mac at restart time. Correct fix (todo): backup ALL buckets, and before any
future pod port-change, rclone the FULL master to Mac. The `evidence/` 3-copy guarantee held;
the `corpus/` copy-on-Mac did not yet.

## RECOVERY (when RunPod re-provisions)
```bash
# 1. Wait for machineId != None, then SSH in:
runpodctl pod get 1dldzposn7ssuu          # machineId should be set, uptime > 0
ssh -i ~/.runpod/ssh/runpodctl-ssh-key -p 11737 root@104.255.9.187

# 2. Verify /runpod remount (MinIO data persisted)
ls /runpod/sovos-master                    # should show data (or be empty if lost)

# 3. Re-init MinIO server on :9000/:9001 (creds in /root/.sovos-master/credentials.env)
export MINIO_ROOT_USER=$(grep MINIO_ROOT_USER /root/.sovos-master/credentials.env | cut -d= -f2)
export MINIO_ROOT_PASSWORD=$(grep MINIO_ROOT_PASSWORD /root/.sovos-master/credentials.env | cut -d= -f2)
nohup /usr/local/bin/minio server /runpod/sovos-master \
  --address ":9000" --console-address ":9001" > /root/.sovos-master/minio.log 2>&1 &

# 4. Re-verify public :9000 reachable now that port is exposed:
curl -s -o /dev/null -w "%{http_code}\n" http://104.255.9.187:9000/minio/health/live   # want 200
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:9000/minio/health/live      # want 200

# 5. Verify objects survived:
/usr/local/bin/mc alias set sovos http://127.0.0.1:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" >/dev/null 2>&1
/usr/local/bin/mc ls sovos/corpus/boards-sov6-2026-08-12/   # want the 21 parked objects
/usr/local/bin/mc ls sovos/evidence/
```

## WHEN A100 IS BACK — finish "connect all nodes"
- **3090** (`fpowppss5ngtkw`, 194.26.196.156:17446): rclone `sovos:` → `http://104.255.9.187:9000`,
  creds `gpu3090-rw`/key in runbook. Now reachable b/c :9000 exposed.
- **Oracle micros**: rclone S3 → same public endpoint.
- **Kaggle**: boto3 → `http://104.255.9.187:9000`, `MINIO`-style access key.
- **Fix backup coverage**: change Mac LaunchAgent to `rclone copy sovos: ~/sovos-master-backup/`
  (ALL buckets), and add `sovos:corpus/` pull now.

## LEARNINGS (canon)
1. **`pod update --ports` on this account can deschedule the pod for a long allocation wait.**
   Before doing it again: (a) full rclone of ALL buckets to Mac FIRST, (b) expect downtime.
2. **Coverage:** backup script must cover every bucket, not just `evidence/`.
3. **CPU pods don't boot on this account** (RUNNING/uptime 0) — don't use them for master.
4. Master data must be considered ON THE PERSISTED VOLUME = safe across reprovision, but
   independent-host copies make "never lose a piece" actually true.

---

## RESOLUTION ADDENDUM (12 Aug 2026 ~11:35 UTC, Kimi lane)

**A100 re-provisioned** (~11:10 UTC) — machineId 4o02unscakdn. Recovery executed and verified:

| Step | Result |
|---|---|
| Port remap discovered | SSH now **11736** (was 11737); **public MinIO = 104.255.9.187:11737** (private :9000); console :11738 |
| /runpod intact | all buckets' data present |
| /root + /usr/local WIPED | minio/mc binaries + root creds gone (ephemeral) — root cause of re-init failure |
| **Full legacy extraction** | entire old master tar'd to Mac (`~/sovos-master-backup/master-legacy.tar.gz`); all 21 boards-sov6 objects recovered incl. peritem_agi (540 rows) + peritem_asi (495 rows) via xl.meta/part extraction; only all12c.log lost (redundant log) |
| Fresh MinIO v2 | new data dir `/runpod/sovos-master-v2`, new root creds |
| **Creds hardened (lesson applied)** | root creds in 3 places: `/runpod/sovos-master-config/credentials.env` (PERSISTENT, 600) + `/root/.sovos-master/` + Mac Keychain `meok-keystone/SOVOS_MASTER_MINIO_ROOT_*`. GCP keystone path dead (BILLING_DISABLED) |
| Buckets/users/policy | 7 buckets + `a100rw-GDiniQ` + `gpu3090rw-11lvAw` (same keys, `sovos-rw` policy) recreated |
| Re-seeded | 20 boards objects + 3 evidence objects via public endpoint; corpus→corpus-backup mirror synced |
| Mac client | rclone `sovos:` → `http://104.255.9.187:11737` (NO tunnel needed) — list/write/read verified; tunnel LaunchAgent removed; nightly backup agent (02:10) now runs over public endpoint |

**New canon:** (5) `/root` and `/usr/local` are ephemeral on pod re-provision — anything
that must survive lives on `/runpod` or off-box. (6) After any pod restart, SSH/HTTP
public ports may REMAP — always query the API for current mappings before assuming.
(7) Full rclone/tar of ALL buckets to Mac BEFORE any pod config change (was learning #1;
the boards' peritem rows existed nowhere else at restart time — now they do).
