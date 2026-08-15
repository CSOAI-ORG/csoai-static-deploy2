# OWEM Cluster Quantization & Optimization Plan

## Current State
- Base model: Qwen2.5 0.5B (494M params, Q4_K_M)
- 12 OWEM families (logic, ethics, aesthetics, etc.)
- Oracle ARM: 4 OCPUs, 24GB RAM (CPU only)
- Free GPU tiers: Kaggle T4, Colab T4, Lightning T4, HF T4

## Quantization Levels

### Q4_K_M (Current)
- Size: ~397MB
- Quality: Good
- Speed: Moderate

### Q4_0 (Faster)
- Size: ~300MB
- Quality: Slightly lower
- Speed: 20-30% faster

### Q4_K_S (Balanced)
- Size: ~350MB
- Quality: Good
- Speed: 15% faster

### Q5_K_S (Higher Quality)
- Size: ~450MB
- Quality: Better
- Speed: 10% slower

### Q8_0 (Highest Quality)
- Size: ~600MB
- Quality: Best
- Speed: 30% slower

## Optimization Strategy

### Phase 1: Quantize OWEM Specialists
Create optimized quantization for each OWEM family:

```bash
# For each OWEM specialist
ollama create sov33-logic-q4 -f Modelfile.logic
ollama create sov33-ethics-q4 -f Modelfile.ethics
ollama create sov33-aesthetics-q4 -f Modelfile.aesthetics
# ... etc for all 12
```

### Phase 2: Mixture of Experts Routing
Instead of one big model, use multiple tiny specialists:

```python
# Route queries to appropriate specialist
def route_query(query):
    if "logic" in query or "reasoning" in query:
        return "sov33-logic-q4"
    elif "ethics" in query or "safety" in query:
        return "sov33-ethics-q4"
    elif "code" in query:
        return "sov33-code-q4"
    # ... etc
```

### Phase 3: Oracle GPU Training
Use Oracle's $300 free credits for GPU training:

1. Sign up for Oracle Cloud free tier
2. Request GPU quota (A10 or H100)
3. Train LoRA adapters on GPU
4. Export quantized models

### Phase 4: Continuous Optimization
Monitor and optimize based on usage patterns:

```python
# Track which specialists are used most
usage_stats = {
    "logic": 45,
    "ethics": 30,
    "code": 25,
    # ...
}
# Optimize frequently used specialists
```

## Implementation

### Step 1: Create Quantized Modelfiles
```bash
# For each OWEM specialist
for specialist in logic ethics aesthetics temporality identity agency relationality embodiment abstraction synthesis destruction preservation; do
  cat > Modelfile.${specialist} << EOF
FROM qwen2.5:0.5b
SYSTEM "You are SOV33-${specialist^}, specialist in ${specialist}."
PARAMETER temperature 0
PARAMETER num_predict 128
EOF
  ollama create sov33-${specialist}-q4 -f Modelfile.${specialist}
done
```

### Step 2: Create Routing System
```python
#!/usr/bin/env python3
"""OWEM Router — routes queries to appropriate specialist."""
import json
import urllib.request

SPECIALISTS = {
    "logic": "sov33-logic-q4",
    "ethics": "sov33-ethics-q4",
    "aesthetics": "sov33-aesthetics-q4",
    "code": "sov33-code-q4",
    "math": "sov33-math-q4",
    "governance": "sov33-governance-q4",
    "security": "sov33-security-q4",
    "defence": "sov33-defence-q4",
}

def route_query(query):
    """Route query to appropriate specialist."""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["logic", "reasoning", "think"]):
        return SPECIALISTS["logic"]
    elif any(word in query_lower for word in ["ethics", "moral", "right", "wrong"]):
        return SPECIALISTS["ethics"]
    elif any(word in query_lower for word in ["code", "python", "program"]):
        return SPECIALISTS["code"]
    elif any(word in query_lower for word in ["math", "calculate", "number"]):
        return SPECIALISTS["math"]
    elif any(word in query_lower for word in ["governance", "compliance", "eu ai"]):
        return SPECIALISTS["governance"]
    elif any(word in query_lower for word in ["security", "hack", "protect"]):
        return SPECIALISTS["security"]
    elif any(word in query_lower for word in ["defence", "military", "army"]):
        return SPECIALISTS["defence"]
    else:
        return "sov33-ultimate-sovereign"

def call_model(model, prompt):
    """Call Ollama model."""
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "num_predict": 128}
    }).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("response", "")
```

### Step 3: Oracle GPU Training
```bash
#!/bin/bash
# oracle_gpu_train.sh — Train on Oracle GPU
set -euo pipefail

# Sign up for Oracle Cloud free tier
# https://www.oracle.com/cloud/free/

# Request GPU quota
# https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm#bm-gpu

# Launch GPU instance
oci compute instance launch \
  --availability-domain "xxxxx" \
  --compartment-id "xxxxx" \
  --shape "VM.GPU.A10.1" \
  --image-id "ocid1.image.oc1..xxxxx" \
  --subnet-id "xxxxx" \
  --ssh-authorized-keys-file ~/.ssh/id_rsa.pub

# SSH into instance
ssh opc@<instance-ip>

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull and train
ollama pull qwen2.5:0.5b
# ... training commands
```

## Expected Results

### Before Optimization
- Single model: 397MB
- All queries go through one model
- No specialization

### After Optimization
- 12 specialists: ~50MB each (600MB total)
- Queries routed to appropriate specialist
- 2-3x faster inference
- Better quality on specialized tasks

## Cost Analysis

### Oracle Free Tier
- $300 free credits
- Enough for ~50 hours of A10 GPU
- Enough for ~10 hours of H100 GPU

### Ongoing Costs
- Oracle ARM: Always free (4 OCPU, 24GB RAM)
- Kaggle T4: 30 hours/week free
- Colab T4: 12 hours/session free
- Lightning T4: 22 hours/month free

## Next Steps

1. [ ] Create quantized Modelfiles for all 12 OWEM specialists
2. [ ] Implement routing system
3. [ ] Sign up for Oracle Cloud free tier
4. [ ] Request GPU quota
5. [ ] Train LoRA adapters on GPU
6. [ ] Deploy optimized cluster
7. [ ] Monitor and optimize
