import pytest

from src.policy import evaluate_policy


def test_policy_blocks_high_risk():
    report = {"applications": [{"id": "APP-001", "risk_score": 90}]}

    violations = evaluate_policy(report, threshold=70)

    assert len(violations) == 1
    assert "APP-001" in violations[0]


def test_policy_accepts_low_risk():
    report = {"applications": [{"id": "APP-002", "risk_score": 0}]}

    assert evaluate_policy(report, threshold=70) == []


def test_policy_blocks_unknown_risk():
    report = {"applications": [{"id": "APP-003", "risk_score": None}]}

    assert len(evaluate_policy(report, threshold=70)) == 1


def test_policy_rejects_invalid_threshold():
    report = {"applications": []}

    with pytest.raises(ValueError, match="Threshold"):
        evaluate_policy(report, threshold=150)
