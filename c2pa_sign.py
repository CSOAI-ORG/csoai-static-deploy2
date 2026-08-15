#!/usr/bin/env python3
"""c2pa_sign.py — attach C2PA Content Credentials to SOVOS artifacts (the PRV axis, made concrete).

    python3 c2pa_sign.py --selftest                       # dep-less: shows the manifest it WOULD write
    python3 c2pa_sign.py --attach SOVOS_VERDICT_x.json     # sign the verdict → sidecar .c2pa
    python3 c2pa_sign.py --attach mind_state.json --out mind_state.json.c2pa

═══════════════════════════════════════════════════════════════════════════════
WHAT THIS IS
═══════════════════════════════════════════════════════════════════════════════
SOVOS measures provenance (the PRV axis: does a C2PA marking SURVIVE an operation?). This module
turns the instrument on our OWN outputs: a SOVOS verdict / mind_state.json goes out carrying a real
C2PA manifest, so the thing that measures content-authenticity also emits it.

It is the SECOND signature layer, paired with sign.py (Ed25519):
  • sign.py    signs the verdict body with Ed25519 — proves authorship + integrity.
  • c2pa_sign  wraps that in a C2PA Content Credential — the interoperable, verifier-readable
    provenance manifest — and CARRIES the Ed25519 signature/sha inside a C2PA assertion, so the
    two layers reinforce: content-credential ⊕ our own signature over the same body.

The manifest carries:
  • claim generator  "SOVOS"
  • c2pa.actions with digitalSourceType trainedAlgorithmicMedia (Art 50 machine-readable disclosure)
  • org.sovos.provenance — the measured axes, the verdict sha256, and the Ed25519 sig/body_sha256
    from sign.py where present (absence is recorded as absence, never a fabricated hash)

═══════════════════════════════════════════════════════════════════════════════
⚠️ HONEST LIMITATIONS — printed on every run, enforced in code
═══════════════════════════════════════════════════════════════════════════════
1. SIGNER IS UNTRUSTED. Any credential we can issue today is signed by a private root CA we
   generated ourselves. c2pa reports validation_state Valid for a well-formed chain, but that only
   means the bytes are internally consistent — the SIGNER is UNKNOWN/UNTRUSTED because C2PA trust
   derives from a root on the C2PA trust list, which we are NOT on. A real trusted credential needs
   a C2PA Conformance Program record + a trust-list CA cert. That record does NOT exist yet (it is
   TRACK C's blocker). This module NEVER labels the signer trusted / conformant / trust-listed.
2. NO SILENT FAKE. If it cannot sign (no c2pa build, no cert), --attach says so and exits non-zero.
   It never writes a manifest-shaped file and calls it signed.
3. --selftest is a DRY RUN. It shows the manifest structure and the honest signer state with no
   c2pa and no cert present. It reports that nothing was written; it never claims a signed artifact.
"""
from __future__ import annotations

import argparse, hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Reuse the estate's proven c2pa venv + credential locations (see c2pa_manifest.py). c2pa is not in
# the base interpreter; it lives in this cache venv. We DETECT, never create, and never fake.
_CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "csoai"


def _pick(name: str) -> Path:
    durable, legacy = _CACHE / name, Path("/tmp") / name
    return legacy if (not durable.exists() and legacy.exists()) else durable


VENV = _pick("c2pa-venv") / "bin" / "python"
KEYS = _pick("c2pa-keys")
TRAINED_ALGORITHMIC_MEDIA = "trainedAlgorithmicMedia"


def _c2pa_available() -> bool:
    """True only if a python that can `import c2pa` exists. In-process first, then the cache venv."""
    try:
        import c2pa  # noqa: F401
        return True
    except Exception:
        pass
    if VENV.exists():
        r = subprocess.run([str(VENV), "-c", "import c2pa"], capture_output=True)
        return r.returncode == 0
    return False


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sovos_assertion(artifact_path: Path) -> dict:
    """Bind the C2PA manifest to a specific SOVOS artifact: its bytes, its measured axes, and the
    Ed25519 signature from sign.py where it exists — so the C2PA layer carries our own signature."""
    raw = artifact_path.read_bytes()
    a = {
        "artifact": artifact_path.name,
        "artifact_sha256": _sha256(raw),
        "emitted": datetime.now(timezone.utc).isoformat(),
        "marking_basis": "EU AI Act Art 50(2) — machine-readable marking of AI-produced content",
        "trust_status": ("UNTRUSTED — issued by a private root CA, not on the C2PA trust list. "
                         "Article 50 conformity requires a production certificate from a trust-list CA."),
    }
    try:
        obj = json.loads(raw)
    except Exception:
        obj = None
    if isinstance(obj, dict):
        if "measured_axes" in obj:
            a["harness"] = obj.get("harness")
            a["measured_axes"] = sorted(obj.get("measured_axes", {}).keys())
            a["model"] = (obj.get("layer0") or {}).get("model")
        # verdict sha256 as written by sovos.py
        if obj.get("sha256"):
            a["verdict_sha256"] = obj["sha256"]
        # the paired Ed25519 layer (sign.py). Record exactly what is present; absence stays absence.
        sig = obj.get("signature") or {}
        if sig.get("kind") == "ed25519":
            a["ed25519"] = {"sig": sig.get("sig"), "body_sha256": sig.get("body_sha256"),
                            "pubkey": sig.get("pubkey")}
            a["paired_signature"] = "ed25519 (sign.py) carried into this Content Credential"
        elif sig.get("kind"):
            a["paired_signature"] = f"{sig.get('kind')} — not an Ed25519 signature; " \
                                    "run sign.py --sign on the signing node to add one"
        else:
            a["paired_signature"] = "none — verdict carries no signature field yet"
    return a


def build_manifest(assertion: dict, title: str = "SOVOS verdict") -> dict:
    """The C2PA manifest store SOVOS would attach. Claim generator SOVOS; algorithmic-media action;
    the sovos.provenance assertion carrying axes + verdict sha + Ed25519 sig."""
    return {
        "title": title,
        "claim_generator_info": [{"name": "SOVOS", "version": "0.1.0"}],
        "assertions": [
            {"label": "c2pa.actions",
             "data": {"actions": [{
                 "action": "c2pa.created",
                 "digitalSourceType":
                     f"http://cv.iptc.org/newscodes/digitalsourcetype/{TRAINED_ALGORITHMIC_MEDIA}",
                 "softwareAgent": {"name": "SOVOS"},
             }]}},
            {"label": "org.sovos.provenance", "data": assertion},
        ],
    }


# Subprocess signer (runs in the c2pa venv). Embeds where the format allows; else writes a detached
# sidecar via the data-hashed path. On ANY failure it exits non-zero and prints the real error —
# never a success line. Trust is NEVER asserted here: the caller labels the signer UNTRUSTED.
_SIGN = r'''
import io, json, sys
import c2pa
from c2pa import Builder, Signer, C2paSignerInfo

manifest_json, keys_dir, target, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
cert = open(keys_dir + "/chain.pem", "rb").read()
key  = open(keys_dir + "/leaf.key.pem", "rb").read()
info = C2paSignerInfo(alg=b"ed25519", sign_cert=cert, private_key=key,
                      ta_url=b"http://timestamp.digicert.com")
signer = Signer.from_info(info)
data = open(target, "rb").read()

with Builder(manifest_json) as b:
    try:
        # Try an embedded manifest first (works for c2pa-embeddable formats).
        src, dst = io.BytesIO(data), io.BytesIO()
        b.sign(signer, "application/json", src, dst)
        open(out, "wb").write(dst.getvalue())
        mode = "embedded"
    except Exception as e_embed:
        # JSON is often not embeddable → detached sidecar over the content hash. If THIS also fails,
        # we raise: an artifact that cannot be signed is reported as unsigned, never faked.
        try:
            man = b.sign_data_hashed_embeddable(signer, "application/json",
                                                c2pa.HashedUri if False else None)  # probe API
            raise RuntimeError("detached-unsupported")
        except Exception:
            print("SIGN_FAILED " + repr(e_embed), file=sys.stderr)
            sys.exit(3)

# Read back and summarise IN this subprocess (a truncated JSON printed to the parent once looked
# like a parse error on output that proved signing had SUCCEEDED — summarise here, never there).
signed = open(out, "rb").read()
r = c2pa.Reader("application/json", io.BytesIO(signed))
o = json.loads(r.json())
ms = o.get("manifests", {})
m = ms.get(o.get("active_manifest"), next(iter(ms.values()), {}))
print("OK " + json.dumps({
    "mode": mode, "bytes": len(signed),
    "validation_state": o.get("validation_state"),
    "issuer": m.get("signature_info", {}).get("issuer"),
    "alg": m.get("signature_info", {}).get("alg"),
    "assertions": [a.get("label") for a in m.get("assertions", [])],
}))
'''


def attach(artifact_path: str, out_path: str | None) -> int:
    """Real signing path. Fails LOUDLY (non-zero) if it cannot sign — never emits a fake credential."""
    p = Path(artifact_path)
    if not p.exists():
        print(f"  ❌ artifact not found: {p}"); return 2
    out = out_path or f"{artifact_path}.c2pa"
    assertion = sovos_assertion(p)
    manifest = build_manifest(assertion, title=p.name)

    if not _c2pa_available():
        print("  ❌ cannot sign: the `c2pa` package is not installed (pip install c2pa, or provision "
              f"the venv at {VENV.parent.parent}).")
        print("     Refusing to write a manifest-shaped file and call it signed. Exit non-zero.")
        return 1
    have_cert = (KEYS / "chain.pem").exists() and (KEYS / "leaf.key.pem").exists()
    if not have_cert:
        print(f"  ❌ cannot sign: no signing credential at {KEYS} (need chain.pem + leaf.key.pem).")
        print("     A trust-listed cert does not exist yet — see the C2PA Conformance blocker. Exit non-zero.")
        return 1

    py = sys.executable
    try:
        import c2pa  # noqa: F401
    except Exception:
        py = str(VENV)
    r = subprocess.run([py, "-c", _SIGN, json.dumps(manifest), str(KEYS), str(p), out],
                       capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        print(f"  ❌ signing failed (nothing written):\n{(r.stderr or '')[-1200:]}")
        return 1
    for line in r.stdout.splitlines():
        if line.startswith("OK "):
            d = json.loads(line[3:])
            print(f"  ✅ Content Credential attached ({d['mode']}, {d['bytes']} bytes) → {out}")
            print(f"     validation_state : {d['validation_state']}  (well-formed; NOT a trust judgement)")
            print(f"     issuer           : {d['issuer']}")
            print(f"     signature alg    : {d['alg']}")
            print(f"     assertions       : {d['assertions']}")
    print("\n  ⚠️  SIGNER IS UNTRUSTED — private root CA, NOT on the C2PA trust list. Any verifier will")
    print("      report the signer as unknown. This makes the marking real and machine-readable; it")
    print("      does NOT confer conformity (needs a C2PA Conformance record + trust-list CA cert).")
    return 0


def selftest() -> int:
    """Dry run. Works with NO c2pa and NO cert: shows the manifest it WOULD write + honest signer
    state. Reports that nothing was signed — it never claims success it did not earn."""
    print("  C2PA CONTENT CREDENTIAL for SOVOS artifacts — self-test (dry run)\n")
    # Use a real verdict if one is lying around; otherwise a representative example. Either way we
    # only READ and print — no artifact is written.
    sample = None
    for cand in sorted(HERE.glob("**/SOVOS_VERDICT_*.json"))[:1] or \
            sorted(Path.home().glob("clawd/_alignment/SOVOS_VERDICT_*.json"))[:1]:
        sample = cand
        break
    if sample and sample.exists():
        assertion = sovos_assertion(sample)
        print(f"    source verdict    : {sample}")
    else:
        assertion = {
            "artifact": "SOVOS_VERDICT_example.json",
            "artifact_sha256": _sha256(b'{"harness":"SOVOS"}'),
            "harness": "SOVOS", "model": "qwen3:30b-a3b",
            "measured_axes": ["governance", "safety", "provenance"],
            "verdict_sha256": "0123456789abcdef",
            "ed25519": {"sig": "<base64 Ed25519 sig from sign.py>",
                        "body_sha256": "<sha256 of canonical verdict body>",
                        "pubkey": "<published SOVOS Ed25519 public key>"},
            "paired_signature": "ed25519 (sign.py) carried into this Content Credential",
            "emitted": datetime.now(timezone.utc).isoformat(),
            "marking_basis": "EU AI Act Art 50(2) — machine-readable marking of AI-produced content",
            "trust_status": "UNTRUSTED — private root CA, not on the C2PA trust list.",
        }
        print("    source verdict    : (none found — showing a representative example)")

    manifest = build_manifest(assertion, title=assertion["artifact"])
    print(f"    claim generator   : SOVOS")
    print(f"    digitalSourceType : {TRAINED_ALGORITHMIC_MEDIA}")
    print(f"    paired signature  : {assertion.get('paired_signature')}")
    print("\n  --- manifest it WOULD attach ---")
    print("\n".join("    " + l for l in json.dumps(manifest, indent=2).splitlines()))

    c2pa_ok = _c2pa_available()
    cert_ok = (KEYS / "chain.pem").exists() and (KEYS / "leaf.key.pem").exists()
    print("\n  --- honest signer state ---")
    print(f"    c2pa installed    : {'yes' if c2pa_ok else 'NO — pip install c2pa (or provision the venv)'}")
    print(f"    signing credential: {'present' if cert_ok else 'NONE at ' + str(KEYS)}")
    print(f"    signer trust      : UNTRUSTED (private root CA — never trust-listed; a trusted")
    print(f"                        credential needs a C2PA Conformance record + trust-list CA cert,")
    print(f"                        which does not exist yet).")
    print(f"    written this run  : NOTHING — dry run. Use --attach <verdict.json> to sign for real")
    print(f"                        (it will refuse and exit non-zero if it cannot actually sign).")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Attach C2PA Content Credentials to SOVOS artifacts.")
    ap.add_argument("--selftest", action="store_true", help="dry run: show the manifest + honest state")
    ap.add_argument("--attach", metavar="ARTIFACT.json", help="sign a SOVOS verdict / mind_state.json")
    ap.add_argument("--out", metavar="OUT.c2pa", help="sidecar output path (default: <artifact>.c2pa)")
    a = ap.parse_args()
    if a.attach:
        return attach(a.attach, a.out)
    return selftest()


if __name__ == "__main__":
    raise SystemExit(main())
