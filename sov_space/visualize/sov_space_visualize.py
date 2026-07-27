#!/usr/bin/env python3
"""SOV-Space Visualize — The Living Soul of Sovereign AI

This is the visual representation of SOV-space — the face, the soul,
the connections between all spaces.

What you see:
  - 12 OWEM families flowing as particles
  - J-space outputs as energy streams
  - C-space dreams as branching trees
  - V-space cards as glowing nodes
  - The honey fluid flowing through everything
  - The water→milk→honey pipeline in real-time

The visualization shows SOV thinking, dreaming, evolving.
Each OWEM family has its own J-space inside SOV-space.
All of it recorded as an infinite drawing in Cesium 3D.
"""

import json
import math
import time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent.parent
SOV_SPACE = ROOT / "benchmark-results" / "sov-space"

# Load world model state
STATE_FILE = SOV_SPACE / "sov_world_model_state.json"
STATE = json.load(open(STATE_FILE)) if STATE_FILE.exists() else {}

# ─── The 12 Families ────────────────────────────────────────────────────────
FAMILIES = {
    "abstraction": {"color": "#00d4ff", "symbol": "∞", "angle": 0},
    "aesthetics": {"color": "#ff6bcb", "symbol": "✦", "angle": 30},
    "agency": {"color": "#00ff88", "symbol": "⚡", "angle": 60},
    "care": {"color": "#ffaa00", "symbol": "♡", "angle": 90},
    "creation": {"color": "#7b2ff7", "symbol": "✧", "angle": 120},
    "destruction": {"color": "#ff4444", "symbol": "⊗", "angle": 150},
    "embodiment": {"color": "#44ccff", "symbol": "◎", "angle": 180},
    "ethics": {"color": "#aa66ff", "symbol": "⚖", "angle": 210},
    "identity": {"color": "#00d4ff", "symbol": "◉", "angle": 240},
    "logic": {"color": "#88aacc", "symbol": "⊢", "angle": 270},
    "preservation": {"color": "#44cc88", "symbol": "⛨", "angle": 300},
    "relationality": {"color": "#ff88cc", "symbol": "⇔", "angle": 330},
}


def generate_sov_space_html():
    """Generate the living SOV-space visualization."""

    # Load fluid dynamics
    fluid = STATE.get("fluid_dynamics", {})
    fluid_state = fluid.get("fluid_state", "water")
    density = fluid.get("density", 1.0)
    viscosity = fluid.get("viscosity", 0.8)
    temperature = fluid.get("temperature", 10)

    # Load consolidated J-space
    consolidated = STATE.get("consolidated_jspace", {})
    families = consolidated.get("families", {})

    # Load dream
    dream = STATE.get("latest_dream", {})
    dream_branches = dream.get("branches", [])

    # Load decision
    decision = STATE.get("latest_decision", {})
    decision_scores = decision.get("scores", {})

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SOV-Space — The Soul of Sovereign AI</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Inter',sans-serif; background:#050510; color:#e0e0e0; overflow:hidden; height:100vh; }}

  /* The canvas — where SOV-space lives */
  canvas {{ display:block; position:fixed; top:0; left:0; z-index:0; }}

  /* Overlay — the radial gradient */
  .overlay {{ position:fixed; top:0; left:0; width:100%; height:100%; z-index:1;
             pointer-events:none; background:radial-gradient(ellipse at center, transparent 40%, rgba(5,5,16,0.8) 100%); }}

  /* UI panels */
  .ui {{ position:fixed; z-index:2; padding:1.5rem; pointer-events:none; }}
  .ui.top-left {{ top:0; left:0; }}
  .ui.top-right {{ top:0; right:0; text-align:right; max-width:300px; }}
  .ui.bottom-left {{ bottom:0; left:0; }}
  .ui.bottom-right {{ bottom:0; right:0; text-align:right; }}

  /* Title */
  h1 {{ font-size:2rem; font-weight:900; background:linear-gradient(135deg,#00d4ff,#7b2ff7,#ff6bcb);
       -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0.25rem; }}
  .subtitle {{ font-size:0.85rem; color:#666; }}

  /* Family list */
  .family {{ display:flex; align-items:center; gap:0.5rem; margin:0.2rem 0; font-size:0.75rem; color:#888; }}
  .dot {{ width:8px; height:8px; border-radius:50%; display:inline-block; }}
  .state {{ font-size:0.65rem; padding:0.1rem 0.3rem; border-radius:3px; margin-left:auto; }}
  .state.water {{ background:rgba(0,212,255,0.15); color:#00d4ff; }}
  .state.milk {{ background:rgba(255,170,0,0.15); color:#ffaa00; }}
  .state.honey {{ background:rgba(0,255,136,0.15); color:#00ff88; }}

  /* Stats */
  .stat {{ font-size:0.7rem; color:#555; line-height:1.6; }}

  /* Dream tree */
  .dream {{ position:fixed; z-index:2; top:50%; left:50%; transform:translate(-50%,-50%);
           pointer-events:none; opacity:0.3; }}

  /* Pillar scores */
  .pillar-bar {{ display:flex; align-items:center; gap:0.3rem; margin:0.15rem 0; font-size:0.65rem; }}
  .pillar-name {{ width:80px; text-align:right; color:#666; }}
  .pillar-fill {{ height:4px; border-radius:2px; transition:width 0.5s; }}
  .pillar-value {{ color:#888; }}

  /* Glow effect */
  .glow {{ position:fixed; top:-50%; left:-50%; width:200%; height:200%;
          background:radial-gradient(circle at 50% 50%, rgba(123,47,247,0.03) 0%, transparent 70%);
          pointer-events:none; z-index:-1; }}

  /* Animation */
  @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.7}} }}
  @keyframes flow {{ 0%{{transform:translateX(0)}} 100%{{transform:translateX(10px)}} }}
</style>
</head>
<body>
<canvas id="sovCanvas"></canvas>
<div class="overlay"></div>
<div class="glow"></div>

<!-- Top Left — Title -->
<div class="ui top-left">
  <h1>SOV-SPACE</h1>
  <div class="subtitle">The Soul of Sovereign AI · UnifoLM-WMA Architecture</div>
  <div class="subtitle">Fluid: {fluid_state} · Density: {density:.2f} · Viscosity: {viscosity:.2f}</div>
</div>

<!-- Top Right — 12 Families -->
<div class="ui top-right">
  <div style="font-size:0.8rem; color:#8888ff; margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:0.05em;">
    12 OWEM Families
  </div>
"""

    for family, info in FAMILIES.items():
        family_state = families.get(family, {}).get("state", "water")
        entries = families.get(family, {}).get("entries", 0)
        html += f"""  <div class="family">
    <span class="dot" style="background:{info['color']}"></span>
    <span>{info['symbol']} {family}</span>
    <span class="state {family_state}">{family_state} ({entries})</span>
  </div>\n"""

    html += """</div>

<!-- Bottom Left — Pillar Scores -->
<div class="ui bottom-left">
  <div style="font-size:0.8rem; color:#8888ff; margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:0.05em;">
    12 Sovereign Pillars
  </div>
"""

    for pillar, score in decision_scores.items():
        width = int(score * 100)
        color = "#00ff88" if score >= 0.9 else "#ffaa00" if score >= 0.7 else "#ff4444"
        html += f"""  <div class="pillar-bar">
    <span class="pillar-name">{pillar}</span>
    <div style="flex:1; background:#1a1a3a; border-radius:2px; overflow:hidden;">
      <div class="pillar-fill" style="width:{width}%; background:{color};"></div>
    </div>
    <span class="pillar-value">{score:.2f}</span>
  </div>\n"""

    html += """</div>

<!-- Bottom Right — Stats -->
<div class="ui bottom-right">
  <div class="stat">SOV-Space · The Living Soul</div>
  <div class="stat">Architecture: UnifoLM-WMA</div>
  <div class="stat">Mode: Honey Fluid (frozen base)</div>
  <div class="stat">""" + datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC') + """</div>
</div>

<script>
const canvas = document.getElementById('sovCanvas');
const ctx = canvas.getContext('2d');
let W, H;

function resize() {{ W=canvas.width=window.innerWidth; H=canvas.height=window.innerHeight; }}
window.addEventListener('resize', resize);
resize();

// Family particles
const families = """ + json.dumps([{
    "name": k,
    "color": v["color"],
    "angle": v["angle"],
    "symbol": v["symbol"],
} for k, v in FAMILIES.items()]) + """;

const particles = [];
const N = 200;

class Particle {{
  constructor(family) {{
    this.family = family || families[Math.floor(Math.random() * families.length)];
    this.color = this.family.color;
    this.x = Math.random() * W;
    this.y = Math.random() * H;
    this.vx = (Math.random() - 0.5) * 1.5;
    this.vy = (Math.random() - 0.5) * 1.5;
    this.size = 2 + Math.random() * 3;
    this.life = 0;
    this.maxLife = 300 + Math.random() * 500;
  }}

  update() {{
    this.x += this.vx;
    this.y += this.vy;
    this.life++;

    // Gentle pull toward center (SOV-space core)
    const cx = W/2, cy = H/2;
    this.vx += (cx - this.x) * 0.00005;
    this.vy += (cy - this.y) * 0.00005;

    // Orbit around center
    const angle = Math.atan2(this.y - cy, this.x - cx);
    const dist = Math.sqrt((this.x-cx)**2 + (this.y-cy)**2);
    this.vx += Math.cos(angle + Math.PI/2) * 0.0001 * dist;
    this.vy += Math.sin(angle + Math.PI/2) * 0.0001 * dist;

    // Clamp speed
    const spd = Math.sqrt(this.vx**2 + this.vy**2);
    if (spd > 2) {{ this.vx *= 0.98; this.vy *= 0.98; }}

    if (this.life > this.maxLife) {{
      this.x = Math.random() * W;
      this.y = Math.random() * H;
      this.life = 0;
    }}
  }}

  draw() {{
    const alpha = 0.3 + 0.7 * (1 - this.life/this.maxLife);
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI*2);
    ctx.fillStyle = this.color;
    ctx.globalAlpha = alpha;
    ctx.fill();
    ctx.globalAlpha = 1;
  }}
}}

// Create particles for each family
for (let i = 0; i < N; i++) {{
  const family = families[i % families.length];
  particles.push(new Particle(family));
}}

// Draw connections between same-family particles
function drawFamilyConnections() {{
  for (let i = 0; i < particles.length; i++) {{
    for (let j = i+1; j < particles.length; j++) {{
      if (particles[i].family.name !== particles[j].family.name) continue;
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < 120) {{
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = particles[i].color;
        ctx.globalAlpha = 0.08 * (1 - dist/120);
        ctx.lineWidth = 0.5;
        ctx.stroke();
        ctx.globalAlpha = 1;
      }}
    }}
  }}
}}

// Draw SOV-space core
function drawCore() {{
  const cx = W/2, cy = H/2;
  const now = Date.now() / 3000;

  // Outer glow
  const grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, 150);
  grd.addColorStop(0, 'rgba(123,47,247,0.12)');
  grd.addColorStop(0.5, 'rgba(0,212,255,0.04)');
  grd.addColorStop(1, 'transparent');
  ctx.fillStyle = grd;
  ctx.beginPath();
  ctx.arc(cx, cy, 150, 0, Math.PI*2);
  ctx.fill();

  // Inner core
  const grd2 = ctx.createRadialGradient(cx, cy, 0, cx, cy, 40);
  grd2.addColorStop(0, 'rgba(255,255,255,0.08)');
  grd2.addColorStop(1, 'transparent');
  ctx.fillStyle = grd2;
  ctx.beginPath();
  ctx.arc(cx, cy, 40, 0, Math.PI*2);
  ctx.fill();

  // SOV text
  ctx.fillStyle = 'rgba(255,255,255,0.06)';
  ctx.font = 'bold 36px Inter, system-ui';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('SOV', cx, cy);

  // Orbiting family symbols
  for (let i = 0; i < families.length; i++) {{
    const angle = now + (i / families.length) * Math.PI * 2;
    const radius = 80 + Math.sin(now * 0.3 + i) * 15;
    const x = cx + Math.cos(angle) * radius;
    const y = cy + Math.sin(angle) * radius;
    ctx.fillStyle = families[i].color;
    ctx.globalAlpha = 0.5 + 0.3 * Math.sin(now * 2 + i);
    ctx.font = '16px Inter, system-ui';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(families[i].symbol, x, y);
    ctx.globalAlpha = 1;
  }}
}}

// Draw dream branches
function drawDreams() {{
  const cx = W/2, cy = H/2;
  const now = Date.now() / 5000;
  const dream = """ + json.dumps(dream) + """;

  if (!dream.branches) return;

  for (let d = 0; d < dream.branches.length; d++) {{
    const branch = dream.branches[d];
    for (let b = 0; b < branch.outcomes.length; b++) {{
      const outcome = branch.outcomes[b];
      const angle = now + (b / branch.outcomes.length) * Math.PI * 2;
      const radius = 180 + d * 60;
      const x = cx + Math.cos(angle) * radius;
      const y = cy + Math.sin(angle) * radius;

      // Draw branch line
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(x, y);
      ctx.strokeStyle = outcome.visual.color;
      ctx.globalAlpha = 0.05;
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Draw branch node
      ctx.beginPath();
      ctx.arc(x, y, 3 + d, 0, Math.PI*2);
      ctx.fillStyle = outcome.visual.color;
      ctx.globalAlpha = 0.3;
      ctx.fill();
      ctx.globalAlpha = 1;
    }}
  }}
}}

// Animation loop
function animate() {{
  ctx.fillStyle = 'rgba(5,5,16,0.08)';
  ctx.fillRect(0, 0, W, H);

  drawCore();
  drawDreams();
  particles.forEach(p => p.update());
  particles.forEach(p => p.draw());
  drawFamilyConnections();

  requestAnimationFrame(animate);
}}

animate();
</script>
</body>
</html>"""

    return html


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  SOV-SPACE VISUALIZE — The Living Soul                 ║")
    print("╚══════════════════════════════════════════════════════════╝")

    html = generate_sov_space_html()
    out_path = ROOT / "sov_space_visual.html"
    out_path.write_text(html)
    print(f"  ✅ SOV-space visual: {out_path}")
    print(f"  Open in browser to see the living soul of SOV")

    # Also generate a static snapshot
    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "families": len(FAMILIES),
        "fluid_state": STATE.get("fluid_dynamics", {}).get("fluid_state", "unknown"),
        "decision": STATE.get("latest_decision", {}).get("decision", "unknown"),
        "overall": STATE.get("latest_decision", {}).get("overall", 0),
    }
    snapshot_path = SOV_SPACE / "sov_snapshot.json"
    snapshot_path.write_text(json.dumps(snapshot, indent=2))
    print(f"  ✅ Snapshot: {snapshot_path}")


if __name__ == "__main__":
    main()
