"""
G-SPACE: Knowledge Graph + GNN for Clan Routing

The G-space contains:
1. Knowledge Graph — nodes are families, edges are capability relationships
2. GNN — learns routing patterns from arena outcomes
3. Win pattern memory — tracks which family beats which competitor type

This is the brain of the swarm — it decides which clan to route to.
"""
import json, hashlib, math
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
EAT_DIR = ROOT / "eat_results"
IWM_DIR = ROOT / "iwms"
IWM_DIR.mkdir(exist_ok=True)

FAMILIES = [
    "qwen", "deepseek", "llama", "mistral", "gemma", "phi", "gpt-oss",
    "code", "vision", "embedding", "qwen-vision", "MiniMax", "nemotron",
    "core", "research", "arch", "compliance", "distribution", "infra"
]

CAPABILITY_DIMS = [
    "reasoning", "coding", "multilingual", "vision", "math",
    "instruction_following", "safety", "speed", "context_length",
    "tool_use", "creative_writing", "knowledge", "edge_deploy"
]

FAMILY_CAPABILITIES = {
    "qwen":          {"reasoning": 0.85, "coding": 0.80, "multilingual": 0.95, "vision": 0.70, "math": 0.85, "instruction_following": 0.90, "safety": 0.80, "speed": 0.75, "context_length": 0.85, "tool_use": 0.85, "creative_writing": 0.75, "knowledge": 0.85, "edge_deploy": 0.60},
    "deepseek":      {"reasoning": 0.95, "coding": 0.90, "multilingual": 0.80, "vision": 0.50, "math": 0.95, "instruction_following": 0.85, "safety": 0.75, "speed": 0.70, "context_length": 0.90, "tool_use": 0.80, "creative_writing": 0.70, "knowledge": 0.90, "edge_deploy": 0.50},
    "llama":         {"reasoning": 0.80, "coding": 0.75, "multilingual": 0.85, "vision": 0.65, "math": 0.75, "instruction_following": 0.85, "safety": 0.90, "speed": 0.80, "context_length": 0.95, "tool_use": 0.80, "creative_writing": 0.80, "knowledge": 0.80, "edge_deploy": 0.70},
    "mistral":       {"reasoning": 0.80, "coding": 0.85, "multilingual": 0.90, "vision": 0.55, "math": 0.80, "instruction_following": 0.85, "safety": 0.80, "speed": 0.85, "context_length": 0.85, "tool_use": 0.80, "creative_writing": 0.75, "knowledge": 0.80, "edge_deploy": 0.75},
    "gemma":         {"reasoning": 0.75, "coding": 0.70, "multilingual": 0.80, "vision": 0.80, "math": 0.75, "instruction_following": 0.80, "safety": 0.95, "speed": 0.85, "context_length": 0.80, "tool_use": 0.75, "creative_writing": 0.70, "knowledge": 0.75, "edge_deploy": 0.85},
    "phi":           {"reasoning": 0.75, "coding": 0.80, "multilingual": 0.65, "vision": 0.50, "math": 0.80, "instruction_following": 0.80, "safety": 0.85, "speed": 0.95, "context_length": 0.70, "tool_use": 0.70, "creative_writing": 0.65, "knowledge": 0.70, "edge_deploy": 0.95},
    "gpt-oss":       {"reasoning": 0.80, "coding": 0.80, "multilingual": 0.80, "vision": 0.55, "math": 0.80, "instruction_following": 0.85, "safety": 0.80, "speed": 0.80, "context_length": 0.80, "tool_use": 0.80, "creative_writing": 0.75, "knowledge": 0.80, "edge_deploy": 0.70},
    "code":          {"reasoning": 0.75, "coding": 0.95, "multilingual": 0.60, "vision": 0.40, "math": 0.75, "instruction_following": 0.80, "safety": 0.70, "speed": 0.80, "context_length": 0.85, "tool_use": 0.90, "creative_writing": 0.50, "knowledge": 0.75, "edge_deploy": 0.70},
    "vision":        {"reasoning": 0.70, "coding": 0.60, "multilingual": 0.70, "vision": 0.95, "math": 0.65, "instruction_following": 0.75, "safety": 0.80, "speed": 0.75, "context_length": 0.75, "tool_use": 0.70, "creative_writing": 0.65, "knowledge": 0.70, "edge_deploy": 0.65},
    "embedding":     {"reasoning": 0.50, "coding": 0.40, "multilingual": 0.85, "vision": 0.30, "math": 0.40, "instruction_following": 0.40, "safety": 0.70, "speed": 0.95, "context_length": 0.90, "tool_use": 0.50, "creative_writing": 0.30, "knowledge": 0.60, "edge_deploy": 0.90},
    "qwen-vision":   {"reasoning": 0.80, "coding": 0.70, "multilingual": 0.90, "vision": 0.90, "math": 0.80, "instruction_following": 0.85, "safety": 0.80, "speed": 0.70, "context_length": 0.80, "tool_use": 0.80, "creative_writing": 0.70, "knowledge": 0.80, "edge_deploy": 0.55},
    "MiniMax":       {"reasoning": 0.80, "coding": 0.75, "multilingual": 0.75, "vision": 0.55, "math": 0.80, "instruction_following": 0.80, "safety": 0.75, "speed": 0.85, "context_length": 0.80, "tool_use": 0.75, "creative_writing": 0.75, "knowledge": 0.75, "edge_deploy": 0.70},
    "nemotron":      {"reasoning": 0.85, "coding": 0.80, "multilingual": 0.75, "vision": 0.60, "math": 0.85, "instruction_following": 0.85, "safety": 0.80, "speed": 0.80, "context_length": 0.80, "tool_use": 0.80, "creative_writing": 0.70, "knowledge": 0.80, "edge_deploy": 0.70},
    "core":          {"reasoning": 0.80, "coding": 0.50, "multilingual": 0.70, "vision": 0.40, "math": 0.60, "instruction_following": 0.70, "safety": 0.95, "speed": 0.60, "context_length": 0.70, "tool_use": 0.50, "creative_writing": 0.60, "knowledge": 0.90, "edge_deploy": 0.50},
    "research":      {"reasoning": 0.90, "coding": 0.70, "multilingual": 0.70, "vision": 0.50, "math": 0.85, "instruction_following": 0.75, "safety": 0.85, "speed": 0.60, "context_length": 0.75, "tool_use": 0.65, "creative_writing": 0.70, "knowledge": 0.95, "edge_deploy": 0.45},
    "arch":          {"reasoning": 0.85, "coding": 0.75, "multilingual": 0.65, "vision": 0.50, "math": 0.80, "instruction_following": 0.70, "safety": 0.80, "speed": 0.65, "context_length": 0.75, "tool_use": 0.70, "creative_writing": 0.60, "knowledge": 0.85, "edge_deploy": 0.55},
    "compliance":    {"reasoning": 0.75, "coding": 0.45, "multilingual": 0.70, "vision": 0.35, "math": 0.55, "instruction_following": 0.80, "safety": 0.95, "speed": 0.55, "context_length": 0.65, "tool_use": 0.50, "creative_writing": 0.55, "knowledge": 0.90, "edge_deploy": 0.45},
    "distribution":  {"reasoning": 0.65, "coding": 0.70, "multilingual": 0.65, "vision": 0.45, "math": 0.60, "instruction_following": 0.65, "safety": 0.70, "speed": 0.80, "context_length": 0.70, "tool_use": 0.70, "creative_writing": 0.50, "knowledge": 0.75, "edge_deploy": 0.85},
    "infra":         {"reasoning": 0.70, "coding": 0.80, "multilingual": 0.60, "vision": 0.40, "math": 0.65, "instruction_following": 0.70, "safety": 0.75, "speed": 0.85, "context_length": 0.70, "tool_use": 0.80, "creative_writing": 0.50, "knowledge": 0.80, "edge_deploy": 0.80},
}


class GSpace:
    """G-space: Knowledge Graph + GNN for clan routing."""

    def __init__(self):
        self.graph = self._build_graph()
        self.win_memory = self._load_win_memory()
        self.routing_table = {}
        self.gnn_weights = self._init_gnn()

    def _build_graph(self):
        """Build knowledge graph with families as nodes and capability similarity as edges."""
        graph = {"nodes": {}, "edges": []}
        for fam in FAMILIES:
            caps = FAMILY_CAPABILITIES.get(fam, {})
            graph["nodes"][fam] = {
                "family": fam,
                "capabilities": caps,
                "eat_entries": self._count_eat(fam),
                "win_rate": 0.5,
                "loss_rate": 0.5,
                "matches": 0,
            }
        # Build edges based on capability similarity
        for i, f1 in enumerate(FAMILIES):
            for j, f2 in enumerate(FAMILIES):
                if i >= j:
                    continue
                c1 = FAMILY_CAPABILITIES.get(f1, {})
                c2 = FAMILY_CAPABILITIES.get(f2, {})
                sim = self._cosine_sim(c1, c2)
                if sim > 0.7:
                    graph["edges"].append({
                        "from": f1, "to": f2,
                        "similarity": sim,
                        "type": "capability_overlap"
                    })
        return graph

    def _cosine_sim(self, c1, c2):
        """Cosine similarity between two capability vectors."""
        keys = set(c1.keys()) & set(c2.keys())
        if not keys:
            return 0.0
        dot = sum(c1[k] * c2[k] for k in keys)
        n1 = math.sqrt(sum(c1[k] ** 2 for k in keys))
        n2 = math.sqrt(sum(c2[k] ** 2 for k in keys))
        if n1 == 0 or n2 == 0:
            return 0.0
        return dot / (n1 * n2)

    def _count_eat(self, family):
        """Count EAT entries for a family."""
        path = EAT_DIR / f"extract_{family}.json"
        if path.exists():
            try:
                return len(json.loads(path.read_text()))
            except Exception:
                return 0
        return 0

    def _init_gnn(self):
        """Initialize GNN weights (simplified: 2-layer message passing)."""
        return {
            "layer1": {"W": [[0.1] * len(CAPABILITY_DIMS)] * len(CAPABILITY_DIMS), "b": [0.0] * len(CAPABILITY_DIMS)},
            "layer2": {"W": [[0.1] * len(CAPABILITY_DIMS)] * len(CAPABILITY_DIMS), "b": [0.0] * len(CAPABILITY_DIMS)},
            "routing_bias": {fam: 0.0 for fam in FAMILIES},
        }

    def _load_win_memory(self):
        """Load win/loss memory from previous arena outcomes."""
        path = IWM_DIR / "win_memory.json"
        if path.exists():
            try:
                return json.loads(path.read_text())
            except Exception:
                pass
        return {"matches": [], "family_win_rates": {}, "competitor_patterns": {}}

    def save_win_memory(self):
        path = IWM_DIR / "win_memory.json"
        path.write_text(json.dumps(self.win_memory, indent=2))

    def route(self, task_description, competitor_type=None):
        """Route a task to the best clan(s) using GNN scoring."""
        task_caps = self._infer_task_capabilities(task_description)
        scores = {}
        for fam in FAMILIES:
            caps = FAMILY_CAPABILITIES.get(fam, {})
            # Base score: capability match
            cap_score = sum(task_caps.get(k, 0) * caps.get(k, 0) for k in CAPABILITY_DIMS)
            # Win rate bonus
            win_bonus = self.gnn_weights["routing_bias"].get(fam, 0.0)
            # Competitor pattern bonus
            comp_bonus = 0.0
            if competitor_type and competitor_type in self.win_memory.get("competitor_patterns", {}):
                pattern = self.win_memory["competitor_patterns"][competitor_type]
                comp_bonus = pattern.get(fam, 0.0)
            scores[fam] = cap_score + win_bonus + comp_bonus
        # Sort by score descending
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked

    def _infer_task_capabilities(self, description):
        """Infer required capabilities from task description."""
        desc = description.lower()
        caps = {}
        if any(w in desc for w in ["reason", "logic", "think", "analyz"]):
            caps["reasoning"] = 0.9
        if any(w in desc for w in ["code", "program", "implement", "debug"]):
            caps["coding"] = 0.9
        if any(w in desc for w in ["translat", "multilingual", "language"]):
            caps["multilingual"] = 0.9
        if any(w in desc for w in ["image", "vision", "visual", "photo"]):
            caps["vision"] = 0.9
        if any(w in desc for w in ["math", "calculat", "equation"]):
            caps["math"] = 0.9
        if any(w in desc for w in ["instruct", "follow", "command"]):
            caps["instruction_following"] = 0.8
        if any(w in desc for w in ["safe", "harm", "danger"]):
            caps["safety"] = 0.9
        if any(w in desc for w in ["fast", "speed", "quick", "real-time"]):
            caps["speed"] = 0.9
        if any(w in desc for w in ["long", "document", "context", "book"]):
            caps["context_length"] = 0.9
        if any(w in desc for w in ["tool", "function", "api", "call"]):
            caps["tool_use"] = 0.9
        if any(w in desc for w in ["write", "story", "creative", "poem"]):
            caps["creative_writing"] = 0.9
        if any(w in desc for w in ["fact", "knowledge", "information"]):
            caps["knowledge"] = 0.9
        if any(w in desc for w in ["edge", "mobile", "embed", "light"]):
            caps["edge_deploy"] = 0.9
        if not caps:
            caps = {k: 0.5 for k in CAPABILITY_DIMS}
        return caps

    def record_outcome(self, family, competitor, won, task_description):
        """Record an arena outcome and update GNN weights."""
        outcome = {
            "family": family,
            "competitor": competitor,
            "won": won,
            "task": task_description,
            "timestamp": datetime.now().isoformat(),
        }
        self.win_memory["matches"].append(outcome)
        # Update family win rates
        if family not in self.win_memory["family_win_rates"]:
            self.win_memory["family_win_rates"][family] = {"wins": 0, "losses": 0}
        if won:
            self.win_memory["family_win_rates"][family]["wins"] += 1
        else:
            self.win_memory["family_win_rates"][family]["losses"] += 1
        # Update competitor patterns
        if competitor not in self.win_memory["competitor_patterns"]:
            self.win_memory["competitor_patterns"][competitor] = {}
        if family not in self.win_memory["competitor_patterns"][competitor]:
            self.win_memory["competitor_patterns"][competitor][family] = 0.0
        # Adjust routing bias (gradient-like update)
        delta = 0.05 if won else -0.05
        self.gnn_weights["routing_bias"][family] = self.gnn_weights["routing_bias"].get(family, 0.0) + delta
        self.win_memory["competitor_patterns"][competitor][family] += delta
        self.save_win_memory()

    def get_topology(self):
        """Return graph topology for visualization."""
        return {
            "nodes": len(self.graph["nodes"]),
            "edges": len(self.graph["edges"]),
            "families": FAMILIES,
            "capability_dims": CAPABILITY_DIMS,
            "total_eat": sum(n["eat_entries"] for n in self.graph["nodes"].values()),
            "total_matches": len(self.win_memory.get("matches", [])),
        }
