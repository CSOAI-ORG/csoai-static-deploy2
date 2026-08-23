# SOVOS → CPO / visual operating layer — grounded mine (2026-08-11)
*What the estate's real math can actually do for a visual "frozen/fluid" operating layer, and where the light/holographic vision is a gap not a build. Every REAL line = code read on the RunPod pod this session; every GAP line = grep returned zero.*

## The honest split (mine result, RunPod sov-brain-2)

### REAL — math primitives that exist and are tested
| Primitive | Where | What it gives the visual layer |
|---|---|---|
| **Task-vector / model fusion** (Fisher-Rao AIRM geodesic, Gromov-Wasserstein cross-arch fusion, `merge_models_via_gw`) | `sovos-info-geometry` (8/8 pytest on the canonical venv, re-run this session 2026-08-11 — note an earlier 6/8 FAIL was a wrong-venv artifact, missing POT; NOT GPU-verified this session — `gpu_self_test` not run) | The math to *blend* specialist behaviours as vectors on a manifold — this is what "apply task vectors to the whole stack" concretely means: a merged control policy is a point on the SPD/Poincaré manifold, and moving along a geodesic = smoothly interpolating between operating modes. |
| **Hyperbolic J-Space** (Poincaré distance, Möbius add, project-to-ball, Procrustes align) | `sovos-jspace-hyperbolic` 13/13, `sovos-jspace-pipeline` 12/12 | A hierarchy-preserving embedding. "Frozen vs fluid" maps directly onto **radius in the Poincaré ball**: near the boundary = frozen/committed (large distance to move), near origin = fluid/general. This is a real geometric handle for the frozen/fluid axis, not a metaphor. |
| **Frozen/fluid StateBus + CPOLink** | `sovos-mind` (state.py, layer0.py) | A working in-memory state fabric with a `CPOLink` type and `register_link`. The "AI aware within all layers" substrate exists as a state bus that layers subscribe to. |
| **SOV SIGNAL = geodesic distance to permitted manifold** | `sovos-info-geometry` | A single scalar "how far is this action from the allowed region" — the governance gate a visual controller would consult before acting. |

### MODELED (real numbers, no hardware) — the CPO / light layer
- **`CPOLink` is co-packaged optics, honestly stubbed.** layer0.py docstring, verbatim: *"No real CPO hardware. CPOLink is a model with the published power/latency numbers from NVIDIA CPO datasheets (30W → 9W)."* So "light e2e" exists as a **power/latency model of silicon photonics interconnect**, not a rendering path or a physical light engine.
- A CPO *model* is genuinely useful (it lets the stack reason about interconnect cost between agent legs) — but it is not "turns screens 3D".

### GAP — zero code on any disk (aspirational, not built)
- **Holographic pixels / screen→3D / light-field rendering / "10101" transform**: grep across all 20 sovos-* packages = 0 matches for holograph/light-field/render3d/photonic-render. This is a hardware+rendering research programme, not a session build.
- **TTT (test-time training) in the stack**: 0 files anywhere. TTT is real published math (ephemeral per-instance weight updates; the TTTFusion multimodal-fusion paper is real) but **nothing in SOVOS implements it yet.** "TTT fusion" is a direction, not a component.
- **"AI having full control and awareness" of a visual environment**: no perception→action loop over a rendered scene exists. The StateBus is text/state, not pixels.

## How to actually apply the math to the stack (the buildable version)
The vision, translated into what the real primitives support:

1. **Operating modes as manifold points.** Each SOVOS "mindset" (Dragon/Turtle/Sage…) = a task vector. Use `sovos-info-geometry`'s Fisher-Rao geodesic to interpolate between them → a *continuous* mode dial ("frozen" ↔ "fluid") instead of discrete switches. This is buildable now; the math is tested.
2. **Frozen/fluid = Poincaré radius.** Embed state in J-Space; a controller reads radius as its commitment level. Buildable now (primitives pass 13/13).
3. **The gate stays SOV SIGNAL.** Any visual/agentic action is checked as geodesic distance to the permitted manifold before execution — the Care-Floor, expressed as geometry. Buildable now.
4. **The visual/holographic layer is a SEPARATE track** that needs: (a) a real renderer (the estate has Cesium+UE mentioned but no light-field code), (b) a perception model to give the AI scene awareness, (c) TTT only if per-scene adaptation is needed. None exist yet — this is the honest roadmap edge, and pretending otherwise fails the first reviewer.

## Bottom line
The estate has a **real geometric control core** (task vectors + hyperbolic frozen/fluid + a governance gate that is itself geometry) — that is the genuinely novel, defensible thing, and it can drive a visual controller's *decisions* today. The **light/holographic/TTT-fusion visual surface** is a research direction with zero implementation; it should be scoped as its own build, not claimed as present. Applying the math to the whole stack = making every mode-switch and every gate a geometry operation on one shared manifold — which is exactly the "one geometric core, four doors" thesis the master doc already states.
