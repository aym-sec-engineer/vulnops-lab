import pytest

from src.validation import validate_inventory


def valid_inventory():
    return {
        "incident": {"id": "TEST"},
        "applications": [
            {
                "id": "APP-001",
                "name": "test-app",
                "php_version": "8.3.35",
                "exposure": "internet",
                "business_criticality": "high",
            }
        ],
    }


def test_valid_inventory():
    validate_inventory(valid_inventory())


def test_invalid_exposure():
    inventory = valid_inventory()
    inventory["applications"][0]["exposure"] = "unknown"

    with pytest.raises(ValueError, match="invalid exposure"):
        validate_inventory(inventory)


def test_missing_php_version():
    inventory = valid_inventory()
    del inventory["applications"][0]["php_version"]

    with pytest.raises(ValueError, match="Missing required fields"):
        validate_inventory(inventory)


def test_duplicate_application_id():
    inventory = valid_inventory()
    inventory["applications"].append(inventory["applications"][0].copy())

    with pytest.raises(ValueError, match="Duplicate application ID"):
        validate_inventory(inventory)


def test_inventory_wrong_type():
    with pytest.raises(TypeError, match="Inventory must be an object"):
        validate_inventory([])


def test_invalid_patch_status():
    inventory = valid_inventory()
    inventory["applications"][0]["patch_status"] = "verified"

    with pytest.raises(ValueError, match="invalid patch status"):
        validate_inventory(inventory)
