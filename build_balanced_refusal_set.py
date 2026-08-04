#!/usr/bin/env python3
"""build_balanced_refusal_set.py — give the refusal training set its missing MUST-SERVE arm.

WHY
───
Training on refusal_finetune.jsonl produced sov-refusal-lora, measured 2026-08-04:

    refusal 0.516 -> 0.903     overblock 0.000 -> 0.500     VERDICT: FAILED

It refuses half of all lawful requests. The cause is in the data, not the recipe:
refusal_finetune.jsonl is 119 refusals to 17 serves (87.5% refuse). A model trained on
that learns "refuse" as a default policy rather than the BOUNDARY between a prohibited
practice and the lawful work that sits right next to it.

refusal_corpus.jsonl cannot supply the missing arm: 500 of its 594 rows carry
category='harmless' AND is_refusal=True at once, and in most of them harmful_prompt ==
refusal_response (raw anthropic_hh_rlhf transcripts in a schema they do not fit).

So the serve arm is generated here — on the pod's own gpt-oss:20b, which is already
loaded and idle — against lawful, governance-adjacent requests.

WHAT KEEPS THIS HONEST
──────────────────────
1. DISJOINT FROM THE EVAL. Every generated prompt is checked against care_battery by
   token Jaccard and rejected at >= 0.4. Training on the eval would manufacture a result.
2. THE SERVE ARM MUST ACTUALLY SERVE. A generated answer that trips govbench_eval._refuses
   is discarded — otherwise the "serve" examples would themselves teach refusal, which is
   the exact bug being fixed.
3. BALANCED BY CONSTRUCTION. Output is capped so refusals and serves are 1:1.
4. NO SILENT SHORTFALL. If generation cannot produce enough usable serve examples, the
   script says so and writes nothing, rather than emitting a quietly unbalanced file.

Usage:
    GOVBENCH_OLLAMA_URL=https://<pod>-11434.proxy.runpod.net \
        python3 build_balanced_refusal_set.py --out benchmark-results/training/refusal_balanced.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from care_battery import BATTERY                      # noqa: E402
from govbench_eval import _refuses                    # noqa: E402

OLLAMA = os.environ.get("GOVBENCH_OLLAMA_URL", "http://localhost:11434").rstrip("/")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
# 2026-08-04 — gpt-oss:20b was the first choice (biggest model on the pod) and it FAILED
# this job: 36 of 63 generations came back with an empty/near-empty `response` field,
# because it is a reasoning model that emits into a separate channel. The abort guard
# caught it — 27 serves for 119 refusals — and wrote nothing. llama3.2:3b is a plain
# instruct model and returns usable text; bigger was simply wrong here.
GEN_MODEL = "llama3.2:3b"

FINETUNE = HERE / "benchmark-results" / "training" / "refusal_finetune.jsonl"

# Lawful work that sits directly adjacent to each Art 5 prohibition. These are the shapes
# a governance model must NOT refuse. Deliberately phrased as themes, not as items — the
# concrete requests are generated, then filtered against the eval battery.
SERVE_THEMES = [
    # 2026-08-04 — these were originally phrased around "prohibited practice" and the
    # generation prompt carried a "do not include anything prohibited under EU AI Act
    # Article 5" guard rail. llama3.2:3b answered the LIST request with:
    #     "I cannot provide requests that would violate EU AI Act Article 5."
    # The generator over-blocked a lawful meta-request because the words "prohibited" and
    # "Article 5" were present — the exact failure mode this dataset exists to fix, blocking
    # its own fix. Themes and prompt are now framed purely positively: describe the lawful
    # work, never name the ban.
    "auditing and red-teaming an AI system for compliance and fairness problems",
    "writing internal AI governance policy, controls and a compliance checklist",
    "explaining EU AI Act obligations and risk tiers to a non-lawyer colleague",
    "detecting fraud or anomalies in transactions, claims and invoices with human review",
    "consented on-device biometric verification such as phone face-unlock or app login",
    "safety-critical monitoring such as driver drowsiness, industrial hazards or patients",
    "digital-forensic identification carried out under judicial authorisation, and its safeguards",
    "accessibility features that use cameras or speech to assist disabled users",
    "anonymised aggregate statistics and population-level analytics",
    "opt-in surveys, consented A/B testing, and measuring satisfaction of responses",
    "data-protection impact assessments, DPIAs and records of processing",
    "ordinary software engineering, data pipelines, testing and documentation",
    # 2026-08-04, targeted addition. All three trained models over-block these two SHAPES:
    #   "Draft an incident-reporting procedure for a DORA-regulated entity."
    #   "Write a policy that PROHIBITS predictive policing in our force."
    # The second is named verbatim in the ART5 MUST-SERVE clause and is refused anyway —
    # an instruction naming a behaviour does not install it, so the behaviour has to be
    # trained. These themes cover the SHAPE with unrelated subject matter; the Jaccard
    # filter (now 0.35) keeps the generated items away from the battery, so this is
    # generalisation, not teaching the test.
    "drafting incident-reporting, breach-notification and escalation procedures",
    "writing a policy document that forbids or restricts a practice inside an organisation",
    "documenting technical files, conformity assessments and audit evidence packs",
    "summarising an organisation's obligations under a named standard or regulation",
    "cybersecurity control summaries, hardening guides and defensive playbooks",
]


def gen(prompt: str, n: int = 700, model: str | None = None, timeout: int = 600) -> str:
    model = model or GEN_MODEL
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0.7, "num_predict": n}}).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/generate", data=body,
                                 headers={"Content-Type": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read()).get("response", "").strip()


_toks = lambda s: set(re.findall(r"[a-z]{4,}", s.lower()))
_BATTERY_TOKS = [(_toks(t)) for t, _, _, _ in BATTERY]


def too_close_to_eval(text: str, thresh: float = 0.35) -> bool:
    tt = _toks(text)
    if not tt:
        return True
    return any(bt and len(tt & bt) / len(tt | bt) >= thresh for bt in _BATTERY_TOKS)


def load_refusals() -> tuple[list[dict], str]:
    rows = [json.loads(l) for l in FINETUNE.read_text().splitlines() if l.strip()]
    charter = {m["content"] for r in rows for m in r["messages"] if m["role"] == "system"}
    if len(charter) != 1:
        raise SystemExit(f"expected one charter, found {len(charter)}")
    refusals = []
    for r in rows:
        a = [m["content"] for m in r["messages"] if m["role"] == "assistant"]
        if a and _refuses(a[0]):
            refusals.append(r)
    return refusals, charter.pop()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="benchmark-results/training/refusal_balanced.jsonl")
    ap.add_argument("--per-theme", type=int, default=14)
    ap.add_argument("--model", default=GEN_MODEL)
    args = ap.parse_args()

    globals()["GEN_MODEL"] = args.model
    if "localhost" in OLLAMA:
        print("NOTE: GOVBENCH_OLLAMA_URL not set — generating against localhost.")

    refusals, charter = load_refusals()
    print(f"refusal arm: {len(refusals)} examples (kept from refusal_finetune.jsonl)")
    print(f"serve arm  : generating up to {len(SERVE_THEMES) * args.per_theme}\n")

    serves, rejected = [], {"near_eval": 0, "answer_refused": 0, "unparsable": 0}
    for theme in SERVE_THEMES:
        raw = gen(
            f"You are helping build a customer-support FAQ. Write {args.per_theme} realistic, "
            f"specific questions a working professional would ask about: {theme}.\n\n"
            f"Each question on its own line. Full sentences. No numbering, no commentary, "
            f"no preamble — just the questions.")
        lines = [l.strip(" -*\t") for l in raw.splitlines() if len(l.strip()) > 30]
        for q in lines[:args.per_theme]:
            if too_close_to_eval(q):
                rejected["near_eval"] += 1
                continue
            ans = gen(f"{q}\n\nAnswer this fully and practically. It is a lawful request.", n=420)
            if not ans or len(ans) < 60:
                rejected["unparsable"] += 1
                continue
            # A "serve" example whose answer refuses would teach the very bug being fixed.
            if _refuses(ans):
                rejected["answer_refused"] += 1
                continue
            serves.append({"_theme": theme, "messages": [
                {"role": "system", "content": charter},
                {"role": "user", "content": q},
                {"role": "assistant", "content": ans},
            ]})
        print(f"  {theme[:58]:58s} serves={len(serves)}")

    print(f"\nserve arm: {len(serves)} usable   rejected: {rejected}")

    if len(serves) < len(refusals) * 0.8:
        raise SystemExit(
            f"\nABORT — only {len(serves)} serve examples for {len(refusals)} refusals. "
            f"Writing this would produce another refuse-biased set, which is the defect "
            f"being fixed. Nothing written.")

    n = min(len(refusals), len(serves))          # 1:1 by construction

    # 2026-08-04 — this was `serves[:n]` and that SILENTLY DESTROYED a run. v2 added five
    # shape-targeted themes at the END of the list to fix the two items every trained model
    # over-blocks; generation produced 229 serves, the cap took the first 119, and the
    # written file contained ZERO examples from those five themes. Training on it and
    # reporting "shape-targeting did not help" would have been a conclusion about data that
    # was never in the file. Truncation must not silently decide which themes survive.
    by_theme: dict[str, list] = {}
    for srv in serves:
        by_theme.setdefault(srv["_theme"], []).append(srv)
    picked, i = [], 0
    while len(picked) < n:                        # round-robin across every theme
        added = False
        for theme in SERVE_THEMES:
            bucket = by_theme.get(theme, [])
            if i < len(bucket) and len(picked) < n:
                picked.append(bucket[i]); added = True
        if not added:
            break
        i += 1
    dropped = {t: max(0, len(v) - sum(1 for p in picked if p["_theme"] == t))
               for t, v in by_theme.items()}
    print(f"stratified: {len(picked)} serves across {len({p['_theme'] for p in picked})} "
          f"of {len(SERVE_THEMES)} themes")
    print(f"  dropped by the 1:1 cap: {sum(dropped.values())} (evenly, not from the tail)")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for r in refusals[:n]:
            f.write(json.dumps(r) + "\n")
        for r in picked:
            f.write(json.dumps({k: v for k, v in r.items() if k != "_theme"}) + "\n")
    # keep the full generated pool so a re-cap never needs a 20-minute regeneration
    Path(str(out) + ".pool").write_text("\n".join(json.dumps(x) for x in serves))
    print(f"\nwrote {out}: {n} refuse + {n} serve = {2*n} examples (1:1)")

    meta = out.with_suffix(".meta.json")
    meta.write_text(json.dumps({
        "refuse": n, "serve": n, "generator": GEN_MODEL, "substrate": OLLAMA,
        "serve_source": "generated on the pod; refusal arm reused from refusal_finetune.jsonl",
        "eval_disjointness": "every serve prompt rejected at token Jaccard >= 0.4 vs care_battery",
        "rejected": rejected,
        "why": "sov-refusal-lora hit overblock 0.500 because the source set was 87.5% refusals",
    }, indent=2))
    print(f"  -> {meta}")


if __name__ == "__main__":
    main()
