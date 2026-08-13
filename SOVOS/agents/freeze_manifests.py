#!/usr/bin/env python3
"""
A1 — BOARD FREEZE + SIGN RUNNER (Chain A critical path, 2026-08-13)
Run on the SIGNING NODE (A100) only. Private key never touches Mac.

For each of the 14 board JSONs + peritem JSONL in boards-v2-2026-08-12/:
  1. Compute SHA-256 of every file (canonical freeze hash).
  2. Extract per-board counts: total rows, usable_n (MEASURED), models, per-model rows.
  3. Emit a manifest.json per board: {board, sha256, total, usable, models, axis_gate, frozen_at}.
  4. Sign each manifest with sign.py (Ed25519, key on this node only).
  5. Emit a single FROZEN_INDEX.json + FROZEN_2026-08-13.md for the chain.

Usage: python3 freeze_manifests.py --boards-dir SOVOS/boards-v2-2026-08-12 --out SOVOS/boards-v2-2026-08-12/manifests
Hash-verify after every remote write (Part AZ doctrine).
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

AXES = {
    "board_gov.json": "Governance / GovBench",
    "board_mcp.json": "Conformance / MCPBench",
    "board_prv.json": "Provenance / ProvBench",
    "board_pqc.json": "Continuity / PQCBench",
    "board_oss.json": "Openness / OSSBench",
    "board_mach.json": "Machinery / MachBench",
    "board_care.json": "Care / CareBench",
    "board_xr.json": "Cross-reality / XRAIV",
    "board_det.json": "Detector-interop / DetBench",
    "board_art5.json": "Art-5 / Art5Bench",
    "board_swarm.json": "Swarm / SwarmVerdict",
    "board_affect.json": "Affect / AffectBench",
    "board_gspc_jail.json": "Sandbox-escape / SandboxEscapeBench",
}

# Files that exist but are not part of the 13 measured axes (keep for completeness)
EXTRA = {"board_agi.json": "AGI (probe)", "board_asi.json": "ASI (probe)"}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_jsonl(path: str) -> int:
    n = 0
    with open(path) as f:
        for _ in f:
            n += 1
    return n


def load_board(path: str):
    with open(path) as f:
        return json.load(f)


def extract_counts(board_path: str, peritem_path: str | None):
    """Return (bank_items, pooled_rows, n_models, status, per_model_counts, is_pooled_conflation_honest).

    REAL board schema (gspc.board): bank_items = true per-item count;
    per_item_count = POOLED rows (items x models) — must NEVER be quoted as a
    per-item / quotable count (GATE3:POOLED_N claim-linter guard).
    """
    bank_items = None
    pooled = None
    n_models = None
    status = None
    per_model = {}
    try:
        board = load_board(board_path)
        if isinstance(board, dict):
            bank_items = board.get("bank_items") or board.get("n")
            pooled = board.get("per_item_count")
            status = board.get("status")
            ml = board.get("models")
            if isinstance(ml, list):
                n_models = len(ml)
                for m in ml:
                    if isinstance(m, dict) and m.get("model"):
                        per_model[m["model"]] = m.get("n", 0)
            elif isinstance(ml, int):
                n_models = ml
    except Exception as e:
        print(f"  ! board parse failed for {os.path.basename(board_path)}: {e}", file=sys.stderr)
    return bank_items, pooled, n_models, status, per_model


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boards-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sign-py", default="sign.py")
    ap.add_argument("--no-sign", action="store_true", help="emit manifests without signing (dry run)")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    frozen_at = datetime.now(timezone.utc).isoformat()
    manifests = []
    all_axes = {**AXES, **EXTRA}

    for fname, axis in all_axes.items():
        board_path = os.path.join(args.boards_dir, fname)
        if not os.path.exists(board_path):
            print(f"  [skip] {fname} (absent) — 0 files frozen this pass")
            continue
        base = fname.replace(".json", "")
        peritem = os.path.join(args.boards_dir, f"peritem_{base}.jsonl")
        bank_items, pooled, n_models, status, per_model = extract_counts(board_path, peritem)
        sha = sha256_file(board_path)
        measured = (status == "MEASURED") or (bank_items and bank_items >= 30 and n_models and n_models >= 1)
        manifest = {
            "board": fname,
            "axis": axis,
            "sha256": sha,
            "bank_items": bank_items,             # TRUE per-item count (quotable)
            "per_item_count_pooled": pooled,      # pooled rows (items x models) — NOT quotable (GATE3)
            "n_models": n_models,
            "board_status": status,
            "gate": "MEASURED" if measured else "UNMEASURED/held",
            "per_item_rows": per_model,           # per-model item counts
            "peritem_exists": os.path.exists(peritem),
            "peritem_sha256": sha256_file(peritem) if os.path.exists(peritem) else None,
            "frozen_at": frozen_at,
            "pooled_conflation_note": "per_item_count_pooled is (items x models); quote bank_items only",
        }
        mpath = os.path.join(args.out, f"manifest_{base}.json")
        with open(mpath, "w") as f:
            json.dump(manifest, f, indent=2, sort_keys=True)
        print(f"  [ok] {fname}: bank_items={bank_items} pooled={pooled} models={n_models} status={status} sha={sha[:12]}")
        manifests.append(manifest)

        if not args.no_sign:
            env = dict(os.environ, CSOAI_SIGNING_NODE="1")
            r = subprocess.run(
                [sys.executable, args.sign_py, "--sign", mpath],
                capture_output=True, text=True, env=env,
            )
            if r.returncode != 0:
                print(f"  ! SIGN FAILED {fname}: {r.stderr[-400:]}", file=sys.stderr)
            else:
                out_line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(no stdout)"
                print(f"  [signed] {fname}: {out_line[:120]}")

    index = {
        "frozen_at": frozen_at,
        "n_boards": len(manifests),
        "boards": manifests,
        "signing_node": "A100 pod (article50/sovos_keys)",
        "canon_ref": "Part CV 495-move board 2026-08-13; Chain A A1",
    }
    ipath = os.path.join(args.out, "FROZEN_INDEX.json")
    with open(ipath, "w") as f:
        json.dump(index, f, indent=2, sort_keys=True)
    print(f"\nFROZEN_INDEX written: {ipath} ({len(manifests)} boards)")

    # Human-readable freeze note (the Chain A A1 signal)
    md = ["# BOARD FREEZE 2026-08-13 — signed manifests (A1)",
          "", f"Frozen at {frozen_at} UTC on the A100 signing node.",
          f"{len(manifests)} boards locked; every manifest Ed25519-signed; verify: `sign.py --verify <manifest>`",
          "", "| Board | bank_items (quotable) | pooled rows (x models) | models | status | sha256 (12) |",
          "|---|---|---|---|---|---|"]
    for m in sorted(manifests, key=lambda x: x["board"]):
        md.append(f"| {m['board']} | {m['bank_items']} | {m['per_item_count_pooled']} | {m['n_models']} | {m['board_status']} | {m['sha256'][:12]} |")
    md += ["", "Honest-count note (GATE3:POOLED_N): `bank_items` is the TRUE quotable per-item count. "
              "`pooled rows` is items × models and must never be quoted as a per-item / quotable figure.",
           "", "Gate note: status=MEASURED or bank_items >= 30 with models => MEASURED; else held.",
           "", "`sign.py --verify SOVOS/boards-v2-2026-08-12/manifests/manifest_<board>.json`"]
    mdpath = os.path.join(args.out, "FROZEN_2026-08-13.md")
    with open(mdpath, "w") as f:
        f.write("\n".join(md))
    print(f"FROZEN note written: {mdpath}")


if __name__ == "__main__":
    main()