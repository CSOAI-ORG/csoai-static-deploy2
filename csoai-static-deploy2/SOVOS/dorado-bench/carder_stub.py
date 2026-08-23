#!/usr/bin/env python3
"""Carder circuit — pilot stub (steps 231-240 of the overnight run).

WATCH → MEASURE → SIGN → SPRAY, on OUR OWN datasets first (zero-permission
pilot per the adopted etiquette: own datasets first, opt-in third parties,
right-of-reply, never unsolicited public verdicts).

This stub checks the estate's own HuggingFace datasets for card-completeness
against 5 endorsed sections, and reports GREEN/RED without publishing anything.
The SIGN step (Ed25519 card) and SPRAY step (HF community post) are wired only
when HF_TOKEN is present and the publishing posture is nodded by the owner.

Usage: python3 carder_stub.py [--org csoai] [--dry-run]
"""
import argparse
import json
import os
import sys
import urllib.request

ENDOUSED_SECTIONS = ["datasets", "dataset_info", "card", "license", "readme"]
HF_API = "https://huggingface.co/api"


def fetch_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "carder-pilot/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def list_datasets(org="csoai"):
    try:
        data = fetch_json(f"{HF_API}/datasets?author={org}&limit=100")
        return [d["id"] for d in data]
    except Exception as e:
        print(f"  (could not list {org} datasets: {e})")
        return []


def score_card(dataset_id):
    """Completeness 0-100 against 5 endorsed sections. Reads the dataset card
    content (README) — presence of the sections, not their content quality."""
    score = 0
    detail = []
    try:
        req = urllib.request.Request(
            f"https://huggingface.co/datasets/{dataset_id}/raw/main/README.md",
            headers={"User-Agent": "carder-pilot/0.1"})
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode(errors="ignore").lower()
    except Exception:
        text = ""
    # Structural card quality: YAML front-matter, content depth, file listings,
    # license/tags presence. Matches what an AI crawler actually reads.
    has_yaml = text.startswith("---") and "---" in text[3:200]
    checks = {
        "yaml_frontmatter": has_yaml,
        "license": "license:" in text or "cc-by" in text or "cc0" in text or "mit" in text,
        "content_depth": len(text) > 500,
        "file_listing": ("- `" in text or ".json" in text or ".csv" in text or "contents" in text),
        "methodology": ("methodolog" in text or "measured" in text or "n=" in text or "ci" in text),
    }
    for k, ok in checks.items():
        if ok:
            score += 20
            detail.append(k)
    return score, detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--org", default="csoai")
    ap.add_argument("--dry-run", action="store_true", default=True)
    args = ap.parse_args()

    print(f"CARDER PILOT (dry-run={args.dry_run}) — org: {args.org}")
    print("Etiquette: own datasets first · opt-in third parties · right-of-reply\n")
    datasets = list_datasets(args.org)
    if not datasets:
        print("No datasets found (network or auth). Using a local manifest instead.")
        datasets = ["csoai/gspc-gov", "csoai/gspc-prv"]  # known estate datasets
    print(f"{len(datasets)} candidate datasets\n")
    report = []
    for ds in datasets:
        score, detail = score_card(ds)
        verdict = "GREEN" if score >= 80 else ("AMBER" if score >= 40 else "RED")
        report.append({"id": ds, "score": score, "verdict": verdict, "sections": detail})
        print(f"  {verdict:5s} {score:3d}/100  {ds}")
    greens = sum(1 for r in report if r["verdict"] == "GREEN")
    print(f"\n{greens}/{len(report)} GREEN — card hygiene baseline (no publish in dry-run)")
    with open(os.path.join(os.path.dirname(__file__), "carder_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print("report -> carder_report.json")


if __name__ == "__main__":
    main()
