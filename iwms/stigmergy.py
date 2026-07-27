"""
STIGMERGY LAYER: Pheromone + Waggle + Pollen

Three communication types inspired by insect swarms:

1. PHEROMONE (ants): Indirect coordination through environment
   - Successful paths get stronger pheromone trails
   - Failed paths evaporate over time
   - Used for routing decisions

2. WAGGLE (bees): Direct communication of location/direction
   - Encodes "where the good stuff is" (which clan/family won)
   - Used for directing swarm attention

3. POLLEN (bees): Knowledge transfer
   - Carries knowledge between brains
   - Used for spreading learned patterns

SPINE DRUM: Heartbeat synchronizer
- Keeps all 6,912 model slots synchronized
- Beats every 100ms
- Ensures all layers are aligned
"""
import json, time, threading, math
from pathlib import Path
from datetime import datetime
from collections import defaultdict

IWM_DIR = Path(__file__).resolve().parent


class StigmergyLayer:
    """Stigmergy: Pheromone + Waggle + Pollen communication."""

    def __init__(self):
        self.pheromone_trails = {}  # ant-style indirect coordination
        self.waggle_dances = []  # bee-style direct communication
        self.pollen_grains = []  # bee-style knowledge transfer
        self.evaporation_rate = 0.01  # pheromone evaporation per cycle

    def propagate_hive(self, hive_results):
        """Propagate all three signal types across hive results."""
        for hive_name, clan_results in hive_results.items():
            for clan_name, clan_result in clan_results.items():
                confidence = clan_result.get("confidence", 0)
                best_fam = clan_result.get("c_space", {}).get("best_family", "unknown")

                # PHEROMONE: Update trail strength
                trail_key = f"{hive_name}:{clan_name}:{best_fam}"
                if trail_key not in self.pheromone_trails:
                    self.pheromone_trails[trail_key] = {"strength": 0, "count": 0, "last_update": None}
                self.pheromone_trails[trail_key]["strength"] += confidence
                self.pheromone_trails[trail_key]["count"] += 1
                self.pheromone_trails[trail_key]["last_update"] = datetime.now().isoformat()

                # WAGGLE: Direct signal about winning clan
                waggle = {
                    "source_hive": hive_name,
                    "source_clan": clan_name,
                    "best_family": best_fam,
                    "confidence": confidence,
                    "direction": "toward" if confidence > 0.5 else "away",
                    "timestamp": datetime.now().isoformat(),
                }
                self.waggle_dances.append(waggle)

                # POLLEN: Knowledge transfer signal
                pollen = {
                    "source": f"{hive_name}:{clan_name}",
                    "target": "all",
                    "knowledge_type": "clan_result",
                    "payload": {"confidence": confidence, "best_family": best_fam},
                    "timestamp": datetime.now().isoformat(),
                }
                self.pollen_grains.append(pollen)

        # Evaporate old pheromone trails
        self._evaporate()

    def _evaporate(self):
        """Evaporate pheromone trails over time."""
        for key in list(self.pheromone_trails.keys()):
            trail = self.pheromone_trails[key]
            trail["strength"] *= (1 - self.evaporation_rate)
            if trail["strength"] < 0.01:
                del self.pheromone_trails[key]

    def get_strongest_trails(self, top_n=10):
        """Get strongest pheromone trails (most successful paths)."""
        sorted_trails = sorted(
            self.pheromone_trails.items(),
            key=lambda x: x[1]["strength"] / max(x[1]["count"], 1),
            reverse=True,
        )
        return sorted_trails[:top_n]

    def get_waggle_summary(self):
        """Get waggle dance summary (where the good stuff is)."""
        if not self.waggle_dances:
            return {"total": 0, "top_targets": []}
        # Count toward/away signals
        toward = sum(1 for w in self.waggle_dances if w["direction"] == "toward")
        away = sum(1 for w in self.waggle_dances if w["direction"] == "away")
        # Top targets
        targets = defaultdict(int)
        for w in self.waggle_dances:
            if w["direction"] == "toward":
                targets[f"{w['source_hive']}:{w['source_clan']}"] += 1
        top = sorted(targets.items(), key=lambda x: x[1], reverse=True)[:5]
        return {"total": len(self.waggle_dances), "toward": toward, "away": away, "top_targets": top}

    def get_pollen_summary(self):
        """Get pollen grain summary (knowledge transfers)."""
        return {
            "total": len(self.pollen_grains),
            "unique_sources": len(set(p["source"] for p in self.pollen_grains)),
        }

    def get_signal_summary(self):
        return {
            "pheromone_trails": len(self.pheromone_trails),
            "waggle_dances": len(self.waggle_dances),
            "pollen_grains": len(self.pollen_grains),
            "strongest_trails": self.get_strongest_trails(5),
            "waggle_summary": self.get_waggle_summary(),
            "pollen_summary": self.get_pollen_summary(),
        }


class SpineDrum:
    """Spine Drum: Heartbeat synchronizer for all model slots."""

    def __init__(self, bpm=600):  # 600 BPM = 10 beats/second
        self.bpm = bpm
        self.interval = 60.0 / bpm  # seconds between beats
        self.beats = 0
        self.last_beat = None
        self.sync_status = {"mac": False, "oracle": False, "kaggle": False, "cloud": False}
        self.heartbeat_log = []

    def beat(self, results=None):
        """Single heartbeat — synchronize all nodes."""
        self.beats += 1
        self.last_beat = datetime.now().isoformat()
        beat_data = {
            "beat": self.beats,
            "timestamp": self.last_beat,
            "nodes_synced": sum(1 for v in self.sync_status.values() if v),
            "total_nodes": len(self.sync_status),
            "results_count": len(results) if results else 0,
        }
        self.heartbeat_log.append(beat_data)
        # Keep only last 100 beats
        if len(self.heartbeat_log) > 100:
            self.heartbeat_log = self.heartbeat_log[-100:]
        return beat_data

    def sync_node(self, node_name, status=True):
        """Register a node as synced."""
        self.sync_status[node_name] = status

    def get_status(self):
        return {
            "bpm": self.bpm,
            "total_beats": self.beats,
            "last_beat": self.last_beat,
            "synced_nodes": sum(1 for v in self.sync_status.values() if v),
            "total_nodes": len(self.sync_status),
            "node_status": self.sync_status,
        }
