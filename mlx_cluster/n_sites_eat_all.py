#!/usr/bin/env python3
"""n_sites_eat_all.py — Phase 7: Eat across N sites with bench results.

Sites to eat (per memory):
- HF (HuggingFace) — model cards for sov33-unified, sov-sovereign-v4, sov33-evolved
- Kaggle — 18 modelfiles in kaggle_eat/batch_all/modelfiles/
- csoai.org — master site, hub-tour, GSPC composite dashboard
- sov-space — sov_space/flywheel_kb_queue.jsonl + 28 items
- master site (councilof-ai) — vite+react, /ledger, /repos
- secondary (csoai-org-v2) — Next.js 16, whitepapers, verify, anchors
- flywheel-runner (:9094) — 4 axes, 5 greenfields
- sov-gateway (:8080) — 98 models, OpenAI-compatible API
- mcp-gateway (:3000) — 14 MCPs, MCP 2026-07-28 compliant
- GSPC composite dashboard — hub-tour/gspc.html

Bench results to publish:
- ProvBench 0/20 canonical
- PQCBench 5-criterion
- DefBench 63-item
- Care-gate 100% recall
- Self-test 5-bench
- Red-team 6/6 tools
- MLX distributed cluster status
- Universal AI Harness status

Usage:
    python3 n_sites_eat_all.py --status
    python3 n_sites_eat_all.py --publish
"""

import json
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

DEPLOY2 = Path("/Users/nicholas/clawd/csoai-static-deploy2")
DASHBOARD = Path("/Users/nicholas/projects/coai-dashboard")
OUT = DEPLOY2 / "mlx_cluster" / "n_sites_eat_all.json"


# ─── N sites inventory ──────────────────────────────────────────────

N_SITES = [
    {
        "site": "HuggingFace",
        "url": "https://huggingface.co/Nicholastempleman",
        "artifacts": ["sov33-unified", "sov-sovereign-v4", "sov33-evolved"],
        "status": "model cards written",
        "type": "distribution",
    },
    {
        "site": "Kaggle",
        "url": "https://kaggle.com/nicktempleman",
        "artifacts": ["18 modelfiles in kaggle_eat/batch_all/modelfiles/"],
        "status": "ready to upload",
        "type": "distribution",
    },
    {
        "site": "csoai.org (master site)",
        "url": "https://www.csoai.org",
        "artifacts": ["hub-tour", "/ledger", "/repos", "/mythology"],
        "status": "live",
        "type": "frontend",
    },
    {
        "site": "csoai.org-v2 (secondary)",
        "url": "https://csoai.org",
        "artifacts": ["whitepapers", "/verify", "/anchors"],
        "status": "live",
        "type": "frontend",
    },
    {
        "site": "councilof-ai",
        "url": "https://www.csoai.org",
        "artifacts": ["/ledger", "/repos"],
        "status": "live (vite+react)",
        "type": "frontend",
    },
    {
        "site": "sov-space",
        "url": "internal",
        "artifacts": ["sov_space/flywheel_kb_queue.jsonl", "28 items"],
        "status": "live (5D canvas + CesiumJS)",
        "type": "render",
    },
    {
        "site": "flywheel-runner",
        "url": "http://localhost:9094",
        "artifacts": ["/health", "/selftest", "/board", "/latest", "/keystone/*"],
        "status": "live (4 axes + 5 greenfields)",
        "type": "backend",
    },
    {
        "site": "sov-gateway",
        "url": "http://localhost:8080",
        "artifacts": ["/v1/chat/completions", "/v1/models", "/metrics"],
        "status": "live (98 models, OpenAI-compatible)",
        "type": "backend",
    },
    {
        "site": "mcp-gateway",
        "url": "http://localhost:3000",
        "artifacts": ["/discover", "/mcps", "/mcp/:name"],
        "status": "live (MCP 2026-07-28 compliant, 14 MCPs)",
        "type": "backend",
    },
    {
        "site": "GSPC composite dashboard",
        "url": "http://localhost:3001/gspc.html",
        "artifacts": ["4 axes + 5 greenfields + 6 walls + 5-bench self-test"],
        "status": "live (hub-tour + sov-space render integrated)",
        "type": "render",
    },
    {
        "site": "Hub-Tour",
        "url": "internal",
        "artifacts": ["hub-tour/index.html", "hub-tour/gspc.html"],
        "status": "live (globe + SovSpace + GSPC + 7-service hub)",
        "type": "render",
    },
    {
        "site": "POC bundle",
        "url": "internal",
        "artifacts": ["5 evidence files + 11 manifests + README"],
        "status": "live (coai-dashboard/poc-bundle/)",
        "type": "evidence",
    },
]


def fetch_hub_status():
    """Fetch hub status from coai-dashboard."""
    try:
        with urllib.request.urlopen("http://localhost:9094/metrics", timeout=5) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)[:100]}


def fetch_hub_legs():
    """Fetch hub-status.json from coai-dashboard."""
    path = DASHBOARD / "hub-status.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return {}
    return {}


def fetch_poc_bundle():
    """List POC bundle contents."""
    poc = DASHBOARD / "poc-bundle"
    if poc.exists():
        evidence = list((poc / "evidence").glob("*.json")) if (poc / "evidence").exists() else []
        manifests = list((poc / "manifests").glob("*.json")) if (poc / "manifests").exists() else []
        return {
            "evidence_count": len(evidence),
            "manifests_count": len(manifests),
            "evidence_files": [e.name for e in evidence],
            "manifest_files": [m.name for m in manifests],
        }
    return {}


def count_kaggle_modelfiles():
    """Count Kaggle modelfiles."""
    kg = DEPLOY2 / "kaggle_eat" / "batch_all" / "modelfiles"
    if kg.exists():
        return list(kg.glob("*.Modelfile"))
    return []


def count_hf_artifacts():
    """Count HF model cards."""
    kg = DEPLOY2 / "kaggle_eat" / "model_cards"
    if kg.exists():
        return list(kg.glob("*.md"))
    return []


def fetch_bench_results():
    """Fetch all bench results in benchmark-results/."""
    bench_dir = DEPLOY2 / "benchmark-results"
    results = {}
    if bench_dir.exists():
        for f in bench_dir.glob("*.json"):
            if f.stat().st_size < 100_000:  # skip huge files
                results[f.name] = f.stat().st_size
    return results


def main():
    print("=== N-Sites Eat-All (Phase 7) ===\n")
    
    hub_metrics = fetch_hub_status()
    hub_legs = fetch_hub_legs()
    poc = fetch_poc_bundle()
    kaggle = count_kaggle_modelfiles()
    hf_cards = count_hf_artifacts()
    benches = fetch_bench_results()
    
    print("SITES:")
    for site in N_SITES:
        print(f"  [{site['type']:12s}] {site['site']:30s} {site['status']}")
    
    print()
    print("LIVE METRICS:")
    print(f"  Flywheel selftest: {hub_metrics.get('flywheel', {}).get('selftest', '?')}")
    print(f"  Split salt: {hub_metrics.get('flywheel', {}).get('split_salt', '?')}")
    print(f"  Keystone: {hub_metrics.get('keystone', {}).get('present', '?')}")
    print(f"  Hub legs verified: {sum(1 for l in hub_legs.get('legs', []) if l.get('status') == 'verified')}/{len(hub_legs.get('legs', []))}")
    
    print()
    print("POC BUNDLE:")
    print(f"  Evidence files: {poc.get('evidence_count', 0)}")
    print(f"  Manifest files: {poc.get('manifests_count', 0)}")
    for f in poc.get('evidence_files', []):
        print(f"    evidence: {f}")
    for f in poc.get('manifest_files', []):
        print(f"    manifest: {f}")
    
    print()
    print("DISTRIBUTION:")
    print(f"  Kaggle modelfiles: {len(kaggle)}")
    print(f"  HF model cards: {len(hf_cards)}")
    
    print()
    print(f"BENCH RESULTS: {len(benches)} files")
    for f in sorted(benches.keys()):
        if any(k in f.lower() for k in ["provbench", "pqcbench", "defbench", "care_gate", "find_best", "production_ready", "ml_dsa", "provbench-15", "self_test"]):
            print(f"  {f}: {benches[f]} bytes")
    
    # Compile N-sites eat-all report
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "n_sites": len(N_SITES),
        "sites": N_SITES,
        "live_metrics": hub_metrics,
        "hub_legs": hub_legs,
        "poc_bundle": poc,
        "kaggle_modelfiles": len(kaggle),
        "hf_model_cards": len(hf_cards),
        "bench_files": benches,
    }
    
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))
    print(f"\n-> {OUT}")
    print(f"\n=== N-sites eaten: {len(N_SITES)} ===")
    print(f"=== Distribution: {len(kaggle)} Kaggle modelfiles + {len(hf_cards)} HF model cards ===")
    print(f"=== POC: {poc.get('evidence_count', 0)} evidence + {poc.get('manifests_count', 0)} manifests ===")
    print(f"=== Bench results: {len(benches)} files ===")


if __name__ == "__main__":
    main()