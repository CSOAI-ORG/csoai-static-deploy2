# MEOK SPACE: Open Source Space Simulation Tools Research

> **Research Date**: 2025-07-24
> **Focus**: Open source tools and data sources for Mars, Moon, planets, and procedural space exploration with UE5 integration paths
> **Total Sources**: 20+ categories, 50+ tools/data sources

---

## Table of Contents

1. [NASA Moon Terrain Data (LRO LOLA)](#1-nasa-moon-terrain-data-lro-lola)
2. [NASA Mars Terrain Data (MOLA)](#2-nasa-mars-terrain-data-mola)
3. [NASA Horizons API - Celestial Body Positions](#3-nasa-horizons-api)
4. [NASA 3D Resources](#4-nasa-3d-resources)
5. [ESA Gaia Data - 1.8 Billion Stars](#5-esa-gaia-data)
6. [Procedural Planet Generation (Open Source)](#6-procedural-planet-generation)
7. [Space Engine](#7-space-engine)
8. [Universe Sandbox](#8-universe-sandbox)
9. [Outerra Engine](#9-outerra-engine)
10. [Kerbal Space Program Modding](#10-kerbal-space-program-modding)
11. [Celestia](#11-celestia)
12. [Stellarium](#12-stellarium)
13. [NASA Exoplanet Archive API](#13-nasa-exoplanet-archive-api)
14. [OpenSpace Project](#14-openspace-project)
15. [UE5 Space Environment/Assets](#15-ue5-space-environment)
16. [Planetary Terrain Generation for UE5](#16-planetary-terrain-for-ue5)
17. [Star Field / Galaxy Procedural Generation](#17-star-field-galaxy-generation)
18. [Space Weather Data APIs](#18-space-weather-apis)
19. [Satellite Tracking Data (NORAD TLE)](#19-satellite-tracking-data)
20. [Additional Space Simulation Tools](#20-additional-tools)
21. [NASA SPICE Toolkit](#21-nasa-spice-toolkit)
22. [Summary Matrix](#22-summary-matrix)

---

## 1. NASA Moon Terrain Data (LRO LOLA)

### Overview
The Lunar Reconnaissance Orbiter (LRO) Lunar Orbiter Laser Altimeter (LOLA) provides the highest resolution topographic data for the Moon.

### Data Sources
| Source | URL | Format | Resolution |
|--------|-----|--------|------------|
| **PDS Geosciences Node - LRO** | https://pds-geosciences.wustl.edu/missions/lro/ | IMG, TIFF, CUB | Up to 118m/pixel |
| **Lunar Orbital Data Explorer** | https://ode.rsl.wustl.edu/moon/index.aspx | Various | Searchable by region |
| **USGS Astrogeology - Moon** | https://astrogeology.usgs.gov/search/map/moon | GeoTIFF, CUB | Multiple resolutions |
| **NASA Moon Trek** | https://trek.nasa.gov/moon/ | WMTS, GeoTIFF | Interactive export |

### Data Formats
- **IMG**: Raw binary image data with .lbl label files (metadata)
- **TIFF/GeoTIFF**: Standard georeferenced imagery
- **CUB**: ISIS cube format (USGS planetary image format)
- **PNG/JPEG**: Processed visual products
- **Heightmaps**: 16-bit signed elevation data

### UE5 Integration Path
1. Download LOLA terrain data as GeoTIFF or PNG heightmaps
2. Use GDAL or Photoshop to convert to 16-bit heightmap
3. Import into UE5 Landscape system (UE5 supports 16-bit RAW/PNG heightmaps natively)
4. Scale appropriately: Moon radius = 1,737 km (use World Partition for large worlds)
5. Use UE5's `World Partition` with `Level Instancing` for massive lunar surfaces
6. Apply LOLA color maps as landscape layers

### License
- **Public Domain** (NASA planetary data is freely available)
- Citation recommended when publishing [^360^] [^370^] [^421^]

---

## 2. NASA Mars Terrain Data (MOLA)

### Overview
The Mars Orbiter Laser Altimeter (MOLA) aboard Mars Global Surveyor provides the primary global topographic dataset for Mars.

### Data Sources
| Source | URL | Format | Resolution |
|--------|-----|--------|------------|
| **PDS MOLA MEGDR** | https://pds-geosciences.wustl.edu/missions/mgs/mola.html | IMG + .lbl | 128 ppd (~463m) |
| **Mars Global Data Sets (ASU)** | https://www.mars.asu.edu/data/ | PNG tiles | 128 ppd/460m |
| **Mars Orbital Data Explorer** | http://ode.rsl.wustl.edu/mars/index.aspx | Various | Searchable |
| **NASA PGDA Whole Catalog** | https://pgda.gsfc.nasa.gov/products/62 | GMT, Binary | 4/16/64/128 ppd |
| **USGS MOLA Global DEM** | https://astrogeology.usgs.gov | CUB, GeoTIFF | 463m global mosaic |
| **NASA Mars Trek** | https://trek.nasa.gov/mars/ | WMTS, GeoTIFF | Interactive |
| **GMT Mars Relief** | https://www.generic-mapping-tools.org/remote-datasets/mars-relief.html | NetCDF | 200m (blended) |

### Key Specifications
- **Highest Resolution**: 128 pixels per degree = ~463m per pixel
- **Format**: Binary .img files with metadata .lbl files
- **Grid**: 16 tiles of 30x30 degrees each
- **Rows/Columns**: 5,632 rows x 23,040 columns per tile
- **Bit Depth**: 16-bit signed
- **Coverage**: 88N to 88S (polar gaps)
- **Elevation Range**: -8,200m (Hellas Basin) to +21,300m (Olympus Mons) [^136^] [^137^] [^139^]

### MOLA Data Processing Pipeline
1. Download .img and .lbl files from PDS
2. Read .lbl for metadata (rows, columns, bit depth)
3. Import raw binary into ImageJ/GIMP/Photoshop (16-bit signed)
4. Export as PNG heightmap
5. Import into UE5 Landscape or mesh generation system

### UE5 Integration Path
- Use `Landscape` system with heightmap import
- Mars radius = 3,389.5 km (scale accordingly)
- Use `Virtual Heightfield Mesh` for high-detail local terrain
- Apply MOLA colorized elevation maps as albedo
- Consider `World Partition` with streaming for full-planet coverage [^143^] [^145^]

### License
- **Public Domain** (NASA planetary science data)

---

## 3. NASA Horizons API

### Overview
JPL Horizons provides highly accurate ephemeris (position/velocity) data for solar system bodies, spacecraft, and small bodies.

### API Details
| Feature | Value |
|---------|-------|
| **Base URL** | https://ssd.jpl.nasa.gov/horizons/app.html#/ |
| **REST API** | https://ssd-api.jpl.nasa.gov/doc/horizons.html |
| **Data Types** | Position vectors, orbital elements, observer tables |
| **Coverage** | Solar system bodies, spacecraft, asteroids, comets |
| **Time Span** | 9999 BC to 9999 AD |

### Alternative Interfaces
- **Web Interface**: https://ssd.jpl.nasa.gov/horizons/app.html#/
- **Telnet**: ssd.jpl.nasa.gov hor 6775
- **Email**: horizons@ssd.jpl.nasa.gov
- **SPICE Kernels**: https://naif.jpl.nasa.gov/pub/naif/ (local computation) [^133^] [^399^]

### Access Methods
```python
# Using astroquery
from astroquery.jplhorizons import Horizons
obj = Horizons(id='Mars', location='@Earth', epochs={'start':'2025-01-01', 'stop':'2025-01-02', 'step':'1d'})
eph = obj.ephemerides()
```

### Data Formats
- JSON (via REST API)
- Text tables (via web/email)
- SPICE binary kernels (.bsp) for local use

### UE5 Integration Path
1. Query Horizons API for body positions at runtime or build-time
2. Parse JSON response for state vectors (x, y, z, vx, vy, vz)
3. Convert from AU/km to UE5 units
4. Use to position celestial bodies in UE5 scene
5. Cache results for offline use

### License
- **Public Domain** (NASA/JPL data)

---

## 4. NASA 3D Resources

### Overview
NASA provides 300+ free 3D models of spacecraft, planets, moons, asteroids, and equipment.

### Data Sources
| Source | URL | Count | Formats |
|--------|-----|-------|---------|
| **NASA 3D Resources (Official)** | https://nasa3d.arc.nasa.gov | 300+ | OBJ, STL, FBX, BLEND, 3DS |
| **NASA 3D Models (Printables)** | https://www.printables.com/tag/nasa | Many | STL (3D print ready) |
| **NASA Data.gov - Satellite Kit** | https://catalog.data.gov/dataset/nasa-3d-models-satellite-kit | Parts kit | ZIP/BIN |
| **Free3D NASA Models** | https://free3d.com/3d-models/nasa | 8 free | .blend, .obj, .c4d, .3ds |

### Available Models
- Spacecraft: ISS, Voyager, Cassini, Juno, New Horizons, Curiosity, Perseverance
- Launch Vehicles: Saturn V, Space Shuttle, SLS, Falcon 9, Starship
- Planets/Moons: Earth, Moon, Mars (with textures)
- Satellites: Various communication and science satellites
- 3D Printable: Satellite kit, rover parts [^132^] [^135^] [^138^] [^140^]

### UE5 Integration Path
- Models available in OBJ/FBX format import directly into UE5
- Use NASA textures (where provided) as base color maps
- Scale models appropriately using real-world dimensions
- Combine with terrain data for planetary surfaces

### License
- **Public Domain** (US Government work) - "files are provided without copyright" [^138^]

---

## 5. ESA Gaia Data - 1.8 Billion Stars

### Overview
The Gaia mission provides the most comprehensive star catalog ever produced with positions, parallaxes, proper motions, photometry, and radial velocities for over 1.8 billion stars.

### Data Sources
| Source | URL | Size | Stars |
|--------|-----|------|-------|
| **ESA Gaia Archive** | https://gea.esac.esa.int/archive/ | ~2 TB | 1.8 billion |
| **Gaia DR3** | https://www.cosmos.esa.int/web/gaia/dr3 | 2 TB full | 1.806 billion |
| **Gaia Sky (Visualizer)** | https://gaiasky.space/ | N/A | Full catalog |
| **CDS Strasbourg** | http://cds.unistra.fr/gaia | Subsets | Various |
| **TAP+ API** | https://gea.esac.esa.int/archive/ | Query-based | Subsets |

### Data Access
```python
# Using astroquery
from astroquery.gaia import Gaia
job = Gaia.launch_job("SELECT TOP 100 ra, dec, parallax, pmra, pmdec "
                      "FROM gaiadr3.gaia_source WHERE parallax > 10")
results = job.get_results()
```

### Data Products
- **DR3**: Full astrometry, photometry, radial velocities, spectra
- **Gaia EDR3**: Positions, parallaxes, proper motions, G-band photometry
- **Gaia DR3 Spectrograph**: ~220 million BP/RP mean spectra
- **Gaia Archive**: TAP+ (Table Access Protocol+) for SQL-like queries [^131^] [^134^] [^141^] [^144^]

### Data Formats
- **VOTable**: Standard astronomical table format
- **CSV/TSV**: Tabular text formats
- **FITS**: Standard astronomical data format
- **Binary**: Optimized binary formats for large datasets

### UE5 Integration Path
1. Query Gaia archive for stars in your field of view (cone search)
2. Download RA, Dec, distance (from parallax), magnitude, color
3. Convert spherical to Cartesian coordinates
4. Generate point cloud or instanced mesh in UE5
5. Use magnitude for brightness/color temperature for star color
6. Use `Niagara` particle system for rendering star fields
7. For Gaia Sky integration: It is open source - study its MS-LOD rendering technique

### License
- ESA Gaia data: free for scientific and educational use with proper citation

---

## 6. Procedural Planet Generation (Open Source)

### Key Projects

| Project | Language | License | URL | Notes |
|---------|----------|---------|-----|-------|
| **SebLague/Procedural-Planets** | C# (Unity) | MIT | https://github.com/SebLague/Procedural-Planets | Most influential tutorial series |
| **SebLague/Solar-System** | C# (Unity) | MIT | https://github.com/SebLague/Solar-System | Solar system with atmospheres |
| **Planet-Generator (Godot)** | GDScript | MIT | https://github.com/Hoimar/Planet-Generator | Godot addon with LOD |
| **ProceduralPlanetGodot** | GDScript | MIT | https://github.com/athillion/ProceduralPlanetGodot | Godot 4 port |
| **PlanetTechJS** | JavaScript | Open | https://github.com/topics/procedural-terrain | Three.js planet library |
| **mapgen4** | TypeScript | MIT | https://github.com/redblobgames/mapgen4 | Wilderness map generator |
| **StarGen** | Unknown | Open | https://digitalcommons.lindenwood.edu/game_design/41/ | Procedural galaxy + star systems |
| **UE5 Proc. Planets** | C++/BP | MIT | https://github.com/alpapaydin/Unreal-5-Procedural-Planets-and-Space-Physics | UE5 specific! |

### Key Techniques (from Sebastian Lague)
1. **Quadtree-based spherical LOD** for planet terrain
2. **Simplex/Perlin noise** layered for terrain height
3. **Triplanar mapping** for seamless texture application
4. **Crater generation** for realistic planetary surfaces
5. **Atmospheric scattering** (Rayleigh/Mie)
6. **Ocean shading** with depth-based coloring [^153^] [^157^] [^162^] [^361^] [^362^] [^374^] [^409^]

### UE5 Integration Path
- **Option A**: Port Sebastian Lague's Unity C# code to UE5 C++
- **Option B**: Use https://github.com/alpapaydin/Unreal-5-Procedural-Planets-and-Space-Physics (already UE5)
- **Option C**: Use UE5 `Geometry Script` + `Dynamic Mesh Component` with Perlin noise
- **Option D**: Use `Virtual Heightfield Mesh` for planet terrain rendering

---

## 7. Space Engine

### Overview
Space Engine is a free 3D astronomy program and game engine that simulates the entire known universe using procedural generation and real astronomical data.

### Key Facts
| Feature | Value |
|---------|-------|
| **Website** | https://spaceengine.org |
| **License** | **Proprietary / Freeware** (personal non-commercial use) |
| **Commercial Use** | Requires SpaceEngine PRO DLC purchase |
| **Open Source** | **NO** - Not open source |
| **API/Scripting** | Limited scripting via console commands |
| **Data Export** | Screenshots, video, cube maps, textures |

### Licensing Details
- **Free version**: Personal, non-commercial use only
- **SpaceEngine PRO DLC**: Required for commercial use
- Content created (screenshots, video, textures, scripts) can be distributed for non-commercial educational use with attribution [^161^] [^163^]

### Value for MEOK SPACE
- Can be used as a **reference** for procedural generation techniques
- Cannot directly integrate into UE5 (not open source)
- Cannot use for commercial game without PRO license
- Excellent for visual reference and data export (textures, heightmaps)

---

## 8. Universe Sandbox

### Overview
Universe Sandbox is a physics-based space simulator that merges gravity, climate, collision, and material interactions.

### Key Facts
| Feature | Value |
|---------|-------|
| **Website** | https://universesandbox.com |
| **License** | **Proprietary / Commercial** |
| **Open Source** | **NO** |
| **API** | **No public API** |
| **Data Export** | Limited (screenshots, videos, save files) |
| **Modding Support** | Limited (custom objects via JSON) |

### Value for MEOK SPACE
- Not open source - no direct integration
- Can be used for physics simulation reference
- No API for data extraction
- No UE5 integration path

---

## 9. Outerra Engine

### Overview
Outerra is a planetary rendering engine capable of rendering entire planets with high detail from orbit to ground level.

### Key Facts
| Feature | Value |
|---------|-------|
| **Website** | https://www.outerra.com |
| **License** | **Proprietary / Commercial** |
| **Open Source** | **NO** |
| **Focus** | Procedural Earth rendering, vehicle simulation |
| **Products** | Anteworld (game), Outerra World Sandbox |

### Value for MEOK SPACE
- Reference for planetary LOD techniques
- Not open source
- No API for external integration
- No UE5 integration path

---

## 10. Kerbal Space Program Modding

### Overview
KSP has a rich modding ecosystem with tools for creating custom planets, star systems, and modifying the solar system.

### Key Modding Tools
| Tool | Purpose | URL |
|------|---------|-----|
| **Kopernicus** | Planet/custom solar system creation | https://github.com/Kopernicus/Kopernicus |
| **Module Manager** | Config file patching | Bundled with most mods |
| **KSP PartTools** | Custom part creation | KSP modding wiki |
| **Blender .mu Import/Export** | 3D model creation | Community tools |

### Popular Planet Packs
- **Real Solar System**: Replaces Kerbol with real Solar System
- **Outer Planets Mod**: Adds Saturn, Uranus, Neptune analogs
- **RSS Expanded**: Adds real trans-Neptunian objects
- **Kerbal Galaxy**: Adds multiple star systems
- **The World Beyond**: 100+ celestial bodies
- **Pledna**: Dwarf planet based on Sedna [^348^]

### KSP-to-UE5 Pipeline
1. Use Kopernicus config files as reference for planet parameters
2. Extract planet heightmap textures from KSP mod packs
3. Study planet configuration format (radius, atmosphere, gravity, etc.)
4. Apply same parameters in UE5 with custom planet generator

### License
- Kopernicus and most tools: Open source (various licenses)
- KSP itself: Proprietary (Squad/Take-Two)

---

## 11. Celestia

### Overview
Celestia is a real-time 3D visualization of space, created in 2001. It simulates the entire known universe with scientifically accurate positions.

### Key Facts
| Feature | Value |
|---------|-------|
| **Website** | https://celestiaproject.space |
| **GitHub** | https://github.com/CelestiaProject/Celestia |
| **License** | **GPL v2** (open source) |
| **Language** | C++ |
| **Platforms** | Windows, Linux, macOS, Android, iOS |
| **Data** | Real star catalogs (Hipparcos, Tycho, Gaia), spacecraft trajectories |

### Data Sources Used
- Hipparcos catalog (default, ~118,000 stars)
- Tycho-2 catalog
- Gaia EDR3 star database (via addon)
- NASA Exoplanet Archive (via addon)
- NGC/IC galaxy database
- Solar system body trajectories (VSOP87 theory)
- SPICE kernels for spacecraft

### Features
- Real-time solar system body positions
- Star catalogs up to billions of stars with addons
- Spacecraft trajectory visualization
- Extensible via Lua scripting
- Add-on system for custom textures, models, orbits
- Cross-platform (Windows, Linux, macOS, iOS, Android) [^146^] [^149^] [^155^] [^156^] [^159^]

### UE5 Integration Path
- Source code is C++/OpenGL - can study rendering techniques
- Extract star position data from catalog files
- Use spacecraft trajectory files (.xyz format)
- Study its planetary rendering/shading code
- Port shaders/techniques to UE5 Material system

---

## 12. Stellarium

### Overview
Stellarium is a free open-source planetarium software that renders realistic skies in real-time.

### Key Facts
| Feature | Value |
|---------|-------|
| **Website** | https://stellarium.org |
| **GitHub** | https://github.com/Stellarium/stellarium |
| **License** | **GPL v2+** (open source) |
| **Language** | C++ (Qt) |
| **Catalogs** | 600K+ stars (default), 177M+ stars (extra), 80K+ DSOs |

### APIs and Scripting
| Interface | Description |
|-----------|-------------|
| **QtScript/JavaScript** | Built-in scripting engine |
| **Remote Control API** | HTTP-based web API |
| **Telescope Control** | ASCOM, INDI protocols |
| **Plugin System** | C++ plugins for extensibility |

### Scripting Example
```javascript
// Stellarium script example
const StarMgr = core.getModule("StarMgr");
StarMgr.setFlagLabels(true);
core.moveToObject("Mars");
```

### UE5 Integration Path
- Use Remote Control API to query star/object positions
- Export sky textures from Stellarium for use in UE5
- Use as reference for atmospheric rendering
- Study its sky rendering algorithms (GPL source available)

### License
- GPL v2+ (copyleft, study only for commercial UE5 projects) [^349^] [^357^] [^358^]

---

## 13. NASA Exoplanet Archive API

### Overview
The NASA Exoplanet Archive maintains the most comprehensive database of confirmed exoplanets and candidates.

### API Details
| Feature | Value |
|---------|-------|
| **Base URL** | https://exoplanetarchive.ipac.caltech.edu/TAP/ |
| **Protocol** | IVOA Table Access Protocol (TAP) |
| **Query Language** | ADQL (Astronomical Data Query Language) |
| **Output Formats** | VOTable, CSV, TSV, JSON |
| **Tables** | `ps` (planetary systems), `pscomppars`, `cumulative` (Kepler) |

### Example Queries
```
# All confirmed planets
https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+ps

# Planets by name with key params
https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,pl_masse,pl_rade,ra,dec+from+ps+where+pl_name='K2-18+b'
```

### Python Access
```python
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
result = NasaExoplanetArchive.query_criteria(table="ps", where="pl_name='Kepler-186 f'")
```

### Data Available
- 5,000+ confirmed exoplanets
- Host star properties (temperature, mass, radius, metallicity)
- Planetary parameters (mass, radius, orbital period, eccentricity)
- Discovery method, facility, reference
- RA/Dec coordinates for sky positioning [^351^] [^353^] [^354^] [^355^] [^356^]

### UE5 Integration Path
1. Query API for confirmed exoplanets
2. Extract RA, Dec, distance, planet radius, star type
3. Generate procedural star systems based on real data
4. Position systems correctly in 3D space
5. Use stellar classification for star color/size
6. Use planet parameters for procedural generation seeds

---

## 14. OpenSpace Project

### Overview
OpenSpace is a NASA-funded open source interactive data visualization software designed to visualize the entire known universe.

### Key Facts
| Feature | Value |
|---------|-------|
| **Website** | https://www.openspaceproject.com |
| **GitHub** | https://github.com/OpenSpace/OpenSpace |
| **License** | **MIT** (permissive open source) |
| **Language** | C++ (OpenGL 4.6) |
| **Platforms** | Windows, Linux |
| **Institutions** | AMNH, Linkoping University, NASA, NYU, Univ. of Utah |

### Features
- Solar system ephemeris (NASA SPICE)
- High-resolution planetary imagery (Earth, Moon, Mars, etc.)
- Animated 3D spacecraft models (ISS, New Horizons, JWST)
- ESA Gaia star catalog (billions of stars)
- Space weather visualization (CCMC)
- Multi-display/planetarium support
- Lua, JavaScript, Python scripting interfaces
- Networked sessions across the globe [^147^] [^148^] [^150^] [^154^] [^158^] [^160^]

### Data Integration
- Uses NASA SPICE kernels for body positions
- Gaia DR3 for star catalogs
- AMNH Digital Universe for extragalactic datasets
- NASA mission data for spacecraft

### UE5 Integration Path
- MIT license - can study and adapt code commercially
- Study its AMNH Digital Universe data loading
- Adapt SPICE kernel integration approach
- Use its Gaia star rendering techniques
- Reference its planetary rendering shaders
- Study its out-of-core rendering for massive datasets

---

## 15. UE5 Space Environment / Assets

### UE5 Built-in Capabilities for Space
| Feature | Description | Use for Space |
|---------|-------------|---------------|
| **World Partition** | Automatic streaming large worlds | Full-scale planets |
| **Virtual Heightfield Mesh** | GPU-driven terrain rendering | Planetary surfaces |
| **Nanite** | Virtualized geometry | High-detail terrain |
| **Lumen** | Real-time global illumination | Space station interiors |
| **Niagara** | Particle systems | Stars, nebulae, thrusters |
| **Volumetric Cloud/Fog** | Atmospheric effects | Planetary atmospheres |
| **Exponential Height Fog** | Atmospheric scattering | Planetary atmospheres |
| **Sky Atmosphere** | Atmospheric scattering model | Earth-like atmospheres |
| **PCG (Procedural Content Generation)** | Built-in procedural tools | Terrain, vegetation |
| **Geometry Script** | Runtime mesh generation | Procedural planets |

### UE5 Plugins for Space
| Plugin | Type | Source |
|--------|------|--------|
| **Atmos Forge** | Atmospheric effects | Fab Marketplace |
| **Procedural Planet System** | Planet generation | Fab Marketplace |
| **Procedural Planets & Space Physics** | Open source planet gen | GitHub (MIT) |
| **Voxel Plugin** | Voxel terrain | GitHub/Commercial |
| **Oceanology** | Ocean water systems | Fab Marketplace |

### Free UE5 Open Source Project
- **Unreal-5-Procedural-Planets-and-Space-Physics**
  - URL: https://github.com/alpapaydin/Unreal-5-Procedural-Planets-and-Space-Physics
  - License: MIT
  - Features: Perlin noise planets, custom gravity, foliage spawning, dynamic spawning, spaceship model [^352^] [^409^]

---

## 16. Planetary Terrain Generation for UE5

### Recommended Approach for MEOK SPACE

**Pipeline: Real NASA Data + Procedural Enhancement**
1. **Base Terrain**: Import NASA MOLA/LOLA heightmaps into UE5 Landscape
2. **Detail Enhancement**: Use procedural noise to add detail beyond data resolution
3. **Material Layers**: Use satellite imagery as base color, blend with procedural detail
4. **Atmosphere**: UE5 Sky Atmosphere with custom parameters per planet
5. **LODs**: World Partition + Virtual Heightfield Mesh for planet-scale streaming

### Heightmap Import Pipeline
```
NASA .img/.lbl → ImageJ/Photoshop → 16-bit PNG/RAW → UE5 Landscape
```

### Scale Considerations
| Body | Radius | UE5 Approach |
|------|--------|--------------|
| Moon | 1,737 km | World Partition + origin rebasing |
| Mars | 3,390 km | World Partition + origin rebasing |
| Earth | 6,371 km | Procedural +局部 detail |
| Gas Giants | 70,000 km | Visual representation only |

### Double Precision
- UE5 supports 64-bit double precision coordinates
- Enables true-to-scale solar system with origin rebasing
- Use `Rebase Origin` for seamless large-world navigation [^425^]

---

## 17. Star Field / Galaxy Procedural Generation

### Open Source Tools

| Tool | Type | License | URL |
|------|------|---------|-----|
| **Spacescape** | Starfield skybox generator | Open (MIT-like) | https://github.com/petrocket/spacescape |
| **Gaia Sky** | Star catalog visualizer | Open | https://gaiasky.space/ |
| **StarGen** | Procedural galaxy tool | Open (Lindenwood) | https://digitalcommons.lindenwood.edu/game_design/41/ |
| **AMNH Digital Universe** | Real star/galaxy data | Illinois Open Source | Via OpenSpace |

### Techniques for Star Fields in UE5
1. **Point Cloud Rendering**: Import star catalogs as point clouds
2. **Instanced Static Meshes**: Billboard sprites for stars
3. **Niagara Particles**: GPU particle rendering
4. **Custom Compute Shader**: GPU-based star rendering

### Star Data Sources
- **Gaia DR3**: 1.8 billion stars with accurate positions [^131^] [^141^] [^144^]
- **Hipparcos**: 118,000 nearby stars [^134^]
- **Tycho-2**: 2.5 million stars
- **2MASS**: Infrared all-sky survey
- **SDSS**: Deep galaxy survey
- **AMNH Digital Universe**: Curated extragalactic dataset [^406^] [^407^] [^412^]

---

## 18. Space Weather Data APIs

### NASA DONKI API
| Feature | Value |
|---------|-------|
| **Full Name** | Database Of Notifications, Knowledge and Information |
| **Base URL** | https://api.nasa.gov/DONKI/ |
| **Data Types** | CMEs, solar flares, geomagnetic storms, SEP, HSS |

### Available Event Types
| Type | Description |
|------|-------------|
| **CME** | Coronal Mass Ejections |
| **FLR** | Solar Flares |
| **SEP** | Solar Energetic Particles |
| **GST** | Geomagnetic Storms |
| **HSS** | High Speed Streams |
| **RBE** | Radio Blackout Events |
| **MPC** | Magnetopause Crossing |

### Python Example
```python
import requests
url = "https://api.nasa.gov/DONKI/CME"
params = {"startDate": "2025-01-01", "endDate": "2025-01-31", "api_key": "DEMO_KEY"}
response = requests.get(url, params=params)
data = response.json()
```

### NOAA Space Weather APIs
| Source | URL | Data |
|--------|-----|------|
| **NOAA SWPC** | https://www.swpc.noaa.gov | Real-time alerts, forecasts |
| **GOES X-Ray Flux** | https://www.swpc.noaa.gov/products/goes-x-ray-flux | Solar flare X-ray data |
| **DSCOVR** | https://services.swpc.noaa.gov/products/solar-wind/ | Real-time solar wind |

### Data Formats
- JSON (NASA DONKI)
- Text/CSV (NOAA real-time)
- RSS feeds (alerts/warnings)

### UE5 Integration
- Query APIs at runtime or cache periodically
- Visualize CME propagation toward Earth
- Display solar flare intensity on HUD
- Show aurora effects based on geomagnetic storm index (Kp) [^363^] [^371^] [^375^] [^382^] [^387^]

---

## 19. Satellite Tracking Data (NORAD TLE)

### Two-Line Element Sets (TLE)
| Feature | Value |
|---------|-------|
| **Maintained by** | USSF 18th Space Defense Squadron |
| **Objects tracked** | 16,000+ satellites and debris |
| **Format** | Text-based TLE/3LE |
| **Update frequency** | Multiple times per day |

### Data Sources
| Source | URL | Access |
|--------|-----|--------|
| **Space-Track.org** | https://www.space-track.org | Registration required |
| **CelesTrak** | https://celestrak.org | Public, no registration |
| **TLE API** | https://tle.ivanstanojevic.me | REST API |

### CelesTrak API Example
```
# ISS TLE
https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE

# All GPS satellites (JSON)
https://celestrak.org/NORAD/elements/gp.php?GROUP=GPS-OPS&FORMAT=JSON

# Starlink satellites
https://celestrak.org/NORAD/elements/gp.php?GROUP=STARLINK&FORMAT=JSON
```

### Python (Skyfield)
```python
from skyfield.api import EarthSatellite, load
satellite = EarthSatellite(line1, line2, name='ISS')
geocentric = satellite.at(t)
lat, lon = wgs84.latlon_of(geocentric)
```

### Data Formats
- **TLE/3LE**: Traditional two-line element sets
- **JSON**: Modern OMM format (recommended)
- **XML**: CCSDS OMM XML
- **CSV**: Comma-separated values
- **KVN**: CCSDS key-value notation

### UE5 Integration
1. Fetch TLE data from CelesTrak API
2. Use SGP4 propagator (C++ port available) to compute positions
3. Update satellite positions each frame or tick
4. Render as instanced meshes or billboard sprites
5. Predict orbital tracks as spline curves [^379^] [^380^] [^381^] [^383^] [^385^] [^389^]

---

## 20. Additional Space Simulation Tools

### Gaia Sky
| Feature | Value |
|---------|-------|
| **URL** | https://gaiasky.space/ |
| **License** | Open source |
| **Features** | Billions of stars, VR, procedural planets, eclipses |
| **Data** | Gaia DR3+, SDSS, NGC, open clusters |
| **Scripting** | Python, custom DSL |
| **Rendering** | Virtual textures, SSR, HDR, dynamic resolution |

### WorldWide Telescope (WWT)
| Feature | Value |
|---------|-------|
| **URL** | https://www.worldwidetelescope.org |
| **GitHub** | https://github.com/worldwidetelescope |
| **License** | **MIT** (open source since 2015) |
| **Data** | 90+ all-sky surveys, JWST, Hubble, Gaia |
| **API** | RESTful Layer Control API (LCAPI) |
| **Integration** | Python (pywwt), JavaScript, WebGL |

### Cosmographia
| Feature | Value |
|---------|-------|
| **URL** | https://naif.jpl.nasa.gov/naif/cosmographia.html |
| **License** | Free (including commercial use) |
| **Source** | Open source (SPICE-enhanced) |
| **Data** | SPICE kernels for planets, spacecraft |
| **Platforms** | Windows, macOS, Linux |

### Digital Universe Atlas (AMNH)
| Feature | Value |
|---------|-------|
| **Distributor** | OpenSpace |
| **License** | Illinois Open Source License |
| **Content** | Stars, galaxies, quasars, Milky Way to cosmic edge |
| **Institution** | AMNH Hayden Planetarium |
| **Data Sources** | 100+ organizations worldwide |

### Marble (KDE Virtual Globe)
| Feature | Value |
|---------|-------|
| **License** | LGPL (open source) |
| **Type** | Virtual globe/world atlas |
| **Planetary** | Earth-focused, limited other bodies |

### Partiview (NCSA)
| Feature | Value |
|---------|-------|
| **Origin** | NCSA Virtual Director project |
| **License** | Open source |
| **Used by** | AMNH Digital Universe |
| **Type** | 4D data visualization |

### JMARS
| Feature | Value |
|---------|-------|
| **URL** | https://jmars.asu.edu |
| **License** | Free (ASU) |
| **Focus** | Mars, Moon, Mercury, Venus, asteroids |
| **Type** | GIS for planetary science |

### NASA Solar System Treks
| Feature | Value |
|---------|-------|
| **URL** | https://trek.nasa.gov |
| **Portals** | Moon, Mars, Mercury, Venus, Titan, Europa, Vesta, Ceres |
| **Data** | WMTS services for GIS |
| **License** | Public Domain [^391^] [^394^] [^401^] [^406^] [^407^] [^412^] [^417^] [^421^]

---

## 21. NASA SPICE Toolkit

### Overview
SPICE is NASA's definitive system for computing geometric information used in planning and analyzing science observations from space-based instruments.

### Key Facts
| Feature | Value |
|---------|-------|
| **Maintained by** | NASA NAIF (Navigation and Ancillary Information Facility) |
| **URL** | https://naif.jpl.nasa.gov/naif/toolkit.html |
| **License** | Free (including commercial) |
| **Languages** | C, Fortran, MATLAB, Python (SpiceyPy), Java, Julia |

### SPICE Kernel Types
| Kernel | Extension | Purpose |
|--------|-----------|---------|
| **SPK** | .bsp | Ephemeris (position/velocity of bodies) |
| **PCK** | .tpc | Physical constants (size, shape, orientation) |
| **IK** | .ti | Instrument parameters |
| **CK** | .bc | Pointing (spacecraft/body orientation) |
| **EK** | .bds | Events |
| **LSK** | .tls | Leap seconds |
| **FK** | .tf | Reference frames |
| **MK** | .tm | Meta-kernels (load multiple kernels) |

### Key SPK Kernels
```
# Planetary ephemeris (covers 1549-2650)
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440.bsp

# Leap seconds
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls

# Mass parameters
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de431.tpc
```

### Python Usage
```python
import spiceypy as spice
spice.furnsh("naif0012.tls")
spice.furnsh("de440.bsp")
et = spice.utc2et("2025-01-01T00:00:00")
pos, _ = spice.spkpos("MARS", et, "J2000", "NONE", "EARTH")
```

### UE5 Integration
1. Use CSPICE C library in UE5 C++ project
2. Load SPK kernels for body positions
3. Use SPICE functions to compute positions at game time
4. Integrate with UE5 actor transforms
5. Cache computed positions for performance
6. Use for: planet positions, spacecraft trajectories, instrument pointing [^133^] [^399^] [^402^] [^405^]

---

## 22. Summary Matrix

### Open Source Tools (Best for MEOK SPACE)
| Tool | License | Stars/Data | UE5 Int. | Priority |
|------|---------|-----------|----------|----------|
| **OpenSpace** | MIT | Universe | Study code | HIGH |
| **Celestia** | GPL v2 | 100K+ stars | Study code | MEDIUM |
| **Gaia Sky** | Open | 1.8B stars | Reference | MEDIUM |
| **Stellarium** | GPL v2+ | 600K+ stars | API/Ref | LOW |
| **WWT** | MIT | 90+ surveys | Python/JS API | MEDIUM |
| **Cosmographia** | Free | SPICE-based | Study | LOW |
| **Kopernicus** | Open | Planet configs | Config ref | MEDIUM |

### Data Sources (Essential for MEOK SPACE)
| Source | License | Type | UE5 Int. | Priority |
|--------|---------|------|----------|----------|
| **MOLA** | Public Domain | Mars terrain | Heightmap | HIGH |
| **LOLA** | Public Domain | Moon terrain | Heightmap | HIGH |
| **Gaia DR3** | Free | 1.8B stars | Point cloud | HIGH |
| **NASA 3D** | Public Domain | Spacecraft models | FBX/OBJ | HIGH |
| **SPICE** | Free | Body positions | C++ lib | HIGH |
| **Horizons** | Free | Ephemeris | REST API | HIGH |
| **Exoplanet Archive** | Free | Exoplanet data | REST API | MEDIUM |
| **CelesTrak** | Free | Satellite TLEs | REST API | MEDIUM |
| **DONKI** | Free | Space weather | REST API | LOW |
| **USGS Astro** | Free | Maps/mosaics | GeoTIFF | MEDIUM |

### UE5-Specific Resources
| Resource | Type | License | URL |
|----------|------|---------|-----|
| **UE5 Procedural Planets** | Project | MIT | https://github.com/alpapaydin/Unreal-5-Procedural-Planets-and-Space-Physics |
| **SebLague Solar System** | Unity (port) | MIT | https://github.com/SebLague/Solar-System |
| **UE5 Voxel Plugin** | Plugin | Free/Commercial | GitHub |
| **UE5 PCG Framework** | Built-in | Epic | UE5.2+ |
| **UE5 Virtual Heightfield** | Built-in | Epic | UE5.1+ |

### Proprietary (Reference Only)
| Tool | License | Commercial Use |
|------|---------|---------------|
| **Space Engine** | Freeware | Requires PRO DLC |
| **Universe Sandbox** | Proprietary | Purchase license |
| **Outerra** | Proprietary | Purchase license |

---

## Recommended Architecture for MEOK SPACE

### Data Layer
```
NASA MOLA/LOLA → Heightmaps → UE5 Landscape
NASA SPICE/Horizons → Body positions → C++ actor transforms
Gaia DR3 → Star catalog → Niagara/Instanced Mesh
NASA 3D Models → FBX → UE5 Static Meshes
Exoplanet Archive → System data → Procedural generation seeds
CelesTrak TLE → Satellite positions → Real-time tracking
```

### Runtime Systems
```
[SPICE Toolkit] ---position data--> [Planet Actors]
[Gaia Star Data] ----coordinates--> [Star Field Renderer]
[MOLA/LOLA Maps] ---heightmaps--> [Landscape System]
[NASA 3D Models] ---meshes-------> [Spacecraft Actors]
[TLE Propagator] ---orbits-------> [Satellite Tracker]
[Exoplanet DB] ---system params-> [ProcGen System]
```

---

## References

Search results cited throughout this document:
- [^131^] TheSky Gaia DR3 integration
- [^132^] NASA 3D Models on Printables
- [^133^] EphemerisSources.jl (JPL Horizons documentation)
- [^134^] Gaia Data Release 1 documentation
- [^136^] MOLA Shaded Relief/Colorized Elevation (ASU)
- [^137^] NASA PGDA Whole MOLA Catalog
- [^138^] 3D Models from NASA (Joshua Stevens blog)
- [^139^] 3D Printing Mars Terrains Using MOLA Data
- [^140^] NASA 3D Models Satellite Kit (Data.gov)
- [^141^] Gaia Sky official website
- [^143^] NASA Mars Relief (Generic Mapping Tools)
- [^144^] Gaia DR3 summary paper (A&A)
- [^145^] MOLA dataset on Wikimedia Commons
- [^146^] CelestiaProject GitHub repositories
- [^147^] OpenSpace at Visualization Center C
- [^148^] OpenSpace NASA Science Activation Team
- [^149^] Celestia official website
- [^150^] OpenSpace AGU abstract
- [^153^] GitHub procedural-terrain topic
- [^154^] OpenSpace Zenodo publication
- [^155^] CelestiaContent repository
- [^156^] CelestiaProject/Celestia main repo
- [^157^] Reddit - Free UE5 procedural planet generator
- [^158^] OpenSpace GitHub README
- [^159^] Celestia Wikipedia article
- [^160^] OpenSpace Project website
- [^161^] SpaceEngine Wikipedia article
- [^162^] GitHub terrain-generation topic
- [^163^] SpaceEngine Steam License Agreement
- [^348^] KSP Planet Packs (Kopernicus Wiki)
- [^349^] Stellarium Wiki (Fandom)
- [^350^] KSP Wiki - Making Planets Tutorial
- [^351^] NASA Exoplanet Archive TAP documentation
- [^352^] UE5 Cinematic Planetary Clouds (YouTube)
- [^353^] NASA Exoplanet Archive API update (GitHub issue)
- [^354^] Astroquery NASA Exoplanet Archive class
- [^355^] NASA Exoplanet Archive paper (arXiv)
- [^356^] NASA Exoplanet TAP API Python example
- [^357^] Creating Videos with Stellarium
- [^358^] Stellarium scripting documentation
- [^359^] Planetary Data System (PDS) on Data.gov
- [^360^] PDS Geosciences Node at WUSTL
- [^361^] ProceduralPlanetGodot (GitHub)
- [^362^] Sebastian Lague Procedural Planets (YouTube)
- [^363^] NOAA CME information page
- [^364^] SebLague Procedural-Landmass-Generation
- [^365^] StackExchange - Procedural star field generator
- [^371^] NOAA GOES X-Ray Flux
- [^374^] SebLague Procedural-Planets repository
- [^375^] NOAA Space Weather Prediction Center
- [^379^] CelesTrak new GP data formats
- [^380^] Two-line element set reference
- [^381^] Space-Track API documentation
- [^382^] NASA DONKI API example (C)
- [^383^] TLE explanation (KeepTrack)
- [^385^] TLE API (ivanstanojevic.me)
- [^387^] Space Weather Laboratory paper
- [^388^] NASA APOD API tutorial
- [^389^] Skyfield TLE processing tutorial
- [^390^] Planet-Generator Godot addon
- [^391^] WorldWide Telescope GitHub
- [^393^] Gaia Data Release information
- [^394^] SPICE-enhanced Cosmographia
- [^395^] WorldWide Telescope at Harvard
- [^396^] Microsoft open-sources WWT
- [^399^] PlanetMapper SPICE kernels documentation
- [^400^] Astroquery Gaia TAP+ documentation
- [^401^] ESA SPICE Cosmographia page
- [^402^] NASA SPICE Toolkit UE5 forum thread
- [^405^] SPICE.jl Julia wrapper documentation
- [^406^] Digital Universe (Grokipedia)
- [^407^] Digital Universe Atlas (LinuxLinks)
- [^409^] UE5 Procedural Planets GitHub
- [^410^] USGS Mars Geologic Map
- [^412^] AMNH Digital Universe Atlas page
- [^417^] Digital Universe Atlas Wikipedia
- [^421^] USGS Explore Data page
- [^425^] UE5 Solar System scale discussion (forums)

---

> **Document generated**: 2025-07-24
> **Total tools researched**: 50+
> **Open source tools**: 30+
> **Data sources**: 20+
