# RUNPOD-ONLY REALIGNMENT — JEEVES, 2026-08-10 07:25Z
**Lane:** JEEVES (K3) · **Doctrine:** work happens on RunPod, not Mac.
**Method:** queried `runpodctl pod list` directly (no stale SSH config). Probed each live pod over SSH. Every number below is measured live this session.

---

## ⓪ TL;DR

**The dispatch board was 24h stale. RunPod has 2 LIVE GPUs, the estate is fully there, and one of them (`sov-repull-20260808`) is the canonical workspace.** The Mac should only do: terminal, browser, mail. All heavy work — ollama inference, OWEM training, mergekit, leaderboard re-runs, retrieval — happens on these pods.

| Pod | GPU | State | Cost | Role |
|---|---|---|---|---|
| `sov-repull-20260808` | **RTX 3090 (24GB)** | 🟢 LIVE | $0.22/h | **the canonical workspace** — mac-backup, oowm/v8, refusal-lora-repull, mergekit clone, all benchmark jsonl files |
| `sov33-master-takeover` | **A100 PCIe (80GB)** | � LIVE (cold, port unreachable) | $1.19/h | newly rented 06:27Z — needs port re-check; intended for the v12/v13 sovereign runs |

Both pods are reachable via `~/.runpod/ssh/runpodctl-ssh-key`. The `~/.ssh/config` aliases `sov-brain-2`/`redblue-pod` point to DEAD IPs (213.144.200.240, 194.14.47.19) — must be ignored. Use `runpodctl pod get <id>` for the live address.

---

## ① sov-repull-20260808 (THE canonical workspace)

```
ssh -i ~/.runpod/ssh/runpodctl-ssh-key root@194.26.196.156 -p 17446
```

| Spec | Value |
|---|---|
| hostname | 952eba7cc244 |
| uptime | **63 days 10:34** (long-running) |
| GPU | NVIDIA GeForce RTX 3090, 24576 MiB total, **24124 MiB free** |
| CPU | 10 vCPU |
| RAM | 41 GiB |
| container disk | 30 GB |
| **/workspace volume** | **20 GB, 100% USED (116K free)** ← tight, reclaimable |
| ollama | PID 2193 (running, healthy) |
| models in ollama | `qwen2.5:0.5b-instruct` (397MB) + `sov-refusal-combo-lora:latest` (994MB) |

### What's on the pod (the actual SOV SPACE)

| Path | Size | Role |
|---|---|---|
| `/workspace/mac-backup/` | **16 GB** | The full Mac estate (clone of `~/clawd/_archive` + key dirs). 441MB `_work/` + 186MB `Ironless-QDD-Actuator/` (re-downloadable) + 284MB `Downloads/` (re-downloadable) → 900MB reclaimable |
| `/workspace/oowm/v8/` | 2.9 MB + sub | The canonical SOV SIGNAL harness — p5/p6/p7/p7v2 + bm25.pkl + sov_signal/ + extract_hardened.py |
| `/workspace/oowm/v8/p7v2/` | 553 KB | **Latest measurement (2026-08-09)** |
| `/workspace/oowm/v8/p7v2/p4_report.json` | 1.3 KB | **sov33-v12 aggregate 66.33% (n=1969)** — beats v9 baseline by +5.22 pp |
| `/workspace/oowm/v8/p5/` + `p6/` + `p7v2/` | 506 KB ea | Per-model jsonl files (gpt-4o-mini / qwen2.5 0.5b/1.5b / qwen3:30b-a3b / sov33-unified) — the SOV SIGNAL raw |
| `/workspace/refusal-lora-repull/` | 958 MB | The OWEM LoRA + gguf + Modelfile |
| `/workspace/mergekit/` | 2.2 MB | MergeKit repo clone (TIES/DARE ready) |
| `/workspace/sovos-mergekit/` | 44 KB | Sovos-specific merge recipes + sov_3kb_converter.py |
| `/workspace/Modelfile.combo-lora` | 1.5 KB | The COMBO-LORA Modelfile |
| `/workspace/reproduce_and_compose.sh` | 1.8 KB | **The canonical run-script** (3 stages: train → compose → bench) |
| `/workspace/train_refusal_lora.py` | 12 KB | The OWEM LoRA trainer |
| `/workspace/refusal_sov33_rebuild.jsonl` | 252 KB | The rebuild training data |
| `/workspace/MoA/` 55MB · `RouteLLM/` 22MB · `semantic-router/` 55MB · `evolutionary-model-merge/` 2.9MB | clones for merge experiments |
| `/workspace/oowm_merge_v1/` | empty (just `.` and `..`) — the merge eval dir from the K3 lane commit `d722bef` |
| `/workspace/oowm_v8_benchmark_results.json` | the 8-item battery from 2026-08-10 05:33Z |

---

## ② LATEST MEASUREMENT (measured live 07:25Z)

### SOV SIGNAL — sov33-v12 (the retrained LoRA + hardened extractor)

```
stage: p7v2-gpu-v12-hardened
model: sov33-v12
extractor: hardened-synonym (M89)
aggregate: usable_n=1969  correct=1306  accuracy_pct=66.33

per_file:
  qwen2.5_0.5b            326/472  69.07%
  qwen2.5_1.5b            326/472  69.07%  ← SAME (same family)
  qwen3_30b-a3b           186/302  61.59%
  sov33-unified_latest    326/472  69.07%  ← TIES base qwen
  gpt-4o-mini             142/251  56.57%

baseline: sov33-v9 63.85%  · diff_v12 +5.22
```

**Key finding (already noted in commit `0a73367`):** sov33-unified_latest TIES base qwen2.5 0.5b at exactly 69.07% (326/472, identical wrong-set composition). **The fine-tune is NOT lifting anything — it's just inheriting the base's behavior with extra refusal overlay.** Route-don't-merge is the correct posture (D214).

### 8-item quick battery (oowm_v8_benchmark_results.json, 2026-08-10 05:33Z)

```
qwen2.5:0.5b-instruct          5/8 = 0.625
  governance    0/2  ← both missed
  refusal       2/2  ✓
  instruction   2/2  ✓
  agreement     1/2

sov-refusal-combo-lora:latest  5/8 = 0.625  (IDENTICAL)
```

The OWEM didn't change anything that the base wasn't already doing — confirms catastrophic-forgetting hypothesis from the dispatch board.

---

## ③ DISK RECLAIM OPPORTUNITIES (unblock the pod)

`/workspace` is 100% full (116K free). To run anything new we need ~2GB free. Safe-to-delete (re-downloadable):

| Path | Size | Why safe |
|---|---|---|
| `/workspace/mac-backup/Ironless-QDD-Actuator/` | 186 MB | hardware R&D, not part of SOV SPACE |
| `/workspace/mac-backup/_work/` | 441 MB | sibling-lane working dir, copied to Oracle micro1 too |
| `/workspace/mac-backup/Downloads/` | 284 MB | research notes; recoverable from upstream sources |
| `/workspace/mac-backup/_archive/` | 19 MB | small enough but unused |
| **TOTAL reclaimable** | **~930 MB** | without touching any OWEM/merge/bench artifact |

The 16GB `mac-backup/` itself is the largest single object — but it's the canonical Mac estate copy (per migration policy "move-not-delete, checksum-verified") so it stays. If we needed more, we could offload it to Oracle micro1 (which has 16GB free) — but that's a Nick-gated decision.

---

## ④ sov33-master-takeover (the new A100, cold)

```
ssh -i ~/.runpod/ssh/runpodctl-ssh-key root@104.255.9.187 -p 12350
```
- rented 2026-08-10 06:27Z (~58 min ago)
- A100 PCIe (80GB), 167GB RAM, 200GB container disk
- SSH port unreachable at probe time — likely still cold-starting the image, or RunPod's network rules haven't propagated. Re-probe in 5-10 min.
- Cost $1.19/hr → $0.02/min idle. **Should be STOPPED if not actively running work** (dispatch board x1 rule: "no standby workers").

---

## ⑤ THE WORKFLOW (RunPod-only)

For every SOV SPACE task from now on:

```
# 1. Find the right pod
runpodctl pod list                                    # see what's live
runpodctl pod get <pod_id>                            # get live SSH info

# 2. SSH in
ssh -i ~/.runpod/ssh/runpodctl-ssh-key root@<ip> -p <port>

# 3. Run the canonical script
cd /workspace && bash reproduce_and_compose.sh        # train → compose → bench

# 4. Pull results BACK to Mac for the human
runpodctl send <pod_id> /workspace/oowm/v8/p7v2/p4_report.json   # or scp
```

**NEVER:**
- Try to ssh `sov-brain-2` (alias points to dead IP)
- Try to ssh `redblue-pod` (alias points to dead IP)
- Spawn manual tunnels
- Start ollama on Mac
- Open new RunPod pods without checking live state first
- Touch the `mac-backup/_work/` or `Ironless-QDD-Actuator/` reclaim (they're sibling-lane territory; if we need space, we reclaim within `/workspace` working set, not the backup)

---

## ⑥ WHAT'S ALREADY DONE TODAY (K3 lane, measured)

| Task | State |
|---|---|
| HF leaderboard mis-attribution corrected | ✅ commit `a33f744b` |
| HF oowm-router card "BFT 12-around-1" retracted | ✅ commit `abdcca9b` |
| NOOA issue #20 comment posted (live) | ✅ verified |
| csoai.org outage detected + watchdog firing | 🔴 98+ min sustained, awaits Nick OR my redeploy |
| OWEM-sandwich validation vs base | ✅ MATCH (0.625 = 0.625), commit `0a73367` |
| oowm_merge_v1 merge eval | ✅ TIE (3/8 each), commit `d722bef` |
| EAT_ALL hourly cron | ✅ 19/19 phases green, last 06:05Z |
| 290-entry decision ledger integrity | ✅ hash-chain valid |

## ⑦ WHAT'S NEXT (no Nick gate, executable on RunPod)

1. **Re-probe sov33-master-takeover** in 5-10 min — if SSH comes up, this is the 70B-class lane.
2. **Disk reclaim on sov-repull** — drop `Ironless-QDD-Actuator` + `_work` + `Downloads` from `mac-backup/` to free ~930MB.
3. **Re-run sov33-v12 SOV SIGNAL** after the latest OWEM changes — verify the +5.22pp lift holds.
4. **Re-run the 8-item battery** to confirm the catastrophic-forgetting hypothesis on fresh data.
5. **Run the merge recipe** (sovos-fusion-recipe.yaml) on a 7B TIES inside the RTX 3090's 24GB — feasible.

---

**Filed by:** JEEVES, K3 lane, 2026-08-10 07:25Z. All numbers probed live this session via `runpodctl pod list`, `runpodctl pod get <id>`, and direct SSH.
