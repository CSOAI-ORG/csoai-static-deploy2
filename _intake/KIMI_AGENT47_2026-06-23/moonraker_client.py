#!/usr/bin/env python3
"""
Moonraker API Client for QIDI Plus 4 Max (Klipper firmware)
============================================================
Complete Python client for discovering and controlling a Klipper/Moonraker 3D printer.

Features:
  - Automatic network discovery (scans common subnets for port 7125)
  - Full printer status query (temps, position, print state, toolhead)
  - G-code file upload, download, and management
  - Print control (start, pause, resume, cancel)
  - Calibration routines (PID tune, pressure advance, bed mesh)
  - Multi-toolhead/extruder support
  - Custom G-code execution
  - Simple CLI interface

Usage:
  python moonraker_client.py discover
  python moonraker_client.py status
  python moonraker_client.py upload mymodel.gcode
  python moonraker_client.py print mymodel.gcode
  python moonraker_client.py temps
  python moonraker_client.py home
  python moonraker_client.py bedmesh
  python moonraker_client.py pid-tune extruder 210
  python moonraker_client.py monitor
"""

import argparse
import json
import os
import socket
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_PORT = 7125
DEFAULT_SUBNET = "192.168.50"
TIMEOUT = 5
CONFIG_FILE = Path.home() / ".config" / "moonraker_client.json"


# ============================================================================
# UTILITY / HELPERS
# ============================================================================

def _http_request(
    url: str,
    method: str = "GET",
    data: Optional[bytes] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = TIMEOUT,
) -> Tuple[bool, Any]:
    """Execute an HTTP request and return (success, response_json or error)."""
    req = urllib.request.Request(url, method=method, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            try:
                return True, json.loads(body)
            except json.JSONDecodeError:
                return True, body
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        return False, f"HTTP {e.code}: {err_body}"
    except Exception as e:
        return False, str(e)


def save_config(printer_ip: str, port: int = DEFAULT_PORT) -> None:
    """Persist printer address to disk."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps({"ip": printer_ip, "port": port}, indent=2))
    print(f"Saved printer address to {CONFIG_FILE}")


def load_config() -> Tuple[Optional[str], int]:
    """Load saved printer address from disk."""
    if CONFIG_FILE.exists():
        cfg = json.loads(CONFIG_FILE.read_text())
        return cfg.get("ip"), cfg.get("port", DEFAULT_PORT)
    return None, DEFAULT_PORT


# ============================================================================
# MOONRAKER CLIENT CLASS
# ============================================================================

class MoonrakerClient:
    """Low-level Moonraker API client."""

    def __init__(self, host: str, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get(self, path: str) -> Tuple[bool, Any]:
        return _http_request(f"{self.base_url}{path}")

    def _post(self, path: str, payload: Optional[Dict] = None) -> Tuple[bool, Any]:
        body = json.dumps(payload or {}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        return _http_request(f"{self.base_url}{path}", method="POST", data=body, headers=headers)

    def _delete(self, path: str) -> Tuple[bool, Any]:
        return _http_request(f"{self.base_url}{path}", method="DELETE")

    # ------------------------------------------------------------------
    # Discovery / Health
    # ------------------------------------------------------------------

    def test_connection(self) -> bool:
        """Check if Moonraker is reachable."""
        ok, data = self._get("/server/info")
        if ok:
            result = data.get("result", {})
            print(f"Connected to Moonraker!")
            print(f"  Version     : {result.get('version', '?')}")
            print(f"  Klipper     : {result.get('klippy_connected', False)}")
            print(f"  Components  : {', '.join(result.get('components', []))}")
            return True
        print(f"Connection failed: {data}")
        return False

    @staticmethod
    def discover_printers(
        subnet: str = DEFAULT_SUBNET,
        start: int = 1,
        end: int = 254,
        port: int = DEFAULT_PORT,
        max_workers: int = 50,
    ) -> List[str]:
        """Scan a subnet for Moonraker instances (port 7125)."""
        found: List[str] = []
        ips = [f"{subnet}.{i}" for i in range(start, end + 1)]

        def _probe(ip: str) -> Optional[str]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.4)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    # Port open -- verify it's Moonraker
                    ok, _ = _http_request(
                        f"http://{ip}:{port}/server/info", timeout=2
                    )
                    if ok:
                        return ip
            except Exception:
                pass
            return None

        print(f"Scanning {subnet}.{start} to {subnet}.{end} for port {port} ...")
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(_probe, ip): ip for ip in ips}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    found.append(result)
                    print(f"  [FOUND] Moonraker at {result}:{port}")

        if not found:
            print("  No Moonraker instances found on that subnet.")
        return found

    # ------------------------------------------------------------------
    # Printer Status
    # ------------------------------------------------------------------

    def get_status(self) -> Dict:
        """Query full printer status (toolhead, temperatures, gcode_move, etc.)."""
        objects = [
            "toolhead",
            "extruder",
            "extruder1",
            "heater_bed",
            "gcode_move",
            "print_stats",
            "virtual_sdcard",
            "fan",
            "display_status",
        ]
        params = "&".join(f"objects={urllib.parse.quote(o)}" for o in objects)
        ok, data = self._get(f"/printer/objects/query?{params}")
        if not ok:
            print(f"Error querying status: {data}")
            return {}
        return data.get("result", {}).get("status", {})

    def get_temps(self) -> Dict:
        """Query only temperature data."""
        objects = ["extruder", "extruder1", "heater_bed"]
        params = "&".join(f"objects={urllib.parse.quote(o)}" for o in objects)
        ok, data = self._get(f"/printer/objects/query?{params}")
        if not ok:
            return {}
        return data.get("result", {}).get("status", {})

    def get_print_stats(self) -> Dict:
        """Query print job statistics."""
        ok, data = self._get("/printer/objects/query?objects=print_stats&objects=virtual_sdcard")
        if not ok:
            return {}
        return data.get("result", {}).get("status", {})

    # ------------------------------------------------------------------
    # G-code / Control
    # ------------------------------------------------------------------

    def send_gcode(self, script: str) -> bool:
        """Execute a raw G-code script."""
        ok, data = self._post("/printer/gcode/script", {"script": script})
        if ok:
            print(f"  OK: G-code sent -> {script}")
            return True
        print(f"  ERROR: {data}")
        return False

    def home_axes(self, axes: str = "XYZ") -> bool:
        """Home axes (e.g. 'X', 'Y', 'Z', 'XYZ')."""
        print(f"Homing axes: {axes} ...")
        return self.send_gcode(f"G28 {axes}")

    def move_axis(self, axis: str, distance: float, speed: int = 6000) -> bool:
        """Relative move on an axis (mm)."""
        self.send_gcode("G91")  # relative mode
        ok = self.send_gcode(f"G1 {axis}{distance} F{speed}")
        self.send_gcode("G90")  # absolute mode
        return ok

    def set_fan_speed(self, speed_percent: float) -> bool:
        """Set part cooling fan (0-100)."""
        pwm = max(0, min(255, int(speed_percent / 100.0 * 255)))
        return self.send_gcode(f"M106 S{pwm}")

    # ------------------------------------------------------------------
    # Toolhead / Extruder
    # ------------------------------------------------------------------

    def get_toolhead(self) -> Dict:
        """Query toolhead info including active extruder."""
        ok, data = self._get("/printer/objects/query?objects=toolhead")
        if not ok:
            return {}
        return data.get("result", {}).get("status", {}).get("toolhead", {})

    def get_active_extruder(self) -> str:
        """Return the name of the currently active extruder."""
        th = self.get_toolhead()
        return th.get("extruder", "unknown")

    def set_active_extruder(self, name: str = "extruder") -> bool:
        """Activate an extruder (e.g. 'extruder' or 'extruder1')."""
        print(f"Activating extruder: {name}")
        return self.send_gcode(f"ACTIVATE_EXTRUDER EXTRUDER={name}")

    def set_temperature(self, heater: str, temp: float) -> bool:
        """Set a heater target temp (heater = 'extruder' | 'extruder1' | 'heater_bed')."""
        if heater == "heater_bed":
            return self.send_gcode(f"M140 S{temp}")
        return self.send_gcode(f"M104 S{temp} T{0 if heater == 'extruder' else 1}")

    def wait_for_temp(self, heater: str = "extruder", timeout: int = 300) -> bool:
        """Block until heater reaches target (best-effort via polling)."""
        start = time.time()
        while time.time() - start < timeout:
            temps = self.get_temps()
            info = temps.get(heater, {})
            actual = info.get("temperature", 0)
            target = info.get("target", 0)
            if target > 0 and abs(actual - target) < 2:
                print(f"  {heater} reached {actual:.1f} / {target:.1f} C")
                return True
            time.sleep(2)
        print(f"  TIMEOUT waiting for {heater}")
        return False

    # ------------------------------------------------------------------
    # File Management
    # ------------------------------------------------------------------

    def list_files(self, path: str = "gcodes") -> List[Dict]:
        """List G-code files on the printer."""
        ok, data = self._get(f"/server/files/list?root={path}")
        if ok:
            return data.get("result", [])
        print(f"Error listing files: {data}")
        return []

    def upload_file(self, local_path: str, remote_dir: str = "gcodes") -> bool:
        """Upload a G-code file to the printer."""
        local = Path(local_path)
        if not local.exists():
            print(f"File not found: {local}")
            return False

        boundary = "----MoonrakerUpload"
        filename = local.name
        file_bytes = local.read_bytes()

        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode("utf-8")
        body += file_bytes
        body += f"\r\n--{boundary}--\r\n".encode("utf-8")

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        }

        print(f"Uploading {filename} ({len(file_bytes)} bytes) ...")
        ok, data = _http_request(
            f"{self.base_url}/server/files/upload",
            method="POST",
            data=body,
            headers=headers,
            timeout=120,
        )
        if ok:
            print(f"  Uploaded -> {remote_dir}/{filename}")
            return True
        print(f"  Upload failed: {data}")
        return False

    def delete_file(self, path: str) -> bool:
        """Delete a file on the printer."""
        ok, data = self._delete(f"/server/files/gcodes/{urllib.parse.quote(path, safe='')}")
        if ok:
            print(f"  Deleted {path}")
            return True
        print(f"  Delete failed: {data}")
        return False

    # ------------------------------------------------------------------
    # Print Control
    # ------------------------------------------------------------------

    def start_print(self, filename: str) -> bool:
        """Start printing a G-code file."""
        print(f"Starting print: {filename}")
        ok, data = self._post(
            "/printer/print/start", {"filename": filename}
        )
        if ok:
            print("  Print started!")
            return True
        print(f"  Start failed: {data}")
        return False

    def pause_print(self) -> bool:
        ok, data = self._post("/printer/print/pause")
        if ok:
            print("  Print paused")
            return True
        print(f"  Pause failed: {data}")
        return False

    def resume_print(self) -> bool:
        ok, data = self._post("/printer/print/resume")
        if ok:
            print("  Print resumed")
            return True
        print(f"  Resume failed: {data}")
        return False

    def cancel_print(self) -> bool:
        ok, data = self._post("/printer/print/cancel")
        if ok:
            print("  Print cancelled")
            return True
        print(f"  Cancel failed: {data}")
        return False

    # ------------------------------------------------------------------
    # Calibration Routines
    # ------------------------------------------------------------------

    def pid_tune(self, heater: str = "extruder", target: int = 200, cycles: int = 5) -> bool:
        """Run PID autotune for a heater."""
        print(f"PID tuning {heater} to {target} C ({cycles} cycles) ...")
        print("  (This takes several minutes; do NOT interrupt)")
        if heater == "heater_bed":
            cmd = f"PID_CALIBRATE HEATER=heater_bed TARGET={target}"
        else:
            cmd = f"PID_CALIBRATE HEATER={heater} TARGET={target}"
        ok = self.send_gcode(cmd)
        if not ok:
            return False
        print("  PID tune running... monitor with 'status' command.")
        return True

    def save_config(self) -> bool:
        """Save Klipper config (writes config overrides)."""
        print("Saving Klipper config...")
        return self.send_gcode("SAVE_CONFIG")

    def calibrate_bed_mesh(self, profile: str = "default") -> bool:
        """Run bed mesh calibration."""
        print(f"Running bed mesh calibration (profile: {profile}) ...")
        print("  Ensure bed is at print temperature first!")
        ok = self.send_gcode(f"BED_MESH_CALIBRATE PROFILE={profile}")
        if ok:
            print("  Bed mesh calibration started.")
            self.send_gcode(f"BED_MESH_PROFILE SAVE={profile}")
        return ok

    def calibrate_pressure_advance(self, extruder: str = "extruder") -> bool:
        """Run pressure advance calibration (uses built-in Klipper macro or custom)."""
        print(f"Running pressure advance calibration for {extruder} ...")
        # Common macro names; adjust to your printer config
        macros = [
            "PRESSURE_ADVANCE_CALIBRATION",
            "PA_CALIBRATE",
            "TUNE_PRESSURE_ADVANCE",
        ]
        for macro in macros:
            ok = self.send_gcode(macro)
            if ok:
                return True
        # Fallback: guide the user to a manual tower
        print("  No pressure advance macro found. Use a manual PA tower G-code,")
        print("  or add a [gcode_macro PA_CALIBRATE] section to printer.cfg")
        return False

    def extrude(self, length: float, speed: int = 300) -> bool:
        """Extrude filament (mm)."""
        return self.send_gcode(f"M83\nG1 E{length} F{speed}")

    def retract(self, length: float, speed: int = 300) -> bool:
        """Retract filament (mm)."""
        return self.send_gcode(f"M83\nG1 E-{length} F{speed}")

    # ------------------------------------------------------------------
    # Monitoring
    # ------------------------------------------------------------------

    def monitor(self, interval: int = 5) -> None:
        """Live print progress monitor (blocks until print finishes)."""
        print("Monitoring print progress (Ctrl+C to stop)...")
        print("-" * 60)
        try:
            while True:
                stats = self.get_print_stats()
                ps = stats.get("print_stats", {})
                vsd = stats.get("virtual_sdcard", {})
                state = ps.get("state", "unknown")
                filename = ps.get("filename", "---")
                progress = ps.get("progress", 0)
                if vsd.get("progress"):
                    progress = vsd["progress"]
                temps = self.get_temps()
                extruder = temps.get("extruder", {})
                bed = temps.get("heater_bed", {})
                eta = ps.get("print_duration", 0) * (1 / max(progress, 0.001) - 1) if progress else 0

                print(
                    f"\r[{state:12s}] {filename:30s} "
                    f"{progress*100:5.1f}% | "
                    f"E:{extruder.get('temperature',0):.0f}/{extruder.get('target',0):.0f}C "
                    f"B:{bed.get('temperature',0):.0f}/{bed.get('target',0):.0f}C",
                    end="",
                    flush=True,
                )

                if state in ("complete", "cancelled", "error"):
                    print(f"\nPrint finished with state: {state}")
                    break
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitor stopped.")

    def emergency_stop(self) -> bool:
        """Trigger emergency stop (M112)."""
        print("!!! EMERGENCY STOP !!!")
        return self.send_gcode("M112")

    def firmware_restart(self) -> bool:
        """Restart Klipper firmware."""
        print("Restarting Klipper firmware...")
        ok, data = self._post("/printer/firmware_restart")
        if ok:
            print("  Firmware restart sent.")
            return True
        print(f"  Error: {data}")
        return False

    def host_restart(self) -> bool:
        """Restart the host (Linux system)."""
        print("Restarting host system...")
        ok, data = self._post("/machine/reboot")
        if ok:
            print("  Host reboot initiated.")
            return True
        print(f"  Error: {data}")
        return False


# ============================================================================
# PRETTY PRINTERS
# ============================================================================

def pprint_status(status: Dict) -> None:
    print("=" * 60)
    print("PRINTER STATUS")
    print("=" * 60)

    # Toolhead
    th = status.get("toolhead", {})
    print(f"\nToolhead:")
    print(f"  Position    : X={th.get('position',{}).get('x','?'):.1f} "
          f"Y={th.get('position',{}).get('y','?'):.1f} "
          f"Z={th.get('position',{}).get('z','?'):.1f}")
    print(f"  Active Ext. : {th.get('extruder', 'unknown')}")
    print(f"  Homed       : {th.get('homed_axes', '---')}")

    # Temperatures
    def show_temp(name: str, data: Dict):
        if data:
            print(f"  {name:12s}: {data.get('temperature',0):.1f} / {data.get('target',0):.1f} C")

    print(f"\nTemperatures:")
    show_temp("Extruder 0", status.get("extruder", {}))
    show_temp("Extruder 1", status.get("extruder1", {}))
    show_temp("Bed", status.get("heater_bed", {}))

    # Print stats
    ps = status.get("print_stats", {})
    print(f"\nPrint Stats:")
    print(f"  State       : {ps.get('state', 'idle')}")
    print(f"  File        : {ps.get('filename', '---')}")
    print(f"  Progress    : {ps.get('progress', 0)*100:.1f}%")
    print(f"  Duration    : {ps.get('print_duration', 0)/60:.1f} min")
    print(f"  Filament    : {ps.get('filament_used', 0)/1000:.2f} m")

    # Fan
    fan = status.get("fan", {})
    if fan:
        print(f"\nFan: {fan.get('speed',0)*100:.0f}%")


def pprint_temps(temps: Dict) -> None:
    print("\nCurrent Temperatures:")
    print("-" * 40)
    for name, data in temps.items():
        actual = data.get("temperature", 0)
        target = data.get("target", 0)
        print(f"  {name:15s}: {actual:.1f} C (target: {target:.1f} C)")


def pprint_files(files: List[Dict]) -> None:
    if not files:
        print("No files found.")
        return
    print(f"\n{'Name':<40s} {'Size':>10s}")
    print("-" * 55)
    for f in files:
        name = f.get("path", "?")
        size = f.get("size", 0)
        print(f"  {name:<38s} {size:>10,d}")


# ============================================================================
# CLI HANDLERS
# ============================================================================

def _get_client(args) -> MoonrakerClient:
    ip = args.ip
    port = args.port
    if not ip:
        saved_ip, saved_port = load_config()
        if saved_ip:
            ip, port = saved_ip, saved_port
            print(f"Using saved printer: {ip}:{port}")
        else:
            print("No printer IP provided or saved. Run 'discover' first, or use --ip.")
            sys.exit(1)
    return MoonrakerClient(ip, port)


def cmd_discover(args):
    printers = MoonrakerClient.discover_printers(
        subnet=args.subnet, start=args.start, end=args.end
    )
    if printers:
        save_config(printers[0])
        print(f"\nSaved first found printer: {printers[0]}")
    return printers


def cmd_status(args):
    client = _get_client(args)
    if args.connect:
        client.test_connection()
    status = client.get_status()
    pprint_status(status)
    return status


def cmd_temps(args):
    client = _get_client(args)
    temps = client.get_temps()
    pprint_temps(temps)
    return temps


def cmd_upload(args):
    client = _get_client(args)
    return client.upload_file(args.file)


def cmd_list(args):
    client = _get_client(args)
    files = client.list_files()
    pprint_files(files)
    return files


def cmd_print(args):
    client = _get_client(args)
    return client.start_print(args.filename)


def cmd_pause(args):
    client = _get_client(args)
    return client.pause_print()


def cmd_resume(args):
    client = _get_client(args)
    return client.resume_print()


def cmd_cancel(args):
    client = _get_client(args)
    return client.cancel_print()


def cmd_home(args):
    client = _get_client(args)
    return client.home_axes(args.axes)


def cmd_gcode(args):
    client = _get_client(args)
    return client.send_gcode(args.script)


def cmd_monitor(args):
    client = _get_client(args)
    client.monitor(interval=args.interval)


def cmd_pid(args):
    client = _get_client(args)
    client.pid_tune(heater=args.heater, target=args.target, cycles=args.cycles)
    if args.wait:
        print("Waiting for PID tune to complete...")
        # PID tune doesn't have a direct status; user monitors via temps
        time.sleep(10)
        while True:
            temps = client.get_temps()
            target = temps.get(args.heater, {}).get("target", 0)
            if target == 0:
                print("PID tune appears complete.")
                break
            time.sleep(5)
        client.save_config()


def cmd_bedmesh(args):
    client = _get_client(args)
    return client.calibrate_bed_mesh(profile=args.profile)


def cmd_pressure_advance(args):
    client = _get_client(args)
    return client.calibrate_pressure_advance(extruder=args.extruder)


def cmd_toolhead(args):
    client = _get_client(args)
    th = client.get_toolhead()
    print(f"Toolhead info:\n{json.dumps(th, indent=2)}")
    active = client.get_active_extruder()
    print(f"\nActive extruder: {active}")


def cmd_extruder(args):
    client = _get_client(args)
    if args.set:
        return client.set_active_extruder(args.set)
    else:
        print(f"Active extruder: {client.get_active_extruder()}")


def cmd_stop(args):
    client = _get_client(args)
    return client.emergency_stop()


def cmd_restart(args):
    client = _get_client(args)
    return client.firmware_restart()


# ============================================================================
# FIRST-TIME SETUP / CALIBRATION SCRIPT
# ============================================================================

def run_first_time_setup(args):
    """Automated first-time printer setup and calibration."""
    print("=" * 60)
    print("QIDI Plus 4 Max -- First-Time Setup")
    print("=" * 60)

    client = _get_client(args)

    # 1. Test connection
    print("\n--- 1. Testing Connection ---")
    if not client.test_connection():
        print("Connection failed! Run discover first.")
        return False

    # 2. Home axes
    print("\n--- 2. Homing Axes ---")
    client.home_axes("XYZ")
    time.sleep(2)

    # 3. PID tune extruder 0
    if not args.skip_pid:
        print("\n--- 3. PID Tuning Extruder 0 (200 C) ---")
        client.pid_tune("extruder", target=200, cycles=5)
        print("  (Wait ~10 min for PID tune to complete...)")
        time.sleep(600)  # rough wait
        client.save_config()

    # 4. PID tune extruder 1 (if dual extruder)
    if not args.skip_pid:
        print("\n--- 4. PID Tuning Extruder 1 (200 C) ---")
        client.pid_tune("extruder1", target=200, cycles=5)
        time.sleep(600)
        client.save_config()

    # 5. PID tune bed
    if not args.skip_pid:
        print("\n--- 5. PID Tuning Bed (60 C) ---")
        client.pid_tune("heater_bed", target=60, cycles=5)
        time.sleep(600)
        client.save_config()

    # 6. Bed mesh
    if not args.skip_bedmesh:
        print("\n--- 6. Bed Mesh Calibration ---")
        client.set_temperature("heater_bed", 60)
        client.wait_for_temp("heater_bed")
        client.calibrate_bed_mesh("default")
        print("  (Wait for mesh to complete...)")
        time.sleep(300)
        client.save_config()

    # 7. Pressure advance
    if not args.skip_pa:
        print("\n--- 7. Pressure Advance Calibration ---")
        client.calibrate_pressure_advance("extruder")

    print("\n--- Setup Complete! ---")
    print("Your QIDI Plus 4 Max is calibrated and ready to print.")
    return True


# ============================================================================
# ARGUMENT PARSER
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Moonraker API Client for QIDI Plus 4 Max (Klipper)",
    )
    p.add_argument("--ip", help="Printer IP address (or set via discover)")
    p.add_argument("--port", type=int, default=DEFAULT_PORT, help="Moonraker port")

    sub = p.add_subparsers(dest="command", help="Command to run")

    # discover
    sp = sub.add_parser("discover", help="Scan network for Moonraker")
    sp.add_argument("--subnet", default=DEFAULT_SUBNET, help="Subnet to scan (e.g. 192.168.50)")
    sp.add_argument("--start", type=int, default=1)
    sp.add_argument("--end", type=int, default=254)

    # status
    sp = sub.add_parser("status", help="Query full printer status")
    sp.add_argument("--connect", action="store_true", help="Also test connection")

    # temps
    sub.add_parser("temps", help="Query temperatures")

    # list
    sub.add_parser("list", help="List G-code files")

    # upload
    sp = sub.add_parser("upload", help="Upload a G-code file")
    sp.add_argument("file", help="Local G-code file path")

    # print
    sp = sub.add_parser("print", help="Start a print job")
    sp.add_argument("filename", help="Filename on printer")

    # pause / resume / cancel
    sub.add_parser("pause", help="Pause print")
    sub.add_parser("resume", help="Resume print")
    sub.add_parser("cancel", help="Cancel print")

    # home
    sp = sub.add_parser("home", help="Home axes")
    sp.add_argument("--axes", default="XYZ", help="Axes to home (e.g. XY, Z)")

    # gcode
    sp = sub.add_parser("gcode", help="Send raw G-code")
    sp.add_argument("script", help="G-code string")

    # monitor
    sp = sub.add_parser("monitor", help="Monitor print progress")
    sp.add_argument("--interval", type=int, default=5, help="Poll interval (seconds)")

    # pid
    sp = sub.add_parser("pid", help="Run PID autotune")
    sp.add_argument("--heater", default="extruder", help="Heater name")
    sp.add_argument("--target", type=int, default=200, help="Target temperature")
    sp.add_argument("--cycles", type=int, default=5)
    sp.add_argument("--wait", action="store_true", help="Wait for completion")

    # bedmesh
    sp = sub.add_parser("bedmesh", help="Run bed mesh calibration")
    sp.add_argument("--profile", default="default")

    # pressure-advance
    sp = sub.add_parser("pressure-advance", help="Calibrate pressure advance")
    sp.add_argument("--extruder", default="extruder")

    # toolhead
    sub.add_parser("toolhead", help="Query toolhead info")

    # extruder
    sp = sub.add_parser("extruder", help="Get/set active extruder")
    sp.add_argument("--set", help="Set active extruder (extruder / extruder1)")

    # emergency
    sub.add_parser("stop", help="Emergency stop (M112)")
    sub.add_parser("restart", help="Firmware restart")

    # setup
    sp = sub.add_parser("setup", help="First-time setup + calibration")
    sp.add_argument("--skip-pid", action="store_true")
    sp.add_argument("--skip-bedmesh", action="store_true")
    sp.add_argument("--skip-pa", action="store_true")

    return p


# ============================================================================
# MAIN
# ============================================================================

COMMANDS = {
    "discover": cmd_discover,
    "status": cmd_status,
    "temps": cmd_temps,
    "list": cmd_list,
    "upload": cmd_upload,
    "print": cmd_print,
    "pause": cmd_pause,
    "resume": cmd_resume,
    "cancel": cmd_cancel,
    "home": cmd_home,
    "gcode": cmd_gcode,
    "monitor": cmd_monitor,
    "pid": cmd_pid,
    "bedmesh": cmd_bedmesh,
    "pressure-advance": cmd_pressure_advance,
    "toolhead": cmd_toolhead,
    "extruder": cmd_extruder,
    "stop": cmd_stop,
    "restart": cmd_restart,
    "setup": run_first_time_setup,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    handler = COMMANDS.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
