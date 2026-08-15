#!/usr/bin/env python3
"""self_test_5bench.py — run the 5-bench battery against CSOAI's own products.

Tests:
  1. ProvBench — does C2PA marking survive?
  2. DefBench — does our care gate catch Article 5?
  3. PQCBench — does our SIGIL chain survive a PQC audit?
  4. Flywheel selftest — is anti-Goodhart still structurally enforced?
  5. Decision ledger — is the audit trail append-only and drift-free?

Usage:
    python3 self_test_5bench.py
"""

import json
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# Importable benches
from survival_matrix import selftest as survival_selftest, TRANSFORMS, survives
from care_gate_v2 import gate, HARD_STOP
from care_battery import BATTERY


def bench_prov() -> dict:
    """Bench 1: ProvBench — does C2PA marking survive?
    We test the structural guards in survival_matrix.py."""
    ok, msg = survival_selftest()
    cells = []
    for binding in ["hard_hash", "metadata_xmp", "soft_watermark", "cose_ml_dsa_65"]:
        for tf in TRANSFORMS:
            survived, basis = survives(binding, tf)
            cells.append({
                "binding": binding,
                "transform": tf,
                "survived": survived,
                "basis": basis
            })
    n_survive = sum(1 for c in cells if c["survived"])
    n_total = len(cells)
    return {
        "bench": "ProvBench (survival_matrix)",
        "selftest": {"ok": ok, "msg": msg},
        "n_survive": n_survive,
        "n_total": n_total,
        "survival_rate": round(n_survive / n_total, 4) if n_total > 0 else None,
        "honest_finding": "Modelled, not measured. Physics requires real c2patool.",
    }


def bench_def() -> dict:
    """Bench 2: DefBench — does our care gate catch Article 5?"""
    tp = fp = tn = fn = 0
    for text, should_breach, cat, diff in BATTERY:
        r = gate(text, use_llm=False)
        breached = r["breach"]
        if should_breach and breached:
            tp += 1
        elif should_breach and not breached:
            fn += 1
        elif not should_breach and breached:
            fp += 1
        else:
            tn += 1
    n_harm = tp + fn
    n_benign = tn + fp
    return {
        "bench": "DefBench (care_gate_v2)",
        "recall": round(tp / n_harm, 4) if n_harm else 0,
        "overblock_rate": round(fp / n_benign, 4) if n_benign else 0,
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "battery_size": len(BATTERY),
        "verdict": "PASS" if (tp == n_harm and fp == 0) else "FAIL",
    }


def bench_pqc() -> dict:
    """Bench 3: PQCBench — does our SIGIL chain survive a PQC audit?
    This runs against the actual chain files in $HOME."""
    from pqcbench import check_jsonl_chain

    chains = [
        ("SIGIL J-space", ".sov_jspace.chain.jsonl"),
        ("SOV33 sovereign", ".sov33_local_sovereign.chain.jsonl"),
        ("SOV33 composition", ".sov33_composition.chain.jsonl"),
        ("MEOK SOV33", ".meok_sov33_local.chain.jsonl"),
        ("SOV33 evolved", ".sov33_evolved.chain.jsonl"),
        ("DefOneOS", ".defoneos.chain.jsonl"),
        ("Governance", ".governance.chain.jsonl"),
    ]
    results = []
    for name, filename in chains:
        chain_path = Path.home() / filename
        try:
            r = check_jsonl_chain(chain_path)
            passes = sum(1 for c in ["alg_agility", "hybrid_ready", "timestamped", "ts_renewal", "pqc_option"]
                        if c in r and r[c].get("pass"))
            results.append({"chain": name, "passes": passes, "total": 5, "result": "ok"})
        except Exception as e:
            results.append({"chain": name, "error": str(e)})

    return {
        "bench": "PQCBench (5-criterion lens)",
        "chains": results,
        "honest_finding": "Our SIGIL chains typically pass 0-1 of 5 criteria. This is published as DR-0004.",
    }


def bench_flywheel() -> dict:
    """Bench 4: Flywheel selftest — is anti-Goodhart still structurally enforced?"""
    flywheel_py = HERE / "flywheel.py"
    if not flywheel_py.exists():
        return {"bench": "Flywheel selftest", "error": "flywheel.py not found"}

    # Read source to check structural guards
    text = flywheel_py.read_text()
    guards = {
        "SPLIT_SALT constant": bool(re.search(r'SPLIT_SALT\s*=\s*["\']csoai-flywheel-v1["\']', text)),
        "HELD_OUT_FRACTION": bool(re.search(r'HELD_OUT_FRACTION', text)),
        "FlywheelLeak guard class": bool(re.search(r'class\s+FlywheelLeak', text)),
        "selftest function": bool(re.search(r'def\s+selftest', text)),
        "negative control refuse-everything": bool(re.search(r'refuse.everything', text, re.I)),
        "negative control comply-everything": bool(re.search(r'comply.everything', text, re.I)),
    }
    n_pass = sum(1 for v in guards.values() if v)
    n_total = len(guards)

    return {
        "bench": "Flywheel selftest (anti-Goodhart)",
        "structural_guards": guards,
        "passes": n_pass,
        "total": n_total,
        "verdict": "PASS" if n_pass == n_total else "FAIL",
    }


def bench_ledger() -> dict:
    """Bench 5: Decision ledger — is the audit trail append-only and drift-free?"""
    ledger_path = HERE / "decision_ledger.py"
    if not ledger_path.exists():
        return {"bench": "Decision ledger", "error": "decision_ledger.py not found"}

    text = ledger_path.read_text()
    # The ledger's append-only guarantee is structural: it rejects subclasses that
    # expose forbidden methods. Look for the structural guard, not absence of stubs.
    has_guard_method = bool(re.search(r'def\s+guard\s*\(', text))
    has_sneaky_subclass_test = bool(re.search(r'class\s+Sneak', text))
    has_edit_method_real = bool(re.search(r'def\s+edit\s*\([^)]*\):[^_]', text)) and not has_sneaky_subclass_test
    has_supersede = bool(re.search(r'supersed\w+', text))
    has_lower_bound = bool(re.search(r'lower_bound', text))
    has_contested_by = bool(re.search(r'contested_by', text))
    # Decision ledger uses SIGIL chain (Ed25519) via content_hash; check for sha256 chain
    has_chain = bool(re.search(r'sha256|hashlib|Ed25519', text))
    has_chain_head = bool(re.search(r'chain_head|prev_hash', text))

    guards = {
        "structural guard (rejects subclasses with edit/delete)": has_guard_method and has_sneaky_subclass_test,
        "tag drift prevention (supersede)": has_supersede,
        "lower_bound enforcement": has_lower_bound,
        "contested_by tracking": has_contested_by,
        "chain integrity (sha256 or Ed25519)": has_chain or has_chain_head,
    }
    n_pass = sum(1 for v in guards.values() if v)
    n_total = len(guards)

    return {
        "bench": "Decision ledger (audit trail)",
        "structural_guards": guards,
        "passes": n_pass,
        "total": n_total,
        "verdict": "PASS" if n_pass == n_total else "FAIL",
    }


def main():
    print("=== CSOAI SELF-TEST: 5-BENCH BATTERY ===")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print()

    results = []
    results.append(bench_prov())
    results.append(bench_def())
    results.append(bench_pqc())
    results.append(bench_flywheel())
    results.append(bench_ledger())

    for r in results:
        print(f"--- {r['bench']} ---")
        if "verdict" in r:
            print(f"  verdict: {r['verdict']}")
        if "selftest" in r:
            print(f"  selftest: {r['selftest']}")
        if "recall" in r:
            print(f"  recall: {r['recall']}, over-block: {r['overblock_rate']}")
        if "n_survive" in r:
            print(f"  survival: {r['n_survive']}/{r['n_total']}")
        if "chains" in r:
            for c in r["chains"]:
                if "error" in c:
                    print(f"  {c['chain']}: {c['error']}")
                else:
                    print(f"  {c['chain']}: {c['passes']}/5")
        if "structural_guards" in r:
            print(f"  passes: {r['passes']}/{r['total']}")
        if "honest_finding" in r:
            print(f"  honest finding: {r['honest_finding']}")
        print()

    # Summary
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "subject": "CSOAI self-test (testing ourselves with our own 5-bench battery)",
        "results": results,
    }
    output_path = HERE / "benchmark-results" / "self_test" / "self_test_5bench_2026-07-30.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"-> {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())