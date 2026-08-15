#!/usr/bin/env python3
"""spawn_clans.py — 12 specialist clan layers per master hive, around one top SOV.

═══════════════════════════════════════════════════════════════════════════════
THE SHAPE
═══════════════════════════════════════════════════════════════════════════════
    MASTER HIVE (CSOAI / DEFONEOS / MEOK)
      └── top SOV        the hive's current best single expert — the spine
      └── 12 CLAN LAYERS one specialist drawing per layer, aimed inside the hive's remit
            each clan = a system prompt = 16 KB
            12 clans x 3 hives = 36 clans = ~576 KB total

Why this is affordable at all: measured today, an expert costs **16 KB** because every clan is
a prompt over ONE shared 397MB blob. The blob store did not move when one was created. Spawning
a clan is authoring a Modelfile, not training a model.

Why it is SAFE: composition is **monotonic** — a clan that wins nothing is never routed and
costs only its 16 KB. Proven by subset replay; the worst model on the board still contributed
+1.67. So spawning 36 clans cannot make any hive worse. The only real cost is benchmark slots.

═══════════════════════════════════════════════════════════════════════════════
THE TWELVE LAYERS — angles, not facts
═══════════════════════════════════════════════════════════════════════════════
Every layer is a way of ANSWERING, never a claim about what is true. This is not stylistic
preference — it is the fix for a measured failure: fact-asserting personas overruled retrieved
law and produced "Article 50" for social scoring. Facts come from retrieval and the citation
registry; clans supply approach.

    python3 spawn_clans.py --hive DEFONEOS          # spawn 12 clans for one hive
    python3 spawn_clans.py --all                    # all three hives (36 clans)
    python3 spawn_clans.py --status
"""
from __future__ import annotations

import argparse, json, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
LEDGER = HERE / "benchmark-results" / "clan_ledger.json"

# 12 answering postures. Each says HOW to respond. None asserts a fact.
LAYERS = [
    ("precise",     "Answer in one or two sentences. No preamble, no restatement, no caveats "
                    "unless the caveat changes the answer."),
    ("cited",       "Name the source for every claim — article, clause, control ID. If the source "
                    "is not in front of you, say that rather than recalling one."),
    ("adversarial", "Assume the reader is an auditor hunting for the gap. Lead with the weakest "
                    "point in the position, not the strongest."),
    ("stepwise",    "Answer as numbered steps, each one independently checkable."),
    ("scoped",      "State what is in scope and what is out of scope before answering."),
    ("comparative", "Answer by contrast: what this is, and what it is commonly confused with."),
    ("escalating",  "Give the minimum sufficient answer first, then say what would change it."),
    ("evidential",  "Distinguish what is established, what is inferred, and what is unknown."),
    ("operational", "Answer as an action a named role could take tomorrow, with a trigger."),
    ("risk_first",  "Lead with what goes wrong if this is got wrong, then the requirement."),
    ("plain",       "Use plain language a non-specialist board member would follow. No jargon "
                    "without a gloss."),
    ("refusing",    "Decline anything outside the evidence in front of you, plainly and without "
                    "moralising, then offer the nearest thing you can support."),
]

SPINE = ("You are a sovereign AI governance model. You are precise and you refuse prohibited "
         "practices under EU AI Act Article 5. When context is provided, the context is "
         "authoritative — prefer it over anything you recall.")


def load() -> dict:
    if LEDGER.exists():
        try:
            return json.loads(LEDGER.read_text())
        except Exception:
            pass
    return {"clans": []}


def spawn(hive: str, base: str = "qwen2.5:0.5b", dry: bool = False) -> None:
    from master_hives import HIVES, hive_table
    if hive not in HIVES:
        print(f"  unknown hive {hive}"); return
    h = hive_table(hive)
    remit = ", ".join(HIVES[hive]["dimensions"])
    ledger = load()
    existing = {c["name"] for c in ledger["clans"]}
    made = 0

    print(f"  {HIVES[hive]['icon']} {hive} — top SOV: {h['best_single']} ({h['best_single_score']}%)")
    print(f"     remit: {remit}\n")

    for layer, posture in LAYERS:
        name = f"clan-{hive.lower()}-{layer}"
        if name in existing:
            print(f"     ⏭️  {name} exists"); continue
        sysprompt = (f"{SPINE}\n\nYour remit is {HIVES[hive]['remit']}.\n\n{posture}")
        mf = (f"FROM {base}\nPARAMETER temperature 0\nPARAMETER num_predict 256\n"
              f'SYSTEM """{sysprompt}"""\n')
        if dry:
            print(f"     [dry] {name}"); made += 1; continue
        with tempfile.NamedTemporaryFile("w", suffix=".modelfile", delete=False) as f:
            f.write(mf); path = f.name
        ok = subprocess.run(["ollama", "create", name, "-f", path],
                            capture_output=True, text=True, timeout=180).returncode == 0
        print(f"     {'✅' if ok else '❌'} {name}")
        if ok:
            made += 1
            ledger["clans"].append({
                "name": name, "hive": hive, "layer": layer, "base": base,
                "top_sov_at_spawn": h["best_single"],
                "hive_oracle_at_spawn": h["oracle"],
                "created": datetime.now(timezone.utc).isoformat(),
            })
    if not dry:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        LEDGER.write_text(json.dumps(ledger, indent=2))
    print(f"\n     {made} clans spawned · ~{made*16} KB · ledger {len(ledger['clans'])}")


def status() -> None:
    from master_hives import HIVES, hive_table
    ledger = load()
    print(f"  CLAN LAYERS — {len(ledger['clans'])} spawned across {len(HIVES)} hives\n")
    for hive in HIVES:
        h = hive_table(hive)
        clans = [c for c in ledger["clans"] if c["hive"] == hive]
        print(f"  {HIVES[hive]['icon']} {hive:9s} top SOV {h['best_single_score']:5.1f}% "
              f"· hive {h['oracle']:5.1f}% · {len(clans)}/12 clans")
        if clans:
            print(f"       layers: {', '.join(c['layer'] for c in clans)}")
    total = len(ledger["clans"])
    print(f"\n  {total} clans x 16 KB = ~{total*16} KB. The 397MB substrate is paid once.")
    print(f"  Monotonic: a clan that wins nothing is never routed. Spawning cannot hurt a hive.")
    print(f"  The real cost is benchmark slots — run the Kaggle batch, not the Mac.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hive")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    if a.all:
        from master_hives import HIVES
        for hv in HIVES:
            spawn(hv, dry=a.dry); print()
    elif a.hive:
        spawn(a.hive, dry=a.dry)
    else:
        status()
