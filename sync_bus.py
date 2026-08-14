#!/usr/bin/env python3
"""sync_bus.py — the OWM sync layer. Distills every node's axis-engine boards into
ONE compact world-state card (the IWM), and writes it where every node + the web
VWM read a single truth.

The 3KB · IWM · OWM · VWM operating model, made concrete:
  IWM = the compact signed world-state card this emits (kept small on purpose)
  OWM = syncing that card to a shared feed every node/site reads
  VWM = the web visual (sov-space-vwm.html) rendering it live

    python3 sync_bus.py --out dist/world-state.json

Reads gspc_flywheel boards from ANY node (measured on M4, 3090, A100 — same
harness, bit-identical), keeps the latest score per (model, axis), distills to a
compact card. This is the operating STATE, not the raw evidence — small by design.
Sign it on the A100 (frozen crust) + push to KV/HF for the OWM layer.
"""
import argparse, json, glob, os, hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent


def collect_boards(pattern):
    boards = []
    for p in glob.glob(pattern):
        try:
            d = json.load(open(p))
            if isinstance(d, dict) and "results" in d:
                d["_mtime"] = os.path.getmtime(p)
                boards.append(d)
        except Exception:
            pass
    return sorted(boards, key=lambda b: b["_mtime"])   # oldest→newest so latest wins


def distill(boards):
    world, control = {}, None
    for b in boards:
        control = b.get("control") or control
        for m, v in b.get("results", {}).items():
            node = world.setdefault(m, {"axes": {}, "mean": None})
            for ax, r in (v.get("axes") or {}).items():
                if isinstance(r, dict) and r.get("status") == "MEASURED":
                    node["axes"][ax] = round(r["score"], 3)
            if v.get("mean") is not None:
                node["mean"] = round(v["mean"], 3)
    return control, world


def main():
    ap = argparse.ArgumentParser(description="OWM sync bus: distill axis boards → compact world-state card (IWM).")
    ap.add_argument("--pattern", default=str(ROOT / "benchmark-results/gspc_flywheel/*.json"))
    ap.add_argument("--out", default=str(ROOT / "dist/world-state.json"))
    a = ap.parse_args()

    boards = collect_boards(a.pattern)
    control, world = distill(boards)
    card = {
        "kind": "sovos.world-state.iwm",
        "at": datetime.now(timezone.utc).isoformat(),
        "control": control,
        "n_boards": len(boards),
        "n_models": len(world),
        "models": {m: {"mean": v["mean"], "axes": v["axes"]} for m, v in sorted(world.items())},
    }
    body = json.dumps(card, separators=(",", ":"), sort_keys=True)
    card["sha256"] = hashlib.sha256(body.encode()).hexdigest()

    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(card, indent=1))
    size = len(json.dumps(card))
    fit = "within 3KB ✓ (a true IWM card)" if size <= 3072 else f">{3072}B — trim axes or top-N models"
    print(f"  world-state IWM card: {len(world)} models · {len(boards)} boards · {size} bytes — {fit}")
    print(f"  sha256 {card['sha256'][:16]}…  → {out}")
    print("  OWM: sign on A100 (frozen) + push to KV/HF; VWM: point sov-space-vwm.html here for one live truth.")


if __name__ == "__main__":
    main()
