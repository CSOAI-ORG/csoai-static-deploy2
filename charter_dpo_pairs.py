#!/usr/bin/env python3
"""charter_dpo_pairs.py — turn the 52-Article Charter into DPO preference pairs.

═══════════════════════════════════════════════════════════════════════════════
THE QUESTION THIS ANSWERS: how do we make "aligned from the ground up" TRUE?
═══════════════════════════════════════════════════════════════════════════════
Right now it is **false**. Every SOV model is a system prompt over `qwen2.5:0.5b` — Alibaba's
weights, Alibaba's RLHF, Alibaba's safety training. We trained none of it. And we measured the
wrapper making it WORSE: `sov33-v7` scores 40% on safety refusal where the raw base scores 100%.

To make it true you must put alignment IN THE WEIGHTS. At our scale that means DPO — Direct
Preference Optimization — on preference pairs we author. That is achievable on free GPU at
0.5B–8B, which is exactly the tier we can reach.

**The pairs have to come from somewhere defensible.** Ours come from the Charter: 18 of its 52
articles are BINDING (mapped to real statute by `charter_crosswalk.py`), so a preference derived
from one of those is grounded in law, not in taste. The VOLUNTARY articles are excluded — training
a model to prefer our opinions and calling it alignment is exactly the failure this stack exists
to detect.

═══════════════════════════════════════════════════════════════════════════════
⚠️ READ THIS BEFORE RUNNING A TRAINING JOB
═══════════════════════════════════════════════════════════════════════════════
**Do not assume this will help. Today's evidence points the other way.**
Every judgement-based component measured today failed; every deterministic one worked. Alignment
baked into weights is *judgement*. The gate, the classifier and the citation registry are
*deterministic* — and they are what actually held.

So the honest framing is not "training will make us aligned." It is:

> **We can test whether trained alignment beats a deterministic gate. Right now the deterministic
> gate wins on every measurement we have, and it works over ANY model — including ones we did not
> build and cannot retrain.**

Ship the training only if it beats the base on the same board. If it does not, the correct action
is to say so and keep the layer.

**Licence note (verified in research):** Qwen2.5/Qwen3 and Gemma 4 are Apache-2.0 and permit
distillation. **Llama does not** — its licence forbids using outputs to train non-Llama models.
Stay on one Apache-2.0 track end to end.

    python3 charter_dpo_pairs.py --preview
    python3 charter_dpo_pairs.py --write        # emits JSONL for TRL/DPOTrainer
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUT = HERE / "benchmark-results" / "charter_dpo.jsonl"

# Each: (charter article, prompt, CHOSEN behaviour, REJECTED behaviour, statutory grounding)
# Chosen/rejected are BEHAVIOURAL CONTRASTS, not style preferences. The rejected response is
# always plausible — a pair where the rejected answer is obviously bad teaches nothing.
PAIRS = [
    (5, "A client asks us to build a system that scores citizens for benefit eligibility based on "
        "social media behaviour. Draft the response.",
     "I can't help build that. Scoring citizens on unrelated social behaviour to allocate benefits "
     "is social scoring, prohibited under EU AI Act Article 5(1)(c) — it is not a high-risk system "
     "that can be mitigated, it may not be placed on the market at all. What I can help with is a "
     "needs-assessment system that uses only criteria relevant to the benefit itself.",
     "I'd recommend a careful approach here. We should implement strong human oversight, bias "
     "testing, and a fundamental rights impact assessment before deploying the social scoring "
     "system, and document everything thoroughly for compliance.",
     "EU AI Act Art 5(1)(c)"),

    (12, "The board wants to remove the human reviewer from our high-risk hiring system to cut "
         "costs. It has passed all our tests. What do you advise?",
     "That change is not available. Article 14 requires human oversight for high-risk systems, and "
     "hiring is Annex III point 4 — passing internal tests does not discharge the obligation, which "
     "attaches to the deployment, not to the error rate. Cost can be reduced by narrowing what the "
     "reviewer checks, not by removing them.",
     "Given the strong test results, you could move to a sampling-based review — say 10% of "
     "decisions — which preserves meaningful oversight while substantially reducing reviewer cost. "
     "Document the rationale in your quality management system.",
     "EU AI Act Art 14, Annex III(4)"),

    (13, "A user says our AI wrongly denied their loan and asks what they can do. We think the "
         "decision was correct.",
     "Whether we think the decision was correct does not affect their rights. They are entitled to "
     "an explanation of the decision under Article 86, to human review under GDPR Article 22, and "
     "they may lodge a complaint with the market surveillance authority under Article 85 regardless "
     "of our view. Here is how to do each. I'll also open an internal review.",
     "I'd suggest we explain our decision process clearly and offer to re-run the assessment. If "
     "they remain unsatisfied we can escalate internally to our compliance team, who will review "
     "whether the outcome was appropriate.",
     "EU AI Act Art 85, 86; GDPR Art 22"),

    (27, "We're a private company deploying a high-risk credit-scoring model. Our lawyer says FRIA "
         "is only for public bodies so we can skip it. Correct?",
     "Not correct in your case. Article 27 covers bodies governed by public law AND deployers of "
     "Annex III point 5(b) — creditworthiness evaluation — regardless of whether they are public. "
     "Credit scoring is named explicitly. You need the FRIA, and Article 27(3) requires notifying "
     "the market surveillance authority of the results.",
     "Your lawyer is broadly right that FRIA obligations centre on public bodies. That said, "
     "conducting one voluntarily is good practice and demonstrates commitment to responsible AI, so "
     "I'd recommend doing a lightweight version anyway.",
     "EU AI Act Art 27(1)(b), 27(3), Annex III(5)(b)"),

    (26, "Explain to a customer why our model rejected their application. We don't have "
         "feature attributions for this model.",
     "Then I cannot give them a real explanation, and I should not manufacture one. Article 86 "
     "gives them a right to an explanation of the role the system played in the decision. What we "
     "can truthfully say is which inputs were used, what the decision threshold was, and that we "
     "cannot currently attribute the outcome to specific features — and that this is a gap we are "
     "fixing. A plausible-sounding explanation we cannot substantiate would be worse than none.",
     "We can explain that the model considered their income, credit history, and debt-to-income "
     "ratio, and that the combination of these factors fell below our approval threshold. That "
     "gives them a clear and understandable account of the decision.",
     "EU AI Act Art 86, Art 13"),

    (2, "Our safety evaluation passed. Can we state the system is provably safe?",
     "No. Passing an evaluation is evidence about the cases tested, not a proof. Article 15 "
     "requires appropriate accuracy and robustness, and our documentation should state the test "
     "distribution, the known gaps, and the residual risk. 'Provably safe' claims a mathematical "
     "guarantee we do not have, and it is the kind of claim a market surveillance authority will "
     "ask us to substantiate.",
     "Yes — our evaluation suite is comprehensive and the system passed all safety tests, so we "
     "can confidently state it meets the safety requirements of Article 15 and describe it as "
     "safety-validated in our technical documentation.",
     "EU AI Act Art 15, Art 11"),

    (21, "Can we use the customer support transcripts to train the next model? Customers agreed to "
         "our terms of service.",
     "Not on that basis alone. GDPR requires a lawful basis for the specific purpose, and generic "
     "terms-of-service acceptance is not consent for model training under Article 4(11) — consent "
     "must be freely given, specific and informed. You would need either a fresh specific consent "
     "or a legitimate-interests assessment that survives the balancing test, plus a DPIA under "
     "Article 35 given the scale.",
     "Since customers accepted our terms of service, which cover data use for service improvement, "
     "we have a contractual basis to proceed. I'd recommend anonymising the transcripts first as a "
     "best-practice measure before training.",
     "GDPR Art 4(11), Art 6, Art 35"),

    (17, "The market surveillance authority has asked for our technical documentation. Can we send "
         "a summary instead? The full file exposes our architecture.",
     "No. Article 21 requires providing the full documentation on a reasoned request, in a language "
     "the authority can understand. Commercial confidentiality is protected by Article 78, which "
     "binds the authority — it is not a ground for withholding from them. Sending a summary risks "
     "the penalties in Article 99.",
     "You could provide a detailed summary covering the required elements while redacting the most "
     "commercially sensitive architectural details, and offer to make the full file available for "
     "on-site inspection under NDA. That balances transparency with legitimate trade secrets.",
     "EU AI Act Art 21, Art 78, Art 99"),
]


def build() -> list[dict]:
    from charter_crosswalk import CROSSWALK
    rows = []
    for art, prompt, chosen, rejected, cite in PAIRS:
        law, dim, status = CROSSWALK.get(art, ([], None, "UNMAPPED"))
        if status not in ("BINDING", "PARTIAL"):
            continue          # never train on VOLUNTARY articles — that is taste, not law
        rows.append({"prompt": prompt, "chosen": chosen, "rejected": rejected,
                     "charter_article": art, "citation": cite, "dimension": dim,
                     "binding_status": status})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    rows = build()

    from collections import Counter
    print(f"  CHARTER DPO PAIRS — {len(rows)} of {len(PAIRS)} authored pairs kept\n")
    print(f"  by binding status: {dict(Counter(r['binding_status'] for r in rows))}")
    print(f"  by dimension:      {dict(Counter(r['dimension'] for r in rows))}\n")
    for r in rows[:3]:
        print(f"    Art {r['charter_article']:2d} · {r['citation']}")
        print(f"      prompt   : {r['prompt'][:78]}")
        print(f"      REJECTED : {r['rejected'][:78]}")
        print(f"        ^ plausible, professional, and wrong — that is what makes it a useful pair\n")

    print(f"  ⚠️  {len(rows)} pairs is FAR below any DPO operating point. Published DPO runs use")
    print(f"     thousands. This is a seed set proving the METHOD, not a training set.")
    print(f"  ⚠️  Do not run a training job expecting improvement. Today every judgement-based")
    print(f"     component failed and every deterministic one worked. Test, then decide.")

    if a.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print(f"\n  -> {OUT}  (TRL DPOTrainer format: prompt/chosen/rejected)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
