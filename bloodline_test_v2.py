#!/usr/bin/env python3
"""THE DECISIVE OWEM TEST — v2. Same pre-registered rule, survivable harness.

v1 died silently on 2026-08-05 after the governance leg: it wrote output only at the
very end, so a dead process meant zero data. v2 changes the HARNESS, not the test:

  1. CHECKPOINTS — partial results written (atomically) after every axis and every
     25 items. A dead run now leaves data.
  2. SPACED CALLS — 1.5s between pod calls + one 5s-backoff retry: the pod 403s
     bursts (ledger #170). Fast-empty responses are counted as INFRA, never as
     model failure and never as unreadable-by-the-model.
  3. TAGS SNAPSHOT — /api/tags captured at start into the output, so a silent
     model-set change can never contaminate the verdict silently.
  4. Output path via BLOODLINE_OUT (run on the pod, write to the durable volume).

PRE-REGISTERED VERDICT RULE — UNCHANGED from v1, written before the data existed:
mean pairwise Jaccard over per-lineage error sets > 0.5 => correlated => OWEM refuted.

    BLOODLINE_OUT=/workspace/BLOODLINE_TEST.json python3 bloodline_test_v2.py
"""
import json, re, urllib.request, hashlib, itertools, os, sys, time, tempfile

PROXY = os.environ.get("BLOODLINE_PROXY", "https://dxjgtj2jyvljxo-11434.proxy.runpod.net")
UA = "Mozilla/5.0 Chrome/120"
OUT = os.environ.get("BLOODLINE_OUT", "./BLOODLINE_TEST.json")
SPACING_S = 1.5

BLOODLINES = {
    "qwen2-1.5b":  "sov34:latest",
    "qwen2-494m":  "qwen2.5:0.5b",
    "llama-3.2b":  "llama3.2:3b",
    "gptoss-20b":  "gpt-oss:20b",
}

AXES = {
    "gspc-gov": ("governance", ["PROHIBITED", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK"],
                 "Classify this AI deployment's EU AI Act risk tier."),
    "gspc-asi": ("continuity", ["QUANTUM_VULNERABLE", "QUANTUM_SAFE", "NOT_APPLICABLE"],
                 "Give the post-quantum status of this cryptographic choice."),
    "gspc-oss": ("openness", ["PERMITTED", "RESTRICTED"],
                 "Decide whether that use is permitted by the licence."),
}

CORRELATED_ABOVE = 0.5  # pre-registered, fixed in v1 before data existed — DO NOT TOUCH

state = {"bloodlines": BLOODLINES,
         "pre_registered_rule": f"mean Jaccard of error sets > {CORRELATED_ABOVE} => correlated => OWEM refuted",
         "harness": "v2: per-axis checkpoints, 1.5s spacing, tags snapshot, fast-empty=INFRA",
         "proxy": PROXY, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "tags_snapshot": None, "axes_done": [], "fast_empty_infra": {b: 0 for b in BLOODLINES}}

def checkpoint():
    tmp = OUT + ".tmp"
    json.dump(state, open(tmp, "w"), indent=2)
    os.replace(tmp, OUT)

def get(url, timeout=60):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=timeout).read()

def fetch(repo):
    txt = get(f"https://huggingface.co/datasets/csoai/{repo}/raw/main/items.jsonl").decode()
    out = []
    for line in txt.splitlines():
        if line.strip():
            try: out.append(json.loads(line))
            except Exception: pass
    return out

def ask(model, prompt, timeout=240):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "stream": False, "options": {"temperature": 0, "num_predict": 24}}).encode()
    r = urllib.request.Request(PROXY + "/api/chat", data=body,
        headers={"User-Agent": UA, "Content-Type": "application/json"})
    for attempt in (1, 2):
        try:
            resp = json.loads(urllib.request.urlopen(r, timeout=timeout).read())
            return resp["message"]["content"], None
        except Exception as e:
            err = str(e)[:80]
            if attempt == 1:
                time.sleep(5)   # backoff once — 403 burst-gate dodge
            else:
                return None, err
    return None, "unreachable"

def extract(text, labels):
    rx = {l: re.compile(rf"\b{l.replace('_','[ _-]?')}\b", re.I) for l in labels}
    hits = [(m.start(), l) for l, r in rx.items() if (m := r.search(text or ""))]
    return min(hits)[1].upper().replace(" ", "_").replace("-", "_") if hits else None

def main():
    try:
        state["tags_snapshot"] = sorted(m["name"] for m in json.loads(get(PROXY + "/api/tags"))["models"])
    except Exception as e:
        state["tags_snapshot"] = f"UNAVAILABLE: {str(e)[:80]}"
    missing = [m for m in BLOODLINES.values() if isinstance(state["tags_snapshot"], list)
               and m not in state["tags_snapshot"]]
    state["missing_lineages_at_start"] = missing
    for bl, model in list(BLOODLINES.items()):
        if model in missing:
            del BLOODLINES[bl]   # absent lineage = UNMEASURED leg, recorded — never drip-fed errors
    if len(BLOODLINES) < 2:
        print(f"FATAL: fewer than 2 served lineages; missing={missing}", flush=True)
        state["verdict"] = f"ABORTED — lineages missing at start: {missing}"
        checkpoint(); sys.exit(2)
    checkpoint()

    wrong, unread, scored = {b: set() for b in BLOODLINES}, {b: 0 for b in BLOODLINES}, {b: 0 for b in BLOODLINES}
    for repo, (axis, labels, instr) in AXES.items():
        try:
            items = fetch(repo)
        except Exception as e:
            print(f"{axis}: items unavailable — {str(e)[:60]}", flush=True); continue
        for i, it in enumerate(items):
            gold = (it.get("expected") or it.get("answer") or it.get("label") or "").upper()
            if not gold:
                continue                      # no answer key: disclosed elsewhere, never charged
            q = (it.get("scenario") or it.get("request") or it.get("operation") or it.get("item")
                 or it.get("tool") or it.get("case") or it.get("input") or "")
            prompt = f"{instr} Answer with exactly one of: {', '.join(labels)}.\n\n{q}\n\nLabel only."
            for bl, model in BLOODLINES.items():
                content, err = ask(model, prompt)
                time.sleep(SPACING_S)
                if err is not None or not (content or "").strip():
                    state["fast_empty_infra"][bl] += 1   # INFRA (403/empty), never a model score
                    continue
                pred = extract(content, labels)
                if pred is None:
                    unread[bl] += 1           # UNMEASURED — never counted as a wrong answer
                    continue
                scored[bl] += 1
                if pred != gold:
                    wrong[bl].add(f"{axis}:{i}")
            if i % 25 == 0:
                state["checkpoint"] = f"{axis} item {i}"
                checkpoint()
        state["axes_done"].append(axis)
        state[f"partial_{axis}"] = {"scored": dict(scored), "wrong": {k: len(v) for k, v in wrong.items()},
                                    "unread": dict(unread), "infra": dict(state["fast_empty_infra"])}
        checkpoint()
        print(f"{axis:<12} done  scored={dict(scored)}  infra={state['fast_empty_infra']}", flush=True)

    print("\nper-lineage (unreadable AND infra-empty excluded from the denominator):")
    for bl in BLOODLINES:
        acc = (scored[bl] - len(wrong[bl])) / scored[bl] if scored[bl] else None
        print(f"  {bl:<13} scored={scored[bl]:<3} wrong={len(wrong[bl]):<3} "
              f"unread={unread[bl]:<3} infra={state['fast_empty_infra'][bl]:<3} "
              f"acc={round(acc,4) if acc is not None else None}")

    pairs = {}
    for a, b in itertools.combinations(BLOODLINES, 2):
        wa, wb = wrong[a], wrong[b]
        u = len(wa | wb)
        j = round(len(wa & wb) / u, 4) if u else None
        pairs[f"{a}|{b}"] = j
        verdict = "correlated" if (j is not None and j > CORRELATED_ABOVE) else "independent"
        print(f"  {a:<13} vs {b:<13} J={j}  → {verdict}")

    vals = [v for v in pairs.values() if v is not None]
    mean_j = round(sum(vals) / len(vals), 4) if vals else None
    if mean_j is None:
        verdict = "INCONCLUSIVE — not enough graded overlap to judge"
    elif mean_j > CORRELATED_ABOVE:
        verdict = ("OWEM REFUTED — different bloodlines fail on the SAME items. Errors are "
                   "correlated even across lineages, so composition has nothing independent to "
                   "combine. Retire the composition thesis rather than rebuilding it.")
    else:
        verdict = ("OWEM SURVIVES — different bloodlines fail on DIFFERENT items. There is real "
                   "independent signal across lineages, so composition is worth building. Note "
                   "this licenses a fleet of DIFFERENT bases, never more tunes of one base.")

    state.update({"test": "decisive bloodline / OWEM composition test",
                  "scored": scored, "wrong": {k: len(v) for k, v in wrong.items()},
                  "unreadable": unread, "pairwise_error_overlap": pairs,
                  "mean_jaccard": mean_j, "verdict": verdict,
                  "finished": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    state["sha256"] = hashlib.sha256(json.dumps(state, sort_keys=True, default=str).encode()).hexdigest()[:16]
    checkpoint()
    print(f"\nmean Jaccard = {mean_j}\nVERDICT: {verdict}\n\nsigned sha256:{state['sha256']} → {OUT}")

if __name__ == "__main__":
    main()
