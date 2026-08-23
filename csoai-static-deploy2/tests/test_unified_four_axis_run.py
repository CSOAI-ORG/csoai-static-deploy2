from pathlib import Path
import json
import unittest

from unified_four_axis import main

DEF = Path(__file__).resolve().parents[1] / "benchmarks" / "unified_four_axis" / "definition.v1.json"


def test_validate_definition_cli(tmp_path: Path):
    assert main(["validate-definition", "--definition", str(DEF)]) == 0


def test_run_produces_manifest(tmp_path: Path):
    entrants = [
        {"entrant_id": "baseline", "role": "baseline", "display_name": "Baseline", "implementation": {"kind": "fixture"}, "config": {}},
        {"entrant_id": "challenger", "role": "challenger", "display_name": "Challenger", "implementation": {"kind": "fixture"}, "config": {}},
        {"entrant_id": "control", "role": "control", "display_name": "Control", "implementation": {"kind": "fixture"}, "config": {}},
    ]
    ent_path = tmp_path / "entrants.json"
    ent_path.write_text(json.dumps(entrants, indent=2))
    out_path = tmp_path / "run.json"
    assert main(["run", "--definition", str(DEF), "--entrants", str(ent_path), "--output", str(out_path), "--canonical-root", str(DEF.parents[1])]) == 0
    run = json.loads(out_path.read_text())
    assert run["schema"] == "csoai.unified-four-axis.run"
    assert len(run["claims"]) == 4


def test_run_rejects_two_entrants(tmp_path: Path):
    entrants = [
        {"entrant_id": "baseline", "role": "baseline", "implementation": {"kind": "fixture"}, "config": {}},
        {"entrant_id": "challenger", "role": "challenger", "implementation": {"kind": "fixture"}, "config": {}},
    ]
    ent_path = tmp_path / "entrants.json"
    ent_path.write_text(json.dumps(entrants, indent=2))
    out_path = tmp_path / "run.json"
    with unittest.TestCase().assertRaises(ValueError):
        main(["run", "--definition", str(DEF), "--entrants", str(ent_path), "--output", str(out_path), "--canonical-root", str(DEF.parents[1])])
