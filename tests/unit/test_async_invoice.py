from pathlib import Path
import pytest
import aiohttp
from aioresponses import aioresponses
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pyalby.async_invoice import AsyncInvoice

# Mock data for the API responses (same as sync tests for consistency)
mock_create_invoice_response = {
    "expires_at": "2022-06-02T08:31:15Z",
    "payment_hash": "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84",
    "payment_request": "lnbcrt10u1p3fsa2jpp5qxkye7e9vhgjyxyh5wlhxpx8r768kygyl4v3ezu3hypus7x3dwzqhp5s6dz9ye889e8uyaxjzjlkh3vtwes50mhyvfraf3y6l3yk8t2mlgscqzpgxqyz5vqsp5zt95vajqwya7haely3p0ev2jg4v6lr84up4ujm5auk8u74xggtas9qyyssq7lmukwlctr2y4gcuw9324gfxefug45zrrywrp5l3fmn85zulk6z44pqx7vywp7zsks2r5rclang06akp6054tlgfad80ktzg9vwyatcqz6ssya"
}

mock_incoming_invoices_response = [
    {
        "amount": 3,
        "state": "SETTLED",
        "type": "incoming"
    }
]

mock_outgoing_invoices_response = [
    {
        "amount": 300,
        "state": "SETTLED",
        "type": "outgoing"
    }
]

mock_specific_invoice_response = {
    "amount": 1000,
    "payment_hash": "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84",
    "state": "SETTLED",
    "type": "incoming",
    "description": "Test invoice"
}

mock_decode_invoice_response = {
    "amount": 1000,
    "description": "Test invoice",
    "destination": "02740d5d0e3b2d4d9e313423587a01e8122f9c6e8717e36ff388a170bdcb8c1e7e",
    "payment_hash": "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84",
    "timestamp": 1654158675
}


@pytest.fixture
def async_invoice_client():
    """Fixture to create AsyncInvoice instance for testing."""
    return AsyncInvoice()


@pytest.mark.asyncio
async def test_create_invoice(async_invoice_client):
    """Test async create_invoice method returns correct data."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/invoices",
            payload=mock_create_invoice_response,
            status=200
        )

        result = await async_invoice_client.create_invoice(amount=100, description="Test Invoice")
        assert result["expires_at"] == "2022-06-02T08:31:15Z"
        assert result["payment_hash"] == "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84"


@pytest.mark.asyncio
async def test_create_invoice_with_optional_params(async_invoice_client):
    """Test async create_invoice method with optional parameters."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/invoices",
            payload=mock_create_invoice_response,
            status=200
        )

        result = await async_invoice_client.create_invoice(
            amount=100,
            description="Test Invoice",
            currency="btc",
            memo="Test memo",
            comment="Test comment",
            payer_name="Test Payer",
            payer_email="test@example.com",
            payer_pubkey="02740d5d0e3b2d4d9e313423587a01e8122f9c6e8717e36ff388a170bdcb8c1e7e"
        )
        assert result["expires_at"] == "2022-06-02T08:31:15Z"
        assert result["payment_hash"] == "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84"


@pytest.mark.asyncio
async def test_get_incoming_invoices(async_invoice_client):
    """Test async get_incoming_invoices method returns correct data."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/invoices/incoming",
            payload=mock_incoming_invoices_response,
            status=200
        )

        result = await async_invoice_client.get_incoming_invoices()
        assert len(result) == 1
        assert result[0]["type"] == "incoming"
        assert result[0]["amount"] == 3
        assert result[0]["state"] == "SETTLED"


@pytest.mark.asyncio
async def test_get_outgoing_invoices(async_invoice_client):
    """Test async get_outgoing_invoices method returns correct data."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/invoices/outgoing",
            payload=mock_outgoing_invoices_response,
            status=200
        )

        result = await async_invoice_client.get_outgoing_invoices()
        assert len(result) == 1
        assert result[0]["type"] == "outgoing"
        assert result[0]["amount"] == 300
        assert result[0]["state"] == "SETTLED"


@pytest.mark.asyncio
async def test_get_specific_invoice(async_invoice_client):
    """Test async get_specific_invoice method returns correct data."""
    payment_hash = "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84"
    
    with aioresponses() as m:
        m.get(
            f"https://api.getalby.com/invoices/{payment_hash}",
            payload=mock_specific_invoice_response,
            status=200
        )

        result = await async_invoice_client.get_specific_invoice(payment_hash)
        assert result["payment_hash"] == payment_hash
        assert result["amount"] == 1000
        assert result["state"] == "SETTLED"
        assert result["type"] == "incoming"
        assert result["description"] == "Test invoice"


@pytest.mark.asyncio
async def test_decode_invoice(async_invoice_client):
    """Test async decode_invoice method returns correct data."""
    bolt11_invoice = "lnbcrt10u1p3fsa2jpp5qxkye7e9vhgjyxyh5wlhxpx8r768kygyl4v3ezu3hypus7x3dwzqhp5s6dz9ye889e8uyaxjzjlkh3vtwes50mhyvfraf3y6l3yk8t2mlgscqzpgxqyz5vqsp5zt95vajqwya7haely3p0ev2jg4v6lr84up4ujm5auk8u74xggtas9qyyssq7lmukwlctr2y4gcuw9324gfxefug45zrrywrp5l3fmn85zulk6z44pqx7vywp7zsks2r5rclang06akp6054tlgfad80ktzg9vwyatcqz6ssya"
    
    with aioresponses() as m:
        m.get(
            f"https://api.getalby.com/decode/bolt11/{bolt11_invoice}",
            payload=mock_decode_invoice_response,
            status=200
        )

        result = await async_invoice_client.decode_invoice(bolt11_invoice)
        assert result["amount"] == 1000
        assert result["description"] == "Test invoice"
        assert result["payment_hash"] == "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84"
        assert result["timestamp"] == 1654158675


@pytest.mark.asyncio
async def test_create_invoice_http_error(async_invoice_client):
    """Test that HTTP errors are properly propagated for create_invoice."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/invoices",
            payload={"error": "Bad Request"},
            status=400
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_invoice_client.create_invoice(amount=100, description="Test Invoice")
        
        assert excinfo.value.status == 400


@pytest.mark.asyncio
async def test_get_incoming_invoices_http_error(async_invoice_client):
    """Test that HTTP errors are properly propagated for get_incoming_invoices."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/invoices/incoming",
            payload={"error": "Unauthorized"},
            status=401
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_invoice_client.get_incoming_invoices()
        
        assert excinfo.value.status == 401


@pytest.mark.asyncio
async def test_get_outgoing_invoices_http_error(async_invoice_client):
    """Test that HTTP errors are properly propagated for get_outgoing_invoices."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/invoices/outgoing",
            payload={"error": "Server Error"},
            status=500
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_invoice_client.get_outgoing_invoices()
        
        assert excinfo.value.status == 500


@pytest.mark.asyncio
async def test_get_specific_invoice_http_error(async_invoice_client):
    """Test that HTTP errors are properly propagated for get_specific_invoice."""
    payment_hash = "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84"
    
    with aioresponses() as m:
        m.get(
            f"https://api.getalby.com/invoices/{payment_hash}",
            payload={"error": "Not Found"},
            status=404
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_invoice_client.get_specific_invoice(payment_hash)
        
        assert excinfo.value.status == 404


@pytest.mark.asyncio
async def test_decode_invoice_http_error(async_invoice_client):
    """Test that HTTP errors are properly propagated for decode_invoice."""
    bolt11_invoice = "invalid_invoice"
    
    with aioresponses() as m:
        m.get(
            f"https://api.getalby.com/decode/bolt11/{bolt11_invoice}",
            payload={"error": "Invalid invoice"},
            status=422
        )

        with pytest.raises(aiohttp.ClientResponseError) as excinfo:
            await async_invoice_client.decode_invoice(bolt11_invoice)
        
        assert excinfo.value.status == 422


@pytest.mark.asyncio
async def test_create_invoice_connection_error(async_invoice_client):
    """Test that connection errors are properly propagated for create_invoice."""
    with aioresponses() as m:
        m.post(
            "https://api.getalby.com/invoices",
            exception=aiohttp.ClientConnectionError("Connection failed")
        )

        with pytest.raises(aiohttp.ClientConnectionError):
            await async_invoice_client.create_invoice(amount=100, description="Test Invoice")


@pytest.mark.asyncio
async def test_get_incoming_invoices_timeout_error(async_invoice_client):
    """Test that timeout errors are properly propagated for get_incoming_invoices."""
    with aioresponses() as m:
        m.get(
            "https://api.getalby.com/invoices/incoming",
            exception=aiohttp.ServerTimeoutError("Request timeout")
        )

        with pytest.raises(aiohttp.ServerTimeoutError):
            await async_invoice_client.get_incoming_invoices()


@pytest.mark.asyncio
async def test_initialization_missing_base_url(monkeypatch):
    """Test that AsyncInvoice initialization fails when BASE_URL is missing."""
    monkeypatch.delenv("BASE_URL", raising=False)
    
    with pytest.raises(ValueError, match="BASE_URL is required"):
        AsyncInvoice()


@pytest.mark.asyncio
async def test_initialization_missing_access_token(monkeypatch):
    """Test that AsyncInvoice initialization fails when ALBY_ACCESS_TOKEN is missing."""
    monkeypatch.delenv("ALBY_ACCESS_TOKEN", raising=False)
    
    with pytest.raises(ValueError, match="ALBY_ACCESS_TOKEN is required"):
        AsyncInvoice()


@pytest.mark.asyncio
async def test_headers_contain_authorization(async_invoice_client):
    """Test that headers contain proper Authorization header."""
    assert "Authorization" in async_invoice_client.headers
    assert async_invoice_client.headers["Authorization"].startswith("Bearer ")
    assert "Content-Type" in async_invoice_client.headers
    assert async_invoice_client.headers["Content-Type"] == "application/json"