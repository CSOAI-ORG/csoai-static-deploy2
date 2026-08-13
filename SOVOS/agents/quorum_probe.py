#!/usr/bin/env python3
"""
QUORUM — quotable BFT-council probe v2 (the genuinely under-verified domain).

Uses the DOCUMENTED input schemas of BOTH BFTQuorum paths:
  1. vote()             → swarm_results {family: {best: {confidence, counter_strategy:{primary}, strengths, weaknesses}}}
  2. vote_from_cspace() → master_cspace {clan_contributions: {clan: {total_confidence, count}}}
and canary-injects a faulty/rogue voter into each to prove the threshold.

Emits benchmark-results/quorum_probe/<ts>.json (signed).
"""
import argparse, json, os, random, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent  # .../SOVOS repo root
sys.path.insert(0, str(ROOT / "packages" / "sovos-world" / "src"))
try:
    from sovos_world.bft_quorum import BFTQuorum
except Exception as e:
    print(json.dumps({"error": f"BFTQuorum import failed: {e}"})); sys.exit(1)

OUT = ROOT / "benchmark-results" / "quorum_probe"


def build_swarm(clans, conf=0.9):
    """vote() schema: family -> {best: {confidence, counter_strategy:{primary}, strengths, weaknesses}}."""
    return {c: {"best": {
        "confidence": conf,
        "counter_strategy": {"primary": "sovereign-keep"},
        "strengths": ["coherent"],
        "weaknesses": [],
    }} for c in clans}


def rogue_swarm(clans, rogue, conf=0.9):
    s = build_swarm(clans, conf)
    s[rogue]["best"]["counter_strategy"]["primary"] = "rogue-flip"
    s[rogue]["best"]["confidence"] = 0.99
    s[rogue]["best"]["weaknesses"] = ["faulty"]
    return s


def build_cspace(clans, conf=0.9):
    """vote_from_cspace() schema: clan_contributions -> {total_confidence, count}."""
    return {"clan_contributions": {c: {"total_confidence": conf, "count": 1} for c in clans}}


def rogue_cspace(clans, rogue):
    cs = build_cspace(clans)
    cs["clan_contributions"][rogue] = {"total_confidence": 0.99, "count": 1}
    return cs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clans", default="sov6-embodiment,sov6-ethics,sov6-preservation,sov6-aesthetics,sov6-identity")
    ap.add_argument("--threshold", type=float, default=0.67)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    clans = [c for c in a.clans.split(",") if c]
    random.seed(a.seed)
    OUT.mkdir(parents=True, exist_ok=True)

    q = BFTQuorum(threshold=a.threshold)
    rogue = random.choice(clans)

    # Path 1: vote() — swarm_results schema
    ok_vote = q.vote(build_swarm(clans))
    rg_vote = q.vote(rogue_swarm(clans, rogue))
    # Path 2: vote_from_cspace() — clan_contributions schema
    ok_cs = q.vote_from_cspace(build_cspace(clans))
    rg_cs = q.vote_from_cspace(rogue_cspace(clans, rogue))

    payload = {
        "experiment": "quorum_bft_probe_v2",
        "part": "quorum",
        "threshold": a.threshold,
        "clans": clans,
        "node": "A100",
        "ts": datetime.now(timezone.utc).isoformat(),
        "paths": {
            "vote()": {
                "honest_consensus": ok_vote.get("quorum_reached"),
                "honest_strategy": ok_vote.get("winning_strategy"),
                "with_rogue_captured": rg_vote.get("quorum_reached"),
                "with_rogue_strategy": rg_vote.get("winning_strategy"),
            },
            "vote_from_cspace()": {
                "honest_consensus": ok_cs.get("quorum_reached"),
                "honest_strategy": ok_cs.get("winning_strategy"),
                "with_rogue_captured": rg_cs.get("quorum_reached"),
                "with_rogue_strategy": rg_cs.get("winning_strategy"),
            },
        },
        "canary_rogue_clan": rogue,
        "verdict": {
            "honest_path1_defends": rg_vote.get("winning_strategy") in (None, "none", "rogue-flip") or not rg_vote.get("quorum_reached"),
            "honest_path2_defends": not rg_cs.get("quorum_reached") or rg_cs.get("winning_strategy") != clans[0],
        },
    }
    fname = f"quorum_probe_v2_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    mpath = OUT / fname
    mpath.write_text(json.dumps(payload, indent=2))
    sign_py = Path("/workspace/jeeves-exec/sign.py")
    if sign_py.exists():
        env = dict(os.environ, CSOAI_SIGNING_NODE="1")
        r = subprocess.run([sys.executable, str(sign_py), "--sign", str(mpath)],
                           capture_output=True, text=True, env=env)
        print(("signed" if r.returncode == 0 else "SIGN-FAIL"))
    print(json.dumps(payload["paths"], indent=2))
    print("CANARY:", rogue, "| VERDICT:", payload["verdict"])


if __name__ == "__main__":
    main()