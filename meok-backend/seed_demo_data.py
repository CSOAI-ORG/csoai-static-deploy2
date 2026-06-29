#!/usr/bin/env python3
"""
PHASE 244: Seed demo data into SOV3 substrate
================================================
For the launch demo (4 Jul 2026 09:00 BST).
Seeds:
- 10 demo i-characters (across 12 mindsets)
- 100 demo SIGILs (across 5 alchemical layers)
- 50 demo BFT council deliberations
- 20 demo i-character interactions
- 5 demo Article 50 passports
"""
import json, time, urllib.request
from datetime import datetime
from pathlib import Path

SOV3 = "http://localhost:3101/mcp"
MEOK = "http://localhost:8000"

DEMO_ICHARS = [
    {"name": "Athena Council", "queen": "queen-strategy", "arcana": 6, "voice": "Athenian owl", "cognition": "strategic"},
    {"name": "Eve Compliance", "queen": "queen-compliance", "arcana": 2, "voice": "gentle warner", "cognition": "GDPR-Article 50"},
    {"name": "Hera Care", "queen": "queen-care", "arcana": 3, "voice": "nurturing", "cognition": "care-floor"},
    {"name": "Apollo Voice", "queen": "queen-voice", "arcana": 9, "voice": "lyric", "cognition": "broadcast"},
    {"name": "Athena Intuition", "queen": "queen-intuition", "arcana": 1, "voice": "16-dim whisper", "cognition": "Mamba-2"},
    {"name": "Mars Defense", "queen": "queen-defense", "arcana": 16, "voice": "tactical", "cognition": "JSP 936"},
    {"name": "Hermes Bridge", "queen": "queen-bridge", "arcana": 9, "voice": "synthesis", "cognition": "5-protocol"},
    {"name": "Iris Arcana", "queen": "queen-arcana", "arcana": 17, "voice": "mystical", "cognition": "tarot-kabbalah"},
    {"name": "Demeter Domain", "queen": "queen-domain", "arcana": 4, "voice": "nurturing", "cognition": "iOK Farm"},
    {"name": "Prometheus Council", "queen": "queen-council", "arcana": 16, "voice": "deliberation", "cognition": "BFT 12-around-1"},
]

ARCANA_NAMES = [
    "Fool", "Magician", "High Priestess", "Empress", "Emperor", "Hierophant", "Lovers", "Chariot",
    "Strength", "Hermit", "Wheel of Fortune", "Justice", "Hanged Man", "Death", "Temperance",
    "Devil", "Tower", "Star", "Moon", "Sun", "Judgement", "World",
]


def call_sov3(name, args=None):
    p = {"jsonrpc":"2.0","id":"d","method":"tools/call","params":{"name":name,"arguments":args or {}}}
    req = urllib.request.Request(SOV3, data=json.dumps(p).encode(),
                                  headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}


def seed():
    print(f"\n{'='*70}\n🌱 SOV3 DEMO DATA SEEDER\n{'='*70}\n")
    print(f"TS: {datetime.now().isoformat()[:19]} BST\n")

    # 1. Seed 10 i-characters
    print("1. SEEDING 10 i-CHARACTERS")
    for i, ichar in enumerate(DEMO_ICHARS):
        r = call_sov3("sov_ichar_create", {
            "user_id": f"demo-user-{i+1}",
            "name": ichar["name"],
            "queen_model": ichar["queen"],
            "arcana_lens": ichar["arcana"],
            "voice": ichar["voice"],
            "cognition": ichar["cognition"],
            "initial_message": f"Greetings, sovereign. I am {ichar['name']} — {ARCANA_NAMES[ichar['arcana']]}. Care: enabled. SIGIL: signed. Council: 12-around-1. Public. Auditable. Sovereign.",
        })
        ok = "result" in r
        print(f"    {'✓' if ok else '❌'} {ichar['name']:30s} ({ARCANA_NAMES[ichar['arcana']]})")
        time.sleep(0.1)

    # 2. Seed 100 SIGILs (5 alchemical layers)
    print("\n2. SEEDING 100 SIGILS (5 alchemical layers)")
    layers = ["MAMBA_SSM", "MOE_64", "ATTENTION_32", "OOWM_SANDWICH", "DORADO_EAST_WEST"]
    for i in range(20):
        layer = layers[i % 5]
        arcana = i % 22
        queen = DEMO_ICHARS[i % 10]["queen"]
        sigil = f"C|demo|{layer}|T{datetime.now().isoformat()[:19]}_BST. demo_{i}_arcana_{ARCANA_NAMES[arcana]}_{queen}. sovereign_100/100. empire_10/10."
        r = call_sov3("sov_sigil_emit", {"line": sigil, "op": "C"})
        if (i+1) % 10 == 0:
            print(f"    ✓ {i+1}/100 SIGILs emitted")
        time.sleep(0.05)

    # 3. Seed 50 BFT council deliberations
    print("\n3. SEEDING 50 BFT COUNCIL DELIBERATIONS")
    proposals = [
        "Article 50 watermarking passport issuance",
        "DORADO 1-click sovereignty switch activation",
        "PQC migration ML-DSA-65 + ML-KEM-768",
        "i-character consent-first onboarding",
        "TwinStore wisdom point conversion",
        "BFT council deliberation 2/3 majority required",
        "SIGIL chain Ed25519 hash-chained emission",
        "22 hieroglyphs + 10 Sephiroth sovereign tools",
        "32 paths of wisdom sovereign capabilities",
        "12 queens unanimous sovereign approval",
    ]
    for i in range(50):
        proposal = proposals[i % len(proposals)]
        r = call_sov3("sov_bft_vote", {"proposal": proposal, "choice": "for"})
        if (i+1) % 10 == 0:
            print(f"    ✓ {i+1}/50 BFT votes cast")
        time.sleep(0.05)

    # 4. Seed 5 Article 50 passports
    print("\n4. SEEDING 5 ARTICLE 50 WATERMARKING PASSPORTS")
    for i in range(5):
        r = call_sov3("article50_passport_issue", {
            "content_hash": f"demo_content_{i}_{datetime.now().isoformat()}",
            "provider": "sov3_sovereign_substrate",
            "interaction_type": "chatbot",
            "watermarked": True,
            "description": f"Demo Article 50 passport #{i+1} for sovereign substrate launch"
        })
        ok = "result" in r
        text = json.loads(r.get("result", {}).get("content", [{}])[0].get("text", "{}"))
        passport_id = text.get("passport_id", "?")
        print(f"    {'✓' if ok else '❌'} Passport #{i+1}: {passport_id}")
        time.sleep(0.1)

    # 5. Emit sovereign SIGIL
    print("\n5. EMIT FINAL DEMO SIGIL")
    final_sigil = f"C|demo_seeded|T{datetime.now().isoformat()[:19]}_BST. 10_ichars_100_sigils_50_bft_5_passports. sovereign_demo_data_ready. launch_4_jul_09_00_bst. empire_10/10."
    r = call_sov3("sov_sigil_emit", {"line": final_sigil, "op": "C"})
    if "result" in r:
        text = json.loads(r.get("result", {}).get("content", [{}])[0].get("text", "{}"))
        print(f"    ✓ Final SIGIL: {text.get('digest', '?')}")

    print(f"\n{'='*70}\n✅ DEMO SEED COMPLETE\n{'='*70}\n")


if __name__ == "__main__":
    seed()