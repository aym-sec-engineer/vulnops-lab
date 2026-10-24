import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "inventory.json"
TARGET = ROOT / "data" / "inventory-remediated.json"

REMEDIATION_PLAN = {
    "APP-001": "8.3.36",
    "APP-003": "8.2.35",
    "APP-004": "8.3.36",
}


def main():
    with SOURCE.open(encoding="utf-8") as file:
        inventory = json.load(file)

    for app in inventory["applications"]:
        if app["id"] in REMEDIATION_PLAN:
            old_version = app["php_version"]
            new_version = REMEDIATION_PLAN[app["id"]]

            app["php_version"] = new_version
            app["patch_status"] = "simulated"

            print(f"{app['id']}: PHP {old_version} -> {new_version}")

    TARGET.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Simulation saved to: {TARGET}")


if __name__ == "__main__":
    main()
