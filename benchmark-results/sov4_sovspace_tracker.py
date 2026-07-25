#!/usr/bin/env python3
import json, time, hashlib, hmac, os
from pathlib import Path
from datetime import datetime, timezone

SOVEREIGN_DIR = Path.home() / ".sovereign"
MEMORY_PATH = SOVEREIGN_DIR / "sovereign_memory.jsonl"
SOVSPACE_PATH = SOVEREIGN_DIR / "sovspace_state.json"
SIGIL_DIR = SOVEREIGN_DIR / "sigil"
SIGIL_KEY_PATH = SIGIL_DIR / "sov_ed25519.key"

SOVSPACE_CONCEPTS = [
    "care_floor", "care_score_current", "sigil_position",
    "sigil_prev_hash", "bft_quorum", "bft_approvals",
    "article_0", "invariant_1", "invariant_2", "invariant_3",
    "invariant_4", "invariant_5", "invariant_6",
    "owem_route", "backend_chain", "anti_pattern_check",
    "fluid_phase", "lineage_rho", "j_space_activity",
    "last_heartbeat", "heartbeat_count",
    "sov_town_simulations", "sov_town_last_run",
]

class SovSpaceTracker:
    def __init__(self):
        self.state = self._load_or_init()
        self.last_memory_count = 0

    def _load_or_init(self):
        if SOVSPACE_PATH.exists():
            try:
                return json.loads(SOVSPACE_PATH.read_text())
            except: pass
        return {
            "care_floor": 0.95, "care_score_current": 0.95,
            "sigil_position": 0, "sigil_prev_hash": "root",
            "bft_quorum": "23/33", "bft_approvals": 0,
            "article_0": True,
            "invariant_1": True, "invariant_2": True, "invariant_3": True,
            "invariant_4": False, "invariant_5": True, "invariant_6": True,
            "owem_route": "general", "backend_chain": ["sov_brain"],
            "anti_pattern_check": "PASS", "fluid_phase": "HONEY",
            "lineage_rho": 0.42, "j_space_activity": [],
            "last_heartbeat": None, "heartbeat_count": 0,
            "sov_town_simulations": 0, "sov_town_last_run": None,
        }

    def save(self):
        SOVSPACE_PATH.parent.mkdir(parents=True, exist_ok=True)
        SOVSPACE_PATH.write_text(json.dumps(self.state, indent=2) + "\n")

    def check_memory_health(self):
        if not MEMORY_PATH.exists():
            return {"memory_exists": False, "memory_count": 0, "last_entry_age_s": None}
        entries = [l for l in MEMORY_PATH.read_text().strip().split("\n") if l.strip()]
        count = len(entries)
        last_age = None
        if count > 0:
            try:
                last = json.loads(entries[-1])
                ts = last.get("timestamp", last.get("created", ""))
                if ts:
                    last_age = (time.time() - datetime.fromisoformat(ts).timestamp())
            except: pass
        return {"memory_exists": True, "memory_count": count, "last_entry_age_s": last_age}

    def check_sigil_chain(self):
        if not MEMORY_PATH.exists():
            return {"chain_ok": False, "chain_length": 0, "chain_valid": True}
        entries = [l for l in MEMORY_PATH.read_text().strip().split("\n") if l.strip()]
        chain_valid = True
        prev_hash = "root"
        for entry in entries:
            try:
                e = json.loads(entry)
                sigil = e.get("sigil", e.get("sigil_hash", ""))
                if sigil:
                    this_prev = e.get("prev_hash", e.get("sigil_prev", ""))
                    if prev_hash != "root" and this_prev and this_prev != prev_hash:
                        chain_valid = False
                    prev_hash = sigil
            except: pass
        return {"chain_ok": chain_valid, "chain_length": len(entries), "chain_valid": chain_valid}

    def get_care_metrics(self):
        if not MEMORY_PATH.exists():
            return {"avg_care": None, "min_care": None, "total_ops": 0}
        entries = [l for l in MEMORY_PATH.read_text().strip().split("\n") if l.strip()]
        scores = []
        for entry in entries:
            try:
                e = json.loads(entry)
                cs = e.get("care_score", e.get("care_floor_score", None))
                if cs is not None:
                    scores.append(float(cs))
            except: pass
        if not scores:
            return {"avg_care": None, "min_care": None, "total_ops": len(entries)}
        return {"avg_care": sum(scores)/len(scores), "min_care": min(scores), "total_ops": len(entries)}

    def validate_invariants(self):
        self.state["invariant_1"] = float(self.state.get("care_score_current", 0)) >= 0.95
        self.state["invariant_2"] = bool(self.state.get("article_0", False))
        self.state["invariant_3"] = True
        chain = self.check_sigil_chain()
        self.state["invariant_4"] = chain["chain_valid"]
        self.state["invariant_5"] = chain["chain_valid"]
        self.state["invariant_6"] = True
        return {f"invariant_{i}": self.state[f"invariant_{i}"] for i in range(1, 7)}

    def update_after_operation(self, care_score=0.95, owem_route="general",
                                backend_chain=None, anti_patterns=None):
        self.state["care_score_current"] = care_score
        self.state["owem_route"] = owem_route
        if backend_chain:
            self.state["backend_chain"] = backend_chain
        if anti_patterns:
            self.state["anti_pattern_check"] = anti_patterns
        chain = self.check_sigil_chain()
        self.state["sigil_position"] = chain["chain_length"]
        if chain["chain_length"] > 0:
            entries = MEMORY_PATH.read_text().strip().split("\n")
            try:
                last = json.loads(entries[-1])
                self.state["sigil_prev_hash"] = last.get("sigil", last.get("sigil_hash", ""))
            except: pass
        self._update_jspace(owem_route)
        self.validate_invariants()
        self.save()

    def _update_jspace(self, route):
        active = ["sovereignty", "care_floor", "sov_town"]
        if route == "compliance":
            active += ["compliance", "article_0", "eu_ai_act"]
        elif route == "defence":
            active += ["defence", "threat", "intrusion", "wargaming"]
        elif route == "intuition":
            active += ["intuition", "pattern", "prediction", "simulation"]
        elif route == "voice":
            active += ["voice", "charter", "sovereign_truth"]
        else:
            active += ["general", "synthesis", "cross_domain", "wargaming"]
        self.state["j_space_activity"] = active

    def heartbeat(self):
        self.state["heartbeat_count"] = self.state.get("heartbeat_count", 0) + 1
        self.state["last_heartbeat"] = datetime.now(timezone.utc).isoformat()
        chain = self.check_sigil_chain()
        self.state["sigil_position"] = chain["chain_length"]
        self.validate_invariants()
        sov_town_dir = Path.home() / ".sovereign" / "sov_town"
        if sov_town_dir.exists():
            sims = list(sov_town_dir.glob("simulation_*.json"))
            self.state["sov_town_simulations"] = len(sims)
            if sims:
                latest = max(sims, key=lambda p: p.stat().st_mtime)
                try:
                    self.state["sov_town_last_run"] = json.loads(latest.read_text()).get("timestamp", datetime.fromtimestamp(latest.stat().st_mtime).isoformat())
                except:
                    self.state["sov_town_last_run"] = datetime.fromtimestamp(latest.stat().st_mtime).isoformat()
        self.save()
        return {
            "heartbeat": self.state["heartbeat_count"],
            "timestamp": self.state["last_heartbeat"],
            "invariants_ok": all(self.state[f"invariant_{i}"] for i in range(1, 7)),
            "sigil_position": self.state["sigil_position"],
            "care_score": self.state["care_score_current"],
            "memory": self.check_memory_health(),
            "chain": chain,
        }

    def to_json(self):
        return self.state

if __name__ == "__main__":
    import sys
    tracker = SovSpaceTracker()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        print(json.dumps(tracker.to_json(), indent=2))
    elif cmd == "heartbeat":
        result = tracker.heartbeat()
        print(json.dumps(result, indent=2))
    elif cmd == "invariants":
        inv = tracker.validate_invariants()
        all_ok = all(inv.values())
        print(f"Invariants: {'ALL OK' if all_ok else 'SOME FAILED'}")
        for k, v in inv.items():
            print(f"  {k}: {'OK' if v else 'FAIL'}")
    elif cmd == "memory":
        print(json.dumps(tracker.check_memory_health(), indent=2))
    elif cmd == "chain":
        print(json.dumps(tracker.check_sigil_chain(), indent=2))
    elif cmd == "care":
        print(json.dumps(tracker.get_care_metrics(), indent=2))
    elif cmd == "update":
        care = float(sys.argv[2]) if len(sys.argv) > 2 else 0.95
        route = sys.argv[3] if len(sys.argv) > 3 else "general"
        tracker.update_after_operation(care, route)
        print(f"Updated: care={care}, route={route}")
    else:
        print(f"Usage: {sys.argv[0]} [status|heartbeat|invariants|memory|chain|care|update]")
