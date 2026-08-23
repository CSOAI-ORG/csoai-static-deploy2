import os
from pathlib import Path
import tempfile
import unittest

import sov_invariants
import sovereign_api
import sov4_router
import sov6_stack


class SovereignRuntimeAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous_key = os.environ.get("SOV_SIGIL_KEY_PATH")
        os.environ["SOV_SIGIL_KEY_PATH"] = str(Path(self.temp.name) / "sigil.key")
        sov_invariants._CHAIN_HEAD = sov_invariants.SIGIL_ROOT

    def tearDown(self):
        if self.previous_key is None:
            os.environ.pop("SOV_SIGIL_KEY_PATH", None)
        else:
            os.environ["SOV_SIGIL_KEY_PATH"] = self.previous_key
        self.temp.cleanup()

    def test_ed25519_chain_and_verification(self):
        first = sov_invariants.emit_sigil("first", {"approve": 28, "amend": 5, "reject": 0}, 0.95)
        second = sov_invariants.emit_sigil("second", {"approve": 28, "amend": 5, "reject": 0}, 0.96)
        self.assertEqual(first["algorithm"], "Ed25519")
        self.assertTrue(sov_invariants.verify_sigil(first, "first"))
        self.assertEqual(second["prev_hash"], first["root_hash"])

    def test_care_floor_cannot_be_lowered(self):
        with self.assertRaises(ValueError):
            sovereign_api.sovereign_call("A safe and sufficiently detailed request", care_floor=0.90)

    def test_owem_alias_is_canonical(self):
        result = sovereign_api.sovereign_call("Explain a safe compliance audit process in detail", owem="defence")
        self.assertEqual(result.owem["id"], "defense")
        self.assertEqual(result.sigil.algorithm, "Ed25519")

    def test_invalid_bft_tally_is_rejected(self):
        with self.assertRaises(ValueError):
            sov_invariants.validate_tally({"approve": 22, "amend": 0, "reject": 0})

    def test_sov6_short_output_is_governed(self):
        result = sov6_stack._governed_result("Explain a safe process", {"ok": True, "response": "A"}, "vision")
        self.assertTrue(result["ok"])
        self.assertEqual(result["capability"], "visual_reasoning")
        self.assertEqual(result["sigil"]["algorithm"], "Ed25519")

    def test_sov4_capability_alias_routes_to_native_vision(self):
        router = sov4_router.Sov4Router.__new__(sov4_router.Sov4Router)
        router.avoid = {}
        router.avoid_threshold = sov4_router.AVOID_THRESHOLD
        router.local_url = "local"
        router.a40_url = "a40"
        router.h100_url = "h100"
        router.runpod_url = ""
        router.allow_a40 = False
        router.allow_h100 = False
        router.allow_runpod = False
        router.allow_serverless = False
        router.host_alive = {"local": True, "a40": False, "h100": False}
        router._rr = 0
        router.stats = {"fallback_swaps": 0}
        route = router.route("vision", {})
        self.assertEqual(route["model"], "llava:7b")


if __name__ == "__main__":
    unittest.main()
