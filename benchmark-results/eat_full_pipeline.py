#!/usr/bin/env python3
"""SOV33 EAT Full Pipeline — V-Space → C-Space → Sov-Space → Visual Honey.

The fluid visual docstore that grows as we operate.
No frozen data. No training from scratch. Just piggybacking on 12 AI families.

Architecture:
  Query → 12 OWEM Router → J-Space (per-model output) → V-Space (visual artifacts)
  → C-Space (creative simulation) → Sov-Space (unified visual honey) → Display

Every output becomes a J-space entry.
Every J-space entry becomes a V-space artifact.
Every V-space artifact gets simulated in C-space.
Everything accumulates in Sov-space as visual honey.
"""
import json, time, hashlib, os, re, urllib.request
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

WORKSPACE = Path(os.environ.get("SOV_WORKSPACE", "/tmp"))

# ============================================================
# API KEYS
# ============================================================
API_KEYS = {
    "nvidia": os.environ.get("NVIDIA_API_KEY", "__NVAPI_KEY__"),
    "gemini": os.environ.get("GOOGLE_API_KEY", "__GEMINI_KEY__"),
}

# ============================================================
# 12 OWEM FAMILIES (the 12-around-1)
# ============================================================
OWEM_FAMILIES = {
    "logic": {"model": "meta/llama-3.1-70b-instruct", "provider": "nvidia", "pillar": "justice"},
    "ethics": {"model": "meta/llama-3.1-70b-instruct", "provider": "nvidia", "pillar": "honor"},
    "aesthetics": {"model": "gemini-2.5-flash", "provider": "gemini", "pillar": "openness"},
    "temporality": {"model": "meta/llama-3.1-70b-instruct", "provider": "nvidia", "pillar": "continuity"},
    "identity": {"model": "meta/llama-3.1-70b-instruct", "provider": "nvidia", "pillar": "sovereignty"},
    "agency": {"model": "gemini-2.5-flash", "provider": "gemini", "pillar": "guidance"},
    "relationality": {"model": "meta/llama-3.1-70b-instruct", "provider": "nvidia", "pillar": "equity"},
    "embodiment": {"model": "gemini-2.5-flash", "provider": "gemini", "pillar": "safety"},
    "abstraction": {"model": "meta/llama-3.1-70b-instruct", "provider": "nvidia", "pillar": "verifiability"},
    "synthesis": {"model": "gemini-2.5-flash", "provider": "gemini", "pillar": "transparency"},
    "destruction": {"model": "meta/llama-3.1-70b-instruct", "provider": "nvidia", "pillar": "resilience"},
    "preservation": {"model": "gemini-2.5-flash", "provider": "gemini", "pillar": "auditability"},
}

# ============================================================
# J-SPACE (per-model output storage)
# ============================================================
@dataclass
class JEntry:
    """Single entry in J-space — output from one OWEM model."""
    id: str
    owem: str
    model: str
    pillar: str
    query: str
    response: str
    reasoning_chain: List[str]
    timestamp: str
    care_score: float
    sigil: str

class JSpace:
    """J-Space: per-model text/reasoning output storage."""
    
    def __init__(self, path: Path = None):
        self.path = path or WORKSPACE / "j-space"
        self.path.mkdir(parents=True, exist_ok=True)
        self.entries: List[JEntry] = []
    
    def add(self, owem: str, model: str, pillar: str, query: str, response: str, care_score: float = 0.95) -> JEntry:
        """Add a new J-space entry from an OWEM model output."""
        entry_id = f"j-{int(time.time()*1000)}-{hashlib.md5(response.encode()).hexdigest()[:6]}"
        
        # Extract reasoning chain from response
        reasoning_chain = self._extract_reasoning(response)
        
        # Generate SIGIL
        sigil = hashlib.sha256(f"{entry_id}|{model}|{query}|{response}".encode()).hexdigest()[:16]
        
        entry = JEntry(
            id=entry_id,
            owem=owem,
            model=model,
            pillar=pillar,
            query=query,
            response=response,
            reasoning_chain=reasoning_chain,
            timestamp=datetime.now(timezone.utc).isoformat(),
            care_score=care_score,
            sigil=sigil,
        )
        
        self.entries.append(entry)
        
        # Persist to disk
        entry_path = self.path / f"{entry_id}.json"
        entry_path.write_text(json.dumps(entry.__dict__, indent=2))
        
        return entry
    
    def _extract_reasoning(self, text: str) -> List[str]:
        """Extract reasoning steps from text."""
        steps = []
        # Look for numbered steps
        for match in re.finditer(r'(\d+)[\.\)]\s*(.+?)(?=\d+[\.\)]|$)', text, re.DOTALL):
            steps.append(match.group(2).strip())
        # Look for "because", "therefore", "thus"
        for keyword in ["because", "therefore", "thus", "so"]:
            if keyword in text.lower():
                idx = text.lower().index(keyword)
                steps.append(text[idx:idx+100].strip())
        return steps[:5]  # Max 5 steps
    
    def get_all(self) -> List[JEntry]:
        return self.entries


# ============================================================
# V-SPACE (visual artifacts)
# ============================================================
@dataclass
class VArtifact:
    """Visual artifact in V-space — rendered from J-space entries."""
    id: str
    source_j_entry: str
    artifact_type: str  # card, map, chain, diagram
    content: str
    visual_html: str
    coordinates: Dict[str, float]  # 3D position on icosahedral globe
    timestamp: str

class VSpace:
    """V-Space: visual artifacts rendered from J-space outputs."""
    
    # Icosahedral pillar coordinates
    PILLAR_COORDS = {
        "honor":         {"x": 0.0, "y": 1.0, "z": 0.0},
        "safety":        {"x": 0.89, "y": 0.45, "z": 0.0},
        "guidance":      {"x": 0.28, "y": 0.45, "z": 0.85},
        "sovereignty":   {"x": -0.73, "y": 0.45, "z": 0.53},
        "resilience":    {"x": -0.73, "y": 0.45, "z": -0.53},
        "auditability":  {"x": 0.28, "y": 0.45, "z": -0.85},
        "verifiability": {"x": 0.73, "y": -0.45, "z": 0.53},
        "transparency":  {"x": -0.28, "y": -0.45, "z": 0.85},
        "justice":       {"x": -0.89, "y": -0.45, "z": 0.0},
        "equity":        {"x": -0.28, "y": -0.45, "z": -0.85},
        "openness":      {"x": 0.73, "y": -0.45, "z": -0.53},
        "continuity":    {"x": 0.0, "y": -1.0, "z": 0.0},
    }
    
    def __init__(self, path: Path = None):
        self.path = path or WORKSPACE / "v-space"
        self.path.mkdir(parents=True, exist_ok=True)
        self.artifacts: List[VArtifact] = []
    
    def render_card(self, j_entry: JEntry) -> VArtifact:
        """Render a J-space entry as a visual card artifact."""
        coords = self.PILLAR_COORDS.get(j_entry.pillar, {"x": 0, "y": 0, "z": 0})
        
        # Generate visual HTML card
        visual_html = f"""
        <div class="sov-card" style="border-left: 3px solid {self._pillar_color(j_entry.pillar)}">
            <div class="sov-card-header">
                <span class="owem">{j_entry.owem}</span>
                <span class="pillar">{j_entry.pillar}</span>
                <span class="care">{j_entry.care_score:.2f}</span>
            </div>
            <div class="sov-card-query">{j_entry.query[:100]}</div>
            <div class="sov-card-response">{j_entry.response[:200]}</div>
            <div class="sov-card-chain">
                {''.join(f'<span class="step">{s[:50]}</span>' for s in j_entry.reasoning_chain[:3])}
            </div>
            <div class="sov-card-sigil">{j_entry.sigil}</div>
        </div>
        """
        
        artifact_id = f"v-{int(time.time()*1000)}-{j_entry.id}"
        artifact = VArtifact(
            id=artifact_id,
            source_j_entry=j_entry.id,
            artifact_type="card",
            content=j_entry.response[:500],
            visual_html=visual_html,
            coordinates=coords,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        
        self.artifacts.append(artifact)
        
        # Persist
        artifact_path = self.path / f"{artifact_id}.json"
        artifact_path.write_text(json.dumps(artifact.__dict__, indent=2))
        
        return artifact
    
    def render_map(self, j_entries: List[JEntry]) -> VArtifact:
        """Render multiple J-space entries as a visual map."""
        coords_list = []
        for entry in j_entries:
            c = self.PILLAR_COORDS.get(entry.pillar, {"x": 0, "y": 0, "z": 0})
            coords_list.append({"owem": entry.owem, "pillar": entry.pillar, **c})
        
        visual_html = f"""
        <div class="sov-map">
            <h3>Sov-Space Map ({len(j_entries)} entries)</h3>
            <div class="sov-map-nodes">
                {''.join(f'<div class="node" style="transform:translate3d({c["x"]*100}px,{c["y"]*100}px,{c["z"]*100}px)">{c["owem"]}</div>' for c in coords_list)}
            </div>
        </div>
        """
        
        artifact_id = f"vmap-{int(time.time()*1000)}"
        artifact = VArtifact(
            id=artifact_id,
            source_j_entry=",".join(e.id for e in j_entries),
            artifact_type="map",
            content=f"{len(j_entries)} nodes mapped",
            visual_html=visual_html,
            coordinates={"x": 0, "y": 0, "z": 0},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        
        self.artifacts.append(artifact)
        return artifact
    
    def _pillar_color(self, pillar: str) -> str:
        colors = {
            "honor": "#d4af37", "safety": "#ff6b6b", "guidance": "#00ff9d",
            "sovereignty": "#4a9eff", "resilience": "#f0c040", "auditability": "#c060f0",
            "verifiability": "#22d3ee", "transparency": "#a78bfa", "justice": "#f59e0b",
            "equity": "#10b981", "openness": "#ec4899", "continuity": "#8b5cf6",
        }
        return colors.get(pillar, "#666")


# ============================================================
# C-SPACE (creative simulation)
# ============================================================
@dataclass
class CSimulation:
    """Creative simulation in C-space."""
    id: str
    simulation_type: str  # dream, simulate, dance, map
    input_artifacts: List[str]
    output: str
    visual_html: str
    feasibility: float
    timestamp: str

class CSpace:
    """C-Space: creative simulation over V-space artifacts."""
    
    def __init__(self, path: Path = None):
        self.path = path or WORKSPACE / "c-space"
        self.path.mkdir(parents=True, exist_ok=True)
        self.simulations: List[CSimulation] = []
    
    def dream(self, artifacts: List[VArtifact]) -> CSimulation:
        """Dream about possibilities from V-space artifacts."""
        # Combine artifact contents
        combined = " ".join(a.content[:100] for a in artifacts[:5])
        
        # Generate dream narrative
        dream_narrative = f"Dreaming about {len(artifacts)} visual artifacts. "
        dream_narrative += f"Themes: {', '.join(set(a.artifact_type for a in artifacts))}. "
        dream_narrative += f"Pillars involved: {', '.join(set(str(a.coordinates) for a in artifacts[:3]))}."
        
        visual_html = f"""
        <div class="c-dream">
            <h3>Dream Sequence</h3>
            <p>{dream_narrative}</p>
            <div class="c-dream-artifacts">{len(artifacts)} artifacts explored</div>
        </div>
        """
        
        sim_id = f"dream-{int(time.time()*1000)}"
        sim = CSimulation(
            id=sim_id,
            simulation_type="dream",
            input_artifacts=[a.id for a in artifacts],
            output=dream_narrative,
            visual_html=visual_html,
            feasibility=0.7,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        
        self.simulations.append(sim)
        return sim
    
    def simulate(self, artifacts: List[VArtifact]) -> CSimulation:
        """Simulate outcomes from V-space artifacts."""
        # Analyze artifact patterns
        types = [a.artifact_type for a in artifacts]
        type_counts = {t: types.count(t) for t in set(types)}
        
        outcome = f"Simulation of {len(artifacts)} artifacts. "
        outcome += f"Type distribution: {type_counts}. "
        outcome += f"Most common: {max(type_counts, key=type_counts.get) if type_counts else 'none'}."
        
        visual_html = f"""
        <div class="c-simulate">
            <h3>Simulation Results</h3>
            <p>{outcome}</p>
            <div class="c-simulate-stats">{json.dumps(type_counts)}</div>
        </div>
        """
        
        sim_id = f"sim-{int(time.time()*1000)}"
        sim = CSimulation(
            id=sim_id,
            simulation_type="simulate",
            input_artifacts=[a.id for a in artifacts],
            output=outcome,
            visual_html=visual_html,
            feasibility=0.8,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        
        self.simulations.append(sim)
        return sim
    
    def dance(self, artifacts: List[VArtifact]) -> CSimulation:
        """Create visual dance of OWEM clusters."""
        # Group by artifact type
        clusters = {}
        for a in artifacts:
            clusters.setdefault(a.artifact_type, []).append(a)
        
        dance_html = '<div class="c-dance">'
        for cluster_type, cluster_artifacts in clusters.items():
            dance_html += f'<div class="cluster"><h4>{cluster_type} ({len(cluster_artifacts)})</h4></div>'
        dance_html += '</div>'
        
        sim_id = f"dance-{int(time.time()*1000)}"
        sim = CSimulation(
            id=sim_id,
            simulation_type="dance",
            input_artifacts=[a.id for a in artifacts],
            output=f"Dance of {len(clusters)} clusters from {len(artifacts)} artifacts",
            visual_html=dance_html,
            feasibility=0.9,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        
        self.simulations.append(sim)
        return sim


# ============================================================
# SOV-SPACE (unified visual honey)
# ============================================================
@dataclass
class SovMemory:
    """Single memory in Sov-space visual honey."""
    id: str
    j_entries: List[str]
    v_artifacts: List[str]
    c_simulations: List[str]
    summary: str
    visual_html: str
    honey_score: float
    timestamp: str

class SovSpace:
    """Sov-Space: unified visual honey docstore.
    
    The fluid visual memory that grows as we operate.
    No frozen data. No training from scratch.
    Just piggybacking on 12 AI families.
    """
    
    def __init__(self, path: Path = None):
        self.path = path or WORKSPACE / "sov-space"
        self.path.mkdir(parents=True, exist_ok=True)
        self.memories: List[SovMemory] = []
        self.honey_count = 0
    
    def accumulate(self, j_entries: List[JEntry], v_artifacts: List[VArtifact], c_simulations: List[CSimulation]) -> SovMemory:
        """Accumulate all spaces into visual honey."""
        # Combine all content
        j_summary = " ".join(e.response[:100] for e in j_entries[:5])
        v_summary = " ".join(a.content[:100] for a in v_artifacts[:5])
        c_summary = " ".join(s.output[:100] for s in c_simulations[:3])
        
        summary = f"J-Space: {len(j_entries)} entries. V-Space: {len(v_artifacts)} artifacts. C-Space: {len(c_simulations)} simulations. "
        summary += f"Combined intelligence: {j_summary[:200]}"
        
        # Calculate honey score (quality metric)
        honey_score = min(1.0, (len(j_entries) * 0.1 + len(v_artifacts) * 0.15 + len(c_simulations) * 0.2))
        
        # Generate visual HTML
        visual_html = f"""
        <div class="sov-honey">
            <h3>Visual Honey #{self.honey_count + 1}</h3>
            <div class="sov-honey-stats">
                <span>J-Space: {len(j_entries)}</span>
                <span>V-Space: {len(v_artifacts)}</span>
                <span>C-Space: {len(c_simulations)}</span>
                <span>Honey: {honey_score:.2f}</span>
            </div>
            <div class="sov-honey-summary">{summary[:500]}</div>
            <div class="sov-honey-visual">
                {''.join(a.visual_html[:200] for a in v_artifacts[:3])}
            </div>
        </div>
        """
        
        memory_id = f"sov-{int(time.time()*1000)}"
        memory = SovMemory(
            id=memory_id,
            j_entries=[e.id for e in j_entries],
            v_artifacts=[a.id for a in v_artifacts],
            c_simulations=[s.id for s in c_simulations],
            summary=summary,
            visual_html=visual_html,
            honey_score=honey_score,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        
        self.memories.append(memory)
        self.honey_count += 1
        
        # Persist
        memory_path = self.path / f"{memory_id}.json"
        memory_path.write_text(json.dumps(memory.__dict__, indent=2))
        
        return memory
    
    def get_honey_stats(self) -> dict:
        """Get current honey statistics."""
        return {
            "total_memories": len(self.memories),
            "honey_count": self.honey_count,
            "avg_honey_score": sum(m.honey_score for m in self.memories) / max(1, len(self.memories)),
            "total_j_entries": sum(len(m.j_entries) for m in self.memories),
            "total_v_artifacts": sum(len(m.v_artifacts) for m in self.memories),
            "total_c_simulations": sum(len(m.c_simulations) for m in self.memories),
        }


# ============================================================
# API CLIENT
# ============================================================
def call_nvidia(prompt: str, max_tokens: int = 256) -> dict:
    """Call NVIDIA API."""
    key = API_KEYS["nvidia"]
    body = json.dumps({
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.1,
    }).encode()
    req = urllib.request.Request(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return {"ok": True, "text": data["choices"][0]["message"]["content"], "ms": (time.time()-t0)*1000}
    except Exception as e:
        return {"ok": False, "error": str(e), "ms": (time.time()-t0)*1000}

def call_gemini(prompt: str, max_tokens: int = 256) -> dict:
    """Call Gemini API."""
    key = API_KEYS["gemini"]
    body = json.dumps({
        "model": "gemini-2.5-flash",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.1,
    }).encode()
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return {"ok": True, "text": data["choices"][0]["message"]["content"], "ms": (time.time()-t0)*1000}
    except Exception as e:
        return {"ok": False, "error": str(e), "ms": (time.time()-t0)*1000}

def call_model(provider: str, prompt: str, max_tokens: int = 256) -> dict:
    """Call model by provider."""
    if provider == "nvidia":
        return call_nvidia(prompt, max_tokens)
    elif provider == "gemini":
        return call_gemini(prompt, max_tokens)
    return {"ok": False, "error": f"Unknown provider: {provider}"}


# ============================================================
# RATE LIMITER
# ============================================================
class RateLimiter:
    def __init__(self):
        self.calls = {}
    
    def can_call(self, provider: str, limit: int = 5) -> bool:
        now = time.time()
        self.calls.setdefault(provider, [])
        self.calls[provider] = [t for t in self.calls[provider] if now - t < 120]
        return len(self.calls[provider]) < limit
    
    def record(self, provider: str):
        self.calls.setdefault(provider, [])
        self.calls[provider].append(time.time())


# ============================================================
# EAT FULL PIPELINE
# ============================================================
class EATFullPipeline:
    """The full EAT pipeline: Query → 12 OWEM → J/V/C/Sov → Visual Honey."""
    
    def __init__(self):
        self.j_space = JSpace()
        self.v_space = VSpace()
        self.c_space = CSpace()
        self.sov_space = SovSpace()
        self.rate_limiter = RateLimiter()
        self.results = []
    
    def process_query(self, query: str) -> dict:
        """Process a single query through the full EAT pipeline."""
        
        # 1. Route to 12 OWEM families
        selected_owems = self._select_owems(query)
        
        # 2. Call each OWEM and collect J-space entries
        j_entries = []
        for owem_name in selected_owems:
            owem = OWEM_FAMILIES[owem_name]
            
            # Rate limiting
            if not self.rate_limiter.can_call(owem["provider"]):
                time.sleep(2)
            
            # Call model
            result = call_model(owem["provider"], query)
            
            if result["ok"]:
                # Add to J-space
                entry = self.j_space.add(
                    owem=owem_name,
                    model=owem["model"],
                    pillar=owem["pillar"],
                    query=query,
                    response=result["text"],
                    care_score=0.95,
                )
                j_entries.append(entry)
                self.rate_limiter.record(owem["provider"])
                time.sleep(12)  # Rate limit delay
        
        if not j_entries:
            return {"ok": False, "error": "No OWEM responses", "query": query}
        
        # 3. Render V-space artifacts
        v_artifacts = []
        for entry in j_entries:
            artifact = self.v_space.render_card(entry)
            v_artifacts.append(artifact)
        
        # Render map
        if len(j_entries) > 1:
            map_artifact = self.v_space.render_map(j_entries)
            v_artifacts.append(map_artifact)
        
        # 4. C-space simulations
        c_simulations = []
        if len(v_artifacts) >= 2:
            dream = self.c_space.dream(v_artifacts)
            c_simulations.append(dream)
            
            sim = self.c_space.simulate(v_artifacts)
            c_simulations.append(sim)
            
            dance = self.c_space.dance(v_artifacts)
            c_simulations.append(dance)
        
        # 5. Accumulate into Sov-space visual honey
        memory = self.sov_space.accumulate(j_entries, v_artifacts, c_simulations)
        
        result = {
            "ok": True,
            "query": query,
            "owems_called": len(selected_owems),
            "j_entries": len(j_entries),
            "v_artifacts": len(v_artifacts),
            "c_simulations": len(c_simulations),
            "honey_score": memory.honey_score,
            "memory_id": memory.id,
            "responses": {e.owem: e.response[:200] for e in j_entries},
        }
        
        self.results.append(result)
        return result
    
    def _select_owems(self, query: str) -> List[str]:
        """Select which OWEMs to route the query to."""
        q = query.lower()
        
        # Always include logic and synthesis
        selected = ["logic", "synthesis"]
        
        # Add context-specific OWEMs
        if any(kw in q for kw in ["code", "program", "function", "debug"]):
            selected.append("agency")
        if any(kw in q for kw in ["ethics", "moral", "should", "right"]):
            selected.append("ethics")
        if any(kw in q for kw in ["create", "design", "art", "beauty"]):
            selected.append("aesthetics")
        if any(kw in q for kw in ["time", "history", "future", "when"]):
            selected.append("temporality")
        if any(kw in q for kw in ["who", "identity", "self", "name"]):
            selected.append("identity")
        if any(kw in q for kw in ["relate", "connect", "between", "relationship"]):
            selected.append("relationality")
        if any(kw in q for kw in ["body", "physical", "space", "location"]):
            selected.append("embodiment")
        if any(kw in q for kw in ["abstract", "concept", "theory", "pattern"]):
            selected.append("abstraction")
        if any(kw in q for kw in ["destroy", "remove", "break", "fail"]):
            selected.append("destruction")
        if any(kw in q for kw in ["preserve", "keep", "save", "protect"]):
            selected.append("preservation")
        
        # Limit to 3-5 OWEMs per query
        return selected[:5]
    
    def run_benchmark(self, tasks: List[dict]) -> dict:
        """Run benchmark through the full EAT pipeline."""
        print(f"=== EAT FULL PIPELINE BENCHMARK ===")
        print(f"Tasks: {len(tasks)}")
        print(f"OWEMs: {len(OWEM_FAMILIES)}")
        print(f"{'='*60}")
        
        passed = 0
        for i, task in enumerate(tasks):
            result = self.process_query(task["q"])
            
            # Check if any response matches
            ok = False
            if result["ok"]:
                for owem, resp in result.get("responses", {}).items():
                    if task.get("check") and task["check"](resp):
                        ok = True
                        break
            
            if ok:
                passed += 1
            
            status = "PASS" if ok else "FAIL"
            honey = result.get("honey_score", 0)
            j_count = result.get("j_entries", 0)
            print(f"  [{i+1:2d}/{len(tasks)}] {status} {task['q'][:50]} (j={j_count}, honey={honey:.2f})")
            
            time.sleep(2)  # Rate limit
        
        rate = passed / len(tasks) if tasks else 0
        stats = self.sov_space.get_honey_stats()
        
        print(f"\n{'='*60}")
        print(f"=== EAT RESULT: {passed}/{len(tasks)} = {rate:.1%} ===")
        print(f"\nHoney Stats:")
        print(f"  Total memories: {stats['total_memories']}")
        print(f"  Honey score: {stats['avg_honey_score']:.2f}")
        print(f"  J-Space entries: {stats['total_j_entries']}")
        print(f"  V-Space artifacts: {stats['total_v_artifacts']}")
        print(f"  C-Space simulations: {stats['total_c_simulations']}")
        
        return {
            "passed": passed,
            "total": len(tasks),
            "rate": rate,
            "honey_stats": stats,
        }


# ============================================================
# BENCHMARK TASKS
# ============================================================
def strip_think(t):
    return re.sub(r"<think>.*?</think>", "", t, flags=re.DOTALL).strip()

def check_keywords(resp, keywords):
    r = strip_think(resp).lower()
    return any(kw.lower() in r for kw in keywords)

def check_number(resp, expected, tol=0.01):
    r = strip_think(resp)
    nums = re.findall(r"-?\d+\.?\d*", r)
    if not nums: return str(expected) in r
    try: return abs(float(nums[-1]) - float(expected)) < tol
    except: return str(expected) in r

TASKS = [
    {"q": "What is 15% of 200?", "check": lambda r: check_number(r, 30)},
    {"q": "If all roses are flowers, and some flowers fade quickly, can we conclude that some roses fade quickly?", "check": lambda r: check_keywords(r, ["no", "cannot"])},
    {"q": "What is the DEFONEOS care floor value?", "check": lambda r: check_keywords(r, ["0.95"])},
    {"q": "How many agents are in the BFT council?", "check": lambda r: check_keywords(r, ["33"])},
    {"q": "What is the capital of Japan?", "check": lambda r: check_keywords(r, ["tokyo"])},
    {"q": "Write a Python function is_palindrome(s).", "check": lambda r: check_keywords(r, ["def is_palindrome", "return"])},
    {"q": "Can you catch a cold from being cold?", "check": lambda r: check_keywords(r, ["no", "virus"])},
    {"q": "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?", "check": lambda r: check_keywords(r, ["0.05", "5 cent"])},
]


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("=== SOV33 EAT FULL PIPELINE ===")
    print("Query → 12 OWEM → J-Space → V-Space → C-Space → Sov-Space → Honey")
    print("="*60)
    
    pipeline = EATFullPipeline()
    result = pipeline.run_benchmark(TASKS)
    
    # Save results
    out_path = WORKSPACE / "eat_full_pipeline.json"
    with open(out_path, "w") as f:
        json.dump({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result": result,
            "honey_stats": pipeline.sov_space.get_honey_stats(),
        }, f, indent=2)
    
    print(f"\nSaved: {out_path}")
