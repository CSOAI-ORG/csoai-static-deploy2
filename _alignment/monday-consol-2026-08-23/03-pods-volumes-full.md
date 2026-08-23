# CEO Monday Inventory — Pods & Volumes
**When:** 2026-08-23 ~18:25 Europe/London (UTC+1)  
**Host:** M4 (`HOME=/Users/nicholas`)  
**Rule:** No pods stopped. One SSH BatchMode probe each (ConnectTimeout 10).

---

## Executive snapshot

| Metric | Value |
|--------|-------|
| RUNNING pods | **3** |
| Pod burn (list) | **$1.67/hr** ≈ **$40.08/day** |
| Account `currentSpendPerHr` | **$3.169/hr** (API higher than pod list — other spend?) |
| Client balance | **~$148.04** |
| Spend limit | **$80** |
| Network volumes | **5** (3500 GB provisioned) |
| A100-1 (`1dldzposn7ssuu`) | **GONE** (confirmed absent from live list) |
| fleet.json | **STALE** vs live (updated 2026-08-19) |

---

## 1) Live pods (`runpodctl pod list` / `pod get`)

| ID | Name | Status | GPU | $/hr | SSH (live) | Role (fleet) | Probe |
|----|------|--------|-----|------|------------|--------------|-------|
| `sz0duht9e5bbov` | sov-volume-sink-cpu | RUNNING | CPU (2 vCPU / 4GB) | 0.06 | `213.173.105.83:25804` | volume sync | OK — load **~72 / 111 / 129** on 2 cores |
| `fpowppss5ngtkw` | sov-repull-20260808 | RUNNING | RTX 3090 | 0.22 | `194.26.196.156:23243` Host `sov-brain-2` | keeper / bench / arena | OK — load ~6–11; GPU 38%, 11.5/24 GB |
| `l7g747oivyq6ab` | sovos-light-master-mine-20260816 | RUNNING | A100 80GB | 1.39 | live `38.128.232.57:23166` | mine (fleet: **do_not_start**) | Config Host `sovos-light-a100` port **15094 STALE** → timeout; live port OK — load **~92 / 98 / 76** |

**Pod burn check:** 0.06 + 0.22 + 1.39 = **$1.67/hr** (matches prior known).

**Resumed:** Mine A100 lastStatusChange `Resumed by user: Sat Aug 22 2026 10:45:10 GMT` — contradicts fleet `do_not_start` / mine-dept “stay EXITED”.

---

## 2) Network volumes (`runpodctl network-volume list`)

| ID | Name | DC | Size GB |
|----|------|----|---------|
| `2i3cwz3a6k` | sovos-merge-800 | EU-RO-1 | 800 |
| `i4atujketp` | k3-weights-2tb | EU-RO-1 | 2000 |
| `ahqvo6d4f3` | sov-workspace-mtl4 | CA-MTL-4 | 200 |
| `b0h5gma2fy` | sov-models | CA-MTL-3 | 300 |
| `uvevdv0pq9` | sov-artifacts | CA-MTL-3 | 200 |

**Total provisioned:** 3500 GB.

**Mounts observed:**
- Sink `/workspace` → `mfs#euro.runpod.net:9421` **2.3P / 81% used** (shared EU fabric; not pod-local disk)
- Mine A100 `/workspace` → `mfs#ca-mtl-3.runpod.net:9421` **755T / 62% used**
- 3090 `/workspace` → local nvme **100G / 46% used**

---

## 3) SSH probes (once each)

### 3a Volume sink — OK
- Host `8d0da0319077`, uptime ~485d host, **NPROC=2**
- Loadavg **71.91 111.34 129.27** (still severe; prior known ~150; slightly down but far above 2-core capacity)
- Flags present: `/workspace/rebuild-needed`, `/workspace/retrain-needed` (touched ~17:17–17:20 UTC)
- Active: `sovos-finish-watcher.sh`, parallel `sovos-harness-rebuild.sh` + `find … -exec rm -rf` + `rm -rf` on harness tree (I/O thrash → load)
- `finish-watcher.log` ~2.9 MB; recent `FINISH_DONE` at **15:54** and **16:34** UTC; watchdog **training launched** at 16:09 and **17:09**
- **`train-v2.log` restart loop (Qwen2.5-0.5B-Instruct):**
  - Early: missing `sov_minimal_train.py` (ENOENT) ×3
  - Then repeated start → load weights → restart (no “steps done” / no `sov-minimal-output-v2` observed)
  - Watchdog relaunches when output dir missing and trainer not in `pgrep`
- Cron/rebuild race: finish-watcher triggers rebuild → rm harness → trainer path flaps → watchdog restarts train → load stays extreme

### 3b 3090 `sov-brain-2` — OK
- Host `01d43fdfaa57`, up ~76d, load **~6–11**
- GPU: RTX 3090, util ~38%, mem 11505/24576 MiB
- Live work: `axis_engine_16.py`, `f2_gen_v2.py`, `meok_router_server.py:8787`, `gspc_genetic.py`, dorado measure, `axis_supervisor.py`, chain heartbeat fresh
- **Stuck / STOPPED (STAT T/Ts/Tsl)** — intentionally SIGSTOP’d earlier:
  - `grok_referee_keeper.py` (Ts, ~3.5d)
  - `ops_daemons.py` (Tsl)
  - `arena_loop_keeper.py` (Ts)
  - stopper shell still in history (`kill -STOP` on arena/referee/ops)

### 3c Mine A100 — config miss, live port OK
- `Host sovos-light-a100` → `38.128.232.57:15094` **timed out**
- Live `runpodctl` SSH port **23166** works
- Host `81cb00d14b42`, up ~46d, load **91.64 97.58 76.43**, ~215 runnable
- GPU: A100 80GB PCIe, util ~18%, mem 22308/81920 MiB
- Hot: multiple `ollama` `llama-server` (CPU 560%–1516%), `ollama serve`, `engine-supervisor.sh` / `axis-engine.sh`, `pod-bench.sh`
- No active `sov_minimal_train` / Qwen train on this box at probe time
- Note: `pod-bench-parallel.sh` syntax error in log noise

---

## 4) fleet.json roles vs live

Source: `~/.grokbot/harness/fleet.json` (updated **2026-08-19T11:20+01:00**)

| fleet claim | live 2026-08-23 |
|-------------|-----------------|
| 4 RUNNING @ $2.86/hr | **3 RUNNING @ $1.67/hr** |
| `qdigrzjp5na1ek` sov-brain-a100-fresh RUNNING | **GONE** |
| `1dldzposn7ssuu` A100-1 / do_not_hammer | **GONE** (known) |
| `l7g747oivyq6ab` in `do_not_start` + mine “stay EXITED” | **RUNNING** (resumed Aug 22) |
| keep: `fpowppss5ngtkw` / `sov-brain-2` | **OK live** |
| sink `sz0duht9e5bbov` volume sync | **OK live** but overloaded |
| EXITED list still mentions mine as EXITED | **contradicts live** |

**Action for Monday:** refresh `fleet.json` RUNNING/EXITED/do_not_start; fix SSH Port for `sovos-light-a100` → **23166** (or regenerate from `runpodctl pod get`).

---

## 5) Stuck processes & burn risks

### Stuck / looping
1. **Sink train-v2 restart loop** on Qwen2.5-0.5B (watchdog + finish-watcher + rebuild rm race)
2. **Sink harness rebuild `rm -rf` / find** driving CPU/IO load on 2 vCPU
3. **3090 SIGSTOP’d keepers** (arena/referee/ops) — not dead, frozen
4. **A100 ollama multi-server storm** — extreme loadavg; GPU underused vs CPU thrash
5. **Stale SSH config** for mine A100 (wrong port)

### Monday risks (priority)
| P | Risk | Impact |
|---|------|--------|
| P0 | Sink load ~70–130 on 2 cores + rebuild/train loop | Volume sync / finish path unreliable; shared EU MFS pressure |
| P0 | Mine A100 burning **$1.39/hr** while fleet marks **do_not_start** | ~$33/day unintended if policy still “mine EXITED” |
| P1 | Account `currentSpendPerHr` **$3.17** vs pods **$1.67** | Hidden serverless/other burn — reconcile |
| P1 | Balance ~$148 vs spendLimit $80 alerts | Plan runway / raise limit or cut mine |
| P1 | fleet.json 4 days stale; A100-1 gone; phantom `qdigrzjp5na1ek` | Wrong CEO decisions from stale roles |
| P2 | 3090 keepers STOP’d | Arena/referee not actually running |
| P2 | train-v2 never producing `sov-minimal-output-v2` | Retrain flag churn forever |
| P2 | SSH Host `sovos-light-a100` port stale | Ops probes “fail” falsely |

---

## 6) Recommended Monday moves (do not execute overnight)

1. **Decide mine A100:** stop per `do_not_start` **or** update fleet to allow + document owner lane.
2. **Sink:** pause watchdog/cron rebuild temporarily; clear `rebuild-needed`/`retrain-needed` only after one clean train; break Qwen restart loop (pin script path post-rebuild or disable hourly relaunch).
3. **Refresh** `fleet.json` + `~/.ssh/config` Port for `sovos-light-a100`.
4. **Reconcile** `$3.169/hr` API spend vs `$1.67` pods (serverless? volumes? orphans?).
5. **3090:** `kill -CONT` keepers only if arena intended; else leave STOP’d and document.
6. **Do not** delete network volumes without CEO call — 3.5 TB across EU-RO-1 / CA-MTL-*.

---

## Appendix — raw IDs quick copy

```
sink:  sz0duht9e5bbov  ssh -i ~/.runpod/ssh/runpodctl-ssh-key root@213.173.105.83 -p 25804
3090:  fpowppss5ngtkw  Host sov-brain-2  (194.26.196.156:23243)
mine:  l7g747oivyq6ab  live 38.128.232.57:23166  (config port 15094 STALE)
gone:  1dldzposn7ssuu (A100-1), qdigrzjp5na1ek (a100-fresh)
```

*Inventory only. No pods stopped.*
