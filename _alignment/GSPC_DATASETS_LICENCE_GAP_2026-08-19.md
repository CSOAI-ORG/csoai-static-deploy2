# GSPC DATASETS LICENCE-GAP — the carder RED wall (2026-08-19)
For K3 (owner of the csoai HF org + the carder convergence, per K3-ALIGNMENT-2026-08-19-PM item #3).

## The finding
All `csoai/gspc-*` datasets served by HF report **no machine-parsed `cardData.license`** (YAML front matter). The canonical carder's licence gate reads ONLY the machine field — body-text licences do NOT count. Hence the RED verdicts (gspc-affect, agi, asi, det, mach, mcp, oss, prv, xr, …). The four flipped GREEN today (gov, care, art5, swarm) = the same fix applied.

## The fix pattern (for the RED remainder)
Add `license: <value>` to each dataset's YAML front matter (HF card metadata), with the value matching the licence declared in the README body text. This lane's contribution: the verified machine-field gap + the recommendation to apply the gov/care/art5/swarm fix pattern to the rest.

## Why it matters
The carder gate is the intake valve for the sim/cross flywheel: RED datasets never enter the commercial bank. Flipping the family GREEN unblocks the estate's own board datasets as carder-clean sources.
