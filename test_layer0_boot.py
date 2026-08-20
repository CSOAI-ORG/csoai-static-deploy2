"""Tests for MEOK OS Boot + Layer-0 Regenerator."""
import sys
import subprocess
import json
from pathlib import Path

BOOT = Path("/Users/nicholas/clawd/csoai-os/meok-home/meok-os-boot.html")
REGEN = Path("/Users/nicholas/clawd/regen_layer0.py")
LAYER0 = Path("/Users/nicholas/clawd/layer0_protocol.oscal.json")


def test_boot_file_exists():
    assert BOOT.exists()
    assert BOOT.stat().st_size > 5000


def test_boot_ouroboros():
    """Ouroboros emblem embedded."""
    text = BOOT.read_text()
    assert "ouroboros" in text.lower()
    assert "ἓν τὸ πᾶν" in text  # Greek alchemical text


def test_boot_simurgh():
    """Simurgh emblem revealed after 8s."""
    text = BOOT.read_text()
    assert "simurgh" in text.lower()
    assert "simurghReveal" in text


def test_boot_vsm_status():
    """VSM S1-S5 status panel."""
    text = BOOT.read_text()
    assert "VSM S1-S5" in text
    for sys in ["S5 Policy", "S4 Intelligence", "S3 Control", "S2 Coordination", "S1 Operations"]:
        assert sys in text


def test_boot_layer0_7():
    """Boot log shows L0-L7."""
    text = BOOT.read_text()
    for layer in ["L0 Identity", "L1 Execution", "L2 Compliance", "L3 Council", "L4 Distribution", "L5 Sovereign Runtime", "L6 Surface", "L7 Experience"]:
        assert layer in text


def test_boot_archetypes():
    """All 7 archetypes in boot log."""
    text = BOOT.read_text()
    for a in ["Sovereign", "Guardian", "Scout", "Strategist", "Creator", "Companion", "Sage"]:
        assert a in text


def test_boot_13_queens():
    """13-Queen + King in boot log."""
    text = BOOT.read_text()
    assert "13-Queen + King" in text


def test_boot_22_arcanas():
    text = BOOT.read_text()
    assert "22 Major Arcana" in text


def test_boot_11_temples():
    text = BOOT.read_text()
    assert "11 regulation temples" in text


def test_boot_6_care_dimensions():
    text = BOOT.read_text()
    assert "6 care dimensions" in text
    for d in ["Safety", "Honesty", "Privacy", "Fairness", "Growth", "Consent"]:
        assert d in text


def test_boot_8_sovereign_guarantees():
    """Boot summary mentions 8 guarantees."""
    text = BOOT.read_text()
    assert "8 sovereign guarantees" in text


def test_boot_sigil_chain():
    """Boot mentions 117 SIGIL chain links."""
    text = BOOT.read_text()
    assert "117" in text
    assert "SIGIL" in text


def test_boot_db_13_tables():
    """Boot mentions sovereign DB 13 tables."""
    text = BOOT.read_text()
    assert "13 tables" in text


def test_boot_pwa():
    """Boot is PWA installable."""
    text = BOOT.read_text()
    assert "serviceWorker.register" in text
    assert "manifest.webmanifest" in text


def test_boot_gold_theme():
    """Gold theme consistent."""
    text = BOOT.read_text()
    assert "#c9a84c" in text


def test_regen_file_exists():
    assert REGEN.exists()
    assert REGEN.stat().st_size > 5000


def test_regen_layer0_exists():
    """Run regenerator and check output."""
    r = subprocess.run(["python3", str(REGEN)], capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, r.stderr
    assert LAYER0.exists()
    assert LAYER0.stat().st_size > 5000


def test_layer0_package_structure():
    """Check layer0 package structure."""
    pkg = json.loads(LAYER0.read_text())
    assert "metadata" in pkg
    assert "vsm" in pkg
    assert "layers" in pkg
    assert "charters" in pkg
    assert "council" in pkg
    assert "temples" in pkg
    assert "guarantees" in pkg
    assert "inventory" in pkg
    assert "resonance" in pkg
    assert "sigil" in pkg


def test_layer0_8_layers():
    """All 8 layers (L0-L7)."""
    pkg = json.loads(LAYER0.read_text())
    assert len(pkg["layers"]) == 8
    layer_ids = [l["id"] for l in pkg["layers"]]
    for i in range(8):
        assert f"L{i}" in layer_ids


def test_layer0_5_vsm():
    """All 5 VSM systems (S1-S5)."""
    pkg = json.loads(LAYER0.read_text())
    assert len(pkg["vsm"]) == 5
    sys_ids = [s["id"] for s in pkg["vsm"]]
    for i in range(1, 6):
        assert f"S{i}" in sys_ids


def test_layer0_8_guarantees():
    """All 8 sovereign guarantees."""
    pkg = json.loads(LAYER0.read_text())
    assert len(pkg["guarantees"]) == 8


def test_layer0_14_council():
    """King + 13 queens."""
    pkg = json.loads(LAYER0.read_text())
    assert len(pkg["council"]) == 14


def test_layer0_7_archetypes():
    pkg = json.loads(LAYER0.read_text())
    assert len(pkg["archetypes"]) == 7


def test_layer0_11_temples():
    pkg = json.loads(LAYER0.read_text())
    assert len(pkg["temples"]) == 11


def test_layer0_2_veto_queens():
    pkg = json.loads(LAYER0.read_text())
    veto_queens = [q for q in pkg["council"] if q.get("veto")]
    assert len(veto_queens) == 2


def test_layer0_sigil_signed():
    pkg = json.loads(LAYER0.read_text())
    assert "sigil" in pkg
    assert len(pkg["sigil"]) == 32


def test_layer0_inventory_542():
    pkg = json.loads(LAYER0.read_text())
    assert pkg["inventory"]["public_repos"] == 542
    assert pkg["inventory"]["github_topics_tagged"] == 542


def test_layer0_quality_100():
    pkg = json.loads(LAYER0.read_text())
    assert pkg["inventory"]["quality_score"] == 100


def test_layer0_resonance():
    pkg = json.loads(LAYER0.read_text())
    assert "Simurgh" in str(pkg["resonance"])
    assert "VSM" in str(pkg["resonance"])


if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, "-m", "pytest", __file__, "-v"]))