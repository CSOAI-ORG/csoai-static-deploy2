from governance_crosswalk_server import crosswalk, frameworks_loaded, handle_tool_call, FRAMEWORKS


def test_frameworks_loaded():
    f = frameworks_loaded()
    assert "EU_AI_ACT" in f
    assert "NIST_RMF" in f
    assert len(f) == 6
    print(f"  ✅ frameworks: {f}")


def test_crosswalk_returns_entries():
    results = crosswalk("EU AI Act Article 5")
    assert len(results) >= 1
    assert all("source" in r for r in results)
    assert all("nist_rmf" in r for r in results)
    print(f"  ✅ crosswalk returned {len(results)} entries")


def test_crosswalk_empty_query():
    assert crosswalk("") == []
    assert crosswalk("   ") == []
    print("  ✅ empty query → empty result")


def test_handle_tool_call():
    r1 = handle_tool_call("frameworks", {})
    assert "frameworks" in r1
    r2 = handle_tool_call("crosswalk", {"query": "GDPR"})
    assert "results" in r2
    r3 = handle_tool_call("unknown_tool", {})
    assert "error" in r3
    print("  ✅ tool dispatch works")


def main():
    tests = [test_frameworks_loaded, test_crosswalk_returns_entries,
             test_crosswalk_empty_query, test_handle_tool_call]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"  ❌ FAIL: {e}")
            failed += 1
    if failed:
        print(f"\n❌ {failed}/{len(tests)} tests FAILED")
        return 1
    print(f"\n✅ {len(tests)}/{len(tests)} tests PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())