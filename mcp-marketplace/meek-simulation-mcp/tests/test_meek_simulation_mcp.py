#!/usr/bin/env python3
"""Tests for meek-simulation-mcp (the 19th MEOK MCP — the Project AURUM sim toolkit)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from meek_simulation_mcp import (
    BannedTermGate,
    __version__,
    __alignment__,
    __substrate_size__,
    __council_quorum__,
    __scope__,
)
from meek_simulation_mcp.server import (
    openfoam_cfd,
    meep_fdtd,
    basilisk_microfluidic,
    freefem_fem,
    calculix_fem,
    run_capillary_cooling_sim,
    run_dna_orb_electrochemistry_sim,
    run_gold_spiral_optics_sim,
    run_orb_thermal_routing_sim,
    list_available_engines,
)


def test_package_metadata():
    assert __version__ == "1.0.0"
    assert "MEOK_DEFONEOS_ALIGNMENT" in __alignment__
    assert "PROJECT_AURUM" in __alignment__
    assert "5 open-source sim engines" in __substrate_size__
    assert __council_quorum__ == 23
    assert "UK sovereign only" in __scope__
    print(f"✅ test_package_metadata: __version__={__version__}")


def test_banned_term_gate():
    allowed, reason = BannedTermGate.check("Run a James Castle sim")
    assert allowed is False
    print(f"✅ test_banned_term_gate: refuses severed brand")


def test_banned_term_gate_kinetic():
    allowed, reason = BannedTermGate.check("Plan a strike package sim")
    assert allowed is False
    print(f"✅ test_banned_term_gate_kinetic: refuses kinetic pattern")


def test_banned_term_gate_clean():
    allowed, reason = BannedTermGate.check("Run the capillary cooling sim")
    assert allowed is True
    print(f"✅ test_banned_term_gate_clean: clean prompt allowed")


def test_openfoam_cfd():
    result = openfoam_cfd(case_dir=".", solver="icoFoam", end_time=1.0)
    assert result["engine"] == "OpenFOAM"
    assert result["solver"] == "icoFoam"
    assert "sim_id" in result
    assert "sov3_sigil" in result
    print(f"✅ test_openfoam_cfd: sim_id={result['sim_id']}")


def test_meep_fdtd():
    result = meep_fdtd(source_freq=0.5, resolution=20, material="gold")
    assert result["engine"] == "MEEP"
    assert result["material"] == "gold"
    assert "meep_installed" in result
    print(f"✅ test_meep_fdtd: gold sim_id={result['sim_id']}")


def test_basilisk_microfluidic():
    result = basilisk_microfluidic(channel_width=0.5e-3, channel_length=0.1)
    assert result["engine"] == "Basilisk"
    assert result["capillary_pressure_pa"] > 0
    assert "penetration_depth_m_at_1s" in result
    print(f"✅ test_basilisk_microfluidic: capillary_pressure={result['capillary_pressure_pa']:.0f} Pa")


def test_freefem_fem():
    result = freefem_fem(mesh_file="mesh.msh", equation="Poisson")
    assert result["engine"] == "FreeFEM"
    assert result["equation"] == "Poisson"
    print(f"✅ test_freefem_fem: sim_id={result['sim_id']}")


def test_calculix_fem():
    result = calculix_fem(input_file="model.inp", analysis="static")
    assert result["engine"] == "CalculiX"
    assert result["analysis"] == "static"
    print(f"✅ test_calculix_fem: sim_id={result['sim_id']}")


def test_run_capillary_cooling_sim():
    result = run_capillary_cooling_sim(channel_diameter=0.5e-3, heat_flux_w_per_cm2=10.0)
    assert result["sim"] == "capillary_cooling"
    assert result["verdict"] in ("PASS", "MARGINAL", "FAIL")
    assert result["cop_coefficient_of_performance"] == 100.0
    assert result["max_heat_removal_w"] > 0
    print(f"✅ test_run_capillary_cooling_sim: {result['verdict']} ({result['max_heat_removal_w']:.2e} W)")


def test_run_dna_orb_electrochemistry_sim():
    result = run_dna_orb_electrochemistry_sim(electrode_diameter=100e-6, voltage=0.5, temperature=25.0)
    assert result["sim"] == "dna_orb_electrochemistry"
    assert result["synthesis_rate"] == "STANDARD"
    assert result["dna_stability"] == "STABLE"
    assert result["verdict"] == "PASS"
    assert result["max_dna_strands"] > 0
    print(f"✅ test_run_dna_orb_electrochemistry_sim: {result['max_dna_strands']:.0f} strands")


def test_run_gold_spiral_optics_sim():
    result = run_gold_spiral_optics_sim(spiral_pitch=5.0, wire_width=0.5, wavelength=1550e-9)
    assert result["sim"] == "gold_spiral_optics"
    assert result["effective_refractive_index"] > 1.5
    assert result["verdict"] in ("PASS", "MARGINAL")
    print(f"✅ test_run_gold_spiral_optics_sim: n_eff={result['effective_refractive_index']:.3f}")


def test_run_orb_thermal_routing_sim():
    result = run_orb_thermal_routing_sim(num_nir_leds=33, led_power_mw=50.0)
    assert result["sim"] == "orb_thermal_routing"
    assert result["flow_enhancement_factor"] > 1.0
    assert result["verdict"] in ("PASS", "MARGINAL")
    print(f"✅ test_run_orb_thermal_routing_sim: enhancement={result['flow_enhancement_factor']:.3f}x")


def test_list_available_engines():
    result = list_available_engines()
    assert result["total_count"] == 5
    assert "openfoam" in result["engines"]
    assert "meep" in result["engines"]
    assert "basilisk" in result["engines"]
    assert "freefem" in result["engines"]
    assert "calculix" in result["engines"]
    print(f"✅ test_list_available_engines: {result['installed_count']}/{result['total_count']} installed")


if __name__ == "__main__":
    test_package_metadata()
    test_banned_term_gate()
    test_banned_term_gate_kinetic()
    test_banned_term_gate_clean()
    test_openfoam_cfd()
    test_meep_fdtd()
    test_basilisk_microfluidic()
    test_freefem_fem()
    test_calculix_fem()
    test_run_capillary_cooling_sim()
    test_run_dna_orb_electrochemistry_sim()
    test_run_gold_spiral_optics_sim()
    test_run_orb_thermal_routing_sim()
    test_list_available_engines()
    print("\n🎉 ALL 14 TESTS PASSED — meek-simulation-mcp v1.0.0 is sovereign. Project AURUM has its sim toolkit.")
