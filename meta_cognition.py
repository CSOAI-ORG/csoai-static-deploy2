#!/usr/bin/env python3
"""meta_cognition.py — "which AI family for what?", answered from the board, never guessed.

    python3 meta_cognition.py            # per-axis: the measured pick, or an honest decline
    python3 meta_cognition.py --json

WHY THIS IS DIFFERENT FROM THE ROUTER THAT FAILED
The estate already built a per-dimension router and MEASURED it near-zero (+0.90, CI [-1.99, +3.79])
because it routed on a GUESS. This does the opposite: it routes only where the cross-company board
RESOLVES a winner at usable_n >= 30, and where two models' intervals overlap it calls a TIED SET, not
a winner. Where no model clears n >= 30, or the field is tied, it DECLINES — "no measured winner" is a
valid, honest answer and the only safe one. A meta-cognition layer that always returns a pick is the
router that failed; one that can say "I cannot tell yet" is the one that measured positive discipline.

Reads CROSS_COMPANY_BOARD.json (spray_openrouter.py output). With today's small-n board, every axis
declines — correctly. The moment the board runs on gspc-gov (n=237), governance resolves and routing
there becomes real. That transition is the whole point: capability earned by n, not asserted.
"""
import argparse, json, math, os, sys

BOARD = os.path.expanduser("~/clawd/_alignment/CROSS_COMPANY_BOARD.json")
USABLE_N = 30


def wilson(c, n):
    if not n: return None
    z = 1.959963985; p = c / n; d = 1 + z * z / n
    m = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0., m - h), 4), round(min(1., m + h), 4)]


def overlap(a, b):
    return a[0] <= b[1] and b[0] <= a[1]


def decide(board):
    by_axis = {}
    for model, axes in board.items():
        for axis, s in axes.items():
            n = s.get("usable_n", 0)
            c = s.get("correct")
            iv = s.get("interval") or (wilson(c, n) if (c is not None and n >= USABLE_N) else None)
            by_axis.setdefault(axis, []).append(
                {"model": model, "acc": s.get("accuracy"), "n": n, "interval": iv})

    out = {}
    for axis, rows in by_axis.items():
        resolved = [r for r in rows if r["n"] >= USABLE_N and r["interval"]]
        if len(resolved) < 2:
            out[axis] = {"decision": "DECLINE",
                         "why": f"only {len(resolved)} model(s) at usable_n>={USABLE_N} — cannot compare; "
                                "no measured winner. Route a default; do not claim a best here.",
                         "candidates_below_gate": sorted(
                             [f"{r['model']}={r['acc']}(n={r['n']})" for r in rows])}
            continue
        resolved.sort(key=lambda r: -r["acc"])
        top = resolved[0]
        tied = [r for r in resolved if overlap(r["interval"], top["interval"])]
        if len(tied) > 1:
            out[axis] = {"decision": "TIED",
                         "why": "top intervals overlap — the board cannot separate them; pick on cost/latency, not accuracy.",
                         "tied_set": [f"{r['model']} {r['interval']}" for r in tied]}
        else:
            out[axis] = {"decision": "ROUTE", "to": top["model"],
                         "interval": top["interval"], "acc": top["acc"], "n": top["n"],
                         "why": f"clears usable_n>={USABLE_N} and its interval is above the next model's."}
    return out


def main():
    ap = argparse.ArgumentParser(description="Meta-cognition: route by the measured board, or decline")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.exists(BOARD):
        sys.exit("No board yet — fire spray_openrouter.py (keystone OPENROUTER_API_KEY). "
                 "Routing with no board would be exactly the guess that measured near-zero.")
    d = json.load(open(BOARD))
    dec = decide(d.get("board", {}))
    if a.json:
        print(json.dumps(dec, indent=2)); return
    print(f"META-COGNITION · from board run {d.get('run','?')} · {len(d.get('board',{}))} models\n")
    for axis, v in dec.items():
        if v["decision"] == "ROUTE":
            print(f"  {axis:<12} → ROUTE to {v['to']}  acc={v['acc']} n={v['n']} {v['interval']}")
        elif v["decision"] == "TIED":
            print(f"  {axis:<12} → TIED: {', '.join(v['tied_set'])}")
        else:
            print(f"  {axis:<12} → DECLINE ({v['why'].split('—')[0].strip()})")
    n_route = sum(1 for v in dec.values() if v["decision"] == "ROUTE")
    print(f"\n  {n_route}/{len(dec)} axes route on measured evidence. "
          "The rest decline — that is the discipline, not a gap to paper over.")


if __name__ == "__main__":
    main()
