#!/usr/bin/env python3
"""
consolidate_and_deploy.py — SOV33 Benchmark Consolidation & Deployment

Loads all results from benchmark-results/, consolidates into a single report,
checks for gaps and weaknesses, auto-fixes common issues, generates a
deploy-ready status, and optionally triggers Vercel deployment.

Usage:
  python3 benchmark-results/consolidate_and_deploy.py
  python3 benchmark-results/consolidate_and_deploy.py --report
  python3 benchmark-results/consolidate_and_deploy.py --deploy
  python3 benchmark-results/consolidate_and_deploy.py --fix
  python3 benchmark-results/consolidate_and_deploy.py --watch
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
BENCH_DIR = ROOT_DIR / "benchmark-results"
RESULTS_DIR = BENCH_DIR / "unified_overnight"
CONSOLIDATED_DIR = BENCH_DIR / "consolidated"
REPORT_FILE = BENCH_DIR / "FULL_CONSOLIDATION_REPORT.json"
REPORT_MD = BENCH_DIR / "FULL_CONSOLIDATION_REPORT.md"
DEPLOY_STATUS_FILE = BENCH_DIR / "deploy_status.json"
SIGIL_LOG = BENCH_DIR / "sigil_chain.log"
LOG_FILE = ROOT_DIR / "consolidate_and_deploy.log"

VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN", "")
VERCEL_PROJECT = os.environ.get("VERCEL_PROJECT", "csoai-static-deploy2")

TARGET_DOMAINS = [
    "eu_ai_act", "defence", "governance", "math", "coding",
    "safety", "reasoning", "agentic", "sovereign",
]
REQUIRED_THRESHOLD = 0.80
TARGET_THRESHOLD = 0.95

for d in [CONSOLIDATED_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ── Logging ────────────────────────────────────────────────────────────────

def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# ── Sigil ──────────────────────────────────────────────────────────────────

def make_sigil(data: Any) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, default=str).encode()
    ).hexdigest()


def log_sigil(event: str, sigil: str) -> None:
    entry = f"{datetime.now(timezone.utc).isoformat()} | {event} | {sigil}\n"
    with open(SIGIL_LOG, "a") as f:
        f.write(entry)


# ── Result Loaders ─────────────────────────────────────────────────────────

def load_all_results() -> list[dict]:
    results: list[dict] = []
    glob_patterns = [
        BENCH_DIR.glob("**/cycle_*_results.json"),
        BENCH_DIR.glob("**/*_benchmark.json"),
        BENCH_DIR.glob("**/*_results.json"),
        BENCH_DIR.glob("**/overnight_run.json"),
        BENCH_DIR.glob("**/final_results.json"),
        BENCH_DIR.glob("**/*report*.json"),
    ]
    seen_paths = set()
    for pattern_group in glob_patterns:
        for path in pattern_group:
            if path in seen_paths:
                continue
            seen_paths.add(path)
            try:
                data = json.loads(path.read_text())
                data["_source"] = str(path.relative_to(ROOT_DIR))
                results.append(data)
            except (json.JSONDecodeError, OSError) as e:
                log(f"  Failed to load {path.name}: {e}")
    log(f"Loaded {len(results)} result files from benchmark-results/")
    return results


def extract_scores(data: dict) -> dict[str, float]:
    scores: dict[str, float] = {}
    for key in list(data.keys()):
        if isinstance(data.get(key), (int, float)):
            if isinstance(data[key], float) and 0 <= data[key] <= 1:
                scores[key] = data[key]
        elif key in ("scores", "results", "domains"):
            sub = data[key]
            if isinstance(sub, dict):
                for k, v in sub.items():
                    if isinstance(v, (int, float)):
                        pct = v if v > 1 else v * 100
                        scores[k] = round(pct, 2)
    if "average" in data:
        avg = data["average"]
        scores["average"] = round(avg if avg > 1 else avg * 100, 2)
    if "best" in data:
        best = data["best"]
        scores["best"] = round(best if best > 1 else best * 100, 2)
    if "best_score" in data:
        bs = data["best_score"]
        scores["best"] = round(bs if bs > 1 else bs * 100, 2)
    return scores


# ── Consolidation Engine ───────────────────────────────────────────────────

class Consolidator:
    def __init__(self, results: list[dict]):
        self.results = results
        self.domain_scores: dict[str, list[float]] = defaultdict(list)
        self.source_map: dict[str, list[str]] = defaultdict(list)
        self.cycle_count = 0
        self.best_overall = 0.0
        self._consolidate()

    def _consolidate(self) -> None:
        for data in self.results:
            source = data.get("_source", "unknown")
            scores = extract_scores(data)
            for domain, score in scores.items():
                if domain in TARGET_DOMAINS or domain == "average":
                    self.domain_scores[domain].append(score)
                    self.source_map[domain].append(source)
            if "cycle" in data:
                self.cycle_count = max(self.cycle_count, int(data["cycle"]))
            best_val = scores.get("best", 0)
            if best_val > self.best_overall:
                self.best_overall = best_val

    def get_domain_summary(self) -> dict[str, dict]:
        summary: dict[str, dict] = {}
        for domain in TARGET_DOMAINS:
            vals = self.domain_scores.get(domain, [])
            if vals:
                summary[domain] = {
                    "mean": round(sum(vals) / len(vals), 2),
                    "max": round(max(vals), 2),
                    "min": round(min(vals), 2),
                    "samples": len(vals),
                    "sources": self.source_map.get(domain, [])[:5],
                }
            else:
                summary[domain] = {
                    "mean": 0.0,
                    "max": 0.0,
                    "min": 0.0,
                    "samples": 0,
                    "sources": [],
                }
        return summary

    def get_gaps(self) -> list[str]:
        gaps = []
        summary = self.get_domain_summary()
        for domain, info in summary.items():
            if info["samples"] == 0:
                gaps.append(f"{domain}: no benchmark data found")
            elif info["max"] < REQUIRED_THRESHOLD * 100:
                gaps.append(f"{domain}: max {info['max']:.1f}% < {REQUIRED_THRESHOLD*100:.0f}%")
        if self.cycle_count == 0:
            gaps.append("No pipeline cycles completed")
        return gaps

    def get_weak_domains(self, threshold: float = REQUIRED_THRESHOLD) -> list[str]:
        weak = []
        summary = self.get_domain_summary()
        for domain in TARGET_DOMAINS:
            info = summary[domain]
            best_val = info["max"] if info["max"] > 0 else info["mean"]
            if best_val < threshold * 100:
                weak.append(domain)
        return weak

    def generate_consolidated_report(self) -> dict:
        domain_summary = self.get_domain_summary()
        gaps = self.get_gaps()
        weak = self.get_weak_domains()
        avg_vals = [v["mean"] for v in domain_summary.values() if v["samples"] > 0]
        overall_mean = round(sum(avg_vals) / len(avg_vals), 2) if avg_vals else 0.0
        max_vals = [v["max"] for v in domain_summary.values() if v["samples"] > 0]
        overall_max = round(max(max_vals), 2) if max_vals else 0.0

        report = {
            "schema": "sov.consolidated-report/v1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycles_completed": self.cycle_count,
            "result_files_loaded": len(self.results),
            "overall_mean": overall_mean,
            "overall_max": overall_max,
            "best_recorded": self.best_overall,
            "target_threshold": TARGET_THRESHOLD * 100,
            "target_reached": overall_max >= TARGET_THRESHOLD * 100,
            "domains": domain_summary,
            "gaps": gaps,
            "weak_domains": weak,
            "readiness": self._assess_readiness(overall_mean, overall_max, gaps, weak),
            "sigil": None,
        }
        report["sigil"] = make_sigil(report)
        return report

    def _assess_readiness(self, mean: float, mx: float,
                          gaps: list, weak: list) -> str:
        if mx >= TARGET_THRESHOLD * 100 and not gaps:
            return "DEPLOY_READY"
        if mx >= REQUIRED_THRESHOLD * 100 and len(weak) <= 2:
            return "NEEDS_REFINEMENT"
        if not gaps and mean >= REQUIRED_THRESHOLD * 100:
            return "TRAINING_CONTINUE"
        return "GAP_ANALYSIS_REQUIRED"

    def summary_markdown(self, report: dict) -> str:
        lines = [
            "# SOV33 Consolidated Benchmark Report",
            "",
            f"**Generated:** {report['timestamp']}",
            f"**Result files loaded:** {report['result_files_loaded']}",
            f"**Pipeline cycles completed:** {report['cycles_completed']}",
            f"**Readiness:** {report['readiness']}",
            f"**Target threshold:** {report['target_threshold']:.0f}%",
            f"**Target reached:** {'YES' if report['target_reached'] else 'NO'}",
            "",
            "## Domain Performance",
            "",
            "| Domain | Mean | Max | Min | Samples | Status |",
            "|--------|------|-----|-----|---------|--------|",
        ]
        for domain in TARGET_DOMAINS:
            info = report["domains"].get(domain, {})
            mean = info.get("mean", 0)
            mx = info.get("max", 0)
            mn = info.get("min", 0)
            samples = info.get("samples", 0)
            if mx >= TARGET_THRESHOLD * 100:
                status = "TARGET"
            elif mx >= REQUIRED_THRESHOLD * 100:
                status = "PASS"
            else:
                status = "WEAK"
            lines.append(
                f"| {domain:20s} | {mean:5.1f}% | {mx:5.1f}% | "
                f"{mn:5.1f}% | {samples:3d} | {status:8s} |"
            )

        lines.extend([
            "",
            f"**Overall Mean:** {report['overall_mean']:.1f}%",
            f"**Overall Max:** {report['overall_max']:.1f}%",
            f"**Best Recorded:** {report['best_recorded']:.1f}%",
            "",
        ])

        if report["gaps"]:
            lines.extend([
                "## Gaps Found",
                "",
            ])
            for gap in report["gaps"]:
                lines.append(f"- {gap}")
            lines.append("")

        if report["weak_domains"]:
            lines.extend([
                "## Weak Domains (below 80%)",
                "",
            ])
            for d in report["weak_domains"]:
                info = report["domains"].get(d, {})
                lines.append(f"- **{d}**: max {info.get('max', 0):.1f}%")
            lines.append("")

        lines.extend([
            "## Recommendations",
            "",
        ])
        readiness = report["readiness"]
        if readiness == "DEPLOY_READY":
            lines.append("- **Ready for deployment** to Vercel and production")
            lines.append("- Run unified_free_pipeline.py to confirm sustained 95%+")
        elif readiness == "NEEDS_REFINEMENT":
            lines.append("- Most domains pass, but some need targeted improvement")
            lines.append(f"- Focus on: {', '.join(report['weak_domains'])}")
            lines.append("- Run 5-10 more pipeline cycles")
        elif readiness == "TRAINING_CONTINUE":
            lines.append("- No gaps found but not yet at target")
            lines.append("- Continue overnight training cycles")
            lines.append("- Generate more domain-specific training data")
        else:
            lines.append("- **Gap analysis required** — run more benchmarks")
            lines.append("- Prioritize domains with no data or low scores")
            lines.append(f"- Critical gaps: {', '.join(report.get('gaps', []))}")

        lines.extend([
            "",
            "---",
            f"**SIGIL:** `{report['sigil']}`",
            "",
        ])
        return "\n".join(lines)


# ── Auto-Fix Engine ────────────────────────────────────────────────────────

FIX_ACTIONS: dict[str, callable] = {}


def register_fix(name: str, func: callable) -> None:
    FIX_ACTIONS[name] = func


def fix_missing_domain_data(domain: str, consolidator: Consolidator) -> bool:
    test_file = BENCH_DIR / "domain_seed" / f"{domain}_baseline.json"
    if not test_file.exists():
        test_file = BENCH_DIR / f"{domain}_baseline.json"
    if not test_file.exists():
        log(f"  No baseline data for {domain}, generating minimal seed")
        seed = {
            "domain": domain,
            "generated": datetime.now(timezone.utc).isoformat(),
            "items": [],
            "note": "auto-generated placeholder — run pipeline to populate",
        }
        Path(BENCH_DIR / f"{domain}_baseline.json").write_text(
            json.dumps(seed, indent=2)
        )
        return True
    return False


def fix_missing_results_directory() -> bool:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    log(f"  Created missing directory: {RESULTS_DIR}")
    return True


def fix_empty_domain_scores(consolidator: Consolidator) -> bool:
    fixed = False
    for domain in TARGET_DOMAINS:
        info = consolidator.get_domain_summary().get(domain, {})
        if info.get("samples", 0) == 0:
            fix_missing_domain_data(domain, consolidator)
            fixed = True
    return fixed


def fix_consolidated_dir() -> bool:
    CONSOLIDATED_DIR.mkdir(parents=True, exist_ok=True)
    return True


register_fix("missing_results_dir", fix_missing_results_directory)
register_fix("empty_domain_scores", fix_empty_domain_scores)
register_fix("missing_consolidated_dir", fix_consolidated_dir)


def auto_fix(consolidator: Consolidator) -> dict[str, bool]:
    log("\n[Auto-Fix] Running repair actions...")
    results: dict[str, bool] = {}
    for name, func in FIX_ACTIONS.items():
        try:
            ok = func(consolidator)
            results[name] = ok
            if ok:
                log(f"  ✓ {name}")
            else:
                log(f"  ✗ {name} — no action needed")
        except Exception as e:
            results[name] = False
            log(f"  ✗ {name} — error: {e}")
    return results


# ── Vercel Deployment ──────────────────────────────────────────────────────

def deploy_to_vercel(report: dict) -> bool:
    if not VERCEL_TOKEN:
        log("  VERCEL_TOKEN not set, skipping deployment")
        return False

    deploy_payload = {
        "timestamp": report["timestamp"],
        "readiness": report["readiness"],
        "overall_mean": report["overall_mean"],
        "overall_max": report["overall_max"],
        "target_reached": report["target_reached"],
        "sigil": report["sigil"],
    }
    DEPLOY_STATUS_FILE.write_text(json.dumps(deploy_payload, indent=2))
    log(f"  Wrote deploy status to {DEPLOY_STATUS_FILE}")

    try:
        result = subprocess.run(
            ["npx", "vercel", "--prod", "--token", VERCEL_TOKEN],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            log("  Vercel deployment successful")
            return True
        else:
            log(f"  Vercel deployment failed: {result.stderr[:300]}")
            return False
    except FileNotFoundError:
        log("  Vercel CLI not found")
        return False
    except subprocess.TimeoutExpired:
        log("  Vercel deployment timed out")
        return False


# ── Watch Mode ─────────────────────────────────────────────────────────────

def watch_mode(interval: int = 60) -> None:
    log(f"Watch mode active — polling every {interval}s")
    last_report = None
    while True:
        try:
            results = load_all_results()
            consolidator = Consolidator(results)
            report = consolidator.generate_consolidated_report()
            if report != last_report:
                log(f"Updated report — mean: {report['overall_mean']:.1f}% "
                     f"max: {report['overall_max']:.1f}% "
                     f"readiness: {report['readiness']}")
                last_report = report
        except Exception as e:
            log(f"Watch error: {e}")
        time.sleep(interval)


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="SOV33 Benchmark Consolidation & Deployment"
    )
    parser.add_argument("--report", action="store_true",
                        help="Generate consolidated report and exit")
    parser.add_argument("--deploy", action="store_true",
                        help="Deploy to Vercel if ready")
    parser.add_argument("--fix", action="store_true",
                        help="Run auto-fix on detected issues")
    parser.add_argument("--watch", action="store_true",
                        help="Watch mode — poll for changes")
    parser.add_argument("--interval", type=int, default=60,
                        help="Poll interval in seconds (default: 60)")
    parser.add_argument("--force-deploy", action="store_true",
                        help="Force deployment regardless of readiness")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    log("=" * 78)
    log("  SOV33 CONSOLIDATION & DEPLOYMENT v1.0")
    log(f"  Target: {TARGET_THRESHOLD*100:.0f}% across {len(TARGET_DOMAINS)} domains")
    log("=" * 78)

    if args.watch:
        watch_mode(args.interval)
        return

    # Load and consolidate
    log("\n[1/4] Loading results...")
    results = load_all_results()
    consolidator = Consolidator(results)

    # Auto-fix
    if args.fix:
        log("\n[2/4] Running auto-fix...")
        fix_results = auto_fix(consolidator)
        fixed_any = any(fix_results.values())
        if fixed_any:
            log("  Re-loading after fixes...")
            results = load_all_results()
            consolidator = Consolidator(results)

    # Generate report
    log("\n[3/4] Generating consolidated report...")
    report = consolidator.generate_consolidated_report()

    domain_summary = consolidator.get_domain_summary()
    log("  Domain Summary:")
    for domain in TARGET_DOMAINS:
        info = domain_summary.get(domain, {})
        mx = info.get("max", 0)
        mn = info.get("mean", 0)
        status = "✓" if mx >= TARGET_THRESHOLD * 100 else "~" if mx >= REQUIRED_THRESHOLD * 100 else "✗"
        log(f"    {status} {domain:20s} mean={mn:5.1f}% max={mx:5.1f}%")

    log(f"\n  Overall Mean: {report['overall_mean']:.1f}%")
    log(f"  Overall Max: {report['overall_max']:.1f}%")
    log(f"  Gaps: {len(report['gaps'])}")
    log(f"  Weak: {len(report['weak_domains'])}")
    log(f"  Readiness: {report['readiness']}")

    # Save report
    REPORT_FILE.write_text(json.dumps(report, indent=2))
    log(f"\n  Report saved: {REPORT_FILE}")

    markdown = consolidator.summary_markdown(report)
    REPORT_MD.write_text(markdown)
    log(f"  Markdown report: {REPORT_MD}")

    log_sigil("consolidation", report["sigil"])
    log(f"  SIGIL: {report['sigil']}")

    # Deploy
    if args.deploy or args.force_deploy:
        log("\n[4/4] Deployment...")
        if report["readiness"] == "DEPLOY_READY" or args.force_deploy:
            ok = deploy_to_vercel(report)
            log(f"  Deployment: {'SUCCESS' if ok else 'FAILED'}")
        else:
            log(f"  Not ready: {report['readiness']}")
            log("  Use --force-deploy to override")
    else:
        log("\n[4/4] Skipped (use --deploy to deploy to Vercel)")

    log("\n" + "=" * 78)
    log("  CONSOLIDATION COMPLETE")
    log(f"  Readiness: {report['readiness']}")
    log(f"  Report: {REPORT_FILE}")
    log("=" * 78)

    return report


if __name__ == "__main__":
    main()
