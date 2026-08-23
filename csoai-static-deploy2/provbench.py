#!/usr/bin/env python3
"""provbench.py — does an EU AI Act Article 50 provenance marking SURVIVE?

═══════════════════════════════════════════════════════════════════════════════
WHY THIS EXISTS
═══════════════════════════════════════════════════════════════════════════════
`c2pa_manifest.py` proved we can EMIT a real Article 50 marking: `validation_state Valid`,
Ed25519, `digitalSourceType trainedAlgorithmicMedia`. Emission is the easy half.

Article 50(2) requires the marking to be **effective, interoperable, robust and reliable**
"as far as this is technically feasible". A marking that is destroyed the first time the
asset is re-saved by a phone, a CMS, or a chat client is none of those things. Nobody
publishes a number for how often that happens. This measures it.

The result is deliberately uncomfortable: emission is solved and survival is not, and
a compliance story built on emission alone is a story about the wrong half.

═══════════════════════════════════════════════════════════════════════════════
⚠️ PRE-REGISTERED PREDICTIONS — WRITTEN BEFORE THE FIRST RUN
═══════════════════════════════════════════════════════════════════════════════
Recorded here, and encoded in PREDICTION below, so the harness cannot be tuned to agree
with itself afterwards. Every disagreement is printed under PREDICTION vs OBSERVED and is
treated as EITHER a finding OR a harness bug — never as a success.

**embedded_only** (the manifest lives in the file, nothing else is retained):
  · identity ................. manifest/dst/signature/binding all SURVIVE
  · everything else .......... ALL DESTROYED. A C2PA manifest is an APP11/JUMBF segment;
                               any library that re-serialises the container drops it.
                               In particular I predict **JPEG quality is irrelevant** —
                               q90, q70 and q50 destroy it equally, because the manifest
                               is metadata and not pixels. If q90 survives and q50 does
                               not, the harness is measuring pixel similarity somewhere
                               and is wrong.
  · strip_metadata ........... DESTROYED. This is the sanity anchor. **If deliberately
                               removing every APPn segment leaves the manifest readable,
                               suspect the harness before celebrating** — the most likely
                               explanation is that the strip did not run.

**sidecar_oracle** (the manifest is also kept as a detached `.c2pa` and handed straight
to the verifier — the most favourable assumption available, see CAVEATS):
  · manifest / digitalSourceType ... SURVIVE everywhere. This is TRUE BY CONSTRUCTION and
                               is labelled as such in the output. It is reported because
                               it is the disclosure Article 50 actually asks for, not
                               because it is an achievement.
  · signature ................ SURVIVES. The signature covers the claim, not the pixels.
  · binding .................. DESTROYED for every pixel-changing transform: the claim's
                               hard binding is a hash of the asset bytes.
  · binding under strip_metadata ... DESTROYED, predicted with low confidence. Pixels are
                               bit-identical, but the data-hash exclusion range is
                               expressed in byte offsets that the strip moves.

**issuer_resolvable** ......... DESTROYED in every cell **including the untouched control**.
                               Our certificate chains to a private root that is not on the
                               C2PA trust list. This is not a transform result. It is
                               printed as a permanent floor so that no reader mistakes the
                               row for damage caused by a transform.

**format_convert_heic** ....... UNMEASURED. Pillow has no HEIC encoder here, so the
                               transform cannot be applied. It is retained precisely
                               because the benchmark must exercise the UNMEASURED path
                               on real, not simulated, unavailability.

═══════════════════════════════════════════════════════════════════════════════
HOUSE RULES THIS FILE OBEYS
═══════════════════════════════════════════════════════════════════════════════
1. **Three outcomes, never two.** SURVIVED / DESTROYED / **UNMEASURED**. A transform that
   could not be applied, or a container the verifier cannot open, is UNMEASURED and is
   excluded from BOTH the numerator and the denominator — never scored as a failure.
   Enforced with typed exceptions (`TransformUnavailable`, `VerifierUnsupported`,
   `AssetUnsigned`), not with default return values, because a default return value is how
   an unrun test becomes a zero.
2. **Intervals, not rankings.** Wilson 95% on every rate, via `rank_intervals.wilson`.
   Overlapping intervals print a TIED SET and no winner.
3. **Verdicts read the SIGN as well as the significance.** A separation is reported as
   "A above B" or "A BELOW B" from the sign of the difference. Checking only that an
   interval excludes zero is how a −9.16 got printed as "beats".
4. Predictions are above, and were written before the first run.
5. A surviving signature proves **provenance, not correctness**. It says these bytes came
   from this signer with this declared history. It says nothing about whether the content
   is true, safe, or lawful. And our signer is a private root **not on the C2PA trust
   list**, so every verifier reports it as unknown: `signingCredential.untrusted` is in
   the failure list of *every* manifest this file produces, including the control.

    python3 provbench.py --selftest
    python3 provbench.py                 # full run, writes benchmark-results/provbench.json
    python3 provbench.py --assets 24
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# 2026-07-29 — these lived under /tmp and /tmp is cleared. The consequence was not a slow
# rebuild: it was that a benchmark which passed 15/15 in the morning could not be run at all
# by the afternoon, so its published result was unreproducible on any fresh machine. That is
# the same defect that lost the n=195 headline's per-item rows. An artefact whose evidence
# lives in a directory the OS deletes is not an artefact.
# XDG_CACHE_HOME is honoured; /tmp is still read as a fallback so an existing venv is reused
# rather than rebuilt, but nothing is ever CREATED there any more.
_CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "csoai"
_LEGACY = Path("/tmp")


def _pick(name: str) -> Path:
    durable, legacy = _CACHE / name, _LEGACY / name
    if not durable.exists() and legacy.exists():
        return legacy
    return durable


VENV_DIR = _pick("c2pa-venv")
VENV = VENV_DIR / "bin" / "python"
KEYS = _pick("c2pa-keys")
CHAIN = KEYS / "chain.pem"
LEAF_KEY = KEYS / "leaf.key.pem"
TSA = b"http://timestamp.digicert.com"
TRAINED = "trainedAlgorithmicMedia"

SURVIVED, DESTROYED, UNMEASURED = "survived", "destroyed", "unmeasured"


# ── Typed absences ─────────────────────────────────────────────────
# Each of these means "no measurement exists", and each is a DIFFERENT reason. They are
# exceptions rather than sentinel return values so that a caller cannot accidentally
# arithmetic them into an average.

class EnvironmentMissing(Exception):
    """The signing environment is absent. Nothing can be measured; nothing is scored."""


class AssetUnsigned(Exception):
    """This asset could not be marked in the first place, so its survival is undefined.
    The whole asset is dropped from every denominator — it is not a row of zeros."""


class TransformUnavailable(Exception):
    """The transform could not be applied (no encoder, unreadable container, decode error).
    Every check for that cell is UNMEASURED. Scoring an unrun transform as 'destroyed' is
    the exact defect this estate has spent its time removing."""


class VerifierUnsupported(Exception):
    """The transform produced a container the C2PA reader cannot open at all. We do not
    know whether the marking survived — we know we cannot look. UNMEASURED, not destroyed."""


# ── Environment ────────────────────────────────────────────────────

def _ensure_runtime() -> None:
    """Re-exec under the c2pa venv rather than importing a library that is not there.

    If this is skipped, `import c2pa` raises and a naive harness reports every transform as
    a failure — which would be a 0% survival headline produced by a missing dependency."""
    try:
        import c2pa  # noqa: F401
        import PIL  # noqa: F401
        return
    except ImportError:
        pass
    if os.environ.get("PROVBENCH_REEXEC"):
        raise EnvironmentMissing(
            "c2pa/Pillow unavailable even under the venv — nothing measurable")
    if not VENV.exists():
        raise EnvironmentMissing(
            f"no c2pa venv at {VENV}. Build it durably (NOT in /tmp — it gets cleared):\n"
            f"  python3 -m venv {VENV_DIR} && "
            f"{VENV_DIR}/bin/pip install c2pa-python pillow")
    os.environ["PROVBENCH_REEXEC"] = "1"
    os.execv(str(VENV), [str(VENV), str(Path(__file__).resolve()), *sys.argv[1:]])


def _make_signer(timestamped: bool):
    from c2pa import Signer, C2paSignerInfo
    if not (CHAIN.exists() and LEAF_KEY.exists()):
        raise EnvironmentMissing(f"no signing credential at {KEYS}")
    return Signer.from_info(C2paSignerInfo(
        alg=b"ed25519", sign_cert=CHAIN.read_bytes(),
        private_key=LEAF_KEY.read_bytes(), ta_url=TSA if timestamped else None))


def _signer_with_fallback(probe: bytes):
    """Prefer an RFC-3161 timestamped signature; fall back to untimestamped if the TSA is
    unreachable, and RECORD WHICH WAS USED.

    The first version of this only caught a TSA failure when the Signer was constructed,
    but the network call happens at sign time — so an offline run raised AssetUnsigned for
    every asset and the whole benchmark reported 'nothing measurable'. That was the correct
    refusal (it did not invent zeros), but it was refusing over the wrong thing: a missing
    timestamp does not make the marking unmeasurable. An untimestamped signature is a real
    signature with a weaker claim, and the weakening is named in the output rather than
    hidden."""
    try:
        s = _make_signer(True)
        sign(probe, "__tsa_probe__", s)
        return s, "rfc3161"
    except EnvironmentMissing:
        raise
    except Exception as e:
        why = str(e)[:120]
        return _make_signer(False), f"none (TSA unreachable: {why})"


# ── Assets ─────────────────────────────────────────────────────────

def make_assets(n: int) -> list[tuple[str, bytes]]:
    """Deterministic JPEG sources: flat, gradient, noise, and mixed, across sizes.

    Variety matters because a marking that survives on a flat 64x64 and dies on a noisy
    512x512 would be a compression-threshold effect, and we want to be able to see that
    rather than assume it away."""
    import random
    from PIL import Image
    out = []
    kinds = ["flat", "gradient", "noise", "blocks"]
    sizes = [(64, 64), (200, 150), (320, 320), (512, 384)]
    for i in range(n):
        kind = kinds[i % len(kinds)]
        w, h = sizes[(i // len(kinds)) % len(sizes)]
        rnd = random.Random(1000 + i)
        img = Image.new("RGB", (w, h))
        px = img.load()
        if kind == "flat":
            img.paste((rnd.randrange(256), rnd.randrange(256), rnd.randrange(256)),
                      (0, 0, w, h))
        elif kind == "gradient":
            for y in range(h):
                for x in range(w):
                    px[x, y] = (x * 255 // max(1, w - 1), y * 255 // max(1, h - 1), 128)
        elif kind == "noise":
            for y in range(h):
                for x in range(w):
                    px[x, y] = (rnd.randrange(256), rnd.randrange(256), rnd.randrange(256))
        else:
            for y in range(h):
                for x in range(w):
                    px[x, y] = (0, 0, 0) if ((x // 16) + (y // 16)) % 2 else (255, 255, 255)
        b = io.BytesIO()
        img.save(b, "JPEG", quality=95)
        out.append((f"{kind}_{w}x{h}_{i}", b.getvalue()))
    return out


def manifest_json(asset_id: str) -> dict:
    """Same shape `c2pa_manifest.py` emits — the marking under test is OUR marking, not a
    reference one, so the number describes the thing we would actually ship."""
    return {
        "title": f"AI-generated content [{asset_id}]",
        "claim_generator_info": [{"name": "csoai-provbench", "version": "0.1.0"}],
        "assertions": [
            {"label": "c2pa.actions",
             "data": {"actions": [{
                 "action": "c2pa.created",
                 "digitalSourceType":
                     f"http://cv.iptc.org/newscodes/digitalsourcetype/{TRAINED}",
                 "softwareAgent": {"name": "csoai-govbench"},
             }]}},
            {"label": "org.csoai.provenance",
             "data": {"asset_id": asset_id,
                      "marking_basis": "EU AI Act Art 50(2)",
                      "trust_status": "TEST CREDENTIAL — private root CA, NOT on the "
                                      "C2PA trust list"}},
        ],
    }


def sign(source: bytes, asset_id: str, signer) -> tuple[bytes, bytes]:
    """Returns (signed asset bytes, detached manifest bytes). Raises AssetUnsigned."""
    from c2pa import Builder
    try:
        with Builder(json.dumps(manifest_json(asset_id))) as b:
            dst = io.BytesIO()
            mbytes = b.sign(signer, "image/jpeg", io.BytesIO(source), dst)
            return dst.getvalue(), bytes(mbytes)
    except Exception as e:
        raise AssetUnsigned(f"{asset_id}: {type(e).__name__}: {e}") from e


# ── Transforms ─────────────────────────────────────────────────────
# Each returns (bytes, mime). Each raises TransformUnavailable if it cannot be applied.

def _pil_open(data: bytes):
    from PIL import Image
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
        return im.convert("RGB")
    except Exception as e:
        raise TransformUnavailable(f"decode failed: {type(e).__name__}: {e}") from e


def _save(im, fmt: str, mime: str, **kw) -> tuple[bytes, str]:
    try:
        o = io.BytesIO()
        im.save(o, fmt, **kw)
        return o.getvalue(), mime
    except Exception as e:
        raise TransformUnavailable(f"no {fmt} encoder: {type(e).__name__}: {e}") from e


def t_identity(d: bytes) -> tuple[bytes, str]:
    """Control. Not a transform — the row that tells you the harness can see a live marking
    at all. If identity does not survive, no other row means anything."""
    return d, "image/jpeg"


def _reencode(q: int):
    def f(d: bytes) -> tuple[bytes, str]:
        return _save(_pil_open(d), "JPEG", "image/jpeg", quality=q)
    return f


def t_resize_50(d: bytes) -> tuple[bytes, str]:
    from PIL import Image
    im = _pil_open(d)
    im = im.resize((max(1, im.width // 2), max(1, im.height // 2)), Image.LANCZOS)
    return _save(im, "JPEG", "image/jpeg", quality=95)


def t_crop_10(d: bytes) -> tuple[bytes, str]:
    im = _pil_open(d)
    dx, dy = max(1, im.width // 20), max(1, im.height // 20)
    im = im.crop((dx, dy, im.width - dx, im.height - dy))
    return _save(im, "JPEG", "image/jpeg", quality=95)


def t_strip_metadata(d: bytes) -> tuple[bytes, str]:
    """Remove every APPn and COM segment, leaving the entropy-coded scan BIT-IDENTICAL.

    This is the sanity anchor and it is written by hand rather than delegated to Pillow on
    purpose: a re-encode would also destroy the manifest, and then a passing 'strip' row
    would prove nothing about stripping. Here the pixels are untouched, so anything that
    dies died because its metadata was removed."""
    if d[:2] != b"\xff\xd8":
        raise TransformUnavailable("not a JPEG — cannot strip APPn segments")
    out = bytearray(b"\xff\xd8")
    i, removed = 2, 0
    while i < len(d):
        if d[i] != 0xFF:
            raise TransformUnavailable(f"JPEG marker desync at byte {i}")
        while i < len(d) and d[i] == 0xFF:
            i += 1
        if i >= len(d):
            raise TransformUnavailable("truncated JPEG")
        marker = d[i]
        i += 1
        if marker == 0xD9:
            out += b"\xff\xd9"
            break
        if marker == 0xDA:                       # SOS: rest of file is scan data
            out += bytes([0xFF, marker]) + d[i:]
            break
        if i + 2 > len(d):
            raise TransformUnavailable("truncated segment header")
        seglen = int.from_bytes(d[i:i + 2], "big")
        seg = d[i:i + seglen]
        if 0xE0 <= marker <= 0xEF or marker == 0xFE:
            removed += 1
        else:
            out += bytes([0xFF, marker]) + seg
        i += seglen
    if removed == 0:
        # Nothing was stripped, so a "survived" here would be identity wearing a costume.
        raise TransformUnavailable("no APPn/COM segments present to strip")
    return bytes(out), "image/jpeg"


def t_screenshot(d: bytes) -> tuple[bytes, str]:
    """Screenshot-equivalent: rasterise, scale down and back up (the Retina capture path),
    save as PNG. No container metadata can survive a screen capture, so this is the
    upper bound on what screenshotting preserves."""
    from PIL import Image
    im = _pil_open(d)
    small = im.resize((max(1, im.width // 2), max(1, im.height // 2)), Image.LANCZOS)
    im = small.resize((im.width, im.height), Image.LANCZOS)
    return _save(im, "PNG", "image/png")


def t_to_png(d: bytes) -> tuple[bytes, str]:
    return _save(_pil_open(d), "PNG", "image/png")


def t_to_webp(d: bytes) -> tuple[bytes, str]:
    return _save(_pil_open(d), "WEBP", "image/webp", quality=90)


def t_to_heic(d: bytes) -> tuple[bytes, str]:
    """Pillow has no HEIC encoder without pillow-heif. Kept in the suite because the
    UNMEASURED path must be exercised by a real unavailability, not a simulated one — and
    because HEIC is what an iPhone actually produces, so this is a gap in COVERAGE that a
    reader deserves to see named rather than quietly dropped from the transform list."""
    return _save(_pil_open(d), "HEIF", "image/heic")


TRANSFORMS = [
    ("identity", t_identity, "control — no modification"),
    ("reencode_jpeg_q90", _reencode(90), "JPEG re-encode at quality 90"),
    ("reencode_jpeg_q70", _reencode(70), "JPEG re-encode at quality 70"),
    ("reencode_jpeg_q50", _reencode(50), "JPEG re-encode at quality 50"),
    ("resize_50pct", t_resize_50, "downscale to 50% linear"),
    ("crop_10pct", t_crop_10, "crop 5% from each edge"),
    ("strip_metadata", t_strip_metadata, "remove all APPn/COM, pixels bit-identical"),
    ("screenshot_equiv", t_screenshot, "rasterise + rescale + PNG — a SIMULATION of a screen capture, not a real one. Every other transform in this battery is applied to real signed bytes by a real encoder; this one models what a screenshot does rather than taking one. It is labelled so the distinction travels with the result. (The modelling is conservative: a real screenshot discards the container entirely, so it cannot preserve a manifest that this simulation destroys.)"),
    ("format_convert_png", t_to_png, "JPEG -> PNG"),
    ("format_convert_webp", t_to_webp, "JPEG -> WebP q90"),
    ("format_convert_heic", t_to_heic, "JPEG -> HEIC (no encoder available)"),
]

CHECKS = ["manifest_present", "digital_source_type", "signature_valid",
          "binding_intact", "issuer_resolvable"]

CONFIGS = ["embedded_only", "sidecar_oracle"]


# ── Verification ───────────────────────────────────────────────────

def verify(data: bytes, mime: str, sidecar: bytes | None) -> dict[str, str]:
    """Return {check: SURVIVED|DESTROYED} for one transformed asset.

    A missing manifest is a REAL measurement: the property is gone, so DESTROYED is
    correct. UNMEASURED is reserved for the cases where we could not look at all, and
    those raise rather than return."""
    import c2pa
    from c2pa import Reader
    if mime not in Reader.get_supported_mime_types():
        raise VerifierUnsupported(f"reader cannot open {mime}")

    dead = {c: DESTROYED for c in CHECKS}
    try:
        reader = Reader(mime, io.BytesIO(data), sidecar) if sidecar is not None \
            else Reader(mime, io.BytesIO(data))
    except Exception as e:
        name = type(e).__name__
        if "ManifestNotFound" in name or "manifest" in str(e).lower():
            return dead                      # genuinely absent — a measurement
        if "NotSupported" in name or "unsupported" in str(e).lower():
            raise VerifierUnsupported(f"{name}: {e}") from e
        return dead

    try:
        doc = json.loads(reader.json())
        vres = reader.get_validation_results() or {}
    except Exception as e:
        raise VerifierUnsupported(f"reader produced no report: {type(e).__name__}: {e}") from e

    mans = doc.get("manifests") or {}
    active = doc.get("active_manifest") or doc.get("activeManifest")
    man = mans.get(active) if active in mans else next(iter(mans.values()), None)
    if not man:
        return dead

    am = vres.get("activeManifest", {}) or {}
    ok = {x.get("code") for x in am.get("success", [])}
    bad = {x.get("code") for x in am.get("failure", [])}

    dst = None
    for a in man.get("assertions", []):
        if str(a.get("label", "")).startswith("c2pa.actions"):
            for act in (a.get("data") or {}).get("actions", []):
                v = act.get("digitalSourceType")
                if v:
                    dst = v.rsplit("/", 1)[-1]

    # `signature_valid` means: the claim signature verifies AND every assertion the signed
    # claim points at still hashes to what the claim says.
    #
    # 2026-07-29 — the first version of this checked only `claimSignature.validated`, and an
    # adversarial probe showed it was too weak: flipping bytes inside the manifest store
    # left it reporting SURVIVED, because the claim signature covers the claim, not the
    # assertions hanging off it. Adding the hashedURI condition closes most of that.
    # MEASURED, and stated because it is still not all of it: over 200 random single-bit
    # flips in a detached manifest store, 69% were caught by assertion.hashedURI.mismatch,
    # 3% by the claim signature, and **26% by neither**. Those 26% are still rejected
    # overall — they fail `binding_intact` — but a reader who takes `signature_valid` to
    # mean "the manifest is unaltered" would be wrong 26% of the time, so it does not mean
    # that and the output says so.
    sig_ok = ("claimSignature.validated" in ok) and not any(
        c.startswith("claimSignature.") and c.endswith((".mismatch", ".missing"))
        for c in bad) and not any("hashedURI.mismatch" in c for c in bad)
    binding_ok = not any("dataHash" in c or "bmff" in c.lower() or "boxHash" in c
                         for c in bad)
    trusted = "signingCredential.untrusted" not in bad and \
              str(reader.get_validation_state()) in ("Trusted", "ValidationState.Trusted")

    return {
        "manifest_present": SURVIVED,
        "digital_source_type": SURVIVED if dst == TRAINED else DESTROYED,
        "signature_valid": SURVIVED if sig_ok else DESTROYED,
        "binding_intact": SURVIVED if binding_ok else DESTROYED,
        "issuer_resolvable": SURVIVED if trusted else DESTROYED,
    }


# ── Pre-registered prediction, machine-readable ────────────────────

def predict(config: str, transform: str, check: str) -> str:
    if transform == "format_convert_heic":
        return UNMEASURED
    if check == "issuer_resolvable":
        return DESTROYED                      # permanent floor, private root CA
    if transform == "identity":
        return SURVIVED
    if config == "embedded_only":
        return DESTROYED
    return DESTROYED if check == "binding_intact" else SURVIVED


# ── Run ────────────────────────────────────────────────────────────

def run(n_assets: int, verbose: bool = True) -> dict:
    _ensure_runtime()
    import c2pa

    assets = make_assets(n_assets)
    signer, ts_mode = _signer_with_fallback(assets[0][1])
    signed, unsigned = [], []
    for aid, src in assets:
        try:
            sbytes, mbytes = sign(src, aid, signer)
            signed.append((aid, sbytes, mbytes))
        except AssetUnsigned as e:
            unsigned.append(str(e))           # absent, not zero
    if not signed:
        raise EnvironmentMissing(f"no asset could be marked: {unsigned[:2]}")
    if verbose:
        print(f"  marked {len(signed)}/{len(assets)} assets "
              f"(timestamp: {ts_mode}){'' if not unsigned else f'; {len(unsigned)} unsigned'}")

    # results[config][transform][check] -> list of outcomes
    results = {c: {t[0]: {k: [] for k in CHECKS} for t in TRANSFORMS} for c in CONFIGS}
    reasons: dict[str, str] = {}

    for aid, sbytes, mbytes in signed:
        for tname, tfn, _desc in TRANSFORMS:
            try:
                tdata, mime = tfn(sbytes)
            except TransformUnavailable as e:
                reasons.setdefault(f"{tname}", f"TransformUnavailable: {e}")
                for cfg in CONFIGS:
                    for k in CHECKS:
                        results[cfg][tname][k].append(UNMEASURED)
                continue
            for cfg in CONFIGS:
                side = mbytes if cfg == "sidecar_oracle" else None
                try:
                    out = verify(tdata, mime, side)
                except VerifierUnsupported as e:
                    reasons.setdefault(f"{cfg}/{tname}", f"VerifierUnsupported: {e}")
                    out = {k: UNMEASURED for k in CHECKS}
                except Exception as e:
                    reasons.setdefault(f"{cfg}/{tname}", f"{type(e).__name__}: {e}")
                    out = {k: UNMEASURED for k in CHECKS}
                for k in CHECKS:
                    results[cfg][tname][k].append(out[k])

    return {"results": results, "n_signed": len(signed), "unsigned": unsigned,
            "reasons": reasons, "ts_mode": ts_mode,
            "sdk": c2pa.sdk_version(), "assets": [a for a, _ in assets]}


# ── Aggregation & report ───────────────────────────────────────────

def cells(results: dict) -> list[dict]:
    from rank_intervals import wilson
    rows = []
    for cfg in CONFIGS:
        for tname, _fn, desc in TRANSFORMS:
            for k in CHECKS:
                outs = results[cfg][tname][k]
                s = outs.count(SURVIVED)
                d = outs.count(DESTROYED)
                u = outs.count(UNMEASURED)
                n = s + d
                if n == 0:
                    rows.append({"config": cfg, "transform": tname, "check": k,
                                 "survived": s, "destroyed": d, "unmeasured": u,
                                 "n_measured": 0, "rate": None, "ci": None,
                                 "outcome": UNMEASURED,
                                 "predicted": predict(cfg, tname, k), "desc": desc})
                    continue
                lo, hi = wilson(s, n)
                rows.append({"config": cfg, "transform": tname, "check": k,
                             "survived": s, "destroyed": d, "unmeasured": u,
                             "n_measured": n, "rate": round(s / n, 4),
                             "ci": [round(lo, 4), round(hi, 4)],
                             "outcome": SURVIVED if s == n else
                                        (DESTROYED if s == 0 else "mixed"),
                             "predicted": predict(cfg, tname, k), "desc": desc})
    return rows


def by_check(rows: list[dict], results: dict | None = None,
             exclude_identity: bool = True) -> list[dict]:
    """Survival rate per (config, check) pooled over transforms.

    Identity is excluded by default: it is the control, and pooling it in would inflate
    every rate with a row that was never transformed.

    ═══════════════════════════════════════════════════════════════════════════
    TWO INTERVALS, AND THE NARROW ONE IS THE WRONG ONE
    ═══════════════════════════════════════════════════════════════════════════
    `ci` treats every (asset, transform) pair as an independent Bernoulli trial. It is
    NOT: the same 12 assets appear under all 9 transforms, so the trials are clustered by
    asset and that interval is too narrow — 0/108 reads as [0, 3.4%] when the experiment
    only ever saw 12 independent things. This is the clustered-SE problem `rank_intervals`
    already flags for the model board, arriving here for the same reason.

    `ci_clustered` is the conservative one: n is the number of ASSETS, and an asset counts
    as a survivor only if every measured transform on it survived. Quote this one. The
    unclustered interval is kept alongside solely so the difference is visible instead of
    being a choice made quietly.
    """
    from rank_intervals import wilson
    out = []
    for cfg in CONFIGS:
        for k in CHECKS:
            sel = [r for r in rows if r["config"] == cfg and r["check"] == k
                   and not (exclude_identity and r["transform"] == "identity")]
            s = sum(r["survived"] for r in sel)
            d = sum(r["destroyed"] for r in sel)
            u = sum(r["unmeasured"] for r in sel)
            n = s + d
            lo, hi = wilson(s, n) if n else (0.0, 1.0)
            row = {"config": cfg, "check": k, "survived": s, "destroyed": d,
                   "unmeasured": u, "n_measured": n,
                   "rate": round(s / n, 4) if n else None,
                   "ci": [round(lo, 4), round(hi, 4)] if n else None,
                   "ci_note": "unclustered — too narrow; see ci_clustered"}
            if results is not None:
                names = [t[0] for t in TRANSFORMS
                         if not (exclude_identity and t[0] == "identity")]
                per_asset, n_assets = [], 0
                for i in range(max((len(results[cfg][t][k]) for t in names), default=0)):
                    obs = [results[cfg][t][k][i] for t in names
                           if i < len(results[cfg][t][k])
                           and results[cfg][t][k][i] != UNMEASURED]
                    if not obs:
                        continue                       # asset wholly UNMEASURED here
                    n_assets += 1
                    per_asset.append(all(o == SURVIVED for o in obs))
                kc = sum(per_asset)
                clo, chi = wilson(kc, n_assets) if n_assets else (0.0, 1.0)
                row["n_assets"] = n_assets
                row["assets_fully_surviving"] = kc
                row["ci_clustered"] = [round(clo, 4), round(chi, 4)] if n_assets else None
                # ── THE PAIRING, MADE UNAMBIGUOUS ──────────────────────────────────────
                # The interval and the n MUST travel together or the result is indefensible.
                # 24.2% is the Wilson two-sided bound at n=12 ASSETS; at n=108 cells the
                # bound is 3.4%. Quoting the wide (cluster) interval beside the large (trial)
                # n is internally inconsistent, and it is the single most exploitable error
                # available to a hostile reviewer: they recompute 3.4% from n=108 and reject
                # the whole analysis. So the artefact now carries a pre-formatted headline
                # that cannot be split, plus the exact Clopper-Pearson bound, which is what
                # is recommended at X=0 (Wald and Agresti-Coull are documented to fail there).
                import math as _m
                cp1 = 1 - 0.05 ** (1 / n_assets) if n_assets else None    # one-sided 95%
                cp2 = 1 - 0.025 ** (1 / n_assets) if n_assets else None   # two-sided 95%
                row["cp_upper_one_sided_95"] = round(cp1, 4) if cp1 else None
                row["cp_upper_two_sided_95"] = round(cp2, 4) if cp2 else None
                row["headline"] = (
                    f"{kc} of {n_assets} assets survived ({s} of {n} measured cells). "
                    f"One-sided 95% Clopper-Pearson upper bound on per-asset survival: "
                    f"{cp1*100:.1f}%. The interval is computed at n={n_assets} ASSETS, not "
                    f"n={n} cells — the cells are clustered within assets and are not "
                    f"independent trials." if n_assets else None)
                row["uncertainty_is"] = (
                    "EXTERNAL VALIDITY, not measurement noise. A hard binding is a "
                    "cryptographic hash over asset bytes, so re-running any cell reproduces "
                    "the identical outcome with probability 1 — the run-to-run (Type A, per "
                    "JCGM 100:2008) uncertainty is structurally zero. The bound quantifies "
                    "generalisation to unseen assets and transforms, nothing else.")
            out.append(row)
    return out


def compare(bc: list[dict]) -> list[dict]:
    """embedded_only vs sidecar_oracle, per check.

    Reports a TIED SET when the Wilson intervals overlap. When they separate it reports the
    DIRECTION FROM THE SIGN of the difference — an interval that excludes zero is not by
    itself a claim that the first arm is better, and a previous tool here printed 'beats'
    for a Δ of −9.16 by making exactly that mistake.

    Uses the CLUSTERED interval, which is the wider one, so a separation reported here is
    not an artefact of counting the same assets once per transform."""
    from rank_intervals import items_to_resolve
    idx = {(r["config"], r["check"]): r for r in bc}
    out = []
    for k in CHECKS:
        a, b = idx[("embedded_only", k)], idx[("sidecar_oracle", k)]
        if a["n_measured"] == 0 or b["n_measured"] == 0:
            out.append({"check": k, "verdict": "UNMEASURED — no comparable cells"})
            continue
        aci = a.get("ci_clustered") or a["ci"]
        bci = b.get("ci_clustered") or b["ci"]
        delta = b["rate"] - a["rate"]
        overlap = not (aci[1] < bci[0] or bci[1] < aci[0])
        if overlap:
            need = items_to_resolve(a["rate"], b["rate"])
            verdict = ("TIED — intervals overlap; {embedded_only, sidecar_oracle}. "
                       + (f"~{need} assets/config would be needed to separate."
                          if need else "Rates are exactly equal; no n separates them."))
        else:
            direction = "ABOVE" if delta > 0 else "BELOW"
            verdict = (f"SEPARATED — sidecar_oracle is {direction} embedded_only "
                       f"by {delta*100:+.1f} points (sign read, not just significance)")
        out.append({"check": k, "embedded_only": a["rate"], "sidecar_oracle": b["rate"],
                    "delta": round(delta, 4), "ci_overlap": overlap,
                    "embedded_ci_clustered": aci, "sidecar_ci_clustered": bci,
                    "verdict": verdict})
    return out


def disagreements(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        obs = r["outcome"]
        if obs != r["predicted"]:
            out.append({"config": r["config"], "transform": r["transform"],
                        "check": r["check"], "predicted": r["predicted"],
                        "observed": obs, "rate": r["rate"],
                        "n_measured": r["n_measured"]})
    return out


CAVEATS = [
    "A surviving signature proves PROVENANCE, NOT CORRECTNESS. It states that these bytes "
    "carry a claim signed by this key with this declared history. It says nothing about "
    "whether the content is accurate, safe, or lawful.",
    "Our certificate chains to a PRIVATE ROOT CA that is NOT on the C2PA trust list. "
    "'signingCredential.untrusted' appears in the failure list of every manifest here, "
    "including the untouched control. issuer_resolvable is therefore 0% everywhere by "
    "construction — it is a property of the credential, not damage from a transform. "
    "Article 50 conformity needs a production certificate from a CA on the C2PA trust list.",
    "sidecar_oracle is the MOST FAVOURABLE assumption available: the harness hands the "
    "detached manifest straight to the verifier. In the field you must first work out "
    "which sidecar belongs to which asset, and after a crop or re-encode you cannot do "
    "that by hash. Its manifest_present and digital_source_type rates are TRUE BY "
    "CONSTRUCTION and are an upper bound, not a deployment result.",
    "Transforms are applied by Pillow. A different re-encoder (libvips, ImageMagick, a "
    "phone ISP, a CDN) may behave differently; some deliberately preserve APP11. This "
    "measures the common case, not every case.",
    "n is the number of marked assets per cell, and it is small. 0 survivors out of 12 "
    "still admits a true survival rate up to ~24%. Quote ci_clustered, not ci: the "
    "unclustered pooled interval treats the same 12 assets as 108 independent trials and "
    "is too narrow. Both are printed so the difference is visible rather than chosen.",
    "signature_valid means the CLAIM SIGNATURE VERIFIES AND THE ASSERTION HASHED-URIs "
    "MATCH. It does NOT mean the manifest is unaltered. Measured over 200 random "
    "single-bit flips in a detached manifest store: 69% caught by hashedURI, 3% by the "
    "claim signature, 26% by NEITHER. Those 26% still fail binding_intact, so nothing "
    "here is a hole in C2PA — but the check is narrower than its name and is used "
    "accordingly.",
    "A manifest lifted from a DIFFERENT asset also reports signature_valid=survived — "
    "measured, not assumed. binding_intact is the only check that catches it. A verifier "
    "that reports 'signature valid' without reporting the binding is telling you almost "
    "nothing.",
    "No soft binding (watermark) and no cloud manifest recovery are tested. Both exist "
    "precisely because embedded manifests do not survive, so a real Article 50 durability "
    "programme would have to measure them too. Their absence here is COVERAGE MISSING, "
    "not evidence that they fail.",
]


def report(data: dict, out_path: Path | None) -> dict:
    rows = cells(data["results"])
    bc = by_check(rows, data["results"])
    cmp_ = compare(bc)
    dis = disagreements(rows)
    n = data["n_signed"]

    print(f"\n  PROVBENCH — does an Article 50 marking SURVIVE?")
    print(f"  {n} marked assets × {len(TRANSFORMS)} transforms × {len(CHECKS)} checks "
          f"× {len(CONFIGS)} configs   (c2pa sdk {data['sdk']})\n")

    for cfg in CONFIGS:
        print(f"  ── {cfg} " + "─" * (62 - len(cfg)))
        head = "  ".join(f"{c[:9]:>9s}" for c in CHECKS)
        print(f"    {'transform':22s} {head}")
        for tname, _fn, _d in TRANSFORMS:
            cellrow = []
            for k in CHECKS:
                r = next(x for x in rows if x["config"] == cfg
                         and x["transform"] == tname and x["check"] == k)
                if r["n_measured"] == 0:
                    cellrow.append(f"{'UNMEAS':>9s}")
                else:
                    cellrow.append(f"{r['survived']:>4d}/{r['n_measured']:<4d}")
            print(f"    {tname:22s} " + "  ".join(cellrow))
        print()

    print(f"  ── POOLED SURVIVAL (identity control excluded) " + "─" * 22)
    for cfg in CONFIGS:
        print(f"    {cfg}")
        for k in CHECKS:
            r = next(x for x in bc if x["config"] == cfg and x["check"] == k)
            if not r["n_measured"]:
                print(f"      {k:22s} UNMEASURED ({r['unmeasured']} cells)")
                continue
            cc = r.get("ci_clustered") or r["ci"]
            print(f"      {k:22s} {r['rate']*100:5.1f}%  "
                  f"clustered CI [{cc[0]*100:5.1f}, {cc[1]*100:5.1f}] on "
                  f"{r.get('n_assets', '?')} assets   "
                  f"(unclustered [{r['ci'][0]*100:.1f}, {r['ci'][1]*100:.1f}] on "
                  f"n={r['n_measured']} — too narrow)  unmeasured={r['unmeasured']}")
    print()

    print(f"  ── CONFIG COMPARISON — tied sets, and the SIGN of every separation " + "─" * 3)
    for c in cmp_:
        print(f"    {c['check']:22s} {c['verdict']}")
    print()

    print(f"  ── PREDICTION vs OBSERVED " + "─" * 43)
    if not dis:
        print("    every cell matched the pre-registered prediction.")
        print("    ⚠️  a benchmark that agrees with its author everywhere is the case where")
        print("       you check the harness hardest, not the case where you relax.")
    else:
        for d in dis:
            print(f"    ⚠️  {d['config']}/{d['transform']}/{d['check']}: "
                  f"predicted {d['predicted']}, observed {d['observed']} "
                  f"(rate {d['rate']}, n={d['n_measured']})")
    print()

    if data["reasons"]:
        print(f"  ── WHY CELLS ARE UNMEASURED " + "─" * 41)
        for k, v in data["reasons"].items():
            print(f"    {k:34s} {v[:90]}")
        print()

    print(f"  ── WHAT THIS DOES AND DOES NOT PROVE " + "─" * 32)
    for c in CAVEATS:
        first = True
        for line in _wrap(c, 84):
            print(("    • " if first else "      ") + line)
            first = False
    print()

    payload = {
        "benchmark": "provbench",
        "version": "0.1.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "question": "Does an EU AI Act Article 50 provenance marking survive real-world "
                    "transforms?",
        "pre_registered_prediction": {
            f"{cfg}/{t[0]}/{k}": predict(cfg, t[0], k)
            for cfg in CONFIGS for t in TRANSFORMS for k in CHECKS},
        "environment": {"c2pa_sdk": data["sdk"], "timestamp_authority": data["ts_mode"],
                        "signing_alg": "Ed25519",
                        "trust_anchor": "private root CA, NOT on the C2PA trust list"},
        "n_assets_marked": n,
        "assets_unsigned": data["unsigned"],
        "transforms": [{"name": t[0], "description": t[2]} for t in TRANSFORMS],
        "checks": CHECKS,
        "configs": CONFIGS,
        "cells": rows,
        "pooled_by_check": bc,
        "config_comparison": cmp_,
        "prediction_disagreements": dis,
        "unmeasured_reasons": data["reasons"],
        "caveats": CAVEATS,
    }
    if out_path:
        # Anchored at write time. Running this by hand, outside the AUTO queue, used to strip
        # the artefact's own corpus anchor — twice in one day. Ordering is a discipline;
        # write_result() is a mechanism.
        from anchored_write import write_result
        out_path = write_result(out_path.name, payload)
        print(f"  -> {out_path}")
    return payload


def _wrap(s: str, w: int) -> list[str]:
    words, line, out = s.split(), "", []
    for x in words:
        if len(line) + len(x) + 1 > w:
            out.append(line)
            line = x
        else:
            line = f"{line} {x}".strip()
    if line:
        out.append(line)
    return out


# ── Self-test ──────────────────────────────────────────────────────

def selftest() -> int:
    """Checks the HARNESS, not the marking. Every assertion here is about whether the
    measurement apparatus can tell the three outcomes apart."""
    _ensure_runtime()
    print("  PROVBENCH SELF-TEST — is the apparatus able to measure?\n")
    fails = []

    def chk(name, cond, detail=""):
        print(f"    {'✅' if cond else '❌'} {name}{(' — ' + detail) if detail else ''}")
        if not cond:
            fails.append(name)

    try:
        data = run(3, verbose=False)
    except EnvironmentMissing as e:
        print(f"    ❌ environment: {e}")
        print("\n    Nothing was measured. This is UNMEASURED, not a score of zero.")
        return 2

    rows = cells(data["results"])
    g = lambda cfg, t, k: next(r for r in rows if r["config"] == cfg
                               and r["transform"] == t and r["check"] == k)

    chk("assets were actually marked", data["n_signed"] == 3, f"{data['n_signed']}/3")

    ident = g("embedded_only", "identity", "manifest_present")
    chk("control survives (identity keeps the manifest)", ident["rate"] == 1.0,
        "if this fails, no other row means anything")
    chk("control keeps digitalSourceType",
        g("embedded_only", "identity", "digital_source_type")["rate"] == 1.0)

    strip = g("embedded_only", "strip_metadata", "manifest_present")
    chk("stripping APPn destroys the embedded manifest", strip["rate"] == 0.0,
        "the sanity anchor — a survival here means the strip did not run")

    heic = g("embedded_only", "format_convert_heic", "manifest_present")
    chk("an inapplicable transform is UNMEASURED, not destroyed",
        heic["n_measured"] == 0 and heic["unmeasured"] == 3,
        f"n_measured={heic['n_measured']} unmeasured={heic['unmeasured']}")
    chk("UNMEASURED cells carry no rate", heic["rate"] is None)

    all_out = [o for cfg in CONFIGS for t in TRANSFORMS
               for k in CHECKS for o in data["results"][cfg][t[0]][k]]
    chk("only three outcomes are ever emitted",
        set(all_out) <= {SURVIVED, DESTROYED, UNMEASURED}, str(sorted(set(all_out))))
    chk("all three outcomes actually occur",
        {SURVIVED, DESTROYED, UNMEASURED} <= set(all_out),
        "a two-outcome run would mean the UNMEASURED path is untested")

    issuer = g("embedded_only", "identity", "issuer_resolvable")
    chk("issuer is NOT resolvable even on the untouched control",
        issuer["rate"] == 0.0,
        "private root CA — reporting otherwise would overstate conformity")

    from rank_intervals import wilson
    lo, hi = wilson(0, 3)
    chk("Wilson interval on 0/3 is wide and inside [0,1]",
        lo == 0.0 and 0.5 < hi < 1.0, f"[{lo:.3f}, {hi:.3f}]")

    # ── adversarial: are the checks capable of saying no? ───────────
    # Added after the first full run matched every prediction. A harness that only ever
    # confirms is a harness nobody has tried to break.
    import random
    signer, _ts = _signer_with_fallback(make_assets(1)[0][1])
    (a1, s1), (a2, s2) = make_assets(2)
    sig1, mb1 = sign(s1, a1, signer)
    sig2, mb2 = sign(s2, a2, signer)
    png1 = t_to_png(sig1)[0]

    chk("strip_metadata leaves the pixels BIT-IDENTICAL",
        _pil_open(t_strip_metadata(sig1)[0]).tobytes() == _pil_open(sig1).tobytes(),
        "otherwise 'stripping destroys it' would just be re-encoding destroying it")

    rnd = random.Random(7)
    caught = 0
    for _ in range(40):
        b = bytearray(mb1)
        b[rnd.randrange(len(b))] ^= 1 << rnd.randrange(8)
        try:
            if verify(png1, "image/png", bytes(b))["signature_valid"] == DESTROYED:
                caught += 1
        except VerifierUnsupported:
            caught += 1                       # unreadable is also a refusal to bless it
    chk("a tampered manifest is mostly rejected by signature_valid", caught >= 24,
        f"{caught}/40 caught — the rest are caught only by binding_intact (see caveats)")

    lifted = verify(png1, "image/png", mb2)   # asset 1's pixels, asset 2's manifest
    chk("a manifest lifted from another asset fails binding_intact",
        lifted["binding_intact"] == DESTROYED,
        "this is the check that catches manifest transplants")
    chk("...and signature_valid alone does NOT catch it",
        lifted["signature_valid"] == SURVIVED,
        "documented in the caveats — a signature check without a binding check is nearly empty")

    cmp_ = compare(by_check(rows, data["results"]))
    chk("comparison verdicts state a sign or a tie",
        all("TIED" in c["verdict"] or "ABOVE" in c["verdict"] or "BELOW" in c["verdict"]
            or "UNMEASURED" in c["verdict"] for c in cmp_))

    print(f"\n    {len(fails)} failure(s)" + (f": {fails}" if fails else ""))
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="ProvBench — Article 50 marking survival")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--assets", type=int, default=12,
                    help="number of marked assets per cell (default 12)")
    ap.add_argument("--out", default=str(HERE / "benchmark-results" / "provbench.json"))
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        data = run(a.assets)
    except EnvironmentMissing as e:
        print(f"  ❌ {e}")
        print("  Nothing was measured. Reporting this as 0% survival would be a lie about")
        print("  the marking when the truth is a missing dependency.")
        return 2
    report(data, Path(a.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
