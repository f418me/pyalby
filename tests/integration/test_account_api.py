import pytest
from pyalby.account import Account

@pytest.fixture
def alby_account():
    return Account()

def test_get_value4value(alby_account):
    # Make a real API call to get value4value data
    result = alby_account.get_value4value()

    assert "keysend_pubkey" in result
    assert "keysend_custom_key" in result
    assert "keysend_custom_value" in result
    assert "lightning_address" in result


def test_get_balance(alby_account):
    # Make a real API call to get balance data
    result = alby_account.get_balance()

    assert "balance" in result
    assert "currency" in result
    assert "unit" in result

def test_get_account_summary(alby_account):
    # Make a real API call to get account summary
    result = alby_account.get_account_summary()

    assert "balance" in result
    assert "transactions_count" in result
    assert "boostagrams_count" in result

def test_get_personal_info(alby_account):
    # Make a real API call to get personal information
    result = alby_account.get_personal_info()

    assert "identifier" in result
    assert "email" in result
    assert "name" in result
    assert "avatar" in result
    assert "keysend_custom_key" in result
    assert "keysend_custom_value" in result
    assert "keysend_pubkey" in result
    assert "lightning_address" in result
    assert "nostr_pubkey" in result