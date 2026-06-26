# MEOK EARTH: Real-World Overlay Technology Research

> **Research Date**: 2025-07-22
> **Purpose**: Identify and evaluate all available technologies for overlaying real-world geospatial data into a UE5-based game environment where players can build on their actual homes, neighborhoods, and cities.
> **Researcher**: Geospatial Technology Research Agent

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [CesiumJS / Cesium for Unreal](#2-cesiumjs--cesium-for-unreal)
3. [Google Photorealistic 3D Tiles API](#3-google-photorealistic-3d-tiles-api)
4. [Mapbox 3D / Maps SDK](#4-mapbox-3d--maps-sdk)
5. [OpenStreetMap 3D Data (OSM2World, Blosm)](#5-openstreetmap-3d-data-osm2world-blosm)
6. [Mapillary Street-Level Imagery](#6-mapillary-street-level-imagery)
7. [NASA SRTM Terrain Data](#7-nasa-srtm-terrain-data)
8. [USGS 3DEP (3D Elevation Program)](#8-usgs-3dep-3d-elevation-program)
9. [Copernicus DEM (European Space Agency)](#9-copernicus-dem-european-space-agency)
10. [CityJSON / 3DCityDB Digital Twin Platform](#10-cityjson--3dcitydb-digital-twin-platform)
11. [Azure Digital Twins](#11-azure-digital-twins)
12. [AWS IoT TwinMaker](#12-aws-iot-twinmaker)
13. [OpenTopography LiDAR Portal](#13-opentopography-lidar-portal)
14. [Landscape Combinator (UE5 Plugin)](#14-landscape-combinator-ue5-plugin)
15. [ArcGIS Maps SDK for Unreal Engine](#15-arcgis-maps-sdk-for-unreal-engine)
16. [NVIDIA Omniverse](#16-nvidia-omniverse)
17. [Additional Tools & Workflows](#17-additional-tools--workflows)
18. [Comprehensive Comparison Matrix](#18-comprehensive-comparison-matrix)
19. [Recommendations for MEOK EARTH](#19-recommendations-for-meok-earth)

---

## 1. Executive Summary

This research identifies **16 major technology stacks** capable of bringing real-world geospatial data into Unreal Engine 5 for a game like MEOK EARTH. The technologies range from **free open-source solutions** (Cesium for Unreal, OSM2World, NASA SRTM) to **commercial APIs** (Google Photorealistic 3D Tiles, Mapbox, Cesium ion commercial tiers) to **enterprise cloud platforms** (Azure Digital Twins, AWS IoT TwinMaker).

### Top Recommendations (Quick Pick)

| Priority | Technology | Role |
|----------|-----------|------|
| **#1** | **Cesium for Unreal** + **Cesium ion** | Primary 3D globe + streaming engine |
| **#2** | **Google Photorealistic 3D Tiles** | Photorealistic 3D buildings (where available) |
| **#3** | **OpenStreetMap** + **OSM2World/Blosm** | Free global building footprints + 3D extrusion |
| **#4** | **NASA SRTM / Copernicus DEM** | Free global terrain elevation |
| **#5** | **Landscape Combinator** | UE5-native real-world landscape generation |
| **#6** | **3DCityDB** | Open-source city-scale digital twin database |

### Key Technical Challenge
The primary challenge for MEOK EARTH is **combining multiple data sources** at different resolutions and ensuring seamless integration. No single source provides complete global coverage with the resolution needed for gameplay at street level. A **multi-layer pipeline** is required:

```
Layer 1: Global terrain (SRTM/Copernicus/Cesium World Terrain)
Layer 2: Regional high-res terrain (USGS 3DEP, OpenTopography LiDAR)
Layer 3: 3D buildings (Google 3D Tiles > OSM extruded buildings > CityJSON)
Layer 4: Street-level imagery (Mapillary for texture reference)
Layer 5: Road/vegetation/water vectors (OSM via Landscape Combinator)
```

---

## 2. CesiumJS / Cesium for Unreal

### Overview
Cesium is the **leading open-source platform** for 3D geospatial visualization. Cesium for Unreal is a free plugin that brings a full-scale, high-accuracy WGS84 globe into Unreal Engine 5, streaming massive 3D datasets in real-time using the open 3D Tiles standard. [^97^] [^99^]

### Key Features
- **Full-scale WGS84 globe** with sub-meter accuracy [^96^]
- **Runtime 3D Tiles engine** with level-of-detail (LOD) selection and caching [^100^]
- **Integration with UE5**: Actors, Components, Blueprints, Landscapes, Foliage, Sequencer [^100^]
- **Physics support**: Character/vehicle collisions with photogrammetry, atmosphere, shadows [^100^]
- **Multiple data sources**: Cesium ion, Google 3D Tiles, self-hosted tilesets [^97^]
- **Plugins available**: Unreal Engine, Unity, O3DE, Omniverse, Godot (2025) [^95^]

### License & Cost
| Aspect | Details |
|--------|---------|
| **Plugin** | **Free, Apache 2.0** - commercial and non-commercial use [^97^] |
| **Cesium ion Community** | Free for non-commercial use, limited streaming quota [^172^] [^185^] |
| **Cesium ion Commercial** | $149/month (Individual), $524/month (Team) [^172^] |
| **Cesium ion Premium** | $499/month (Individual), $874/month (Team) [^172^] |
| **Cesium ion Enterprise** | Custom pricing, self-hosted option available [^172^] |

### UE5 Integration Difficulty
- **Easy**: Install from Unreal Marketplace, connect Cesium ion account, add tilesets via UI panel [^122^]
- **Setup time**: 15-30 minutes for basic globe with terrain + buildings
- **Requires**: UE 5.1+ (supports UE 4.26+ for older versions) [^97^]
- **Tutorials**: Comprehensive quickstart at cesium.com/learn/unreal [^122^]

### Coverage & Resolution
| Data Type | Coverage | Resolution |
|-----------|----------|------------|
| Cesium World Terrain | Global | ~10-30m, varies by region |
| Cesium OSM Buildings | Global | Building footprints extruded from OSM |
| Bing Maps Imagery | Global | 15cm-30m satellite imagery |
| Google Photorealistic 3D | 2,500+ cities | ~7.5cm photogrammetry [^101^] |

### URLs
- **GitHub**: https://github.com/CesiumGS/cesium-unreal [^97^]
- **Official**: https://cesium.com/platform/cesium-for-unreal/ [^99^]
- **Marketplace**: Unreal Engine Marketplace (free) [^95^]
- **Docs**: https://cesium.com/learn/unreal/unreal-quickstart/ [^122^]

### Why It's Critical for MEOK EARTH
Cesium for Unreal is the **foundation technology** - it provides the globe-scale coordinate system, streaming engine, and integration layer that all other data sources can plug into. Epic Games has officially partnered with Cesium, calling it "ideal to support Epic's vision for an open Metaverse." [^96^]

---

## 3. Google Photorealistic 3D Tiles API

### Overview
Google's photorealistic 3D tiles provide **high-resolution 3D mesh models** of real-world buildings and terrain, created from aerial photogrammetry. Accessible through Cesium ion integration in UE5. [^90^] [^181^]

### Key Features
- **Real photogrammetric 3D models** (not extruded footprints) [^101^]
- **Aerial capture quality** - approximately 7.5cm imagery resolution [^101^]
- **Global coverage** of 2,500+ cities and urban areas [^90^]
- **Streamed via Cesium for Unreal** using Google Maps Platform API [^181^]
- **VR-ready** - works with Meta Quest and other VR headsets [^174^]

### License & Cost
| Tier | Price | Notes |
|------|-------|-------|
| 0-1K root tiles/month | **FREE** | Evaluation tier [^90^] |
| 1K-100K | $6.00 CPM ($0.006/session) | Per root tile = roughly per app launch [^90^] |
| 100K-500K | $5.10 CPM | Volume discount [^90^] |
| 500K-1M | $4.20 CPM | Volume discount [^90^] |
| 1M-5M | $3.30 CPM | Volume discount [^90^] |
| 5M+ | $2.40 CPM | Contact Google for pricing [^90^] |

> **Important**: Google provides a **$200/month credit** across all Maps Platform APIs. With Photorealistic 3D Tiles at $6/CPM, this equals ~33,333 free root tile sessions/month. [^104^]

> **EU/EEA Restriction**: As of July 2025, Google 3D Tiles are **unavailable for new projects** with EU/EEA billing addresses. [^154^]

### UE5 Integration Difficulty
- **Easy-Medium**: Requires Cesium for Unreal plugin + Google Cloud API key [^181^]
- **Steps**: (1) Install Cesium for Unreal, (2) Create Google Cloud project + enable Maps Tiles API, (3) Add API key to Cesium ion, (4) Select "Google Photorealistic 3D Tiles" from Cesium panel [^181^]
- **Setup time**: 30-60 minutes including Google Cloud setup

### Coverage & Resolution
| Metric | Value |
|--------|-------|
| **Spatial coverage** | ~2,500 cities worldwide, primarily high-density urban areas [^101^] |
| **Resolution** | ~7.5cm imagery, less detailed geometry in some areas [^101^] |
| **Temporal coverage** | Updated roughly every 1-5 years [^101^] |
| **US coverage** | Most major cities covered |
| **EU coverage** | Available but new projects blocked for EU/EEA billing |

### URLs
- **Cesium Tutorial**: https://cesium.com/learn/unreal/unreal-photorealistic-3d-tiles/ [^181^]
- **VR Tutorial**: https://dev.epicgames.com/community/learning/tutorials/v2ZB/ [^174^]
- **Google Pricing**: https://developers.google.com/maps/documentation/tile/usage-and-billing

### Cost Risk Analysis for MEOK EARTH
| Monthly Active Users | Monthly Cost (after $200 credit) |
|---------------------|----------------------------------|
| 10,000 | FREE (within credit) |
| 50,000 | ~$100 |
| 100,000 | ~$400 |
| 500,000 | ~$2,440 |
| 1,000,000+ | Contact Google (volume pricing) |

> **Warning**: Google has **no hard spending caps** - only alerts. A viral spike could result in unexpected bills. [^104^]

---

## 4. Mapbox 3D / Maps SDK

### Overview
Mapbox provides mapping, navigation, and location data services including 3D terrain, satellite imagery, and building data. Has SDKs for Unity (legacy) and web, but **no official UE5 plugin**. [^155^] [^179^]

### Key Features
- **3D Terrain v2**: Global elevation data as vector tiles
- **3D Buildings**: Extruded building footprints from Mapbox Streets data [^179^]
- **Satellite imagery**: Global coverage at multiple resolutions
- **Custom styles**: Mapbox Studio for creating custom map styles
- **Unity SDK**: Available but v2 not in active development, v3 in development [^179^]

### License & Cost
| Service | Monthly Free Tier | Paid Rate |
|---------|-------------------|-----------|
| **Maps (Web Loads)** | 50,000 loads | $5.00/1K (drops to $3.00/1K at 200K+) [^147^] |
| **Vector Tiles API** | 200,000 requests | Pay per request [^155^] |
| **Raster Tiles** | 200,000 requests | Pay per request [^155^] |
| **Satellite Tiles** | 750,000 requests | Pay per request [^155^] |
| **Geocoding** | 100,000 requests | $4-5/1K (most expensive API) [^147^] |
| **Tilesets API** | None | Pay from first request [^147^] |

> No spending caps available - customers bear unlimited financial risk without proper controls. [^147^]

### UE5 Integration Difficulty
- **Hard**: No official UE5 SDK exists
- **Workaround**: Use Cesium for Unreal + MapTiler integration (WMTS tiles) [^94^]
- **Alternative**: Use Mapbox Unity SDK (not actively maintained) [^179^]
- **Best path**: Use Cesium + MapTiler or Cesium + Cesium ion imagery instead

### Coverage & Resolution
| Data Type | Coverage | Resolution |
|-----------|----------|------------|
| Terrain | Global | Vector TIN tiles |
| Satellite | Global | Variable, typically 30cm-5m |
| Buildings | Major cities | Extruded footprints (not photogrammetric) |

### URLs
- **Pricing**: https://www.mapbox.com/pricing [^155^]
- **Unity SDK**: https://docs.mapbox.com/unity/maps/guides/install/ [^179^]
- **MapTiler+Cesium**: https://docs.maptiler.com/unreal/ [^94^]

### Verdict for MEOK EARTH
**Not recommended as primary solution** due to lack of UE5 SDK. Better options exist through Cesium ecosystem. Mapbox data can be accessed via MapTiler integration with Cesium if needed.

---

## 5. OpenStreetMap 3D Data (OSM2World, Blosm)

### Overview
OpenStreetMap (OSM) is a **free, crowdsourced** geographic database with global building footprints, road networks, vegetation, water bodies, and some building height data. Multiple tools convert OSM data into 3D models. [^130^] [^124^]

### OSM Building Height Data
- Only **~3% of 335 million building footprints** have explicit `height` tags [^126^]
- **~3.5%** have `building:levels` tags (number of floors) [^126^]
- Height data concentrated in **Europe and North America** [^126^]
- Heights sourced from government imports, on-site measurements, or shadow detection [^126^]

### Key Tools

#### OSM2World
- **Converts OSM data to 3D models** (OBJ, glTF, 3D Tiles) [^125^]
- Supports building heights, roof shapes, building parts, materials [^125^]
- Outputs compatible with Cesium 3D Tiles [^125^]
- **License**: Open source (GPL)
- **URL**: https://osm2world.org/ [^125^]

#### Blosm (formerly Blender-OSM)
- **UE5 workflow**: Import OSM buildings into Blender, then export to UE5
- Free base version, Pro version with textures/materials
- Imports buildings, terrain (~30m res), roads, rivers, forests, vegetation [^154^]
- Supports Google 3D Tiles import (not EU/EEA for new projects) [^161^]
- **License**: GPL (source available)
- **URL**: https://github.com/vvoovv/blosm [^161^]
- **Download**: https://prochitecture.gumroad.com/l/blender-osm [^154^]

#### Overpass API
- **Query OSM data programmatically** using Overpass QL language [^221^]
- Free, read-only API for extracting building data by bounding box [^221^]
- Returns building footprints, heights, levels, and other tags [^209^]
- **Rate limits**: Public servers under heavy load; Geofabrik offers paid instances [^215^]
- **URL**: https://wiki.openstreetmap.org/wiki/Overpass_API [^221^]
- **Interactive query builder**: https://overpass-turbo.eu/ [^221^]

### License & Cost
| Component | License | Cost |
|-----------|---------|------|
| OpenStreetMap data | **ODbL** (Open Database License) | **FREE** |
| OSM2World | GPL | **FREE** |
| Blosm (base) | GPL | **FREE** (donation optional) |
| Blosm Pro | GPL | ~EUR 100 (one-time) |
| Overpass API | AGPL | **FREE** (public servers) |

### UE5 Integration Difficulty
- **Medium**: Workflow is OSM -> Blender (Blosm) -> FBX/OBJ -> UE5
- **Steps**: (1) Download OSM data via Overpass API or Geofabrik, (2) Import to Blender with Blosm, (3) Export as FBX/glTF, (4) Import into UE5
- **Alternative**: Use Cesium OSM Buildings (already in Cesium ion) for quick global coverage [^122^]
- **Time estimate**: Hours for custom areas; minutes via Cesium OSM Buildings

### Coverage & Resolution
| Metric | Value |
|--------|-------|
| **Building footprints** | 335M+ globally, improving daily |
| **Buildings with height** | ~3% globally, higher in Europe/NA [^126^] |
| **Building levels** | ~3.5% globally [^126^] |
| **Roads** | Near-complete global coverage |
| **Water bodies** | Near-complete global coverage |
| **Terrain (via Blosm)** | ~30m resolution |

### URLs
- **OSM**: https://www.openstreetmap.org/
- **OSM2World**: https://osm2world.org/ [^125^]
- **Blosm GitHub**: https://github.com/vvoovv/blosm [^161^]
- **Overpass API**: https://wiki.openstreetmap.org/wiki/Overpass_API [^221^]
- **Geofabrik extracts**: https://download.geofabrik.de/

---

## 6. Mapillary Street-Level Imagery

### Overview
Mapillary is a **crowdsourced street-level imagery platform** with over **2.4 billion geotagged images** across 190+ countries. Provides ground-level perspective that complements satellite/aerial data. [^103^] [^92^]

### Key Features
- **2.4B+ street-level images** globally [^103^]
- **Computer vision extraction**: Traffic signs (1,500+ classes), road markings, street furniture (40+ feature classes), POI detection [^103^]
- **CC BY-SA 4.0 license** - free for commercial and non-commercial use [^102^]
- **API access**: Free with rate limits; Python SDK and JavaScript library available [^92^]
- **Integrations**: QGIS plugin, OpenStreetMap editing tools [^92^]
- **Privacy**: Faces and license plates automatically blurred [^102^]

### License & Cost
| Aspect | Details |
|--------|---------|
| **License** | CC BY-SA 4.0 (free for all uses) [^102^] |
| **API access** | **FREE** with rate limits [^102^] |
| **Commercial use** | Permitted at no cost [^102^] |
| **Acquisition** | Acquired by Meta (Facebook) in 2020, paid tier eliminated [^102^] |

### UE5 Integration Difficulty
- **Hard**: No direct UE5 integration
- **Use cases for MEOK EARTH**: 
  - Texture reference for building facades
  - Street-level visual validation of generated 3D geometry
  - Extracting real-world sign/POI locations for gameplay elements
- **Workflow**: Query via API -> download images -> use as textures in UE5 materials

### Coverage & Resolution
| Metric | Value |
|--------|-------|
| **Image count** | 2.4B+ images [^103^] |
| **Countries** | 190+ [^92^] |
| **Coverage quality** | Uneven - best in populated areas, sparse in remote regions [^102^] |
| **Resolution** | Varies by capture device (smartphone to professional 360 cameras) [^102^] |

### URLs
- **Platform**: https://www.mapillary.com/ [^103^]
- **API Docs**: https://www.mapillary.com/developer [^92^]
- **Help Center**: https://help.mapillary.com/hc/en-us [^103^]

### Use for MEOK EARTH
Best used as a **supplementary texture/data source** rather than primary geometry pipeline. Can provide authentic street-level photographs for texturing building facades in key areas.

---

## 7. NASA SRTM Terrain Data

### Overview
The Shuttle Radar Topography Mission (SRTM) is NASA's **free global digital elevation dataset**, covering ~80% of Earth. The most widely-used free terrain dataset globally. [^117^] [^120^]

### Key Features
- **Near-global coverage** (56S to 60N latitude) [^120^]
- **Two resolutions**: 1 arc-second (~30m) and 3 arc-second (~90m) [^121^]
- **Available formats**: GeoTIFF, DTED, BIL [^127^]
- **Vertical accuracy**: <16m reported error [^120^]
- **Free and unrestricted** download via USGS EarthExplorer or NASA Earthdata [^117^]

### License & Cost
| Aspect | Details |
|--------|---------|
| **License** | Public domain (US Government work) |
| **Cost** | **FREE** |
| **Access** | Earthdata Login (free registration) [^117^] |
| **Restrictions** | None |

### UE5 Integration Difficulty
- **Medium**: Requires conversion to heightmap format
- **Workflow**: (1) Download SRTM GeoTIFF from EarthExplorer/USGS, (2) Convert to 16-bit PNG heightmap using GIS tool (QGIS, GDAL), (3) Import into UE5 Landscape system
- **Tools**: terrain.party (simplified), QGIS (full control), World Machine [^157^]
- **Landscape Combinator plugin** automates this workflow [^213^]

### Coverage & Resolution
| Product | Resolution | Coverage |
|---------|-----------|----------|
| SRTM 1 Arc-Second | ~30m | Global (56S-60N) [^121^] |
| SRTM 3 Arc-Second | ~90m | Global [^120^] |
| NASA ASTER GDEM | ~30m | Global (83N-83S) [^117^] |

### URLs
- **NASA Earthdata**: https://www.earthdata.nasa.gov/topics/land-surface/digital-elevation-terrain-model-dem [^117^]
- **USGS EarthExplorer**: https://earthexplorer.usgs.gov/ [^127^]
- **CGIAR SRTM 90m**: https://csidotinfo.wordpress.com/data/srtm-90m-digital-elevation-database-v4-1/ [^120^]

---

## 8. USGS 3DEP (3D Elevation Program)

### Overview
The USGS 3D Elevation Program is a **nationwide initiative to collect high-resolution (1m) LiDAR-based DEM** for the United States. The gold standard for US terrain data. [^115^]

### Key Features
- **1-meter resolution** LiDAR-derived DEMs for the entire US [^115^]
- **Point cloud data** available in .LAZ format, classified (ground, vegetation, buildings, water) [^115^]
- **Multiple visualizations**: Hillshade, slope, aspect, elevation-tinted [^115^]
- **Web services**: WMS available for direct integration into tools like Cesium [^115^]
- **50% cost-match** available for new LiDAR collections [^115^]

### License & Cost
| Aspect | Details |
|--------|---------|
| **License** | Public domain (US Government work) |
| **Cost** | **FREE** |
| **Access** | The National Map Downloader, OpenTopography |
| **Restrictions** | US only |

### UE5 Integration Difficulty
- **Medium**: Similar to SRTM but higher resolution requires more processing
- **Best workflow**: Download GeoTIFF DEM -> convert to heightmap -> UE5 Landscape
- **Advanced**: Download LiDAR point clouds (.LAZ) -> convert to mesh for detailed areas
- **Cesium integration**: USGS 3DEP data viewable in Cesium via Entwine Point Tiles [^115^]

### Coverage & Resolution
| Metric | Value |
|--------|-------|
| **Coverage** | United States (continental + Alaska, Hawaii, territories) |
| **Resolution** | 1-meter (DEM), sub-meter (source LiDAR) [^115^] |
| **Accuracy** | Decimeter vertical accuracy |
| **Availability** | ~90%+ of US covered, ongoing collection |

### URLs
- **Wiki**: https://wiki.openstreetmap.org/wiki/USGS_3D_Elevation_Program [^115^]
- **USGS 3DEP Explorer**: https://apps.nationalmap.gov/3depdem/
- **OpenTopography**: https://opentopography.org/ (LiDAR point cloud access) [^146^]

### Use for MEOK EARTH
**Best-in-class terrain data for the United States**. If MEOK EARTH targets US markets, 3DEP provides the highest quality free terrain available globally.

---

## 9. Copernicus DEM (European Space Agency)

### Overview
The Copernicus DEM is a **global Digital Surface Model** derived from the TanDEM-X radar satellite mission, provided free by the European Space Agency. Superior to SRTM in many regions. [^178^]

### Key Features
- **Three instances**: GLO-30 (global, 30m), GLO-90 (global, 90m), EEA-10 (Europe, 10m) [^178^]
- **Radar-based** (not optical) - works through clouds [^178^]
- **Includes buildings and vegetation** (DSM, not bare-earth DTM) [^178^]
- **Available as Cloud Optimized GeoTIFFs** via OpenTopography API [^175^]
- **Free license** for GLO-30 and GLO-90 worldwide [^178^]

### License & Cost
| Product | Resolution | Cost | Coverage |
|---------|-----------|------|----------|
| **GLO-90** | 90m | **FREE** | Global [^178^] |
| **GLO-30** | 30m | **FREE** | Global (minor gaps in some countries) [^178^] |
| **EEA-10** | 10m | Restricted | 39 European countries [^178^] |
| **License** | | Copernicus open license | |

### UE5 Integration
- Same workflow as SRTM: Download GeoTIFF -> convert to heightmap -> UE5 Landscape
- OpenTopography provides API for subsetting: no need to download full tiles [^175^]
- Higher quality than SRTM for most regions

### URLs
- **OpenTopography**: https://portal.opentopography.org/datasetMetadata?otCollectionID=OT.032021.4326.1 [^180^]
- **ESA Copernicus**: https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM [^178^]
- **EU GISCO**: https://ec.europa.eu/eurostat/web/gisco/geodata/digital-elevation-model/copernicus [^177^]

---

## 10. CityJSON / 3DCityDB Digital Twin Platform

### Overview
CityJSON and 3DCityDB are **open-source standards and tools** for storing, managing, and visualizing large-scale semantic 3D city models - essentially creating digital twins of cities. [^208^] [^114^]

### CityJSON
- **JSON-based encoding** for 3D city models (OGC standard) [^208^]
- **~7x more compact** than CityGML-XML [^208^]
- **Bidirectional conversion** with CityGML via citygml-tools [^208^]
- **Web viewer** (ninja) - drag-and-drop visualization [^208^]
- **Multiple tools**: QGIS plugin, Blender plugin, cjio CLI [^210^]

### 3DCityDB
- **Open-source geodatabase** for storing semantic 3D city models [^116^]
- **Used by**: Berlin, New York, Rotterdam, Zurich, Singapore, Munich, London [^116^]
- **Supports**: PostgreSQL/PostGIS, Oracle [^114^]
- **Exports to**: CityGML, KML, COLLADA, glTF, 3D Tiles [^114^]
- **Version 5.0** released March 2025 with major improvements [^116^]

### License & Cost
| Component | License | Cost |
|-----------|---------|------|
| **CityJSON** | OGC Standard (open) | **FREE** [^208^] |
| **3DCityDB** | Open source | **FREE** [^116^] |
| **citygml-tools** | Open source | **FREE** [^210^] |
| **cjio** | Open source | **FREE** [^210^] |
| **ninja viewer** | Open source | **FREE** [^210^] |

### UE5 Integration Difficulty
- **Hard**: No direct UE5 plugin
- **Workflow**: 3DCityDB -> export to 3D Tiles/glTF -> import to UE5 via Cesium or Datasmith
- **Cesium integration**: 3DCityDB exports directly to 3D Tiles, which Cesium for Unreal can stream [^116^]
- **Best for**: City-scale digital twins with semantic building data

### Coverage & Resolution
| Metric | Value |
|--------|-------|
| **Data availability** | Depends on city (many European cities have full CityGML/CityJSON datasets) |
| **Building detail** | LoD1-LoD4 (from simple extruded footprints to detailed architectural models) [^212^] |
| **Semantic data** | Building function, materials, roof types, energy properties [^119^] |

### URLs
- **CityJSON**: https://www.cityjson.org/ [^208^]
- **3DCityDB**: https://www.3dcitydb.org/ [^116^]
- **3DCityDB v5 Announcement**: https://www.ed.tum.de/en/ed/news-single-view-start/article/release-of-3d-city-database-v5/ [^116^]
- **Software list**: https://www.cityjson.org/software/ [^210^]

### Use for MEOK EARTH
Best suited for **cities with existing 3D city models** (mainly Europe). Can provide semantically rich building data. For cities without existing datasets, creating CityJSON from scratch is labor-intensive.

---

## 11. Azure Digital Twins

### Overview
Microsoft's cloud-based digital twin platform for modeling environments, assets, and relationships using a **graph-based approach**. Best for IoT-connected smart building/city scenarios. [^150^] [^151^]

### Key Features
- **Graph-based twin modeling**: Assets, spaces, and relationships [^150^]
- **Real-time event ingestion**: Via Azure IoT Hub, Event Hubs [^150^]
- **Query engine**: Query across twin graphs for impact analysis [^150^]
- **3D visualization**: Via partner integrations (not native high-fidelity 3D) [^150^]
- **Azure ecosystem**: Integrates with analytics, AI, and automation pipelines [^150^]

### License & Cost
| Component | Pricing |
|-----------|---------|
| **Messages** | $1 per million messages [^155^] |
| **Operations** | $2.50 per million operations [^155^] |
| **Query units** | $0.50 per million query units [^155^] |
| **Storage** | ~$0.10 per GB/month [^151^] |
| **Data transfer** | ~$0.01 per GB [^151^] |

> Pay-as-you-go consumption model. Free tier available for exploration. [^155^]

### UE5 Integration Difficulty
- **Very Hard**: No direct UE5 integration
- **Architecture**: Azure Digital Twins provides the data/backend layer; a custom UE5 plugin would need to be built to query the REST API and visualize twins
- **Best for**: IoT-connected building monitoring, not game environments

### Coverage & Resolution
| Metric | Value |
|--------|-------|
| **Deployment** | Cloud (Azure) only |
| **3D capability** | Requires additional visualization tools |
| **Best for** | Smart buildings, campuses, industrial environments [^150^] |

### URLs
- **Azure Pricing**: https://azure.microsoft.com/en-us/pricing/details/digital-twins/ [^155^]
- **Docs**: https://learn.microsoft.com/azure/digital-twins/

### Verdict for MEOK EARTH
**Overkill for game overlay purposes**. Azure Digital Twins is designed for operational IoT monitoring, not real-time 3D game worlds. Consider only if MEOK EARTH needs live IoT sensor integration.

---

## 12. AWS IoT TwinMaker

### Overview
Amazon's digital twin service for creating operational twins across multiple data sources. Composable twin views with Grafana integration. [^150^] [^152^]

### Key Features
- **Composable twin views** across multiple data sources [^150^]
- **Grafana plugin** for visualization [^159^]
- **Integration with AWS IoT Core**, SiteWise, and other AWS services
- **Knowledge graph** for modeling relationships between entities
- **3D scene composition** (basic, not game-engine quality)

### License & Cost
| Component | Pricing |
|-----------|---------|
| **IoT TwinMaker operations** | $1.65 per million operations [^152^] |
| **IoT Core messages** | $1.20 per million messages (first tier) [^152^] |
| **Lambda functions** | $0.20 per million requests [^152^] |

### UE5 Integration Difficulty
- **Very Hard**: No UE5 integration; primarily Grafana-based visualization
- **Best for**: Industrial operations dashboards, not game environments

### URLs
- **AWS Docs**: https://aws.amazon.com/iot-twinmaker/

### Verdict for MEOK EARTH
Similar to Azure Digital Twins - designed for industrial IoT, not game worlds. Not recommended unless live sensor data is a core requirement.

---

## 13. OpenTopography LiDAR Portal

### Overview
OpenTopography is an **NSF-funded portal** providing free access to high-resolution topographic data including LiDAR point clouds, DEMs, and photogrammetric datasets. The largest community-accessible portal for LiDAR topography. [^146^] [^149^]

### Key Features
- **High-resolution LiDAR point clouds** (sub-meter to 2m) [^146^]
- **Cloud-based processing**: Generate custom DEMs without downloading raw data [^146^]
- **Data sources**: USGS 3DEP, NOAA Coastal LiDAR, Natural Resources Canada, international datasets [^149^]
- **Entwine Point Tiles (EPT)**: Stream massive point clouds to Cesium/web viewers [^115^]
- **On-demand products**: Hillshade, slope, aspect, hydrological derivatives [^146^]

### License & Cost
| Aspect | Details |
|--------|---------|
| **Academic users** | **FREE** (including USGS 3DEP, NOAA data) |
| **OT+ subscription** | Required for some commercial/international datasets |
| **API keys** | Free for personal use; enterprise keys available [^175^] |
| **Data license** | Varies by dataset (most are open) |

### UE5 Integration Difficulty
- **Medium-Hard**: LiDAR point clouds require conversion
- **Workflow**: (1) Query OpenTopography for area, (2) Download point cloud or DEM, (3) Convert to heightmap or mesh, (4) Import to UE5
- **Cesium integration**: Can view LiDAR in Cesium via Entwine Point Tiles [^115^]
- **USGS 3DEP data**: Best accessed directly via USGS for non-academic users

### Coverage & Resolution
| Data Type | Resolution | Coverage |
|-----------|-----------|----------|
| **USGS 3DEP LiDAR** | 0.5-2m point density | United States [^146^] |
| **NOAA Coastal LiDAR** | Sub-meter | US coastal areas [^149^] |
| **Canada HRDEM** | 1m | Southern Canada [^150^] |
| **New Zealand LINZ** | Sub-meter | New Zealand [^150^] |
| **Global DEMs** | 30-90m | Worldwide (SRTM, Copernicus) [^146^] |

### URLs
- **Portal**: https://opentopography.org/ [^149^]
- **Data catalog**: https://opentopography.org/data [^149^]
- **API docs**: https://portal.opentopography.org/apidocs/ [^175^]

### Use for MEOK EARTH
**Essential for high-resolution terrain** in areas with LiDAR coverage. The cloud-based processing eliminates the need for local GIS software for basic DEM generation.

---

## 14. Landscape Combinator (UE5 Plugin)

### Overview
An **open-source UE5 plugin** that creates real-world landscapes from heightmap and OSM data directly within the Unreal Editor. Specifically designed for the exact use case MEOK EARTH needs. [^213^]

### Key Features
- **Real-world heightmap import**: Creates UE5 Landscapes from real elevation data [^213^]
- **OSM spline generation**: Creates landscape splines for roads, paths from OSM [^213^]
- **Procedural foliage placement**: Spawns vegetation based on OSM landuse data (via PCG) [^213^]
- **Water body support**: Lakes, rivers from OSM (partial) [^213^]
- **Direct data fetching**: Pulls from online sources within UE5 editor

### License & Cost
| Aspect | Details |
|--------|---------|
| **Personal use** | **FREE** (GitHub) |
| **Commercial use** | ~100 EUR (planned Marketplace price) [^213^] |
| **License** | Open source |
| **GitHub**: | https://github.com/LandscapeCombinator/LandscapeCombinator [^213^] |

### UE5 Integration Difficulty
- **Easy**: Native UE5 plugin, installs to project
- **Steps**: (1) Clone/download from GitHub, (2) Add to Plugins folder, (3) Enable in Editor, (4) Use built-in tools to select area and import
- **Setup time**: 15-30 minutes

### Coverage & Resolution
| Metric | Value |
|--------|-------|
| **Terrain source** | Multiple online sources (depends on availability) |
| **OSM data** | Global (building footprints, roads, vegetation) |
| **Terrain resolution** | Depends on source (typically 30m-90m for free global data) |

### URL
- **GitHub**: https://github.com/LandscapeCombinator/LandscapeCombinator [^213^]
- **Forum announcement**: https://forums.unrealengine.com/t/plugin-landscape-combinator/772305 [^213^]

### Why It's Important for MEOK EARTH
Landscape Combinator is the **only UE5-native tool** designed specifically for creating real-world landscapes with OSM integration. It bridges the gap between GIS data and UE5 Landscape system without requiring external tools like QGIS or Blender.

---

## 15. ArcGIS Maps SDK for Unreal Engine

### Overview
Esri's official SDK for bringing ArcGIS geospatial data (maps, 3D scenes, feature layers) into Unreal Engine. Provides a comprehensive GIS integration. [^157^]

### Key Features
- **3D Object Scene Layers**: High-detail 3D buildings from ArcGIS Online [^157^]
- **Feature layers**: Query and display geographic features [^157^]
- **Geocoding**: Address search and reverse geocoding [^157^]
- **Routing**: Pathfinding between points [^157^]
- **Real-time data**: Stream layer support for live updates [^157^]
- **XR support**: VR and AR sample projects included [^157^]

### License & Cost
| Aspect | Details |
|--------|---------|
| **SDK** | Free to download |
| **ArcGIS Online** | Requires subscription (developer account available) |
| **Data usage** | Billed through ArcGIS Online credits |

### UE5 Integration Difficulty
- **Medium**: Requires ArcGIS Online account and understanding of Esri ecosystem
- **Setup**: Install SDK, configure ArcGIS Online access, add map/scene to level
- **UE5 version**: Requires UE 5.5+ for XR samples [^157^]

### Coverage & Resolution
| Metric | Value |
|--------|-------|
| **Map coverage** | Global (via ArcGIS Online) |
| **3D buildings** | Available for many cities through ArcGIS Living Atlas |
| **Data quality** | Varies by region; best in US/Europe |

### URLs
- **GitHub Samples**: https://github.com/Esri/arcgis-maps-sdk-unreal-engine-samples [^157^]
- **Esri**: https://developers.arcgis.com/unreal-engine/

### Use for MEOK EARTH
Good alternative to Cesium if already invested in Esri ecosystem. Cesium has broader 3D globe support and better open-source ecosystem for game development.

---

## 16. NVIDIA Omniverse

### Overview
NVIDIA's real-time 3D design collaboration platform built on OpenUSD. Enables high-fidelity digital twins with physics simulation and multi-user collaboration. [^152^] [^160^]

### Key Features
- **OpenUSD-based**: Universal Scene Description for 3D data exchange [^160^]
- **Cesium integration**: Cesium for Omniverse plugin available [^95^]
- **High-fidelity rendering**: GPU-accelerated ray tracing [^153^]
- **Digital twin workflows**: Spatial streaming to Apple Vision Pro, GDN [^153^]
- **300,000+ users** across industrial and design applications [^160^]

### License & Cost
- **Free for individual use** (Omniverse platform)
- **Enterprise licensing** for teams and commercial deployment
- **Requires NVIDIA GPU**

### UE5 Integration Difficulty
- **Very Hard**: Not directly compatible with UE5
- **Approach**: Omniverse is a separate runtime; could be used for asset preparation/preview
- **Cesium for Omniverse** streams geospatial data, but into Omniverse, not UE5 [^95^]

### URL
- **NVIDIA Omniverse**: https://www.nvidia.com/en-us/omniverse/ [^152^]

### Verdict for MEOK EARTH
Not directly applicable since MEOK EARTH uses UE5. Consider only if asset pipeline needs USD-based collaboration.

---

## 17. Additional Tools & Workflows

### 17.1 TerrainMagic (UE5 Plugin)
- Commercial plugin for importing real-world terrain into UE5 in seconds
- Search by lat/long, one-click import
- Supports mixing multiple terrain areas
- **Cost**: Paid (Marketplace)
- **Tutorial**: https://dev.epicgames.com/community/learning/tutorials/m2Vb/ [^156^]

### 17.2 TerraForm Pro
- Professional terrain import plugin for UE
- Imports GeoTIFF heightmaps and shapefiles as splines
- **Status**: Commercial plugin for earlier UE versions [^217^]

### 17.3 World Machine / Gaea
- **World Machine**: Professional terrain generation software, exports to UE5 heightmaps [^154^]
- **Gaea**: Modern procedural terrain tool with real-world data import [^153^]
- **Workflow**: Real-world heightmap -> World Machine/Gaea (detail enhancement) -> UE5

### 17.4 terrain.party
- Simple web tool for downloading real-world heightmaps
- Enter location, select area, download PNG heightmap
- **Free** and easy to use [^157^]

### 17.5 QGIS (Free GIS Software)
- Essential tool for processing geospatial data
- Convert between formats (GeoTIFF -> PNG heightmap)
- Clip, reproject, and analyze terrain data
- **Free, open source**

### 17.6 GDAL/OGR
- Command-line tools for geospatial data conversion
- Automate heightmap processing pipelines
- **Free, open source**

---

## 18. Comprehensive Comparison Matrix

| Technology | Type | Cost | UE5 Integration | Global Coverage | Resolution | Best For |
|------------|------|------|-----------------|-----------------|------------|----------|
| **Cesium for Unreal** | 3D Globe Plugin | FREE (Apache 2.0) | **Easy** (Marketplace) | Global | Variable | **Foundation layer** |
| **Google 3D Tiles** | Photogrammetric 3D | $6/CPM (free $200 credit) | **Easy** (via Cesium) | ~2,500 cities | ~7.5cm | **Photorealistic cities** |
| **Mapbox** | Maps API | Freemium | Hard (no UE5 SDK) | Global | Variable | Web/mobile maps |
| **OSM + OSM2World** | 3D Buildings | FREE (ODbL) | Medium (Blender bridge) | Global (footprints) | ~3% have height | **Free building data** |
| **Blosm** | Blender OSM addon | FREE / ~EUR 100 Pro | Medium (Blender->UE5) | Global | 30m terrain | **Blender workflow** |
| **Mapillary** | Street imagery | FREE (CC BY-SA) | Hard (manual) | 190+ countries | Varies | **Texture reference** |
| **NASA SRTM** | Terrain DEM | FREE | Medium (heightmap conv.) | ~80% of Earth | 30m | **Free global terrain** |
| **USGS 3DEP** | LiDAR DEM | FREE | Medium | United States | 1m | **US high-res terrain** |
| **Copernicus DEM** | Radar DSM | FREE | Medium | Global | 30m (10m EU) | **Free global terrain v2** |
| **CityJSON/3DCityDB** | 3D City DB | FREE | Hard (via 3D Tiles) | City-dependent | LoD1-LoD4 | **Semantic city models** |
| **Azure Digital Twins** | Cloud IoT | Pay-per-use | Very Hard | Cloud | N/A | **IoT integration** |
| **AWS IoT TwinMaker** | Cloud IoT | Pay-per-use | Very Hard | Cloud | N/A | **IoT integration** |
| **OpenTopography** | LiDAR Portal | FREE (academic) | Medium-Hard | Varies | 0.5-2m LiDAR | **High-res LiDAR** |
| **Landscape Combinator** | UE5 Plugin | FREE (personal) | **Easy** (native UE5) | Global (via OSM) | 30m terrain | **UE5 real-world landscapes** |
| **ArcGIS Maps SDK** | GIS SDK | Free (w/ subscription) | Medium | Global | Variable | **Enterprise GIS** |
| **NVIDIA Omniverse** | 3D Platform | Free (individual) | N/A (separate runtime) | Via Cesium | Varies | **Design collaboration** |

---

## 19. Recommendations for MEOK EARTH

### Tier 1: Core Stack (Required)

| Component | Technology | Why |
|-----------|-----------|-----|
| **3D Globe Engine** | Cesium for Unreal | Free, open-source, full WGS84 globe, streaming, UE5 native |
| **Global Terrain** | Cesium World Terrain (ion) or Copernicus DEM | Ready-to-stream via Cesium; alternatively import DEMs as Landscapes |
| **Global Buildings** | Cesium OSM Buildings | Free, global coverage via Cesium ion |
| **UE5 Landscape Gen** | Landscape Combinator | Native UE5, OSM integration, free for personal use |

### Tier 2: Enhanced Visual Quality (Recommended)

| Component | Technology | When to Use |
|-----------|-----------|-------------|
| **Photorealistic Cities** | Google Photorealistic 3D Tiles | Where available and budget allows (~$6/CPM) |
| **High-Res US Terrain** | USGS 3DEP 1m DEM | For US gameplay areas |
| **3D Building Models** | Blosm (Blender) -> UE5 | For custom areas with good OSM height data |
| **Street Textures** | Mapillary API | For texturing key building facades |

### Tier 3: Advanced Features (Future)

| Component | Technology | Use Case |
|-----------|-----------|----------|
| **Semantic City Models** | CityJSON/3DCityDB | Cities with rich 3D city model data |
| **Live IoT Data** | Azure Digital Twins | If integrating real-world sensor data |
| **LiDAR Detail** | OpenTopography | Sub-meter terrain for special areas |

### Implementation Roadmap

```
Phase 1 (MVP):
  - Install Cesium for Unreal
  - Set up Cesium ion (Community tier)
  - Add Cesium World Terrain + Cesium OSM Buildings
  - Test gameplay at key locations

Phase 2 (Enhanced):
  - Add Google Photorealistic 3D Tiles for major cities
  - Integrate Landscape Combinator for custom terrain areas
  - Set up heightmap pipeline for high-res regions (US 3DEP, Copernicus)

Phase 3 (Polish):
  - Blosm pipeline for detailed OSM building imports
  - Mapillary texture integration for key facades
  - Custom 3D building submissions from players
```

### Cost Estimate (At Scale)

| Scale | Cesium ion | Google 3D Tiles | Total/Month |
|-------|-----------|-----------------|-------------|
| Development | FREE (Community) | FREE ($200 credit) | ~$0 |
| Small (10K MAU) | $149 (Commercial) | FREE (within credit) | ~$149 |
| Medium (100K MAU) | $499 (Premium) | ~$400 | ~$899 |
| Large (1M MAU) | Custom | ~$4,000+ | $5,000+ |

### Critical Risks

1. **Google 3D Tiles EU/EEA restriction** [^154^] - European players may not have access to Google's photorealistic tiles. Mitigation: Use Cesium OSM Buildings + Copernicus DEM for Europe.

2. **No global photogrammetric 3D coverage** - Only ~2,500 cities have Google's 3D tiles. Mitigation: OSM extruded buildings fill gaps.

3. **OSM building height sparsity** - Only 3% have height data. Mitigation: Estimate heights from `building:levels` tag (3.5% coverage) or apply default heights by building type.

4. **Google cost unpredictability** - No hard spending caps. Mitigation: Implement session pooling, caching, and monitor usage alerts closely.

5. **Terrain editing limitations in Cesium** - Cannot directly edit Cesium terrain in UE5 Landscape tools. Mitigation: Use composite terrain approach (custom GeoTIFFs overlaid on Cesium World Terrain) [^123^].

---

## Reference URLs Summary

| Technology | Primary URL |
|------------|-------------|
| Cesium for Unreal | https://cesium.com/platform/cesium-for-unreal/ [^99^] |
| Cesium for Unreal GitHub | https://github.com/CesiumGS/cesium-unreal [^97^] |
| Cesium ion Pricing | https://cesium.com/platform/cesium-ion/pricing/ [^185^] |
| Google Photorealistic 3D Tiles | https://cesium.com/learn/unreal/unreal-photorealistic-3d-tiles/ [^181^] |
| Google Maps Tiles API Pricing | https://developers.google.com/maps/documentation/tile/usage-and-billing |
| Mapbox Pricing | https://www.mapbox.com/pricing [^155^] |
| OpenStreetMap | https://www.openstreetmap.org/ |
| OSM2World | https://osm2world.org/ [^125^] |
| Blosm (Blender-OSM) | https://github.com/vvoovv/blosm [^161^] |
| Mapillary | https://www.mapillary.com/ [^103^] |
| NASA SRTM | https://www.earthdata.nasa.gov/ [^117^] |
| USGS 3DEP | https://apps.nationalmap.gov/3depdem/ |
| OpenTopography | https://opentopography.org/ [^149^] |
| Copernicus DEM | https://dataspace.copernicus.eu/ [^178^] |
| CityJSON | https://www.cityjson.org/ [^208^] |
| 3DCityDB | https://www.3dcitydb.org/ [^116^] |
| Azure Digital Twins | https://azure.microsoft.com/services/digital-twins/ |
| AWS IoT TwinMaker | https://aws.amazon.com/iot-twinmaker/ |
| Landscape Combinator | https://github.com/LandscapeCombinator/LandscapeCombinator [^213^] |
| ArcGIS Maps SDK | https://developers.arcgis.com/unreal-engine/ |
| Overpass API | https://wiki.openstreetmap.org/wiki/Overpass_API [^221^] |
| NVIDIA Omniverse | https://www.nvidia.com/omniverse/ |

---

*Research compiled from 15+ targeted web searches across geospatial technology, game engine integration, and digital twin platforms. All citations marked with [^N^] reference the search result index from the research process.*
