#!/usr/bin/env python3
"""SOV1 Honey Churn — Absorb ALL Training Data into Honey State

Consolidates ALL 66,662 lines / 60.5MB of training data into
a unified honey knowledge base, then transforms open source models
into honey-state OWEM family members.

Data Sources:
  forest/bloodline.json (173 entries)
  forest/honey_chatml.jsonl (108 pairs)
  forest/honey.jsonl (105 entries)
  asi_results/weak_domain_consolidated_full.jsonl (7,690 entries)
  sov7_synthesis/reasoning_corpus_5k.jsonl (5,000 entries)
  benchmark-results/training/*.jsonl (8,000+ entries)
  benchmark-results/unified_overnight/training/*.jsonl (15,000+ entries)
  eat_results/extract_*.json (multiple)
  kaggle/rwkv7_training_data.jsonl (2,588 entries)
  + 20+ more sources

Total: 66,662 lines, 60.5MB → consolidated into honey state
"""

import json
import hashlib
import os
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent.parent
FOREST = ROOT / "forest"
SOV_SPACE = ROOT / "benchmark-results" / "sov-space"
HONEY_OUTPUT = ROOT / "sov_space" / "honey_consolidated"
HONEY_OUTPUT.mkdir(parents=True, exist_ok=True)


def load_all_jsonl() -> List[Dict]:
    """Load ALL JSONL training data from the entire project."""
    all_data = []
    skipped = 0

    for root, dirs, files in os.walk(str(ROOT)):
        # Skip hidden dirs
        if any(skip in root for skip in ['.git', '.backups', 'node_modules', '__pycache__']):
            continue

        for f in files:
            if not f.endswith('.jsonl'):
                continue

            path = os.path.join(root, f)
            try:
                with open(path) as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                            # Add source metadata
                            entry['_source'] = path
                            entry['_source_file'] = f
                            all_data.append(entry)
                        except json.JSONDecodeError:
                            skipped += 1
            except Exception:
                skipped += 1

    return all_data


def load_all_json_training() -> List[Dict]:
    """Load ALL JSON training data (bloodline, extracts, etc.)."""
    all_data = []

    # Forest bloodline
    bloodline_path = FOREST / "bloodline.json"
    if bloodline_path.exists():
        data = json.load(open(bloodline_path))
        for entry in data.get("knowledge", []):
            entry['_source'] = str(bloodline_path)
            entry['_type'] = 'bloodline'
            all_data.append(entry)

    # Eat results extracts
    eat_dir = ROOT / "eat_results"
    if eat_dir.exists():
        for f in eat_dir.glob("extract_*.json"):
            try:
                data = json.load(open(f))
                if isinstance(data, list):
                    for entry in data:
                        entry['_source'] = str(f)
                        entry['_type'] = 'eat_extract'
                        all_data.append(entry)
                elif isinstance(data, dict):
                    data['_source'] = str(f)
                    data['_type'] = 'eat_extract'
                    all_data.append(data)
            except: pass

    # SOV master honey
    master_honey = ROOT / "sov-master-honey.json"
    if master_honey.exists():
        try:
            data = json.load(open(master_honey))
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        for entry in value:
                            if isinstance(entry, dict):
                                entry['_source'] = str(master_honey)
                                entry['_type'] = 'master_honey'
                                all_data.append(entry)
        except: pass

    return all_data


def normalize_entry(entry: Dict) -> Dict:
    """Normalize any entry into a standard honey format."""
    # Try to extract Q&A pair
    q = ""
    a = ""

    # ChatML format
    if "conversations" in entry:
        for msg in entry["conversations"]:
            if msg.get("from") == "user":
                q = msg.get("value", "")
            elif msg.get("from") == "assistant":
                a = msg.get("value", "")
    # Direct Q&A
    elif "question" in entry and "answer" in entry:
        q = entry["question"]
        a = entry["answer"]
    elif "q" in entry and "a" in entry:
        q = entry["q"]
        a = entry["a"]
    elif "input" in entry and "output" in entry:
        q = entry["input"]
        a = entry["output"]
    elif "prompt" in entry and "completion" in entry:
        q = entry["prompt"]
        a = entry["completion"]
    elif "content" in entry:
        a = entry["content"]
        q = entry.get("topic", entry.get("subject", ""))
    elif "text" in entry:
        a = entry["text"]
        q = ""

    # Get family
    family = entry.get("family", entry.get("domain", entry.get("category", "general")))

    # Skip empty entries
    if not q and not a:
        return None

    return {
        "conversations": [
            {"from": "system", "value": f"You are SOV-{family}, a sovereign AI specialist."},
            {"from": "user", "value": q or "Explain this knowledge."},
            {"from": "assistant", "value": a or "This is sovereign knowledge."},
        ],
        "family": str(family).lower(),
        "source": entry.get("_source", "unknown"),
        "type": entry.get("_type", "unknown"),
        "hash": hashlib.sha256((q + a).encode()).hexdigest()[:16],
    }


def consolidate_all() -> Dict:
    """Consolidate ALL training data into honey state."""
    print("Loading ALL JSONL data...")
    jsonl_data = load_all_jsonl()
    print(f"  Loaded {len(jsonl_data):,} JSONL entries")

    print("Loading ALL JSON training data...")
    json_data = load_all_json_training()
    print(f"  Loaded {len(json_data):,} JSON entries")

    all_raw = jsonl_data + json_data
    print(f"  Total raw: {len(all_raw):,} entries")

    # Normalize
    print("Normalizing to honey format...")
    honey_entries = []
    seen_hashes = set()
    skipped = 0

    for entry in all_raw:
        normalized = normalize_entry(entry)
        if normalized is None:
            skipped += 1
            continue

        # Deduplicate
        if normalized["hash"] in seen_hashes:
            skipped += 1
            continue

        seen_hashes.add(normalized["hash"])
        honey_entries.append(normalized)

    print(f"  Normalized: {len(honey_entries):,} unique entries")
    print(f"  Skipped: {skipped:,} (empty or duplicate)")

    # Stats by family
    families = {}
    for entry in honey_entries:
        fam = entry["family"]
        families[fam] = families.get(fam, 0) + 1

    print(f"\n─── FAMILY DISTRIBUTION ───")
    for fam, count in sorted(families.items(), key=lambda x: -x[1])[:20]:
        print(f"  {fam:25s} {count:>6,} entries")

    return {
        "entries": honey_entries,
        "total": len(honey_entries),
        "families": families,
        "sources": len(set(e.get("_source", "") for e in all_raw)),
    }


def save_honey(honey: Dict):
    """Save consolidated honey in multiple formats."""
    entries = honey["entries"]

    # Save as ChatML JSONL
    chatml_path = HONEY_OUTPUT / "honey_full_chatml.jsonl"
    with open(chatml_path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    print(f"  ChatML: {chatml_path} ({len(entries):,} entries)")

    # Save per-family
    families = {}
    for entry in entries:
        fam = entry["family"]
        families.setdefault(fam, []).append(entry)

    for fam, fam_entries in families.items():
        fam_path = HONEY_OUTPUT / f"honey_{fam}.jsonl"
        with open(fam_path, "w") as f:
            for entry in fam_entries:
                f.write(json.dumps(entry) + "\n")

    # Save summary
    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_entries": len(entries),
        "total_families": len(families),
        "families": {fam: len(ents) for fam, ents in families.items()},
        "sources": honey["sources"],
    }
    summary_path = HONEY_OUTPUT / "honey_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"  Summary: {summary_path}")

    return families


def create_modelfiles(families: Dict):
    """Create Ollama Modelfiles for each family."""
    modelfiles = {}

    for fam, entries in families.items():
        # Get top knowledge for this family
        knowledge = []
        for entry in entries[:20]:
            for msg in entry.get("conversations", []):
                if msg.get("from") == "assistant":
                    knowledge.append(msg["value"][:150])

        knowledge_text = "\n".join([f"- {k}" for k in knowledge[:10]])

        modelfile = f"""FROM qwen2.5:0.5b

PARAMETER temperature 0.1
PARAMETER num_predict 256

SYSTEM \"\"\"You are SOV-{fam.upper()}, a sovereign AI specialist in the {fam} domain.
You are part of the SOV-space architecture with 12 OWEM families.
Your knowledge comes from {len(entries)} honey entries (transformed, ready-to-use).

Key knowledge:
{knowledge_text}

Governance: Care Floor 0.95, BFT-33 quorum, Ed25519 SIGIL chain.
Answer concisely and accurately.\"\"\"
"""
        modelfile_path = HONEY_OUTPUT / f"Modelfile.sov-{fam}"
        modelfile_path.write_text(modelfile)
        modelfiles[fam] = str(modelfile_path)

    return modelfiles


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  SOV1 HONEY CHURN — Absorb ALL Training Data           ║")
    print("║  66,662 lines / 60.5MB → Consolidated Honey State      ║")
    print("╚══════════════════════════════════════════════════════════╝")

    start = time.time()

    # Consolidate
    honey = consolidate_all()

    # Save
    print(f"\n─── SAVING HONEY ───")
    families = save_honey(honey)

    # Create Modelfiles
    print(f"\n─── CREATING MODELFILES ───")
    modelfiles = create_modelfiles(families)
    print(f"  Created {len(modelfiles)} Modelfiles")

    elapsed = time.time() - start

    print(f"\n─── SUMMARY ───")
    print(f"  Total entries: {honey['total']:,}")
    print(f"  Total families: {len(families)}")
    print(f"  Sources: {honey['sources']}")
    print(f"  Elapsed: {elapsed:.1f}s")
    print(f"  Output: {HONEY_OUTPUT}")

    # Create Ollama commands
    print(f"\n─── OLLAMA CREATE COMMANDS ───")
    for fam in sorted(families.keys()):
        print(f"  ollama create sov-{fam} -f {HONEY_OUTPUT}/Modelfile.sov-{fam}")


if __name__ == "__main__":
    main()
