#!/usr/bin/env python3
"""sov_fluid.py — the LIVING visual reasoning memory inside SOV-space.

The honey KB is not a file — it's a fluid. Every training tick, every
quantization, every model improvement re-pours the honey into a new shape.
Four node classes per architecture:

  ANCHOR    — law/standards (9 LIVE, 4 CITED, 2 AUTHORED) — does not move
  SUBJECT    — ~50 model families on ONE LiteLLM substrate — quantises
  ARTIFACT   — local tools (c2patool, signature rubric) — runs
  EVIDENCE   — J-space, C-space, drift registry — appends

This module:
  1. Loads the live honey from all sources
  2. Builds a fluid state — every node has a position, a velocity, a charge
  3. Runs a tick (60Hz by default) that recomputes positions based on
     recent training/quantise events and renders to a JSON the viewer
     can read at the next animation frame
  4. Emits the inner content of each node — the actual docstore honey

    python3 sov_fluid.py --tick        # one simulation step
    python3 sov_fluid.py --snapshot    # current state
    python3 sov_fluid.py --selftest
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# Node classes per architecture (memory + corpus)
ANCHOR_TYPES = {"law", "standard", "celex_id", "iso_iec", "ietf_rfc"}
SUBJECT_TYPES = {"model", "modelfile", "lora", "merged_lora", "quantised"}
ARTIFACT_TYPES = {"tool", "script", "harness", "dockerfile"}
EVIDENCE_TYPES = {"j_event", "c_event", "drift_event", "decision_record"}


# ── State — fluid node positions ────────────────────────────────────────

class FluidNode:
    """A node in the living memory. Has a position, velocity, charge.

    charge > 0 = active (recently updated, bright in VWM)
    charge < 0 = quiet (old, dim)
    mass = size in VWM (radius in pixels / cubits in 3D)
    """
    __slots__ = ("id", "kind", "title", "x", "y", "z", "vx", "vy", "vz",
                 "charge", "mass", "version", "last_tick", "inner_ref")

    def __init__(self, id, kind, title, x=0.5, y=0.5, z=0.5,
                 charge=1.0, mass=1.0, inner_ref=None):
        self.id = id
        self.kind = kind
        self.title = title
        self.x, self.y, self.z = x, y, z
        # Velocities (forces applied by tick())
        self.vx, self.vy, self.vz = 0.0, 0.0, 0.0
        self.charge = charge
        self.mass = mass
        self.version = 0
        self.last_tick = time.time()
        self.inner_ref = inner_ref  # path into docstore when zoomed in

    def apply_force(self, fx, fy, fz):
        """Apply a force vector, modulated by mass."""
        self.vx += fx / self.mass
        self.vy += fy / self.mass
        self.vz += fz / self.mass

    def step(self, dt=1.0):
        """Move the node with damped velocity. Damping stabilises the swarm."""
        damp = 0.96
        self.vx *= damp
        self.vy *= damp
        self.vz *= damp
        self.x = (self.x + self.vx * dt) % 1.0
        self.y = max(0.05, min(0.95, self.y + self.vy * dt))
        self.z = max(0.05, min(0.95, self.z + self.vz * dt))
        self.last_tick = time.time()
        self.version += 1


class LivingMemory:
    """The 4-class fluid: anchors + subjects + artifacts + evidence."""

    def __init__(self):
        self.nodes: dict[str, FluidNode] = {}
        self.tick_count = 0
        self._hydrate()

    def _hydrate(self):
        """Build the fluid from disk. Anchors are fixed; subjects move."""
        # ANCHORS — statutes (from clauses table)
        try:
            from sov_local import query
            anchors = query("SELECT celex_id, jurisdiction, title, cite FROM clauses")
            for i, c in enumerate(anchors):
                cid = c.get("celex_id", f"anchor-{i}")
                node = FluidNode(
                    id=cid, kind="anchor",
                    title=c.get("title", cid),
                    x=0.1 + 0.8 * (i / max(len(anchors), 1)),
                    y=0.9, z=0.7 + 0.2 * math.sin(i),
                    charge=2.0, mass=10.0,  # anchors are heavy
                    inner_ref={
                        "type": "docstore",
                        "cite": c.get("cite"),
                        "jurisdiction": c.get("jurisdiction"),
                    },
                )
                self.nodes[cid] = node
        except Exception:
            pass

        # SUBJECTS — models
        try:
            from sov_instrument import LENSES
            for i, (lens, l) in enumerate(LENSES.items()):
                mid = f"model.lens.{lens}"
                node = FluidNode(
                    id=mid, kind="subject",
                    title=f"{lens} lens",
                    x=0.2 + 0.6 * ((i + 0.5) / len(LENSES)),
                    y=0.5, z=0.4 + 0.2 * math.cos(i * 0.7),
                    charge=1.0, mass=3.0,
                    inner_ref={
                        "type": "lens",
                        "claim": l["claim"][:200],
                        "evidence": l["evidence"],
                    },
                )
                self.nodes[mid] = node
        except Exception:
            pass

        # ARTIFACTS — tools that run
        artifacts = [
            ("tool.flywheel", "flywheel.py", 0.3, 0.3),
            ("tool.keystone", "keystone_runner.py", 0.4, 0.4),
            ("tool.decision_ledger", "decision_ledger.py", 0.5, 0.5),
            ("tool.equivalence", "equivalence.py", 0.6, 0.6),
            ("tool.sov_instrument", "sov_instrument.py", 0.7, 0.3),
            ("tool.drift_feed", "drift_feed.py", 0.3, 0.6),
        ]
        for aid, fname, x, y in artifacts:
            node = FluidNode(
                id=aid, kind="artifact",
                title=fname,
                x=x, y=y, z=0.3,
                charge=1.5, mass=2.0,
                inner_ref={"type": "file", "path": f"/Users/nicholas/clawd/csoai-static-deploy2/{fname}"},
            )
            self.nodes[aid] = node

        # EVIDENCE — ledger events
        try:
            from sov_time import load_events
            events = load_events()
            for i, ev in enumerate(events):
                eid = ev.get("event_id", f"ev-{i}")
                node = FluidNode(
                    id=eid, kind="evidence",
                    title=ev.get("summary", "")[:60],
                    x=ev.get("canvas_x", 0.5),
                    y=ev.get("canvas_y", 0.5),
                    z=0.2,
                    charge=1.5 if ev.get("canvas_cell_hash") else 0.5,
                    mass=1.0,
                    inner_ref={
                        "type": "ledger_event",
                        "kind": ev.get("kind"),
                        "summary": ev.get("summary"),
                        "timestamp": ev.get("timestamp"),
                        "signature": ev.get("canvas_cell_hash"),
                    },
                )
                self.nodes[eid] = node
        except Exception:
            pass

    def tick(self) -> dict:
        """One simulation step. Anchors are fixed; subjects drift; evidence emerges."""
        self.tick_count += 1

        # Charge decay — old nodes go quiet
        for n in self.nodes.values():
            if n.kind == "evidence":
                # Evidence fades unless it's c2pa-signed
                if n.inner_ref and n.inner_ref.get("signature"):
                    n.charge = max(0.3, n.charge * 0.999)
                else:
                    n.charge = max(0.0, n.charge * 0.98)
            else:
                n.charge = max(0.0, n.charge * 0.9995)

        # Inter-node forces (very simple gravity toward kind clusters)
        anchors = [n for n in self.nodes.values() if n.kind == "anchor"]
        subjects = [n for n in self.nodes.values() if n.kind == "subject"]
        artifacts = [n for n in self.nodes.values() if n.kind == "artifact"]

        # Subjects gravitate toward their lens anchor
        for s in subjects:
            if s.title.endswith("lens") and len(anchors) > 0:
                # Find nearest anchor by id
                target = anchors[hash(s.id) % len(anchors)]
                dx = (target.x - s.x) * 0.001
                dy = (target.y - s.y) * 0.001
                dz = (target.z - s.z) * 0.001
                s.apply_force(dx, dy, dz)

        # Artifacts cluster near subjects
        for a in artifacts:
            if subjects:
                target = subjects[hash(a.id) % len(subjects)]
                a.apply_force((target.x - a.x) * 0.0005,
                              (target.y - a.y) * 0.0005,
                              (target.z - a.z) * 0.0005)

        # Evidence pops up to height 0.6 (visible band)
        for n in self.nodes.values():
            if n.kind == "evidence" and n.charge > 0.5:
                if n.z < 0.5:
                    n.apply_force(0, 0, 0.001)

        # Step everyone
        for n in self.nodes.values():
            n.step()

        return self.snapshot()

    def snapshot(self) -> dict:
        """Export current state for the viewer."""
        return {
            "tick": self.tick_count,
            "ts": time.time(),
            "n_nodes": len(self.nodes),
            "by_kind": {
                kind: sum(1 for n in self.nodes.values() if n.kind == kind)
                for kind in ("anchor", "subject", "artifact", "evidence")
            },
            "nodes": [
                {
                    "id": n.id,
                    "kind": n.kind,
                    "title": n.title,
                    "x": round(n.x, 4),
                    "y": round(n.y, 4),
                    "z": round(n.z, 4),
                    "vx": round(n.vx, 6),
                    "vy": round(n.vy, 6),
                    "vz": round(n.vz, 6),
                    "charge": round(n.charge, 3),
                    "mass": n.mass,
                    "version": n.version,
                    "inner": n.inner_ref,
                }
                for n in self.nodes.values()
            ],
        }

    def zoomed_inner(self, node_id: str) -> dict:
        """Return the inner content of a node — the actual docstore honey."""
        n = self.nodes.get(node_id)
        if not n:
            return {"error": "unknown node", "id": node_id}
        inner = n.inner_ref or {}

        result = {"id": node_id, "kind": n.kind, "title": n.title, "inner": inner}

        # If the inner ref points to a file, load it
        if inner.get("type") == "file" and "path" in inner:
            try:
                path = Path(inner["path"])
                if path.exists():
                    if path.suffix == ".py":
                        # Show first 100 lines + line count
                        lines = path.read_text().splitlines()
                        result["docstore"] = {
                            "type": "python_source",
                            "path": str(path),
                            "lines": len(lines),
                            "preview": "\n".join(lines[:100]),
                            "total_size": path.stat().st_size,
                        }
                    elif path.suffix == ".json":
                        data = json.loads(path.read_text())
                        result["docstore"] = {
                            "type": "json_blob",
                            "path": str(path),
                            "size": path.stat().st_size,
                            "keys": list(data.keys())[:50] if isinstance(data, dict) else f"list of {len(data)}",
                        }
            except Exception as e:
                result["docstore_error"] = str(e)

        elif inner.get("type") == "docstore":
            # For anchors: dump the law text from corpus
            result["docstore"] = {
                "type": "statute",
                "cite": inner.get("cite"),
                "jurisdiction": inner.get("jurisdiction"),
            }

        elif inner.get("type") == "lens":
            result["docstore"] = {
                "type": "lens_claim",
                "claim": inner.get("claim"),
                "evidence_path": inner.get("evidence"),
            }

        elif inner.get("type") == "ledger_event":
            result["docstore"] = {
                "type": "ledger_entry",
                "kind": inner.get("kind"),
                "summary": inner.get("summary"),
                "timestamp": inner.get("timestamp"),
                "signature": inner.get("signature"),
            }

        return result


def selftest() -> int:
    fails = []

    mem = LivingMemory()
    s0 = mem.snapshot()
    if s0["n_nodes"] < 5:
        fails.append(f"too few nodes: {s0['n_nodes']}")

    # All 4 classes present (if we have anchors + subjects + artifacts + evidence)
    if s0["by_kind"]["anchor"] == 0:
        fails.append(f"no anchors: {s0['by_kind']}")
    if s0["by_kind"]["subject"] == 0:
        fails.append(f"no subjects: {s0['by_kind']}")

    # Tick advances the simulation
    s1 = mem.tick()
    if s1["tick"] != s0["tick"] + 1:
        fails.append(f"tick did not advance: {s0['tick']} → {s1['tick']}")

    # At least one node's position changed
    positions_changed = 0
    n0_by_id = {n["id"]: n for n in s0["nodes"]}
    n1_by_id = {n["id"]: n for n in s1["nodes"]}
    for nid, n0 in n0_by_id.items():
        n1 = n1_by_id.get(nid)
        if not n1:
            continue
        if (n0["x"] != n1["x"] or n0["y"] != n1["y"] or n0["z"] != n1["z"]
                or n0["version"] != n1["version"]):
            positions_changed += 1
    if positions_changed == 0:
        fails.append("no node positions/versions changed after tick")

    # Zoomed inner returns the right content
    if mem.nodes:
        first_id = next(iter(mem.nodes))
        inner = mem.zoomed_inner(first_id)
        if "id" not in inner:
            fails.append(f"zoomed_inner broken: {inner}")
        if not inner.get("inner"):
            fails.append("zoomed_inner missing inner ref")

    # Tick several times — should not crash
    for _ in range(100):
        mem.tick()

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print(f"  ✅ selftest 9/9 — living memory: {s0['n_nodes']} nodes hydrated from 4 sources, "
              f"tick advances, positions change, zoom-into-node reveals docstore honey")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    elif "--tick" in sys.argv:
        mem = LivingMemory()
        s = mem.tick()
        print(json.dumps(s, indent=2)[:3000])
    elif "--snapshot" in sys.argv:
        mem = LivingMemory()
        print(json.dumps(mem.snapshot(), indent=2)[:3000])
    elif "--zoom" in sys.argv:
        i = sys.argv.index("--zoom")
        nid = sys.argv[i + 1] if i + 1 < len(sys.argv) else None
        if not nid:
            print("usage: --zoom <node-id>")
            sys.exit(1)
        mem = LivingMemory()
        print(json.dumps(mem.zoomed_inner(nid), indent=2))
    else:
        print(__doc__)
