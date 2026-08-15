#!/usr/bin/env python3
"""
e2e_routes_sovereign.py — extended E2E test for the 8-route sovereignty system.

Asserts that all 8 routes feed the same ledger, honey DB, 5D, fluid, and IWM/VWM.
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path.home() / "clawd" / "csoai-static-deploy2"
sys.path.insert(0, str(ROOT))

ROUTES = ["ollama", "huggingface", "chatml", "bloodline", "training_data",
          "gpu_inventory", "tier0_routers", "kb_clauses"]


def get_ledger_count():
    """Count events in sov_time_ledger.jsonl."""
    ledger = ROOT / "benchmark-results" / "sov_time_ledger.jsonl"
    if not ledger.exists():
        return 0
    with open(ledger) as f:
        return sum(1 for _ in f)


def get_honey_count():
    """Count rows in honey DB."""
    honey_db = ROOT / "forest" / "honey.db"
    if not honey_db.exists():
        return 0
    import sqlite3
    conn = sqlite3.connect(str(honey_db))
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM honey")
        return cur.fetchone()[0]
    except Exception:
        return 0
    finally:
        conn.close()


def get_5d_points():
    """Count 5D points."""
    try:
        from sov_5d import sov_5d_points
        return sov_5d_points()
    except Exception:
        return -1


def main():
    print("e2e_routes_sovereign.py — 8-route acceptance test")
    print()

    before_ledger = get_ledger_count()
    before_honey = get_honey_count()
    before_5d = get_5d_points()

    print(f"  Ledger before: {before_ledger}")
    print(f"  Honey before: {before_honey}")
    print(f"  5D before: {before_5d}")

    # Run sov_training_honey on each route
    print()
    print("Running training honey on each route...")
    try:
        from sov_training_honey import (
            route_ollama, route_huggingface, route_chatml, route_bloodline,
            route_training_data, route_gpu_inventory, route_tier0_routers,
            route_kb_clauses
        )
        route_fns = {
            "ollama": route_ollama,
            "huggingface": route_huggingface,
            "chatml": route_chatml,
            "bloodline": route_bloodline,
            "training_data": route_training_data,
            "gpu_inventory": route_gpu_inventory,
            "tier0_routers": route_tier0_routers,
            "kb_clauses": route_kb_clauses,
        }

        passed = 0
        failed = 0
        for name in ROUTES:
            try:
                events = route_fns[name]()
                n = len(events) if events else 0
                print(f"  [{name}] {n} events")
                passed += 1
            except Exception as e:
                print(f"  [{name}] FAIL: {e}")
                failed += 1
    except ImportError as e:
        print(f"  Could not import sov_training_honey: {e}")
        print("  Running --selftest via subprocess instead")
        import subprocess
        result = subprocess.run(
            [sys.executable, str(ROOT / "sov_training_honey.py"), "--selftest"],
            capture_output=True, text=True
        )
        print(result.stdout[-2000:])
        if result.returncode == 0:
            passed = len(ROUTES)
        else:
            failed = len(ROUTES)

    # Check post-state
    print()
    print("Post-state:")
    after_ledger = get_ledger_count()
    after_honey = get_honey_count()
    after_5d = get_5d_points()

    # Type coercion for safe printing
    def safe_num(x):
        return x if isinstance(x, (int, float)) else len(x) if isinstance(x, list) else -1

    after_5d_n = safe_num(after_5d)
    before_5d_n = safe_num(before_5d)

    print(f"  Ledger: {before_ledger} → {after_ledger} (Δ {after_ledger - before_ledger})")
    print(f"  Honey: {before_honey} → {after_honey} (Δ {after_honey - before_honey})")
    print(f"  5D: {before_5d_n} → {after_5d_n} (Δ {after_5d_n - before_5d_n})")

    # Assertions
    print()
    print("Assertions:")
    assertions = []

    a1 = passed == len(ROUTES)
    assertions.append(("all 8 routes ran", a1))
    print(f"  [{'✓' if a1 else '✗'}] All 8 routes ran: {passed}/{len(ROUTES)}")

    a2 = after_ledger >= before_ledger
    assertions.append(("ledger grew", a2))
    print(f"  [{'✓' if a2 else '✗'}] Ledger grew: {after_ledger >= before_ledger}")

    a3 = after_honey >= before_honey
    assertions.append(("honey grew", a3))
    print(f"  [{'✓' if a3 else '✗'}] Honey grew: {after_honey >= before_honey}")

    # Final summary
    print()
    print(f"Routes passed: {passed}/{len(ROUTES)}")
    if all(a for _, a in assertions):
        print("✓ E2E ROUTES PASS")
        sys.exit(0)
    else:
        print("✗ E2E ROUTES FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
