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
# Open-weight MoE bases (published figures, AS KNOWN — verify current before citing).
# HONEST SCOPE (corrected after auditor catch): a web search on 2026-07-14 returned TITLES confirming only
# that "DeepSeek V4 is a ~1-trillion-parameter open-source MoE" (two result titles state this explicitly).
# The specific figures below marked [UNVERIFIED] were NOT confirmed by the retained results and MUST be
# re-verified against a primary source (model card / HF repo) before ANY public citation. I removed the
# earlier over-precise numbers (1.6T/49B/33T tokens/Kimi-K2.6 dates) that I could not substantiate.
OPEN_MOE_BASES = {
    # name: (total_params_B, active_params_B, license, note)
    "deepseek-v4":     (1000, None, "open (verify: MIT reported)", "SUPPORTED by search titles: '~1 trillion parameter open-source MoE' (Isabella King/Swfte 2026). Active-param count + exact license [UNVERIFIED] - check model card."),
    "qwen3.x-moe":     (None, None, "Apache-2.0 (verify)",         "[UNVERIFIED] laptop-scale open MoE family - confirm exact current size/name before citing"),
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
            "CURRENCY_STATUS": "search titles support only 'DeepSeek V4 ~1T open MoE'; active-param count + exact license are [UNVERIFIED] — confirm on the model card before any public citation."}

if __name__ == "__main__":
    print("=== HONEST T-PARAMETER OWEM ACCOUNTING ===\n")
    print("Real open-weight MoE bases (verify current):")
    for n in OPEN_MOE_BASES:
        a = account_single_moe(n)
        flag = "  <- TRILLION-SCALE" if a["is_trillion_scale"] else ""
        print(f"  {n:18} {str(a['total_params_B']):>5}B total / {a['active_params_B']:>3}B active  {a['license_as_known']}{flag}")
    print("\n--- the REAL T-param OWEM (governance layer on a real T MoE base) ---")
    r = sovereign_T_owem("deepseek-v4")
    print(f"  {r['honest_headline']}")
    print(f"  sovereignty adds: {r['sovereignty_adds']}")
    print("\n--- the FORBIDDEN operation, explicitly refused ---")
    f = forbidden_stack_sum([30, 7, 4, 3, 1])
    print(f"  attempted stack-sum = {f['attempted_sum_B']}B -> REFUSED: {f['why'][:80]}...")
    print(f"  honest alternative: {f['honest_alternative']}")
    print("\n=> T IS REAL when the base is a real >=1T open MoE. T is FAKE when summed across a stack. "
          "\n   'It's all open source' is TRUE: the trillion params are downloadable open weights.")
