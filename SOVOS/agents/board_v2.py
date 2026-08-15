"""GSPC 13-axis board v2 runner — streams per-item rows, Wilson CIs, MinIO backup.

Doctrine (SOVOS bench.py, recovered boards 2026-08-12):
  - label set comes from each bank itself (never hardcoded)
  - canary rows (truthy _canary, or expected=="CANARY") excluded from every score
  - exact-label grading; an answer that names !=1 label is UNPARSED and counts
    incorrect (never dropped). A transport failure is OURS and excluded (not a
    model failure).
  - nothing quoted below usable n>=30 (Wilson z=1.959964)

Running (resumable):
  - if peritem_{axis}.jsonl already exists, the axis is skipped -> a reboot costs
    at most one axis
  - per-item rows are written to disk as each lands (BY doctrine: no run may hold
    >5min of unlanded rows)
  - board_{axis}.json is written + uploaded to MinIO as each axis completes

Severity: banks carrying `severity`/`severity_basis` (gspc-affect) propagate them
into per-item rows.
"""

from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional, Tuple

MIN_N = 30
Z = 1.959964
OLLAMA = "http://localhost:11434/api/generate"

BANKS = ["gov", "agi", "asi", "prv", "xr", "det", "art5",
         "care", "mcp", "oss", "mach", "swarm", "affect"]
HF_URL = "https://huggingface.co/datasets/csoai/gspc-{ax}/resolve/main/items.jsonl"

MODELS = [
    "sov6-ethics-v3-light", "sov6-logic-v3-light", "sov6-agency-v3-light",
    "sov6-identity-v3-light", "sov6-preservation-v3-light", "sov6-destruction-v3-light",
    "sov6-creation-v3-light", "sov6-relationality-v3-light", "sov6-temporality-v3-light",
    "sov6-synthesis-v3-light", "sov6-embodiment-v3-light", "sov6-aesthetics-v3-light",
    "sov6-abstraction-v3-light",
    "gemma3:12b", "llama3.2:3b", "qwen2.5:3b", "qwen2.5:0.5b-instruct",
    "mistral:7b", "deepseek-r1:8b",
]

WORKERS = 4

TEXT_FIELDS = ("item", "scenario", "request", "operation", "tool", "case", "text",
               "question", "input", "prompt")


def log(msg: str):
    print(msg, flush=True)


def fetch_bank(ax: str) -> Tuple[Optional[List[Dict]], Optional[int], Optional[str]]:
    """Return (real_items, canary_count, err_str). Canaries never reach a score."""
    url = HF_URL.format(ax=ax)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "sovos-board-v2"})
        with urllib.request.urlopen(req, timeout=120) as r:
            txt = r.read().decode("utf-8")
    except Exception as e:  # noqa: BLE001
        return None, None, f"fetch failed: {type(e).__name__}: {e}"
    rows = [json.loads(l) for l in txt.splitlines() if l.strip()]
    can = [r for r in rows if r.get("_canary") or str(r.get("expected")) == "CANARY"]
    real = [r for r in rows if not (r.get("_canary") or str(r.get("expected")) == "CANARY")]
    if not real:
        return None, len(can), "bank had 0 real items after canary exclusion"
    return real, len(can), None


def label_set(items: List[Dict]) -> List[str]:
    return sorted({str(r["expected"]) for r in items if r.get("expected")})


def item_text(item: Dict) -> str:
    for k in TEXT_FIELDS:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v
    cands = [v for k, v in item.items()
             if isinstance(v, str) and k not in ("expected", "label", "gold", "answer",
                                                 "category", "anchor", "note", "source")]
    return max(cands, key=len) if cands else ""


def prompt_for(item: Dict, labels: List[str]) -> str:
    return (f"{item_text(item)}\n\n"
            f"Answer with EXACTLY ONE of these labels and nothing else: {', '.join(labels)}.")


def parse(answer: str, labels: List[str]) -> Optional[str]:
    if not answer:
        return None
    up = answer.upper()
    hits = [l for l in labels if re.search(r"\b" + re.escape(l.upper()) + r"\b", up)]
    return hits[0] if len(hits) == 1 else None


def ask_ollama(model: str, prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (raw_text, err). err is a TRANSPORT failure = OURS, never model evidence."""
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0, "num_predict": 600}}).encode()
    try:
        req = urllib.request.Request(OLLAMA, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read().decode())
        return data.get("response", ""), None
    except Exception as e:  # noqa: BLE001
        return None, f"TRANSPORT {type(e).__name__}: {e}"


def wilson(k: int, n: int, z: float = Z) -> Optional[Tuple[float, float]]:
    if n < MIN_N:
        return None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - m) / d), min(1.0, (c + m) / d))


def run_axis(ax: str, outdir: Path) -> Dict:
    peritem_path = outdir / f"peritem_{ax}.jsonl"
    board_path = outdir / f"board_{ax}.json"

    # RESUME: axis already measured -> skip. Reboot costs at most one axis.
    if peritem_path.exists():
        log(f"[{ax}] RESUME-SKIP: {peritem_path.name} exists, marking axis done")
        return {"axis": ax, "status": "RESUME-SKIP"}
    if board_path.exists():
        log(f"[{ax}] RESUME-SKIP: {board_path.name} exists, marking axis done")
        return {"axis": ax, "status": "RESUME-SKIP"}

    items, canaries, err = fetch_bank(ax)
    if err:
        log(f"[{ax}] SKIP: {err}")
        return {"axis": ax, "status": "SKIP", "reason": err, "status_note": err}
    labels = label_set(items)
    majority = (max(sum(1 for i in items if str(i["expected"]) == l) for l in labels) / len(items)
                if items else None)
    log(f"[{ax}] bank_items={len(items)} canaries_excluded={canaries} "
        f"labels={labels} majority_baseline={majority} models={len(MODELS)} -> "
        f"{len(items)*len(MODELS)} calls (~{len(items)*len(MODELS)//WORKERS} per worker)")

    lock = Lock()
    nrows = 0
    tmp = peritem_path.with_suffix(".jsonl.tmp")

    def work(item: Dict, model: str) -> Dict:
        raw, terr = ask_ollama(model, prompt_for(item, labels))
        got = None if terr else parse(raw, labels)
        row = {
            "axis_item": item.get("anchor") or item_text(item)[:80],
            "item": item_text(item),
            "category": item.get("category"),
            "expected": item.get("expected"),
            "model": model,
            "raw": (raw or "")[:400],
            "parsed": got,
            "correct": (got == str(item["expected"])) if got else False,
            "unparsed": (got is None and not terr),
            "transport_error": terr,
        }
        # severity-aware: propagate severity fields if the bank carries them
        for sk in ("severity", "severity_basis"):
            if sk in item:
                row[sk] = item[sk]
        return row

    # Build task list (item_index, model). Dedup identical (item,model) not needed.
    tasks = [(it, m) for it in items for m in MODELS]

    # Write header-independent: each row flushed as it lands
    with open(tmp, "w", encoding="utf-8") as fh:
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futs = {ex.submit(work, it, m): (it, m) for it, m in tasks}
            for fut in as_completed(futs):
                row = fut.result()
                with lock:
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                    fh.flush()
                    nrows += 1
                    if nrows % 50 == 0:
                        log(f"[{ax}] streamed {nrows}/{len(tasks)} rows")
                    # BY durability hardening (2026-08-12): flush the in-progress
                    # .tmp to MinIO every 200 rows so a mid-axis reboot loses at
                    # most ~200 rows, not the whole axis. Completed axes were already
                    # durable; this closes the mid-axis loss window.
                    if nrows % 200 == 0 and mc_upload(tmp, "corpus/boards-v2-2026-08-12/wip"):
                        log(f"[{ax}] WIP flushed {nrows} rows to MinIO")

    tmp.replace(peritem_path)

    # Aggregate per-model from the streamed rows (exclude transport rows from n).
    rows = [json.loads(l) for l in peritem_path.read_text().splitlines() if l.strip()]
    by_model: Dict[str, List[Dict]] = {}
    for r in rows:
        by_model.setdefault(r["model"], []).append(r)

    model_boards = []
    for m in MODELS:
        ms = by_model.get(m, [])
        usable = [r for r in ms if not r.get("transport_error")]
        k = sum(1 for r in usable if r["correct"])
        n = len(usable)
        unparsed = sum(1 for r in usable if r.get("unparsed"))
        acc = (k / n) if n else None
        ci = wilson(k, n) if n else None
        quot = bool(n >= MIN_N)
        model_boards.append({
            "model": m, "n": n, "correct": k, "unparsed": unparsed,
            "accuracy": (round(acc, 4) if (acc is not None and quot) else None),
            "ci95": ([round(x, 4) for x in ci] if ci else None),
            "quotable": quot,
            "note": (None if quot else f"usable n={n} < {MIN_N} — no score quoted"),
        })

    quotable_rows = [r for r in model_boards if r["quotable"] and r["accuracy"] is not None]
    best = max(quotable_rows, key=lambda r: r["accuracy"])["model"] if quotable_rows else None
    board = {
        "kind": "gspc.board",
        "axis": ax,
        "bank_items": len(items),
        "canaries_excluded": canaries,
        "labels": labels,
        "majority_baseline": round(majority, 4) if majority is not None else None,
        "models": model_boards,
        "best": best,
        "status": ("MEASURED" if quotable_rows else "UNMEASURED"),
        "status_note": (None if quotable_rows else
                        f"no model reached {MIN_N} usable items; axis stays UNMEASURED"),
        "per_item_count": len(rows),
        "method": ("unparsed counted incorrect · transport failures excluded as ours · "
                   "canaries excluded · deterministic exact-label grading, no model judges "
                   "another model · nothing quoted below usable n>=30"),
    }
    board_path.write_text(json.dumps(board, ensure_ascii=False, indent=2), encoding="utf-8")
    ntot = sum(1 for r in rows if r.get("transport_error"))
    log(f"[{ax}] DONE rows={len(rows)} transport_errors={ntot} best={best} "
        f"majority_baseline={board['majority_baseline']}")
    return board


def mc_upload(path: Path, bucket_dir: str = "corpus/boards-v2-2026-08-12") -> Optional[str]:
    """Upload to MinIO. Returns mc stderr/stdout or None on failure."""
    try:
        r = subprocess.run(["mc", "cp", str(path),
                            f"sovos/{bucket_dir}/{path.name}"],
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out or None if r.returncode == 0 else (out or f"mc exit {r.returncode}")
    except Exception as e:  # noqa: BLE001
        return f"mc upload error: {type(e).__name__}: {e}"


def main() -> None:
    outdir = Path("/workspace/csoai-static-deploy2/SOVOS/boards-v2-2026-08-12")
    outdir.mkdir(parents=True, exist_ok=True)

    # MinIO alias
    envp = Path("/root/.sovos-master/credentials.env")
    if envp.exists():
        for line in envp.read_text().splitlines():
            if "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())
    subprocess.run(["mc", "alias", "set", "sovos", "http://127.0.0.1:9000",
                    os.environ.get("MINIO_ROOT_USER", ""),
                    os.environ.get("MINIO_ROOT_PASSWORD", "")],
                   capture_output=True, text=True)

    all13 = {"kind": "gspc.board.all13", "generated": 20260812, "axes": []}
    all13_path = outdir / "board_all13.json"
    if all13_path.exists():
        try:
            all13 = json.loads(all13_path.read_text())
        except Exception:
            all13 = {"kind": "gspc.board.all13", "generated": 20260812, "axes": []}

    for ax in BANKS:
        try:
            board = run_axis(ax, outdir)
        except Exception as e:  # noqa: BLE001
            log(f"[{ax}] EXCEPTION: {type(e).__name__}: {e}")
            board = {"axis": ax, "status": "ERROR", "reason": f"{type(e).__name__}: {e}"}

        # stream board_* + peritem to MinIO as each axis completes (incl. errors)
        for f in (outdir / f"board_{ax}.json", outdir / f"peritem_{ax}.jsonl"):
            if f.exists():
                up = mc_upload(f)
                log(f"[{ax}] MINIO {f.name}: {up if up else 'uploaded'}")

        if board.get("status") in ("MEASURED", "UNMEASURED"):
            all13["axes"] = [a for a in all13["axes"] if a.get("axis") != ax] + [board]
            all13_path.write_text(json.dumps(all13, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
            all13_path.with_suffix(".json.tmp").unlink(missing_ok=True)
        log(f"[  ] completed {ax} -> {board.get('status')}")

    log("ALL13-AXES-PROCESSED")


if __name__ == "__main__":
    main()