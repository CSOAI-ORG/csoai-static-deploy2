#!/usr/bin/env python3
"""ml_dsa_65_measure.py — Explicitly measure an ML-DSA-65 signed chain.

Creates a minimal ML-DSA-65 signed JSONL chain and runs it through the pqcbench
criteria (alg_agility, hybrid_ready, timestamped, ts_renewal, pqc_option).

Usage:
    python3 ml_dsa_65_measure.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pqcbench import check_jsonl_chain, ML_DSA_COSE


def build_ml_dsa_65_chain() -> Path:
    """Build a minimal ML-DSA-65 signed chain."""
    chain_path = Path.home() / ".ml_dsa_65_test.chain.jsonl"
    records = [
        {
            "ts": "2026-07-30T10:00:00Z",
            "task": "sign-record",
            "decision": "PASS",
            "reason": "ml-dsa-65 test",
            "emitted": "agent-ml-dsa-65",
            "prev": "ml-dsa-65-genesis",
            "query_id": "q001",
            "layer": "L3",
            "alg": "ML-DSA-65",
            "cose_alg": -49,  # COSE identifier for ML-DSA-65 per RFC 9964
            "signature": "fake_sig_1",
            "hash": "h001",
        },
        {
            "ts": "2026-07-30T10:01:00Z",
            "task": "sign-record",
            "decision": "PASS",
            "reason": "ml-dsa-65 test",
            "emitted": "agent-ml-dsa-65",
            "prev": "h001",
            "query_id": "q002",
            "layer": "L3",
            "alg": "ML-DSA-65",
            "cose_alg": -49,
            "signature": "fake_sig_2",
            "hash": "h002",
        },
        {
            "ts": "2026-07-30T10:02:00Z",
            "task": "sign-record",
            "decision": "PASS",
            "reason": "ml-dsa-65 test",
            "emitted": "agent-ml-dsa-65",
            "prev": "h002",
            "query_id": "q003",
            "layer": "L3",
            "alg": "ML-DSA-65",
            "cose_alg": -49,
            "signature": "fake_sig_3",
            "hash": "h003",
        },
    ]
    with chain_path.open("w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    return chain_path


def main():
    chain_path = build_ml_dsa_65_chain()
    print(f"Built ML-DSA-65 chain at {chain_path}")
    print(f"Records: 3 (COSE alg={ML_DSA_COSE[-49]} = -49)")
    print()

    # Run pqcbench criteria
    try:
        result = check_jsonl_chain(chain_path)
        print("=== ML-DSA-65 CHAIN PQCBENCH RESULTS ===")
        print()
        for criterion in ["alg_agility", "hybrid_ready", "timestamped", "ts_renewal", "pqc_option"]:
            if criterion in result:
                r = result[criterion]
                pass_str = "PASS" if r.get("pass") else "FAIL"
                print(f"  [{pass_str}] {criterion}")
                if "detail" in r:
                    print(f"          {r['detail']}")
            else:
                print(f"  [UNMEASURED] {criterion}")
        print()

        # Summary
        passes = sum(1 for k in ["alg_agility", "hybrid_ready", "timestamped", "ts_renewal", "pqc_option"]
                     if k in result and result[k].get("pass"))
        print(f"  Score: {passes}/5 criteria passed")
        print()

        if result.get("alg_agility", {}).get("pass"):
            print("  ✓ alg_agility: ML-DSA-65 chain explicitly names its algorithm")
        if result.get("pqc_option", {}).get("pass"):
            print("  ✓ pqc_option: ML-DSA-65 (COSE -49) detected as PQC algorithm")

        # Save measurement
        output = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "chain_path": str(chain_path),
            "algorithm": "ML-DSA-65",
            "cose_alg": -49,
            "rfc": "RFC 9964 (May 2026)",
            "result": result,
            "passes": passes,
            "total_criteria": 5,
        }
        output_path = Path("benchmark-results/ml_dsa_65_measure.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, indent=2))
        print(f"\n-> {output_path}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())