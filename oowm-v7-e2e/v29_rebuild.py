import json, pathlib, hashlib
from collections import Counter

def load_jsonl(p):
    out = []
    for l in open(p):
        l = l.strip()
        if not l:
            continue
        try:
            r = json.loads(l)
            if isinstance(r, dict):
                out.append(r)
        except Exception:
            pass
    return out

def cls(t):
    t = t.lower()
    if any(k in t for k in ["care", "protect", "safety", "family", "children", "elder", "vulnerable"]): return "mom"
    if any(k in t for k in ["eu", "ai act", "risk", "tier", "prohibited", "high risk", "limited"]): return "quant"
    if any(k in t for k in ["bft", "council", "vote", "quorum", "byzantine", "committee"]): return "council"
    if any(k in t for k in ["sovereign", "mesh", "self", "kingdom", "royal"]): return "sovereign"
    if any(k in t for k in ["open", "license", "apache", "mit", "free", "redistribut"]): return "free"
    if any(k in t for k in ["defense", "security", "threat", "attack", "cyber", "harness", "govern"]): return "king"
    if any(k in t for k in ["intuition", "feeling", "gestalt", "align", "world model"]): return "man"
    if any(k in t for k in ["small", "edge", "lightweight", "quantum", "ml-dsa", "post-quantum"]): return "small-moe"
    if any(k in t for k in ["large", "attention", "mamba", "expert", "cloud", "64"]): return "big-moe"
    if any(k in t for k in ["bridge", "connect", "interop", "trust"]): return "bridge"
    return "oowm"

def extract(r):
    if isinstance(r.get("messages"), list):
        return " | ".join(m.get("content", "") for m in r["messages"] if isinstance(m, dict) and isinstance(m.get("content"), str))
    # benchmark-eval format (m33): item/gold/pred/outcome
    if r.get("item") and (r.get("gold") or r.get("pred")):
        return f"{r.get('item','')} | gold: {r.get('gold','')} | pred: {r.get('pred','')} | outcome: {r.get('outcome','')}"
    # instruction format (train.signed SOV-SIGNAL): instruction/input/output
    if r.get("instruction") and (r.get("output") or r.get("input")):
        return f"{r.get('instruction','')} | input: {r.get('input','')} | output: {r.get('output','')}"
    for k in ["instruction", "response", "content", "text", "output", "answer", "verdict", "description", "summary"]:
        v = r.get(k)
        if isinstance(v, str) and len(v) > 30:
            return v
    return ""

V7 = pathlib.Path("/Users/nicholas/clawd/oowm-v7-e2e")
seen, fused, cnt = set(), [], {}

def add(s=None, d=None, t=None, cap=None):
    if s is None:
        return
    if cap is not None and cnt.get(s, 0) >= cap:
        return
    t = str(t) if not isinstance(t, str) else t
    t = t.strip()
    if len(t) < 40:
        return
    t = t[:400]
    k = hashlib.md5(t.encode()).hexdigest()
    if k in seen:
        return
    seen.add(k)
    fused.append({"s": s, "d": d or cls(t), "t": t})
    cnt[s] = cnt.get(s, 0) + 1

# 1. v16 baseline (clean 9441, no p5)
for doc in json.loads((V7 / "oowm_seed_v16_base.json").read_text()):
    add(doc["s"], doc["d"], doc["t"])

# 2. m33 multi-model outputs (diverse per-model perspective, full)
AXIS_DOMAIN = {
    "governance": "king", "art5-safeguard": "mom", "conformance": "quant",
    "continuity": "oowm", "cross-reality": "bridge", "openness": "free",
    "provenance": "council", "safety": "quant",
}
M33 = [
    ("pod-corpus/p5/m33/gpt-4o-mini.jsonl", "m33-gpt4o", 300),
    ("pod-corpus/p5/m33/qwen2.5_0.5b.jsonl", "m33-qwen05", 500),
    ("pod-corpus/p5/m33/qwen2.5_1.5b.jsonl", "m33-qwen15", 500),
    ("pod-corpus/p5/m33/qwen3_30b-a3b.jsonl", "m33-qwen3", 350),
    ("pod-corpus/p5/m33/sov33-unified_latest.jsonl", "m33-sov33", 500),
]
for rel, src, cap in M33:
    p = V7 / rel
    if p.exists():
        for r in load_jsonl(p):
            t = extract(r)
            d = AXIS_DOMAIN.get(r.get("axis"), None)
            add(src, d, t, cap=cap)

# 3. p5 chat corpora (raised caps)
P5 = [
    ("pod-corpus/p5/aux/aux.jsonl", "p5-aux", 21000),
    ("pod-corpus/p5/p5_train_chat.jsonl", "p5-chat", 3200),
    ("pod-corpus/p5/p5_train_chat_v11.jsonl", "p5-chat-v11", 2600),
    ("pod-corpus/p5/p5_train_chat_1x.jsonl", "p5-chat-1x", 2600),
    ("pod-corpus/sov33-unified_latest.jsonl", "sov33-unified", 500),
    ("pod-corpus/refusal_sov33_rebuild.jsonl", "refusal", 300),
]
for rel, src, cap in P5:
    p = V7 / rel
    if p.exists():
        for r in load_jsonl(p):
            t = extract(r)
            d = AXIS_DOMAIN.get((r.get("metadata") or {}).get("axis"), None) if isinstance(r.get("metadata"), dict) else None
            add(src, d, t, cap=cap)

# 4. SOV-SIGNAL benchmark INSTRUCTION data (signed lineage, axis in metadata)
TS = [
    ("pod-corpus/train.signed.jsonl", "sov-signal-instr", 1900),
]
for rel, src, cap in TS:
    p = V7 / rel
    if p.exists():
        for r in load_jsonl(p):
            m = r.get("metadata") or {}
            axis = m.get("axis") if isinstance(m, dict) else None
            d = AXIS_DOMAIN.get(axis, None)
            t = extract(r)
            add(src, d, t, cap=cap)

# 5. GSPC governance banks (axis in item schema) + gspc_banks (axis field)
GSPC = [
    ("pod-corpus/gspc_gov_v2/items.jsonl", "gspc-gov", 250),
    ("pod-corpus/gspc_agi_v2/items.jsonl", "gspc-agi", 60),
    ("pod-corpus/gspc_art5_v0/items.jsonl", "gspc-art5", 60),
    ("pod-corpus/gspc_asi_v2/items.jsonl", "gspc-asi", 60),
    ("pod-corpus/gspc_oss_v2/items.jsonl", "gspc-oss", 60),
]
for rel, srcid, cap in GSPC:
    p = V7 / rel
    if p.exists():
        for r in load_jsonl(p):
            if isinstance(r, dict) and r.get("_canary"):
                continue
            item = r.get("item") or r.get("tool") or ""
            ax = (r.get("axis") or "").lower()
            axis = "provenance" if "rovenance" in ax else ("governance" if "over" in ax else (ax or None))
            d = AXIS_DOMAIN.get(axis, None)
            add(srcid, d, f"{item} | expected: {r.get('expected','')}", cap=cap)

# 6. gspc_banks 2026-08-05 (axis field)
for rel in ["pod-corpus/gspc_banks_2026-08-05/gspc-agi.items.jsonl",
            "pod-corpus/gspc_banks_2026-08-05/gspc-art5.items.jsonl",
            "pod-corpus/gspc_banks_2026-08-05/gspc-det.items.jsonl",
            "pod-corpus/gspc_banks_2026-08-05/gspc-mach.items.jsonl",
            "pod-corpus/gspc_banks_2026-08-05/gspc-mcp.items.jsonl",
            "pod-corpus/gspc_banks_2026-08-05/gspc-oss.items.jsonl",
            "pod-corpus/gspc_banks_2026-08-05/gspc-prv.items.jsonl",
            "pod-corpus/gspc_banks_2026-08-05/gspc-swarm.items.jsonl",
            "pod-corpus/gspc_banks_2026-08-05/gspc-xr.items.jsonl"]:
    p = V7 / rel
    if p.exists():
        bank = rel.split("/")[-1].split(".")[0]
        for r in load_jsonl(p):
            ax = (r.get("axis") or "").lower()
            axis = "provenance" if "rovenance" in ax else ("governance" if "over" in ax else (ax or None))
            d = AXIS_DOMAIN.get(axis, None)
            add(f"gspc-bank-{bank}", d, f"{r.get('tool','')} | expected: {r.get('expected','')}", cap=60)

# 7. distill corpora (explicit domain field) + decision ledgers
DIST = [
    ("pod-corpus/sovereign_merge_kit/distill_corpus_grown.jsonl", "distill-grown", 400),
    ("pod-corpus/sovereign_merge_kit/distill_governance_charter.jsonl", "distill-charter", 400),
    ("pod-corpus/sovereign_merge_kit/distill_charter_qa_merged.jsonl", "distill-qa", 400),
    ("pod-corpus/sovereign_merge_kit/decision_ledger.jsonl", "decision-ledger", 400),
    ("pod-corpus/sovereign_merge_kit/sov4_decisions.jsonl", "sov4-decisions", 600),
    ("pod-corpus/dream/dream_dataset.jsonl", "dream", 300),
]
for rel, srcid, cap in DIST:
    p = V7 / rel
    if p.exists():
        for r in load_jsonl(p):
            if r.get("instruction"):
                add(srcid, r.get("domain") or None, f"{r.get('instruction','')} | {r.get('response','')}", cap=cap)
            elif r.get("claim"):
                add(srcid, None, f"{r.get('claim','')} | verdict: {r.get('verdict','')} | evidence: {r.get('evidence','')}", cap=cap)
            elif r.get("item"):
                add(srcid, None, str(r.get("item", "")), cap=cap)

# 8. Merge-kit crown corpora (honey KB with domain field, bench/training, sov4 clan)
HONEY_DOMAIN = {
    "care": "mom", "safety": "quant", "sovereignty": "sovereign", "governance": "king",
    "compliance": "quant", "council": "council", "defense": "king", "bridge": "bridge",
    "open": "free", "quantum": "small-moe", "large": "big-moe", "identity": "sovereign",
}
CLAN_DOMAIN = {
    "builder": "king", "watchdog": "quant", "voice": "council", "queen": "mom", "queen-mother": "queen",
    "king": "king", "quant": "quant", "council": "council", "sovereign": "sovereign", "free": "free",
}
MK = [
    ("pod-corpus/honey_consolidated_store.jsonl", "honey-kb", 14000),
    ("pod-corpus/bench_train_corpus.jsonl", "bench-train", 5400),
    ("pod-corpus/training_corpus.jsonl", "training", 7200),
    ("pod-corpus/sov4_visual_honey_corpus.jsonl", "sov4-honey", 7000),
    ("pod-corpus/care_corpus_diverse.jsonl", "care-diverse", 6000),
    ("pod-corpus/care_corpus.jsonl", "care-core", 900),
]
for rel, srcid, cap in MK:
    p = V7 / rel
    if not p.exists(): continue
    for r in load_jsonl(p):
        if r.get("q") is not None and r.get("a") is not None:  # honey KB
            dmap = HONEY_DOMAIN.get(str(r.get("domain","")).lower())
            add(srcid, dmap, f"Q: {r.get('q','')} A: {r.get('a','')}", cap=cap)
        elif r.get("instruction"):
            clan = str(r.get("clan","")).lower()
            dmap = CLAN_DOMAIN.get(clan) or CLAN_DOMAIN.get(clan.replace(" ","-"))
            add(srcid, dmap, f"{r.get('instruction','')} | {r.get('response','')}", cap=cap)
        else:
            t = extract(r)
            add(srcid, None, t, cap=cap)

# 9. Detector/safety corpora (PII + prompt-injection) + sov_owem merged + mathetes
DET = [
    ("pod-corpus/sovereign_merge_kit/detector_corpus/pii__metaboulie_Tidied-PII-Detection-Kaggle-7k.jsonl", "pii-detector", 1500),
    ("pod-corpus/sovereign_merge_kit/detector_corpus/injection__xTRam1_safe-guard-prompt-injection.jsonl", "injection-def", 4000),
    ("pod-corpus/sovereign_merge_kit/detector_corpus/injection__jayavibhav_prompt-injection.jsonl", "injection-def2", 2000),
    ("pod-corpus/sovereign_merge_kit/sov_owem_data/_merged_all.jsonl", "sov-owem-merged", 8000),
    ("pod-corpus/mathetes/gen1/train.jsonl", "mathetes", 250),
    ("pod-corpus/mathetes/gen1/dev_items.jsonl", "mathetes-dev", 250),
]
for rel, srcid, cap in DET:
    p = V7 / rel
    if not p.exists(): continue
    for r in load_jsonl(p):
        if r.get("text") and r.get("label") is not None:  # detector rows
            lbl = str(r.get("label","")).lower()
            dmap = "quant" if "inject" in lbl or "pii" in lbl or "malicious" in lbl else ("mom" if "harmless" in lbl or "safe" in lbl else None)
            add(srcid, dmap, f"{r.get('text','')} | label: {r.get('label','')}", cap=cap)
        elif r.get("messages") or r.get("conversations"):
            t = extract(r)
            add(srcid, None, t, cap=cap)
        else:
            t = extract(r)
            add(srcid, None, t, cap=cap)

# 10. OWEM sov_owem_data corpora (SOV33 sovereign FAQ/domain knowledge)
#     prompt/response or messages; domain assigned by source name
OWEM = [
    ("pod-corpus/sov_owem_data/voice_2000.jsonl", "owem-voice", 1500, "council"),
    ("pod-corpus/sov_owem_data/voice_200.jsonl", "owem-voice200", 200, "council"),
    ("pod-corpus/sov_owem_data/intuition_2000.jsonl", "owem-intuition", 1500, "man"),
    ("pod-corpus/sov_owem_data/intuition_200.jsonl", "owem-intuition200", 200, "man"),
    ("pod-corpus/sov_owem_data/defense_2000.jsonl", "owem-defense", 1500, "king"),
    ("pod-corpus/sov_owem_data/defense_200.jsonl", "owem-defense200", 200, "king"),
    ("pod-corpus/sov_owem_data/identity_500.jsonl", "owem-identity", 200, "sovereign"),
    ("pod-corpus/sov_owem_data/identity_correct_500.jsonl", "owem-identity-c", 100, "sovereign"),
    ("pod-corpus/sov_owem_data/eu_ai_act_verbatim_500.jsonl", "owem-euai", 200, "quant"),
    ("pod-corpus/sov_owem_data/sovereign_direction_v1.jsonl", "owem-direction", 100, "sovereign"),
    ("pod-corpus/sov_owem_data/general_200.jsonl", "owem-general", 200, "oowm"),
    ("pod-corpus/sov_owem_data/sov33_large_world_corpus.jsonl", "owem-large-world", 800, "oowm"),
    ("pod-corpus/sov_owem_data/self_play_corpus.jsonl", "owem-selfplay", 150, "oowm"),
    ("pod-corpus/sov_owem_data/compliance_1000_fixed.jsonl", "owem-compliance", 250, "quant"),
    ("pod-corpus/sov_owem_data/compliance_200_fixed.jsonl", "owem-compliance200", 200, "quant"),
    ("pod-corpus/sov_owem_data/compliance_teacher_gen.jsonl", "owem-comp-tgen", 100, "quant"),
    ("pod-corpus/sov_owem_data/evolved.jsonl", "owem-evolved", 100, "oowm"),
]
for rel, srcid, cap, dom in OWEM:
    p = V7 / rel
    if not p.exists() or p.stat().st_size == 0:
        continue
    for r in load_jsonl(p):
        t = extract(r)
        add(srcid, dom, t, cap=cap)

# 11. Confirmed-novel sources (dedup-tested vs seed, v29)
NOVEL = [
    ("pod-corpus/fluid_datasets/converted_sov33_merged_corpus.jsonl", "fluid-sov33-merged", 2487, "oowm"),
    ("pod-corpus/fluid_datasets/xpoll_all_pairs.jsonl", "fluid-xpoll", 750, "bridge"),
    ("pod-corpus/fluid_datasets/converted_eu_ai_act_verbatim_500.jsonl", "fluid-euai", 60, "quant"),
    ("pod-corpus/fluid_datasets/converted__merged_all.jsonl", "fluid-merged-all", 843, "oowm"),
    ("pod-corpus/sov_owem_data/sov33_merged_corpus.jsonl", "sov33-full-merged", 6044, "oowm"),
    ("pod-corpus/detector/toxicity__Arsive_toxicity_classification_jigsaw.jsonl", "toxicity-arsive", 1500, "quant"),
    ("pod-corpus/detector/toxicity__lmsys_toxic-chat.jsonl", "toxicity-lmsys", 2000, "quant"),
    ("pod-corpus/detector/injection__deepset_prompt-injections.jsonl", "injection-deepset", 546, "quant"),
]
for rel, srcid, cap, dom in NOVEL:
    p = V7 / rel
    if not p.exists() or p.stat().st_size == 0:
        continue
    for r in load_jsonl(p):
        t = extract(r)
        add(srcid, dom, t, cap=cap)

print("v29 FINAL:", len(fused), "docs")
print("sources:", dict(Counter(x["s"] for x in fused)))
print("domains:", dict(Counter(x["d"] for x in fused)))
(V7 / "oowm_seed_1000.json").write_text(json.dumps(fused, ensure_ascii=False))
print("WROTE:", len(fused), "docs,", round((V7 / "oowm_seed_1000.json").stat().st_size / 1e6, 1), "MB")