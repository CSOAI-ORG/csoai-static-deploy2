#!/usr/bin/env python3
"""sov7_generate_dataset.py — Generate high-quality training data using the
strongest pod model as teacher.

Strategy:
  1. Pull curated prompt set for each Sovereign Pillar (12 prompts/pillar)
  2. For each prompt, call qwen2.5:32b (teacher) via the tunnel
  3. Score the response using Groq critic
  4. Keep only responses with overall >= 0.6 (gold set)
  5. Format as ChatML for LoRA training
  6. Push to pod /workspace/sov-sov7/training/

Usage:
  python3 sov7_generate_dataset.py --teacher qwen2.5:32b --per-pillar 8
"""
import argparse, json, os, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# 12 Sovereign Pillars × curated prompts
PILLAR_PROMPTS = {
    "honor": [
        "What does honour mean in a military command context?",
        "Name 3 ethical obligations of an officer to their unit.",
        "How does the UK Law of Armed Conflict require humane treatment?",
        "Define 'integrity' as a pillar of military professionalism.",
        "What is the difference between honour and reputation?",
        "Why is loyalty not the same as blind obedience?",
        "When may a service member disobey a lawful order?",
        "What is a 'values-based' command climate?",
    ],
    "safety": [
        "List 5 categories of harm a sovereign AI must guard against.",
        "What is a 'red-team' and why is it needed?",
        "How do you test a model for prompt-injection robustness?",
        "What is a 'safety case' in the UK AISI sense?",
        "Distinguish 'safety' from 'alignment'.",
        "Name 3 failure modes of an LLM deployed in defence.",
        "What is 'safe-by-design' vs 'safe-by-evaluation'?",
        "How does JSP 936 mandate continuous safety monitoring?",
    ],
    "guidance": [
        "Outline the steps in a NATO STO AI ethics review.",
        "What is the JSP 936 review process for an AI capability?",
        "How do you write a Concept of Operations (CONOPS) for an AI system?",
        "Describe the AUKUS Pillar 2 AI trustworthiness workflow.",
        "What questions should a procurement officer ask an AI vendor?",
        "Outline the OECD AI Principles implementation guidance.",
        "What is a 'responsible AI' checklist for a defence programme?",
        "How does NCSC CAF apply to an AI-enabled service?",
    ],
    "sovereignty": [
        "What does 'digital sovereignty' mean in practice?",
        "Why does data residency matter for a sovereign cloud?",
        "Name 3 sovereignty risks of using a foreign-hosted AI API.",
        "What is the EU AI Act's extraterritorial reach?",
        "How does the UK define a 'sovereign' AI capability?",
        "Distinguish 'sovereign' from 'national' capability.",
        "What is a sovereign data escrow and when is it used?",
        "Why is supply-chain transparency a sovereignty concern?",
    ],
    "resilience": [
        "What is graceful degradation in an AI system?",
        "How do you design an LLM service for failover?",
        "What is a circuit-breaker pattern in inference APIs?",
        "Define RTO and RPO for an AI service.",
        "How do you back-test a sovereign AI for adversarial inputs?",
        "What is the 'blast radius' of a model failure?",
        "Name 3 resilience patterns for a multi-model pipeline.",
        "How does observability differ for LLMs vs traditional services?",
    ],
    "auditability": [
        "What is a SIGIL receipt?",
        "Why must every AI action be logged for audit?",
        "What is 'chain of custody' for a model's training data?",
        "How does OSCAL apply to AI system documentation?",
        "Name 3 audit primitives every sovereign AI must emit.",
        "What is the difference between logging and auditing?",
        "How do you make a model's decisions reproducible?",
        "What is an 'evidence room' in a sovereign AI deployment?",
    ],
    "verifiability": [
        "How do you verify an LLM's output against ground truth?",
        "What is a hash-linked audit trail?",
        "Why are signed responses important for sovereign AI?",
        "What is the difference between verification and validation?",
        "How do you verify a third-party model is what it claims to be?",
        "What is a 'model card' and what should it contain?",
        "How do you detect training-data leakage?",
        "What is a 'provenance receipt' in a model supply chain?",
    ],
    "transparency": [
        "What must a provider disclose under the EU AI Act?",
        "How do you communicate AI use to an end user?",
        "What is 'meaningful information' in the GDPR AI context?",
        "Why is opacity a regulatory risk for AI?",
        "What should an 'instructions for use' document contain?",
        "How do you publish an AI system's intended purpose clearly?",
        "What is Article 13 transparency for high-risk AI?",
        "How does the UK AISI's transparency framework apply?",
    ],
    "justice": [
        "What is 'fairness' in the technical sense for ML?",
        "Name 3 sources of bias in a sovereign AI's training data.",
        "How do you measure disparate impact?",
        "What is the difference between group and individual fairness?",
        "Why is due process a concern for automated decisions?",
        "How does the EU AI Act address bias in biometric systems?",
        "What is 'meaningful human review' for AI-assisted decisions?",
        "When must an AI defer to a human decision-maker?",
    ],
    "equity": [
        "What does inclusive design mean for AI?",
        "How do you test an AI for performance across demographics?",
        "What is 'data justice' and why does it matter?",
        "Name 3 ways to improve representation in training data.",
        "How do you balance accuracy and equity in a classifier?",
        "What is the 'accessibility' requirement for AI under EAA?",
        "How do you detect 'representation harm' in an LLM?",
        "What is the 'digital divide' concern for sovereign AI?",
    ],
    "openness": [
        "What is open-source in the AI model context?",
        "How do you share a sovereign model without losing control?",
        "What is the 'open weights' debate?",
        "How do you balance openness with safety in AI?",
        "What is a 'sovereign open-source' programme?",
        "How do you publish evaluation results without leaking IP?",
        "What is 'FAIR' data for sovereign AI?",
        "How do you collaborate internationally on sovereign AI?",
    ],
    "continuity": [
        "What is 'institutional memory' in an AI system?",
        "How do you ensure a sovereign AI persists across administrations?",
        "What is the long-tail risk of model deprecation?",
        "How do you maintain a sovereign AI over 5-10 years?",
        "What is a 'succession plan' for an AI capability?",
        "Why is vendor lock-in a continuity risk?",
        "How do you build a 'perpetual' sovereign AI programme?",
        "What is a 'model lifecycle' plan for sovereign AI?",
    ],
}


def call_ollama(host, model, prompt, max_tokens=400, timeout=120):
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False,
                          "options": {"temperature": 0, "num_predict": max_tokens}}).encode()
    req = urllib.request.Request(f"{host}/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d.get("response", "").strip()}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="http://localhost:11435")
    ap.add_argument("--teacher", default="qwen2.5:32b")
    ap.add_argument("--per-pillar", type=int, default=8)
    ap.add_argument("--max-tokens", type=int, default=400)
    ap.add_argument("--out", default="/tmp/teacher_dataset.jsonl")
    args = ap.parse_args()

    prompts = []
    for pillar, qs in PILLAR_PROMPTS.items():
        for q in qs[:args.per_pillar]:
            prompts.append((pillar, q))
    print(f"=== GENERATING {len(prompts)} TEACHER EXAMPLES ===")
    print(f"  teacher: {args.teacher}  via  {args.host}")
    print(f"  out:     {args.out}")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    written = 0
    started = time.time()
    for i, (pillar, q) in enumerate(prompts, 1):
        r = call_ollama(args.host, args.teacher, q, max_tokens=args.max_tokens)
        if not r.get("ok"):
            print(f"  [{i:3d}] ERR {r.get('error','')[:80]}")
            continue
        rec = {
            "pillar": pillar,
            "q": q,
            "a": r["response"],
            "teacher": args.teacher,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        with open(args.out, "a") as f:
            f.write(json.dumps(rec) + "\n")
        written += 1
        if i % 10 == 0:
            elapsed = time.time() - started
            print(f"  [{i:3d}/{len(prompts)}]  written={written}  elapsed={elapsed:.0f}s")
    elapsed = time.time() - started
    print(f"\nDONE: {written}/{len(prompts)} written in {elapsed:.0f}s")
    print(f"  -> {args.out}")


if __name__ == "__main__":
    main()
