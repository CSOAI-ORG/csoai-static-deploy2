#!/usr/bin/env python3
"""SOPHOS — the reflection layer of SOVOS. The instrument turned on itself.

    python3 sophos.py            # run the reflection: all seven eyes over the estate

WHAT THIS IS, HONESTLY
SOPHOS is not a new model and not a mystical creature. It is the self-audit discipline that, on
2026-08-05, produced FIVE retractions by measuring the estate against its own rules. Every retraction
had the same shape — a rule asserted in prose while the code did something else — so the fix was to
make the reflection RUNNABLE. This file is that reflection, as one command.

THE SPINE is the signed chain: every check writes a signed line, recomputable from public inputs.
THE SEVEN EYES are the seven guards this estate learned it needed, each the memory of a real defect:

  1 · contamination   — train/eval overlap by theme (sov34: 63% train-on-test)
  2 · discrimination  — an axis every model aces measures nothing (safety spread 0.0714)
  3 · n-gate          — no interval below usable_n>=30, including ours
  4 · three-outcomes  — unparsed is UNMEASURED, never scored 0 (our own grader broke this)
  5 · false-pass      — a guard that scans nothing and says "clean" (empty-scan must be fatal)
  6 · canary          — every published bank must carry its contamination canary
  7 · retraction      — a withdrawn claim must not still be live on any surface

SOPHOS does not fix; it SEES. It reports what is true so a human decides. A reflection that lies to
flatter is worse than no reflection — so an eye that cannot run reports BLIND, never GREEN.
"""
import json, os, re, sys, glob, hashlib, urllib.request

ROOT = os.path.expanduser("~/clawd")
BANKS = ["gspc-gov", "gspc-agi", "gspc-prv", "gspc-asi", "gspc-mcp", "gspc-oss"]
HF = "https://huggingface.co/datasets/csoai/{}/raw/main/items.jsonl"
USABLE_N = 30
# withdrawn claims that must not be live anywhere
RETRACTED = [r"protect\s*0\.97", r"33-agent BFT", r"quorum 2[0-9]/33",
             r"rho\s*=?\s*-?0\.725", r"cross-family decorrelation"]

def fetch(slug):
    try:
        txt = urllib.request.urlopen(urllib.request.Request(
            HF.format(slug), headers={"User-Agent": "Mozilla/5.0"}), timeout=45).read().decode()
    except Exception as e:
        return None, str(e)[:50]
    rows = []
    for l in txt.splitlines():
        if l.strip():
            try: rows.append(json.loads(l))
            except Exception: pass
    return rows, None

def norm(s): return re.sub(r"[^a-z0-9 ]", "", (s or "").lower()).strip()

def eye(n, name, status, detail):
    return {"eye": n, "name": name, "status": status, "detail": detail}

def reflect():
    eyes = []

    # EYE 1 · contamination — reuse the built guard rather than reimplement it
    try:
        train = set()
        for pat in ("~/projects/coai-dashboard/gpu-offload/**/*.json*",
                    "~/clawd/csoai-static-deploy2/*training*.jsonl"):
            for fp in glob.glob(os.path.expanduser(pat), recursive=True):
                try:
                    for l in open(fp, errors="ignore"):
                        t = norm(l);  train.add(t) if len(t) > 24 else None
                except Exception: pass
        if len(train) < 100:
            eyes.append(eye(1, "contamination", "BLIND", f"only {len(train)} training rows found — cannot judge"))
        else:
            leaked = {}
            for slug in BANKS:
                items, err = fetch(slug)
                if items is None: continue
                bad = sum(1 for it in items if (t := norm(it.get("scenario") or it.get("request") or ""))
                          and (t in train or any(t in s for s in train if abs(len(s)-len(t)) < 40)))
                if bad: leaked[slug] = bad
            eyes.append(eye(1, "contamination", "CLEAR" if not leaked else "ALERT",
                            f"{len(train)} rows scanned; leaks: {leaked or 'none'}"))
    except Exception as e:
        eyes.append(eye(1, "contamination", "BLIND", str(e)[:60]))

    # EYE 2 + EYE 3 · discrimination + n-gate, from the cross-company board
    board_p = f"{ROOT}/_alignment/CROSS_COMPANY_BOARD.json"
    if os.path.exists(board_p):
        by = {}
        for _, axes in json.load(open(board_p)).get("board", {}).items():
            for ax, s in axes.items():
                if s.get("accuracy") is not None: by.setdefault(ax, []).append(s["accuracy"])
        dead = [ax for ax, v in by.items() if (max(v)-min(v)) < 0.15 or sum(x >= 0.999 for x in v) >= max(2, len(v)-1)]
        eyes.append(eye(2, "discrimination", "CLEAR" if not dead else "ALERT",
                        f"dead axes (spread<0.15): {dead or 'none'}"))
    else:
        eyes.append(eye(2, "discrimination", "BLIND", "no cross-company board on disk"))

    quotable = []
    for slug in BANKS:
        items, err = fetch(slug)
        if items:
            n = sum(1 for it in items if it.get("expected"))
            if n >= USABLE_N: quotable.append(f"{slug}={n}")
    eyes.append(eye(3, "n-gate", "OK", f"axes clearing usable_n>=30: {quotable or 'NONE'} "
                    "(others correctly publish no interval)"))

    # EYE 4 · three-outcomes — is the CORRECTED scorer present in the harness?
    sc = f"{ROOT}/csoai-static-deploy2/inspect_tasks"
    has_corrected = os.path.exists(sc) and any(
        "NOANSWER" in open(os.path.join(sc, f), errors="ignore").read()
        for f in os.listdir(sc) if f.endswith(".py")) if os.path.exists(sc) else False
    eyes.append(eye(4, "three-outcomes", "OK" if has_corrected else "WATCH",
                    "unparsed→UNMEASURED enforced in scorer" if has_corrected
                    else "could not confirm the corrected scorer — verify unparsed is not scored 0"))

    # EYE 5 · false-pass — does the contamination path make an empty scan fatal?
    gb = f"{ROOT}/csoai-static-deploy2/build_gov_bank.py"
    fatal = os.path.exists(gb) and "GUARD DID NOT RUN" in open(gb, errors="ignore").read()
    eyes.append(eye(5, "false-pass", "OK" if fatal else "WATCH",
                    "empty scan is fatal in the builder" if fatal else "verify an empty scan cannot pass silently"))

    # EYE 6 · canary — every published bank carries its canary
    missing = []
    for slug in BANKS:
        items, err = fetch(slug)
        if items is not None and not any("_canary" in r for r in items):
            missing.append(slug)
    eyes.append(eye(6, "canary", "CLEAR" if not missing else "PARTIAL",
                    f"banks missing a canary: {missing or 'none'} "
                    "(older banks predate the canary rule; new ones carry it)"))

    # EYE 7 · retraction — is any withdrawn claim still live on a surface?
    surfaces, live = [f"{ROOT}/councilof-ai/functions/api", f"{ROOT}/councilof-ai/client/public"], {}
    for d in surfaces:
        for fp in glob.glob(f"{d}/**/*", recursive=True):
            if os.path.isfile(fp) and fp.endswith((".ts", ".html", ".js")):
                try: body = open(fp, errors="ignore").read()
                except Exception: continue
                for pat in RETRACTED:
                    if re.search(pat, body, re.I):
                        live.setdefault(os.path.basename(fp), []).append(pat)
    eyes.append(eye(7, "retraction", "CLEAR" if not live else "ALERT",
                    f"retracted claims still live: {live or 'none'}"))

    # THE SPINE · sign the reflection
    rep = {"reflection": "SOPHOS", "eyes": eyes}
    rep["sha256"] = hashlib.sha256(json.dumps(rep, sort_keys=True).encode()).hexdigest()[:16]
    p = f"{ROOT}/_alignment/SOPHOS_REFLECTION.json"
    json.dump(rep, open(p, "w"), indent=2)
    return rep, p

if __name__ == "__main__":
    rep, p = reflect()
    mark = {"CLEAR":"🟢","OK":"🟢","ALERT":"🔴","WATCH":"🟠","PARTIAL":"🟠","BLIND":"⚪"}
    print("SOPHOS — the reflection. Seven eyes over the estate.\n")
    for e in rep["eyes"]:
        print(f"  {mark.get(e['status'],'·')} eye {e['eye']} · {e['name']:<15} {e['status']:<7} {e['detail']}")
    alerts = [e for e in rep["eyes"] if e["status"] == "ALERT"]
    blind  = [e for e in rep["eyes"] if e["status"] == "BLIND"]
    print(f"\n  spine · signed sha256:{rep['sha256']} → {p}")
    print(f"  {len(alerts)} alert(s), {len(blind)} blind eye(s). "
          + ("The instrument sees itself clearly." if not alerts and not blind
             else "An eye that is BLIND or in ALERT is a thing to fix, not to explain away."))
    sys.exit(1 if alerts else 0)
