# test_invoice_integration.py
import pytest
from pyalby.invoice import Invoice

@pytest.fixture
def invoice_client():
    return Invoice()

def test_create_invoice_integration(invoice_client):
    result = invoice_client.create_invoice(amount=100, description="Integration Test Invoice")
    assert "expires_at" in result
    assert "payment_hash" in result

def test_get_incoming_invoices_integration(invoice_client):
    result = invoice_client.get_incoming_invoices(items=5)
    assert isinstance(result, list)

def test_get_outgoing_invoices_integration(invoice_client):
    result = invoice_client.get_outgoing_invoices(items=5)
    assert isinstance(result, list)
