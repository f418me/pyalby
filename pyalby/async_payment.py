import os
import logging
from dotenv import load_dotenv
from pyalby.async_utils import make_async_post_request

# Load environment variables
load_dotenv()

class AsyncPayment:
    """
    A class to interact with the Alby API to do payments asynchronously.
    
    This class provides asynchronous methods for sending Lightning Network payments
    through the Alby API. All methods return awaitable coroutines that can be used
    with async/await syntax.
    
    Example:
        Basic payment operations:
        
        ```python
        import asyncio
        from pyalby import AsyncPayment
        
        async def main():
            payment = AsyncPayment()
            
            # Pay a BOLT11 invoice
            bolt11_result = await payment.bolt11_payment(
                "lnbc110n1pnr0vp9pp5s9qlv2ypuaxgf2zmwnwajchtq7p62lcnfsud40j7jna3l6y3wp9s..."
            )
            print(f"Payment successful: {bolt11_result}")
            
            # Send a keysend payment
            keysend_result = await payment.keysend_payment(
                amount=1000,  # 1000 satoshis
                destination="02abc123...",  # Destination pubkey
                memo="Async keysend payment"
            )
            print(f"Keysend payment sent: {keysend_result}")
            
        asyncio.run(main())
        ```
        
        Multiple payments concurrently:
        
        ```python
        import asyncio
        from pyalby import AsyncPayment
        
        async def send_multiple_payments():
            payment = AsyncPayment()
            
            # Send multiple keysend payments at once
            keysends = [
                {
                    "amount": 500,
                    "destination": "02abc123...",
                    "memo": "First payment"
                },
                {
                    "amount": 750,
                    "destination": "02def456...",
                    "memo": "Second payment"
                }
            ]
            
            results = await payment.multi_keysend_payment(keysends)
            print(f"Sent {len(results)} payments")
            
        asyncio.run(send_multiple_payments())
        ```
        
        Error handling with payments:
        
        ```python
        import asyncio
        from pyalby import AsyncPayment
        
        async def safe_payment():
            payment = AsyncPayment()
            
            try:
                result = await payment.keysend_payment(
                    amount=1000,
                    destination="02abc123...",
                    memo="Safe payment with error handling"
                )
                print("Payment successful!")
                return result
            except Exception as e:
                print(f"Payment failed: {e}")
                return None
                
        asyncio.run(safe_payment())
        ```
    
    Warning:
        Payment operations involve real Bitcoin transactions. Always test with small
        amounts first. This is experimental software - do not use for large amounts.
        
    Note:
        Requires ALBY_ACCESS_TOKEN and BASE_URL environment variables to be set.
    """
    def __init__(self):
        """
        Initializes the AsyncPayment instance with base URL and access token from environment variables.
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

    async def bolt11_payment(self, invoice):
        """Pay a lightning invoice (bolt11) asynchronously.

        Args:
            invoice (str): The BOLT11 invoice string to be paid.

        Returns:
            dict: Information about the successfully paid invoice.
        """
        url = f"{self.base_url}/payments/bolt11"
        data = {"invoice": invoice}
        return await make_async_post_request(url, data, self.headers)

    async def keysend_payment(self, amount, destination, memo=None, custom_records=None):
        """Send a spontaneous payment (keysend) asynchronously.

        Args:
            amount (int): Amount in satoshis.
            destination (str): Destination pubkey (starts with 02 or 03).
            memo (str, optional): Internal memo for reference.
            custom_records (dict, optional): Custom key-value records.

        Returns:
            dict: Information about the successfully completed keysend payment.
        """
        url = f"{self.base_url}/payments/keysend"
        data = {
            "amount": amount,
            "destination": destination
        }
        if memo:
            data["memo"] = memo
        if custom_records:
            data["custom_records"] = custom_records

        return await make_async_post_request(url, data, self.headers)

    async def multi_keysend_payment(self, keysends):
        """Make multiple keysend payments in a single request asynchronously.

        Args:
            keysends (list of dict): A list of keysend payment objects.

        Returns:
            list of dict: Each object represents an individual payment response.
        """
        url = f"{self.base_url}/payments/keysend/multi"
        data = {"keysends": keysends}

        return await make_async_post_request(url, data, self.headers)
