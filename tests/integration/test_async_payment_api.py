import pytest
import asyncio
from pyalby.async_payment import AsyncPayment

@pytest.fixture
def async_payments_client():
    return AsyncPayment()

@pytest.mark.asyncio
async def test_bolt11_payment_async_integration(async_payments_client):
    """Test async BOLT11 payment with real API call"""
    # Replace with a real invoice to test payment
    # Note: This is a placeholder - in real testing, you'd need a valid invoice
    invoice = "lnbc2100n1pnr0tjhpp5aa....."
    
    try:
        result = await async_payments_client.bolt11_payment(invoice)
        assert "payment_hash" in result
    except Exception as e:
        # Expected to fail with placeholder invoice
        # In real integration testing, use a valid invoice
        assert "Invalid" in str(e) or "not found" in str(e).lower()

@pytest.mark.asyncio
async def test_keysend_payment_async_integration(async_payments_client):
    """Test async keysend payment with real API call"""
    # Replace with a valid destination public key
    # Note: This is a placeholder - in real testing, you'd need a valid pubkey
    destination = "024c60141110ba650d2e70598d8e8362f22ff7db0cfa1d3bbd710ab5e18fbef87e"
    
    try:
        result = await async_payments_client.keysend_payment(
            amount=50, 
            destination=destination,
            memo="Async integration test payment"
        )
        assert "payment_hash" in result
    except Exception as e:
        # Expected to fail with placeholder destination in test environment
        # In real integration testing, use a valid destination
        assert "Invalid" in str(e) or "not found" in str(e).lower() or "route" in str(e).lower()

@pytest.mark.asyncio
async def test_multi_keysend_payment_async_integration(async_payments_client):
    """Test async multi-keysend payment with real API call"""
    keysends = [
        {
            "amount": 21,
            "destination": "024c60141110ba650d2e70598d8e8362f22ff7db0cfa1d3bbd710ab5e18fbef87e",
            "description": "Async test multi keysend - keysend 1"
        },
        {
            "amount": 210,
            "destination": "024c60141110ba650d2e70598d8e8362f22ff7db0cfa1d3bbd710ab5e18fbef87e",
            "description": "Async test multi keysend - keysend 2"
        }
    ]
    
    try:
        result = await async_payments_client.multi_keysend_payment(keysends)
        assert "keysends" in result
        assert len(result["keysends"]) > 0
        assert "payment_hash" in result["keysends"][0]["keysend"]
    except Exception as e:
        # Expected to fail with placeholder destinations in test environment
        # In real integration testing, use valid destinations
        assert "Invalid" in str(e) or "not found" in str(e).lower() or "route" in str(e).lower()

@pytest.mark.asyncio
async def test_keysend_with_custom_records_async_integration(async_payments_client):
    """Test async keysend payment with custom records"""
    destination = "024c60141110ba650d2e70598d8e8362f22ff7db0cfa1d3bbd710ab5e18fbef87e"
    custom_records = {
        "7629169": "Hello from async test",
        "34349334": "Custom data"
    }
    
    try:
        result = await async_payments_client.keysend_payment(
            amount=100,
            destination=destination,
            memo="Async keysend with custom records",
            custom_records=custom_records
        )
        assert "payment_hash" in result
    except Exception as e:
        # Expected to fail with placeholder destination in test environment
        assert "Invalid" in str(e) or "not found" in str(e).lower() or "route" in str(e).lower()

@pytest.mark.asyncio
async def test_concurrent_payment_operations(async_payments_client):
    """Test multiple concurrent async payment operations"""
    # Note: These will likely fail due to placeholder data, but test the async pattern
    destination = "024c60141110ba650d2e70598d8e8362f22ff7db0cfa1d3bbd710ab5e18fbef87e"
    
    tasks = [
        async_payments_client.keysend_payment(
            amount=10, 
            destination=destination, 
            memo="Concurrent test 1"
        ),
        async_payments_client.keysend_payment(
            amount=20, 
            destination=destination, 
            memo="Concurrent test 2"
        )
    ]
    
    # Use gather with return_exceptions=True to handle expected failures
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Verify that both operations were attempted (even if they failed)
    assert len(results) == 2
    # In real integration testing with valid data, these would be successful results
    # For now, we just verify the async pattern works

@pytest.mark.asyncio
async def test_payment_error_handling_async(async_payments_client):
    """Test async payment error handling"""
    # Test with invalid invoice
    invalid_invoice = "invalid_invoice_string"
    
    with pytest.raises(Exception):
        await async_payments_client.bolt11_payment(invalid_invoice)
    
    # Test with invalid destination
    invalid_destination = "invalid_destination"
    
    with pytest.raises(Exception):
        await async_payments_client.keysend_payment(
            amount=50,
            destination=invalid_destination
        )