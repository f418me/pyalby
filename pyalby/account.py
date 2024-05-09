import os
import logging
from dotenv import load_dotenv
from pyalby.utils import make_get_request

# Load environment variables from the `.env` file
load_dotenv()

class Account:
    """
    A class to interact with the Alby API to retrieve account information.
    """

    def __init__(self):
        """
        Initializes the Account instance with base URL and access token from environment variables.
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

    def get_value4value(self):
        """
        Retrieves the user's Lightning Address and keysend information.

        Returns:
            dict: A dictionary containing keysend_pubkey, keysend_custom_key,
                  keysend_custom_value, and lightning_address.
        """
        url = f"{self.base_url}/user/value4value"
        return make_get_request(url, self.headers)

    def get_balance(self):
        """
        Retrieves the balance of the user's wallet.

        Returns:
            dict: A dictionary containing balance, currency, and unit.
        """
        url = f"{self.base_url}/balance"
        return make_get_request(url, self.headers)

    def get_account_summary(self):
        """
        Retrieves the account summary including balance, transaction count, and boostagram count.

        Returns:
            dict: A dictionary containing balance, boostagrams_count, currency,
                  invoices_count, last_invoice_at, transactions_count, and unit.
        """
        url = f"{self.base_url}/user/summary"
        return make_get_request(url, self.headers)

    def get_personal_info(self):
        """
        Retrieves the user's personal information including e-mail address, display name, avatar,
        nostr pubkey, and value4value information.

        Returns:
            dict: A dictionary containing identifier, email, name, avatar, keysend_custom_key,
                  keysend_custom_value, keysend_pubkey, lightning_address, and nostr_pubkey.
        """
        url = f"{self.base_url}/user/me"
        return make_get_request(url, self.headers)
