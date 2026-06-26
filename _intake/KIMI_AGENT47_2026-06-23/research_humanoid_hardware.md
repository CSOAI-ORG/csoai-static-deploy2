# Open Source 3D-Printable Humanoid Robot Research for QIDI Plus 4 Max
## Nick at MEOK Labs — Complete Build Guide & Comparison

**Research Date:** July 2026
**Printer:** QIDI Plus 4 Max (heated chamber, 350C nozzle, direct drive, multi-material)
**Materials supported:** PLA, PETG, ABS, ASA, PC, PA-CF, PA-GF, TPU

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Comparison Matrix](#comparison-matrix)
3. [Priority Project: Berkeley Humanoid Lite (Deep Dive)](#1-berkeley-humanoid-lite)
4. [InMoov](#2-inmoov)
5. [Poppy Humanoid](#3-poppy-humanoid)
6. [Reachy Family](#4-reachy-family)
7. [ToddlerBot](#5-toddlerbot)
8. [ROBOTO ORIGIN](#6-roboto-origin)
9. [AgiBot Lingxi X1](#7-agibot-lingxi-x1)
10. [pib (Printable Intelligent Bot)](#8-pib)
11. [K-Bot (K-Scale Labs)](#9-k-bot)
12. [NAO (SoftBank/Aldebaran)](#10-nao)
13. [Fourier GR-1](#11-fourier-gr-1)
14. [Unitree G1](#12-unitree-g1)
15. [EngineAI PM01](#13-engineai-pm01)
16. [LeRobot SO-100 / SO-101 Arms](#14-lerobot-so-100--so-101)
17. [Apptronik Apollo](#15-apptronik-apollo)
18. [UBTech Walker Series](#16-ubtech-walker-series)
19. [Tesla Optimus](#17-tesla-optimus)
20. [Other Notable Projects](#18-other-notable-projects)
21. [Best First Print Order](#best-first-print-order-for-nick-at-meok-labs)
22. [QIDI Plus 4 Max Recommended Settings](#qidi-plus-4-max-recommended-settings)
23. [Resources & Links](#resources--links)

---

## Executive Summary

This document catalogs **every major open source humanoid robot project** that can be built with a 3D printer, with special focus on the **QIDI Plus 4 Max** heated-chamber printer. Nick at MEOK Labs has an ideal printer for this work — the heated chamber (up to 350C nozzle) enables printing not just PLA/PETG but also PA-CF, PC, and ABS for structural robot parts.

**Top 5 recommendations for Nick:**

| Rank | Project | Why |
|------|---------|-----|
| 1 | **Berkeley Humanoid Lite** | The best balance of open-source, cost (~$5k), active community, proven walking, designed for FDM printing |
| 2 | **ROBOTO ORIGIN** | Full-stack open source, runs 3m/s, ~$6.8k BOM, very active 2026 project |
| 3 | **ToddlerBot** | Stanford-backed, ML-first, compact, 30 DOF, under $6k |
| 4 | **InMoov** | Classic proven platform, cheapest entry point (~$800), massive community |
| 5 | **K-Bot** | Open source, $8,999, full-size, YC-backed (note: company shut down, IP released) |

---

## Comparison Matrix

| Project | License | BOM Cost | Height | Weight | DOF | Print Material | QIDI Compatible | Difficulty | Status |
|---------|---------|----------|--------|--------|-----|----------------|-----------------|------------|--------|
| **Berkeley Humanoid Lite** | MIT (code) / CC-BY-SA 4.0 (HW) | ~$5,000 | 0.8m | 16kg | 22 | PLA (std) | YES | Advanced | Active, buildable NOW |
| **InMoov** | GPL/open | $800-$2,500 | 1.8m | ~30kg | 22-45 | PLA/PETG | YES | Intermediate | Mature, proven |
| **Poppy Humanoid** | CC-BY-SA | $8,000-$9,000 | 84cm | ~3.5kg | 25 | PLA/ABS | YES | Advanced | Mature |
| **Reachy Mini** | Apache 2.0 | $299 | 28cm | 1.5kg | 6 | (pre-built) | N/A | Beginner | Pre-order |
| **Reachy 2** | Apache 2.0 | ~$70,000 | ~1.4m | ~20kg | ~17 | (pre-built) | N/A | Advanced | Available |
| **ToddlerBot** | MIT (code) / CC-BY-NC (HW) | ~$6,000 | 0.56m | 3.4kg | 30 | PLA/PETG | YES | Advanced | Active, 2.0 released |
| **ROBOTO ORIGIN** | GPL v3 | ~$6,800 | 1.25m | 34kg | 23 | Mixed | YES | Advanced | Very active 2026 |
| **AgiBot Lingxi X1** | Open (GitHub) | ~$15,000? | 1.33m | 33kg | 34 | Mixed | Partial | Expert | Open sourced 2024 |
| **pib** | Open source | ~$500-800 | 89cm (upper) | ~5kg | 16+ | PLA/PETG | YES | Beginner | Active, v4 released |
| **K-Bot** | CERN-OHL-S / GPL v3 | $8,999 kit | 1.4m | 35kg | Full | Mixed | Partial | Expert | Company shut down |
| **NAO v6** | Proprietary + SDK | ~$7,500 | 58cm | 5.4kg | 25 | (pre-built) | N/A | Beginner (use) | Available |
| **Fourier GR-1** | Closed (some SDK) | ~$125,000 | 1.65m | 55kg | 25-40 | (pre-built) | N/A | Expert | Available |
| **Unitree G1** | Closed (SDK) | $16,000 | 1.32m | 35kg | 23-43 | (pre-built) | N/A | Expert | Available |
| **EngineAI PM01** | Open SW, closed HW | ~$12,000 | 1.38m | 40kg | 24 | (pre-built) | N/A | Advanced | Available |
| **SO-100 Arm** | Apache 2.0 | ~$100-200 | N/A | ~0.5kg | 6 | PLA/PETG | YES | Beginner | Very active |
| **Apptronik Apollo** | Closed | ~$50-300k | 1.73m | 73kg | 44 | (pre-built) | N/A | Expert | Available |
| **UBTech Walker S** | Closed (SDK) | ~$50-150k | 1.7m | 76kg | 41 | (pre-built) | N/A | Expert | Available |
| **Tesla Optimus** | Closed (patents) | ~$20k (target) | 1.73m | ~57kg | 28+ | (pre-built) | N/A | N/A | In development |

---

## 1. Berkeley Humanoid Lite (PRIORITY PROJECT)

### Overview
**Berkeley Humanoid Lite** is an open-source, sub-$5,000 humanoid robot developed at UC Berkeley, featuring modular 3D-printed cycloidal gearboxes and widely available components. Released in 2025, it's the most distinctive open-hardware humanoid target available right now.

- **Paper:** arXiv:2504.17249 (presented at RSS 2025)
- **Status:** Buildable NOW — v1.1.0 released Sept 2025, community actively building
- **Height:** 0.8m (80cm) — resembles a 5-year-old child
- **Weight:** 16kg
- **DOF:** 22 (6 left arm, 6 right arm, 5 left leg, 5 right leg)
- **Walking:** Yes — RL-based policies with sim-to-real transfer

### License
- **Code:** MIT License
- **Hardware assets (CAD, STLs, docs):** Creative Commons Attribution-ShareAlike 4.0 (CC-BY-SA 4.0)
- This is a genuinely open, commercially-usable license. You CAN sell derivatives.

### Full BOM (~$5,000)

| Category | Component | Qty | Est. Cost (US) | Est. Cost (China) | Source |
|----------|-----------|-----|----------------|-------------------|--------|
| **Actuators** | 6512 Actuator (larger, for legs) | 8 | ~$120 each | ~$90 each | Self-built |
| **Actuators** | 5010 Actuator (smaller, for arms) | 10 | ~$100 each | ~$75 each | Self-built |
| **Motor** | M6C12 150KV BLDC drone motor (MAD Components) | 18 | $84 | $62 | AliExpress |
| **Motor Driver** | B-G431B-ESC1 (STM32-based) | 18 | ~$25 | ~$18 | Mouser/DigiKey |
| **Bearings** | 6811ZZ ball bearing | 18 | ~$5 | ~$3 | AliExpress |
| **Frame** | 2020 Aluminum extrusion | 1 set | ~$30 | ~$20 | Amazon/AliExpress |
| **Computer** | Intel N95 Mini PC | 1 | ~$120 | ~$100 | Amazon/AliExpress |
| **IMU** | Cell-phone grade IMU (over Arduino) | 1 | ~$25 | ~$15 | Amazon |
| **USB-CAN** | USB to CAN adapter | 4 | ~$15 | ~$10 | Amazon |
| **Arduino** | Arduino (for IMU interface) | 1 | ~$10 | ~$5 | Amazon |
| **Battery** | 6S 22.2V 4000mAh LiPo | 1-2 | ~$60 | ~$45 | HobbyKing |
| **Power mgmt** | Power distribution board | 1 | ~$30 | ~$20 | Self-built or bought |
| **Screws/fasteners** | M3, M4, M5 hardware kit | 1 | ~$30 | ~$20 | Amazon |
| **Wiring** | CAN cables, power cables | 1 set | ~$30 | ~$20 | Amazon |
| **Joystick** | Logitech F710 (for control) | 1 | ~$40 | ~$30 | Amazon |
| **3D Filament** | PLA (2-3kg total) | 3kg | ~$60 | ~$45 | Bambu/Hatchbox |
| **Optional** | SteamVR for teleop | 1 set | ~$200+ | ~$200+ | Valve/HTC |
| **TOTAL** | | | **~$4,500-5,500** | **~$3,500-4,500** | |

**Notes on BOM:**
- The 6512 and 5010 actuators are the SAME modular design — different sizes for different torque requirements
- All actuator housings, cycloidal gears, input shafts, and output shafts are 3D printed
- A brass hex stand is embedded in the input shaft for stiffness
- Full BOM spreadsheet with links: https://docs.google.com/spreadsheets/d/1AQEHcH_nPkXYfor2-h7bwNIUMmsePtAm53epnsWgZXc/edit

### Actuator Details (Key Innovation)
The cycloidal gearbox design is the key innovation:
- **Large gear teeth** distribute load across a larger surface area than traditional gears
- This compensates for PLA's inherent weakness vs. CNC aluminum
- **Two actuator sizes:** 6512 (65mm diameter, 12:1 reduction) and 5010 (50mm, 10:1)
- Single encoder on motor shaft (no joint encoder) — requires calibration after each power cycle

### 3D Print Settings
**Critical: Designed for Bambu Lab X1C but works on QIDI Plus 4 Max**

| Setting | Actuator Housing | Actuator Shaft | Robot Body Parts |
|---------|-----------------|----------------|-----------------|
| **Material** | PLA (recommended) | PLA (recommended) | PLA (recommended) |
| **Layer height** | 0.2mm | 0.2mm | 0.2mm |
| **Wall loops** | 4+ | 4+ | 3+ |
| **Top/bottom layers** | 5+ | 5+ | 4+ |
| **Infill** | 40%+ Gyroid | 40%+ Gyroid | 25%+ Gyroid |
| **Print orientation** | Flat (follow docs) | Flat (follow docs) | As oriented in project |
| **Support** | Tree support | Tree support | As needed |
| **Brim** | Recommended for adhesion | Recommended | Optional |

**For QIDI Plus 4 Max specifically:**
- Use the **heated chamber** for better layer adhesion
- PA-CF or PC could be used for high-stress parts (gearbox housings) for extra durability
- However, the design is validated for PLA — don't overcomplicate initially
- Mirror parts along X axis for left/right limbs

### Electronics Architecture
- **Intel N95 Mini PC** — runs RL policies + low-level control
- **CAN 2.0 bus** at 1 Mbps — 4 separate CAN buses (one per limb)
- **USB-to-CAN adapters** — interface between PC and motor drivers
- **B-G431B-ESC1** — STM32-based motor controller running custom firmware
- **Arduino** — reads IMU over USB
- **Communication rate:** 250 Hz to actuators and IMU
- **Power:** 6S LiPo, ~30 min runtime

### Assembly
- **Estimated time:** ~3 days for experienced builder, ~1 week for novice
- **Assembly guide:** https://berkeley-humanoid-lite.gitbook.io/docs/
- **Tools needed:** Standard metric hex keys, soldering iron, multimeter, crimping tool
- **Key steps:** Print actuators first → Assemble and test each actuator → Flash motor firmware → Calibrate joints → Build torso frame → Mount PC and electronics → Attach limbs → Test walking

### Software Stack
- **Simulation:** Isaac Lab (NVIDIA) — RL training
- **Low-level control:** Custom C controller running on the N95 PC
- **Policy deployment:** RL-trained policies transfer zero-shot from sim to real
- **Teleoperation:** SteamVR (optional, for manipulation tasks)
- **ROS2:** Compatible (URDF/MJCF/USD files provided)
- **LeRobot:** Integration available (Hugging Face)

### Community & Resources
- **GitHub:** https://github.com/hybridrobotics/berkeley-humanoid-lite
- **Documentation:** https://berkeley-humanoid-lite.gitbook.io/docs/
- **Discord:** Active community (linked from GitHub)
- **CAD:** Onshape (editable) + STL releases on GitHub
- **Paper:** arXiv:2504.17249
- **Video:** Multiple build and walking videos on project page
- **MakerWorld:** Community 3D print files shared

### Known Issues & Workarounds
- Joint calibration required after each power cycle (no absolute encoders) — automated via provided script
- PLA gears may wear over time — print spares, consider PA-CF for gears on QIDI Plus 4 Max
- CAN bus wiring requires care — follow wiring guide closely
- Initial firmware flashing requires STM32 tools

---

## 2. InMoov

### Overview
The original and most iconic open-source 3D-printed humanoid robot. Created by French sculptor Ga"el Langevin in 2012. It's a life-size, modular humanoid with the largest community in the world.

- **Creator:** Ga"el Langevin (France)
- **Height:** Life-size (~1.75-1.8m depending on build)
- **Weight:** ~30kg
- **DOF:** 22-45 depending on configuration (head: 6, torso: 2, arms: 10, hands: 16, legs: non-motorized by default)
- **Community:** 10,000+ builders worldwide

### License
- **Fully open source** — all CAD, STLs, electronics schematics, and code freely available
- Effectively public domain / GPL-like (no formal single license)
- Can be used commercially

### BOM (~$800-$2,500)

| Component | Details | Cost |
|-----------|---------|------|
| Servo motors (28x) | MG996R, HS-805BB, DS3218, etc. | $200-400 |
| Arduino Mega 2560 | 2 units | $30-50 |
| Nervo Board shields | Custom shield for Arduino | $30-60 (or self-built) |
| Cameras | 2x USB webcams for eyes | $20-40 |
| Kinect sensor | For 3D depth/gesture | $30-50 (used) |
| PIR sensor | Presence detection | $3-5 |
| Speakers | 2x for speech | $10-20 |
| Power supply | 5V/6V bench supply | $30-50 |
| Filament (PLA) | ~5-8kg total | $60-120 |
| Hardware kit | Screws, bearings, cables | $50-100 |
| Electronics misc | Wires, connectors, sensors | $50-100 |
| **TOTAL** | | **$800-2,500** |

### 3D Printability
- **Build volume required:** 12x12x12cm minimum (most parts fit on QIDI Plus 4 Max)
- **Material:** PLA recommended (parts designed for PLA)
- **Number of parts:** ~57 different unique parts, ~200+ total pieces
- **Print time:** 200-400 hours depending on settings
- **Best first print:** Start with fingers, then hand, then forearm

### Electronics
- **2x Arduino Mega 2560** — one for body, one for head
- **Nervo Boards** — custom servo driver shields
- **MyRobotLab** — open-source Java-based control software
- **ROS:** Community ports available
- **Speech recognition:** Supports multiple engines (Google, local)
- **Vision:** OpenCV integration

### Software
- **MyRobotLab** (primary): https://myrobotlab.org/
- **Language support:** Python, Java
- **Features:** Speech recognition, object tracking, gesture recognition, chatbot, weather
- **VR teleoperation:** Community extensions

### Assembly Difficulty
- **Time:** 40-80 hours of assembly
- **Skills:** Basic soldering, 3D printing, Arduino programming
- **Approach:** Modular — build body sections independently (hand, arm, head, torso)

### Resources
- **Website:** https://inmoov.fr/
- **Thingiverse:** https://www.thingiverse.com/inmoov
- **GitHub:** Multiple community repos
- **MyRobotLab:** https://myrobotlab.org/
- **YouTube:** Ga"el Langevin channel has extensive build videos
- **Community:** MyRobotLab forums, Discord

---

## 3. Poppy Humanoid

### Overview
Open-source 3D-printed humanoid from Inria Bordeaux (France). Research and education focused. Uses high-quality Robotis Dynamixel actuators.

- **Origin:** Flowers laboratory at Inria Bordeaux, 2012
- **Managed by:** Poppy Station (non-profit)
- **Height:** 84cm
- **Weight:** ~3.5kg
- **DOF:** 25 (powered by Dynamixel servos)

### License
- **Hardware:** CC-BY-SA (Creative Commons Attribution-ShareAlike)
- **Software:** GPL v3
- **Name "Poppy"** is trademarked — you can build/modify but can't call commercial products "Poppy"

### BOM (~$8,000-$9,000)
- **25x Robotis Dynamixel actuators** (~$200 each = $5,000)
- **XL-320** (smaller) and **MX-28** (larger) Dynamixel servos
- **Raspberry Pi 3/4** as main computer
- **3D printed parts** (STL files on GitHub releases)
- **Power supply, wiring, sensors**
- **Assembly time:** ~7 hours for experienced builder

### Key Features
- **Snap! visual programming** — beginner-friendly
- **Python API** — advanced control
- **Pypot library** — motor control and kinematics
- **Simulation:** V-REP integration
- **Designed for:** Research in education, AI, robotics

### Resources
- **GitHub:** https://github.com/poppy-project/poppy-humanoid
- **BOM:** https://github.com/poppy-project/poppy-humanoid/blob/master/hardware/BOM.md
- **Assembly:** https://github.com/poppy-project/poppy-humanoid/blob/master/hardware/doc/Poppy_Humanoid_assembly_instructions.md
- **STL files:** Available in GitHub releases
- **Forum:** https://forum.poppy-project.org/
- **Full kits:** Available from G"en"eration Robots (Europe)

### QIDI Compatibility
- **YES** — all parts designed for standard desktop FDM printers
- **Material:** PLA or ABS recommended
- **Build volume:** Standard 12x12x12cm sufficient

---

## 4. Reachy Family

### Reachy 2 (Full-Size Humanoid)
- **Price:** ~$70,000 (email sales)
- **License:** Apache 2.0 (SDK and software)
- **Height:** ~1.4m
- **Weight:** ~20kg
- **DOF:** 17 (7 per arm + 3 for head/neck)
- **Status:** Available now, used in Cornell, Carnegie Mellon labs
- **GitHub:** https://github.com/pollen-robotics

### Reachy Mini (Desktop Robot) — 2025
- **Price:** Starting at $299
- **License:** Fully open source (hardware CAD + Python SDK)
- **Height:** 28cm
- **Weight:** 1.5kg
- **DOF:** 6 (head movement)
- **Features:** Expressive LED eyes, head tracking, 360-degree body rotation
- **Versions:** Lite (USB) and Wireless (Raspberry Pi CM4 + WiFi)
- **GitHub:** https://github.com/pollen-robotics/reachy_mini
- **Hugging Face:** Integrated with HF Spaces app store
- **Status:** Pre-order, shipping late 2025

### Reachy 2019 (Original)
- **License:** Apache 2.0
- **Software:** `pip install reachy-2019`
- **3D models and code:** Full open source
- **Documentation:** https://pollen-robotics.github.io/reachy-2019-docs/

### Key Notes
- Pollen Robotics was **acquired by Hugging Face** in April 2025
- Strong integration with LeRobot ecosystem
- The Amazing Hand — fully 3D printed robotic hand for <$200

---

## 5. ToddlerBot

### Overview
Stanford University's open-source humanoid robot designed for ML policy learning. Extremely compact and capable. One of the most ML-compatible platforms available.

- **Institution:** Stanford University (REALab + TML)
- **Paper:** arXiv:2502.00893 (CoRL 2025)
- **Height:** 0.56m (56cm)
- **Weight:** 3.4kg
- **DOF:** 30 (7 per arm, 6 per leg, 2 neck, 2 waist)
- **BOM cost:** Under $6,000

### License
- **Code:** MIT License
- **Design (CAD/STL):** CC-BY-NC (non-commercial) — IMPORTANT for commercial use
- **Onshape CAD:** Available and editable

### Key Features
- **Cartwheel capable** — highly dynamic movement
- **Crawling** — uses arms and legs coordinated
- **VR teleoperation** — Meta Quest 2
- **Omnidirectional walking** — RL with zero-shot sim-to-real
- **Bimanual manipulation** — RGB diffusion policy
- **Payload:** 1.48kg (40% of body weight)
- **Runtime:** 19 minutes continuous walking
- **Repair time:** 21 min printing + 14 min assembly for full restoration

### Actuators
- **ROBOTIS Dynamixel:** 2XC430, 2XL430, XC330, XC430, XM430
- **U2D2** communication adapter
- **Reference:** ROBOTIS sells a ToddlerBot bundle kit

### Electronics
- **Jetson Orin NX 16GB** — onboard computing
- **2x fisheye cameras** — stereo vision
- **2x microphones + speaker**
- **IMU**

### Resources
- **GitHub:** https://github.com/hshi74/toddlerbot
- **Website:** https://toddlerbot.github.io/
- **CAD:** Onshape (linked from GitHub)
- **3D files:** MakerWorld (Bambu Lab)
- **Community:** Discord + WeChat
- **BOM:** https://hshi74.github.io/toddlerbot/hardware/01_bill_of_materials.html

### QIDI Compatibility
- **YES** — all parts 3D printed, designed for FDM
- **Material:** PLA or PETG recommended
- Build volume of QIDI Plus 4 Max more than sufficient

---

## 6. ROBOTO ORIGIN

### Overview
The world's first full-stack open-source bipedal humanoid robot, developed by Xiaomi-backed RoboParty in just 120 days. One of the most exciting new projects of 2026.

- **Company:** RoboParty (Shanghai), founded Feb 2025 by 21-year-old Yi Huang
- **Funding:** $10M seed from Xiaomi, MPCi, Galbot
- **Height:** 1.25m
- **Weight:** 34kg
- **DOF:** 23
- **BOM cost:** ~49,743 CNY (~$6,800 USD)
- **Max speed:** 3 m/s (running!)
- **GitHub stars:** 1,000+ in first month

### License
- **Software:** GPL v3
- **Hardware:** Full open source (structural drawings, EBOM, SOPs, supplier lists)
- All sub-repositories have specific licenses

### Full Stack Open Sourced
| Module | Repository | Content |
|--------|------------|---------|
| Hardware | `rpo_hardware` | CAD, PCB, BOM, structural drawings |
| Deployment | `roboparty_deploy` | ROS2 middleware, control |
| Training | `roboparty_train` | RL in IsaacLab, Sim2Sim |
| Description | `rpo_description` | URDF/MJCF kinematic models |
| Firmware | `roboparty_firmware` | USB2CAN, OrangePi build |
| Navigation | `roboparty_navigation` | Navigation modules |
| XR Teleop | `roboparty_xr_teleop` | VR teleoperation |

### Key Specs
- **Actuators:** DM 4340P and DM 10010L servo actuators
- **Computer:** Orange Pi 5 Plus (RK3588)
- **IMU:** HIPNUC HI13
- **Battery:** 48V 15Ah lithium-ion
- **Software:** ROS2 deployment framework, IsaacLab training
- **Gait:** AMP (Adversarial Motion Priors) for natural walking
- **Motion:** SMPL-X human model adaptation

### Resources
- **GitHub:** https://github.com/Roboparty/roboto_origin
- **Sub-repos:** 8 separate repositories (see table above)
- **Pre-orders:** ~100 development kit pre-orders
- **Community:** QQ Group: 546376843

### QIDI Compatibility
- **YES** — designed for DIY assembly with FDM printing
- Components sourced from Taobao + rapid prototyping services

---

## 7. AgiBot Lingxi X1

### Overview
Fully open-source humanoid robot from Chinese robotics company AgiBot (Zhiyuan Innovation), founded by former Huawei "Genius Youth" Peng Zhihui. One of the most significant open-source releases from China.

- **Company:** AgiBot (Shanghai), founded Feb 2023
- **Open sourced:** October 24, 2024
- **Height:** 1.33m (133cm)
- **Weight:** 33kg
- **DOF:** 34
- **BOM cost:** Estimated ~$15,000 (with proprietary PowerFlow servos)

### License
- **Full open source** — hardware blueprints + software code
- Total data size: 1.2 GB
- Includes: structural drawings, hardware block diagrams, full BOM (every screw and gear), assembly instructions
- **Software:** AimRT framework, URDF, Sim2Sim, RL training code, inference tools

### Key Components
- **PowerFlow servos** — proprietary AgiBot actuators (high torque density)
- **AimRT framework** — open-source robotics middleware
- **Sensors:** RGBD cameras, LiDAR, force sensors, IMU
- **Battery:** ~2 hours

### Important Note
- The **PowerFlow servos are proprietary** — you can't easily source them independently
- This makes self-building more challenging than Berkeley Humanoid Lite
- Better as a reference design than a DIY build

### Resources
- **GitHub:** https://github.com/AgibotTech (multiple repos)
- **Training:** https://github.com/AgibotTech/agibot_x1_train
- **Inference:** https://github.com/AgibotTech/agibot_x1_infer
- **AimRT:** https://www.aimrt.org/
- **Website:** https://www.agibot.com/

---

## 8. pib (Printable Intelligent Bot)

### Overview
German open-source 3D-printable humanoid robot from isento GmbH. Focused on education and makers. Now in version 4.

- **Company:** isento GmbH, Nuremberg, Germany
- **Height:** 89cm (upper body), 68cm arms
- **Weight:** ~5kg
- **Community:** 1,800+ members
- **Used in:** 70+ schools and educational institutions

### License
- **Open source** — STL files, assembly instructions, code freely available
- **Awards:** German Design Award 2025, German Innovation Award 2025

### Key Features (v4)
- **Microphone array** — detects sound direction
- **New speakers** with blue accent lighting
- **3 programmable RGB buttons** on torso
- **Simplified design** — easier motor calibration, better electronics access
- **AI integration** — ChatGPT and other LLMs

### BOM
- **Cost:** ~$500-800 for full build
- **Servos:** Standard hobby servos (MG996R or similar)
- **Electronics:** Arduino/Raspberry Pi based
- **Filament:** ~2-3kg PLA or PETG
- **Shop available:** Complete component sets sold on pib.rocks

### Resources
- **Website:** https://pib.rocks/
- **Shop:** https://pib.rocks/shop/
- **Community:** Discord server
- **Education platform:** pib.Education

### QIDI Compatibility
- **YES** — designed for standard desktop FDM printers
- **Material:** PLA or PETG
- **Difficulty:** Beginner to intermediate

---

## 9. K-Bot (K-Scale Labs)

### Overview
Open-source full-size humanoid robot from Y Combinator startup K-Scale Labs. The company shut down in late 2024 but released all IP under open licenses.

- **Company:** K-Scale Labs (Palo Alto), YC W24 — **SHUT DOWN**
- **Final price:** $8,999 (Founder's Edition)
- **Height:** 1.4m
- **Weight:** 35kg
- **License:** CERN-OHL-S (hardware) / GPL v3 (software)

### Key Details
- Company shut down due to funding issues (couldn't raise Series A)
- All proprietary IP released under open licenses
- Over $2M in pre-orders at time of shutdown
- K-Bot was shipping to customers before shutdown

### Resources
- **GitHub:** https://github.com/kscalelabs/kbot
- **Docs:** https://docs.kscale.dev/
- **Status:** Community can continue development
- **Philosophy:** "Android for the real world"

### Important Caveat
- Company no longer exists — no support, no warranty
- But the open-source community can fork and continue
- Good for experienced builders who can self-support

---

## 10. NAO (SoftBank / Aldebaran)

### Overview
The classic educational humanoid robot. Not 3D-printable but has significant open-source SDK elements. NAOqi OS is accessible for development.

- **Manufacturer:** Aldebaran Robotics (now SoftBank Robotics Europe)
- **Height:** 58cm
- **Weight:** 5.4kg
- **DOF:** 25
- **Price:** ~$7,500 (V6)
- **Units deployed:** 13,000+ in 70+ countries

### Open Elements
- **NAOqi SDK** — Python, C++, Java APIs
- **Choregraphe** — visual programming tool
- **ROS integration** — `nao_bringup` package
- **Simulation** — Webots integration
- **URDF models** — Available for simulation

### Limitations
- **Hardware is NOT open source** — cannot 3D print or modify hardware
- SoftBank Robotics Europe entered receivership in 2025 — future uncertain
- Primarily a closed platform with open SDK

### Resources
- **Documentation:** http://doc.aldebaran.com/
- **Community:** ROS NAO packages, various forums
- **GitHub:** https://github.com/cyberbotics/naoqisim (simulator)

---

## 11. Fourier GR-1

### Overview
Advanced humanoid from Shanghai-based Fourier Intelligence. NOT open source hardware, but some open software elements.

- **Price:** ~$125,000
- **Height:** 1.65m
- **Weight:** 55kg
- **DOF:** 25-40 (depending on configuration)
- **Speed:** 5 km/h walking, 50kg payload
- **Status:** Available, mass-produced

### Open Elements
- NVIDIA Isaac Gym integration for RL training
- Some SDK access
- **NOT a DIY platform** — fully manufactured product

### Resources
- **Website:** https://fourierintelligence.com/gr1/
- **NVIDIA blog:** https://developer.nvidia.com/blog/spotlight-fourier-trains-humanoid-robots-for-real-world-roles-using-nvidia-isaac-gym/

---

## 12. Unitree G1

### Overview
$16,000 commercial humanoid from Unitree (known for quadrupeds). NOT open source, but popular platform.

- **Price:** $16,000 (standard), ~$25,000 (EDU)
- **Height:** 1.32m
- **Weight:** 35kg
- **DOF:** 23-43 (depending on version)
- **Speed:** Various demos show impressive mobility
- **Open elements:** SDK + ROS2 support, but NOT open hardware

### Can You Print a Clone?
- **No complete open-source clone exists**
- Some community projects attempt to replicate the form factor
- The Unitree actuators are proprietary and not available separately
- Better to build Berkeley Humanoid Lite or ROBOTO ORIGIN for a similar form factor

### Resources
- **Website:** https://www.unitree.com/products/g1
- **GitHub:** Unitree provides SDK repos

---

## 13. EngineAI PM01

### Overview
Compact open-software humanoid from Shenzhen-based EngineAI. Open software, closed hardware.

- **Price:** $12,000-$25,500
- **Height:** 1.38m
- **Weight:** 40kg
- **DOF:** 24
- **Speed:** 2 m/s (can run!)
- **Did front flip:** World first for compact humanoid

### Open Elements
- **Open-source software:** Control algorithms on GitHub
- **RL training framework:** Based on MIT Cheetah Software
- **Simulation:** engineai_legged_gym (RL training)
- **Hardware:** NOT open — pre-built robot only

### Key Specs
- **Compute:** Intel N97 CPU + NVIDIA Jetson Orin
- **Camera:** Intel RealSense depth camera
- **Battery:** 2 hours, swappable
- **Waist:** 320-degree rotation

### Resources
- **GitHub:** https://github.com/engineai-robotics/engineai_humanoid
- **RL training:** https://github.com/engineai-robotics/engineai_legged_gym
- **Website:** https://en.engineai.com.cn/

---

## 14. LeRobot SO-100 / SO-101

### Overview
While not a full humanoid, the SO-100/SO-101 arms are the most accessible entry point into the Hugging Face LeRobot ecosystem. Start here if you want to learn before building a full humanoid.

- **SO-100 price:** ~$100
- **SO-101 price:** ~$150-200
- **DOF:** 6 per arm
- **License:** Apache 2.0

### Key Features
- **3D printed** — all structural parts
- **FeeTech STS3215 servos** — $10-15 each
- **LeRobot integration** — train policies on real hardware
- **Teleoperation:** Leader-follower setup (SO-101 supports phone-based teleop)
- **GR00T fine-tuning** — NVIDIA's humanoid model runs on SO-100
- **Bimanual setup** — use two arms together

### Resources
- **BOM + Assembly:** https://github.com/TheRobotStudio/SO-ARM100
- **LeRobot docs:** https://huggingface.co/docs/lerobot
- **Community:** 5,000+ datasets shared on Hugging Face Hub

### QIDI Compatibility
- **YES** — all parts PLA/PETG, standard FDM
- **Perfect first project** for Nick before attempting full humanoid

---

## 15. Apptronik Apollo

### Overview
Commercial humanoid designed for industrial work. Closed source.

- **Price:** $50,000-$300,000
- **Height:** 1.73m
- **Weight:** 73kg
- **DOF:** 44
- **Runtime:** 4 hours (hot-swappable battery)
- **Payload:** 25kg per arm

### Open Elements
- **NONE** — fully proprietary
- Raised $350M from Google and others
- Uses proprietary linear actuators

### Verdict
Not a DIY platform. Reference only.

---

## 16. UBTech Walker Series

### Overview
Chinese humanoid robots from publicly-listed UBTech. Closed source with some open interfaces.

- **Models:** Walker C, S, S2, X, TG Walker
- **Height:** 1.63-1.7m
- **DOF:** 20-52
- **Price:** ~$50,000-$300,000
- **Features:** Factory deployment (NIO, BYD, Foxconn)

### Open Elements
- **TG Walker** (research version): Open interfaces for joints and sensors
- **URDF models:** Available for simulation
- **RL training frameworks:** Open-source components
- **Datasets:** To be released progressively
- **ROSA 2.0:** Integrates with ROS2

### Verdict
Not a 3D-printable platform. Reference for commercial state-of-the-art.

---

## 17. Tesla Optimus

### Overview
Tesla's humanoid robot. Closed source with patent publications.

- **Target price:** $20,000-$30,000
- **Height:** 1.73m
- **Weight:** ~57kg
- **DOF:** 28+
- **Status:** In development, summer 2026 low-volume production target

### Open Elements
- **Patents only** — published April 2026 revealing hand architecture
- 25-actuator, 22-DoF hand design detailed
- NOT open source — patents are defensive, not permissive

### Verdict
Not a DIY platform. Reference only.

---

## 18. Other Notable Projects

### Booster Robotics T1 / K1 Geek
- **Company:** Booster Robotics (China)
- **K1 Geek:** 95cm, 19.5kg, 22 DOF, $5,999
- **RoboCup 2025 KidSize champion**
- **Open source:** Development platform, ROS2 support
- **Website:** https://www.boostertech.co/

### Hope-JR Humanoid Arm
- **Integrated with LeRobot**
- **Open source** arm design
- **GitHub:** https://github.com/TheRobotStudio/HopeJr

### dmBot
- **Height:** 0.76m, 15kg, 18 DOF
- **BOM:** ~$3,000
- **Open source:** Yes (per comparison table in Berkeley paper)

### Noetix N2
- **Height:** 1.18m, 30kg, 18 DOF
- **Company:** Noetix Robotics
- **Status:** Available

---

## Best First Print Order for Nick at MEOK Labs

### Phase 1: Build Skills (Week 1-2)
1. **Print SO-100 arm** (~$100, 20-30 hrs printing)
   - Learn LeRobot ecosystem
   - Understand servo control, teleoperation
   - Get familiar with policy training

### Phase 2: Validate Printer for Humanoid Parts (Week 2-3)
2. **Print one Berkeley Humanoid Lite actuator**
   - Print the 5010 actuator housing + shaft
   - Test fit with bearings and motor
   - Validate your print settings
   - This is the CORE building block — master this first

### Phase 3: Full Actuator Production (Week 3-5)
3. Print all 18 actuator housings (10x 5010, 8x 6512)
4. Print all cycloidal gears and shafts
5. Assemble and test each actuator individually

### Phase 4: Frame and Electronics (Week 5-7)
6. Print torso frame parts
7. Print leg and arm structural parts
8. Cut aluminum extrusion
9. Flash motor firmware to all 18 ESCs

### Phase 5: Integration (Week 7-9)
10. Mount all actuators to frame
11. Wire CAN buses
12. Install Intel N95 PC, battery, IMU
13. Run calibration scripts

### Phase 6: Software and Walking (Week 9-12)
14. Install low-level control software
15. Train RL policy in Isaac Lab (or use pretrained)
16. Deploy to real robot
17. TUNE, TUNE, TUNE

---

## QIDI Plus 4 Max Recommended Settings

### For Berkeley Humanoid Lite (PLA)
```
Nozzle: 0.4mm (stock)
Layer height: 0.2mm
Temperature: 210C / 60C bed
Chamber: 45C (heated chamber advantage!)
Walls: 4
Top/bottom: 5
Infill: 40% Gyroid
Speed: 50mm/s outer, 80mm/s inner
Support: Tree (auto)
Adhesion: Brim for large parts
```

### For High-Stress Parts (Optional PA-CF Upgrade)
```
Nozzle: 0.6mm hardened steel (for carbon fiber)
Temperature: 280-300C / 80C bed
Chamber: 60C (use heated chamber!)
Dry filament: PA-CF is hygroscopic — dry at 80C for 4+ hrs
Parts to print in PA-CF: Cycloidal gears, output shafts
Parts to keep in PLA: Housing (easier to print, less warping)
```

### QIDI Advantages for This Project
| Feature | Why It Matters |
|---------|---------------|
| **Heated chamber** | Better layer adhesion for large structural parts |
| **350C nozzle** | Enables PA-CF, PC for high-strength gears |
| **Direct drive** | Better extrusion control for abrasive filaments |
| **Large build volume** | Can print multiple parts at once |
| **Multi-material** | Could use different materials for different parts |

---

## Resources & Links

### Essential Links for Nick

| Resource | URL |
|----------|-----|
| **Berkeley Humanoid Lite Main Repo** | https://github.com/hybridrobotics/berkeley-humanoid-lite |
| **BHL Documentation** | https://berkeley-humanoid-lite.gitbook.io/docs/ |
| **BHL BOM Spreadsheet** | https://docs.google.com/spreadsheets/d/1AQEHcH_nPkXYfor2-h7bwNIUMmsePtAm53epnsWgZXc/edit |
| **BHL Assets (CAD/URDF)** | https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets |
| **BHL Low-level Control** | https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Lowlevel |
| **BHL Releases** | https://github.com/HybridRobotics/Berkeley-Humanoid-Lite/releases |
| **BHL arXiv Paper** | https://arxiv.org/abs/2504.17249 |
| **InMoov** | https://inmoov.fr/ |
| **Poppy Humanoid** | https://github.com/poppy-project/poppy-humanoid |
| **ToddlerBot** | https://github.com/hshi74/toddlerbot |
| **ROBOTO ORIGIN** | https://github.com/Roboparty/roboto_origin |
| **AgiBot X1** | https://github.com/AgibotTech/agibot_x1_train |
| **pib Robot** | https://pib.rocks/ |
| **K-Bot** | https://github.com/kscalelabs/kbot |
| **LeRobot** | https://github.com/huggingface/lerobot |
| **SO-100 Assembly** | https://github.com/TheRobotStudio/SO-ARM100 |
| **Reachy Mini** | https://github.com/pollen-robotics/reachy_mini |
| **Pollen Robotics** | https://www.pollen-robotics.com/ |
| **EngineAI GitHub** | https://github.com/engineai-robotics/engineai_humanoid |
| **Unitree G1** | https://www.unitree.com/products/g1 |

### Where to Buy Parts

| Vendor | Best For |
|--------|----------|
| **AliExpress** | Motors, bearings, hardware, electronics (China prices) |
| **Amazon (US)** | Faster shipping, verified BOM links |
| **Mouser/DigiKey** | B-G431B-ESC1 motor drivers, electronic components |
| **RobotShop/Robotis** | Dynamixel servos (for Poppy/ToddlerBot) |
| **HobbyKing** | LiPo batteries |
| **MakerWorld** | Community 3D print profiles |
| **Onshape** | Berkeley Humanoid Lite CAD (free to view/copy) |

### Communities

| Community | Platform | Link/Access |
|-----------|----------|-------------|
| **Berkeley Humanoid Lite** | Discord | Linked from GitHub |
| **Berkeley Humanoid Lite** | WeChat | China community |
| **InMoov** | MyRobotLab forums | https://myrobotlab.org/ |
| **ToddlerBot** | Discord | Linked from GitHub |
| **ToddlerBot** | WeChat | China community |
| **pib** | Discord | https://pib.rocks/ |
| **K-Scale** | Discord | https://docs.kscale.dev/ |
| **LeRobot** | Discord | Hugging Face server |
| **ROBOTO ORIGIN** | QQ Group | 546376843 |
| **General humanoid** | Reddit r/robotics | https://reddit.com/r/robotics |

---

*Document compiled from extensive research of GitHub, arXiv, project websites, manufacturer documentation, and community resources. All information current as of July 2026.*
