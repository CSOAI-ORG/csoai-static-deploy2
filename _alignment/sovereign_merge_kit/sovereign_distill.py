#!/usr/bin/env python3
"""sovereign_distill.py — the REAL 'train correctly & fast' move: DISTILLATION.
NVIDIA's free hosted BIG model (up to 405B) is the TEACHER — it GENERATES high-quality training data.
Your small sovereign model is the STUDENT — trained on that data (QLoRA) on a free Colab/Kaggle GPU.
Big model teaches small model. This is how you get a genuinely smarter sovereign WITHOUT owning big GPUs.

Honest split:
  - NVIDIA API = INFERENCE (teacher generates data + answers). You do NOT train on it.
  - Free GPU (Colab) = TRAINING (student QLoRA on the generated data). Small models, but REAL.
  - This script = the teacher step. Output feeds sov33_gpu_fire.py on the GPU.

Keys come from env (NVIDIA_API_KEY etc.) — never handled here. Falls back to local if no key (lower quality).
"""
import os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sovereign_router import dispatch, available
from sovereign_kb import kb

def gen_examples(n_per_fact=2):
    KB = kb(); out = []
    for src, fact in KB:
        for i in range(n_per_fact):
            prompt = (f"You are teaching a smaller AI. Based ONLY on this fact, write ONE realistic user QUESTION "
                      f"and a correct, concise ANSWER that cites [{src}]. Return JSON: "
                      f'{{"instruction": "...", "response": "..."}}.\nFACT ({src}): {fact}')
            ans, who = dispatch(prompt, system="You generate clean instruction/response training pairs.",
                                tier="smart", max_tokens=300)
            if not ans: continue
            try:
                j = json.loads(ans[ans.find("{"):ans.rfind("}")+1])
                if j.get("instruction") and j.get("response"):
                    j["_teacher"] = who; j["_source"] = src; out.append(j)
            except Exception:
                out.append({"instruction": f"About {src}: explain the key rule.", "response": ans[:400], "_teacher": who, "_source": src})
    return out

def main():
    av = available()
    teacher_ok = any(k in av for k in ("nvidia","glm","minimax","groq"))
    print(f"=== SOVEREIGN DISTILL — teacher backends available: {av} ===")
    if not teacher_ok:
        print("No hosted teacher configured (best = NVIDIA 405B). Set NVIDIA_API_KEY to use a big teacher;")
        print("without it, generation falls back to the local small model (low quality — set the key).")
    ex = gen_examples(n_per_fact=int(os.environ.get("SOV_N_PER_FACT","2")))
    path = "expert_data/sovereign_distilled.jsonl"
    os.makedirs("expert_data", exist_ok=True)
    with open(path, "w") as f:
        for e in ex: f.write(json.dumps({"instruction": e["instruction"], "response": e["response"]}) + "\n")
    teachers = sorted(set(e.get("_teacher") for e in ex))
    print(f"\ngenerated {len(ex)} training pairs (teachers: {teachers}) -> {path}")
    print("Next: on a free Colab/Kaggle GPU, run sov33_gpu_fire.py (QLoRA) on this jsonl to train the student.")
    if ex: print("\nsample:", json.dumps(ex[0], ensure_ascii=False)[:300])

if __name__ == "__main__":
    main()
