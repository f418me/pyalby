import os
import logging
from dotenv import load_dotenv
from pyalby.async_utils import make_async_get_request

# Load environment variables from the `.env` file
load_dotenv()

class AsyncAccount:
    """
    An async class to interact with the Alby API to retrieve account information.
    
    This class provides asynchronous methods for retrieving account data from the Alby API.
    All methods return awaitable coroutines that can be used with async/await syntax.
    
    Example:
        Basic usage with async/await:
        
        ```python
        import asyncio
        from pyalby import AsyncAccount
        
        async def main():
            account = AsyncAccount()
            
            # Get account balance
            balance = await account.get_balance()
            print(f"Balance: {balance['balance']} {balance['unit']}")
            
            # Get account summary
            summary = await account.get_account_summary()
            print(f"Total transactions: {summary['transactions_count']}")
            
        asyncio.run(main())
        ```
        
        Concurrent operations:
        
        ```python
        import asyncio
        from pyalby import AsyncAccount
        
        async def get_all_account_info():
            account = AsyncAccount()
            
            # Run multiple operations concurrently
            balance, summary, personal_info = await asyncio.gather(
                account.get_balance(),
                account.get_account_summary(),
                account.get_personal_info()
            )
            
            return balance, summary, personal_info
            
        asyncio.run(get_all_account_info())
        ```
    
    Note:
        Requires ALBY_ACCESS_TOKEN and BASE_URL environment variables to be set.
        This is experimental software - do not use for storing large amounts.
    """

    def __init__(self):
        """
        Initializes the AsyncAccount instance with base URL and access token from environment variables.
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

    async def get_value4value(self):
        """
        Retrieves the user's Lightning Address and keysend information.

        Returns:
            dict: A dictionary containing keysend_pubkey, keysend_custom_key,
                  keysend_custom_value, and lightning_address.
        """
        url = f"{self.base_url}/user/value4value"
        return await make_async_get_request(url, self.headers)

    async def get_balance(self):
        """
        Retrieves the balance of the user's wallet.

        Returns:
            dict: A dictionary containing balance, currency, and unit.
        """
        url = f"{self.base_url}/balance"
        return await make_async_get_request(url, self.headers)

    async def get_account_summary(self):
        """
        Retrieves the account summary including balance, transaction count, and boostagram count.

        Returns:
            dict: A dictionary containing balance, boostagrams_count, currency,
                  invoices_count, last_invoice_at, transactions_count, and unit.
        """
        url = f"{self.base_url}/user/summary"
        return await make_async_get_request(url, self.headers)

    async def get_personal_info(self):
        """
        Retrieves the user's personal information including e-mail address, display name, avatar,
        nostr pubkey, and value4value information.

        Returns:
            dict: A dictionary containing identifier, email, name, avatar, keysend_custom_key,
                  keysend_custom_value, keysend_pubkey, lightning_address, and nostr_pubkey.
        """
        url = f"{self.base_url}/user/me"
        return await make_async_get_request(url, self.headers)