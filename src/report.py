import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from src.prioritizer import calculate_risk
from src.scanner import check_php_version
from src.validation import validate_inventory

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INVENTORY = ROOT / "data" / "inventory.json"
DEFAULT_REPORTS = ROOT / "reports"


def get_remediation_verification(app):
    patch_status = app.get("patch_status", "unknown")

    if patch_status == "simulated":
        return "SIMULATED_ONLY"

    return "NOT_VERIFIED"


def analyze_inventory(inventory):
    validate_inventory(inventory)
    results = []

    for app in inventory["applications"]:
        status = check_php_version(app["php_version"])
        score = calculate_risk(app, status)

        results.append(
            {
                "id": app["id"],
                "name": app["name"],
                "php_version": app["php_version"],
                "status": status,
                "remediation_verification": get_remediation_verification(app),
                "risk_score": score,
                "exposure": app["exposure"],
                "business_criticality": app["business_criticality"],
            }
        )

    return sorted(
        results,
        key=lambda item: (
            item["risk_score"] is not None,
            item["risk_score"] or 0,
        ),
        reverse=True,
    )


def build_report(inventory):
    results = analyze_inventory(inventory)

    return {
        "incident": inventory["incident"],
        "generated_at": datetime.now(UTC).isoformat(),
        "environment": "FICTIONAL_LAB",
        "disclaimer": (
            "Static version analysis only. No live vulnerability "
            "scan or confirmed remediation."
        ),
        "summary": {
            "total": len(results),
            "potentially_vulnerable": sum(
                r["status"] == "POTENTIALLY_VULNERABLE" for r in results
            ),
            "unsupported": sum(r["status"] == "UNSUPPORTED" for r in results),
            "patched_upstream": sum(r["status"] == "PATCHED_UPSTREAM" for r in results),
            "requires_review": sum(r["risk_score"] is None for r in results),
        },
        "applications": results,
    }


def to_markdown(report):
    summary = report["summary"]

    lines = [
        "# VulnOps — Security Assessment",
        "",
        f"**Incident:** {report['incident']['id']}",
        f"**Generated:** {report['generated_at']}",
        "**Environment:** Fictional laboratory",
        "",
        "## Executive summary",
        "",
        f"- Applications analyzed: {summary['total']}",
        f"- Potentially vulnerable: {summary['potentially_vulnerable']}",
        f"- Unsupported: {summary['unsupported']}",
        f"- Patched upstream: {summary['patched_upstream']}",
        f"- Requiring review: {summary['requires_review']}",
        "",
        "## Prioritized findings",
        "",
        "| Application | PHP | Status | Version risk | Verification |",
        "|---|---|---|---|---|",
    ]

    for app in report["applications"]:
        score = app["risk_score"]
        score_text = str(score) if score is not None else "REVIEW"

        lines.append(
            f"| {app['name']} | {app['php_version']} | "
            f"{app['status']} | {score_text} | "
            f"{app['remediation_verification']} |"
        )

    lines.extend(
        [
            "",
            "## Recommended actions",
            "",
            "1. Verify vendor advisories and installed package releases.",
            "2. Prioritize exposed and business-critical assets.",
            "3. Plan and approve patches or supported-version migration.",
            "4. Test application behavior and deployment rollback.",
            "5. Confirm remediation using evidence from target systems.",
            "",
            "## Limitations",
            "",
            "- The inventory is fictional and manually maintained.",
            "- Upstream versions do not prove installed patch status.",
            "- Vendor backports are not automatically verified.",
            "- No exploitation or live infrastructure assessment.",
            "- Risk scores are illustrative and not CVSS values.",
            "",
        ]
    )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_REPORTS)
    args = parser.parse_args()

    with args.inventory.open(encoding="utf-8") as file:
        inventory = json.load(file)

    report = build_report(inventory)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    json_path = args.output_dir / "security-report.json"
    markdown_path = args.output_dir / "security-report.md"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    markdown_path.write_text(to_markdown(report), encoding="utf-8")

    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")
    print(f"Applications analyzed: {report['summary']['total']}")


if __name__ == "__main__":
    main()
