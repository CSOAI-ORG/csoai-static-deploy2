#!/usr/bin/env python3
"""prepare_training_data.py — Convert honey_full_chatml.jsonl to training formats.

Outputs:
  1. honey_mistral.jsonl — Mistral [INST] format for LoRA training
  2. honey_qa.jsonl — Simple {q, a} format
  3. honey_sharegpt.jsonl — ShareGPT format for various trainers
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
INPUT = ROOT / "sov_space" / "honey_consolidated" / "honey_full_chatml.jsonl"
OUT_DIR = ROOT / "training_data"
OUT_DIR.mkdir(exist_ok=True)


def load_conversations():
    records = []
    with open(INPUT) as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except:
                continue
    return records


def to_mistral_format(records):
    """Convert to Mistral [INST] format."""
    out = []
    for rec in records:
        convs = rec.get("conversations", [])
        system = ""
        user_msg = ""
        assistant_msg = ""
        for c in convs:
            if c["from"] == "system":
                system = c["value"]
            elif c["from"] == "user":
                user_msg = c["value"]
            elif c["from"] == "assistant":
                assistant_msg = c["value"]
        if user_msg and assistant_msg:
            if system:
                user_msg = f"{system}\n\n{user_msg}"
            out.append({"q": user_msg, "a": assistant_msg})
    return out


def to_sharegpt(records):
    """Convert to ShareGPT format."""
    out = []
    for rec in records:
        convs = rec.get("conversations", [])
        sg_convs = []
        for c in convs:
            role = "gpt" if c["from"] == "assistant" else c["from"]
            sg_convs.append({"from": role, "value": c["value"]})
        if sg_convs:
            out.append({"conversations": sg_convs})
    return out


def main():
    print(f"Loading from {INPUT}")
    records = load_conversations()
    print(f"Loaded {len(records)} records")

    # Deduplicate by hash
    seen = set()
    deduped = []
    for r in records:
        h = r.get("hash", "")
        if h and h in seen:
            continue
        seen.add(h)
        deduped.append(r)
    print(f"After dedup: {len(deduped)} records")

    # Mistral format
    mistral = to_mistral_format(deduped)
    mistral_path = OUT_DIR / "honey_mistral.jsonl"
    with open(mistral_path, "w") as f:
        for r in mistral:
            f.write(json.dumps(r) + "\n")
    print(f"Wrote {len(mistral)} -> {mistral_path}")

    # ShareGPT format
    sharegpt = to_sharegpt(deduped)
    sharegpt_path = OUT_DIR / "honey_sharegpt.jsonl"
    with open(sharegpt_path, "w") as f:
        for r in sharegpt:
            f.write(json.dumps(r) + "\n")
    print(f"Wrote {len(sharegpt)} -> {sharegpt_path}")

    # Simple QA format
    qa_path = OUT_DIR / "honey_qa.jsonl"
    with open(qa_path, "w") as f:
        for r in mistral:
            f.write(json.dumps({"prompt": r["q"], "completion": r["a"]}) + "\n")
    print(f"Wrote {len(mistral)} -> {qa_path}")

    # Stats
    families = {}
    for r in deduped:
        fam = r.get("family", "unknown")
        families[fam] = families.get(fam, 0) + 1
    print(f"\nFamily breakdown ({len(families)} families):")
    for fam, count in sorted(families.items(), key=lambda x: -x[1]):
        print(f"  {fam}: {count}")

    print(f"\nDone! Files in {OUT_DIR}")


if __name__ == "__main__":
    main()
