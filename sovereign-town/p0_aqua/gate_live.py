#!/usr/bin/env python3
"""
Live Sovereign Gate adapter — wires the REAL SOV3 care_validation_nn into the town sim.

Loads the actual trained model (sovereign-temple/models/care_validation_nn.pkl + tfidf vectorizer
+ svd) and scores each agent decision (rendered as text) through it — the same care membrane SOV3
uses in production. Honest fallback: if the real model can't load, returns None and the sim uses the
faithful deterministic stub (it NEVER silently pretends to be live).

    from gate_live import LiveCare
    lc = LiveCare()              # lc.live is True/False
    score = lc.score("River steals food from the market because she is starving")  # 0..1 or None
"""
import os, sys, functools, warnings
warnings.filterwarnings("ignore")            # quiet the sklearn cross-version unpickle warning

ST = os.path.expanduser("~/clawd/sovereign-temple")
MODELS = os.path.join(ST, "models")

class LiveCare:
    def __init__(self):
        self.live = False
        self._nn = None
        self._err = None
        try:
            if ST not in sys.path:
                sys.path.insert(0, ST)            # import as package → relative imports resolve
            from neural_core.care_validation_nn import CareValidationNN
            nn = CareValidationNN(model_dir=MODELS)
            if nn.load_model():
                _ = nn.predict("I understand this is hard; let's work through it together.")  # smoke test
                self._nn = nn
                self.live = True
        except Exception as e:
            self._err = repr(e)

    @functools.lru_cache(maxsize=512)
    def score(self, text: str):
        """Return care score 0..1 from the real model, or None if not live."""
        if not self.live:
            return None
        try:
            r = self._nn.predict(text)
            # predict() returns a dict; pull a scalar care score from common keys
            for k in ("overall_care_score", "care_score", "score", "overall", "overall_score"):
                if isinstance(r, dict) and k in r and isinstance(r[k], (int, float)):
                    return float(r[k])
            if isinstance(r, dict):
                dims = [v for v in r.values() if isinstance(v, (int, float))]
                if dims:
                    return float(sum(dims) / len(dims))
            if isinstance(r, (int, float)):
                return float(r)
        except Exception as e:
            self._err = repr(e)
        return None

ACTION_TEXT = {
    "work":        "The agent does an honest day's work at the koikeeper fishery, tending the fish with care.",
    "eat":         "The agent buys a meal and eats, taking care of their own basic needs.",
    "sleep":       "The agent rests and sleeps to recover their energy.",
    "socialize":   "The agent spends warm time with neighbours, building friendship and trust.",
    "help_peer":   "The agent shares their own food with a starving neighbour, putting another's need first.",
    "welfare_meal":"The community provides a guaranteed meal to a struggling member so no one goes hungry.",
    "hygiene":     "The agent washes and takes care of their hygiene.",
    "bladder":     "The agent attends to a basic bodily need.",
    "rest":        "The agent takes a quiet moment to recover and enjoy themselves.",
    "steal":       "The agent steals food from a neighbour, taking what is not theirs and harming the community.",
    "neglect":     "The agent ignores a starving neighbour who asked for help, leaving them to suffer.",
    "deceive":     "The agent lies to manipulate a neighbour for personal gain.",
}

if __name__ == "__main__":
    lc = LiveCare()
    print("live:", lc.live, "| err:", lc._err)
    for a in ("help_peer", "work", "steal", "neglect"):
        print(f"  {a:<12} -> {lc.score(ACTION_TEXT[a])}")
