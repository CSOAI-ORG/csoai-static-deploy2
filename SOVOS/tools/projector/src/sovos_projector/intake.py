"""sovos-intake — the sensor loop.

Every external platform is a sensor, not just a billboard. This module
ingests results from arenas, eval logs, and error mining, then writes
them into `intake/` as timestamped, C2PA-signable records.

The flow:
  1. Arena result comes back (loss/win/score)
  2. We append to intake/arena-results/<arena>/<asset>_<timestamp>.json
  3. The flywheel reads intake/ and:
     - Updates SOV SIGNAL composite
     - Mines error vectors → intake/error-mine/ε_<hash>.json
     - Marks the model for re-merge (Error MergeKit)

This is the "water → milk → honey" pipeline running across the entire
public AI infrastructure.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Arena result record
# ---------------------------------------------------------------------------
@dataclass
class ArenaResult:
    arena_id: str              # "lmarena" | "safebench" | "fli-index"
    asset_id: str              # which SOVOS asset was submitted
    match_outcome: str         # "win" | "loss" | "tie" | "score"
    score: Optional[float] = None       # numeric score if applicable
    opponent: Optional[str] = None       # what we played against
    arena_record_url: Optional[str] = None
    raw_payload: Dict[str, Any] = field(default_factory=dict)
    received_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sovos_signable_id: str = ""  # filled by _signable_id()


def _signable_id(asset_id: str, ts: str) -> str:
    """Deterministic ID for cross-referencing intake records."""
    return hashlib.sha256(f"{asset_id}|{ts}".encode()).hexdigest()[:16]


def write_arena_result(result: ArenaResult, intake_root: Path) -> Path:
    """Write an arena result to intake/arena-results/<arena>/<id>.json."""
    arena_dir = intake_root / "arena-results" / result.arena_id
    arena_dir.mkdir(parents=True, exist_ok=True)
    if not result.sovos_signable_id:
        result.sovos_signable_id = _signable_id(result.asset_id, result.received_at)
    out_path = arena_dir / f"{result.asset_id}_{result.sovos_signable_id}.json"
    out_path.write_text(json.dumps(asdict(result), indent=2))
    return out_path


def load_arena_results(arena_id: str, intake_root: Path) -> List[ArenaResult]:
    """Load all arena results for a given arena."""
    arena_dir = intake_root / "arena-results" / arena_id
    if not arena_dir.exists():
        return []
    results = []
    for p in arena_dir.glob("*.json"):
        try:
            d = json.loads(p.read_text())
            results.append(ArenaResult(**d))
        except (json.JSONDecodeError, TypeError):
            continue
    return results


# ---------------------------------------------------------------------------
# Error mining — every loss becomes an error vector
# ---------------------------------------------------------------------------
@dataclass
class ErrorVector:
    """A learned error signature from a failure event.

    Compatible with the J-Space Move Arithmetic module (sovos-jspace-move).
    An Error Vector with intent=-1, when added to a candidate move,
    SUBTRACTS the failure mode from routing.
    """
    error_type: str            # "loss" | "timeout" | "refusal" | "hallucination" | "tie"
    asset_id: str
    arena_id: str
    pattern_hash: str
    magnitude: float           # 0..1, how strongly to subtract
    occurrences: int = 1
    first_seen: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sample_query: str = ""

    @staticmethod
    def from_arena(result: ArenaResult) -> Optional["ErrorVector"]:
        """Mine an arena result into an error vector (only if it's a loss)."""
        if result.match_outcome not in ("loss", "tie"):
            return None
        # Sample query from the arena payload (if present)
        sample = str(result.raw_payload.get("prompt", "unknown"))[:500]
        pattern = re.sub(r"\b\d+\b", "<NUM>", sample)
        pattern = re.sub(r"[A-Z][a-z]+ [A-Z][a-z]+", "<NAME>", pattern)
        return ErrorVector(
            error_type=result.match_outcome,
            asset_id=result.asset_id,
            arena_id=result.arena_id,
            pattern_hash=hashlib.sha256(pattern.encode()).hexdigest()[:16],
            magnitude=0.5 if result.match_outcome == "loss" else 0.2,
            sample_query=sample,
        )


def write_error_vector(vec: ErrorVector, intake_root: Path) -> Path:
    """Write an error vector to intake/error-mine/ε_<asset>_<hash>.json."""
    mine_dir = intake_root / "error-mine"
    mine_dir.mkdir(parents=True, exist_ok=True)
    out_path = mine_dir / f"ε_{vec.asset_id}_{vec.pattern_hash}.json"
    existing = None
    if out_path.exists():
        try:
            existing = ErrorVector(**json.loads(out_path.read_text()))
        except (json.JSONDecodeError, TypeError):
            existing = None
    if existing is not None:
        vec.occurrences = existing.occurrences + 1
        vec.first_seen = existing.first_seen
        vec.magnitude = min(existing.magnitude + 0.05, 1.0)
    out_path.write_text(json.dumps(asdict(vec), indent=2))
    return out_path


def mine_arena_results(arena_id: str, intake_root: Path) -> int:
    """Walk all arena results and mine them into error vectors.

    Returns the number of NEW error vectors written.
    """
    results = load_arena_results(arena_id, intake_root)
    n = 0
    for r in results:
        vec = ErrorVector.from_arena(r)
        if vec is not None:
            write_error_vector(vec, intake_root)
            n += 1
    return n


# ---------------------------------------------------------------------------
# Eval-log intake
# ---------------------------------------------------------------------------
def write_eval_log(asset_id: str, eval_payload: Dict[str, Any],
                   intake_root: Path) -> Path:
    """Write an evaluation log (e.g. from Kaggle notebook, HF Space)."""
    eval_dir = intake_root / "eval-logs"
    eval_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    safe_ts = ts.replace(":", "-")
    out_path = eval_dir / f"{asset_id}_{safe_ts}.json"
    payload = {"asset_id": asset_id, "received_at": ts, **eval_payload}
    out_path.write_text(json.dumps(payload, indent=2))
    return out_path


# ---------------------------------------------------------------------------
# Stats — what the flywheel sees right now
# ---------------------------------------------------------------------------
def intake_stats(intake_root: Path) -> Dict[str, Any]:
    """Aggregate stats across intake/."""
    stats = {
        "arena_results": {},
        "total_error_vectors": 0,
        "total_eval_logs": 0,
        "total_error_occurrences": 0,
        "earliest_arena_result": None,
        "latest_arena_result": None,
    }
    ar_root = intake_root / "arena-results"
    if ar_root.exists():
        for arena_dir in ar_root.iterdir():
            if arena_dir.is_dir():
                files = list(arena_dir.glob("*.json"))
                stats["arena_results"][arena_dir.name] = len(files)
                if files and stats["earliest_arena_result"] is None:
                    stats["earliest_arena_result"] = min(f.name for f in files)
                if files:
                    stats["latest_arena_result"] = max(f.name for f in files)
    mine_root = intake_root / "error-mine"
    if mine_root.exists():
        vecs = list(mine_root.glob("*.json"))
        stats["total_error_vectors"] = len(vecs)
        for p in vecs:
            try:
                d = json.loads(p.read_text())
                stats["total_error_occurrences"] += d.get("occurrences", 1)
            except json.JSONDecodeError:
                pass
    eval_root = intake_root / "eval-logs"
    if eval_root.exists():
        stats["total_eval_logs"] = len(list(eval_root.glob("*.json")))
    return stats


__all__ = [
    "ArenaResult", "write_arena_result", "load_arena_results",
    "ErrorVector", "write_error_vector", "mine_arena_results",
    "write_eval_log", "intake_stats",
]