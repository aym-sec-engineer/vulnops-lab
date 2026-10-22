import pytest

from src.prioritizer import calculate_risk
from src.scanner import check_php_version


@pytest.mark.parametrize(
    "version, expected",
    [
        ("8.3.35", "POTENTIALLY_VULNERABLE"),
        ("8.3.36", "PATCHED_UPSTREAM"),
        ("8.4.26", "POTENTIALLY_VULNERABLE"),
        ("8.4.27", "PATCHED_UPSTREAM"),
        ("8.2.34", "POTENTIALLY_VULNERABLE"),
        ("8.2.35", "PATCHED_UPSTREAM"),
        ("8.5.11", "POTENTIALLY_VULNERABLE"),
        ("8.5.12", "PATCHED_UPSTREAM"),
        ("7.4.33", "UNSUPPORTED"),
        ("invalid", "UNKNOWN"),
        ("9.0.0", "REVIEW_REQUIRED"),
        ("8.6.0", "REVIEW_REQUIRED"),
    ],
)
def test_php_versions(version, expected):
    assert check_php_version(version) == expected


def test_critical_internet_application():
    app = {
        "exposure": "internet",
        "business_criticality": "critical",
    }

    result = calculate_risk(app, "POTENTIALLY_VULNERABLE")

    assert result == 100


def test_internal_medium_application():
    app = {
        "exposure": "internal",
        "business_criticality": "medium",
    }

    result = calculate_risk(app, "POTENTIALLY_VULNERABLE")

    assert result == 55


def test_patched_application():
    app = {
        "exposure": "internet",
        "business_criticality": "critical",
    }

    result = calculate_risk(app, "PATCHED_UPSTREAM")

    assert result == 0


def test_unknown_status():
    app = {
        "exposure": "internet",
        "business_criticality": "high",
    }

    result = calculate_risk(app, "UNKNOWN")

    assert result is None
