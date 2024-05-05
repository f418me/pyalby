# test_invoice_unit.py
import pytest
import responses
from pyalby.invoice import Invoice

@pytest.fixture
def invoice_client():
    return Invoice()

@responses.activate
def test_create_invoice(invoice_client):
    mock_response = {
        "expires_at": "2022-06-02T08:31:15Z",
        "payment_hash": "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84",
        "payment_request": "lnbcrt10u1p3fsa2jpp5qxkye7e9vhgjyxyh5wlhxpx8r768kygyl4v3ezu3hypus7x3dwzqhp5s6dz9ye889e8uyaxjzjlkh3vtwes50mhyvfraf3y6l3yk8t2mlgscqzpgxqyz5vqsp5zt95vajqwya7haely3p0ev2jg4v6lr84up4ujm5auk8u74xggtas9qyyssq7lmukwlctr2y4gcuw9324gfxefug45zrrywrp5l3fmn85zulk6z44pqx7vywp7zsks2r5rclang06akp6054tlgfad80ktzg9vwyatcqz6ssya"
    }
    responses.add(
        responses.POST,
        "https://api.getalby.com/invoices",
        json=mock_response,
        status=200
    )

    result = invoice_client.create_invoice(amount=100, description="Test Invoice")
    assert result["expires_at"] == "2022-06-02T08:31:15Z"
    assert result["payment_hash"] == "01ac4cfb2565d1221897a3bf7304c71fb47b1104fd591c8b91b903c878d16b84"

@responses.activate
def test_get_incoming_invoices(invoice_client):
    mock_response = [
        {
            "amount": 3,
            "state": "SETTLED",
            "type": "incoming"
        }
    ]
    responses.add(
        responses.GET,
        "https://api.getalby.com/invoices/incoming",
        json=mock_response,
        status=200
    )

    result = invoice_client.get_incoming_invoices()
    assert len(result) == 1
    assert result[0]["type"] == "incoming"

@responses.activate
def test_get_outgoing_invoices(invoice_client):
    mock_response = [
        {
            "amount": 300,
            "state": "SETTLED",
            "type": "outgoing"
        }
    ]
    responses.add(
        responses.GET,
        "https://api.getalby.com/invoices/outgoing",
        json=mock_response,
        status=200
    )

    result = invoice_client.get_outgoing_invoices()
    assert len(result) == 1
    assert result[0]["type"] == "outgoing"
