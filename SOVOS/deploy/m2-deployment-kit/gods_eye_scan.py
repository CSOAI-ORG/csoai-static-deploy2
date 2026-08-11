#!/usr/bin/env python3
"""
gods_eye_scan.py — Omniscient scan of SOV3 substrate health.

Usage:
  python3 gods_eye_scan.py
  python3 gods_eye_scan.py --format json
"""
import json, sys, argparse, os, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def scan():
    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "checks": {}
    }

    html_count = len(list(ROOT.glob("*.html")))
    results["checks"]["html_pages"] = {"count": html_count, "status": "ok" if html_count > 100 else "warn"}

    python_count = len(list(ROOT.glob("*.py")))
    results["checks"]["python_files"] = {"count": python_count, "status": "ok"}

    rag_count = len(list((ROOT / "benchmark-results" / "rag").glob("*.md"))) if (ROOT / "benchmark-results" / "rag").exists() else 0
    results["checks"]["rag_corpora"] = {"count": rag_count, "status": "ok" if rag_count >= 10 else "warn"}

    registry = ROOT / "sovereign-charters" / "sov33-capability-registry.json"
    results["checks"]["capability_registry"] = {"exists": registry.exists(), "status": "ok" if registry.exists() else "error"}

    return results

def main():
    parser = argparse.ArgumentParser(description="God's Eye Scan")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    results = scan()

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print("God's Eye Scan Results:")
        for check, data in results["checks"].items():
            status = "✓" if data["status"] == "ok" else "⚠" if data["status"] == "warn" else "✗"
            print(f"  {status} {check}: {data}")

if __name__ == "__main__":
    main()
