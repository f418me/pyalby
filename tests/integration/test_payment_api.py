import pytest
from pyalby.payment import Payment

@pytest.fixture
def payments_client():
    return Payment()

def test_bolt11_payment_integration(payments_client):
    # Replace with a real invoice to test payment
    invoice = "lnbc2100n1pnr0tjhpp5aac7asluk0rsfwsl8hvnq8h4cavhdz2hgyn20y8xdm26g0uv9e7sdqhf38xy6t5wvsxjmnkda5kxegcqzrrxqypr9qsp5nwwlf7rgysjtxh2xs47a5qqz702g4ljml4z9spu3zl8vt4drahvq9qyyssqj87nhz92gk7nlvmyt2pdwlvdxnwfcev5nu67ntsm473pq0vktjkzzjkxe2v689w50mphwfm2mtw2f7jrlhhw2vllp358je0lke67tmcql3xsvn"
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
