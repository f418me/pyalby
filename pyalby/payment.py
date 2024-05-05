import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Payment:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "https://api.getalby.com")
        self.access_token = os.getenv('ALBY_ACCESS_TOKEN')
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
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

        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

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

        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

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
