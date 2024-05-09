import os
import requests
import logging
from dotenv import load_dotenv
from pyalby.utils import make_post_request

# Load environment variables
load_dotenv()

class Payment:
    """
       A class to interact with the Alby API to do payments.
       """
    def __init__(self):
        """
        Initializes the Payment instance with base URL and access token from environment variables.
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

    def bolt11_payment(self, invoice):
        """Pay a lightning invoice (bolt11).

        Args:
            invoice (str): The BOLT11 invoice string to be paid.

        Returns:
            dict: Information about the successfully paid invoice.
        """
        url = f"{self.base_url}/payments/bolt11"
        data = {"invoice": invoice}
        return make_post_request(url, data, self.headers)

    def keysend_payment(self, amount, destination, memo=None, custom_records=None):
        """Send a spontaneous payment (keysend).

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

        return make_post_request(url, data, self.headers)

    def multi_keysend_payment(self, keysends):
        """Make multiple keysend payments in a single request.

        Args:
            keysends (list of dict): A list of keysend payment objects.

        Returns:
            list of dict: Each object represents an individual payment response.
        """
        url = f"{self.base_url}/payments/keysend/multi"
        data = {"keysends": keysends}

        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
