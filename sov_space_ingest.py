#!/usr/bin/env python3
"""sov_space_ingest.py — convert open datasets into SOV-space as RETRIEVAL, not training.

═══════════════════════════════════════════════════════════════════════════════
THE THREE TIERS — these are different mechanisms and conflating them wastes months
═══════════════════════════════════════════════════════════════════════════════
| tier      | what it changes        | cost                | ceiling                |
|-----------|------------------------|---------------------|------------------------|
| DRAWING   | what the model         | **16 KB**, instant  | can only reweight what |
|           | foregrounds            | no GPU              | the weights already know|
| RETRIEVAL | what the model can     | corpus size only    | limited by context     |
|           | SEE at answer time     | no GPU              | window and recall      |
| TRAINING  | the weights themselves | GPU-hours           | **~8B on 16GB free**   |

A drawing cannot add knowledge the base does not have — it can only change emphasis. That is
why drawings alone plateau. Retrieval is what actually ADDS knowledge, and on this estate's own
measurement it is the strongest lever available:

    added context     = **+31 points** on the weakest dimensions
    3x the parameters = **+1.9 points** on governance

So "consume all knowledge" is a RETRIEVAL problem, not a training problem — and that is the
fortunate answer, because retrieval needs no GPU and has no 8B ceiling.

**Training a dataset in changes one model. Indexing a dataset makes it available to EVERY
expert on the substrate at once.** With 16KB drawings sharing one blob, the retrieval corpus is
shared too — one ingest lifts the whole cluster.

═══════════════════════════════════════════════════════════════════════════════
⚠️ WHERE MONOTONICITY STOPS — the one thing not to over-extend
═══════════════════════════════════════════════════════════════════════════════
Composition is monotonic WITHIN a dimension: max-selection means a new expert can only add.
That does NOT extend across the pipeline. The path is

    OWM perception  ->  IWM reasoning  ->  answer

and a perfect IWM cannot repair a misrouted OWM. **The delivered score is bounded by the
WEAKEST layer in the path, not by the max of each.** Spine accuracy is 0.387 — so today the
pipeline is bounded by perception, and adding more experts raises a ceiling the router cannot
reach. Fix routing before scaling the expert pool; otherwise thousands of drawings buy nothing.

Same caution for retrieval: a corpus only helps if the right chunk is RETRIEVED. Bad recall
makes a bigger corpus worse, not better — more to miss, more to distract.

    python3 sov_space_ingest.py --status
    python3 sov_space_ingest.py --ingest path/to/corpus.jsonl --dimension compliance
"""
from __future__ import annotations

import argparse, hashlib, json, re, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
CORPUS = HERE / "benchmark-results" / "sov_space_corpus.jsonl"

# Datasets whose licence permits derivative/commercial use. Named explicitly for the same reason
# the honey harvester allow-lists providers: a governance product cannot be the one caught
# arguing licence terms.
KNOWN_OPEN = {
    "eurlex":        "EU law — Official Journal, public domain (© EU, reuse permitted)",
    "nist":          "NIST publications — US Government work, public domain",
    "iso-summary":   "ONLY summaries/citations. ISO standards themselves are COPYRIGHTED — do "
                     "not ingest their text.",
    "cc-by":         "Creative Commons BY — attribution required, recorded per chunk",
    "apache-2.0":    "Apache 2.0 datasets",
    "mit":           "MIT-licensed datasets",
    "public-domain": "Public domain",
}


def _chunks(text: str, size: int = 900, overlap: int = 120):
    """Sentence-aware chunking. Splitting mid-sentence produces chunks that retrieve well and
    read badly — the model then cites a fragment that says something the source did not."""
    sents = re.split(r"(?<=[.!?])\s+", text)
    buf, out = "", []
    for s in sents:
        if len(buf) + len(s) > size and buf:
            out.append(buf.strip())
            buf = buf[-overlap:] + " " + s
        else:
            buf += " " + s
    if buf.strip():
        out.append(buf.strip())
    return out


def ingest(path: Path, dimension: str, licence: str, source: str, dry: bool = False) -> dict:
    if licence not in KNOWN_OPEN:
        print(f"  ❌ REFUSING — licence '{licence}' not in the open allow-list.")
        print(f"     Permitted: {', '.join(KNOWN_OPEN)}")
        print(f"     Ingesting copyrighted text into a shipping product is not a grey area.")
        return {"refused": True}

    if not path.exists():
        print(f"  ❌ not found: {path}"); return {}

    seen = set()
    if CORPUS.exists():
        with CORPUS.open() as f:
            for line in f:
                if line.strip():
                    try:
                        seen.add(json.loads(line)["sha256"])
                    except Exception:
                        pass

    added = dup = 0
    out = []
    raw = path.read_text(errors="replace")
    docs = []
    if path.suffix == ".jsonl":
        for line in raw.splitlines():
            if not line.strip():
                continue
            try:
                d = json.loads(line)
                docs.append(d.get("text") or d.get("content") or json.dumps(d))
            except Exception:
                docs.append(line)
    else:
        docs = [raw]

    for doc in docs:
        for ch in _chunks(doc):
            h = hashlib.sha256(ch.encode()).hexdigest()
            if h in seen:
                dup += 1
                continue
            seen.add(h)
            out.append({"text": ch, "sha256": h, "dimension": dimension,
                        "source": source, "licence": licence,
                        "licence_note": KNOWN_OPEN[licence],
                        "ingested": datetime.now(timezone.utc).isoformat()})
            added += 1

    if not dry and out:
        CORPUS.parent.mkdir(parents=True, exist_ok=True)
        with CORPUS.open("a") as f:
            for o in out:
                f.write(json.dumps(o, ensure_ascii=False) + "\n")

    print(f"  {'(dry) ' if dry else ''}ingested {added} chunks · {dup} duplicates skipped")
    print(f"  dimension={dimension} licence={licence}")
    print(f"  Every chunk carries its licence — provenance is per-chunk, not per-corpus,")
    print(f"  so a single bad source can be removed without rebuilding everything.")
    return {"added": added, "duplicates": dup}


def status() -> None:
    if not CORPUS.exists():
        print("  SOV-SPACE CORPUS — empty\n")
        print("  Nothing ingested yet. The mechanism is built; the corpus is not.")
        print("  Do NOT claim knowledge coverage until this has content.")
        return
    dims, srcs, lics = Counter(), Counter(), Counter()
    n = chars = 0
    with CORPUS.open() as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line); n += 1; chars += len(d["text"])
            dims[d["dimension"]] += 1; srcs[d["source"]] += 1; lics[d["licence"]] += 1
    print(f"  SOV-SPACE CORPUS — {n} chunks · {chars/1e6:.2f}M chars\n")
    print("  by dimension:"); [print(f"    {k:15s} {v}") for k, v in dims.most_common()]
    print("  by licence:");   [print(f"    {k:15s} {v}") for k, v in lics.most_common()]
    print(f"\n  ⚠️  A corpus only helps if the right chunk is RETRIEVED. Recall is not yet")
    print(f"     measured — until it is, corpus size is not evidence of capability.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ingest")
    ap.add_argument("--dimension", default="governance")
    ap.add_argument("--licence", default="public-domain")
    ap.add_argument("--source", default="unknown")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    if a.ingest:
        ingest(Path(a.ingest), a.dimension, a.licence, a.source, a.dry)
    else:
        status()
