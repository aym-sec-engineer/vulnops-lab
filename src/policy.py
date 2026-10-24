import argparse
import json
from pathlib import Path

from src.report import build_report


def evaluate_policy(report, threshold=70):
    if not 0 <= threshold <= 100:
        raise ValueError("Threshold must be between 0 and 100")

    violations = []

    for app in report["applications"]:
        score = app["risk_score"]

        if score is None:
            violations.append(f"{app['id']}: manual review required")
        elif score >= threshold:
            violations.append(f"{app['id']}: risk {score} >= {threshold}")

    return violations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--threshold", type=int, default=70)
    args = parser.parse_args()

    with args.inventory.open(encoding="utf-8") as file:
        inventory = json.load(file)

    report = build_report(inventory)
    violations = evaluate_policy(report, args.threshold)

    if violations:
        print("VERSION TRIAGE POLICY: FAIL")
        for violation in violations:
            print(f" - {violation}")
        return 1

    print("VERSION TRIAGE POLICY: PASS")
    print("Note: installed patches are NOT verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
