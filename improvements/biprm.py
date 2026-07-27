# BIPRM: bidirectional PRM (+10.6%)
# Paper: arxiv:2508.01682
class BiPRM:
    def evaluate(self, steps):
        if not steps: return 0.0
        fwd = 1.0
        for s in steps[1:]:
            if any(w in s.lower() for w in ["therefore","thus","hence"]): fwd *= 1.0
            elif any(w in s.lower() for w in ["however","but"]): fwd *= 0.9
        if len(steps) < 2: return fwd
        conclusion = steps[-1].lower()
        premises = " ".join(steps[:-1]).lower()
        overlap = len(set(premises.split()) & set(conclusion.split()))
        bwd = min(1.0, overlap / max(1, len(conclusion.split())))
        return (fwd + bwd) / 2.0
