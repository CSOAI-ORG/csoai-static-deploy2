# THE DEFINITIVE QIDI Plus 4 Max Materials Guide for Robot Parts
## MEOK Labs — Nick's Go-To Reference for Structural, Functional, Load-Bearing Components

---

## TABLE OF CONTENTS

1. [QIDI Plus 4 Max — Confirmed Specs](#1-qidi-plus-4-max--confirmed-specs)
2. [Material Overview Matrix](#2-material-overview-matrix)
3. [PLA — Basic Prototyping](#3-pla--basic-prototyping)
4. [PETG — Stronger Everyday Material](#4-petg--stronger-everyday-material)
5. [ABS — Tough & Heat Resistant](#5-abs--tough--heat-resistant)
6. [ASA — ABS Alternative, UV Resistant](#6-asa--abs-alternative-uv-resistant)
7. [PA (Nylon) — Strong & Flexible](#7-pa-nylon--strong--flexible)
8. [PA-CF (Carbon Fiber Nylon) — THE Premium Structural Material](#8-pa-cf-carbon-fiber-nylon--the-premium-structural-material)
9. [PC (Polycarbonate) — Extremely Strong](#9-pc-polycarbonate--extremely-strong)
10. [TPU/TPE — Flexible & Compliant](#10-tputpe--flexible--compliant)
11. [Composites (Wood-Filled, Metal-Filled)](#11-composites-wood-filled-metal-filled)
12. [Robot Part Material Selection Guide](#12-robot-part-material-selection-guide)
13. [QIDI-Specific Tips & Best Practices](#13-qidi-specific-tips--best-practices)
14. [Complete PA-CF Print Profile](#14-complete-pa-cf-print-profile--the-most-important-material)
15. [Material Drying & Storage Guide](#15-material-drying--storage-guide)
16. [Quick Reference Card](#16-quick-reference-card)

---

## 1. QIDI Plus 4 Max — Confirmed Specs

| Spec | Value | Notes |
|------|-------|-------|
| **Build Volume** | **305 x 305 x 280 mm** | Slightly smaller than initial 330mm claim |
| **Hotend Max Temp** | **370 degC** | 80W bimetal hotend with ceramic heat break |
| **Bed Max Temp** | **120 degC** | 6mm thick aluminum substrate |
| **Chamber Max Temp** | **65 degC** | Active heated chamber with 400W heater + air circulation |
| **Max Print Speed** | 600 mm/s | 20,000 mm/s acceleration |
| **Extruder** | Direct drive, dual gear | Hardened steel nozzle (0.4mm standard) |
| **Nozzle Type** | Multi-metal composite, hardened tip | Wear-resistant for CF/fiber filaments |
| **Build Surface** | Dual-sided textured PEI | Flexible, easy part removal |
| **Firmware** | Klipper v0.12 (open source) | Full auto calibration |
| **Multi-Material** | QIDI Box compatible | Up to 16-color multi-material support |
| **Connectivity** | WiFi, USB, LAN | 1080p camera, timelapse support |
| **Slicer** | QIDI Studio (Orca-based) | Also works with OrcaSlicer, Cura, PrusaSlicer |

### What This Means for Robot Parts

The QIDI Plus 4 Max is exceptionally well-suited for robot part fabrication:

- **370 degC hotend** = Can print PC, PA, PA-CF, PPA-CF, even PPS-CF
- **65 degC heated chamber** = Critical for ABS, ASA, PC, PA (prevents warping)
- **Direct drive extruder** = Excellent for flexible materials (TPU) and precise extrusion
- **Hardened nozzle** = Ready for abrasive carbon fiber and glass fiber filaments
- **Large build volume** = Big enough for full-size robot limbs, frames, and multi-part assemblies
- **Thick 6mm aluminum bed** = Excellent flatness for large footprint prints
- **Active chamber heating with air circulation** = Uniform temperature, no drafts

---

## 2. Material Overview Matrix

| Material | Strength | Flexibility | Heat Res. | Ease of Print | Best For Robot... | Nozzle Risk |
|----------|----------|-------------|-----------|---------------|-------------------|-------------|
| PLA | Low | Rigid | Low (55 degC) | Very Easy | Prototypes, test fits | None |
| PETG | Medium | Slight | Medium (75 degC) | Easy | Enclosures, brackets | None |
| ABS | Medium-High | Slight | High (100 degC) | Moderate | Gears, housings | None |
| ASA | Medium-High | Slight | High (95 degC) | Moderate | Outdoor parts, covers | None |
| PA (Nylon) | High | High | Very High (150 degC) | Moderate-Hard | Joints, gears, wear parts | Low |
| **PA-CF** | **Very High** | **Low (rigid)** | **Very High (180 degC+)** | **Moderate** | **Limbs, frames, structural** | **High (hardened req.)** |
| PC | Extremely High | Rigid | Extreme (145 degC) | Hard | High-stress structural | Low |
| TPU | Low | Very Flexible | Medium | Moderate | Grippers, bumpers, flex joints | None |
| Composites | Varies | Varies | Varies | Moderate | Aesthetic parts, weight sim | High |

---

## 3. PLA — Basic Prototyping

### Overview
PLA (Polylactic Acid) is the easiest material to print but the WEAKEST choice for functional robot parts. Use it only for prototyping, fit-checking, and non-load-bearing cosmetic pieces.

### Pros & Cons for Robot Parts

| Pros | Cons |
|------|------|
| Extremely easy to print | Very brittle — cracks under impact |
| No warping, no chamber needed | Deforms at 55 degC (dashboard on a sunny day) |
| Wide color selection | Creeps under sustained load |
| Biodegradable | Not suitable for load-bearing parts |
| Low cost | Poor layer adhesion compared to engineering filaments |

### Recommended Print Settings

| Setting | Value |
|---------|-------|
| Nozzle Temperature | 200-220 degC |
| Bed Temperature | 50-60 degC |
| Chamber Temperature | Room temp (no heating needed) |
| Print Speed | 100-300 mm/s (can go fast) |
| Cooling Fan | 100% |
| Bed Adhesion | Textured PEI, clean with IPA |
| Retraction | 0.5-1.0 mm @ 25-40 mm/s |
| Layer Height | 0.2 mm (standard) |
| Infill | 20-30% (prototypes) |

### Best Brands for Robot Prototyping
- **Prusament PLA** — Excellent dimensional accuracy
- **eSUN PLA+** — Stronger than standard PLA
- **Polymaker PolyLite PLA** — Reliable, consistent
- **QIDI PLA** — Optimized for QIDI printers

### Nick's Rule: PLA for Robot Parts
> Use PLA ONLY for: prototype fit-checks, display models, non-structural covers, and calibration prints. NEVER use PLA for load-bearing robot joints, limbs, or gears.

---

## 4. PETG — Stronger Everyday Material

### Overview
PETG (Polyethylene Terephthalate Glycol) is the perfect step up from PLA. Stronger, more durable, better chemical resistance, and still easy to print. Great for enclosures and medium-stress parts.

### Pros & Cons for Robot Parts

| Pros | Cons |
|------|------|
| Stronger than PLA (2-3x impact) | More stringing than PLA |
| Good chemical resistance | Somewhat glossy surface |
| Higher temp resistance (75 degC) | Can stick too well to PEI |
| Easy to print, minimal warping | Less rigid than ABS/PA-CF |
| Food safe (some grades) | Not ideal for high-heat applications |
| Good layer adhesion | |

### Ideal Robot Applications
- Electronics enclosures and covers
- Cable management brackets
- Sensor housings
- Medium-stress brackets (non-load-bearing)
- Battery compartments

### Recommended Print Settings

| Setting | Value |
|---------|-------|
| Nozzle Temperature | 230-250 degC |
| Bed Temperature | 70-80 degC |
| Chamber Temperature | Room temp to 35 degC |
| Print Speed | 50-150 mm/s |
| Cooling Fan | 30-50% (minimal) |
| Bed Adhesion | Textured PEI + glue stick for easy release |
| Retraction | 1.0-2.0 mm @ 25-35 mm/s |
| Layer Height | 0.2-0.28 mm |
| Infill | 30-50% for functional parts |

### Best Brands
- **Polymaker PolyLite PETG** — Excellent consistency
- **Prusament PETG** — Great dimensional accuracy
- **eSUN PETG** — Affordable, reliable
- **Atomic Filament PETG** — Premium, made in USA

---

## 5. ABS — Tough & Heat Resistant

### Overview
ABS (Acrylonitrile Butadiene Styrene) is a classic engineering material. Tough, impact-resistant, and heat-tolerant. The QIDI's heated chamber gives it a MASSIVE advantage for printing ABS without warping.

### Pros & Cons for Robot Parts

| Pros | Cons |
|------|------|
| High impact resistance | Warps without heated chamber |
| Good heat resistance (up to 100 degC) | Releases styrene fumes (ventilation needed) |
| Can be acetone smoothed | Poor UV resistance (yellows outdoors) |
| Excellent for gears and housings | Hygroscopic (absorbs moisture) |
| Easy to post-process (sand, drill, tap) | Strong odor during printing |
| Can be glued with acetone | |

### Ideal Robot Applications
- Gears and gearboxes
- Structural housings (indoor robots)
- Motor mounts
- Internal brackets and supports
- Parts needing acetone vapor smoothing

### Recommended Print Settings

| Setting | Value |
|---------|-------|
| Nozzle Temperature | 240-260 degC |
| Bed Temperature | 100-110 degC |
| Chamber Temperature | 50-60 degC |
| Print Speed | 60-120 mm/s |
| Cooling Fan | 0-10% (off or minimal) |
| Bed Adhesion | Textured PEI + ABS slurry or glue stick |
| Retraction | 1.0-2.0 mm @ 25-30 mm/s |
| Layer Height | 0.2 mm |
| Infill | 40-60% for structural parts |
| Brim | Recommended for large parts (8-10mm) |

### Best Brands
- **Polymaker PolyLite ABS** — Low odor, consistent
- **eSUN ABS+** — Reduced warping formula
- **3DXMAX ABS** — Premium engineering grade
- **QIDI ABS** — Pre-tuned for QIDI printers

### QIDI Advantage for ABS
The 65 degC heated chamber virtually eliminates ABS warping. This is a game-changer compared to open-frame printers. Nick can print large ABS parts with confidence.

---

## 6. ASA — ABS Alternative, UV Resistant

### Overview
ASA (Acrylonitrile Styrene Acrylate) is the outdoor-capable cousin of ABS. Nearly identical mechanical properties but with EXCELLENT UV resistance. If your robot will operate outdoors or near windows, use ASA instead of ABS.

### Pros & Cons for Robot Parts

| Pros | Cons |
|------|------|
| Excellent UV resistance | Slightly more expensive than ABS |
| Similar strength to ABS | Still needs heated chamber |
| Better weather resistance | Releases fumes (ventilation needed) |
| Less warping than ABS | |
| Great for outdoor robots/drones | |
| Can be acetone smoothed | |

### When to Use ASA vs ABS

| Scenario | Winner | Why |
|----------|--------|-----|
| Outdoor robot | ASA | UV won't degrade it |
| Indoor robot | ABS | Cheaper, easier to find |
| Drone/UAV | ASA | Sun exposure + impact |
| Automotive parts | ASA | Under-hood heat + UV |
| Prototype (indoor) | ABS | Lower cost |
| Garden/agricultural robot | ASA | Weather + moisture |

### Recommended Print Settings

| Setting | Value |
|---------|-------|
| Nozzle Temperature | 245-265 degC |
| Bed Temperature | 90-110 degC |
| Chamber Temperature | 50-60 degC |
| Print Speed | 60-120 mm/s |
| Cooling Fan | 0-10% |
| Bed Adhesion | Textured PEI + glue stick |
| Retraction | 1.0-2.0 mm @ 25-30 mm/s |
| Layer Height | 0.2 mm |
| Brim | 8-10mm for large parts |

### Best Brands
- **3DXMAX ASA** — Premium, UV-stable
- **Polymaker PolyLite ASA** — Easy to print
- **Prusament ASA** — Great dimensional accuracy
- **eSUN ASA** — Budget-friendly

---

## 7. PA (Nylon) — Strong & Flexible

### Overview
Nylon (Polyamide) is the workhorse material for functional robot parts. It combines high strength with flexibility, excellent wear resistance, and self-lubricating properties. Ideal for gears, joints, and parts that need to flex without breaking.

### Types of Nylon

| Type | Properties | Best For |
|------|------------|----------|
| **PA6** | Highest strength, absorbs more moisture | Structural parts, gears |
| **PA12** | Better dimensional stability, lower moisture | Precision parts, housings |
| **PA66** | Highest heat resistance, harder to print | High-temp applications |

### Pros & Cons for Robot Parts

| Pros | Cons |
|------|------|
| Very strong and durable | Highly hygroscopic (must be dried) |
| Flexible — won't shatter under impact | Warps if not in heated chamber |
| Self-lubricating (great for gears/bearings) | Requires high nozzle temps |
| Excellent wear resistance | Can be tricky to get first layer right |
| High chemical resistance | More expensive than ABS/PETG |

### Ideal Robot Applications
- Gears (self-lubricating!)
- Bushings and bearings
- Flexible joints and couplers
- Living hinges
- Wear pads and slides
- High-impact parts

### Recommended Print Settings

| Setting | Value |
|---------|-------|
| Nozzle Temperature | 250-270 degC |
| Bed Temperature | 70-100 degC |
| Chamber Temperature | 45-60 degC |
| Print Speed | 40-80 mm/s |
| Cooling Fan | 0-20% |
| Bed Adhesion | Textured PEI + PVA glue stick (essential!) |
| Retraction | 1.0-2.0 mm @ 20-30 mm/s |
| Layer Height | 0.2 mm |
| Infill | 30-50% |
| **DRYING** | ** REQUIRED: 80 degC for 4-8 hours before printing** |

### Best Brands
- **Polymaker PolyMide PA6-CF** — Excellent, QIDI-tested
- **eSUN ePA** — Affordable nylon
- **Taulman Alloy 910** — Premium USA-made nylon
- **Prusament PA11/PA12** — Great dimensional stability
- **MatterHackers NylonG** (Glass-filled) — Super rigid

### Critical: Drying Nylon
Nylon absorbs moisture from the air rapidly. Wet nylon = popping, bubbling, weak layers, failed prints. ALWAYS dry nylon before printing and keep it in a dry box during printing. The QIDI Box has built-in 65 degC drying — use it!

---

## 8. PA-CF (Carbon Fiber Nylon) — THE Premium Structural Material

### Overview
**This is THE material for serious robot parts.** PA-CF combines the strength and durability of nylon with the stiffness and lightweight properties of carbon fiber. The result is parts that rival aluminum in strength-to-weight ratio while being printable on the QIDI Plus 4 Max.

### Why PA-CF is #1 for Robot Parts

| Property | PA-CF Value | What It Means |
|----------|-------------|---------------|
| **Tensile Strength** | 127 MPa | Stronger than most metals by weight |
| **Tensile Modulus** | 10.8 GPa | Very stiff — minimal flex under load |
| **Heat Deflection Temp** | 120-209 degC | Won't deform in hot environments |
| **Layer Adhesion** | Excellent | Strong, fused layers |
| **Weight** | 1.19 g/cm3 | Lighter than aluminum |
| **Dimensional Stability** | Excellent | Holds tight tolerances |

### Pros & Cons for Robot Parts

| Pros | Cons |
|------|------|
| Exceptional strength-to-weight ratio | Abrasive — requires hardened nozzle |
| Extremely rigid (carbon fiber stiffness) | More expensive ($40-80/kg) |
| High heat resistance | Requires dry storage |
| Excellent layer adhesion | Slightly reduced impact vs pure nylon |
| Professional matte finish | Slower print speeds |
| Lighter than metal alternatives | |

### PA6-CF vs PA12-CF

| Property | PA6-CF | PA12-CF |
|----------|--------|---------|
| Strength | Higher | Slightly lower |
| Moisture Absorption | Higher (drying critical) | Lower |
| Warp Tendency | Higher | Lower |
| Heat Resistance | Higher (~209 degC) | Still excellent (~176 degC) |
| Printability | Harder | Easier |
| Best For | Maximum strength structural | Precision, outdoor, chemical |

### Ideal Robot Applications (ALL load-bearing!)
- **Humanoid robot legs** — Rigid, lightweight, high-strength
- **Quadruped frames** — Rigid chassis, minimal flex
- **Robot arms** — Structural links, end effector mounts
- **Joint housings** — High-stress pivot points
- **Motor mounts** — Vibration resistant, strong
- **Bearing blocks** — Wear resistant
- **End effectors** — Tool changers, grippers (rigid parts)

### Recommended Print Settings for PA-CF

| Setting | Value | Notes |
|---------|-------|-------|
| **Nozzle Temperature** | **270-290 degC** | Start at 280 degC |
| **Bed Temperature** | **80-100 degC** | Use 100 degC for large parts |
| **Chamber Temperature** | **50-65 degC** | Max out the QIDI chamber |
| **Print Speed** | **30-60 mm/s** | Slower = stronger layers |
| **Cooling Fan** | **0-10%** | OFF for maximum layer adhesion |
| **Bed Adhesion** | **Textured PEI + PVA glue stick** | Essential for large parts |
| **Retraction** | **1.0-2.0 mm @ 20-30 mm/s** | Keep it conservative |
| **Layer Height** | **0.2-0.3 mm** | 0.2mm for detail, 0.3mm for speed |
| **Line Width** | **0.4-0.5 mm** | Wider = stronger |
| **Wall Count** | **4-6 walls** | For structural parts |
| **Infill** | **40-60% gyroid or cubic** | Gyroid for isotropic strength |
| **Top/Bottom Layers** | **5-6 each** | Ensure solid surfaces |
| **Z-Seam** | **Sharpest corner** | Hide the seam |
| **Brim** | **8-12 mm** | Critical for bed adhesion |
| **Dry Filament** | **80 degC, 6-12 hours** | Before EVERY print |
| **Nozzle Type** | **Hardened steel (included!)** | QIDI comes with one |

### Best Brands for PA-CF

| Brand | Product | Price Range | Notes |
|-------|---------|-------------|-------|
| **Polymaker** | PolyMide PA6-CF | $$$ | QIDI officially tested, excellent |
| **eSUN** | ePA-CF | $$ | Great value, reliable |
| **Prusament** | PA11-CF | $$$ | Premium quality |
| **3DXTECH** | CarbonX PA6-CF | $$$$ | USA-made, professional grade |
| **Fiberlogy** | PA12+CF15 | $$ | Good balance, European |
| **QIDI** | NexPA-CF25 | $$ | Optimized for QIDI printers |
| **Sunlu** | PA6-CF | $ | Budget option, decent quality |

### Nick's PA-CF Pro Tips

1. **ALWAYS dry the filament** — Even fresh from the bag, PA-CF can have moisture. Dry at 80 degC for 6+ hours.
2. **Use the chamber heater** — Set to 60-65 degC for maximum layer adhesion and minimal warping.
3. **Print slow** — 40-50 mm/s gives the best results. Speed kills strength with PA-CF.
4. **Cooling fan OFF** — Layer adhesion is everything. The heated chamber manages cooling.
5. **Glue stick is your friend** — PVA glue on PEI prevents part warping AND makes removal easier.
6. **Check nozzle wear** — Even hardened nozzles wear eventually. Inspect after every 2-3 kg of CF filament.
7. **Store in dry box** — QIDI Box has drying built-in. Keep filament at <20% humidity.

---

## 9. PC (Polycarbonate) — Extremely Strong

### Overview
Polycarbonate is one of the strongest 3D printable materials available. It requires a heated chamber (which the QIDI has!) and high temperatures. PC parts are incredibly tough and impact-resistant.

### Pros & Cons for Robot Parts

| Pros | Cons |
|------|------|
| Extremely high impact strength | Requires 110+ degC bed, 65 degC chamber |
| Very high heat resistance (145 degC) | Can warp significantly without proper setup |
| Transparent options available | Highly hygroscopic |
| Excellent mechanical properties | Requires meticulous drying |
| Good for high-stress structural parts | More expensive |

### Ideal Robot Applications
- High-stress structural brackets
- Impact-resistant covers
- Parts in high-temperature environments
- Safety-critical components
- Load-bearing joints where some flex is OK

### Recommended Print Settings

| Setting | Value |
|---------|-------|
| Nozzle Temperature | 290-310 degC |
| Bed Temperature | 110-120 degC |
| Chamber Temperature | 60-65 degC (max it out) |
| Print Speed | 30-60 mm/s |
| Cooling Fan | 0-10% |
| Bed Adhesion | Textured PEI + nano polymer adhesive or glue stick |
| Retraction | 1.0-2.0 mm @ 20-30 mm/s |
| Layer Height | 0.2 mm |
| Wall Count | 4-6 |
| Infill | 40-60% |
| Brim | 10-15 mm |
| **DRYING** | **100 degC for 8-12 hours (CRITICAL!)** |

### Best Brands
- **Polymaker PolyMax PC** — Impact-resistant blend
- **Prusament PC Blend** — Easier to print than pure PC
- **3DXMAX PC** — Premium engineering grade
- **eSUN ePC** — Budget-friendly option
- **MatterHackers PRO Series PC** — Made in USA

### QIDI Advantage for PC
The QIDI Plus 4 Max is one of the few sub-$1000 printers that can reliably print polycarbonate. The 370 degC hotend + 65 degC chamber + 120 degC bed is the complete package for PC printing.

---

## 10. TPU/TPE — Flexible & Compliant

### Overview
TPU (Thermoplastic Polyurethane) is a flexible, rubber-like material. Essential for robot parts that need to grip, absorb shock, or flex. The QIDI's direct drive extruder handles TPU exceptionally well.

### Shore Hardness Scale for Robot Applications

| Shore Rating | Flexibility | Robot Application |
|--------------|-------------|-------------------|
| 85A | Very soft, very flexible | Seals, gaskets, soft grips |
| 90A | Soft, flexible | Gripper pads, bumpers |
| 95A | Medium flexible | Flexible joints, couplers |
| 64D | Semi-rigid | Wheels, treads, dampeners |
| 70D-85D | Rigid but tough | Shock mounts, flexible brackets |

### Pros & Cons for Robot Parts

| Pros | Cons |
|------|------|
| Excellent flexibility and elasticity | Slower print speeds |
| High impact resistance | Can string/ooze |
| Good chemical resistance | Hard to bridge and overhang |
| Great shock absorption | Some brands are hygroscopic |
| Wear resistant | |

### Ideal Robot Applications
- **Gripper fingers/pads** — Compliant, adaptive grasping
- **Foot pads** — Shock absorption for walking robots
- **Bumper covers** — Impact protection
- **Flexible couplers** — Motor-to-shaft connections
- **Vibration dampeners** — Isolate motors/sensors
- **Seals and gaskets** — Dust/water protection
- **Tire treads** — Robot wheels

### Recommended Print Settings (Direct Drive)

| Setting | Value |
|---------|-------|
| Nozzle Temperature | 220-240 degC |
| Bed Temperature | 40-60 degC |
| Chamber Temperature | Room temp |
| **Print Speed** | **25-40 mm/s** (SLOW!) |
| **Cooling Fan** | **30-50%** |
| Bed Adhesion | Textured PEI (clean) |
| **Retraction** | **0.5-1.5 mm @ 25-35 mm/s** |
| Layer Height | 0.2 mm |
| **Travel Speed** | **100-150 mm/s** |
| Infill | 20-30% (gyroid for flexibility) |
| Combing | ON (avoid crossing perimeters) |
| Wipe Before Retract | ON |

### Best Brands
- **SainSmart TPU** — Reliable, good range of hardness
- **NinjaTek Cheetah** (95A) — Premium, very flexible
- **NinjaTek Armadillo** (75D) — Rigid TPU
- **eSUN eTPU** — Budget-friendly
- **Polymaker PolyFlex** — Easy to print
- **Prusament Flex** — Great for QIDI/Orca profiles

### TPU Printing Tips for Direct Drive
1. **Print SLOW** — 30 mm/s is the sweet spot for quality flexible prints
2. **Tighten filament path** — Any gap will cause the flexible filament to buckle
3. **Minimize retraction** — Too much retraction causes jams with flexible filament
4. **Enable combing** — Keep travel moves inside the model
5. **Don't use a filament guide tube** — Can cause too much friction

---

## 11. Composites (Wood-Filled, Metal-Filled)

### Overview
Composite filaments mix PLA or other base materials with fibers or particles (wood, metal, etc.) for aesthetic and functional properties. These are NOT structural materials but have niche uses in robotics.

### Types of Composites

| Type | Base Material | Filler | Properties |
|------|---------------|--------|------------|
| Wood-filled | PLA | Wood fiber | Aesthetic, sandable, paintable |
| Metal-filled | PLA/ABS | Metal powder | Heavy, metallic look, can be polished |
| Carbon-filled (non-CF) | PETG/ABS | Carbon particles | ESD-safe, slightly stronger |
| Ceramic-filled | PLA | Ceramic | Heat resistant after firing |
| Glow-in-dark | PLA | Phosphorescent | Aesthetic, signage |

### Ideal Robot Applications
- **Aesthetic covers** — Wood-filled for natural look
- **Weight simulation** — Metal-filled for realistic weight distribution
- **ESD-sensitive areas** — Carbon-filled for static dissipation
- **Display/showcase robots** — Premium look and feel

### Important Notes
- **Abrasive to nozzles** — Use hardened nozzle (QIDI has one!)
- **Not for structural parts** — Lower strength than base material
- **Clogging risk** — Some composites clog easily
- **Higher temps needed** — Usually 10-20 degC higher than base

### Print Settings (General)

| Setting | Value |
|---------|-------|
| Nozzle Temperature | Base temp + 10-20 degC |
| Bed Temperature | Same as base material |
| Print Speed | 30-60 mm/s (slower) |
| Cooling Fan | Same as base material |
| Nozzle | **Hardened steel required** |
| Layer Height | 0.2-0.3 mm |
| Retraction | Minimal (composites clog easily) |

---

## 12. Robot Part Material Selection Guide

### Comprehensive Part-Material Matrix

| Robot Part | Primary Material | Secondary Material | Why |
|------------|-----------------|-------------------|-----|
| **Humanoid leg (structural)** | **PA-CF** | PC | Max stiffness + lightweight |
| **Humanoid arm (structural)** | **PA-CF** | ABS | Strong, light, machinable |
| **Quadruped frame/chassis** | **PA-CF** | CF-PETG | Rigid + lightweight |
| **Gear (load-bearing)** | **PA (Nylon)** | PA-CF | Self-lubricating, durable |
| **Gear (high torque)** | **PA-CF** | PC | No flex under load |
| **Bushing/bearing** | **PA (Nylon)** | PA-CF | Self-lubricating, low friction |
| **Gripper fingers** | **TPU (95A)** | Flexible PLA | Compliant, adaptive grasp |
| **Gripper frame** | **PA-CF** | PETG | Rigid mount for TPU pads |
| **Joint connector** | **PA-CF** | ABS | High stress, impact |
| **Motor mount** | **PA-CF** | ABS | Vibration + heat |
| **Foot pad (humanoid)** | **TPU (90A)** | TPE | Shock absorption |
| **Foot pad (quadruped)** | **TPU (95A)** | TPE | Grip + durability |
| **Enclosure/cover** | **PETG** | ASA | Easy print, durable |
| **Outdoor enclosure** | **ASA** | ASA-CF | UV resistant |
| **Cable management** | **PETG** | TPU | Durable, flexible clips |
| **Sensor housing** | **PETG** | ASA | Chemical resistant |
| **Battery holder** | **ABS** | PETG | Heat resistant |
| **Wheel/tread** | **TPU (85A-95A)** | TPE | Grip, shock |
| **Flexible coupler** | **TPU (95A)** | Nylon | Vibration isolation |
| **Shock mount** | **TPU (90A)** | TPE | Impact absorption |
| **Living hinge** | **PA (Nylon)** | TPU | Flexes without fatigue |
| **End effector (rigid)** | **PA-CF** | PC | Precise, strong |
| **End effector (compliant)** | **TPU** | Nylon | Adaptive grasp |
| **Prototype/test fit** | **PLA** | PETG | Fast, cheap iterations |

### By Robot Type

#### Humanoid Robots
- **Torso frame**: PA-CF (structural) + ABS (internal mounts)
- **Legs**: PA-CF (primary) — MUST be rigid
- **Arms**: PA-CF (structural links) + ABS (joint housings)
- **Hands**: PA-CF (palm/frame) + TPU (fingers/pads)
- **Head**: PETG or ASA (enclosure)
- **Feet**: PA-CF (ankle) + TPU (sole pad)

#### Quadruped Robots
- **Chassis/frame**: PA-CF (essential — any flex kills gait)
- **Leg links**: PA-CF (rigid, lightweight)
- **Foot pads**: TPU 95A (grip + shock)
- **Body cover**: PETG or ASA
- **Internal mounts**: ABS or PETG

#### Robotic Arms
- **Base structure**: PA-CF or PC (high rigidity)
- **Arm links**: PA-CF (lightweight + stiff)
- **Joint housings**: PA-CF or ABS
- **End effector**: PA-CF (rigid) or TPU (compliant)
- **Cable tracks**: PETG or TPU

---

## 13. QIDI-Specific Tips & Best Practices

### Bed Adhesion by Material

| Material | Bed Surface | Adhesion Aid | Removal Method |
|----------|-------------|--------------|----------------|
| PLA | Textured PEI | None (clean with IPA) | Flex plate when cool |
| PETG | Textured PEI | **Glue stick** (prevents bonding) | Flex plate when cool |
| ABS | Textured PEI | Glue stick or ABS slurry | Flex plate when cool |
| ASA | Textured PEI | Glue stick | Flex plate when cool |
| PA | Textured PEI | **PVA glue stick (essential)** | Flex plate when cool |
| **PA-CF** | Textured PEI | **PVA glue stick (essential)** | Flex plate when cool |
| PC | Textured PEI | **Nano polymer adhesive or glue stick** | Flex plate when warm |
| TPU | Textured PEI | None (clean) | Flex plate when cool |

### Chamber Temperature Recommendations

| Material | Chamber Temp | Time to Heat |
|----------|-------------|--------------|
| PLA | Room temp | N/A |
| PETG | 30-35 degC | ~2 min |
| ABS | 50-60 degC | ~5 min |
| ASA | 50-60 degC | ~5 min |
| PA | 50-60 degC | ~5 min |
| **PA-CF** | **60-65 degC (MAX)** | **~8 min** |
| PC | 60-65 degC (MAX) | ~8 min |
| TPU | Room temp | N/A |

### Nozzle Recommendations

| Material | Nozzle Type | Notes |
|----------|-------------|-------|
| PLA, PETG, ABS, ASA | Stock hardened steel (0.4mm) | QIDI includes this |
| **PA-CF, PA-GF** | **Hardened steel or ruby** | Stock nozzle works, check wear |
| **PC** | **Hardened steel** | Stock nozzle fine |
| TPU | Stock nozzle (0.4-0.6mm) | Larger helps with flexible |
| Wood-filled, metal-filled | **Hardened steel required** | Abrasive particles |
| Glow-in-dark | Hardened steel recommended | Phosphorescent particles are abrasive |

### Print Speed Optimization for QIDI Plus 4 Max

| Material | Quality Speed | Balanced Speed | Max Speed |
|----------|--------------|----------------|-----------|
| PLA | 100 mm/s | 200 mm/s | 400 mm/s |
| PETG | 50 mm/s | 100 mm/s | 200 mm/s |
| ABS | 60 mm/s | 100 mm/s | 200 mm/s |
| ASA | 60 mm/s | 100 mm/s | 200 mm/s |
| PA | 40 mm/s | 60 mm/s | 100 mm/s |
| **PA-CF** | **30-40 mm/s** | **50 mm/s** | **80 mm/s** |
| PC | 40 mm/s | 60 mm/s | 100 mm/s |
| TPU | 25 mm/s | 35 mm/s | 50 mm/s |

> **Nick's Rule**: For structural robot parts, always print at "Quality Speed" — the strength difference is significant.

### Multi-Material Printing with QIDI Box

The QIDI Box enables multi-material printing (up to 4 boxes chained = 16 materials). For robot parts:

| Combination | Use Case |
|-------------|----------|
| PA-CF + TPU | Rigid structure + flexible gripper |
| PA-CF + PETG | Structural frame + support interface |
| PA + PA-CF | Flexible joints + rigid links |
| ABS + HIPS | Complex parts with dissolvable supports |
| PC + PVA | Intricate PC parts with water-soluble supports |

### Essential Accessories for Robot Part Printing

| Accessory | Purpose | Priority |
|-----------|---------|----------|
| **Filament dry box** | Keep hygroscopic materials dry | **CRITICAL** |
| **QIDI Box** | Multi-material + active drying | HIGH |
| **Extra hardened nozzles** (0.4mm, 0.6mm) | Replace worn nozzles | HIGH |
| **0.6mm nozzle** | Faster PA-CF prints, stronger layers | MEDIUM |
| **PVA glue sticks** (Elmer's) | Bed adhesion for nylon | **CRITICAL** |
| **Digital calipers** | Dimensional accuracy checks | HIGH |
| **IPA (isopropyl alcohol)** | Clean PEI bed between prints | HIGH |
| **Acetone** | ABS/ASA vapor smoothing | MEDIUM |

---

## 14. Complete PA-CF Print Profile (The Most Important Material)

### THIS IS YOUR GO-TO PROFILE FOR STRUCTURAL ROBOT PARTS

---

### QIDI Plus 4 Max — PA-CF Print Profile (OrcaSlicer / QIDI Studio)

#### General Settings

```
Printer: QIDI Plus 4 Max
Nozzle Diameter: 0.4mm (hardened steel)
Filament: PA-CF (Polymaker PA6-CF, eSUN ePA-CF, or equivalent)
Profile Name: "MEOK-Robot-PA-CF-Structural"
```

#### Temperature Settings

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Nozzle Temperature** | **280 degC** | Optimal flow + layer adhesion |
| First Layer Nozzle | 285 degC | Better first layer bonding |
| **Bed Temperature** | **100 degC** | Strong adhesion to PEI |
| First Layer Bed | 105 degC | Extra adhesion for first layer |
| **Chamber Temperature** | **65 degC** | Maximum — prevents warping |
| Standby Temperature | 180 degC | During tool changes (multi-material) |

#### Speed Settings

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **First Layer Speed** | **20 mm/s** | Critical adhesion |
| **Perimeter/Wall Speed** | **40 mm/s** | Quality exterior surfaces |
| **External Perimeter** | **35 mm/s** | Best surface finish |
| **Infill Speed** | **50 mm/s** | Internal strength |
| **Top/Bottom Solid** | **40 mm/s** | Clean solid layers |
| **Travel Speed** | **200 mm/s** | Fast non-print moves |
| **Z-Hop Speed** | 10 mm/s | Gentle z-lifts |

#### Cooling Settings

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Part Cooling Fan** | **0% (OFF)** | Max layer adhesion |
| Bridge Fan Speed | 20% | Minimal for bridges |
| Overhang Threshold | 45 deg | When to slow down |

#### Extrusion Settings

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Layer Height** | **0.2 mm** | Quality vs speed balance |
| **Line Width** | **0.45 mm** | Slightly wider = stronger |
| **Wall Count** | **5 walls** | Robust perimeter |
| **Top Layers** | **6** | Solid top surface |
| **Bottom Layers** | **6** | Solid bottom surface |
| **Infill Pattern** | **Gyroid** | Isotropic strength |
| **Infill Density** | **50%** | Structural strength |
| **Infill Overlap** | 25% | Strong wall-infill bond |

#### Strength-Enhancing Settings

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Wall Order** | **Inner/Outer** | Better overhangs + strength |
| **Fill Gaps** | **Yes** | Solid infill everywhere |
| **Thin Walls** | **Yes** | Detect and print thin features |
| **Seam Position** | **Aligned** | Hidden on corner |
| **Ironing** | **OFF** | Not needed, can weaken surface |

#### Bed Adhesion Settings

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Brim** | **10 mm** | Essential for PA-CF |
| Brim Lines | 12 | Wide adhesion ring |
| **Skirt** | **2 loops, 5mm distance** | Prime extruder |
| **Elephant Foot Compensation** | 0.15 mm | Counteract first layer squish |

#### Retraction Settings (Direct Drive)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Retraction Distance** | **1.5 mm** | Minimal for direct drive |
| **Retraction Speed** | **25 mm/s** | Gentle, reduces stringing |
| **Detraction Speed** | **20 mm/s** | Consistent re-engagement |
| **Z-Hop** | **0.4 mm** | Avoid collisions |

#### Advanced Settings

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Pressure Advance** | **0.04** | Calibrate for your filament |
| **Input Shaper** | Enabled | Enable in Klipper |
| **Max Volumetric Speed** | **8 mm3/s** | Conservative for CF |
| **Extrusion Multiplier** | 0.95-1.0 | Calibrate per filament |

### PA-CF Pre-Print Checklist

- [ ] Filament dried at 80 degC for 6-12 hours
- [ ] Humidity in dry box <20%
- [ ] PEI sheet clean (wipe with IPA)
- [ ] PVA glue stick applied to print area
- [ ] Hardened nozzle installed (check for wear)
- [ ] Chamber heater enabled, target 65 degC
- [ ] Bed leveled and Z-offset calibrated
- [ ] First layer test printed and verified
- [ ] Brim enabled (10mm)
- [ ] Cooling fan set to OFF
- [ ] Print speed <= 50 mm/s

### PA-CF Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Warping/lifting | Wet filament or low bed temp | Dry filament more, increase bed to 110 degC, increase brim |
| Popping/bubbling | Moisture in filament | Dry at 80 degC for 12+ hours |
| Under-extrusion | Partial clog or worn nozzle | Clean nozzle, check for wear, replace if needed |
| Layer separation | Too cold or fan too high | Increase nozzle to 290 degC, turn fan OFF |
| Stringing | Retraction too low | Increase retraction to 2.0mm, check temp |
| Rough surface | Wet filament or wrong temp | Dry filament, try 275-285 degC range |
| Nozzle clogging | Carbon fiber buildup | Increase temp, do atomic pull cleaning |

---

## 15. Material Drying & Storage Guide

### Critical Drying Requirements

| Material | Dry Temp | Dry Time | Storage Humidity | Shelf Life (exposed) |
|----------|----------|----------|------------------|---------------------|
| PLA | 45-50 degC | 4-6 hrs | <30% | Months |
| PETG | 65 degC | 4-6 hrs | <30% | Weeks |
| ABS | 80 degC | 4-6 hrs | <25% | Weeks |
| ASA | 80 degC | 4-6 hrs | <25% | Weeks |
| **PA (Nylon)** | **80 degC** | **6-12 hrs** | **<15%** | **Hours!** |
| **PA-CF** | **80 degC** | **6-12 hrs** | **<15%** | **Hours!** |
| **PC** | **100 degC** | **8-12 hrs** | **<15%** | **Hours!** |
| TPU | 65 degC | 4-6 hrs | <25% | Days |
| Composites | Follow base material | | | |

### Storage Solutions

1. **QIDI Box** — Built-in 65 degC drying, use during printing
2. **eSun eBox / Sunlu S2** — Dedicated filament dryers with feeding
3. **Food dehydrator** — Budget option, works great
4. **Vacuum bags with desiccant** — Long-term storage
5. **DIY dry box** — Sealed container + silica gel packets + hygrometer

### Nick's Storage Rules
1. **Open a spool → Dry it → Use it → Store in dry box**
2. **PA-CF and PC: Never leave out overnight.** Print directly from dry storage.
3. **Label spools with open date and last dried date**
4. **Invest in a $15 digital hygrometer for your dry box**
5. **When in doubt, dry it again** — Extra drying never hurts

---

## 16. Quick Reference Card

### Print This and Tape It to the Printer!

```
+--------------------------------------------------------------+
|         QIDI PLUS 4 MAX - ROBOT PARTS QUICK REFERENCE        |
+------------------+--------+------+---------+--------+--------+
|    MATERIAL      | NOZZLE | BED  | CHAMBER | FAN  | SPEED  |
+------------------+--------+------+---------+--------+--------+
| PLA (prototypes) | 210    | 60   | OFF     | 100% | 200    |
| PETG (enclosure) | 240    | 80   | 30C     | 30%  | 100    |
| ABS (gears)      | 250    | 110  | 60C     | 0%   | 100    |
| ASA (outdoor)    | 255    | 100  | 60C     | 0%   | 100    |
| PA (joints)      | 260    | 90   | 55C     | 0%   | 60     |
| PA-CF (STRUCT)   | 280    | 100  | 65C     | 0%   | 40     |
| PC (high-stress) | 300    | 120  | 65C     | 0%   | 50     |
| TPU (gripper)    | 230    | 50   | OFF     | 40%  | 30     |
+------------------+--------+------+---------+--------+--------+
| ALL: Hardened nozzle (stock) | GLUE: PA-CF/PC/PA/Nylon    |
| DRY: PA/PA-CF/PC before use  | SLOW = STRONG for robots   |
+------------------+--------+------+---------+--------+--------+

NICK'S TOP 3 MATERIALS FOR ROBOT PARTS:
1. PA-CF  - Structural everything (legs, arms, frames)
2. TPU    - Flexible everything (grippers, feet, dampeners)
3. PETG   - Enclosures, brackets, non-structural
```

### First-Purchase Recommendation List

For Nick starting out at MEOK Labs, here's the priority order:

| Priority | Material | Spools | Est. Cost | Used For |
|----------|----------|--------|-----------|----------|
| **1 (CRITICAL)** | PA-CF (Polymaker PA6-CF) | 3 | $120-150 | All structural robot parts |
| **2 (CRITICAL)** | TPU (95A shore) | 2 | $40-60 | Grippers, feet, flex parts |
| **3 (HIGH)** | PETG | 2 | $40-50 | Enclosures, brackets |
| **4 (HIGH)** | ABS | 1 | $20-30 | Gears, indoor housings |
| **5 (MEDIUM)** | PA (Nylon, unfilled) | 1 | $30-40 | Self-lubricating gears |
| **6 (MEDIUM)** | ASA | 1 | $25-35 | Outdoor robot covers |
| **7 (LOW)** | PC | 1 | $40-60 | Extreme stress parts |
| **8 (LOW)** | PLA+ | 1 | $20-25 | Prototypes only |
| | **TOTAL STARTER KIT** | **~12 spools** | **~$330-450** | |

---

## Appendices

### A. Material Strength Comparison Chart

| Material | Tensile Strength (MPa) | Flexural Strength (MPa) | Impact Strength | HDT (degC) |
|----------|----------------------|------------------------|-----------------|------------|
| PLA | 50-65 | 80-100 | Low | 55 |
| PETG | 30-50 | 70-90 | Medium | 75 |
| ABS | 30-40 | 60-80 | High | 100 |
| ASA | 33-40 | 60-80 | High | 95 |
| PA6 (Nylon) | 80-85 | 100-120 | Very High | 65-80 |
| **PA6-CF** | **127** | **177** | **High** | **120-209** |
| **PC** | **60-70** | **90-110** | **Extremely High** | **145** |
| TPU (95A) | 25-35 | 20-30 | Extremely High | 50-60 |

### B. Glossary

| Term | Definition |
|------|------------|
| **Hygroscopic** | Absorbs moisture from air (nylon, PC, PA-CF) |
| **HDT** | Heat Deflection Temperature — where material softens |
| **Tensile Strength** | Resistance to pulling/breaking force |
| **Flexural Strength** | Resistance to bending force |
| **Shore Hardness** | Measure of material flexibility (A=soft, D=hard) |
| **Direct Drive** | Extruder motor mounted on print head (better for flexibles) |
| **Heated Chamber** | Actively heated build volume (reduces warping) |
| **Gyroid Infill** | 3D wavy infill pattern — strong in all directions |
| **PEI** | Polyetherimide — build surface material |
| **PVA Glue** | Polyvinyl acetate — Elmer's glue stick (bed adhesion aid) |

### C. OrcaSlicer / QIDI Studio Material Preset Directory

The QIDI Plus 4 Max works best with **QIDI Studio** (fork of OrcaSlicer). Download material presets from:
- QIDI Studio built-in profiles (recommended)
- OrcaSlicer community profiles
- Manufacturer websites (Polymaker, eSUN, Prusament all provide profiles)

### D. Safety Notes

| Material | Ventilation Required | Notes |
|----------|---------------------|-------|
| PLA | No | Generally safe |
| PETG | Recommended | Low odor |
| ABS | **YES** | Styrene fumes — use enclosure exhaust |
| ASA | **YES** | Similar to ABS, milder but still ventilate |
| PA/PA-CF | **YES** | Can release caprolactam — ventilate |
| PC | **YES** | Releases BPA fumes at high temps |
| TPU | Recommended | Some brands release isocyanates |

> **MEOK Labs Safety**: The QIDI Plus 4 Max's enclosed design helps contain fumes. For ABS/ASA/PA/PA-CF/PC printing, ensure the room has ventilation or use an inline fan exhaust system.

---

*Document Version: 1.0*
*Created for: Nick @ MEOK Labs*
*Printer: QIDI Plus 4 Max*
*Primary Use Case: Robot Parts (Humanoids, Quadrupeds, Arms)*
*Last Updated: Based on QIDI Plus 4 Max firmware/specs as of 2025*

---

**END OF GUIDE — Print the Quick Reference Card (Section 16) and keep it handy!**
