"""Direct tests for versioned entitlement mask joins."""

import json


CATALOG = json.dumps({"features": [
    {"id": "REPORTS", "description": "Generate the standard usage report for one workspace."},
    {"id": "EXPORT", "description": "Export workspace records in the supported archive format."},
]})


def _catalog(contract, vm, provider):
    vm.sender = provider
    return contract.publish_catalog("CORE", CATALOG, "provider-plan-catalog-snapshot")


def _version(contract, vm, provider, catalog_id, base=1, legacy=0):
    vm.sender = provider
    return contract.publish_version("V1", catalog_id, 0, 1000, base, legacy)


def _subscription(contract, vm, provider, version_id, subscriber, addon=0, grandfathered=False):
    vm.sender = provider
    return contract.issue_subscription("SUB-1", version_id, subscriber, 10, addon, grandfathered)


def _check(contract, vm, subscriber, subscription_id, feature):
    vm.sender = subscriber
    vm.mock_llm(r".*Map one public requested capability.*", json.dumps({"feature_id": feature}))
    return contract.check_feature("REQ-1", subscription_id, "Please check whether this subscription includes the requested capability.")


def test_catalog_and_version(contract, direct_vm, direct_alice):
    catalog_id = _catalog(contract, direct_vm, direct_alice)
    version_id = _version(contract, direct_vm, direct_alice, catalog_id)
    assert contract.get_version(version_id)["base_mask"] == 1


def test_rejects_overlapping_base_and_legacy(contract, direct_vm, direct_alice):
    catalog_id = _catalog(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("invalid_version_fields"):
        contract.publish_version("BAD", catalog_id, 0, 10, 1, 1)


def test_only_subscriber_checks(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    catalog_id = _catalog(contract, direct_vm, direct_alice)
    version_id = _version(contract, direct_vm, direct_alice, catalog_id)
    subscription_id = _subscription(contract, direct_vm, direct_alice, version_id, direct_bob)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_subscriber"):
        contract.check_feature("REQ-X", subscription_id, "Check whether standard reporting is included in this subscription.")


def test_base_feature_is_included(contract, direct_vm, direct_alice, direct_bob):
    catalog_id = _catalog(contract, direct_vm, direct_alice)
    version_id = _version(contract, direct_vm, direct_alice, catalog_id)
    subscription_id = _subscription(contract, direct_vm, direct_alice, version_id, direct_bob)
    request_id = _check(contract, direct_vm, direct_bob, subscription_id, "REPORTS")
    assert contract.matches_entitlement(request_id, "REPORTS", "INCLUDED") is True
    assert contract.get_request(request_id)["source"] == "BASE"


def test_addon_feature_is_included(contract, direct_vm, direct_alice, direct_bob):
    catalog_id = _catalog(contract, direct_vm, direct_alice)
    version_id = _version(contract, direct_vm, direct_alice, catalog_id, 0, 0)
    subscription_id = _subscription(contract, direct_vm, direct_alice, version_id, direct_bob, 2)
    request_id = _check(contract, direct_vm, direct_bob, subscription_id, "EXPORT")
    assert contract.get_request(request_id)["source"] == "ADDON"


def test_grandfathered_feature_is_included(contract, direct_vm, direct_alice, direct_bob):
    catalog_id = _catalog(contract, direct_vm, direct_alice)
    version_id = _version(contract, direct_vm, direct_alice, catalog_id, 0, 2)
    subscription_id = _subscription(contract, direct_vm, direct_alice, version_id, direct_bob, 0, True)
    request_id = _check(contract, direct_vm, direct_bob, subscription_id, "EXPORT")
    assert contract.get_request(request_id)["source"] == "GRANDFATHERED"


def test_unknown_mapping_fails_closed_to_unknown(contract, direct_vm, direct_alice, direct_bob):
    catalog_id = _catalog(contract, direct_vm, direct_alice)
    version_id = _version(contract, direct_vm, direct_alice, catalog_id)
    subscription_id = _subscription(contract, direct_vm, direct_alice, version_id, direct_bob)
    request_id = _check(contract, direct_vm, direct_bob, subscription_id, "UNKNOWN")
    assert contract.get_request(request_id)["result"] == "UNKNOWN"


def test_provider_deactivates_subscription(contract, direct_vm, direct_alice, direct_bob):
    catalog_id = _catalog(contract, direct_vm, direct_alice)
    version_id = _version(contract, direct_vm, direct_alice, catalog_id)
    subscription_id = _subscription(contract, direct_vm, direct_alice, version_id, direct_bob)
    direct_vm.sender = direct_alice
    contract.deactivate_subscription(subscription_id)
    assert contract.get_subscription(subscription_id)["active"] is False
