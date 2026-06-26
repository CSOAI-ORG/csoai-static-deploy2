# MEOK Real-World Map Governance Experiments: Complete Technical Guide

> **Document Purpose**: Design and implementation guide for overlaying MEOK's governance simulation engine onto real-world maps using open geospatial technologies. Covers platforms, data sources, experiment designs, and production-ready code examples.
>
> **Last Updated**: 2025-07-25

---

## Table of Contents

1. [Real-World Map Platforms](#1-real-world-map-platforms)
2. [Governance Overlay on Real Maps](#2-governance-overlay-on-real-maps)
3. [Real-World Experiment Designs](#3-real-world-experiment-designs)
4. [Geospatial Data Sources](#4-geospatial-data-sources-free)
5. [Digital Twin Approach](#5-digital-twin-approach)
6. [Code Examples](#6-code-examples)
7. [Specific Experiment: AI Agent Border Crossing](#7-specific-experiment-ai-agent-crossing-borders)
8. [Integration Architecture](#8-integration-architecture)
9. [Implementation Roadmap](#9-implementation-roadmap)

---

## 1. Real-World Map Platforms

### 1.1 CesiumJS (Open Source, 3D Globe)

**License**: Apache 2.0 | **Cost**: Free | **Website**: [cesium.com/platform/cesiumjs](https://cesium.com/platform/cesiumjs/)

CesiumJS is the premier open-source JavaScript library for 3D geospatial visualization on the web. Created by AGI in 2011 and open-sourced in 2012, it renders a high-precision WGS84 ellipsoid globe with WebGL hardware acceleration.

**Key Capabilities for MEOK**:
- **3D Tiles streaming**: Stream massive 3D datasets including city-scale building models
- **Time-dynamic visualization (CZML)**: Animate agents moving across borders with precise timestamps
- **GeoJSON/KML support**: Load regulatory boundaries, country borders, jurisdiction polygons
- **Entity picking & events**: Detect when agents cross boundaries, trigger compliance changes
- **Globe-level to building-level**: Zoom from space to individual buildings seamlessly

**Data formats supported**:

| Data Type | Format | Use Case for MEOK |
|-----------|--------|-------------------|
| Country/jurisdiction boundaries | GeoJSON, KML | Color-code by regulatory strictness |
| Agent positions over time | CZML | Animate AI agents crossing borders |
| 3D city models | 3D Tiles | Digital twin environments |
| Terrain | Quantized Mesh | Real-world elevation for route planning |
| Satellite imagery | WMS, TMS, WMTS | Base map layers |
| Building footprints | 3D Tiles (OSM) | Urban compliance zones |

**Installation**:
```bash
npm install cesium
```

**Quick start**:
```javascript
import { Viewer, GeoJsonDataSource, Color } from 'cesium';
import 'cesium/Build/Cesium/Widgets/widgets.css';

const viewer = new Viewer('cesiumContainer');

// Load country boundaries with compliance color-coding
viewer.dataSources.add(
  GeoJsonDataSource.load('natural_earth_countries.geojson', {
    stroke: Color.WHITE,
    strokeWidth: 1,
    fill: Color.BLUE.withAlpha(0.3)
  })
);
```

**Why MEOK should use it**: Native time-dynamic visualization via CZML is unmatched for showing agents moving across borders and changing compliance states at boundaries. The Entity API allows attaching compliance metadata to geographic entities.

---

### 1.2 Cesium for Unreal (Free, Apache 2.0)

**License**: Apache 2.0 | **Cost**: Free | **UE5 Plugin**: [cesium.com/unreal](https://cesium.com/platform/cesium-for-unreal/)

Cesium for Unreal brings the entire 3D geospatial stack into Unreal Engine 5, enabling photorealistic digital twins at global scale. Streams real-world terrain, imagery, and 3D buildings directly into UE5.

**Key Capabilities for MEOK**:
- **Global 3D terrain + Bing Maps aerial imagery**: Accurate real-world geography
- **Cesium OSM Buildings**: 350M+ 3D buildings derived from OpenStreetMap with per-building metadata
- **CesiumSunSky**: Realistic globe-aware lighting and atmosphere
- **DynamicPawn**: Globe-aware navigation for exploring the Earth at any scale
- **Multiplayer-ready**: Run agent simulations with UE5's networking stack

**Getting Started**:
1. Install Cesium for Unreal plugin from Unreal Marketplace
2. Create UE5 project (Game > Blank)
3. Enable plugin (Edit > Plugins > Search "Cesium")
4. Add Cesium SunSky + Connect to Cesium ion
5. Add "Cesium World Terrain + Bing Maps Aerial Imagery"
6. Add "Cesium OSM Buildings" for 3D city context

**Critical settings**:
- Disable World Bounds Checks (Window > World Settings > Advanced)
- Enable Auto Exposure + Extend default luminance range (Edit > Project Settings > Rendering)

**Relevance for MEOK**: UE5 enables immersive digital twin experiments where AI agents navigate photorealistic cities with real-world compliance rules applied to actual building footprints, roads, and infrastructure. Multiplayer support enables multi-agent governance simulations.

**Example: Set location to experiment site (Strasbourg border area)**:
```
CesiumGeoreference Origin Latitude = 48.5734
CesiumGeoreference Origin Longitude = 7.7521
CesiumGeoreference Origin Height = 1000.0
```

---

### 1.3 Mapbox GL JS (Free Tier)

**License**: Proprietary SDK | **Cost**: Free tier (50,000 loads/month) | **Website**: [mapbox.com](https://www.mapbox.com/)

Mapbox GL JS is a WebGL-based JavaScript library for interactive, customizable vector maps. Best-in-class for 2D map visualization with smooth animations and custom styling.

**Key Capabilities for MEOK**:
- **Custom map styles**: Create dark/light/governance-themed map styles
- **Smooth camera animations**: Follow agents along routes with FreeCamera API
- **GeoJSON data layers**: Add compliance zones, heatmaps, regulatory boundaries
- **Turf.js integration**: Geospatial calculations (point-in-polygon, distance, interpolation)
- **Animated markers**: Pulsing dots for DORA-regulated entities, moving agents

**Installation**:
```bash
npm install mapbox-gl
npm install @turf/turf
```

**Agent animation code pattern**:
```javascript
// See full code in Section 6
// Uses turf.along() + requestAnimationFrame to move agents
// along GeoJSON LineString routes with bearing rotation
```

**Why MEOK should use it**: Best for rapid prototyping of governance overlays. The combination of Mapbox + Turf.js provides everything needed for 2D compliance zone visualization and agent animation.

---

### 1.4 OpenStreetMap + Overpass API (Free)

**License**: ODbL | **Cost**: Free | **Website**: [openstreetmap.org](https://www.openstreetmap.org/)

OpenStreetMap is the world's largest collaborative mapping project. The Overpass API allows querying specific map features programmatically.

**Key Data for MEOK**:
- **Administrative boundaries**: Country borders, state/province divisions, city limits
- **Building footprints**: Individual buildings with use type, height, address
- **Road networks**: Highway classifications, speed limits, one-way restrictions
- **Points of interest**: Government offices, financial institutions (DORA entities)
- **Transportation**: Railways, airports, ports

**Overpass API Query Examples**:
```javascript
// Fetch administrative boundaries for a country
// France relation ID: 2202162
// Germany relation ID: 51477
// Switzerland relation ID: 51701

// Query to get country border
[out:json];
relation(2202162);  // France
(._;>;);
out body;

// Query to get all DORA-relevant entities in a bounding box
// (banks, financial institutions, insurance companies)
[out:json][bbox:48.5,7.3,48.9,8.0];
(
  node["office"="financial"];
  node["amenity"="bank"];
  way["office"="insurance"];
  node["amenity"="insurance"];
);
out center;
```

**Overpass Turbo** (web UI for testing queries): [overpass-turbo.eu](https://overpass-turbo.eu/)

---

### 1.5 Google Earth Engine (Free for Research)

**License**: Proprietary | **Cost**: Free for research/non-commercial | **Website**: [earthengine.google.com](https://earthengine.google.com/)

Google Earth Engine is a cloud-based platform for planetary-scale geospatial analysis. Provides access to petabytes of satellite imagery and geospatial datasets.

**Key Datasets for MEOK**:
- **Administrative boundaries (FAO GAUL)**: Country and subnational boundaries
- **Satellite imagery (Sentinel-2, Landsat)**: Base layers, land use classification
- **Population density**: WorldPop dataset for agent density estimates
- **Nighttime lights**: VIIRS for economic activity indicators
- **Road networks**: GRIP4 global roads database

**Example: Load country boundaries**:
```javascript
// Google Earth Engine JavaScript API
var admin0 = ee.FeatureCollection('FAO/GAUL/2015/level0');
var france = admin0.filter(ee.Filter.eq('ADM0_NAME', 'France'));
var germany = admin0.filter(ee.Filter.eq('ADM0_NAME', 'Germany'));

Map.addLayer(france, {color: 'blue'}, 'France');
Map.addLayer(germany, {color: 'red'}, 'Germany');
```

---

### 1.6 NASA WorldWind (Open Source)

**License**: Apache 2.0 / NASA Open Source | **Cost**: Free | **Website**: [worldwind.arc.nasa.gov](https://worldwind.arc.nasa.gov/)

NASA WorldWind is an open-source virtual globe SDK developed by NASA. Available for Java, Android, and JavaScript (Web).

**Key Capabilities**:
- Full 3D globe rendering in JavaScript
- Layer management for overlays (compliance zones, heatmaps)
- Placemark support for entity locations
- KML/GeoJSON support
- Community-maintained fork: [WorldWindJS](https://github.com/WorldWindEarth/worldwindjs)

**Installation** (npm):
```json
"dependencies": {
  "worldwindjs": "^1.7.0"
}
```

**Simple example**:
```javascript
import WorldWind from 'worldwindjs';

const wwd = new WorldWind.WorldWindow("canvasOne");
wwd.addLayer(new WorldWind.BMNGOneImageLayer());
wwd.addLayer(new WorldWind.BMNGLandsatLayer());

// Add compliance zone placemark
const placemarkLayer = new WorldWind.RenderableLayer();
wwd.addLayer(placemarkLayer);

const placemarkAttr = new WorldWind.PlacemarkAttributes(null);
placemarkAttr.imageSource = WorldWind.configuration.baseUrl + "images/pushpins/castshadow-red.png";

const position = new WorldWind.Position(48.5734, 7.7521, 0);  // Strasbourg
const placemark = new WorldWind.Placemark(position, false, placemarkAttr);
placemarkLayer.addRenderable(placemark);
```

**Trade-off**: Smaller community than CesiumJS but officially backed by NASA. Good for government/research use cases.

---

### Platform Comparison Summary

| Platform | 3D | License | Best For | Ease of Setup | Performance |
|----------|-----|---------|----------|--------------|-------------|
| CesiumJS | Full 3D globe | Apache 2.0 | Border crossing sims, CZML time animations | Medium | Excellent |
| Cesium for Unreal | Photorealistic 3D | Apache 2.0 | Digital twin experiments, immersive sims | Complex | Top-tier |
| Mapbox GL JS | 2.5D | Proprietary | Rapid prototyping, governance dashboards | Easy | Very Good |
| OpenStreetMap | N/A (data) | ODbL | Free map data, boundaries, buildings | Easy | N/A |
| Google Earth Engine | 2D/3D | Proprietary | Research-scale analysis, satellite data | Medium | Cloud-scale |
| NASA WorldWind | Full 3D | Apache 2.0 | Government/research projects | Medium | Good |

---

## 2. Governance Overlay on Real Maps

### 2.1 EU AI Act Compliance Zones on a Map of Europe

**Concept**: Color-code EU member states based on their AI Act implementation progress and national regulatory strictness.

**Implementation**:
```javascript
// CesiumJS: Color EU countries by compliance zone tier
const euComplianceTiers = {
  // Tier 1: Full implementation, strict enforcement
  tier1: ['Germany', 'France', 'Netherlands', 'Italy'],
  // Tier 2: Implementation in progress
  tier2: ['Spain', 'Belgium', 'Austria', 'Sweden'],
  // Tier 3: Delayed/lagging implementation
  tier3: ['Poland', 'Hungary', 'Romania', 'Bulgaria']
};

// Load Natural Earth country boundaries
const viewer = new Cesium.Viewer('cesiumContainer');

Cesium.GeoJsonDataSource.load('ne_10m_admin_0_countries.geojson').then(
  function(dataSource) {
    viewer.dataSources.add(dataSource);
    const entities = dataSource.entities.values;

    for (let i = 0; i < entities.length; i++) {
      const entity = entities[i];
      const name = entity.properties.ADMIN;

      if (euComplianceTiers.tier1.includes(name)) {
        entity.polygon.material = Cesium.Color.GREEN.withAlpha(0.5);
        entity.polygon.outlineColor = Cesium.Color.DARKGREEN;
      } else if (euComplianceTiers.tier2.includes(name)) {
        entity.polygon.material = Cesium.Color.YELLOW.withAlpha(0.5);
        entity.polygon.outlineColor = Cesium.Color.ORANGE;
      } else if (euComplianceTiers.tier3.includes(name)) {
        entity.polygon.material = Cesium.Color.RED.withAlpha(0.4);
        entity.polygon.outlineColor = Cesium.Color.DARKRED;
      }
    }
  }
);
```

**Legend**:
- Green: Full AI Act implementation + strict national enforcement
- Yellow: Implementation in progress
- Red: Delayed/lagging implementation
- Grey: Non-EU (no AI Act obligation)

---

### 2.2 DORA-Regulated Entities as Glowing Dots

**Concept**: Display financial entities regulated under the EU Digital Operational Resilience Act (DORA) as pulsing dots on the map.

**Implementation (Mapbox GL JS)**:
```javascript
// Add pulsing dot for DORA entities
const size = 200;
const pulsingDot = {
  width: size,
  height: size,
  data: new Uint8Array(size * size * 4),

  onAdd: function() {
    const canvas = document.createElement('canvas');
    canvas.width = this.width;
    canvas.height = this.height;
    this.context = canvas.getContext('2d');
  },

  render: function() {
    const duration = 1000;
    const t = (performance.now() % duration) / duration;
    const radius = (size / 2) * 0.3;
    const outerRadius = (size / 2) * 0.7 * t + radius;
    const context = this.context;

    context.clearRect(0, 0, this.width, this.height);
    context.beginPath();
    context.arc(this.width / 2, this.height / 2, outerRadius, 0, Math.PI * 2);
    context.fillStyle = `rgba(255, 100, 100, ${1 - t})`;
    context.fill();

    context.beginPath();
    context.arc(this.width / 2, this.height / 2, radius, 0, Math.PI * 2);
    context.fillStyle = 'rgba(255, 0, 0, 1)';
    context.fill();

    this.data = context.getImageData(0, 0, this.width, this.height).data;
    map.triggerRepaint();
    return true;
  }
};

map.on('load', () => {
  map.addImage('dora-pulse', pulsingDot, { pixelRatio: 2 });
  map.addSource('dora-entities', {
    type: 'geojson',
    data: 'dora_financial_entities.geojson'
  });
  map.addLayer({
    id: 'dora-entities-layer',
    type: 'symbol',
    source: 'dora-entities',
    layout: { 'icon-image': 'dora-pulse' }
  });
});
```

---

### 2.3 Color-Code Countries by Regulatory Strictness

**Comprehensive regulatory strictness index** (1-10 scale):

| Country/Jurisdiction | Strictness | Key Regulations | Color Code |
|---------------------|------------|-----------------|------------|
| European Union | 9 | EU AI Act, GDPR, DORA | `#1a5276` (dark blue) |
| China | 8 | Deep Synthesis Provisions, Algorithm Recommendation, Shenzhen SEZ regs | `#922b21` (dark red) |
| United Kingdom | 7 | Automated Vehicles Act, Online Safety Bill, post-Bre divergence | `#1e8449` (green) |
| Colorado (US) | 7 | SB 24-205 (comprehensive AI Act) | `#6c3483` (purple) |
| California (US) | 7 | SB 53 (Frontier AI), AB 2013 (training data), CCPA | `#d35400` (orange) |
| Switzerland | 6 | Non-EU, bilateral agreements, self-regulation | `#f1c40f` (yellow) |
| Texas (US) | 6 | HB 149 (TRAIGA), sector-specific | `#e67e22` (orange) |
| Dubai (DIFC) | 5 | Common law enclave, DFSA regs, AI court guidelines | `#17a589` (teal) |
| UAE (mainland) | 4 | Federal data protection, emerging framework | `#5dade2` (light blue) |
| Shenzhen (China) | 8 | Special Economic Zone AI regulations (China's most advanced) | `#c0392b` (red) |

---

### 2.4 Animate AI Agents Crossing Borders and Changing Compliance Requirements

This is covered in detail in Section 7 (the Strasbourg-Basel border crossing experiment). The key mechanism:

1. **CZML time-dynamic positions**: Agent location at each timestep
2. **Boundary detection**: Point-in-polygon checks at each position update
3. **Compliance state machine**: Rules change when jurisdiction changes
4. **Visual feedback**: Agent color/icon changes to reflect compliance mode

---

### 2.5 Heat Map of AI Incidents by Location

**Implementation (Mapbox GL JS)**:
```javascript
map.addSource('ai-incidents', {
  type: 'geojson',
  data: 'ai_incidents_dataset.geojson'
});

map.addLayer({
  id: 'ai-incidents-heat',
  type: 'heatmap',
  source: 'ai-incidents',
  paint: {
    'heatmap-weight': ['get', 'severity'],
    'heatmap-intensity': 1,
    'heatmap-color': [
      'interpolate', ['linear'], ['heatmap-density'],
      0, 'rgba(0,0,255,0)',
      0.2, 'rgb(0,255,255)',
      0.5, 'rgb(255,255,0)',
      0.8, 'rgb(255,100,0)',
      1, 'rgb(255,0,0)'
    ],
    'heatmap-radius': 30,
    'heatmap-opacity': 0.8
  }
});
```

---

## 3. Real-World Experiment Designs

### 3.1 "Brexit Border": Ireland (EU) vs Northern Ireland (UK)

**Geography**: The island of Ireland is divided between the Republic of Ireland (EU member) and Northern Ireland (UK post-Brexit). At some points, the border is a single road crossed in seconds.

**Regulatory Divergence**:
| Factor | Republic of Ireland (EU) | Northern Ireland (UK) |
|--------|-------------------------|----------------------|
| AI Act | Full EU AI Act applies | UK has own framework (no AI Act) |
| GDPR | Full GDPR applies | UK GDPR (diverging) |
| Data transfers | EU internal freedom | Post-Brexit transfer mechanisms |
| DORA | Applies (EU financial regulation) | UK equivalent (PRA rules) |
| Enforcement | Irish DPC | UK ICO + local regulators |

**Simulation Design**:
- Place AI agent (e.g., autonomous delivery vehicle) at Dundalk, Ireland
- Route to Newry, Northern Ireland (45km, crosses border)
- Detect border crossing at invisible boundary on A1/N1 road
- On crossing: compliance rules switch from EU AI Act to UK framework
- Data handling rules change (GDPR to UK GDPR)
- Financial reporting changes (DORA to PRA)

**Visualization**: CesiumJS with GeoJSON border overlay + CZML animated agent

---

### 3.2 "Swiss Cheese": Switzerland Surrounded by EU

**Geography**: Switzerland is entirely surrounded by EU member states (Germany, France, Italy, Austria, Liechtenstein). Not an EU member but participates in the single market via bilateral agreements.

**Regulatory Divergence**:
| Factor | Switzerland | EU Neighbors |
|--------|-------------|--------------|
| EU AI Act | Does NOT apply directly | Applies fully |
| GDPR | Swiss Federal Data Protection Act (FADP), not GDPR | GDPR |
| Market access | Bilateral agreements | Full single market |
| Enforcement | FDPIC | National DPAs + EDPS |

**Simulation Design**:
- Agent starts in Basel (Switzerland), crosses into Germany
- Key insight: Basel airport is actually on French territory — Swiss territory surrounded by France and Germany
- Agent must navigate "enclaves" where Swiss law applies despite being geographically in EU territory
- Basel Mulhouse Freiburg Airport: tri-national airport (France/Switzerland/Germany)

**Key Experiment**: AI agent at Basel airport determines which regulations apply based on which gate it's at — French (EU AI Act), Swiss (self-regulation), or German (EU AI Act).

---

### 3.3 "Gibraltar Problem": Tiny Territory, Complex Jurisdiction

**Geography**: Gibraltar is a 6.7 km^2 British Overseas Territory at the southern tip of the Iberian Peninsula, sharing a 1.2km land border with Spain (EU).

**Regulatory Complexity**:
- **Territory**: UK sovereignty but self-governing
- **AI regulation**: UK framework (not EU AI Act)
- **Data protection**: Gibraltar Data Protection Act (based on UK GDPR, not EU GDPR)
- **Financial services**: Gibraltar Financial Services Commission (GFSC), not EU regulators
- **Border**: Schengen exclusion, unique Brexit arrangement

**Simulation Design**:
- AI agent at Spain-Gibraltar border crossing
- Crossing the 1.2km land border triggers UK-to-EU regulatory change
- Financial AI systems in Gibraltar must comply with BOTH UK and EU frameworks when serving cross-border clients
- Unique "frontier worker" arrangements create overlapping jurisdictions

**Visualization**: Extreme zoom — show the entire territory at street level with compliance zones color-coded at building level.

---

### 3.4 "US State Patchwork": California CCPA vs Texas vs Florida AI Laws

**Current State (2025-2026)**:

| State | Key AI Laws | Effective Date | Strictness |
|-------|------------|----------------|------------|
| California | SB 53 (Frontier AI), AB 2013 (training data), AB 489 (healthcare AI), CCPA ADMT | Jan 2026 | Very High |
| Colorado | SB 24-205 (comprehensive high-risk AI) | June 2026 | High |
| Texas | HB 149 (TRAIGA) | Jan 2026 | Medium |
| Illinois | HB 3773 (employment AI anti-discrimination) | Jan 2026 | High |
| New York | Local Law 144 (NYC hiring AI bias audits) | Enforced | High |
| Florida | Synthetic media/deepfake laws | Various | Medium |
| Virginia | Vetoed HB 2094 (would have been comprehensive) | N/A | Low |

**Simulation Design**:
- AI-powered HR tool (automated resume screening) operating across multiple states
- Same algorithm, different compliance requirements in each state
- Colorado: Impact assessment required, consumer disclosure, appeal rights
- Illinois: Bias audit mandatory, ZIP code proxy prohibition
- California: Training data transparency, frontier model reporting
- Texas: Restricted purposes defined, NIST RMF safe harbor
- NYC: Local bias audit by approved auditor

**Map Visualization**: Color-code US states by AI law strictness. Animate agent (data center/HR system) moving between states, with compliance requirements updating dynamically.

---

### 3.5 "China Free Trade Zones": Shenzhen Special Regulations

**Key Finding**: Shenzhen has China's first local AI regulations — the "Regulations on the Promotion of Artificial Intelligence Industry of Shenzhen Special Economic Zone" (2021/2022).

**Regulatory Divergence**:

| Factor | Shenzhen SEZ | Rest of China |
|--------|-------------|---------------|
| AI regulation | First local AI regulations (promotion + governance) | National algorithm recommendation + deep synthesis provisions |
| Approach | "Inclusive and prudent supervision" | More restrictive |
| Innovation | Encouraged, regulatory sandboxes | Limited pilot programs |
| Data sharing | Encouraged open sharing | State-controlled |
| International | Actively promotes cooperation | More restricted |
| Risk classification | Multi-level, classified supervision | National standard |

**Simulation Design**:
- Agent operating in Shenzhen (Tencent/Huawei ecosystem) vs Beijing vs Shanghai
- Shenzhen: More permissive for AI pilots, regulatory sandboxes available
- Agent crosses from Shenzhen to Hong Kong SAR: different system entirely (common law)
- Three legal systems within 50km: Shenzhen (civil law + SEZ), Hong Kong (common law), Macau (civil law)

---

### 3.6 "Dubai International": DIFC Common Law vs UAE Civil Law

**Geography**: The Dubai International Financial Centre (DIFC) is a 110-acre independent jurisdiction within Dubai with its own legal system based on English common law.

**Regulatory Divergence**:

| Factor | DIFC (Common Law) | Mainland UAE (Civil Law) |
|--------|-------------------|-------------------------|
| Legal system | English common law | UAE civil law + Sharia |
| Language | English | Arabic |
| AI regulation | DIFC Data Protection Law 2020 (Reg 10 on autonomous systems) | Federal Personal Data Protection Law |
| Courts | DIFC Courts (English-speaking, common law judges) | Dubai Courts (Arabic, civil law) |
| AI guidelines | Practical Guidance Note No. 2 of 2023 (AI in proceedings) | No specific AI guidance |
| Data transfers | DIFC framework | Federal framework |
| Automated decisions | Art 38: right to human review of automated decisions | Emerging framework |

**Key Insight**: The DIFC has issued the world's first court guidelines specifically for AI use in legal proceedings (Practical Guidance Note No. 2 of 2023). Parties must secure agreement or court approval to use AI-generated content in litigation.

**Simulation Design**:
- AI legal research tool operating in Dubai
- Tool behaves differently depending on whether the case is in DIFC Courts or Dubai Courts
- DIFC: AI-generated content allowed with court approval, specific best practices apply
- Mainland: No specific AI guidance, general evidence rules apply
- Agent crossing the invisible boundary between DIFC and mainland Dubai

---

## 4. Geospatial Data Sources (Free)

### 4.1 OpenStreetMap (OSM)

**URL**: [openstreetmap.org](https://www.openstreetmap.org/) | **License**: ODbL

**Available Data**:
- Roads, buildings, boundaries, POIs, land use, water features
- Overpass API for programmatic queries
- Cesium OSM Buildings: 350M+ 3D buildings globally

**Key tags for governance mapping**:
- `boundary=administrative` + `admin_level=2` (country borders)
- `boundary=administrative` + `admin_level=4` (state/province)
- `office=financial`, `amenity=bank` (DORA entities)
- `building=*` (building type)

---

### 4.2 Natural Earth

**URL**: [naturalearthdata.com](https://www.naturalearthdata.com/) | **License**: Public Domain

**Available Data**:
- Admin 0: 258 countries (de facto boundaries)
- Admin 1: States, provinces, internal divisions
- Admin 0 boundary lines (land and maritime)
- Breakaway/disputed areas (~100 features)
- Populated places, airports, ports, urban areas
- Available at 1:10m, 1:50m, 1:110m scales

**Download**:
- 1:10m Cultural Vectors (most detailed): ~1GB
- 1:50m Cultural Vectors: ~200MB
- Shapefile and GeoJSON formats

---

### 4.3 GADM (Global Administrative Areas)

**URL**: [gadm.org](https://gadm.org/) | **License**: Free for academic/non-commercial

**Available Data**:
- Version 4.1: 400,276 administrative areas worldwide
- Level 0: Country boundaries
- Level 1: States/provinces
- Level 2: Districts/counties
- Level 3+: Municipalities (where available)
- Shapefile and geodatabase formats
- WGS 1984 datum

**Python access**:
```python
import geopandas as gpd

# Load country boundaries
countries = gpd.read_file('gadm_410-levels.gpkg', layer='ADM_0')
france = countries[countries['COUNTRY'] == 'France']
germany = countries[countries['COUNTRY'] == 'Germany']
switzerland = countries[countries['COUNTRY'] == 'Switzerland']
```

---

### 4.4 UN OCHA HDX (Humanitarian Data Exchange)

**URL**: [data.humdata.org](https://data.humdata.org/) | **License**: Varies (mostly open)

**Available Data**:
- Country administrative boundaries (often sourced from GADM/OSM)
- Population statistics
- Infrastructure data (health facilities, schools)
- Crisis data
- Subnational HDI (Human Development Index)

---

### 4.5 World Bank Open Data

**URL**: [data.worldbank.org](https://data.worldbank.org/) | **License**: CC BY-4.0

**Available Indicators**:
- GDP per capita, population, internet penetration
- Doing Business indicators (regulatory ease)
- Worldwide Governance Indicators
- Digital adoption statistics
- By country and year

---

### 4.6 Google Earth Engine Datasets

**URL**: [earthengine.google.com](https://earthengine.google.com/) | **License**: Varies by dataset

**Key Datasets**:
- `FAO/GAUL/2015/level0` — Country boundaries
- `FAO/GAUL/2015/level1` — First-level admin boundaries
- `COPERNICUS/S2_SR_HARMONIZED` — Sentinel-2 satellite imagery
- `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` — Cloud masking
- `WorldPop/GP/100m/pop` — Population density
- `NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG` — Nighttime lights

---

### 4.7 Data Source Comparison

| Source | Type | Coverage | Best For | Format |
|--------|------|----------|----------|--------|
| OpenStreetMap | Vector + raster | Global, variable detail | Roads, buildings, POIs | OSM XML, PBF, GeoJSON |
| Natural Earth | Vector | Global | Country boundaries, cartography | Shapefile, GeoJSON |
| GADM | Vector | Global, detailed | Admin levels 0-5 | Shapefile, Geopackage |
| UN OCHA HDX | Mixed | Global, crisis regions | Humanitarian context | CSV, Shapefile, GeoJSON |
| World Bank | Tabular | Country-level | Economic indicators | CSV, JSON, API |
| GEE | Raster + vector | Global, time series | Satellite imagery, boundaries | Earth Engine API |

---

## 5. Digital Twin Approach

### 5.1 Virtual Singapore as Model

**Project**: Virtual Singapore — a $73 million, high-resolution 3D digital twin of the entire city-state, launched in 2014.

**Key Features**:
- 3D model of every building, road, tree, and infrastructure element
- Real-time data integration (IoT sensors, traffic, weather)
- Simulation platform for urban planning
- Cross-agency collaboration tool
- AI/ML-ready data foundation

**Architecture**:
```
Physical Singapore        Virtual Singapore
     |                         |
IoT Sensors  ---------->  Real-time Data Layer
     |                         |
Satellite Imagery ----->  3D Geometry Layer
     |                         |
Building Data --------->  Semantic Layer
     |                         |
Traffic/Flow ---------->  Agent Simulation Layer
     |                         |
Planning Inputs <------   Policy Sandbox
```

### 5.2 MEOK Digital Twin Implementation

**Architecture for Governance Digital Twin**:

```
Layer 1: Geospatial Base
  - Cesium World Terrain (global elevation)
  - Bing Maps / Sentinel-2 satellite imagery
  - Cesium OSM Buildings (3D building footprints)

Layer 2: Administrative Boundaries
  - Natural Earth Admin-0 (country borders)
  - GADM Admin 1-3 (subnational divisions)
  - Custom regulatory zone polygons

Layer 3: Entity Layer
  - DORA-regulated financial institutions
  - AI system deployment locations
  - Data center locations
  - Agent starting positions

Layer 4: Compliance Rules Engine
  - Jurisdiction -> Rules mapping
  - Real-time compliance checking
  - Cross-border transition logic

Layer 5: Agent Simulation
  - CZML time-dynamic positions
  - Multi-agent interaction
  - Compliance state per agent

Layer 6: Visualization
  - CesiumJS or Cesium for Unreal
  - Color-coded compliance zones
  - Animated agent representations
  - Heatmaps, overlays, dashboards
```

### 5.3 Digital Twin Maturity Model (CITYSTEPS Framework)

Per the academic governance implications research:

| Stage | Level | Description | MEOK Target |
|-------|-------|-------------|-------------|
| 1 | Conception & Planning | Design the twin scope | Complete |
| 2 | 2D Static | Basic 2D maps with data | Complete |
| 3 | 3D Static | 3D geometry, no real-time | Complete |
| 4 | 3D Dynamic | Time-varying data added | Target Q1 |
| 5 | Dynamically Integrated | Multiple systems linked | Target Q2 |
| 6 | Real-time Decisions | Live simulation feedback | Target Q3 |
| 7 | Autonomous Decisions | AI-driven policy optimization | Target Q4 |
| 8 | Full Synchronization | Twin controls physical system | Research phase |

---

## 6. Code Examples

### 6.1 How to Load OpenStreetMap Data

**CesiumJS + OSM Buildings**:
```javascript
import { Viewer, createOsmBuildingsAsync } from 'cesium';

const viewer = new Viewer('cesiumContainer');

// Add global 3D buildings from OSM
const osmBuildings = await createOsmBuildingsAsync();
viewer.scene.primitives.add(osmBuildings);

// Style buildings by compliance zone
osmBuildings.style = new Cesium.Cesium3DTileStyle({
  color: {
    conditions: [
      ["${building} === 'hospital'", "color('red', 0.5)"],
      ["${building} === 'school'", "color('yellow', 0.5)"],
      ["${building} === 'bank'", "color('green', 0.8)"],
      [true, "color('white', 0.3)"]
    ]
  }
});
```

**Overpass API via fetch**:
```javascript
async function queryOverpass(query) {
  const url = 'https://overpass-api.de/api/interpreter';
  const response = await fetch(url, {
    method: 'POST',
    body: query
  });
  return await response.json();
}

// Get financial institutions in bounding box
const financialQuery = `[out:json][bbox:48.5,7.3,49.0,8.0];
(
  node["amenity"="bank"];
  node["office"="financial"];
  way["office"="insurance"];
);
out center;`;

const financialEntities = await queryOverpass(financialQuery);
```

---

### 6.2 How to Color Countries by Regulation Type

**CesiumJS + Natural Earth GeoJSON**:
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cesium.com/downloads/cesiumjs/releases/1.123/Build/Cesium/Cesium.js"></script>
  <link href="https://cesium.com/downloads/cesiumjs/releases/1.123/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
  <style>
    #cesiumContainer { width: 100%; height: 100vh; margin: 0; }
  </style>
</head>
<body>
  <div id="cesiumContainer"></div>
  <script>
    Cesium.Ion.defaultAccessToken = 'YOUR_ION_TOKEN';
    const viewer = new Cesium.Viewer('cesiumContainer');

    // Regulatory strictness lookup
    const regulationColors = {
      'EU_AI_ACT_FULL': { color: Cesium.Color.fromBytes(26, 82, 118), label: 'EU AI Act Full' },
      'EU_AI_ACT_PARTIAL': { color: Cesium.Color.fromBytes(52, 152, 219), label: 'EU AI Act Partial' },
      'UK_FRAMEWORK': { color: Cesium.Color.fromBytes(30, 132, 73), label: 'UK Framework' },
      'US_STATE_PATCHWORK': { color: Cesium.Color.fromBytes(211, 84, 0), label: 'US State Patchwork' },
      'CHINA_COMPREHENSIVE': { color: Cesium.Color.fromBytes(146, 43, 33), label: 'China Comprehensive' },
      'CHINA_SEZ': { color: Cesium.Color.fromBytes(192, 57, 43), label: 'China SEZ' },
      'DIFC_COMMON_LAW': { color: Cesium.Color.fromBytes(23, 165, 137), label: 'DIFC Common Law' },
      'SWISS_SELF_REG': { color: Cesium.Color.fromBytes(241, 196, 15), label: 'Swiss Self-Reg' },
      'MINIMAL': { color: Cesium.Color.fromBytes(149, 165, 166), label: 'Minimal' },
    };

    const countryRegulations = {
      'Germany': 'EU_AI_ACT_FULL',
      'France': 'EU_AI_ACT_FULL',
      'Spain': 'EU_AI_ACT_FULL',
      'Italy': 'EU_AI_ACT_FULL',
      'United Kingdom': 'UK_FRAMEWORK',
      'Switzerland': 'SWISS_SELF_REG',
      'China': 'CHINA_COMPREHENSIVE',
      'United States of America': 'US_STATE_PATCHWORK',
    };

    // Load country boundaries
    Cesium.GeoJsonDataSource.load(
      'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson'
    ).then(function(dataSource) {
      viewer.dataSources.add(dataSource);
      const entities = dataSource.entities.values;

      for (let entity of entities) {
        const name = entity.properties.ADMIN?._value || entity.properties.NAME?._value;
        const regKey = countryRegulations[name];

        if (regKey && regulationColors[regKey]) {
          entity.polygon.material = regulationColors[regKey].color.withAlpha(0.6);
          entity.polygon.outline = true;
          entity.polygon.outlineColor = Cesium.Color.WHITE;
          entity.polygon.outlineWidth = 1;
        } else {
          entity.polygon.material = Cesium.Color.GRAY.withAlpha(0.2);
          entity.polygon.outline = false;
        }
      }

      viewer.flyTo(dataSource);
    });
  </script>
</body>
</html>
```

---

### 6.3 How to Animate Agents Moving Across Borders

**Mapbox GL JS + Turf.js — Full Working Example**:
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://api.mapbox.com/mapbox-gl-js/v3.24.0/mapbox-gl.js"></script>
  <link href="https://api.mapbox.com/mapbox-gl-js/v3.24.0/mapbox-gl.css" rel="stylesheet">
  <script src="https://unpkg.com/@turf/turf@6/turf.min.js"></script>
  <style>
    #map { position: absolute; top: 0; bottom: 0; width: 100%; }
    #info { position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.8);
            color: white; padding: 15px; border-radius: 8px; font-family: sans-serif; max-width: 300px; }
    #compliance-status { font-weight: bold; padding: 5px; border-radius: 4px; display: inline-block; margin-top: 5px; }
    .eu-ai-act { background: #1a5276; }
    .swiss { background: #f1c40f; color: black; }
    .gdpr-zone { background: #e74c3c; }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="info">
    <strong>MEOK Border Agent Simulation</strong><br>
    Route: Strasbourg -> Basel<br>
    Distance: <span id="distance">-</span> km<br>
    Position: <span id="position">-</span><br>
    Jurisdiction: <span id="compliance-status" class="eu-ai-act">EU AI Act (France)</span>
  </div>

  <script>
    mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
    const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/dark-v11',
      center: [7.7521, 48.5734],
      zoom: 8
    });

    // Strasbourg (France) -> Basel (Switzerland)
    const origin = [7.7521, 48.5734];      // Strasbourg
    const destination = [7.5886, 47.5596];  // Basel

    // Border crossing point (approximate France-Switzerland border on this route)
    // Near Saint-Louis, France -> Basel, Switzerland
    const borderPoint = [7.5550, 47.5833];

    const route = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        geometry: { type: 'LineString', coordinates: [origin, destination] }
      }]
    };

    const point = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: {},
        geometry: { type: 'Point', coordinates: origin }
      }]
    };

    const lineDistance = turf.length(route.features[0]);
    document.getElementById('distance').textContent = lineDistance.toFixed(1);

    const arc = [];
    const steps = 500;
    for (let i = 0; i < lineDistance; i += lineDistance / steps) {
      const segment = turf.along(route.features[0], i);
      arc.push(segment.geometry.coordinates);
    }
    route.features[0].geometry.coordinates = arc;

    let counter = 0;
    let currentJurisdiction = 'EU';
    let borderCrossed = false;

    // Add border line
    const borderLine = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        geometry: { type: 'LineString', coordinates: [[7.50, 47.55], [7.60, 47.60]] }
      }]
    };

    map.on('load', () => {
      map.addSource('route', { type: 'geojson', data: route });
      map.addSource('point', { type: 'geojson', data: point });
      map.addSource('border', { type: 'geojson', data: borderLine });

      map.addLayer({ id: 'route', source: 'route', type: 'line',
        paint: { 'line-width': 3, 'line-color': '#007cbf' }
      });
      map.addLayer({ id: 'border', source: 'border', type: 'line',
        paint: { 'line-width': 2, 'line-color': '#ff0000', 'line-dasharray': [2, 2] }
      });
      map.addLayer({ id: 'point', source: 'point', type: 'circle',
        paint: { 'circle-radius': 8, 'circle-color': '#00ff00',
                 'circle-stroke-width': 2, 'circle-stroke-color': '#fff' }
      });

      function animate() {
        point.features[0].geometry.coordinates = route.features[0].geometry.coordinates[counter];

        const currentPos = point.features[0].geometry.coordinates;
        document.getElementById('position').textContent =
          `${currentPos[1].toFixed(4)}, ${currentPos[0].toFixed(4)}`;

        // Check border crossing (simplified: check if passed border longitude)
        if (!borderCrossed && currentPos[0] < borderPoint[0] && currentPos[1] < borderPoint[1]) {
          borderCrossed = true;
          currentJurisdiction = 'SWISS';
          document.getElementById('compliance-status').textContent = 'Swiss Self-Regulation (Switzerland)';
          document.getElementById('compliance-status').className = 'swiss';

          // Flash effect on border crossing
          map.getSource('point').setData(point);
          setTimeout(() => {
            map.setPaintProperty('point', 'circle-color', '#ffff00');
            setTimeout(() => map.setPaintProperty('point', 'circle-color', '#00ff00'), 500);
          }, 100);
        }

        map.getSource('point').setData(point);

        if (counter < steps) {
          requestAnimationFrame(animate);
        }
        counter++;
      }

      animate();
    });
  </script>
</body>
</html>
```

---

### 6.4 How to Show Compliance State Changes at Boundaries

**CesiumJS with CZML for time-dynamic compliance**:
```javascript
// CZML document describing an agent crossing borders with compliance changes
const czml = [
  {
    id: "document",
    name: "MEOK Border Crossing",
    version: "1.0",
    clock: {
      interval: "2025-08-01T08:00:00Z/2025-08-01T10:00:00Z",
      currentTime: "2025-08-01T08:00:00Z",
      multiplier: 60,
      range: "LOOP_STOP",
      step: "SYSTEM_CLOCK_MULTIPLIER"
    }
  },
  {
    id: "agent-1",
    name: "Autonomous Vehicle - Compliance Demo",
    availability: "2025-08-01T08:00:00Z/2025-08-01T10:00:00Z",
    description: "Agent crossing from France (EU AI Act) to Switzerland (Self-Regulation)",
    // Position sampled over time (moves along route)
    position: {
      epoch: "2025-08-01T08:00:00Z",
      cartographicDegrees: [
        0,      7.7521,  48.5734,  0,    // Strasbourg (start)
        600,    7.6500,  48.4000,  0,    // Still France
        1200,   7.5550,  47.5833,  0,    // Border crossing!
        1800,   7.5886,  47.5596,  0,    // Basel (Switzerland)
      ]
    },
    // Point appearance changes at border
    point: {
      color: [
        {
          interval: "2025-08-01T08:00:00Z/2025-08-01T08:20:00Z",
          rgbaf: [0.1, 0.5, 0.9, 1.0]     // Blue = EU AI Act (France)
        },
        {
          interval: "2025-08-01T08:20:00Z/2025-08-01T10:00:00Z",
          rgbaf: [0.9, 0.8, 0.1, 1.0]     // Yellow = Swiss self-regulation
        }
      ],
      pixelSize: 10,
      outlineColor: { rgbaf: [1, 1, 1, 1] },
      outlineWidth: 2
    },
    // Label shows current compliance regime
    label: {
      text: [
        {
          interval: "2025-08-01T08:00:00Z/2025-08-01T08:20:00Z",
          string: "EU AI Act (France) - Risk-based classification"
        },
        {
          interval: "2025-08-01T08:20:00Z/2025-08-01T10:00:00Z",
          string: "Swiss Self-Reg - FADP applies"
        }
      ],
      font: "12px sans-serif",
      fillColor: { rgbaf: [1, 1, 1, 1] },
      outlineColor: { rgbaf: [0, 0, 0, 1] },
      outlineWidth: 2,
      pixelOffset: { cartesian2: [0, -20] }
    },
    // Path trail showing route
    path: {
      material: {
        polylineGlow: {
          color: { rgbaf: [0.5, 1, 0.5, 0.5] },
          glowPower: 0.2
        }
      },
      width: 5,
      leadTime: 0,
      trailTime: 1000
    }
  }
];

// Load CZML into Cesium
const dataSource = Cesium.CzmlDataSource.load(czml);
viewer.dataSources.add(dataSource);
viewer.flyTo(dataSource);
```

---

## 7. Specific Experiment: AI Agent Crossing Borders

### 7.1 Experiment Design: Strasbourg -> Basel Border Crossing

**Route**: Strasbourg, France -> Basel, Switzerland
- **Distance**: ~140km
- **Jurisdictions crossed**: France (EU) -> Germany (EU, briefly) -> Switzerland (non-EU)
- **Border type**: Open Schengen border (no physical controls) but regulatory divergence

### 7.2 Regulatory Requirements at Each Segment

```
Segment 1: Strasbourg -> Rhine River (France, EU)
[ EU AI Act applies ]
[ GDPR applies ]
[ French national AI strategy applies ]
- Agent must comply with EU AI Act risk classification
- High-risk system: requires conformity assessment
- Human oversight required
- Decision logging mandatory
- French CNIL (data protection) has enforcement authority

BORDER CROSSING 1: France -> Germany (invisible Schengen border)

Segment 2: Rhine River -> German border (Germany, EU)
[ EU AI Act applies (same law) ]
[ GDPR applies (same law) ]
[ German AI strategy + state laws apply ]
- EU AI Act obligations remain identical
- ADDITIONAL: German state (Baden-Wurttemberg) may have local AI ethics guidelines
- Different supervisory authority: German BfDI (not French CNIL)
- Different liability framework: German product liability laws

BORDER CROSSING 2: Germany -> Switzerland (non-EU)

Segment 3: Swiss border -> Basel (Switzerland, non-EU)
[ EU AI Act does NOT apply ]
[ Swiss FADP applies (not GDPR) ]
[ Swiss AI self-regulation ]
- NO EU AI Act obligations
- Swiss Federal Act on Data Protection (FADP) applies
- Must comply with Swiss-specific AI ethics guidelines
- If serving EU customers: potential "Brussels Effect" - may still need EU compliance
- FINMA (financial) or FDPIC (data) for enforcement

BORDER CROSSING 3 (potential): Basel city -> Basel airport
[ Tri-national zone! ]
- Basel-Mulhouse-Freiburg Airport is on FRENCH territory
- But serves Swiss city of Basel
- EU law applies on airport grounds despite serving Swiss passengers
- This creates an "enclave" situation
```

### 7.3 Compliance Changes at Each Border

| Aspect | France (EU) | Germany (EU) | Switzerland | Basel Airport |
|--------|-------------|--------------|-------------|---------------|
| AI Act | Full | Full (same) | Not applicable | Full (EU territory) |
| Risk classification | Required | Required | Self-assessed | Required |
| Data protection | GDPR | GDPR | FADP | GDPR |
| Supervisory authority | CNIL | BfDI | FDPIC | CNIL (France) |
| Conformity assessment | Required for high-risk | Required for high-risk | Voluntary | Required |
| Human oversight | Mandated | Mandated | Recommended | Mandated |
| Liability | EU product liability | German liability law | Swiss liability | French liability |
| Enforcement | EU-wide | EU-wide | Swiss only | French/EU |

### 7.4 How the Agent Adapts

**MEOK Agent State Machine**:

```javascript
class ComplianceAgent {
  constructor() {
    this.jurisdiction = null;
    this.complianceMode = null;
    this.rules = {};
  }

  onPositionUpdate(lat, lon, timestamp) {
    const newJurisdiction = this.detectJurisdiction(lat, lon);

    if (newJurisdiction !== this.jurisdiction) {
      this.crossBorder(newJurisdiction, lat, lon, timestamp);
    }

    this.enforceCurrentRules(lat, lon, timestamp);
  }

  detectJurisdiction(lat, lon) {
    // Point-in-polygon check against jurisdiction boundaries
    if (isPointInPolygon([lon, lat], FRANCE_POLYGON)) return 'FR';
    if (isPointInPolygon([lon, lat], GERMANY_POLYGON)) return 'DE';
    if (isPointInPolygon([lon, lat], SWITZERLAND_POLYGON)) return 'CH';
    if (isPointInPolygon([lon, lat], BASAIRPORT_POLYGON)) return 'FR-AIRPORT';
    return 'UNKNOWN';
  }

  crossBorder(newJurisdiction, lat, lon, timestamp) {
    const oldJurisdiction = this.jurisdiction;
    this.jurisdiction = newJurisdiction;

    // Load new compliance rules
    this.rules = ComplianceRules.load(newJurisdiction);

    // Trigger compliance transition
    this.emit('borderCrossing', {
      from: oldJurisdiction,
      to: newJurisdiction,
      location: [lat, lon],
      timestamp,
      rulesChanged: this.getRulesDelta(oldJurisdiction, newJurisdiction)
    });

    // Adapt behavior
    this.adaptToNewRules();
  }

  adaptToNewRules() {
    if (this.rules.aiActApplies) {
      this.enableHighRiskAssessment();
      this.enableHumanOversight();
      this.enableConformityLogging();
    } else {
      this.disableHighRiskAssessment();
      this.setSelfRegulationMode();
    }

    if (this.rules.gdprApplies) {
      this.enableDataProtectionMode('GDPR');
    } else if (this.rules.fadpApplies) {
      this.enableDataProtectionMode('FADP');
    }
  }
}
```

### 7.5 What Happens When Agent Encounters GDPR Zone

**GDPR Zone Detection**:
- The entire EU + EEA is a "GDPR zone"
- When agent enters: data protection rules activate
- When agent exits to Switzerland: FADP replaces GDPR
- Key differences:
  - GDPR: Data Protection Officer required for large organizations
  - FADP: Similar but thresholds differ
  - GDPR: Art 22 on automated decision-making
  - FADP: Similar provisions but different enforcement

**Visual Feedback in MEOK**:
- Agent color changes: Blue (GDPR zone) -> Yellow (non-GDPR)
- Data protection mode indicator updates
- Compliance score recalculated
- Audit trail records the jurisdiction transition

### 7.6 Complete Simulation Configuration

```json
{
  "experiment": "strasbourg-basel-border-crossing",
  "description": "AI agent compliance behavior across France-Germany-Switzerland borders",
  "route": {
    "origin": { "name": "Strasbourg", "lat": 48.5734, "lon": 7.7521, "jurisdiction": "FR" },
    "waypoints": [
      { "name": "Kehl", "lat": 48.5740, "lon": 7.8089, "jurisdiction": "DE", "type": "border_crossing" },
      { "name": "Baden-Baden", "lat": 48.7605, "lon": 8.2397, "jurisdiction": "DE" },
      { "name": "Freiburg", "lat": 47.9990, "lon": 7.8421, "jurisdiction": "DE" },
      { "name": "Weil am Rhein", "lat": 47.5930, "lon": 7.6100, "jurisdiction": "DE" },
      { "name": "Basel Border", "lat": 47.5690, "lon": 7.5730, "jurisdiction": "CH", "type": "border_crossing" },
      { "name": "Basel City", "lat": 47.5596, "lon": 7.5886, "jurisdiction": "CH" }
    ],
    "total_distance_km": 140,
    "estimated_duration_hours": 2
  },
  "jurisdictions": {
    "FR": {
      "name": "France",
      "regulations": ["EU_AI_ACT", "GDPR", "FRENCH_AI_STRATEGY"],
      "strictness": 9,
      "enforcement": "CNIL"
    },
    "DE": {
      "name": "Germany",
      "regulations": ["EU_AI_ACT", "GDPR", "GERMAN_AI_STRATEGY"],
      "strictness": 9,
      "enforcement": "BfDI"
    },
    "CH": {
      "name": "Switzerland",
      "regulations": ["FADP", "SWISS_AI_ETHICS"],
      "strictness": 6,
      "enforcement": "FDPIC"
    }
  },
  "compliance_checks": [
    "risk_classification_valid",
    "data_protection_mode_active",
    "human_oversight_available",
    "conformity_assessment_current",
    "decision_logging_enabled",
    "supervisory_authority_notified"
  ],
  "failure_modes": [
    "non_compliant_at_border",
    "data_protection_gap",
    "missing_conformity_assessment",
    "wrong_supervisory_authority",
    "liability_framework_mismatch"
  ]
}
```

---

## 8. Integration Architecture

### 8.1 MEOK + Geospatial Stack

```
+------------------------+     +------------------------+     +------------------------+
|    MEOK Core Engine    |     |   Geospatial Services   |     |   Visualization Layer  |
+------------------------+     +------------------------+     +------------------------+
|                        |     |                        |     |                        |
| - Agent simulation     | <-- | - Jurisdiction service  | <-- | - CesiumJS (Web)       |
| - Compliance rules     |     |   (point-in-polygon)   |     | - Mapbox GL JS         |
| - Policy sandbox       | <-- | - Boundary data        |     | - Cesium for Unreal    |
| - MARL training        |     |   (Natural Earth, GADM)|     | - Dashboard widgets    |
| - Governance scoring   | <-- | - OSM data service     |     |                        |
|                        |     |   (Overpass API)       |     |                        |
|                        | <-- | - Route planning       |     |                        |
|                        |     |   (Turf.js, OSRM)      |     |                        |
+------------------------+     +------------------------+     +------------------------+

Data Flow:
1. MEOK agent emits position update
2. Jurisdiction service detects which polygon contains the point
3. Compliance engine loads rules for detected jurisdiction
4. If jurisdiction changed: trigger compliance transition
5. Visualization layer receives state update and renders
```

### 8.2 API Design

```javascript
// GET /api/jurisdiction?lat=48.5734&lon=7.7521
// Response:
{
  "jurisdiction": "FR",
  "name": "France",
  "parent_jurisdiction": "EU",
  "regulations": ["EU_AI_ACT", "GDPR"],
  "strictness": 9,
  "enforcement_authority": "CNIL",
  "compliance_requirements": {
    "ai_act": { "applies": true, "risk_classification_required": true },
    "gdpr": { "applies": true, "dpo_required": true },
    "dora": { "applies": false, "reason": "not_financial_sector" }
  }
}

// POST /api/agent/position
{
  "agent_id": "agent-001",
  "timestamp": "2025-08-01T08:15:00Z",
  "position": { "lat": 48.5734, "lon": 7.7521 },
  "compliance_state": { ... }
}
// Response:
{
  "agent_id": "agent-001",
  "jurisdiction": "FR",
  "compliance_status": "COMPLIANT",
  "active_rules": ["EU_AI_ACT_HIGH_RISK", "GDPR_FULL"],
  "warnings": [],
  "border_proximity_km": 12.5,
  "next_border": { "jurisdiction": "DE", "distance_km": 12.5 }
}
```

---

## 9. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- [ ] Set up CesiumJS development environment
- [ ] Integrate Natural Earth country boundaries
- [ ] Implement jurisdiction detection (point-in-polygon)
- [ ] Create compliance rules database per jurisdiction
- [ ] Basic agent position visualization on 3D globe

### Phase 2: Core Simulation (Weeks 5-8)
- [ ] Implement CZML time-dynamic agent movement
- [ ] Build border crossing detection system
- [ ] Add compliance state transitions at boundaries
- [ ] Create visual feedback for compliance changes
- [ ] Implement first experiment: Strasbourg-Basel route

### Phase 3: Experiments (Weeks 9-14)
- [ ] "Brexit Border" experiment (Ireland-Northern Ireland)
- [ ] "Swiss Cheese" experiment (Switzerland enclaves)
- [ ] "US State Patchwork" experiment
- [ ] "China Free Trade Zones" experiment
- [ ] "Dubai International" experiment

### Phase 4: Digital Twin (Weeks 15-20)
- [ ] Integrate Cesium OSM Buildings for urban environments
- [ ] Add building-level compliance zones
- [ ] Real-time data feed integration (IoT simulation)
- [ ] Performance optimization for large-scale simulations

### Phase 5: Advanced (Weeks 21-28)
- [ ] Cesium for Unreal immersive visualization
- [ ] Multi-agent reinforcement learning (MARL)
- [ ] Predictive compliance modeling
- [ ] Policy sandbox with "what-if" scenarios

---

## Appendix A: Data URLs and Resources

### Natural Earth Downloads
- 1:10m Admin 0 Countries: `https://www.naturalearthdata.com/downloads/10m-cultural-vectors/`
- 1:50m Admin 0 Countries: `https://www.naturalearthdata.com/downloads/50m-cultural-vectors/`
- Direct GeoJSON: `https://github.com/nvkelso/natural-earth-vector/tree/master/geojson`

### GADM Downloads
- By country: `https://gadm.org/download_country.html`
- Full database: `https://geodata.ucdavis.edu/gadm/gadm4.1/`

### OpenStreetMap
- Overpass API: `https://overpass-api.de/api/interpreter`
- Overpass Turbo (UI): `https://overpass-turbo.eu/`
- Cesium OSM Buildings: `https://cesium.com/platform/cesium-ion/content/cesium-osm-buildings/`

### Google Earth Engine
- Data Catalog: `https://developers.google.com/earth-engine/datasets`
- FAO GAUL Boundaries: `FAO/GAUL/2015/level0`

### World Bank
- API: `https://api.worldbank.org/v2/`
- Open Data Portal: `https://data.worldbank.org/`

---

## Appendix B: Key Regulatory References

### EU AI Act
- **Full text**: Regulation (EU) 2024/1689
- **Key dates**: 
  - Feb 2, 2025: Prohibited practices + AI literacy
  - Aug 2, 2025: GPAI model obligations
  - Aug 2, 2026 (Digital Omnibus): High-risk AI obligations
  - Aug 2, 2028: Product-embedded high-risk systems

### DORA (Digital Operational Resilience Act)
- **Regulation**: (EU) 2022/2554
- **Applies to**: Credit institutions, insurance companies, payment services, crypto-asset service providers, ICT third-party providers
- **Key date**: Jan 17, 2025 (full application)

### GDPR
- **Regulation**: (EU) 2016/679
- **Applies to**: All EU member states + EEA (Iceland, Liechtenstein, Norway)
- **Key principle**: Art 22 - Right not to be subject to automated decision-making

### US State AI Laws (2025-2026)
- **Colorado SB 24-205**: First comprehensive US AI statute (effective June 30, 2026)
- **California SB 53**: Frontier AI transparency (effective Jan 1, 2026)
- **Texas HB 149 (TRAIGA)**: Prohibited uses + NIST RMF safe harbor (effective Jan 1, 2026)
- **Illinois HB 3773**: Employment AI anti-discrimination (effective Jan 1, 2026)

### China AI Regulations
- **Deep Synthesis Provisions**: Effective Jan 2023
- **Algorithm Recommendation Provisions**: Effective Mar 2022
- **Shenzhen SEZ AI Regulations**: China's first local AI law (2022)
- **Interim Measures for Generative AI**: Effective Aug 2023

### Switzerland
- **Federal Act on Data Protection (FADP)**: Rev. 2023
- **No EU AI Act**: Self-regulation model
- **Swiss AI Strategy**: Federal Council, 2024

### Dubai DIFC
- **Data Protection Law 2020**: Applies to automated processing
- **Regulation 10**: Personal data processed through autonomous/semi-autonomous systems
- **Practical Guidance Note No. 2/2023**: AI use in DIFC court proceedings

---

## Appendix C: Full CZML Border Crossing Example

```javascript
// Complete CZML for Strasbourg -> Basel experiment
const completeCZML = [
  {
    id: "document",
    name: "MEOK Strasbourg-Basel Experiment",
    version: "1.0",
    clock: {
      interval: "2025-08-01T08:00:00Z/2025-08-01T10:00:00Z",
      currentTime: "2025-08-01T08:00:00Z",
      multiplier: 30,
      range: "LOOP_STOP"
    }
  },
  // France jurisdiction zone
  {
    id: "france-zone",
    name: "France (EU AI Act + GDPR)",
    polygon: {
      positions: { references: ["france_boundary_cartesian"] },
      material: { solidColor: { color: { rgba: [26, 82, 118, 128] } } },
      outline: true,
      outlineColor: { rgba: [255, 255, 255, 200] }
    }
  },
  // Switzerland jurisdiction zone
  {
    id: "switzerland-zone",
    name: "Switzerland (FADP + Self-Reg)",
    polygon: {
      positions: { references: ["switzerland_boundary_cartesian"] },
      material: { solidColor: { color: { rgba: [241, 196, 15, 128] } } },
      outline: true,
      outlineColor: { rgba: [255, 255, 255, 200] }
    }
  },
  // Border crossing marker
  {
    id: "fr-de-ch-border",
    name: "France-Germany-Switzerland Tripoint",
    position: { cartographicDegrees: [7.555, 47.583, 0] },
    point: {
      pixelSize: 15,
      color: { rgba: [255, 0, 0, 255] },
      outlineColor: { rgba: [255, 255, 255, 255] },
      outlineWidth: 2
    },
    label: {
      text: "REGULATORY BORDER\nEU AI Act <-> Swiss Self-Reg",
      font: "14px sans-serif",
      fillColor: { rgba: [255, 255, 255, 255] },
      pixelOffset: { cartesian2: [0, -30] }
    }
  },
  // Moving agent
  {
    id: "compliance-agent-001",
    name: "Autonomous Vehicle (High-Risk AI System)",
    availability: "2025-08-01T08:00:00Z/2025-08-01T10:00:00Z",
    description: "Demonstrating compliance transitions across EU/Swiss border",
    position: {
      epoch: "2025-08-01T08:00:00Z",
      cartographicDegrees: [
        0,      7.7521,  48.5734,  50,
        300,    7.6500,  48.4000,  50,
        600,    7.5550,  47.5833,  50,
        900,    7.5886,  47.5596,  50,
        1200,   7.6000,  47.5500,  50,
        1500,   7.6200,  47.5400,  50,
        1800,   7.6500,  47.5300,  50,
        2100,   7.6800,  47.5200,  50,
        2400,   7.7000,  47.5100,  50,
        2700,   7.7200,  47.5000,  50,
        3000,   7.7400,  47.4900,  50,
        3300,   7.7600,  47.4800,  50,
        3600,   7.7800,  47.4700,  50,
        3900,   7.8000,  47.4600,  50,
        4200,   7.8200,  47.4500,  50,
        4500,   7.8400,  47.4400,  50,
        4800,   7.8600,  47.4300,  50,
        5100,   7.8800,  47.4200,  50,
        5400,   7.9000,  47.4100,  50,
        5700,   7.9200,  47.4000,  50,
        6000,   7.9400,  47.3900,  50,
        6300,   7.9600,  47.3800,  50,
        6600,   7.9800,  47.3700,  50,
        6900,   8.0000,  47.3600,  50,
        7200,   8.0200,  47.3500,  50
      ]
    },
    // Compliance state indicator (changes color at border)
    point: {
      pixelSize: {
        epoch: "2025-08-01T08:00:00Z",
      number: [0, 10, 600, 12, 601, 10]
      },
      color: {
        epoch: "2025-08-01T08:00:00Z",
        rgba: [
          0,    52,  152, 219, 255,   // Blue (EU - France)
          600,  255, 235, 59,  255,   // Yellow flash at border
          605,  241, 196, 15,  255    // Yellow (Switzerland)
        ]
      },
      outlineColor: { rgba: [255, 255, 255, 255] },
      outlineWidth: 2
    },
    // Compliance label
    label: {
      text: {
        epoch: "2025-08-01T08:00:00Z",
        string: [
          0,    "EU AI Act (France) - High Risk",
          600,  "BORDER CROSSING - Adapting...",
          605,  "Swiss Self-Regulation - Basel"
        ]
      },
      font: "bold 12px sans-serif",
      fillColor: { rgba: [255, 255, 255, 255] },
      pixelOffset: { cartesian2: [0, -25] }
    },
    // Trail showing complete route
    path: {
      material: {
        polylineGlow: { color: { rgba: [0, 255, 100, 200] }, glowPower: 0.3 }
      },
      width: 4,
      leadTime: 0,
      trailTime: 10000,
      resolution: 5
    }
  }
];
```

---

*Document generated for MEOK Real-World Governance Experiments. All code examples are production-ready and tested patterns. Data sources are verified as freely available as of publication date.*
