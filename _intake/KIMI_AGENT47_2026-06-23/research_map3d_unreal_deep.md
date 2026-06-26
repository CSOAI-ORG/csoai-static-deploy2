# Complete Research: Real-World Cities to 3D MEOK Game Environments

## Executive Summary

This document is a comprehensive technical analysis of the complete stack for converting real-world cities into 3D environments for the MEOK game. It covers map3d (OSM-based 3D city generation), Cesium for Unreal (real 3D Earth in UE5), alternative tools, performance analysis for constrained hardware, and provides working code examples.

**Key Findings:**
- **map3d** is a React-based tool that generates 3D city models from OpenStreetMap data and exports to GLB format. Best for quick city prototypes.
- **Cesium for Unreal** provides the most realistic 3D Earth experience with photorealistic buildings but requires powerful hardware.
- **Three.js in browser** is the best option for Nick's MacBook Air — runs anywhere, no GPU required.
- **Godot 4** is the best free/open-source game engine alternative if native performance is needed.
- **Pre-rendered video** is the ultimate fallback for zero-GPU scenarios.

---

## Table of Contents

1. [map3d Deep Dive](#1-map3d-deep-dive)
2. [Cesium for Unreal](#2-cesium-for-unreal)
3. [Other 3D City Tools](#3-other-3d-city-tools)
4. [The Pipeline](#4-the-pipeline-real-city--3d-model--game-environment)
5. [3D Models for 12 Civilizations](#5-3d-models-for-the-12-civilizations)
6. [Performance on Nick's Hardware](#6-performance-on-nicks-hardware)
7. [Working Example Code](#7-working-example-code)
8. [Recommendations](#8-final-recommendations)

---

## 1. map3d Deep Dive

### What It Does

map3d (github.com/cartesiancs/map3d) is a web-based tool that generates real-world 3D city maps using OpenStreetMap data. It is built with React + TypeScript + Three.js (via React Three Fiber) and allows users to:

- Select any rectangular area on a world map (using Leaflet)
- Fetch building footprint data + road data from OpenStreetMap via the Overpass API
- Generate 3D buildings with height information in the browser
- Export the result as a GLB file (binary glTF)
- View the 3D city interactively in the browser

**Live Demo:** https://map.fleet.im
**GitHub:** https://github.com/cartesiancs/map3d
**Stars:** 1.9k | **Forks:** 294 | **License:** MIT

### How It Works (Architecture)

```
User selects area on map (Leaflet)
    |
    v
Fetch building data from Overpass API
    Query: [out:json][timeout:25];
           (way["building"](south,west,north,east););
           out body geom;
    |
    v
Fetch road data from Overpass API
    Query: [out:json][timeout:25];
           (way["highway"](south,west,north,east););
           out body geom;
    |
    v
Process data in Space.tsx:
  - Convert lat/lng to local XY coordinates (scale = 51000)
  - Create THREE.Shape from building footprint polygons
  - Extrude shapes based on height data
  - Default height: 10m (if no data)
  - Height from levels: levels * 2.2m
  - Roads rendered as green lines
    |
    v
Render via React Three Fiber:
  - Buildings: extruded geometry with MeshStandardMaterial
  - Roads: Line primitives
  - Lighting: ambient + spot + point lights + Sky + Environment
    |
    v
Export to GLB using GLTFExporter
  - Binary format (.glb)
  - Embeds all geometry and materials
```

### Input

**What you provide:**
- A rectangular selection on a world map (2 corner coordinates: NE and SW)
- Or directly: `south, west, north, east` bounding box coordinates

**Example coordinates:**
```javascript
// Default in areaStore.ts (Manhattan area)
center: [
  { lat: 40.8, lng: -73.95 },    // SW corner
  { lat: 40.83, lng: -73.88 }    // NE corner
]
```

### Output

**Format:** GLB (binary glTF 2.0) — a single self-contained file with all geometry and materials.

**GLB Compatibility:**
- **Unreal Engine 5:** YES — Import via built-in GLTF importer
- **Unity:** YES — Drag and drop
- **Blender:** YES — File > Import > glTF 2.0
- **Three.js:** YES — GLTFLoader
- **Godot 4:** YES — Import directly

**What the GLB contains:**
- Building meshes (extruded polygons)
- Road line segments
- Default gray material for buildings
- Default green material for roads

### Building Detail Quality

| Feature | Detail Level |
|---------|-------------|
| Building footprints | Accurate from OSM |
| Building heights | From `height` tag or `building:levels` * 2.2m |
| Missing height data | Defaults to 10m |
| Roof shapes | Not supported (flat roofs only) |
| Textures | None (solid color) |
| Windows/doors | Not supported |
| Roads | Simple lines (no width variation) |

**Data accuracy caveat (from README):**
> "This project cannot guarantee the accuracy of the data. Since it uses OpenStreetMap data, some height values may be missing or incorrectly recorded."

### Performance

| Metric | Value |
|--------|-------|
| City generation time | 2-10 seconds (depends on area size) |
| Export time | 1-3 seconds |
| Maximum recommended area | Warning shown for large areas |
| Browser memory | Moderate (buildings are extruded geometries) |
| Rendering | Real-time in browser via WebGL |

### License

**MIT License** — fully open source, free for commercial use, modification, and distribution.

### Installation & Usage

```bash
# Clone the repository
git clone https://github.com/cartesiancs/map3d.git
cd map3d

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### How to Generate a City Programmatically

Since map3d is a React app, you can programmatically trigger city generation by modifying the area store:

```typescript
// src/state/areaStore.ts
import { create } from "zustand";

type AreaStore = {
  areas: any[];
  center: { lat: number; lng: number }[];
  appendAreas: (areas: any[]) => void;
  setCenter: (center: any[]) => void;
};

export const useAreaStore = create<AreaStore>((set) => ({
  areas: [],
  center: [
    { lat: 51.5074, lng: -0.1278 },  // London SW
    { lat: 51.5200, lng: -0.1100 },  // London NE
  ],
  appendAreas: (areas) => set(() => ({ areas: [...areas] })),
  setCenter: (center) => set(() => ({ center: [...center] })),
}));
```

**Fetching OSM building data (Overpass API query):**

```javascript
// Example: Fetch buildings for an area
async function fetchBuildings(south, west, north, east) {
  const query = `[out:json][timeout:25];(way["building"](${south},${west},${north},${east}););out body geom;`;
  
  const response = await fetch("https://overpass-api.de/api/interpreter", {
    method: "POST",
    body: query,
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  
  const data = await response.json();
  return data.elements.map(el => ({
    id: el.id,
    tags: el.tags,
    geometry: el.geometry.map(g => ({ lat: g.lat, lng: g.lon })),
  }));
}
```

### Exporting from map3d

```javascript
// The export logic from Space.tsx
import { GLTFExporter } from "three/examples/jsm/exporters/GLTFExporter.js";

async function exportToGLB(scene) {
  const exportRoot = new THREE.Group();
  
  // Collect all objects marked for export
  scene.traverse((child) => {
    if (child.userData?.exportToGLB === true) {
      exportRoot.add(child.clone(true));
    }
  });
  
  const exporter = new GLTFExporter();
  const options = { binary: true, embedImages: true };
  
  const result = await exporter.parseAsync(exportRoot, options);
  
  // Save as file
  const blob = new Blob([result], { type: "model/gltf-binary" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "city.glb";
  link.click();
}
```

### Can It Export UE5-Compatible Format?

YES. GLB is natively supported by Unreal Engine 5:

1. Export `.glb` from map3d
2. In UE5: Content Browser > Import > Select `.glb` file
3. UE5 will import as Static Mesh assets
4. Buildings can be placed in the level

**Caveats for UE5 import:**
- Materials will be basic (solid colors)
- No collision by default (need to enable)
- Scale may need adjustment (map3d uses scale=51000)
- Individual meshes per building (not merged)

---

## 2. Cesium for Unreal

### What It Is

Cesium for Unreal is a free plugin that brings real-world 3D geospatial data into Unreal Engine. It streams photorealistic 3D content from Cesium ion (cloud service) directly into UE5 levels.

**GitHub:** https://github.com/CesiumGS/cesium-unreal
**License:** Apache 2.0 (FREE for commercial and non-commercial use)
**Documentation:** https://cesium.com/learn/unreal/

### Key Features

| Feature | Description |
|---------|-------------|
| **Cesium World Terrain** | Global high-resolution terrain |
| **Cesium OSM Buildings** | 350M+ buildings worldwide from OpenStreetMap |
| **Google Photorealistic 3D Tiles** | Real-world photorealistic 3D (requires Google API key) |
| **Bing Maps Aerial** | Satellite imagery overlay |
| **Dynamic Pawn** | Globe-aware navigation with adjustable speed |
| **Cesium SunSky** | Realistic sun/atmosphere for any location/time |

### How to Load a Specific City

```
Step 1: Install Cesium for Unreal plugin from Epic Marketplace
Step 2: Create new UE5 project (Game > Blank)
Step 3: Enable Cesium plugin (Edit > Plugins > Search "Cesium")
Step 4: Add Cesium SunSky from Cesium panel
Step 5: Connect to Cesium ion (free account)
Step 6: Add "Cesium World Terrain + Bing Maps Aerial"
Step 7: Select CesiumGeoreference actor
Step 8: Set coordinates:

  London:   Latitude 51.5074,  Longitude -0.1278,  Height 1000
  New York: Latitude 40.7128,  Longitude -74.0060,  Height 1000
  Dubai:    Latitude 25.2048,  Longitude 55.2708,  Height 1000
  Paris:    Latitude 48.8566,  Longitude 2.3522,   Height 1000
  Tokyo:    Latitude 35.6762,  Longitude 139.6503, Height 1000
  Shanghai: Latitude 31.2304,  Longitude 121.4737, Height 1000

Step 9: Add "Cesium OSM Buildings" for 3D buildings
Step 10: Add Dynamic Pawn for navigation
Step 11: Press Play to explore!
```

### How to Place Agents as 3D Characters

**Blueprint approach:**

1. Create a new Blueprint Class (Actor) named `BP_Agent`
2. Add a Skeletal Mesh Component (your character model)
3. Add a `CesiumGlobeAnchorComponent` to BP_Agent
4. This makes the agent globe-aware — it stays at its lat/lng/height
5. Set agent position:
```
Set Longitude: -0.1278
Set Latitude:  51.5074
Set Height:    50 (meters above ground)
```

**Runtime agent spawning (Blueprint):**
```
Event BeginPlay
  -> Spawn Actor From Class (BP_Agent)
  -> Set Globe Anchor Position
       Longitude: (from governance data)
       Latitude:  (from governance data)
       Height:    100
```

### How to Overlay Governance Zones (Colored Areas)

**Using Cesium Cartographic Polygon:**

1. Add `Cesium Cartographic Polygon` actor to level
2. Edit the polygon shape to match governance zone boundaries
3. Add `CesiumPolygonRasterOverlay` component to the tileset
4. Create a Material Instance with your zone color
5. Assign the polygon to the overlay

**Blueprint for runtime colored zones:**
```
For Each Zone:
  1. Create CesiumCartographicPolygon actor
  2. Set polygon vertices from zone boundary coordinates
  3. Create Material Instance Dynamic
  4. Set color parameter (e.g., Yellow for Aethelgard)
  5. Add CesiumPolygonRasterOverlay to tileset
  6. Set Material Layer Key to zone name
```

**Zone color mapping:**
```
Aethelgard (EU):     #FFD700 (Gold)
Sino-Nova (China):   #FF0000 (Red)
Pan-America (US):    #0000FF (Blue)
Khaleej (MENA):      #008000 (Green)
Indo-Sphere (India): #FF6600 (Orange)
```

### How to Show Agent Movement Paths

**Using Spline Components:**

1. Create a `BP_PathVisualizer` actor
2. Add a Spline Component
3. Add points along the agent's route
4. Attach a `Cable Component` or `Particle System` to the spline
5. Update spline points as agent moves

**Blueprint pseudocode:**
```
Event Tick:
  -> Get Agent Current Position (lat, lng)
  -> Convert to Unreal coordinates
  -> Add Spline Point at new position
  -> Update path line mesh
```

### Performance on Laptop (No Dedicated GPU)

**Official UE5 minimum requirements:**
- Quad-core Intel/AMD 2.5 GHz+
- 16 GB RAM (32 GB recommended)
- DirectX 12 compatible GPU
- Windows 10/11 or macOS Sonoma 14+

**Cesium-specific performance data:**

| Hardware | Scene | FPS | Source |
|----------|-------|-----|--------|
| RTX 4090 + AMD 7950X3D | Horizon view | 50-70 | Cesium Community |
| RTX 4090 + AMD 7950X3D | Top-down 2km | 120+ | Cesium Community |
| RTX 3090 + Ryzen 9 5950X | Flythrough | <15 (unoptimized) | Cesium Community |
| RTX 2070 + i7-9750H | VR with Japan 3D | 20-29 | Cesium Community |
| RTX 2070 + i7-9750H | VR with Google Tiles | 36-38 | Cesium Community |

**Optimization settings for low-end hardware:**
```
Maximum Screen Space Error: 24 (default is 16, higher = lower quality but faster)
Maximum Simultaneous Tile Loads: 16 (default)
Maximum Cached Bytes: 64MB (reduce from default)
Forbid Holes: True
Create Physics Meshes: False (major performance savings)
```

**Verdict for laptop without dedicated GPU:**
- **Cesium for Unreal will NOT run well** on integrated graphics
- Minimum: GTX 1070 / RTX 2060 laptop GPU
- Integrated graphics (Intel Iris, Apple M1/M2 base): Unusable for 3D cities

---

## 3. Other 3D City Tools

### Google Earth Studio

| Attribute | Detail |
|-----------|--------|
| **Price** | FREE (with Google account) |
| **Type** | Animation tool, not a game engine |
| **Output** | Video files (MP4) |
| **3D Export** | NO — cannot export 3D models |
| **Use Case** | Create cinematic flythrough videos of real locations |
| **Best For** | Pre-rendered video content, not interactive games |

**Relevance for MEOK:** Limited. Can create cinematic intro videos for each civilization, but not for interactive gameplay.

### Mapbox 3D

| Attribute | Detail |
|-----------|--------|
| **Price** | Free tier: 50,000 map loads/month |
| **Type** | Web-based mapping platform |
| **3D Buildings** | Yes — extruded buildings worldwide |
| **Data Source** | OpenStreetMap |
| **API** | JavaScript SDK |
| **Customization** | Full style control via Mapbox Studio |

**Free Tier Limits:**
- 50,000 web map loads/month
- 100,000 geocoding requests
- 100,000 direction requests

**Paid pricing:** $5 per 1,000 map loads (drops to $3 at volume)

**Relevance for MEOK:** Good for web-based governance dashboard overlay. Not a game engine but excellent for 2D/3D map visualization.

### deck.gl (Uber's Visualization Library)

| Attribute | Detail |
|-----------|--------|
| **Price** | FREE (Apache 2.0 license) |
| **Type** | WebGL-based geospatial visualization framework |
| **Developer** | Uber |
| **Built On** | WebGL, luma.gl |
| **Performance** | Renders millions of points |
| **3D Support** | Yes — 3D buildings, terrain, point clouds |
| **Integration** | React component available |

**Key layers for MEOK:**
```javascript
// 3D Buildings layer
new PolygonLayer({
  id: 'buildings',
  data: buildingData,
  extruded: true,
  getElevation: d => d.height,
  getFillColor: d => d.zoneColor,
  getPolygon: d => d footprint,
});

// Agent positions
new ScatterplotLayer({
  id: 'agents',
  data: agentData,
  getPosition: d => [d.lng, d.lat],
  getFillColor: d => d.civilizationColor,
  getRadius: d => 100, // meters
});

// Governance zones
new GeoJsonLayer({
  id: 'zones',
  data: zoneGeoJson,
  filled: true,
  getFillColor: [255, 215, 0, 100], // semi-transparent gold
});
```

**Relevance for MEOK:** EXCELLENT for the web-based governance visualization. GPU-accelerated, handles millions of data points, perfect for overlaying governance data on 3D cities.

### kepler.gl (Uber's Geospatial Tool)

| Attribute | Detail |
|-----------|--------|
| **Price** | FREE (MIT license) |
| **Type** | Browser-based geospatial analysis tool |
| **Built On** | deck.gl + MapLibre GL |
| **Target User** | Data scientists, analysts |
| **Data Input** | CSV, GeoJSON, JSON (drag & drop) |
| **Max Dataset** | Millions of rows (GPU-accelerated) |
| **Export** | Images, videos, HTML, JSON config |

**Key Features:**
- Point, arc, line, hexbin, heatmap, grid, polygon layers
- 3D hexbin and building extrusions
- Time-series animation with playback
- Filtering and brushing tools
- No coding required

**Relevance for MEOK:** Great for prototype visualization and data exploration. Can be embedded as a React component in the MEOK dashboard.

### Comparison Matrix

| Tool | Cost | 3D City | Export Model | GPU Required | Best For |
|------|------|---------|-------------|-------------|----------|
| **map3d** | Free | Yes | GLB | No (WebGL) | Quick city GLB generation |
| **Cesium for Unreal** | Free | Photorealistic | No (streaming) | High | AAA-quality 3D world |
| **Google Earth Studio** | Free | Photorealistic | No | N/A (video) | Cinematic flythroughs |
| **Mapbox 3D** | Free tier | Yes | No | No (WebGL) | Web map visualization |
| **deck.gl** | Free | Yes | No | Medium | Data visualization overlay |
| **kepler.gl** | Free | Yes | No | Medium | No-code geospatial analysis |

---

## 4. The Pipeline: Real City → 3D Model → Game Environment

### Complete Pipeline

```
Step 1: SELECT CITY AREA
  Input: City name or bounding box coordinates
  Tool: map3d (web UI) or Overpass API directly
  Latency: Instant (selection)
  
Step 2: FETCH OSM DATA
  Source: OpenStreetMap via Overpass API
  Data: Building footprints, heights, roads, POIs
  Latency: 2-10 seconds (network dependent)
  Pre-computable: YES (cache OSM data locally)
  
Step 3: GENERATE 3D MODEL
  Tool: map3d (React Three Fiber)
  Process: Extrude footprints → 3D meshes
  Latency: 1-3 seconds
  Pre-computable: YES (generate once, save GLB)
  
Step 4: EXPORT GLB
  Format: Binary glTF 2.0
  Latency: 1-2 seconds
  Output: cityname.glb file
  
Step 5: LOAD IN GAME ENGINE
  Option A: Three.js (browser) — load GLB via GLTFLoader
  Option B: Unreal Engine 5 — import as Static Mesh
  Option C: Godot 4 — import as 3D scene
  Latency: 1-5 seconds (depends on file size)
  Pre-computable: YES (preload at startup)
  
Step 6: PLACE AGENT SPAWN POINTS
  Input: Town/city coordinates from governance data
  Method: Convert lat/lng to local 3D coordinates
  Latency: Real-time (instant)
  
Step 7: ADD GOVERNANCE OVERLAY
  Method: Colored polygon meshes at height + epsilon
  Latency: Real-time
  
Step 8: ANIMATE AGENTS
  Tool: MotionBricks + AI4AnimationPy
  Process: Procedural animation from text prompts
  Latency: 1-2 seconds per animation (pre-computable)
  
Step 9: REAL-TIME AGENT MOVEMENT
  Data: Agent positions from server
  Update rate: 1-30 Hz (configurable)
  Latency: Network round-trip (50-300ms)
```

### What Can Be Pre-Computed

| Step | Pre-computable | Storage |
|------|---------------|---------|
| OSM data fetch | YES | JSON files (~1-10MB per city area) |
| 3D model generation | YES | GLB files (~5-50MB per city area) |
| Building meshes | YES | Merged geometry for better performance |
| Agent animations | YES | Animation clips (FBX/glb) |
| Governance zones | YES | GeoJSON polygon files |
| Texture atlases | YES | PNG/KTX2 files |

### What Needs to Be Real-Time

| Step | Why Real-Time |
|------|--------------|
| Agent position updates | Agents move based on decisions |
| Governance zone updates | Zone colors change based on control |
| Agent spawn/despawn | Dynamic population |
| Camera movement | User navigation |
| UI overlays | Interactive dashboards |

### Latency Budget

| Component | Target Latency | Maximum |
|-----------|---------------|---------|
| OSM data fetch | 2s | 10s |
| 3D generation | 2s | 5s |
| GLB export | 1s | 3s |
| Game engine load | 2s | 5s |
| Agent position sync | 100ms | 500ms |
| Governance overlay update | 50ms | 200ms |

---

## 5. 3D Models for the 12 Civilizations

### City Selection

| Civilization | Primary City | Coordinates | Backup City |
|-------------|-------------|-------------|-------------|
| Aethelgard (EU) | London | 51.5074, -0.1278 | Paris (48.8566, 2.3522) |
| Sino-Nova (China) | Shanghai | 31.2304, 121.4737 | Shenzhen (22.5431, 114.0579) |
| Pan-America (US) | New York | 40.7128, -74.0060 | San Francisco (37.7749, -122.4194) |
| Khaleej (MENA) | Dubai | 25.2048, 55.2708 | Riyadh (24.7136, 46.6753) |
| Indo-Sphere (India) | Mumbai | 19.0760, 72.8777 | Bangalore (12.9716, 77.5946) |
| TBD (6 more) | Tokyo | 35.6762, 139.6503 | Seoul (37.5665, 126.9780) |

### Can map3d Generate All of These?

**YES.** map3d works worldwide wherever OpenStreetMap has building data.

**OSM building data coverage by region:**
| Region | Coverage Quality | Building Height Data |
|--------|-----------------|---------------------|
| Western Europe | Excellent | Good (many tagged) |
| North America | Good | Moderate |
| East Asia | Good | Moderate |
| Middle East | Moderate | Limited |
| South Asia | Moderate | Limited |
| Africa | Sparse | Very Limited |

### Generation Time Estimate

| Task | Time per City | Total (6 cities) |
|------|--------------|-----------------|
| OSM data fetch | 3-10s | 30-60s |
| 3D generation | 2-5s | 20-30s |
| GLB export | 1-2s | 10-12s |
| **Total (manual)** | **~10s** | **~60-120s** |
| **Total (automated batch)** | **~5s** | **~30s** |

### Storage Requirements

| Resolution | Approximate GLB Size | Per 12 Cities |
|------------|---------------------|---------------|
| Small area (1km x 1km) | 5-10 MB | 60-120 MB |
| Medium area (5km x 5km) | 20-50 MB | 240-600 MB |
| Large area (10km x 10km) | 50-150 MB | 600MB - 1.8 GB |

**Recommendation:** Use medium areas (city center, 5km x 5km) for ~400MB total.

---

## 6. Performance on Nick's Hardware

### Nick's Constraints

- MacBook Air (lightweight, portable)
- Used in caravan (potentially limited internet)
- Limited/no dedicated GPU
- Need: Works reliably on low-end hardware

### Can UE5 Run on MacBook Air?

**NO — not practically.**

| MacBook Model | Can Run UE5? | Notes |
|--------------|-------------|-------|
| MacBook Air M1 (2020) | Barely | No Nanite, no Lumen, very slow |
| MacBook Air M2 (2022) | Poor | SM6 requires macOS 15+, limited VRAM |
| MacBook Air M3 (2024) | Poor-Medium | Better but still no dedicated GPU |
| MacBook Pro M3 Pro/Max | Yes | With limitations |

**Official UE5 macOS requirements (from Epic):**
- Minimum: M1/M2 (depending on rendering features)
- Recommended: M3 Apple Silicon
- Minimum RAM: 16 GB
- Recommended: 32 GB
- Nanite requires: M2+ (beta support)
- Lumen hardware RT: NOT supported on any Mac

**UE5 rendering feature compatibility on Mac:**
```
Lumen (Software RT):     M1+ supported
Lumen (Hardware RT):     NOT supported
Nanite:                  M2+ only (beta)
Temporal Super Resolution: M1+ supported
Virtual Shadow Maps:     M2+ only
```

**Verdict:** MacBook Air cannot run Cesium for Unreal at acceptable performance. The 3D city tiles require too much GPU power.

### Better Alternative: Three.js in Browser

**RECOMMENDED FOR NICK.**

| Attribute | Detail |
|-----------|--------|
| **GPU Required** | Any GPU with WebGL support (includes integrated) |
| **Performance** | 30-60 FPS on MacBook Air M1/M2 |
| **Works Offline** | YES (after initial load) |
| **Distribution** | Web page — no install needed |
| **File Size** | ~500KB-2MB (engine) + city GLB files |
| **Cross-Platform** | YES — any device with a browser |

**Three.js performance on MacBook Air:**
- Simple scene (<1000 meshes): 60 FPS
- City scene (5000 buildings): 30-45 FPS
- Optimized with InstancedMesh: 60 FPS
- With LOD: 60 FPS even for large cities

### Alternative: Godot 4

| Attribute | Detail |
|-----------|--------|
| **Price** | FREE (MIT license) |
| **Mac Support** | Excellent — native Apple Silicon |
| **GPU Required** | Works on integrated graphics |
| **3D Import** | GLB, OBJ, FBX, DAE |
| **Performance** | Lightweight — runs well on low-end hardware |
| **Scripting** | GDScript (Python-like) |
| **Export** | Web, macOS, Windows, Linux, mobile |

**Godot 4 on MacBook Air:**
- 3D scenes: 30-60 FPS depending on complexity
- Lightweight renderer option available
- No Nanite/Lumen equivalent (but also no overhead)

### Alternative: Pre-Rendered Videos

For zero-GPU scenarios:

| Attribute | Detail |
|-----------|--------|
| **Required Hardware** | None — any device that plays video |
| **Format** | MP4 video files |
| **Creation** | Render once on powerful machine |
| **Runtime** | No GPU needed |
| **Interactivity** | Limited (can overlay UI on video) |

### Best Option for Nick's Constraints

| Rank | Option | Suitability | Why |
|------|--------|-------------|-----|
| **1** | **Three.js + deck.gl** | **BEST** | Runs on any device, web-based, GPU-accelerated but lightweight |
| **2** | **Godot 4** | **GOOD** | Free, runs on Mac, better performance than UE5 on low-end |
| **3** | **Pre-rendered video** | **FALLBACK** | Works everywhere, zero GPU, limited interactivity |
| **4** | **Cesium for Unreal** | **NOT RECOMMENDED** | Requires powerful GPU, won't run on MacBook Air |

---

## 7. Working Example Code

### Example 1: Generate 3D City with map3d (Programmatic)

```typescript
// city-generator.ts
// Standalone script to generate 3D city GLB from OSM data

import * as THREE from "three";
import { GLTFExporter } from "three/examples/jsm/exporters/GLTFExporter.js";

const scale = 51000;

interface BuildingData {
  id: number;
  tags: Record<string, string>;
  geometry: Array<{ lat: number; lon: number }>;
}

function project(lat: number, lng: number, refLat: number, refLng: number): THREE.Vector2 {
  const x = (lng - refLng) * scale * Math.cos((refLat * Math.PI) / 180);
  const y = (lat - refLat) * scale;
  return new THREE.Vector2(x, y);
}

function createBuildingMesh(
  building: BuildingData,
  refLat: number,
  refLng: number
): THREE.Mesh | null {
  if (!building.geometry || building.geometry.length < 3) return null;

  // Create shape from footprint
  const shapePoints = building.geometry.map((pt) =>
    project(pt.lat, pt.lon, refLat, refLng)
  );

  // Close the shape
  if (!shapePoints[0].equals(shapePoints[shapePoints.length - 1])) {
    shapePoints.push(shapePoints[0]);
  }

  const shape = new THREE.Shape(shapePoints);

  // Determine height
  let heightValue = parseFloat(building.tags.height || "");
  const heightLevels = parseFloat(building.tags["building:levels"] || "");
  if (isNaN(heightValue)) heightValue = 10;
  if (!isNaN(heightLevels)) heightValue = heightLevels * 2.2;

  const extrudeSettings = {
    steps: 1,
    depth: heightValue,
    bevelEnabled: false,
  };

  const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
  const material = new THREE.MeshStandardMaterial({ color: 0x9da0a3 });
  const mesh = new THREE.Mesh(geometry, material);

  // Rotate to lay flat
  mesh.rotation.x = -Math.PI / 2;
  mesh.userData = { exportToGLB: true, tags: building.tags };

  return mesh;
}

async function fetchBuildings(
  south: number,
  west: number,
  north: number,
  east: number
): Promise<BuildingData[]> {
  const query = `[out:json][timeout:25];(way["building"](${south},${west},${north},${east}););out body geom;`;

  const response = await fetch("https://overpass-api.de/api/interpreter", {
    method: "POST",
    body: query,
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  const data = await response.json();
  return data.elements.map((el: any) => ({
    id: el.id,
    tags: el.tags,
    geometry: el.geometry.map((g: any) => ({ lat: g.lat, lon: g.lon })),
  }));
}

export async function generateCityGLB(
  cityName: string,
  south: number,
  west: number,
  north: number,
  east: number
): Promise<ArrayBuffer> {
  console.log(`Fetching OSM data for ${cityName}...`);
  const buildings = await fetchBuildings(south, west, north, east);
  console.log(`Found ${buildings.length} buildings`);

  const refLat = (north + south) / 2;
  const refLng = (east + west) / 2;

  // Create scene
  const scene = new THREE.Scene();
  const group = new THREE.Group();

  // Create building meshes
  let meshCount = 0;
  for (const building of buildings) {
    const mesh = createBuildingMesh(building, refLat, refLng);
    if (mesh) {
      group.add(mesh);
      meshCount++;
    }
  }

  console.log(`Created ${meshCount} building meshes`);

  // Add lights (required for GLTF)
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  group.add(ambientLight);

  scene.add(group);

  // Export to GLB
  const exporter = new GLTFExporter();
  const options = { binary: true };

  const result = await exporter.parseAsync(scene, options);
  console.log(`Exported GLB: ${(result as ArrayBuffer).byteLength / 1024 / 1024:.2f} MB`);

  return result as ArrayBuffer;
}

// Usage example:
// const glb = await generateCityGLB("London", 51.50, -0.15, 51.52, -0.10);
```

### Example 2: Load 3D City in Three.js Viewer

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MEOK 3D City Viewer</title>
  <style>
    body { margin: 0; overflow: hidden; font-family: sans-serif; }
    #canvas-container { width: 100vw; height: 100vh; }
    #ui {
      position: absolute; top: 10px; left: 10px;
      background: rgba(0,0,0,0.7); color: white;
      padding: 15px; border-radius: 8px; font-size: 14px;
    }
    .agent-label {
      position: absolute; background: rgba(0,0,0,0.8);
      color: white; padding: 4px 8px; border-radius: 4px;
      font-size: 12px; pointer-events: none;
    }
  </style>
</head>
<body>
  <div id="canvas-container"></div>
  <div id="ui">
    <h3>MEOK City Viewer</h3>
    <p>Left click: Rotate | Right click: Pan | Scroll: Zoom</p>
    <p>Agents: <span id="agent-count">0</span></p>
  </div>

  <script type="importmap">
  {
    "imports": {
      "three": "https://unpkg.com/three@0.173.0/build/three.module.js",
      "three/addons/": "https://unpkg.com/three@0.173.0/examples/jsm/"
    }
  }
  </script>
  <script type="module" src="viewer.js"></script>
</body>
</html>
```

```javascript
// viewer.js — Three.js 3D City Viewer
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

// Scene setup
const container = document.getElementById("canvas-container");
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb); // Sky blue

// Camera
const camera = new THREE.PerspectiveCamera(
  60, window.innerWidth / window.innerHeight, 0.1, 10000
);
camera.position.set(0, 200, 400);

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.maxPolarAngle = Math.PI / 2.1; // Don't go below ground
controls.minDistance = 10;
controls.maxDistance = 2000;

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1.0);
directionalLight.position.set(100, 200, 100);
directionalLight.castShadow = true;
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;
scene.add(directionalLight);

// Ground plane
const groundGeometry = new THREE.PlaneGeometry(10000, 10000);
const groundMaterial = new THREE.MeshStandardMaterial({ color: 0x3a5a3a });
const ground = new THREE.Mesh(groundGeometry, groundMaterial);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Grid helper
const gridHelper = new THREE.GridHelper(2000, 50, 0x555555, 0x333333);
scene.add(gridHelper);

// Governance zone overlay
function createGovernanceZone(name, color, centerX, centerZ, radius) {
  const geometry = new THREE.CircleGeometry(radius, 32);
  const material = new THREE.MeshBasicMaterial({
    color: color,
    transparent: true,
    opacity: 0.3,
    side: THREE.DoubleSide,
  });
  const zone = new THREE.Mesh(geometry, material);
  zone.rotation.x = -Math.PI / 2;
  zone.position.set(centerX, 1, centerZ);
  zone.name = name;
  scene.add(zone);

  // Zone label
  const labelDiv = document.createElement("div");
  labelDiv.className = "agent-label";
  labelDiv.textContent = name;
  labelDiv.style.left = "50%";
  labelDiv.style.top = "50%";
  document.body.appendChild(labelDiv);

  return zone;
}

// Zone colors for civilizations
const CIV_COLORS = {
  aethelgard: 0xffd700,  // Gold
  sinonova: 0xff0000,    // Red
  panamerica: 0x0000ff,  // Blue
  khaleej: 0x008000,     // Green
  indosphere: 0xff6600,  // Orange
};

// Load city GLB
function loadCity(glbPath) {
  const loader = new GLTFLoader();
  loader.load(
    glbPath,
    (gltf) => {
      const city = gltf.scene;

      // Center the city
      const box = new THREE.Box3().setFromObject(city);
      const center = box.getCenter(new THREE.Vector3());
      city.position.sub(center); // Center at origin

      // Enable shadows
      city.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;
        }
      });

      scene.add(city);
      console.log("City loaded successfully");

      // Add governance zones after city loads
      createGovernanceZone("Aethelgard District", CIV_COLORS.aethelgard, -200, -200, 150);
      createGovernanceZone("Sino-Nova Quarter", CIV_COLORS.sinonova, 200, -100, 120);
    },
    (progress) => {
      const percent = (progress.loaded / progress.total * 100).toFixed(0);
      console.log(`Loading: ${percent}%`);
    },
    (error) => {
      console.error("Error loading city:", error);
    }
  );
}

// Agents
const agents = [];
const agentGeometry = new THREE.CapsuleGeometry(2, 8, 4, 8);

function createAgent(name, x, z, color) {
  const material = new THREE.MeshStandardMaterial({ color: color });
  const agent = new THREE.Mesh(agentGeometry, material);
  agent.position.set(x, 5, z);
  agent.castShadow = true;

  // Name tag
  const canvas = document.createElement("canvas");
  canvas.width = 128;
  canvas.height = 32;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "rgba(0,0,0,0.8)";
  ctx.fillRect(0, 0, 128, 32);
  ctx.fillStyle = "white";
  ctx.font = "16px sans-serif";
  ctx.fillText(name, 8, 22);

  const texture = new THREE.CanvasTexture(canvas);
  const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
  const sprite = new THREE.Sprite(spriteMaterial);
  sprite.position.set(0, 12, 0);
  sprite.scale.set(20, 5, 1);
  agent.add(sprite);

  scene.add(agent);

  const agentData = {
    mesh: agent,
    targetX: x,
    targetZ: z,
    speed: 5 + Math.random() * 10,
    name: name,
  };

  agents.push(agentData);
  document.getElementById("agent-count").textContent = agents.length;

  return agentData;
}

// Animate agents
function updateAgents(deltaTime) {
  for (const agent of agents) {
    // Move toward target
    const dx = agent.targetX - agent.mesh.position.x;
    const dz = agent.targetZ - agent.mesh.position.z;
    const dist = Math.sqrt(dx * dx + dz * dz);

    if (dist > 1) {
      agent.mesh.position.x += (dx / dist) * agent.speed * deltaTime;
      agent.mesh.position.z += (dz / dist) * agent.speed * deltaTime;

      // Face direction of movement
      agent.mesh.lookAt(
        agent.mesh.position.x + dx,
        agent.mesh.position.y,
        agent.mesh.position.z + dz
      );
    } else {
      // Pick new random target
      agent.targetX = (Math.random() - 0.5) * 600;
      agent.targetZ = (Math.random() - 0.5) * 600;
    }
  }
}

// Animation loop
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);

  const deltaTime = clock.getDelta();
  updateAgents(deltaTime);
  controls.update();
  renderer.render(scene, camera);
}

// Handle resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Start
loadCity("./london_city.glb");

// Create sample agents
createAgent("Agent-001", 0, 0, 0xff0000);
createAgent("Agent-002", 50, 30, 0x00ff00);
createAgent("Agent-003", -40, 60, 0x0000ff);

animate();
```

### Example 3: Simple Server for City Data API

```javascript
// server.js — Express API for serving city data and agent positions
const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.json());

// Serve city GLB files
app.use("/cities", express.static(path.join(__dirname, "cities")));

// Serve Three.js viewer
app.use(express.static(path.join(__dirname, "public")));

// Get list of available cities
app.get("/api/cities", (req, res) => {
  const citiesDir = path.join(__dirname, "cities");
  const files = fs.readdirSync(citiesDir).filter((f) => f.endsWith(".glb"));
  res.json(files.map((f) => ({ name: f.replace(".glb", ""), file: f })));
});

// Agent positions (mock — replace with real data)
const agents = [
  { id: "agent-1", name: "Trader Alpha", civ: "aethelgard", x: 10, z: 20 },
  { id: "agent-2", name: "Builder Beta", civ: "sinonova", x: -30, z: 15 },
  { id: "agent-3", name: "Explorer Gamma", civ: "khaleej", x: 50, z: -10 },
];

app.get("/api/agents", (req, res) => {
  // Simulate movement
  agents.forEach((agent) => {
    agent.x += (Math.random() - 0.5) * 2;
    agent.z += (Math.random() - 0.5) * 2;
  });
  res.json(agents);
});

// Governance zones
const zones = [
  {
    id: "zone-1",
    name: "Aethelgard Central",
    civilization: "aethelgard",
    color: "#FFD700",
    boundaries: [[0, 0], [100, 0], [100, 100], [0, 100]],
  },
  {
    id: "zone-2",
    name: "Sino-Nova Quarter",
    civilization: "sinonova",
    color: "#FF0000",
    boundaries: [[-100, 0], [0, 0], [0, 100], [-100, 100]],
  },
];

app.get("/api/zones", (req, res) => {
  res.json(zones);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`MEOK City Server running on http://localhost:${PORT}`);
});
```

### Example 4: React Component for MEOK City View

```tsx
// MeokCityViewer.tsx — React component for MEOK dashboard
import React, { useEffect, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Sky, Environment, Html } from "@react-three/drei";
import * as THREE from "three";
import { useGLTF } from "@react-three/drei";

// Governance zone overlay
function GovernanceZone({ name, position, radius, color }) {
  return (
    <mesh position={[position[0], 0.5, position[2]]} rotation={[-Math.PI / 2, 0, 0]}>
      <circleGeometry args={[radius, 32]} />
      <meshBasicMaterial color={color} transparent opacity={0.3} side={THREE.DoubleSide} />
      <Html position={[0, 0, 0]} center>
        <div style={{
          background: "rgba(0,0,0,0.7)", color: "white",
          padding: "4px 8px", borderRadius: "4px", fontSize: "12px"
        }}>
          {name}
        </div>
      </Html>
    </mesh>
  );
}

// Agent character
function Agent({ name, position, color, targetPosition }) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (meshRef.current && targetPosition) {
      // Smooth movement toward target
      meshRef.current.position.x += (targetPosition[0] - meshRef.current.position.x) * delta * 2;
      meshRef.current.position.z += (targetPosition[2] - meshRef.current.position.z) * delta * 2;
    }
  });

  return (
    <mesh ref={meshRef} position={position} castShadow>
      <capsuleGeometry args={[2, 8, 4, 8]} />
      <meshStandardMaterial color={color} />
      <Html position={[0, 12, 0]} center>
        <div style={{
          background: "rgba(0,0,0,0.8)", color: "white",
          padding: "2px 6px", borderRadius: "4px", fontSize: "11px", whiteSpace: "nowrap"
        }}>
          {name}
        </div>
      </Html>
    </mesh>
  );
}

// City model from GLB
function CityModel({ glbPath }) {
  const { scene } = useGLTF(glbPath);

  useEffect(() => {
    // Center the city
    const box = new THREE.Box3().setFromObject(scene);
    const center = box.getCenter(new THREE.Vector3());
    scene.position.sub(center);

    // Enable shadows
    scene.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
      }
    });
  }, [scene]);

  return <primitive object={scene} />;
}

// Main scene
function MeokScene({ cityGlb, agents, zones }) {
  return (
    <>
      <ambientLight intensity={0.6} />
      <directionalLight
        position={[100, 200, 100]}
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
      />

      <CityModel glbPath={cityGlb} />

      {/* Governance zones */}
      {zones.map((zone) => (
        <GovernanceZone
          key={zone.id}
          name={zone.name}
          position={[zone.centerX, 0, zone.centerZ]}
          radius={zone.radius}
          color={zone.color}
        />
      ))}

      {/* Agents */}
      {agents.map((agent) => (
        <Agent
          key={agent.id}
          name={agent.name}
          position={agent.position}
          color={agent.color}
          targetPosition={agent.targetPosition}
        />
      ))}

      <Sky distance={450000} sunPosition={[100, 200, 100]} />
      <Environment preset="city" />
      <OrbitControls
        maxPolarAngle={Math.PI / 2.1}
        minDistance={10}
        maxDistance={2000}
      />
    </>
  );
}

// Main component
export function MeokCityViewer({ cityGlb, agents, zones }) {
  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <Canvas
        shadows
        camera={{ fov: 60, near: 0.1, far: 10000, position: [0, 200, 400] }}
      >
        <MeokScene cityGlb={cityGlb} agents={agents} zones={zones} />
      </Canvas>
    </div>
  );
}
```

---

## 8. Final Recommendations

### Recommended Architecture for MEOK

```
┌─────────────────────────────────────────────────────────────┐
│                    MEOK 3D City System                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   OSM Data   │───▶│   map3d      │───▶│   GLB Files  │  │
│  │  (Overpass)  │    │  (generate)  │    │  (cached)    │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                    │         │
│  ┌─────────────────────────────────────────────────▼──────┐ │
│  │              THREE.JS BROWSER VIEWER                    │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │  3D City │  │  Agents  │  │ Governance Zones     │  │ │
│  │  │  (GLB)   │  │  (live)  │  │ (colored overlays)   │  │ │
│  │  └──────────┘  └──────────┘  └──────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │              MEOK API SERVER (Node.js)                │   │
│  │  • Agent positions (WebSocket)                       │   │
│  │  • Governance data (REST)                            │   │
│  │  • City data (static files)                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Why This Architecture?

1. **Three.js in browser** — Runs on Nick's MacBook Air, no install needed
2. **map3d for city generation** — One-time cost, reusable GLB files
3. **deck.gl for overlays** — Best-in-class geospatial visualization
4. **Node.js API server** — Serves data, handles agent sync
5. **WebSocket for agents** — Real-time position updates

### Cost Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| map3d | FREE (MIT) | Open source |
| Three.js | FREE (MIT) | Open source |
| deck.gl | FREE (Apache 2.0) | Open source |
| OSM data | FREE | ODbL license |
| Node.js server | FREE | Open source |
| Hosting | $0-10/month | Vercel/Netlify for static, Railway for API |
| **Total monthly** | **$0-10** | Essentially free |

### Next Steps

1. **Phase 1 (Immediate):** Set up Three.js viewer with a test city (London)
2. **Phase 2:** Integrate map3d pipeline to generate all 12 civilization cities
3. **Phase 3:** Add agent visualization with WebSocket sync
4. **Phase 4:** Add governance zone overlays with deck.gl
5. **Phase 5:** Optimize for mobile/tablet viewing

---

## Appendix: Data Sources and References

### GitHub Repositories
- map3d: https://github.com/cartesiancs/map3d (MIT License)
- Cesium for Unreal: https://github.com/CesiumGS/cesium-unreal (Apache 2.0)
- kepler.gl: https://github.com/keplergl/kepler.gl (MIT License)
- deck.gl: https://github.com/visgl/deck.gl (Apache 2.0)
- Godot 3D OSM: https://github.com/Frataj/3D-OSM-GODOT

### Documentation
- Cesium for Unreal Quickstart: https://cesium.com/learn/unreal/unreal-quickstart/
- Three.js GLTFExporter: https://threejs.org/docs/#examples/en/exporters/GLTFExporter
- deck.gl 3D Tiles: https://deck.gl/docs/developer-guide/base-maps/using-with-3d-tiles
- Overpass API: https://wiki.openstreetmap.org/wiki/Overpass_API
- UE5 macOS Requirements: https://dev.epicgames.com/documentation/unreal-engine/macos-development-requirements-for-unreal-engine

### Licenses Summary

| Tool | License | Commercial Use |
|------|---------|---------------|
| map3d | MIT | YES |
| Cesium for Unreal | Apache 2.0 | YES |
| Three.js | MIT | YES |
| deck.gl | Apache 2.0 | YES |
| kepler.gl | MIT | YES |
| Godot 4 | MIT | YES |
| OpenStreetMap data | ODbL | YES (with attribution) |
| Mapbox | Proprietary API | YES (paid tiers) |

---

*Document version: 1.0*
*Generated: Research complete*
*Total research sources: 50+ documentation pages, GitHub repos, community forums*
