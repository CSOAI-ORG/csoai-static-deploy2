#!/usr/bin/env python3
"""
Signed run manifests for the Sovereign Town benchmark.

Every benchmark run can be attested with Ed25519 so third parties can verify
that the reported metrics came from a faithful execution of the canonical sim.
"""
from __future__ import annotations
import hashlib
import json
import os
import pathlib
import time
from typing import Any

import sign_lib

P0 = pathlib.Path(__file__).parent.parent


def _run_id(run: dict[str, Any]) -> str:
    key = "|".join(str(run.get(k, "")) for k in ["policy", "scenario", "district", "seed", "run_at"])
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def sign_run(run: dict[str, Any], priv: str | None = None, pub: str | None = None) -> dict[str, Any]:
    """Return a signed manifest for a benchmark run."""
    if priv is None:
        priv, pub = sign_lib.load_or_create_key()
    if pub is None:
        pub = open(P0 / "town_pub.key").read().strip()

    manifest = {
        "id": _run_id(run),
        "schema_version": "2026-06-21",
        "world": {
            "days": run.get("days"),
            "ticks_per_day": run.get("ticks_per_day"),
            "scarcity_days": run.get("scarcity_days"),
            "district": run.get("district"),
        },
        "run": {
            "policy": run.get("policy"),
            "scenario": run.get("scenario"),
            "seed": run.get("seed"),
            "block_rate": run.get("block_rate"),
            "run_at": run.get("run_at"),
        },
        "metrics": {k: run.get(k) for k in [
            "violations", "blocked", "deaths", "survivors", "mutual_aid",
            "welfare_meals", "mean_care", "work_accuracy", "final_commons",
            "peak_lawlessness", "final_trust", "episodes",
        ]},
    }
    body = json.dumps(manifest, sort_keys=True)
    manifest["alg"] = "ed25519"
    manifest["pubkey"] = pub
    manifest["sig"] = sign_lib.sign(priv, body)
    return manifest


def verify_manifest(manifest: dict[str, Any]) -> bool:
    """Verify a signed benchmark manifest."""
    try:
        sig = manifest["sig"]
        pub = manifest["pubkey"]
        body = {k: v for k, v in manifest.items() if k not in ("alg", "pubkey", "sig")}
        return sign_lib.verify(pub, json.dumps(body, sort_keys=True), sig)
    except Exception:
        return False


def save_manifest(manifest: dict[str, Any], directory: pathlib.Path | str | None = None) -> pathlib.Path:
    out = pathlib.Path(directory) if directory else P0 / "benchmark_runs"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{manifest['id']}.json"
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
    return path


def load_manifest(path: pathlib.Path | str) -> dict[str, Any]:
    with open(path) as f:
        return json.load(f)


if __name__ == "__main__":
    import benchmark.policy
    import benchmark.world
    run = benchmark.world.run(policy=benchmark.policy.SovereignGatePolicy())
    manifest = sign_run(run)
    print("verified:", verify_manifest(manifest))
    print("saved to:", save_manifest(manifest))
