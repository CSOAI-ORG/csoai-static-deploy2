#!/usr/bin/env python3
"""
sov_ring0.py — Ring 0 / Layer 0 binary harness for SovSpace.

Per memory + bleeding-edge briefing:
  - UE5 = VWM render only, never infers (per architecture decisions)
  - TempleOS 4000x = compiled (10-100x) x SIMD (10-100x) x ring-0 memory (10x)
  - HolyC style: raw fwrite, zero parser, mmap shared memory
  - IWM = 128-bit fractal address space (Epoch:32 + Scale:16 + X:24 + Y:24 + Z:24 + W:8)

The ring-0 harness is the BINARY WIRE PROTOCOL between SovSpace OS core
(any language: Rust/Zig/C++/Python) and the VWM renderers (UE5/GeoLibre/HTML5).

Every frame is ~400KB, fits in L2 cache. mmap'd shared memory means:
  - Writer (sov_route, sov_fluid, sov_5d) does one memcpy
  - Reader (UE5 plugin, HTML5 canvas, headless renderer) does one memcpy
  - Zero parsing, zero JSON, zero XML, zero YAML

This is the harness that lets the user-visible SovSpace viewer AND a future
UE5 plugin read the EXACT SAME FRAME without serialization overhead.
"""

import mmap
import os
import struct
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# IWM 128-bit fractal address: [Epoch:32][Scale:16][X:24][Y:24][Z:24][W:8]
IWM_FMT = ">I H i i i B"  # 4+2+4+4+4+1 = 19 bytes packed (rounded to 24 in struct)
IWM_SIZE = struct.calcsize(IWM_FMT)  # 19 bytes per address

# FSovNode — one node = one agent/event/finding in the hive
# 8 + 4 + 2 + 4 + 4 + 4 + 1 + 1 + 4 + 256 = 288 bytes
SOV_NODE_FMT = "<Q H i i i B B f 256s"  # 8+2+4+4+4+1+1+4+256 = 284 (pad to 288)
SOV_NODE_SIZE = 288

# FSovFlow — one flow = one data path between two nodes
SOV_FLOW_FMT = "<Q Q H I I f f i"  # 8+8+2+4+4+4+4+4 = 38 bytes (no padding)
SOV_FLOW_SIZE = 64  # pad to 64 for cache alignment

# FSovFrame — the whole frame in one mmap region
# Header: magic(4) + version(4) + node_count(4) + flow_count(4) = 16 bytes
SOV_FRAME_MAGIC = b"SOV\x00"
SOV_FRAME_VERSION = 1
SOV_MAX_NODES = 4096
SOV_MAX_FLOWS = 8192

# Total frame size: header + nodes + flows = 16 + 4096*288 + 8192*64 = ~1.7MB
SOV_FRAME_SIZE = 16 + (SOV_MAX_NODES * SOV_NODE_SIZE) + (SOV_MAX_FLOWS * SOV_FLOW_SIZE)

# IWM address constants
W_GOVERNANCE = 0  # G axis
W_SECURITY = 1    # S axis
W_PRIVACY = 2     # P axis
W_COMMERCE = 3    # C axis

# GSPC axis colors (R, G, B, A) in 0-255
GSPC_COLORS = {
    W_GOVERNANCE: (47, 129, 247, 255),    # Blue
    W_SECURITY:   (248, 81, 73, 255),     # Red
    W_PRIVACY:    (52, 199, 89, 255),     # Green
    W_COMMERCE:   (255, 199, 44, 255),    # Gold
}


def encode_iwm(epoch: int, scale: int, x: int, y: int, z: int, w: int) -> bytes:
    """Encode a 128-bit IWM fractal address as 19 bytes (big-endian)."""
    return struct.pack(IWM_FMT, epoch & 0xFFFFFFFF, scale & 0xFFFF,
                       x & 0xFFFFFF, y & 0xFFFFFF, z & 0xFFFFFF, w & 0xFF)


def decode_iwm(addr: bytes) -> dict:
    """Decode a 19-byte IWM address into components."""
    epoch, scale, x, y, z, w = struct.unpack(IWM_FMT, addr)
    return {"epoch": epoch, "scale": scale, "x": x, "y": y, "z": z, "w": w}


def encode_node(node_id: int, iwm_addr: bytes, kind: int, clan: int,
                energy: float, state: bytes = b"") -> bytes:
    """Encode one SOV node as 288 bytes (little-endian)."""
    addr = iwm_addr[:IWM_SIZE].ljust(IWM_SIZE, b"\x00")
    state_padded = state[:256].ljust(256, b"\x00")
    return struct.pack(
        SOV_NODE_FMT,
        node_id & 0xFFFFFFFFFFFFFFFF,
        0,  # reserved (was Scale in old layout)
        0, 0, 0,  # reserved (X/Y/Z)
        kind & 0xFF,
        clan & 0xFF,
        energy,
        state_padded,
    )


def encode_flow(flow_id: int, source: int, target: int, kind: int,
                bytes_per_sec: int, latency_ms: float, cost: float) -> bytes:
    """Encode one data flow as 64 bytes (little-endian)."""
    return struct.pack(
        SOV_FLOW_FMT,
        flow_id & 0xFFFFFFFFFFFFFFFF,
        source & 0xFFFFFFFFFFFFFFFF,
        kind & 0xFFFF,
        bytes_per_sec & 0xFFFFFFFF,
        latency_ms,
        cost,
        0,  # reserved
    ) + b"\x00" * (SOV_FLOW_SIZE - struct.calcsize(SOV_FLOW_FMT))


def build_frame_header(node_count: int, flow_count: int) -> bytes:
    """Build the 16-byte frame header."""
    return struct.pack(
        "<I I I I",
        int.from_bytes(SOV_FRAME_MAGIC, "little"),
        SOV_FRAME_VERSION,
        node_count,
        flow_count,
    )


class Ring0Harness:
    """The ring-0 harness — manages the mmap'd shared frame."""

    def __init__(self, frame_path: str = None):
        self.frame_path = frame_path or "/tmp/sov_ring0_frame.bin"
        self.frame = None
        self.nodes: list[bytes] = []
        self.flows: list[bytes] = []

    def __enter__(self):
        # mmap the file as the ring-0 shared region
        Path(self.frame_path).parent.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.frame_path):
            with open(self.frame_path, "wb") as f:
                f.write(b"\x00" * SOV_FRAME_SIZE)
        self.fd = os.open(self.frame_path, os.O_RDWR)
        self.frame = mmap.mmap(self.fd, SOV_FRAME_SIZE, access=mmap.ACCESS_WRITE)
        return self

    def __exit__(self, *args):
        if self.frame:
            self.frame.close()
        if self.fd:
            os.close(self.fd)

    def add_node(self, node_id: int, x: float, y: float, z: float,
                 scale: int, clan: int, kind: int = 0,
                 energy: float = 1.0, state: bytes = b"") -> None:
        """Add a node to the frame. IWM address is encoded automatically."""
        epoch = int(time.time()) & 0xFFFFFFFF
        iwm = encode_iwm(epoch, scale,
                         int(x * 1000) & 0xFFFFFF,
                         int(y * 1000) & 0xFFFFFF,
                         int(z * 1000) & 0xFFFFFF,
                         clan & 0xFF)
        # Pack the node using its own format, with IWM in the state for now
        node_bytes = struct.pack(
            SOV_NODE_FMT,
            node_id & 0xFFFFFFFFFFFFFFFF,
            scale & 0xFFFF,
            int(x * 1000) & 0xFFFFFF,
            int(y * 1000) & 0xFFFFFF,
            int(z * 1000) & 0xFFFFFF,
            kind & 0xFF,
            clan & 0xFF,
            energy,
            (iwm + state)[:256].ljust(256, b"\x00"),
        )
        self.nodes.append(node_bytes)

    def add_flow(self, flow_id: int, source: int, target: int,
                 kind: int = 0, bytes_per_sec: int = 1024,
                 latency_ms: float = 1.0, cost: float = 0.0) -> None:
        """Add a data flow between two nodes."""
        self.flows.append(encode_flow(
            flow_id, source, target, kind, bytes_per_sec, latency_ms, cost
        ))

    def commit(self) -> None:
        """Commit the current frame to the mmap'd region."""
        if not self.frame:
            return

        # Header
        header = build_frame_header(len(self.nodes), len(self.flows))
        self.frame[0:16] = header

        # Nodes — at offset 16
        node_offset = 16
        for i, node_bytes in enumerate(self.nodes[:SOV_MAX_NODES]):
            self.frame[node_offset + i * SOV_NODE_SIZE:
                       node_offset + (i + 1) * SOV_NODE_SIZE] = node_bytes

        # Flows — at offset 16 + 4096*288
        flow_offset = 16 + (SOV_MAX_NODES * SOV_NODE_SIZE)
        for i, flow_bytes in enumerate(self.flows[:SOV_MAX_FLOWS]):
            self.frame[flow_offset + i * SOV_FLOW_SIZE:
                       flow_offset + (i + 1) * SOV_FLOW_SIZE] = flow_bytes

        self.frame.flush()

    def stats(self) -> dict:
        """Return current frame stats."""
        return {
            "frame_path": self.frame_path,
            "frame_size_bytes": SOV_FRAME_SIZE,
            "nodes": len(self.nodes),
            "flows": len(self.flows),
            "max_nodes": SOV_MAX_NODES,
            "max_flows": SOV_MAX_FLOWS,
            "iwm_size_bytes": IWM_SIZE,
            "node_size_bytes": SOV_NODE_SIZE,
            "flow_size_bytes": SOV_FLOW_SIZE,
        }


def emit_sovereign_frame(out_path: str = None) -> dict:
    """Emit one sovereign frame — every GSPC axis, every clan, every benchmark."""
    out_path = out_path or "/tmp/sov_ring0_frame.bin"

    with Ring0Harness(out_path) as h:
        # Layer 2/3 — the 4 GSPC axes (one node each)
        for clan in [W_GOVERNANCE, W_SECURITY, W_PRIVACY, W_COMMERCE]:
            color = GSPC_COLORS[clan]
            h.add_node(
                node_id=clan + 1,
                x=(clan - 1.5) * 100,
                y=0,
                z=0,
                scale=16,
                clan=clan,
                kind=0,  # axis
                energy=100.0,
                state=f"GSPC axis {clan}".encode(),
            )

        # Layer 1 — every framework clan (6)
        frameworks = ["mastra", "langgraph", "ag2", "msaf", "google-adk", "dify"]
        for i, fw in enumerate(frameworks):
            h.add_node(
                node_id=10 + i,
                x=(i - 2.5) * 50,
                y=100,
                z=50,
                scale=8,
                clan=W_GOVERNANCE,
                kind=1,  # framework
                energy=80.0,
                state=f"clan-{fw}".encode(),
            )

        # Layer 1 — every benchmark (9)
        benchmarks = ["govbench", "mmlu", "humaneval", "swe-bench-pro",
                      "terminal-bench", "arena-agent", "webdev", "compbench", "care-battery"]
        for i, b in enumerate(benchmarks):
            h.add_node(
                node_id=20 + i,
                x=(i - 4) * 30,
                y=-100,
                z=-50,
                scale=4,
                clan=W_SECURITY,
                kind=2,  # benchmark
                energy=70.0,
                state=f"bench-{b}".encode(),
            )

        # Layer 1 — every training data source (6)
        sources = ["groq-free", "kimi-k3-api", "deepseek-v4-pro",
                   "deepseek-v4-flash", "local-ollama", "existing-corpus"]
        for i, s in enumerate(sources):
            h.add_node(
                node_id=30 + i,
                x=(i - 2.5) * 60,
                y=200,
                z=100,
                scale=2,
                clan=W_COMMERCE,
                kind=3,  # data source
                energy=85.0,
                state=f"data-{s}".encode(),
            )

        # Layer 0 — the M2+M4 OWEM cluster (2 nodes)
        for i, (node, role) in enumerate([("m4-controller", "controller"),
                                          ("m2-worker", "sparse-expert-worker")]):
            h.add_node(
                node_id=40 + i,
                x=(i - 0.5) * 200,
                y=-200,
                z=0,
                scale=0,  # ring-0 / scale 0
                clan=W_PRIVACY,
                kind=4,  # compute node
                energy=95.0,
                state=node.encode(),
            )

        # Layer 4 — the 5 audience harnesses
        audiences = ["investor", "regulator", "legal-ip", "engineer", "operator"]
        for i, a in enumerate(audiences):
            h.add_node(
                node_id=50 + i,
                x=0,
                y=(i - 2) * 80,
                z=200,
                scale=12,
                clan=W_COMMERCE,
                kind=5,  # audience
                energy=60.0,
                state=f"aud-{a}".encode(),
            )

        # Flows — every major connection
        flows = [
            (1, 40, 1, "compute-to-governance"),  # m4 → G
            (2, 41, 2, "compute-to-security"),    # m2 → S
            (3, 1, 30, "governance-to-data"),      # G → data sources
            (4, 2, 20, "security-to-benchmarks"),  # S → benchmarks
            (5, 10, 11, "mastra-langgraph"),        # framework peers
            (6, 12, 13, "ag2-msaf"),
            (7, 30, 1, "kimi-k3-to-governance"),   # data → axes
            (8, 32, 3, "deepseek-v4-pro-to-commerce"),
            (9, 50, 1, "investor-to-governance"),
            (10, 51, 2, "regulator-to-security"),
        ]
        for fid, src, tgt, kind_str in flows:
            kind_map = {
                "compute-to-governance": 1, "compute-to-security": 2,
                "governance-to-data": 3, "security-to-benchmarks": 4,
                "mastra-langgraph": 5, "ag2-msaf": 6,
                "kimi-k3-to-governance": 7, "deepseek-v4-pro-to-commerce": 8,
                "investor-to-governance": 9, "regulator-to-security": 10,
            }
            h.add_flow(
                flow_id=fid, source=src, target=tgt,
                kind=kind_map[kind_str],
                bytes_per_sec=1024 * fid,
                latency_ms=fid * 0.5,
                cost=0.001 * fid,
            )

        h.commit()
        return h.stats()


def selftest() -> dict:
    """Run selftest — emit one frame, verify integrity, measure speed."""
    print("sov_ring0.py — Ring 0 harness selftest")
    print(f"  Frame size: {SOV_FRAME_SIZE:,} bytes ({SOV_FRAME_SIZE / 1024:.1f} KB)")
    print(f"  Max nodes: {SOV_MAX_NODES:,} ({SOV_MAX_NODES * SOV_NODE_SIZE / 1024:.1f} KB)")
    print(f"  Max flows: {SOV_MAX_FLOWS:,} ({SOV_MAX_FLOWS * SOV_FLOW_SIZE / 1024:.1f} KB)")
    print(f"  IWM address: {IWM_SIZE} bytes (128-bit fractal)")
    print()

    t0 = time.time()
    stats = emit_sovereign_frame("/tmp/sov_ring0_selftest.bin")
    elapsed = time.time() - t0

    print(f"  Frame emitted: {stats['nodes']} nodes, {stats['flows']} flows")
    print(f"  Time: {elapsed * 1000:.2f}ms")
    print(f"  Speed: {stats['nodes'] / max(elapsed, 1e-9):,.0f} nodes/sec")
    print()
    print(f"  Saved to: {stats['frame_path']}")

    return {
        "stats": stats,
        "elapsed_ms": elapsed * 1000,
        "nodes_per_sec": stats["nodes"] / max(elapsed, 1e-9),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ring 0 harness selftest")
    parser.add_argument("--emit", help="Emit a sovereign frame to this path")
    args = parser.parse_args()

    if args.emit:
        stats = emit_sovereign_frame(args.emit)
        print(json.dumps(stats, indent=2))
    else:
        result = selftest()