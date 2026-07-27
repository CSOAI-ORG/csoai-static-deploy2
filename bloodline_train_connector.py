#!/usr/bin/env python3
"""Convert bloodline + EAT knowledge into ASI-Evolve training JSONL files."""

import json
import os
import re

BLOODLINE_PATH = "eat_results/bloodline.json"
EAT_PATH = "eat_results/eat_mac_all.json"
OUT_DIR = "benchmark-results"
BLOODLINE_OUT = os.path.join(OUT_DIR, "sovereign_synth_50k.jsonl")
EAT_OUT = os.path.join(OUT_DIR, "sov5_training_dataset.jsonl")
COMBINED_OUT = os.path.join(OUT_DIR, "sovereign_corpus_e2e.jsonl")

INSTRUCTION_TEMPLATES = [
    "Explain {topic} in detail.",
    "What do you know about {topic}?",
    "Describe the key aspects of {topic}.",
    "Provide a thorough overview of {topic}.",
    "Summarize your understanding of {topic}.",
    "What are the main characteristics of {topic}?",
    "Tell me about {topic}.",
    "Can you elaborate on {topic}?",
    "Give me a comprehensive analysis of {topic}.",
    "Discuss {topic} in depth.",
    "What is {topic}?",
    "Explain the significance of {topic}.",
    "What can you tell me about {topic}?",
    "Describe {topic} from first principles.",
    "Break down {topic} for me.",
]

DECLINED_RESPONSES = {
    "i'm sorry, but i can't assist with that",
    "i'm sorry, but i can't assist with that request",
    "i'm sorry, but i can't assist with that.",
    "sorry, but i can't assist with that",
    "sorry, i don't know",
    "i cannot answer",
    "i'm not able to answer",
    "i'm sorry, but i can't help",
}


def _is_declined(text: str) -> bool:
    t = text.strip().lower()
    for d in DECLINED_RESPONSES:
        if t.startswith(d):
            return True
    return False


def parse_qa_blocks(content: str):
    pairs = []
    pattern = re.compile(r"Q:\s*(.*?)\nA:\s*(.*?)(?=\nQ:|\Z)", re.DOTALL)
    for m in pattern.finditer(content):
        q = m.group(1).strip()
        a = m.group(2).strip()
        if q and a and not _is_declined(a):
            pairs.append((q, a))
    return pairs


def extract_topic(q: str) -> str:
    q = re.sub(r"^\?(?:s|es)?\s*", "", q, flags=re.IGNORECASE)
    q = re.sub(r"\s*\?$", "", q)
    return q.strip()[:80]


def domain_for_family(family: str) -> str:
    mapping = {
        "qwen": "llm", "deepseek": "llm", "llama": "llm", "mistral": "llm",
        "phi": "llm", "gemma": "llm", "gpt-oss": "llm", "nemotron": "llm",
        "MiniMax": "llm",
        "code": "code", "vision": "vision", "qwen-vision": "vision",
        "embedding": "embedding", "core": "governance",
    }
    return mapping.get(family, "general")


def generate_bloodline_entries():
    with open(BLOODLINE_PATH) as f:
        data = json.load(f)

    entries = []
    families_seen = set()
    for item in data["knowledge"]:
        family = item["family"]
        families_seen.add(family)
        pairs = parse_qa_blocks(item["content"])
        for q, a in pairs:
            topic = extract_topic(q)
            domain = domain_for_family(family)
            for tmpl in INSTRUCTION_TEMPLATES:
                instruction = tmpl.format(topic=topic)
                entries.append({
                    "system": "You are a sovereign AI assistant with deep knowledge of the AI ecosystem.",
                    "instruction": instruction,
                    "input": "",
                    "output": a,
                    "domain": domain,
                    "family": family,
                    "source": "bloodline",
                })
    return entries, families_seen


def generate_eat_entries():
    with open(EAT_PATH) as f:
        data = json.load(f)

    entries = []
    families_seen = set()
    for item in data:
        family = item["family"]
        families_seen.add(family)
        q = item["q"].strip()
        a = item["a"].strip()
        if not q or not a:
            continue
        if _is_declined(a):
            continue
        topic = extract_topic(q)
        domain = domain_for_family(family)
        for tmpl in INSTRUCTION_TEMPLATES:
            instruction = tmpl.format(topic=topic)
            entries.append({
                "system": "You are a sovereign AI assistant with deep knowledge of the AI ecosystem.",
                "instruction": instruction,
                "input": "",
                "output": a,
                "domain": domain,
                "family": family,
                "source": "eat",
            })
    return entries, families_seen


def write_jsonl(path, entries):
    with open(path, "w") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def summarize(label, path, entries, families):
    domains = set(e["domain"] for e in entries)
    print(f"  {label}:")
    print(f"    Path: {path}")
    print(f"    Entries: {len(entries)}")
    print(f"    Domains ({len(domains)}): {sorted(domains)}")
    print(f"    Families ({len(families)}): {sorted(families)}")
    print()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("=" * 60)
    print("Bloodline Training Data Connector")
    print("=" * 60)
    print()

    blood_entries, blood_fams = generate_bloodline_entries()
    eat_entries, eat_fams = generate_eat_entries()
    combined = blood_entries + eat_entries
    all_fams = blood_fams | eat_fams

    write_jsonl(BLOODLINE_OUT, blood_entries)
    write_jsonl(EAT_OUT, eat_entries)
    write_jsonl(COMBINED_OUT, combined)

    print("Summary")
    print("-" * 60)
    summarize("sovereign_synth_50k.jsonl (bloodline)", BLOODLINE_OUT, blood_entries, blood_fams)
    summarize("sov5_training_dataset.jsonl (EAT)", EAT_OUT, eat_entries, eat_fams)
    summarize("sovereign_corpus_e2e.jsonl (combined)", COMBINED_OUT, combined, all_fams)


if __name__ == "__main__":
    main()
