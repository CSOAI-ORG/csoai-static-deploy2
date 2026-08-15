#!/usr/bin/env python3
"""
results_sync.py — Pull results from all GPU platforms, push to SovTime.

Pulls GovBench results from:
- Local Ollama (OWEM flywheel)
- Kaggle T4 (parallel benchmarks)
- Groq (fast inference)
- Modal (serverless GPU)
- Oracle ARM (light CPU tasks)

Pushes all results to SovTime ledger.

Usage:
  python3 results_sync.py --all
  python3 results_sync.py --platform kaggle_t4

Output:
  - Consolidated results from all platforms
  - Results pushed to SovTime ledger
  - Summary report
"""

import json
import hashlib
import glob
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# SovTime configuration
GATEWAY_KEY = "7cb80764e3e915903752181c0fa21798e3f5ec2472e98d6930d797d420055624"
SOV_TIME_URL = "http://localhost:8080/sov-time"

# Result file paths
RESULT_PATHS = {
    "local": "/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/govbench/*latest*.json",
    "kaggle_t4": "/Users/nicholas/clawd/csoai-static-deploy2/kaggle_results/**/*.json",
    "groq": "/Users/nicholas/clawd/csoai-static-deploy2/groq_results.json",
    "modal": "/Users/nicholas/clawd/csoai-static-deploy2/modal_results.json",
    "oracle_arm": "/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/govbench/*latest*.json",
}

def load_results(platform: str) -> list:
    """Load results from a specific platform."""
    path_pattern = RESULT_PATHS.get(platform)
    if not path_pattern:
        return []
    
    results = []
    for path in glob.glob(path_pattern, recursive=True):
        try:
            with open(path) as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Single result
                    if "model" in data:
                        results.append(data)
                    # Array of results
                    elif "results" in data:
                        results.extend(data["results"])
        except (json.JSONDecodeError, IOError) as e:
            print(f"  Error loading {path}: {e}")
    
    return results

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
            'origin': 'results_sync',
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
        return True
    except Exception as e:
        print(f"  SovTime push failed: {e}")
        return False

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Results sync")
    parser.add_argument("--all", action="store_true", help="Sync all platforms")
    parser.add_argument("--platform", type=str, help="Specific platform to sync")
    parser.add_argument("--output", type=str, default="sync_results.json", help="Output file")
    args = parser.parse_args()
    
    platforms = []
    if args.all:
        platforms = list(RESULT_PATHS.keys())
    elif args.platform:
        platforms = [args.platform]
    else:
        print("Error: specify --all or --platform")
        sys.exit(1)
    
    all_results = []
    for platform in platforms:
        print(f"\n{'='*60}")
        print(f"Syncing: {platform}")
        print(f"{'='*60}")
        
        results = load_results(platform)
        print(f"  Loaded {len(results)} results")
        
        # Push to SovTime
        pushed = 0
        for result in results:
            if push_to_sovtime(result, platform):
                pushed += 1
        
        print(f"  Pushed {pushed}/{len(results)} to SovTime")
        
        all_results.extend([
            {"platform": platform, "result": r} for r in results
        ])
    
    # Save results
    output_path = Path(args.output)
    output_path.write_text(json.dumps({
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'platforms_synced': len(platforms),
        'total_results': len(all_results),
        'results': all_results
    }, indent=2))
    print(f"\nResults saved to {output_path}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(all_results)} results synced from {len(platforms)} platforms")
    print(f"{'='*60}")
    for r in all_results:
        model = r['result'].get('model', '?')
        score = r['result'].get('overall_score', 0)
        print(f"  {model}: {score}% via {r['platform']}")

if __name__ == "__main__":
    main()
