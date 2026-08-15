#!/usr/bin/env python3
"""
owem_scheduler.py — Auto-route models to cheapest available GPU.

Routes GovBench evaluation to the cheapest available free GPU platform:
1. Kaggle T4 (30h/week free) — first choice for parallel benchmarks
2. Groq (30 RPM free) — fast inference for lightweight probes
3. Modal ($30/mo credit) — serverless GPU for burst capacity
4. Oracle ARM (always free) — light CPU tasks
5. RunPod A100 ($1.39/hr spot) — heavy training, backup

Usage:
  python3 owem_scheduler.py --models-file clan_models.txt
  python3 owem_scheduler.py --model clan-sovereignty-refusing:latest

Output:
  - Routes models to cheapest available GPU
  - Results pushed to SovTime ledger
  - Summary report
"""

import json
import hashlib
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# SovTime configuration
GATEWAY_KEY = "7cb80764e3e915903752181c0fa21798e3f5ec2472e98d6930d797d420055624"
SOV_TIME_URL = "http://localhost:8080/sov-time"

# GPU platform availability
GPU_PLATFORMS = {
    "kaggle_t4": {"cost": 0, "limit": "30h/week", "available": True},
    "groq": {"cost": 0, "limit": "30 RPM", "available": True},
    "modal": {"cost": 30, "limit": "$30/mo credit", "available": True},
    "oracle_arm": {"cost": 0, "limit": "always free", "available": True},
    "runpod_a100": {"cost": 1.39, "limit": "spot pricing", "available": False},
}

def get_cheapest_platform() -> str:
    """Get the cheapest available GPU platform."""
    available = [
        (name, info) for name, info in GPU_PLATFORMS.items()
        if info["available"]
    ]
    
    if not available:
        return None
    
    # Sort by cost (0 first), then by limit (prefer unlimited)
    available.sort(key=lambda x: (x[1]["cost"], x[1]["limit"]))
    return available[0][0]

def route_to_platform(model: str, platform: str) -> dict:
    """Route model evaluation to a specific platform."""
    print(f"Routing {model} to {platform}...")
    
    if platform == "kaggle_t4":
        # Use Kaggle T4 for parallel benchmarks
        result = subprocess.run(
            ["python3", "govbench_kaggle.py", "--model", model],
            capture_output=True, text=True, timeout=600
        )
    elif platform == "groq":
        # Use Groq for fast inference
        result = subprocess.run(
            ["python3", "govbench_groq.py", "--model", model],
            capture_output=True, text=True, timeout=60
        )
    elif platform == "modal":
        # Use Modal for serverless GPU
        result = subprocess.run(
            ["python3", "govbench_modal.py", "--model", model],
            capture_output=True, text=True, timeout=600
        )
    elif platform == "oracle_arm":
        # Use Oracle ARM for light CPU tasks
        result = subprocess.run(
            ["python3", "govbench_eval.py", "--model", model, "--provider", "ollama"],
            capture_output=True, text=True, timeout=300
        )
    else:
        print(f"Unknown platform: {platform}")
        return None
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    
    # Parse the result
    try:
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.startswith('{'):
                return json.loads(line)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        return None
    
    return None

def push_to_sovtime(result: dict, platform: str) -> bool:
    """Push result to SovTime ledger."""
    try:
        model = result.get('model', '?')
        score = result.get('overall_score', 0)
        gov = result.get('dimensions', {}).get('governance', 0)
        safety = result.get('dimensions', {}).get('safety', 0)
        q_hash = hashlib.sha256(model.encode()).hexdigest()[:16]
        
        stamp = {
            'space': 'C',
            'kind': 'govbench-result',
            'stage': f'govbench.{platform}',
            'origin': 'owem_scheduler',
            'status': 'verified',
            'detail': f'{model} GovBench={score}% Gov={gov}% Safety={safety}% via {platform}',
            'full_answer': json.dumps(result.get('dimensions', {})),
            'source': platform,
            'q_hash': q_hash,
            'verified': True
        }
        
        body = json.dumps(stamp).encode()
        req = urllib.request.Request(
            SOV_TIME_URL,
            data=body,
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {GATEWAY_KEY}'
            }
        )
        resp = urllib.request.urlopen(req, timeout=5)
        result = json.loads(resp.read())
        print(f"  Pushed to SovTime: {result.get('id', '?')[:8]}")
        return True
    except Exception as e:
        print(f"  SovTime push failed: {e}")
        return False

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="OWEM scheduler")
    parser.add_argument("--model", type=str, help="Model to benchmark")
    parser.add_argument("--models-file", type=str, help="File with model list")
    parser.add_argument("--output", type=str, default="owem_scheduler_results.json", help="Output file")
    args = parser.parse_args()
    
    models = []
    if args.model:
        models = [args.model]
    elif args.models_file:
        with open(args.models_file) as f:
            models = [line.strip() for line in f if line.strip()]
    else:
        print("Error: specify --model or --models-file")
        sys.exit(1)
    
    results = []
    for model in models:
        print(f"\n{'='*60}")
        print(f"Scheduling: {model}")
        print(f"{'='*60}")
        
        # Get cheapest available platform
        platform = get_cheapest_platform()
        if not platform:
            print("Error: no available GPU platforms")
            break
        
        print(f"  Selected platform: {platform}")
        
        # Route to platform
        result = route_to_platform(model, platform)
        if result:
            results.append({
                "model": model,
                "platform": platform,
                "result": result
            })
            
            # Push to SovTime
            push_to_sovtime(result, platform)
            
            # Print summary
            score = result.get('overall_score', 0)
            print(f"  Overall: {score}%")
        else:
            print(f"  Failed to benchmark {model}")
    
    # Save results
    output_path = Path(args.output)
    output_path.write_text(json.dumps({
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'models_scheduled': len(results),
        'results': results
    }, indent=2))
    print(f"\nResults saved to {output_path}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(results)}/{len(models)} models scheduled")
    print(f"{'='*60}")
    for r in results:
        print(f"  {r['model']}: {r['result'].get('overall_score', 0)}% via {r['platform']}")

if __name__ == "__main__":
    main()
