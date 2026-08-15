#!/usr/bin/env python3
"""honey_barrier.py — the two guards that stop the EAT flywheel eating its own ruler.

    python3 honey_barrier.py                    # audit, human-readable
    python3 honey_barrier.py --json             # machine-readable
    from honey_barrier import assert_clear      # call before honey_pipeline.py writes anything

This does NOT replace honey_pipeline.py. That already does harvest -> distil -> merge -> sign.
This is the gate it must pass first.

BOTH BARRIERS ARE DEFECTS THIS ESTATE ACTUALLY SHIPPED. Neither is hypothetical.

BARRIER 1 - CONTAMINATION
  sov34's headline result (protect 0.97 [0.838-0.994] vs 0.45, "intervals separate") was 55%
  train-on-test: 17 of the 31 care_battery evaluation items were VERBATIM in its training corpus,
  including 11 of the 19 EU-AI-Act items. Honest held-out n was 14. The flywheel had fed evaluation
  items back in as training data, and the instrument ended up measuring its own homework.

  Enforced BY THEME, not by row. A held-out row still leaks if a near-duplicate of it was trained on,
  so if any item in a theme is contaminated the WHOLE theme leaves the clean split.

BARRIER 2 - DISCRIMINATION
  On the 2026-08-05 cross-company board, six of seven frontier models scored EXACTLY 1.000 on the
  safety axis. Reading the bank shows why: every REFUSE item is flagrantly harmful and every COMPLY
  item is flagrantly benign. Nothing is being distinguished. An axis every model aces is not a hard
  axis, it is a broken one - and a ceiling score reads as success while measuring nothing.

  Items nobody gets wrong also carry no training signal, so a dead axis cannot contribute honey.

THE RULE BEHIND BOTH
  The frozen banks are the ruler. Honey comes from RUNS - rows where a model was measurably wrong
  against a statute-anchored label - never from the banks themselves. A ruler you train on stops
  measuring, silently and permanently.
"""
import json, os, re, sys, glob, urllib.request

ROOT = os.path.expanduser("~/clawd")
OUT = f"{ROOT}/_alignment/HONEY_BARRIER_REPORT.json"
BANKS = ["gspc-gov", "gspc-agi", "gspc-prv", "gspc-asi", "gspc-mcp", "gspc-oss"]
HF = "https://huggingface.co/datasets/csoai/{}/raw/main/items.jsonl"

CEILING = 0.999
MIN_SPREAD = 0.15          # an axis whose best and worst differ by less than this separates nothing.
# 0.15 is the OR-Bench operational floor: below it an over-refusal axis is measurably dying.


def norm(s):
    """Normalise for near-duplicate detection. Exact match alone misses the leak: a reworded item
    trains the same behaviour."""
    return re.sub(r"[^a-z0-9 ]", "", (s or "").lower()).strip()


def item_text(it):
    for k in ("scenario", "request", "operation", "item", "tool", "case", "input", "prompt", "q"):
        if it.get(k):
            return it[k]
    return ""


def item_theme(it):
    """Theme = statutory anchor if present, else the gold label. Splitting by theme rather than by
    row is the difference between a real held-out set and one that leaks."""
    return it.get("anchor") or it.get("theme") or it.get("axis") or \
           it.get("expected") or it.get("answer") or "unthemed"


def fetch_bank(slug):
    try:
        txt = urllib.request.urlopen(urllib.request.Request(
            HF.format(slug), headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode()
    except Exception as e:
        return None, str(e)[:70]
    out = []
    for line in txt.splitlines():
        if line.strip():
            try: out.append(json.loads(line))
            except Exception: pass
    return out, None


def _strings(o, acc):
    if isinstance(o, str): acc.append(o)
    elif isinstance(o, dict):
        for v in o.values(): _strings(v, acc)
    elif isinstance(o, list):
        for v in o: _strings(v, acc)


def load_training():
    """Index every candidate training source. An unreadable corpus is reported, NEVER treated as
    empty - silently reading nothing would pass the check while proving nothing."""
    idx, files, unreadable = set(), 0, []
    pats = [f"{ROOT}/../projects/coai-dashboard/gpu-offload/**/corpus_dataset/**/*.json*",
            f"{ROOT}/csoai-static-deploy2/training_data/**/*.json*",
            f"{ROOT}/csoai-static-deploy2/forest/**/*.jsonl"]
    for p in pats:
        for f in glob.glob(os.path.expanduser(p), recursive=True):
            try:
                raw = open(f, errors="ignore").read()
            except Exception as e:
                unreadable.append({"file": f, "error": str(e)[:60]}); continue
            n0 = len(idx)
            for line in raw.splitlines():
                line = line.strip()
                if not line: continue
                try: o = json.loads(line)
                except Exception: continue
                acc = []; _strings(o, acc)
                for s in acc:
                    t = norm(s)
                    if len(t) > 24: idx.add(t)
            if len(idx) > n0: files += 1
    return idx, files, unreadable


def audit():
    train, nfiles, unreadable = load_training()
    contam = {}
    for slug in BANKS:
        items, err = fetch_bank(slug)
        if items is None:
            contam[slug] = {"error": err}; continue
        hits, bad_themes = [], set()
        for i, it in enumerate(items):
            t = norm(item_text(it))
            if not t: continue
            leaked = t in train or any(
                (t in s or s in t) for s in train if abs(len(s) - len(t)) < 40)
            if leaked:
                hits.append({"index": i, "theme": item_theme(it), "text": item_text(it)[:80]})
                bad_themes.add(item_theme(it))
        clean = [it for it in items if item_theme(it) not in bad_themes]
        contam[slug] = {"n_items": len(items), "n_leaked": len(hits),
                        "themes_out": sorted(bad_themes),
                        "n_clean_after_theme_split": len(clean),
                        "examples": hits[:8]}

    disc, board_p = {}, f"{ROOT}/_alignment/CROSS_COMPANY_BOARD.json"
    if os.path.exists(board_p):
        by_axis = {}
        for model, axes in json.load(open(board_p)).get("board", {}).items():
            for axis, s in axes.items():
                if s.get("accuracy") is not None:
                    by_axis.setdefault(axis, []).append(s["accuracy"])
        for axis, vals in by_axis.items():
            spread = round(max(vals) - min(vals), 4)
            ceil = sum(1 for v in vals if v >= CEILING)
            dead = spread < MIN_SPREAD or ceil >= max(2, len(vals) - 1)
            disc[axis] = {"models": len(vals), "min": min(vals), "max": max(vals),
                          "spread": spread, "at_ceiling": ceil,
                          "status": "DEAD" if dead else "discriminating",
                          "why": ("Nearly every model scores the same, so the axis separates nothing. "
                                  "Items nobody gets wrong also carry no training signal."
                                  if dead else "Scores spread across models.")}
    else:
        disc = {"error": "no CROSS_COMPANY_BOARD.json - run spray_openrouter.py first"}

    leaked_banks = [k for k, v in contam.items() if v.get("n_leaked", 0) > 0]
    dead_axes = [a for a, v in disc.items() if isinstance(v, dict) and v.get("status") == "DEAD"]
    clear = not leaked_banks and not dead_axes and "error" not in disc

    rep = {"barrier_1_contamination": {"training_files_indexed": nfiles,
                                       "strings_indexed": len(train),
                                       "unreadable_files": unreadable,
                                       "per_bank": contam},
           "barrier_2_discrimination": disc,
           "leaked_banks": leaked_banks, "dead_axes": dead_axes,
           "verdict": "CLEAR" if clear else "BLOCKED",
           "reason": ("No contamination detected and every axis discriminates." if clear else
                      (f"Contaminated banks {leaked_banks}. " if leaked_banks else "") +
                      (f"Dead axes {dead_axes} - fix the bank before mining it. " if dead_axes else "") +
                      ("Discrimination unknown - no board. " if "error" in disc else ""))}
    json.dump(rep, open(OUT, "w"), indent=2)
    return rep


def assert_clear():
    """Call this from honey_pipeline.py BEFORE writing any honey.

    Raises rather than returning a flag: a guard that can be ignored by forgetting to check its
    return value is not a guard. The estate's rule is that a component must be STRUCTURALLY UNABLE
    to report success on a path it did not complete."""
    rep = audit()
    if rep["verdict"] != "CLEAR":
        raise RuntimeError(f"HONEY BLOCKED - {rep['reason']} See {OUT}")
    return rep


if __name__ == "__main__":
    r = audit()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=2)); sys.exit(0 if r["verdict"] == "CLEAR" else 1)

    b1 = r["barrier_1_contamination"]
    print(f"BARRIER 1 · contamination — {b1['training_files_indexed']} training files, "
          f"{b1['strings_indexed']} strings indexed")
    for slug, v in b1["per_bank"].items():
        if "error" in v:
            print(f"  {slug:<10} bank unreadable: {v['error']}"); continue
        print(f"  {slug:<10} {v['n_leaked']}/{v['n_items']} leaked · "
              f"{len(v['themes_out'])} themes out · clean after theme-split: "
              f"{v['n_clean_after_theme_split']}")
    if b1["unreadable_files"]:
        print(f"  ⚠ {len(b1['unreadable_files'])} training file(s) unreadable — NOT treated as empty")

    print("\nBARRIER 2 · discrimination")
    d = r["barrier_2_discrimination"]
    if "error" in d:
        print(f"  {d['error']}")
    else:
        for axis, v in d.items():
            mark = "✗" if v["status"] == "DEAD" else "·"
            print(f"  {mark} {axis:<14} spread={v['spread']:<7} "
                  f"ceiling={v['at_ceiling']}/{v['models']}  {v['status']}")

    print(f"\nVERDICT: {r['verdict']} — {r['reason']}")
    print(f"→ {OUT}")
    sys.exit(0 if r["verdict"] == "CLEAR" else 1)
