#!/usr/bin/env python3
"""build_sublimb_index.py — content-hash Article 5(1)(a)-(h) individually.

CLOSES a limitation the published bundle names about itself:

    "The provision snapshot is ARTICLE-level; Art 5(1) sub-limbs are named in prose,
     not hashed."   -- publish/gspc-open-artifacts/MANIFEST.json

Why it matters: ORPA's whole novelty claim is that an item anchors to a provision whose text
a reader can verify unchanged. Anchoring to "Article 5" when the item turns on Article 5(1)(c)
means a reader verifies 11,580 characters to check a 729-character claim, and an amendment to
5(1)(a) invalidates the hash for an item that never depended on it. Sub-limb hashes make the
anchor as narrow as the claim.

ADDITIVE BY DESIGN. This writes a SEPARATE index and does NOT touch manifest.json,
provisions.json, or the snapshot files. Recomputing `set_manifest_hash` would mint a new
`set_id`, and `SNAPSET-EU-AI-ACT-202608-ea843ecb` is referenced by other lanes and by every
artifact already published. An index that composes with the signed set is correct here; a
rewrite of the signed set is a decision for its owner, not a side effect of adding hashes.

Each entry carries the PARENT article's hash as well, so the chain is:

    sub-limb text -> sub_limb_sha256
                  -> parent_file_sha256 (must equal manifest.json's recorded hash)
                  -> set_id
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from grounding_retrieval import ART5, SNAP  # noqa: E402

MANIFEST = SNAP / "manifest.json"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main():
    man = json.loads(MANIFEST.read_text())
    art5_entry = next(s for s in man["snapshots"] if s["file"] == "art05.txt")
    art5_bytes = (SNAP / "art05.txt").read_bytes()

    # VERIFY THE PARENT BEFORE HASHING ITS PARTS. A sub-limb hash chained to an article whose
    # own hash no longer matches the manifest is worse than no hash: it looks verified.
    actual = sha(art5_bytes)
    if actual != art5_entry["sha256"]:
        sys.exit(f"REFUSING: art05.txt hash {actual[:12]} != manifest {art5_entry['sha256'][:12]}. "
                 f"The parent is not the text the manifest signed; sub-limb hashes would be "
                 f"chained to nothing.")

    entries = []
    for letter, text in sorted(ART5.items()):
        # Hash the exact substring, normalised only by the strip() the splitter already applied.
        # Recorded verbatim so a verifier reproduces it without guessing a normalisation.
        b = text.encode("utf-8")
        entries.append({
            "sub_provision_id": f"eu-ai-act:art5(1)({letter})",
            "parent_provision_id": art5_entry["provision_id"],
            "parent_file": "art05.txt",
            "parent_file_sha256": art5_entry["sha256"],
            "parent_snapshot_id": art5_entry["snapshot_id"],
            "chars": len(text),
            "sub_limb_sha256": sha(b),
            "first_80_chars": text[:80],
        })

    idx = {
        "index": "EU AI Act Article 5(1) sub-limb content hashes",
        "version": "v0.1.0",
        "built_at": datetime.now(timezone.utc).isoformat(),
        "set_id": man["set_id"],
        "additive": ("this index does NOT modify manifest.json, provisions.json or any snapshot "
                     "file, and does NOT change set_id. It composes with the signed set."),
        "extraction_rule": ("Article 5(1) is split on markers of the form '- (x)' where x is the "
                            "SUCCESSOR letter of the current sub-limb, capped at (h). Roman-numeral "
                            "sub-points — 5(1)(c)(i) and the 5(1)(h)(i)-(iii) law-enforcement "
                            "exceptions — are retained INSIDE their parent limb rather than "
                            "promoted, because a letter-blind split invents a non-existent "
                            "Article 5(1)(i) and detaches conditions from the rule they qualify."),
        "verification": ("recompute: split art05.txt by extraction_rule, utf-8 encode each limb "
                         "verbatim, sha256. parent_file_sha256 must equal manifest.json's entry "
                         "for art05.txt, which this build verified before emitting."),
        "sub_limbs": entries,
    }
    out = HERE / "publish/gspc-open-artifacts/art5-sublimb-hashes-v0.1.0.json"
    out.write_text(json.dumps(idx, indent=2))

    print(f"parent art05.txt verified against manifest: {actual[:16]}")
    print(f"set_id: {man['set_id']}  (unchanged — index is additive)\n")
    for e in entries:
        print(f"  {e['sub_provision_id']:24s} {e['chars']:5d} chars  "
              f"{e['sub_limb_sha256'][:16]}")
    print(f"\n  {len(entries)} sub-limbs -> {out}")


if __name__ == "__main__":
    main()
