# SOV8 Architecture — Oracle as Data Hub, Kaggle as GPU

## The Problem
Oracle has 956MB RAM. Running 13 Python processes = OOM death.

## The Fix
Oracle = **data store only** (rsync, cron, lightweight)  
Kaggle T4 = **GPU work** (one notebook per task, independent)  
RunPod = **heavy GPU** when needed  
MacBook = **thin client** (no work, just editing)

## Architecture

```
MacBook (thin client)
  │
  ├─ rsync → Oracle (data backup)
  │
  ├─ kaggle kernels push → Kaggle T4 (GPU work)
  │
  └─ opencode (editing only)
  
Oracle (data hub, always-on)
  │
  ├─ Stores all artifacts (98MB+)
  │
  ├─ Cron: rsync from MacBook every hour
  │
  ├─ Cron: check Kaggle status, pull results
  │
  └─ Lightweight: no heavy processes
  
Kaggle T4 (GPU work, free)
  │
  ├─ Notebook 1: Reasoning LoRA training (~4h)
  ├─ Notebook 2: EAT cycle benchmarking (~2h)
  ├─ Notebook 3: Model merging (~1h)
  ├─ Notebook 4: Groq distillation (~1h)
  └─ Notebook 5: Visual synthesis (~30min)
  
RunPod (heavy GPU, when credits available)
  │
  ├─ A40: LoRA training on 7B+ models
  ├─ H100: Full fine-tuning
  └─ 3090: Benchmarking
```

## Rules
1. **Never run heavy processes on Oracle** — it has 956MB RAM
2. **Never run work on MacBook** — use Kaggle/RunPod
3. **All data flows to Oracle** — single source of truth
4. **Kaggle notebooks are independent** — each runs on its own T4
5. **Progress is never lost** — Oracle stores everything

## How to Start
```bash
# On Oracle (lightweight only):
crontab -e
# Add:
# Every hour: rsync from MacBook
# Every 5 min: check Kaggle status
# Daily: pull Kaggle results

# On MacBook:
# Push notebook to Kaggle:
kaggle kernels push -p /tmp/sov7-reasoning-lora

# Check status:
kaggle kernels status nicktempleman/sov7-reasoning-lora

# Pull results when done:
kaggle kernels pull nicktempleman/sov7-reasoning-lora -p /tmp/sov7-results
```
