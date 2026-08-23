#!/usr/bin/env python3
"""
sov_space_visual.py — SOV Space Visual Operating Layer

Routes outputs from 12 OWEM models into J-spaces, combines their
reasoning into visual honey for SOV to operate on.

Architecture:
  WATER → 12 OWEM → J-spaces → HONEY → Visual Operating Layer

Each model's output (chat/image/voice/visual) gets:
  1. Routed into its own J-space (sov5/sov6/sov7)
  2. Visualized as reasoning cards
  3. Combined into honey (synthesized intelligence)
  4. Displayed as visual operating layer

Usage:
  python3 sov_space_visual.py --mode visual --task "explain the EU AI Act"
  python3 sov_space_visual.py --mode honey --models all
  python3 sov_space_visual.py --mode map  # visual map of all spaces
"""
from __future__ import annotations
import argparse, json, os, sys, time, hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
BENCH = ROOT / "benchmark-results"
JSPACE = BENCH / "j-space"
JSPACE.mkdir(exist_ok=True)
HONEY = BENCH / "honey"
HONEY.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "kaggle"))

try:
    from sov33_e2e_orchestrator_v2 import PROVIDERS
except ImportError:
    PROVIDERS = {}

# ── Model callers ──────────────────────────────────────────────────────────
def _call_ollama(model: str, prompt: str, specialist: str = "") -> str:
    """Call Ollama model."""
    import urllib.request
    body = json.dumps({
        "model": model, "stream": False,
        "messages": [{"role": "user", "content": f"[{specialist}] {prompt}"}],
        "options": {"num_predict": 128, "temperature": 0.3},
    }).encode()
    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/chat", data=body, method="POST",
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return data.get("message", {}).get("content", "").strip()
    except Exception as e:
        return None

def _call_api(provider: str, model: str, prompt: str) -> str:
    """Call API model."""
    import urllib.request
    cfg = PROVIDERS.get(provider, {})
    api_key = os.environ.get(cfg.get("key", ""), "")
    if not api_key or not cfg.get("base"):
        return None
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 128,
    }).encode()
    try:
        req = urllib.request.Request(
            f"{cfg['base']}/chat/completions", data=body, method="POST",
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json",
                     "User-Agent": "SOV33/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None

# ── The 12 OWEM Specialists ────────────────────────────────────────────────
OWEM_SPECIALISTS = {
    "logic": {"model": "qwen3:8b", "space": "sov5", "type": "reasoning",
              "color": "#4FC3F7", "icon": "🧠", "provider": "ollama"},
    "ethics": {"model": "llama3.2:3b", "space": "sov5", "type": "reasoning",
               "color": "#81C784", "icon": "⚖️", "provider": "ollama"},
    "aesthetics": {"model": "mistral:7b", "space": "sov5", "type": "visual",
                   "color": "#FFD54F", "icon": "🎨", "provider": "ollama"},
    "temporality": {"model": "qwen2.5:0.5b", "space": "sov6", "type": "temporal",
                    "color": "#FF8A65", "icon": "⏰", "provider": "ollama"},
    "identity": {"model": "qwen2.5:0.5b", "space": "sov6", "type": "identity",
                 "color": "#CE93D8", "icon": "🪪", "provider": "ollama"},
    "agency": {"model": "deepseek-coder:1.3b", "space": "sov6", "type": "agentic",
               "color": "#90CAF9", "icon": "🤖", "provider": "ollama"},
    "relationality": {"model": "llama3.2:3b", "space": "sov6", "type": "social",
                      "color": "#F48FB1", "icon": "🤝", "provider": "ollama"},
    "embodiment": {"model": "mistral:7b", "space": "sov6", "type": "physical",
                   "color": "#A5D6A7", "icon": "🦾", "provider": "ollama"},
    "abstraction": {"model": "qwen2.5:0.5b", "space": "sov7", "type": "abstract",
                    "color": "#B39DDB", "icon": "🔮", "provider": "ollama"},
    "synthesis": {"model": "llama3.2:3b", "space": "sov7", "type": "synthesis",
                  "color": "#80CBC4", "icon": "🔗", "provider": "ollama"},
    "intuition": {"model": "qwen3:8b", "space": "sov7", "type": "intuition",
                  "color": "#FFAB91", "icon": "💡", "provider": "ollama"},
    "care": {"model": "mistral:7b", "space": "sov7", "type": "care",
             "color": "#EF9A9A", "icon": "❤️", "provider": "ollama"},
}

# ── J-Space: per-model output storage ───────────────────────────────────────
class JSpace:
    """J-Space: stores and routes outputs from individual models."""
    
    def __init__(self, model_name: str, space_id: str):
        self.model_name = model_name
        self.space_id = space_id
        self.entries = []
        self.dir = JSPACE / model_name
        self.dir.mkdir(parents=True, exist_ok=True)
    
    def add_entry(self, task_id: str, input_text: str, output: str,
                  output_type: str = "text", metadata: dict = None):
        """Add an entry to this J-space."""
        entry = {
            "task_id": task_id,
            "input": input_text[:500],
            "output": output[:1000],
            "output_type": output_type,  # text, image, voice, visual
            "space": self.space_id,
            "model": self.model_name,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "sigil": hashlib.sha256(f"{self.model_name}|{task_id}|{output[:100]}".encode()).hexdigest()[:16],
        }
        self.entries.append(entry)
        
        # Save to disk
        entry_file = self.dir / f"{task_id}_{int(time.time())}.json"
        entry_file.write_text(json.dumps(entry, indent=2))
        return entry
    
    def get_honey(self) -> dict:
        """Extract honey (synthesized intelligence) from this J-space."""
        if not self.entries:
            return {"model": self.model_name, "honey": "no entries"}
        
        # Aggregate reasoning patterns
        patterns = defaultdict(int)
        for entry in self.entries:
            output_type = entry.get("output_type", "text")
            patterns[output_type] += 1
        
        return {
            "model": self.model_name,
            "space": self.space_id,
            "total_entries": len(self.entries),
            "output_types": dict(patterns),
            "latest_output": self.entries[-1]["output"][:200] if self.entries else None,
            "sigil_chain": [e["sigil"] for e in self.entries[-5:]],
        }


# ── Honey: synthesized intelligence layer ───────────────────────────────────
class HoneyLayer:
    """Honey layer: combines outputs from all J-spaces into visual intelligence."""
    
    def __init__(self):
        self.jspaces = {}
        self.honey_entries = []
    
    def get_or_create_jspace(self, model_name: str, space_id: str) -> JSpace:
        key = f"{model_name}:{space_id}"
        if key not in self.jspaces:
            self.jspaces[key] = JSpace(model_name, space_id)
        return self.jspaces[key]
    
    def synthesize(self, task_id: str, task_prompt: str) -> dict:
        """Synthesize honey from all J-spaces for a given task."""
        task_honey = {
            "task_id": task_id,
            "prompt": task_prompt,
            "timestamp": datetime.now().isoformat(),
            "model_outputs": [],
            "synthesized": None,
            "visual_card": None,
        }
        
        # Collect outputs from all J-spaces
        for jspace in self.jspaces.values():
            for entry in jspace.entries:
                if entry["task_id"] == task_id:
                    task_honey["model_outputs"].append({
                        "model": entry["model"],
                        "output": entry["output"][:300],
                        "type": entry["output_type"],
                        "space": entry["space"],
                    })
        
        # Synthesize: combine all outputs into unified reasoning
        if task_honey["model_outputs"]:
            combined_outputs = [o["output"] for o in task_honey["model_outputs"]]
            task_honey["synthesized"] = " | ".join(combined_outputs[:5])
            task_honey["visual_card"] = self._create_visual_card(task_honey)
        
        self.honey_entries.append(task_honey)
        return task_honey
    
    def _create_visual_card(self, honey: dict) -> dict:
        """Create a visual card representation of the honey."""
        card = {
            "type": "sov_honey_card",
            "task_id": honey["task_id"],
            "prompt": honey["prompt"][:100],
            "models_used": len(honey["model_outputs"]),
            "output_types": list(set(o["type"] for o in honey["model_outputs"])),
            "spaces_used": list(set(o["space"] for o in honey["model_outputs"])),
            "reasoning_chain": [o["output"][:100] for o in honey["model_outputs"][:5]],
            "timestamp": honey["timestamp"],
            "sigil": hashlib.sha256(json.dumps(honey, default=str).encode()).hexdigest()[:16],
        }
        return card
    
    def save_honey(self, task_id: str):
        """Save honey to disk."""
        for honey in self.honey_entries:
            if honey["task_id"] == task_id:
                out_path = HONEY / f"{task_id}_honey.json"
                out_path.write_text(json.dumps(honey, indent=2, default=str))
                return out_path
        return None


# ── Visual Map Generator ───────────────────────────────────────────────────
def generate_visual_map(honey_layer: HoneyLayer) -> str:
    """Generate HTML visual map of all J-spaces and honey."""
    html = """<!DOCTYPE html>
<html><head>
<meta charset=utf-8>
<title>SOV Space Visual Map</title>
<style>
body{font:13px/1.4 -apple-system,system-ui,sans-serif;background:#0a0e14;color:#e8ecf1;padding:24px;margin:0}
h1{font-size:24px;margin:0 0 16px}
.space{background:#111827;border-radius:8px;padding:16px;margin:8px 0;border-left:4px solid}
.space h3{margin:0 0 8px;font-size:14px}
.model{background:#1a2233;border-radius:4px;padding:8px;margin:4px 0;font-size:12px}
.honey{background:#1a2a1a;border:1px solid #2d5a2d;border-radius:8px;padding:16px;margin:16px 0}
.sigil{font-family:monospace;font-size:10px;color:#666}
</style>
</head><body>
<h1>🐝 SOV Space Visual Map</h1>
<p>12 OWEM specialists → J-spaces → HONEY → Visual Operating Layer</p>
"""
    
    # Group by space
    spaces = defaultdict(list)
    for name, spec in OWEM_SPECIALISTS.items():
        spaces[spec["space"]].append((name, spec))
    
    for space_id, models in sorted(spaces.items()):
        html += f'<div class="space" style="border-color: {models[0][1]["color"]}">\n'
        html += f'  <h3>{space_id.upper()} — {models[0][1]["icon"]} {models[0][1]["type"]}</h3>\n'
        for name, spec in models:
            html += f'  <div class="model">{spec["icon"]} {name} ({spec["model"]}) <span class="sigil">{spec["color"]}</span></div>\n'
        html += '</div>\n'
    
    # Honey layer
    html += """
<div class="honey">
  <h3>🍯 HONEY Layer</h3>
  <p>Synthesized intelligence from all J-spaces</p>
  <ul>
    <li>Text reasoning → J-space:sov5</li>
    <li>Visual output → J-space:sov6</li>
    <li>Synthesis → J-space:sov7</li>
  </ul>
</div>
</body></html>"""
    
    out_path = BENCH / "sov_space_visual.html"
    out_path.write_text(html)
    return str(out_path)


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="map",
                    choices=["visual", "honey", "map", "route"])
    ap.add_argument("--task", default="explain the EU AI Act Article 50")
    ap.add_argument("--models", default="all")
    args = ap.parse_args()

    honey = HoneyLayer()
    
    if args.mode == "map":
        path = generate_visual_map(honey)
        print(f"Visual map: {path}")
    
    elif args.mode == "route":
        # Route task through all OWEM specialists
        print(f"\n{'='*70}")
        print(f"  ROUTING: {args.task[:60]}")
        print(f"{'='*70}\n")
        
        for name, spec in OWEM_SPECIALISTS.items():
            jspace = honey.get_or_create_jspace(name, spec["space"])
            
            # Try live model call
            output = None
            if spec.get("provider") == "ollama":
                output = _call_ollama(spec["model"], args.task, name)
            elif spec.get("provider") == "api":
                output = _call_api(spec.get("api_provider", "groq"), spec["model"], args.task)
            
            if not output:
                output = f"[{name}] Analysis of: {args.task[:50]}..."
            
            entry = jspace.add_entry(
                task_id="demo",
                input_text=args.task,
                output=output,
                output_type=spec["type"],
            )
            print(f"  {spec['icon']} {name:15s} → {spec['space']:6s} → J-space:{name}")
            print(f"     {output[:80]}")
        
        # Synthesize honey
        honey_result = honey.synthesize("demo", args.task)
        print(f"\n{'='*70}")
        print(f"  HONEY (synthesized)")
        print(f"{'='*70}")
        print(f"  Models used: {len(honey_result['model_outputs'])}")
        print(f"  Visual card: {json.dumps(honey_result.get('visual_card', {}), indent=2)}")
    
    elif args.mode == "honey":
        print("Honey mode: generating from all models...")
        # In production: call each model, collect outputs, synthesize
        print("(Use --route to test with demo data)")


if __name__ == "__main__":
    main()