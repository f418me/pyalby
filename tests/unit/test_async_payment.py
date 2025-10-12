from pathlib import Path
import pytest
import aiohttp
from aioresponses import aioresponses
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pyalby.async_payment import AsyncPayment

# Mock data for the API responses (same as sync tests for consistency)
mock_bolt11_response = {
    "amount": 100,
    "description": "Alby invoice",
    "destination": "025c1d5d1b4c983cc6350fc2d756fbb59b4dc365e45e87f8e3afe07e24013e8220",
    "fee": 0,
    "payment_hash": "38caadbe0f6112d9b638e9ae24338f7e9bd930a3387100da776644e56965c9c1",
    "payment_preimage": "2f84e22556af9919f695d7761f404e98ff98058b7d32074de8c0c83bf63eecd7",
    "payment_request": "lnbcrt1u1p3d23dkpp58r92m0s0vyfdnd3caxhzgvu006dajv9r8pcspknhvezw26t9e8qsdq5g9kxy7fqd9h8vmmfvdjscqzpgxqyz5vqsp59efe44rg6cjl3xwh9glgx4ztcgwtg5l8uhry2v9v7s0zn2wpaz2s9qyyssq2z799an4pt4wtfy8yrk5ee0qqj7w5a74prz5tm8rulwez08ttlaz9xx7eqw7fe94y7t0600d03k55fyguyj24nd9tjmx6sf7dsxkk4gpkyenl8"
}

mock_keysend_response = {
    "amount": 1000,
    "destination": "0234abcd...",
    "payment_hash": "example-payment-hash",
    "payment_preimage": "example-preimage"
}

mock_multi_keysend_response = {
    "keysends": [
        {
            "error": {
                "code": 0,
                "error": False,
                "message": "string"
            },
            "keysend": {
                "amount": 100,
                "description": "test",
                "destination": "0234",
                "payment_hash": "paymenthash",
                "payment_preimage": "preimage"
            }
        }
    ]
}


@pytest.fixture
def async_payments_client():
    """Fixture to create AsyncPayment instance for testing."""
    return AsyncPayment()


@pytest.mark.asyncio
async def test_bolt11_payment(async_payments_client):
    """Test async bolt11_payment method returns correct data."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/bolt11",
            payload=mock_bolt11_response,
            status=200
        )

        result = await async_payments_client.bolt11_payment(invoice="test-invoice")
        assert result["amount"] == 100
        assert result["payment_hash"] == "38caadbe0f6112d9b638e9ae24338f7e9bd930a3387100da776644e56965c9c1"


@pytest.mark.asyncio
async def test_keysend_payment(async_payments_client):
    """Test async keysend_payment method returns correct data."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/keysend",
            payload=mock_keysend_response,
            status=200
        )

        result = await async_payments_client.keysend_payment(amount=1000, destination="0234abcd...")
        assert result["amount"] == 1000
        assert result["destination"] == "0234abcd..."


@pytest.mark.asyncio
async def test_keysend_payment_with_memo(async_payments_client):
    """Test async keysend_payment method with memo parameter."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/keysend",
            payload=mock_keysend_response,
            status=200
        )

        result = await async_payments_client.keysend_payment(
            amount=1000, 
            destination="0234abcd...", 
            memo="Test memo"
        )
        assert result["amount"] == 1000
        assert result["destination"] == "0234abcd..."


@pytest.mark.asyncio
async def test_keysend_payment_with_custom_records(async_payments_client):
    """Test async keysend_payment method with custom_records parameter."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/keysend",
            payload=mock_keysend_response,
            status=200
        )

        custom_records = {"key1": "value1", "key2": "value2"}
        result = await async_payments_client.keysend_payment(
            amount=1000, 
            destination="0234abcd...", 
            custom_records=custom_records
        )
        assert result["amount"] == 1000
        assert result["destination"] == "0234abcd..."


@pytest.mark.asyncio
async def test_multi_keysend_payment(async_payments_client):
    """Test async multi_keysend_payment method returns correct data."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/keysend/multi",
            payload=mock_multi_keysend_response,
            status=200
        )

        keysends = [
            {
                "amount": 100,
                "destination": "0234",
                "description": "test"
            }
        ]
        result = await async_payments_client.multi_keysend_payment(keysends=keysends)
        assert len(result["keysends"]) == 1
        assert result["keysends"][0]["keysend"]["amount"] == 100


@pytest.mark.asyncio
async def test_bolt11_payment_http_error(async_payments_client):
    """Test that HTTP errors are properly propagated for bolt11_payment."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/bolt11",
            payload={"error": "Unauthorized"},
            status=401
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_payments_client.bolt11_payment(invoice="test-invoice")
        
        assert excinfo.value.status == 401


@pytest.mark.asyncio
async def test_keysend_payment_http_error(async_payments_client):
    """Test that HTTP errors are properly propagated for keysend_payment."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/keysend",
            payload={"error": "Server Error"},
            status=500
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_payments_client.keysend_payment(amount=1000, destination="0234abcd...")
        
        assert excinfo.value.status == 500


@pytest.mark.asyncio
async def test_multi_keysend_payment_http_error(async_payments_client):
    """Test that HTTP errors are properly propagated for multi_keysend_payment."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/keysend/multi",
            payload={"error": "Forbidden"},
            status=403
        )

        keysends = [{"amount": 100, "destination": "0234", "description": "test"}]
        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_payments_client.multi_keysend_payment(keysends=keysends)
        
        assert excinfo.value.status == 403


@pytest.mark.asyncio
async def test_bolt11_payment_connection_error(async_payments_client):
    """Test that connection errors are properly propagated for bolt11_payment."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/bolt11",
            exception=aiohttp.ClientConnectionError("Connection failed")
        )

        with pytest.raises(aiohttp.ClientConnectionError):
            await async_payments_client.bolt11_payment(invoice="test-invoice")


@pytest.mark.asyncio
async def test_keysend_payment_timeout_error(async_payments_client):
    """Test that timeout errors are properly propagated for keysend_payment."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/keysend",
            exception=aiohttp.ServerTimeoutError("Request timeout")
        )

        with pytest.raises(aiohttp.ServerTimeoutError):
            await async_payments_client.keysend_payment(amount=1000, destination="0234abcd...")


@pytest.mark.asyncio
async def test_multi_keysend_payment_connection_error(async_payments_client):
    """Test that connection errors are properly propagated for multi_keysend_payment."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/payments/keysend/multi",
            exception=aiohttp.ClientConnectionError("Connection failed")
        )

        keysends = [{"amount": 100, "destination": "0234", "description": "test"}]
        with pytest.raises(aiohttp.ClientConnectionError):
            await async_payments_client.multi_keysend_payment(keysends=keysends)


@pytest.mark.asyncio
async def test_initialization_missing_base_url(monkeypatch):
    """Test that AsyncPayment initialization fails when BASE_URL is missing."""
    monkeypatch.delenv("BASE_URL", raising=False)
    
    with pytest.raises(ValueError, match="BASE_URL is required"):
        AsyncPayment()


@pytest.mark.asyncio
async def test_initialization_missing_access_token(monkeypatch):
    """Test that AsyncPayment initialization fails when ALBY_ACCESS_TOKEN is missing."""
    monkeypatch.delenv("ALBY_ACCESS_TOKEN", raising=False)
    
    with pytest.raises(ValueError, match="ALBY_ACCESS_TOKEN is required"):
        AsyncPayment()


@pytest.mark.asyncio
async def test_headers_contain_authorization(async_payments_client):
    """Test that headers contain proper Authorization header."""
    assert "Authorization" in async_payments_client.headers
    assert async_payments_client.headers["Authorization"].startswith("Bearer ")
    assert "Content-Type" in async_payments_client.headers
    assert async_payments_client.headers["Content-Type"] == "application/json"