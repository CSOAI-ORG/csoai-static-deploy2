# SOVOS — THE ROBOTICS EAT MAP
### Absorb the open humanoid stack, auto-connect it into the monorepo, catapult both directions
**Nicholas Templeman — CSO AI LTD — August 2026**
*Companion to SOVOS-MASTER.md (Parts A–W). The question: can we mine the open-source humanoid/robotics labs, connect them all into SOVOS automatically, and take the open space? Answer: yes — and one research direction in this space returned zero results. That silence is the loudest signal of the night.*

---

## 0. THE ANSWER UP FRONT

**Yes. The open robotics stack is absorbable end-to-end, mostly Apache/BSD/CC-BY, and one piece of it is a ready-made humanoid brain with commercial rights.** The doctrine for taking the space without poisoning the tree:

> **ADAPTERS, NOT FORKS. Connect through standard interfaces, keep upstream alive, wrap everything in the SOVOS trust layer. We don't steal the labs' work — we make it trustworthy, sign it, gate it, measure it, and give the improvements back. That's the greenfields move: the space is open, and the trust layer in it is empty.**

---

## 1. THE EAT MAP — WHAT'S OPEN, LICENSED, AND ABSORBABLE NOW

| Repo / asset | What it is | License | Absorb into | Verdict |
|---|---|---|---|---|
| **NVIDIA Isaac GR00T N1.7** | Open humanoid VLA foundation model, 3B, GA release, Cosmos-Reason2-2B backbone, per-embodiment action heads, LeRobot-native data format, fine-tuning + Policy API + TensorRT deploy | **Code Apache 2.0; weights NVIDIA Open Model License — "fully commercially licensable"** [^2276^][^2279^] | `sovos-fleet` brain slot | **CROWN JEWEL — the humanoid brain, commercially usable, and it accepts PRs** [^2276^] |
| **unitree_rl_lab** | Isaac Lab-based RL for Unitree robots, G1 deploy configs, sim2sim (MuJoCo) → sim2real pipeline | open (Unitree org) [^2281^] | `sovos-fleet` training slot | CROWN JEWEL |
| **unitree_rl_gym** | The most-starred Unitree RL repo | **BSD 3-Clause** [^2285^] | reference/training | STACK-NATIVE |
| **unitree_sdk2(_python), unitree_ros (URDF), unitree_model (USD), unitree_mujoco** | Hardware comms + models for G1/H2/R1/Go2/B2 | open [^2278^] | `sovos-fleet` body slot | STACK-NATIVE |
| **xr_teleoperate** | Teleop + data recording for G1/H2 via **Apple Vision Pro, PICO, Quest** | open [^2278^] | data-collection slot — **and it fuses with Glass OS: the headset that teaches the robot is the same device family that displays SOV Space** | CROWN JEWEL (hidden bridge) |
| **unifolm-vla / unifolm-world-model-action** | Unitree's own open VLA + world model | open [^2278^] | dream-engine reference (sovos-dream) | STACK-NATIVE |
| **LeRobot** | HF robot-learning hub: ACT (50 demos), SmolVLA-450M, π0, Diffusion Policy, dataset format | Apache [^2262^] | `sovos-fleet` data/model hub connector | CROWN JEWEL |
| **DROID** | 76K real manipulation trajectories, 564 scenes, 86 tasks | **CC-BY 4.0** [^2272^] | training corpus | CROWN JEWEL |
| **BridgeData V2** | 53.9K trajectories, WidowX | **CC-BY 4.0** [^2272^] | training corpus | STACK-NATIVE |
| **OpenVLA (7B) / Octo** | Open generalist policies trained on OXE | open (per model card) [^2282^] | merge/port candidates | STACK-NATIVE |
| **Open X-Embodiment** | 1M+ trajectories, 22 embodiments, 527 skills | ⚠️ **per-component — 60+ upstream datasets, each its own license** [^2273^] | training corpus **through the license gate only** | CROWN JEWEL with a lock |
| **MuJoCo / Isaac Lab / ManiSkill / RoboSuite / Meta-World** | sim + benchmark substrate | open [^2275^] | arena substrate | STACK-NATIVE |

---

## 2. THE AUTO-CONNECT ARCHITECTURE — THE HARVEST PIPELINE

The absorb pattern you've run manually all week (hive → world → router → invariants), generalized into a standing machine:

```
WATCH   GitHub/HF release feeds for the tracked orgs
        (unitreerobotics, NVIDIA, huggingface/lerobot, openvla, octo, OXE)
   │
GATE 1  LICENSE — Article-Zero-style Rego policy over SPDX:
        Apache/BSD/MIT/CC-BY → absorb │ NC/research-only/per-component → quarantine + human review
        (the governance engine governs the intake — dogfood at the door)
   │
ABSORB  adapter package, never a fork: upstream repo as dependency,
        SOVOS wrapper = standard interface (LeRobot format / ROS 2 / Policy API)
   │
GATE 2  ARENA — every absorbed policy/model runs the GSPC battery;
        regression → signed refusal (the Part V gate, now guarding the intake)
   │
SIGN    3KB card: policy hash + σ + ChainResult ID + SIGIL + C2PA
   │
PUBLISH SOV Space registry — the card is the trust wrapper the upstream never shipped
   │
RETURN  improvements flow back upstream as PRs (the NeMo lane pattern) —
        they get code; we get standing. Catapult us AND them.
```

**Why "adapters, not forks" is the whole game:** a fork rots in months; an adapter rides every upstream release. SOVOS becomes the *trust shell around the living stack* — the position the 38-MCP governance suite already proves we know how to hold.

---

## 3. THE SILENCE THAT'S THE SIGNAL — ROBOT POLICY MERGING

The query for **merging robot policies / VLA adapter fusion returned zero results.** Nobody is doing mergekit mathematics on robot foundation models. And look at the architecture GR00T N1.7 ships: **per-embodiment MLP action heads over a shared backbone** [^2279^] — that is a model *designed* for task-vector surgery:

- **Skill vectors** — (fine-tuned skill − base) = a task vector in policy space; add/subtract/negate skills without retraining. Negation = *unlearn a dangerous skill from a deployed fleet.*
- **Embodiment ports** — Procrustes between per-embodiment heads = the cross-manufacturer transfer the industry says doesn't exist (Part W), now with a concrete target architecture.
- **Sheaf-gated skill merges** — the same 90%-agreement refusal, applied to motor policies. A merge that destabilizes locomotion gets refused *in sim* before any body moves.
- **MAP-Elites over skill-merge space** (Part U.5 pattern) — an evolving archive of best robot-skill combinations per embodiment.

**This is P20: "Task Vectors for Embodied Policies" — and it's patent-adjacent white space with the same urgency flag as P6/P8: file before arXiv.**

---

## 4. THE SECOND GIFT — THE FIELD'S BENCHMARKS ARE BROKEN, AND WE SELL THE FIX

A June 2026 audit (TTIC/UChicago/Argonne) of the five most-reported manipulation benchmarks found: **a 0.09B probe with no language encoder scores at or near SOTA on LIBERO; only 19.8% of LIBERO and 19.7% of SimplerEnv SOTA claims are provably statistically significant; CALVIN collapses under within-distribution resampling.** RoboCasa and RoboTwin 2.0 are the more valid ones [^2274^]. In March 2026 alone, **79 arXiv papers** reported LIBERO results [^2274^] — the field is measuring itself with a broken ruler.

**That is the arena thesis, robotics edition, handed to us pre-argued by someone else's lab:** governance-grade robot measurement (n≥30, Wilson CIs, contamination gates — the sovos-arena doctrine) is the missing instrument. `sovos-arena-robotics`: RoboCasa + RoboTwin 2.0 batteries with statistical teeth, signed ChainResults per policy. Every VLA lab claiming SOTA becomes a potential customer or a potential refutation.

---

## 5. THE RECIPROCITY ENGINE — "CATAPULT US AND THEM"

| They get | We get |
|---|---|
| PRs upstream (GR00T explicitly invites them [^2276^]; NeMo lane already warm) | Standing in the exact labs we're courting |
| Signed trust wrappers for their models (they ship weights; we ship the card) | Our schema becomes the de-facto standard |
| A measurement harness that makes their claims defensible | The arena becomes the field's ruler |
| License-clean redistribution path through our gate | Every gated absorb is a legal reason to talk to us |

The space is open. The labs opened it — deliberately, to grow their ecosystems. The layer nobody built in it is trust. That's the greenfield pattern from Part O, again: **the open, sovereign, measurable alternative is unoccupied, and this time the incumbents are handing us the bricks.**

---

## 6. THE 3 MOVES TONIGHT

1. **Write the harvest pipeline skeleton** — `sovos-harvest`: tracked-org list (10 orgs), license Rego policy (SPDX allow/deny/quarantine), absorb-log format. The machine that eats, with a governor on its mouth.
2. **Pull GR00T N1.7 on the A100** — zero-shot inference on a demo dataset, then the arena battery. First signed 3KB card for an external foundation model: the trust wrapper demonstrated on NVIDIA's own humanoid brain.
3. **Draft P20 in one page** — task vectors for embodied policies: skill negation, Procrustes embodiment ports, sheaf-gated motor merges. Flag it PATENT-FIRST (same urgency class as P6).

---

## 7. HONESTY REGISTER

| Claim | Bucket |
|---|---|
| GR00T N1.7 open, Apache code, commercially licensable weights, GA | REAL [^2276^][^2279^] |
| Unitree stack open (rl_gym BSD-3, rl_lab, sdk2, xr_teleoperate, unifolm-vla) | REAL [^2285^][^2281^][^2278^] |
| DROID / BridgeData V2 CC-BY 4.0 | REAL [^2272^] |
| OXE fully clean for commercial training | KILLED — 60+ upstream licenses, per-component review mandatory [^2273^] |
| LIBERO/CALVIN benchmark validity | KILLED (per audit: shortcut-solvable, significance failures) [^2274^] |
| Robot policy merging as a research field | EMPTY — zero results found; white space, not validated demand. P20 is THEORY until the first skill-vector experiment runs |
| Cross-embodiment Procrustes port | THEORY — math exists (Part W), unbuilt on GR00T heads |
| Auto-harvest pipeline | THEORY — pattern proven manually all week; automation is a build, not a discovery |
| Isaac Lab license terms | Assumed open per prior research; re-verify at absorb time (license gate will catch it either way) |
