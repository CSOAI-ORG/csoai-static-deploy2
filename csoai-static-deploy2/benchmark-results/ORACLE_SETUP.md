# Oracle Cloud Free Tier — Quick Setup Guide

## Step 1: Create Account (5 min)
1. Go to https://signup.cloud.oracle.com/
2. Sign up with email + credit card (no charges, just verification)
3. You get $300 credit for 30 days + Always Free services forever

## Step 2: Create Ampere A1 Instance (5 min)
1. Console → Compute → Instances → Create Instance
2. Name: `sov-oracle`
3. Image: Ubuntu 22.04 (ARM64)
4. Shape: `VM.Standard.A1.Flex` — 4 OCPU, 24GB RAM
5. **This is Always Free — no charges ever**
6. Add your SSH key
7. Create

## Step 3: Open Ports
1. Instance → VCN → Security Lists → Add Ingress Rules:
   - Port 22 (SSH) — your IP only
   - Port 8766 (SOV Oracle API) — 0.0.0.0/0

## Step 4: Deploy
```bash
# From your Mac:
export SOV_ORACLE_HOST="YOUR_ORACLE_IP"

# Sync code to Oracle
rsync -rltz -e "ssh -o StrictHostKeyChecking=accept-new" \
  ./ root@$SOV_ORACLE_HOST:/opt/sov-oracle/

# SSH in and set up
ssh root@$SOV_ORACLE_HOST
cd /opt/sov-oracle
bash benchmark-results/oracle_setup.sh

# Start the daemon
systemctl start sov-oracle
systemctl status sov-oracle
```

## Step 5: Sync with RunPod
```bash
# When RunPod is available:
export SOV_RUNPOD_HOST="YOUR_RUNPOD_IP"
export SOV_RUNPOD_PORT="22123"

# Pull benchmarks from RunPod → Oracle
./benchmark-results/oracle_sync.sh pull

# Push state from Oracle → RunPod
./benchmark-results/oracle_sync.sh push
```

## What Runs on Oracle (Always On)
- BFT-33 council orchestration
- SignedMemoryDelta chain (7 deltas, verified)
- ASI evolution cycles (hourly)
- Oracle manifest updates
- Backup rotation (daily)
- Small model serving (qwen2.5:0.5b on CPU)

## What Runs on RunPod (When Available)
- GPU training (LoRA, QLoRA, RWKV-7)
- Large model inference (qwen3-30b, etc.)
- OWEM benchmark suite
- MergeKit model merges
- Multi-clan serving
