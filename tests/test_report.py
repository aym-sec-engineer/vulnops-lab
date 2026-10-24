from src.report import analyze_inventory, build_report, to_markdown


def sample_inventory():
    return {
        "incident": {
            "id": "TEST-INCIDENT",
            "cves": [],
        },
        "applications": [
            {
                "id": "APP-TEST-1",
                "name": "public-app",
                "php_version": "8.3.35",
                "exposure": "internet",
                "business_criticality": "high",
            },
            {
                "id": "APP-TEST-2",
                "name": "patched-app",
                "php_version": "8.3.36",
                "exposure": "internal",
                "business_criticality": "medium",
            },
        ],
    }


def test_report_counts():
    report = build_report(sample_inventory())

    assert report["summary"]["total"] == 2
    assert report["summary"]["potentially_vulnerable"] == 1
    assert report["summary"]["patched_upstream"] == 1


def test_results_sorted_by_risk():
    results = analyze_inventory(sample_inventory())

    assert results[0]["id"] == "APP-TEST-1"
    assert results[0]["risk_score"] == 90


def test_markdown_contains_findings():
    report = build_report(sample_inventory())
    markdown = to_markdown(report)

    assert "public-app" in markdown
    assert "patched-app" in markdown
    assert "TEST-INCIDENT" in markdown
