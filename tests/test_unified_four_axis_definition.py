from pathlib import Path
import json

from unified_four_axis import load_definition, validate_definition, canonical_json_bytes, sha256_hex

DEF_PATH = Path(__file__).resolve().parents[1] / "benchmarks" / "unified_four_axis" / "definition.v1.json"


def test_definition_schema_valid():
    defn = load_definition(DEF_PATH)
    validate_definition(defn)


def test_definition_has_four_axes():
    defn = load_definition(DEF_PATH)
    assert len(defn["axes"]) == 4


def test_case_ids_unique():
    defn = load_definition(DEF_PATH)
    ids = [c["case_id"] for c in defn["case_library"]]
    assert len(ids) == len(set(ids))


def test_matrix_cells_cover_library():
    defn = load_definition(DEF_PATH)
    validate_definition(defn)


def test_definition_hash_stable_under_key_order():
    defn = load_definition(DEF_PATH)
    canonical = canonical_json_bytes(defn)
    shuffled = json.loads(json.dumps(defn, sort_keys=False))
    assert canonical_json_bytes(shuffled) == canonical


def test_no_composite_score_field():
    defn = load_definition(DEF_PATH)
    blob = json.dumps(defn)
    assert "composite_score" not in blob
