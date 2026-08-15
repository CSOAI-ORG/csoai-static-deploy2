#!/usr/bin/env python3
"""corpus_anchor.py — the keystone the drift product hangs on, and it did not exist.

═══════════════════════════════════════════════════════════════════════════════
THE CORRECTION THIS FILE EXISTS FOR
═══════════════════════════════════════════════════════════════════════════════
The drift spec lists `corpus_hash on every score` as **✅ exists** and concludes the product is
*"already 90% built — only the registry is missing."*

Measured 2026-07-29: **zero result artefacts carry a corpus_hash.** Not system_bench,
system_analysis, defbench, provbench, pqcbench, layer_attribution or coverage_crosswalk. The
`item_fingerprints.json` the dataset card advertises is also absent from disk.

That inverts the build order. The expiry rule is *"a pack is STALE when any corpus_hash it is
anchored to no longer matches the current text of that provision"* — so with no anchors,
**nothing can ever go stale** and the drift feed can compute precisely nothing. The registry is
not the missing piece; the anchor is, and the registry is downstream of it.

═══════════════════════════════════════════════════════════════════════════════
NORMALISATION IS THE WHOLE GAME
═══════════════════════════════════════════════════════════════════════════════
The spec says so and it is right. If whitespace or consolidation boilerplate is not stripped
identically every time, every poll reports false drift and the product cries wolf until nobody
reads it.

So the normaliser is **frozen, versioned, and hashed into every record**. A normaliser change
is itself a drift event and must be visible as one — otherwise changing how we read the law
would silently expire everybody's evidence and look like the law had changed.

═══════════════════════════════════════════════════════════════════════════════
FAIL CLOSED
═══════════════════════════════════════════════════════════════════════════════
A provision that cannot be read is `UNKNOWN`, never `unchanged`. A watcher reporting "no drift"
when it could not fetch is the health-check bug again — a verdict about the law when the fact
was about the request.

    python3 corpus_anchor.py               # anchor every result artefact, report drift
    python3 corpus_anchor.py --selftest
"""
from __future__ import annotations

import hashlib, json, re, sqlite3, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"
from statute_retrieval import DB  # noqa: E402

# ── The frozen normaliser ──────────────────────────────────────────────────────────────────
# Bump this ONLY with a recorded reason. Every anchor carries it, so a bump is detectable as a
# normaliser drift event rather than masquerading as a change in the law.
NORMALISER_VERSION = "1.0.0"

_WS = re.compile(r"\s+")
_SOFT_HYPHEN = re.compile(r"[­​‌‍﻿]")
# Consolidated EUR-Lex text carries editorial markers that change without the law changing.
_EDITORIAL = re.compile(
    r"►?[MC]\d+\s*|\(\s*OJ\s+L[^)]*\)|\[?consolidated text\]?|▼[A-Z]\d*", re.I)


def normalise(text: str) -> str:
    """Frozen. Identical input → identical output, forever, or the product cries wolf."""
    if text is None:
        raise ValueError("cannot normalise None — a missing provision is UNKNOWN, not empty")
    t = _SOFT_HYPHEN.sub("", text)
    t = _EDITORIAL.sub(" ", t)
    t = t.replace("’", "'").replace("‘", "'")
    t = t.replace("“", '"').replace("”", '"')
    t = t.replace("–", "-").replace("—", "-").replace(" ", " ")
    t = _WS.sub(" ", t).strip()
    return t.casefold()


def provision_hash(text: str) -> str:
    """Hash of the NORMALISED text, salted with the normaliser version.

    Salting matters: it makes a normaliser bump change every hash, which is correct — the
    anchors genuinely are no longer comparable — and it makes that fact visible instead of
    silent.
    """
    return hashlib.sha256(
        f"{NORMALISER_VERSION}\x00{normalise(text)}".encode()).hexdigest()


def load_corpus() -> dict[str, str]:
    """{'32024R1689:50': sha256} for all 417 provisions. Raises if the corpus is unreadable —
    an empty corpus must never be mistaken for 'nothing changed'."""
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        rows = con.execute("SELECT celex, article_number, content FROM articles").fetchall()
    finally:
        con.close()
    if not rows:
        raise RuntimeError("statute corpus empty — anchors are UNMEASURABLE, not zero")
    out = {}
    for celex, num, content in rows:
        if content is None:
            continue                      # UNKNOWN, not empty — absent from the anchor set
        out[f"{celex}:{num}"] = provision_hash(content)
    return out


def corpus_root(anchors: dict[str, str]) -> str:
    """One hash over the whole anchored corpus — the cheap 'did anything at all move' check."""
    h = hashlib.sha256()
    for k in sorted(anchors):
        h.update(k.encode()); h.update(anchors[k].encode())
    return h.hexdigest()


def diff(before: dict[str, str], after: dict[str, str]) -> dict:
    """Deterministic. Four classes, and 'unknown' is not one of the three change classes."""
    b, a = set(before), set(after)
    changed = sorted(k for k in (b & a) if before[k] != after[k])
    return {"amended": changed,
            "added": sorted(a - b),
            "removed": sorted(b - a),
            "unchanged": len((b & a)) - len(changed)}


def anchor_artefacts() -> dict:
    """Stamp every result artefact with the corpus root it was measured against.

    Retro-anchoring is honest ONLY because it is labelled: these results were produced before
    anchoring existed, so their anchor records the corpus as it is NOW, and says so. It gives
    every future run a baseline; it cannot retroactively prove what the law said last week.
    """
    anchors = load_corpus()
    root = corpus_root(anchors)
    stamped, skipped = [], []
    for p in sorted(RESULTS.glob("*.json")):
        if p.name in ("corpus_anchor.json", "production_ready.json", "board_preflight.json"):
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:
            skipped.append((p.name, "unparseable")); continue
        if not isinstance(d, dict):
            skipped.append((p.name, "not an object")); continue
        if d.get("corpus_anchor", {}).get("corpus_root") == root:
            continue                                   # already current
        d["corpus_anchor"] = {
            "corpus_root": root,
            "provisions": len(anchors),
            "normaliser_version": NORMALISER_VERSION,
            "anchored_at": datetime.now(timezone.utc).isoformat(),
            "retro": True,
            "note": ("Anchored retrospectively on 2026-07-29. This records the corpus as it "
                     "stands NOW; it does not prove what the text said when the result was "
                     "produced. Runs from this point forward anchor at measurement time."),
        }
        p.write_text(json.dumps(d, indent=2))
        stamped.append(p.name)
    return {"root": root, "anchors": anchors, "stamped": stamped, "skipped": skipped}


def main() -> int:
    prev_p = RESULTS / "corpus_anchor.json"
    prev = json.loads(prev_p.read_text()) if prev_p.exists() else None

    r = anchor_artefacts()
    print("  CORPUS ANCHOR — the field the drift product needs and did not have\n")
    print(f"    provisions anchored   {len(r['anchors'])}")
    print(f"    normaliser            v{NORMALISER_VERSION} (frozen, hashed into every anchor)")
    print(f"    corpus root           {r['root'][:32]}…")
    print(f"    artefacts stamped     {len(r['stamped'])}")
    for n in r["stamped"][:8]:
        print(f"                          {n}")
    if len(r["stamped"]) > 8:
        print(f"                          … and {len(r['stamped'])-8} more")
    for n, why in r["skipped"][:4]:
        print(f"    ⚠️  skipped {n} — {why}")

    if prev:
        if prev.get("normaliser_version") != NORMALISER_VERSION:
            print(f"\n    ⚠️  NORMALISER DRIFT v{prev.get('normaliser_version')} → v{NORMALISER_VERSION}")
            print(f"        Every anchor is invalidated by this, and that is correct. It is a")
            print(f"        change in how we READ the law, not a change in the law — and it must")
            print(f"        never be reported as the latter.")
        else:
            d = diff(prev.get("anchors", {}), r["anchors"])
            moved = len(d["amended"]) + len(d["added"]) + len(d["removed"])
            print(f"\n    DRIFT SINCE LAST ANCHOR")
            print(f"      amended {len(d['amended'])} · added {len(d['added'])} · "
                  f"removed {len(d['removed'])} · unchanged {d['unchanged']}")
            for k in d["amended"][:6]:
                print(f"        ⚠️  {k} text changed — every pack anchored to it is STALE")
            if moved == 0:
                print(f"      ✅ no provision moved")
    else:
        print(f"\n    first anchor — no baseline to diff against yet. This run IS the baseline.")

    print(f"\n    ⚠️  WHAT THIS DOES NOT YET DO: nothing here fetches from EUR-Lex or")
    print(f"        legislation.gov.uk. It anchors and diffs the LOCAL corpus. Real drift")
    print(f"        detection needs the watcher polling the authority — until then this")
    print(f"        detects our own corpus edits, not changes in the law.")

    out = {"corpus_root": r["root"], "provisions": len(r["anchors"]),
           "normaliser_version": NORMALISER_VERSION,
           "anchored_at": datetime.now(timezone.utc).isoformat(),
           "artefacts_stamped": r["stamped"], "anchors": r["anchors"],
           "watcher": "NOT BUILT — local corpus only; no authority is polled"}
    prev_p.write_text(json.dumps(out, indent=2))
    print(f"\n    -> {prev_p}")
    return 0


def selftest() -> int:
    fails = []

    # Normalisation must be stable across the variations that cause false drift.
    a = "Article 50(2)   The provider shall ensure—that content is marked."
    b = "Article 50(2) The  provider shall ensure—that content is marked."
    if provision_hash(a) != provision_hash(b):
        fails.append("whitespace/dash variants produced different hashes — false drift")
    if provision_hash("▼M1 Article 5") != provision_hash("Article 5"):
        fails.append("editorial marker not stripped — consolidation would look like an amendment")
    if provision_hash("The PROVIDER shall") != provision_hash("the provider shall"):
        fails.append("case difference produced different hashes")

    # …but a REAL change must still change the hash. A normaliser that flattens everything
    # would be perfectly stable and perfectly useless.
    if provision_hash("shall ensure") == provision_hash("shall not ensure"):
        fails.append("a genuine textual change did NOT change the hash")
    if provision_hash("marked by 2 August") == provision_hash("marked by 2 December"):
        fails.append("a date change did not change the hash")

    # A missing provision is UNKNOWN, never empty-string-hashed into 'unchanged'.
    try:
        normalise(None); fails.append("None normalised instead of raising")
    except ValueError:
        pass

    # The normaliser version must be salted in, or a bump would silently keep old anchors valid.
    import corpus_anchor as ca
    keep = ca.NORMALISER_VERSION
    h1 = provision_hash("Article 5")
    ca.NORMALISER_VERSION = "9.9.9"
    h2 = ca.provision_hash("Article 5")
    ca.NORMALISER_VERSION = keep
    if h1 == h2:
        fails.append("normaliser version not salted into the hash — a bump would be invisible")

    # Diff must name every class, and must not report a change as unchanged.
    d = diff({"a": "1", "b": "2", "c": "3"}, {"a": "1", "b": "X", "d": "4"})
    if d["amended"] != ["b"]: fails.append(f"amended wrong: {d['amended']}")
    if d["added"] != ["d"]: fails.append(f"added wrong: {d['added']}")
    if d["removed"] != ["c"]: fails.append(f"removed wrong: {d['removed']}")
    if d["unchanged"] != 1: fails.append(f"unchanged wrong: {d['unchanged']}")

    # The corpus root must move when any single provision moves.
    if corpus_root({"x": "1", "y": "2"}) == corpus_root({"x": "1", "y": "3"}):
        fails.append("corpus root did not move when a provision changed")

    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 12/12' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else main())
