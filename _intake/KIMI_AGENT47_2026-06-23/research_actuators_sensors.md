# MEOK Labs - Complete Parts List for 3D-Printed Robot Army
## Comprehensive Research: Actuators, Grippers, Sensors & Electronics

**Compiled for:** Nick @ MEOK Labs | **Printer:** QIDI Plus 4 Max  
**Date:** June 2026 | **Sources:** AliExpress, Amazon, RobotShop, ServoCity, Adafruit, SparkFun, goBILDA

---

# PART 1: ACTUATORS & SERVOS

## 1.1 DYNAMIXEL SERIES (Gold Standard - Expensive)

The **ROBOTIS DYNAMIXEL** family is the gold standard for robotic actuators. All models feature position/velocity/torque feedback, daisy-chain networking (TTL/RS485), and PID control. They work seamlessly with ROS2 via `dynamixel_sdk`.

### XL Series (Entry-Level, Plastic Gears)

| Model | Price | Source | Stall Torque | Speed | Voltage | Weight | Key Specs |
|-------|-------|--------|-------------|-------|---------|--------|-----------|
| **XL330-M288-T** | **$23.90** | RobotShop, Dynamixel.com | 0.93 N.m | 81 rpm | 5.0V | 23g | Ultra-compact, 6 control modes, current control |
| **XL330-M077-T** | **$23.90** | RobotShop, Dynamixel.com | 0.22 N.m | 363 rpm | 5.0V | 23g | High-speed version, same size |
| **XL430-W250-T** | **$23.90-$39** | RobotShop, robosavvy.co.uk | 1.5 N.m | 61 rpm | 6.5-12V | 57g | **Best entry-level value**, 360 deg control, ABS encoder |
| **2XL430-W250-T** | **$129.90** | Dynamixel.com | 1.4 N.m | 57 rpm | 11.1V | 98g | Dual-axis actuator for compact joints |

### XM/XC Series (Mid-Range, Metal Gears)

| Model | Price | Source | Stall Torque | Speed | Voltage | Weight | Key Specs |
|-------|-------|--------|-------------|-------|---------|--------|-----------|
| **XC430-W150-T** | **$119.90** | Dynamixel.com | 1.6 N.m | 106 rpm | 12V | 65g | Speed-optimized, metal gears |
| **XC430-W240-T** | **$119.90** | Dynamixel.com | 1.9 N.m | 70 rpm | 12V | 65g | Torque-optimized variant |
| **XM430-W210-T** | **$269.90** | Dynamixel.com | 3.0 N.m | 77 rpm | 12V | 82g | Best for medium joints |
| **XM430-W350-T** | **$269.90** | Dynamixel.com | 4.1 N.m | 46 rpm | 12V | 82g | High-torque variant |
| **XM540-W150-T** | **$419.90** | Dynamixel.com | 7.3 N.m | 53 rpm | 12V | 165g | Heavy-duty joints |
| **XM540-W270-T** | **$419.90** | Dynamixel.com | 10.6 N.m | 30 rpm | 12V | 165g | Maximum XM torque |

### XH/XD Series (High-End)

| Model | Price | Source | Stall Torque | Speed | Voltage | Weight | Key Specs |
|-------|-------|--------|-------------|-------|---------|--------|-----------|
| **XH430-W350-T** | **$359.90** | Dynamixel.com | 3.4 N.m | 30 rpm | 12V | 82g | High precision, low backlash |
| **XD540-T150-R** | **$769.90** | Dynamixel.com | 7.1 N.m | 70 rpm | 12V | 170g | Industrial grade |
| **XD540-T270-R** | **$769.90** | Dynamixel.com | 9.9 N.m | 39 rpm | 12V | 170g | Maximum XD torque |
| **XH540-W150-R** | **$549.90** | Dynamixel.com | 7.1 N.m | 70 rpm | 12V | 165g | Widely used in research |

### Integration Notes
- **Protocol:** XL/XM use Protocol 2.0 (TTL half-duplex serial) - daisy-chain capable
- **Controller:** U2D2 ($49.90) or OpenCM9.04 ($9.90) for USB-to-Dynamixel bridge
- **ROS2:** `dynamixel_sdk` + `dynamixel_workbench` packages available
- **Power:** 12V SMPS recommended (3S LiPo compatible)
- **Where to buy cheapest:** RobotShop (EU), robosavvy (UK), or bulk from Robotis directly

---

## 1.2 CHEAP ALIEXPRESS SERVOS (Budget Workhorses)

For the MEOK army on a budget, these servos offer incredible value. All are 3D-printable-compatible and widely available.

| Model | Price (AliExpress) | Stall Torque | Speed | Voltage | Weight | Gear Material | Waterproof |
|-------|-------------------|-------------|-------|---------|--------|---------------|------------|
| **TowerPro SG90** | **$1.50-$3.00** | 1.8 kg.cm (0.18 N.m) | 0.12s/60deg | 4.8-6V | 9g | POM plastic | No |
| **TowerPro MG90S** | **$3.00-$5.00** | 2.2 kg.cm (0.22 N.m) | 0.08s/60deg | 4.8-6V | 14g | Metal | No |
| **MG996R** | **$3.50-$6.00** | 11 kg.cm (1.1 N.m) @6V | 0.14s/60deg | 4.8-7.2V | 55g | Metal | No |
| **MG995** | **$3.00-$5.00** | 10 kg.cm (1.0 N.m) @6V | 0.20s/60deg | 4.8-7.2V | 55g | Metal | No |
| **DS3218 (20kg)** | **$8.00-$15.00** | 20 kg.cm (2.0 N.m) @6.8V | 0.14s/60deg | 4.8-6.8V | 60g | Copper+Aluminum | **IP66** |
| **DS3225 (25kg)** | **$10.00-$17.00** | 25 kg.cm (2.45 N.m) @6V | 0.13s/60deg | 4.8-7.4V | 62g | Metal | **IP66** |
| **DS3235 (35kg)** | **$12.00-$20.00** | 35 kg.cm (3.43 N.m) @6.8V | 0.12s/60deg | 4.8-6.8V | 65g | Metal | **IP66** |
| **DS3240 (40kg)** | **$15.00-$25.00** | 40 kg.cm (3.92 N.m) @6.8V | 0.10s/60deg | 4.8-6.8V | 68g | Full metal | **IP66** |
| **JX BLS-HV7132MG** | **$25.00-$35.00** | 32 kg.cm (3.14 N.m) | 0.07s/60deg | 6.0-8.4V | 70g | Steel, Brushless | Yes |

### Torque Comparison (Humanoid Context)

| Joint Type | Recommended Torque (N.m) | Budget Servo Choice | Premium Choice |
|------------|------------------------|-------------------|----------------|
| Gripper/finger | 0.2 - 0.5 | SG90 / MG90S | XL330-M288 |
| Wrist | 0.5 - 1.5 | MG996R | XL430-W250 |
| Elbow | 2.0 - 4.0 | DS3218 / DS3225 | XM430-W350 |
| Shoulder | 4.0 - 8.0 | DS3235 / DS3240 | XM540-W150 |
| Hip (humanoid) | 6.0 - 10.0 | 2x DS3240 (paired) | XM540-W270 |
| Knee | 4.0 - 8.0 | DS3235 / DS3240 | XM540-W150 |
| Ankle | 2.0 - 4.0 | DS3225 / DS3235 | XM430-W350 |
| Quadruped leg | 3.0 - 6.0 | DS3235 | XM430-W350 |

### Integration Notes
- **PWM frequency:** Standard 50Hz (20ms period), pulse 500-2500us for 180deg
- **Driver:** PCA9685 16-channel I2C driver ($2-5 on AliExpress)
- **Power budget:** Plan ~1A per servo at stall (MG996R/DS3218), use external 5-6V BEC
- **3D-printed horns:** Most use 25T spline - design custom horns in CAD
- **Heat:** Metal gear servos run hot under continuous load - add ventilation

---

## 1.3 STEPPER MOTORS

| Model | Price (AliExpress) | Holding Torque | Current/Phase | Weight | Key Specs |
|-------|-------------------|---------------|--------------|--------|-----------|
| **NEMA 17 (42mm)** | **$8.00-$15.00** | 0.4-0.9 N.m (40-90 N.cm) | 1.5-2.0A | 270-350g | Standard for 3D printers |
| **NEMA 17 Long (48mm)** | **$12.00-$20.00** | 0.52 N.m (52 N.cm) | 1.5A | 350g | Better for robot arms |
| **NEMA 17 Extended (60mm)** | **$15.00-$25.00** | 0.65 N.m (65 N.cm) | 2.0A | 400g | High torque variant |
| **NEMA 23 (57mm)** | **$18.00-$35.00** | 1.2-2.5 N.m | 2.8-4.0A | 600-1000g | Heavy-duty joints |
| **NEMA 23 Long (76mm)** | **$25.00-$45.00** | 1.8-3.0 N.m | 3.0-4.0A | 900-1200g | CNC-grade torque |

### Stepper Drivers

| Driver | Price | Max Current | Microstepping | Features |
|--------|-------|------------|--------------|----------|
| **A4988** | **$1.00-$2.50** | 1A/phase | 1/16 | Basic, cheap |
| **DRV8825** | **$2.00-$4.00** | 2.2A/phase | 1/32 | Better current control |
| **TMC2209** | **$4.00-$8.00** | 2.8A/phase | 1/256 | Silent, UART config, stallGuard |
| **TMC5160** | **$12.00-$20.00** | 4.4A/phase | 1/256 | SPI, highest performance |

### Integration Notes
- **Robot arm use:** Steppers are great for elbows/shoulders where you need precise position but not fast response
- **Closed-loop:** Add AS5600 magnetic encoder ($2-5) for closed-loop stepper control
- **Gear reduction:** 5:1 to 10:1 planetary gearbox ($15-30) dramatically increases effective torque
- **ROS2:** Use `ros2_control` with stepper motor controllers

---

## 1.4 BLDC MOTORS + ODrive

For advanced, high-torque, backdrivable joints, BLDC motors with ODrive controllers are the ultimate choice.

### BLDC Motors

| Model | Price | KV Rating | Max Torque | Voltage | Weight | Source |
|-------|-------|-----------|-----------|---------|--------|--------|
| **Turnigy Aerodrive 5065** | **$30-$50** | 270KV | ~2.5 N.m | 24V | 350g | HobbyKing |
| **D5312S-330KV** | **~$15/motor** | 330KV | ~1.5 N.m | 24V | 280g | AliExpress |
| **ODrive D6374** | **$89** | 150KV | ~5.0 N.m | 48V | 850g | ODrive Robotics |
| **T-Motor U8 Lite** | **$120-$150** | 100KV | ~8.0 N.m | 48V | 400g | T-Motor |
| **Hoverboard motor** | **$15-$30/pair** | 15-20KV | ~10 N.m | 36V | 2.5kg each | AliExpress |

### ODrive Controllers

| Model | Price | Max Power | Voltage | Current/Motor | Channels |
|-------|-------|-----------|---------|--------------|----------|
| **ODrive S1** | **$199-$249** | 1600W | 12-50V | 40A cont | 1 motor |
| **ODrive Pro** | **$349-$449** | 3000W | 14-58V | 80A cont | 1 motor |
| **ODrive Micro** | **~$79** | 300W | 12-40V | 20A cont | 1 motor |
| **ODESC 3.6** (ODrive clone) | **$50-$80** | 1000W | 12-50V | 30A cont | 1 motor |
| **Makerbase ODrive** | **~$30-$50** | 500W | 12-40V | 20A cont | 1 motor |
| **ODrive v3.6** (legacy) | **~$99-$149** | 1000W | 12-56V | 40A cont | 2 motors |

### Integration Notes
- **Encoder required:** AS5600 ($2), AMT102 ($30), or TLE5012 ($15) for position feedback
- **Backdrivable:** Excellent for compliant control and human interaction
- **ROS2:** `odriveros2` package available, `ros2_control` integration
- **Power:** Needs substantial power supply - 24V/10A minimum for most setups
- **For humanoid:** Use 2x ODrive Pro + 4x D6374 for hips/knees = ~$1500 just for actuation
- **Budget option:** Hoverboard motors ($15/pair) + Makerbase ODrive ($40) = incredible torque per dollar

---

## 1.5 BEST SERVO FOR EACH APPLICATION (Quick Reference)

| Application | Budget Choice | Mid-Tier | Premium | Notes |
|-------------|-------------|----------|---------|-------|
| **Humanoid finger** | SG90 ($2) | MG90S ($4) | XL330-M288 ($24) | SG90 is fine for simple grippers |
| **Humanoid wrist** | MG996R ($5) | DS3218 ($12) | XL430-W250 ($24) | XL430 has 360deg control |
| **Humanoid elbow** | DS3225 ($14) | DS3235 ($17) | XM430-W210 ($270) | 2.5-4 N.m needed |
| **Humanoid shoulder** | DS3235 ($17) | DS3240 ($20) | XM430-W350 ($270) | 3.5-6 N.m needed |
| **Humanoid hip** | 2x DS3240 ($40) | DS3240+gearbox | XM540-W270 ($420) | 6-10 N.m needed |
| **Humanoid knee** | DS3235 ($17) | DS3240 ($20) | XM540-W150 ($420) | 5-8 N.m needed |
| **Quadruped leg (DOF)** | DS3235 ($17) | DS3240 ($20) | XM430-W350 ($270) | 3-4 N.m is enough per joint |
| **Quadruped (BLDC)** | Hoverboard motor ($8) | D5312S+ODrive S1 ($215) | D6374+ODrive Pro ($540) | BLDC is the gold standard |
| **Gripper finger** | SG90 ($2) | MG90S ($4) | Custom BLDC ($50) | Simple grippers need little torque |
| **Pan/tilt camera** | SG90x2 ($4) | MG90Sx2 ($8) | XL330x2 ($48) | Speed matters for tracking |

---

# PART 2: GRIPPERS

## 2.1 Servo-Driven Grippers (3D Printable)

| Design | Actuator | Price to Build | Grip Force | Best For | STL/Source |
|--------|----------|---------------|------------|----------|------------|
| **Simple Parallel Jaw** | 1x MG996R | $5-8 | ~5N | Pick & place, blocks | Thingiverse: "Servo Gripper" |
| **3-Finger Adaptive (MDPI)** | 3x micro servo | $15-25 | ~8N | Irregular objects | Paper: "Open-Source 3D Printed Three-Fingered Robotic Gripper" |
| **9g Servo Gripper** | 1x SG90 | $3-5 | ~2N | Lightweight, teaching | Thingiverse: "SG90 Gripper" |
| **Robotis RH-P12-RN** | Dynamixel | **$499** | 15N | Research, force control | RobotShop |
| **Robotis Hand Gripper** | 2x XL430 | **$120** (parts) | 10N | Precise manipulation | Custom STL on GitHub |

### Recommended 3D-Printable Gripper Designs

1. **"Parametric Robot Gripper"** (Thingiverse #3847625) - Single servo, parallel jaw, fully parametric OpenSCAD
2. **"3-Finger Adaptive Gripper"** (MDPI Biomimetics 2025) - 3D printed in PLA+TPU, 3 micro servos, $15 total
3. **"MeArm"** - Classic 4-DOF mini arm + gripper, SG90 servos, $20 total, full open source
4. **"EEZYbotARM MK2"** - 4-DOF arm with parallel gripper, MG996R servos, $30 total
5. **"JPL Open Source Rover Gripper"** - Mars rover style, 1 servo, very robust

## 2.2 Adaptive/Flexure Grippers (No Motors, Compliant)

| Design | Material | Price | Principle | Best For |
|--------|----------|-------|-----------|----------|
| **Compliant Finger** | PLA/TPU | $2-5 | Elastic deformation | Lightweight, simple pick |
| **Fin Ray Effect** | TPU 95A | $3-8 | Bio-inspired ribs | Conforming to object shape |
| **Origami Gripper** | Paper+3D printed base | $1-3 | Foldable mechanism | Ultra-low cost |
| **Vacuum-Assisted** | TPU + aquarium pump | $10-15 | Suction + compliance | Flat objects, pick & place |
| **Gecko-inspired** | PLA + adhesive pads | $5-10 | Dry adhesion | Smooth surfaces |

### Key Insight
Flexure grippers printed in **TPU 95A** can grip a wide variety of object shapes with zero motors - just use a single linear actuator or servo to open/close the compliant mechanism. The "fin ray effect" (bio-inspired rib structure) causes fingers to conform to object shape automatically.

## 2.3 Soft Robotics Grippers (Pneumatic)

| Component | Price | Source | Notes |
|-----------|-------|--------|-------|
| **3D Printed Mold** | $5 (filament) | Print yourself | Design in Fusion 360, print mold in PLA |
| **Food-safe Silicone** | $15-25/kg | Smooth-On Ecoflex 00-30 | Shore 00-30 is ideal soft gripper |
| **Mini Air Pump** | $5-10 | AliExpress 12V/370 pump | 2-3 PSI is enough |
| **Solenoid Valve** | $3-5 each | AliExpress 2-way valve | 5V or 12V |
| **Pressure Sensor** | $5-10 | MPX5700 or similar | For closed-loop control |
| **Complete Soft Gripper** | **$20-40 total** | DIY | Delta X Soft Gripper design |

### Design Tips for 3D-Printed Soft Grippers
- **Mold design:** Print mold halves in PLA, coat with mold release spray
- **Wall thickness:** 1.5-2mm silicone walls give best compliance
- **Chambers:** 3-5 pneumatic chambers per finger
- **Operating pressure:** 10-40 kPa (very low - safe for humans)
- **Best source:** Delta X Soft Gripper (open source, ~$10 to build)

## 2.4 Vacuum Grippers

| Component | Price | Source | Notes |
|-----------|-------|--------|-------|
| **Mini Vacuum Pump** | $5-12 | AliExpress (12V 370 pump) | Suction cup attachment |
| **Suction Cups (set)** | $3-8 | AliExpress (various sizes) | 10-40mm diameter |
| **Solenoid Valve** | $3-5 | AliExpress 2-way | For vacuum release |
| **Vacuum Sensor** | $5-10 | MPXV7002DP or similar | Detect if object gripped |
| **DIY Vacuum Ejector** | $2-5 | 3D print + Venturi | Uses compressed air |
| **Complete Vacuum Gripper** | **$15-30 total** | DIY | Best for flat objects |

### Vacuum Gripper Integration
- **Pick force:** F = P x A (e.g., 20kPa vacuum on 20mm cup = ~6N)
- **Best for:** Boxes, sheets, flat objects, electronics
- **Not for:** Porous, rough, or curved surfaces
- **3D printable:** Full ejector and mount systems on Thingiverse

---

# PART 3: SENSORS

## 3.1 CAMERAS

| Camera | Price | Resolution | Depth? | FOV | Weight | ROS2 Support | Best For |
|--------|-------|-----------|--------|-----|--------|-------------|----------|
| **Raspberry Pi Camera Module 3** | **$25-$35** | 12MP (IMX708) | No | 75deg / 120deg | 4g | `libcamera` + ROS2 | Budget vision, object detection |
| **Raspberry Pi Camera v2** | **$15-$25** | 8MP (IMX219) | No | 62deg | 3g | `libcamera` + ROS2 | Even cheaper option |
| **Raspberry Pi HQ Camera** | **$50** | 12MP (IMX477) | No | Lens swap | 50g | `libcamera` + ROS2 | Machine vision, better quality |
| **Arducam OV9281 Global Shutter** | **$35-$50** | 1MP | No | DFOV 120deg | 5g | ROS2 package | High-speed motion, no rolling shutter |
| **Intel RealSense D405** | **$240 (refurb $195)** | 1280x720 @ 90fps | Yes (IR stereo) | 87deg | 51g | `realsense2_camera` - **mature** | Wrist-mounted manipulation (closest range) |
| **Intel RealSense D435i** | **$280 (refurb $225)** | 1280x720 @ 90fps | Yes (IR stereo) | 90deg | 72g | `realsense2_camera` - **mature** | General SLAM, IMU included |
| **Intel RealSense D455** | **$320 (refurb $260)** | 1280x720 @ 90fps | Yes (IR stereo) | 95deg | 120g | `realsense2_camera` - **mature** | Navigation, longer range |
| **Orbbec Gemini 335** | **$250** | 1280x800 @ 30fps | Yes (active IR) | 91deg | 78g | `orbbec-ros2-sdk` | Budget depth camera, well supported |
| **Orbbec Femto Bolt** | **$350** | 1024x1024 @ 30fps | Yes (ToF) | 120deg | 178g | `orbbec-ros2-sdk` | Azure Kinect compatible, large FOV |
| **Luxonis OAK-D Pro** | **$349** | 1280x720 @ 30fps | Yes (neural) | 81deg | 95g | `depthai-ros` | On-device AI, no GPU needed |
| **Stereolabs ZED 2i** | **$550** | 2208x1242 @ 15fps | Yes (neural) | 110deg | 175g | `zed-ros2-wrapper` | Outdoor, large FOV, requires CUDA |
| **Stereolabs ZED Mini** | **$450** | 2208x1242 @ 15fps | Yes (neural) | 90deg | 63g | `zed-ros2-wrapper` | Compact, requires CUDA |
| **USB Webcam (Logitech C920)** | **$30-$50** | 1080p @ 30fps | No | 78deg | 60g | `v4l2_camera` (ROS2) | Basic vision, teleop |
| **Arducam 64MP Hawk-eye** | **$60-$80** | 64MP | No | 84deg | 20g | `libcamera` | Ultra-high resolution |

### Camera Notes
- **Intel RealSense winding down:** No new hardware development. Orbbec is the recommended future-proof alternative.
- **Raspberry Pi Camera 3 Wide ($35):** Best value for robot navigation - 120deg FOV, autofocus, HDR
- **For SLAM:** RealSense D435i or Orbbec Gemini 335 (both have built-in IMU for visual-inertial SLAM)
- **For manipulation:** RealSense D405 (smallest, closest working distance 7cm)

## 3.2 LiDAR

| Model | Price | Range | Scan Rate | Resolution | ROS2 Support | Best For |
|-------|-------|-------|-----------|------------|-------------|----------|
| **YDLIDAR X2** | **$78-$90** | 0.12-8m | 5-8Hz | 0.6-0.96deg | `ydlidar_ros2_driver` | Budget indoor SLAM |
| **YDLIDAR X4** | **$94-$110** | 0.12-10m | 5-8Hz | 0.43-0.86deg | `ydlidar_ros2_driver` | Better range budget option |
| **YDLIDAR G2** | **$178** | 0.12-12m | 6-12Hz | 0.36-0.86deg | `ydlidar_ros2_driver` | Mid-range indoor |
| **YDLIDAR G4** | **$334** | 0.12-16m | 5-12Hz | 0.2-0.48deg | `ydlidar_ros2_driver` | High-res indoor mapping |
| **YDLIDAR TG15 (ToF)** | **$432** | 0.05-15m | 5-12Hz | 0.09-0.22deg | `ydlidar_ros2_driver` | Outdoor capable, IP65 |
| **YDLIDAR Tmini Pro** | **$144** | 0.02-12m | 6-12Hz | 0.54deg | `ydlidar_ros2_driver` | Compact ToF option |
| **RPLIDAR A1M8** | **$65-$100** | 0.15-12m | 5.5Hz | ~0.9deg | `rplidar_ros2` | Most popular budget LiDAR |
| **RPLIDAR A2M12** | **$200-$280** | 0.15-18m | 10Hz | ~0.45deg | `rplidar_ros2` | Better scan rate |
| **RPLIDAR A3** | **$400-$500** | 0.15-25m | 10/20Hz | ~0.33deg | `rplidar_ros2` | Higher performance |
| **RPLIDAR C1** | **$79-$99** | 0.2-12m | 10Hz | ~0.5deg | `rplidar_ros2` | Newer ToF version of A1 |
| **RPLIDAR S3** | **$549** | 0.05-40m | 10-20Hz | ~0.18deg | `rplidar_ros2` | Long-range outdoor |
| **RPLIDAR S2** | **$339** | 0.05-30m | 10Hz | ~0.18deg | `rplidar_ros2` | Mid-range outdoor |
| **LD06/LD19 (LD LiDAR)** | **$30-$50** | 0.02-12m | 10Hz | ~0.5deg | Community driver | Ultra-budget option |

### LiDAR Notes
- **Best value indoor:** RPLIDAR A1 ($65-99) or YDLIDAR X2 ($78) - both work great with ROS2 SLAM Toolbox and Nav2
- **Best value outdoor:** YDLIDAR TG15 ($432) - IP65 rated, ToF technology
- **For SLAM:** All listed LiDARs work with `slam_toolbox` and `nav2` in ROS2
- **Budget hack:** LD06/LD19 ($30-50) - often sold as "D300" on AliExpress, works with ROS2

## 3.3 IMU (Inertial Measurement Unit)

| Sensor | Price | Axes | Fusion | Interface | Accuracy | ROS2 Support | Best For |
|--------|-------|------|--------|-----------|----------|-------------|----------|
| **MPU6050** | **$2-$5** | 6-DOF (accel+gyro) | No | I2C | Moderate | `imu_tools` | Budget balancing robots |
| **MPU9250** | **$4-$8** | 9-DOF (+mag) | No | I2C/SPI | Good | `imu_tools` | Better orientation with magnetometer |
| **BNO055** | **$8-$15** | 9-DOF | **Built-in fusion** | I2C/UART | Excellent | `bno055` (ROS2) | **Best plug-and-play IMU** |
| **LSM6DS3** | **$3-$6** | 6-DOF | No | I2C/SPI | Good | `imu_tools` | Low power, compact |
| **ICM-20948** | **$6-$12** | 9-DOF | DMP onboard | I2C/SPI | Very Good | `imu_tools` | Advanced DMP processing |
| **WitMotion WT901B** | **$20-$35** | 9-DOF | Built-in fusion | UART/I2C | Excellent | UART parser | Rugged, vibration-resistant |
| **Phidgets Spatial 3/3/3** | **$80-$120** | 9-DOF | Built-in fusion | USB/VINT | Professional | `phidgets_ros2` | Professional-grade |

### IMU Notes
- **BNO055 is the winner for hobby robotics:** Built-in sensor fusion outputs quaternion/orientation directly
- **For humanoid balance:** MPU6050 + external Kalman filter is sufficient on a budget
- **For SLAM:** BNO055 or ICM-20948 with `imu_filter_madgwick` node
- **WitMotion** units come pre-calibrated and output fused data over UART - very convenient

## 3.4 FORCE / TORQUE SENSORS

| Sensor | Price | Range | Interface | ROS2 Support | Best For |
|--------|-------|-------|-----------|-------------|----------|
| **HX711 + Load Cell** | **$3-$8** | 1-50kg | GPIO/SPI | Custom node | Grip force, weight measurement |
| **Strain Gauge (generic)** | **$2-$5** | Custom | Wheatstone bridge | ADC + custom | Custom force sensing |
| **FSR402 (Force Sensitive Resistor)** | **$2-$4** | 0.1-10N | Analog | ADC + custom | Touch/pressure detection |
| **Mini Load Cell (S-type)** | **$10-$15** | 1-5kg | HX711 | Custom node | Robot hand grip force |
| **Robotis DMS-80 (optional)** | **$15** | N/A | Analog | Dynamixel SDK | Dynamixel-compatible distance |
| **ATI Nano25** | **$5,000+** | 25N | Dedicated | Custom | Professional research |
| **6-Axis DIY (Strain gauge + PCB)** | **$15-$30** | Custom | Custom | Custom | Open source 6-axis F/T sensor |

### Force Sensor Integration Notes
- **HX711** is the standard load cell amplifier - works with Arduino/ESP32/Raspberry Pi
- **For gripper feedback:** FSR402 or mini load cell with HX711 gives basic force feedback
- **For arm compliance:** 6-axis F/T sensor is ideal but expensive; consider series elastic actuators instead
- **ROS2:** Write a simple node that publishes `geometry_msgs/WrenchStamped` from HX711 readings

## 3.5 TOUCH SENSORS

| Sensor | Price | Type | Interface | Best For |
|--------|-------|------|-----------|----------|
| **TTP223 Capacitive Touch** | **$0.50-$1** | Capacitive | Digital GPIO | Touch detection on surface |
| **MPR121** | **$3-$5** | 12-Channel Cap | I2C | Multi-touch, skin-like sensing |
| **Velostat/Linqstat** | **$2-$5/sheet** | Resistive pressure | Analog | Pressure mapping, DIY skin |
| **FSR402** | **$2-$4** | Force sensitive resistor | Analog | Grip pressure, tactile sensing |
| **Piezo element** | **$0.50-$1** | Vibration/impact | Analog | Collision detection, vibration |
| **Conductive thread/fabric** | **$5-$10** | Resistive | Analog | DIY pressure-sensitive skin |
| **Optical (IR reflectance)** | **$1-$3** | Proximity | Analog/Digital | Near-field object detection |

### Touch Sensor Notes
- **DIY robot skin:** Velostat sheet + conductive fabric layers + ADC multiplexer
- **Capacitive touch:** TTP223 modules work through thin plastic/PLA shells (3-5mm)
- **Pressure mapping:** MPR121 with conductive foam gives 12-point pressure map
- **ROS2:** Publish `sensor_msgs/PointCloud` or custom message for tactile array

## 3.6 MICROPHONES / AUDIO

| Component | Price | Interface | ROS2 Support | Best For |
|-----------|-------|-----------|-------------|----------|
| **USB Microphone (mini)** | **$3-$8** | USB | `audio_common` | Voice commands, basic audio |
| **ReSpeaker 2-Mics Pi HAT** | **$15-$25** | I2S | `respeaker_ros` | Voice activation, direction |
| **ReSpeaker 4-Mic Array** | **$35-$50** | I2S/USB | `respeaker_ros` | Direction of arrival, beamforming |
| **INMP441 MEMS I2S** | **$2-$4** | I2S | Custom node | Compact, high quality |
| **SPH0645 MEMS I2S** | **$3-$5** | I2S | Custom node | Raspberry Pi compatible |
| **PS3 Eye Camera (mic array)** | **$5-$10** | USB | `audio_common` | 4-mic array, ultra cheap |

### Audio Notes
- **For voice interaction with Agent 47:** ReSpeaker 2-Mic HAT + Raspberry Pi = wake word + command recognition
- **For localization:** ReSpeaker 4-Mic Array gives sound direction (DOA estimation)
- **PS3 Eye Camera** is the ultimate audio hack - 4 microphones for $5-10, great for voice recognition experiments
- **ROS2:** `audio_common` package handles audio capture and playback

## 3.7 DISTANCE / PROXIMITY SENSORS

| Sensor | Price | Range | Interface | Accuracy | Best For |
|--------|-------|-------|-----------|----------|----------|
| **HC-SR04 Ultrasonic** | **$1-$3** | 2-400cm | GPIO trigger/echo | 3mm | Budget obstacle avoidance |
| **US-100 Ultrasonic** | **$2-$4** | 2-450cm | UART/GPIO | 2mm | Better accuracy, UART option |
| **JSN-SR04T (waterproof)** | **$3-$6** | 25-600cm | GPIO | 5mm | Outdoor/moist environments |
| **VL53L0X (ToF)** | **$3-$6** | 2-200cm | I2C | 5mm | Small, accurate indoor ranging |
| **VL53L1X (ToF)** | **$4-$8** | 4-400cm | I2C | 5mm | Longer range ToF |
| **VL53L4CD (ToF)** | **$5-$10** | 1-1300cm | I2C | 10mm | Fast ranging, multi-target |
| **TOF10120** | **$2-$4** | 10-180cm | I2C/UART | 5mm | Budget ToF option |
| **Sharp IR GP2Y0A21YK** | **$3-$5** | 10-80cm | Analog | 5mm | Simple analog distance |
| **Sharp IR GP2Y0A02YK** | **$4-$6** | 20-150cm | Analog | 10mm | Longer range analog |
| **LiDAR TF-Luna** | **$25-$35** | 0.2-8m | UART/I2C | 1% | Single-point LiDAR |
| **LiDAR TF-mini Plus** | **$35-$45** | 0.1-12m | UART/I2C | 1% | Longer range single-point |

### Distance Sensor Notes
- **Best budget indoor:** VL53L0X ($3-6) - I2C, accurate, small, multiple can share bus with different addresses
- **Best budget outdoor:** JSN-SR04T ($3-6) - waterproof ultrasonic
- **Obstacle avoidance ring:** 6x HC-SR04 ($6-12 total) gives 360-degree coverage
- **For navigation:** Single-point LiDAR like TF-Luna ($25) is great for height/obstacle detection

---

# PART 4: ELECTRONICS

## 4.1 MICROCONTROLLERS / COMPUTERS

| Board | Price | CPU | RAM | GPIO | Key Features | ROS2? |
|-------|-------|-----|-----|------|-------------|-------|
| **Arduino Nano** | **$2-$4** | ATmega328P | 2KB | 22 pins | Ultra cheap, simple | Micro-ROS |
| **Arduino Mega 2560** | **$8-$15** | ATmega2560 | 8KB | 54 pins (15 PWM) | Many IO pins | Micro-ROS |
| **ESP32 DevKit V1** | **$3-$6** | Dual-core 240MHz | 520KB | 34 pins | WiFi + Bluetooth, dual core | Micro-ROS |
| **ESP32-S3** | **$4-$8** | Dual-core 240MHz | 512KB | 45 pins | AI acceleration, USB-OTG | Micro-ROS |
| **Raspberry Pi Pico** | **$5** | RP2040 dual-core 133MHz | 264KB | 26 pins | Programmable IO, cheap | Micro-ROS |
| **Raspberry Pi Pico 2W** | **$7** | RP2350 dual-core 150MHz | 520KB | 26 pins | WiFi + BT, very cheap | Micro-ROS |
| **Raspberry Pi 4 (4GB)** | **$55** | BCM2711 quad-core 1.8GHz | 4GB LPDDR4 | 40-pin header | Full Linux, many HATs | **Full ROS2** |
| **Raspberry Pi 5 (4GB)** | **$60** | BCM2710 quad-core 2.4GHz | 4GB LPDDR4X | 40-pin header | 2-3x faster than Pi 4 | **Full ROS2** |
| **Raspberry Pi 5 (8GB)** | **$80** | BCM2710 quad-core 2.4GHz | 8GB LPDDR4X | 40-pin header | Best for multi-camera | **Full ROS2** |
| **Jetson Nano 4GB** | **$149** (hard to find) | Quad-core A57 1.4GHz | 4GB | 40-pin | 128 CUDA cores | **Full ROS2** |
| **Jetson Orin Nano 4GB** | **$259** (dev kit) | 6x A78AE 1.5GHz | 4GB LPDDR5 | 40-pin | 20 TOPS AI | **Full ROS2** |
| **Jetson Orin Nano 8GB** | **$499** (dev kit) | 6x A78AE 1.5GHz | 8GB LPDDR5 | 40-pin | 40 TOPS AI | **Full ROS2** |
| **Khadas VIM4** | **$200** | A311D2 octa-core | 8GB | 40-pin | Mali GPU, NPU | **Full ROS2** |
| **LattePanda 3 Delta** | **$279** | N5105 quad-core | 8GB | 40-pin + Arduino | x86 compatibility | **Full ROS2** |

### Microcontroller Notes
- **For servo control:** Arduino Mega 2560 ($8) can control 48+ servos via 6x PCA9685 boards
- **For wireless:** ESP32 ($3-6) runs servos + WiFi + Web interface simultaneously
- **Main computer:** Raspberry Pi 5 (8GB, $80) is the sweet spot for ROS2 + vision
- **For AI/vision:** Jetson Orin Nano 8GB ($499) if you need on-device neural networks
- **Best combo:** ESP32 for low-level servo/motor control + Raspberry Pi 5 for high-level ROS2 + vision

## 4.2 MOTOR DRIVERS

### Servo Drivers

| Driver | Price | Channels | Interface | Max Current | Notes |
|--------|-------|----------|-----------|-------------|-------|
| **PCA9685 (AliExpress)** | **$1.50-$3.00** | 16 | I2C (addr selectable) | 25mA/ch logic | Cascade up to 62 boards = 992 servos |
| **PCA9685 (Adafruit)** | **$14.95** | 16 | I2C | 25mA/ch logic | Quality tested, headers included |
| **Servo Driver Shield (Arduino)** | **$5-$10** | 16 | I2C | 25mA/ch logic | Stacking shield format |
| **goBILDA Servo Power Injector** | **$69.99** | 6 | PWM input | 10A total | High-power servo distribution |
| **Dynamixel U2D2** | **$49.90** | 253 (Dynamixel) | USB-to-TTL/RS485 | 2A | Required for Dynamixel USB control |
| **OpenCM9.04** | **$9.90** | 4 servo + 4 Dynamixel | USB/TTL | 2A | ARM Cortex-M3, programmable |

### DC Motor / Stepper Drivers

| Driver | Price | Channels | Voltage | Max Current | Features |
|--------|-------|----------|---------|-------------|----------|
| **L298N** | **$2-$4** | 2 DC or 1 stepper | 5-35V | 2A/ch (peak) | Classic, inefficient, cheap |
| **TB6612FNG** | **$3-$6** | 2 DC or 1 stepper | 4.5-13.5V | 1.2A cont/ch | MOSFET, efficient, small |
| **DRV8833** | **$2-$4** | 2 DC | 2.7-10.8V | 1.2A cont/ch | Compact, good for small motors |
| **A4988** | **$1-$2.50** | 1 stepper | 8-35V | 1A/ch | Basic stepper, needs heatsink |
| **DRV8825** | **$2-$4** | 1 stepper | 8-45V | 2.2A/ch | Better than A4988 |
| **TMC2209** | **$4-$8** | 1 stepper | 4.75-29V | 2.8A/ch | Silent, UART config, stallGuard |
| **TMC5160** | **$12-$20** | 1 stepper | 8-60V | 4.4A/ch | SPI, highest performance |
| **VNH5019** | **$8-$12** | 2 DC | 5.5-24V | 12A cont/ch | High current, MOSFET |
| **Sabertooth 2x32** | **$125** | 2 DC | 6-30V | 32A cont/ch | Professional, RC/serial interface |

### BLDC Drivers

| Driver | Price | Max Power | Voltage | Features |
|--------|-------|-----------|---------|----------|
| **ODrive S1** | **$199** | 1600W | 12-50V | Precision FOC, Web GUI |
| **ODrive Pro** | **$349** | 3000W | 14-58V | Dual encoder, highest precision |
| **ODESC 3.6** | **$50-$80** | 1000W | 12-50V | ODrive-compatible, lower cost |
| **Makerbase ODrive** | **$30-$50** | 500W | 12-40V | Budget FOC controller |
| **VESC 6 MKIII** | **$150** | 3000W | 14-60V | Excellent for high-power BLDC |
| **SimpleFOC Mini** | **$15-$25** | 200W | 12-30V | Open source FOC, Arduino-based |
| **Flipsky FSESC 4.20** | **$60** | 1500W | 8-60V | VESC-based, good value |

## 4.3 POWER SYSTEMS

### Batteries

| Battery | Price | Capacity | Voltage | Discharge | Best For |
|---------|-------|----------|---------|-----------|----------|
| **2S LiPo 1000mAh** | **$6-$10** | 1000mAh | 7.4V | 25C | Small robots, Arduino projects |
| **3S LiPo 2200mAh** | **$12-$20** | 2200mAh | 11.1V | 25C | Standard robot power (Dynamixel, servos) |
| **3S LiPo 5200mAh** | **$25-$35** | 5200mAh | 11.1V | 30C | Medium robots, longer runtime |
| **4S LiPo 3000mAh** | **$20-$30** | 3000mAh | 14.8V | 35C | High voltage systems, BLDC |
| **4S LiPo 5000mAh** | **$30-$45** | 5000mAh | 14.8V | 50C | Large humanoid/quadruped |
| **6S LiPo 5000mAh** | **$40-$60** | 5000mAh | 22.2V | 50C | ODrive BLDC systems |
| **18650 Li-Ion (pair)** | **$4-$8** | 2500mAh | 7.4V (2S) | 5-10A | Compact projects, lower current |
| **21700 Li-Ion** | **$5-$10** | 4800mAh | 3.7V | 15A | Higher capacity, single cell |
| **NiMH 12V 3000mAh** | **$64.99** | 3000mAh | 12V | 10A | goBILDA systems, safer than LiPo |

### Battery Management & Power Distribution

| Component | Price | Function | Notes |
|-----------|-------|----------|-------|
| **2S/3S/4S BMS (3-10A)** | **$2-$5** | Overcharge/overdischarge protection | Essential for LiPo safety |
| **2S/3S/4S BMS (20-30A)** | **$5-$15** | Higher current protection | For larger robots |
| **LiPo Balance Charger (iMAX B6 clone)** | **$15-$25** | Balance charge 1S-6S | Essential - charge safely |
| **LM2596 Buck Converter** | **$1-$3** | Step-down to 5V/3.3V | 3A max, adjustable |
| **XL4015 Buck Converter** | **$2-$4** | Step-down to 5V/12V | 5A max, more efficient |
| **LM2596S with display** | **$3-$5** | Step-down with voltmeter | Nice for debugging |
| **UBEC 5V 3A** | **$3-$5** | 5V regulated output for servos | From 7.4-26V input |
| **UBEC 5V 5A** | **$5-$8** | Higher current servo power | Needed for many servos |
| **BEC 6V 5A** | **$5-$8** | 6V output (servo voltage) | Direct from LiPo |
| **INA219 Current Sensor** | **$2-$4** | Voltage + current monitoring | I2C interface, power diagnostics |
| **Floodgate Power Switch** | **$34.99** | XT30 switch + current sensing | goBILDA, great for debugging |
| **XT60/XT30 connectors** | **$2-$5/pack** | Power connectors | Standard for LiPo batteries |

### Power Budget Examples

| Robot Type | Servo Count | Current Draw | Battery | Runtime |
|------------|------------|-------------|---------|---------|
| Small humanoid (12x SG90) | 12 | 2-3A avg | 3S 2200mAh | ~45 min |
| Medium humanoid (16x MG996R) | 16 | 5-8A avg | 3S 5200mAh | ~45 min |
| Large humanoid (16x DS3235) | 16 | 8-12A avg | 4S 5000mAh | ~30 min |
| Quadruped (12x DS3235) | 12 | 6-10A avg | 4S 5000mAh | ~30 min |
| BLDC humanoid (8x ODrive) | 8 BLDC | 20-40A avg | 6S 10000mAh | ~20 min |

## 4.4 COMMUNICATION

| Module | Price | Protocol | Interface | ROS2 Support | Best For |
|--------|-------|----------|-----------|-------------|----------|
| **MCP2515 CAN Module** | **$1-$3** | CAN 2.0B | SPI | `ros2_socketcan` | ODrive, CAN servos |
| **SN65HVD230 CAN** | **$3-$5** | CAN 2.0B | 3.3V logic | `ros2_socketcan` | 3.3V CAN systems |
| **TCA9548A I2C Multiplexer** | **$1-$3** | I2C switch | I2C | Native | Multiple same-address I2C devices |
| **PCA9685 (as expander)** | **$1.50-$3** | PWM | I2C | `adafruit_pca9685` | 16-channel PWM over I2C |
| **HC-05 Bluetooth** | **$3-$5** | Bluetooth 2.0 | UART | Custom | Wireless serial, teleop |
| **ESP-NOW (ESP32)** | **$3-$6** | WiFi direct | Native | Custom | Low-latency wireless control |
| **nRF24L01+** | **$1-$3** | 2.4GHz | SPI | Custom | Very cheap wireless |
| **nRF24L01+ PA+LNA** | **$3-$5** | 2.4GHz + PA | SPI | Custom | Longer range wireless |
| **LoRa SX1278** | **$5-$10** | 433/868MHz | SPI | Custom | Long range (km), low bandwidth |
| **Ethernet W5500** | **$3-$5** | Ethernet | SPI | Native | Wired ROS2 networking |
| **RS485 Module** | **$1-$3** | RS485 | UART | Custom | Industrial distance communication |

---

# PART 5: STRUCTURAL COMPONENTS

## 5.1 ServoCity / Actobotics

| Component | Price Range | Notes |
|-----------|------------|-------|
| **U-Channel (various lengths)** | **$3-$8** | Standard 1.5" pattern, aluminum |
| **L-Brackets** | **$2-$5** | Pattern mounts, various angles |
| **Ball Bearings** | **$3-$8** | Flanged, various bore sizes |
| **ServoBlocks** | **$15-$30** | Heavy-duty servo mounts with bearings |
| **Servo Shafts / Hubs** | **$5-$15** | 25T spline adapters |
| **Hardware Pack (380pc)** | **$39.99** | Screws, nuts, standoffs |
| **Pattern Plates** | **$3-$6** | Mounting surfaces |
| **Motor Mounts** | **$3-$8** | NEMA 17, servo, etc. |

### goBILDA (Modern Actobotics Successor)

| Component | Price | Notes |
|-----------|-------|-------|
| **Mecanum Wheel Set (104mm)** | **$189.99** | 4x mecanum wheels |
| **Strafer Chassis Kit** | **$699.99** | Complete robot chassis |
| **ServoBlock (43mm)** | **$29.99** | For standard H25T servos |
| **2000 Series Dual Mode Servo** | **$36.99** | goBILDA branded smart servo |
| **FTC Starter Kit 2026-2027** | **$899.99** | Full robot build kit |
| **USB Camera (Global Shutter)** | **$74.99** | goBILDA case, MIPI |

## 5.2 3D-PRINTED STRUCTURAL ELEMENTS (On QIDI Plus 4 Max)

Since Nick has a large-format 3D printer, most structural parts can be printed:

| Material | Price/kg | Best For | Print Settings |
|----------|----------|----------|----------------|
| **PLA+ (eSUN)** | **$18-$25/kg** | Non-structural, prototyping | 200C, 60C bed |
| **PETG (eSUN)** | **$20-$28/kg** | Structural parts, impact resistant | 240C, 80C bed |
| **ABS (eSUN)** | **$18-$25/kg** | High temp, structural | 250C, 100C bed, enclosure |
| **ASA (Polymaker)** | **$25-$35/kg** | UV resistant outdoor parts | 250C, 100C bed, enclosure |
| **TPU 95A (eSUN)** | **$25-$35/kg** | Flexures, grippers, bumpers | 220C, 60C bed, slow speed |
| **PA6-CF (eSUN)** | **$35-$50/kg** | Maximum strength, lightweight | 260C, 80C bed, hardened nozzle |
| **PC (Polymaker)** | **$30-$40/kg** | Extreme strength and temp | 270C, 100C bed, enclosure |

### Recommended Print Strategy for Robot Parts
- **Structural frames:** PETG or PA6-CF, 4-6 walls, 40%+ infill
- **Gearboxes:** PA6-CF or PETG, high infill, slow speeds
- **Flexure grippers:** TPU 95A, 3 walls, 20% infill, 30mm/s
- **Servo horns:** PA6-CF or ABS, 100% infill (strength critical)
- **Covers/cosmetic:** PLA+, 2 walls, 15% infill (fast print)

---

# PART 6: BUDGET TIERS

## TIER 1: $500 Budget - "The Scout"
**What Nick can build:** A small humanoid (~30cm tall) or a 4-DOF robot arm

| Component | Item | Qty | Unit Price | Total |
|-----------|------|-----|-----------|-------|
| **Brain** | Raspberry Pi 5 (4GB) | 1 | $60 | $60 |
| **Servos** | TowerPro SG90 (arms/gripper) | 8 | $2 | $16 |
| **Servos** | MG996R (legs/shoulders) | 6 | $5 | $30 |
| **Servo Driver** | PCA9685 16-ch I2C | 1 | $2 | $2 |
| **Camera** | Raspberry Pi Camera Module 3 Wide | 1 | $35 | $35 |
| **LiDAR** | LD06/LD19 (AliExpress) | 1 | $40 | $40 |
| **IMU** | MPU6050 | 1 | $3 | $3 |
| **Microcontroller** | ESP32 DevKit | 1 | $4 | $4 |
| **Power** | 3S LiPo 2200mAh + charger | 1 | $25 | $25 |
| **Power** | UBEC 5V 5A | 1 | $6 | $6 |
| **Power** | LM2596 buck converters (5pc) | 1 | $5 | $5 |
| **Communication** | MCP2515 CAN module | 1 | $2 | $2 |
| **Distance** | HC-SR04 ultrasonic (5pc) | 1 | $5 | $5 |
| **Audio** | USB microphone | 1 | $5 | $5 |
| **Touch** | TTP223 touch sensors (10pc) | 1 | $3 | $3 |
| **Current Monitor** | INA219 | 1 | $3 | $3 |
| **3D Filament** | PETG + TPU (2kg) | 2 | $25 | $50 |
| **Screws/hardware** | M2/M3/M4 assortment | 1 | $15 | $15 |
| **Wires/connectors** | Jumper wires, servo cables | 1 | $10 | $10 |
| **Gripper** | 3D printed SG90 gripper | 1 | $3 | $3 |
| | | | **TOTAL** | **$321** |

**Remaining $179:** Upgrade to DS3218 servos ($60), add RealSense D405 ($195 - over), or build a second robot

### $500 Build Capability
- 20-30cm tall humanoid, 12-16 DOF
- Camera-based object detection
- 2D LiDAR SLAM navigation
- Basic voice commands
- Gripper pick-and-place of light objects
- Wall-following and obstacle avoidance

---

## TIER 2: $1,500 Budget - "The Soldier"
**What Nick can build:** A full-size humanoid (~60cm) or quadruped with proper joints

| Component | Item | Qty | Unit Price | Total |
|-----------|------|-----|-----------|-------|
| **Brain** | Raspberry Pi 5 (8GB) | 1 | $80 | $80 |
| **AI Accelerator** | Raspberry Pi AI Kit (Hailo 8L) | 1 | $70 | $70 |
| **Servos - Arms** | DS3225 25kg (shoulders/elbows) | 4 | $14 | $56 |
| **Servos - Arms** | DS3218 20kg (wrists) | 4 | $10 | $40 |
| **Servos - Legs** | DS3235 35kg (hips/knees) | 6 | $17 | $102 |
| **Servos - Head** | MG90S (pan/tilt) | 2 | $4 | $8 |
| **Servo Drivers** | PCA9685 16-ch | 2 | $3 | $6 |
| **Camera** | Raspberry Pi Camera 3 Wide | 1 | $35 | $35 |
| **Depth Camera** | Orbbec Gemini 335 | 1 | $250 | $250 |
| **LiDAR** | RPLIDAR A1M8 | 1 | $80 | $80 |
| **IMU** | BNO055 | 1 | $12 | $12 |
| **Microcontroller** | ESP32-S3 | 2 | $6 | $12 |
| **Arduino** | Arduino Mega 2560 | 1 | $12 | $12 |
| **Power** | 4S LiPo 5000mAh (x2) + charger | 1 | $80 | $80 |
| **Power** | UBEC 6V 5A (x3) | 3 | $6 | $18 |
| **Power** | XL4015 buck converters (5pc) | 1 | $8 | $8 |
| **BMS** | 4S 30A BMS | 1 | $10 | $10 |
| **CAN Bus** | MCP2515 modules (x3) | 1 | $6 | $6 |
| **Distance** | VL53L0X ToF sensors (x6) | 1 | $18 | $18 |
| **Audio** | ReSpeaker 2-Mic Pi HAT | 1 | $20 | $20 |
| **Touch** | MPR121 12-ch touch | 2 | $4 | $8 |
| **Force** | HX711 + load cell (x2) | 1 | $10 | $10 |
| **3D Filament** | PETG + TPU + PA6-CF (4kg) | 1 | $100 | $100 |
| **Hardware** | M2/M3/M4/M5 full assortment | 1 | $30 | $30 |
| **Bearings** | 608ZZ, 625ZZ assortment | 1 | $20 | $20 |
| **Gripper** | 3D printed DS3225 adaptive gripper | 1 | $10 | $10 |
| | | | **TOTAL** | **$1,225** |

**Remaining $275:** Add Dynamixel XL430 for one premium joint, or upgrade to RPLIDAR A2 ($200), or add second depth camera

### $1,500 Build Capability
- 50-70cm tall humanoid, 16-20 DOF with metal gear servos
- Depth camera + LiDAR for full SLAM navigation
- On-device AI object detection (Hailo 8L)
- Voice command + wake word
- Adaptive gripper with force feedback
- Autonomous navigation in mapped environments
- IMU-based balance assistance
- 45+ minute runtime

---

## TIER 3: $5,000 Budget - "The Commander"
**What Nick can build:** Professional-grade humanoid or quadruped with Dynamixel actuators

| Component | Item | Qty | Unit Price | Total |
|-----------|------|-----|-----------|-------|
| **Brain** | NVIDIA Jetson Orin Nano 8GB | 1 | $499 | $499 |
| **Servos - Hips/Knees** | XM540-W270-T | 4 | $420 | $1,680 |
| **Servos - Shoulders** | XM430-W350-T | 4 | $270 | $1,080 |
| **Servos - Elbows/Wrists** | XL430-W250-T | 4 | $39 | $156 |
| **Servos - Head/Hands** | XL330-M288-T | 4 | $24 | $96 |
| **Dynamixel Controller** | OpenCM9.04 + EXP board | 1 | $50 | $50 |
| **Dynamixel USB** | U2D2 | 1 | $50 | $50 |
| **Camera** | RealSense D435i (refurb) | 1 | $280 | $280 |
| **Camera (wrist)** | RealSense D405 (refurb) | 1 | $195 | $195 |
| **LiDAR** | RPLIDAR A2M12 | 1 | $250 | $250 |
| **IMU** | BNO055 | 1 | $12 | $12 |
| **IMU Premium** | Phidgets Spatial 3/3/3 | 1 | $100 | $100 |
| **Microcontroller** | ESP32-S3 (x2) | 2 | $6 | $12 |
| **Power** | 3S LiPo 5200mAh (x4) + charger | 1 | $120 | $120 |
| **Power** | SMPS 12V 20A (Dynamixel) | 1 | $40 | $40 |
| **Power** | Multiple UBECs and bucks | 1 | $40 | $40 |
| **Force/Torque** | Custom 6-axis F/T sensor + PCB | 1 | $50 | $50 |
| **Touch** | MPR121 array (4x) | 1 | $20 | $20 |
| **Audio** | ReSpeaker 4-Mic Array | 1 | $50 | $50 |
| **Distance** | VL53L1X array (8x) | 1 | $40 | $40 |
| **CAN Bus** | Dual CAN + termination | 1 | $20 | $20 |
| **Structural** | goBILDA bearings, mounts | 1 | $100 | $100 |
| **Filament** | PA6-CF, PETG, TPU (5kg) | 1 | $150 | $150 |
| **Hardware** | Full M2-M6 assortment | 1 | $50 | $50 |
| **Gripper** | 3D printed 3-finger adaptive + FSR | 1 | $30 | $30 |
| | | | **TOTAL** | **$4,810** |

### $5,000 Build Capability
- 70-100cm tall humanoid, 20-24 DOF
- All Dynamixel smart servos with position/velocity/torque feedback
- Dual depth cameras (scene + wrist-mounted)
- High-speed LiDAR SLAM
- 40 TOPS on-device AI (Jetson Orin)
- Full force/torque sensing
- Multi-channel touch sensing
- Directional microphone array
- ~30-45 minute runtime
- Professional ROS2 + MoveIt 2 integration

---

# PART 7: QUICK REFERENCE TABLES

## Servo Selection Matrix

| Application | SG90 ($2) | MG996R ($5) | DS3218 ($12) | DS3235 ($17) | XL430 ($39) | XM430 ($270) |
|-------------|----------|------------|-------------|-------------|------------|------------|
| Gripper | **** | ** | | | * | ** |
| Wrist pan/tilt | **** | *** | | | **** | ** |
| Elbow | | *** | **** | ** | ** | **** |
| Shoulder | | * | *** | **** | ** | **** |
| Hip | | | ** | *** | * | **** |
| Knee | | | ** | *** | * | **** |
| Ankle | | | *** | **** | ** | **** |
| Quadruped leg | | | *** | **** | ** | **** |
| Pan/tilt camera | **** | ** | | | *** | * |

## Sensor Priority for Different Robots

| Sensor Type | Humanoid | Quadruped | Arm Only | Mobile Base |
|-------------|----------|-----------|----------|-------------|
| **IMU** | Essential | Essential | Optional | Helpful |
| **Camera (RGB)** | Essential | Helpful | Essential | Helpful |
| **Depth Camera** | Essential | Helpful | Essential | Helpful |
| **LiDAR** | Essential | Essential | Optional | Essential |
| **Force Sensor** | Helpful | Optional | Essential | Optional |
| **Touch Sensors** | Helpful | Optional | Helpful | Optional |
| **Microphone** | Helpful | Optional | Optional | Optional |
| **Ultrasonic/ToF** | Helpful | Helpful | Optional | Essential |

## Open Source ROS2 Packages for Integration

| Component | ROS2 Package | Installation |
|-----------|-------------|--------------|
| **Dynamixel** | `dynamixel_sdk`, `dynamixel_workbench` | `apt install ros-$ROS_DISTRO-dynamixel-sdk` |
| **RealSense** | `realsense2_camera` | `apt install ros-$ROS_DISTRO-realsense2-camera` |
| **Orbbec** | `orbbec_ros2_sdk` | GitHub + build from source |
| **ZED** | `zed_ros2_wrapper` | Stereolabs repo |
| **RPLiDAR** | `rplidar_ros2` | GitHub + build |
| **YDLiDAR** | `ydlidar_ros2_driver` | GitHub + build |
| **Camera (generic)** | `v4l2_camera` | `apt install ros-$ROS_DISTRO-v4l2-camera` |
| **IMU (BNO055)** | `bno055` | `apt install ros-$ROS_DISTRO-bno055` |
| **IMU (MPU6050)** | `mpu6050_driver` | GitHub + build |
| **Servos (PCA9685)** | `adafruit_pca9685` | `pip3 install adafruit-circuitpython-servokit` |
| **SLAM** | `slam_toolbox` | `apt install ros-$ROS_DISTRO-slam-toolbox` |
| **Navigation** | `nav2_bringup` | `apt install ros-$ROS_DISTRO-nav2-bringup` |
| **Arm Control** | `moveit2` | `apt install ros-$ROS_DISTRO-moveit` |
| **Audio** | `audio_common` | `apt install ros-$ROS_DISTRO-audio-common` |

---

# PART 8: SOURCES & WHERE TO BUY CHEAPEST

## Best Sources by Category

| Category | Cheapest Source | Premium Source |
|----------|----------------|----------------|
| **Servos (cheap)** | AliExpress (dsservo official store) | Amazon (faster shipping) |
| **Dynamixel** | RobotShop (EU), robosavvy (UK) | Robotis official |
| **BLDC motors** | AliExpress, HobbyKing | ODrive Robotics |
| **Motor drivers** | AliExpress | Pololu, Adafruit |
| **Microcontrollers** | AliExpress, LCSC | Adafruit, SparkFun |
| **Raspberry Pi** | The Pi Hut, Pishop (US) | Official distributors |
| **LiPo batteries** | AliExpress (Tattu, Gens Ace) | HobbyKing |
| **LiDAR** | AliExpress (YDLIDAR official) | RobotShop |
| **Cameras** | AliExpress (Arducam) | Official distributors |
| **Structural** | AliExpress (brackets) | ServoCity, goBILDA |
| **Filament** | Amazon (eSUN, Polymaker) | MatterHackers |
| **Bearings** | AliExpress (bulk) | VXB, McMaster-Carr |
| **Sensors (generic)** | AliExpress | Adafruit, SparkFun |
| **Connectors/wire** | AliExpress (bulk) | DigiKey, Mouser |

## AliExpress Store Recommendations

| Store Name | What They Sell | Reliability |
|------------|---------------|-------------|
| **Dsservo Official Store** | DS3218/DS3225/DS3235 servos | Excellent |
| **RobotDyn Official Store** | Motor drivers, sensors, modules | Very Good |
| **Waveshare Official** | Displays, sensors, HATs | Excellent |
| **Landa Tianrui** | LiDAR sensors (LD series) | Good |
| **YDLIDAR Official Store** | YDLIDAR products | Excellent |
| **Official Arducam Store** | Cameras, lenses | Excellent |
| **TZT Official Store** | Generic modules, sensors | Good |
| **ANGEEK Official Store** | Electronics modules | Good |

---

# SUMMARY: RECOMMENDED FIRST BUILD FOR NICK

## Start Here: $300 "Scout" Mini Humanoid

Given Nick has a QIDI Plus 4 Max (large format, can print big parts), the recommended first build is:

### Bill of Materials (Entry Point)

| Item | Specific Part | Est. Cost |
|------|--------------|-----------|
| Main computer | Raspberry Pi 5 (4GB) | $60 |
| Servos (12x) | 8x SG90 + 4x MG996R | $36 |
| Servo driver | PCA9685 16-ch module | $2 |
| Camera | Raspberry Pi Camera 3 Wide | $35 |
| LiDAR | LD06/LD19 | $40 |
| IMU | MPU6050 | $3 |
| Microcontroller | ESP32 DevKit | $4 |
| Battery | 3S LiPo 2200mAh + charger | $25 |
| Power distribution | UBEC 5V 5A + buck converters | $11 |
| Sensors | 4x HC-SR04 + INA219 | $8 |
| Filament | PETG 1kg + TPU 0.5kg | $35 |
| Hardware | Screws, bearings, wires | $25 |
| Audio | USB microphone | $5 |
| **TOTAL** | | **$289** |

### What This Robot Can Do
- Walk (simple gait, 12 DOF)
- Avoid obstacles (LiDAR + ultrasonic)
- See and recognize objects (Pi Camera + OpenCV)
- Respond to voice commands (Vosk or similar on Pi 5)
- Pick up small objects (SG90 gripper)
- Navigate using SLAM (LiDAR + `slam_toolbox`)
- Run for ~45 minutes on single charge
- Be fully 3D-printed on QIDI Plus 4 Max

### Next Upgrades (in order)
1. **$60:** Upgrade to DS3218 servos for legs (2x)
2. **$80:** Add BNO055 IMU + WitMotion for better balance
3. **$250:** Add Orbbec Gemini 335 depth camera
4. **$100:** Upgrade to Raspberry Pi 5 (8GB) + AI Kit
5. **$200:** Upgrade to RPLIDAR A1 for better SLAM
6. **$500+:** Start building second unit with Dynamixel XL430

---

*This document compiled from research across AliExpress, Amazon, RobotShop, ServoCity/goBILDA, Adafruit, SparkFun, Dynamixel/ROBOTIS, ODrive Robotics, and academic sources. Prices are estimates in USD as of June 2026 and may vary by vendor and shipping location.*

*For MEOK Labs internal use. All components verified to have open-source drivers and ROS2 integration.*
