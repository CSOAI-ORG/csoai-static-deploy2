# Open Source 3D-Printable Quadruped Robots & Robotic Arms Research
## For Nick at MEOK Labs - QIDI Plus 4 Max Compatible Projects

**Research Date:** July 2025
**Printer Reference:** QIDI Plus 4 Max (420 x 420 x 500 mm build volume, CoreXY, supports PLA/PETG/ABS/TPU/PC/Nylon/Carbon Fiber)

---

## Table of Contents
1. [Overview & How to Use This Guide](#overview)
2. [Quick Comparison Table - Quadruped Robots](#quadruped-comparison-table)
3. [Quick Comparison Table - Robotic Arms](#robotic-arm-comparison-table)
4. [Quadruped Robots - Detailed Profiles](#quadruped-details)
5. [Robotic Arms - Detailed Profiles](#robotic-arm-details)
6. [New & Emerging Projects (2024-2026)](#new-projects)
7. [Electronics & Components Sourcing Guide](#electronics-guide)
8. [QIDI Plus 4 Max Print Settings](#print-settings)
9. [Recommended Build Order for MEOK Labs](#recommended-build-order)

---

## 1. Overview & How to Use This Guide <a name="overview"></a>

This guide catalogs every major open-source quadruped robot and robotic arm that can be 3D printed on a QIDI Plus 4 Max or similar large-format 3D printer. For each project, you'll find:

- **License**: Open source license type
- **BOM Cost**: Estimated total parts cost
- **Print Time**: Estimated printing hours
- **DOF**: Degrees of freedom
- **Weight**: Final assembled weight
- **QIDI Compatible**: Whether the parts fit on a QIDI Plus 4 Max
- **ROS2 Support**: Robot Operating System 2 compatibility
- **Difficulty**: Beginner / Intermediate / Advanced

### QIDI Plus 4 Max Key Specs for Reference:
| Spec | Value |
|------|-------|
| Build Volume | 420 x 420 x 500 mm (XYZ) |
| Max Nozzle Temp | 350C |
| Max Bed Temp | 120C |
| Supported Materials | PLA, PETG, ABS, TPU, PC, Nylon, Carbon Fiber |
| Bed Type | PEI Spring Steel |
| Controller | Klipper-based |

---

## 2. Quick Comparison Table - Quadruped Robots <a name="quadruped-comparison-table"></a>

| Project | License | BOM Cost | Print Time | DOF | Weight | QIDI Compatible | ROS2? | Difficulty |
|---------|---------|----------|------------|-----|--------|-----------------|-------|------------|
| **Spot Micro** | CC (files) | ~$300-500 | ~80-120h | 12 | ~2-3 kg | YES | Community ROS1/2 | Intermediate |
| **Mini Pupper** (MangDang) | MIT | ~$500-800 kit | ~40-60h | 12 | 560g | YES | YES Native | Beginner |
| **Stanford Doggo** | BSD/MIT | ~$1,500-2,000 | ~100-150h | 12 | ~5 kg | YES (body parts) | Community | Advanced |
| **Pupper v3** (Stanford) | Open Source | ~$2,000 | ~150h+ | 12 | TBD | YES | YES Planned | Advanced |
| **MIT Mini Cheetah** | BSD-3 | ~$10,000-15,000 | N/A (mostly CNC) | 12 | ~9 kg | Partial | YES (Cheetah-Software) | Expert |
| **OpenCat (Bittle/Nybble)** | LGPL | $250-350 kit | Pre-printed | 8-9 | ~300g | N/A (buy kit) | Community | Beginner |
| **Xiaomi CyberDog 2** | Partial Open | $1,789 retail | N/A (commercial) | 12 | 8.9 kg | N/A | YES | Intermediate |
| **Unitree Go2** | SDK Available | $1,600+ retail | N/A (commercial) | 12 | ~15 kg | N/A | YES Native | Intermediate |
| **Solo12 (ODRI)** | BSD-3 | ~$3,000-5,000 kit | Some 3D printed | 12 | 2.5 kg | Partial | YES | Advanced |
| **Champ (ROS Framework)** | BSD | Varies | Varies | Varies | Varies | YES | YES Native | Intermediate |
| **EG01 (NavBot)** | Open Source | ~$50-100 | ~20-30h | 8 | ~500g | YES | NO | Beginner |

---

## 3. Quick Comparison Table - Robotic Arms <a name="robotic-arm-comparison-table"></a>

| Project | License | BOM Cost | Print Time | DOF | Weight | QIDI Compatible | ROS2? | Difficulty |
|---------|---------|----------|------------|-----|--------|-----------------|-------|------------|
| **BCN3D Moveo** | Open Source | ~$300-500 | ~80-100h | 5 | ~5 kg | YES | Community | Intermediate |
| **Thor** | CC-BY-SA-4.0 | ~$350 (EUR) | ~60-80h | 6 | ~3 kg | YES | YES (Docker) | Intermediate |
| **AR2/AR3 (Annin Robotics)** | CC | ~$1,500-2,000 | ~100h+Alu parts | 6 | ~8 kg | YES (printed ver) | Community | Advanced |
| **AR4 (Annin Robotics)** | CC/Paid | ~$2,000 | ~80h+CNC parts | 6 | ~10 kg | Partial | Community | Advanced |
| **Kauda** | Open Source | ~$200-400 | ~40-60h | 4-5 | ~2 kg | YES | NO | Beginner |
| **Kauda Pro** | Open Source | ~$400-600 | ~50-70h | 5-6 | ~3 kg | YES | NO | Intermediate |
| **SmallRobotArm (Skyentific)** | GPL-3.0 | ~$300-500 | ~60-80h | 6 | ~2.5 kg | YES | Community | Intermediate |
| **Arctos Arm** | Paid CAD (~EUR40) | ~$300-400 | ~80-100h (3kg PLA) | 6 | ~4 kg | YES | YES (GitHub) | Intermediate |
| **HELENE Arm** | Open Source | ~$1,000 (EUR) | ~5 days print | 6 | ~5 kg | YES | YES Native | Intermediate |
| **Dobot Magician** | SDK Available | $1,695 retail | N/A | 4 | 11.3 kg | N/A | SDK | Beginner |
| **uArm Swift Pro** | Open SDK | ~$800-1,000 | N/A (acrylic) | 4 | ~2.2 kg | N/A | Community | Beginner |
| **UFactory Lite 6** | Open API | ~$3,000 | N/A (commercial) | 6 | 8 kg | N/A | YES | Beginner |
| **Reachy 2 (Pollen)** | Open Source | ~$10,000+ | Some 3D printed | 7 (per arm) | ~15 kg total | Partial | YES Native | Advanced |
| **Tactigon T-SKIN** | Open SDK | ~$150-200 (controller) | N/A | N/A | N/A | N/A | NO | Beginner |
| **MeArm V0.4** | CC | ~$30-50 | ~8-12h | 4 | ~200g | YES | NO | Beginner |
| **6AR Robot Arm** | Open Source | ~$500-800 | ~60-80h | 6 | ~4 kg | YES | Planned | Intermediate |

---

## 4. Quadruped Robots - Detailed Profiles <a name="quadruped-details"></a>

---

### Spot Micro (Boston Dynamics Spot Clone)
**Status:** Active community project | **Original Designer:** KDY0523 | **Software:** mike4192 and others

Spot Micro is the most popular 3D-printable Boston Dynamics Spot clone. The original CAD was created by KDY0523 on Thingiverse in 2019, and multiple software stacks have been developed by the community since. It is one of the most iconic DIY quadruped projects.

| Attribute | Details |
|-----------|---------|
| **License** | CC (3D files), Various (software) |
| **BOM Cost** | $300-500 (budget servos) / $600-800 (quality servos) |
| **Print Time** | ~80-120 hours |
| **DOF** | 12 (3 per leg) |
| **Weight** | ~2-3 kg |
| **QIDI Compatible** | YES - All parts fit comfortably |
| **ROS2 Support** | Community (ROS1 Kinetic confirmed, ROS2 ports exist) |
| **Difficulty** | Intermediate |

#### Key Components (BOM)
| Part | Qty | Est. Cost | Source |
|------|-----|-----------|--------|
| MG996R or HV5523MG/CLS6336HV servos | 12 | $60-150 | AliExpress, Amazon |
| Raspberry Pi 3B+/4 | 1 | $35-75 | Raspberry Pi retailers |
| PCA9685 16-Channel PWM Driver | 1 | $5-10 | AliExpress |
| MPU-6050 IMU | 1 | $3-5 | AliExpress |
| HC-SR04 Ultrasonic sensors | 2 | $3 | AliExpress |
| HC-06 Bluetooth module | 1 | $5-8 | AliExpress |
| 2S LiPo Battery 4000mAh | 1 | $20-30 | Hobby shops |
| 5V UBEC regulator | 1 | $5 | AliExpress |
| F625zz Flange Bearings | 8 | $8 | AliExpress |
| M3/M4/M5 Hardware | Set | $15-20 | Hardware store |
| 3D Printing Filament (PETG/PLA) | ~1.5kg | $20-40 | 3D printing store |
| **Total** | | **$194-363** | |

#### Source Links
- **Thingiverse (Original CAD):** https://www.thingiverse.com/thing:3445283
- **GitHub (mike4192 ROS Software):** https://github.com/mike4192/spotMicro
- **GitHub (MZandtheRaspberryPi demo):** https://github.com/MZandtheRaspberryPi/spot_micro_demo

#### Electronics Stack
- **Primary Controller:** Raspberry Pi 3B+/4
- **Servo Driver:** PCA9685 over I2C
- **IMU:** MPU-6050 or MPU-9250
- **Software:** Ubuntu + ROS Kinetic/Melodic/Noetic (ROS2 community ports available)
- ** gait control:** Inverse kinematics with sinusoidal leg trajectories

#### Assembly Notes
- Print in PETG for durability (body) and TPU for feet
- Shoulder reinforcement parts recommended (from mike4192's repo)
- Servo calibration is critical - use a calibration platform
- ~4-6 weeks build time for a first-timer

#### Video Tutorials
- KDY0523 Assembly Part 1: https://youtu.be/03RR-mz2hwA
- KDY0523 Assembly Part 2: https://youtu.be/LV5vvmhwtxM
- Multiple community build videos on YouTube

#### Community Support
- **Level:** Medium - Active GitHub repos, scattered documentation
- **GitHub Topics:** https://github.com/topics/spotmicro
- **Note:** Multiple competing software stacks can be confusing for beginners

---

### Mini Pupper (by MangDang)
**Status:** Commercial product + Open Source | **Origin:** Stanford Pupper collaboration

Mini Pupper is a palm-sized, 12-DOF quadruped robot based on Stanford's Pupper platform. Successfully Kickstarted in 2021 (1000% funded in 1 day). Endorsed by Raspberry Pi. Now supports multimodal generative AI features.

| Attribute | Details |
|-----------|---------|
| **License** | MIT (software), Open Hardware |
| **BOM Cost** | $500-800 (self-sourced) / $599-799 (kit) |
| **Print Time** | ~40-60 hours |
| **DOF** | 12 (3 per leg) |
| **Weight** | 560g |
| **QIDI Compatible** | YES - Compact design |
| **ROS2 Support** | YES - Native ROS 2 + ROS 1 support |
| **Difficulty** | Beginner |

#### Key Components (BOM)
| Part | Qty | Est. Cost | Source |
|------|-----|-----------|--------|
| Raspberry Pi 4B (recommended) | 1 | $55-75 | Raspberry Pi retailers |
| Custom controller board (from MangDang) | 1 | $50-80 | Tindie, MangDang |
| High-torque digital servos (PDI-HV5523MG or better) | 12 | $60-120 | AliExpress, Kit |
| 320x240 IPS LCD Display | 1 | $15-25 | AliExpress |
| 800mAh LiPo Battery | 1 | $15-20 | MangDang |
| 3D Printed Chassis Parts | Set | ~$20 filament | Self-print |
| OAK-D Lite AI Camera (optional) | 1 | $100-150 | Luxonis |
| LiDAR Module (optional, for SLAM) | 1 | $100-200 | Various |
| **Total (self-sourced)** | | **$415-710** | |

#### Source Links
- **GitHub:** https://github.com/mangdangroboticsclub
- **Hackster.io:** https://www.hackster.io/mangdang
- **Project Page:** https://minipupperdocs.readthedocs.io/

#### Electronics Stack
- **Primary Controller:** Raspberry Pi 4B
- **Servo Controller:** Custom MangDang board (PCA9685-based)
- **IMU:** Integrated on controller board
- **Display:** 320x240 IPS LCD for facial expressions
- **Software:** Ubuntu + ROS 1/ROS 2, OpenCV
- **AI:** OpenVINO, OAK-D Lite support

#### Capabilities
- Walk, trot, bound gait patterns
- SLAM (with LiDAR or camera)
- Autonomous navigation
- AI vision (object detection, tracking)
- Facial animation customization
- OpenCV integration

#### Assembly Notes
- Kit includes most parts pre-sorted
- Assembly time: ~4-8 hours
- Calibration via web interface
- Extensive documentation available

#### Community Support
- **Level:** HIGH - Active Discord, workshops at ROS/IEEE events
- Endorsed by Raspberry Pi
- Featured on Kickstarter (2021), CES 2024
- Active contributor community

---

### Stanford Doggo & Pupper v3
**Status:** Pupper v3 active (Doggo deprecated) | **Origin:** Stanford Student Robotics

Stanford Doggo was a record-breaking open-source quadruped (highest vertical jumping agility of any robot). The project has been deprecated in favor of Pupper v3, which is the current-generation platform from Stanford.

#### Stanford Doggo (Legacy)
| Attribute | Details |
|-----------|---------|
| **License** | BSD/MIT (code), Open Hardware |
| **BOM Cost** | ~$1,500-2,000 |
| **Print Time** | ~100-150 hours |
| **DOF** | 12 |
| **Weight** | ~5 kg |
| **QIDI Compatible** | YES |
| **ROS2 Support** | Community only (originally ROS Kinetic) |
| **Difficulty** | Advanced |

#### Key Components - Stanford Doggo
- 4x ODrive motor controllers
- 8x brushless motors (hip/knee)
- Teensy 3.6 microcontroller
- Custom 3D printed body + machined leg parts
- XBee wireless module
- IMU

#### Pupper v3 (Current - 2024/2025)
| Attribute | Details |
|-----------|---------|
| **License** | Fully Open Source |
| **BOM Cost** | ~$2,000 |
| **Print Time** | ~150+ hours |
| **DOF** | 12 |
| **Weight** | TBD (~3-5 kg estimated) |
| **QIDI Compatible** | YES |
| **ROS2 Support** | Planned |
| **Difficulty** | Advanced |

#### Pupper v3 Key Components
| Part | Details |
|------|---------|
| 400W GIM4305 brushless motors | High-torque actuators |
| Raspberry Pi 5 | Main controller |
| Luxonis SR Depth Camera | Vision system |
| LCD Screen | Debug + facial expressions |
| Custom 3D printed body | Full CAD available |

#### Source Links
- **Stanford Doggo GitHub:** https://github.com/Nate711/StanfordDoggoProject
- **Pupper v3 Docs:** https://pupper-v3-documentation.readthedocs.io/
- **Stanford Student Robotics:** http://roboticsclub.stanford.edu/
- **Boston Robot Hackers (Pupper v3 build):** https://bostonrobothackers.com/projects/pupper.html

#### Capabilities
- Highest vertical jumping agility record
- Trot, walk, bound, pronk gaits
- Backflip capable
- Dynamic balance on varied terrain
- Pupper v3 adds: OpenAI Realtime API voice interaction, reinforcement learning locomotion, VLM perception

#### Assembly Notes
- ODrive calibration is complex
- Requires understanding of FOC motor control
- Mechanical assembly is involved
- Pupper v3 build instructions being actively developed

---

### MIT Mini Cheetah / Cheetah Software
**Status:** Research-grade, partially open source | **Origin:** MIT Biomimetics Lab

The MIT Mini Cheetah is NOT fully open source as a 3D-printable project, but significant components are available. Best suited for research labs with machining capabilities.

| Attribute | Details |
|-----------|---------|
| **License** | BSD-3 (software), Partial (hardware) |
| **BOM Cost** | ~$10,000-15,000 |
| **Print Time** | N/A (CNC machined primarily) |
| **DOF** | 12 |
| **Weight** | ~9 kg |
| **QIDI Compatible** | Partial (some brackets/fixtures) |
| **ROS2 Support** | NO (custom software stack) |
| **Difficulty** | Expert |

#### Open Source Elements Available
- **Cheetah Software:** https://github.com/mit-biomimetics/Cheetah-Software
- **Motor Controller Hardware:** https://github.com/bgkatz/3phase_integrated
- **SPIne Hardware:** https://github.com/bgkatz/SPIne
- **Motor Controller Firmware:** https://os.mbed.com/users/benkatz/code/Hobbyking_Cheetah_Compact_DRV8323/

#### Key Notes
- Body is CNC machined aluminum, not 3D printed
- Custom-designed motor controllers required
- Requires advanced knowledge of power electronics
- Not recommended as a first quadruped project
- For MEOK Labs: Use as reference for motor control algorithms only

---

### OpenCat / Petoi (Nybble & Bittle)
**Status:** Active commercial product | **Origin:** Dr. Rongzhong Li, 2016

OpenCat is the most-starred open-source quadruped robot framework on GitHub. Bittle is the current robot dog model; Nybble is the robot cat. At ~$250-350, it is the most accessible entry point.

| Attribute | Details |
|-----------|---------|
| **License** | LGPL (OpenCat framework) |
| **BOM Cost** | $250-350 (pre-assembled kit) |
| **Print Time** | N/A (Injection molded parts) |
| **DOF** | 9 (Bittle) / 8 (Nybble) |
| **Weight** | ~300g |
| **QIDI Compatible** | N/A (buy kit, but mods can be printed) |
| **ROS2 Support** | Community documented |
| **Difficulty** | Beginner |

#### Source Links
- **GitHub (OpenCat):** https://github.com/PetoiCamp/OpenCat
- **GitHub (OpenCat ESP32):** https://github.com/PetoiCamp/OpenCat-Quadruped-Robot
- **Website:** https://www.petoi.com/
- **Documentation:** https://docs.petoi.com/

#### Key Components (Included in Kit)
- NyBoard V1/V2 (ATmega328P-based) or BiBoard (ESP32)
- 9x P1S servo motors (Bittle)
- 7.4V Li-ion battery pack
- Bluetooth/WiFi dongles
- Infrared remote

#### Programming Options
- **Block-based:** Petoi Coding Blocks (Scratch-like)
- **C++:** Arduino IDE, OpenCat framework
- **Python:** petoi Python library
- **Advanced:** Raspberry Pi or NVIDIA Jetson Nano add-on

#### Community Support
- **Level:** VERY HIGH - 15,000+ units shipped, 60+ countries
- Active forums, competitions, educational programs
- Used in universities and K-12 programs worldwide

#### QIDI Plus 4 Relevance
- While Bittle itself is injection molded, OpenCat can be ported to custom 3D-printed robot frames
- Use OpenCat software stack for any custom servo-based quadruped
- Excellent starting point for learning quadruped locomotion control

---

### Xiaomi CyberDog 2
**Status:** Commercial product with open-source elements | **Released:** 2023

| Attribute | Details |
|-----------|---------|
| **License** | Partial open source (Ubuntu/ROS 2 based) |
| **BOM Cost** | $1,789 (retail) |
| **Print Time** | N/A (commercial product) |
| **DOF** | 12 |
| **Weight** | 8.9 kg |
| **QIDI Compatible** | N/A |
| **ROS2 Support** | YES - Native |
| **Difficulty** | Intermediate |

#### Key Specs
- NVIDIA Jetson Xavier NX (6-core, 384-core GPU, 8GB RAM)
- 19 high-precision sensors (LiDAR, Intel RealSense D430, RGB camera, 4x ToF)
- CyberGear micro-actuators
- Max speed: 1.6 m/s
- Max payload: 1 kg
- Runtime: 90 minutes
- Continuous backflip capability

#### Developer Access
- Runs Ubuntu 18.04 with ROS 2
- XiaoAI smart home integration
- Voice control
- Open API for development

#### Source Links
- **Product Page:** https://www.mi.com/cyberdog2
- **Origin of Bots Specs:** https://www.originofbots.com/robot-dog/xiaomi-cyberdog-2

#### MEOK Labs Note
Not a 3D-printable project, but included as the most affordable retail quadruped with ROS 2 and open API access. Good reference platform.

---

### Unitree Go2
**Status:** Commercial product with extensive SDK | **Released:** 2023-2024

| Attribute | Details |
|-----------|---------|
| **License** | SDK available, URDF open sourced |
| **BOM Cost** | $1,600+ (retail) |
| **Print Time** | N/A (commercial product) |
| **DOF** | 12 |
| **Weight** | ~15 kg |
| **QIDI Compatible** | N/A |
| **ROS2 Support** | YES - Native unitree_ros2 package |
| **Difficulty** | Intermediate |

#### Key Specs
- Max speed: 3.7 m/s (limit ~5 m/s)
- Slope capability: +/- 40 degrees
- Max step height: 16cm
- 8-core ARM processor built-in
- WiFi 6, Bluetooth 5.2, 4G (built-in)
- 64GB storage
- Runtime: 1-2h (8Ah battery) / 3-5h (15Ah battery)

#### Open Source Resources
- **GitHub:** https://github.com/unitreerobotics
- **unitree_ros2:** ROS 2 development package
- **unitree_sdk2:** SDK for Go2, B2, H1, G1
- **unitree_guide:** Open source control algorithms
- **URDF files:** All robot kinematics available

#### MEOK Labs Note
Best retail quadruped for ROS 2 research. Not printable but has the most open-source software stack of any commercial quadruped.

---

### Solo12 (Open Dynamic Robot Initiative)
**Status:** Active research platform | **Origin:** Max Planck Institute + NYU + LAAS/CNRS

Solo12 is a 2.5kg research-grade quadruped with torque-controlled brushless motors. Mostly 3D-printable with off-the-shelf components.

| Attribute | Details |
|-----------|---------|
| **License** | BSD-3-Clause |
| **BOM Cost** | ~$3,000-5,000 (kit from PAL Robotics) |
| **Print Time** | Some 3D printed parts (body) |
| **DOF** | 12 |
| **Weight** | 2.5 kg |
| **QIDI Compatible** | Partial (body structure) |
| **ROS2 Support** | YES (through community) |
| **Difficulty** | Advanced |

#### Key Features
- 12 identical actuator modules (modular design)
- Torque-controlled brushless motors
- Dual-stage 9:1 timing belt transmission per joint
- Custom field-oriented control (FOC) motor drivers
- 1kHz control loop over WiFi/Ethernet
- Dynamic tricks: jumps waist-high, lands on feet

#### Source Links
- **ODRI Website:** https://open-dynamic-robot-initiative.github.io/
- **GitHub:** https://github.com/open-dynamic-robot-initiative
- **PAL Robotics (kits):** https://solo.pal-robotics.com/
- **Hardware Repo:** https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware

#### MEOK Labs Note
Excellent research platform. The actuator module design is particularly valuable as reference for custom builds. Kits available from PAL Robotics.

---

### Champ (ROS Quadruped Framework)
**Status:** Active | **Author:** Juan Miguel Jimeno

Champ is NOT a physical robot but a ROS-based software framework that can control multiple quadruped hardware configurations. Use it as the software stack for any custom build.

| Attribute | Details |
|-----------|---------|
| **License** | BSD-3-Clause |
| **BOM Cost** | Varies (software only) |
| **DOF** | Configurable |
| **ROS2 Support** | YES |
| **Difficulty** | Intermediate |

#### Source Links
- **GitHub:** https://github.com/chvmp/champ
- **Supports:** ROS 1 and ROS 2
- **Compatible with:** Spot Micro, custom builds, Gazebo simulation

---

### EG01 NavBot (New - Educational Quadruped)
**Status:** Active open source project | **Origin:** Fuwei/NavBot | **Release:** 2024

A low-cost ESP32-based educational quadruped robot. Extremely affordable entry point.

| Attribute | Details |
|-----------|---------|
| **License** | Open Source |
| **BOM Cost** | ~$50-100 |
| **Print Time** | ~20-30 hours |
| **DOF** | 8 |
| **Weight** | ~500g |
| **QIDI Compatible** | YES |
| **ROS2 Support** | NO |
| **Difficulty** | Beginner |

#### Source Links
- **GitHub:** https://github.com/fuwei007/NavBot-EG01
- **Product:** https://navbot.com/

---

## 5. Robotic Arms - Detailed Profiles <a name="robotic-arm-details"></a>

---

### BCN3D Moveo
**Status:** Classic reference design | **Origin:** BCN3D Technologies + Catalunya Education Dept | **Year:** 2016

BCN3D Moveo is the grandfather of open-source 3D-printed robot arms. Fully documented, actively used in education worldwide.

| Attribute | Details |
|-----------|---------|
| **License** | Open Source (not commercialized) |
| **BOM Cost** | ~$300-500 |
| **Print Time** | ~80-100 hours |
| **DOF** | 5 |
| **Weight** | ~5 kg |
| **QIDI Compatible** | YES - All parts fit easily |
| **ROS2 Support** | Community (Arduino-based, ROS serial possible) |
| **Difficulty** | Intermediate |

#### Key Components (BOM)
| Part | Qty | Est. Cost | Source |
|------|-----|-----------|--------|
| NEMA 17 Stepper Motors | 5 | $50-75 | AliExpress, Amazon |
| A4988 Stepper Drivers | 5 | $5-10 | AliExpress |
| Arduino Mega 2560 | 1 | $15-25 | AliExpress |
| CNC Shield V3 | 1 | $5-10 | AliExpress |
| GT2 Belts & Pulleys | Set | $15-25 | AliExpress |
| 608ZZ Bearings | Set | $10-15 | AliExpress |
| Threaded Rods (M5/M8) | Set | $10-15 | Hardware store |
| Power Supply 12V/5A | 1 | $15-25 | Amazon |
| Gripper Servo (MG996R) | 1 | $5-10 | AliExpress |
| 3D Printing Filament (PLA) | ~2-3kg | $30-60 | 3D printing store |
| **Total** | | **$160-270** | |

#### Source Links
- **GitHub:** https://github.com/BCN3D/BCN3D-Moveo
- **Website:** https://bcn3d.com/bcn3d-moveo-the-future-of-learning-robotic-arm/
- **Thingiverse:** https://www.thingiverse.com/thing:1693444
- **Assembly Video:** https://www.youtube.com/watch?v=XSY0kieEL8A

#### Electronics Stack
- **Controller:** Arduino Mega 2560 + CNC Shield V3
- **Drivers:** A4988 or DRV8825
- **Firmware:** GRBL-based or custom Arduino firmware
- **Communication:** USB serial

#### Capabilities
- Pick and place operations
- Teaching mode (manual guidance)
- G-code compatible motion
- 5-axis coordinated movement
- Optional pneumatic gripper

#### Assembly Notes
- Print all parts in PLA (body) with 20-30% infill
- GT2 belt tension is critical
- Arduino programming knowledge required
- Assembly time: ~20-40 hours

#### Community Support
- **Level:** HIGH - Very well documented, multiple language translations
- Used in 15+ Catalan schools, worldwide adoption
- Active Thingiverse community with remixes

---

### Thor
**Status:** Active | **Origin:** AngelLM (Spain) | **Year:** 2015-present

Thor is one of the most complete open-source 3D-printable robot arms, with full ROS2 support, extensive documentation, and a global community.

| Attribute | Details |
|-----------|---------|
| **License** | CC-BY-SA-4.0 |
| **BOM Cost** | ~$350 (EUR) / $400-500 USD |
| **Print Time** | ~60-80 hours |
| **DOF** | 6 (yaw-roll-roll-yaw-roll-yaw) |
| **Weight** | ~3 kg |
| **QIDI Compatible** | YES - Parts fit easily |
| **ROS2 Support** | YES - Docker-based implementation |
| **Difficulty** | Intermediate |

#### Key Components (BOM)
| Part | Qty | Est. Cost | Source |
|------|-----|-----------|--------|
| NEMA 17 Stepper Motors (various sizes) | 7 | $60-100 | AliExpress |
| A4988/DRV8825 Stepper Drivers | 7 | $10-15 | AliExpress |
| Arduino Mega 2560 | 1 | $15-25 | AliExpress |
| Custom Thor Control Shield (or RAMPS) | 1 | $15-30 | Fabricate or buy |
| GT2 Belts & Pulleys | Set | $15-25 | AliExpress |
| 625ZZ Bearings | Set | $10-15 | AliExpress |
| Optoisolator Endstops | 5 | $5-10 | AliExpress |
| Micro-endstop | 1 | $2-3 | AliExpress |
| Hardware (M3/M4/M5 bolts) | Set | $15-20 | Hardware store |
| 3D Printing Filament (PLA) | ~2kg | $20-40 | 3D printing store |
| **Total** | | **$157-283** | |

#### Source Links
- **GitHub:** https://github.com/AngelLM/Thor
- **Website:** https://thor.angel-lm.com/
- **Documentation:** https://thor.angel-lm.com/documentation
- **Thor-ROS2:** https://github.com/AngelLM/Thor-ROS
- **ThorControlPCB:** https://github.com/AngelLM/ThorControlPCB
- **Asgard (Control Software):** https://github.com/AngelLM/Asgard
- **Thingiverse:** https://www.thingiverse.com/thing:1743075

#### Capabilities
- 6-axis industrial-style kinematics
- G-code controlled (like 3D printers)
- Forward and inverse kinematics
- Pick and place (up to 750g payload)
- ROS2 + MoveIt2 integration
- Multiple end effector options

#### Assembly Notes
- Print with PLA, 0.2mm layer height, 3 perimeters, 30% infill
- FreeCAD source files available for modification
- 30+ units built in 17 countries
- Several published research papers using Thor

#### Community Support
- **Level:** HIGH - Active forums, Discord, multiple languages
- 30+ documented builds worldwide
- Academic papers published
- Regular community updates

---

### AR2 / AR3 / AR4 (Annin Robotics)
**Status:** Active commercial + open source | **Origin:** Chris Annin | **Year:** 2016-present

Chris Annin's AR series is among the most popular open-source robot arms. The AR4 is the current model, available as CNC parts or 3D-printed.

#### AR2/AR3 (Legacy)
| Attribute | Details |
|-----------|---------|
| **License** | CC (open source plans) |
| **BOM Cost** | ~$1,500-2,000 CAD |
| **Print Time** | ~100h (if 3D printed) |
| **DOF** | 6 |
| **Weight** | ~8 kg |
| **QIDI Compatible** | YES (3D printed version) |
| **ROS2 Support** | Community |
| **Difficulty** | Advanced |

#### AR4 (Current Model)
| Attribute | Details |
|-----------|---------|
| **License** | CC (with paid CNC part kits available) |
| **BOM Cost** | ~$2,000 (CNC kit + electronics) |
| **Print Time** | ~80h + CNC parts |
| **DOF** | 6 |
| **Weight** | ~10 kg |
| **QIDI Compatible** | Partial (some parts CNC machined) |
| **ROS2 Support** | Community |
| **Difficulty** | Advanced |

#### Key Components (AR4 BOM)
| Part | Qty | Est. Cost | Source |
|------|-----|-----------|--------|
| NEMA 23/17 Stepper Motors | 6 | $100-200 | StepperOnline |
| Closed-loop Stepper Drivers | 6 | $120-200 | Annin Robotics |
| Arduino Mega / Teensy | 1 | $20-50 | Various |
| Capstan drive hardware | Set | $50-100 | Annin Robotics |
| Linear Rails & Bearings | Set | $100-200 | Various |
| Aluminum/CNC Parts | Set | $500-800 | Annin Robotics |
| Hardware | Set | $50-100 | Hardware store |
| **Total** | | **~$1,500-2,000** | |

#### Source Links
- **Website:** https://www.anninrobotics.com/
- **YouTube:** https://www.youtube.com/c/ChrisAnnin
- **Wevolver:** https://www.wevolver.com/specs/ar2.robotic.arm
- **Hackster AR4 Review:** https://www.hackster.io/news/is-the-annin-ar4-the-workhorse-robot-arm-for-you

#### Capabilities
- Industrial-style 6-axis movement
- Capstan drive wrist (novel design)
- Closed-loop encoder feedback (on AR4)
- Programming via PC software
- Pick and place
- Machine tending capable

#### Known Issues (AR4)
- Significant backlash reported
- Closed-loop feedback not fully implemented in firmware
- Some engineering choices (grub screws on bearing races) questionable
- Accuracy/repeatability below industrial standards

---

### Kauda & Kauda Pro
**Status:** Active | **Origin:** DIY-Tech (Italy)

Kauda is a family of affordable 3D-printable desktop robotic arms. The Pro version adds enhanced hardware and software capabilities.

#### Kauda (Standard)
| Attribute | Details |
|-----------|---------|
| **License** | Open Source |
| **BOM Cost** | ~$200-400 |
| **Print Time** | ~40-60 hours |
| **DOF** | 4-5 |
| **Weight** | ~2 kg |
| **QIDI Compatible** | YES |
| **ROS2 Support** | NO |
| **Difficulty** | Beginner |

#### Kauda Pro
| Attribute | Details |
|-----------|---------|
| **License** | Open Source |
| **BOM Cost** | ~$400-600 |
| **Print Time** | ~50-70 hours |
| **DOF** | 5-6 |
| **Weight** | ~3 kg |
| **QIDI Compatible** | YES |
| **ROS2 Support** | NO |
| **Difficulty** | Intermediate |

#### Source Links
- **Website:** https://www.diy-tech.it/projects
- **Projects:** Kauda, Kauda Pro, TAYE (shredder)

#### Capabilities
- Desktop pick and place
- Arduino-based control
- Simple programming interface
- Educational focus

---

### SmallRobotArm (by Skyentific)
**Status:** Active | **Origin:** Skyentific (Switzerland)

A well-designed 6-DOF stepper-based robot arm with carbon fiber and 3D-printed parts. Popular YouTube channel with extensive build videos.

| Attribute | Details |
|-----------|---------|
| **License** | GPL-3.0 |
| **BOM Cost** | ~$300-500 |
| **Print Time** | ~60-80 hours |
| **DOF** | 6 |
| **Weight** | ~2.5 kg |
| **QIDI Compatible** | YES |
| **ROS2 Support** | Community |
| **Difficulty** | Intermediate |

#### Key Components
- 6x NEMA 17 stepper motors
- Trinamic stepper drivers (silent operation)
- Arduino/Raspberry Pi control
- 3D printed + carbon fiber parts
- GT2 belt drives

#### Source Links
- **GitHub:** https://github.com/SkyentificGit/SmallRobotArm
- **YouTube Channel:** https://www.youtube.com/c/Skyentific
- **Build Video:** https://www.youtube.com/watch?v=12Be3Hoh-sY

#### Assembly Notes
- Carbon fiber tubes used for arm segments
- Trinamic drivers make it very quiet
- Excellent documentation through YouTube series
- Active GitHub community

---

### Arctos Robotics Arm
**Status:** Active | **Origin:** Arctos Robotics | **Year:** 2023-present

Arctos is a 6-DOF 3D-printed robot arm that can be built largely from 3D printer spare parts. CAD files are paid (~EUR 40) but firmware and ROS files are open source.

| Attribute | Details |
|-----------|---------|
| **License** | Paid CAD ($40), Open Source firmware/ROS |
| **BOM Cost** | ~$300-400 |
| **Print Time** | ~80-100 hours (3kg PLA) |
| **DOF** | 6 |
| **Weight** | ~4 kg |
| **QIDI Compatible** | YES |
| **ROS2 Support** | YES (ROS1 + ROS2 on GitHub) |
| **Difficulty** | Intermediate |

#### Key Components
- NEMA 17 and NEMA 23 stepper motors
- GT2 pulleys and belts
- A4988/DRV8825 drivers
- Arduino Mega 2560 + CNC Shield
- 4mm smooth stainless rod
- M3/M4 threaded rods
- Cycloidal gearboxes (Y and Z axes)

#### Source Links
- **Website:** https://arctosrobotics.com/
- **GitHub:** https://github.com/Arctos-Robotics
- **Thingiverse:** https://www.thingiverse.com/thing:6068730
- **Hackaday:** https://hackaday.com/2023/05/08/arctos-robotics-build-a-robot-arm-out-of-3d-printer-spares/

#### Capabilities
- 500g payload
- GRBL firmware compatible
- ROS integration
- RoboDK compatible
- Closed-loop encoder support (optional)

---

### HELENE Arm
**Status:** Active (2025) | **Origin:** TU Darmstadt, Germany

HELENE is one of the newest open-source 3D-printed robot arms, featuring closed-loop position control with absolute encoders and native ROS integration. Published in a peer-reviewed journal in 2025.

| Attribute | Details |
|-----------|---------|
| **License** | Open Source (academic) |
| **BOM Cost** | ~$1,000 (EUR ~900) |
| **Print Time** | ~5 days (120 hours) |
| **DOF** | 6 |
| **Weight** | ~5 kg |
| **QIDI Compatible** | YES (needs 210x210x180mm minimum) |
| **ROS2 Support** | YES - Native ROS integration |
| **Difficulty** | Intermediate |

#### Key Specs
- Reach: 432 mm
- Repeatability: 0.87 mm
- Position accuracy: 8.4 mm
- Payload: 500g (up to 1.5kg in limited workspace)
- Closed-loop with absolute encoders
- No startup calibration needed

#### Key Components
- NEMA 17 stepper motors (various torque ratings)
- Planetary gearboxes (joints 2 and 3)
- Custom ESP32-based motor controllers
- CAN bus communication between joints
- Absolute magnetic encoders (AS5048A or similar)
- 2mm and 3mm pitch timing belts
- 6009 and 6806 ball bearings

#### Source Links
- **Paper:** https://doi.org/10.3390/hardware3030007
- **Hardware Journal:** https://www.mdpi.com/2813-6640/3/3/7
- **Build volume needed:** 210 x 210 x 180 mm (fits on QIDI Plus 4 easily)

#### Assembly Notes
- Print in PLA: 0.4mm nozzle, 0.2mm layer height, 5 perimeters, 70% infill
- Custom PCBs can be ordered pre-assembled
- 10 prototypes built and tested
- ~500 hours of student operation validated
- 1 hour for electronics prep, rest is assembly

---

### Dobot Magician
**Status:** Commercial (educational) | **Origin:** Shenzhen Yuejiang Technology

Multi-functional desktop robotic arm for education. Not 3D-printable but has open SDK.

| Attribute | Details |
|-----------|---------|
| **License** | SDK available |
| **BOM Cost** | $1,695 (retail) |
| **Print Time** | N/A |
| **DOF** | 4 |
| **Weight** | 11.3 kg (Basic) / 2.4 kg (Lite) |
| **QIDI Compatible** | N/A |
| **ROS2 Support** | SDK only |
| **Difficulty** | Beginner |

#### Capabilities
- 3D printing (yes, the arm IS a 3D printer!)
- Laser engraving
- Writing and drawing
- Pick and place (vacuum + pneumatic gripper)
- Teach and playback
- Multi-Dobot cooperation
- 20+ programming languages supported
- Blockly visual programming

#### Source Links
- **GitHub (examples):** https://github.com/SERLatBTH/StarterGuide-DobotMagician
- **Product:** https://www.dobot.cc/dobot-magician/product-overview

---

### uArm / UFactory
**Status:** Commercial | **Origin:** UFactory (China)

Desktop robot arms with open SDKs. Not 3D-printable but included for reference as accessible alternatives.

| Model | Price | DOF | Payload | Reach | Weight |
|-------|-------|-----|---------|-------|--------|
| uArm Swift Pro | ~$800-1,000 | 4 | 500g | 320mm | 2.2 kg |
| Lite 6 | ~$3,000 | 6 | 600g | 440mm | 8 kg |
| xArm 6 | ~$5,300+ | 6 | 5 kg | 700mm | 12.5 kg |

#### SDK Support
- Python, C++ APIs
- ROS/ROS2 (Lite 6 and xArm)
- Blockly visual programming
- UFactory Studio

#### Source Links
- **Website:** https://www.ufactory.cc/
- **Documentation:** http://download.ufactory.cc/

---

### Reachy 2 (Pollen Robotics)
**Status:** Active | **Origin:** Pollen Robotics (France)

Open-source humanoid robot with bimanual 7-DOF arms. Used in research and AI/ML applications.

| Attribute | Details |
|-----------|---------|
| **License** | Open Source hardware + software |
| **BOM Cost** | ~$10,000+ (complete system) |
| **DOF** | 7 (per arm) |
| **Weight** | ~15 kg (full system) |
| **QIDI Compatible** | Partial (some printed parts) |
| **ROS2 Support** | YES - Native ROS2 Humble |
| **Difficulty** | Advanced |

#### Key Features
- 7-DOF arms (human-like proportions)
- 3 kg payload per arm
- Orbita patented actuators
- VR teleoperation (125ms glass-to-glass latency)
- Python SDK
- Stereo 3D vision
- Mobile base option

#### Source Links
- **Website:** https://www.pollen-robotics.com/reachy/
- **GitHub:** https://github.com/pollen-robotics
- Hugging Face partnership for open-source household robot

---

### Tactigon T-SKIN
**Status:** Niche product | **Origin:** Next Industries (Italy)

A gesture control wearable platform, NOT a robot arm itself, but can be used to control robotic arms via gestures.

| Attribute | Details |
|-----------|---------|
| **License** | Open SDK |
| **Cost** | ~$150-200 (controller board) |
| **Function** | Gesture control for any robot arm |
| **ROS2 Support** | NO |
| **Difficulty** | Beginner |

#### Features
- 9-axis IMU (gyro + accel + magnetometer)
- Environmental sensors (temp, pressure)
- Bluetooth 4.0 LE
- AI-based gesture recognition
- MQTT protocol support
- Arduino IDE programmable

#### Source Links
- **Project:** https://www.hackster.io/thetactigon/remote-gesture-controller-with-mqtt-1a1246
- **Product:** https://www.thetactigon.com/

---

### MeArm V0.4
**Status:** Classic | **Origin:** Phenoptix / Jack Howard

The pocket-sized classic educational robot arm. Simple, cheap, effective for teaching basics.

| Attribute | Details |
|-----------|---------|
| **License** | CC |
| **BOM Cost** | ~$30-50 |
| **Print Time** | ~8-12 hours |
| **DOF** | 4 |
| **Weight** | ~200g |
| **QIDI Compatible** | YES |
| **ROS2 Support** | NO |
| **Difficulty** | Beginner |

#### Source Links
- **Thingiverse:** https://www.thingiverse.com/thing:360108
- **Website:** https://mearm.com/

---

### 6AR Robot Arm
**Status:** Active | **Origin:** fabien-prog | **Year:** 2025

A feature-rich open-source 6-axis robot arm with web-based UI and advanced motion control.

| Attribute | Details |
|-----------|---------|
| **License** | Open Source |
| **BOM Cost** | ~$500-800 |
| **Print Time** | ~60-80 hours |
| **DOF** | 6 |
| **Weight** | ~4 kg |
| **QIDI Compatible** | YES |
| **ROS2 Support** | Planned |
| **Difficulty** | Intermediate |

#### Key Features
- Full 6DOF + spherical wrist
- Full pose IK (position + orientation)
- Joint & Cartesian motion
- Linear & circular paths
- Trapezoidal velocity profiles
- Web-based UI
- Drag-and-drop programming
- 16+ digital I/O

#### Source Links
- **GitHub:** https://github.com/fabien-prog/6AR-Open-Source-6-Axis-Robot

---

## 6. New & Emerging Projects (2024-2026) <a name="new-projects"></a>

### Quadruped Robots - New

| Project | Year | Description | Status | Est. Cost |
|---------|------|-------------|--------|-----------|
| **Pupper v3** (Stanford) | 2024-2025 | AI-powered, RL locomotion, voice interaction | Active development | ~$2,000 |
| **EG01 NavBot** | 2024 | ESP32-based, ultra-low-cost educational | Active | ~$50-100 |
| **Champ ROS2** | 2024-2025 | Universal ROS2 quadruped framework | Active | Software only |
| **SimpleFOC Quadrupeds** | 2024-2025 | Brushless servo-based DIY quadrupeds | Community | ~$500-1,000 |

### Robotic Arms - New

| Project | Year | Description | Status | Est. Cost |
|---------|------|-------------|--------|-----------|
| **HELENE** (TU Darmstadt) | 2025 | 6-DOF, closed-loop, absolute encoders, ROS | Published, active | ~$1,000 |
| **6AR** | 2025 | 6-DOF, web UI, advanced motion planning | Active | ~$500-800 |
| **SAM Arm** (LeRobot) | 2024-2025 | 6-DOF, optimized for LeRobot/AI, ~$450 | Active | ~$450 |
| **SO-ARM100** | 2024 | Hugging Face LeRobot standard arm | Active | ~$100-300 |
| **Arctos v2** | 2024 | Updated 6-DOF, ROS2, cycloidal drives | Active | ~$300-400 |
| **PingTi-Arm** | 2024 | Low-cost human-arm-length design | Active | ~$260 |

---

## 7. Electronics & Components Sourcing Guide <a name="electronics-guide"></a>

### Where to Buy Components

| Store | Best For | Shipping |
|-------|----------|----------|
| **AliExpress** | Servos, steppers, electronics, hardware | 2-4 weeks |
| **Amazon** | Fast shipping, slightly higher prices | 1-2 days |
| **StepperOnline** | Quality stepper motors + drivers | 1-2 weeks |
| **ServoCity** | Servos, actuators, robot parts | 1 week (US) |
| **Pololu** | Electronics, motor drivers, sensors | 1 week (US) |
| **Mouser/DigiKey** | Professional electronics | 1-2 days |
| **Banggood** | Electronics, 3D printer parts | 2-3 weeks |

### Common Electronics for Robot Projects

| Component | Use | Price Range | Link/Source |
|-----------|-----|-------------|-------------|
| Raspberry Pi 4B (4GB/8GB) | Main controller | $55-75 | RaspberryPi.com |
| Raspberry Pi 5 | High-performance controller | $60-80 | RaspberryPi.com |
| Arduino Mega 2560 | Motor control, sensors | $15-25 | AliExpress/Amazon |
| ESP32 DevKit | WiFi/Bluetooth controller | $5-10 | AliExpress |
| PCA9685 16-ch PWM | Servo control | $3-5 | AliExpress |
| MPU-6050 IMU | Orientation sensing | $2-4 | AliExpress |
| BNO055 IMU | 9-DOF absolute orientation | $15-25 | Adafruit/AliExpress |
| NEMA 17 Stepper (17HS19-2004S) | Standard robot joint | $10-15 | StepperOnline |
| NEMA 23 Stepper | High-torque joints | $20-40 | StepperOnline |
| A4988 Stepper Driver | Basic stepper control | $1-2 | AliExpress |
| DRV8825 Stepper Driver | Higher current drivers | $2-3 | AliExpress |
| TMC2209 Stepper Driver | Silent stepper drivers | $5-8 | AliExpress |
| MG996R Servo | Standard hobby servo | $3-5 | AliExpress |
| PDI-HV5523MG Servo | High-voltage digital servo | $8-15 | AliExpress |
| CLS6336HV Servo | High-torque digital servo | $15-25 | AliExpress |
| Dynamixel AX-12A | Smart servo (robotics standard) | $45-50 | Robotis |
| ODrive 3.6 | Brushless motor controller | $120-150 | ODrive Robotics |
| RPLidar A1 | 2D LiDAR for SLAM | $100-150 | Slamtec |
| OAK-D Lite | AI depth camera | $100-150 | Luxonis |
| Intel RealSense D435 | Depth camera | $200-300 | Intel |

---

## 8. QIDI Plus 4 Max Print Settings <a name="print-settings"></a>

### Recommended Settings by Material

| Material | Use Case | Nozzle Temp | Bed Temp | Layer Height | Infill | Speed | Notes |
|----------|----------|-------------|----------|--------------|--------|-------|-------|
| **PLA** | Robot arms (rigid parts) | 200C | 60C | 0.2mm | 30-50% | 60mm/s | Standard, easy to print |
| **PETG** | Quadruped bodies (durable) | 240C | 80C | 0.2mm | 40-60% | 50mm/s | More impact resistant |
| **ABS** | High-stress parts | 250C | 100C | 0.2mm | 50% | 50mm/s | Enclosure recommended |
| **TPU (95A)** | Robot feet, grippers, flexible parts | 230C | 60C | 0.2mm | 20-30% | 30mm/s | Flexible, grippy |
| **Nylon** | High-strength mechanical parts | 260C | 80C | 0.2mm | 50% | 40mm/s | Dry filament required |
| **Carbon Fiber PETG** | Rigid, strong structural parts | 240C | 80C | 0.28mm | 50% | 40mm/s | Abrasive, use hardened nozzle |

### General Tips for Robot Printing
- **Hardened steel nozzle** recommended for carbon fiber and glow-in-dark filaments
- **Brim** (5-8mm) recommended for parts with small footprints
- **Supports** needed for overhangs >45 degrees
- **Orientation matters** - print parts so layer lines run along stress directions
- **Threaded inserts** (heat-set) strongly recommended over printed threads
- **Calibration** - ensure dimensional accuracy for bearing fits

---

## 9. Recommended Build Order for MEOK Labs <a name="recommended-build-order"></a>

### Phase 1: Warm-Up (Beginner, Weeks 1-2)
1. **MeArm V0.4** ($50, 12h print) - Learn basics of servo control and arm kinematics
2. **EG01 NavBot** ($75, 25h print) - Learn quadruped basics with ESP32

### Phase 2: Core Learning (Intermediate, Weeks 3-6)
3. **Mini Pupper** ($600 kit, 50h print) - Full ROS 2 quadruped with SLAM
4. **BCN3D Moveo** ($400, 90h print) - Classic 5-DOF arm, learn stepper control
   - OR **Thor** ($450, 70h print) - 6-DOF with ROS 2

### Phase 3: Advanced Builds (Weeks 7-16)
5. **Spot Micro** ($500, 100h print) - Full ROS quadruped with custom software
6. **HELENE Arm** ($1,000, 120h print) - Research-grade 6-DOF with closed-loop control
   - OR **Arctos Arm** ($350, 90h print) - 6-DOF with ROS, lower cost

### Phase 4: Research Grade (Ongoing)
7. **Pupper v3** ($2,000, 150h+ print) - Stanford-grade RL locomotion
8. **Solo12** ($4,000 kit) - Torque-controlled brushless research platform

---

## Sources & References

### GitHub Repositories
- Spot Micro: https://github.com/mike4192/spotMicro
- Stanford Doggo: https://github.com/Nate711/StanfordDoggoProject
- Pupper v3: https://pupper-v3-documentation.readthedocs.io/
- Mini Pupper: https://github.com/mangdangroboticsclub
- OpenCat: https://github.com/PetoiCamp/OpenCat
- BCN3D Moveo: https://github.com/BCN3D/BCN3D-Moveo
- Thor: https://github.com/AngelLM/Thor
- Arctos: https://github.com/Arctos-Robotics
- SmallRobotArm: https://github.com/SkyentificGit/SmallRobotArm
- HELENE: Paper at https://doi.org/10.3390/hardware3030007
- Solo12: https://github.com/open-dynamic-robot-initiative
- MIT Cheetah Software: https://github.com/mit-biomimetics/Cheetah-Software
- Unitree SDK: https://github.com/unitreerobotics
- Reachy: https://github.com/pollen-robotics
- 6AR: https://github.com/fabien-prog/6AR-Open-Source-6-Axis-Robot

### Project Websites
- Thor: https://thor.angel-lm.com/
- Arctos: https://arctosrobotics.com/
- Petoi: https://www.petoi.com/
- Mini Pupper: https://minipupperdocs.readthedocs.io/
- PAL Robotics: https://solo.pal-robotics.com/
- ODRI: https://open-dynamic-robot-initiative.github.io/
- Annin Robotics: https://www.anninrobotics.com/
- Pollen Robotics: https://www.pollen-robotics.com/

### Key Papers & Publications
- Stanford Doggo: ICRA 2019, https://arxiv.org/abs/1905.04254
- HELENE: Hardware 2025, https://doi.org/10.3390/hardware3030007
- Solo12: Multiple publications at ICRA/RSS
- ODRI Actuator: https://ieeexplore.ieee.org (Open torque-controlled modular robot architecture)

---

*Document compiled for Nick at MEOK Labs. Happy robot building!*

*Last updated: July 2025*
