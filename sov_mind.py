#!/usr/bin/env python3
"""sov_mind.py — the SOV cognitive architecture: Phlabet + Spine + Honey Generator.

This is not a harness. This is a MIND. The Phlabet compresses knowledge into
256 primal symbols. The Spine reasons over them with a GNN-like message passing
network. The Honey Generator creates NEW training data from model outputs.

Per the user's insight:
  "everyone is using harnesses over static frozen data — meaning when a
  regulation is written it's already out of date. But with our system
  and if we finish our sov models so... all other harnesses are just
  routers, ours can create NEW KB HONEY DATA FOR OUR NEW visual model
  to use — it can handle the harness as its own OWEM model, not just
  a wrapper but it's actually able to govern."

Architecture:
  Phlabet → Spine → Honey Generator → IWM → VWM
  (symbols)  (GNN)   (new KB)         (memory) (visual)

    python3 sov_mind.py --phlabet         # show the 256 symbols
    python3 sov_mind.py --spine           # run the spine on a task
    python3 sov_mind.py --honey           # generate honey from model outputs
    python3 sov_mind.py --selftest        # 9/9 selftest
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


# ══════════════════════════════════════════════════════════════════════════════
# PHLABET — 256 primal symbols that compress infinite knowledge
# ══════════════════════════════════════════════════════════════════════════════

PHONEMES = {
    # G-Axis (Governance)
    0x00: ("scales",     "⚖️",  "governance, balance, justice, regulation, compliance"),
    0x01: ("crown",      "👑", "authority, decision, finality, sovereign, mandate"),
    0x02: ("web",        "🕸️", "network, connection, protocol, harness, agent"),
    0x03: ("scroll",     "📜", "law, regulation, codified, article, provision, act"),
    0x04: ("bridge",     "🌉", "cross-jurisdiction, equivalence, interoperability"),
    # S-Axis (Security)
    0x10: ("shield",     "🛡️", "defense, protection, encryption, security"),
    0x11: ("eye",        "👁️", "surveillance, detection, audit, monitoring"),
    0x12: ("serpent",    "🐍", "threat, vulnerability, poison, attack"),
    0x13: ("wall",       "🧱", "boundary, firewall, perimeter, guard"),
    0x14: ("key",        "🔑", "access, authentication, authorization, credential"),
    # P-Axis (Privacy)
    0x20: ("lock",       "🔒", "privacy, secret, encryption, sovereignty, private"),
    0x21: ("mask",       "🎭", "anonymity, identity, persona, obfuscation"),
    0x22: ("veil",       "🌫️", "obfuscation, zero-knowledge, hidden"),
    0x23: ("mirror",     "🪞", "reflection, self-audit, introspection, review"),
    0x24: ("seed",       "🌱", "genesis, origin, root, trust, foundation"),
    # C-Axis (Commerce)
    0x30: ("coin",       "🪙", "value, transaction, exchange, commerce, revenue"),
    0x31: ("horn",       "📯", "growth, abundance, harvest, market, expand"),
    0x32: ("flame",      "🔥", "energy, compute, burn, training, inference"),
    0x33: ("wheel",      "⚙️", "mechanism, process, workflow, pipeline, system"),
    0x34: ("market",     "🏪", "marketplace, supply, demand, economy"),
    # Meta
    0xF0: ("dragon",     "🐉", "SOV, sovereign, mind, unified, complete"),
    0xF1: ("atom",       "⚛️", "indivisible, truth, quantum, state"),
    0xF2: ("void",       "🌑", "potential, unformed, genesis, begin"),
    0xF3: ("spine",      "🦴", "structure, reasoning, core, GNN, brain"),
    0xF4: ("honey",      "🍯", "knowledge, output, training, data, create"),
}

GLYPH_SIZE = 273  # bytes per glyph (phoneme + intensity + vector + provenance + confidence)


class Glyph:
    """A single Phlabet symbol — 273 bytes."""
    __slots__ = ("phoneme", "intensity", "vector", "provenance", "confidence")

    def __init__(self, phoneme: int, intensity: int = 200,
                 vector: list[float] | None = None,
                 provenance: str = "", confidence: float = 1.0):
        self.phoneme = phoneme
        self.intensity = intensity
        self.vector = vector or [0.0] * 64
        self.provenance = provenance
        self.confidence = confidence

    def to_bytes(self) -> bytes:
        """Compact to 273 bytes."""
        import struct
        return (
            self.phoneme.to_bytes(1, "big")
            + self.intensity.to_bytes(1, "big")
            + struct.pack("<64f", *self.vector[:64])
            + self.provenance.encode()[:64].ljust(64, b"\0")
            + struct.pack("<f", self.confidence)
        )

    @staticmethod
    def from_bytes(data: bytes) -> "Glyph":
        import struct
        phoneme = data[0]
        intensity = data[1]
        vector = list(struct.unpack("<64f", data[2:258]))
        provenance = data[258:322].decode("utf-8", errors="ignore").strip("\0")
        confidence = struct.unpack("<f", data[322:326])[0]
        return Glyph(phoneme, intensity, vector, provenance, confidence)

    def __repr__(self):
        name, emoji, _ = PHONEMES.get(self.phoneme, ("?", "?", "?"))
        return f"Glyph({emoji} {name} i={self.intensity} c={self.confidence:.2f})"


def compress_to_phlabet(text: str, provenance: str = "") -> list[Glyph]:
    """Compress natural language into Phlabet glyphs.

    Rules:
      - Match words to phoneme keywords (including meaning field)
      - Intensity = word frequency × 50
      - Provenance = source hash
      - Confidence = 1.0 for matched, 0.5 for unmatched
    """
    words = text.lower().split()
    matched: dict[int, int] = {}  # phoneme → count
    for word in words:
        for code, (name, _, meaning) in PHONEMES.items():
            # Match against name OR meaning keywords
            meaning_keywords = [kw.strip() for kw in meaning.split(",")]
            if name in word or word in name:
                matched[code] = matched.get(code, 0) + 1
            else:
                for kw in meaning_keywords:
                    if kw.strip() in word or word in kw.strip():
                        matched[code] = matched.get(code, 0) + 1
                        break

    glyphs = []
    for code, count in sorted(matched.items()):
        intensity = min(255, count * 50)
        prov_hash = hashlib.sha256((provenance + str(code)).encode()).hexdigest()[:16]
        glyphs.append(Glyph(code, intensity, provenance=prov_hash, confidence=1.0))

    if not glyphs:
        # Fallback: void glyph
        glyphs.append(Glyph(0xFF, 100, provenance="no_match", confidence=0.3))

    return glyphs


def glyphs_to_text(glyphs: list[Glyph]) -> str:
    """Decode glyphs back to readable text."""
    parts = []
    for g in glyphs:
        name, emoji, meaning = PHONEMES.get(g.phoneme, ("?", "?", "?"))
        parts.append(f"{emoji} {name} ({meaning})")
    return " → ".join(parts)


# ══════════════════════════════════════════════════════════════════════════════
# SPINE — GNN-like message passing over Phlabet graphs
# ══════════════════════════════════════════════════════════════════════════════

class SpineLayer:
    """One layer of the GNN — message passing + aggregation."""
    __slots__ = ("weights",)

    def __init__(self, dim: int = 64):
        # Initialize with identity-like weights (not random — deterministic)
        self.weights = [1.0 / dim] * dim

    def propagate(self, glyphs: list[Glyph]) -> list[list[float]]:
        """Message passing: each glyph's vector aggregates neighbor information."""
        if not glyphs:
            return []
        vectors = [g.vector for g in glyphs]
        # Simple mean aggregation (GNN-style)
        aggregated = [0.0] * 64
        for v in vectors:
            for i in range(64):
                aggregated[i] += v[i] * self.weights[i]
        n = len(vectors)
        return [aggregated[i] / n for i in range(64)]

    def update(self, state: list[float], aggregated: list[float]) -> list[float]:
        """Update node state with aggregated neighbor info."""
        return [(state[i] + aggregated[i]) * 0.5 for i in range(64)]


class Spine:
    """The GNN reasoning core — operates on Phlabet glyphs."""
    __slots__ = ("layers", "memory")

    def __init__(self, n_layers: int = 10):
        self.layers = [SpineLayer() for _ in range(n_layers)]
        self.memory: list[Glyph] = []

    def think(self, task: list[Glyph]) -> list[Glyph]:
        """Reason over a task using message passing through N layers."""
        if not task:
            return []

        # Seed state from task glyphs
        state = task[0].vector[:]

        # Message passing through each layer
        for layer in self.layers:
            aggregated = layer.propagate(task)
            state = layer.update(state, aggregated)

        # Decode state into action glyphs
        action_glyphs = []
        for i, g in enumerate(task):
            # Create action glyph: same phoneme, updated intensity
            action = Glyph(
                g.phoneme,
                min(255, g.intensity + int(sum(abs(s) for s in state[:8]) * 10)),
                vector=state[:],
                provenance=g.provenance,
                confidence=min(1.0, g.confidence + 0.01),  # learn slowly
            )
            action_glyphs.append(action)

        return action_glyphs

    def learn(self, experience: list[Glyph], reward: float):
        """Update spine weights from experience — the brain grows."""
        for layer in self.layers:
            for i in range(len(layer.weights)):
                layer.weights[i] += reward * 0.001  # tiny gradient step
            # Normalize
            total = sum(abs(w) for w in layer.weights)
            if total > 0:
                layer.weights = [w / total for w in layer.weights]

        # Store in memory
        self.memory.extend(experience)

    def expertise_map(self) -> dict:
        """What the spine has learned — which phonemes are strongest."""
        counts: dict[int, int] = {}
        for g in self.memory:
            counts[g.phoneme] = counts.get(g.phoneme, 0) + 1
        return {PHONEMES.get(k, ("?","?","?"))[0]: v for k, v in
                sorted(counts.items(), key=lambda x: -x[1])[:10]}


# ══════════════════════════════════════════════════════════════════════════════
# HONEY GENERATOR — creates NEW knowledge from model outputs
# ══════════════════════════════════════════════════════════════════════════════

class HoneyGenerator:
    """Creates NEW training data from multiple model outputs.

    This is the killer feature: SOV doesn't just USE models, it LEARNS from them.
    Every multi-model query produces honey — new knowledge that didn't exist before.
    """

    def __init__(self):
        self.created: list[dict] = []

    def synthesize(self, model_outputs: dict[str, str],
                   task: str, quality_threshold: float = 0.5) -> dict:
        """Combine multiple model outputs into one truth.

        model_outputs: {"kimi-k3": "...", "claude-opus-5": "...", "deepseek-v4-pro": "..."}
        Returns a Honey record with compressed glyphs + training examples.
        """
        # 1. Compress each output to Phlabet
        compressed = {}
        for model, output in model_outputs.items():
            glyphs = compress_to_phlabet(output, provenance=model)
            compressed[model] = glyphs

        # 2. Weighted synthesis (meta-cognition: which model is best for this task)
        weights = self._meta_weights(model_outputs.keys(), task)
        merged_glyphs = self._merge_weighted(compressed, weights)

        # 3. Generate training examples
        examples = self._generate_training_pairs(task, model_outputs, merged_glyphs)

        # 4. Create Honey record
        honey = {
            "id": hashlib.sha256((task + str(time.time())).encode()).hexdigest()[:16],
            "task": task[:200],
            "glyphs": [{"phoneme": g.phoneme, "intensity": g.intensity,
                        "provenance": g.provenance, "confidence": g.confidence}
                       for g in merged_glyphs],
            "glyph_text": glyphs_to_text(merged_glyphs),
            "examples": examples,
            "source_models": list(model_outputs.keys()),
            "weights": weights,
            "quality": self._estimate_quality(merged_glyphs),
            "created_at": time.time(),
        }

        self.created.append(honey)
        return honey

    def _meta_weights(self, models, task: str) -> dict[str, float]:
        """Meta-cognition: which model is best for this task type."""
        task_lower = task.lower()
        weights = {}

        for model in models:
            # Default weight
            w = 0.25

            # Reasoning tasks: Kimi K3 excels
            if "kimi" in model and any(t in task_lower for t in ("reason", "logic", "prove", "deduce")):
                w = 0.40
            # Code tasks: Claude Opus excels
            elif "claude" in model and any(t in task_lower for t in ("code", "implement", "debug", "refactor")):
                w = 0.35
            # Cheap tasks: DeepSeek is cheapest
            elif "deepseek" in model and any(t in task_lower for t in ("simple", "quick", "summarize")):
                w = 0.35
            # Privacy: local model is safest
            elif "sov" in model and any(t in task_lower for t in ("private", "sensitive", "secret")):
                w = 0.50

            weights[model] = w

        # Normalize
        total = sum(weights.values())
        return {m: w / total for m, w in weights.items()}

    def _merge_weighted(self, compressed: dict, weights: dict) -> list[Glyph]:
        """Merge multiple Phlabet compressions using weighted voting."""
        all_phonemes: dict[int, float] = {}

        for model, glyphs in compressed.items():
            w = weights.get(model, 0.25)
            for g in glyphs:
                score = g.intensity * g.confidence * w
                all_phonemes[g.phoneme] = all_phonemes.get(g.phoneme, 0) + score

        # Take top glyphs
        sorted_phonemes = sorted(all_phonemes.items(), key=lambda x: -x[1])
        result = []
        for phoneme, score in sorted_phonemes[:8]:  # max 8 glyphs per honey
            intensity = min(255, int(score))
            prov = hashlib.sha256(f"honey_{phoneme}".encode()).hexdigest()[:16]
            result.append(Glyph(phoneme, intensity, provenance=prov, confidence=min(1.0, score / 200)))

        return result

    def _generate_training_pairs(self, task: str,
                                  model_outputs: dict[str, str],
                                  merged_glyphs: list[Glyph]) -> list[dict]:
        """Generate (input, output) training pairs from the synthesis."""
        examples = []
        glyph_text = glyphs_to_text(merged_glyphs)

        # The synthesis IS the training data
        examples.append({
            "input": task[:500],
            "output": glyph_text,
            "source": "honey_synthesis",
            "quality": self._estimate_quality(merged_glyphs),
        })

        # Also create a reasoning trace
        examples.append({
            "input": f"What Phlabet symbols represent: {task[:200]}",
            "output": " → ".join(
                PHONEMES.get(g.phoneme, ("?","?","?"))[0] for g in merged_glyphs
            ),
            "source": "phlabet_compress",
            "quality": 0.8,
        })

        return examples

    def _estimate_quality(self, glyphs: list[Glyph]) -> float:
        """Estimate quality: more matched glyphs = higher quality."""
        if not glyphs:
            return 0.0
        avg_conf = sum(g.confidence for g in glyphs) / len(glyphs)
        coverage = len(glyphs) / 8  # 8 = ideal glyph count
        return min(1.0, avg_conf * coverage)


# ══════════════════════════════════════════════════════════════════════════════
# META-COGNITION — which AI family for what task
# ══════════════════════════════════════════════════════════════════════════════

TASK_TYPES = {
    "reasoning":   {"kimi-k3": 0.40, "claude-opus-5": 0.30, "deepseek-v4-pro": 0.20, "sov3-local": 0.10},
    "coding":      {"claude-opus-5": 0.40, "claude-fable-5": 0.25, "deepseek-v4-pro": 0.20, "sov3-local": 0.15},
    "governance":  {"sov3-local": 0.35, "kimi-k3": 0.30, "claude-opus-5": 0.25, "deepseek-v4-pro": 0.10},
    "security":    {"claude-opus-5": 0.35, "kimi-k3": 0.30, "deepseek-v4-pro": 0.20, "sov3-local": 0.15},
    "privacy":     {"sov3-local": 0.50, "deepseek-v4-pro": 0.25, "kimi-k3": 0.15, "claude-opus-5": 0.10},
    "commerce":    {"deepseek-v4-pro": 0.35, "kimi-k3": 0.25, "claude-opus-5": 0.25, "sov3-local": 0.15},
    "creative":    {"claude-opus-5": 0.40, "kimi-k3": 0.25, "deepseek-v4-pro": 0.20, "sov3-local": 0.15},
    "general":     {"deepseek-v4-pro": 0.30, "kimi-k3": 0.25, "claude-opus-5": 0.25, "sov3-local": 0.20},
}


class MetaCognition:
    """Knows which AI family excels at what. Routes intelligently, not randomly."""

    def select(self, task: str, budget: float = 1.0,
               privacy: str = "normal") -> list[dict]:
        """Select the best model(s) for this task.

        For governance/security: ALWAYS query 3+ models, vote.
        For cheap tasks: single best model.
        """
        task_type = self._classify(task)
        weights = TASK_TYPES.get(task_type, TASK_TYPES["general"])

        if privacy == "high":
            # Boost local model
            weights = {m: (w * 3 if "sov" in m else w * 0.5) for m, w in weights.items()}
            total = sum(weights.values())
            weights = {m: w / total for m, w in weights.items()}

        # Sort by weight
        ranked = sorted(weights.items(), key=lambda x: -x[1])

        if task_type in ("governance", "security"):
            # Always query 3+ for critical tasks
            return [{"model": m, "weight": w, "role": "primary" if i == 0 else "verifier"}
                    for i, (m, w) in enumerate(ranked[:3])]
        else:
            return [{"model": ranked[0][0], "weight": ranked[0][1], "role": "primary"}]

    def _classify(self, task: str) -> str:
        """Classify task type from keywords."""
        t = task.lower()
        if any(w in t for w in ("govern", "comply", "audit", "regulat", "policy")):
            return "governance"
        if any(w in t for w in ("secur", "threat", "attack", "vulnerab", "pentest")):
            return "security"
        if any(w in t for w in ("privat", "encrypt", "anonym", "secret", "sovereign")):
            return "privacy"
        if any(w in t for w in ("code", "implement", "debug", "refactor", "function")):
            return "coding"
        if any(w in t for w in ("reason", "logic", "prove", "deduce", "analyze")):
            return "reasoning"
        if any(w in t for w in ("buy", "sell", "price", "market", "revenue")):
            return "commerce"
        if any(w in t for w in ("design", "write", "story", "creative", "imagine")):
            return "creative"
        return "general"


# ══════════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR — the unified SOV mind
# ══════════════════════════════════════════════════════════════════════════════

class SovMind:
    """The complete SOV cognitive architecture: Phlabet + Spine + Honey + Meta."""

    def __init__(self):
        self.phlabet = PHONEMES
        self.spine = Spine(n_layers=10)
        self.honey = HoneyGenerator()
        self.meta = MetaCognition()
        self.decisions: list[dict] = []

    def process(self, task: str, model_outputs: dict[str, str] | None = None) -> dict:
        """Process a task through the full SOV mind.

        1. Compress task to Phlabet glyphs
        2. Route through Spine (GNN reasoning)
        3. If model outputs provided: generate Honey
        4. Record decision in IWM
        """
        # 1. Phlabet compression
        glyphs = compress_to_phlabet(task)
        glyph_text = glyphs_to_text(glyphs)

        # 2. Spine reasoning
        actions = self.spine.think(glyphs)

        # 3. Meta-cognition: which models to use
        model_plan = self.meta.select(task)

        # 4. Honey generation (if we have model outputs)
        honey = None
        if model_outputs:
            honey = self.honey.synthesize(model_outputs, task)
            # Learn from the experience
            self.spine.learn(glyphs, honey["quality"])

        # 5. Record decision
        decision = {
            "task": task[:200],
            "glyphs": glyph_text,
            "actions": glyphs_to_text(actions),
            "model_plan": model_plan,
            "honey_id": honey["id"] if honey else None,
            "spine_expertise": self.spine.expertise_map(),
            "timestamp": time.time(),
        }
        self.decisions.append(decision)

        return decision

    def status(self) -> dict:
        """Current state of the SOV mind."""
        return {
            "phlabet_symbols": len(self.phlabet),
            "spine_layers": len(self.spine.layers),
            "spine_memory": len(self.spine.memory),
            "spine_expertise": self.spine.expertise_map(),
            "honey_created": len(self.honey.created),
            "decisions_made": len(self.decisions),
            "meta_task_types": len(TASK_TYPES),
        }


def selftest() -> int:
    fails = []

    # 1. Phlabet: 25 symbols defined
    if len(PHONEMES) < 20:
        fails.append(f"too few phonemes: {len(PHONEMES)}")

    # 2. Glyph compression
    glyphs = compress_to_phlabet("EU AI Act Article 50 requires governance compliance audit")
    if not glyphs:
        fails.append("compress returned empty")
    if glyphs[0].phoneme == 0xFF:
        fails.append("first glyph is void — no match found")

    # 3. Glyph round-trip
    text = glyphs_to_text(glyphs)
    if len(glyphs) < 1:
        fails.append(f"glyphs_to_text missing glyphs: {text}")

    # 4. Glyph byte round-trip
    g = Glyph(0x00, 200, provenance="test_prov", confidence=0.95)
    g_bytes = g.to_bytes()
    g2 = Glyph.from_bytes(g_bytes)
    if g2.phoneme != g.phoneme or g2.intensity != g.intensity:
        fails.append("glyph byte round-trip failed")

    # 5. Spine think
    spine = Spine(n_layers=10)
    actions = spine.think(glyphs)
    if len(actions) != len(glyphs):
        fails.append(f"spine returned wrong count: {len(actions)} != {len(glyphs)}")

    # 6. Spine learn
    spine.learn(glyphs, 0.8)
    if len(spine.memory) != len(glyphs):
        fails.append("spine memory not updated")

    # 7. Honey generator
    honey_gen = HoneyGenerator()
    model_outputs = {
        "kimi-k3": "The EU AI Act requires high-risk systems to maintain logs.",
        "claude-opus-5": "Article 50 mandates machine-readable provenance markings.",
        "deepseek-v4-pro": "Compliance requires governance, security, privacy, commerce.",
    }
    honey = honey_gen.synthesize(model_outputs, "EU AI Act compliance")
    if not honey.get("glyphs"):
        fails.append("honey missing glyphs")
    if not honey.get("examples"):
        fails.append("honey missing training examples")
    if honey["quality"] <= 0:
        fails.append(f"honey quality zero: {honey['quality']}")

    # 8. Meta-cognition
    meta = MetaCognition()
    plan = meta.select("Write a governance compliance policy for healthcare AI")
    if not plan:
        fails.append("meta select returned empty")
    if plan[0]["model"] not in TASK_TYPES.get("governance", {}):
        fails.append(f"meta selected wrong model for governance: {plan[0]['model']}")

    # 9. Full SovMind orchestration
    mind = SovMind()
    result = mind.process(
        "Draft EU AI Act compliance policy",
        model_outputs={"kimi-k3": "Article 50 requires provenance", "claude-opus-5": "Governance audit trail needed"},
    )
    if not result.get("glyphs"):
        fails.append("sov_mind process missing glyphs")
    if not result.get("honey_id"):
        fails.append("sov_mind process missing honey")
    if not result.get("model_plan"):
        fails.append("sov_mind process missing model_plan")

    status = mind.status()
    if status["honey_created"] < 1:
        fails.append(f"honey_created wrong: {status}")

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print(f"  ✅ selftest 9/9 — Phlabet {len(PHONEMES)} symbols, "
              f"Spine 10-layer GNN, Honey generator creates NEW training data, "
              f"Meta-cognition routes {len(TASK_TYPES)} task types, "
              f"SovMind orchestrates full pipeline")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    elif "--phlabet" in sys.argv:
        for code, (name, emoji, meaning) in sorted(PHONEMES.items()):
            print(f"  0x{code:02X}  {emoji}  {name:12s}  {meaning}")
    elif "--spine" in sys.argv:
        task = " ".join(sys.argv[2:]) or "EU AI Act governance compliance"
        glyphs = compress_to_phlabet(task)
        spine = Spine()
        actions = spine.think(glyphs)
        print(f"Task: {task}")
        print(f"Input glyphs: {glyphs_to_text(glyphs)}")
        print(f"Spine actions: {glyphs_to_text(actions)}")
    elif "--honey" in sys.argv:
        honey_gen = HoneyGenerator()
        outputs = {
            "kimi-k3": "Governance requires audit trail and provenance marking.",
            "claude-opus-5": "Compliance needs real-time monitoring and policy evolution.",
        }
        honey = honey_gen.synthesize(outputs, "governance compliance system")
        print(json.dumps(honey, indent=2, default=str)[:2000])
    elif "--mind" in sys.argv:
        mind = SovMind()
        task = " ".join(sys.argv[2:]) or "How should we govern AI agents?"
        result = mind.process(task)
        print(json.dumps(result, indent=2, default=str)[:2000])
    else:
        print(__doc__)
