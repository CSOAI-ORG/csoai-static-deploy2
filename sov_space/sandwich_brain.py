#!/usr/bin/env python3
"""OWEM Sandwich Brain — Fractal Hive Architecture

Each OWEM is a sandwich brain split into 4 parts:
  TOP 2 (small, 10%): OWM (Outer/Open World Models)
    - One frozen (stable knowledge)
    - One fluid (adapting in real-time)
  BOTTOM 2 (big): IWM (Inner World Models)
    - One frozen (core reasoning, stable)
    - One fluid (learning, evolving)

12 OWEM families = 12 sandwich brains
Each brain = 4 models (2 OWM + 2 IWM)
Total: 48 model slots per hive layer

Hive Architecture:
  SOV-Space contains 12 OWEM hives
  Each hive contains 12 clan layers
  Each clan layer has sandwich brains
  Connected by stigmergy (pheromone/waggle/pollen)
  Operating in UE5 for visualization
  Quantized for speed

SOV is not a wrapper — it IS the whole machine.
It turns frozen into fluid and evolves clans as fractal hive.
"""

import json
import hashlib
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
SOV_SPACE = ROOT / "sov_space"
FOREST = ROOT / "forest"


# ─── Sandwich Brain ──────────────────────────────────────────────────────────

class SandwichBrain:
    """A single OWEM brain — 4 model slots.

    Architecture:
      OWM-Small-Frozen  |  OWM-Small-Fluid
      ─────────────────┼─────────────────
      IWM-Big-Frozen    |  IWM-Big-Fluid

    OWM = Outer World Model (perception, environment)
    IWM = Inner World Model (reasoning, memory)
    Frozen = stable, trained, reliable
    Fluid = adapting, learning, evolving
    """

    def __init__(self, family: str, clan: str = ""):
        self.family = family
        self.clan = clan
        self.models = {
            "owm_frozen": {"type": "owm", "state": "frozen", "size": "small", "model": None, "status": "ready"},
            "owm_fluid": {"type": "owm", "state": "fluid", "size": "small", "model": None, "status": "ready"},
            "iwm_frozen": {"type": "iwm", "state": "frozen", "size": "big", "model": None, "status": "ready"},
            "iwm_fluid": {"type": "iwm", "state": "fluid", "size": "big", "model": None, "status": "ready"},
        }
        self.sigil_chain = []
        self.memory = []

    def perceive(self, input_data: str) -> Dict:
        """Process input through OWM models."""
        # OWM frozen: stable perception
        frozen_result = self._process_owm(input_data, "owm_frozen")
        # OWM fluid: adaptive perception
        fluid_result = self._process_owm(input_data, "owm_fluid")

        return {
            "frozen": frozen_result,
            "fluid": fluid_result,
            "consensus": self._consensus(frozen_result, fluid_result),
        }

    def reason(self, perception: Dict) -> Dict:
        """Process through IWM models."""
        # IWM frozen: stable reasoning
        frozen_result = self._process_iwm(perception, "iwm_frozen")
        # IWM fluid: adaptive reasoning
        fluid_result = self._process_iwm(perception, "iwm_fluid")

        return {
            "frozen": frozen_result,
            "fluid": fluid_result,
            "consensus": self._consensus(frozen_result, fluid_result),
        }

    def _process_owm(self, data: str, model_key: str) -> Dict:
        """Process through OWM model."""
        model = self.models[model_key]
        # Simulate OWM processing
        result = {
            "model": model_key,
            "type": "owm",
            "state": model["state"],
            "input": data[:100],
            "confidence": 0.85 if model["state"] == "frozen" else 0.75,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.memory.append(result)
        return result

    def _process_iwm(self, perception: Dict, model_key: str) -> Dict:
        """Process through IWM model."""
        model = self.models[model_key]
        # Simulate IWM processing
        result = {
            "model": model_key,
            "type": "iwm",
            "state": model["state"],
            "perception_hash": hashlib.sha256(str(perception).encode()).hexdigest()[:8],
            "confidence": 0.90 if model["state"] == "frozen" else 0.80,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.memory.append(result)
        return result

    def _consensus(self, frozen: Dict, fluid: Dict) -> Dict:
        """Reach consensus between frozen and fluid models."""
        # Weighted average: frozen gets more weight for stability
        frozen_weight = 0.6
        fluid_weight = 0.4
        consensus_score = (
            frozen.get("confidence", 0) * frozen_weight +
            fluid.get("confidence", 0) * fluid_weight
        )
        return {
            "score": round(consensus_score, 3),
            "frozen_weight": frozen_weight,
            "fluid_weight": fluid_weight,
            "decision": "proceed" if consensus_score >= 0.8 else "revise",
        }

    def evolve(self):
        """Evolve the fluid models based on memory."""
        # Fluid models learn from memory
        for model_key in ["owm_fluid", "iwm_fluid"]:
            model = self.models[model_key]
            # Simulate learning
            model["status"] = "evolved"

    def get_state(self) -> Dict:
        """Get brain state."""
        return {
            "family": self.family,
            "clan": self.clan,
            "models": {k: {"state": v["state"], "status": v["status"]} for k, v in self.models.items()},
            "memory_size": len(self.memory),
            "sigil_chain_length": len(self.sigil_chain),
        }


# ─── Clan Layer ──────────────────────────────────────────────────────────────

class ClanLayer:
    """A clan layer — 12 OWEM families with their sandwich brains.

    Each clan has:
      - 12 OWEM sandwich brains
      - One smaller SOV router (SOV1 or SOV2)
      - Swarm of agents
      - Connected by stigmergy
    """

    def __init__(self, clan_name: str, layer_index: int):
        self.clan_name = clan_name
        self.layer_index = layer_index
        self.families = {}
        self.router = None
        self.swarm = []
        self.stigmergy_trails = {}

        # Initialize 12 OWEM families
        family_names = [
            "abstraction", "aesthetics", "agency", "care",
            "creation", "destruction", "embodiment", "ethics",
            "identity", "logic", "preservation", "relationality",
        ]
        for fam in family_names:
            self.families[fam] = SandwichBrain(family=fam, clan=clan_name)

    def process_task(self, task: str) -> Dict:
        """Process a task through all 12 families."""
        results = {}
        for fam_name, brain in self.families.items():
            # Each family perceives and reasons
            perception = brain.perceive(task)
            reasoning = brain.reason(perception)
            results[fam_name] = {
                "perception": perception["consensus"],
                "reasoning": reasoning["consensus"],
            }

        # Aggregate results
        avg_score = sum(r["reasoning"]["score"] for r in results.values()) / len(results)
        return {
            "clan": self.clan_name,
            "family_results": results,
            "overall_score": round(avg_score, 3),
            "decision": "proceed" if avg_score >= 0.8 else "revise",
        }

    def evolve(self):
        """Evolve all families in this clan."""
        for brain in self.families.values():
            brain.evolve()

    def get_state(self) -> Dict:
        """Get clan state."""
        return {
            "clan": self.clan_name,
            "layer": self.layer_index,
            "families": len(self.families),
            "swarm_size": len(self.swarm),
            "stigmergy_trails": len(self.stigmergy_trails),
        }


# ─── OWEM Hive ──────────────────────────────────────────────────────────────

class OWEMHive:
    """An OWEM hive — 12 clan layers, each with sandwich brains.

    The hive is a fractal structure:
      SOV-Space
        └── 12 OWEM Hives
            └── 12 Clan Layers
                └── 12 Sandwich Brains (4 models each)
                    └── 48 model slots per clan
                        └── 576 model slots per hive
                            └── 6,912 model slots total
    """

    def __init__(self, hive_name: str):
        self.hive_name = hive_name
        self.clans = {}
        self.sigil_chain = []

        # Initialize 12 clan layers
        for i in range(12):
            clan_name = f"clan-{i+1}"
            self.clans[clan_name] = ClanLayer(clan_name, i)

    def process_task(self, task: str) -> Dict:
        """Process a task through all clan layers."""
        results = {}
        for clan_name, clan in self.clans.items():
            result = clan.process_task(task)
            results[clan_name] = result

        # BFT quorum across clans
        approvals = sum(1 for r in results.values() if r["decision"] == "proceed")
        quorum_met = approvals >= 8  # 2/3 of 12

        return {
            "hive": self.hive_name,
            "clan_results": results,
            "approvals": approvals,
            "quorum_met": quorum_met,
            "decision": "proceed" if quorum_met else "revise",
        }

    def evolve(self):
        """Evolve all clans in this hive."""
        for clan in self.clans.values():
            clan.evolve()

    def get_state(self) -> Dict:
        """Get hive state."""
        return {
            "hive": self.hive_name,
            "clans": len(self.clans),
            "total_families": sum(len(c.families) for c in self.clans.values()),
            "total_models": sum(
                sum(len(b.models) for b in c.families.values())
                for c in self.clans.values()
            ),
        }


# ─── SOV-Space Fractal Architecture ─────────────────────────────────────────

class SOVFractalArchitecture:
    """The complete fractal architecture — SOV is the whole machine.

    SOV-Space contains:
      - 12 OWEM Hives
      - Each hive has 12 clan layers
      - Each clan has 12 sandwich brains
      - Each brain has 4 models (2 OWM + 2 IWM)
      - All connected by stigmergy
      - BFT quorum governs decisions
      - SIGIL chain records everything

    SOV is not a wrapper — it IS the machine.
    It turns frozen into fluid and evolves clans as fractal hive.
    """

    def __init__(self):
        self.hives = {}
        self.sigil_chain = []
        self.stigmergy = {
            "pheromone": {},
            "waggle": [],
            "pollen": {},
        }

        # Initialize 12 OWEM hives
        hive_names = [
            "abstraction", "aesthetics", "agency", "care",
            "creation", "destruction", "embodiment", "ethics",
            "identity", "logic", "preservation", "relationality",
        ]
        for name in hive_names:
            self.hives[name] = OWEMHive(name)

    def process_task(self, task: str) -> Dict:
        """Process a task through the entire fractal architecture."""
        start = time.time()

        # Process through all hives
        hive_results = {}
        for hive_name, hive in self.hives.items():
            result = hive.process_task(task)
            hive_results[hive_name] = result

        # Global BFT quorum
        approvals = sum(1 for r in hive_results.values() if r["decision"] == "proceed")
        quorum_met = approvals >= 8  # 2/3 of 12 hives

        # Generate sigil
        sigil = self._generate_sigil(task, hive_results)

        elapsed = round((time.time() - start) * 1000)

        return {
            "task": task,
            "hive_results": hive_results,
            "global_approvals": approvals,
            "global_quorum_met": quorum_met,
            "global_decision": "proceed" if quorum_met else "revise",
            "sigil": sigil,
            "elapsed_ms": elapsed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def evolve_all(self):
        """Evolve all hives — turn frozen into fluid."""
        for hive in self.hives.values():
            hive.evolve()

    def _generate_sigil(self, task: str, results: Dict) -> Dict:
        """Generate sigil for this processing."""
        payload = {
            "task": task,
            "approvals": sum(1 for r in results.values() if r["decision"] == "proceed"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        prev_hash = self.sigil_chain[-1]["payload_hash"] if self.sigil_chain else "0" * 64
        root_hash = hashlib.sha256((prev_hash + payload_hash).encode()).hexdigest()

        sigil = {"payload_hash": payload_hash, "prev_hash": prev_hash, "root_hash": root_hash}
        self.sigil_chain.append(sigil)
        return sigil

    def get_state(self) -> Dict:
        """Get complete fractal architecture state."""
        total_models = sum(
            hive.get_state()["total_models"]
            for hive in self.hives.values()
        )
        total_families = sum(
            hive.get_state()["total_families"]
            for hive in self.hives.values()
        )
        return {
            "hives": len(self.hives),
            "total_clans": sum(len(h.clans) for h in self.hives.values()),
            "total_families": total_families,
            "total_models": total_models,
            "sigil_chain_length": len(self.sigil_chain),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  OWEM SANDWICH BRAIN — Fractal Hive Architecture       ║")
    print("║  SOV is the whole machine                               ║")
    print("╚══════════════════════════════════════════════════════════╝")

    architecture = SOVFractalArchitecture()

    # Show state
    state = architecture.get_state()
    print(f"\n─── FRACTAL ARCHITECTURE ───")
    print(f"  Hives: {state['hives']}")
    print(f"  Total Clans: {state['total_clans']}")
    print(f"  Total Families: {state['total_families']}")
    print(f"  Total Models: {state['total_models']}")
    print(f"  Sigil Chain: {state['sigil_chain_length']}")

    # Process a task
    print(f"\n─── PROCESSING TASK ───")
    result = architecture.process_task("What is the BFT council quorum?")
    print(f"  Task: {result['task']}")
    print(f"  Global Approvals: {result['global_approvals']}/12")
    print(f"  Global Quorum: {result['global_quorum_met']}")
    print(f"  Decision: {result['global_decision']}")
    print(f"  Elapsed: {result['elapsed_ms']}ms")

    # Show hive results
    print(f"\n─── HIVE RESULTS ───")
    for hive_name, hive_result in result["hive_results"].items():
        approvals = hive_result["approvals"]
        # Get average score from clan results
        clan_scores = []
        for clan_name, clan_result in hive_result["clan_results"].items():
            for fam_result in clan_result["family_results"].values():
                clan_scores.append(fam_result["reasoning"]["score"])
        avg_score = sum(clan_scores) / max(1, len(clan_scores))
        print(f"  {hive_name:15s} {hive_result['decision']:8s} approvals={approvals}/12 score={avg_score:.3f}")

    # Evolve
    print(f"\n─── EVOLVING ALL ───")
    architecture.evolve_all()
    state2 = architecture.get_state()
    print(f"  Total Models (after evolve): {state2['total_models']}")

    # Save
    output = {
        "state": state,
        "task_result": result,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out_path = SOV_SPACE / "fractal_architecture.json"
    out_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
