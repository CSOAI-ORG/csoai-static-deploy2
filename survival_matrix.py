"""P-axis manifest-SURVIVAL matrix — cells x transforms, the white-space the compass calls 'genuinely first'.
Question: does a C2PA content-credential MARKING survive a real-world transform (re-encode/crop/screenshot/upload)?
This is NOT watermark-algorithm robustness (WAVES/UnMarker measure that) — it's whether the MANIFEST persists.

HONESTY (load-bearing): survival PHYSICS requires real C2PA-signed image files + real transforms + c2patool to
validate. The sandbox has neither, so this harness ships two modes:
  - STRUCTURE (real, runs now): the matrix engine, selftest, CI computation, deterministic pass/fail from a binding
    model. Verified correct here.
  - PHYSICS (modeled, labelled): each transform's strip-or-survive outcome is set from DOCUMENTED C2PA binding
    behaviour (hard binding = detached/metadata -> stripped by re-encode/screenshot; soft binding = watermark/durable
    -> may survive). Marked modeled=True until run on real files with c2patool. NO real 0/108 claimed here."""
import json, hashlib, math

# Transforms an asset undergoes in the wild (the columns)
TRANSFORMS = ["identity","jpeg_reencode","png_reencode","crop","resize","screenshot","social_upload","strip_metadata"]

# Binding types a manifest can use (documented C2PA)
# hard binding = manifest bound to exact bytes (hash) or sidecar/metadata -> dies on ANY re-encode/strip
# soft binding = durable content id / watermark -> can survive lossy transforms
def survives(binding, transform):
    """Modeled from documented C2PA behaviour. Returns (survives: bool, basis: str). modeled — not measured."""
    if transform=="identity": return True, "no transform"
    if binding=="hard_hash":       # embedded/hashed manifest bound to exact bytes
        return False, "hard binding: any byte change breaks the hash"
    if binding=="metadata_xmp":    # manifest in XMP/EXIF metadata block
        if transform in ("strip_metadata","screenshot","social_upload"): return False, "metadata stripped"
        if transform in ("jpeg_reencode","png_reencode","crop","resize"): return False, "re-encode drops metadata block"
        return True, "metadata preserved"
    if binding=="soft_watermark":  # durable content credential / watermark soft binding
        if transform in ("screenshot","social_upload","jpeg_reencode","resize"): return True, "soft binding survives lossy"
        if transform in ("crop",): return False, "crop can remove watermark region"
        if transform in ("strip_metadata",): return True, "watermark is in pixels, not metadata"
        return True, "soft binding robust"
    # SEED V2: COSE ML-DSA-65 binding (2026-07-30)
    # Mirrors C2PA v2.4 approach: signed manifest with PQC algorithm
    if binding=="cose_ml_dsa_65":  # COSE-signed manifest with ML-DSA-65 (PQC)
        if transform in ("strip_metadata","screenshot","social_upload"): return False, "COSE signature in metadata stripped"
        if transform in ("jpeg_reencode","png_reencode","crop","resize"): return False, "re-encode drops COSE container"
        return True, "COSE signature preserved"
    return False, "unknown binding"

def run_matrix(cells):
    """cells: list of {asset_id, binding}. Returns matrix result + survival stats with a rule-of-three CI when 0 survive."""
    rows=[]; n_survive=0; n_total=0
    for c in cells:
        for tf in TRANSFORMS:
            if tf=="identity": continue   # identity is the selftest control, not a survival trial
            ok,basis=survives(c["binding"], tf)
            rows.append({"asset":c["asset_id"],"binding":c["binding"],"transform":tf,"survived":ok,"basis":basis})
            n_survive+=int(ok); n_total+=1
    return {"rows":rows,"n_survive":n_survive,"n_total":n_total}

def survival_ci(n_survive, n_total):
    """Honest CI. If 0 survive: rule-of-three upper bound = 3/n (INDEPENDENCE assumed — flag clustering).
    Else Wilson-ish point estimate. Returns dict with the independence caveat baked in."""
    if n_total==0: return {"rate":None,"note":"no trials"}
    rate=n_survive/n_total
    if n_survive==0:
        ub=3.0/n_total
        return {"survival_rate":0.0,"rule_of_three_upper_95":round(ub,4),
                "caveat":"upper bound valid ONLY under independence; cells cluster by (asset,binding) -> report effective-n"}
    return {"survival_rate":round(rate,4),"n_survive":n_survive,"n_total":n_total}

def selftest():
    """The identity control MUST survive for every binding (else the harness is broken)."""
    for b in ["hard_hash","metadata_xmp","soft_watermark","cose_ml_dsa_65"]:
        ok,_=survives(b,"identity")
        if not ok: return False, f"selftest FAIL: identity did not survive for {b}"
    return True, "selftest pass: identity survives all bindings"
