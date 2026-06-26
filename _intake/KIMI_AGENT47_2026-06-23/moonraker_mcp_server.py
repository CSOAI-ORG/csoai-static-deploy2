#!/usr/bin/env python3
r"""
Moonraker MCP Server for QIDI Plus 4 Max (Klipper firmware)
===========================================================
An MCP (Model Context Protocol) server that wraps the Moonraker API,
enabling Claude Code (and other MCP clients) to control the 3D printer
via natural language commands.

Example usage from Claude Code:
  "What's the printer status?"
  "Start printing cube.gcode"
  "Pause the print"
  "What are the current temperatures?"
  "Home all axes"
  "Run PID tune on the extruder at 200C"
  "Upload my_3d_model.gcode to the printer"

Setup:
  1. Set MOONRAKER_IP environment variable (or it auto-discovers)
  2. pip install mcp
  3. Run: python moonraker_mcp_server.py
  4. Add to your Claude Code MCP config (see below)

Claude Code MCP Config (~/Library/Application\ Support/Claude/settings.json on macOS):
  {
    "mcpServers": {
      "moonraker": {
        "command": "python",
        "args": ["/path/to/moonraker_mcp_server.py"],
        "env": {
          "MOONRAKER_IP": "192.168.50.xxx"
        }
      }
    }
  }

Prerequisites:
  pip install mcp
"""

import asyncio
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Try to import the MCP SDK
# ---------------------------------------------------------------------------
try:
    from mcp.server import Server
    from mcp.types import (
        CallToolRequestParams,
        TextContent,
        Tool,
    )
    from mcp.server.stdio import stdio_server
except ImportError:
    print(
        "ERROR: The 'mcp' package is not installed.\n"
        "Install it with:  pip install mcp\n"
        "Docs: https://github.com/modelcontextprotocol/python-sdk"
    )
    sys.exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_PORT = 7125
MOONRAKER_IP = os.environ.get("MOONRAKER_IP", "")
MOONRAKER_PORT = int(os.environ.get("MOONRAKER_PORT", str(DEFAULT_PORT)))
CONFIG_FILE = Path.home() / ".config" / "moonraker_client.json"


# ============================================================================
# LOW-LEVEL HTTP HELPER
# ============================================================================

def _http_request(
    url: str,
    method: str = "GET",
    data: Optional[bytes] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
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


def _discover_printer(timeout: int = 5) -> Optional[str]:
    """Quick network scan to find Moonraker on common subnets."""
    import socket
    from concurrent.futures import ThreadPoolExecutor, as_completed

    subnets = ["192.168.50", "192.168.1", "192.168.0", "10.0.0"]
    port = DEFAULT_PORT

    def _probe(ip: str) -> Optional[str]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.4)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                ok, _ = _http_request(f"http://{ip}:{port}/server/info", timeout=2)
                if ok:
                    return ip
        except Exception:
            pass
        return None

    for subnet in subnets:
        ips = [f"{subnet}.{i}" for i in range(1, 255)]
        with ThreadPoolExecutor(max_workers=40) as pool:
            futures = {pool.submit(_probe, ip): ip for ip in ips}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    return result
    return None


def _load_saved_ip() -> Optional[str]:
    if CONFIG_FILE.exists():
        cfg = json.loads(CONFIG_FILE.read_text())
        return cfg.get("ip")
    return None


# ============================================================================
# MOONRAKER CLIENT (lightweight, for the MCP server)
# ============================================================================

class MoonrakerMCPClient:
    """Lightweight Moonraker client used by the MCP server."""

    def __init__(self, host: str, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    def _get(self, path: str) -> Tuple[bool, Any]:
        return _http_request(f"{self.base_url}{path}")

    def _post(self, path: str, payload: Optional[Dict] = None) -> Tuple[bool, Any]:
        body = json.dumps(payload or {}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        return _http_request(f"{self.base_url}{path}", method="POST", data=body, headers=headers)

    def _delete(self, path: str) -> Tuple[bool, Any]:
        return _http_request(f"{self.base_url}{path}", method="DELETE")

    # --- Endpoints ---

    def get_status(self) -> Dict:
        objects = [
            "toolhead", "extruder", "extruder1", "heater_bed",
            "gcode_move", "print_stats", "virtual_sdcard", "fan", "display_status",
        ]
        params = "&".join(f"objects={urllib.parse.quote(o)}" for o in objects)
        ok, data = self._get(f"/printer/objects/query?{params}")
        if ok:
            return data.get("result", {}).get("status", {})
        return {"error": str(data)}

    def get_temps(self) -> Dict:
        objects = ["extruder", "extruder1", "heater_bed"]
        params = "&".join(f"objects={urllib.parse.quote(o)}" for o in objects)
        ok, data = self._get(f"/printer/objects/query?{params}")
        if ok:
            return data.get("result", {}).get("status", {})
        return {"error": str(data)}

    def start_print(self, filename: str) -> Tuple[bool, str]:
        ok, data = self._post("/printer/print/start", {"filename": filename})
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def pause_print(self) -> Tuple[bool, str]:
        ok, data = self._post("/printer/print/pause")
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def resume_print(self) -> Tuple[bool, str]:
        ok, data = self._post("/printer/print/resume")
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def cancel_print(self) -> Tuple[bool, str]:
        ok, data = self._post("/printer/print/cancel")
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def home_axes(self, axes: str = "XYZ") -> Tuple[bool, str]:
        ok, data = self._post("/printer/gcode/script", {"script": f"G28 {axes}"})
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def send_gcode(self, script: str) -> Tuple[bool, str]:
        ok, data = self._post("/printer/gcode/script", {"script": script})
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def list_files(self) -> List[Dict]:
        ok, data = self._get("/server/files/list?root=gcodes")
        if ok:
            return data.get("result", [])
        return []

    def upload_file(self, local_path: str) -> Tuple[bool, str]:
        local = Path(local_path)
        if not local.exists():
            return False, f"File not found: {local_path}"

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

        ok, data = _http_request(
            f"{self.base_url}/server/files/upload",
            method="POST",
            data=body,
            headers=headers,
            timeout=120,
        )
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def pid_tune(self, heater: str, target: int, cycles: int = 5) -> Tuple[bool, str]:
        cmd = f"PID_CALIBRATE HEATER={heater} TARGET={target}"
        ok, data = self._post("/printer/gcode/script", {"script": cmd})
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def calibrate_bed_mesh(self, profile: str = "default") -> Tuple[bool, str]:
        ok, data = self._post("/printer/gcode/script", {"script": f"BED_MESH_CALIBRATE PROFILE={profile}"})
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def emergency_stop(self) -> Tuple[bool, str]:
        ok, data = self._post("/printer/gcode/script", {"script": "M112"})
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def firmware_restart(self) -> Tuple[bool, str]:
        ok, data = self._post("/printer/firmware_restart")
        return ok, json.dumps(data, indent=2) if ok else str(data)

    def get_server_info(self) -> Dict:
        ok, data = self._get("/server/info")
        if ok:
            return data.get("result", {})
        return {"error": str(data)}


# ============================================================================
# INITIALIZE CLIENT (with auto-discovery fallback)
# ============================================================================

def get_client() -> MoonrakerMCPClient:
    """Get or create the Moonraker client, with discovery fallback."""
    global MOONRAKER_IP
    if not MOONRAKER_IP:
        MOONRAKER_IP = _load_saved_ip() or ""
    if not MOONRAKER_IP:
        print("[MCP] No MOONRAKER_IP set, attempting auto-discovery...")
        discovered = _discover_printer()
        if discovered:
            MOONRAKER_IP = discovered
            print(f"[MCP] Discovered printer at {MOONRAKER_IP}")
        else:
            print("[MCP] WARNING: Could not discover printer. Set MOONRAKER_IP env var.")
    return MoonrakerMCPClient(MOONRAKER_IP, MOONRAKER_PORT)


# ============================================================================
# MCP SERVER
# ============================================================================

# Tool definitions with JSON schemas
TOOLS: List[Tool] = [
    Tool(
        name="printer_status",
        description="Get the full current status of the 3D printer including position, temperatures, print state, active extruder, and fan speed.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="query_temperatures",
        description="Query the current temperatures of the hotend(s) and heated bed, including actual and target values.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="start_print",
        description="Start printing a G-code file that is already on the printer.",
        inputSchema={
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the G-code file on the printer (e.g., 'cube.gcode')",
                },
            },
            "required": ["filename"],
        },
    ),
    Tool(
        name="pause_print",
        description="Pause the currently running print job.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="resume_print",
        description="Resume a paused print job.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="cancel_print",
        description="Cancel (abort) the currently running print job.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="home_axes",
        description="Home one or more axes (X, Y, Z, or all). Homes all axes by default.",
        inputSchema={
            "type": "object",
            "properties": {
                "axes": {
                    "type": "string",
                    "description": "Axes to home, e.g. 'XYZ', 'XY', 'Z'. Default is 'XYZ'.",
                    "default": "XYZ",
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="run_gcode",
        description="Execute custom G-code on the printer. Use this for any command not covered by other tools.",
        inputSchema={
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "The G-code string to execute (e.g., 'M104 S200', 'G1 X10 Y10 F3000')",
                },
            },
            "required": ["script"],
        },
    ),
    Tool(
        name="upload_file",
        description="Upload a G-code file from the local computer to the printer.",
        inputSchema={
            "type": "object",
            "properties": {
                "local_path": {
                    "type": "string",
                    "description": "Full local path to the G-code file to upload (e.g., '/Users/nick/Downloads/cube.gcode')",
                },
            },
            "required": ["local_path"],
        },
    ),
    Tool(
        name="list_files",
        description="List all G-code files stored on the printer.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="emergency_stop",
        description="EMERGENCY STOP - immediately halts all printer activity using M112.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="firmware_restart",
        description="Restart the Klipper firmware. Useful after config changes.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="pid_tune",
        description="Run PID autotune calibration for a heater. This optimizes temperature control.",
        inputSchema={
            "type": "object",
            "properties": {
                "heater": {
                    "type": "string",
                    "description": "Heater name: 'extruder', 'extruder1', or 'heater_bed'",
                },
                "target": {
                    "type": "integer",
                    "description": "Target temperature in Celsius (e.g., 200 for hotend, 60 for bed)",
                },
                "cycles": {
                    "type": "integer",
                    "description": "Number of PID cycles (default 5)",
                    "default": 5,
                },
            },
            "required": ["heater", "target"],
        },
    ),
    Tool(
        name="calibrate_bed_mesh",
        description="Run bed mesh calibration to create a height map of the print bed surface.",
        inputSchema={
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string",
                    "description": "Profile name to save the mesh as (default 'default')",
                    "default": "default",
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="set_temperature",
        description="Set the target temperature for a heater.",
        inputSchema={
            "type": "object",
            "properties": {
                "heater": {
                    "type": "string",
                    "description": "Heater name: 'extruder', 'extruder1', or 'heater_bed'",
                },
                "temperature": {
                    "type": "integer",
                    "description": "Target temperature in Celsius",
                },
            },
            "required": ["heater", "temperature"],
        },
    ),
    Tool(
        name="get_active_extruder",
        description="Get the currently active extruder/toolhead name.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="set_active_extruder",
        description="Switch to a different extruder (for dual-extruder printers).",
        inputSchema={
            "type": "object",
            "properties": {
                "extruder": {
                    "type": "string",
                    "description": "Extruder name: 'extruder' or 'extruder1'",
                },
            },
            "required": ["extruder"],
        },
    ),
]


# ============================================================================
# FORMATTERS
# ============================================================================

def _format_status(status: Dict) -> str:
    if "error" in status:
        return f"Error: {status['error']}"

    lines = ["3D Printer Status:", "=" * 40]

    th = status.get("toolhead", {})
    pos = th.get("position", {})
    lines.append(f"Position: X={pos.get('x','?'):.1f} Y={pos.get('y','?'):.1f} Z={pos.get('z','?'):.1f}")
    lines.append(f"Active Extruder: {th.get('extruder', 'unknown')}")
    lines.append(f"Homed Axes: {th.get('homed_axes', '---')}")

    ps = status.get("print_stats", {})
    lines.append(f"Print State: {ps.get('state', 'idle')}")
    lines.append(f"Current File: {ps.get('filename', '---')}")
    lines.append(f"Progress: {ps.get('progress', 0)*100:.1f}%")

    for name in ["extruder", "extruder1", "heater_bed"]:
        data = status.get(name, {})
        if data:
            lines.append(f"{name}: {data.get('temperature',0):.1f}C / {data.get('target',0):.1f}C")

    fan = status.get("fan", {})
    if fan:
        lines.append(f"Fan: {fan.get('speed',0)*100:.0f}%")

    return "\n".join(lines)


def _format_temps(temps: Dict) -> str:
    if "error" in temps:
        return f"Error: {temps['error']}"
    lines = ["Current Temperatures:", "-" * 30]
    for name, data in temps.items():
        actual = data.get("temperature", 0)
        target = data.get("target", 0)
        lines.append(f"  {name}: {actual:.1f} C (target: {target:.1f} C)")
    return "\n".join(lines)


def _format_files(files: List[Dict]) -> str:
    if not files:
        return "No G-code files found on the printer."
    lines = ["Files on Printer:", "-" * 40]
    for f in files:
        name = f.get("path", "?")
        size = f.get("size", 0)
        lines.append(f"  {name:<35s} {size:>10,d} bytes")
    return "\n".join(lines)


# ============================================================================
# SERVER SETUP
# ============================================================================

async def main():
    server = Server("moonraker-mcp")
    client: Optional[MoonrakerMCPClient] = None

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict) -> List[TextContent]:
        nonlocal client
        if client is None:
            try:
                client = get_client()
            except Exception as e:
                return [TextContent(type="text", text=f"Failed to connect to printer: {e}")]

        try:
            if name == "printer_status":
                status = client.get_status()
                return [TextContent(type="text", text=_format_status(status))]

            elif name == "query_temperatures":
                temps = client.get_temps()
                return [TextContent(type="text", text=_format_temps(temps))]

            elif name == "start_print":
                ok, result = client.start_print(arguments["filename"])
                msg = f"Print started: {arguments['filename']}" if ok else f"Failed: {result}"
                return [TextContent(type="text", text=msg)]

            elif name == "pause_print":
                ok, result = client.pause_print()
                return [TextContent(type="text", text="Print paused." if ok else f"Failed: {result}")]

            elif name == "resume_print":
                ok, result = client.resume_print()
                return [TextContent(type="text", text="Print resumed." if ok else f"Failed: {result}")]

            elif name == "cancel_print":
                ok, result = client.cancel_print()
                return [TextContent(type="text", text="Print cancelled." if ok else f"Failed: {result}")]

            elif name == "home_axes":
                axes = arguments.get("axes", "XYZ")
                ok, result = client.home_axes(axes)
                return [TextContent(type="text", text=f"Homed axes {axes}." if ok else f"Failed: {result}")]

            elif name == "run_gcode":
                ok, result = client.send_gcode(arguments["script"])
                return [TextContent(type="text", text=f"G-code sent: {arguments['script']}" if ok else f"Failed: {result}")]

            elif name == "upload_file":
                ok, result = client.upload_file(arguments["local_path"])
                return [TextContent(type="text", text=f"File uploaded." if ok else f"Failed: {result}")]

            elif name == "list_files":
                files = client.list_files()
                return [TextContent(type="text", text=_format_files(files))]

            elif name == "emergency_stop":
                ok, result = client.emergency_stop()
                return [TextContent(type="text", text="EMERGENCY STOP triggered!" if ok else f"Failed: {result}")]

            elif name == "firmware_restart":
                ok, result = client.firmware_restart()
                return [TextContent(type="text", text="Firmware restarted." if ok else f"Failed: {result}")]

            elif name == "pid_tune":
                ok, result = client.pid_tune(
                    arguments["heater"], arguments["target"], arguments.get("cycles", 5)
                )
                msg = f"PID tune started for {arguments['heater']} at {arguments['target']}C." if ok else f"Failed: {result}"
                return [TextContent(type="text", text=msg)]

            elif name == "calibrate_bed_mesh":
                profile = arguments.get("profile", "default")
                ok, result = client.calibrate_bed_mesh(profile)
                msg = f"Bed mesh calibration started (profile: {profile})." if ok else f"Failed: {result}"
                return [TextContent(type="text", text=msg)]

            elif name == "set_temperature":
                heater = arguments["heater"]
                temp = arguments["temperature"]
                if heater == "heater_bed":
                    cmd = f"M140 S{temp}"
                else:
                    idx = 0 if heater == "extruder" else 1
                    cmd = f"M104 S{temp} T{idx}"
                ok, result = client.send_gcode(cmd)
                msg = f"Set {heater} to {temp}C." if ok else f"Failed: {result}"
                return [TextContent(type="text", text=msg)]

            elif name == "get_active_extruder":
                status = client.get_status()
                th = status.get("toolhead", {})
                active = th.get("extruder", "unknown")
                return [TextContent(type="text", text=f"Active extruder: {active}")]

            elif name == "set_active_extruder":
                extruder = arguments["extruder"]
                ok, result = client.send_gcode(f"ACTIVATE_EXTRUDER EXTRUDER={extruder}")
                return [TextContent(type="text", text=f"Switched to {extruder}." if ok else f"Failed: {result}")]

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error executing {name}: {e}")]

    # Run the server via stdio
    async with stdio_server(server) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
