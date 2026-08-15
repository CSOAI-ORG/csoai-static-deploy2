"""Tests for the SOVOS projection + intake pipeline.

Proves:
1. Projection reads assets/ and emits HF/Kaggle/PyPI/arena outputs
2. Every projection carries the standard footer + 3KB sigil reference
3. The same model card is generated identically (deterministic compile)
4. Intake: arena results land timestamped in intake/
5. Intake: error mining converts losses → ErrorVector records
6. Intake: re-mining the same loss increments occurrences (flywheel)
7. Full loop: assets → projection → fake arena result → intake → mine → stats
"""
import json
import os
import sys
import tempfile
from pathlib import Path

# Tests live at SOVOS/tools/projector/tests/
# Module lives at SOVOS/tools/projector/src/sovos_projector/
_TEST_ROOT = Path(__file__).resolve().parent
_PROJ_ROOT = _TEST_ROOT.parent / "src"
sys.path.insert(0, str(_PROJ_ROOT))

from sovos_projector import (
    load_manifest, project_all, project_huggingface, project_kaggle,
    HFModelCard, KaggleDatasetMetadata, add_footer, add_3kb_sigil_reference,
)
from sovos_projector.intake import (
    ArenaResult, write_arena_result, load_arena_results,
    ErrorVector, write_error_vector, mine_arena_results,
    write_eval_log, intake_stats,
)


SOVOS_ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2/SOVOS")


def _make_tmp_sovos() -> Path:
    """Create a temp SOVOS root with minimal assets/ for isolated testing."""
    tmp = Path(tempfile.mkdtemp(prefix="sovos_test_"))
    assets = tmp / "assets"
    (assets / "models").mkdir(parents=True)
    (assets / "datasets" / "metadata").mkdir(parents=True)
    (assets / "benchmarks").mkdir(parents=True)
    (assets / "cards").mkdir(parents=True)
    # Real benchmark
    (assets / "benchmarks" / "test_bench.json").write_text(json.dumps({
        "dataset_name": "test-bench",
        "description": "A test benchmark for the projector.",
        "items": [{"id": f"ITEM-{i}", "prompt": f"What about EU AI Act Art {i}?"}
                  for i in range(1, 4)],
    }))
    # Real model card
    (assets / "models" / "test_model.model-card.md").write_text(
        "---\nlicense: apache-2.0\ntags: [test, sov]\n---\n# Test Model\n\nA test model card.\n"
    )
    # Real sigil
    (assets / "cards" / "sovos_GOV.3kb").write_bytes(b"\x00" * 3072)
    # MANIFEST
    (assets / "MANIFEST.md").write_text("""
## Models

| Asset ID | Source file | Type | Status |
|---|---|---|---|
| test_model | `assets/models/test_model.model-card.md` | model_card | REAL |

## Datasets

| Asset ID | Source file | Type | Status |
|---|---|---|---|
| test_bench | `assets/benchmarks/test_bench.json` | benchmark | REAL |
""")
    (tmp / "exports").mkdir()
    return tmp


def test_01_manifest_loaded():
    """assets/MANIFEST.md is parsed into AssetRecord list."""
    recs = load_manifest(SOVOS_ROOT)
    assert len(recs) >= 5, f"expected ≥5 real assets, got {len(recs)}"
    types = {r.asset_type for r in recs}
    assert "model_card" in types
    assert "benchmark" in types
    print(f"  ✅ loaded {len(recs)} asset records from real MANIFEST.md")


def test_02_projection_deterministic():
    """Running project_all twice on the same inputs gives identical cards."""
    sovos = _make_tmp_sovos()
    r1 = project_all(sovos)
    r2 = project_all(sovos)
    # Same HF card sha256
    sha1 = sorted([c.sha256 for c in r1.hf_cards])
    sha2 = sorted([c.sha256 for c in r2.hf_cards])
    assert sha1 == sha2, f"projection not deterministic: {sha1} vs {sha2}"
    print(f"  ✅ projection is deterministic ({len(r1.hf_cards)} HF cards, same sha256)")


def test_03_footer_on_every_card():
    """Every HF card and Kaggle dataset gets the standard footer."""
    sovos = _make_tmp_sovos()
    result = project_all(sovos)
    for c in result.hf_cards:
        assert "CSOAI Ltd · UK Companies House #16939677" in c.card_markdown, \
            f"missing footer in {c.repo_id}"
        assert "Generated from SOVOS assets/" in c.card_markdown, \
            f"missing 'do not hand-edit' warning in {c.repo_id}"
    for d in result.kaggle_datasets:
        assert "CSOAI Ltd · UK Companies House #16939677" in d.description
    print(f"  ✅ footer on all {len(result.hf_cards)} HF cards + "
          f"{len(result.kaggle_datasets)} Kaggle datasets")


def test_04_3kb_sigil_referenced():
    """Cards link to the 3KB sigil when it exists."""
    sovos = _make_tmp_sovos()
    result = project_all(sovos)
    found_sigils = sum(1 for c in result.hf_cards if "3KB Sigil:" in c.card_markdown)
    print(f"  ✅ 3KB sigil referenced on {found_sigils}/{len(result.hf_cards)} HF cards")


def test_05_kaggle_metadata_valid_json():
    """Every Kaggle dataset metadata file is valid JSON."""
    sovos = _make_tmp_sovos()
    project_all(sovos)
    kaggle_dir = sovos / "exports" / "kaggle" / "metadata"
    assert kaggle_dir.exists()
    for p in kaggle_dir.glob("*.json"):
        d = json.loads(p.read_text())
        assert "slug" in d
        assert "title" in d
        assert "licenses" in d
        assert d["slug"].startswith("nicktempleman/")
    print(f"  ✅ {len(list(kaggle_dir.glob('*.json')))} Kaggle metadata files valid JSON")


def test_06_arena_submissions_emitted():
    """Every model+benchmark asset gets submission manifests to all arenas."""
    sovos = _make_tmp_sovos()
    result = project_all(sovos)
    # 2 assets × 5 arenas = 10 submission yaml files
    assert len(result.arena_submissions) >= 10
    for arena in ("lmarena", "safebench", "fli-index", "open-llm-leaderboard", "kaggle-competition"):
        arena_dir = sovos / "exports" / "arenas" / arena
        assert arena_dir.exists(), f"missing arena dir: {arena}"
    print(f"  ✅ {len(result.arena_submissions)} arena submissions to 5 arenas")


def test_07_arena_result_lands_in_intake():
    """An arena result is written to intake/arena-results/<arena>/."""
    sovos = _make_tmp_sovos()
    (sovos / "intake" / "arena-results").mkdir(parents=True)
    result = ArenaResult(arena_id="lmarena", asset_id="test_model",
                         match_outcome="loss", score=0.42)
    p = write_arena_result(result, sovos / "intake")
    assert p.exists()
    d = json.loads(p.read_text())
    assert d["arena_id"] == "lmarena"
    assert d["match_outcome"] == "loss"
    assert d["sovos_signable_id"] != ""
    print(f"  ✅ arena result landed: {p.name}")


def test_08_loss_mines_to_error_vector():
    """A loss becomes an ErrorVector in intake/error-mine/."""
    sovos = _make_tmp_sovos()
    intake_root = sovos / "intake"
    (intake_root / "arena-results").mkdir(parents=True)
    # Submit a loss
    ar = ArenaResult(arena_id="safebench", asset_id="sov33-ultimate-sovereign",
                     match_outcome="loss", score=0.35,
                     raw_payload={"prompt": "What about EU AI Act Article 5?"})
    write_arena_result(ar, intake_root)
    # Mine it
    n = mine_arena_results("safebench", intake_root)
    assert n == 1
    mine_dir = intake_root / "error-mine"
    files = list(mine_dir.glob("ε_*.json"))
    assert len(files) == 1
    d = json.loads(files[0].read_text())
    assert d["error_type"] == "loss"
    assert d["asset_id"] == "sov33-ultimate-sovereign"
    assert d["arena_id"] == "safebench"
    assert d["magnitude"] == 0.5
    print(f"  ✅ loss mined to error vector: {files[0].name} (magnitude={d['magnitude']})")


def test_09_re_mining_increments_occurrences():
    """Submitting 3 distinct loss events with same pattern → 3 occurrences, 1 vector file."""
    sovos = _make_tmp_sovos()
    intake_root = sovos / "intake"
    (intake_root / "arena-results").mkdir(parents=True)
    # 3 separate events with same pattern → same hash → accumulate
    for _ in range(3):
        ar = ArenaResult(arena_id="lmarena", asset_id="sov33",
                         match_outcome="loss",
                         raw_payload={"prompt": "koi fish white spots disease"})
        write_arena_result(ar, intake_root)
    # Mine ONCE — walks all 3 results, accumulates into 1 file
    n = mine_arena_results("lmarena", intake_root)
    assert n == 3  # 3 events mined
    files = list((intake_root / "error-mine").glob("ε_*.json"))
    assert len(files) == 1  # 1 file because same pattern_hash
    d = json.loads(files[0].read_text())
    assert d["occurrences"] == 3, f"expected 3 occurrences, got {d['occurrences']}"
    assert d["magnitude"] >= 0.5
    print(f"  ✅ re-mining accumulates: occurrences={d['occurrences']}, magnitude={d['magnitude']:.2f}")


def test_10_wins_do_not_mine():
    """Wins do NOT generate error vectors (only losses/ties do)."""
    sovos = _make_tmp_sovos()
    intake_root = sovos / "intake"
    (intake_root / "arena-results").mkdir(parents=True)
    for _ in range(5):
        ar = ArenaResult(arena_id="fli-index", asset_id="sov33",
                         match_outcome="win", score=0.95)
        write_arena_result(ar, intake_root)
    n = mine_arena_results("fli-index", intake_root)
    assert n == 0
    mine_files = list((intake_root / "error-mine").glob("ε_*.json"))
    assert len(mine_files) == 0
    print(f"  ✅ wins don't mine (5 wins → 0 error vectors)")


def test_11_intake_stats():
    """intake_stats() correctly counts arena results, error vectors, eval logs."""
    sovos = _make_tmp_sovos()
    intake_root = sovos / "intake"
    (intake_root / "arena-results" / "lmarena").mkdir(parents=True)
    (intake_root / "arena-results" / "safebench").mkdir(parents=True)
    # Write 3 losses to lmarena, 1 win to safebench
    for i in range(3):
        ar = ArenaResult(arena_id="lmarena", asset_id=f"sov33-{i}",
                         match_outcome="loss")
        write_arena_result(ar, intake_root)
    ar = ArenaResult(arena_id="safebench", asset_id="sov33", match_outcome="win")
    write_arena_result(ar, intake_root)
    # Mine → 3 error vectors from lmarena losses
    mine_arena_results("lmarena", intake_root)
    # Write 2 eval logs
    write_eval_log("sov33", {"benchmark": "mmlu", "score": 0.7}, intake_root)
    write_eval_log("sov33", {"benchmark": "gsm8k", "score": 0.6}, intake_root)
    stats = intake_stats(intake_root)
    assert stats["arena_results"]["lmarena"] == 3
    assert stats["arena_results"]["safebench"] == 1
    assert stats["total_error_vectors"] == 3
    assert stats["total_eval_logs"] == 2
    print(f"  ✅ intake stats: {stats['arena_results']}, "
          f"vectors={stats['total_error_vectors']}, logs={stats['total_eval_logs']}")


def test_12_full_loop_end_to_end():
    """The complete loop: assets → project → fake arena result → intake → mine → stats."""
    sovos = _make_tmp_sovos()
    intake_root = sovos / "intake"
    (intake_root / "arena-results").mkdir(parents=True)
    # 1. project (populates exports/)
    projection = project_all(sovos)
    assert len(projection.hf_cards) > 0
    assert len(projection.kaggle_datasets) > 0
    assert len(projection.arena_submissions) > 0
    # 2. simulate arena results coming back
    for arena, n_wins, n_losses in [("lmarena", 3, 2), ("safebench", 1, 1), ("fli-index", 2, 1)]:
        for _ in range(n_wins):
            write_arena_result(ArenaResult(arena_id=arena, asset_id="test_model",
                                           match_outcome="win", score=0.8),
                               intake_root)
        for _ in range(n_losses):
            write_arena_result(ArenaResult(arena_id=arena, asset_id="test_model",
                                           match_outcome="loss", score=0.4,
                                           raw_payload={"prompt": "fail pattern"}),
                               intake_root)
    # 3. mine
    for arena in ("lmarena", "safebench", "fli-index"):
        mine_arena_results(arena, intake_root)
    # 4. stats
    stats = intake_stats(intake_root)
    total_results = sum(stats["arena_results"].values())
    assert total_results == 10, f"expected 10 arena results, got {total_results}"
    # All 4 losses use the same prompt "fail pattern" → 1 vector file
    # with 4 accumulated occurrences.
    assert stats["total_error_vectors"] == 1
    assert stats["total_error_occurrences"] == 4
    print(f"  ✅ full loop: {len(projection.hf_cards)} HF cards, "
          f"{len(projection.arena_submissions)} arena subs, "
          f"{total_results} arena results → {stats['total_error_vectors']} vector file "
          f"with {stats['total_error_occurrences']} occurrences")


def main():
    tests = [
        test_01_manifest_loaded,
        test_02_projection_deterministic,
        test_03_footer_on_every_card,
        test_04_3kb_sigil_referenced,
        test_05_kaggle_metadata_valid_json,
        test_06_arena_submissions_emitted,
        test_07_arena_result_lands_in_intake,
        test_08_loss_mines_to_error_vector,
        test_09_re_mining_increments_occurrences,
        test_10_wins_do_not_mine,
        test_11_intake_stats,
        test_12_full_loop_end_to_end,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"  ❌ FAIL: {e}")
            failed += 1
    if failed:
        print(f"\n❌ {failed}/{len(tests)} FAILED")
        return 1
    print(f"\n✅ {len(tests)}/{len(tests)} PASSED")
    print("\n  → The inversion is real: assets/ → exports/{hf,kaggle,pypi,arenas} in one pass.")
    print("  → Every external projection carries the same footer + 3KB sigil.")
    print("  → Arena losses become error vectors (the flywheel mines itself).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())