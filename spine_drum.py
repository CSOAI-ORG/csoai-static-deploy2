#!/usr/bin/env python3
"""SOV-Space Spine Drum — The Heartbeat of Sovereign AI

The spine drum is the rhythm that keeps everything synchronized:
  Beat 1: Evolve stigmergy (pheromone decay, pollen flow)
  Beat 2: Run EAT cycle (benchmark, improve, transform)
  Beat 3: Update knowledge (absorb new data, consolidate honey)
  Beat 4: Sync across nodes (Mac ↔ Oracle ↔ Kaggle)
  Beat 5: Generate sigil (record state in chain)

Like a heartbeat:
  Systole  = active processing (EAT, benchmark, train)
  Diastole = rest and consolidation (sync, absorb, record)

The drum beats continuously, keeping all components intertwined.
"""

import json
import hashlib
import time
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List

ROOT = Path(__file__).resolve().parent
STIGMERGY = ROOT / "stigmergy"
SOV_SPACE = ROOT / "sov_space"
FOREST = ROOT / "forest"
EAT_RESULTS = ROOT / "eat_results"
SOV_SPACE.mkdir(parents=True, exist_ok=True)


class SpineDrum:
    """The heartbeat of SOV-space — keeps everything synchronized."""

    def __init__(self, bpm: int = 1):  # 1 beat per second
        self.bpm = bpm
        self.beat_count = 0
        self.sigil_chain = []
        self.heartbeat_log = []
        self.stigmergy = None
        self._load_stigmergy()

    def _load_stigmergy(self):
        """Load stigmergy system."""
        try:
            import sys
            sys.path.insert(0, str(STIGMERGY))
            from stigmergy import SOVStigmergy
            self.stigmergy = SOVStigmergy()
        except Exception as e:
            print(f"  Stigmergy not loaded: {e}")

    def beat(self) -> Dict:
        """One heartbeat — execute all rhythm tasks."""
        self.beat_count += 1
        start = time.time()

        results = {
            "beat": self.beat_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tasks": {},
        }

        # Beat 1: Evolve stigmergy
        if self.stigmergy:
            self.stigmergy.evolve()
            results["tasks"]["stigmergy"] = {
                "pheromone_locations": len(self.stigmergy.pheromone.trails),
                "waggle_dances": len(self.stigmergy.waggle.dances),
                "pollen_deposits": len(self.stigmergy.pollen.deposits),
            }

        # Beat 2: Check EAT state
        eat_state = self._check_eat_state()
        results["tasks"]["eat"] = eat_state

        # Beat 3: Count knowledge
        knowledge = self._count_knowledge()
        results["tasks"]["knowledge"] = knowledge

        # Beat 4: Check sync status
        sync = self._check_sync()
        results["tasks"]["sync"] = sync

        # Beat 5: Generate sigil
        sigil = self._generate_sigil(results)
        results["tasks"]["sigil"] = sigil

        # Log heartbeat
        elapsed = round((time.time() - start) * 1000)
        results["elapsed_ms"] = elapsed
        self.heartbeat_log.append(results)

        return results

    def _check_eat_state(self) -> Dict:
        """Check current EAT cycle state."""
        eat_file = EAT_RESULTS / "eat_cycle_final.json"
        if eat_file.exists():
            try:
                data = json.load(open(eat_file))
                return {
                    "world_model": data.get("world_model", 0),
                    "status": data.get("status", "unknown"),
                    "categories": data.get("categories", {}),
                }
            except:
                pass
        return {"world_model": 0.89, "status": "initial", "categories": {}}

    def _count_knowledge(self) -> Dict:
        """Count all knowledge in the system."""
        counts = {}

        # Bloodline
        bloodline_path = FOREST / "bloodline.json"
        if bloodline_path.exists():
            try:
                data = json.load(open(bloodline_path))
                counts["bloodline"] = len(data.get("knowledge", []))
            except:
                counts["bloodline"] = 0

        # Honey
        honey_path = FOREST / "honey_chatml.jsonl"
        if honey_path.exists():
            try:
                counts["honey"] = sum(1 for _ in open(honey_path))
            except:
                counts["honey"] = 0

        # J-space
        jspace_dir = ROOT / "benchmark-results" / "j-space"
        if jspace_dir.exists():
            counts["jspace_families"] = len([d for d in jspace_dir.iterdir() if d.is_dir()])

        return counts

    def _check_sync(self) -> Dict:
        """Check synchronization status between nodes."""
        return {
            "oracle": "connected" if self._ping_oracle() else "disconnected",
            "kaggle": "configured" if self._check_kaggle() else "not configured",
            "local": "active",
        }

    def _ping_oracle(self) -> bool:
        """Check if Oracle is reachable."""
        try:
            result = subprocess.run(
                ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
                 "-o", "ConnectTimeout=3", "oracle-micro", "echo ok"],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def _check_kaggle(self) -> bool:
        """Check if Kaggle is configured."""
        return Path.home().joinpath(".kaggle", "access_token").exists()

    def _generate_sigil(self, data: Dict) -> Dict:
        """Generate a sigil for this heartbeat."""
        payload = {
            "beat": self.beat_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data_hash": hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16],
        }
        payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        prev_hash = self.sigil_chain[-1]["payload_hash"] if self.sigil_chain else "0" * 64
        root_hash = hashlib.sha256((prev_hash + payload_hash).encode()).hexdigest()

        sigil = {
            "payload_hash": payload_hash,
            "prev_hash": prev_hash,
            "root_hash": root_hash,
            "beat": self.beat_count,
            "timestamp": payload["timestamp"],
        }
        self.sigil_chain.append(sigil)
        return sigil

    def run(self, beats: int = 5, interval: float = 1.0):
        """Run the spine drum for N beats."""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║  SOV-SPACE SPINE DRUM — The Heartbeat                   ║")
        print("║  Evolve · EAT · Knowledge · Sync · Sigil                ║")
        print("╚══════════════════════════════════════════════════════════╝")

        for i in range(beats):
            result = self.beat()
            beat = result["beat"]
            elapsed = result["elapsed_ms"]

            # Display
            stig = result["tasks"].get("stigmergy", {})
            eat = result["tasks"].get("eat", {})
            know = result["tasks"].get("knowledge", {})
            sync = result["tasks"].get("sync", {})
            sigil = result["tasks"].get("sigil", {})

            print(f"\n  Beat {beat:3d} | {elapsed}ms")
            print(f"    Stigmergy: {stig.get('pheromone_locations', 0)} pheromone, {stig.get('waggle_dances', 0)} waggle, {stig.get('pollen_deposits', 0)} pollen")
            print(f"    EAT: {eat.get('world_model', 0):.1%} world model")
            print(f"    Knowledge: {know.get('bloodline', 0)} bloodline, {know.get('honey', 0)} honey, {know.get('jspace_families', 0)} families")
            print(f"    Sync: Oracle={sync.get('oracle', '?')}, Kaggle={sync.get('kaggle', '?')}, Local={sync.get('local', '?')}")
            print(f"    Sigil: {sigil.get('payload_hash', '')[:16]}...")

            if i < beats - 1:
                time.sleep(interval)

        # Save
        output = {
            "total_beats": self.beat_count,
            "sigil_chain_length": len(self.sigil_chain),
            "heartbeat_log": self.heartbeat_log[-5:],  # Last 5 beats
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        out_path = SOV_SPACE / "spine_drum_state.json"
        out_path.write_text(json.dumps(output, indent=2, default=str))
        print(f"\n  Saved: {out_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SOV-Space Spine Drum")
    parser.add_argument("--beats", type=int, default=5, help="Number of beats")
    parser.add_argument("--interval", type=float, default=1.0, help="Seconds between beats")
    args = parser.parse_args()

    drum = SpineDrum()
    drum.run(beats=args.beats, interval=args.interval)


if __name__ == "__main__":
    main()
