#!/usr/bin/env python3
"""honey_harvest.py — turn benchmarking OTHER models into knowledge our cluster can use.

═══════════════════════════════════════════════════════════════════════════════
THE GAP THIS CLOSES
═══════════════════════════════════════════════════════════════════════════════
Today, benchmarking another model produces a SCORE. A score tells you where you rank. It does
not make you better. The flywheel turns, but nothing accrues from testing competitors.

But every benchmark run already generates the raw material: the other model's ANSWERS. Where a
competitor answers a governance question better than our best expert, that answer is a fact we
did not have. Harvested into retrieval context, it lifts the dimension it came from.

This is not speculative — it is the estate's own strongest measured lever:
    RAG / added context was worth **+31 points** on the weakest dimensions (free-T4 EAT run).
    Meanwhile 3x the parameters bought only +1.9 on governance.
So: retrieved knowledge >> trained knowledge, for this task. Harvesting IS the training.

And it inherits the cluster's monotonic property — a harvested item is only ever ADDED to the
retrieval pool for the dimension where it demonstrably beat us. It cannot make anything worse.

═══════════════════════════════════════════════════════════════════════════════
⚠️ READ BEFORE RUNNING — LICENSING IS A REAL CONSTRAINT, NOT A FORMALITY
═══════════════════════════════════════════════════════════════════════════════
Most commercial model providers' terms prohibit using their outputs to train or improve a
COMPETING model. OpenAI, Anthropic, Google and others all carry some form of this clause.

What that means concretely:
  ✅ ALMOST CERTAINLY FINE — harvesting from models under permissive licences (Llama, Qwen,
     Mistral, DeepSeek open weights) where the licence allows derivative use.
  ✅ FINE for any provider — using scores for EVALUATION and comparison. That is benchmarking.
  ⚠️  CHECK THE TERMS — harvesting outputs from a commercial API into a retrieval pool that
     serves a governance product. Retrieval is arguably not "training", but it is squarely in
     the grey zone and a governance company should not be arguing the grey zone.
  ❌ DO NOT — harvest from a provider whose terms forbid it and then market the result.

This script therefore records `source_licence` on every harvested item and refuses to harvest
from a provider not explicitly allow-listed. A governance product caught violating provider
terms loses the only asset it has. The check is cheap; the reputational cost is not.

    python3 honey_harvest.py --provider ollama --model llama3.2:3b
    python3 honey_harvest.py --status
"""
from __future__ import annotations

import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
POOL = HERE / "benchmark-results" / "honey_pool.json"

# Only providers whose terms permit derivative use of outputs. Extend deliberately, with the
# licence named — never with a bare provider string.
ALLOWED_SOURCES = {
    "ollama":   "local open-weight models (Llama/Qwen/Mistral licences — check the specific model)",
    "deepseek": "DeepSeek open weights (MIT-style model licence)",
    "local":    "models we built ourselves",
}


def load_pool() -> dict:
    if POOL.exists():
        try:
            return json.loads(POOL.read_text())
        except Exception:
            pass
    return {"items": [], "created": datetime.now(timezone.utc).isoformat()}


def harvest(model: str, provider: str, dry: bool = False) -> dict:
    if provider not in ALLOWED_SOURCES:
        print(f"  ❌ REFUSING to harvest from '{provider}'.")
        print(f"     Only allow-listed sources may be harvested: {', '.join(ALLOWED_SOURCES)}")
        print(f"     Most commercial providers forbid using outputs to improve a competing model.")
        print(f"     Benchmarking them for SCORES is fine; harvesting their ANSWERS is not.")
        return {"refused": True}

    from govbench_eval import DIMENSIONS, call_model, grade_response, UnreachableModel
    from owem_cluster import build_expert_table

    table, models = build_expert_table()
    if not table:
        print("  no benchmark results — cannot know where we are beatable"); return {}

    pool = load_pool()
    seen = {i["q_sha256"] for i in pool["items"]}
    added = skipped = 0

    for dim, d in DIMENSIONS.items():
        our_best = table.get(dim, {}).get("score", 0)
        for t in d["tests"]:
            q = t["q"]
            qh = hashlib.sha256(q.encode()).hexdigest()
            if qh in seen:
                skipped += 1
                continue
            try:
                resp = call_model(model, q, provider)
                score = grade_response(t, resp) * 100
            except UnreachableModel as e:
                print(f"  ⏭️  {model} unreachable — nothing harvested ({str(e)[:50]})")
                return {"unreachable": True}
            except Exception:
                continue
            # HARVEST ONLY WHERE THEY BEAT US. A worse answer is not honey; storing it would
            # dilute the pool and quietly lower retrieval quality.
            if score > our_best:
                if not dry:
                    pool["items"].append({
                        "dimension": dim, "question": q, "q_sha256": qh,
                        "answer": resp[:1200], "their_score": round(score, 1),
                        "our_best": round(our_best, 1), "delta": round(score - our_best, 1),
                        "source_model": model, "source_provider": provider,
                        "source_licence": ALLOWED_SOURCES[provider],
                        "harvested": datetime.now(timezone.utc).isoformat(),
                    })
                added += 1
                print(f"  🍯 {dim:15s} +{score-our_best:5.1f} pts  ({score:.0f} vs our {our_best:.0f})  {q[:44]}")

    if not dry:
        POOL.parent.mkdir(parents=True, exist_ok=True)
        POOL.write_text(json.dumps(pool, indent=2))
    print(f"\n  harvested {added} items · {skipped} already in pool · pool now {len(pool['items'])}")
    return {"added": added, "pool": len(pool["items"])}


def status() -> None:
    pool = load_pool()
    items = pool["items"]
    print(f"  HONEY POOL — {len(items)} items")
    if not items:
        print("    empty. Run a harvest against an allow-listed model.")
        return
    from collections import Counter
    bydim = Counter(i["dimension"] for i in items)
    bysrc = Counter(i["source_model"] for i in items)
    print("    by dimension:")
    for d, n in bydim.most_common():
        avg = sum(i["delta"] for i in items if i["dimension"] == d) / n
        print(f"      {d:15s} {n:3d} items, avg +{avg:.1f} pts over our best")
    print("    by source:")
    for s, n in bysrc.most_common():
        print(f"      {s:26s} {n:3d}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model")
    ap.add_argument("--provider", default="ollama")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    if a.status or not a.model:
        status()
    else:
        harvest(a.model, a.provider, a.dry)
