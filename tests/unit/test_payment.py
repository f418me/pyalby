import pytest
import responses
from pyalby.payment import Payment

@pytest.fixture
def payments_client():
    return Payment()

@responses.activate
def test_bolt11_payment(payments_client):
    mock_response = {
        "amount": 100,
        "description": "Alby invoice",
        "destination": "025c1d5d1b4c983cc6350fc2d756fbb59b4dc365e45e87f8e3afe07e24013e8220",
        "fee": 0,
        "payment_hash": "38caadbe0f6112d9b638e9ae24338f7e9bd930a3387100da776644e56965c9c1",
        "payment_preimage": "2f84e22556af9919f695d7761f404e98ff98058b7d32074de8c0c83bf63eecd7",
        "payment_request": "lnbcrt1u1p3d23dkpp58r92m0s0vyfdnd3caxhzgvu006dajv9r8pcspknhvezw26t9e8qsdq5g9kxy7fqd9h8vmmfvdjscqzpgxqyz5vqsp59efe44rg6cjl3xwh9glgx4ztcgwtg5l8uhry2v9v7s0zn2wpaz2s9qyyssq2z799an4pt4wtfy8yrk5ee0qqj7w5a74prz5tm8rulwez08ttlaz9xx7eqw7fe94y7t0600d03k55fyguyj24nd9tjmx6sf7dsxkk4gpkyenl8"
    }
    responses.add(
        responses.POST,
        "https://api.getalby.com/payments/bolt11",
        json=mock_response,
        status=200
    )

    result = payments_client.bolt11_payment(invoice="test-invoice")
    assert result["amount"] == 100
    assert result["payment_hash"] == "38caadbe0f6112d9b638e9ae24338f7e9bd930a3387100da776644e56965c9c1"

@responses.activate
def test_keysend_payment(payments_client):
    mock_response = {
        "amount": 1000,
        "destination": "0234abcd...",
        "payment_hash": "example-payment-hash",
        "payment_preimage": "example-preimage"
    }
    responses.add(
        responses.POST,
        "https://api.getalby.com/payments/keysend",
        json=mock_response,
        status=200
    )

    result = payments_client.keysend_payment(amount=1000, destination="0234abcd...")
    assert result["amount"] == 1000
    assert result["destination"] == "0234abcd..."

@responses.activate
def test_multi_keysend_payment(payments_client):
    mock_response = {
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
    responses.add(
        responses.POST,
        "https://api.getalby.com/payments/keysend/multi",
        json=mock_response,
        status=200
    )

    keysends = [
        {
            "amount": 100,
            "destination": "0234",
            "description": "test"
        }
    ]
    result = payments_client.multi_keysend_payment(keysends=keysends)
    assert len(result["keysends"]) == 1
    assert result["keysends"][0]["keysend"]["amount"] == 100
