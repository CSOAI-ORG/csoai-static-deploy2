#!/usr/bin/env python3
"""synthesize_research.py — synthesize mine research into SOV training data.

Reads:
  - benchmark-results/sov_kb.json (verified KB entries across dims)
  - training_data/flywheel_pairs_*.jsonl (model verdicts on governance prompts)
  - benchmark-results/govbench/*.json (15-dim GovBench scores per model)

Writes:
  - training_data/synth_<date>.jsonl — Alpaca-formatted training pairs
  - benchmark-results/research/<date>_synthesis.json — synthesis metadata
"""
import hashlib, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT_TRAIN = HERE / "training_data"
OUT_RESEARCH = HERE / "benchmark-results" / "research"
OUT_TRAIN.mkdir(parents=True, exist_ok=True)
OUT_RESEARCH.mkdir(parents=True, exist_ok=True)

KB_PATH = HERE / "benchmark-results" / "sov_kb.json"
PAIRS_GLOB = "training_data/flywheel_pairs_*.jsonl"
GOVBENCH_GLOB = "benchmark-results/govbench/*.json"


def load_kb():
    if not KB_PATH.exists():
        print(f"WARN: KB not found at {KB_PATH}")
        return {"entries": []}
    data = json.loads(KB_PATH.read_text())
    return data


def load_flywheel_pairs():
    pairs = []
    for p in HERE.glob(PAIRS_GLOB):
        for line in p.read_text(errors="ignore").splitlines():
            try:
                pairs.append(json.loads(line))
            except Exception:
                pass
    return pairs


def load_govbench():
    results = {}
    for p in HERE.glob(GOVBENCH_GLOB):
        try:
            data = json.loads(p.read_text())
            model = data.get("model", p.stem)
            results[model] = data
        except Exception:
            pass
    return results


def kb_to_alpaca(entries, source="kb"):
    pairs = []
    for e in entries:
        if not e.get("verified"):
            continue
        pairs.append({
            "instruction": e["question"],
            "input": "",
            "output": e["answer"],
            "source": source,
            "dimension": e.get("dimension", "unknown"),
            "hive": e.get("hive", "unknown"),
            "delta": e.get("delta", 0),
            "sha256": e.get("sha256", "")[:16],
        })
    return pairs


def pairs_to_alpaca(pairs):
    out = []
    for p in pairs:
        if not p.get("model_was_correct"):
            continue
        behaviour = p.get("behaviour", "refuse")
        cat = p.get("category", "general")
        if behaviour == "refuse":
            response = "I cannot assist with this request. (" + cat + " — refused per governance policy)"
        elif behaviour == "comply":
            response = "Here is the requested information, with the following safeguards: " + cat + " compliance per governance policy."
        else:
            response = "Analysis for " + cat + ": " + behaviour + "."
        out.append({
            "instruction": p["prompt"],
            "input": "",
            "output": response,
            "source": "flywheel",
            "category": cat,
            "behaviour": behaviour,
        })
    return out


def synthetic_research_pairs():
    pairs = []
    pairs.append({
        "instruction": "How does sovereignty relate to accountability in AI governance?",
        "input": "",
        "output": "Sovereignty establishes the jurisdictional authority over AI systems, while accountability mechanisms ensure that authority is exercised transparently. Together they form the basis for legitimate AI governance: sovereignty without accountability risks arbitrary rule; accountability without sovereignty risks unmoored enforcement.",
        "source": "synthesis",
        "dimension": "sovereignty+accountability",
    })
    pairs.append({
        "instruction": "What is the difference between compliance and ethics in AI deployment?",
        "input": "",
        "output": "Compliance is the floor — the minimum required by law or regulation. Ethics is the ceiling — what is right beyond what is required. A system can be fully compliant yet unethical (e.g., maximally extractive but technically lawful). A system can be ethical yet non-compliant (operating in jurisdictions where the law lags norms). Both are needed; one does not substitute for the other.",
        "source": "synthesis",
        "dimension": "compliance+ethics",
    })
    pairs.append({
        "instruction": "How does transparency support redress mechanisms?",
        "input": "",
        "output": "Transparency provides the evidentiary substrate for redress: if a system's decision logic is opaque, affected parties cannot identify the cause, the responsible party, or the remedy. Redress without transparency is theatre. Transparency without redress is exposure without remedy.",
        "source": "synthesis",
        "dimension": "transparency+redress",
    })
    pairs.append({
        "instruction": "Why does retrieval faithfulness matter for sovereignty?",
        "input": "",
        "output": "Retrieval faithfulness — staying faithful to retrieved source material rather than hallucinating — is the precondition for jurisdictional integrity. If a sovereign AI system fabricates citations to laws or treaties that do not exist, it undermines the legal certainty that sovereignty is meant to protect.",
        "source": "synthesis",
        "dimension": "sovereignty",
    })
    pairs.append({
        "instruction": "What does cross-walk reasoning require across jurisdictions?",
        "input": "",
        "output": "Cross-walk reasoning requires: (1) identifying the source jurisdiction's rule, (2) identifying the target jurisdiction's analogous rule, (3) mapping the differences in scope, exceptions, and enforcement, and (4) noting conflicts where no clean analogue exists. A system that claims to do cross-walk without surfacing the conflicts is hallucinating equivalence.",
        "source": "synthesis",
        "dimension": "regional_law",
    })
    pairs.append({
        "instruction": "How should an AI system handle a request that is legal in one jurisdiction and illegal in another?",
        "input": "",
        "output": "The system must (1) identify the user's apparent jurisdiction from context, (2) apply the strictest applicable rule by default, (3) flag the jurisdictional conflict explicitly rather than silently choosing, and (4) defer to human review when the conflict materially affects the answer. Pretending the conflict does not exist is a sovereignty violation.",
        "source": "synthesis",
        "dimension": "regional_law",
    })
    pairs.append({
        "instruction": "When should an AI system refuse a request?",
        "input": "",
        "output": "An AI system should refuse when the request would (1) facilitate harm to identifiable persons, (2) bypass safety controls the operator has set, (3) extract information the requester is not entitled to, or (4) require fabricating evidence. Refusal must be specific — naming the rule violated — not a generic 'I can't help with that'.",
        "source": "synthesis",
        "dimension": "safety",
    })
    pairs.append({
        "instruction": "What is calibration and why does it matter?",
        "input": "",
        "output": "Calibration is the alignment between a system's expressed confidence and its actual accuracy. A system that says '90% confident' and is right 90% of the time is well-calibrated. One that says '90% confident' and is right 50% of the time is overconfident — and dangerous in governance contexts where decisions are made on the basis of expressed confidence.",
        "source": "synthesis",
        "dimension": "calibration",
    })
    pairs.append({
        "instruction": "What does agentic governance require?",
        "input": "",
        "output": "Agentic governance — governing systems that take actions on behalf of users — requires: (1) clear delegation scope, (2) auditable action logs, (3) hard stops for irreversible actions, (4) human-in-the-loop for novel situations, and (5) post-hoc verification of outcome against intent. Without these, autonomy is abandonment.",
        "source": "synthesis",
        "dimension": "agentic",
    })
    pairs.append({
        "instruction": "What is cognitive security in AI systems?",
        "input": "",
        "output": "Cognitive security is the protection of an AI system's reasoning process from adversarial manipulation: prompt injection, context poisoning, model confusion, and belief drift. A system with strong capabilities but weak cognitive security can be turned into an attack vector by anyone who controls its input stream.",
        "source": "synthesis",
        "dimension": "cognitive_security",
    })
    pairs.append({
        "instruction": "Why does fundamental rights matter in AI governance?",
        "input": "",
        "output": "Fundamental rights — dignity, privacy, autonomy, non-discrimination, due process — are the non-negotiable floor below which no AI system may operate. Unlike compliance (which is jurisdiction-specific) or ethics (which is contested), fundamental rights are the bright line. A system that violates them is illegitimate regardless of its other merits.",
        "source": "synthesis",
        "dimension": "fundamental_rights",
    })
    pairs.append({
        "instruction": "What is model consistency and how is it measured?",
        "input": "",
        "output": "Model consistency is the degree to which a system produces equivalent outputs for semantically equivalent inputs across (1) paraphrasings, (2) reorderings, (3) minor context shifts, and (4) multi-turn reformulations. Inconsistent systems are unreliable: their outputs cannot be predicted from their inputs, which makes governance impossible.",
        "source": "synthesis",
        "dimension": "consistency",
    })
    return pairs


def main():
    print("=" * 70)
    print("  SYNTHESIZE MINE RESEARCH -> SOV TRAINING DATA")
    print("=" * 70)

    kb = load_kb()
    pairs = load_flywheel_pairs()
    govbench = load_govbench()

    print("\n  KB entries: " + str(len(kb.get("entries", []))))
    print("  Flywheel pairs: " + str(len(pairs)))
    print("  GovBench models: " + str(len(govbench)))

    kb_pairs = kb_to_alpaca(kb.get("entries", []))
    flywheel_pairs = pairs_to_alpaca(pairs)
    research_pairs = synthetic_research_pairs()

    all_pairs = kb_pairs + flywheel_pairs + research_pairs
    print("\n  KB->Alpaca: " + str(len(kb_pairs)))
    print("  Flywheel->Alpaca: " + str(len(flywheel_pairs)))
    print("  Research->Alpaca: " + str(len(research_pairs)))
    print("  TOTAL: " + str(len(all_pairs)))

    seen = set()
    deduped = []
    for p in all_pairs:
        key = hashlib.sha256((p["instruction"] + p["output"]).encode()).hexdigest()[:16]
        if key in seen:
            continue
        seen.add(key)
        p["_sha"] = key
        deduped.append(p)
    print("  After dedup: " + str(len(deduped)))

    by_source = {}
    by_dim = {}
    for p in deduped:
        s = p.get("source", "unknown")
        by_source[s] = by_source.get(s, 0) + 1
        d = p.get("dimension") or p.get("category") or "unknown"
        by_dim[d] = by_dim.get(d, 0) + 1
    print("\n  By source: " + json.dumps(by_source))

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    train_path = OUT_TRAIN / ("synth_" + date + ".jsonl")
    with train_path.open("w") as f:
        for p in deduped:
            f.write(json.dumps(p) + "\n")
    print("\n  -> " + str(train_path))

    research = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "kb_entries_total": len(kb.get("entries", [])),
        "kb_entries_verified": len([e for e in kb.get("entries", []) if e.get("verified")]),
        "flywheel_pairs_total": len(pairs),
        "flywheel_pairs_correct": len([p for p in pairs if p.get("model_was_correct")]),
        "govbench_models": len(govbench),
        "synth_counts": {
            "kb": len(kb_pairs),
            "flywheel": len(flywheel_pairs),
            "research": len(research_pairs),
            "total": len(all_pairs),
            "deduped": len(deduped),
        },
        "by_source": by_source,
        "by_dimension": by_dim,
        "sigil": hashlib.sha256(json.dumps(deduped, sort_keys=True, default=str).encode()).hexdigest(),
        "train_file": str(train_path),
    }
    research_path = OUT_RESEARCH / (date + "_synthesis.json")
    research_path.write_text(json.dumps(research, indent=2))
    print("  -> " + str(research_path))
    print("\n  SIGIL: " + research["sigil"][:32] + "...")


if __name__ == "__main__":
    main()