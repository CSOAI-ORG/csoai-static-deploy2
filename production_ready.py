#!/usr/bin/env python3
"""production_ready.py — one gate over the whole estate. Three outcomes, never two.

Answers a single question for every shippable component: **could this go in front of a
regulator today?** Not "does it run" — `run_stack` already answers that. This asks whether the
thing is *defensible*: does it self-test, is its result reproducible from a stored artefact,
does it refuse to overclaim, and is anything it publishes still true?

    READY        self-tests pass, artefact present, claims match the artefact
    NOT_READY    a real failure — it is wrong, or it publishes something it cannot support
    UNMEASURED   cannot be determined here (missing credential, absent dependency, no data)

UNMEASURED is not a soft NOT_READY. Conflating them is how "we could not check it" becomes
"it is fine" — the defect this estate has spent its whole history removing. A component that
cannot be checked is reported as uncheckable and blocks nothing else from being honest.

    python3 production_ready.py [--json]
"""
from __future__ import annotations

import json, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"

READY, NOT_READY, UNMEASURED = "READY", "NOT_READY", "UNMEASURED"


def sh(cmd: list[str], timeout: int = 900) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return -9, "TIMEOUT"
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


def selftest(script: str, timeout: int = 900) -> tuple[str, str]:
    """A component that cannot self-test is UNMEASURED, not READY and not broken."""
    if not (HERE / script).exists():
        return UNMEASURED, f"{script} not present"
    rc, out = sh([sys.executable, script, "--selftest"], timeout)
    tail = [l for l in out.strip().splitlines() if l.strip()][-1:] or [""]
    t = tail[0].strip()[:88]
    if rc == 0 and ("✅" in out or "0 failure" in out):
        return READY, t
    if "TIMEOUT" in out:
        return UNMEASURED, "self-test timed out"
    # Distinguish "the test failed" from "the test could not run".
    if any(k in out for k in ("EnvironmentMissing", "ModuleNotFoundError", "no c2pa venv",
                              "not present", "unavailable")):
        return UNMEASURED, t or "dependency or credential absent"
    return NOT_READY, t or f"exit {rc}"


def artefact(name: str, must: list[str] | None = None) -> tuple[str, str]:
    """Is the claim recomputable from something on disk right now?"""
    p = RESULTS / name
    if not p.exists():
        return UNMEASURED, f"{name} absent — claim not recomputable"
    try:
        d = json.loads(p.read_text())
    except Exception as e:
        return NOT_READY, f"{name} unparseable: {type(e).__name__}"
    for k in (must or []):
        if k not in d:
            return NOT_READY, f"{name} missing key {k!r}"
    return READY, f"{name} · {p.stat().st_size:,}B"


def http(url: str, timeout: int = 25) -> tuple[str, str]:
    # A real UA: a health check once reported two LIVE services down for months because
    # Cloudflare blocked Python-urllib. That was a verdict about the service when the fact
    # was about the request.
    rc, out = sh(["curl", "-sL", "-o", "/dev/null", "--max-time", str(timeout),
                  "-A", "Mozilla/5.0", "-w", "%{http_code}", url], timeout + 15)
    code = out.strip()[-3:]
    if code == "200":
        return READY, "HTTP 200"
    if not code.isdigit():
        return UNMEASURED, f"no response ({out.strip()[:40]})"
    return NOT_READY, f"HTTP {code}"


CHECKS: list[tuple[str, str, callable]] = [
    # ── the four lenses ────────────────────────────────────────────────────────
    ("LENS", "GovBench — analysis", lambda: selftest("system_analysis.py")),
    ("LENS", "GovBench — layer attribution", lambda: selftest("layer_attribution.py")),
    ("LENS", "DefBench", lambda: selftest("defbench.py")),
    ("LENS", "ProvBench", lambda: selftest("provbench.py")),
    ("LENS", "PQCBench", lambda: selftest("pqcbench.py")),
    ("LENS", "OSSBench (public releases)", lambda: selftest("ossbench.py")),
    ("LENS", "the instrument (4 lenses, 1 engine)", lambda: selftest("sov_instrument.py")),

    # ── evidence: is every published claim recomputable? ──────────────────────
    ("EVIDENCE", "governance claim", lambda: artefact("system_analysis.json", ["clustering", "verdict"])),
    ("EVIDENCE", "governance per-item rows", lambda: artefact("system_bench.json", ["items"])),
    ("EVIDENCE", "layer partition", lambda: artefact("layer_attribution.json", ["partitions"])),
    ("EVIDENCE", "defence claim", lambda: artefact("defbench.json", ["entrants", "tied_sets"])),
    ("EVIDENCE", "provenance claim", lambda: artefact("provbench.json")),
    ("EVIDENCE", "continuity claim", lambda: artefact("pqcbench.json", ["per_criterion"])),
    ("EVIDENCE", "coverage crosswalk", lambda: artefact("coverage_crosswalk.json", ["survey_status"])),

    # ── integrity gates ───────────────────────────────────────────────────────
    ("GATE", "withdrawn-model audit", lambda: (READY, "no withdrawn model routed")
        if sh([sys.executable, "withdrawn.py", "--audit"])[0] == 0 else (NOT_READY, "a withdrawn model is reachable")),
    ("GATE", "ingestion licence audit", lambda: (READY, "0 sources ingestible without a verified licence")
        if sh([sys.executable, "coverage_crosswalk.py", "--audit"])[0] == 0 else (NOT_READY, "ingestible source lacks a verified licence")),
    ("GATE", "Article 50 signer", lambda: selftest("c2pa_manifest.py")),
    ("GATE", "board preflight", lambda: selftest("board_preflight.py")),
    ("GATE", "corpus anchor", lambda: selftest("corpus_anchor.py")),
    ("GATE", "anchored-at-write-time", lambda: selftest("anchored_write.py")),
    ("EVIDENCE", "no artefact written unanchored", lambda:
        (READY, "every result artefact carries its anchor")
        if sh([sys.executable, "anchored_write.py"], 300)[0] == 0
        else (NOT_READY, "an artefact was written without a corpus anchor")),
    ("GATE", "positioning guard (selftest)", lambda: selftest("positioning_guard.py")),
    ("CLAIM", "no claim to authority we lack", lambda: _positioning()),
    ("CLAIM", "pages agree with their artefacts", lambda: _evidence_synced()),
    ("EVIDENCE", "scores are anchored to statute", lambda: _anchored()),
    ("GATE", "no dead run scored as zero", lambda: _no_dead_runs()),

    # ── live surfaces ─────────────────────────────────────────────────────────
    ("LIVE", "HF Space (leaderboard)", lambda: http("https://nicholastempleman-sov33-benchmark.static.hf.space/")),
    ("LIVE", "csoai on Cloudflare", lambda: http("https://csoai-org.nicholastempleman.workers.dev/")),
    ("LIVE", "MCP (OAuth-gated)", lambda: http("https://sovereign.templeman-opticians.com/health")),
    ("LIVE", "SOV3 local", lambda: http("http://localhost:3101/health")),
]


def claim_consistency() -> list[tuple[str, str, str]]:
    """Do the numbers we publish still match the artefacts they came from?

    This is the check that would have caught +34.84 sitting on two live surfaces for a day
    after the run that produced it stopped existing.
    """
    out = []
    try:
        sa = json.loads((RESULTS / "system_analysis.json").read_text())
        la = json.loads((RESULTS / "layer_attribution.json").read_text())
    except Exception as e:
        return [("CLAIM", "governance figures", f"{UNMEASURED}|artefacts unreadable: {type(e).__name__}")]

    # The headline must carry a clustered interval, not a naive one.
    cl = sa.get("clustering")
    out.append(("CLAIM", "headline is cluster-robust",
                f"{READY}|deff {cl['design_effect']}, effective n {cl['n_effective']}"
                if isinstance(cl, dict) else f"{NOT_READY}|clustering {cl!r}"))

    # Layer rows must PARTITION their own run. The published table summed to 186 under a
    # 195-item headline — layers from one run, total from another.
    out.append(("CLAIM", "layer rows partition the run",
                f"{READY}|{la.get('n')} rows accounted for" if la.get("partitions")
                else f"{NOT_READY}|subgroups do not partition — double-counted or missing"))

    # Verdict must not say CLAIMABLE without evidence behind it.
    v = sa.get("verdict", "")
    out.append(("CLAIM", "verdict earned, not asserted",
                f"{READY}|{v}" if ("CLAIMABLE" in v and isinstance(cl, dict))
                else f"{NOT_READY}|{v}" if "CLAIMABLE" in v else f"{UNMEASURED}|{v}"))

    # A retracted number must not still be sitting in a shipped surface as live.
    site = Path("/Users/nicholas/clawd/csoai-dashboard-master/client/src/pages")
    stale = []
    for f in ("GovBench.tsx", "Benchmarks.tsx"):
        p = site / f
        if not p.exists():
            continue
        t = p.read_text()
        # WHAT THIS CHECKS, AND WHY IT IS NARROW.
    # Three versions of this were wrong before this one, and the wrongness is instructive:
    #   1. whole-file `"etract" not in t` — case-sensitive, missed `RETRACTED`, failed a
    #      correct file;
    #   2. whole-file presence — one retraction paragraph would excuse a live figure anywhere;
    #   3. per-occurrence proximity — still flagged `[+1.05, +12.21]` (the LIVE interval's
    #      upper bound) and a docstring warning *about* the retraction.
    # The lesson: the same digits legitimately appear as an interval bound, as cautionary
    # prose, and in a `was:` field. Prose cannot be adjudicated by substring search, and
    # tuning the regex until it goes green would be fitting the check to the answer.
    # So this checks the ONE thing that is mechanically decidable: the DATA STRUCTURE that
    # renders the table. A number a reader sees in a table comes from `LAYERS`; prose is prose.
    lay = site / "GovBench.tsx"
    if lay.exists():
        t = lay.read_text()
        i = t.find("const LAYERS")
        block = t[i: t.find("];", i)] if i != -1 else ""
        if not block:
            stale.append("GovBench.tsx: LAYERS table not found — cannot verify rendered figures")
        else:
            if "34.84" in block:
                stale.append("GovBench.tsx: LAYERS renders the retracted +34.84")
            if "Deterministic gate" in block and "−20.00" not in block and "-20.00" not in block:
                stale.append("GovBench.tsx: gate row does not carry the corrected value")
    out.append(("CLAIM", "no retracted figure shipped as live",
                f"{READY}|site surfaces clean" if not stale else f"{NOT_READY}|{'; '.join(stale)}"))
    return out



def _no_dead_runs() -> tuple[str, str]:
    """A truncated or unanswered run must never carry a numeric score into a board.

    This is the gate that would have stopped `0.0%` from an endpoint that returned 57 empty
    responses at 107 ms from anchoring the bottom of a public leaderboard.
    """
    p = RESULTS / "board_preflight.json"
    if not p.exists():
        return UNMEASURED, "board_preflight.json absent — run board_preflight.py"
    d = json.loads(p.read_text())
    bad = [e for e in d.get("entries", [])
           if e.get("status") == "UNMEASURED" and isinstance(e.get("pct"), (int, float))]
    if bad:
        return NOT_READY, f"{len(bad)} unmeasured entr(ies) still carry a score"
    n_un = sum(1 for e in d.get("entries", []) if e.get("status") == "UNMEASURED")
    n_ok = sum(1 for e in d.get("entries", []) if e.get("status") == "MEASURED")
    return READY, f"{n_ok} measurable, {n_un} correctly UNMEASURED, 0 scored while dead"



def _anchored() -> tuple[str, str]:
    """Every published claim must name the corpus it was measured against.

    Without this, no evidence can ever be shown to have EXPIRED — which is the entire drift
    product. The spec listed this as already existing; measured 2026-07-29, zero artefacts
    carried it.
    """
    need = ["system_analysis.json", "defbench.json", "provbench.json", "pqcbench.json"]
    missing = [n for n in need
               if not (RESULTS / n).exists()
               or "corpus_anchor" not in json.loads((RESULTS / n).read_text())]
    if missing:
        return NOT_READY, f"unanchored: {', '.join(missing)}"
    root = json.loads((RESULTS / "system_analysis.json").read_text())["corpus_anchor"]["corpus_root"]
    return READY, f"4 lens claims anchored to corpus {root[:16]}…"



def _positioning() -> tuple[str, str]:
    """Claims to conferred authority are a harder failure than a wrong number.

    A wrong number gets retracted. A claim to enforcement power is legally void AND kills the
    independence that is the entire moat — a body that measures and a body that punishes cannot
    credibly be the same operation.
    """
    rc, out = sh([sys.executable, "positioning_guard.py"], 300)
    line = next((l for l in out.splitlines() if "prohibited claim" in l or "no claim to" in l), "")
    return (READY, line.strip()[:70]) if rc == 0 else (NOT_READY, line.strip()[:70])



def _evidence_synced() -> tuple[str, str]:
    """The front end must not state a number its artefact does not contain.

    Every figure on the site was a hand-typed string literal with no source to go stale
    against — which is exactly how a retracted +34.84 survived on two live surfaces. This
    reconciles the rendered figures against the JSON that produced them.
    """
    rc, out = sh([sys.executable, "sync_evidence.py", "--check"], 300)
    line = next((l for l in out.splitlines() if "agree ·" in l), "").strip()
    return (READY, line[:70]) if rc == 0 else (NOT_READY, line[:70] or "reconciliation failed")


def main() -> int:
    t0 = time.time()
    rows: list[tuple[str, str, str, str]] = []
    for group, name, fn in CHECKS:
        try:
            st, detail = fn()
        except Exception as e:
            st, detail = UNMEASURED, f"check raised {type(e).__name__}"
        rows.append((group, name, st, detail))
    for group, name, packed in claim_consistency():
        st, _, detail = packed.partition("|")
        rows.append((group, name, st, detail))

    icon = {READY: "✅", NOT_READY: "❌", UNMEASURED: "⚠️ "}
    cur = None
    print(f"  PRODUCTION READINESS — {len(rows)} checks\n")
    for group, name, st, detail in rows:
        if group != cur:
            print(f"  {group}"); cur = group
        print(f"    {icon[st]} {name:36s} {detail[:74]}")

    n = {k: sum(1 for r in rows if r[2] == k) for k in (READY, NOT_READY, UNMEASURED)}
    print(f"\n  {n[READY]} READY · {n[NOT_READY]} NOT READY · {n[UNMEASURED]} UNMEASURED"
          f"  ({time.time()-t0:.0f}s)")
    if n[NOT_READY]:
        print("\n  ❌ NOT production ready — the failures above are real, not missing checks.")
    elif n[UNMEASURED]:
        print(f"\n  ⚠️  No failures, but {n[UNMEASURED]} component(s) COULD NOT BE CHECKED here.")
        print("     That is not a pass. Anything shipped on their behalf is unevidenced.")
    else:
        print("\n  ✅ Every check ran and every check passed.")

    out = {"checks": [{"group": g, "name": nm, "status": s, "detail": d} for g, nm, s, d in rows],
           "ready": n[READY], "not_ready": n[NOT_READY], "unmeasured": n[UNMEASURED]}
    (RESULTS / "production_ready.json").write_text(json.dumps(out, indent=2))
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
    return 1 if n[NOT_READY] else 0


if __name__ == "__main__":
    raise SystemExit(main())
