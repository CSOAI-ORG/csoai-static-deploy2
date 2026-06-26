# QIDI Plus 4 Max - Moonraker Connection Guide
## Complete Setup & Troubleshooting for macOS (Nick's Network: 192.168.50.x)

---

## Table of Contents

1. [Quick Start Checklist](#1-quick-start-checklist)
2. [Finding the Printer's IP Address](#2-finding-the-printers-ip-address)
3. [WiFi Network Setup](#3-wifi-network-setup)
4. [Checking if Moonraker is Running](#4-checking-if-moonraker-is-running)
5. [Opening Port 7125](#5-opening-port-7125)
6. [SSH Access to the Printer](#6-ssh-access-to-the-printer)
7. [USB Connection (Fallback)](#7-usb-connection-fallback)
8. [mDNS Auto-Discovery Setup](#8-mdns-auto-discovery-setup)
9. [Running the Python Client](#9-running-the-python-client)
10. [Setting Up the MCP Server](#10-setting-up-the-mcp-server)
11. [Calibration Guide](#11-calibration-guide)
12. [Common Issues & Solutions](#12-common-issues--solutions)
13. [Moonraker API Reference](#13-moonraker-api-reference)
14. [Useful G-Codes for QIDI Plus 4 Max](#14-useful-g-codes-for-qidi-plus-4-max)

---

## 1. Quick Start Checklist

Before diving into detailed troubleshooting, run through this checklist:

- [ ] Printer is powered on and booted (touchscreen shows main menu)
- [ ] Printer is connected to your WiFi network (same as your Mac)
- [ ] You know the printer's IP address
- [ ] Your Mac can ping the printer's IP
- [ ] Moonraker service is running on the printer
- [ ] Port 7125 is not blocked by a firewall

**If all checks pass, run:**
```bash
python moonraker_client.py --ip YOUR_PRINTER_IP status
```

---

## 2. Finding the Printer's IP Address

### Method 1: From the Touchscreen (Easiest)

1. On the QIDI Plus 4 Max touchscreen, tap **Settings** (gear icon)
2. Go to **Network** or **WiFi Settings**
3. Look for **IP Address** - it will show something like `192.168.50.xxx`
4. Write this down - this is your `MOONRAKER_IP`

> QIDI printers often show the IP on the main screen or in a network info widget. Look for a small WiFi icon with numbers.

### Method 2: From Your Router Admin Panel

1. Open a browser on your Mac
2. Navigate to your router's admin page (usually `http://192.168.50.1` or `http://192.168.1.1`)
3. Log in (check router sticker for credentials)
4. Go to **Connected Devices** or **DHCP Client List**
5. Look for a device named:
   - `QIDI`
   - `qidi-plus4`
   - `klipper`
   - Or a MAC address starting with the printer's vendor prefix
6. Note the IP address

### Method 3: Using `arp-scan` on macOS

Install and run arp-scan to find devices on your network:

```bash
# Install arp-scan (if not already installed)
brew install arp-scan

# Scan the network (replace en0 with your active interface)
sudo arp-scan --localnet --interface=en0

# Or scan specific range
sudo arp-scan 192.168.50.1-192.168.50.254
```

Look for entries with vendor names like `Qidi`, `Raspberry Pi`, or similar.

### Method 4: Using Python Client's Discovery

```bash
# Auto-scan the network
python moonraker_client.py discover --subnet 192.168.50
```

This scans all IPs from .1 to .254 on port 7125 and reports any Moonraker instances found.

**To scan multiple subnets:**
```bash
python moonraker_client.py discover --subnet 192.168.1
python moonraker_client.py discover --subnet 10.0.0
```

---

## 3. WiFi Network Setup

### If the Printer is NOT on WiFi Yet

The QIDI Plus 4 Max needs to be connected to your 2.4GHz WiFi network (most 3D printers don't support 5GHz).

#### Option A: Via Touchscreen

1. On the printer touchscreen, go to **Settings > WiFi**
2. Select your network name (SSID)
3. Enter your WiFi password
4. Wait for it to connect - you should see an IP address appear

#### Option B: Via USB Connection (if touchscreen method fails)

1. Connect your Mac to the printer via USB-C cable
2. The printer should appear as a serial device
3. Use a terminal program (like `screen` or `minicom`) to connect:

```bash
# Find the serial device
ls /dev/tty.*
# Look for something like /dev/tty.usbserial-XXXX or /dev/ttyACM0

# Connect (replace with your device)
screen /dev/tty.usbserial-XXXX 115200
```

4. Once connected, you can use the Klipper console to configure WiFi:

```
# For printers with network manager
WIFI_CONNECT SSID="YourNetworkName" PASSWORD="YourPassword"
```

#### Option C: Edit Configuration Directly (Advanced)

If you have SSH access (see Section 6):

```bash
ssh root@PRINTER_IP
# Edit the WiFi config (location varies, common paths):
nano /etc/wpa_supplicant.conf
# or
nano /etc/network/interfaces
# Restart networking
systemctl restart networking
```

### Ensuring Same Network/Subnet

Your Mac and the printer MUST be on the same network subnet to communicate.

**Check your Mac's IP:**
```bash
ipconfig getifaddr en0
# Output example: 192.168.50.100
```

The first three octets must match the printer's IP (e.g., both start with `192.168.50`).

**If they're on different subnets**, either:
1. Move the printer to the same WiFi network as your Mac
2. Or configure your router to allow inter-subnet communication

---

## 4. Checking if Moonraker is Running

Once you have the printer's IP, test if Moonraker is accessible:

### From Your Mac (Terminal)

```bash
# Test basic connectivity
ping 192.168.50.xxx

# Test if port 7125 is open
nc -zv 192.168.50.xxx 7125
# or
telnet 192.168.50.xxx 7125
```

### Test Moonraker API Directly

```bash
# Get server info
curl http://192.168.50.xxx:7125/server/info

# Get printer status
curl 'http://192.168.50.xxx:7125/printer/objects/query?objects=toolhead&objects=extruder'

# List files
curl http://192.168.50.xxx:7125/server/files/list?root=gcodes
```

**Expected response** (server info):
```json
{
  "result": {
    "version": "v0.8.0",
    "klippy_connected": true,
    "components": ["database", "file_manager", "klippy_apis", "machine"]
  }
}
```

### If Moonraker is NOT Responding

#### Check from the Printer (via SSH)

```bash
ssh root@192.168.50.xxx

# Check if Moonraker service is running
systemctl status moonraker

# If not running, start it
systemctl start moonraker

# Enable auto-start
systemctl enable moonraker

# Check Moonraker logs
journalctl -u moonraker -f
# or
tail -f /tmp/moonraker.log
```

#### Restart Moonraker Manually

```bash
ssh root@192.168.50.xxx

# Restart the service
systemctl restart moonraker

# Or kill and restart manually
pkill -f moonraker
moonraker -c /etc/moonraker.conf
```

---

## 5. Opening Port 7125

### Check if the Port is Open

From your Mac:
```bash
# Check if port 7125 is reachable
nmap -p 7125 192.168.50.xxx

# Or use netcat
nc -zv 192.168.50.xxx 7125
```

### If the Port is Blocked

#### A. Check Printer Firewall (via SSH)

```bash
ssh root@192.168.50.xxx

# Check if firewall is active
iptables -L -n | grep 7125

# If blocked, add a rule to allow port 7125
iptables -A INPUT -p tcp --dport 7125 -j ACCEPT

# Save rules (method varies by Linux distro)
iptables-save > /etc/iptables/rules.v4
```

#### B. Check moonraker.conf

```bash
ssh root@192.168.50.xxx
cat /etc/moonraker.conf
```

Look for the `[server]` section:
```ini
[server]
host: 0.0.0.0
port: 7125
# Make sure host is 0.0.0.0 (accept all) not 127.0.0.1 (localhost only)
```

If `host` is set to `127.0.0.1`, change it to `0.0.0.0`:
```bash
nano /etc/moonraker.conf
# Change: host: 0.0.0.0
systemctl restart moonraker
```

#### C. Check Router Firewall

Some routers have client isolation that blocks devices from talking to each other.

1. Log into your router admin (`http://192.168.50.1`)
2. Look for settings like:
   - "AP Isolation" - **DISABLE this**
   - "Client Isolation" - **DISABLE this**
   - "Guest Network Isolation" - Don't connect printer to guest network

#### D. macOS Firewall

Your Mac's firewall usually doesn't block outbound connections, but check:

```bash
# Check firewall status
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# If needed, temporarily disable
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
# Re-enable after testing
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
```

---

## 6. SSH Access to the Printer

Most QIDI Plus 4 Max printers run a Linux-based SBC (Single Board Computer) like a Raspberry Pi or similar. SSH gives you full control.

### Default SSH Credentials (QIDI)

| Field | Value |
|-------|-------|
| Username | `root` or `qidi` |
| Password | `root` or `qidi` or `klipper` |
| Port | 22 |

### Connecting via SSH

```bash
# Try these combinations
ssh root@192.168.50.xxx
# Password: root

ssh qidi@192.168.50.xxx
# Password: qidi

# If those don't work, try common defaults
ssh root@192.168.50.xxx
# Password: klipper
# Password: 123456
# Password: (empty - just press Enter)
```

### Finding the Correct Credentials

If defaults don't work:
1. Check QIDI documentation/manual
2. Check QIDI's official website/support
3. Try the touchscreen - some printers show SSH info in Settings > About
4. Check online forums for QIDI Plus 4 Max SSH credentials

### Useful SSH Commands Once Connected

```bash
# Check system info
uname -a
cat /etc/os-release

# Check running services
systemctl list-units --type=service

# Check Moonraker specifically
systemctl status moonraker
journalctl -u moonraker --no-pager -n 50

# Check Klipper
systemctl status klipper

# View printer configuration
cat ~/printer_data/config/printer.cfg

# Restart services
systemctl restart moonraker
systemctl restart klipper

# Check disk space
df -h

# Check network
ip addr show
ifconfig
```

---

## 7. USB Connection (Fallback)

If WiFi/network connection fails entirely, use USB as a fallback.

### macOS USB Connection

1. Connect the QIDI Plus 4 Max to your Mac via USB cable
2. Open Terminal and find the device:

```bash
# List serial devices
ls /dev/tty.*
ls /dev/cu.*

# Common names:
# /dev/tty.usbserial-XXXX
# /dev/tty.usbmodemXXXX
# /dev/cu.usbserial-XXXX
# /dev/cu.wchusbserialXXXX
```

3. Use `screen` to connect:
```bash
screen /dev/tty.usbserial-XXXX 115200
```

4. Press Enter - you should see a Klipper console prompt

### Using the Client with USB (Serial Bridge)

Some setups expose Moonraker over a USB serial bridge. If so, the API might be available at a different endpoint. Check if your QIDI printer supports this.

### Alternative: USB-to-Ethernet

If the printer has an Ethernet port (check the back):
1. Connect an Ethernet cable directly from printer to Mac (or via router)
2. The printer may get an IP via DHCP
3. Check the IP on the touchscreen or router

---

## 8. mDNS Auto-Discovery Setup

mDNS (Bonjour/Avahi) lets your printer auto-discover on the network without knowing its IP.

### Enable mDNS on the Printer (via SSH)

```bash
ssh root@192.168.50.xxx

# Install avahi (if not present)
apt-get update && apt-get install -y avahi-daemon

# Create mDNS service file for Moonraker
cat > /etc/avahi/services/moonraker.service << 'EOF'
<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">%h Moonraker</name>
  <service>
    <type>_http._tcp</type>
    <port>7125</port>
    <txt-record>path=/</txt-record>
  </service>
</service-group>
EOF

# Restart avahi
systemctl restart avahi-daemon
systemctl enable avahi-daemon
```

### Discover from macOS

```bash
# Browse for Moonraker services
dns-sd -B _http._tcp

# Or use the Python client with mDNS
python -c "
import socket
try:
    result = socket.getaddrinfo('qidi-plus4.local', 7125)
    print('Found:', result[0][4][0])
except:
    print('mDNS name not found')
"
```

### Using .local Hostname

After setting up mDNS, you can connect using:
```bash
python moonraker_client.py --ip qidi-plus4.local status
```

---

## 9. Running the Python Client

### Installation

```bash
# The client uses only Python standard library - no pip install needed!
# Just download and run
chmod +x moonraker_client.py
```

### Basic Commands

```bash
# 1. Discover printer on network
python moonraker_client.py discover --subnet 192.168.50

# 2. Check status
python moonraker_client.py --ip 192.168.50.xxx status

# 3. Check temperatures
python moonraker_client.py --ip 192.168.50.xxx temps

# 4. List files
python moonraker_client.py --ip 192.168.50.xxx list

# 5. Upload a file
python moonraker_client.py --ip 192.168.50.xxx upload ~/Downloads/benchy.gcode

# 6. Start a print
python moonraker_client.py --ip 192.168.50.xxx print benchy.gcode

# 7. Monitor print progress
python moonraker_client.py --ip 192.168.50.xxx monitor

# 8. Pause/Resume/Cancel
python moonraker_client.py --ip 192.168.50.xxx pause
python moonraker_client.py --ip 192.168.50.xxx resume
python moonraker_client.py --ip 192.168.50.xxx cancel
```

### Save IP for Convenience

After discovery, the client saves the IP automatically. Then you can omit `--ip`:

```bash
python moonraker_client.py status
python moonraker_client.py temps
```

---

## 10. Setting Up the MCP Server

### Prerequisites

```bash
# Install the MCP Python SDK
pip install mcp
```

### Configure for Claude Code

Edit your Claude Code settings file:

```bash
# Location on macOS
mkdir -p ~/Library/Application\ Support/Claude
nano ~/Library/Application\ Support/Claude/settings.json
```

Add the Moonraker MCP server:

```json
{
  "mcpServers": {
    "moonraker": {
      "command": "python3",
      "args": ["/path/to/moonraker_mcp_server.py"],
      "env": {
        "MOONRAKER_IP": "192.168.50.xxx",
        "MOONRAKER_PORT": "7125"
      }
    }
  }
}
```

**Replace** `/path/to/moonraker_mcp_server.py` with the actual path and `192.168.50.xxx` with your printer's IP.

### Start the MCP Server Manually (for testing)

```bash
export MOONRAKER_IP=192.168.50.xxx
python3 moonraker_mcp_server.py
```

### Using with Claude Code

Once configured, you can ask Claude things like:

- "What's the current temperature of my printer?"
- "Start printing the calibration cube file"
- "Pause the current print"
- "Home all axes"
- "Run PID tune on the extruder at 210 degrees"
- "List all G-code files on the printer"
- "Upload this file and start printing it"

### MCP Tools Available

| Tool | Description |
|------|-------------|
| `printer_status` | Full printer status (position, temps, state, extruder) |
| `query_temperatures` | Just temperature readings |
| `start_print` | Start a print job (specify filename) |
| `pause_print` | Pause current print |
| `resume_print` | Resume paused print |
| `cancel_print` | Cancel/abort print |
| `home_axes` | Home X/Y/Z axes |
| `run_gcode` | Execute any G-code command |
| `upload_file` | Upload G-code from your Mac |
| `list_files` | List files on printer |
| `emergency_stop` | Emergency stop (M112) |
| `firmware_restart` | Restart Klipper firmware |
| `pid_tune` | PID autotune for a heater |
| `calibrate_bed_mesh` | Bed mesh calibration |
| `set_temperature` | Set heater target temperature |
| `get_active_extruder` | Get current active extruder |
| `set_active_extruder` | Switch extruder (dual head) |

---

## 11. Calibration Guide

### Full First-Time Setup

```bash
# Run the automated setup (this takes ~30-40 minutes)
python moonraker_client.py --ip 192.168.50.xxx setup
```

This runs:
1. Connection test
2. XYZ homing
3. PID tune extruder 0 (200C)
4. PID tune extruder 1 (200C) - if dual extruder
5. PID tune bed (60C)
6. Bed mesh calibration
7. Pressure advance calibration

### Individual Calibration Steps

#### PID Tune (Hotend)

```bash
# Tune extruder at 200C (PLA)
python moonraker_client.py --ip 192.168.50.xxx pid --heater extruder --target 200

# Tune extruder at 250C (ABS/ASA)
python moonraker_client.py --ip 192.168.50.xxx pid --heater extruder --target 250

# Tune bed at 60C
python moonraker_client.py --ip 192.168.50.xxx pid --heater heater_bed --target 60
```

**Important:** After PID tune completes, you MUST save config:
```bash
python moonraker_client.py --ip 192.168.50.xxx gcode --script "SAVE_CONFIG"
```

#### Bed Mesh Calibration

```bash
# Heat bed first (to print temperature)
python moonraker_client.py --ip 192.168.50.xxx gcode --script "M140 S60"

# Wait for bed to reach temp (check with temps command)
python moonraker_client.py --ip 192.168.50.xxx temps

# Run bed mesh
python moonraker_client.py --ip 192.168.50.xxx bedmesh --profile default

# Save the mesh
python moonraker_client.py --ip 192.168.50.xxx gcode --script "BED_MESH_PROFILE SAVE=default"
python moonraker_client.py --ip 192.168.50.xxx gcode --script "SAVE_CONFIG"
```

#### Pressure Advance

```bash
# Run pressure advance calibration
python moonraker_client.py --ip 192.168.50.xxx pressure-advance --extruder extruder
```

If the macro isn't found, print a PA calibration tower and manually find the best PA value, then set it in your slicer or printer.cfg.

---

## 12. Common Issues & Solutions

### Issue: "Connection refused" or "No route to host"

**Causes & Fixes:**
1. **Wrong IP** - Double-check the IP on the touchscreen
2. **Different subnet** - Mac and printer must share first 3 octets
3. **Printer not on WiFi** - Connect via touchscreen first
4. **Firewall blocking** - Check router and Mac firewall settings
5. **Moonraker not running** - SSH in and `systemctl start moonraker`

### Issue: "Moonraker found but Klipper not connected"

```bash
# Check Klipper status
ssh root@192.168.50.xxx systemctl status klipper

# Restart Klipper
ssh root@192.168.50.xxx systemctl restart klipper

# Check for config errors
ssh root@192.168.50.xxx journalctl -u klipper -n 20
```

### Issue: Upload fails / times out

1. Check disk space: `ssh root@192.168.50.xxx df -h`
2. Check file permissions
3. Try smaller file first
4. Increase timeout in the client code

### Issue: Print won't start

1. Check if printer is homed: `python moonraker_client.py status`
2. Home axes first: `python moonraker_client.py home`
3. Check if file exists: `python moonraker_client.py list`
4. Check bed mesh is loaded

### Issue: Temperatures read 0C

1. Check thermistor connections inside printer
2. Check printer.cfg has correct thermistor pins
3. Restart Klipper after config changes

### Issue: Dual extruder not working

```bash
# Check which extruder is active
python moonraker_client.py --ip 192.168.50.xxx toolhead

# Switch to extruder 1
python moonraker_client.py --ip 192.168.50.xxx extruder --set extruder1

# Check extruder config in printer.cfg via SSH
ssh root@192.168.50.xxx cat ~/printer_data/config/printer.cfg | grep -A5 "extruder1"
```

---

## 13. Moonraker API Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/server/info` | GET | Server version, components, Klipper connection state |
| `/printer/objects/query` | GET | Query any printer object (toolhead, temps, etc.) |
| `/printer/print/start` | POST | Start printing a file |
| `/printer/print/pause` | POST | Pause current print |
| `/printer/print/resume` | POST | Resume paused print |
| `/printer/print/cancel` | POST | Cancel current print |
| `/printer/gcode/script` | POST | Execute G-code |
| `/printer/firmware_restart` | POST | Restart Klipper firmware |
| `/server/files/upload` | POST | Upload a file |
| `/server/files/list` | GET | List files in a directory |
| `/server/files/delete` | DELETE | Delete a file |
| `/machine/reboot` | POST | Reboot the host system |

### Query Objects

Common objects to query via `/printer/objects/query?objects=NAME`:

| Object | Data Provided |
|--------|--------------|
| `toolhead` | Position, active extruder, homed axes |
| `extruder` | Temperature, pressure advance, target |
| `extruder1` | Second extruder data |
| `heater_bed` | Bed temperature, target |
| `print_stats` | Print state, filename, progress, duration |
| `virtual_sdcard` | SD card/virtual file progress |
| `gcode_move` | Current position, speed, extrude factor |
| `fan` | Fan speed |
| `display_status` | Display/progress info |

---

## 14. Useful G-Codes for QIDI Plus 4 Max

### Temperature Control
```
M104 S200          ; Set hotend temp (no wait)
M109 S200          ; Set hotend temp and wait
M140 S60           ; Set bed temp (no wait)
M190 S60           ; Set bed temp and wait
M140 S0 / M104 S0  ; Turn off heaters
```

### Movement
```
G28                ; Home all axes
G28 X              ; Home X only
G1 X10 Y10 F3000   ; Move to position at speed
G1 Z5              ; Move Z axis
G91                ; Relative positioning
G90                ; Absolute positioning
```

### Extrusion
```
M83                ; Relative extrusion mode
G1 E10 F300        ; Extrude 10mm
G1 E-5 F300        ; Retract 5mm
G1 E-40 F1800      ; Full filament retract (for change)
```

### Calibration
```
PID_CALIBRATE HEATER=extruder TARGET=200   ; PID tune
BED_MESH_CALIBRATE                         ; Bed mesh
BED_MESH_PROFILE SAVE=default              ; Save mesh
SAVE_CONFIG                                ; Save all settings
```

### Information
```
M115               ; Firmware info
M503               ; Current settings
M105               ; Temperature report
```

---

## Need More Help?

- **Klipper docs**: https://www.klipper3d.org/
- **Moonraker docs**: https://moonraker.readthedocs.io/
- **QIDI support**: Check QIDI's official support channels
- **Reddit**: r/klippers, r/3Dprinting
- **Discord**: Klipper Discord server
