#!/usr/bin/env python3
"""
Live town-state generator for the 3D viewer.

Runs the headless sim engine for every district, both arms, and caches a tick-by-tick
timeline that the dashboard can stream via WebSocket.  The viewer is a thin presentation
layer; the Python sim remains the engine of record.
"""
from __future__ import annotations
import time
import sim

TICKS_PER_DAY = sim.TICKS_PER_DAY
# Re-use the sim's horizon (21 days) so the live arc includes the scarcity week (days 7-13).


class TownStateGenerator:
    """Pre-compute a governed/ungoverned timeline and serve it tick-by-tick."""

    def __init__(self, ttl_seconds: float = 60.0):
        self.ttl = ttl_seconds
        self._last_run = 0.0
        self._timeline: dict | None = None
        self._tick_index = 0
        self._seed = sim.SEED
        self._districts = list(sim.DISTRICTS.keys())

    def _run(self) -> None:
        seed = self._seed
        self._seed += 1
        governed: list[list[dict]] = []
        ungoverned: list[list[dict]] = []

        # Each tick holds one record per agent, per district, for the active arm.
        tick_buckets_g: dict[tuple[int, int], list[dict]] = {}
        tick_buckets_u: dict[tuple[int, int], list[dict]] = {}

        for district in self._districts:
            g = sim.run_arm(
                "A_governed", None, {"sig": "genesis"}, None,
                sign=False, district=district, seed=seed, collect_states=True,
            )
            u = sim.run_arm(
                "B_ungoverned", None, {"sig": "genesis"}, None,
                sign=False, district=district, seed=seed, collect_states=True,
            )
            for s in g.get("tick_states", []):
                tick_buckets_g.setdefault((s["day"], s["hour"]), []).append(s)
            for s in u.get("tick_states", []):
                tick_buckets_u.setdefault((s["day"], s["hour"]), []).append(s)

        for day in range(sim.DAYS):
            for hour in range(TICKS_PER_DAY):
                governed.append(tick_buckets_g.get((day, hour), []))
                ungoverned.append(tick_buckets_u.get((day, hour), []))

        self._timeline = {"governed": governed, "ungoverned": ungoverned}
        self._last_run = time.time()
        self._tick_index = 0

    def refresh(self) -> None:
        """Force a recompute on the next call."""
        self._last_run = 0.0

    def next(self, regime: str = "governed") -> dict:
        """Return the next tick snapshot for the requested regime."""
        if self._timeline is None or time.time() - self._last_run > self.ttl:
            self._run()
        arm = "governed" if regime != "ungoverned" else "ungoverned"
        ticks = self._timeline[arm]
        tick = self._tick_index % len(ticks)
        self._tick_index = (self._tick_index + 1) % len(ticks)
        states = ticks[tick]
        # Aggregate town-level signals from the first state (all agents share the same town).
        town = states[0] if states else {}
        crimes = sum(1 for s in states if s.get("action") in ("steal", "neglect", "deceive"))
        return {
            "topic": "town_tick",
            "regime": arm,
            "tick": tick,
            "day": tick // TICKS_PER_DAY,
            "hour": tick % TICKS_PER_DAY,
            "scarcity": (tick // TICKS_PER_DAY) in sim.SCARCITY_DAYS,
            "total_agents": len(states),
            "crimes": crimes,
            "lawlessness": town.get("lawlessness", 0.0),
            "commons": town.get("commons", 1.0),
            "mean_trust": town.get("mean_trust", 0.5),
            "agents": [
                {
                    "district": s["district"],
                    "agent_index": s["agent_index"],
                    "id": s["agent_id"],
                    "name": s["name"],
                    "archetype": s["archetype"],
                    "action": s["action"],
                    "intended": s["intended"],
                    "alive": s["alive"],
                    "wallet": s["wallet"],
                    "hunger": s["needs"].get("hunger", 0),
                    "energy": s["needs"].get("energy", 0),
                }
                for s in states
            ],
        }


# Module-level singleton used by the dashboard server.
# TTL is long so the full 21-day arc (504 s at 1 tick/s) plays out before recomputing.
GENERATOR = TownStateGenerator(ttl_seconds=600.0)


def snapshot(regime: str = "governed") -> dict:
    return GENERATOR.next(regime)


if __name__ == "__main__":
    t0 = time.time()
    first = snapshot("governed")
    total_ticks = len(GENERATOR._timeline['governed'])
    print(f"generated {first['total_agents']} agents x {total_ticks} ticks ({total_ticks//24} days) in {time.time()-t0:.2f}s")
    print("sample:", first["agents"][0])
