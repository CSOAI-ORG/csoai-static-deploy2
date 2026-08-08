#!/usr/bin/env python3
"""sov3.py — THE MASTER. The convergence world-mind: V/I/O world models as one command.

    python3 sov3.py --status              # the whole mind, one screen: what is measured, what is honest
    python3 sov3.py --pipeline            # local chain: signal → phlabet → spine → reflection
    python3 sov3.py --query "..."         # ask the mind: which measured lessons apply

WHAT THIS IS
"Eat all into master." Every piece the estate built is a scattered script; sov3 is the one entrypoint
that composes them into the convergence Nick drew in SOVOS GOAL:

   Layer 0 (SOVOS harness)  ─ measures ─▶  SOV Signal (iWM: inner world model, per item, accreting)
   SOV Signal  ─ phlabet ─▶  J-Space cards  ─ spine ─▶  the card graph
   SOPHOS  ─ reflects ─▶  keeps every layer honest (seven eyes)
   the three views of ONE structure:  IWM inner · OWM outer · VWM visual

sov3 does NOT invent numbers. It reports what each layer actually produced, and where a layer is
absent it says so — an absent world model is a gap to build, never a blank to fill with a claim.
The doc's grander pieces (GNN training, the JEPA Dream Engine, the UE5 render) are marked STAGED here,
not faked: the master is honest about which of its organs are alive.
"""
import argparse, json, os, subprocess, sys, glob, hashlib

A = os.path.expanduser("~/clawd/_alignment")
HERE = os.path.dirname(os.path.abspath(__file__))
P = {
    "verdict":  glob.glob(f"{A}/SOVOS_VERDICT_*.json"),
    "signal":   glob.glob(f"{A}/SOV_SIGNAL/*.jsonl"),
    "deck":     f"{A}/PHLABET_DECK.json",
    "spine":    f"{A}/SPINE_GRAPH.json",
    "sophos":   f"{A}/SOPHOS_REFLECTION.json",
    "board":    f"{A}/CROSS_COMPANY_BOARD.json",
}


def _load(p):
    try: return json.load(open(p))
    except Exception: return None


def status():
    print("SOV3 — the convergence mind. What is measured, and what is honest about not being.\n")

    # LAYER 0 — the harness verdict
    verdicts = [(_load(p), p) for p in P["verdict"]]
    verdicts = [(v, p) for v, p in verdicts if v]
    print("  LAYER 0 · SOVOS harness")
    if not verdicts:
        print("    (no signed verdict yet)")
    for v, p in verdicts:
        m = v.get("layer0", {}).get("model", "?")
        for ax, s in v.get("measured_axes", {}).items():
            iv = s.get("interval")
            tag = f"interval={iv}" if iv else f"(n={s.get('usable_n')} < 30, no interval)"
            print(f"    {m} · {ax:<12} acc={s.get('accuracy')} {tag}")

    # IWM — inner world model = the SOV Signal, accreting; compressed into the Phlabet deck
    print("\n  IWM · inner world model (SOV Signal → Phlabet)")
    n_rows = sum(sum(1 for _ in open(f, errors="ignore")) for f in P["signal"]) if P["signal"] else 0
    print(f"    signal: {len(P['signal'])} file(s), {n_rows} per-item rows"
          if P["signal"] else "    signal: none — run a measurement first")
    deck = _load(P["deck"])
    if deck:
        cards = deck.get("cards", [])
        comp = f"{len(cards)} J-Space cards (deck {deck.get('sha256')})"
        print(f"    phlabet: {comp}")
    else:
        print("    phlabet: no deck yet")

    # SPINE — the card graph
    spine = _load(P["spine"])
    print("\n  SPINE · J-Space card graph (GNN retrieval now, training GPU-gated)")
    print(f"    {spine['n_nodes']} nodes · {spine['n_edges']} edges (graph {spine.get('sha256')})"
          if spine else "    no graph yet — run phlabet then spine")

    # OWM + VWM — outer (simulation) and visual (render): staged surfaces, honestly flagged
    print("\n  OWM · outer world model (simulation / clans / physical)   STAGED — data model not built")
    print("  VWM · visual world model (globe render)")
    for f in ("sovspace.html", "sovspace-os.html", "globe3d.html"):
        fp = os.path.expanduser(f"~/clawd/councilof-ai/client/public/{f}")
        print(f"    {'✓' if os.path.exists(fp) else '✗'} {f}")

    # SOPHOS — the reflection
    soph = _load(P["sophos"])
    print("\n  SOPHOS · reflection (seven eyes)")
    if soph:
        alerts = [e for e in soph.get("eyes", []) if e["status"] == "ALERT"]
        blind = [e for e in soph.get("eyes", []) if e["status"] == "BLIND"]
        print(f"    spine {soph.get('sha256')} · {len(alerts)} alert(s), {len(blind)} blind eye(s)")
    else:
        print("    not run yet — python3 sophos.py")

    # the cross-company board (discrimination lives here)
    board = _load(P["board"])
    print("\n  BOARD · cross-company discrimination")
    print(f"    {len(board.get('board', {}))} models measured" if board
          else "    no board yet — fire spray_openrouter.py (needs OPENROUTER_API_KEY via keystone)")

    print("\n  The mind is only as real as its live organs. Absent layers above are the build list, "
          "not blanks to assert over.")


def export():
    """Emit mind_state.json — the ONE data structure the three views (IWM/OWM/VWM) read at different
    zoom levels. Same graph, three renders. Written to _alignment AND to the SOV Space public dir so the
    card view can fetch it. Absent organs are emitted as nulls with a reason, never invented."""
    verdicts = [v for v in (_load(p) for p in P["verdict"]) if v]
    deck = _load(P["deck"]) or {}
    spine = _load(P["spine"]) or {}
    board = _load(P["board"]) or {}
    layer0 = {}
    for v in verdicts:
        m = v.get("layer0", {}).get("model", "?")
        layer0[m] = {ax: {"acc": s.get("accuracy"), "n": s.get("usable_n"), "interval": s.get("interval")}
                     for ax, s in v.get("measured_axes", {}).items()}
    n_rows = sum(sum(1 for _ in open(f, errors="ignore")) for f in P["signal"]) if P["signal"] else 0
    # GSPC discrimination compass — per axis, does the board actually separate models? Computed live
    # from the board so the HUD shows measured state (discriminates / marginal / dead / unmeasured),
    # never a decorative dial. Mirrors honey_barrier's rule: spread >= 0.15 and not near-ceiling.
    gspc = {}
    axis_vals = {}
    for _m, _axes in board.get("board", {}).items():
        for _ax, _s in _axes.items():
            if _s.get("accuracy") is not None:
                axis_vals.setdefault(_ax, []).append(_s["accuracy"])
    for _ax, _v in axis_vals.items():
        spread = round(max(_v) - min(_v), 4)
        ceil = sum(1 for x in _v if x >= 0.999)
        dead = spread < 0.15 or ceil >= max(2, len(_v) - 1)
        gspc[_ax] = {"spread": spread, "models": len(_v), "at_ceiling": ceil,
                     "min": round(min(_v), 4), "max": round(max(_v), 4),
                     "verdict": "dead" if dead else ("marginal" if spread < 0.20 else "discriminates")}
    state = {
        "mind": "sov3", "generated_by": "sov3.py --export",
        "layer0": layer0,                                  # the harness verdicts
        "iwm": {"signal_rows": n_rows,                     # inner: the signal accreting
                "cards": deck.get("cards", []), "deck_sha256": deck.get("sha256")},
        "spine": {"nodes": spine.get("nodes", []), "edges": spine.get("edges", []),
                  "gnn": "NOT_TRAINED — GPU-gated"},
        "owm": {"status": "STAGED", "note": "outer/simulation data model not built yet"},
        "vwm": {"surfaces": ["sovspace.html", "sovspace-os.html", "globe3d.html"]},
        "board": {"models": list(board.get("board", {}).keys())},
        "gspc": gspc,                                      # the compass: live discrimination per axis
        "gates": {"usable_n": 30, "intervals_below_gate": "withheld",
                  "gnn": "untrained", "owm": "staged", "dream_engine": "GPU+owner gated"},
    }
    state["sha256"] = hashlib.sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()[:16]
    outs = [f"{A}/mind_state.json",
            os.path.expanduser("~/clawd/councilof-ai/client/public/mind_state.json")]
    for o in outs:
        try:
            os.makedirs(os.path.dirname(o), exist_ok=True)
            json.dump(state, open(o, "w"), indent=2)
            print(f"  wrote {o}")
        except Exception as e:
            print(f"  (could not write {o}: {str(e)[:50]})")
    print(f"  mind_state sha256:{state['sha256']} · {len(state['iwm']['cards'])} J-cards · "
          f"{state['iwm']['signal_rows']} signal rows")


def run(cmd):
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.call(cmd)


def pipeline():
    """Local convergence chain that needs no GPU: signal → phlabet → spine → reflection.
    The measure step (Layer 0) needs an endpoint and is run separately via sovos.py."""
    if not P["signal"]:
        sys.exit("No SOV Signal yet. Measure first:  python3 sovos.py --model <m> --endpoint <pod|openrouter>")
    steps = [["python3", f"{HERE}/phlabet.py"],
             ["python3", f"{HERE}/spine.py"],
             ["python3", f"{HERE}/sophos.py"]]
    for s in steps:
        rc = run(s)
        if rc not in (0, 1):   # sophos exits 1 on ALERT by design — not a pipeline failure
            sys.exit(f"pipeline stopped: {' '.join(s)} exited {rc}")
    print("\nSOV3 pipeline complete — signal compressed, graph built, reflection signed.")


def query(q):
    rc = run(["python3", f"{HERE}/spine.py", "--query", q])
    sys.exit(rc)


def main():
    ap = argparse.ArgumentParser(description="SOV3 — the convergence mind, one entrypoint")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--pipeline", action="store_true")
    ap.add_argument("--export", action="store_true", help="write mind_state.json for the SOV Space render")
    ap.add_argument("--query")
    a = ap.parse_args()
    if a.query: query(a.query)
    elif a.pipeline: pipeline()
    elif a.export: export()
    else: status()


if __name__ == "__main__":
    main()
