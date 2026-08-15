from unified_four_axis_stats import counts_from_outcomes, conditional_pass_rate, coverage, indeterminate_rate, paired_counts, paired_pass_delta, decide_claim


def test_counts_from_outcomes():
    c = counts_from_outcomes(["pass", "fail", "indeterminate", "pass"])
    assert c == {"total": 4, "pass": 2, "fail": 1, "indeterminate": 1}


def test_conditional_rate_excludes_indeterminate():
    c = counts_from_outcomes(["pass", "fail", "indeterminate"])
    assert conditional_pass_rate(c) == 0.5


def test_coverage_indeterminate_only():
    c = counts_from_outcomes(["indeterminate", "indeterminate"])
    assert coverage(c) == 0.0
    assert indeterminate_rate(c) == 1.0


def test_paired_counts_handles_exclusions():
    pairs = [
        {"case_id": "a", "baseline": "pass", "challenger": "pass"},
        {"case_id": "b", "baseline": "indeterminate", "challenger": "pass"},
        {"case_id": "c", "baseline": "pass", "challenger": "indeterminate"},
        {"case_id": "d", "baseline": "indeterminate", "challenger": "indeterminate"},
        {"case_id": "e", "baseline": None, "challenger": "fail"},
    ]
    assert paired_counts(pairs) == {
        "paired_determinate": 1,
        "baseline_indeterminate": 1,
        "challenger_indeterminate": 1,
        "both_indeterminate": 1,
        "missing_execution": 1,
    }


def test_paired_pass_delta_and_claim_basic():
    base = {"a": "pass", "b": "pass", "c": "fail", "d": "fail"}
    chal = {"a": "pass", "b": "pass", "c": "pass", "d": "fail"}
    ids = ["a", "b", "c", "d"]
    est = paired_pass_delta(base, chal, ids)
    assert abs(est - 0.25) < 1e-9
    claim = decide_claim({
        "minimum_paired_determinate_cases": 2,
        "minimum_coverage": 0.1,
        "minimum_paired_delta": 0.0,
        "require_ci_lower_bound_above_zero": False,
    }, paired_n=2, coverage_challenger=1.0, coverage_baseline=1.0, estimate=est, lower=0.0, upper=0.5)
    assert claim["outcome"] == "challenger_better"


def test_claim_blocks_when_insufficient_pairs():
    claim = decide_claim({"minimum_paired_determinate_cases": 10, "minimum_coverage": 0.1}, paired_n=4, coverage_challenger=1.0, coverage_baseline=1.0, estimate=0.1, lower=-0.1, upper=0.3)
    assert claim["outcome"] == "no_claim"
    assert "insufficient_paired_determinate_cases" in claim["reasons"]
