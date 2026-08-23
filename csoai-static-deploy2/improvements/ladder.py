# LADDER: recursive self-improvement (1% to 82%)
# Paper: arxiv:2503
class Ladder:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.data = []
    def generate_variants(self, problem, depth=0):
        if depth >= self.max_depth: return [problem]
        variants = [problem]
        for i in range(3):
            s = self._simplify(problem, depth)
            if s and s != problem: variants.extend(self.generate_variants(s, depth+1))
        return variants
    def _simplify(self, problem, depth):
        if "factorial" in problem.lower():
            return ["What is 5 factorial?", "What is 3 factorial?", "What is 2 factorial?"][min(depth,2)]
        return problem
