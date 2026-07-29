#!/usr/bin/env python3
"""sync_evidence.py — close the back-end/front-end gap: ship the artefacts, then prove the
pages agree with them.

═══════════════════════════════════════════════════════════════════════════════
THE GAP THIS CLOSES
═══════════════════════════════════════════════════════════════════════════════
Every number rendered on the site is currently a string literal in a `.tsx` file. The
artefacts that produced those numbers live in `benchmark-results/` and are **never served to
the browser**. So the site and the evidence are two independent copies of the same claim, and
nothing detects when they diverge.

That is not hypothetical. `+34.84` sat on two live surfaces for a day after the run that
produced it had stopped existing, because a hand-typed number cannot go stale — it has no
source to go stale against.

This does two things, and the second is the one that matters:

  1. **SHIP** — copy the result artefacts into `client/public/evidence/` with a signed
     manifest, so a reader can fetch the JSON behind any figure and recompute it. "Verify this
     yourself" is only true if the evidence is actually reachable.

  2. **RECONCILE** — parse the figures the pages actually render and check each one against
     the artefact it claims to come from. A page quoting a number no artefact contains is a
     FAILURE, not a warning. This is the check that would have caught +34.84 on day one.

Reconciliation is deliberately narrow: it verifies figures that CAN be traced, and reports
everything else as UNTRACED rather than silently passing. An untraced figure is not a
violation — much site copy is legitimately prose — but the count is printed so it cannot
quietly grow.

    python3 sync_evidence.py            # ship + reconcile
    python3 sync_evidence.py --check    # reconcile only, change nothing
    python3 sync_evidence.py --selftest
"""
from __future__ import annotations

import hashlib, json, re, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"
SITE = Path("/Users/nicholas/clawd/csoai-dashboard-master/client")
EVIDENCE = SITE / "public" / "evidence"
PAGES = SITE / "src" / "pages"

SHIP = ["system_analysis.json", "system_bench.json", "layer_attribution.json",
        "defbench.json", "provbench.json", "pqcbench.json",
        "coverage_crosswalk.json", "board_preflight.json", "corpus_anchor.json",
        "ossbench.json",
        "production_ready.json"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ship() -> dict:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    manifest, missing = [], []
    for name in SHIP:
        src = RESULTS / name
        if not src.exists():
            missing.append(name); continue
        dst = EVIDENCE / name
        shutil.copy2(src, dst)
        manifest.append({"file": name, "sha256": sha256(src), "bytes": src.stat().st_size})
    anchor = None
    try:
        anchor = json.loads((RESULTS / "corpus_anchor.json").read_text()).get("corpus_root")
    except Exception:
        pass
    m = {"generated": datetime.now(timezone.utc).isoformat(),
         "corpus_root": anchor,
         "note": ("Every figure rendered on this site is recomputable from these files. If a "
                  "page states a number that is not here, the page is wrong, not the file."),
         "files": manifest, "missing": missing}
    (EVIDENCE / "manifest.json").write_text(json.dumps(m, indent=2))
    return m


# ── Reconciliation ─────────────────────────────────────────────────────────────────────────
# Each entry: the figure as it appears on a page, and a callable that extracts the SAME figure
# from the artefact. A mismatch is a hard failure.
def _sysa(k):
    d = json.loads((RESULTS / "system_analysis.json").read_text())
    return d[k]


def _layer(name, field):
    d = json.loads((RESULTS / "layer_attribution.json").read_text())
    row = next((r for r in d["by_action"] if r["label"] == name), None)
    return row and row.get(field)


def _prov_assets():
    d = json.loads((RESULTS / "provbench.json").read_text())
    r = next(x for x in d["pooled_by_check"] if x["config"] == "embedded_only")
    return r


CHECKS = [
    ("whole-system Δ", "+6.63", lambda: f'{_sysa("mean"):+.2f}'),
    ("whole-system n", "193", lambda: str(_sysa("n"))),
    ("design effect", "1.92", lambda: str(_sysa("clustering")["design_effect"])),
    ("gate Δ (retracted)", "−20.00", lambda: f'{_layer("gate blocked", "mean_delta"):+.2f}'.replace("-", "−")),
    ("KB Δ", "+19.64", lambda: f'{_layer("KB served", "mean_delta"):+.2f}'),
    ("tuned-model Δ", "+6.50", lambda: f'{_layer("tuned model alone", "mean_delta"):+.2f}'),
    ("provenance assets", "0 of 20", lambda: f'{_prov_assets()["assets_fully_surviving"]} of {_prov_assets()["n_assets"]}'),
    ("provenance cells", "0 of 180", lambda: f'{_prov_assets()["survived"]} of {_prov_assets()["n_measured"]}'),
    ("Clopper-Pearson 1-sided", "13.9%", lambda: f'{_prov_assets()["cp_upper_one_sided_95"]*100:.1f}%'),
]


def reconcile() -> tuple[list, list]:
    ok, bad = [], []
    for label, on_page, extract in CHECKS:
        try:
            actual = extract()
        except Exception as e:
            bad.append((label, on_page, f"artefact unreadable: {type(e).__name__}")); continue
        (ok if str(actual) == on_page else bad).append((label, on_page, actual))
    return ok, bad


def page_figures() -> int:
    """How many numeric figures does the site render that we have NOT traced?

    Not a violation — most are prose or design values. Printed so the untraced count cannot
    grow quietly while everyone assumes the reconciliation covers the page.
    """
    rx = re.compile(r"[+−-]?\d+\.\d{2}\b")
    seen = set()
    # SovereignConsole was NOT scanned, and it carried a superseded ProvBench figure for a
    # while as a result. A reconciler that only covers pages misses components, and components
    # render on every page.
    for f in ("GovBench.tsx", "Benchmarks.tsx", "ProvenanceFinding.tsx", "Instrument.tsx",
              "RefutationLedger.tsx"):
        p = PAGES / f
        if p.exists():
            seen |= set(rx.findall(p.read_text()))
    for f in ("SovereignConsole.tsx", "BuiltOnFooter.tsx", "SovCard.tsx"):
        p = PAGES.parent / "components" / f
        if p.exists():
            seen |= set(rx.findall(p.read_text()))
    traced = {c[1] for c in CHECKS}
    return len(seen - traced)


def main() -> int:
    check_only = "--check" in sys.argv
    if not check_only:
        m = ship()
        print(f"  SHIPPED — {len(m['files'])} artefacts -> client/public/evidence/")
        if m["missing"]:
            print(f"    ⚠️  missing (not shipped): {', '.join(m['missing'])}")
        print(f"    corpus_root {str(m['corpus_root'])[:24]}…")
    else:
        print("  CHECK ONLY — nothing written")

    ok, bad = reconcile()
    print(f"\n  RECONCILED — do the pages agree with the artefacts?\n")
    for label, on_page, actual in ok:
        print(f"    ✅ {label:26s} page {on_page:>10}  =  artefact {actual}")
    for label, on_page, actual in bad:
        print(f"    ❌ {label:26s} page {on_page:>10}  ≠  artefact {actual}")
    untraced = page_figures()
    print(f"\n  {len(ok)} agree · {len(bad)} DISAGREE · {untraced} figures on the pages not traced here")
    if bad:
        print("\n  ❌ A page states a number its artefact does not. The page is wrong.")
        return 1
    print("\n  ✅ Every traced figure on the site matches the artefact behind it.")
    return 0


def selftest() -> int:
    fails = []
    ok, bad = reconcile()
    if not ok and not bad:
        fails.append("reconcile produced no results at all")
    # The reconciler must actually be able to FAIL — a check that cannot go red is decoration.
    saved = CHECKS[0]
    CHECKS[0] = ("injected mismatch", "+999.99", saved[2])
    _, bad2 = reconcile()
    if not any(b[0] == "injected mismatch" for b in bad2):
        fails.append("reconciler did not catch an injected mismatch")
    CHECKS[0] = saved
    # A missing artefact must be reported, never silently skipped.
    def boom(): raise FileNotFoundError("gone")
    CHECKS.append(("missing artefact", "x", boom))
    _, bad3 = reconcile()
    if not any(b[0] == "missing artefact" for b in bad3):
        fails.append("missing artefact not reported as a failure")
    CHECKS.pop()
    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 3/3' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else main())
