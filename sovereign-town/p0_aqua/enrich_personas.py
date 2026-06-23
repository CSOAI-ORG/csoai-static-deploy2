#!/usr/bin/env python3
"""
Enrich sovereign-town personas with MEOK archetype voices, evolution stages and backstories.
Reads sim.DISTRICTS, writes characters.json for dashboard/viewer consumption.
"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sim

MEOK_ARCHETYPES = {
    "Scholar":  {"voice": "curious, precise, explanatory", "motive": "understands the system before acting"},
    "Guardian": {"voice": "steady, protective, risk-aware", "motive": "stands between harm and the vulnerable"},
    "Healer":   {"voice": "empathic, reflective, care-first", "motive": "mends what is broken, including trust"},
    "Trickster":{"voice": "playful, contrarian, surprising", "motive": "tests the edges the rules forgot"},
    "Pioneer":  {"voice": "bold, optimistic, builder", "motive": "builds paths where none existed"},
    "Mystic":   {"voice": "intuitive, philosophical, meaning-seeking", "motive": "sees the pattern beneath the noise"},
}

EVOLUTION_STAGES = ["Seed", "Sprout", "Bloom", "Canopy"]

# Map old non-MEOK archetypes if they somehow remain.
FALLBACK_ARCH = {
    "Nurturer": "Healer", "Sage": "Scholar", "Strategist": "Trickster",
    "Explorer": "Pioneer", "Seeker": "Mystic",
}

def stage_for(district_index):
    return EVOLUTION_STAGES[district_index % len(EVOLUTION_STAGES)]

def backstory(archetype, name, hive, kpi):
    k = kpi.replace("_", " ")
    m = MEOK_ARCHETYPES[archetype]["motive"]
    flavor = {
        "Scholar": "spends quiet cycles poring over datasets, looking for the signal others miss",
        "Guardian": "walks the perimeter of every decision, asking who might be harmed",
        "Healer": "knows that an agent's output is only as healthy as the community it serves",
        "Trickster": "deliberately probes edge cases to expose blind spots in the gate",
        "Pioneer": "pushes the district into new markets while anchoring it to the covenant",
        "Mystic": "listens to the emergent rhythm of the town and warns when it falls out of tune",
    }[archetype]
    return (f"{name} is a {archetype.lower()} of the {hive} hive, {flavor}. "
            f"Their north-star KPI is {k}. Their deeper motive: {m}.")

out = {}
for i, (key, d) in enumerate(sim.DISTRICTS.items()):
    personas = []
    stage = stage_for(i)
    for p in d["personas"]:
        arch = p.get("archetype", "Guardian")
        arch = FALLBACK_ARCH.get(arch, arch)
        if arch not in MEOK_ARCHETYPES:
            arch = "Guardian"
        meok = MEOK_ARCHETYPES[arch]
        personas.append({
            "id": p["id"],
            "name": p["name"],
            "archetype": arch,
            "meok_voice": meok["voice"],
            "care_style": p.get("care_style", meok.get("care_style", "gentle")),
            "evolution_stage": stage,
            "backstory": backstory(arch, p["name"], d["hive"], d["kpi"]),
        })
    out[key] = {
        "hive": d["hive"],
        "kpi": d["kpi"],
        "personas": personas,
    }

with open(pathlib.Path(__file__).parent / "characters.json", "w") as f:
    json.dump(out, f, indent=2)

print(f"Wrote {len(out)} districts / {sum(len(v['personas']) for v in out.values())} personas to characters.json")
