#!/usr/bin/env python3
"""SOV-Space Stigmergy — Pheromone Trails, Waggle Dances, Pollen

Agents communicate indirectly through SOV-space environment:
  Pheromone trails  — success/failure signals that evaporate over time
  Waggle dances     — structured messages from scout agents
  Pollen deposits   — knowledge fragments agents carry and deposit

SOV reads all traces to understand what's happening across clans.
No direct agent-to-agent needed — environment mediates everything.

Like bees and ants:
  Bees waggle dance → tell other bees where food is
  Ants leave pheromones → other ants follow strongest trail
  Pollen → knowledge carried between flowers (families)
"""

import json
import hashlib
import math
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
SOV_SPACE = ROOT / "benchmark-results" / "sov-space"
STIGMERGY = ROOT / "stigmergy"
STIGMERGY.mkdir(parents=True, exist_ok=True)


# ─── Pheromone Trail ────────────────────────────────────────────────────────

class PheromoneTrail:
    """Digital pheromone — success/failure signals that evaporate.

    Strong pheromone = many agents succeeded here
    Weak pheromone = few agents tried or many failed
    Evaporation = old signals fade, new signals dominate
    """

    def __init__(self, decay_rate: float = 0.1):
        self.trails = defaultdict(float)  # location -> strength
        self.history = defaultdict(list)  # location -> [(timestamp, strength)]
        self.decay_rate = decay_rate

    def deposit(self, location: str, amount: float, agent_id: str = "",
                family: str = "", clan: str = ""):
        """Deposit pheromone at a location."""
        self.trails[location] += amount
        self.history[location].append({
            "amount": amount,
            "agent": agent_id,
            "family": family,
            "clan": clan,
            "strength": self.trails[location],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def evaporate(self):
        """Evaporate all pheromone trails (call periodically)."""
        for loc in list(self.trails.keys()):
            self.trails[loc] *= (1 - self.decay_rate)
            if self.trails[loc] < 0.01:
                del self.trails[loc]

    def sense(self, location: str) -> float:
        """Sense pheromone strength at a location."""
        return self.trails.get(location, 0.0)

    def strongest(self, top_k: int = 10) -> List[Dict]:
        """Get strongest pheromone trails."""
        sorted_trails = sorted(self.trails.items(), key=lambda x: -x[1])[:top_k]
        return [{"location": loc, "strength": round(strength, 3)}
                for loc, strength in sorted_trails]

    def to_dict(self) -> Dict:
        return {
            "trails": {k: round(v, 3) for k, v in self.trails.items()},
            "total_locations": len(self.trails),
            "strongest": self.strongest(5),
        }


# ─── Waggle Dance ───────────────────────────────────────────────────────────

class WaggleDance:
    """Structured messages from scout agents — like bee waggle dances.

    Scouts discover opportunities and communicate them via structured
    messages that other agents can read and act on.
    """

    def __init__(self):
        self.dances = []

    def dance(self, scout_id: str, family: str, clan: str,
              target: str, quality: float, direction: str = "",
              distance: float = 0.0, details: str = "") -> Dict:
        """Perform a waggle dance — communicate a discovery."""
        dance = {
            "scout": scout_id,
            "family": family,
            "clan": clan,
            "target": target,
            "quality": round(quality, 3),
            "direction": direction,
            "distance": distance,
            "details": details[:200],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hash": hashlib.sha256(
                f"{scout_id}{target}{quality}".encode()
            ).hexdigest()[:12],
        }
        self.dances.append(dance)
        return dance

    def read_dances(self, family: str = None, clan: str = None,
                    min_quality: float = 0.0) -> List[Dict]:
        """Read waggle dances — filter by family, clan, or quality."""
        results = self.dances
        if family:
            results = [d for d in results if d["family"] == family]
        if clan:
            results = [d for d in results if d["clan"] == clan]
        if min_quality > 0:
            results = [d for d in results if d["quality"] >= min_quality]
        return sorted(results, key=lambda d: -d["quality"])

    def to_dict(self) -> Dict:
        return {
            "total_dances": len(self.dances),
            "recent": self.dances[-10:] if self.dances else [],
            "by_family": self._count_by("family"),
            "by_clan": self._count_by("clan"),
        }

    def _count_by(self, field: str) -> Dict[str, int]:
        counts = defaultdict(int)
        for d in self.dances:
            counts[d.get(field, "unknown")] += 1
        return dict(counts)


# ─── Pollen Deposit ─────────────────────────────────────────────────────────

class PollenDeposit:
    """Knowledge fragments that agents carry and deposit.

    Like bees carrying pollen between flowers:
      Agent visits family A → picks up knowledge
      Agent visits family B → deposits knowledge
      Cross-pollination happens naturally
    """

    def __init__(self):
        self.deposits = []
        self.pollen_map = defaultdict(list)  # family -> [pollen]

    def deposit(self, agent_id: str, from_family: str, to_family: str,
                knowledge: str, weight: float = 1.0) -> Dict:
        """Deposit pollen (knowledge) at a family."""
        pollen = {
            "agent": agent_id,
            "from": from_family,
            "to": to_family,
            "knowledge": knowledge[:300],
            "weight": weight,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hash": hashlib.sha256(knowledge.encode()).hexdigest()[:12],
        }
        self.deposits.append(pollen)
        self.pollen_map[to_family].append(pollen)
        return pollen

    def read_pollen(self, family: str) -> List[Dict]:
        """Read pollen deposited at a family."""
        return self.pollen_map.get(family, [])

    def cross_pollinate(self, family_a: str, family_b: str) -> List[Dict]:
        """Get knowledge that flowed between two families."""
        a_to_b = [p for p in self.deposits
                  if p["from"] == family_a and p["to"] == family_b]
        b_to_a = [p for p in self.deposits
                  if p["from"] == family_b and p["to"] == family_a]
        return {"a_to_b": a_to_b, "b_to_a": b_to_a}

    def to_dict(self) -> Dict:
        return {
            "total_deposits": len(self.deposits),
            "families_with_pollen": len(self.pollen_map),
            "by_family": {f: len(ps) for f, ps in self.pollen_map.items()},
        }


# ─── SOV Stigmergy — The Complete System ────────────────────────────────────

class SOVStigmergy:
    """The complete stigmergic communication system for SOV-space.

    Agents leave traces in SOV-space:
      Pheromone  → success/failure signals (what worked)
      Waggle     → structured discoveries (what was found)
      Pollen     → knowledge fragments (what was learned)

    SOV reads all traces to understand the swarm state.
    """

    def __init__(self):
        self.pheromone = PheromoneTrail(decay_rate=0.1)
        self.waggle = WaggleDance()
        self.pollen = PollenDeposit()
        self.sigil_chain = []

    def agent_succeeds(self, agent_id: str, family: str, clan: str,
                       task: str, result: str):
        """Agent succeeded — deposit positive pheromone."""
        self.pheromone.deposit(
            location=task,
            amount=1.0,
            agent_id=agent_id,
            family=family,
            clan=clan,
        )
        # Also deposit pollen (knowledge gained)
        self.pollen.deposit(
            agent_id=agent_id,
            from_family=family,
            to_family=family,
            knowledge=result[:300],
        )

    def agent_fails(self, agent_id: str, family: str, clan: str,
                    task: str):
        """Agent failed — deposit negative pheromone (warning)."""
        self.pheromone.deposit(
            location=task,
            amount=-0.5,
            agent_id=agent_id,
            family=family,
            clan=clan,
        )

    def scout_discovers(self, scout_id: str, family: str, clan: str,
                        target: str, quality: float, details: str = ""):
        """Scout discovered something — perform waggle dance."""
        self.waggle.dance(
            scout_id=scout_id,
            family=family,
            clan=clan,
            target=target,
            quality=quality,
            details=details,
        )

    def read_environment(self, family: str = None) -> Dict:
        """Read the entire stigmergic environment — what SOV sees."""
        return {
            "pheromone": self.pheromone.to_dict(),
            "waggle": self.waggle.to_dict(),
            "pollen": self.pollen.to_dict(),
            "family_view": self._family_view(family) if family else None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _family_view(self, family: str) -> Dict:
        """What a specific family sees in the environment."""
        return {
            "pheromone_strongest": self.pheromone.strongest(5),
            "waggle_dances": self.waggle.read_dances(family=family, min_quality=0.5),
            "pollen_received": self.pollen.read_pollen(family),
        }

    def evolve(self):
        """Evolve the environment — evaporate pheromone, age pollen."""
        self.pheromone.evaporate()

    def generate_sigil(self, action: str) -> Dict:
        """Generate a sigil for stigmergy action."""
        payload = {
            "action": action,
            "pheromone_count": len(self.pheromone.trails),
            "waggle_count": len(self.waggle.dances),
            "pollen_count": len(self.pollen.deposits),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        payload_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()
        prev_hash = self.sigil_chain[-1]["payload_hash"] if self.sigil_chain else "0" * 64
        root_hash = hashlib.sha256((prev_hash + payload_hash).encode()).hexdigest()
        sigil = {"payload_hash": payload_hash, "prev_hash": prev_hash, "root_hash": root_hash}
        self.sigil_chain.append(sigil)
        return sigil

    def get_state(self) -> Dict:
        """Get the complete stigmergy state."""
        return {
            "pheromone_locations": len(self.pheromone.trails),
            "waggle_dances": len(self.waggle.dances),
            "pollen_deposits": len(self.pollen.deposits),
            "sigil_chain_length": len(self.sigil_chain),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  SOV-SPACE STIGMERGY — Pheromone · Waggle · Pollen     ║")
    print("║  Agents leave traces SOV can read                       ║")
    print("╚══════════════════════════════════════════════════════════╝")

    stigmergy = SOVStigmergy()

    # Simulate agents leaving traces
    print(f"\n─── SIMULATING AGENT ACTIVITY ───")

    # Scout discovers opportunity
    stigmergy.scout_discovers(
        scout_id="scout-reasoning-01",
        family="reasoning",
        clan="clan-reasoning",
        target="EU AI Act compliance task",
        quality=0.85,
        details="Found 173 bloodline entries relevant to EU AI Act"
    )
    print(f"  Scout: waggle dance → EU AI Act compliance (quality: 0.85)")

    # Agent succeeds
    stigmergy.agent_succeeds(
        agent_id="agent-sovereign-01",
        family="sovereign",
        clan="clan-sovereign",
        task="BFT quorum verification",
        result="BFT-33 council quorum is 23 out of 33 members"
    )
    print(f"  Agent: pheromone+pollen → BFT quorum (success)")

    # Agent fails
    stigmergy.agent_fails(
        agent_id="agent-math-01",
        family="math",
        clan="clan-math",
        task="ARC challenge"
    )
    print(f"  Agent: pheromone (negative) → ARC challenge (failure)")

    # More activity
    for i in range(5):
        stigmergy.agent_succeeds(
            agent_id=f"agent-{i}",
            family="general",
            clan="clan-general",
            task=f"task-{i}",
            result=f"Knowledge from task {i}"
        )

    # Scout discoveries
    stigmergy.scout_discovers("scout-01", "compliance", "clan-compliance",
                             "GDPR Article 83", 0.9, "Fine up to 20M EUR or 4%")
    stigmergy.scout_discovers("scout-02", "defense", "clan-defense",
                             "AUKUS Pillar 2", 0.8, "AI autonomy quantum cyber")

    # Cross-pollination
    stigmergy.pollen.deposit("agent-a", "reasoning", "sovereign",
                             "Chain-of-thought reasoning improves accuracy by 10-20%")
    stigmergy.pollen.deposit("agent-b", "compliance", "ethics",
                             "EU AI Act Article 50 requires transparency for limited risk")

    # Read environment
    print(f"\n─── SOV READS ENVIRONMENT ───")
    env = stigmergy.read_environment()
    print(f"  Pheromone locations: {env['pheromone']['total_locations']}")
    print(f"  Strongest trails:")
    for trail in env['pheromone']['strongest']:
        print(f"    {trail['location']:30s} strength={trail['strength']}")
    print(f"  Waggle dances: {env['waggle']['total_dances']}")
    print(f"  Pollen deposits: {env['pollen']['total_deposits']}")
    print(f"  Families with pollen: {env['pollen']['families_with_pollen']}")

    # Family-specific view
    print(f"\n─── REASONING FAMILY VIEW ───")
    view = stigmergy.read_environment(family="reasoning")
    fv = view.get("family_view", {})
    print(f"  Waggle dances: {len(fv.get('waggle_dances', []))}")
    print(f"  Pollen received: {len(fv.get('pollen_received', []))}")

    # Evolve
    stigmergy.evolve()
    print(f"\n─── AFTER EVOLUTION ───")
    env2 = stigmergy.read_environment()
    print(f"  Pheromone locations: {env2['pheromone']['total_locations']}")
    print(f"  Strongest trails (after decay):")
    for trail in env2['pheromone']['strongest']:
        print(f"    {trail['location']:30s} strength={trail['strength']}")

    # Save
    output = {
        "state": stigmergy.get_state(),
        "environment": env,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out_path = STIGMERGY / "stigmergy_state.json"
    out_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
