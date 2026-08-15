#!/usr/bin/env python3
"""5D Infinite Drawing — SOV-Space in Unreal Engine 5

Five dimensions of SOV-space rendered as an infinite drawing:
  X, Y, Z — spatial position in 3D space
  Time — animation/keyframes (Sequencer)
  Depth — zoom level (World Partition streaming)

Each OWEM family occupies a region of 5D space.
Each knowledge entry is a particle (Niagara).
Each dream is a branching tree.
Each action is a node in the graph.

The infinite drawing uses:
  Nanite — infinite geometry detail
  Lumen — real-time lighting
  World Partition — infinite world streaming
  PCG — procedural content generation
  Niagara — particle systems for data points
  Sequencer — temporal dimension
"""

import json
import math
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent.parent
SOV_SPACE = ROOT / "benchmark-results" / "sov-space"


# ─── 5D Coordinate System ────────────────────────────────────────────────────

class Coord5D:
    """A point in 5D SOV-space."""

    def __init__(self, x: float = 0, y: float = 0, z: float = 0,
                 t: float = 0, d: float = 0):
        self.x = x  # Spatial X (left-right)
        self.y = y  # Spatial Y (forward-back)
        self.z = z  # Spatial Z (up-down)
        self.t = t  # Time (0-1 normalized)
        self.d = d  # Depth/Zoom (0=far, 1=close)

    def to_dict(self) -> Dict:
        return {"x": self.x, "y": self.y, "z": self.z, "t": self.t, "d": self.d}

    def distance_5d(self, other: "Coord5D") -> float:
        """5D Euclidean distance."""
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2 +
            (self.t - other.t) ** 2 +
            (self.d - other.d) ** 2
        )


# ─── 5D Family Layout ────────────────────────────────────────────────────────

FAMILY_POSITIONS = {
    "abstraction":    Coord5D(0, 0, 0, 0, 0.5),
    "aesthetics":     Coord5D(1, 0, 0, 0.1, 0.5),
    "agency":         Coord5D(2, 0, 0, 0.2, 0.5),
    "care":           Coord5D(0, 1, 0, 0.3, 0.5),
    "creation":       Coord5D(1, 1, 0, 0.4, 0.5),
    "destruction":    Coord5D(2, 1, 0, 0.5, 0.5),
    "embodiment":     Coord5D(0, 2, 0, 0.6, 0.5),
    "ethics":         Coord5D(1, 2, 0, 0.7, 0.5),
    "identity":       Coord5D(2, 2, 0, 0.8, 0.5),
    "logic":          Coord5D(0.5, 0.5, 1, 0.9, 0.7),
    "preservation":   Coord5D(1.5, 0.5, 1, 0.95, 0.7),
    "relationality":  Coord5D(1, 1, 2, 1.0, 0.9),
}

FAMILY_COLORS = {
    "abstraction": "#00d4ff",
    "aesthetics": "#ff6bcb",
    "agency": "#00ff88",
    "care": "#ffaa00",
    "creation": "#7b2ff7",
    "destruction": "#ff4444",
    "embodiment": "#44ccff",
    "ethics": "#aa66ff",
    "identity": "#00d4ff",
    "logic": "#88aacc",
    "preservation": "#44cc88",
    "relationality": "#ff88cc",
}


class InfiniteDrawing:
    """5D Infinite Drawing for SOV-space in UE5."""

    def __init__(self):
        self.nodes = []  # Knowledge entries as 5D points
        self.edges = []  # Connections between nodes
        self.families = {}  # Family regions
        self.dreams = []  # Dream branches
        self.actions = []  # B-Space actions

    def add_node(self, family: str, content: str, coord: Coord5D = None):
        """Add a knowledge node to the 5D space."""
        if coord is None:
            base = FAMILY_POSITIONS.get(family, Coord5D(0, 0, 0, 0, 0))
            # Add jitter for multiple entries in same family
            import random
            random.seed(hash(content))
            coord = Coord5D(
                base.x + random.uniform(-0.3, 0.3),
                base.y + random.uniform(-0.3, 0.3),
                base.z + random.uniform(-0.1, 0.1),
                base.t + random.uniform(-0.05, 0.05),
                base.d + random.uniform(-0.1, 0.1),
            )

        node = {
            "id": len(self.nodes),
            "family": family,
            "content": content[:100],
            "coord": coord.to_dict(),
            "color": FAMILY_COLORS.get(family, "#ffffff"),
            "size": 0.5 + coord.d * 0.5,  # Closer = bigger
        }
        self.nodes.append(node)
        return node

    def add_edge(self, from_id: int, to_id: int, relation: str = ""):
        """Add a connection between nodes."""
        edge = {
            "from": from_id,
            "to": to_id,
            "relation": relation,
        }
        self.edges.append(edge)

    def add_dream(self, scenario: str, branches: List[Dict]):
        """Add a dream as a branching tree."""
        dream = {
            "scenario": scenario,
            "branches": branches,
            "coord": Coord5D(1.5, 1.5, 1.5, 0.5, 0.8).to_dict(),
        }
        self.dreams.append(dream)

    def add_action(self, agent_id: str, action_type: str, coord: Coord5D):
        """Add a B-Space action."""
        action = {
            "agent_id": agent_id,
            "type": action_type,
            "coord": coord.to_dict(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.actions.append(action)

    def to_ue5_blueprint(self) -> str:
        """Generate UE5 Blueprint code for rendering the 5D drawing."""
        bp = """// 5D Infinite Drawing — SOV-Space Blueprint
// Generated by sov5d_drawing.py

// 1. Create Niagara System for particles
// Each node = one particle with 5D coordinates mapped to:
//   Position (X,Y,Z) = spatial coordinates
//   Color = family color
//   Size = depth (closer = bigger)
//   Age = time dimension

// 2. Create PCG Graph for procedural layout
// PCG rules:
//   - Family clusters at predefined 5D positions
//   - Knowledge density determines particle count
//   - Connections rendered as Niagara ribbons

// 3. Create Level Sequence for temporal dimension
// Sequencer timeline:
//   - Frame 0-100: Initial state
//   - Frame 100-200: Evolution cycle 1
//   - Frame 200-300: Evolution cycle 2
//   - etc.

// 4. Create Camera Blueprint for infinite zoom
// Camera controls:
//   - Mouse wheel = zoom in/out (depth dimension)
//   - WASD = move in XY plane
//   - QE = move in Z plane
//   - Timeline scrubber = time dimension

// 5. Enable World Partition for infinite streaming
// World Partition grid:
//   - Cell size: 1000 units
//   - Streaming distance: 5000 units
//   - Each cell contains family-specific data

// 6. Enable Nanite for infinite geometry detail
// Nanite settings:
//   - Virtual shadow maps: enabled
//   - Mesh density: billions of triangles
//   - Automatic LOD: per-pixel selection

// 7. Enable Lumen for real-time lighting
// Lumen settings:
//   - Global illumination: enabled
//   - Reflections: enabled
//   - Software ray tracing: enabled
"""
        return bp

    def to_niagara_data(self) -> Dict:
        """Generate Niagara particle data for UE5."""
        particles = []
        for node in self.nodes:
            particles.append({
                "position": [node["coord"]["x"] * 100, node["coord"]["y"] * 100, node["coord"]["z"] * 100],
                "color": node["color"],
                "size": node["size"] * 10,
                "velocity": [0, 0, 0],
                "lifetime": 999999,
            })
        return {
            "particle_count": len(particles),
            "particles": particles,
            "connections": self.edges,
        }

    def to_pcg_graph(self) -> Dict:
        """Generate PCG graph data for procedural layout."""
        return {
            "nodes": [
                {
                    "type": "SurfaceSampler",
                    "settings": {
                        "family": family,
                        "position": pos.to_dict(),
                        "density": len([n for n in self.nodes if n["family"] == family]),
                        "color": FAMILY_COLORS.get(family, "#ffffff"),
                    },
                }
                for family, pos in FAMILY_POSITIONS.items()
            ],
            "edges": self.edges,
        }

    def save(self, path: Path = None):
        """Save the 5D drawing."""
        if path is None:
            path = SOV_SPACE / "sov5d_drawing.json"

        data = {
            "version": "1.0.0",
            "dimensions": 5,
            "dimension_names": ["x", "y", "z", "time", "depth"],
            "nodes": self.nodes,
            "edges": self.edges,
            "dreams": self.dreams,
            "actions": self.actions,
            "families": {k: v.to_dict() for k, v in FAMILY_POSITIONS.items()},
            "colors": FAMILY_COLORS,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        path.write_text(json.dumps(data, indent=2))
        return path


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  5D INFINITE DRAWING — SOV-Space in UE5                ║")
    print("║  X, Y, Z + Time + Depth                                ║")
    print("╚══════════════════════════════════════════════════════════╝")

    drawing = InfiniteDrawing()

    # Load knowledge
    bloodline = json.load(open(ROOT / "forest" / "bloodline.json"))
    knowledge = bloodline.get("knowledge", [])

    print(f"\n─── ADDING KNOWLEDGE NODES ───")
    for entry in knowledge:
        family = entry.get("family", "unknown")
        content = entry.get("content", "")
        drawing.add_node(family, content)

    print(f"  Total nodes: {len(drawing.nodes)}")

    # Add connections
    print(f"\n─── ADDING CONNECTIONS ───")
    for i in range(len(drawing.nodes) - 1):
        if drawing.nodes[i]["family"] == drawing.nodes[i + 1]["family"]:
            drawing.add_edge(i, i + 1, "same_family")

    print(f"  Total edges: {len(drawing.edges)}")

    # Load dreams
    cspace = SOV_SPACE / "cspace_dreams.json"
    if cspace.exists():
        dreams = json.load(open(cspace)).get("dreams", [])
        for dream in dreams:
            drawing.add_dream(dream["scenario"], dream.get("branches", []))
        print(f"  Dreams: {len(dreams)}")

    # Save
    path = drawing.save()
    print(f"\n─── OUTPUT ───")
    print(f"  Saved: {path}")
    print(f"  Nodes: {len(drawing.nodes)}")
    print(f"  Edges: {len(drawing.edges)}")
    print(f"  Dreams: {len(drawing.dreams)}")
    print(f"  Actions: {len(drawing.actions)}")

    # Generate Niagara data
    niagara = drawing.to_niagara_data()
    niagara_path = SOV_SPACE / "sov5d_niagara.json"
    niagara_path.write_text(json.dumps(niagara, indent=2))
    print(f"  Niagara data: {niagara_path}")

    # Generate PCG graph
    pcg = drawing.to_pcg_graph()
    pcg_path = SOV_SPACE / "sov5d_pcg.json"
    pcg_path.write_text(json.dumps(pcg, indent=2))
    print(f"  PCG graph: {pcg_path}")


if __name__ == "__main__":
    main()
