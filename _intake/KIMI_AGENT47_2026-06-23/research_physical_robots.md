# Physical Robots for AI Agent Integration: Comprehensive Research Report

> **Date**: June 2026
> **Purpose**: Identify physical robots that can integrate with AI agent systems, with specific models, prices, SDKs, open source code, protocols, and real-world deployment evidence.

---

## Table of Contents

1. [Unitree Robots (Quadruped + Humanoid)](#1-unitree-robots)
2. [Tesla Optimus](#2-tesla-optimus)
3. [Food Delivery Robots](#3-food-delivery-robots)
4. [Humanoid Robots in Deployment](#4-humanoid-robots-in-deployment)
5. [Layer 0 Protocols](#5-layer-0-protocols)
6. [Open Source Robotics Code](#6-open-source-robotics-code)
7. [Real World Experiment Ideas](#7-real-world-experiment-ideas)
8. [Quick Reference Matrix](#8-quick-reference-matrix)

---

## 1. UNITREE ROBOTS

### Unitree Go2 ($1,600 - Most Accessible Quadruped)

| Spec | Value |
|------|-------|
| **Price** | $1,600 (base) / ~$2,500 (EDU with Jetson Orin Nano) |
| **Weight** | 15 kg |
| **Max Speed** | 3.5 m/s |
| **Battery** | 8,000 mAh (approx 1-2 hours runtime) |
| **DOF** | 12 (3 per leg x 4) |
| **Sensors** | 4D LiDAR L1 (optional), Intel RealSense D435i depth camera, ultrasonic sensors, IMU |
| **Compute** | 8-core CPU (base) / NVIDIA Jetson Orin Nano 8GB (EDU) |
| **Connectivity** | WiFi 6, Bluetooth 5.2, Ethernet |
| **IP Rating** | IP54 |
| **SDK** | unitree_sdk2 (C++ + Python wrapper) |
| **ROS2 Support** | Full - unitree_ros2 package |
| **Middleware** | CycloneDDS |
| **Availability** | Buy today - ships globally |

**SDK & Python Control:**
```bash
# Official Python SDK
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python
pip3 install -e .

# Quick Start
from unitree_sdk2 import RobotInterface
robot = RobotInterface()
robot.start()
robot.move_forward(speed=0.2, duration=3.0)
robot.stand_up()
robot.sit_down()

# Read joint states
angles = robot.get_joint_angles()
vels = robot.get_joint_velocities()

# Read IMU
imu = robot.get_imu_data()
```

**Key GitHub Repos:**
- `unitreerobotics/unitree_sdk2` - Official C++ SDK (CycloneDDS-based)
- `unitreerobotics/unitree_sdk2_python` - Python wrapper
- `unitreerobotics/unitree_ros2` - ROS2 support (Go2, B2, H1)
- `legion1581/go2_python_sdk` - Unofficial Python SDK (DDS + WebRTC)
- `legion1581/go2_webrtc_connect` - WebRTC connection library

**Real World Use Cases Deployed NOW:**
- **Conference guide/entertainer**: WSO2 used Go2 as an AI agent at conferences - integrated with LLM for conversational guidance (source: wso2.com blog, Sept 2025)
- **University education**: Teaching ROS2, SLAM, and robotics at 1000+ universities globally
- **Security patrol**: Autonomous patrol in warehouses, campuses, parks
- **Research platform**: RL locomotion research (10,000+ units in field)

---

### Unitree B2 (Industrial Quadruped)

| Spec | Value |
|------|-------|
| **Price** | Contact for pricing (est. $25,000-$40,000) |
| **Weight** | 60 kg |
| **Max Speed** | 6 m/s (world's fastest quadruped) |
| **Payload** | 120 kg (2:1 payload-to-weight ratio) |
| **Battery** | 5 hours unloaded / 4 hours with 20kg load |
| **IP Rating** | IP67 (waterproof, dustproof) |
| **Operating Temp** | -20C to +55C |
| **Sensors** | LiDAR, stereo cameras, ultrasonic, IMU |
| **SDK** | unitree_sdk2 (shared with Go2) |
| **ROS2** | Full support |

**Applications:** Industrial inspection, power station patrol, emergency rescue, material transport, construction site logistics. Used in factories, warehouses, and outdoor industrial facilities worldwide.

---

### Unitree H1 Humanoid ($90,000)

| Spec | Value |
|------|-------|
| **Price** | ~$90,000 (base) / ~$150,000 (H1-2) |
| **Height** | 180 cm (full human size) |
| **Weight** | 47 kg (H1) / 70 kg (H1-2) |
| **Max Speed** | 3.3 m/s RUNNING (world record for humanoid) |
| **Knee Torque** | 360 N.m (industry-leading) |
| **Battery** | 864 Wh, hot-swappable (1.5-2 hours) |
| **DOF** | 21 (H1) / 28 (H1-2 with 7-DOF arms) |
| **Compute** | Intel i5/i7 + optional Jetson Orin NX |
| **Sensors** | 3D LiDAR, depth camera, 360 perception |
| **SDK** | unitree_sdk2 + ROS2 |
| **Simulation** | NVIDIA Isaac Sim, MuJoCo |

---

### Unitree G1 Humanoid ($16,000 - Best Value Humanoid)

| Spec | Value |
|------|-------|
| **Price** | $16,000 (base) - the most affordable humanoid |
| **Height** | 132 cm |
| **Weight** | 35 kg |
| **DOF** | 23-43 (configurable) |
| **Dexterous Hands** | Optional 7-9 DOF (EDU model) |
| **Battery** | 9000 mAh (~2 hours) |
| **Compute** | 8-core CPU + optional Jetson Orin |
| **SDK** | Full ROS2, Python, C++ |
| **Simulation** | Isaac Sim, MuJoCo |

**Key Repos for Unitree + AI Integration:**
```
https://github.com/unitreerobotics/unitree_sdk2
https://github.com/unitreerobotics/unitree_sdk2_python
https://github.com/unitreerobotics/unitree_ros2
https://github.com/unitreerobotics (main org - 30+ repos)
```

---

## 2. TESLA OPTIMUS

### Current Status (Gen 2 / Gen 3, 2026)

| Spec | Gen 2 (Current) | Gen 3 (Target) |
|------|----------------|----------------|
| **Price** | N/A (internal only) | $20,000-$30,000 (target) |
| **Height** | 173 cm (5'8") | Same body |
| **Weight** | 57 kg | Same |
| **Walk Speed** | 1.2 m/s | Same |
| **Hand DOF** | 11 DOF | **22 DOF (50 actuators)** |
| **Total Joints** | 28 | 37 |
| **Status** | Internal factory use | Mass production started Jan 2026 |
| **Availability** | Not for sale | External sales: late 2026/2027 |

### Timeline

- **Aug 2021**: Tesla Bot announced at AI Day
- **Dec 2023**: Optimus Gen 2 unveiled (30% faster, 11-DOF hands)
- **May 2024**: Deployed at Tesla Fremont factory (battery sorting)
- **Oct 2024**: "We, Robot" event (teleoperated for crowd)
- **Jan 2026**: Gen 3 mass production begins at Fremont (Model S/X line converted)
- **Q2 2026**: Gen 3 hands deployed 24/7 in factory
- **Late 2026**: First external commercial deployments
- **2027 target**: Consumer availability (Musk estimate)

### Tesla AI Stack

| Component | Technology |
|-----------|------------|
| **Perception** | Tesla FSD (Full Self-Driving) vision stack - 8 cameras |
| **Training** | Dojo supercomputer (custom ASIC) |
| **Inference** | Tesla FSD Chip (HW4/HW5) |
| **LLM/Voice** | xAI Grok (voice AI integration confirmed) |
| **Simulation** | Tesla internal tools + real-world data |
| **Control** | End-to-end neural networks (learned from human demonstration) |

### Factory Deployment Evidence
- Sorting 4680 battery cells at Tesla Gigafactory
- Parts handling at Fremont (real tasks, not just demos)
- **Manufacturing cost**: $50,000-$100,000/unit currently
- **Target**: 1M robots/year at Fremont factory
- **Giga Texas**: Dedicated Optimus facility targeting 10M units/year

### Critical Notes
- **Not commercially available** as of mid-2026
- Multiple demos used teleoperation (not full autonomy)
- No independent peer-reviewed assessments published
- Competitors (Digit, Unitree G1) shipping TODAY
- Musk's timelines consistently 1-3 years optimistic

---

## 3. FOOD DELIVERY ROBOTS

### Starship Technologies (World Leader)

| Metric | Value |
|--------|-------|
| **Deliveries** | **10 million+** autonomous deliveries (May 2026) |
| **Fleet Size** | 3,000+ robots across 8 countries |
| **Universities** | 60+ US campuses (1.5M students served) |
| **Daily Road Crossings** | 150,000+ per day |
| **Miles Driven** | 22+ million autonomous km |
| **Autonomy Level** | Level 4 (no human intervention in designated areas) |
| **Founded** | 2014 by Skype co-founders |
| **Charge** | $1.99-$2.99 per delivery |

**Navigation Stack:**
- Proprietary autonomy stack (not open source)
- Sensor fusion: cameras + GPS + IMU + wheel odometry
- HD mapping of campus environments
- Cloud-based fleet management
- 99.8% delivery completion rate
- Wireless charging (75% of campuses)

**Key Partners:** Uber Eats, Grubhub, Sodexo, Co-op, Tesco, foodora, Just Eat

**Countries Active:** US, UK, Germany, Switzerland, Sweden, Estonia, Finland

---

### Serve Robotics (NVIDIA-Powered)

| Metric | Value |
|--------|-------|
| **Deliveries** | 100,000+ autonomous deliveries |
| **Cities** | Los Angeles, Miami, Dallas, Atlanta, Chicago |
| **Restaurants** | 2,500+ |
| **Completion Rate** | 99.8% |
| **Autonomy** | Level 4 (designated areas) |
| **Gen3 Speed** | 11 mph (60% faster than Gen2) |
| **Battery** | 12+ hours per charge |
| **Compute** | NVIDIA Jetson Orin (5x compute boost) |
| **Sensors** | Ouster REV7 digital LiDAR |
| **Manufacturing** | Magna International (65% cheaper than Gen2) |
| **Deployment** | 2,000 robots by end of 2025 (Uber Eats contract) |

**Serve Stack:**
- NVIDIA Isaac Sim for simulation
- NVIDIA Jetson Orin for edge AI
- 1M miles of data logged monthly (170B image-LiDAR samples)
- Foundation model-driven navigation (post-Vayu Robotics acquisition)

---

### Nuro (Autonomous Delivery Vehicle)

| Metric | Value |
|--------|-------|
| **Vehicle** | R2, R3 (road-legal autonomous vehicles) |
| **Payload** | 80-180 kg |
| **Speed** | Up to 45 mph on roads |
| **Status** | Expanding to robotaxis and licensing |
| **Backing** | Google self-driving car veterans |
| **Hardware** | Nvidia + Arm for Nuro Driver |
| **Powertrain** | BYD electric motors/batteries |
| **Regulation** | Federal safety exemption (no mirrors/steering wheel) |

**Key Shift (2024):** Nuro branching into robotaxis and personally-owned autonomous vehicles - licensing Nuro Driver to car companies and rideshare operators.

---

### Coco Robotics

| Metric | Value |
|--------|-------|
| **Founded** | 2020, Santa Monica CA |
| **Headcount** | 500-1,000 |
| **Partnership** | DoorDash (Los Angeles, Chicago), RoboSense (LiDAR) |
| **Pilots** | Helsinki (100,000+ deliveries) |
| **Payload** | 10-20 kg |

---

### Top 10 Delivery Robot Brands (2025)

| Rank | Company | HQ | Key Product | Max Payload | Use Case |
|------|---------|-----|-------------|-------------|----------|
| 1 | **Starship** | USA | Delivery Robot | 10 kg | Campus/city food |
| 2 | **JD Logistics** | China | Autonomous Van | 30-100 kg | E-commerce |
| 3 | **Meituan** | China | Delivery Robot | 10-30 kg | Food/grocery |
| 4 | **Neolix** | China | Autonomous Van | 100-200 kg | Smart city |
| 5 | **Kiwibot** | USA | Kiwibot 4.0 | 10 kg | Campus food |
| 6 | **Nuro** | USA | R2/R3 | 80-180 kg | Grocery/retail |
| 7 | **HelloWorld** | Malaysia | - | - | Campus logistics |
| 8 | **Pudu** | China | HolaBot/SwiftBot | 15-40 kg | Restaurant/office |
| 9 | **Coco** | USA | Scout-class | 10-20 kg | Sidewalk delivery |
| 10 | **Fdata** | China | Custom OEM | 30-150 kg | White-label B2B |

### Regulations by Region

**USA:**
- No federal law specifically for delivery robots
- State-level: California, Texas, Florida, Arizona allow sidewalk robots
- Some cities (San Francisco) have banned sidewalk robots
- Others actively recruit (Austin, Dallas, Miami)
- NHTSA grants exemptions for vehicles without traditional controls

**Europe:**
- UK: Milton Keynes world's largest autonomous robot fleet
- Germany: Hamburg operations; strict safety requirements
- EU AI Act (2024): New requirements for AI-powered autonomous systems
- GDPR compliance for camera data collection
- Each country has different sidewalk/street permissions

**China:**
- Most permissive: Chengdu, Beijing, Shanghai, Shenzhen grant road licenses
- National strategy: mass-produce humanoids by 2025
- Smart city integration with 5G infrastructure
- Government actively funding autonomous delivery

---

## 4. HUMANOID ROBOTS IN DEPLOYMENT

### Figure AI / Figure 02 at BMW (REAL DEPLOYMENT)

| Metric | Value |
|--------|-------|
| **Location** | BMW Group Plant Spartanburg, South Carolina |
| **Duration** | 11 months continuous |
| **Shifts** | 10-hour shifts, Monday-Friday |
| **Parts Moved** | 90,000+ sheet metal components |
| **Vehicles Produced** | 30,000+ BMW X3 |
| **Runtime** | 1,250+ hours |
| **Steps Taken** | 1.2+ million |
| **Task** | Sheet metal loading (pick-and-place) |
| **Accuracy** | 5mm tolerance placement |
| **Cycle Time** | 84 seconds total, 37 seconds load |
| **KPI Success** | Target: 99% accuracy, 0 interventions per shift |

**Key Learning:** Transition from lab to production was FASTER than expected. Motion sequences transferred quickly into stable shift operation. Integration via standardized interfaces into BMW Smart Robotics ecosystem.

**Figure 03:** Released Nov 2025. Redesigned wrist electronics (direct motor controller communication), improved forearm reliability (top failure point at BMW).

---

### Agility Digit at Amazon + GXO (First Commercial Humanoid)

| Spec | Value |
|------|-------|
| **Price** | Target <$50,000 |
| **Height** | 175 cm |
| **Weight** | 65 kg |
| **Payload** | 16 kg per hand |
| **Walk Speed** | 5.1 km/h |
| **Battery** | ~2-3 hours |
| **DOF** | 28 |
| **Manufacturing** | RoboFab (Salem, OR) - 10,000/year capacity |

**Deployments:**
- **Amazon**: Testing tote recycling at R&D center near Seattle (2023)
- **GXO/Spanx**: First commercial humanoid deployment in production (2024)
  - Tote-moving tasks in warehouse
  - "First humanoid deployed at a customer site, generating revenue"

---

### Apptronik Apollo (NASA Heritage)

| Spec | Value |
|------|-------|
| **Height** | 173 cm (5'8") |
| **Weight** | 72.6 kg |
| **Payload** | 25 kg |
| **Battery** | 4 hours hot-swappable |
| **DOF** | 44 |
| **Config** | Stationary / wheeled / bipedal (modular) |
| **Max Speed** | 1.2-1.5 m/s walking |
| **Actuators** | Proprietary linear electric (13+ generations) |
| **Heritage** | NASA Valkyrie robot project |

**Partnerships:**
- **Jabil**: Scaling production + manufacturing deployment (Feb 2025)
- **NASA**: Valkyrie humanoid project heritage
- Designed for logistics, manufacturing, human-safe collaboration

---

### Chinese Humanoid Robots

#### UBTech Walker X
- **Price**: Not publicly disclosed (est. $50,000+)
- **DOF**: 41 (record for service robots)
- **Height**: 145 cm
- **Battery**: 2 hours (major limitation)
- **Speed**: 3 km/h
- **Deployment**: Shopping centers, hotels, public spaces in China/Southeast Asia
- **Features**: Smart home integration (Xiaomi, Huawei, Google Home)
- **Limitation**: Proprietary SDK, closed ecosystem, limited European support

#### Fourier Intelligence GR-1
- **Price**: ~$125,000
- **Height**: 165 cm
- **Weight**: 55 kg
- **DOF**: 40
- **Max Speed**: 5 km/h walk, 3 km/h normal
- **Payload**: 50 kg (very strong for its class)
- **Market**: Healthcare, rehabilitation, research
- **Status**: Production version launched Oct 2024
- **Country**: China

#### Xiaomi CyberOne
- **Price**: $89,000-$104,000 (not commercially available)
- **Height**: 177 cm
- **Weight**: 52 kg
- **DOF**: 21
- **Speed**: 3.6 km/h walking, 7.2 km/h running
- **Payload**: 1.5 kg per hand (weak)
- **Special**: Emotion recognition (45 classes), 85 sound types
- **Features**: Curved OLED face, Mi-Sense depth vision
- **Status**: R&D platform only, no mass production timeline

#### Other Notable Chinese Humanoids
| Robot | Price | Key Feature |
|-------|-------|-------------|
| AGIBOT A2 Ultra | $100,000-$190,000 | Available now |
| Unitree R1 | $4,900 | Pre-order (ships April 2026) |
| Noetix Bumi | $1,400 | Hobbyist/entry level |
| NEURA 4NE1 | EUR 19,999-98,000 | Porsche collaboration |
| EngineAI T800 | $25,000 | Available now |

### Price History: Humanoid Robot Cost Drop

```
$2.5M  Honda ASIMO (2000)
$1M+   Boston Dynamics Atlas (2013)
$25K    SoftBank Pepper (2015)
$90K    Unitree H1 (2024)
$16K    Unitree G1 (2024)
$4.9K   Unitree R1 (2025)

99.4% price drop in 25 years
Projected $5K by 2030
```

---

## 5. LAYER 0 PROTOCOLS

The foundational communication protocols that enable robots to operate, communicate, and integrate with AI agents.

### ROS2 (Robot Operating System 2) - The De Facto Standard

| Attribute | Value |
|-----------|-------|
| **Type** | Open-source robotics middleware |
| **License** | Apache 2.0 |
| **Current LTS** | Jazzy Jalisco (May 2024 - May 2029) |
| **Previous LTS** | Humble Hawksbill (May 2022 - May 2027) |
| **Latest** | Lyrical Luth (May 2026 - May 2031) |
| **Underlying** | DDS (Data Distribution Service) |
| **Languages** | Python, C++ |
| **Stars** | The core is used by 10,000+ repos |

**ROS2 Distributions (2026):**

| Distro | Release | Type | EOL | Ubuntu | Python |
|--------|---------|------|-----|--------|--------|
| Humble | May 2022 | LTS | May 2027 | 22.04 | 3.10 |
| Jazzy | May 2024 | LTS | May 2029 | 24.04 | 3.12 |
| Kilted | May 2025 | Standard | Dec 2026 | 24.04 | 3.12 |
| Lyrical | May 2026 | LTS | May 2031 | 26.04 | 3.13 |

**Key ROS2 Components for AI Agents:**
```
Nodes: Independent computation units (AI models, sensors, actuators)
Topics: Pub/sub message channels (sensor data, commands)
Services: Request/response RPC
Actions: Long-running tasks with feedback
Nav2: Navigation stack (SLAM, path planning, obstacle avoidance)
MoveIt 2: Motion planning for manipulators
ros2_control: Hardware abstraction layer
```

**Python Example:**
```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class AIAgentNode(Node):
    def __init__(self):
        super().__init__('ai_agent')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.timer = self.create_timer(0.1, self.control_loop)
    
    def image_callback(self, msg):
        # AI agent processes image
        pass
    
    def control_loop(self):
        cmd = Twist()
        cmd.linear.x = 0.5  # Move forward
        self.publisher_.publish(cmd)

rclpy.init()
node = AIAgentNode()
rclpy.spin(node)
```

---

### DDS (Data Distribution Service) - Real-Time Pub/Sub

| Attribute | Value |
|-----------|-------|
| **Standard** | OMG (Object Management Group) |
| **Protocol** | RTPS (Real-Time Publish-Subscribe) over UDP/IP |
| **Implementations** | CycloneDDS, FastDDS (eProsima), RTI Connext, OpenDDS |
| **Key Feature** | Decentralized discovery, no broker needed |
| **QoS** | Configurable: reliability, durability, deadline, lifespan |
| **Use Case** | Real-time robot-to-robot communication |

**ROS2 DDS Implementations:**
- **FastDDS** (default in Humble/Jazzy)
- **CycloneDDS** (used by Unitree, Eclipse foundation)
- **RTI Connext** (commercial, high-performance)
- **Zenoh** (emerging alternative, Tier 1 in Kilted+)

**Unitree SDK2 is built directly on CycloneDDS** - communicates without ROS2 running, but is ROS2-compatible via DDS interop.

---

### MQTT (Message Queuing Telemetry Transport) - IoT Messaging

| Attribute | Value |
|-----------|-------|
| **Type** | Lightweight pub/sub messaging |
| **Transport** | TCP/IP |
| **Overhead** | Minimal (2-byte fixed header) |
| **Pattern** | Client-Broker (centralized) |
| **QoS Levels** | 0 (at most once), 1 (at least once), 2 (exactly once) |
| **Best For** | Low-power sensors, cloud connectivity, fleet management |

**MQTT for Robots:**
```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("mqtt.broker.com", 1883)

# Publish sensor data
client.publish("robot/go2/battery", "87%")
client.publish("robot/go2/position", "{x: 1.2, y: 3.4}")

# Subscribe to commands
client.subscribe("robot/go2/cmd")

def on_message(client, userdata, msg):
    if msg.topic == "robot/go2/cmd":
        execute_command(msg.payload)

client.on_message = on_message
client.loop_start()
```

**Use Cases:** Cloud fleet monitoring, over-the-air updates, telemetry, cross-facility coordination.

---

### AMQP (Advanced Message Queuing Protocol) - Enterprise Messaging

| Attribute | Value |
|-----------|-------|
| **Type** | Enterprise message queuing |
| **Pattern** | Exchange -> Queue -> Consumer |
| **Features** | Message persistence, transactions, complex routing |
| **Implementations** | RabbitMQ, Apache Qpid, Azure Service Bus |
| **Best For** | Backend systems, order processing, multi-robot task allocation |

**MQTT vs AMQP for Robotics:**
- **MQTT**: Use on robot (lightweight, embedded-friendly)
- **AMQP**: Use in backend (reliable, complex routing, persistence)
- **Together**: Robot publishes via MQTT -> Gateway converts to AMQP -> Backend processes

---

### OPC-UA (Open Platform Communications Unified Architecture) - Industrial Standard

| Attribute | Value |
|-----------|-------|
| **Type** | Industrial automation communication |
| **Standard** | IEC 62541 |
| **Foundation** | OPC Foundation (678+ members: Siemens, ABB, Rockwell, Microsoft) |
| **Architecture** | Client-Server + Pub/Sub |
| **Security** | Built-in encryption, certificates, authentication |
| **Data Modeling** | Semantic data models (companion specs for robots, CNC, etc.) |
| **Best For** | Factory automation, PLC integration, Industry 4.0 |

**OPC-UA for Robots:**
- Companion specification for robotics
- Direct PLC integration without custom gateways
- Semantic data model (not just raw values - knows what the data means)
- Publish/Subcribe over MQTT (PubSub over MQTT spec)
- Time-Sensitive Networking (TSN) support for real-time

---

### CAN bus (Controller Area Network) - Vehicle/Internal Network

| Attribute | Value |
|-----------|-------|
| **Type** | Multi-master serial bus |
| **Speed** | Up to 1 Mbps (CAN), 5-8 Mbps (CAN-FD) |
| **Max Nodes** | 128 (theoretical), typically < 32 |
| **Distance** | Up to 40m at 1 Mbps |
| **Topology** | Differential twisted pair |
| **Best For** | Motor controllers, sensors, embedded real-time control |

**CAN bus in Robotics:**
- Internal robot bus for motor drivers, IMU, encoders
- Used by Unitree Go2 (internal leg motor communication)
- Standard in automotive (Tesla, Nuro)
- Real-time with priority-based arbitration
- Every motor controller, sensor publishes on the bus

```
Motor Controller 1 <--->
Motor Controller 2 <---> CAN bus <---> Main Computer
Motor Controller 3 <--->
IMU Sensor     <--->
```

---

### EtherCAT - Real-Time Industrial Ethernet

| Attribute | Value |
|-----------|-------|
| **Type** | Real-time industrial Ethernet |
| **Speed** | 100 Mbps |
| **Cycle Time** | < 100 microseconds |
| **Topology** | Line/pass-through (each node forwards frame) |
| **Protocol** | Master-Slave |
| **Best For** | High-speed synchronized motion control, CNC, factory automation |

**EtherCAT for Robots:**
- Industrial robot arm control (KUKA, FANUC, Universal Robots)
- Synchronized multi-axis motion
- Used in Agility Digit, Figure 03 manufacturing
- Not typical for mobile robots (CAN bus preferred there)

---

### RTPS (Real-Time Publish-Subscribe) - DDS Wire Protocol

| Attribute | Value |
|-----------|-------|
| **Type** | Wire protocol for DDS |
| **Standard** | OMG DDSI-RTPS |
| **Transport** | UDP/IP (multicast for discovery) |
| **Key Feature** | Automatic discovery - no central broker |
| **QoS** | Configurable for each topic |
| **Use Case** | Robot-to-robot real-time data exchange |

**RTPS enables:**
- Automatic node discovery (robots find each other on the network)
- Decentralized communication (no single point of failure)
- Configurable QoS per topic (some need reliability, some need speed)

---

### gRPC - Robot-to-Cloud Communication

| Attribute | Value |
|-----------|-------|
| **Type** | High-performance RPC framework |
| **Transport** | HTTP/2 |
| **Serialization** | Protocol Buffers (binary, efficient) |
| **Patterns** | Unary, server streaming, client streaming, bidirectional |
| **Best For** | Robot-to-cloud API calls, multi-robot fleet management |

**gRPC for Robots:**
```protobuf
// Robot service definition
service RobotService {
  rpc GetStatus(RobotId) returns (RobotStatus);
  rpc StreamSensorData(RobotId) returns (stream SensorData);
  rpc SendCommand(Command) returns (CommandResult);
  rpc BidirectionalControl(stream Command) returns (stream State);
}
```

---

### Eclipse Zenoh - The Emerging Alternative

| Attribute | Value |
|-----------|-------|
| **Type** | Next-gen pub/sub/query protocol |
| **Features** | Pub/Sub + Queries + Storage |
| **Transport** | TCP, UDP, QUIC, WebSockets, Bluetooth, serial |
| **Best For** | Cloud-to-edge, multi-robot fleets, IoT integration |
| **Status** | Tier 1 middleware in ROS2 Kilted+ |

**Zenoh advantages:**
- Works over any transport (not just Ethernet)
- Internet-native (not just LAN like DDS)
- Less configuration than DDS
- No XML config files

---

### How AI Agents Interface with These Protocols

```
AI AGENT LAYER:
  LLM (Grok, GPT-4, Claude) --> Natural language commands
  VLA Models (Pi0, GR00T) --> Vision-to-action
  Planning (PDDL, LLM-based) --> Task decomposition

ROBOT MIDDLEWARE LAYER:
  ROS2 / DDS / Zenoh --> Node communication
  Nav2 --> Navigation, SLAM, path planning
  MoveIt 2 --> Arm motion planning
  ros2_control --> Hardware abstraction

HARDWARE PROTOCOL LAYER:
  CAN bus --> Motor control, encoders, IMU
  EtherCAT --> High-speed synchronized motion
  WiFi/Ethernet --> Video streaming, LiDAR data
  Bluetooth --> Low-bandwidth sensors

CLOUD/INTEGRATION LAYER:
  gRPC --> Robot-to-cloud API
  MQTT --> Fleet telemetry, OTA updates
  OPC-UA --> Factory PLC integration
  AMQP --> Backend task allocation
```

---

## 6. OPEN SOURCE ROBOTICS CODE

### Simulation

| Repository | Stars | License | Last Update | Description |
|------------|-------|---------|-------------|-------------|
| `isaac-sim/IsaacSim` | 3.5K | Apache 2.0 | June 2026 | NVIDIA Isaac Sim - GPU-accelerated robot simulation |
| `gazebosim/gz-sim` | 410 | Apache 2.0 | June 2026 | Gazebo - de facto standard robot simulator |
| `Unity-Technologies/Unity-Robotics-Hub` | 2.5K | Apache 2.0 | Nov 2024 | Unity Robotics tools |
| `google-deepmind/mujoco` | 9.5K+ | Apache 2.0 | Active | MuJoCo physics engine (acquired by Google) |

### SLAM & Navigation

| Repository | Stars | License | Last Update | Description |
|------------|-------|---------|-------------|-------------|
| `UZ-SLAMLab/ORB_SLAM3` | 6.5K | GPLv3 | Active | Visual, visual-inertial, multi-map SLAM |
| `TixiaoShan/LIO-SAM` | 4.5K | BSD | Active | Lidar-inertial odometry via smoothing/mapping |
| `HKUST-Aerial-Robotics/FAST_LIO` | 3.2K | BSD | Active | Fast LiDAR-inertial odometry |
| `PRBonn/kinematic-icp` | 200+ | MIT | Active | Kinematic ICP for SLAM |
| `ros-planning/navigation2` | 2.3K | Apache 2.0 | Active | Nav2 for ROS2 - navigation stack |

### Robot Learning

| Repository | Stars | License | Last Update | Description |
|------------|-------|---------|-------------|-------------|
| `huggingface/lerobot` | **24.1K** | Apache 2.0 | Active | End-to-end robot learning (imitation + RL + VLA) |
| `nvidia/IsaacLab` | 3.2K | BSD-3 | Active | NVIDIA Isaac Lab - RL for robotics |
| `roboterax/humanoid-gym` | 800+ | MIT | Active | RL for humanoid zero-shot sim2real |
| `jonyzhang2023/awesome-humanoid-learning` | 1.5K | - | Active | Curated humanoid learning resources |

### Computer Vision for Robots

| Repository | Stars | License | Last Update | Description |
|------------|-------|---------|-------------|-------------|
| `ultralytics/ultralytics` | 35K+ | AGPL 3.0 | Active | YOLOv8 - object detection for robots |
| `monkeyrom/3D_Object_Detection_and_Pose_Estimation_for_Automated_Bin-Picking_Application` | 100+ | - | Active | YOLOv5 + FAST/BRISK for bin picking |
| `Walid-khaled/YOLO-Object-Detection-for-Pick-and-Place-task-using-ROS-on-KUKA-iiwa` | 200+ | - | Active | YOLOv4 pick-and-place with ROS |

### Unitree / Quadruped Control

| Repository | Stars | License | Last Update | Description |
|------------|-------|---------|-------------|-------------|
| `unitreerobotics/unitree_sdk2` | 500+ | - | Active | Official C++ SDK for Go2/B2/H1 |
| `unitreerobotics/unitree_sdk2_python` | 400+ | - | Active | Python SDK wrapper |
| `unitreerobotics/unitree_ros2` | 300+ | - | Active | ROS2 support |
| `legion1581/go2_python_sdk` | 200+ | MIT | Active | Unofficial Python SDK (DDS) |
| `legion1581/go2_webrtc_connect` | 150+ | MIT | Active | WebRTC connection for Go2 |

### Humanoid Control

| Repository | Stars | License | Last Update | Description |
|------------|-------|---------|-------------|-------------|
| `roboterax/humanoid-gym` | 800+ | MIT | Active | RL training for humanoid sim2real |
| `RoboMasters/China-Open-2024` | Various | - | 2024 | RoboMaster humanoid competition |

### Key Open-Source Humanoid Projects

| Project | Type | Hardware | Cost |
|---------|------|----------|------|
| **SO-ARM100 (LeRobot)** | Robot arm | 3D-printed + servo motors | ~$200 |
| **Koch v1.1** | Robot arm | 3D-printed | ~$250 |
| **LeKiwi** | Mobile manipulator | 3D-printed + wheels | ~$350 |
| **OpenLoong** | Humanoid | 3D-printed biped | ~$1,000 |
| **Axon** | Humanoid | Raspberry Pi + ESP32 | ~$500 |
| **SMART Humanoid** | Full humanoid | Modular, research-grade | $5,000+ |

---

## 7. REAL WORLD EXPERIMENT IDEAS

### CSOAI Governance Experiments with Physical Robots

#### Experiment 1: "When a Delivery Robot Crosses from EU to UK Post-Brexit"

**Setup:**
- Deploy Starship robot on a route that crosses Northern Ireland / Republic of Ireland border
- Or simulate: same robot model operating in both jurisdictions

**Governance Questions:**
- Which safety regulations apply? EU Machinery Directive vs UK CA marking?
- GDPR applies in EU - what camera data can be collected in ROI vs NI?
- Liability: if robot causes accident at the border, which legal system applies?
- Insurance requirements differ - how does the robot "know" which rules apply?

**Technical Implementation:**
```python
# Robot carries a "jurisdiction registry"
class RobotGovernance:
    jurisdictions = {
        "EU": {"gdpr": True, "safety_std": "EN_ISO_12100", "speed_limit": 6},
        "UK": {"gdpr": False, "safety_std": "BS_EN_ISO_12100", "speed_limit": 4},
    }
    
    def on_gps_position_update(self, lat, lon):
        current_jurisdiction = self.get_jurisdiction(lat, lon)
        self.apply_rules(current_jurisdiction)
        self.log_compliance(current_jurisdiction)
```

---

#### Experiment 2: "Multi-Jurisdiction Humanoid Workplace Safety"

**Setup:**
- Same humanoid robot (Unitree H1 or similar) operating in:
  - USA (OSHA regulations)
  - Germany (DGUV/ISO standards)
  - China (GB standards)

**Governance Questions:**
- Safety zone distances differ by country - how to reconfigure?
- Emergency stop requirements vary
- Worker notification/consent requirements differ
- Documentation and audit trails have different requirements

**Technical Implementation:**
- Robot loads jurisdiction-specific safety module on boot
- AI agent monitors compliance and generates audit logs
- Dynamic reconfiguration based on GPS + facility database

---

#### Experiment 3: "Autonomous Vehicle Liability Attribution"

**Setup:**
- Delivery robot fleet with mixed autonomy levels
- Log every decision point where AI agent vs. human operator has control

**Governance Questions:**
- When robot is in AI mode: who is liable for accident?
- When human teleoperator intervenes: does liability shift?
- How to prove (in court) who was in control at moment of incident?
- What logging/evidence standards are required?

**Technical Implementation:**
- Blockchain-based decision logging (immutable)
- Real-time control mode recording
- Automatic incident report generation

---

#### Experiment 4: "Cross-Border Robot Data Governance"

**Setup:**
- Robot collects camera/LiDAR data in multiple countries
- Data processed in cloud (potentially different country)
- Training data used to improve models (potentially different country again)

**Governance Questions:**
- Camera data from German streets - can it be used to train models in US?
- GDPR "right to be forgotten" - how to remove a person from training data?
- Data residency requirements by country
- Cross-border AI model transfer restrictions

---

#### Experiment 5: "Robot Governance Compliance Automation"

**Setup:**
- AI agent continuously monitors robot operations against regulatory database
- Auto-generates compliance reports
- Flags potential violations before they occur

**Architecture:**
```
Robot Sensors --> AI Agent --> Regulatory Knowledge Graph
                                  |
                                  v
                           Compliance Monitor
                                  |
                    +-------------+-------------+
                    |             |             |
                    v             v             v
               Auto-report   Alert human   Reconfigure
               generation    operator      robot
```

---

## 8. QUICK REFERENCE MATRIX

### Robot Selection for AI Agent Integration

| Use Case | Robot | Price | SDK Quality | ROS2 | Availability |
|----------|-------|-------|-------------|------|--------------|
| **Education/Research** | Unitree Go2 EDU | $2,500 | Excellent | Full | Buy now |
| **Low-cost humanoid** | Unitree G1 | $16,000 | Excellent | Full | Buy now |
| **Industrial inspection** | Unitree B2 | $30K est. | Good | Full | Buy now |
| **Delivery (build on)** | Reference: Starship | N/A | N/A | N/A | Partner only |
| **Warehouse automation** | Agility Digit | <$50K | Good | Yes | Pilot program |
| **Factory integration** | Figure 03 | TBA | Good | Yes | Late 2026 |
| **Wait-and-see** | Tesla Optimus | $20-30K (target) | Unknown | Unknown | 2027+ |
| **Healthcare/service** | Fourier GR-1 | $125K | Limited | Partial | Early access |

### Protocol Selection Matrix

| Need | Protocol | When to Use |
|------|----------|-------------|
| Robot application development | **ROS2** | Always (de facto standard) |
| Real-time robot-to-robot comms | **DDS/RTPS** | Multi-robot systems |
| Motor control, embedded | **CAN bus** | Internal robot bus |
| Industrial PLC integration | **OPC-UA** | Factory automation |
| Cloud connectivity, telemetry | **MQTT** | Fleet management, IoT |
| Backend task allocation | **AMQP** | Enterprise multi-robot |
| High-speed motion control | **EtherCAT** | Industrial robot arms |
| Robot-to-cloud API | **gRPC** | Fleet management systems |
| Next-gen multi-robot | **Zenoh** | Cloud-to-edge, 2025+ |

---

## SOURCES & REFERENCES

### Key URLs

**Unitree:**
- https://github.com/unitreerobotics
- https://support.unitree.com/home/en/developer
- https://www.unitree.com

**Tesla Optimus:**
- https://www.tesla.com/optimus
- https://www.figure.ai
- https://blog.robozaps.com/b/tesla-optimus-gen-2-review

**Delivery Robots:**
- https://www.starship.xyz
- https://serverobotics.com
- https://www.nuro.ai
- https://www.cocodelivery.com

**Open Source:**
- https://github.com/huggingface/lerobot (24.1K stars)
- https://github.com/isaac-sim/IsaacSim (3.5K stars)
- https://github.com/UZ-SLAMLab/ORB_SLAM3 (6.5K stars)
- https://github.com/TixiaoShan/LIO-SAM (4.5K stars)

**Protocols:**
- https://docs.ros.org/en/jazzy/
- https://opcfoundation.org/about/what-is-opc/
- https://mqtt.org
- https://zenoh.io

---

*Report compiled: June 2026*
*For CSOAI governance experiment planning*
