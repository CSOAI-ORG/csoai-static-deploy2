#!/usr/bin/env python3
"""sov33_param_accounting.py — HONEST trillion-parameter accounting for a real T-scale OWEM. MEASURED-RULES.

The honest way to "make T real": build the SOV sovereign layer on a genuine OPEN-WEIGHT trillion-parameter
MoE base. The T lives in the base weights (real, open) — sovereignty is our wrapper. This module does the
honest accounting and ENFORCES the one rule that keeps it honest:

  LEGITIMATE: total_params of ONE MoE model (params really exist in one artifact). State total AND active.
  FORBIDDEN:  summing params across SEPARATE stacked models ("30B + 7B + ... = 1T"). Params don't combine.

So a "T-param OWEM" is REAL iff its base is a real >=1T open MoE — NOT iff you added up a stack of wrappers.

CURRENCY NOTE (per flow CURRENCY_PRINCIPLE): the model list below is from training-knowledge and MAY BE STALE.
Verify live before citing a specific size/license. Sizes are the published figures as known; confirm current.
"""
# Open-weight MoE bases. FIGURES CORROBORATED via web search 2026-07-14 with SNIPPET-LEVEL content across ~7
# independent sources (morphllm, codersera, freedeepseekapi, aimadetools, clore.ai, aiwiki, arxiv 2605.29270).
# CAVEAT (from the sources themselves): these are VENDOR-CLAIMED from DeepSeek's announcement + model card;
# independent reproductions still publishing — "directional, not gospel". One source dissents (~1T/Apache,
# likely conflating an older family member); the ~7-source majority is 1.6T/49B/MIT. Re-check model card
# before any load-bearing public/investor claim. (History: an EARLIER search returned titles-only, so these
# were correctly held as UNVERIFIED then; snippet-level corroboration now supports carrying them.)
OPEN_MOE_BASES = {
    # name: (total_params_B, active_params_B, license, note)  [corroborated 2026-07-14, vendor-claimed]
    "deepseek-v4-pro":  (1600, 49, "MIT",       "1.6T total / 49B active, 61 layers, 384 routed + 1 shared expert (6 active/token), 33T train tokens, 1M ctx, 80.6% SWE-bench. Vendor-claimed; verify model card."),
    "deepseek-v4-flash":(284,  13, "MIT",       "284B total / 13B active, same architecture, ~160GB, fits 1x80GB GPU quantized. Vendor-claimed."),
    "kimi-k2.6":        (1000, 32, "MIT (verify)","~1T total / 32B active MoE (fewer corroborating snippets than V4 — treat as lead)."),
    "glm-5.2":          (744,  40, "MIT (verify)","~744B / ~40B active (Z.ai) — fewer corroborating snippets, treat as lead."),
    "qwen3.x-moe":      (None, None,"Apache-2.0 (verify)","laptop-scale open MoE family — confirm exact current size/name before citing."),
}

def account_single_moe(name):
    """Honest accounting for ONE MoE base: total + active params (both real, both stated)."""
    if name not in OPEN_MOE_BASES:
        return {"error": f"unknown base {name}", "known": list(OPEN_MOE_BASES)}
    tot, act, lic, note = OPEN_MOE_BASES[name]
    tstr = f"{tot}B total ({tot/1000:.2f}T)" if tot is not None else "size [UNVERIFIED]"
    tflag = "This IS a trillion-param model (per search titles)." if (tot is not None and tot >= 1000) else "size unconfirmed."
    return {"base": name, "total_params_B": tot, "active_params_B": act if act is not None else "UNVERIFIED",
            "license_as_known": lic, "is_trillion_scale": (tot is not None and tot >= 1000), "note": note,
            "honest_statement": f"{name}: {tstr}, {act if act is not None else '?'}B active per token. {tflag}"}

def forbidden_stack_sum(model_sizes_B):
    """The FORBIDDEN operation, implemented ONLY to REFUSE it explicitly."""
    return {"REFUSED": True,
            "why": "Summing params across SEPARATE stacked models is the retracted category error. "
                   "A router between a 30B and a 7B is NOT a 37B model; a stack is NOT the sum.",
            "attempted_sum_B": sum(model_sizes_B),
            "honest_alternative": "cite the LARGEST single model's real params, or use a real >=1T MoE base."}

def sovereign_T_owem(base_name):
    """A REAL T-param OWEM = sovereign governance layer wrapping a real open T-scale MoE base.
    The T is the base's real total params; sovereignty is our added layer (adds governance, NOT params)."""
    acc = account_single_moe(base_name)
    if "error" in acc: return acc
    return {"owem": f"sovereign-{base_name}",
            "T_real": acc["is_trillion_scale"],
            "params_from_base": {"total_B": acc["total_params_B"], "active_B": acc["active_params_B"]},
            "sovereignty_adds": "governance (care-floor + Venturi=SIGIL + BFT), memory, attestation — NOT params",
            "honest_headline": (f"sovereign-{base_name} is a REAL {acc['total_params_B']/1000:.2f}T-parameter "
                                f"open-world model: {acc['total_params_B']}B total / {acc['active_params_B']}B active "
                                f"(params from the open {base_name} MoE base), governed + attested by the SOV layer.")
                                if acc["is_trillion_scale"] else
                                f"sovereign-{base_name}: {acc['total_params_B']}B — real but sub-trillion; "
                                f"use a verified >=1T open MoE base (search titles support DeepSeek V4 ~1T) for a genuine T.",
            "governance_layer": "identical across all base sizes (the swap-persistence property)",
            "CURRENCY_STATUS": "DeepSeek V4-Pro 1.6T/49B/MIT corroborated across ~7 sources 2026-07-14 (vendor-claimed, independent repro pending); verify model card before load-bearing public claim."}

if __name__ == "__main__":
    print("=== HONEST T-PARAMETER OWEM ACCOUNTING ===\n")
    print("Real open-weight MoE bases (verify current):")
    for n in OPEN_MOE_BASES:
        a = account_single_moe(n)
        flag = "  <- TRILLION-SCALE" if a["is_trillion_scale"] else ""
        print(f"  {n:18} {str(a['total_params_B']):>5}B total / {a['active_params_B']:>3}B active  {a['license_as_known']}{flag}")
    print("\n--- the REAL T-param OWEM (governance layer on a real T MoE base) ---")
    r = sovereign_T_owem("deepseek-v4-pro")
    print(f"  {r['honest_headline']}")
    print(f"  sovereignty adds: {r['sovereignty_adds']}")
    print("\n--- the FORBIDDEN operation, explicitly refused ---")
    f = forbidden_stack_sum([30, 7, 4, 3, 1])
    print(f"  attempted stack-sum = {f['attempted_sum_B']}B -> REFUSED: {f['why'][:80]}...")
    print(f"  honest alternative: {f['honest_alternative']}")
    print("\n=> T IS REAL when the base is a real >=1T open MoE. T is FAKE when summed across a stack. "
          "\n   'It's all open source' is TRUE: the trillion params are downloadable open weights.")
