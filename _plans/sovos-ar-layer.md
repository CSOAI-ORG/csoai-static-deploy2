# SOVOS — SOV GO: THE AR LAYER
### The real-world bridge: Pokémon GO for governed AI, humanoid POV overlays, SOV Space visible on your street
**Nicholas Templeman — CSO AI LTD — August 2026**
*Companion to SOVOS-MASTER.md (Parts A–AD). The ask: bridge SOV City into the real world — VR/AR, humanoids at home/work/street, robot POV, live SOV Space view. Answer: yes, and the WebAR platform that used to cost $3K/project/month went MIT open-source in February.*

---

## 0. THE TIMING GIFT (verified)

**8th Wall — the leading WebAR engine — shut down its hosted platform and released the core technology open-source under MIT (8thwall.org, Feb 2026)** [^2353^][^2355^]. World tracking + SLAM engine binary **free for commercial use**, image targets, face effects, sky effects, ECS runtime, works with **Three.js** (our stack), A-Frame, Babylon, PlayCanvas [^2353^]. This was $700–$3,000 per project per month; now zero [^2353^]. Browser AR, no app install, 3B+ devices.

**Google's world-scale layer is live and free:** ARCore Geospatial API (anchors at lat/long/altitude), **Streetscape Geometry** (3D mesh of buildings within 100m), Scene Semantics (12 pixel-class labels), Geospatial Depth (65m), Rooftop Anchors — Android **and** iOS [^2359^][^2360^].

**Robot-side:** Unitree's sdk2 streams camera/video; digital-twin platforms already compile machine twins to Quest/HoloLens/AVP and Three.js web viewers [^2361^].

---

## 1. THE THREE EXPERIENCES

### ① SOV GO — Pokémon GO for governed AI
The real map is the board. MEOK characters and clan citizens are **geospatially anchored** — in your home, your office, your street. Players find them, interrogate them, recruit them, or **RED-team them** (Part AD's adversarial mode, now physical). Rewards are **signed 3KB cards** — the first collectible in gaming that is also a cryptographic proof. Governance missions tie to real places: *"this building runs AI systems — run the transparency check"* — Art. 50 scavenger hunts that teach regulation by walking through it.

### ② HUMANOID POV — see what the robot sees
A Unitree's camera stream (sdk2) + its world-model state → AR overlay: **the robot's predictions and σ field rendered over reality.** You stand in the room; your phone shows what the humanoid *thinks* is there, what it plans to do, and how sure it is — σ fog over its uncertain predictions (the shader language from Part T/AD, now literal). No other robotics company can show a robot's *calibrated uncertainty* because no one else computes it.

### ③ SOV SPACE REAL-TIME VIEW — the city overlaid on reality
Point the phone anywhere: the live simulation state anchors to real geometry via Streetscape mesh — districts ghosted onto buildings, the council's current vote hovering over your kitchen table, the Daily City Report as an AR object. **σ as weather, in the sky** (Sky Effects: storm clouds where the city's confidence is low).

---

## 2. THE TRIPLE DATA FLYWHEEL

```
NIGHT:  machine-vs-machine (volume)          — Part AC
DAY:    human-vs-machine sessions (surprise) — Part AD
WORLD:  AR physical decisions (embodiment)   — THIS LAYER
        where humans walk, what they inspect, which agents they trust
        → signed, consented, 3KB cards → honey strata
```

The AR stream is the rarest: *embodied* human judgment data — what people do with AI when it shares their physical space. Nobody in governance has it because nobody else has a game.

---

## 3. STACK + HONESTY

```
8th Wall open engine (MIT) + Three.js       ← browser AR, no install
ARCore Geospatial + Streetscape             ← world anchors + building mesh
Unitree sdk2 video / WebRTC                 ← robot POV
sovos-bus-redis + SIGIL                     ← live state, signed events
Article 0 + DPIA lane                       ← we govern our own game (dogfood)
```

| Risk | Ruling |
|---|---|
| 8th Wall engine binary is as-is, unmaintained long-term | REAL [^2353^] — fine for v1; Three.js/A-Frame path keeps us portable |
| Consumer AR games are a hits business; retention is brutal | REAL — position SOV GO as **top-of-funnel + data stream, not core revenue**. Revenue stays in substrate/training/RAS |
| Camera + geolocation + street mesh = GDPR/DPIA territory | REAL — consent flow, on-device processing where possible, and **our own game passes through our own gates** (the dogfood story writes itself) |
| Robot POV latency/quality in the wild | THEORY until the sdk2 stream is tested on the pod |
| Geospatial VPS coverage gaps | REAL — degrade gracefully to marker/room-scale AR |

---

## 4. THE 3 MOVES TONIGHT

1. **Hello-world SOV GO:** 8th Wall open engine + one MEOK character anchored at a lat/long, phone browser, one screenshot — the AR layer exists by morning
2. **σ-sky shader in AR:** port the uncertainty shader to Sky Effects — storm over a low-σ agent. The game's visual signature, one shader
3. **Spec the POV pipeline:** sdk2 video → WebRTC → Three.js overlay with σ field — the doc that turns "see what the humanoid sees" into tasks

*Not legal advice; AR data-handling design reviewed against GDPR before any public deployment.*
