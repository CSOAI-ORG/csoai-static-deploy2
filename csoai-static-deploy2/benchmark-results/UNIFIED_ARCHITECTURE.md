# UNIFIED ARCHITECTURE — J-Space + V-Space + C-Space in SOV SPACE

## The Complete Vision (Absorbed from All Sources)

### Data Flow: Water → Milk → Honey → Visual

```
WATER (raw input: text, image, voice, video)
    ↓
12 OWEM SPECIALISTS (logic, ethics, aesthetics, temporality,
                     identity, agency, relationality, embodiment,
                     abstraction, synthesis, destruction, preservation)
    ↓
J-SPACE (Judgment — each specialist's reasoning output)
    ├─ chat output → text J-space
    ├─ image output → visual J-space
    ├─ voice output → audio J-space
    └─ video output → temporal J-space
    ↓
V-SPACE (Visual — reasoning cards, sigils, color-coded)
    ├─ each specialist gets a visual card
    ├─ HMAC-SIGIL signed
    └─ color = specialist family, shape = reasoning type
    ↓
SOV SPACE (Combined memory — 33 agents, 13 model classes,
           1Hz SIGIL heartbeat, BFT-33 quorum)
    ├─ visual docstore memory
    ├─ reasoning chains from all J-spaces
    └─ fluid honey layer (water→milk→honey pipeline)
    ↓
C-SPACE (Creative — dreams, simulations, outcome branching)
    ├─ AI visualizes alternative outcomes
    ├─ probability-weighted visual branches
    ├─ OWEM clusters appear as "visual dances"
    └─ diagonals = infinite drawing of all reasoning
    ↓
INFINITE DRAWING (spatialized viewport over ALL memory)
    ├─ position = embedding similarity
    ├─ zoom = memory granularity
    ├─ glow = Hebbian potentiation
    ├─ fade = Ebbinghaus decay
    └─ THE DRAWING IS THE MEMORY
```

### Key Insight: Piggyback, Don't Pre-Build

Instead of building frozen data → fluid conversion:
- **Build fluid AS we operate**
- Each OWEM output naturally creates J-space
- J-space outputs naturally create V-space visualizations
- Combined reasoning naturally creates C-space dreams
- Everything flows into the infinite drawing
- **The visual docstore IS the memory**

### What Exists (Already Built)

| Component | Status | Location |
|---|---|---|
| OWEM routing (95 models) | Active | sov4_router.py |
| J-space contract | Active (13/13 tests) | j_space_contract.py |
| J-space lens | Active | sov4_jspace_lens.py |
| V-space visual artifacts | Data exists | benchmark-results/v-space/visual_artifacts.json |
| C-space dream scenarios | Data exists | benchmark-results/c-space/cspace_data.json |
| SOV-space memory | Data exists | benchmark-results/sov-space/sovspace_memory.json |
| Infinite draw API | Endpoint exists | api/infinite-draw.js |
| J-space think pipeline | Endpoint exists | api/j-space-think.js |
| Visual operators (16 spatial ops) | Active | visual_operators.py |
| Honey knowledge (65+ Q/A) | Active | sov5_honey.json |
| SIGIL chain | Active | signed_memory_delta.py |
| BFT-33 council | Active | bft_council.py |

### What's Missing (To Build)

1. **Unified Space Pipeline**: No single pipeline routes OWEM → J-space → V-space → SOV SPACE → C-space → Infinite Drawing
2. **Real Visual Renderer**: API returns JSON, no WebGPU/canvas renderer
3. **Fluid Memory NN**: No Titans/MIRAS sidecar, no delta-rule state
4. **C-space Dream Engine**: Current is deterministic branching, not real creative reasoning
5. **MemPalace Integration**: Empty forest/ directory
6. **CRDT Sync (DRUM)**: No Yjs, no persistent peer sync
7. **SignedMemoryDelta in serving path**: Not wired into inference
8. **Multi-clan serving**: Single model at a time, no vLLM/SGLang

### Architecture Components

#### J-Space (Judgment Space)
Each OWEM specialist's output gets its own J-space:
- Schema: `sov.jspace-event/v1`
- Properties: reportable, modulable, causally mediating
- Chain: SHA-256 hash chain with Ed25519 SIGIL signatures
- Storage: JSONL append-only log with intervention tracking

#### V-Space (Visual Space)
Visual artifacts from J-space outputs:
- Reasoning cards with color-coded specialists
- HMAC-SIGIL signed visual artifacts
- Specialist family → color mapping
- Reasoning type → shape mapping

#### C-Space (Creative Space)
Creative visual reasoning layer:
- Dream scenarios with branching outcomes
- Probability-weighted visual branches
- HSL color coding for outcome probability
- OWEM clusters as "visual dances"
- Diagonals = infinite drawing of all reasoning

#### SOV SPACE
The sovereign operating space:
- 33 active agents
- 13 model classes
- 1Hz SIGIL heartbeat
- BFT-33 quorum (23/33)
- Visual docstore memory
- Fluid honey layer

#### Infinite Drawing
The culminating visual layer:
- Spatialized, zoomable viewport over entire memory graph
- Position = embedding similarity
- Zoom = memory granularity (universe → wings → rooms → drawers)
- Glow = Hebbian potentiation (frequently-accessed memories brighten)
- Fade = Ebbinghaus decay (unused memories sink)
- Clan-colored swarms = per-agent wings/diaries
- THE DRAWING IS THE MEMORY

### Build Order (Priority)

1. **Unified Pipeline Script**: Route OWEM → J-space → V-space → SOV SPACE → C-space → Drawing
2. **WebGPU Canvas Renderer**: Visualize the infinite drawing in browser
3. **Fluid Memory NN**: RWKV-7 or Gated DeltaNet for test-time writable state
4. **C-space Dream Engine**: Real creative reasoning with branching outcomes
5. **Multi-clan Serving**: vLLM/SGLang with concurrent LoRA adapters
6. **CRDT Sync**: Yjs documents with clans as peers

### Sources Absorbed
- C_SPACE_ARCHITECTURE.md (68 lines)
- FOREST_MASTER_PLAN.md (79 lines)
- OWEM_MASTER_REGISTRY.md (72 lines)
- Kimi OWEM Deep Dive (445+ lines)
- Kimi R33/R34 research
- Dimension 1-4 research docs
- sov_space_visual.py (344 lines)
- infinite-draw.js (231 lines)
- j-space.js (125 lines)
- j-space-think.js (241 lines)
- sov-space-state.js (134 lines)
- 95 OWEM models across 8 families
- 65+ honey knowledge pairs
- 16 visual operators
- SignedMemoryDelta chain (7 deltas)
- BFT-33 council (6 models, real voting)
