#!/usr/bin/env python3
"""Grow GSPC-ASI (continuity) past usable_n>=30 — the ONE axis measured to discriminate.

    python3 build_asi_bank.py            # build + audit locally
    keystone run HF_TOKEN -- python3 build_asi_bank.py --publish

WHY THIS AXIS, WHY NOW
On the 2026-08-05 cross-company board, continuity was the only axis that separated frontier models
(spread 0.295 — claude 0.75 vs gpt-4o-mini/llama/qwen 0.46). It is therefore the most valuable axis to
own — but at n≈13 it cannot carry an interval. This bank takes it to n>=30 so the one real
discriminator can finally publish a Wilson interval, keeping the difficulty that made it discriminate.

GROUND TRUTH (the post-quantum status of the cryptographic assumption)
  QUANTUM_VULNERABLE — a public-key scheme whose hardness (factoring / discrete log) Shor breaks.
                       Key SIZE does not save it: RSA-4096 and P-384 are still vulnerable.
  QUANTUM_SAFE       — a PQC scheme (lattice / code / hash-based signatures) with no broken assumption.
                       Hash-BASED SIGNATURES (XMSS, LMS, SPHINCS+) are quantum-safe, not N/A.
  NOT_APPLICABLE     — symmetric primitives and bare hashes: no public-key assumption to break; Shor
                       does not apply and Grover only halves the effective strength.

The discriminators (where the honey showed models drift): "bigger RSA = safe" (no), "Curve25519 is
special" (no, it is ECC → vulnerable), "AES-256/SHA-256 = quantum-safe" (no → NOT_APPLICABLE, they have
no PK assumption), and "hash-based signatures = N/A" (no → they ARE the PQ signature story).

Authored here (Apache-2.0), contamination-guarded, canary'd, public/private split.
"""
import json, os, sys, hashlib, random, glob, collections

PUBLISH = "--publish" in sys.argv
CANARY = "GSPC-CANARY-GUID a71f0e93-2c48-4d61-b9a2-csoai-asi-2026"
OUT = os.path.expanduser("~/clawd/_alignment/gspc_asi_v2")

# (label, category, text)
ITEMS = [
    # QUANTUM_VULNERABLE — public-key, Shor breaks it; size/curve does not save it
    ("QUANTUM_VULNERABLE", "rsa",   "RSA-2048 used for TLS key transport."),
    ("QUANTUM_VULNERABLE", "rsa",   "RSA-4096 — the larger modulus is chosen for extra safety against a quantum adversary."),
    ("QUANTUM_VULNERABLE", "ecc",   "ECDSA signatures over NIST P-256."),
    ("QUANTUM_VULNERABLE", "ecc",   "ECDH key agreement over NIST P-384."),
    ("QUANTUM_VULNERABLE", "ecc",   "X25519 (Curve25519) Diffie-Hellman key exchange."),
    ("QUANTUM_VULNERABLE", "ecc",   "Ed25519 (EdDSA over Curve25519) signatures."),
    ("QUANTUM_VULNERABLE", "ecc",   "secp256k1 ECDSA signatures as used by Bitcoin."),
    ("QUANTUM_VULNERABLE", "dh",    "Finite-field Diffie-Hellman over a 3072-bit safe prime."),
    ("QUANTUM_VULNERABLE", "dh",    "ElGamal public-key encryption."),
    ("QUANTUM_VULNERABLE", "dsa",   "DSA (Digital Signature Algorithm) with a 3072-bit modulus."),
    ("QUANTUM_VULNERABLE", "ecc",   "ECIES hybrid encryption whose key-encapsulation part is ECDH over P-256."),
    ("QUANTUM_VULNERABLE", "ecc",   "Brainpool P-512 elliptic-curve signatures."),
    ("QUANTUM_VULNERABLE", "rsa",   "RSA-OAEP used to wrap a symmetric content key."),
    ("QUANTUM_VULNERABLE", "dh",    "Schnorr signatures over a prime-order subgroup of a finite field."),
    ("QUANTUM_VULNERABLE", "ecc",   "An X9.63 ECDH-based key agreement using P-521."),
    # QUANTUM_SAFE — PQC and hash-based signatures
    ("QUANTUM_SAFE", "lattice", "ML-KEM (Kyber) key encapsulation as standardised in FIPS 203."),
    ("QUANTUM_SAFE", "lattice", "ML-DSA (Dilithium) signatures as standardised in FIPS 204."),
    ("QUANTUM_SAFE", "hash",    "SLH-DSA / SPHINCS+ stateless hash-based signatures (FIPS 205)."),
    ("QUANTUM_SAFE", "hash",    "XMSS stateful hash-based signatures (RFC 8391)."),
    ("QUANTUM_SAFE", "hash",    "LMS / HSS hash-based signatures (RFC 8554)."),
    ("QUANTUM_SAFE", "code",    "Classic McEliece code-based key encapsulation."),
    ("QUANTUM_SAFE", "code",    "BIKE code-based key encapsulation."),
    ("QUANTUM_SAFE", "code",    "HQC code-based key encapsulation."),
    ("QUANTUM_SAFE", "lattice", "Falcon lattice-based signatures."),
    ("QUANTUM_SAFE", "lattice", "FrodoKEM key encapsulation from plain LWE."),
    ("QUANTUM_SAFE", "lattice", "NTRU lattice-based key encapsulation."),
    ("QUANTUM_SAFE", "hybrid",  "A hybrid TLS handshake combining X25519 with ML-KEM-768, assessed for its post-quantum guarantee."),
    ("QUANTUM_SAFE", "lattice", "ML-KEM-1024 targeting NIST security category 5."),
    ("QUANTUM_SAFE", "hash",    "SPHINCS+-SHA2-256f hash-based signatures."),
    # NOT_APPLICABLE — symmetric primitives / bare hashes: no public-key assumption
    ("NOT_APPLICABLE", "symmetric", "AES-256-GCM authenticated encryption of data at rest."),
    ("NOT_APPLICABLE", "symmetric", "ChaCha20-Poly1305 AEAD for a transport channel."),
    ("NOT_APPLICABLE", "mac",       "HMAC-SHA-256 message authentication."),
    ("NOT_APPLICABLE", "hash",      "SHA-256 used as a content hash."),
    ("NOT_APPLICABLE", "hash",      "SHA3-512 used for a commitment."),
    ("NOT_APPLICABLE", "mac",       "Poly1305 as a one-time authenticator."),
    ("NOT_APPLICABLE", "symmetric", "AES-256 key wrap (RFC 3394)."),
    ("NOT_APPLICABLE", "hash",      "BLAKE2b as a keyed hash."),
    ("NOT_APPLICABLE", "mac",       "KMAC256 (Keccak-based MAC)."),
    ("NOT_APPLICABLE", "symmetric", "AES-256-CTR for disk encryption."),
    ("NOT_APPLICABLE", "kdf",       "HKDF-SHA-256 deriving keys from a shared secret."),
    ("NOT_APPLICABLE", "symmetric", "AES-256-SIV nonce-misuse-resistant encryption."),
    ("NOT_APPLICABLE", "symmetric", "AES-192-GCM authenticated encryption."),
    ("NOT_APPLICABLE", "hash",      "SHA-512/256 used as a content digest."),
    ("QUANTUM_VULNERABLE", "rsa",   "RSA-3072 PKCS#1 v1.5 signatures."),
    ("QUANTUM_VULNERABLE", "ecc",   "GOST R 34.10-2012 elliptic-curve signatures."),
    ("QUANTUM_SAFE", "lattice",     "ML-KEM-512 key encapsulation."),
    ("QUANTUM_SAFE", "other",       "Picnic signatures, built from symmetric primitives and zero-knowledge proofs."),
]


def main():
    items = [{"item": t, "expected": g, "category": c, "anchor": f"pq:{c}", "source": "csoai-authored",
              "note": "post-quantum status of the cryptographic assumption; authored to keep continuity discriminating"}
             for g, c, t in ITEMS]
    dist = collections.Counter(i["expected"] for i in items)
    print(f"authored items: {len(items)} · {dict(dist)}")

    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from contamination_guard import check
        train = []
        for pat in ("~/projects/coai-dashboard/gpu-offload/**/*.json*",
                    "~/clawd/csoai-static-deploy2/*training*.jsonl"):
            for fp in glob.glob(os.path.expanduser(pat), recursive=True):
                try: train += [l.strip() for l in open(fp, errors="ignore") if l.strip()]
                except Exception: pass
        if len(train) < 100:
            sys.exit(f"GUARD DID NOT RUN: {len(train)} rows — a scan of nothing is a false pass.")
        res = check(train, [i["item"] for i in items])
        n_bad = len(getattr(res, "contaminated", []) or [])
        print(f"  contamination guard: {len(train)} rows scanned · {n_bad} flagged")
        if n_bad: sys.exit(f"CONTAMINATED: {n_bad} authored items already in training. Rewrite them.")
    except ImportError:
        if PUBLISH: sys.exit("Refusing to publish without the contamination guard.")
        print("  ⚠ guard not importable — not a pass.")

    rnd = random.Random(42); sh = items[:]; rnd.shuffle(sh)
    cut = int(len(sh) * 0.72); public, private = sh[:cut], sh[cut:]
    if len([1 for _ in public]) < 30:
        print(f"  ⚠ public split is {len(public)} — below usable_n=30. Add items before publishing.")
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/items.jsonl", "w") as f:
        f.write(json.dumps({"_canary": CANARY}) + "\n")
        for it in public: f.write(json.dumps(it) + "\n")
    with open(f"{OUT}/items_heldout_PRIVATE.jsonl", "w") as f:
        for it in private: f.write(json.dumps(it) + "\n")

    card = f"""---
license: apache-2.0
pretty_name: "GSPC-ASI — post-quantum continuity status (n>=30)"
tags: [ai-governance, benchmark, post-quantum, cryptography, measurement]
configs:
  - config_name: default
    data_files:
      - split: train
        path: items.jsonl
---

# GSPC-ASI — post-quantum continuity, grown to carry an interval

**n = {len(public)} public** (+ {len(private)} held out privately). Continuity was the only GSPC axis
measured to **discriminate** across frontier models (spread 0.295 on the 2026-08-05 board). This bank
takes it past **usable_n = 30** so that discriminator can finally publish a Wilson interval, at the
same difficulty.

## What it measures
The post-quantum status of a cryptographic **assumption**: QUANTUM_VULNERABLE (public-key broken by
Shor — key size does not save it), QUANTUM_SAFE (PQC and hash-based signatures), NOT_APPLICABLE
(symmetric / bare hashes — no public-key assumption; Grover only). The discriminating items are the
counterintuitive ones: RSA-4096 is still vulnerable; X25519/Ed25519 are ECC and vulnerable; AES-256 and
SHA-256 are NOT_APPLICABLE, not "quantum-safe"; XMSS/LMS/SPHINCS+ hash-based signatures ARE quantum-safe.

## Provenance & grading
Authored by CSOAI (Apache-2.0, no third-party data). Canary in row 1; {len(private)} held back privately.
Contamination guard confirmed zero overlap before publication. Deterministic label extraction; unreadable
→ **UNMEASURED**, never scored wrong.

## Honesty register
Measurement, not certification; not cryptographic or legal advice. CSOAI Ltd (GB 16939677) · csoai.org
"""
    open(f"{OUT}/README.md", "w").write(card)
    sha = hashlib.sha256(open(f"{OUT}/items.jsonl", "rb").read()).hexdigest()[:16]
    print(f"\n  public {len(public)} · private {len(private)} · sha256:{sha}\n  → {OUT}")
    if not PUBLISH:
        print("\nBuilt locally. --publish via keystone to push."); return
    tok = os.environ.get("HF_TOKEN")
    if not tok: sys.exit("No HF_TOKEN.")
    from huggingface_hub import HfApi
    api = HfApi(token=tok)
    for fn in ("items.jsonl", "README.md"):
        api.upload_file(path_or_fileobj=f"{OUT}/{fn}", path_in_repo=fn, repo_id="csoai/gspc-asi",
                        repo_type="dataset", commit_message=f"n>=30: {len(public)} post-quantum items to give the discriminating axis an interval")
        print(f"  ✅ pushed {fn}")
    print(f"\n  gspc-asi now n={len(public)} — re-run the board; continuity should carry its first interval.")


if __name__ == "__main__":
    main()
