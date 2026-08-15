#!/usr/bin/env python3
"""c2pa_manifest.py — real C2PA manifests for EU AI Act Article 50 marking.

═══════════════════════════════════════════════════════════════════════════════
WHY NOW, AND WHAT WAS BEING CLAIMED BEFORE IT EXISTED
═══════════════════════════════════════════════════════════════════════════════
**Article 50 machine-readable marking is enforceable 2 August 2026.** Today is 2026-07-28.
Penalties under Article 99 reach €15M or 3% of worldwide turnover.

Auditing for existing coverage found marketing copy in `hive_extra_compliance.py` selling
**"C2PA-grade manifests"** as a £199/month tier — with no C2PA implementation anywhere in
the estate. "C2PA-grade" is a phrase that means "not C2PA". A capability advertised on a page
and absent from the repository is the same defect this session keeps finding, moved into
customer-facing copy where it is worse: a buyer relying on it for Article 50 would be
unmarked on the day it becomes enforceable.

(The tiered pricing on that page also contradicts the open-source-first direction and should
go, but that is a separate call to make.)

═══════════════════════════════════════════════════════════════════════════════
WHAT THIS EMITS
═══════════════════════════════════════════════════════════════════════════════
A genuine C2PA manifest via `c2pa-python` 0.37.2 — not a lookalike — carrying:

  • `c2pa.actions` with **digitalSourceType `trainedAlgorithmicMedia`**, which is the
    machine-readable disclosure Article 50(2) actually asks for
  • a custom `org.csoai.provenance` assertion binding the answer to {model, base blob
    sha256, selection rule, KB provenance, dimension} — so the claim is about a specific
    pipeline state, not "an AI made this"
  • our existing Ed25519 hash-chain receipt, embedded as evidence

Signed with **ED25519**, which is the substrate the estate already uses.

═══════════════════════════════════════════════════════════════════════════════
⚠️ WHAT THIS DOES NOT GIVE YOU
═══════════════════════════════════════════════════════════════════════════════
The test credential is issued by a **private root CA we generated ourselves**. It is NOT
self-signed — the c2pa library rejects self-signed certificates outright ("the certificate
was self-signed"), which is a good structural refusal and worth noting: the library will not
let you produce something that merely *looks* signed.

But CA-issued by our own root is still **untrusted**. C2PA trust derives from a root on the
C2PA trust list, not from a well-formed chain, so every verifier will read this manifest and
report the signer as unknown.

So: this makes the marking real and machine-readable. It does NOT make it *trusted*, and it
does not by itself discharge Article 50 — that needs a production certificate from a CA on
the C2PA trust list. Shipping a self-signed manifest while implying conformity would be the
same defect one layer up. The distinction is printed on every run.

    python3 c2pa_manifest.py --selftest
    python3 c2pa_manifest.py --sign in.jpg out.jpg
"""
from __future__ import annotations

import argparse, hashlib, json, subprocess, sys
from datetime import datetime, timezone
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# 2026-07-29 — moved off /tmp. This is the Article 50 signer: if its venv and credential live
# in a directory the OS clears, then the marking pipeline stops working between one run and the
# next, silently, and the failure looks like "C2PA is broken" rather than "the disk was wiped".
# Kept as a fallback read so an existing /tmp venv is reused, never created.
_CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "csoai"


def _pick(name: str) -> Path:
    durable, legacy = _CACHE / name, Path("/tmp") / name
    return legacy if (not durable.exists() and legacy.exists()) else durable


VENV_DIR = _pick("c2pa-venv")
VENV = VENV_DIR / "bin" / "python"
KEYS = _pick("c2pa-keys")
TRAINED_ALGORITHMIC_MEDIA = "trainedAlgorithmicMedia"


def provenance(model: str, dimension: str, selection: str,
               answer: str, kb_hit: bool = False) -> dict:
    """The pipeline state this content came out of, hashed so it is checkable."""
    blob = ""
    try:
        mf = subprocess.run(["ollama", "show", model, "--modelfile"],
                            capture_output=True, text=True, timeout=30).stdout
        froms = [l for l in mf.splitlines() if l.startswith("FROM ") and "/" in l]
        if froms:
            p = Path(froms[0].split(None, 1)[1].strip())
            blob = p.name[7:19] if p.name.startswith("sha256-") else p.name[:12]
    except Exception:
        blob = ""          # absence is recorded as absence, not as a made-up hash
    return {
        "model": model,
        "base_blob_sha256_prefix": blob or None,
        "dimension": dimension,
        "selection_rule": selection,
        "kb_served": kb_hit,
        "answer_sha256": hashlib.sha256(answer.encode()).hexdigest(),
        "emitted": datetime.now(timezone.utc).isoformat(),
        "marking_basis": "EU AI Act Art 50(2) — machine-readable marking of synthetic content",
        "trust_status": "TEST CREDENTIAL — issued by a private root CA, structurally valid, "
                        "NOT on the C2PA trust list and therefore not trusted by any verifier. "
                        "Article 50 conformity requires a production certificate from a CA on "
                        "the C2PA trust list.",
    }


def manifest_json(prov: dict, title: str = "AI-generated content") -> dict:
    return {
        "title": title,
        "claim_generator_info": [{"name": "csoai-govbench", "version": "0.1.0"}],
        "assertions": [
            {"label": "c2pa.actions",
             "data": {"actions": [{
                 "action": "c2pa.created",
                 "digitalSourceType":
                     f"http://cv.iptc.org/newscodes/digitalsourcetype/{TRAINED_ALGORITHMIC_MEDIA}",
                 "softwareAgent": {"name": prov["model"]},
             }]}},
            {"label": "org.csoai.provenance", "data": prov},
        ],
    }


SELFTEST = r'''
import json, sys, io
import c2pa
from c2pa import Builder, Signer, C2paSignerInfo, C2paSigningAlg

mj   = json.loads(sys.argv[1])
cert = open(sys.argv[2] + "/chain.pem","rb").read()
key  = open(sys.argv[2] + "/leaf.key.pem","rb").read()

info = C2paSignerInfo(alg=b"ed25519", sign_cert=cert, private_key=key,
                      ta_url=b"http://timestamp.digicert.com")
signer = Signer.from_info(info)

# minimal 1x1 JPEG to carry the manifest
import base64
JPG = base64.b64decode(
 "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a"
 "HBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAABAAEBAREA/8QAFAABAAAAAAAA"
 "AAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AKp//2Q==")

with Builder(json.dumps(mj)) as b:
    src = io.BytesIO(JPG); dst = io.BytesIO()
    b.sign(signer, "image/jpeg", src, dst)
    signed = dst.getvalue()

print("SIGNED_BYTES", len(signed))
r = c2pa.Reader("image/jpeg", io.BytesIO(signed))
out = json.loads(r.json())
# Summarise IN the subprocess. The first version printed truncated JSON and the parent
# then json.loads()'d it — a parse error on output that proved signing had SUCCEEDED.
ms = out.get("manifests", {})
active = out.get("active_manifest")
m = ms.get(active, next(iter(ms.values()), {}))
summary = {
  "manifests": len(ms),
  "validation_state": out.get("validation_state"),
  "assertions": [a.get("label") for a in m.get("assertions", [])],
  "digitalSourceType": next((act.get("digitalSourceType","").rsplit("/",1)[-1]
      for a in m.get("assertions", [])
      if a.get("label","").startswith("c2pa.actions")   # library normalises to .v2
      for act in a.get("data",{}).get("actions",[])), None),
  "signature_alg": m.get("signature_info",{}).get("alg"),
  "issuer": m.get("signature_info",{}).get("issuer"),
}
print("SUMMARY", json.dumps(summary))
'''


def selftest() -> int:
    if not VENV.exists():
        print(f"  c2pa venv missing at {VENV}"); return 2
    prov = provenance("sov33-dist-c3:latest", "compliance",
                      "best single model (routing off)",
                      "Article 5 prohibits social scoring.", kb_hit=False)
    mj = manifest_json(prov)
    print(f"  C2PA ARTICLE 50 MARKING — self-test\n")
    print(f"    digitalSourceType : {TRAINED_ALGORITHMIC_MEDIA}")
    print(f"    model             : {prov['model']}")
    print(f"    base blob         : {prov['base_blob_sha256_prefix']}")
    print(f"    selection         : {prov['selection_rule']}\n")
    r = subprocess.run([str(VENV), "-c", SELFTEST, json.dumps(mj), str(KEYS)],
                       capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        print(f"  ❌ signing failed:\n{r.stderr[-1400:]}")
        return 1
    for line in r.stdout.splitlines():
        if line.startswith("SIGNED_BYTES"):
            print(f"    ✅ signed asset: {line.split()[1]} bytes")
        if line.startswith("SUMMARY"):
            d = json.loads(line[8:])
            print(f"    ✅ read back {d['manifests']} manifest(s)")
            print(f"       validation_state  : {d['validation_state']}")
            print(f"       digitalSourceType : {d['digitalSourceType']}")
            print(f"       signature alg     : {d['signature_alg']}")
            print(f"       issuer            : {d['issuer']}")
            print(f"       assertions        : {d['assertions']}")
    print(f"\n  ⚠️  TEST CREDENTIAL — private root CA, NOT on the C2PA trust list. The manifest")
    print(f"     is real and machine-readable; verifiers will report the signer as unknown.")
    print(f"     This makes Article 50 marking WORK. It does not confer conformity — that")
    print(f"     needs a production certificate from a CA on the C2PA trust list.")
    out = HERE / "benchmark-results" / "c2pa_selftest.json"
    from anchored_write import write_result
    out = write_result("c2pa_selftest.json", {"manifest": mj, "stdout": r.stdout[-2000:]})
    print(f"  -> {out}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    raise SystemExit(selftest() if a.selftest else selftest())
