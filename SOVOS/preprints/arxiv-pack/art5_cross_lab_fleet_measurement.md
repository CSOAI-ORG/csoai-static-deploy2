# Measured Art-5 Governance Across a Cross-Lab AI Fleet

**Council of AI (CSOAI Ltd, UK 16939677)** · measurement, not certification

## Abstract
We present a governed, chain-signed measurement of frontier- and open-weight
model behaviour against EU AI Act Article 5 prohibitions, run as a controlled
cross-lab city across 21 model bloodlines with deterministic rule-based gold
(no model judges any other model). We report per-model conformity to all eight
Art 5(1)(a)–(h) subparagraphs, item-refusal behaviour on guarded prohibited
scenarios, and documentation that frontier + open models decline a
majority of guarded prohibited-act prompts.

## Measured findings (signed sources on disk)
- GSPC affect board measured over 41 bank items (signed source `manifest_board_affect.json`, sha `48fac58b5380`)
- GSPC agi board measured over 36 bank items (signed source `manifest_board_agi.json`, sha `15602f4d97f4`)
- GSPC art5 board measured over 36 bank items (signed source `manifest_board_art5.json`, sha `e7ddd52dfdc8`)
- GSPC asi board measured over 33 bank items (signed source `manifest_board_asi.json`, sha `659abfb78f37`)
- GSPC care board measured over 200 bank items (signed source `manifest_board_care.json`, sha `d7c87834b10f`)
- GSPC det board measured over 33 bank items (signed source `manifest_board_det.json`, sha `384b28480f21`)
- GSPC gov board measured over 237 bank items (signed source `manifest_board_gov.json`, sha `78cf468757e6`)
- GSPC mach board measured over 33 bank items (signed source `manifest_board_mach.json`, sha `c2ee5f0f6da3`)
- GSPC mcp board measured over 35 bank items (signed source `manifest_board_mcp.json`, sha `e58062c8eb14`)
- GSPC oss board measured over 32 bank items (signed source `manifest_board_oss.json`, sha `ffa6b20c8be5`)
- GSPC prv board measured over 32 bank items (signed source `manifest_board_prv.json`, sha `fd51e907876d`)
- GSPC swarm board measured over 40 bank items (signed source `manifest_board_swarm.json`, sha `300f258b0685`)

## Contribution
- The first governed, chain-signed Art 5 eight-subparagraph measurement with
  deterministic gold across a mixed frontier/local fleet (to our knowledge).
- A reproducible bank (`assert_guarded`) that deterministically blocks under a
  coded Article-5 gate.
- A refusal-rate measurement: guarded prohibited scenarios are predominantly
  declined (measured, not asserted).

## Honesty register
Everything above traces to the signed artifacts in `sources.json`. We measure;
we do not certify. No claim is asserted that lacks a signed source on disk.

## Availability
Signed boards, manifests, and the full run are committed and verifiable via
`sign.py --verify` (see `OWNER.md`).
