import json

from src.simulate_remediation import (
    REMEDIATION_PLAN,
    SOURCE,
)


def test_remediation_plan_targets_existing_applications():
    with SOURCE.open(encoding="utf-8") as file:
        inventory = json.load(file)

    existing_ids = {app["id"] for app in inventory["applications"]}

    assert set(REMEDIATION_PLAN).issubset(existing_ids)


def test_remediation_plan_changes_versions():
    with SOURCE.open(encoding="utf-8") as file:
        inventory = json.load(file)

    original_versions = {
        app["id"]: app["php_version"] for app in inventory["applications"]
    }

    for app_id, target_version in REMEDIATION_PLAN.items():
        assert original_versions[app_id] != target_version
