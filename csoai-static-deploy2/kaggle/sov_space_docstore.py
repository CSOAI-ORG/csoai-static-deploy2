#!/usr/bin/env python3
"""
sov_space_docstore.py — SOV SPACE Visual Docstore Memory

The operating memory layer for SOV's visual emergence model.

J-SPACE: Text/reasoning outputs from 12 OWEM specialists
V-SPACE: Visual artifacts (cards, maps, reasoning chains)
SOV-SPACE: Synthesized visual docstore — the fluid operating memory

Key insight: Build the fluid AS you operate. No frozen datasets.
Every interaction creates visual artifacts that accumulate into
SOV SPACE — the system learns by observing its own operation.

Architecture:
  Task → 12 OWEM → J-spaces → V-space → SOV SPACE → Visual Memory
                     (text)    (visual)   (synth)     (fluid)

Usage:
  python3 sov_space_docstore.py --observe "explain EU AI Act Article 50"
  python3 sov_space_docstore.py --visualize
  python3 sov_space_docstore.py --export  # export all memory
"""
from __future__ import annotations
import argparse, json, os, sys, time, hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
BENCH = ROOT / "benchmark-results"
SOVSPACE = BENCH / "sov-space"
SOVSPACE.mkdir(exist_ok=True)
VSPACE = BENCH / "v-space"
VSPACE.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "kaggle"))

# ── J-Space Entry ──────────────────────────────────────────────────────────
class JEntry:
    """Single entry in J-space: one model's output on one task."""
    def __init__(self, model: str, space: str, task_id: str,
                 input_text: str, output: str, output_type: str):
        self.model = model
        self.space = space
        self.task_id = task_id
        self.input = input_text
        self.output = output
        self.output_type = output_type
        self.timestamp = datetime.now().isoformat()
        self.sigil = hashlib.sha256(
            f"{model}|{task_id}|{output[:200]}".encode()
        ).hexdigest()[:16]
    
    def to_dict(self):
        return {
            "model": self.model, "space": self.space,
            "task_id": self.task_id, "input": self.input[:500],
            "output": self.output[:1000], "output_type": self.output_type,
            "timestamp": self.timestamp, "sigil": self.sigil,
        }


# ── V-Space: Visual Artifacts ─────────────────────────────────────────────
class VArtifact:
    """Visual artifact: card, map, reasoning chain visualization."""
    def __init__(self, artifact_type: str, data: dict):
        self.type = artifact_type
        self.data = data
        self.timestamp = datetime.now().isoformat()
        self.sigil = hashlib.sha256(
            json.dumps(data, default=str).encode()
        ).hexdigest()[:16]
    
    def to_html(self) -> str:
        if self.type == "reasoning_card":
            return self._reasoning_card_html()
        elif self.type == "model_output":
            return self._model_output_html()
        return f"<div class='artifact'>{json.dumps(self.data)}</div>"
    
    def _reasoning_card_html(self):
        model = self.data.get("model", "?")
        output = self.data.get("output", "")
        space = self.data.get("space", "?")
        icon = self.data.get("icon", "🧠")
        color = self.data.get("color", "#4FC3F7")
        return f'''<div class="card" style="border-left:4px solid {color};padding:12px;margin:8px 0;background:#111827;border-radius:6px">
  <div style="font-size:12px;color:{color}">{icon} {model} → {space}</div>
  <div style="margin-top:6px;font-size:13px">{output[:200]}</div>
  <div class="sigil" style="font-size:10px;color:#555;margin-top:4px">{self.sigil}</div>
</div>'''
    
    def _model_output_html(self):
        model = self.data.get("model", "?")
        task = self.data.get("task_id", "?")
        output = self.data.get("output", "")
        return f'''<div class="model-output" style="padding:8px;margin:4px 0;background:#0e1420;border-radius:4px">
  <div style="font-size:11px;color:#8ab">{model} · {task}</div>
  <div style="font-size:12px;margin-top:4px">{output[:300]}</div>
</div>'''


# ── SOV SPACE: Visual Docstore Memory ──────────────────────────────────────
class SovSpace:
    """SOV SPACE: the fluid visual docstore memory."""
    
    def __init__(self):
        self.jspaces = defaultdict(list)  # model → [JEntry]
        self.vspace = []  # [VArtifact]
        self.sovspace = []  # synthesized memory entries
        self.observation_count = 0
    
    def observe(self, task_id: str, task_input: str, model_outputs: dict):
        """Observe a task and all model outputs. Accumulate into SOV SPACE."""
        self.observation_count += 1
        
        # 1. Store each model's output in J-space
        for model, output_data in model_outputs.items():
            entry = JEntry(
                model=model,
                space=output_data.get("space", "sov5"),
                task_id=task_id,
                input_text=task_input,
                output=output_data.get("output", ""),
                output_type=output_data.get("type", "text"),
            )
            self.jspaces[model].append(entry)
            
            # 2. Create visual artifact for V-space
            artifact = VArtifact("reasoning_card", {
                "model": model,
                "output": output_data.get("output", ""),
                "space": output_data.get("space", "sov5"),
                "icon": output_data.get("icon", "🧠"),
                "color": output_data.get("color", "#4FC3F7"),
            })
            self.vspace.append(artifact)
        
        # 3. Synthesize into SOV SPACE (the fluid memory)
        synthesis = self._synthesize(task_id, task_input, model_outputs)
        self.sovspace.append(synthesis)
        
        return synthesis
    
    def _synthesize(self, task_id: str, task_input: str, model_outputs: dict) -> dict:
        """Synthesize all model outputs into SOV SPACE memory."""
        # Combine all reasoning
        all_outputs = []
        for model, data in model_outputs.items():
            all_outputs.append({
                "model": model,
                "output": data.get("output", ""),
                "type": data.get("type", "text"),
                "space": data.get("space", "sov5"),
            })
        
        # Create synthesis
        synthesis = {
            "task_id": task_id,
            "input": task_input[:500],
            "observation": self.observation_count,
            "timestamp": datetime.now().isoformat(),
            "models_used": len(model_outputs),
            "spaces_used": list(set(d.get("space", "sov5") for d in model_outputs.values())),
            "reasoning_chain": [o["output"][:200] for o in all_outputs],
            "visual_cards": [o["output"][:100] for o in all_outputs if o["type"] in ("visual", "reasoning")],
            "combined_output": " | ".join(o["output"][:100] for o in all_outputs[:5]),
            "sigil": hashlib.sha256(
                json.dumps(all_outputs, default=str).encode()
            ).hexdigest()[:16],
        }
        
        return synthesis
    
    def export_memory(self) -> dict:
        """Export all SOV SPACE memory."""
        return {
            "timestamp": datetime.now().isoformat(),
            "observations": self.observation_count,
            "jspaces": {model: [e.to_dict() for e in entries]
                       for model, entries in self.jspaces.items()},
            "vspace_count": len(self.vspace),
            "sovspace_count": len(self.sovspace),
            "sovspace_entries": self.sovspace,
        }
    
    def save(self):
        """Save all memory to disk."""
        # Save J-spaces
        for model, entries in self.jspaces.items():
            jspace_file = BENCH / "j-space" / f"{model}_jspace.json"
            jspace_file.parent.mkdir(exist_ok=True)
            jspace_file.write_text(json.dumps(
                [e.to_dict() for e in entries], indent=2))
        
        # Save V-space
        vspace_file = VSPACE / "visual_artifacts.json"
        vspace_file.write_text(json.dumps(
            [{"type": a.type, "data": a.data, "sigil": a.sigil}
             for a in self.vspace], indent=2))
        
        # Save SOV SPACE
        sovspace_file = SOVSPACE / "sovspace_memory.json"
        sovspace_file.write_text(json.dumps(self.export_memory(), indent=2))
        
        return sovspace_file


# ── Visual Dashboard ───────────────────────────────────────────────────────
def generate_dashboard(sovspace: SovSpace) -> str:
    """Generate HTML dashboard showing SOV SPACE state."""
    html = '''<!DOCTYPE html>
<html><head>
<meta charset=utf-8>
<title>SOV SPACE — Visual Docstore Memory</title>
<meta http-equiv="refresh" content="30">
<style>
body{font:13px/1.4 -apple-system,system-ui,sans-serif;background:#0a0e14;color:#e8ecf1;padding:24px;margin:0}
h1{font-size:24px;margin:0 0 8px}
h2{font-size:16px;margin:16px 0 8px;color:#8ab}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.space{background:#111827;border-radius:8px;padding:16px}
.card{background:#0e1420;border-radius:6px;padding:12px;margin:8px 0;border-left:4px solid}
.sigil{font-family:monospace;font-size:10px;color:#555}
.stats{display:flex;gap:16px;margin:16px 0}
.stat{background:#111827;border-radius:6px;padding:12px;text-align:center;flex:1}
.stat .num{font-size:24px;font-weight:700;color:#4FC3F7}
</style>
</head><body>
<h1>🐝 SOV SPACE — Visual Docstore Memory</h1>
<p>Fluid intelligence from 12 OWEM specialists. Build as you operate.</p>

<div class="stats">
  <div class="stat"><div class="num">''' + str(sovspace.observation_count) + '''</div><div>Observations</div></div>
  <div class="stat"><div class="num">''' + str(len(sovspace.jspaces)) + '''</div><div>J-Spaces</div></div>
  <div class="stat"><div class="num">''' + str(len(sovspace.vspace)) + '''</div><div>V-Artifacts</div></div>
  <div class="stat"><div class="num">''' + str(len(sovspace.sovspace)) + '''</div><div>SOV Memories</div></div>
</div>

<div class="grid">
<div class="space">
<h2>J-Space (Text/Reasoning)</h2>
'''
    for model, entries in sovspace.jspaces.items():
        html += f'<div class="card" style="border-color:#4FC3F7"><b>{model}</b> ({len(entries)} entries)</div>\n'
    
    html += '''</div>
<div class="space">
<h2>V-Space (Visual Artifacts)</h2>
'''
    for artifact in sovspace.vspace[-10:]:
        html += artifact.to_html()
    
    html += '''</div>
</div>

<div class="space" style="margin-top:16px">
<h2>SOV SPACE (Synthesized Memory)</h2>
'''
    for entry in sovspace.sovspace[-5:]:
        html += f'''<div class="card" style="border-color:#2d5a2d">
  <div>Task: {entry.get("task_id", "?")} · {entry.get("models_used", 0)} models</div>
  <div style="font-size:12px;margin-top:4px">{entry.get("combined_output", "")[:200]}</div>
  <div class="sigil">{entry.get("sigil", "")}</div>
</div>\n'''
    
    html += '''</div>
</body></html>'''
    
    out_path = BENCH / "sov_space_dashboard.html"
    out_path.write_text(html)
    return str(out_path)


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="observe",
                    choices=["observe", "visualize", "export"])
    ap.add_argument("--task", default="What is the EU AI Act Article 50?")
    ap.add_argument("--task-id", default="")
    args = ap.parse_args()

    sovspace = SovSpace()
    
    if args.mode == "observe":
        # Observe: route task through all models, accumulate into SOV SPACE
        task_id = args.task_id or f"task-{int(time.time())}"
        
        print(f"\n{'='*70}")
        print(f"  OBSERVING: {args.task[:60]}")
        print(f"  Task ID: {task_id}")
        print(f"{'='*70}\n")
        
        # Simulate model outputs (in production: call actual models)
        model_outputs = {}
        specialists = {
            "logic": {"space": "sov5", "type": "reasoning", "icon": "🧠", "color": "#4FC3F7"},
            "ethics": {"space": "sov5", "type": "reasoning", "icon": "⚖️", "color": "#81C784"},
            "aesthetics": {"space": "sov5", "type": "visual", "icon": "🎨", "color": "#FFD54F"},
            "temporality": {"space": "sov6", "type": "temporal", "icon": "⏰", "color": "#FF8A65"},
            "identity": {"space": "sov6", "type": "identity", "icon": "🪪", "color": "#CE93D8"},
            "agency": {"space": "sov6", "type": "agentic", "icon": "🤖", "color": "#90CAF9"},
        }
        
        for name, spec in specialists.items():
            model_outputs[name] = {
                "output": f"[{name}] Analysis: {args.task[:50]}...",
                "type": spec["type"],
                "space": spec["space"],
                "icon": spec["icon"],
                "color": spec["color"],
            }
            print(f"  {spec['icon']} {name:15s} → {spec['space']}")
        
        # Observe and synthesize
        synthesis = sovspace.observe(task_id, args.task, model_outputs)
        print(f"\n  Synthesized: {synthesis['models_used']} models → SOV SPACE")
        print(f"  Sigil: {synthesis['sigil']}")
        
        # Save
        sovspace.save()
        print(f"\n  Saved to: {SOVSPACE / 'sovspace_memory.json'}")
    
    elif args.mode == "visualize":
        path = generate_dashboard(sovspace)
        print(f"Dashboard: {path}")
    
    elif args.mode == "export":
        data = sovspace.export_memory()
        out = SOVSPACE / "sovspace_export.json"
        out.write_text(json.dumps(data, indent=2))
        print(f"Exported: {out}")


if __name__ == "__main__":
    main()