import pytest
import asyncio
from pyalby.async_account import AsyncAccount

@pytest.fixture
def async_alby_account():
    return AsyncAccount()

@pytest.mark.asyncio
async def test_get_value4value_async(async_alby_account):
    """Test async get_value4value with real API call"""
    # Make a real async API call to get value4value data
    result = await async_alby_account.get_value4value()

    assert "keysend_pubkey" in result
    assert "keysend_custom_key" in result
    assert "keysend_custom_value" in result
    assert "lightning_address" in result

@pytest.mark.asyncio
async def test_get_balance_async(async_alby_account):
    """Test async get_balance with real API call"""
    # Make a real async API call to get balance data
    result = await async_alby_account.get_balance()

    assert "balance" in result
    assert "currency" in result
    assert "unit" in result

@pytest.mark.asyncio
async def test_get_account_summary_async(async_alby_account):
    """Test async get_account_summary with real API call"""
    # Make a real async API call to get account summary
    result = await async_alby_account.get_account_summary()

    assert "balance" in result
    assert "transactions_count" in result
    assert "boostagrams_count" in result

@pytest.mark.asyncio
async def test_get_personal_info_async(async_alby_account):
    """Test async get_personal_info with real API call"""
    # Make a real async API call to get personal information
    result = await async_alby_account.get_personal_info()

    assert "identifier" in result
    assert "email" in result
    assert "name" in result
    assert "avatar" in result
    assert "keysend_custom_key" in result
    assert "keysend_custom_value" in result
    assert "keysend_pubkey" in result
    assert "lightning_address" in result
    assert "nostr_pubkey" in result

@pytest.mark.asyncio
async def test_concurrent_account_calls(async_alby_account):
    """Test multiple concurrent async account API calls"""
    # Test that multiple async calls can be made concurrently
    tasks = [
        async_alby_account.get_balance(),
        async_alby_account.get_value4value(),
        async_alby_account.get_account_summary()
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Verify all calls completed successfully
    assert len(results) == 3
    assert "balance" in results[0]  # get_balance result
    assert "keysend_pubkey" in results[1]  # get_value4value result
    assert "transactions_count" in results[2]  # get_account_summary result