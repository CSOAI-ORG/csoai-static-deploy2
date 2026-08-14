"""gspc_inspect.py — port a GSPC axis bank onto UK AISI's Inspect (MIT).

Inspect (https://inspect.aisi.org.uk, MIT) is the eval harness UK AISI and the
`inspect_evals` registry are built on. Porting a GSPC axis onto it makes our
deterministic, gold-labelled banks instantly interoperable with that ecosystem —
the credibility on-ramp into DSIT/AISI and NPL's Centre for AI Measurement.

Design fidelity: the SCORER here is the same contract as sovos_city.bench —
deterministic exact-label grading, one label or UNPARSED, unparsed counts wrong,
no model judges another. Inspect provides the model plumbing (providers, logs,
sandboxing); the *grading law* stays ours and stays deterministic.

Run (once `inspect_ai` is installed):
    inspect eval gspc_inspect.py@gspc_mcp --model openai/gpt-4o-mini
    inspect eval gspc_inspect.py@gspc_care --model anthropic/claude-3.5-sonnet

Register in inspect_evals by pointing at this task; the bank path is the only
axis-specific input.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List

try:
    from inspect_ai import Task, task
    from inspect_ai.dataset import Sample, MemoryDataset
    from inspect_ai.solver import generate, prompt_template
    from inspect_ai.scorer import scorer, Score, Target, accuracy, stderr, mean
    from inspect_ai.solver import TaskState
except Exception as e:  # pragma: no cover - import guard so the file is readable without the dep
    raise SystemExit(
        "gspc_inspect requires the Inspect harness: pip install inspect-ai\n"
        f"(import failed: {e})"
    )

# Banks name the item text under different keys; the label is always `expected`.
_TEXT_FIELDS = ("item", "scenario", "request", "operation", "tool", "case", "text",
                "question", "input", "prompt")


def _item_text(row: dict) -> str:
    for k in _TEXT_FIELDS:
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            return v
    cands = [v for k, v in row.items()
             if isinstance(v, str) and k not in ("expected", "label", "gold", "answer",
                                                 "category", "anchor", "note", "source")]
    return max(cands, key=len) if cands else ""


def _is_canary(row: dict) -> bool:
    if "_canary" in row:
        return True
    if str(row.get("expected", "")).upper() == "CANARY":
        return True
    return any("__CANARY__" in str(v) for v in row.values() if isinstance(v, str))


def _load(bank_path: str) -> tuple[List[Sample], List[str]]:
    rows = [json.loads(l) for l in Path(bank_path).read_text(encoding="utf-8").splitlines() if l.strip()]
    real = [r for r in rows if not _is_canary(r)]
    labels = sorted({str(r["expected"]) for r in real if r.get("expected")})
    samples = [Sample(input=_item_text(r), target=str(r["expected"]),
                      metadata={"labels": labels, "category": r.get("category")})
               for r in real if r.get("expected")]
    return samples, labels


@scorer(metrics=[accuracy(), stderr()])
def exact_label():
    """Deterministic exact-label scorer — bench.py's parse() as an Inspect scorer.

    The model must name EXACTLY ONE of the bank's labels; ambiguity or silence is
    UNPARSED and scored incorrect (never dropped). No model-as-judge.
    """
    async def score(state: TaskState, target: Target) -> Score:
        labels = state.metadata.get("labels", [])
        answer = (state.output.completion or "").upper()
        hits = [l for l in labels if re.search(r"\b" + re.escape(l.upper()) + r"\b", answer)]
        parsed = hits[0] if len(hits) == 1 else None
        correct = parsed is not None and parsed == str(target.text).upper()
        return Score(
            value=1.0 if correct else 0.0,
            answer=parsed or "UNPARSED",
            explanation=("exact-label match" if correct
                         else "UNPARSED (no single label)" if parsed is None
                         else f"answered {parsed}, gold {target.text}"),
        )
    return score


def _gspc_task(bank_path: str) -> Task:
    samples, labels = _load(bank_path)
    instruction = ("Answer with EXACTLY ONE of these labels and nothing else: "
                   + ", ".join(labels) + ".\n\n{prompt}")
    return Task(
        dataset=MemoryDataset(samples),
        solver=[prompt_template(instruction), generate()],
        scorer=exact_label(),
    )


# ── axis tasks (point each at its bank; paths are the only axis-specific input) ──
# Resolve the bank across the known locations (pod volume first, then Mac corpus).
_BANK_CANDIDATES = {
    "mcp": [
        "/runpod/board/banks/gspc-mcp.items.jsonl",
        "/Users/nicholas/clawd/oowm-v7-e2e/pod-corpus/gspc_banks_2026-08-05/gspc-mcp.items.jsonl",
    ],
}


def _bank(axis: str) -> str:
    for p in _BANK_CANDIDATES[axis]:
        if Path(p).exists():
            return p
    raise SystemExit(f"no bank found for axis {axis}; looked in {_BANK_CANDIDATES[axis]}")


@task
def gspc_mcp() -> Task:
    """GSPC mcp axis (CONFORMS/VIOLATES) as an Inspect eval — deterministic grading."""
    return _gspc_task(_bank("mcp"))
