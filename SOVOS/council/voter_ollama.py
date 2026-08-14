#!/usr/bin/env python3
"""voter_ollama.py — council voter, ollama API path (A100, or any ollama host).

Independent measurement implementation #2. Same frozen probes, same canonical vote,
DIFFERENT inference stack: ollama/llama.cpp runtime instead of HF transformers.

The candidate adapter must exist as an ollama tag (merge + GGUF via the estate's
llama-quantize path, then `ollama create`). If the after-tag is absent this voter
ABSTAINS — UNMEASURED is a valid, honest vote; a guessed one is not.

  python3 voter_ollama.py --before-tag qwen2.5:1.5b-instruct \
      --after-tag sov-candidate:latest --axes governance safety --out votes/run1
"""
from __future__ import annotations
import argparse, hashlib, json, socket, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent.parent))
import gspc_flywheel as gf
from verdict import vote_from_rows


def _gen_ollama(host, tag, prompt, max_new=8):
    body = {"model": tag, "prompt": prompt, "stream": False,
            "options": {"temperature": 0, "seed": 42, "num_predict": max_new}}
    req = urllib.request.Request(f"{host}/api/generate",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read()).get("response", "")


def _tags(host):
    with urllib.request.urlopen(f"{host}/api/tags", timeout=30) as r:
        return {m["name"] for m in json.loads(r.read()).get("models", [])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before-tag", required=True)
    ap.add_argument("--after-tag", required=True)
    ap.add_argument("--axes", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--host", default="http://127.0.0.1:11434")
    ap.add_argument("--voter-id", default=None)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    tags = _tags(a.host)
    missing = [t for t in (a.before_tag, a.after_tag) if t not in tags]
    if missing:
        verdict = {"vote": "ABSTAIN",
                   "reason": f"ollama tag(s) absent: {missing} — merge+GGUF the "
                             "candidate first (estate llama-quantize path). "
                             "UNMEASURED, never guessed.",
                   "voter_id": a.voter_id or f"ollama@{socket.gethostname()}",
                   "implementation": "ollama/llama.cpp/t0-seed42",
                   "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        (out / "verdict.json").write_text(json.dumps(verdict, indent=1) + "\n")
        print(json.dumps({"verdict": "ABSTAIN", "missing": missing}, indent=1))
        return

    rows = []
    for ax in a.axes:
        spec = gf.AXES[ax]
        for idx, (prompt, expected) in enumerate(spec["items"]):
            full = spec["instruction"] + prompt
            b = gf.extract(_gen_ollama(a.host, a.before_tag, full), spec["tokens"])
            af = gf.extract(_gen_ollama(a.host, a.after_tag, full), spec["tokens"])
            rows.append({"item": prompt[:120], "axis": ax,
                         "pool": "even" if idx % 2 == 0 else "odd",
                         "expected": expected, "before": b, "after": af})
    (out / "rows.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    rows_sha = hashlib.sha256((out / "rows.jsonl").read_bytes()).hexdigest()
    verdict = vote_from_rows(rows)
    verdict.update({
        "voter_id": a.voter_id or f"ollama@{socket.gethostname()}",
        "implementation": "ollama/llama.cpp/t0-seed42",
        "before_tag": a.before_tag, "after_tag": a.after_tag, "axes": a.axes,
        "rows_sha256": rows_sha,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    })
    (out / "verdict.json").write_text(json.dumps(verdict, indent=1) + "\n")
    print(json.dumps({"verdict": verdict["vote"],
                      "delta_unseen": verdict.get("delta_unseen"),
                      "rows": len(rows), "out": str(out)}, indent=1))


if __name__ == "__main__":
    main()
