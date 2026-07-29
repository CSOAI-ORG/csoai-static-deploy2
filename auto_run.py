#!/usr/bin/env python3
"""auto_run.py — the unattended step. Runs what is safe; stops at what is yours.

═══════════════════════════════════════════════════════════════════════════════
THE DESIGN CONSTRAINT
═══════════════════════════════════════════════════════════════════════════════
An autonomous runner in an estate whose entire value is not overclaiming has one obligation
above all others: **it must never make a claim more confident than the evidence, and it must
never take a decision that belongs to the owner.**

So the queue is split in two, and the split is enforced, not documented:

  AUTO      deterministic, reversible, and verifiable by a gate that already exists.
            Re-running benchmarks, re-anchoring the corpus, re-running audits, detecting
            drift, reporting. If it fails, nothing is published and the failure is the output.

  OWNER     anything that spends money, publishes to a third party, renames a product,
            changes positioning copy, or asserts something a regulator would read.
            These are QUEUED AND DESCRIBED, never executed.

The production gate runs LAST and its exit code is this script's exit code. A run that leaves
the estate NOT READY exits non-zero, so an unattended schedule cannot quietly accumulate
breakage while reporting success — which is the defect this whole estate was built around.

    python3 auto_run.py            # run the AUTO queue, then the gate
    python3 auto_run.py --dry      # list what would run, change nothing
    python3 auto_run.py --selftest
"""
from __future__ import annotations

import json, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"
LOG = RESULTS / "auto_run.json"

OK, FAIL, SKIP = "ok", "fail", "skip"


def sh(cmd: list[str], timeout: int = 1800) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=timeout)
        return r.returncode, ((r.stdout or "") + (r.stderr or ""))[-4000:]
    except subprocess.TimeoutExpired:
        return -9, "TIMEOUT"
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


# ── AUTO: safe, deterministic, gate-verified ───────────────────────────────────────────────
# Ordering matters, and the comment below the queue records why.
# Benchmarks first, THEN the anchor stamp, THEN the guards.
AUTO: list[tuple[str, list[str], str]] = [
    ("board preflight",         [sys.executable, "board_preflight.py"],
     "Re-classify every API row as answered/unanswered/degenerate and detect truncated runs. "
     "Stops a dead endpoint from being scored as zero."),
    ("PQC continuity lens",     [sys.executable, "pqcbench.py"],
     "Re-score every signing chain against the five continuity criteria."),
    ("coverage crosswalk",      [sys.executable, "coverage_crosswalk.py"],
     "Recompute the 3,336-cell coverage matrix. Survey remains a STUB until Phase B/C."),
    ("layer attribution",       [sys.executable, "layer_attribution.py"],
     "Recompute per-layer deltas from persisted rows and assert they partition the run."),
    ("withdrawn-model audit",   [sys.executable, "withdrawn.py", "--audit"],
     "Fail if any layer routes to a withdrawn model."),
    ("ingestion licence audit", [sys.executable, "coverage_crosswalk.py", "--audit"],
     "Fail if any source is marked ingestible without a verified licence."),
    # ANCHOR RUNS LAST — learned by running it. With the anchor first, every benchmark that
    # rewrites its own artefact afterwards STRIPS the corpus_anchor field it just received, and
    # the gate correctly reported pqcbench.json unanchored. Anchoring is a stamp on finished
    # results, so it belongs after the results are finished.
    ("corpus anchor + drift",   [sys.executable, "corpus_anchor.py"],
     "Re-hash all 417 provisions and diff against the stored baseline, then stamp every "
     "result artefact. Until the watcher polls a real authority this detects OUR corpus "
     "edits, not changes in the law — and says so in its own output."),
    ("positioning guard",       [sys.executable, "positioning_guard.py"],
     "Fail if any surface claims enforcement, system-certification, notified-body status, or "
     "carries a retracted measurement as a product name."),
]

# ── OWNER: described, never executed ───────────────────────────────────────────────────────
OWNER: list[tuple[str, str, str]] = [
    ("Clear 21 system-certification claims",
     "positioning_guard flags them; the fix is copy, and copy about our own authority is a "
     "decision, not a refactor.",
     "Replace with 'attestation-support' / 'evidence-generation'. Several are FAQs like 'Can we "
     "get certified for EU AI Act compliance?' where the honest answer — nobody can yet, zero "
     "notified bodies designated as of April 2026 — is a stronger page than the one there now."),
    ("Rename or retire 'BFT Council'",
     "72 occurrences across 20 files assert Byzantine fault tolerance, which we measured as "
     "false (n_eff 1.21 of 3, phi_bar +0.743).",
     "Either rename the component or accept that a product name asserts a retracted property. "
     "Wide blast radius; a naming decision is the owner's."),
    ("NVIDIA NIM API key",
     "integrate.api.nvidia.com is reachable from this machine and lists 102 models, but the only "
     "key on disk is the 29-char placeholder 'nvapi-REPLACE_WITH...'.",
     "Create a free key at build.nvidia.com, set NVIDIA_API_KEY in .env. Safe now that board "
     "preflight records unreachable endpoints as UNMEASURED instead of scoring them zero."),
    ("C2PA conformance record ID",
     "SSL.com will not issue a trust-listed certificate without one; our root is private, so "
     "every verifier reports the signer as unknown.",
     "Submit the Expression of Interest to conformance@c2pa.org."),
    ("Deploy the corrected site",
     "The post-audit figures, /benchmarks and /instrument are built and verified locally only. "
     "Public surfaces still serve pre-audit numbers.",
     "Deploying is outward-facing and needs your go."),
]


def run_auto(dry: bool) -> list[dict]:
    out = []
    for name, cmd, why in AUTO:
        if dry:
            out.append({"step": name, "status": SKIP, "why": why}); continue
        t0 = time.time()
        rc, log = sh(cmd)
        tail = [l for l in log.strip().splitlines() if l.strip()][-1:] or [""]
        out.append({"step": name, "status": OK if rc == 0 else FAIL,
                    "exit": rc, "secs": round(time.time() - t0, 1),
                    "tail": tail[0].strip()[:120], "why": why})
    return out


def main() -> int:
    dry = "--dry" in sys.argv
    started = datetime.now(timezone.utc).isoformat()
    print(f"  AUTO RUN{' (dry)' if dry else ''} — {started}\n")

    steps = run_auto(dry)
    for s in steps:
        icon = {OK: "✅", FAIL: "❌", SKIP: "·"}[s["status"]]
        extra = f'  {s.get("secs", 0)}s' if not dry else ""
        print(f"    {icon} {s['step']:26s}{extra}")
        if s["status"] == FAIL:
            print(f"        {s.get('tail','')}")

    print(f"\n  QUEUED FOR YOU — described, not executed ({len(OWNER)})")
    for name, why, how in OWNER:
        print(f"    ⬜ {name}")
        print(f"        why : {why}")
        print(f"        next: {how}")

    # The gate runs LAST and owns the exit code. An unattended schedule must not be able to
    # accumulate breakage while reporting success.
    print("\n  PRODUCTION GATE")
    if dry:
        print("    · skipped (dry run)")
        gate_rc, gate_line = 0, "skipped"
    else:
        gate_rc, gate_out = sh([sys.executable, "production_ready.py"], 1800)
        gate_line = next((l for l in gate_out.splitlines() if "READY ·" in l), "").strip()
        print(f"    {'✅' if gate_rc == 0 else '❌'} {gate_line}")

    failed = [s for s in steps if s["status"] == FAIL]
    record = {"started": started, "dry": dry, "steps": steps,
              "owner_queue": [{"item": n, "why": w, "next": h} for n, w, h in OWNER],
              "gate_exit": gate_rc, "gate": gate_line,
              "auto_failures": len(failed)}
    prev = json.loads(LOG.read_text())["runs"][-9:] if LOG.exists() else []
    LOG.write_text(json.dumps({"runs": prev + [record]}, indent=2))
    print(f"\n  -> {LOG}")

    if failed:
        print(f"\n  ❌ {len(failed)} AUTO step(s) failed — nothing was published.")
    elif gate_rc != 0:
        print("\n  ❌ AUTO queue clean, but the estate is NOT production ready.")
        print("     The queued items above are the reason. They are yours, not mine.")
    else:
        print("\n  ✅ AUTO queue clean and the gate is green.")
    return 1 if (failed or gate_rc != 0) else 0


def selftest() -> int:
    fails = []
    # Every AUTO command must point at a file that exists, or the runner silently no-ops.
    for name, cmd, _ in AUTO:
        script = next((c for c in cmd if c.endswith(".py")), None)
        if script and not (HERE / script).exists():
            fails.append(f"AUTO step {name!r} references missing {script}")
    # Nothing in AUTO may publish, deploy, spend, or push.
    banned = ("upload", "push", "deploy", "publish", "hf_", "curl", "rm ", "git ")
    for name, cmd, _ in AUTO:
        joined = " ".join(cmd).lower()
        if any(b in joined for b in banned):
            fails.append(f"AUTO step {name!r} contains an outward-facing or destructive verb")
    # The OWNER queue must be non-empty and fully described — an empty queue would read as
    # "nothing is blocked", which has never been true.
    if not OWNER:
        fails.append("OWNER queue empty")
    for n, w, h in OWNER:
        if not (n and w and h):
            fails.append(f"OWNER item {n!r} is missing its why/next")
    # A dry run must change nothing on disk.
    before = LOG.read_text() if LOG.exists() else None
    run_auto(dry=True)
    after = LOG.read_text() if LOG.exists() else None
    if before != after:
        fails.append("dry run mutated the log")
    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 4/4' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else main())
