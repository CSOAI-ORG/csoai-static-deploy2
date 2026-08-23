#!/usr/bin/env python3
"""FRAMEWORKS DRUM — test suite (move 11 of NEXT_100_MOVES).

Run:  python3 tests/test_drum.py
Exit 0 = all green. Covers catalog integrity, id uniqueness, card coverage,
JSON validity, hygiene (no banned strings on public surfaces), feeds shape.
"""
import json
import os
import re
import sys

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERNAL = ["sov3", "sov33", "oowm", "sigil", "horus", "liquid-kan", "maternal", "byzantine", "bft", "ceasai"]

failures = []


def check(name, cond, detail=""):
    if cond:
        print(f"  ok  {name}")
    else:
        failures.append(name)
        print(f"FAIL {name} {detail}")


def seed_integrity():
    import sys as _s
    _s.path.insert(0, PACK)
    import build_catalog as b
    return [e for e in b.SEED if not e.get("id") or not e.get("name")]


def main():
    print("FRAMEWORKS DRUM tests")
    cat = json.load(open(os.path.join(PACK, "catalog.json")))
    items = cat["items"]

    check("catalog is list", isinstance(items, list), "items not a list")
    check("counts match items", sum(cat["counts"].values()) == len(items),
          f"{sum(cat['counts'].values())} != {len(items)}")

    ids = [i["id"] for i in items]
    check("no duplicate ids", len(ids) == len(set(ids)), f"{len(ids) - len(set(ids))} dups")
    req = ["id", "name", "kind", "status"]
    check("all items have required fields", all(all(k in i for k in req) for i in items),
          [i["id"] for i in items if not all(k in i for k in req)][:3])
    bad_seed = seed_integrity()
    check("seed entries have id+name", not bad_seed, bad_seed[:2])
    check("kinds are valid", all(i["kind"] in ("framework", "charter", "regulation", "article", "sector") for i in items))

    # card coverage: every item has a card, no stale cards
    dirs = {"framework": "frameworks", "charter": "charters", "regulation": "regulations", "article": "articles", "sector": "sectors"}
    cards = set()
    for d in dirs.values():
        dpath = os.path.join(PACK, d)
        cards |= {f"{d}/{f[:-3]}" for f in os.listdir(dpath) if f.endswith(".md")}
    expected = {f"{dirs[i['kind']]}/{i['id']}" for i in items}
    check("every item has a card", expected <= cards, f"{len(expected - cards)} missing")
    check("no stale cards", cards <= expected, f"{len(cards - expected)} stale")

    # hygiene: public surfaces carry no internal codenames (internal items may, but they are flagged)
    publics = [i for i in items if not i.get("internal")]
    def clean(name, text):
        t = (text or "").lower()
        return not any(c in t for c in INTERNAL)
    check("public items clean (names)", all(clean(i["name"], i["name"]) for i in publics),
          [i["name"] for i in publics if not clean(i["name"], i["name"])][:3])
    check("public items clean (descriptions)", all(clean(i["description"], i["description"]) for i in publics),
          [i["name"] for i in publics if not clean(i["description"], i["description"])][:3])
    for f in ("llms.txt", "README.md", "docs/WIRING.md", "mcp/manifest.json", "a2a/agent-card.json"):
        p = os.path.join(PACK, f)
        if os.path.exists(p):
            check(f"surface clean: {f}", not any(c in open(p, encoding="utf-8").read().lower() for c in INTERNAL))

    # feeds shape
    reg = json.load(open(os.path.join(PACK, "feeds", "reg_events.json")))
    check("reg_events has events", isinstance(reg.get("events"), list) and len(reg["events"]) > 0)
    check("reg_events count matches", reg["count"] == len(reg["events"]))
    eat = json.load(open(os.path.join(PACK, "feeds", "eat_7box.json")))
    check("eat_7box has 7 boxes", len(eat.get("boxes", {})) == 7)

    print()
    if failures:
        print(f"{len(failures)} FAILURES: {failures}")
        sys.exit(1)
    print("ALL GREEN")
    sys.exit(0)


if __name__ == "__main__":
    main()
