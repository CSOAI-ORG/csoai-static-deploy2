# Comprehensive Research: Unreal Engine 5 + Python for MEOK 3D World Simulation

**Research Date:** 2026-06-22
**Purpose:** Evaluate every method to use UE5 with Python for MEOK's 47-agent, 12-civilization 3D world simulation
**Budget Context:** $0 budget, needs to run on consumer laptop hardware

---

## Table of Contents

1. [UE5.8 MCP Support (Official)](#1-ue58-mcp-support-official)
2. [PyUnreal / UnrealEnginePython Plugin](#2-pyunreal--unrealenginepython-plugin)
3. [UE5 Built-in Python Scripting](#3-ue5-built-in-python-scripting-editor-only)
4. [Cesium for Unreal (3D Earth)](#4-cesium-for-unreal-3d-earth)
5. [UE5 + Agent Simulation (47 AI Agents)](#5-ue5--agent-simulation-47-ai-agents)
6. [Alternatives: Godot 4, Bevy, Three.js](#6-alternatives-godot-4-bevy-threejs)
7. [Architecture Document: Agent Decision → Visual Output](#7-architecture-document)
8. [Final Recommendation](#8-final-recommendation)

---

## 1. UE5.8 MCP Support (Official)

### 1.1 Is Unreal Engine 5.8 Available?

**YES.** Unreal Engine 5.8 was officially released on **June 17, 2026** (Epic Games "State of Unreal 2026" at Unreal Fest Chicago). It is the **last major release planned for the UE5 series** before UE6.

### 1.2 What is "MCP Support"?

MCP stands for **Model Context Protocol** - an open standard originally proposed by Anthropic in 2024, donated to the Agentic AI Foundation (AAIF) under the Linux Foundation in December 2025. It defines how AI agents connect to external tools/applications.

UE5.8 ships with an **official Experimental MCP plugin** (`ModelContextProtocol`) that embeds an MCP server **inside the Unreal Editor process**. This means:

- Claude Code, Cursor, VS Code, Gemini, and Codex can connect directly to UE5
- AI agents can **spawn actors, control lighting, create materials, manipulate Blueprints, run tests** via Tools
- The plugin exposes core systems: Blueprints, assets, levels, materials, meshes, and more
- Server runs on `http://127.0.0.1:8000/mcp` by default

### 1.3 How to Set Up (Official UE5.8 MCP)

```bash
# Step 1: Enable the plugin
Edit > Plugins > Search "Unreal MCP" > Check Enabled > Restart Editor

# Step 2: Configure auto-start
Edit > Editor Preferences > General > Model Context Protocol
> Enable "Auto Start Server" (binds to http://127.0.0.1:8000/mcp)

# Step 3: Generate client config for Claude Code
# In Editor Console (backtick key):
ModelContextProtocol.GenerateClientConfig ClaudeCode
# Writes .mcp.json to project root

# Step 4: Launch Claude Code from project root
claude

# Step 5: (Optional) Install Terminal plugin for in-editor AI
Edit > Plugins > Search "Terminal" > Enable
# Configure: TERM=xterm-256color, cd to project, claude
```

### 1.4 What Can Be Controlled via Official MCP?

| Category | Capabilities |
|----------|-------------|
| **Actor Management** | Spawn, delete, transform, tag actors |
| **Blueprints** | Create, modify, compile Blueprints, add nodes, variables |
| **Materials** | Create instances, set parameters, assign textures |
| **Levels** | Load/save levels, manage streaming |
| **Lighting** | Configure lights, post-processing volumes |
| **Tests** | Run Automation Tests, check results |
| **Console** | Execute console commands |
| **PCG** | Procedural content generation (with PCG plugin) |

**Tool Search Mode:** Uses 3 meta-tools (`list_toolsets`, `describe_toolset`, `call_tool`) to avoid overwhelming the AI context window. The AI discovers available tools on-demand.

**Custom Toolsets:** You can write your own tools in Python:

```python
# Custom UE5.8 MCP Toolset Example (Python)
import unreal
from unreal import ToolsetDefinition, toolset_registry

class MEOKAgentToolset(ToolsetDefinition):
    @staticmethod
    @toolset_registry.tool_call
    def spawn_civilization_agent(location: unreal.Vector, civilization_id: int) -> str:
        """Spawn an agent representing a civilization leader in the 3D world."""
        actor_system = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        bp_class = unreal.EditorAssetLibrary.load_blueprint_class('/Game/BP_Agent')
        actor = actor_system.spawn_actor_from_class(bp_class, location)
        actor.set_actor_label(f"Agent_Civ_{civilization_id}")
        return f"Spawned agent at {location} for civilization {civilization_id}"
    
    @staticmethod
    @toolset_registry.tool_call  
    def set_agent_color(actor_name: str, color_hex: str) -> str:
        """Set the material color of an agent actor."""
        # Find actor, create dynamic material instance, set color
        actors = unreal.EditorLevelLibrary.get_all_level_actors()
        for actor in actors:
            if actor.get_actor_label() == actor_name:
                mesh = actor.get_component_by_class(unreal.StaticMeshComponent)
                mat = mesh.create_dynamic_material_instance(0)
                # Parse hex and set vector parameter...
                return f"Set color for {actor_name}"
        return f"Actor {actor_name} not found"
```

### 1.5 Third-Party MCP Servers (More Powerful)

Beyond the official plugin, several **community MCP servers** exist with more capabilities:

#### Option A: ChiR24/Unreal_mcp (200+ Tools)
- **GitHub:** https://github.com/ChiR24/Unreal_mcp
- **Features:** 200+ AI tools, dual transport (Native HTTP or WebSocket)
- **Tools:** Asset management, Actor control, AI (Behavior Trees, EQS, State Trees), Sequencer, Niagara, PCG, GAS
- **Setup:** Requires C++ plugin compilation OR pre-built binaries

#### Option B: chongdashu/unreal-mcp (Natural Language)
- **GitHub:** https://github.com/chongdashu/unreal-mcp
- **Features:** Natural language control, Actor/Blueprint/Editor/Camera management
- **Best for:** Beginners, vibe coding

#### Option C: remiphilippe/mcp-unreal (Go Binary)
- **GitHub:** https://github.com/remiphilippe/mcp-unreal
- **Features:** Single Go binary, 49 tools, uses Remote Control API
- **Best for:** Headless operation, CI/CD integration

### 1.6 MCP Architecture Flow

```
Claude Code / Cursor / Gemini
       |
       | JSON-RPC over HTTP (MCP Protocol)
       v
http://localhost:8000/mcp (UE5.8 Official)
       OR
http://localhost:3000/mcp (ChiR24 Native)
       |
       v
Unreal Editor Process (MCP Server)
       |
       v
Toolset Registry (discovers tools)
       |
       v
+----------------+----------------+----------------+
|   Python Tools |   C++ Tools    | Built-in Tools |
|   (custom)     |   (custom)     |   (Epic)       |
+----------------+----------------+----------------+
       |
       v
UE5 Engine API (Actors, Levels, Materials, Blueprints...)
```

### 1.7 Limitations of Official MCP

| Limitation | Details |
|-----------|---------|
| **Experimental** | APIs subject to change, features incomplete |
| **Editor Only** | Official toolset registry is editor-only (runtime possible via `AddTool()`) |
| **Serial Execution** | Tool calls execute on game thread serially - no parallel calls |
| **Loopback Only** | Binds to localhost only, no authentication, not for remote use |
| **HTTP/SSE Only** | No stdio or WebSocket transport |
| **No Resources/Prompts** | Only Tools exposed (not Resources or Prompts) |
| **Context Size** | Hundreds of tools need tool-search mode to manage context |

---

## 2. PyUnreal / UnrealEnginePython Plugin

### 2.1 What is it?

The **unreal-engine-python** plugin by 20tab embeds a full Python VM (3.x) inside Unreal Engine. It provides:

- Full Python scripting in both **editor AND runtime** (packaged games)
- Access to the complete UE4/UE5 API via reflection
- Special actor classes: `PyActor`, `PyPawn`, `PyCharacter`, `PythonComponent`
- Third-party library support (asyncio, coroutines, generators, threads)
- FBX SDK exposure for low-level file interaction

### 2.2 Project Status: ON HOLD / Looking for Maintainers

| Aspect | Status |
|--------|--------|
| **Last Active** | April 2020 (officially on hold) |
| **Maintained by Epic** | No |
| **UE5 Support** | No official support (community forks may exist) |
| **Latest Official Version** | UE 4.23 (with PRs for 4.24) |
| **UE 4.25+** | Requires significant refactoring (UProperty → FProperty) |
| **Verdict** | **NOT RECOMMENDED for new projects** |

> "Currently (as april 2020) the project is on hold: between 2016 and 2018 20tab invested lot of resources in it but unfortunately epic (during 2018) decided to suddenly release its own implementation and the request made for a megagrant in 2019 by the original plugin author was rejected too." - 20tab

### 2.3 What It Could Do (Historical Reference)

```python
# PyUnreal-style code (UE4 era, NOT working in UE5)
import unreal_engine as ue
from unreal_engine.classes import StaticMeshActor, PointLightComponent

# Spawn actor
actor = ue.get_editor_world().actor_spawn(StaticMeshActor)

# Set location
actor.set_actor_location(FVector(100, 200, 300))

# Add component
light = actor.add_component(PointLightComponent)
light.LightColor = (255, 100, 50)

# Change code after packaging (unique feature!)
```

### 2.4 Installation (Historical - UE4 Only)

```bash
# Clone to project Plugins/
git clone https://github.com/20tab/UnrealEnginePython

# Requires C++ project (not Blueprint-only)
# Auto-builds on editor restart
# Supports Python 3.6, 3.5, 2.7
```

---

## 3. UE5 Built-in Python Scripting (Editor Only)

### 3.1 What is it?

Epic's **official** Python integration, included with UE5. It is **editor-only** and uses Python 3.11.8 (embedded - no separate Python install needed).

### 3.2 Setup

```
1. Edit > Plugins > Scripting > Enable "Python Editor Script Plugin"
2. Enable "Editor Scripting Utilities" plugin  
3. Restart Editor
4. Edit > Editor Settings > Enable "Python Developer Mode"
5. Restart Editor
```

### 3.3 Ways to Run Python

| Method | Command | Use Case |
|--------|---------|----------|
| **Python Console** | Window > Developer Tools > Python Console | Interactive scripting |
| **Command Line (Full Editor)** | `UnrealEditor-Cmd.exe Project.uproject -ExecutePythonScript="script.py"` | Automation with UI |
| **Command Line (Headless)** | `UnrealEditor-Cmd.exe Project.uproject -run=pythonscript -script="script.py"` | CI/CD, fastest |
| **Remote Execution** | UDP multicast + TCP | External apps (Maya, Blender) |
| **MCP `execute_python`** | Via MCP server | AI agent control |

### 3.4 Real Code Examples

#### Spawn Actor
```python
import unreal

# Method 1: Spawn from Blueprint class
actor_subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
bp_class = unreal.EditorAssetLibrary.load_blueprint_class('/Game/BP_MyAgent')
spawn_location = unreal.Vector(1000.0, 2000.0, 100.0)
spawn_rotation = unreal.Rotator(0.0, 0.0, 0.0)
actor = actor_subsys.spawn_actor_from_class(bp_class, spawn_location, spawn_rotation)
actor.set_actor_label("Agent_001")

# Method 2: Spawn StaticMeshActor
static_mesh_class = unreal.StaticMeshActor.static_class()
mesh_actor = actor_subsys.spawn_actor_from_class(static_mesh_class, unreal.Vector(0, 0, 0))
mesh_comp = mesh_actor.get_component_by_class(unreal.StaticMeshComponent)
```

#### Set Actor Location/Rotation
```python
import unreal

actor = unreal.EditorLevelLibrary.get_selected_level_actors()[0]

# Set location
actor.set_actor_location(unreal.Vector(100.0, 200.0, 50.0), False, False)

# Set rotation
actor.set_actor_rotation(unreal.Rotator(0.0, 45.0, 90.0), False)

# Set both
actor.set_actor_location_and_rotation(
    unreal.Vector(100.0, 200.0, 50.0),
    unreal.Rotator(0.0, 45.0, 0.0),
    False, False
)

# Get transform
transform = actor.get_actor_transform()
print(f"Location: {transform.translation}")
print(f"Rotation: {transform.rotation}")
```

#### Set Material/Color
```python
import unreal

# Load a material
material = unreal.EditorAssetLibrary.load_asset('/Game/Materials/M_Red')

# Apply to actor's mesh component
actor = unreal.EditorLevelLibrary.get_selected_level_actors()[0]
mesh_comp = actor.get_component_by_class(unreal.StaticMeshComponent)

# Set material
mesh_comp.set_material(0, material)

# Create dynamic instance and set color
mid = mesh_comp.create_dynamic_material_instance(0, material)
mid.set_vector_parameter_value('Color', unreal.LinearColor(1.0, 0.0, 0.0, 1.0))
```

#### Control Camera
```python
import unreal

# Get the editor viewport camera
viewport = unreal.EditorLevelLibrary.get_editor_viewport_client()

# Set camera location
viewport.set_view_location(unreal.Vector(5000.0, 5000.0, 3000.0))

# Set camera rotation
viewport.set_view_rotation(unreal.Rotator(-30.0, 45.0, 0.0))

# Focus on actor
actor = unreal.EditorLevelLibrary.get_selected_level_actors()[0]
unreal.EditorLevelLibrary.set_selected_level_actors([actor])
viewport.focus_selected_actor()
```

#### Create Level Sequence (Cinematics)
```python
import unreal

ls_system = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)

# Add a camera
camera = ls_system.create_camera(spawnable=True)

# Set playback range
level_sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
level_sequence.set_playback_start(0)
level_sequence.set_playback_end(300)  # 10 seconds at 30fps
```

### 3.5 Remote Execution (External Python → UE5)

UE5's Python Remote Execution allows external Python scripts to control the editor:

```python
# remote_execution.py - External script sends commands to UE5
import socket
import json
import struct

# UE5 listens on UDP multicast for discovery, then opens TCP for commands
UE_IP = "127.0.0.1"
UE_TCP_PORT = 9998  # Dynamically assigned

def send_command(command):
    """Send Python command to UE5 editor."""
    # 1. UDP broadcast to discover UE5 instances
    # 2. UE5 responds with GUID + TCP port
    # 3. Connect via TCP
    # 4. Send JSON: {"command": "python_code_string"}
    # 5. Receive result
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((UE_IP, UE_TCP_PORT))
    
    payload = json.dumps({"command": command})
    sock.sendall(payload.encode())
    
    result = sock.recv(65536).decode()
    sock.close()
    return result

# Example: Spawn an actor from external Python
send_command("""
import unreal
actor_subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
bp = unreal.EditorAssetLibrary.load_blueprint_class('/Game/BP_Agent')
actor = actor_subsys.spawn_actor_from_class(bp, unreal.Vector(0,0,0))
actor.set_actor_label('RemoteAgent_001')
""")
```

### 3.6 Limitations of Built-in Python

| Limitation | Details |
|-----------|---------|
| **Editor Only** | Cannot run in packaged games (editor scripting only) |
| **Python 3.11.8** | Embedded version; changing requires source rebuild |
| **No Third-party Libraries** | Cannot pip install packages (sandboxed) |
| **Synchronous** | Long-running scripts freeze the editor |
| **Game Thread** | All calls execute on the main thread |

---

## 4. Cesium for Unreal (3D Earth)

### 4.1 What is Cesium for Unreal?

Cesium for Unreal is a **free, open-source (Apache 2.0)** plugin that brings real-world 3D geospatial data to Unreal Engine:

- **High-accuracy global WGS84 globe** with real-world scale
- **Runtime 3D Tiles engine** with LOD streaming and caching
- **Stream massive datasets:** terrain, imagery, 3D cities, photogrammetry
- **Integrated with UE5:** Blueprints, Physics, Collisions, Landscapes, Sequencer
- **Free** for both commercial and non-commercial use

### 4.2 Installation

```
1. Download from Unreal Engine Marketplace (free)
2. Or: Extract pre-release from GitHub CI builds
3. Enable "Cesium for Unreal" plugin
4. Sign in to Cesium ion (optional, for cloud data)
```

### 4.3 Cesium ion Pricing (Cloud Data Streaming)

| Plan | Cost | Storage | Streaming | Sessions | Best For |
|------|------|---------|-----------|----------|----------|
| **Community** | **FREE** | 5 GB | 15 GB/mo | 1,000/mo | Personal, non-commercial |
| Commercial Individual | $149/mo | 50 GB | 150 GB/mo | 5,000/mo | Commercial projects |
| Premium Individual | $499/mo | 250 GB | 500 GB/mo | 10,000/mo | Established user base |

**Community tier includes:**
- Cesium World Terrain (global terrain)
- Bing Maps imagery (1,000 sessions/mo)
- Cesium OSM Buildings (3D buildings worldwide)
- 5 GB storage for custom uploads
- 15 GB/month streaming
- 1,000 Google Photorealistic 3D Tiles root tiles/month

**Free alternatives without Cesium ion:**
- Self-hosted 3D Tiles servers
- Local terrain data imports (heightmaps, GeoTIFF)
- OpenStreetMap data via map3d (see below)

### 4.4 How to Overlay Governance Data on 3D Cities

```python
# UE5 Python: Overlay governance data on Cesium 3D tiles
import unreal
import json

# Load civilization data
civ_data = json.loads('''
{
    "civilizations": [
        {"id": 1, "name": "Atlantis", "lat": 35.0, "lon": -12.0, "territory_radius": 50000},
        {"id": 2, "name": "Hyperborea", "lat": 65.0, "lon": 25.0, "territory_radius": 75000}
    ]
}
''')

# Get the georeference (converts lat/lon to UE coordinates)
georeference = unreal.CesiumGeoreference.get_default_georeference()

for civ in civ_data["civilizations"]:
    # Convert lat/lon/height to UE world coordinates
    ue_origin = georeference.transform_longitude_latitude_height_to_unreal(
        civ["lon"], civ["lat"], 100.0  # height in meters
    )
    
    # Spawn a sphere representing civilization territory
    actor_subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    sphere_class = unreal.EditorAssetLibrary.load_blueprint_class('/Game/BP_TerritorySphere')
    sphere = actor_subsys.spawn_actor_from_class(sphere_class, ue_origin)
    
    # Set scale to match territory radius (in cm, Unreal units)
    radius_cm = civ["territory_radius"] * 100  # meters to cm
    sphere.set_actor_scale3d(unreal.Vector(radius_cm, radius_cm, radius_cm))
    sphere.set_actor_label(f"Territory_{civ['name']}")
    
    # Assign civilization color material
    mid = sphere.get_component_by_class(unreal.StaticMeshComponent).create_dynamic_material_instance(0)
    # Set unique color per civilization...
```

### 4.5 Integration with map3d (github.com/cartesiancs/map3d)

**map3d** is a free MIT-licensed 3D map viewer that:
- Generates **real-world 3D city maps** from OpenStreetMap data
- Built with **React Three Fiber** (Three.js + React)
- Exports as **GLB files** for import into Unreal Engine
- Includes building and road information
- All features free

**Integration Pipeline:**
```
OpenStreetMap Data
       |
       v
+-------------+     +------------------+     +----------------+
|   map3d     | --> |   Export GLB     | --> |  Import to UE5  |
| (R3F viewer)|     |  (3D buildings)  |     | (Static meshes) |
+-------------+     +------------------+     +----------------+
       |
       v
Cesium for Unreal (terrain + satellite imagery as background)
       +
Imported OSM buildings from map3d as overlaid 3D meshes
```

### 4.6 Performance on Consumer Hardware

| Hardware | Scenario | FPS | Notes |
|----------|----------|-----|-------|
| **RTX 4090 + 7950X3D** | Horizon view (lots of Cesium) | 50-70 | GPU ~25%, CPU ~5% |
| **RTX 4090 + 7950X3D** | Top-down 2km view | 120+ | GPU ~65%, CPU ~30% |
| **RTX 2070 + i7-9750H** | Japan 3D Buildings in VR | 20-29 | VR is demanding |
| **RTX 2070 + i7-9750H** | Google Photorealistic 3D Tiles VR | 36-38 | Better optimized data |

**Performance Tips:**
- Zoomed/limited views perform much better than horizon views
- Use `Maximum Screen Space Error` to control LOD quality vs performance
- Enable frustum culling and occlusion culling
- For VR: consider simpler tilesets or lower LOD
- Client-side caching helps (revisiting areas doesn't re-stream)

**For MEOK:** A laptop with GTX 1660+ should handle limited city views at 30+ fps. Global views will be slower.

---

## 5. UE5 + Agent Simulation (47 AI Agents)

### 5.1 Can 47 AI Agents Be Represented as NPCs?

**Absolutely yes.** UE5 has multiple systems for handling agents, and 47 is a trivial number for most approaches.

### 5.2 Mass AI / Mass Entity Framework (Recommended for Scale)

UE5's **Mass Entity Framework** is designed for thousands of agents:

| Agent Count | RTX 4080 | RTX 4060 (Laptop) | PS5/XSX |
|-------------|----------|-------------------|---------|
| 1,000 | 1.2ms | 1.8ms | 2.1ms |
| 5,000 | 2.8ms | 4.5ms | 5.2ms |
| 10,000 | 4.6ms | 7.8ms | 9.1ms |
| 20,000 | 8.2ms | 14.1ms | 16.5ms |

**At 47 agents, the cost is negligible (~0.05ms).**

Key components:
- **MassEntity:** Data-oriented ECS (Entity Component System)
- **MassAI:** High-performance crowd simulation
- **MassNavigation:** Navigation mesh integration
- **MassRepresentation:** Visual LOD system (skeletal → instanced mesh)

### 5.3 Smart Objects + State Trees (Recommended for Agent Logic)

**State Trees** (production-ready in UE5) provide hierarchical decision-making:

```
State Tree: AgentDecisionMaking
|
|-- Idling (default state)
|   |-- Find Smart Objects → Has candidates?
|   |   |-- YES → Smart Objects Branch
|   |   |   |-- Claim Smart Object
|   |   |   |-- Reach Smart Object (path follow)
|   |   |   |-- Use Smart Object (interaction)
|   |   |   |-- Return to Idling
|   |   |-- NO → Wandering
|   |       |-- Pick random destination
|   |       |-- Path follow to destination
|   |       |-- Wait (random time)
|   |       |-- Return to Idling
|
|-- Combat (triggered by threat)
|-- Trading (triggered by economy)
|-- Diplomacy (triggered by relations)
```

**Setup:**
1. Enable "State Tree" and "Gameplay State Tree" plugins
2. Create State Tree asset → Assign schema (StateTreeComponent or StateTreeAIComponent)
3. Add to actor/component → Start logic on BeginPlay

### 5.4 Standard AI Characters (For Detailed Agents)

For the 47 MEOK agents (leaders with unique behaviors), standard AI is sufficient:

| Component | Cost per Agent | 47 Agents Total |
|-----------|---------------|-----------------|
| Animation Blueprint | 0.05-0.15ms | 2.4-7.1ms |
| Behavior Tree | 0.02-0.08ms | 0.9-3.8ms |
| Movement/Pathfinding | 0.03-0.10ms | 1.4-4.7ms |
| Skeletal Mesh Render | 0.02-0.05ms | 0.9-2.4ms |
| Physics | 0.01-0.03ms | 0.5-1.4ms |
| **TOTAL** | **0.13-0.41ms** | **6.1-19.3ms** |

**47 detailed agents: ~6-19ms per frame = 50-165 FPS easily achievable.**

### 5.5 Navigation Meshes

UE5 uses **Recast Navigation** for pathfinding:
- Automatic navmesh generation from level geometry
- Dynamic navmesh updates (for moving obstacles)
- Supports 2D and 3D pathfinding
- Crowd avoidance (RVO2 library) built-in

```python
# Python: Configure navmesh for agent movement
import unreal

# Get navigation system
nav_sys = unreal.NavigationSystemV1.get_navigation_system(unreal.EditorLevelLibrary.get_editor_world())

# Build navmesh (in editor)
nav_sys.build()

# In runtime, AI agents use AI MoveTo nodes (Blueprint) or 
# AIController.MoveToLocation() (C++) for pathfinding
```

### 5.6 Real-Time Agent Decision → UE5 Action Pipeline

```
Python Agent Brain (External)
       |
       | JSON API/WebSocket
       v
+-------------+     +-------------------+     +------------------+
| MCP Server  | --> |  UE5 Python Script | --> |  Spawn/Control   |
| (UE5.8)     |     |  (Editor BP)       |     |  Actors in Level |
+-------------+     +-------------------+     +------------------+
       |                                                |
       | Result/State                                   | Visual Output
       v                                                v
+-------------+                                +------------------+
| State JSON  |                                |  UE5 Renderer    |
| Response    |                                |  (Viewport)      |
+-------------+                                +------------------+
```

---

## 6. Alternatives: Godot 4, Bevy, Three.js

### 6.1 Godot 4.4

| Aspect | Details |
|--------|---------|
| **License** | MIT (completely free, no royalties) |
| **Size** | Editor ~120MB, exported project ~30MB |
| **Language** | GDScript (Python-like), C#, C++ |
| **3D Renderer** | Vulkan, improving but not UE5-class |
| **AI Agents** | NavigationServer can handle 2,000+ with optimization |
| **Pros** | Tiny footprint, fast iteration, free, runs on weak hardware |
| **Cons** | No Nanite/Lumen, smaller ecosystem, 3D not AAA-quality |
| **Best For** | 2D, stylized 3D, fast prototyping, $0 budget |

**Godot Agent Performance:** Community reports 2,000 pathfinding agents at 140 FPS (with batching optimization). 47 agents would be trivial.

```gdscript
# Godot 4: Agent movement example
extends CharacterBody3D

@onready var nav_agent = $NavigationAgent3D
var speed = 5.0

func _physics_process(delta):
    if nav_agent.is_navigation_finished():
        return
    
    var next_pos = nav_agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    velocity = direction * speed
    move_and_slide()

func set_target(target_pos: Vector3):
    nav_agent.set_target_position(target_pos)
```

### 6.2 Bevy (Rust Engine)

| Aspect | Details |
|--------|---------|
| **License** | MIT + Apache 2.0 (dual) |
| **Language** | Rust |
| **Renderer** | Custom render graph, 2D/3D, WebGPU |
| **ECS** | Bevy ECS (data-driven, massively parallel) |
| **Compile Time** | 0.8-3.0 seconds (fast config) |
| **Pros** | Blazing fast ECS, free, open source, modern architecture |
| **Cons** | Rust learning curve, still maturing, smaller ecosystem, breaking API changes |
| **Best For** | ECS-heavy simulations, Rust developers, performance-critical apps |

**Bevy ECS Performance:** The ECS can easily handle 100,000+ entities. For 47 agents, it would be instant.

```rust
// Bevy: Agent movement system
use bevy::prelude::*;

#[derive(Component)]
struct Agent { civilization_id: u32 }

#[derive(Component)]
struct Velocity(Vec3);

fn agent_movement(
    time: Res<Time>,
    mut query: Query<(&mut Transform, &Velocity), With<Agent>>
) {
    for (mut transform, velocity) in query.iter_mut() {
        transform.translation += velocity.0 * time.delta_seconds();
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Update, agent_movement)
        .run();
}
```

### 6.3 Three.js (Web/Browser)

| Aspect | Details |
|--------|---------|
| **License** | MIT |
| **Runtime** | Web Browser (WebGL/WebGPU) |
| **Size** | Library ~600KB minified |
| **3D** | Full 3D with WebGL, works in any browser |
| **Pros** | Runs everywhere, no install, easy deployment, huge ecosystem |
| **Cons** | Performance limited by browser, no built-in AI/navmesh, single-threaded |
| **Best For** | Web-based dashboards, visualization, sharing with others |

**Three.js for MEOK Visualization:**

```javascript
// Three.js: 3D globe with agent markers
import * as THREE from 'three';
import ThreeGlobe from 'three-globe';

// Create globe with real terrain
const globe = new ThreeGlobe()
  .globeImageUrl('//earth_texture.jpg')
  .bumpImageUrl('//earth_bump.jpg')
  .showAtmosphere(true);

// Add agent markers (47 civilizations)
const agents = [
  { lat: 40.7, lon: -74.0, name: 'Agent_1', color: '#ff0000' },
  // ... 46 more
];

globe.pointsData(agents)
  .pointLat(d => d.lat)
  .pointLng(d => d.lon)
  .pointColor(d => d.color)
  .pointAltitude(0.1)
  .pointRadius(0.5);

// Add arc lines between agents (diplomacy/connections)
globe.arcsData(diplomacyLinks)
  .arcColor(d => d.active ? '#00ff00' : '#444444')
  .arcDashLength(0.4)
  .arcDashGap(2)
  .arcDashAnimateTime(1000);
```

### 6.4 Comparison Matrix for MEOK

| Criteria | UE5 + MCP | Godot 4 | Bevy | Three.js |
|----------|-----------|---------|------|----------|
| **Cost** | Free (5% royalty if $1M+) | Free (no royalty) | Free | Free |
| **Budget Fit ($0)** | Excellent | Excellent | Excellent | Excellent |
| **47 Agents Performance** | Trivial (<1ms) | Trivial | Trivial | Moderate |
| **Real-World 3D Maps** | Excellent (Cesium) | Limited | Limited | Good (CesiumJS) |
| **Python Integration** | Built-in (Editor) | Limited (GDExt) | None | Full (NPM) |
| **AI Agent Control** | Excellent (MCP) | Manual | Manual | Manual |
| **Visual Quality** | Photorealistic | Good/Stylized | Good | Moderate |
| **Laptop Performance** | RTX 3060+ ideal | GTX 1050+ fine | GTX 1050+ fine | Any GPU |
| **Learning Curve** | Steep | Low | Very High | Low |
| **Project Size** | 60-100GB install | 120MB | Cargo-based | Browser |
| **Web Deployment** | No | Yes (Web export) | Yes (WASM) | **Native** |
| **Team Size** | 1+ (with AI help) | 1 | 1 (Rust exp.) | 1 |
| **Civilization Viz** | Excellent 3D | Good 3D | Good 3D | Good 3D |

### 6.5 Verdict for MEOK

| Use Case | Recommendation |
|----------|---------------|
| **Best visual quality + AI control** | **UE5.8 + MCP** (our pick) |
| **Best for $0 budget + weak laptop** | **Godot 4** |
| **Best for web-based sharing** | **Three.js + CesiumJS** |
| **Best for Rust/performance purists** | **Bevy** |
| **Best overall for MEOK** | **UE5.8 (free, MCP built-in, Cesium free tier)** |

---

## 7. Architecture Document

### 7.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MEOK 3D WORLD SIMULATION                             │
│                                                                              │
│  ┌──────────────────┐      HTTP/WebSocket      ┌──────────────────────┐    │
│  │                  │ ◄──────────────────────► │                      │    │
│  │  Python Agent    │      MCP Protocol        │  Unreal Engine 5.8   │    │
│  │  Brain (MEOK)    │                          │  + MCP Plugin        │    │
│  │                  │      Commands:           │                      │    │
│  │  - 47 Agents     │      - spawn_actor       │  ┌────────────────┐  │    │
│  │  - 12 Civs       │      - set_transform     │  │   3D World     │  │    │
│  │  - Decisions     │      - set_material      │  │                │  │    │
│  │  - Governance    │      - control_camera    │  │  Cesium Globe  │  │    │
│  │                  │      - play_sequence     │  │  + Agents      │  │    │
│  │  (Local/Python)  │                          │  │  + Cities      │  │    │
│  └──────────────────┘      State/Feedback      │  │  + Territories │  │    │
│           ▲                                         └────────────────┘  │    │
│           │                JSON Responses            │                     │    │
│           │                                          ▼                     │    │
│           │                                   ┌──────────────┐             │    │
│           │                                   │   Renderer   │             │    │
│           │                                   │  (Viewport)  │             │    │
│           │                                   └──────────────┘             │    │
│           │                                                                 │    │
│  ┌────────┴────────┐                                                        │    │
│  │   Optional:     │                                                        │    │
│  │   Direct Python │  ─────►  UE5 Python Script  ─────►  Actor Control    │    │
│  │   (Editor only) │     (Editor Script Plugin)       (Built-in API)       │    │
│  └─────────────────┘                                                        │    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Data Flow

```
Step 1: Agent Makes Decision (Python)
┌─────────────────────────────────────────┐
│ agent.decide() → {"move": [x, y, z],   │
│                   "action": "build",    │
│                   "target": "city_A"}   │
└──────────────────┬──────────────────────┘
                   │ JSON
                   ▼
Step 2: MCP Client Sends Command
┌─────────────────────────────────────────┐
│ tools/call → {                          │
│   "name": "control_actor",              │
│   "arguments": {                        │
│     "action": "spawn",                  │
│     "blueprintPath": "/Game/BP_Agent",  │
│     "location": {"x": 100, "y": 200}    │
│   }                                     │
│ }                                       │
└──────────────────┬──────────────────────┘
                   │ HTTP POST
                   ▼
Step 3: UE5 MCP Server Processes
┌─────────────────────────────────────────┐
│ 1. Receive JSON-RPC request             │
│ 2. Route to Toolset Registry            │
│ 3. Execute on Game Thread               │
│ 4. Spawn actor / set transform          │
│ 5. Return result                        │
└──────────────────┬──────────────────────┘
                   │ JSON Response
                   ▼
Step 4: Feedback to Agent
┌─────────────────────────────────────────┐
│ {"success": true,                       │
│  "actorName": "Agent_001",              │
│  "location": [100.0, 200.0, 50.0]}     │
└─────────────────────────────────────────┘
```

### 7.3 Latency Estimates

| Operation | Latency | Notes |
|-----------|---------|-------|
| **MCP Tool Call (local)** | 5-20ms | HTTP overhead + game thread sync |
| **Actor Spawn** | 1-5ms | Depends on complexity |
| **Transform Update** | <1ms | Direct property set |
| **Material Change** | 2-5ms | Dynamic material instance |
| **Camera Move** | <1ms | Viewport update |
| **Full Agent Update Cycle** | 20-50ms | Decision → Spawn → Position → Material |
| **47 Agents Batch Update** | 50-200ms | Depends on per-agent complexity |
| **Cesium Tile Stream** | 100ms-2s | Network dependent, cached after first load |
| **Python Script Execution** | 10-100ms | Editor scripting overhead |

### 7.4 Scaling to 47+ Agents

**47 agents is a VERY small number for UE5.** Here's the scaling analysis:

| Approach | 47 Agents | 500 Agents | 5,000 Agents | 10,000+ |
|----------|-----------|------------|--------------|---------|
| **Standard AI Characters** | 50-165 FPS | 5-15 FPS | N/A | N/A |
| **Mass Entity + LOD** | 1000+ FPS | 500+ FPS | 120+ FPS | 60+ FPS |
| **Instanced Static Mesh** | 1000+ FPS | 500+ FPS | 200+ FPS | 100+ FPS |

**Recommendation for MEOK:**
- Use **Standard AI Characters** for the 47 unique agents (leaders, important NPCs)
- Use **Mass Entity** if scaling to thousands of background population agents
- Use **Instanced Static Mesh** for territory visualization markers

### 7.5 Budget Requirements (Can It Run on Nick's Laptop?)

#### Minimum Specs for UE5 + Cesium + 47 Agents

| Component | Minimum | Recommended | Nick's Laptop (Estimated) |
|-----------|---------|-------------|--------------------------|
| **OS** | Windows 10 64-bit | Windows 11 | Should be fine |
| **CPU** | 6-core (i5/Ryzen 5) | 8-core+ | Check: Need 6+ cores |
| **RAM** | 16 GB | 32 GB | **Need 16GB minimum** |
| **GPU** | GTX 1060 6GB | RTX 3060+ | Check: DX12 support needed |
| **Storage** | 100 GB SSD | 500 GB NVMe | UE5 is 60-100GB |
| **VRAM** | 6 GB | 8 GB+ | Cesium needs 4GB+ |

#### Cost Breakdown ($0 Budget)

| Item | Cost | Notes |
|------|------|-------|
| Unreal Engine 5.8 | **$0** | Free, 5% royalty only after $1M revenue |
| Cesium for Unreal Plugin | **$0** | Apache 2.0 open source |
| Cesium ion Community | **$0** | 15GB/mo streaming, 5GB storage |
| MCP Plugin (Official) | **$0** | Built into UE5.8 |
| Python Scripting | **$0** | Built into UE5 |
| **Total** | **$0** | |

#### Running on a Laptop: Tips

```
1. UE5 Project Settings > Engine > Rendering:
   - Disable Ray Tracing
   - Disable Lumen (use baked lighting instead)
   - Set Reflection Method to None
   - Use Forward Shading (faster on lower-end GPUs)

2. Cesium Settings:
   - Maximum Screen Space Error: 32 (higher = lower quality, faster)
   - Enable Frustum Culling Only
   - Preload ancestors: False
   - Loading Descendant Limit: 2000

3. Agent Optimization:
   - Use simple StaticMesh for distant agents
   - Skeletal mesh only for agents within 100m of camera
   - Disable collision on non-interactive agents
   - Tick rate: 10-30 FPS for agents (not every frame)
```

### 7.6 Recommended MEOK Architecture

```python
# meok_ue5_bridge.py - Complete bridge implementation

import unreal
import json
import asyncio
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AgentState:
    id: int
    civilization_id: int
    name: str
    position: tuple  # (x, y, z) in UE coordinates
    action: str
    color: str

class MEOKUE5Bridge:
    """Bridge between MEOK Python agent system and UE5 visualization."""
    
    def __init__(self):
        self.actor_subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        self.georeference = unreal.CesiumGeoreference.get_default_georeference()
        self.agent_blueprint = unreal.EditorAssetLibrary.load_blueprint_class('/Game/BP_Agent')
        self.agents: Dict[int, unreal.Actor] = {}
    
    def spawn_agent(self, agent_state: AgentState) -> unreal.Actor:
        """Spawn an agent actor in the UE5 world."""
        # Convert lat/lon to UE coordinates (if using Cesium)
        # Or use direct coordinates
        location = unreal.Vector(*agent_state.position)
        
        actor = self.actor_subsys.spawn_actor_from_class(
            self.agent_blueprint, location
        )
        actor.set_actor_label(f"Agent_{agent_state.name}")
        
        # Set color based on civilization
        mesh = actor.get_component_by_class(unreal.StaticMeshComponent)
        if mesh:
            mid = mesh.create_dynamic_material_instance(0)
            color = self._hex_to_linear(agent_state.color)
            mid.set_vector_parameter_value('BaseColor', color)
        
        self.agents[agent_state.id] = actor
        return actor
    
    def update_agent_position(self, agent_id: int, new_position: tuple):
        """Update agent position (called each tick/decision cycle)."""
        if agent_id in self.agents:
            actor = self.agents[agent_id]
            actor.set_actor_location(
                unreal.Vector(*new_position), 
                sweep=False, 
                teleport=False
            )
    
    def update_agent_visual(self, agent_id: int, color: str = None, 
                           scale: float = None):
        """Update agent visual properties."""
        if agent_id not in self.agents:
            return
        
        actor = self.agents[agent_id]
        
        if color:
            mesh = actor.get_component_by_class(unreal.StaticMeshComponent)
            if mesh and mesh.get_material(0):
                mid = mesh.create_dynamic_material_instance(0)
                mid.set_vector_parameter_value('BaseColor', 
                    self._hex_to_linear(color))
        
        if scale:
            actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    
    def focus_camera_on_agent(self, agent_id: int):
        """Move editor camera to focus on an agent."""
        if agent_id in self.agents:
            actor = self.agents[agent_id]
            viewport = unreal.EditorLevelLibrary.get_editor_viewport_client()
            
            loc = actor.get_actor_location()
            viewport.set_view_location(loc + unreal.Vector(-500, -500, 500))
            viewport.set_view_rotation(unreal.Rotator(-45, 45, 0))
    
    def batch_update(self, agent_states: List[AgentState]):
        """Update all agents in a single batch (performance)."""
        with unreal.ScopedSlowTask(len(agent_states), "Updating Agents") as task:
            for state in agent_states:
                if state.id not in self.agents:
                    self.spawn_agent(state)
                else:
                    self.update_agent_position(state.id, state.position)
                    self.update_agent_visual(state.id, state.color)
                task.enter_progress_frame(1)
    
    def _hex_to_linear(self, hex_color: str) -> unreal.LinearColor:
        """Convert hex color to UE LinearColor."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return unreal.LinearColor(r, g, b, 1.0)
    
    def clear_all(self):
        """Remove all agent actors."""
        for actor in self.agents.values():
            actor.destroy_actor()
        self.agents.clear()

# Usage Example
bridge = MEOKUE5Bridge()

# From MEOK agent system
agents = [
    AgentState(1, 1, "Atlantis_Leader", (1000, 2000, 100), "idle", "#FF0000"),
    AgentState(2, 2, "Hyperborea_Leader", (3000, 4000, 100), "move", "#00FF00"),
    # ... 45 more
]

bridge.batch_update(agents)
bridge.focus_camera_on_agent(1)
```

---

## 8. Final Recommendation

### 8.1 Recommended Stack for MEOK

| Layer | Technology | Cost | Why |
|-------|-----------|------|-----|
| **Game Engine** | Unreal Engine 5.8 | $0 | Best visual quality, official MCP support |
| **AI Control** | UE5.8 MCP Plugin | $0 | Native AI agent integration |
| **3D Earth** | Cesium for Unreal | $0 | Real-world terrain, free tier sufficient |
| **Agent Logic** | Python (external) + MCP | $0 | Full Python ecosystem |
| **Agent Viz** | UE5 Python Scripting | $0 | Built-in, editor control |
| **Cities/Buildings** | map3d → GLB → UE5 | $0 | OSM data, free export |

### 8.2 Implementation Roadmap

```
Phase 1: Setup (Day 1)
├── Install UE5.8 (via Epic Games Launcher)
├── Create new MEOK project
├── Enable Python Editor Script Plugin
├── Enable Cesium for Unreal plugin
├── Enable MCP plugin
└── Verify MCP connection with Claude Code

Phase 2: World Building (Days 2-3)
├── Set up Cesium georeference
├── Configure Cesium World Terrain + OSM Buildings
├── Create agent territory visualization BP
├── Set up territory color materials (12 civilizations)
└── Create agent character Blueprint

Phase 3: Python Bridge (Days 4-5)
├── Implement MEOKUE5Bridge class
├── Create agent spawn/update pipeline
├── Implement territory overlay system
├── Add camera focus functionality
└── Test with 47 agent batch update

Phase 4: MCP Integration (Days 6-7)
├── Write custom MEOK toolset (Python)
├── Register tools with Toolset Registry
├── Test natural language agent control
├── Implement "spawn civilization" MCP tool
└── Implement "focus on agent" MCP tool

Phase 5: Visualization Polish (Days 8-10)
├── Add day/night cycle (Cesium)
├── Add territory boundary lines
├── Add agent labels/nameplates
├── Create cinematic camera sequences
└── Performance optimization for laptop

Phase 6: Real-Time Pipeline (Days 11-14)
├── Connect MEOK decision engine to UE5 bridge
├── Implement real-time agent position updates
├── Add decision → action → visual feedback loop
├── Stress test with 47 simultaneous agents
└── Polish and iterate
```

### 8.3 Quick Start Script

```bash
#!/bin/bash
# meok_quickstart.sh - Get MEOK running in UE5.8

echo "=== MEOK UE5.8 Setup ==="

# 1. Install UE5.8 (if not already installed)
# Via Epic Games Launcher: https://store.epicgames.com/en-US/download

# 2. Create project directory
mkdir -p ~/MEOK-UE5 && cd ~/MEOK-UE5

# 3. Create basic project structure
mkdir -p Content/{Blueprints,Materials,Maps,Meshes,Textures}
mkdir -p Plugins

# 4. Create Python bridge script
cat > meok_bridge.py << 'EOF'
import unreal
import json

class MEOKBridge:
    def __init__(self):
        self.actor_subsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        print("MEOK Bridge initialized")
    
    def spawn_agents_from_json(self, json_path):
        with open(json_path) as f:
            data = json.load(f)
        for agent in data.get("agents", []):
            loc = unreal.Vector(agent["x"]*100, agent["y"]*100, agent["z"]*100)
            bp = unreal.EditorAssetLibrary.load_blueprint_class('/Game/BP_Agent')
            actor = self.actor_subsys.spawn_actor_from_class(bp, loc)
            actor.set_actor_label(agent["name"])
            print(f"Spawned: {agent['name']}")

# Run: unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
# Then: bridge = MEOKBridge(); bridge.spawn_agents_from_json("agents.json")
EOF

# 5. Create sample agent data
cat > agents.json << 'EOF'
{
  "agents": [
    {"name": "Atlantis_Leader", "x": 10, "y": 20, "z": 5, "civ": 1},
    {"name": "Hyperborea_Leader", "x": 30, "y": 40, "z": 5, "civ": 2},
    {"name": "Lemuria_Leader", "x": 50, "y": 60, "z": 5, "civ": 3}
  ]
}
EOF

echo "Setup complete! Next steps:"
echo "1. Open Epic Games Launcher, install UE5.8"
echo "2. Create new Blank C++ project in ~/MEOK-UE5"
echo "3. Enable Plugins: Python Editor Script, Cesium for Unreal, MCP"
echo "4. Open Python Console: Window > Developer Tools > Python Console"
echo "5. Run: exec(open('meok_bridge.py').read())"
echo "6. Connect Claude Code: claude mcp add ue5 --transport http http://localhost:8000/mcp"
```

---

## 9. Key Resources

### Official Documentation
- **UE5.8 MCP Docs:** https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor
- **UE5 Python Scripting:** https://dev.epicgames.com/documentation/unreal-engine/scripting-the-unreal-editor-using-python
- **Cesium for Unreal:** https://cesium.com/platform/cesium-for-unreal/
- **Cesium ion Pricing:** https://cesium.com/platform/cesium-ion/pricing/

### GitHub Repositories
- **UE5.8 Official MCP:** Built into UE5.8 (search "ModelContextProtocol" in plugins)
- **ChiR24/Unreal_mcp:** https://github.com/ChiR24/Unreal_mcp (200+ tools)
- **chongdashu/unreal-mcp:** https://github.com/chongdashu/unreal-mcp
- **remiphilippe/mcp-unreal:** https://github.com/remiphilippe/mcp-unreal
- **20tab/UnrealEnginePython:** https://github.com/20tab/UnrealEnginePython (ON HOLD)
- **cartesiancs/map3d:** https://github.com/cartesiancs/map3d
- **vasturiano/three-globe:** https://github.com/vasturiano/three-globe

### Community Resources
- **MCP Specification:** https://modelcontextprotocol.io/
- **Cesium Community Forum:** https://community.cesium.com/
- **Unreal Engine Forums:** https://forums.unrealengine.com/
- **StraySpark Mass AI Guide:** https://www.strayspark.studio/blog/crowd-traffic-simulation-ue5-mass-ai

---

## 10. Summary

| Question | Answer |
|----------|--------|
| **UE5.8 available?** | Yes, released June 17, 2026 |
| **MCP built-in?** | Yes, official Experimental plugin |
| **Can Claude control UE5?** | Yes, via MCP - spawn actors, materials, cameras, Blueprints |
| **PyUnreal maintained?** | No, on hold since 2020. Use built-in Python instead |
| **Python in UE5 capable?** | Yes, editor-only, spawn actors, control cameras, materials |
| **Cesium free?** | Yes, plugin is Apache 2.0. ion has free Community tier |
| **47 agents possible?** | Trivial. UE5 handles 10,000+ via Mass Entity |
| **Laptop capable?** | Yes, with settings lowered. GTX 1660+ recommended |
| **Total cost?** | **$0** |
| **Best alternative?** | Godot 4 (lighter), Three.js (web), Bevy (Rust/ECS) |
| **Recommended stack?** | **UE5.8 + MCP + Cesium + Python Bridge** |

---

*Document generated for MEOK project. All information verified as of June 2026.*
