import hashlib
import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context(fragment, response):
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {fragment: json.dumps(response)}},
    )
    return {
        "validators": [validator.to_dict() for validator in validators],
        "genvm_datetime": "2026-08-25T12:00:00Z",
    }


def _deploy(contract_file, owner_account):
    factory = get_contract_factory(
        contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / contract_file
    )
    receipt = factory.deploy_contract_tx(
        args=[],
        account=owner_account,
        wait_transaction_status=TransactionStatus.FINALIZED,
    )
    _ok(receipt)
    return factory, extract_contract_address(receipt)


def _send(method, args, context=None):
    if context is None:
        receipt = method(args=args).transact(
            wait_transaction_status=TransactionStatus.FINALIZED
        )
    else:
        receipt = method(args=args).transact(
            transaction_context=context,
            wait_transaction_status=TransactionStatus.FINALIZED,
        )
    _ok(receipt)
    return receipt


def test_five_validator_versioned_entitlement_join_flow():
    provider_account, subscriber_account = create_accounts(2)
    factory, address = _deploy("entitlement_version_join.py", provider_account)
    provider = factory.build_contract(address, account=provider_account)
    subscriber = factory.build_contract(address, account=subscriber_account)
    catalog_id = f"{str(provider_account.address).lower()}:CORE"
    version_id = f"{str(provider_account.address).lower()}:V1"
    subscription_id = f"{str(provider_account.address).lower()}:SUB-1"
    request_id = f"{str(subscriber_account.address).lower()}:REQ-1"
    catalog = json.dumps({"features": [
        {"id": "REPORTS", "description": "Generate the standard usage report for one workspace."},
        {"id": "EXPORT", "description": "Export workspace records in the supported archive format."},
    ]})
    _send(provider.publish_catalog, ["CORE", catalog, "provider-plan-catalog-snapshot"])
    _send(provider.publish_version, ["V1", catalog_id, 0, 1000, 1, 0])
    _send(provider.issue_subscription, ["SUB-1", version_id, subscriber_account.address, 10, 0, False])
    _send(
        subscriber.check_feature,
        ["REQ-1", subscription_id, "Please check whether this subscription includes the requested capability."],
        _context("Map one public requested capability", {"feature_id": "REPORTS"}),
    )
    assert subscriber.matches_entitlement(args=[request_id, "REPORTS", "INCLUDED"]).call() is True
    assert subscriber.get_request(args=[request_id]).call()["source"] == "BASE"
