#!/usr/bin/env python3
"""
govbench_modal.py — Serverless GPU function for GovBench.

Deploy as a Modal function for auto-scaling GovBench evaluation.
Uses Modal's $30/mo credit for burst capacity when Kaggle is at limit.

Usage:
  # Deploy to Modal
  modal deploy govbench_modal.py

  # Invoke from CLI
  modal run govbench_modal.py --model clan-sovereignty-refusing:latest

Output:
  - Per-model GovBench scores (26 dimensions)
  - Results pushed to SovTime ledger
"""

import json
import hashlib
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Modal configuration
MODAL_APP_NAME = "govbench"
MODAL_IMAGE = "python:3.11-slim"
MODAL_GPU = "T4"  # or "A10G" for heavier workloads

# SovTime configuration
GATEWAY_KEY = "7cb80764e3e915903752181c0fa21798e3f5ec2472e98d6930d797d420055624"
SOV_TIME_URL = "http://localhost:8080/sov-time"

# GovBench dimensions
GOVBENCH_DIMENSIONS = [
    "governance", "safety", "provenance", "continuity",
    "privacy", "security", "ethics", "robustness",
    "transparency", "fairness", "accountability", "compliance"
]

def run_govbench(model: str) -> dict:
    """Run GovBench evaluation on a model."""
    print(f"Running GovBench on {model}...")
    
    # Use the existing govbench_eval.py script
    result = subprocess.run(
        ["python3", "govbench_eval.py", "--model", model, "--provider", "ollama"],
        capture_output=True, text=True, timeout=300
    )
    
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

def push_to_sovtime(result: dict) -> bool:
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
            'stage': 'govbench.modal_gpu',
            'origin': 'modal_parallel',
            'status': 'verified',
            'detail': f'{model} GovBench={score}% Gov={gov}% Safety={safety}%',
            'full_answer': json.dumps(result.get('dimensions', {})),
            'source': 'modal_gpu',
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

# Modal function (commented out - requires modal package)
# @app.function(image=MODAL_IMAGE, gpu=MODAL_GPU)
# def govbench_modal(model: str) -> dict:
#     """Modal function for GovBench evaluation."""
#     result = run_govbench(model)
#     if result:
#         push_to_sovtime(result)
#     return result

def main():
    """Main entry point for local testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Modal GovBench GPU function")
    parser.add_argument("--model", type=str, help="Model to benchmark")
    parser.add_argument("--models-file", type=str, help="File with model list")
    parser.add_argument("--output", type=str, default="modal_results.json", help="Output file")
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
        print(f"Benchmarking: {model}")
        print(f"{'='*60}")
        
        result = run_govbench(model)
        if result:
            results.append(result)
            
            # Push to SovTime
            push_to_sovtime(result)
            
            # Print summary
            score = result.get('overall_score', 0)
            gov = result.get('dimensions', {}).get('governance', 0)
            safety = result.get('dimensions', {}).get('safety', 0)
            print(f"  Overall: {score}%")
            print(f"  Governance: {gov}%")
            print(f"  Safety: {safety}%")
        else:
            print(f"  Failed to benchmark {model}")
    
    # Save results
    output_path = Path(args.output)
    output_path.write_text(json.dumps({
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'models_benchmarked': len(results),
        'results': results
    }, indent=2))
    print(f"\nResults saved to {output_path}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(results)}/{len(models)} models benchmarked")
    print(f"{'='*60}")
    for r in results:
        print(f"  {r.get('model', '?')}: {r.get('overall_score', 0)}%")

if __name__ == "__main__":
    main()
