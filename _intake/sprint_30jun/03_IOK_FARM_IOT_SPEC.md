# iOK Farm Pond IoT Spec — the physical beacon for Lincolnshire

**Goal:** ESP32 + sensors on the 13m koi pond → real-time data → CesiumJS gold beacon on the globe.

## Hardware

### ESP32-S3 DevKit
- Wi-Fi + Bluetooth 5 (LE)
- Dual-core Xtensa LX7 @ 240 MHz
- 8 MB PSRAM, 16 MB flash
- USB-C, battery charging
- ~£15 per unit

### Sensors
- **pH probe** (Atlas Scientific EZO-pH): I2C, ±0.1 accuracy, range 0-14
- **Dissolved oxygen** (Atlas Scientific EZO-DO): I2C, ±0.1 mg/L
- **Temperature** (DS18B20): 1-Wire, ±0.5°C, range -55 to 125°C
- **Water level** (HC-SR04 ultrasonic): GPIO trigger/echo, ±1 cm
- **ORP** (Atlas Scientific EZO-ORP): I2C, optional

### Actuators
- **Pumps** (4 bead filter pumps + 2 Evolution Aqua UVs): 240V via Sonoff S31 smart plug
- **Auto-feeder** (3D-printed koi feeder, Qidi Max4): servo-driven, runs 2x daily
- **Aerator** (Hailea V-20): 240V via Sonoff
- **Water-change solenoid**: 12V via relay

## Software

### Firmware (ESP32)
- Arduino framework + PubSubClient (MQTT)
- Reads sensors every 60 sec
- Publishes JSON to MQTT broker:
  ```json
  {
    "device": "sovereign-pond-01",
    "ts": "2026-06-27T14:00:00Z",
    "ph": 7.4,
    "do_mgL": 8.2,
    "temp_c": 22.1,
    "level_cm": 89,
    "care_floor": "ok"
  }
  ```
- Subscribes to `sovereign/cmd/{device}/actuate` for pump control
- Ed25519 signs every payload locally (uses sovereign key on SD card)

### MQTT broker
- `mqtts://iot.meok.ai:8883` (Mosquitto 2.x with TLS 1.3)
- Client certificates issued by sovereign CA
- Topic ACL: devices can publish to `sovereign/farm/{device_id}`, subscribe to `sovereign/cmd/{device_id}/#`
- Retention: 30 days for sensor data, 1 year for actuation events

### Backend (meok-sovereign-iot-mcp)
- Bridges MQTT → MCP server
- 5 tools: `sov_iot_status`, `sov_iot_history`, `sov_iot_actuate`, `sov_iot_emergency_stop`, `sov_iot_subscribe`
- Every actuation REQUIRES BFT council approval (delegation through `sov_council` MCP)
- Care-floor: if water quality drops below threshold, auto-actuate emergency water change

### CesiumJS integration
- `sovereign-mom` hive on the globe gets a pulsing gold beacon
- Beacon intensity scales with pond health (care_floor = "ok" = steady pulse, "warning" = fast pulse, "critical" = red shockwave)
- Real-time data overlay: 9 koi sprite count near the beacon
- Drone feed: optional (Phase 2)

## Cost
- ESP32 + sensors: £100 per unit
- 5 ponds × £100 = £500
- MQTT broker: £10/mo cloud VM
- ESPHome / Tasmota firmware: free
- 1 day of integration work

## Timeline
- Week 1: Order hardware, test 1 ESP32 on bench
- Week 2: Deploy to actual pond
- Week 3: Wire to MCP + CesiumJS
- Week 4: First live demo for the bleed-edge launch (Jul 4)

## Free cloud credit allocation
- NVIDIA Inception $50K → NOT for IoT (use for sovereign model training)
- DO Hatch $10K → USE for MQTT broker + iOK Farm IoT dashboards
- MS Founders $150K → USE for Microsoft Azure IoT Hub if needed
- Total: $10-15K for full IoT stack over 12 months
