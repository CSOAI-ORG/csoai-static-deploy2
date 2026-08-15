#!/usr/bin/env python3
"""phlabet.py — the PHLABET: symbolic compression of SOV Signal into J-Space cards.

    python3 phlabet.py                      # compress all SOV_SIGNAL/*.jsonl into J-cards
    python3 phlabet.py --signal FILE        # one signal file
    python3 phlabet.py --show               # print the current Phlabet (the deck)

WHERE THIS SITS (from SOVOS GOAL, top→bottom)
  SOV Signal (iWM, per-item) ── phlabet.py ──▶ J-Space cards ──▶ C-space (the composed board)
The Signal is the raw inner world model, one row per measured item. The Phlabet COMPRESSES it: many
honey rows collapse to a few archetypes. Each J-Space card is one compressed archetype — a glyph, its
statutory anchor, and the reasoning it triggers ("for this pattern the answer is X; models drift to Y").
A card is a LESSON, not a copy of a row. That is why it is compression, not storage.

THE ONE RULE IT INHERITS
Honey = a row a model got WRONG against a known, anchored label — never a row from a frozen bank, and
never an UNMEASURED (unparsed) row. Cards are built only from 'wrong'. Before any card is used to TRAIN
anything, honey_barrier.assert_clear() must pass — the ruler you train on stops measuring. Compressing
the signal here does not train; it prepares. The barrier is enforced at the training edge, not here.

An empty signal is FATAL, never a silent pass: no signal → no deck → say so and exit non-zero.
"""
import argparse, glob, json, os, sys, hashlib, collections

SIG_DIR = os.path.expanduser("~/clawd/_alignment/SOV_SIGNAL")
DECK = os.path.expanduser("~/clawd/_alignment/PHLABET_DECK.json")
# A stable symbolic alphabet — the glyph is deterministic from the archetype, so the same lesson always
# draws the same card. Greek letters as a compact, order-free symbol set (the "symbolic tarot").
GLYPHS = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω"


def glyph_for(archetype):
    h = int(hashlib.sha256(archetype.encode()).hexdigest(), 16)
    return GLYPHS[h % len(GLYPHS)]


def load_signal(paths):
    rows, files = [], 0
    for p in paths:
        try:
            these = [json.loads(l) for l in open(p, errors="ignore") if l.strip()]
        except Exception:
            continue
        if these:
            rows += these; files += 1
    return rows, files


def compress(rows):
    """Many honey rows → one J-Space card per archetype. Archetype = the DIRECTIONAL ERROR CLASS
    (axis, gold → drift), not the row and not the raw anchor. This is what makes it a compression: 80
    governance misses that are all 'answer is LIMITED, model said MINIMAL' are ONE lesson, not 80. The
    anchor (which articles) is evidence carried inside the card, never the card's identity — keying on
    it (the first cut did) gives ~0% compression because each anchor is unique."""
    honey = [r for r in rows if r.get("outcome") == "wrong"]
    by = collections.defaultdict(list)
    for r in honey:
        by[(r.get("axis", "?"), r.get("gold", "?"), r.get("pred") or "UNREAD")].append(r)
    cards = []
    for (axis, gold, drift), group in sorted(by.items(), key=lambda kv: -len(kv[1])):
        models = sorted({r.get("model", "?") for r in group})
        anchors = collections.Counter(str(r.get("anchor", "?")) for r in group)
        archetype = f"{axis}:{gold}→{drift}"
        card = {
            "glyph": glyph_for(archetype),
            "axis": axis,
            "archetype": archetype,
            # the trigger is the USABLE correction: phrased at inference time, when you only see the drift
            "trigger": (f"On {axis}, this model tends to answer {drift} where the correct label is "
                        f"{gold} — when you land on {drift}, check whether it should be {gold}."),
            "correct": gold,
            "drift": drift,
            "n_honey": len(group),
            "models_that_missed": models,
            "example_anchors": [a for a, _ in anchors.most_common(5)],   # evidence, not identity
            "examples": [r["item"][:120] for r in group[:2]],
        }
        card["sha256"] = hashlib.sha256(
            json.dumps({k: card[k] for k in ("archetype", "correct", "drift", "n_honey")},
                       sort_keys=True).encode()).hexdigest()[:16]
        cards.append(card)
    return cards


def main():
    ap = argparse.ArgumentParser(description="PHLABET — compress SOV Signal into J-Space cards")
    ap.add_argument("--signal", help="a single signal jsonl (default: all of SOV_SIGNAL/*.jsonl)")
    ap.add_argument("--show", action="store_true", help="print the current deck and exit")
    a = ap.parse_args()

    if a.show:
        if not os.path.exists(DECK):
            sys.exit("No deck yet — run phlabet.py after a measured run.")
        deck = json.load(open(DECK))
        print(f"PHLABET — {len(deck['cards'])} J-Space cards · deck sha256:{deck['sha256']}\n")
        for c in deck["cards"]:
            print(f"  {c['glyph']}  {c['archetype']:<28} → {c['correct']:<16} "
                  f"drift={c['drift']} n={c['n_honey']}")
        return

    paths = [os.path.expanduser(a.signal)] if a.signal else sorted(glob.glob(f"{SIG_DIR}/*.jsonl"))
    rows, files = load_signal(paths)
    if not rows:
        sys.exit(f"NO SIGNAL: 0 rows across {len(paths)} file(s) in {SIG_DIR}. "
                 "Run sovos.py first — a Phlabet built from nothing is a false deck.")
    cards = compress(rows)
    n_wrong = sum(1 for r in rows if r.get("outcome") == "wrong")
    print(f"PHLABET · {len(rows)} signal rows from {files} file(s) · {n_wrong} honey "
          f"→ compressed to {len(cards)} J-Space cards "
          f"({(1 - len(cards)/max(n_wrong,1))*100:.0f}% compression)\n")
    for c in cards:
        print(f"  {c['glyph']}  {c['archetype']:<28} → {c['correct']:<16} drift={c['drift']} n={c['n_honey']}")
    deck = {"phlabet": "J-Space", "n_cards": len(cards), "built_from": paths, "cards": cards}
    deck["sha256"] = hashlib.sha256(json.dumps(deck["cards"], sort_keys=True).encode()).hexdigest()[:16]
    json.dump(deck, open(DECK, "w"), indent=2)
    print(f"\n  deck signed sha256:{deck['sha256']} → {DECK}")
    if not cards:
        print("  (no honey yet — the measured model got nothing wrong on the run's axes, or the run "
              "is incomplete. That is a real, honest empty deck, not a failure.)")


if __name__ == "__main__":
    main()
