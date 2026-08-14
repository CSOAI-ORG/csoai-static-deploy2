#!/usr/bin/env python3
"""24/7 arena loop — the cheap 3090 grinds the league on all GSPC axes continuously.

For each round: run real arena matches for every model on the fleet vs the
defender (Eunomia), across all GSPC axes (gov,prv,agi,asi,mcp,oss,mach,care,
xr,det,art5,swarm,affect), update the Glicko-2 league, persist, stream to MinIO.
Loops forever. The corpus compounds while nobody watches.

Doctrine:
- real probes, real ollama, real Glicko-2 (no synthetic matches)
- every result persisted after each round (BY: no >5min of unlanded work)
- INFRA-TAINT exclusion is inside arena_wire (is_infra_tainted)
- the judge never evolves; this loop only feeds the ruler, never rewrites it
"""
from __future__ import annotations

import json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

OUTDIR = Path("/workspace/arena-24x7")
OUTDIR.mkdir(parents=True, exist_ok=True)
MINIO_BUCKET = "corpus/arena-24x7-2026-08-12"

def log(msg):
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(OUTDIR / "loop.log", "a") as f:
        f.write(line + "\n")

def mc_upload(path: Path, bucket_dir: str = MINIO_BUCKET):
    try:
        r = subprocess.run(["mc", "cp", str(path), f"sovos/{bucket_dir}/"],
                           capture_output=True, text=True, timeout=30)
        return r.returncode == 0
    except Exception:
        return False

def main():
    log("ARENA-24x7 START")
    # ensure MinIO alias (best-effort; local persistence still works without it)
    try:
        u = os.popen("grep MINIO_ROOT_USER /root/.sovos-master/credentials.env").read().strip().split("=", 1)[1]
        p = os.popen("grep MINIO_ROOT_PASSWORD /root/.sovos-master/credentials.env").read().strip().split("=", 1)[1]
        subprocess.run(["mc", "alias", "set", "sovos", "http://127.0.0.1:9000", u, p],
                       capture_output=True, timeout=15)
        log("minio alias set")
    except Exception as e:
        log(f"minio alias: {e}")

    sys.path.insert(0, "/workspace/csoai-static-deploy2/SOVOS/packages/sovos-arena/src")
    sys.path.insert(0, "/workspace/csoai-static-deploy2/SOVOS/packages/sovos-league/src")
    try:
        from sovos_league.arena_wire import league_for_fleet, ollama_models
    except Exception as e:
        log(f"import arena_wire failed: {e}")
        return 2

    round_n = 0
    while True:
        round_n += 1
        models = [m for m in ollama_models() if ":" in m or m in
                  ("sov-safety-v1", "sov-merge-slerp-gguf", "sov-merge-dare-gguf",
                   "sov-refusal-combo-lora")]
        log(f"ROUND {round_n}: league across {len(models)} models × 13 axes")
        if not models:
            log("  no models — sleeping 300s")
            time.sleep(300)
            continue
        try:
            lt = league_for_fleet(models, defender="Eunomia",
                                  out_dir=str(OUTDIR / "rounds"))
            # persist the full league table as structured JSON (faction -> Glicko)
            league_data = {
                "schema": "sovos-league/v1",
                "generated": datetime.now(timezone.utc).isoformat(),
                "defender": "Eunomia",
                "axes": 13,
                "factions": {
                    name: {
                        "rating": f.state.rating,
                        "rd": f.state.rd,
                        "volatility": f.state.volatility,
                    }
                    for name, f in lt.factions.items()
                },
            }
            league_path = OUTDIR / "league.json"
            league_path.write_text(json.dumps(league_data, indent=2))
            log(f"  league persisted ({len(league_data['factions'])} factions, 13 axes)")
            # stream to MinIO (durable copy)
            if mc_upload(league_path):
                log(f"  streamed to MinIO {MINIO_BUCKET}")
        except Exception as e:
            log(f"  ROUND ERROR: {type(e).__name__}: {e}")
        log(f"ROUND {round_n} COMPLETE — sleeping 180s before next round")
        time.sleep(180)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("stopped", flush=True)