"""Strict feature-choice validator and state-boundary regressions."""

from tests.direct.test_entitlement_version_join import _catalog, _check, _subscription, _version


def _prepared(contract, vm, provider, subscriber):
    catalog_id = _catalog(contract, vm, provider)
    version_id = _version(contract, vm, provider, catalog_id)
    subscription_id = _subscription(contract, vm, provider, version_id, subscriber)
    return subscription_id


def test_validator_rejects_out_of_catalog_feature(contract, direct_vm, direct_alice, direct_bob):
    subscription_id = _prepared(contract, direct_vm, direct_alice, direct_bob)
    _check(contract, direct_vm, direct_bob, subscription_id, "REPORTS")
    assert direct_vm.run_validator(leader_result={"feature_id": "NOPE"}) is False


def test_validator_accepts_honest_feature(contract, direct_vm, direct_alice, direct_bob):
    subscription_id = _prepared(contract, direct_vm, direct_alice, direct_bob)
    _check(contract, direct_vm, direct_bob, subscription_id, "REPORTS")
    assert direct_vm.run_validator() is True


def test_post_consensus_invalid_feature_creates_no_request(contract, direct_vm, direct_alice, direct_bob, monkeypatch):
    from genlayer import gl

    subscription_id = _prepared(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_bob
    monkeypatch.setattr(gl.vm, "run_nondet_unsafe", lambda *args: {"feature_id": "NOPE"})
    with direct_vm.expect_revert("invalid_feature_id"):
        contract.check_feature("REQ-1", subscription_id, "Please check whether this subscription includes the requested capability.")
    assert contract.get_request_count() == 0
