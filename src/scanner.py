import json
from pathlib import Path

from packaging.version import InvalidVersion, Version

from src.prioritizer import calculate_risk

PATCHED_VERSIONS = {
    "8.2": "8.2.35",
    "8.3": "8.3.36",
    "8.4": "8.4.27",
    "8.5": "8.5.12",
}

INVENTORY_PATH = Path(__file__).resolve().parent.parent / "data" / "inventory.json"


def load_inventory():
    with INVENTORY_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def check_php_version(version_string):
    try:
        version = Version(version_string)
    except InvalidVersion:
        return "UNKNOWN"

    branch = f"{version.major}.{version.minor}"

    if branch not in PATCHED_VERSIONS:
        if version < Version("8.2.0"):
            return "UNSUPPORTED"

        return "REVIEW_REQUIRED"

    patched_version = Version(PATCHED_VERSIONS[branch])

    if version < patched_version:
        return "POTENTIALLY_VULNERABLE"

    return "PATCHED_UPSTREAM"


def main():
    inventory = load_inventory()
    applications = inventory["applications"]

    print("=== VULNOPS LAB ===")
    print(f"Applications inventoriées : {len(applications)}")

    for app in applications:
        status = check_php_version(app["php_version"])
        risk_score = calculate_risk(app, status)
        print(
            f"{app['id']} | "
            f"{app['name']} | "
            f"PHP {app['php_version']} | "
            f"{status} | "
            f"RISK: {risk_score}"
        )


if __name__ == "__main__":
    main()
