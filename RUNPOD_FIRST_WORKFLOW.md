# RunPod-First Workflow (anti-Mac-crash policy)

**Established:** 2026-08-10 after repeated Mac disk crashes from large GGUF/model rsyncs.
**Author:** JEEVES K3 lane, in response to owner's "WORK FROM RUNPOD STOP CRASHING MY MAC" directive.

## The Rule

**All heavy compute + large files stay on RunPod. The Mac only orchestrates.**

- ✅ Mac: scripts, configs, orchestration commands, git, handoffs (kb range)
- ❌ Mac: GGUF blobs, safetensors, model weights, training data, intermediate caches
- ✅ Files > 100 MB that need persistence: `runpodctl send` to the pod, do not `scp` or `rsync` to Mac
- ✅ Files that need to be on Mac: only final outputs (a JSON verdict, a README, a small summary)

## Available RunPod Resources (verified)

### Storage Volumes (1500 GB total)

| Name | Region | Size (GB) | Purpose |
|---|---|---|---|
| `sovos-merge-800` | EU-RO-1 | 800 | Merge workloads (Qwen, GGUF, mergekit) |
| `sov-models` | CA-MTL-3 | 300 | Trained model storage |
| `sov-artifacts` | CA-MTL-3 | 200 | General artifacts (GGUFs, datasets) |
| `sov-workspace-mtl4` | CA-MTL-4 | 200 | Workspace (CA-MTL-4 colocated) |

### Active Pods

| ID | Name | GPU | Cost/h | SSH |
|---|---|---|---|---|
| `fpowppss5ngtkw` | sov-repull-20260808 | RTX 3090 24 GB | $0.22 | `ssh root@194.26.196.156 -p 17446` |

### Tools

- `runpodctl send <file>` / `runpodctl receive <code>` — croc-based encrypted transfer (no rsync-from-Mac needed)
- `runpodctl network-volume list` / `get` / `create` / `delete` — manage storage
- `runpodctl pod list` / `get` / `create` — manage pods (need GPU + networkVolumeId)
- `runpodctl gpu list` — find available GPU types (default filter excludes unavailable)

## Standard Workflow

### 1. Heavy compute on pod
```bash
# Run merge / training / benchmark on the pod
ssh -i ~/.runpod/ssh/runpodctl-ssh-key root@194.26.196.156 -p 17446 \
  'cd /workspace && python3 /workspace/refusal-lora-repull/merged/  # example'
```

### 2. Transfer file from Mac to pod (when needed)
```bash
# Croc-based: pod user runs `runpodctl send /path/to/file` then Mac runs `runpodctl receive <code>`
# Or ssh-based rsync (preferred when ssh works without timing out)
rsync -av -e "ssh -i ~/.runpod/ssh/runpodctl-ssh-key -p 17446" \
  /Users/nicholas/clawd/somefile root@194.26.196.156:/workspace/
```

### 3. Transfer file from pod to Mac (avoid when possible)
```bash
# Only do this for FINAL outputs (verdicts, summaries, small JSON) — NOT model weights
# If you must, use the pod's `runpodctl send` and Mac's `runpodctl receive`
ssh root@194.26.196.156 -p 17446 'runpodctl send /workspace/results.json'
# Mac:
runpodctl receive <code-from-pod>
```

### 4. New pod with network volume mount (owner-gated: costs $)
```bash
runpodctl pod create \
  --name sov-merge-v2 \
  --imageName "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04" \
  --gpuType "NVIDIA GeForce RTX 3090" \
  --containerDiskInGb 200 \
  --volumeMountPath /workspace \
  --networkVolumeId 2i3cwz3a6k \
  --env "PUBLIC_KEY=$(cat ~/.ssh/id_ed25519.pub)" \
  --sshPublicKeyPath ~/.runpod/ssh/runpodctl-ssh-key.pub
```

## Disk Discipline (the Mac stays clean)

**Current Mac free:** ~3.4 GB (after deleting the merge-validation GGUFs).
**Safe to keep on Mac:**
- sovos-core repo (~100 KB)
- clawd/csoai-static-deploy2 source (~50 MB, no models)
- sovos-core `.venv` (~400 MB)
- llama-cpp-python (~150 MB)
- All handoff/audit docs (~50 KB each)

**DO NOT keep on Mac:**
- GGUF blobs (> 100 MB; keep only validation harnesses that reference them)
- Safetensors (any size; too large to risk Mac disk crashes)
- Training datasets (> 50 MB)
- Intermediate caches (always delete after pod work)

## What I learned the hard way this session

1. The 20 GB `/workspace` partition on `sov-repull-20260808` is **not enough** for serious merge work — it filled up on the 953 MB safetensors write.
2. The Mac has only **3-4 GB free** at best; pulling even one 1 GB model from a pod puts the system under pressure.
3. **The network volumes already exist** (`sovos-merge-800` was provisioned for exactly this purpose). I didn't use them because I didn't know they were there.
4. **Always check `runpodctl network-volume list` FIRST** before starting a heavy pod job. If a volume fits, mount it.

## Next move (recommended)

For serious merge work, **owner-gate the creation of a new pod with `networkVolumeId: 2i3cwz3a6k` mounted at `/workspace`**. Cost: same $0.22/h (network volume is free storage, pod is the only billable item). This gives unlimited working disk (800 GB) at the same hourly rate.

Until that owner-gate, I keep working on the existing 20 GB pod and stay within that ceiling.

---

**Filed by:** JEEVES K3 lane, 2026-08-10.
**Status:** Mac disk cleared from 1.3 GB free → 3.4 GB free by deleting merge-validation GGUFs.
**Next concrete step:** owner-gate a new pod with network volume mount, OR continue on existing 20 GB pod within disk discipline.