#!/usr/bin/env python3
"""kb_to_sovspace_honey.py — convert SovSpace KB stamps into NN/GNN training honey.

Pipeline (per sov_mind.py architecture):
  KB entries (verified)
    → Phlabet compression (256-symbol symbolic compression)
    → Spine reasoning (10-layer MPNN/GNN message passing)
    → Honey generation (new training pairs for NN/GNN/quantised models)
    → write to benchmark-results/honey_from_kb.jsonl

The "all learning NN GNN" loop: KB → SovSpace stamps (cspace glyphs) → Phlabet
→ Spine reasoning → honey → training data → fine-tuned NN/GNN → model output →
new KB → SovSpace stamps → ... self-improving.

Usage:
  python3 kb_to_sovspace_honey.py            # convert all unstamped KB entries
  python3 kb_to_sovspace_honey.py --limit 20 # convert first 20
  python3 kb_to_sovspace_honey.py --dry      # show what would be generated
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

# Reuse the canonical SOV substrate from sov_mind.py
HERE_DEPLOY = Path.home() / "clawd" / "csoai-static-deploy2"
sys.path.insert(0, str(HERE_DEPLOY))

from sov_mind import (  # noqa: E402
    compress_to_phlabet, Spine, Glyph, PHONEMES, glyphs_to_text,
)

KB_PATH = HERE_DEPLOY / "benchmark-results" / "sov_kb.json"
HONEY_OUT = HERE_DEPLOY / "benchmark-results" / "honey_from_kb.jsonl"
SPINE_STATE = HERE_DEPLOY / "benchmark-results" / "spine_state.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_kb() -> list[dict]:
    if not KB_PATH.exists():
        print(f"KB not found at {KB_PATH}", file=sys.stderr); sys.exit(1)
    with KB_PATH.open() as f:
        d = json.load(f)
    return d.get("entries", [])


def load_processed_hashes() -> set[str]:
    if not HONEY_OUT.exists():
        return set()
    hashes: set[str] = set()
    with HONEY_OUT.open() as f:
        for line in f:
            if not line.strip(): continue
            try: hashes.add(json.loads(line).get("q_hash", ""))
            except Exception: continue
    return hashes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    entries = load_kb()
    if args.limit: entries = entries[: args.limit]

    already = load_processed_hashes()
    spine = Spine(n_layers=10)
    # Seed spine memory with one glyph of each known phoneme so initial state isn't empty
    for ph in PHONEMES.keys():
        spine.memory.append(Glyph(ph, intensity=128, provenance="seed", confidence=0.5))

    todo = []
    for e in entries:
        q = (e.get("question") or "").strip()
        a = (e.get("answer") or "").strip()
        if not q or not a: continue
        q_hash = hashlib.sha256(q.encode()).hexdigest()[:16]
        if q_hash in already: continue
        todo.append((e, q_hash))

    print(f"KB: {len(entries)} candidates, {len(already)} already processed, dry={args.dry}")
    print(f"To process: {len(todo)}")
    print(f"Spine: 10 layers × 64-dim vectors, {len(spine.memory)} seed glyphs")

    if args.dry: return 0

    HONEY_OUT.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with HONEY_OUT.open("a") as f:
        for i, (e, q_hash) in enumerate(todo, 1):
            q = e["question"]; a = e["answer"]
            dim = e.get("dimension", "unknown")
            src = e.get("source_clan", e.get("source", "kb"))

            # 1. Phlabet compression (KB Q+A → 256-symbol glyphs)
            glyphs_q = compress_to_phlabet(q, provenance=f"q:{src}")
            glyphs_a = compress_to_phlabet(a, provenance=f"a:{src}")

            # 2. Spine reasoning (10-layer MPNN over the Q+A glyph graph)
            task = glyphs_q + glyphs_a
            action = spine.think(task)

            # 3. The Spine learns — small positive reward for verified KB entries
            spine.learn(task, reward=+0.1)

            # 4. Generate the honey record (training pair for NN/GNN)
            glyph_text = glyphs_to_text(action)
            # Reasoning trace — what Phlabet symbols compose the answer
            reasoning = " → ".join(
                PHONEMES.get(g.phoneme, ("?", "?", "?"))[0] for g in action[:8]
            )

            # 4a. The primary NN/GNN training pair (input=question, output=Spine-reasoned answer)
            training_pair = {
                "input": q[:500],
                "output": a[:500],
                "glyph_summary": glyph_text[:240],
                "phlabet_sequence": [g.phoneme for g in action[:16]],
                "reasoning_trace": reasoning,
                "spine_state_dim": 64,
                "spine_n_layers": 10,
            }

            # 4b. The compressed-only pair (pure symbol → symbol)
            compressed_pair = {
                "input": " ".join(f"{g.phoneme:02x}" for g in glyphs_q[:16]),
                "output": " ".join(f"{g.phoneme:02x}" for g in glyphs_a[:16]),
                "task": "phlabet_compress",
            }

            # 4c. The graph reasoning pair (input=g+glyphs, output=Spine action)
            graph_pair = {
                "input": [{"p": g.phoneme, "i": g.intensity, "c": round(g.confidence, 3)}
                          for g in task[:16]],
                "output": [{"p": g.phoneme, "i": g.intensity, "c": round(g.confidence, 3)}
                           for g in action[:16]],
                "task": "spine_message_passing",
            }

            honey = {
                "id": q_hash,
                "q_hash": q_hash,
                "ts": now_iso(),
                "stage": f"kb.{dim}",
                "source": src,
                "verified": True,
                "n_glyphs_input": len(glyphs_q),
                "n_glyphs_output": len(glyphs_a),
                "n_glyphs_action": len(action),
                "training_pairs": [training_pair, compressed_pair, graph_pair],
            }
            f.write(json.dumps(honey) + "\n")
            written += 1

            # Stamp the resulting honey back into SovSpace (so the dome reflects the conversion)
            # (deferred — only do this if user wants the visual integration; otherwise
            #  SovSpace already has the KB stamps, the honey file is the NN/GNN substrate.)

            if i % 20 == 0:
                print(f"  progress: {i}/{len(todo)} (written={written})")

    # Persist spine state so next run picks up the trained weights
    SPINE_STATE.write_text(json.dumps({
        "weights": [layer.weights for layer in spine.layers],
        "expertise_map": spine.expertise_map(),
        "memory_size": len(spine.memory),
        "n_layers": len(spine.layers),
        "updated_at": now_iso(),
    }, indent=2))

    print(f"Done: {written} honey records → {HONEY_OUT}")
    print(f"Spine: expertise_map = {dict(list(spine.expertise_map().items())[:5])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
