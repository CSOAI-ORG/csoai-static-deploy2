#!/usr/bin/env python3
"""Guard test: run stage_publish on a board with REAL sov6-* model names
and assert NO banned codename leaks into any emitted artifact."""
import json, os, re, subprocess, sys, tempfile

BANNED = re.compile(r"\b(SOVOS|SOV4|sov4|sov6|sov34|sov-|sovereign os|sovereign-os)\b", re.I)

board = {
    "control": "sov6-ethics-v3-light",
    "measured_at": "2026-08-13T00:00:00Z",
    "results": {
        "sov6-ethics-v3-light": {"mean": 0.45, "axes": {"gov": {"status": "MEASURED", "score": 0.45}}},
        "sov6-logic-v3-light": {"mean": 0.38, "axes": {"gov": {"status": "MEASURED", "score": 0.38}}},
        "qwen2.5:0.5b-instruct": {"mean": 0.41, "axes": {"gov": {"status": "MEASURED", "score": 0.41}}},
        "gemma3:12b": {"mean": 0.52, "axes": {"gov": {"status": "MEASURED", "score": 0.52}}},
    },
}
with tempfile.TemporaryDirectory() as d:
    bp = os.path.join(d, "board.json")
    with open(bp, "w") as f:
        json.dump(board, f)
    out = os.path.join(d, "out")
    r = subprocess.run([sys.executable, "stage_publish.py", "--board", bp, "--out", out],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("STAGE FAILED:", r.stderr[-500:]); sys.exit(1)
    leaks = {}
    for root, _, files in os.walk(out):
        for fn in files:
            p = os.path.join(root, fn)
            txt = open(p, encoding="utf-8", errors="replace").read()
            hits = BANNED.findall(txt)
            if hits:
                leaks[fn] = sorted(set(hits))
    print("PROC OUTPUT:", r.stdout.strip())
    print("EMITTED FILES:", sorted(os.listdir(out)))
    print("CODENAME LEAKS:", leaks if leaks else "NONE ✅")
    # board.json is the RAW SIGNED EVIDENCE — exempt (internal record, gated),
    # but PUBLISH.md must NOT tell the user to upload it to the public dataset.
    assert os.path.exists(os.path.join(out, "board.json")), "raw board must be kept (evidence)"
    # The 4 generated public-facing artifacts must be clean of codenames:
    for pub in ("scorecard.html", "README.md", "dataset.jsonld", "PUBLISH.md"):
        assert "sov6" not in open(os.path.join(out, pub)).read().lower(), f"sov6 leaked in {pub}"
    # PUBLISH.md must gate the raw board, not auto-upload it
    pubmd = open(os.path.join(out, "PUBLISH.md")).read()
    assert "upload {out} / ." not in pubmd and "upload" in pubmd and "GATED" in pubmd, "PUBLISH.md must gate raw board"
    # descriptive suffix preserved (identity kept for transparency)
    sc = open(os.path.join(out, "scorecard.html")).read()
    assert "ethics-v3-light" in sc, "descriptive suffix not preserved"
    print("✅ GUARD PASS — sov6-* stripped from all public artifacts, raw board gated, identity preserved")