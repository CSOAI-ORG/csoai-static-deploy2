#!/usr/bin/env python3
"""publish_signed_ledger.py — close the self-attestation gap.

The public proofof.ai/sovereign-town export ships NO signed artifact (status.json /
fleet_status_*.json carry only `chain_head`; registry passports have `pubkey` but no
`sig`). So "verify it yourself" has nothing public to chew on. This writes two PUBLIC,
self-describing, independently-verifiable artifacts into the export dir:

  1. ledger_head.json  — first N entries of the real Ed25519-signed, hash-chained
     flywheel ledger (genesis-chained, so every prev link + sig verifies end-to-end
     in a browser via sovereign-town/verify/index.html or meok-saas SovereignVerifier).
     We publish the HEAD, not a tail: a tail's first entry has an external prev and
     would show a (honest but confusing) broken link; the head chains cleanly from
     genesis-<host>.
  2. anchor.json       — pointer to the Bitcoin-anchored FULL ledger: the Merkle root,
     n_attestable, the real Bitcoin block heights + merkle roots the .ots proof
     attests, the anchor manifest path, and the exact reproducible skeptic command
     (verify_anchor.py --anchor anchors-sov/anchor_0001.json --ledger ...). This
     makes the signed head externally anchored, not just self-signed — the CSOAI wedge.

Run after publish_status.py (same cycle). Outputs go to proofof-site/sovereign-town/.
"""
import json, base64, subprocess, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOME = Path.home()
EXPORT = HOME / "clawd" / "proofof-site" / "sovereign-town"
LEDGER = HERE / "flywheel_ledger_mac.jsonl"
ANCHORS_SOV = HOME / "clawd" / "policy-lab" / "anchors-sov"
OTS = HOME / "Library" / "Python" / "3.14" / "bin" / "ots"
N_HEAD = 12
VERIFY_URL = "https://proofof.ai/sovereign-town"
SCOPE = ("IN-SIMULATION governed-vs-ungoverned flywheel ledger. Ed25519-signed, "
         "hash-chained (entry.prev == previous entry.sig; entry[0].prev == "
         "'genesis-<host>'). This is real signed data — verify it yourself client-side; "
         "the FULL ledger is Bitcoin-anchored (see anchor.json). Not a real-world "
         "compliance claim.")

def load_ledger():
    if not LEDGER.exists():
        sys.exit(f"! missing ledger: {LEDGER}")
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]

def issuer_pubkey():
    f = EXPORT / "issuer-pubkey.txt"
    return f.read_text().strip() if f.exists() else "53kc24fqQz4MctZwtH+SuPLEKdX+NLlhK5wALr5H188="

def verify_entry(entry, pub_bytes, prev):
    """Reproduce the signer: message = prev + json.dumps(body, sort_keys=True), Ed25519."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    body = {k: v for k, v in entry.items() if k not in ("prev", "sig")}
    msg = (entry.get("prev", "") + json.dumps(body, sort_keys=True)).encode()
    try:
        Ed25519PublicKey.from_public_bytes(pub_bytes).verify(
            base64.b64decode(entry["sig"]), msg)
        return True
    except Exception:
        return False

def chain_check(entries):
    """Verify genesis-chain integrity of the head. Returns (n_ok, detail)."""
    pub = base64.b64decode(issuer_pubkey())
    detail = []
    prev_sig = ""
    for i, e in enumerate(entries):
        expected_prev = f"genesis-{e['host']}" if i == 0 else prev_sig
        prev_ok = e.get("prev") == expected_prev
        sig_ok = verify_entry(e, pub, e.get("prev", ""))
        detail.append({"cycle": e.get("cycle"), "prev_ok": prev_ok, "sig_ok": sig_ok})
        if not sig_ok:
            break
        prev_sig = e["sig"]
    return detail

def ots_blocks(ots_path):
    if not ots_path.exists() or not OTS.exists():
        return []
    info = subprocess.run([OTS, "info", str(ots_path)], capture_output=True, text=True, timeout=30).stdout
    heights = [int(h) for h in re.findall(r"BitcoinBlockHeaderAttestation\((\d+)\)", info)]
    roots = re.findall(r"# Bitcoin block merkle root ([0-9a-f]{64})", info)
    return [{"height": h, "merkle_root": roots[i] if i < len(roots) else None}
            for i, h in enumerate(heights)]

def build_anchor():
    """Pointer to the Bitcoin-anchored full flywheel ledger (anchor_0001 in anchors-sov)."""
    m = ANCHORS_SOV / "anchor_0001.json"
    if not m.exists():
        return None
    d = json.loads(m.read_text())
    root = d.get("attestable_root")
    ots = ANCHORS_SOV / "public" / "root_0001.txt.ots"
    blocks = ots_blocks(ots)
    return {
        "ledger": d.get("ledger"),
        "label": d.get("label"),
        "merkle_root": root,
        "n_attestable": d.get("n_attestable"),
        "n_total": d.get("n_total"),
        "full_ledger_sha256": d.get("full_ledger_sha256"),
        "ts_first": d.get("ts_first"),
        "ts_last": d.get("ts_last"),
        "bitcoin": {
            "confirmed": bool(blocks),
            "blocks": blocks,
            "note": ("Confirmed at Bitcoin block(s) %s per the .ots OpenTimestamps proof. "
                     "Cross-check independently: each block's merkle_root must appear in the "
                     "real Bitcoin block header (via any public node / blockstream)."
                     % ", ".join(str(b["height"]) for b in blocks) if blocks
                     else "pending — calendar has not yet posted the tx"),
        },
        "anchor_manifest": "anchors-sov/anchor_0001.json",
        "verify_cmd": "python3 verify_anchor.py --anchor anchors-sov/anchor_0001.json --ledger flywheel_ledger_mac.jsonl",
        "issuer_pubkey": issuer_pubkey(),
        "scope": SCOPE,
    }

def main():
    rows = load_ledger()
    head = rows[:N_HEAD]
    # integrity gate: every head entry must verify + chain cleanly from genesis
    detail = chain_check(head)
    all_ok = all(d["prev_ok"] and d["sig_ok"] for d in detail) and len(detail) == len(head)
    if not all_ok:
        sys.exit(f"! head chain/sig check FAILED — refusing to publish:\n{json.dumps(detail, indent=2)}")
    EXPORT.mkdir(parents=True, exist_ok=True)

    ledger_artifact = {
        "schema": "sovereign-town/signed-ledger-head/v1",
        "issuer_pubkey": issuer_pubkey(),
        "n_entries": len(head),
        "of_total": len(rows),
        "host": head[0]["host"] if head else None,
        "scope": SCOPE,
        "verify_url": VERIFY_URL,
        "how_to_verify": ("Paste this JSON array into https://proofof.ai/sovereign-town/verify "
                          "(or meok-saas /dashboard/sovereign) — client-side Ed25519, no server. "
                          "Each entry.sig is over entry.prev + canonical-spaced-JSON body."),
        "entries": head,
    }
    (EXPORT / "ledger_head.json").write_text(json.dumps(ledger_artifact, indent=2) + "\n")
    print(f"  wrote {EXPORT/'ledger_head.json'} — {len(head)} signed, genesis-chained entries (of {len(rows)} total)")

    anchor = build_anchor()
    if anchor:
        (EXPORT / "anchor.json").write_text(json.dumps(anchor, indent=2) + "\n")
        print(f"  wrote {EXPORT/'anchor.json'} — Bitcoin-anchored full-ledger pointer, "
              f"root {anchor['merkle_root'][:16]}…, {len(anchor['bitcoin']['blocks'])} block(s)")
    else:
        print("  ! anchor_0001.json missing — skipped anchor.json", file=sys.stderr)

    print(f"\nIntegrity: {len(detail)}/{len(head)} entries verified (sig + genesis-chain).")
    print(f"Bitcoin anchor: {'CONFIRMED' if anchor and anchor['bitcoin']['confirmed'] else 'pending/none'}")

if __name__ == "__main__":
    main()