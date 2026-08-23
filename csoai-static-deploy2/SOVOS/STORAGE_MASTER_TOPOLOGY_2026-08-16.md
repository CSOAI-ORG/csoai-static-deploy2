# STORAGE MASTER TOPOLOGY — 2026-08-16 (per Nick directive: no Mac, no GCP)

**Directive (verbatim-ish):** move ALL compute + storage to RunPod volumes
and Oracle. It should NOT run on the MacBook; it should run on RunPod for SOVOS
(volumes) or Oracle. GCP is billing-disabled (evac watcher armed).

## Where SOVOS master lives (canonical)

| Store | Host | Path | Status | Role |
|---|---|---|---|---|
| **SOVOS master volume** | A100-1 `1dldzposn7ssuu` | `/runpod/sovos-master` (MinIO :9000) | ❌ gateway down (recover) | ROOT — MinIO buckets, boards, keys |
| **Compute+storage clone** | 3090 `fpowppss5ngtkw` | `/workspace/fleet-sync` (feat @ bb1c592) | ✅ LIVE 149G free | current exec home for bench + jobs |
| **Oracle micro1** | sov33-owem-micro | ~/boards-data/ | ✅ ALIVE 15G free | GSPC axis registry + daily reports |
| **Oracle micro2** | sov33-owem-micro2 | ~/boards-data/ | ✅ ALIVE 1.5G free | GSPC axis registry + daily reports |
| ~~GCP meok-backend~~ | 35.242.143.249 | — | ❌ billing disabled | dead — evac watcher armed |
| ~~Mac~~ | — | — | editor-only 116Mi | NO compute/storage going forward |

## Rules (bind)

1. **Compute** runs on RunPod 3090 ($0.22/h) by default; A100s for signing/mergekit;
   Oracle micros for lightweight cron/registry.
2. **Storage master** = MinIO on A100-1 `/runpod/sovos-master` (recover when gateway
   returns). Mirror = 3090 `/workspace/fleet-sync` + both Oracle micros.
3. **Mac = editor + git only.** Nothing compute/storage-heavy on the MacBook.
4. **GCP** = not a target (billing dead). Oracle = the free UK always-on tier.
5. Every new run placed: 3090 (bench) / A100 (sign) / Oracle (cron) — never the Mac.

## Current exec home (this session)
- `/workspace/fleet-sync` on 3090 = clean clone @ bb1c592 (all session work).
- Oracle micros hold GSPC axis registries + daily city reports (05:00 UTC cron).
- A100-1 volume holds root MinIO — pending gateway recovery.

## Recovery action (gateway returns)
Kill retry loop → re-establish 6 tunnels per AGENTS.md → confirm MinIO master →
sync root volume to 3090 + Oracle (3-copy: master + mirror + Oracle).
---

## UPDATE 14:50 UTC (per Nick: "restart do all needed")

- **overnight-bench-a100-v2 (5ynpuvuiae807k) PAUSED** — runpodctl stop fired, EXITED verified. ~$860/mo saved.
- **A100-1 (1dldzposn7ssuu) RESTARTED** — full stop/start; RUNNING verified (billing-normal), but returned to same machine (4o02unscakdn) because the /runpod volume is pinned there. Gateway 104.255.9.187 still flapping at SSH — the flapping is RunPod-infra-level, not the pod.
- **Persistent A100 watch armed from 3090** (PID 1530337, /workspace/a100_watch.sh): polls every 15s up to 600 tries. On connect: storage_recovery_after_reconnect.sh auto-syncs /runpod/sovos-master -> 3090 mirror -> Oracle (3-copy), sets recovery_done.flag.
- **Oracle verify_record fixed on BOTH micros**: probe URL /mcp -> /health. Verified live HTTP 200 {"status":"ok"} (was 404 sewage every 30 min).
- **Round-2 gov bench running on 3090** (proc_25d322d92842): 5 models (council-oowm, council-safe, qwen3:4b, qwen2.5:1.5b, 0.5b) x 193 gov items, deterministic gate.
