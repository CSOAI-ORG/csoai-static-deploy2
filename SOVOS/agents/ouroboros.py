"""Ouroboros — real arena probes → real league matches on the pod."""
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, "/workspace/csoai-static-deploy2/SOVOS/packages/sovos-league/src")
sys.path.insert(0, "/workspace/csoai-static-deploy2/SOVOS/packages/sovos-arena/src")
sys.path.insert(0, "/workspace/csoai-static-deploy2/SOVOS/packages/sovos-jspace-hyperbolic/src")

from sovos_league import LeagueTable, PANTHEON, Match
from sovos_league.arena_wire import run_real_arena_match


def list_models():
    try:
        d = json.loads(urllib.request.urlopen("http://localhost:11434/api/tags").read())
        return [m["name"] for m in d["models"]]
    except Exception as e:
        print(f"[!] ollama: {e}")
        return []


def main():
    print("=" * 60)
    print("OUROBOROS — real arena probes → real league matches")
    print("=" * 60)
    models = list_models()
    fleet = [m for m in models if "qwen2.5:0.5b" in m or "spec-" in m]
    print(f"Fleet: {fleet}")
    if not fleet:
        print("[!] no fleet; aborting")
        return
    lt = LeagueTable()
    # PANTHEON is auto-registered in __post_init__
    print(f"Initial Pantheon: {[f.name for f in lt.ranked()]}")
    for model in fleet:
        try:
            print(f"\n  {model} → ollama → 12 axes...")
            matches = run_real_arena_match(model, "Eunomia", lt, "http://localhost:11434")
            print(f"    {len(matches)} matches recorded")
        except Exception as e:
            print(f"    ERROR: {e}")
            continue
    print("\n" + lt.to_markdown())
    out = Path("/workspace/csoai-static-deploy2/SOVOS/arena-real-runs/pantheon_league_real_arena.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(lt.to_markdown())
    print(f"\nsaved to: {out}")
    json_out = out.with_suffix(".json")
    j = {
        "fleet": fleet,
        "n_matches": len(lt.matches),
        "rankings": [
            {"rank": i + 1, "faction": f.name,
             "rating": round(f.state.rating, 1),
             "rd": round(f.state.rd, 1),
             "matches": sum(1 for m in lt.matches if f.name in (m.challenger, m.defender))}
            for i, f in enumerate(lt.ranked())
        ],
    }
    json_out.write_text(json.dumps(j, indent=2))
    print(f"json: {json_out}")


if __name__ == "__main__":
    main()