# MEOK EARTH + SPACE: Open Source UE5 World Building Tools Research

> Research compiled from 20+ GitHub searches across all major UE5 tool categories.
> Sources cited with [^N^] notation.

---

## Table of Contents

1. [Procedural World Generation](#1-procedural-world-generation)
2. [Terrain Generation Tools](#2-terrain-generation-tools)
3. [City Generators](#3-city-generators)
4. [NPC AI Systems](#4-npc-ai-systems)
5. [Vehicle Physics](#5-vehicle-physics)
6. [Weather Systems](#6-weather-systems)
7. [Day/Night Cycles](#7-daynight-cycles)
8. [Multiplayer Frameworks](#8-multiplayer-frameworks)
9. [Voxel Engines](#9-voxel-engines)
10. [Water/Ocean Systems](#10-waterocean-systems)
11. [Procedural Foliage](#11-procedural-foliage)
12. [Building Generators](#12-building-generators)
13. [Dialogue Systems](#13-dialogue-systems)
14. [Quest Systems](#14-quest-systems)
15. [Inventory Systems](#15-inventory-systems)
16. [Minimap Systems](#16-minimap-systems)
17. [Save Systems](#17-save-systems)
18. [Modular Character Systems](#18-modular-character-systems)
19. [Digital Twin Tools](#19-digital-twin-tools)
20. [MCP Servers (AI Agents)](#20-mcp-servers-for-ai-agents)
21. [Honorable Mentions - Curated Lists](#21-honorable-mentions)

---

## 1. Procedural World Generation

### UnrealSandboxTerrain
- **URL**: https://github.com/bw2012/UnrealSandboxTerrain
- **Stars**: ~379 | **License**: GPL 3.0 (non-commercial) / Commercial contact
- **Last Commit**: Active - tested with UE 5.1-5.7
- **Description**: UE4/UE5 procedural smooth voxel terrain plugin. Runtime terrain modification, procedural landscape/caves generation, LOD per chunk, up to 65535 terrain materials, multiplayer network support. C++ only. [^257^]

### UE5VoxelTerrainDemo
- **URL**: https://github.com/bw2012/UE5VoxelTerrainDemo
- **Stars**: ~173 | **License**: GPL 3.0
- **Last Commit**: Discontinued at UE 5.3
- **Description**: Full UE5 procedural voxel terrain example with grass, trees, foliage. Playable demo available. Based on Transvoxel Algorithm. [^250^]

### UE5VoxelTerrainTemplate
- **URL**: https://github.com/bw2012/UE5VoxelTerrainTemplate
- **Stars**: ~10 | **License**: GPL 3.0
- **Last Commit**: 2024
- **Description**: Minimal working example of voxel terrain plugin for UE 5.4. [^260^]

### CashGenUE (CashGen)
- **URL**: https://github.com/midgen/cashgenUE
- **Stars**: ~200+ | **License**: MIT
- **Last Commit**: Legacy (UE4.25 era)
- **Description**: Runtime procedural terrain generator for Unreal Engine. Multithreaded heightmap/erosion/geometry, hydraulic erosion, multiple tile LODs with collision/tessellation, dithered LOD transitions, water depth map generation. [^166^]

### ProceduralDungeon
- **URL**: https://github.com/BenPyton/ProceduralDungeon
- **Stars**: ~500+ | **License**: MIT
- **Last Commit**: Active
- **Description**: UE4/UE5 plugin to generate procedural dungeons with room-based generation. [^172^]

### DungeonGenerator
- **URL**: https://github.com/KMakai/DungeonGenerator
- **Stars**: ~50+ | **License**: MIT
- **Description**: UE4 dungeon generator plugin. [^172^]

---

## 2. Terrain Generation Tools

### OpenLand (Open Source Landscape Auto Material)
- **URL**: https://github.com/GDi4K/unreal-openland
- **Stars**: ~200+ | **License**: MIT (non-commercial)
- **Last Commit**: Active
- **Description**: Landscape auto-material for Unreal Engine with RVT tools. Create customizable landscape themes easily. Also includes OpenLand Grass system. [^252^]

### TerrainMagic
- **URL**: https://github.com/GDi4K/unreal-terrain-magic
- **Stars**: ~100+ | **License**: MIT (non-commercial)
- **Description**: Toolset for creating and modifying landscapes in Unreal Engine. Works with existing landscapes and materials. [^251^]

### Voxel Plugin (Legacy - Free)
- **URL**: https://github.com/VoxelPlugin/VoxelPluginFreeLegacy
- **Stars**: ~650+ | **License**: MIT
- **Last Commit**: Active
- **Description**: Voxel plugin for Unreal Engine - procedural voxel terrain with high performance. Legacy open-source version. [^165^]

---

## 3. City Generators

### ProceduralCityGenerator (UE5 Samurais)
- **URL**: https://github.com/TheSamurais/ProceduralCityGenerator
- **Stars**: ~50+ | **License**: Not specified
- **Last Commit**: 2022
- **Description**: UE5 demo project for procedural building and city generation. [^175^]

### CityBLD
- **URL**: Commercial (https://www.citybld.com/)
- **License**: Paid marketplace tool
- **Description**: Professional procedural city creation toolkit for UE5. Not open-source but worth mentioning as the best-in-class city generator for UE5. [^166^]

### ArcGIS Maps SDK for Unreal Engine
- **URL**: https://developers.arcgis.com/unreal-engine/
- **License**: Esri license (free for non-commercial)
- **Description**: Import real-world GIS data, 3D buildings, terrain into UE5. [^166^]

### Cesium for Unreal
- **URL**: https://github.com/CesiumGS/cesium-unreal
- **Stars**: ~900+ | **License**: Apache 2.0
- **Description**: 3D geospatial plugin for UE - brings real-world terrain, buildings, photorealistic 3D Tiles. Open-source. [^166^]

---

## 4. NPC AI Systems

### NPCForge
- **URL**: https://github.com/NPCForge/Plugin
- **Stars**: ~200+ | **License**: MIT
- **Last Commit**: Active (UE 5.4+)
- **Description**: AI-powered NPC system for UE5. Drop-in C++ component, WebSocket communication to AI backend, async AI "brains", environment scanning, cognitive culling, event-driven actions, Blueprint-ready. Inspired by Stanford Smallville/Voyager. [^241^]

### UnrealGenAISupport (Generative AI Plugin)
- **URL**: https://github.com/prajwalshettydev/UnrealGenAISupport
- **Stars**: ~300+ | **License**: MIT
- **Last Commit**: Active
- **Description**: UE5 plugin for LLM/GenAI models. Supports GPT-5, DeepSeek, Claude, Gemini, Grok, Qwen, Kimi, ElevenLabs TTS, and 200+ models. Includes MCP server for AI agent control. NPC AI, agentic chat, 3D generation, TTS, multimodal. [^238^]

### Reasonable Planning AI
- **URL**: https://github.com/JakobP拥挤/ReasonablePlanningAI
- **Stars**: ~100+ | **License**: MIT
- **Description**: Utility Reasoning with Goal Oriented Action Planning (GOAP). Data-driven with C++ and Blueprint support. [^172^]

### BTUtilityPlugin
- **URL**: https://github.com/iuripa/BTUtilityPlugin
- **Stars**: ~50+ | **License**: MIT
- **Description**: Extension to engine behavior tree system, adding utility-based selection nodes. [^172^]

### ALIS (Survival Game - Full NPC Systems)
- **URL**: https://github.com/fallintodusk/alis
- **Stars**: ~150+ | **License**: Custom (open source)
- **Last Commit**: Active (2026)
- **Description**: Open-source UE5 survival game with modular C++ architecture. Includes: Dialogue system (universal data-driven), Inventory (server-authoritative), Vitals, Mind (inner-voice), Interaction, Object Capabilities, GAS integration. [^248^]

---

## 5. Vehicle Physics

### Chaos Vehicles (Built-in UE5)
- **URL**: Built into Unreal Engine 5
- **License**: UE EULA
- **Description**: UE5's official lightweight vehicle physics system using Chaos Physics. Supports cars, trucks, motorcycles, wheeled vehicles. [^167^]

### NetworkedPhysics (Chaos Modular Vehicle)
- **URL**: https://github.com/cem-akkaya/NetworkedPhysics
- **Stars**: ~200+ | **License**: MIT
- **Last Commit**: 2025
- **Description**: Advanced networked physics showcase for UE5.7. Chaos Modular Vehicle, async physics, multi-body physics vehicles (Pod Racer), Loader Truck with hydraulic arms, Mining Truck. [^163^]

### MrRobinOfficial Unreal-CommonVehicle
- **URL**: https://github.com/MrRobinOfficial/Unreal-CommonVehicle
- **Stars**: ~150+ | **License**: MIT
- **Last Commit**: 2024
- **Description**: Plugin extending Chaos Vehicle plugin. ACarPawn and ACarDriveablePawn classes, Enhanced Input support. [^167^]

### VehiclePhysics (Blueprints)
- **URL**: https://github.com/WimbleSoft/VehiclePhysics
- **Stars**: ~80+ | **License**: Custom
- **Description**: Vehicle Physics Simulation on Unreal Engine via Blueprints. [^172^]

### PsRealVehicle
- **URL**: https://github.com/Prvtdncr/PsRealVehicle
- **Stars**: ~50+ | **License**: MIT
- **Description**: Simple force-driven vehicle simulation plugin for UE4/UE5. [^172^]

---

## 6. Weather Systems

### Global Environmental System (GES)
- **URL**: https://github.com/delebash/UE_GlobalEnvironmentalSystem
- **Stars**: ~300+ | **License**: MIT
- **Last Commit**: Active (UE 5.6)
- **Description**: Integrates Ultra Dynamic Sky with Megascan foliage, UE Water, wind systems. Season/health changes on foliage, weather effects, wind direction/strength, water wave asset changing. [^171^]

### ThermoForge
- **URL**: https://github.com/cem-akkaya/ThermoForge
- **Stars**: ~80+ | **License**: MIT
- **Last Commit**: 2025
- **Description**: UE5 plugin for simulating realistic heat, climate, and thermal conditions. Volume-based thermal field baking, climate simulation with diurnal cycles/seasons, altitude effects, heat sources, AI EQS integration. [^249^]

### OceanProject
- **URL**: https://github.com/UE4-OceanProject/OceanProject
- **Stars**: ~1,500+ | **License**: MIT
- **Last Commit**: Legacy (UE4 primarily)
- **Description**: Ocean simulation project for Unreal Engine. FFT-based ocean waves, buoyancy system. [^172^]

---

## 7. Day/Night Cycles

### NewProjectTemplate (Day/Night + Weather)
- **URL**: https://github.com/RYRY1002/NewProjectTemplate-old
- **Stars**: ~30+ | **License**: MIT
- **Description**: UE5 project template with DayNightManager, weather system, World Partition grids, street lights that auto-toggle at night. [^259^]

### Ultra Dynamic Sky (Marketplace - Free)
- **URL**: https://www.unrealengine.com/marketplace/en-US/product/ultra-dynamic-sky
- **License**: Free on Marketplace
- **Description**: Dynamic sky system with day/night cycle, weather, seasons. Industry standard, free. Integrates with GES. [^171^]

### ThermoForge (Climate Cycles)
- **URL**: https://github.com/cem-akkaya/ThermoForge
- **Stars**: ~80+ | **License**: MIT
- **Description**: Diurnal cycles, annual climate model (Desert/Tropic/Arctic/Temperate), dynamic living world creation. [^249^]

---

## 8. Multiplayer Frameworks

### Lyra Starter Game (Official Epic Sample)
- **URL**: https://github.com/EpicGames/UnrealEngine (in Samples/Games/Lyra)
- **License**: UE EULA
- **Description**: Epic's official UE5 sample game. Cross-play multiplayer using Epic Online Services, modular gameplay, Gameplay Ability System, CommonUI, EnhancedInput, scalability from mobile to PC. [^253^]

### TargetVector
- **URL**: https://github.com/Voidware-Prohibited/TargetVector
- **Stars**: ~50+ | **License**: MIT
- **Description**: UE5 template with EOS, Steam, Modular Gameplay, Common UI, ALS. Multiplayer-ready framework. [^265^]

### Bomber
- **URL**: https://github.com/JanSeliv/Bomber
- **Stars**: ~300+ | **License**: MIT
- **Last Commit**: Active (UE 5.6)
- **Description**: Open-source multiplayer game in UE5.6. Clean codebase, latest UE5 features, multiplayer functionalities. [^176^]

### UE5-Multiplayer-Replication-Guide
- **URL**: https://github.com/droganaida/UE5-Multiplayer-Replication-Guide
- **Stars**: ~200+ | **License**: MIT
- **Description**: Practical guide and template for UE5 multiplayer replication, authority, Listen Server, RPC, RepNotify. [^164^]

### TutorialMPBasics
- **URL**: https://github.com/rubenmoor/TutorialMPBasics
- **Stars**: ~100+ | **License**: MIT
- **Description**: Beginner-friendly multiplayer setup for Unreal Engine/C++. Session lifecycle, joining, hosting. [^175^]

---

## 9. Voxel Engines

### UnrealSandboxTerrain
- **URL**: https://github.com/bw2012/UnrealSandboxTerrain
- **Stars**: ~379 | **License**: GPL 3.0 (non-commercial)
- **Description**: The main UE5 voxel engine. Runtime modification, procedural generation, LOD, 65535 materials, multiplayer. [^257^]

### UE5VoxelTerrainDemo
- **URL**: https://github.com/bw2012/UE5VoxelTerrainDemo
- **Stars**: ~173 | **License**: GPL 3.0
- **Description**: Full-featured demo with grass, trees, foliage, caves. [^250^]

### Voxel Plugin (Free Legacy)
- **URL**: https://github.com/VoxelPlugin/VoxelPluginFreeLegacy
- **Stars**: ~650+ | **License**: MIT
- **Description**: Professional-grade voxel plugin. High-performance procedural voxel terrain. [^165^]

---

## 10. Water/Ocean Systems

### OceanProject
- **URL**: https://github.com/UE4-OceanProject/OceanProject
- **Stars**: ~1,500+ | **License**: MIT
- **Description**: FFT ocean rendering with Phillips spectrum, wind-wave dissipation, buoyancy. UE4/UE5 compatible. [^172^]

### FFTOcean
- **URL**: https://github.com/UnrealXinda/FFTOcean
- **Stars**: ~200+ | **License**: MIT
- **Description**: UE4 plugin for frequency-based ocean rendering with Phillips spectrum and wind-wave dissipation. [^266^]

### UE5 Water Plugin (Built-in)
- **URL**: Built into Unreal Engine 5.4+
- **License**: UE EULA
- **Description**: Official UE5 water system with waves, buoyancy, underwater rendering. [^171^]

---

## 11. Procedural Foliage

### Foliage Shadow Imposters
- **URL**: https://github.com/SabreDartStudios/FoliageShadowImposters
- **Stars**: ~50+ | **License**: MIT
- **Description**: UE5.1+ plugin for Nanite foliage performance. Adds cheap shadow-casting imposters for WPO-animated foliage. [^205^]

### OpenLand Grass
- **URL**: https://github.com/GDi4K/unreal-openland-grass
- **Stars**: ~80+ | **License**: MIT (non-commercial)
- **Description**: Game-ready grass system for Unreal Engine with RVT blending and management tools. [^254^]

### UE5 Procedural Foliage Tool (Built-in)
- **URL**: Built into Unreal Engine 5
- **License**: UE EULA
- **Description**: Official procedural foliage spawning system. Spawn forests from foliage types with density/scale/slope controls. [^201^]

---

## 12. Building Generators

### ProceduralCityGenerator
- **URL**: https://github.com/TheSamurais/ProceduralCityGenerator
- **Stars**: ~50+ | **License**: Not specified
- **Description**: UE5 demo for procedural building and city generation. [^175^]

### CityGenerator (Node.js/Blockchain)
- **URL**: https://github.com/universalbit-dev/CityGenerator
- **Stars**: ~20+ | **License**: MIT
- **Description**: Dynamic city models inspired by Fab City principles. Sustainable urban simulation. [^164^]

### Houdini Engine for Unreal
- **URL**: https://github.com/sideeffects/HoudiniEngineForUnreal
- **Stars**: ~700+ | **License**: Houdini license
- **Description**: Professional procedural building/city generation via Houdini Digital Assets. Industry standard for procedural content in UE5. [^267^]

---

## 13. Dialogue Systems

### DlgSystem (Not Yet Dialogue System)
- **URL**: https://github.com/NotYetGames/DlgSystem
- **Stars**: ~700+ | **License**: MIT
- **Last Commit**: Active (UE 5.5-5.7)
- **Description**: Full-featured dialogue plugin. Graph editor, search, dialogue browser, events/conditions, branching, JSON import/export, real-time runtime edit. Used in 100+ games including The Ascent. [^200^]

### Joint (Formerly Commercial)
- **URL**: https://github.com/GGgRain/Unreal-Joint
- **Stars**: ~400+ | **License**: Custom (free/open)
- **Last Commit**: Active (UE 4.27-5.6)
- **Description**: Modular scripting framework for dynamic dialogue (Undertale/Animal Crossing style). Former commercial product now open-source. Clean & intuitive playback design. [^199^]

### SUDS (Steve's Unreal Dialogue System)
- **URL**: https://github.com/sinbad/SUDS
- **Stars**: ~300+ | **License**: MIT
- **Description**: Text-file-based dialogue system. VSCode plugin for syntax highlighting, multi-line speech, player choices, flow control, variables, localization, save game integration. [^264^]

### Mountea Dialogue System
- **URL**: https://github.com/Mountea-Framework/MounteaDialogueSystem
- **Stars**: ~250+ | **License**: MIT
- **Last Commit**: Active (UE 5.2-5.5)
- **Description**: Open-source Mountea Framework tool. Graph editor with validation, graph themes, dialogue previews, decorators, runtime debug. Companion "Dialoguer" standalone builder. [^197^]

### DialogueTree
- **URL**: https://github.com/unraed/DialogueTree
- **Stars**: ~200+ | **License**: MIT
- **Description**: Free UE5 dialogue plugin. Expansive graph editor, easy setup, highly customizable. Also on Marketplace. [^196^]

---

## 14. Quest Systems

### Arc Activities
- **URL**: https://github.com/coitlo/ArcActivities
- **Stars**: ~100+ | **License**: MIT
- **Last Commit**: Active (UE 5.5+)
- **Description**: Activity and Quest system with custom editor graph for creating gameplay activities. [^172^]

### SimpleQuest
- **URL**: https://github.com/TheGeebus/SimpleQuest
- **Stars**: ~50+ | **License**: MIT
- **Description**: Goal state management in visual graph for UE5.6+. Intuitive quest authoring. [^248^]

### UE5DialogAndQuestPlugin
- **URL**: https://github.com/Synock/UE5DialogAndQuestPlugin
- **Stars**: ~40+ | **License**: MIT
- **Description**: Combined quest and dialog system. Quest steps, quest journal, dialog-based progression. [^246^]

### Fallout-Inspired Interaction/Quest System
- **URL**: https://github.com/LuckyLuke00/fallout-inspired-ue5-interaction-quest-system
- **Stars**: ~80+ | **License**: GPL 3.0
- **Description**: Recreates Fallout 4 interaction system. Sphere triggers, sphere casts, ray casts, HUD prompts, grabbing, perspective toggle, dynamic quest system, quest log. [^242^]

---

## 15. Inventory Systems

### InventorySystemCPP
- **URL**: https://github.com/DavidCRicardo/InventorySystemCPP
- **Stars**: ~200+ | **License**: MIT
- **Description**: Multiplayer inventory system with equip-able and usable items. Drag & Drop UI, move/drop/use/equip, dynamic tooltips, hotbar, localization, Windows/Android support. [^245^]

### FaerieDataSystem
- **URL**: https://github.com/Drakynfly/FaerieDataSystem
- **Stars**: ~100+ | **License**: MIT
- **Last Commit**: Active (UE 5.6)
- **Description**: Multi-purpose inventory, equipment, and crafting system. Grid-based inventory, extensible bags, item weight, monetary system, double item slots. [^251^]

### UE5Inventory
- **URL**: https://github.com/Synock/UE5Inventory
- **Stars**: ~60+ | **License**: MIT
- **Description**: Replicated inventory system for UE5. Grid-based with equipment system, extensible bags, item weight/size, monetary system. [^249^]

### Unreal-Inventory-System
- **URL**: https://github.com/recepilhanli/Unreal-Inventory-System
- **Stars**: ~4 | **License**: MIT
- **Description**: Multiplayer inventory with pickup, use, drop. Synced across all players. UI in Blueprints, logic in C++. [^243^]

### Inventory + Equipment System (unreal-arch)
- **URL**: https://github.com/unreal-arch/Inventory-Equipment-System
- **Stars**: ~100+ | **License**: MIT
- **Description**: Generic multipurpose inventory container and equipment system for UE4/UE5. [^172^]

---

## 16. Minimap Systems

### MiniMap Tutorial Series (Built-in)
- **URL**: https://dev.epicgames.com/community/learning/tutorials/KBYx/unreal-engine-5-complete-map-and-mini-map-tutorial-series
- **License**: Free (Epic tutorial)
- **Description**: Official UE5 complete map and minimap tutorial series. [^166^]

### VaFogOfWar
- **URL**: https://github.com/ufna/VaFogOfWar
- **Stars**: ~150+ | **License**: MIT
- **Description**: Clear and simple fog of war solution for UE4/UE5. [^172^]

### Radar System (Horizontal 360)
- **URL**: https://github.com/unreal-arch/Horizontal-360-Radar
- **Stars**: ~50+ | **License**: MIT
- **Description**: Horizontal 360-degree radar/minimap system similar to Skyrim's compass. [^172^]

---

## 17. Save Systems

### SPUD (Steve's Persistent Unreal Data)
- **URL**: https://github.com/sinbad/SPUD
- **Stars**: ~500+ | **License**: MIT
- **Last Commit**: Active (UE 5.x)
- **Description**: Save game and streaming level persistence for UE5. ISpudObject interface, property saving via SaveGame flag, dynamically spawned actor respawning, destroyed actor persistence, World Partition support, Blueprint/C++ support. [^255^]

### Creatorama SaveExtension
- **URL**: https://github.com/CreatoramaStudio/SaveExtension
- **Stars**: ~30+ | **License**: MIT
- **Description**: UE5 save-game system with savegame tags, level streaming support, date/time integration. Forked from PipeRift. [^264^]

---

## 18. Modular Character Systems

### ALS-Refactored (Advanced Locomotion System)
- **URL**: https://github.com/Sixze/ALS-Refactored
- **Stars**: ~1,500+ | **License**: MIT
- **Description**: Completely reworked C++ version of ALS V4. Modular locomotion system, network-ready. [^172^]

### ALS-Community
- **URL**: https://github.com/dyanikoglu/ALS-Community
- **Stars**: ~800+ | **License**: MIT
- **Description**: Replicated and optimized community ALS V4 for UE4.26+ with bug fixes. [^172^]

### GASP-ALS
- **URL**: https://github.com/GaspCtrl/GASP-ALS
- **Stars**: ~200+ | **License**: MIT
- **Description**: Game Animation Sample with ALS layering for UE5.3+. [^172^]

### Lyra Character Framework (Built-in)
- **URL**: Epic's Lyra Starter Game
- **License**: UE EULA
- **Description**: Official modular character system with Gameplay Ability System, experience-based pawn data, modular gameplay actors. [^253^]

---

## 19. Digital Twin Tools

### CARLA Digital Twins
- **URL**: https://github.com/carla-simulator/carla-digitaltwins
- **Stars**: ~100+ | **License**: MIT
- **Description**: CARLA digital twins plugin for UE5. Import real-world maps as digital twins for autonomous driving simulation. [^220^]

### Cesium for Unreal
- **URL**: https://github.com/CesiumGS/cesium-unreal
- **Stars**: ~900+ | **License**: Apache 2.0
- **Description**: 3D geospatial plugin for real-world digital twins. Photorealistic 3D Tiles, terrain, buildings. [^166^]

### WirelessDT
- **URL**: https://github.com/codelzz/WirelessDT
- **Stars**: ~50+ | **License**: MIT
- **Description**: Wireless Digital Twin platform on UE5. WiTracing for wireless signal simulation, requires custom UE5 build. [^222^]

### UnrealMapboxBridge
- **URL**: https://github.com/delebash/UnrealMapboxBridgePlugin
- **Stars**: ~100+ | **License**: MIT
- **Description**: Import real-world locations into UE as landscapes via Mapbox. [^171^]

### SegGen
- **URL**: https://github.com/Secure-and-Intelligent-Systems-Lab/SegGen
- **Stars**: ~30+ | **License**: MIT
- **Description**: UE5 pipeline for generating multimodal datasets with procedural biome generation. [^169^]

---

## 20. MCP Servers for AI Agents

### ue5-mcp (mirno-ehf)
- **URL**: https://github.com/mirno-ehf/ue5-mcp
- **Stars**: ~300+ | **License**: MIT
- **Description**: MCP server plugin for Claude Code. AI can edit Blueprints, materials, Anim Blueprints. Reads, modifies, creates UE5 assets via HTTP server. [^216^]

### Unreal_mcp (ChiR24)
- **URL**: https://github.com/ChiR24/Unreal_mcp
- **Stars**: ~200+ | **License**: MIT
- **Description**: Comprehensive MCP server with 100+ tools across 34 domains. Asset/Actor/Editor/Level/Animation/VFX/Sequencer/Graph editing/Audio/System control. C++ Automation Bridge + TypeScript bridge. [^217^]

### mcp-unreal (remiphilippe)
- **URL**: https://github.com/remiphilippe/mcp-unreal
- **Stars**: ~150+ | **License**: MIT
- **Description**: Single Go binary MCP server. 49 tools for build/test/Blueprints/procedural meshes/doc lookup. Uses Remote Control API + MCPUnreal plugin. [^219^]

### UnrealMCP (kvick-games)
- **URL**: https://github.com/kvick-games/UnrealMCP
- **Stars**: ~100+ | **License**: MIT
- **Description**: Unofficial UE5 MCP plugin. TCP server, JSON command protocol, scene manipulation, Python companion scripts. [^224^]

### flopperam/unreal-engine-mcp
- **URL**: https://github.com/flopperam/unreal-engine-mcp
- **Stars**: ~200+ | **License**: MIT
- **Description**: The Flop Agent - autonomous AI inside Unreal Engine. Full Blueprint creation/editing, world building, materials, 50+ tools. Supports UE 5.5-5.7. [^226^]

### UnrealGenAISupport (MCP + GenAI)
- **URL**: https://github.com/prajwalshettydev/UnrealGenAISupport
- **Stars**: ~300+ | **License**: MIT
- **Description**: Full MCP support + 200+ AI model integration. Blueprint auto-generation, scene control, Python script execution. [^238^]

---

## 21. Honorable Mentions

### Curated Awesome Lists
- **insthync/awesome-unreal**: https://github.com/insthync/awesome-unreal - 2,500+ stars. Categorized collection of awesome open-source UE4/5 repos. [^172^]
- **tomByrer/awesome-unreal-engine**: https://github.com/tomByrer/awesome-unreal-engine - Comprehensive list of UE tools and resources. [^170^]
- **Coop56/awesome-unreal**: https://github.com/Coop56/awesome-unreal - UE5 focused awesome list. [^259^]

### Key Frameworks
- **Lyra Starter Game**: Epic's official UE5 sample - best practices for multiplayer, GAS, CommonUI, modular gameplay. [^253^]
- **Gameplay Ability System (GAS)**: Built into UE5 - abilities, attributes, effects, cooldowns. Essential for RPG/ability-driven games. [^172^]
- **CommonUI**: Built into UE5 - professional UI framework with gamepad/keyboard support.
- **Modular Gameplay**: Built into UE5 - game feature plugins for modular architecture.

### Notable Game Projects (Architecture Reference)
- **ALIS**: https://github.com/fallintodusk/alis - Open-source UE5 survival game, modular C++ plugin architecture, data-driven JSON workflows. [^248^]
- **Bomber**: https://github.com/JanSeliv/Bomber - Open-source UE5.6 multiplayer game. [^176^]

---

## Recommendations for MEOK EARTH + SPACE

### Priority 1: Core World Building
| Tool | Use Case |
|------|----------|
| **UnrealSandboxTerrain** | Voxel terrain for Mars/Earth surface |
| **OpenLand** | Landscape auto-material for planetary surfaces |
| **Cesium for Unreal** | Real-world Earth digital twin |
| **OceanProject** | Water/ocean simulation |

### Priority 2: Environment & Atmosphere
| Tool | Use Case |
|------|----------|
| **GES (Global Environmental System)** | Weather, wind, seasons on foliage |
| **ThermoForge** | Climate/thermal simulation |
| **Ultra Dynamic Sky** | Day/night cycle + weather |

### Priority 3: Systems & Gameplay
| Tool | Use Case |
|------|----------|
| **SPUD** | Save game persistence |
| **DlgSystem** | NPC dialogue |
| **FaerieDataSystem** | Inventory/equipment |
| **NPCForge** | AI-powered NPCs |

### Priority 4: AI Agent Integration
| Tool | Use Case |
|------|----------|
| **ue5-mcp (mirno-ehf)** | AI-controlled Blueprint editing |
| **Unreal_mcp (ChiR24)** | Full AI agent tool suite (100+ tools) |
| **UnrealGenAISupport** | 200+ AI models integrated |

### Priority 5: Multiplayer & Networking
| Tool | Use Case |
|------|----------|
| **Lyra Starter Game** | Base multiplayer framework |
| **NetworkedPhysics** | Advanced vehicle physics networking |

---

*Research compiled: 2025*
*Total searches: 20+ across GitHub and web*
*Sources cited with [^N^] notation referencing search results*
