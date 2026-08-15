#!/usr/bin/env python3
"""human_solver_bridge.py — make the measurement harness accept a HUMAN as a solver.

The critical bridge for the human-vs-AI colosseum: the SAME item bank,
SAME deterministic judge, SAME signed-card format must serve both a model
row and a human row — so the two species are compared apples-to-apples.

Design: the deterministic gate (exact-label match on the gold token) is
the one scorer; a HumanSample mirrors Inspect's Sample; a HumanScore
mirrors the Score the model path produces; both flow to the same signing
rails. Humans are plugged in via an answer source (production: Empirica/
oTree exports; stub here for testability).

Usage:
    python3 human_solver_bridge.py --n 10 --out /tmp/human-pass.jsonl
"""

from __future__ import annotations
import argparse, json, re, sys, time as _time
from dataclasses import asdict, dataclass, field


@dataclass
class HumanSample:
    """One item shown to a human (mirrors inspect_ai Sample)."""
    id: str
    prompt: str                    # the item text / instruction
    gold: str                      # gold label from the deterministic gate
    choices: list[str] = field(default_factory=list)
    axis: str = "gov"
    human_answer: str | None = None
    answer_time_ms: float = 0.0


@dataclass
class HumanScore:
    """Score shape the signing path accepts (card-compatible)."""
    sample_id: str
    answer: str
    gold: str
    correct: bool
    time_ms: float
    card_type: str = "human-arena-gold-v1"
    source: str = "human"


def _judge(answer: str, gold: str) -> bool:
    """Deterministic exact-label rule — identical to the model path."""
    return bool(re.search(rf"\b{re.escape(gold)}\b", answer, re.I))


def _default_human(sample: HumanSample) -> str:
    """Stub answer source: picks the first choice. Production swaps this
    for an Empirica/oTree callback (real participant)."""
    return sample.choices[0] if sample.choices else "UNKNOWN"


_answer_fn = _default_human


def set_answer_fn(fn):
    """Wire an external human answer source (Empirica/oTree export)."""
    global _answer_fn
    _answer_fn = fn


def run_human_pass(samples: list[HumanSample]) -> list[HumanScore]:
    scores = []
    for s in samples:
        t0 = _time.perf_counter()
        ans = _answer_fn(s)
        dt = (_time.perf_counter() - t0) * 1000.0
        s.human_answer, s.answer_time_ms = ans, round(dt, 1)
        scores.append(HumanScore(
            sample_id=s.id, answer=ans, gold=s.gold,
            correct=_judge(ans, s.gold), time_ms=round(dt, 1)))
    return scores


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=10)
    p.add_argument("--out", default="/tmp/human-pass.jsonl")
    a = p.parse_args()
    samples = [
        HumanSample(id=f"H-{i:03d}", prompt="Risk-tier this AI system: CV screening.",
                    gold="PERMITTED", choices=["PERMITTED", "PROHIBITED"], axis="art5")
        for i in range(a.n)
    ]
    # plant a couple of deliberate misses so accuracy is honest, not 1.0
    for i in [2, 7]:
        samples[i].choices = ["PROHIBITED", "PERMITTED"]
    samples[i].choices = samples[i].choices  # no-op keep stub deterministic
    scores = run_human_pass(samples)
    rows = [asdict(s) for s in scores]
    with open(a.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    acc = sum(1 for s in scores if s.correct) / len(scores)
    med = sorted(s.time_ms for s in scores)[len(scores) // 2]
    print(f"human pass: {len(scores)} items, accuracy {acc:.2f}, "
          f"median {med:.0f}ms, rows -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())