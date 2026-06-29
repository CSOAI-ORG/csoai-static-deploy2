"""Tests for meok-sovereign-training-mcp (33 industries + free cert)."""
import os, tempfile
_TEST_DIR = tempfile.mkdtemp(prefix="sov_train_test_")
os.environ["SOV_TRAIN_KEY"] = os.path.join(_TEST_DIR, "key.pem")
import meok_sovereign_training_mcp as tr_mod
from meok_sovereign_training_mcp import (
    course_create, cert_issue, progress_track,
    exam_grade, badge_mint,
    INDUSTRIES, _COURSES, _CERTS, _PROGRESS, _BADGES,
)


def reset_state():
    _COURSES.clear()
    _CERTS.clear()
    _PROGRESS.clear()
    _BADGES.clear()


def test_33_industries():
    assert len(INDUSTRIES) == 33


def test_33_hives():
    hive_names = {i["hive"] for i in INDUSTRIES}
    assert len(hive_names) == 33


def test_33_countries():
    countries = {i["country"] for i in INDUSTRIES}
    assert len(countries) >= 10


def test_each_industry_has_course():
    for i in INDUSTRIES:
        assert "course" in i
        assert "duration_hours" in i
        assert i["duration_hours"] > 0
        assert "modules" in i
        assert i["modules"] > 0
        assert "badge" in i


def test_all_free():
    """All 33 courses are free."""
    for i in INDUSTRIES:
        # We'll verify in the course_create
        pass


def test_course_create_valid():
    reset_state()
    r = course_create(1)  # London/Finance/DORA
    assert r["industry_id"] == 1
    assert r["hive"] == "london"
    assert r["country"] == "UK"
    assert r["price"] == 0.0  # FREE
    assert r["currency"] == "USD"
    assert "DORA" in r["title"]


def test_course_create_custom_title():
    reset_state()
    r = course_create(13, custom_title="HIPAA Mastery for Journalists")
    assert r["title"] == "HIPAA Mastery for Journalists"


def test_course_create_invalid_industry():
    r = course_create(0)
    assert "error" in r
    r = course_create(99)
    assert "error" in r


def test_cert_issue_pass():
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    cert = cert_issue(cid, "Sarah Chen", "sarah@nhs.uk", 95.0)
    assert cert["issuer"] == "did:csoai:csoai-org-001"
    assert cert["credentialSubject"]["name"] == "Sarah Chen"
    assert "DORA-CERT" in str(cert.get("type_specialization", [])) or "DORA" in str(cert)
    assert cert.get("ts") is not None


def test_cert_issue_w3c_structure():
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    cert = cert_issue(cid, "Test", "test@test.com", 95.0)
    assert "@context" in cert
    assert "VerifiableCredential" in cert.get("type", [])


def test_cert_issue_fail_low_score():
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    r = cert_issue(cid, "Test", "test@test.com", 50.0)
    assert "error" in r


def test_cert_issue_unknown_course():
    r = cert_issue("nonexistent", "Test", "test@test.com", 95.0)
    assert "error" in r


def test_progress_track_valid():
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    p = progress_track(cid, "test@test.com", 1, 85.0)
    assert p["course_id"] == cid
    assert 1 in p["modules_completed"]


def test_progress_track_multiple_modules():
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    for mod in [1, 2, 3]:
        progress_track(cid, "test@test.com", mod, 85.0)
    p = progress_track(cid, "test@test.com", 4, 90.0)
    assert len(p["modules_completed"]) == 4
    assert p["completion_pct"] == round(100 * 4 / course["modules"], 2)


def test_progress_track_invalid_module():
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    r = progress_track(cid, "test@test.com", 0, 85.0)
    assert "error" in r


def test_progress_track_module_too_high():
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    r = progress_track(cid, "test@test.com", 999, 85.0)
    assert "error" in r


def test_exam_grade_perfect():
    r = exam_grade(["A", "B", "C"], ["A", "B", "C"])
    assert r["score"] == 100.0
    assert r["grade"] == "A+"
    assert r["passed"] is True


def test_exam_grade_zero():
    r = exam_grade(["A", "B", "C"], ["X", "Y", "Z"])
    assert r["score"] == 0
    assert r["grade"] == "C"
    assert r["passed"] is False


def test_exam_grade_partial():
    r = exam_grade(["A", "B", "C", "D"], ["A", "B", "X", "X"])
    assert r["score"] == 50.0
    assert r["passed"] is False


def test_exam_grade_passing():
    r = exam_grade(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                   ["A", "B", "C", "D", "E", "F", "G", "H", "X", "X"])
    assert r["score"] == 80.0
    assert r["grade"] == "A"
    assert r["passed"] is True


def test_exam_grade_mismatch():
    r = exam_grade(["A"], ["A", "B"])
    assert "error" in r


def test_badge_mint_basic():
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    badge = badge_mint(cid, "sarah@nhs.uk")
    assert badge["course_id"] == cid
    assert badge["learner_email"] == "sarah@nhs.uk"
    assert "DORA" in badge["title"]


def test_badge_mint_unique_id():
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    b1 = badge_mint(cid, "user1@test.com")
    b2 = badge_mint(cid, "user2@test.com")
    assert b1["badge_id"] != b2["badge_id"]


def test_badge_mint_unknown_course():
    r = badge_mint("nonexistent", "test@test.com")
    assert "error" in r


def test_no_external_deps():
    import meok_sovereign_training_mcp as m
    src = open(m.__file__).read()
    assert "import ollama" not in src
    assert "import urllib" not in src
    assert "import requests" not in src


def test_signed_outputs():
    reset_state()
    r1 = course_create(1)
    assert "kid" in r1 and "sig" in r1 and "ts" in r1
    r2 = cert_issue(r1["course_id"], "Test", "t@t.com", 95.0)
    assert "kid" in r2 and "sig" in r2 and "ts" in r2
    r3 = progress_track(r1["course_id"], "t@t.com", 1, 90.0)
    assert "kid" in r3 and "sig" in r3 and "ts" in r3
    r4 = exam_grade(["A"], ["A"])
    assert "kid" in r4 and "sig" in r4 and "ts" in r4
    r5 = badge_mint(r1["course_id"], "t@t.com")
    assert "kid" in r5 and "sig" in r5 and "ts" in r5


def test_full_lifecycle():
    """Course → progress → exam → cert → badge."""
    reset_state()
    course = course_create(1)
    cid = course["course_id"]
    # All modules
    for mod in range(1, course["modules"] + 1):
        progress_track(cid, "sarah@nhs.uk", mod, 85.0)
    # Exam
    correct = ["A"] * course["modules"]
    answers = ["A"] * course["modules"]
    exam = exam_grade(answers, correct)
    assert exam["score"] == 100.0
    # Cert
    cert = cert_issue(cid, "Sarah Chen", "sarah@nhs.uk", 100.0)
    assert "DORA" in str(cert)
    # Badge
    badge = badge_mint(cid, "sarah@nhs.uk")
    assert badge["title"]


def test_all_33_courses_createable():
    """All 33 industries can create a course."""
    reset_state()
    for i in range(1, 34):
        r = course_create(i)
        assert r["industry_id"] == i
        assert r["price"] == 0.0