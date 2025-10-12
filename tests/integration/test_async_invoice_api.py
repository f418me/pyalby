import pytest
import asyncio
from pyalby.async_invoice import AsyncInvoice

@pytest.fixture
def async_invoice_client():
    return AsyncInvoice()

@pytest.mark.asyncio
async def test_create_invoice_async_integration(async_invoice_client):
    """Test async invoice creation with real API call"""
    result = await async_invoice_client.create_invoice(
        amount=100, 
        description="Async Integration Test Invoice"
    )
    
    assert "expires_at" in result
    assert "payment_hash" in result
    assert "payment_request" in result
    assert result["amount"] == 100
    assert result["description"] == "Async Integration Test Invoice"

@pytest.mark.asyncio
async def test_get_incoming_invoices_async_integration(async_invoice_client):
    """Test async get_incoming_invoices with real API call"""
    result = await async_invoice_client.get_incoming_invoices()
    
    assert isinstance(result, list)
    # If there are invoices, check structure
    if result:
        invoice = result[0]
        assert "payment_hash" in invoice
        assert "amount" in invoice

@pytest.mark.asyncio
async def test_get_outgoing_invoices_async_integration(async_invoice_client):
    """Test async get_outgoing_invoices with real API call"""
    result = await async_invoice_client.get_outgoing_invoices()
    
    assert isinstance(result, list)
    # If there are invoices, check structure
    if result:
        invoice = result[0]
        assert "payment_hash" in invoice
        assert "amount" in invoice

@pytest.mark.asyncio
async def test_decode_invoice_async_integration(async_invoice_client):
    """Test async decode_invoice with real API call"""
    # First create an invoice to decode
    created_invoice = await async_invoice_client.create_invoice(
        amount=50,
        description="Test invoice for decoding"
    )
    
    bolt11_invoice = created_invoice["payment_request"]
    
    # Now decode it
    result = await async_invoice_client.decode_invoice(bolt11_invoice)
    
    assert "amount" in result
    assert "description" in result
    assert result["amount"] == 50
    assert result["description"] == "Test invoice for decoding"

@pytest.mark.asyncio
async def test_concurrent_invoice_operations(async_invoice_client):
    """Test multiple concurrent async invoice operations"""
    # Test concurrent invoice creation and retrieval
    tasks = [
        async_invoice_client.create_invoice(amount=25, description="Concurrent test 1"),
        async_invoice_client.create_invoice(amount=75, description="Concurrent test 2"),
        async_invoice_client.get_incoming_invoices()
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Verify all operations completed successfully
    assert len(results) == 3
    assert "payment_hash" in results[0]  # First invoice creation
    assert "payment_hash" in results[1]  # Second invoice creation
    assert isinstance(results[2], list)  # Invoice list retrieval

@pytest.mark.asyncio
async def test_get_specific_invoice_async_integration(async_invoice_client):
    """Test async get_specific_invoice with real API call"""
    # First create an invoice
    created_invoice = await async_invoice_client.create_invoice(
        amount=200,
        description="Test specific invoice retrieval"
    )
    
    payment_hash = created_invoice["payment_hash"]
    
    # Now retrieve the specific invoice
    result = await async_invoice_client.get_specific_invoice(payment_hash)
    
    assert "payment_hash" in result
    assert "amount" in result
    assert "description" in result
    assert result["payment_hash"] == payment_hash
    assert result["amount"] == 200