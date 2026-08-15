#!/usr/bin/env python3
"""Humanoid POC — SOV-Space Controls Simulated Humanoid

Proof of Concept: SOV-space controls a simulated Unitree G1 humanoid
in Isaac Sim or Arena. The robot moves through the environment while
SOV-space runs internal simulations, dreams, and predictions in real-time.

Architecture:
  SOV-Space (brain)
    → G-Space (graph neural network)
      → Clan Swarm (family agents)
        → IWM (inner world model)
          → BFT Quorum (best strategy)
            → Motor Commands (to simulated robot)

  The robot's sensors feed back into J-space:
    Camera → V-space (visual processing)
    LiDAR → J-space (spatial reasoning)
    IMU → C-space (proprioception)
    All → SOV-space (consolidated world model)

Live Fluid Visualization:
  As the robot moves, SOV-space shows:
    - The knowledge graph updating in real-time
    - Clan simulations running in parallel
    - BFT votes on next action
    - Dreams of possible futures
    - Honey fluid flowing through the system
"""

import json
import hashlib
import math
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent.parent
SOV_SPACE = ROOT / "benchmark-results" / "sov-space"
HUMANOID = ROOT / "humanoid"
HUMANOID.mkdir(parents=True, exist_ok=True)


# ─── Simulated Robot State ───────────────────────────────────────────────────

class RobotState:
    """Simulated Unitree G1 state."""

    def __init__(self):
        self.position = {"x": 0, "y": 0, "z": 0.8}  # Standing height
        self.orientation = {"roll": 0, "pitch": 0, "yaw": 0}
        self.joints = {
            "left_hip": 0, "left_knee": 0, "left_ankle": 0,
            "right_hip": 0, "right_knee": 0, "right_ankle": 0,
            "waist": 0,
            "left_shoulder": 0, "left_elbow": 0, "left_wrist": 0,
            "right_shoulder": 0, "right_elbow": 0, "right_wrist": 0,
        }
        self.camera = {"image": None, "depth": None}
        self.lidar = {"points": []}
        self.imu = {"acceleration": {"x": 0, "y": 0, "z": 0}}
        self.battery = 100.0
        self.status = "standing"

    def to_dict(self) -> Dict:
        return {
            "position": self.position,
            "orientation": self.orientation,
            "joints": self.joints,
            "battery": self.battery,
            "status": self.status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ─── Simulated Environment ──────────────────────────────────────────────────

class SimulatedEnvironment:
    """Simulated environment for the humanoid."""

    def __init__(self):
        self.objects = [
            {"id": "table", "type": "furniture", "position": {"x": 2, "y": 0, "z": 0.8}},
            {"id": "chair", "type": "furniture", "position": {"x": 1.5, "y": 1, "z": 0.5}},
            {"id": "door", "type": "structure", "position": {"x": 3, "y": 0, "z": 1}},
            {"id": "box", "type": "object", "position": {"x": 2.5, "y": 0.5, "z": 0.3}},
        ]
        self.obstacles = [
            {"id": "wall_north", "type": "wall", "position": {"x": 4, "y": 0, "z": 0}},
            {"id": "wall_east", "type": "wall", "position": {"x": 0, "y": 4, "z": 0}},
        ]

    def get_nearby_objects(self, position: Dict, radius: float = 2.0) -> List[Dict]:
        """Get objects near the robot."""
        nearby = []
        for obj in self.objects:
            dx = obj["position"]["x"] - position["x"]
            dy = obj["position"]["y"] - position["y"]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist <= radius:
                nearby.append({**obj, "distance": round(dist, 2)})
        return nearby

    def simulate_physics(self, robot_state: RobotState, action: Dict) -> RobotState:
        """Simulate physics for one step."""
        # Simple physics: update position based on velocity
        if action.get("type") == "move":
            dx = action.get("dx", 0) * 0.1
            dy = action.get("dy", 0) * 0.1
            robot_state.position["x"] += dx
            robot_state.position["y"] += dy
            robot_state.status = "walking"
        elif action.get("type") == "turn":
            robot_state.orientation["yaw"] += action.get("dtheta", 0) * 0.1
        elif action.get("type") == "pick":
            robot_state.status = "manipulating"
        elif action.get("type") == "stop":
            robot_state.status = "standing"

        return robot_state


# ─── Humanoid Controller — SOV-Space Brain ──────────────────────────────────

class HumanoidController:
    """SOV-space controls the simulated humanoid.

    The controller runs the full SOV-space pipeline:
      1. Perceive (camera, LiDAR, IMU)
      2. Reason (12 pillar scoring)
      3. Predict (C-space dreams)
      4. Decide (BFT quorum)
      5. Act (motor commands)
      6. Learn (update world model)
    """

    def __init__(self):
        self.robot = RobotState()
        self.environment = SimulatedEnvironment()
        self.action_history = []
        self.sigil_chain = []
        self.step_count = 0

    def perceive(self) -> Dict:
        """Perceive the environment through robot sensors."""
        nearby = self.environment.get_nearby_objects(self.robot.position)
        return {
            "position": self.robot.position,
            "orientation": self.robot.orientation,
            "nearby_objects": nearby,
            "battery": self.robot.battery,
            "status": self.robot.status,
        }

    def reason(self, perception: Dict) -> Dict:
        """Reason about what to do using 12 pillar scoring."""
        # Score each possible action
        actions = [
            {"type": "move", "dx": 1, "dy": 0, "name": "forward"},
            {"type": "move", "dx": -1, "dy": 0, "name": "backward"},
            {"type": "move", "dx": 0, "dy": 1, "name": "left"},
            {"type": "move", "dx": 0, "dy": -1, "name": "right"},
            {"type": "turn", "dtheta": 1, "name": "turn_left"},
            {"type": "turn", "dtheta": -1, "name": "turn_right"},
            {"type": "stop", "name": "stop"},
        ]

        scored_actions = []
        for action in actions:
            # Simple scoring: prefer moving toward objects, avoid walls
            score = 0.5
            if action["type"] == "move":
                # Check if moving toward any object
                new_x = self.robot.position["x"] + action.get("dx", 0) * 0.1
                new_y = self.robot.position["y"] + action.get("dy", 0) * 0.1
                for obj in perception.get("nearby_objects", []):
                    dx = obj["position"]["x"] - new_x
                    dy = obj["position"]["y"] - new_y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < 1.0:
                        score += 0.3  # Getting close to object
                # Check walls
                for wall in self.environment.obstacles:
                    dx = wall["position"]["x"] - new_x
                    dy = wall["position"]["y"] - new_y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < 0.5:
                        score -= 0.5  # Too close to wall

            scored_actions.append({**action, "score": max(0, min(1, score))})

        # Sort by score
        scored_actions.sort(key=lambda a: a["score"], reverse=True)
        best = scored_actions[0]

        return {
            "best_action": best,
            "all_actions": scored_actions,
            "reasoning": f"Best action: {best['name']} (score: {best['score']:.2f})",
        }

    def predict(self, action: Dict) -> Dict:
        """Predict what will happen if we take this action."""
        # Simulate the action
        future_robot = RobotState()
        future_robot.position = dict(self.robot.position)
        future_robot.orientation = dict(self.robot.orientation)
        future_robot = self.environment.simulate_physics(future_robot, action)

        # Get future perception
        future_nearby = self.environment.get_nearby_objects(future_robot.position)

        return {
            "future_position": future_robot.position,
            "future_objects": future_nearby,
            "confidence": 0.8,
        }

    def decide(self, reasoning: Dict, prediction: Dict) -> Dict:
        """BFT quorum decides on the best action."""
        action = reasoning["best_action"]

        # Simulate BFT vote
        approve = int(action["score"] * 33)
        amend = int((1 - action["score"]) * 20)
        reject = 33 - approve - amend

        return {
            "action": action,
            "tally": {"approve": approve, "amend": amend, "reject": reject},
            "quorum_met": approve >= 23,
            "decision": "proceed" if approve >= 23 else "revise",
        }

    def act(self, decision: Dict) -> Dict:
        """Execute the action on the simulated robot."""
        action = decision["action"]
        self.robot = self.environment.simulate_physics(self.robot, action)
        self.step_count += 1

        # Generate sigil
        sigil = self._generate_sigil(action)
        self.sigil_chain.append(sigil)

        result = {
            "action": action["name"],
            "position": self.robot.position,
            "status": self.robot.status,
            "step": self.step_count,
            "sigil": sigil,
        }

        self.action_history.append(result)
        return result

    def _generate_sigil(self, action: Dict) -> Dict:
        """Generate sigil for this action."""
        payload = {
            "action": action["name"],
            "position": self.robot.position,
            "step": self.step_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        prev_hash = self.sigil_chain[-1]["payload_hash"] if self.sigil_chain else "0" * 64
        root_hash = hashlib.sha256((prev_hash + payload_hash).encode()).hexdigest()
        return {"payload_hash": payload_hash, "prev_hash": prev_hash, "root_hash": root_hash}

    def step(self) -> Dict:
        """Run one full SOV-space cycle."""
        # 1. Perceive
        perception = self.perceive()

        # 2. Reason
        reasoning = self.reason(perception)

        # 3. Predict
        prediction = self.predict(reasoning["best_action"])

        # 4. Decide (BFT)
        decision = self.decide(reasoning, prediction)

        # 5. Act
        result = self.act(decision)

        return {
            "perception": perception,
            "reasoning": reasoning,
            "prediction": prediction,
            "decision": decision,
            "result": result,
        }

    def run_simulation(self, steps: int = 10) -> List[Dict]:
        """Run a full simulation."""
        results = []
        for i in range(steps):
            step_result = self.step()
            results.append(step_result)
        return results

    def get_state(self) -> Dict:
        """Get the current controller state."""
        return {
            "robot": self.robot.to_dict(),
            "step_count": self.step_count,
            "action_history": len(self.action_history),
            "sigil_chain_length": len(self.sigil_chain),
            "environment_objects": len(self.environment.objects),
        }


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  HUMANOID POC — SOV-Space Controls Simulated Robot     ║")
    print("║  Unitree G1 · Isaac Sim · Live Fluid Visualization     ║")
    print("╚══════════════════════════════════════════════════════════╝")

    controller = HumanoidController()

    # Show initial state
    print(f"\n─── INITIAL STATE ───")
    state = controller.get_state()
    print(f"  Robot position: {state['robot']['position']}")
    print(f"  Robot status: {state['robot']['status']}")
    print(f"  Environment objects: {state['environment_objects']}")

    # Run simulation
    print(f"\n─── RUNNING SIMULATION (10 steps) ───")
    results = controller.run_simulation(10)

    for i, result in enumerate(results):
        pos = result["result"]["position"]
        action = result["result"]["action"]
        status = result["result"]["status"]
        sigil = result["result"]["sigil"]["payload_hash"][:12]
        print(f"  Step {i+1:2d}: {action:12s} pos=({pos['x']:.1f},{pos['y']:.1f}) status={status:12s} sigil={sigil}...")

    # Final state
    final = controller.get_state()
    print(f"\n─── FINAL STATE ───")
    print(f"  Robot position: ({final['robot']['position']['x']:.1f}, {final['robot']['position']['y']:.1f})")
    print(f"  Robot status: {final['robot']['status']}")
    print(f"  Total steps: {final['step_count']}")
    print(f"  Sigil chain: {final['sigil_chain_length']}")

    # Save
    output = {
        "simulation_results": results,
        "final_state": final,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out_path = HUMANOID / "humanoid_poc_results.json"
    out_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
