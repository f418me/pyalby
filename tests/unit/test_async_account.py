from pathlib import Path
import pytest
import aiohttp
from aioresponses import aioresponses
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pyalby.async_account import AsyncAccount

# Mock data for the API responses (same as sync tests for consistency)
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
def async_alby_account():
    """Fixture to create AsyncAccount instance for testing."""
    return AsyncAccount()


@pytest.mark.asyncio
async def test_get_value4value(async_alby_account):
    """Test async get_value4value method returns correct data."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/user/value4value",
            payload=mock_value4value_response,
            status=200
        )

        result = await async_alby_account.get_value4value()
        assert result == mock_value4value_response


@pytest.mark.asyncio
async def test_get_balance(async_alby_account):
    """Test async get_balance method returns correct data."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/balance",
            payload=mock_balance_response,
            status=200
        )

        result = await async_alby_account.get_balance()
        assert result == mock_balance_response


@pytest.mark.asyncio
async def test_get_account_summary(async_alby_account):
    """Test async get_account_summary method returns correct data."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/user/summary",
            payload=mock_summary_response,
            status=200
        )

        result = await async_alby_account.get_account_summary()
        assert result == mock_summary_response


@pytest.mark.asyncio
async def test_get_personal_info(async_alby_account):
    """Test async get_personal_info method returns correct data."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/user/me",
            payload=mock_personal_info_response,
            status=200
        )

        result = await async_alby_account.get_personal_info()
        assert result == mock_personal_info_response


@pytest.mark.asyncio
async def test_get_value4value_http_error(async_alby_account):
    """Test that HTTP errors are properly propagated for get_value4value."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/user/value4value",
            payload={"error": "Unauthorized"},
            status=401
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_alby_account.get_value4value()
        
        assert excinfo.value.status == 401


@pytest.mark.asyncio
async def test_get_balance_http_error(async_alby_account):
    """Test that HTTP errors are properly propagated for get_balance."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/balance",
            payload={"error": "Server Error"},
            status=500
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_alby_account.get_balance()
        
        assert excinfo.value.status == 500


@pytest.mark.asyncio
async def test_get_account_summary_http_error(async_alby_account):
    """Test that HTTP errors are properly propagated for get_account_summary."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/user/summary",
            payload={"error": "Forbidden"},
            status=403
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_alby_account.get_account_summary()
        
        assert excinfo.value.status == 403


@pytest.mark.asyncio
async def test_get_personal_info_http_error(async_alby_account):
    """Test that HTTP errors are properly propagated for get_personal_info."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/user/me",
            payload={"error": "Not Found"},
            status=404
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_alby_account.get_personal_info()
        
        assert excinfo.value.status == 404


@pytest.mark.asyncio
async def test_get_value4value_connection_error(async_alby_account):
    """Test that connection errors are properly propagated for get_value4value."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/user/value4value",
            exception=aiohttp.ClientConnectionError("Connection failed")
        )

        with pytest.raises(aiohttp.ClientConnectionError):
            await async_alby_account.get_value4value()


@pytest.mark.asyncio
async def test_get_balance_timeout_error(async_alby_account):
    """Test that timeout errors are properly propagated for get_balance."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/balance",
            exception=aiohttp.ServerTimeoutError("Request timeout")
        )

        with pytest.raises(aiohttp.ServerTimeoutError):
            await async_alby_account.get_balance()


@pytest.mark.asyncio
async def test_initialization_missing_base_url(monkeypatch):
    """Test that AsyncAccount initialization fails when BASE_URL is missing."""
    monkeypatch.delenv("BASE_URL", raising=False)
    
    with pytest.raises(ValueError, match="BASE_URL is required"):
        AsyncAccount()


@pytest.mark.asyncio
async def test_initialization_missing_access_token(monkeypatch):
    """Test that AsyncAccount initialization fails when ALBY_ACCESS_TOKEN is missing."""
    monkeypatch.delenv("ALBY_ACCESS_TOKEN", raising=False)
    
    with pytest.raises(ValueError, match="ALBY_ACCESS_TOKEN is required"):
        AsyncAccount()


@pytest.mark.asyncio
async def test_headers_contain_authorization(async_alby_account):
    """Test that headers contain proper Authorization header."""
    assert "Authorization" in async_alby_account.headers
    assert async_alby_account.headers["Authorization"].startswith("Bearer ")
    assert "Content-Type" in async_alby_account.headers
    assert async_alby_account.headers["Content-Type"] == "application/json"