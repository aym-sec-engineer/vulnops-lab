VALID_EXPOSURES = {"internet", "internal"}
VALID_PATCH_STATUSES = {"unknown", "simulated"}

VALID_CRITICALITIES = {
    "critical",
    "high",
    "medium",
    "low",
}


def validate_application(app):
    if not isinstance(app, dict):
        raise TypeError("Application must be an object")

    required_fields = {
        "id",
        "name",
        "php_version",
        "exposure",
        "business_criticality",
    }

    missing = required_fields - app.keys()

    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}")

    if not isinstance(app["php_version"], str) or not app["php_version"].strip():
        raise ValueError(f"{app['id']}: invalid PHP version")

    if app["exposure"] not in VALID_EXPOSURES:
        raise ValueError(f"{app['id']}: invalid exposure")

    if app["business_criticality"] not in VALID_CRITICALITIES:
        raise ValueError(f"{app['id']}: invalid business criticality")

    patch_status = app.get("patch_status", "unknown")

    if patch_status not in VALID_PATCH_STATUSES:
        raise ValueError(f"{app['id']}: invalid patch status")


def validate_inventory(inventory):
    if not isinstance(inventory, dict):
        raise TypeError("Inventory must be an object")

    if not isinstance(inventory.get("incident"), dict):
        raise TypeError("Missing or invalid incident")

    applications = inventory.get("applications")

    if not isinstance(applications, list):
        raise TypeError("Applications must be a list")

    seen_ids = set()

    for app in applications:
        validate_application(app)

        if app["id"] in seen_ids:
            raise ValueError(f"Duplicate application ID: {app['id']}")

        seen_ids.add(app["id"])
