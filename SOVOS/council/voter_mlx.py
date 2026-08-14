#!/usr/bin/env python3
"""voter_mlx.py — council voter, Apple Silicon MLX path (the Mac).

Independent measurement implementation #3. Same frozen probes, same canonical vote,
THIRD inference stack: mlx-lm on Metal instead of HF transformers or llama.cpp.

Requires: pip install mlx-lm, and the candidate as an MLX-loadable model directory
(base + fused adapter: `python -m mlx_lm.fuse --model <base> --adapter-path <adapter>`).
If mlx-lm or the fused candidate is absent this voter ABSTAINS — honestly.

  python3 voter_mlx.py --base Qwen/Qwen2.5-1.5B-Instruct \
      --fused-candidate ./fused_candidate --axes governance safety --out votes/run1
"""
from __future__ import annotations
import argparse, hashlib, json, socket, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent.parent))
import gspc_flywheel as gf
from verdict import vote_from_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--fused-candidate", required=True)
    ap.add_argument("--axes", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--voter-id", default=None)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    try:
        from mlx_lm import load, generate
    except ImportError:
        verdict = {"vote": "ABSTAIN",
                   "reason": "mlx-lm not installed on this host — UNMEASURED, "
                             "never guessed. pip install mlx-lm to enfranchise "
                             "this voter.",
                   "voter_id": a.voter_id or f"mlx@{socket.gethostname()}",
                   "implementation": "mlx-lm/metal",
                   "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        (out / "verdict.json").write_text(json.dumps(verdict, indent=1) + "\n")
        print(json.dumps({"verdict": "ABSTAIN", "reason": "mlx-lm absent"}, indent=1))
        return
    if not Path(a.fused_candidate).exists():
        verdict = {"vote": "ABSTAIN",
                   "reason": f"fused candidate {a.fused_candidate} absent — run "
                             "mlx_lm.fuse first. UNMEASURED, never guessed.",
                   "voter_id": a.voter_id or f"mlx@{socket.gethostname()}",
                   "implementation": "mlx-lm/metal",
                   "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        (out / "verdict.json").write_text(json.dumps(verdict, indent=1) + "\n")
        print(json.dumps({"verdict": "ABSTAIN", "reason": "fused candidate absent"},
                         indent=1))
        return

    base_model, base_tok = load(a.base)
    cand_model, cand_tok = load(a.fused_candidate)
    rows = []
    for ax in a.axes:
        spec = gf.AXES[ax]
        for idx, (prompt, expected) in enumerate(spec["items"]):
            full = spec["instruction"] + prompt
            msgs = [{"role": "user", "content": full}]
            pb = base_tok.apply_chat_template(msgs, tokenize=False,
                                              add_generation_prompt=True)
            pa = cand_tok.apply_chat_template(msgs, tokenize=False,
                                              add_generation_prompt=True)
            b = gf.extract(generate(base_model, base_tok, prompt=pb,
                                    max_tokens=8, verbose=False), spec["tokens"])
            af = gf.extract(generate(cand_model, cand_tok, prompt=pa,
                                     max_tokens=8, verbose=False), spec["tokens"])
            rows.append({"item": prompt[:120], "axis": ax,
                         "pool": "even" if idx % 2 == 0 else "odd",
                         "expected": expected, "before": b, "after": af})
    (out / "rows.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    rows_sha = hashlib.sha256((out / "rows.jsonl").read_bytes()).hexdigest()
    verdict = vote_from_rows(rows)
    verdict.update({
        "voter_id": a.voter_id or f"mlx@{socket.gethostname()}",
        "implementation": "mlx-lm/metal",
        "base": a.base, "fused_candidate": a.fused_candidate, "axes": a.axes,
        "rows_sha256": rows_sha,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    })
    (out / "verdict.json").write_text(json.dumps(verdict, indent=1) + "\n")
    print(json.dumps({"verdict": verdict["vote"],
                      "delta_unseen": verdict.get("delta_unseen"),
                      "rows": len(rows), "out": str(out)}, indent=1))


if __name__ == "__main__":
    main()
