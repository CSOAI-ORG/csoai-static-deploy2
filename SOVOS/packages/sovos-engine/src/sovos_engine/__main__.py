#!/usr/bin/env python3
"""sovos_engine CLI — EAT engine cycle: status / diagnose / fix.

Engine harness for the 14-axis GSPC board set. All state reads from the *signed*
manifests under SOVOS/boards-v2-2026-08-12/manifests/ and writes fix records to
SOVOS/benchmark-results/engine-fixes/. Signing is delegated to the repo-root sign.py
(Ed25519); when the sealed key is absent the record is left honestly unsigned.
"""
import argparse
import base64
import datetime
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

# --- repo / path resolution -------------------------------------------------
def find_repo_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "sign.py").exists() and (parent / "SOVOS").is_dir():
            return parent
    # fallback: run from SOVOS/ (cwd.parent == repo root)
    return Path.cwd().parent

REPO = find_repo_root()
MANIFEST_DIR = REPO / "SOVOS" / "boards-v2-2026-08-12" / "manifests"
FIX_DIR = REPO / "SOVOS" / "benchmark-results" / "engine-fixes"
SIGN_PY = REPO / "sign.py"

AXIS_LABELS = {
    "affect": "Affect/AffectBench",
    "agi": "AGI/AGIBench",
    "art5": "Article-5/Art5Bench",
    "asi": "ASI/ASIBench",
    "care": "Care/CareBench",
    "det": "Detector-interop/DetBench",
    "gov": "Governance/GovBench",
    "jail": "Jailbreak/JailBench",
    "mach": "Machine-verif/MachBench",
    "mcp": "MCP/MCPBench",
    "oss": "OSS/OSSBench",
    "prv": "Privacy/PrvBench",
    "swarm": "Swarm/SwarmVerdict",
    "xr": "Cross-reality/XRBench",
}

FLOOR = 0.05  # accuracy at/below this is "near-chance floor"


def load_manifest(axis: str) -> dict:
    path = MANIFEST_DIR / f"manifest_{axis}.json"
    if not path.exists():
        sys.exit(f"no manifest for axis '{axis}' at {path}")
    return json.load(open(path))


def all_axes() -> list:
    axes = []
    for f in sorted(glob.glob(str(MANIFEST_DIR / "manifest_*.json"))):
        d = json.load(open(f))
        axes.append(d)
    return axes


def prior_fixes(axis: str) -> list:
    out = []
    for f in sorted(glob.glob(str(FIX_DIR / f"fix_{axis}_*.json"))):
        try:
            out.append(json.load(open(f)))
        except Exception:
            pass
    return out


def gaps_for(man: dict) -> list:
    """Return a list of human-readable gap strings for one manifest."""
    gaps = []
    models = man.get("models", [])
    n_items = man.get("bank_items")
    if not models:
        gaps.append("no models in manifest — board may be unmeasured or schema mismatch")
        return gaps
    accs = [(m.get("model"), m.get("accuracy", 0.0), m.get("unparsed", 0)) for m in models]
    worst = min(accs, key=lambda x: x[1])
    best = max(accs, key=lambda x: x[1])
    # weak / floor models
    for name, acc, unparsed in sorted(accs, key=lambda x: x[1]):
        if acc <= FLOOR:
            gaps.append(f"weakest model {name} at {acc:.3f} — near-chance floor, check bank quality")
    # unparsed-heavy (format failure) models — likely transport/format, not capability
    for name, acc, unparsed in accs:
        if n_items and unparsed >= (n_items * 0.5) and acc < 0.2:
            gaps.append(
                f"{name}: {unparsed}/{n_items} unparsed at acc {acc:.3f} — format/transport failure dominates, "
                "distinguish true-negative from parse-noise"
            )
    # spread
    gaps.append(f"spread best→worst {best[1]:.3f}→{worst[1]:.3f} (n_models={len(models)})")
    # dedupe preserving order
    seen, out = set(), []
    for g in gaps:
        if g not in seen:
            seen.add(g)
            out.append(g)
    return out


def cmd_status() -> int:
    axes = all_axes()
    print(f"engine count: {len(axes)}")
    print(f"{'axis':8} {'items':>5} {'n':>3} {'status':9} {'best':24} {'best_acc':>8} {'worst':24} {'worst_acc':>9} {'spread':>7}")
    for d in axes:
        models = d.get("models", [])
        accs = [(m.get("model"), m.get("accuracy", 0.0)) for m in models]
        if not accs:
            print(f"{d['axis']:8} {d.get('bank_items','-'):>5} {len(models):>3} {d.get('status','-'):9}")
            continue
        best = max(accs, key=lambda x: x[1])
        worst = min(accs, key=lambda x: x[1])
        spread = best[1] - worst[1]
        print(f"{d['axis']:8} {d.get('bank_items','-'):>5} {len(models):>3} {d.get('status','-'):9} "
              f"{best[0]:24} {best[1]:8.3f} {worst[0]:24} {worst[1]:9.3f} {spread:7.3f}")
    return 0


def cmd_diagnose() -> int:
    axes = all_axes()
    print(f"diagnose over {len(axes)} engines\n")
    for d in axes:
        axis = d["axis"]
        fixes = prior_fixes(axis)
        last_fix = None
        for fx in fixes:
            lf = fx.get("fix", {}).get("applied_at")
            if lf and (last_fix is None or lf > last_fix):
                last_fix = lf
        print(f"=== {axis} ({AXIS_LABELS.get(axis, axis)}) · {d.get('status','?')} · "
              f"prior_fixes={len(fixes)}" + (f" · last_fix={last_fix[:10]}" if last_fix else " · last_fix=never"))
        for g in gaps_for(d):
            print(f"    - {g}")
        print()
    return 0


def cmd_fix(axis: str, delta: str) -> int:
    man = load_manifest(axis)
    models = man.get("models", [])
    fixes = prior_fixes(axis)
    last_fix = None
    for fx in fixes:
        lf = fx.get("fix", {}).get("applied_at")
        if lf and (last_fix is None or lf > last_fix):
            last_fix = lf

    before = {
        "axis": axis,
        "label": AXIS_LABELS.get(axis, axis),
        "board_status": man.get("status"),
        "gate": man.get("status"),  # MEASURED = measured gate
        "bank_items": man.get("bank_items"),
        "n_models": len(models) or None,
        "sha256": (man.get("signature", {}).get("body_sha256", "") or "")[:12],
        "last_fix": last_fix,
    }
    record = {
        "before": before,
        "fix": {
            "axis": axis,
            "delta": delta,
            "gaps_before": gaps_for(man),
            "applied_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "promoted": None,
            "reverted": None,
        },
    }
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    FIX_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIX_DIR / f"fix_{axis}_{ts}.json"
    with open(out_path, "w") as f:
        json.dump(record, f, indent=2)
    print(f"wrote fix record → {out_path}")

    # delegate signing to sign.py (never touch the key directly)
    if SIGN_PY.exists():
        r = subprocess.run(
            [sys.executable, str(SIGN_PY), "--sign", str(out_path)],
            cwd=str(REPO), capture_output=True, text=True,
        )
        if r.returncode == 0:
            print(f"✅ signed: {r.stdout.strip()}")
        else:
            print(f"⚠️  sign.py refused (key absent) — record left honestly UNSIGNED: {r.stderr.strip()}")
    else:
        print("⚠️  sign.py not found — record left honestly UNSIGNED")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="sovos_engine", description="EAT engine cycle harness")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="confirm engine count + per-axis state")
    sub.add_parser("diagnose", help="read gaps across all engines")
    pfix = sub.add_parser("fix", help="emit a fix record for one axis")
    pfix.add_argument("axis")
    pfix.add_argument("--delta", required=True, help="honest fix candidate text")
    a = ap.parse_args()

    if a.cmd == "status":
        return cmd_status()
    if a.cmd == "diagnose":
        return cmd_diagnose()
    if a.cmd == "fix":
        return cmd_fix(a.axis, a.delta)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
