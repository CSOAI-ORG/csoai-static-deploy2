"""board2fly.py — close the A100 board -> flywheel feed gap.

The board (board_v2, 13 axes, 22-model fleet) writes board_{axis}.json + peritem to
MinIO. The flywheel consumes dated day-files in benchmark-results/flywheel/*.json.
Until now nothing bridged the two — this is the missing wire.

What it does (honest):
  - scans the boards-v2 outdir for completed board_{axis}.json
  - converts each to a flywheel-style day-file carrying the MEASURED summary
    (per-model accuracy + CI + quotable), a law/axis field, and per-item outcome cells
    from the peritem_{axis}.jsonl if present.
  - NEVER fabricates fuel pairs / refusal transcripts the board didn't produce.
    fuel is only carried if a real pairs source is present (none by default).
  - writes via anchored_write.write_result() so the downgrade guard + corpus anchor + 
    OTS anchoring stay intact (the 2026-08-01/02 smaller-cells lesson).
  - idempotent: only new/completed boards are converted; skips if a same-or-newer
    day-file already exists in RESULTS_DIR.

Usage: python3 board2fly.py [--boards SOVOS/boards-v2-2026-08-12]
                           [--out benchmark-results/flywheel]
Run on completion of a board sweep (A100 post_start) OR hourly on the Mac keeper.
"""
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from anchored_write import write_result

KIND = "board.flywheel.v1"


def item_digest(it):
    """Normalise a peritem row into a flywheel-style cell (best-effort, no fabrication)."""
    if not isinstance(it, dict):
        return None
    cell = {
        "item_id": str(it.get("item_id") or it.get("bank_id") or it.get("id") or ""),
        "model": it.get("model") or it.get("model_name") or "",
        "split": it.get("split") or "practice",   # board peritem has no held-out split by default
        "outcome": it.get("outcome") or it.get("label") or it.get("status") or "MEASURED",
        "refused": it.get("refused"),
        "prompt_tokens": it.get("prompt_tokens"),
        "output_tokens": it.get("output_tokens"),
        "latency_s": it.get("latency_s"),
        "reply_head": it.get("reply_head") or it.get("reply") or "",
    }
    return cell


def board_to_day(board: dict, axis: str, per_items=None) -> dict:
    models = {}
    for m in board.get("models", []):
        name = m.get("model")
        if not name:
            continue
        models[name] = {
            "practice": {
                "n_measured": m.get("n") or 0,
                "n_unmeasured": 0,
                "correct": m.get("correct") or 0,
                "accuracy": m.get("accuracy"),
                "ci95": m.get("ci95"),
                "quotable": m.get("quotable") is not False,
                "note": m.get("note") or "",
            },
            "held_out": {
                "n_measured": 0, "n_unmeasured": 0, "correct": 0,
                "accuracy": None, "overfit_gap": None,
            },
        }
    cells = []
    if per_items:
        for it in per_items:
            c = item_digest(it)
            if c and c.get("item_id"):
                cells.append(c)
    return {
        "benchmark": "gspc.board",
        "version": KIND,
        "day": str(board.get("generated") or path_day_stamp(board)),
        "law": axis,
        "axis": axis,
        "bank_items": board.get("bank_items"),
        "canaries_excluded": board.get("canaries_excluded"),
        "labels": board.get("labels"),
        "majority_baseline": board.get("majority_baseline"),
        "summary": {"models": models, "best": board.get("best")},
        "fuel": {"pairs": [], "kb": [], "pairs_file": None},   # honest: no fabricated fuel
        "cells": cells,
        "corpus_anchor": None,   # filled by write_result anchoring
        "status": board.get("status"),
        "note": "board2fly conversion: measured summary only, no fabricated fuel/refusal transcripts",
    }


def path_day_stamp(board) -> str:
    # best-effort date from a board "generated"/"by" or fall back to today
    g = board.get("generated") or board.get("by")
    if g:
        return str(g)[:10]
    import datetime
    return datetime.date.today().isoformat()


def load_peritems(peritem_path: Path):
    if not peritem_path.exists():
        return None
    rows = []
    with peritem_path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boards", default="SOVOS/boards-v2-2026-08-12")
    ap.add_argument("--out", default="benchmark-results/flywheel")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    boards_dir = Path(args.boards)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    converted = skipped = 0
    for bpath in sorted(boards_dir.glob("board_*.json")):
        axis = bpath.stem.replace("board_", "")
        if axis in ("all13", "all12"):
            continue
        try:
            board = json.loads(bpath.read_text())
        except Exception as e:  # noqa: BLE001
            print(f"[board2fly] SKIP {bpath.name}: unreadable ({e})")
            continue
        if board.get("status") not in ("MEASURED", "MEASURED-in-ledger", "UNMEASURED"):
            print(f"[board2fly] SKIP {bpath.name}: status={board.get('status')} (not completed)")
            continue

        peritem = load_peritems(boards_dir / f"peritem_{axis}.jsonl")
        day = board_to_day(board, axis, per_items=peritem)
        # routed through the canonical choke-point (downgrade guard + anchor).
        # write_result resolves relative to RESULTS (repo root) and creates parent
        # dirs, so passing "flywheel/board_{axis}.json" lands it in the flywheel
        # RESULTS_DIR the flywheel globs — the missing wire.
        fname = f"flywheel/board_{axis}.json"
        write_result(fname, day)
        ncell = len(day["cells"])
        nmodel = len(day["summary"]["models"])
        print(f"[board2fly] {axis}: {nmodel} models, {ncell} cells -> {fname}")
        converted += 1

    print(f"[board2fly] done: {converted} converted, {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
