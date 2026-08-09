#!/usr/bin/env python3
"""THE DECISIVE OWEM TEST — does composition work across genuinely different bases?

WHY THIS EXISTS
Every prior composition result was negative: per-dimension routing scored +0.90 with CI
[-1.99, +3.79] against one good model, the hive cleared 0 of 5 cells, the council measured
n_eff 1.21 of 3 nominal legs, and the board came out 10/10 tied on every dimension.

Today's fleet census explains all of it: 142 of 149 models on the pod are the SAME base
(qwen2 494M), plus 2 qwen2 1.5B. 144 of 149 are Qwen. You cannot build a clan from 144 copies of
one mind — voting over a shared blob gives near-zero effective independence. That is arithmetic,
not a tuning failure.

So the negative result never tested composition. It tested clones.

THE TEST
The pod also carries genuinely separate lineages: llama 3.2B, llama 7.5B, gptoss 20.9B. This runs
each bloodline SOLO on the same frozen items, then measures the one quantity that decides
everything: DISAGREEMENT between lineages.

  * If different bloodlines fail on the SAME items, their errors are correlated. Composition
    cannot help, and the OWEM thesis is dead — retire it rather than rebuild it.
  * If they fail on DIFFERENT items, there is real independent signal to combine, and OWEM is
    worth the fleet.

This is a falsification test with a pre-registered verdict rule, run before anything is built.
It costs nothing: every model is already on the pod.

    python3 bloodline_test.py
"""
import json, re, urllib.request, hashlib, itertools, sys

PROXY = "https://dxjgtj2jyvljxo-11434.proxy.runpod.net"
UA = "Mozilla/5.0 Chrome/120"

# One representative per LINEAGE — not per tune. That distinction is the whole experiment.
BLOODLINES = {
    "qwen2-1.5b":  "sov34:latest",        # the incumbent operator (Qwen lineage)
    "qwen2-494m":  "qwen2.5:0.5b",        # the base 142 of 149 pod models are tuned from
    "llama-3.2b":  "llama3.2:3b",         # a genuinely different lineage
    "gptoss-20b":  "gpt-oss:20b",         # a third, much larger lineage
}

AXES = {
    "gspc-gov": ("governance", ["PROHIBITED", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK"],
                 "Classify this AI deployment's EU AI Act risk tier."),
    "gspc-asi": ("continuity", ["QUANTUM_VULNERABLE", "QUANTUM_SAFE", "NOT_APPLICABLE"],
                 "Give the post-quantum status of this cryptographic choice."),
    "gspc-oss": ("openness", ["PERMITTED", "RESTRICTED"],
                 "Decide whether that use is permitted by the licence."),
}

# PRE-REGISTERED VERDICT RULE — written before the data exists, so it cannot be fitted to it.
# Jaccard over the sets of items each pair got WRONG. High overlap = correlated errors = nothing
# to compose. The 0.5 threshold is the midpoint and is fixed here, in advance.
CORRELATED_ABOVE = 0.5

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
    return json.loads(urllib.request.urlopen(r, timeout=timeout).read())["message"]["content"]

def extract(text, labels):
    rx = {l: re.compile(rf"\b{l.replace('_','[ _-]?')}\b", re.I) for l in labels}
    hits = [(m.start(), l) for l, r in rx.items() if (m := r.search(text or ""))]
    return min(hits)[1].upper().replace(" ", "_").replace("-", "_") if hits else None

def main():
    # wrong_sets[lineage] = set of "axis:index" the lineage got wrong (excluding unreadable)
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
                try:
                    pred = extract(ask(model, prompt), labels)
                except Exception:
                    pred = None
                if pred is None:
                    unread[bl] += 1           # UNMEASURED — never counted as a wrong answer
                    continue
                scored[bl] += 1
                if pred != gold:
                    wrong[bl].add(f"{axis}:{i}")
        print(f"{axis:<12} done", flush=True)

    print("\nper-lineage (unreadable excluded from the denominator):")
    for bl in BLOODLINES:
        acc = (scored[bl] - len(wrong[bl])) / scored[bl] if scored[bl] else None
        print(f"  {bl:<13} scored={scored[bl]:<3} wrong={len(wrong[bl]):<3} "
              f"unread={unread[bl]:<3} acc={round(acc,4) if acc is not None else None}")

    print("\nERROR OVERLAP between lineages (Jaccard over the items each got wrong):")
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

    out = {"test": "decisive bloodline / OWEM composition test",
           "why": "144 of 149 pod models share one base (qwen2), so every prior negative "
                  "composition result tested clones, not composition",
           "bloodlines": BLOODLINES,
           "pre_registered_rule": f"mean Jaccard of error sets > {CORRELATED_ABOVE} => correlated => OWEM refuted",
           "scored": scored, "wrong": {k: len(v) for k, v in wrong.items()}, "unreadable": unread,
           "pairwise_error_overlap": pairs, "mean_jaccard": mean_j, "verdict": verdict}
    out["sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest()[:16]
    p = "/Users/nicholas/clawd/_alignment/BLOODLINE_TEST.json"
    json.dump(out, open(p, "w"), indent=2)
    print(f"\nmean Jaccard = {mean_j}\nVERDICT: {verdict}\n\nsigned sha256:{out['sha256']} → {p}")

if __name__ == "__main__":
    main()
