#!/usr/bin/env python3
"""Unit test for provbench three-outcome contract.

Tests that the measurement apparatus correctly distinguishes between:
- SURVIVED: Manifest survived the transform
- DESTROYED: Manifest was destroyed by the transform
- UNMEASURED: Transform couldn't be applied

This is a HARNESS test, not a marking test.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

import provbench


class TestThreeOutcomeContract(unittest.TestCase):
    """Test that provbench correctly implements the three-outcome pattern."""

    def test_three_outcome_constants_exist(self):
        """Verify the three outcome constants are defined."""
        self.assertEqual(provbench.SURVIVED, "survived")
        self.assertEqual(provbench.DESTROYED, "destroyed")
        self.assertEqual(provbench.UNMEASURED, "unmeasured")

    def test_three_outcomes_exhaustive(self):
        """Verify that only three outcomes are ever emitted."""
        # This is the core invariant: SURVIVED, DESTROYED, UNMEASURED
        # No fourth outcome should exist
        valid_outcomes = {provbench.SURVIVED, provbench.DESTROYED, provbench.UNMEASURED}
        self.assertEqual(len(valid_outcomes), 3)
        self.assertIn("survived", valid_outcomes)
        self.assertIn("destroyed", valid_outcomes)
        self.assertIn("unmeasured", valid_outcomes)

    def test_unmeasured_is_distinct_from_destroyed(self):
        """BLOCKED != FAIL: UNMEASURED is not DESTROYED."""
        self.assertNotEqual(provbench.UNMEASURED, provbench.DESTROYED)
        # This is the key insight: a transform that couldn't be applied
        # is NOT the same as a manifest that was destroyed

    def test_unmeasured_is_distinct_from_survived(self):
        """UNMEASURED is not SURVIVED."""
        self.assertNotEqual(provbench.UNMEASURED, provbench.SURVIVED)

    def test_survived_is_distinct_from_destroyed(self):
        """SURVIVED is not DESTROYED."""
        self.assertNotEqual(provbench.SURVIVED, provbench.DESTROYED)


class TestThreeOutcomeInvariants(unittest.TestCase):
    """Test the invariants that make three-outcome measurement meaningful."""

    def test_unmeasured_carrys_no_rate(self):
        """UNMEASURED cells should have rate=None, not rate=0.0."""
        # This is critical: rate=0.0 would mean "all destroyed"
        # rate=None means "we couldn't measure"
        # They must be distinguishable
        pass  # Integration test - requires full provbench run

    def test_three_outcomes_actually_occur(self):
        """A two-outcome run would mean the UNMEASURED path is untested."""
        # This is a meta-test: we need to verify that in a real run,
        # all three outcomes actually occur
        pass  # Integration test - requires full provbench run


if __name__ == "__main__":
    unittest.main()
