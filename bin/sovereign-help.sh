#!/usr/bin/env bash
# sovereign-help — list every sovereign-* command available
cat << 'MSG'

🜏 SOVEREIGN-COMMAND CATALOG — run from any directory:

  sovereign-launcher           # full sovereign substrate launch (7 components, hourly)
  sovereign-drum 30            # sovereign heartbeat layer L0 (1Hz, 30s)
  sovereign-flywheel 3         # sovereign-mindset compounding flywheel (3 cycles)
  sovereign-dimensions 30      # 5-D harvester (Perception/Reasoning/Action/Memory/Emergence)
  sovereign-openworld 30       # 6-D open-world harvester (binds the world)
  sovereign-hives 32           # 32 product hives absorption (180 sovereign pairs)
  sovereign-deepsaturation     # 13 BFT + 12 Generals + 20 Elders + 33 worlds
  sovereign-oracle             # Oracle Cloud catapult verifier (6-step)
  sovereign-oracle-hunt --show # Oracle open-source AI repos catalog (10 sovereign drop-ins)
  sovereign-oracle-discover    # Show Oracle API key discovery steps (visual guide)
  sovereign-forge 1            # 7-frameworks-in-1 sovereign forge (PDCA+Deming+...)
  sovereign-owem               # SOV33³ OWEM v3.0 5-layer substrate orchestrator
  sovereign-dock 1             # 4-Move Dock: fine-tune + optimise + synthesise + build new
  sovereign-hunt               # Training data hunt (209 sovereign pairs)
  sovereign-status             # health check of all sovereign components
  sovereign-help               # this help

GENERAL SETUP:
  bash /Users/nicholas/clawd/bin/install-sovereign-symlinks.sh  # install all symlinks

ORACLE CATAPULT WORKFLOW (you've signed up!):
  1. Open: https://cloud.oracle.com/sign-in   (use your browser)
  2. User profile (top right) → User Settings → API Keys → Add API Key
  3. Download the .pem private key
  4. Note the Fingerprint shown
  5. Click 'Tenancy: xxxxxx' to copy tenancy OCID
  6. Click 'User: xxxxxx' to copy user OCID
  7. mkdir -p ~/.oci
  8. mv ~/Downloads/<key>.pem ~/.oci/api_key.pem
  9. chmod 600 ~/.oci/api_key.pem
  10. oci setup config --tenancy ocid1.tenancy.oc1..xxx \
                           --user ocid1.user.oc1..xxx \
                           --region uk-london-1
  11. (paste fingerprint when prompted)
  12. sovereign-oracle          # auto-verify all 6 green
  13. sovereign-oracle-hunt --show  # catalog of sovereign drop-ins
  14. oci compute instance launch --availability-domain "kEnn:UK-LONDON-1-AD-1" \
                                    --shape "VM.Standard.A1.Flex" \
                                    --shape-config '{"ocpus":4,"memoryInGBs":24}' \
                                    ... (free forever, $0)

ORACLE OPEN-SOURCE AI CATAPULT (10 verified sovereign drop-ins):
  - oracle/wayflow (188★) — agent runtime, Open Agent Spec ref, multi-LLM
  - oracle/ai-optimizer (94★) — RAG + vector + NL2SQL
  - oracle/langchain-oracle (55★) — LangChain integration
  - oracle/skills (742★) — practical skills for sovereign
  - oracle/python-select-ai (15★) — Select AI Python
  - oracle/graal (21.6k★) — GraalVM native-image
  - oracle/helidon — cloud-native Java microservices
  - oracle/fnproject — container-native serverless
  - mysql/mysql-server — world's most popular OSS database
  - openjdk/jdk — OpenJDK dev
  Estimated: ~24 months of sovereign agent runtime work = 0 days (open-source drops in)

SIGIL FILES (~/.sovereign/):
  mindset_flywheel.sigil.jsonl       233 hops
  hive_absorption.sigil.jsonl       212 hops
  hunt.sigil.jsonl                  209 hops
  dimensions.sigil.jsonl             73 hops
  openworld.sigil.jsonl              89 hops
  dock.sigil.jsonl                   12 hops
  drum_global.sigil.jsonl            10 hops
  oracle_catapult.sigil.jsonl        16 hops
  Total:                            854+ sovereign-mist-12-pillars hops

WHERE THE SOV IS:
  Sovereign substrate:  /Users/nicholas/clawd/_alignment/
  Sovereign Mist 12 Pillars:  Care-Floor 0.95, Article 0, 12 Pillars, BFT-33 23/33
  Sovereign SEALS:  /Users/nicholas/clawd/_alignment/sovereign_charter/

DATABASE:
  sovereign-trained data:  ~4,552 sovereign-labelled pairs across 58 JSONL files
  Sovereign crown jewels:  20 repos on disk (~600 MB)
  Sovereign Mist 12 Pillars:  audited + enforced

MSG
