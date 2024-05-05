import responses
import pytest
from pyalby.account import Account

# Mock data for the API responses
mock_value4value_response = {
    "keysend_pubkey": "02740d5d0e3b2d4d9e313423587a01e8122f9c6e8717e36ff388a170bdcb8c1e7e",
    "keysend_custom_key": "696969",
    "keysend_custom_value": "01wDdDkTsaRuNTAJzXiW",
    "lightning_address": "hello@getalby.com"
}

mock_balance_response = {
    "balance": 1000,
    "currency": "BTC",
    "unit": "sat"
}

mock_summary_response = {
    "balance": 10000,
    "boostagrams_count": 8,
    "currency": "BTC",
    "invoices_count": 9,
    "last_invoice_at": "2022-06-02T08:40:08.000Z",
    "transactions_count": 33,
    "unit": "sat"
}

mock_personal_info_response = {
    "identifier": "LlzljZKnMATJxC6z9t19",
    "email": "kwinten@getalby.com",
    "name": "Kwinten",
    "avatar": "https://fra1.digitaloceanspaces.com/getalbycom/uploads/lightning_address/avatar/28/thumb_signal-2022-05-15-17-19-02-995.jpg",
    "keysend_custom_key": "696969",
    "keysend_custom_value": "LlzljZKnMATJxC6z9t19",
    "keysend_pubkey": "030a58b8653d32b99200a2334cfe913e51dc7d155aa0116c176657a4f1722677a3",
    "lightning_address": "kiwiidb@getalby.com",
    "nostr_pubkey": "npub13sajvl5ak6cpz4ycesl0e5v869r5sey5pt50l9mcy6uas0fqtpmscth4np"
}

@pytest.fixture
def alby_account():
    return Account()

@responses.activate
def test_get_value4value(alby_account):
    # Mock the API response
    responses.add(
        responses.GET,
        "https://api.getalby.com/user/value4value",
        json=mock_value4value_response,
        status=200
    )

    # Test the API call
    result = alby_account.get_value4value()
    assert result == mock_value4value_response

@responses.activate
def test_get_balance(alby_account):
    # Mock the API response
    responses.add(
        responses.GET,
        "https://api.getalby.com/balance",
        json=mock_balance_response,
        status=200
    )

    # Test the API call
    result = alby_account.get_balance()
    assert result == mock_balance_response

@responses.activate
def test_get_account_summary(alby_account):
    # Mock the API response
    responses.add(
        responses.GET,
        "https://api.getalby.com/user/summary",
        json=mock_summary_response,
        status=200
    )

    # Test the API call
    result = alby_account.get_account_summary()
    assert result == mock_summary_response

@responses.activate
def test_get_personal_info(alby_account):
    # Mock the API response
    responses.add(
        responses.GET,
        "https://api.getalby.com/user/me",
        json=mock_personal_info_response,
        status=200
    )

    # Test the API call
    result = alby_account.get_personal_info()
    assert result == mock_personal_info_response