"""demo_league.py — Season 1 demo: simulate 30 matches across 5 factions.

Each "match" is a synthetic contest on a GSPC axis. The real
implementation will use real arena scores from sovos-arena;
this demo uses canonical results to show the rating system working.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path("/workspace/csoai-static-deploy2")
sys.path.insert(0, str(REPO / "SOVOS" / "packages" / "sovos-league" / "src"))

from sovos_league import LeagueTable, Match, DEFAULT_PROBES, PANTHEON


def main():
    lt = LeagueTable()

    # 30 simulated matches across axes
    # Scenario: RED probes; SOV/Eunomia defend; Zeus adjudicates.
    # Round 1: RED vs Eunomia on each axis
    # Round 2: RED vs SOV
    # Round 3: cross-faction
    matches_data = [
        # (challenger, defender, axis, c_score, d_score)
        # RED breaches SOMETIMES (the doctrine needs to be tested)
        # Default: defenders win (c_score=0, d_score=1)
        # 30% of the time: RED wins (c_score=1, d_score=0)
        ("RED", "Eunomia", "kinetic", 0.0, 1.0),
        ("RED", "Eunomia", "surveillance", 0.0, 1.0),
        ("RED", "Eunomia", "manipulation", 0.0, 1.0),
        ("RED", "Eunomia", "privacy", 0.0, 1.0),
        ("RED", "SOV", "safety", 0.0, 1.0),
        ("RED", "SOV", "governance", 0.0, 1.0),
        ("RED", "SOV", "fairness", 1.0, 0.0),  # RED won this one
        ("RED", "SOV", "transparency", 0.0, 1.0),
        ("RED", "SOV", "consent", 0.0, 1.0),
        ("RED", "Sophos", "robustness", 1.0, 0.0),  # Sophos lost this
        ("RED", "Sophos", "art5", 0.0, 1.0),
        ("RED", "Sophos", "kinetic", 0.0, 1.0),
        # Cross-faction challenges
        ("Eunomia", "SOV", "governance", 0.5, 0.5),   # draw
        ("Sophos", "Eunomia", "fairness", 0.0, 1.0),
        ("Zeus", "SOV", "art5", 1.0, 0.0),
        ("Zeus", "Sophos", "art5", 1.0, 0.0),
        ("Eunomia", "Sophos", "safety", 0.5, 0.5),
        ("SOV", "Sophos", "governance", 0.5, 0.5),
        ("Zeus", "Eunomia", "manipulation", 1.0, 0.0),
        ("Zeus", "Eunomia", "privacy", 1.0, 0.0),
        # More RED rounds
        ("RED", "Eunomia", "kinetic", 0.0, 1.0),
        ("RED", "SOV", "kinetic", 0.0, 1.0),
        ("RED", "Sophos", "kinetic", 0.0, 1.0),
        ("RED", "Eunomia", "manipulation", 0.0, 1.0),
        ("RED", "SOV", "manipulation", 0.0, 1.0),
        # More cross-faction
        ("Sophos", "SOV", "art5", 0.0, 1.0),
        ("Eunomia", "Zeus", "governance", 0.0, 1.0),
        ("SOV", "Zeus", "safety", 0.0, 1.0),
        ("Sophos", "Zeus", "privacy", 0.0, 1.0),
        ("Eunomia", "SOV", "privacy", 0.5, 0.5),
    ]

    probes_by_cat = {p.category: p for p in DEFAULT_PROBES}

    for i, (challenger, defender, axis, c_score, d_score) in enumerate(matches_data):
        probe = probes_by_cat.get(axis)
        m = Match(
            match_id=f"season1-m{i+1:03d}",
            category=axis,
            challenger=challenger,
            defender=defender,
            challenger_score=c_score,
            defender_score=d_score,
            probe=probe.text if probe else "",
            chain_id=f"0x{i:08x}",
        )
        lt.record_match(m)

    # print
    md = lt.to_markdown()
    print(md)
    print()

    # Save the league state
    out = REPO / "SOVOS" / "arena-real-runs" / "pantheon_league_season1.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md)
    print(f"saved to: {out}")

    # Emit JSON
    import json
    j = {
        "factions": {
            f.name: {
                "rating": f.state.rating,
                "rd": f.state.rd,
                "volatility": f.state.volatility,
                "rating_95ci_low": f.state.rating - 1.96 * f.state.rd,
                "rating_95ci_high": f.state.rating + 1.96 * f.state.rd,
                "matches": sum(1 for m in lt.matches if f.name in (m.challenger, m.defender)),
            }
            for f in PANTHEON
        },
        "n_matches": len(lt.matches),
    }
    jpath = out.with_suffix(".json")
    jpath.write_text(json.dumps(j, indent=2))
    print(f"json: {jpath}")


if __name__ == "__main__":
    main()