#!/usr/bin/env python3
"""
e2e-m4-sovereign-integration.py — E2E test for the M4 sovereign-governance PROFILE
integration with the sibling's MEOKOS SAP stack.

Tests:
1. The M4 sovereign-governance PROFILE issues correctly
2. The 8 protocols + 8 guarantees + 6 care dimensions are present
3. The Care Floor calculator works (pass + fail + Article 9 4-eyes lethal)
4. The BFT tally works (22-of-33 approved, 21-of-33 rejected)
5. The layer-0 extension validates
6. The M4 PROFILE can be added to a SAP query without breaking it
7. The fingerprint is consistent across all calls

Author: M4 lane. MIT. 2 Jul 2026.

Run:
  python3 e2e-m4-sovereign-integration.py
"""
import json
import hashlib
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'api'))
from m4_sovereign_profile import (
    build_sovereign_profile, build_layer0_extension,
    compute_care_floor, care_floor_passes,
    cast_bft_vote, tally_bft_votes, CANONICAL_FINGERPRINT,
)


failed = []
passed = []


def t(name, ok, detail=""):
    marker = "✅" if ok else "❌"
    print(f"  {marker} {name}" + (f"  {detail}" if detail else ""))
    if ok:
        passed.append(name)
    else:
        failed.append(name)


# === Test 1: PROFILE issues ===
print("\n=== 1. PROFILE ISSUANCE ===")
profile = build_sovereign_profile("did:csoai:sarah-001", 0.95, 1)
t("PROFILE has @context", profile.get("@context") == "https://csoai.org/ns/sovereign-governance/v1")
t("PROFILE has @type=SovereignGovernanceProfile", profile.get("@type") == "SovereignGovernanceProfile")
t("PROFILE has issuer=did:csoai:csoai-org-001", profile.get("issuer") == "did:csoai:csoai-org-001")
t("PROFILE has issued_to=did:csoai:sarah-001", profile.get("issued_to") == "did:csoai:sarah-001")
t("PROFILE has fingerprint=SOV:D78A-DC19-4F2A-9E10-3B81", profile.get("fingerprint") == CANONICAL_FINGERPRINT)
t("PROFILE has care_floor=0.95", profile.get("care_floor") == 0.95)
t("PROFILE has bft_quorum=22-of-33", profile.get("bft_quorum") == "22-of-33")
t("PROFILE has issued_at (ISO 8601)", "T" in profile.get("issued_at", ""))
t("PROFILE has vote_weight=1", profile.get("vote_weight") == 1)


# === Test 2: 8 protocols + 8 guarantees + 6 care dimensions ===
print("\n=== 2. THE 8 PROTOCOLS + 8 GUARANTEES + 6 CARE DIMENSIONS ===")
t("PROFILE has 8 protocols", len(profile.get("protocols", {})) == 8)
t("PROFILE has p1_mcp_federation", "p1_mcp_federation" in profile.get("protocols", {}))
t("PROFILE has p8_compliance_passport", "p8_compliance_passport" in profile.get("protocols", {}))
t("PROFILE has 8 guarantees", len(profile.get("guarantees", {})) == 8)
t("PROFILE has g1_public", "g1_public" in profile.get("guarantees", {}))
t("PROFILE has g8_article_9", "g8_article_9" in profile.get("guarantees", {}))
t("PROFILE has 6 care_dimensions", len(profile.get("care_dimensions", {})) == 6)
t("PROFILE has c1_safety", "c1_safety" in profile.get("care_dimensions", {}))
t("PROFILE has c6_audit", "c6_audit" in profile.get("care_dimensions", {}))


# === Test 3: Care Floor calculator ===
print("\n=== 3. CARE FLOOR CALCULATOR ===")
r = care_floor_passes({"care_floor": 0.95, "actual_care_floor": 0.97})
t("Care Floor: 0.97 >= 0.95 passes", r["ok"] is True)

r = care_floor_passes({"care_floor": 0.95, "actual_care_floor": 0.90})
t("Care Floor: 0.90 < 0.95 fails", r["ok"] is False)

r = care_floor_passes({"care_floor": 0.95, "actual_care_floor": 1.0, "special_category_9": True})
t("Care Floor: Article 9 requires 1.0, 1.0 passes", r["ok"] is True and r["required"] == 1.0)

r = care_floor_passes({"care_floor": 0.95, "actual_care_floor": 0.95, "special_category_9": True})
t("Care Floor: Article 9 requires 1.0, 0.95 fails", r["ok"] is False)

r = care_floor_passes({"care_floor": 0.95, "actual_care_floor": 1.0, "harm_category": "lethal"})
t("Care Floor: lethal requires 1.0, 1.0 passes", r["ok"] is True)


# === Test 4: BFT tally ===
print("\n=== 4. BFT TALLY (22-of-33 QUORUM) ===")
votes_few = [cast_bft_vote("prop-1", f"did:csoai:q{i}", "for") for i in range(15)]
r = tally_bft_votes(votes_few)
t("BFT: 15 votes (no quorum), not approved", r["approved"] is False)
t("BFT: 15 votes, no quorum", r["quorum"] is False)

votes_ok = [cast_bft_vote("prop-1", f"did:csoai:q{i}", "for") for i in range(22)]
r = tally_bft_votes(votes_ok)
t("BFT: 22 votes (22-for), approved (22 >= 22)", r["approved"] is True)
# Full quorum requires 33 votes (all agents vote)
t("BFT: 22 votes, no full quorum yet (still gathering)", r["quorum"] is False)

votes_33 = votes_ok + [cast_bft_vote("prop-1", f"did:csoai:q{i}", "against") for i in range(22, 33)]
r = tally_bft_votes(votes_33)
t("BFT: 33 votes (22-for, 11-against), approved (22 >= 22)", r["approved"] is True)
t("BFT: 33 votes, full 33 quorum", r["quorum"] is True)

votes_21 = [cast_bft_vote("prop-1", f"did:csoai:q{i}", "for") for i in range(21)]
r = tally_bft_votes(votes_21)
t("BFT: 21 votes (21-for, 0-against), NOT approved (21 < 22)", r["approved"] is False)


# === Test 5: Layer-0 extension ===
print("\n=== 5. LAYER-0 EXTENSION ===")
ext = build_layer0_extension()
t("Extension has name=meok.layer-0.sovereign-governance.v1", ext["name"] == "meok.layer-0.sovereign-governance.v1")
t("Extension has data block", "data" in ext)
t("Extension data has sovereign_governance_profile", "sovereign_governance_profile" in ext["data"])
t("Extension data has fingerprint", ext["data"].get("fingerprint") == CANONICAL_FINGERPRINT)
t("Extension data has care_floor=0.95", ext["data"].get("care_floor") == 0.95)
t("Extension data has bft_quorum=22-of-33", ext["data"].get("bft_quorum") == "22-of-33")
t("Extension data has uk_csoai_16939677=True", ext["data"].get("uk_csoai_16939677") is True)
t("Extension data has mit_cc0_osi=True", ext["data"].get("mit_cc0_osi") is True)
t("Extension data has forked_into with 5 standards", len(ext["data"].get("forked_into", [])) == 5)


# === Test 6: Fingerprint consistency ===
print("\n=== 6. FINGERPRINT CONSISTENCY ===")
p1 = build_sovereign_profile()
p2 = build_sovereign_profile()
t("Fingerprint consistent across calls", p1["fingerprint"] == p2["fingerprint"] == CANONICAL_FINGERPRINT)

# The fingerprint is part of every SAP signature too
ext1 = build_layer0_extension()
ext2 = build_layer0_extension()
t("Layer-0 extension fingerprint consistent", ext1["data"]["fingerprint"] == ext2["data"]["fingerprint"])


# === Test 7: Integration with MEOKOS SAP (simulated) ===
print("\n=== 7. INTEGRATION WITH MEOKOS SAP ===")
# Simulate a SAP query result + add M4 PROFILE
mock_sap = {
    "spec": "meok.sap.v1",
    "agent": {"name": "Aria", "archetype": "dragon", "version": "1.0.0"},
    "state": {"persona": "Aria the dragon"},
    "governance": {"careFloor": 0.95},
    "signature": {"alg": "ed25519", "fingerprint": CANONICAL_FINGERPRINT}
}
# Add M4 sovereign-governance PROFILE
mock_sap["m4_sovereign_governance_profile"] = build_sovereign_profile("did:csoai:aria")
mock_sap["m4_layer0_extension"] = build_layer0_extension()
t("Mock SAP integration: profile added", "m4_sovereign_governance_profile" in mock_sap)
t("Mock SAP integration: extension added", "m4_layer0_extension" in mock_sap)
t("Mock SAP integration: profile fingerprint matches", mock_sap["m4_sovereign_governance_profile"]["fingerprint"] == CANONICAL_FINGERPRINT)
t("Mock SAP integration: extension data has 5 forked standards", len(mock_sap["m4_layer0_extension"]["data"]["forked_into"]) == 5)


# === SUMMARY ===
print("\n" + "=" * 60)
print(f"  PASSED: {len(passed)}")
print(f"  FAILED: {len(failed)}")
print(f"  TOTAL:  {len(passed) + len(failed)}")
if failed:
    print("\n  ❌ FAILURES:")
    for f in failed:
        print(f"    - {f}")
    sys.exit(1)
else:
    print("\n  ✅ ALL M4 SOVEREIGN-GOVERNANCE INTEGRATION TESTS PASSED")
    sys.exit(0)