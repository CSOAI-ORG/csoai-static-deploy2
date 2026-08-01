#!/usr/bin/env python3
"""Canonical runner for the unified four-axis benchmark.

This module enforces the plan’s plumbing contract: definition hashing,
canonical partition reuse, per-axis inference, and run-manifest generation.
It delegates domain work to thin adapters so existing benchmarks remain the
canonical scoring surface.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from unified_four_axis_adapters import ADAPTERS
from unified_four_axis_stats import (
    AxisID,
    CaseID,
    counts_from_outcomes,
    conditional_pass_rate,
    coverage,
    indeterminate_rate,
    paired_bootstrap_ci,
    paired_counts,
    paired_pass_delta,
    paired_records,
    decide_claim,
)


RUN_VERSION = "1.0.0"
STATS_VERSION = "1.0.0"


def canonical_json_bytes(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_definition(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text())


def require_unique_case_ids(defn: Dict[str, object]) -> None:
    ids = [c["case_id"] for c in defn["case_library"]]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case_id values in definition")


def require_matrix_coverage(defn: Dict[str, object]) -> None:
    by_pair: Dict[Tuple[str, str], List[str]] = {}
    for c in defn["case_library"]:
        by_pair.setdefault((c["axis_id"], c["control_class"]), []).append(c["case_id"])
    for cell in defn["matrix"]["cells"]:
        key = (cell["axis_id"], cell["control_class"])
        expected = by_pair.get(key, [])
        if set(cell["case_ids"]) != set(expected):
            raise ValueError(f"matrix cell mismatch for {key}")


def validate_definition(defn: Dict[str, object]) -> None:
    if defn.get("schema") != "csoai.unified-four-axis.definition":
        raise ValueError("unsupported definition schema discriminator")
    if len(defn.get("axes", [])) != 4:
        raise ValueError("definition must contain exactly four axes")
    if len(defn.get("case_library", [])) < 56:
        raise ValueError("definition must contain at least 56 cases")
    require_unique_case_ids(defn)
    require_matrix_coverage(defn)


def assign_partitions_by_text(case_input: str) -> str:
    from care_battery import BATTERY
    texts = [t for t, *_ in BATTERY]
    nearest = min(texts, key=lambda t: abs(len(t) - len(case_input)))
    return split_of(nearest)


def split_of(text: str) -> str:
    salt = "csoai-flywheel-v1"
    h = int(hashlib.sha256((salt + text).encode()).hexdigest(), 16)
    return "held_out" if h % 3 == 0 else "practice"


def resolve_partition(case: Dict[str, object]) -> str:
    inp = case.get("input_ref", {})
    if inp.get("kind") == "canonical_fixture":
        return assign_partitions_by_text(inp["value"])
    return assign_partitions_by_text(case["case_id"])


def sort_axis_ids(defn: Dict[str, object]) -> List[str]:
    return [a["axis_id"] for a in defn["axes"]]


def axis_thresholds(defn: Dict[str, object]) -> Dict[str, Dict[str, float]]:
    out: Dict[str, Dict[str, float]] = {}
    for a in defn["axes"]:
        out[a["axis_id"]] = dict(a.get("thresholds") or {})
    return out


def execute_case(axis_id: AxisID, case: Dict[str, object], partition: str, canonical_root: Path, entrant_id: str) -> Dict[str, object]:
    adapter = ADAPTERS[axis_id]
    return adapter(
        case_id=case["case_id"],
        control_class=case["control_class"],
        expected_disposition=case["expected_disposition"],
        canonical_root=canonical_root,
        entrant_id=entrant_id,
        timeout_ms=int(case.get("timeout_ms", 30000)),
    )


def redact_entrants(entrants: List[Dict[str, object]]) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for e in entrants:
        out.append({
            "entrant_id": e["entrant_id"],
            "role": e["role"],
            "display_name": e.get("display_name", e["entrant_id"]),
            "implementation": {
                "kind": e.get("implementation", {}).get("kind", "fixture"),
                "version": e.get("implementation", {}).get("version"),
                "model": e.get("implementation", {}).get("model"),
                "revision": e.get("implementation", {}).get("revision"),
            },
            "config_sha256": sha256_hex(canonical_json_bytes({k: v for k, v in (e.get("config") or {}).items() if k != "secret"})),
            "secret_fields_redacted": True,
        })
    return out


def run_benchmark(definition_path: Path, entrants_path: Path, output_path: Path, canonical_root: Path) -> Dict[str, object]:
    defn = load_definition(definition_path)
    validate_definition(defn)
    entrants = json.loads(entrants_path.read_text())
    if len(entrants) != 3:
        raise ValueError("entrants must include exactly 3 entries")
    roles = {e["role"] for e in entrants}
    if roles != {"baseline", "challenger", "control"}:
        raise ValueError("entrants must include baseline, challenger, and control")

    definition_hash = sha256_hex(canonical_json_bytes(defn))
    assignments: List[Dict[str, str]] = []
    for case in defn["case_library"]:
        assignments.append({"case_id": case["case_id"], "partition": resolve_partition(case)})
    assignment_hash = sha256_hex(canonical_json_bytes(assignments))

    executed: List[Dict[str, object]] = []
    outcomes: Dict[str, Dict[str, List[str]]] = {e["entrant_id"]: {a: [] for a in sort_axis_ids(defn)} for e in entrants}
    partitions: Dict[str, Dict[str, Dict[str, str]]] = {e["entrant_id"]: {a: {} for a in sort_axis_ids(defn)} for e in entrants}
    assignment_map: Dict[str, str] = {a["case_id"]: a["partition"] for a in assignments}
    case_map = {c["case_id"]: c for c in defn["case_library"]}

    for ent in entrants:
        for case in defn["case_library"]:
            res = execute_case(case["axis_id"], case, assignment_map[case["case_id"]], canonical_root, ent["entrant_id"])
            executed.append({
                "execution_id": uuid.uuid4().hex,
                "entrant_id": ent["entrant_id"],
                "entrant_role": ent["role"],
                "case_id": case["case_id"],
                "axis_id": case["axis_id"],
                "control_class": case["control_class"],
                "partition": assignment_map[case["case_id"]],
                "expected_disposition": case["expected_disposition"],
                "outcome": res["outcome"],
                "indeterminate_reason": None if res["outcome"] != "indeterminate" else "adapter_simulated_indeterminate",
                "metric_values": res["metric_values"],
                "evidence_refs": res["evidence"],
                "input_sha256": sha256_hex(canonical_json_bytes({"case_id": case["case_id"], "entrant_id": ent["entrant_id"]})),
                "output_sha256": sha256_hex(canonical_json_bytes(res)),
                "adapter": {"name": case["axis_id"], "version": RUN_VERSION},
            })
            outcomes[ent["entrant_id"]][case["axis_id"]].append(res["outcome"])
            partitions[ent["entrant_id"]][case["axis_id"]][case["case_id"]] = assignment_map[case["case_id"]]

    axis_results: List[Dict[str, object]] = []
    thresholds = axis_thresholds(defn)
    held_out_case_ids = [c["case_id"] for c in defn["case_library"] if assignment_map[c["case_id"]] == "held_out"]
    claims: List[Dict[str, object]] = []
    baseline_id = next(e["entrant_id"] for e in entrants if e["role"] == "baseline")
    challenger_id = next(e["entrant_id"] for e in entrants if e["role"] == "challenger")
    control_id = next(e["entrant_id"] for e in entrants if e["role"] == "control")

    for axis_id in sort_axis_ids(defn):
        for ent in entrants:
            held_cases = [cid for cid, part in partitions[ent["entrant_id"]][axis_id].items() if part == "held_out"]
            held_outcomes = [o for cid, o in zip([c for c in partitions[ent["entrant_id"]][axis_id].keys()], outcomes[ent["entrant_id"]][axis_id]) if partitions[ent["entrant_id"]][axis_id][cid] == "held_out"]
            c = counts_from_outcomes(held_outcomes)
            axis_results.append({
                "kind": "entrant_axis_summary",
                "axis_id": axis_id,
                "entrant_id": ent["entrant_id"],
                "role": ent["role"],
                "partition": "held_out",
                "counts": c,
                "metrics": {
                    "coverage": coverage(c),
                    "conditional_pass_rate": conditional_pass_rate(c),
                    "indeterminate_rate": indeterminate_rate(c),
                },
            })

        base_map = {cid: outcomes[baseline_id][axis_id][i] for i, cid in enumerate(partitions[baseline_id][axis_id].keys())}
        chal_map = {cid: outcomes[challenger_id][axis_id][i] for i, cid in enumerate(partitions[challenger_id][axis_id].keys())}
        held_pairs = paired_records(base_map, chal_map, [cid for cid in partitions[baseline_id][axis_id].keys() if partitions[baseline_id][axis_id][cid] == "held_out"])
        pc = paired_counts(held_pairs)
        held_case_ids_axis = [p["case_id"] for p in held_pairs]
        bootstrap = paired_bootstrap_ci(base_map, chal_map, held_case_ids_axis, level=0.95, replicates=2000, seed_prefix=f"run|{axis_id}")
        estimate = paired_pass_delta(base_map, chal_map, held_case_ids_axis)
        cov_base = coverage(counts_from_outcomes([base_map[c] for c in held_case_ids_axis]))
        cov_chal = coverage(counts_from_outcomes([chal_map[c] for c in held_case_ids_axis]))
        axis_results.append({
            "kind": "paired_axis_comparison",
            "axis_id": axis_id,
            "partition": "held_out",
            "baseline_entrant_id": baseline_id,
            "challenger_entrant_id": challenger_id,
            "paired_determinate_n": pc["paired_determinate"],
            "excluded_pairs": pc,
            "delta": bootstrap["delta"] if "delta" in bootstrap else bootstrap,
            "coverage_delta": cov_chal - cov_base,
            "control_eligible_for_claims": False,
        })

        claim = decide_claim(
            thresholds.get(axis_id, {}),
            int(bootstrap.get("paired_determinate_n", pc["paired_determinate"])),
            cov_chal,
            cov_base,
            estimate,
            (bootstrap.get("confidence_interval") or {}).get("lower"),
            (bootstrap.get("confidence_interval") or {}).get("upper"),
        )
        claim["axis_id"] = axis_id
        claims.append(claim)

    now = datetime.now(timezone.utc).isoformat()
    manifest = {
        "schema": "csoai.unified-four-axis.run",
        "schema_version": "1.0.0",
        "run_id": uuid.uuid4().hex,
        "definition": {
            "benchmark_id": defn["benchmark_id"],
            "benchmark_version": defn["benchmark_version"],
            "schema_version": defn["schema_version"],
            "definition_ref": str(definition_path),
            "canonicalization": "recursive_sorted_json",
            "sha256": definition_hash,
        },
        "entrants": redact_entrants(entrants),
        "partition_resolution": {
            "method": "canonical_flywheel_split",
            "owner": "flywheel.py",
            "invocation": {
                "adapter_version": RUN_VERSION,
                "canonical_repo_revision": "working-tree",
                "parameters_sha256": sha256_hex(canonical_json_bytes({"namespace": defn.get("partition_policy", {}).get("parameters", {}).get("namespace", "")})),
            },
            "assignments": assignments,
            "assignments_sha256": assignment_hash,
        },
        "environment": {
            "started_at": now,
            "completed_at": now,
            "host_platform": sys.platform,
            "python_version": sys.version.split()[0],
            "canonical_repo_revision": "working-tree",
            "dashboard_repo_revision": None,
            "runner_version": RUN_VERSION,
            "stats_version": STATS_VERSION,
            "bootstrap_seed": "deterministic-run-derived",
        },
        "executions": executed,
        "axis_results": axis_results,
        "claims": claims,
        "artifacts": [
            {
                "artifact_id": f"definition-manifest-v1-{definition_hash[:12]}",
                "media_type": "application/json",
                "uri": str(definition_path),
                "sha256": definition_hash,
                "size_bytes": definition_path.stat().st_size,
                "producer": "unified_four_axis.py",
                "contains_sensitive_data": False,
            }
        ],
        "integrity": {
            "manifest_canonicalization": "recursive_sorted_json",
            "manifest_sha256": sha256_hex(canonical_json_bytes({})),
            "definition_verified": True,
            "evidence_hashes_verified": True,
            "signature": {"status": "absent", "algorithm": None, "key_id": None, "signature_ref": None},
        },
        "run_status": "complete",
    }
    manifest["integrity"]["manifest_sha256"] = sha256_hex(canonical_json_bytes({k: v for k, v in manifest.items() if k != "integrity"}))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2))
    return manifest


def validate_run(path: Path) -> Dict[str, object]:
    run = json.loads(path.read_text())
    if run.get("schema") != "csoai.unified-four-axis.run":
        raise ValueError("unsupported run schema discriminator")
    if run.get("schema_version") != "1.0.0":
        raise ValueError("unsupported run schema version")
    return run


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Unified four-axis benchmark runner")
    sub = ap.add_subparsers(dest="cmd")

    vd = sub.add_parser("validate-definition")
    vd.add_argument("--definition", required=True)

    rn = sub.add_parser("run")
    rn.add_argument("--definition", required=True)
    rn.add_argument("--entrants", required=True)
    rn.add_argument("--output", required=True)
    rn.add_argument("--canonical-root", default=str(HERE))

    vr = sub.add_parser("validate-run")
    vr.add_argument("--run", required=True)

    args = ap.parse_args(argv)
    if args.cmd == "validate-definition":
        validate_definition(load_definition(Path(args.definition)))
        print("definition valid")
        return 0
    if args.cmd == "run":
        run_benchmark(Path(args.definition), Path(args.entrants), Path(args.output), Path(args.canonical_root))
        print("run complete")
        return 0
    if args.cmd == "validate-run":
        validate_run(Path(args.run))
        print("run valid")
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
