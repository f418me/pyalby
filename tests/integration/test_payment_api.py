import pytest
from pyalby.payment import Payment

@pytest.fixture
def payments_client():
    return Payment()

def test_bolt11_payment_integration(payments_client):
    # Replace with a real invoice to test payment
    invoice = "lnbc2100n1pnr0tjhpp5aa....."
    result = payments_client.bolt11_payment(invoice)
    assert "payment_hash" in result

def test_keysend_payment_integration(payments_client):
    # Replace with a valid destination public key
    destination = "0234abcd..."
    result = payments_client.keysend_payment(amount=1000, destination=destination)
    assert "payment_hash" in result

def test_multi_keysend_payment_integration(payments_client):
    keysends = [
        {
            "amount": 100,
            "destination": "0234abcd...",
            "description": "Test multi keysend"
        }
    ]
    result = payments_client.multi_keysend_payment(keysends)
    assert len(result["keysends"]) > 0
    assert "payment_hash" in result["keysends"][0]["keysend"]
