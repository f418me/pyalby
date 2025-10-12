import os
import logging
from dotenv import load_dotenv

from pyalby.async_utils import make_async_get_request, make_async_post_request

# Load environment variables from the `.env` file
load_dotenv()


class AsyncInvoice:
    """
    A class to interact with the Alby API to create and get invoices asynchronously.
    
    This class provides asynchronous methods for creating, retrieving, and managing
    Lightning Network invoices through the Alby API. All methods return awaitable
    coroutines that can be used with async/await syntax.
    
    Example:
        Basic invoice operations:
        
        ```python
        import asyncio
        from pyalby import AsyncInvoice
        
        async def main():
            invoice = AsyncInvoice()
            
            # Create a new invoice
            new_invoice = await invoice.create_invoice(
                amount=1000,  # 1000 satoshis
                description="Payment for services",
                memo="Additional memo text"
            )
            print(f"Created invoice: {new_invoice['bolt11']}")
            
            # Get incoming invoices
            incoming = await invoice.get_incoming_invoices()
            print(f"Found {len(incoming)} incoming invoices")
            
            # Decode an invoice
            decoded = await invoice.decode_invoice(new_invoice['bolt11'])
            print(f"Invoice amount: {decoded['amount_msat']} msat")
            
        asyncio.run(main())
        ```
        
        Concurrent invoice operations:
        
        ```python
        import asyncio
        from pyalby import AsyncInvoice
        
        async def get_all_invoices():
            invoice = AsyncInvoice()
            
            # Get incoming and outgoing invoices concurrently
            incoming, outgoing = await asyncio.gather(
                invoice.get_incoming_invoices(),
                invoice.get_outgoing_invoices()
            )
            
            print(f"Incoming: {len(incoming)}, Outgoing: {len(outgoing)}")
            return incoming, outgoing
            
        asyncio.run(get_all_invoices())
        ```
    
    Note:
        Requires ALBY_ACCESS_TOKEN and BASE_URL environment variables to be set.
        This is experimental software - do not use for storing large amounts.
    """
    def __init__(self):
        """
        Initializes the AsyncInvoice instance with base URL and access token from environment variables.
        """
        self.base_url = os.getenv("BASE_URL")
        if not self.base_url:
            logging.error("BASE_URL is not set in environment variables.")
            raise ValueError("BASE_URL is required")

        self.access_token = os.getenv('ALBY_ACCESS_TOKEN')
        if not self.access_token:
            logging.error("ALBY_ACCESS_TOKEN is not set in environment variables.")
            raise ValueError("ALBY_ACCESS_TOKEN is required")

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def create_invoice(
            self,
            amount,  # Required
            description,  # Required
            currency="btc",  # Optional
            memo=None,  # Optional
            comment=None,  # Optional
            payer_name=None,  # Optional
            payer_email=None,  # Optional
            payer_pubkey=None,  # Optional
    ):
        """Create a new invoice for receiving lightning payments.

        Args:
            amount (int): Required amount in satoshis.
            description (str): Required description text (included in the BOLT11 invoice).
            currency (str, optional): Currency of the invoice. Defaults to "btc".
            memo (str, optional): Same as "description". Defaults to None.
            comment (str, optional): Arbitrary text to save alongside the invoice. Defaults to None.
            payer_name (str, optional): Name of the payer. Defaults to None.
            payer_email (str, optional): Email of the payer. Defaults to None.
            payer_pubkey (str, optional): Nostr or node pubkey of the payer. Defaults to None.

        Returns:
            dict: JSON response containing the invoice data.
        """
        url = f"{self.base_url}/invoices"
        data = {
            "amount": amount,
            "description": description,
            "currency": currency,
            "memo": memo,
            "comment": comment,
            "payer_name": payer_name,
            "payer_email": payer_email,
            "payer_pubkey": payer_pubkey
        }
        return await make_async_post_request(url, data, self.headers)

    async def get_incoming_invoices(self):
        """Get the list of incoming invoices with optional filters.

        Returns:
            list: List of incoming invoices.
        """
        url = f"{self.base_url}/invoices/incoming"
        return await make_async_get_request(url, self.headers)

    async def get_outgoing_invoices(self):
        """Get the list of outgoing invoices with optional filters.

        Returns:
            list: List of outgoing invoices.
        """
        url = f"{self.base_url}/invoices/outgoing"
        return await make_async_get_request(url, self.headers)

    async def get_specific_invoice(self, payment_hash):
        """Get details about a specific invoice.

        Args:
            payment_hash (str): Payment hash of the specific invoice.

        Returns:
            dict: Details of the specified invoice.
        """
        url = f"{self.base_url}/invoices/{payment_hash}"
        return await make_async_get_request(url, self.headers)

    async def decode_invoice(self, bolt11_invoice):
        """Decode a Bolt11 invoice.

        Args:
            bolt11_invoice (str): Bolt11 invoice string to decode.

        Returns:
            dict: Decoded invoice information.
        """
        url = f"{self.base_url}/decode/bolt11/{bolt11_invoice}"
        return await make_async_get_request(url, self.headers)