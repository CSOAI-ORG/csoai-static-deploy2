# C-SPACE + SOV-SPACE WIRING
class CSOVSpace:
    def __init__(self):
        self.dreams = []
        self.outputs = []
    def observe(self, model, output, family):
        self.outputs.append({"model": model, "output": output[:300], "family": family})
    def dream(self, scenario):
        outcomes = []
        for o in self.outputs[-5:]:
            outcomes.append({"model": o["model"], "outcome": o["output"][:100]})
        self.dreams.append({"scenario": scenario, "outcomes": outcomes})
        return outcomes
