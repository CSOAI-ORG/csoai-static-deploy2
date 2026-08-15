#!/usr/bin/env python3
"""refutations_to_sovspace_honey.py — flip the refutation ledger into the
Phlabet+Spine→honey pipeline, mirroring kb_to_sovspace_honey.py.

Pipeline:
  8 refutation entries (the "scars")
    → SovSpace stamps as cspace-verdict (kind=REFUTED, scars)
    → Phlabet compression (256-symbol)
    → Spine.think (10-layer MPNN/GNN message passing)
    → Spine.learn (negative reward — scars teach by counter-example)
    → 3 training-pair types:
        - natural-language claim + measured + why (scar shape)
        - Phlabet hex compression (input/output phoneme sequence)
        - graph reasoning (input/output {phoneme,intensity,confidence})
    → write benchmark-results/honey_from_refutations.jsonl

The user framing:
  scars  = the killed theses (self-inflicted wounds; honest disclosure)
  silver = published refutations (silver medal: visible to peers)
  gold   = claims that survived challenge (gold medal: durable)
  honey  = distilled training data (the knowledge that learning NN/GNN
           consumes, derived from scar→silver→gold progression)

Scars teach the NN/GNN WHAT NOT TO BELIEVE — the most valuable kind of
training signal. Per the user's earlier session note: 'Each Phlabet glyph
honours a scar by teaching the next model NOT to make the same mistake.'

Usage:
  python3 refutations_to_sovspace_honey.py            # all 8 refutations
  python3 refutations_to_sovspace_honey.py --dry      # preview only
  python3 refutations_to_sovspace_honey.py --source councilof-ai
                                                     # read from a different path
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

HERE_DEPLOY = Path.home() / "clawd" / "csoai-static-deploy2"
sys.path.insert(0, str(HERE_DEPLOY))

from sov_mind import (  # noqa: E402
    compress_to_phlabet, Spine, Glyph, PHONEMES, glyphs_to_text,
)

HONEY_OUT = HERE_DEPLOY / "benchmark-results" / "honey_from_refutations.jsonl"
SPINE_STATE = HERE_DEPLOY / "benchmark-results" / "spine_state_refutations.json"

DEFAULT_SOURCES = [
    Path.home() / "clawd" / "councilof-ai" / "client" / "src" / "pages" / "RefutationLedger.tsx",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_ledger_from_source(source: Path) -> list[dict]:
    """Parse the hardcoded LEDGER const out of RefutationLedger.tsx.

    Each entry has shape: {n, claim, measured, artefact, why} spread across
    multiple lines with em-dashes and special characters. We split into
    top-level entries by tracking brace depth, then extract each field's
    string literal by walking past escaped characters and quotes.
    """
    src = source.read_text()
    m = re.search(r"const\s+LEDGER\s*=\s*\[(.*?)\n\];", src, re.DOTALL)
    if not m:
        print(f"  could not find LEDGER const in {source}", file=sys.stderr)
        return []
    body = m.group(1)

    entries: list[dict] = []
    depth = 0
    current: list[str] = []
    entry_chunks: list[str] = []
    for ch in body:
        if ch == "{":
            depth += 1
            current.append(ch)
        elif ch == "}":
            depth -= 1
            current.append(ch)
            if depth == 0:
                entry_chunks.append("".join(current))
                current = []
        elif depth > 0:
            current.append(ch)

    for chunk in entry_chunks:
        e: dict = {}

        def extract_field(field: str) -> str | None:
            start = chunk.find(f"{field}:")
            if start < 0:
                return None
            q = chunk.find('"', start + len(field) + 1)
            if q < 0:
                return None
            i = q + 1
            out: list[str] = []
            while i < len(chunk):
                c = chunk[i]
                if c == "\\":
                    out.append(chunk[i + 1])
                    i += 2
                    continue
                if c == '"':
                    return "".join(out).encode().decode("unicode_escape")
                out.append(c)
                i += 1
            return None

        for field in ("n", "claim", "measured", "artefact", "why"):
            val = extract_field(field)
            if val is not None:
                e[field] = val
        if "n" in e and "claim" in e:
            try:
                e["n"] = int(str(e["n"]).strip())
            except (ValueError, TypeError):
                pass
            entries.append(e)
    return entries


def load_processed_hashes() -> set[str]:
    hashes: set[str] = set()
    if not HONEY_OUT.exists():
        return hashes
    with HONEY_OUT.open() as f:
        for line in f:
            if not line.strip():
                continue
            try:
                d = json.loads(line)
                h = d.get("q_hash")
                if h:
                    hashes.add(h)
            except Exception:
                continue
    return hashes


def classify(measured: str) -> tuple[str, str]:
    """Classify a measured value as SCAR / SILVER / GOLD / HONEY.

    SCAR = significant negative effect (the architecture hurt itself)
    SILVER = published refutation (any measurable non-effect is silver to peers)
    GOLD = null / no effect observed / survived challenge
    HONEY = significant positive effect (the architecture produced durable knowledge)
    """
    m = measured.lower()
    if "significant harm" in m or "leak" in m or "refusal" in m or "−" in m and "no effect" in m:
        # The scar-bearing claims
        if "−" in m or "harm" in m or "leak" in m:
            return "scar", "self-inflicted wound — measurable harm"
    if "null" in m or "no effect" in m or "no benefit" in m:
        return "gold", "challenge-survived — null effect is honest answer"
    if "Δ" in m and ("+" in m or "−" in m):
        return "silver", "published refutation — measurable effect either way"
    return "honey", "distilled into training substrate"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--source", action="append",
                    help="Override refutation source path (can repeat)")
    args = ap.parse_args()

    sources = [Path(s) for s in args.source] if args.source else DEFAULT_SOURCES
    entries: list[dict] = []
    for s in sources:
        if not s.exists():
            print(f"  source not found: {s}", file=sys.stderr)
            continue
        entries.extend(load_ledger_from_source(s))

    print(f"Refutation sources: {len(sources)}, total entries: {len(entries)}")

    already = load_processed_hashes()
    spine = Spine(n_layers=10)
    # Seed with KB-trained glyphs if available (otherwise seed fresh)
    seed_state = HERE_DEPLOY / "benchmark-results" / "spine_state.json"
    if seed_state.exists():
        try:
            state = json.loads(seed_state.read_text())
            for i, w in enumerate(state.get("weights", [])):
                if i < len(spine.layers):
                    spine.layers[i].weights = w
            print(f"  loaded trained spine weights from {seed_state}")
        except Exception:
            pass
    for ph in PHONEMES.keys():
        spine.memory.append(Glyph(ph, intensity=128, provenance="seed", confidence=0.5))

    todo = []
    for e in entries:
        q = (e.get("claim") or "").strip()
        if not q:
            continue
        q_hash = hashlib.sha256(q.encode()).hexdigest()[:16]
        if q_hash in already:
            continue
        todo.append((e, q_hash))

    print(f"To process: {len(todo)} ({len(already)} already done)")

    if args.dry:
        for e, _ in todo:
            kind, reason = classify(e.get("measured", ""))
            print(f"  [{kind}] #{e['n']} {e['claim'][:80]}")
            print(f"          reason: {reason}")
        return 0

    HONEY_OUT.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    by_kind: dict[str, int] = {}
    with HONEY_OUT.open("a") as f:
        for e, q_hash in todo:
            claim = e["claim"]
            measured = e.get("measured", "")
            why = e.get("why", "")
            artefact = e.get("artefact", "")
            n = e.get("n", "?")

            kind, kind_reason = classify(measured)
            by_kind[kind] = by_kind.get(kind, 0) + 1

            # Combine into a scar-shaped text block
            scar_text = (
                f"Claim {n}: {claim}\n"
                f"Measured: {measured}\n"
                f"Why: {why}"
            )

            # 1. Phlabet compression (claim + measured + why)
            glyphs_claim = compress_to_phlabet(claim, provenance=f"scar:{n}")
            glyphs_meas = compress_to_phlabet(measured, provenance=f"scar:{n}:measured")
            glyphs_why = compress_to_phlabet(why, provenance=f"scar:{n}:why")

            # 2. Spine reasoning — NEGATIVE reward for scars (counter-example training)
            task = glyphs_claim + glyphs_meas + glyphs_why
            action = spine.think(task)
            reward = -0.05 if kind == "scar" else (+0.02 if kind == "gold" else +0.01)
            spine.learn(task, reward=reward)

            # 3. Three training-pair types per scar
            scar_pair = {
                "input": f"Claim (REJECTED if scar): {claim[:400]}",
                "output": f"Measured: {measured[:200]}\nReason: {why[:400]}",
                "kind": kind,
                "kind_reason": kind_reason,
                "scar_n": n,
                "glyph_summary": glyphs_to_text(action)[:240],
                "phlabet_sequence": [g.phoneme for g in action[:16]],
                "reasoning_trace": " → ".join(
                    PHONEMES.get(g.phoneme, ("?", "?", "?"))[0] for g in action[:8]
                ),
                "spine_state_dim": 64,
                "spine_n_layers": 10,
                "spine_reward": reward,
                "artefact": artefact,
            }
            compressed_pair = {
                "input": " ".join(f"{g.phoneme:02x}" for g in glyphs_claim[:16]),
                "output": " ".join(f"{g.phoneme:02x}" for g in glyphs_meas[:16]),
                "task": "phlabet_compress_scar",
                "scar_n": n,
                "kind": kind,
            }
            graph_pair = {
                "input": [{"p": g.phoneme, "i": g.intensity, "c": round(g.confidence, 3)}
                          for g in task[:16]],
                "output": [{"p": g.phoneme, "i": g.intensity, "c": round(g.confidence, 3)}
                           for g in action[:16]],
                "task": "spine_message_passing_scar",
                "scar_n": n,
                "kind": kind,
            }

            honey = {
                "id": q_hash,
                "q_hash": q_hash,
                "ts": now_iso(),
                "stage": f"refutation.{kind}",
                "source": "refutation_ledger",
                "scar_n": n,
                "claim": claim,
                "measured": measured,
                "why": why,
                "artefact": artefact,
                "kind": kind,
                "kind_reason": kind_reason,
                "n_glyphs_input": len(glyphs_claim) + len(glyphs_meas),
                "n_glyphs_action": len(action),
                "spine_reward": reward,
                "training_pairs": [scar_pair, compressed_pair, graph_pair],
            }
            f.write(json.dumps(honey) + "\n")
            written += 1

    # Persist scar-trained spine state separately so it doesn't clobber the KB-trained one
    SPINE_STATE.write_text(json.dumps({
        "weights": [layer.weights for layer in spine.layers],
        "expertise_map": spine.expertise_map(),
        "memory_size": len(spine.memory),
        "n_layers": len(spine.layers),
        "updated_at": now_iso(),
        "trained_on": "refutation_ledger",
        "by_kind": by_kind,
    }, indent=2))

    print(f"Done: {written} honey records → {HONEY_OUT}")
    print(f"By kind: {by_kind}")
    print(f"Spine expertise: {dict(list(spine.expertise_map().items())[:5])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
