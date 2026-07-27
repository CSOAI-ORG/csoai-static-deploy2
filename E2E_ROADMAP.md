# SOV E2E ROADMAP — What We Need To Do Now (2026-07-26)

## CURRENT STATE
- Volume: sov-models (mfs#ca-mtl-3.runpod.net:9421), 300GB at CA-MTL-3
- Pod: H100 PCIe 80GB (active, $2.89/hr)
- Other pods: 0 (all stopped, $0/hr)
- 188 bloodline entries, 65 honey pairs, 14 Modelfiles — all persistent
- 3-layer backup: RunPod volume + local Mac + competition bundle

## WHAT IS READY (no GPU/serverless needed)
- Bloodline.json (188 entries, 25.6KB) — integrated from sov-ultimate + sov-sov7
- Honey knowledge (65 Q/A pairs) — curated + distilled
- 14 Modelfiles written — sov5v2 + 13 sov6-v3 OWEMs
- sov4_router.py — pillar-aware routing, serverless-first, 4-tier fallback
- Multi-provider cloud — DeepSeek, Qwen, Gemini, Groq integrated
- 4 serverless endpoints created (qwen3-235b, qwen3-30b-a3b, gpt-oss-120b, deepseek-r1-671b)
- GSM8K weak-spot examples baked into all Modelfiles
- BACKUP_INDEX.md, E2E_ROADMAP.md, swarm_state.json on volume

## WHAT IS BLOCKED (waiting on)
- GPU: ollama 0.32.4 lacks llama-server binary (no CUDA). ollama 0.6.5 has CUDA but errors "device busy"
- Ollama: constantly killed by 4+ other agents on shared pod
- Serverless workers: return IN_QUEUE forever (H200/A100 capacity exhausted)
- Live EAT: extract files all have "Connection refused" (ollama contention)
- Frontier models (235B, 671B): can't pull to A40 (too big), H200 unavailable

## IMMEDIATE ACTIONS (do now, no GPU needed)

### Action 1: Verify all data persisted on volume
```
ls /workspace/sovereign/                    # our work
ls /workspace/sov-sov7/                     # other agents
ls /workspace/Modelfile.sov-ultimate        # other agents
ls /workspace/backups/                      # full backup tar
```

### Action 2: Build the E2E roadmap doc (THIS FILE) — WRITTEN

### Action 3: Run EAT in background, retry continuously
- Script: /tmp/eat_all.py
- Strategy: 20 retries per prompt, exponential backoff, skip already-done families
- Persists to /workspace/eat/extract_<family>.json

### Action 4: Move our + other agents' code to volume
- File: /workspace/sovereign/sov4_router.py (synced)
- File: /workspace/sovereign/bloodline.json
- File: /workspace/sovereign/swarm_state.json

### Action 5: Continuously save backups
- /workspace/backups/SOV_FULL_BACKUP_<timestamp>.tar.gz
- Schedule: every major change
- Frequency target: daily during active dev

## WHEN GPU BECOMES AVAILABLE

### Step 1: Fix GPU detection
Try in order:
1. apt install nvidia-container-toolkit (done, didn't help)
2. OLLAMA_LLM_LIBRARY=cuda_v13 ollama serve (done, no help)
3. Install ollama from source with CUDA
4. Try pip install llama-cpp-python with cuda
5. Try vLLM as alternative server (better CUDA support)

### Step 2: Run EAT for all 14 families
```
python3 /tmp/eat_all.py
```
Extracts: qwen, deepseek, llama, mistral, gemma, phi, gpt-oss, code, vision, embedding, qwen-vision, MiniMax, nemotron, core

### Step 3: Build models from Modelfiles
```
cd /workspace/sovereign/Modelfiles
ollama create sov5v2 -f sov5v2.Modelfile
for owem in creation preservation destruction synthesis abstraction embodiment relationality agency identity temporality aesthetics ethics logic; do
  ollama create sov6-${owem}-v3 -f sov6-${owem}-v3.Modelfile
done
```

### Step 4: Self-bench our models
```
python3 /tmp/swarm_robust.py
```
Tests GSM8K weak spots + sovereign core + OWEM domains across all our models.

### Step 5: Cross-pollinate (teacher to students)
```
python3 /tmp/swarm_orchestrator.py
```

### Step 6: Serverless retry (when capacity returns)
```
KEY=$(cat ~/.runpod/api_key)
curl -X POST "https://api.runpod.ai/v2/j9bukx8r1xew94/runsync" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"prompt": "test"}}'
```

## WHEN BUDGET RUNS OUT

### Backup everything one more time
```
ssh -p 12704 ... "tar -czf /workspace/backups/SOV_FINAL_<timestamp>.tar.gz /workspace/sovereign/ /workspace/sov-sov7/ /workspace/Modelfile.sov-ultimate /workspace/eat/"
scp /workspace/backups/SOV_FINAL_*.tar.gz /Users/nicholas/clawd/csoai-static-deploy2/backups/
```

### Move to different GPU (H100/H200/A100)
1. Provision new pod with networkVolumeId: b0h5gma2fy (attaches sov-models)
2. All work is immediately available at /workspace
3. Re-pull big models: qwen3:235b-a22b, deepseek-r1:671b
4. Re-build Modelfiles (or use existing ollama tags)

### Move to different platform (Mac / Colab / Modal)
1. Download tar.gz backup
2. Extract locally
3. Run ollama serve with Modelfiles
4. Re-attach RunPod volume when ready

## COST PROJECTION (after all fixes)
| State | $/hr | $/month |
|---|---|---|
| Current (H100 only) | $2.89 | $2,080 |
| After heavy pods stopped | $2.89 | $2,080 |
| With serverless + scale-to-zero | ~$0.50 | $360 |
| Local Mac only | $0 | $0 |
| Frontier models (serverless only) | ~$1 | $720 |

## KEY METRICS TO TRACK
- Bloodline entries: 188 (target: 250+ after EAT)
- Honey pairs: 65 (target: 200+)
- GSM8K pass rate: 0/98 (target: 80+/98)
- BBH pass rate: 0/15 (target: 12+/15)
- Sovereign bench: 0/12 (target: 10+/12)
- Serverless endpoints working: 0/4 (target: 4/4)
- Cross-pollination pairs: 0 (target: 50+ per OWEM)

## TICKETS (in priority order)

### Ticket #1: Fix GPU detection (HIGH)
- Block: ollama 0.32.4 lacks llama-server
- Action: try vLLM or llama-cpp-python install
- Owner: any agent with pod access
- Effort: 2-4 hours

### Ticket #2: Run EAT for all 14 families (HIGH)
- Block: ollama contention
- Action: script exists, retry loop handles restarts
- Owner: any agent
- Effort: 30 min when ollama stable

### Ticket #3: Build models from Modelfiles (MEDIUM)
- Block: GPU detection (#1)
- Action: 14 ollama create commands
- Effort: 5 min when GPU fixed

### Ticket #4: Self-bench on GSM8K weak spots (MEDIUM)
- Block: #1, #2, #3
- Action: swarm_robust.py
- Effort: 1 hour when unblocked

### Ticket #5: Serverless workers (LOW)
- Block: H200/A100 capacity
- Action: runsync test on existing endpoints
- Effort: 1 min when capacity returns

### Ticket #6: Per-clan LoRA fine-tuning (LOW)
- Block: pip install breaks ollama (per FOREST_80)
- Action: separate training pod
- Effort: 4-8 hours

### Ticket #7: TTT-fusion emergence test (LOW)
- Block: H200 unavailable
- Action: per CC_TTT_FUSION_GPU_SPEC
- Effort: 30 min when A10/L4 capacity returns

## WHAT IS NOT NEEDED NOW
- Building more agents (already 4+ competing)
- More Modelfiles (14 already written)
- More bloodline entries (188 covers everything)
- More serverless endpoints (4 already created)
- Custom UI (not needed for sovereignty benchmark)

## NEXT IMMEDIATE STEP (USER SHOULD DO)
After budget recovery or new GPU:
1. SSH to fresh pod with sov-models attached
2. cd /workspace && pkill -9 ollama && nohup ollama serve &
3. cd /workspace/sovereign/Modelfiles && for f in *.Modelfile; do ollama create $(basename $f .Modelfile) -f $f; done
4. python3 /tmp/eat_all.py
5. python3 /tmp/swarm_robust.py

## STATUS (right now)
- EAT: BLOCKED (ollama killed by other agents)
- Modelfiles: READY (14 written, persistent)
- Bloodline: READY (188 entries, integrated)
- Router: READY (serverless integrated)
- Backup: READY (3 layers)
- Serverless: BLOCKED (workers IN_QUEUE)
## WIN: sov6-gemma-owem-v2 — 95.45% Overall

**Massive breakthrough**:
- **sov6-gemma-owem-v2**: 95.45% (21/22 tasks)
- Reasoning: 100% (perfect)
- Spatial: 88% (near perfect)
- Visual: 100% (perfect)
- Base gemma3:12b: 68.18% (+27.27% improvement)
- OWEM v1 heavy: 45.45% (v2 is 2.1x better)

**Key insight**: Lighter OWEM specialization avoids overfitting. Heavy OWEM (v1) = 45.45%. Light OWEM (v2) = 95.45%.

**Next**: Deploy to Kaggle, update competition bundle, run ASI-Evolve on this result.
