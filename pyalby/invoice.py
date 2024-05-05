import os
import requests
from dotenv import load_dotenv

# Load environment variables from the `.env` file
load_dotenv()


class Invoice:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.access_token = os.getenv('ALBY_ACCESS_TOKEN')
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def create_invoice(
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

        # Remove any optional arguments with None values
        data = {k: v for k, v in data.items() if v is not None}

        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_incoming_invoices(
            self,
            created_at_gt=None,
            created_at_lt=None,
            since=None,
            before=None,
            page=1,
            items=25,
    ):
        """Get the list of incoming invoices with optional filters.

        Args:
            created_at_gt (int, optional): Invoices created after this Unix timestamp.
            created_at_lt (int, optional): Invoices created before this Unix timestamp.
            since (str, optional): Invoices created after the given identifier.
            before (str, optional): Invoices created before the given identifier.
            page (int, optional): Page number. Defaults to 1.
            items (int, optional): Number of items per page. Defaults to 25.

        Returns:
            list: List of incoming invoices.
        """
        url = f"{self.base_url}/invoices/incoming"
        params = {
            "q[created_at_gt]": created_at_gt,
            "q[created_at_lt]": created_at_lt,
            "q[since]": since,
            "q[before]": before,
            "page": page,
            "items": items,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_outgoing_invoices(
            self,
            created_at_gt=None,
            created_at_lt=None,
            since=None,
            before=None,
            page=1,
            items=25,
    ):
        """Get the list of outgoing invoices with optional filters.

        Args:
            created_at_gt (int, optional): Invoices created after this Unix timestamp.
            created_at_lt (int, optional): Invoices created before this Unix timestamp.
            since (str, optional): Invoices created after the given identifier.
            before (str, optional): Invoices created before the given identifier.
            page (int, optional): Page number. Defaults to 1.
            items (int, optional): Number of items per page. Defaults to 25.

        Returns:
            list: List of outgoing invoices.
        """
        url = f"{self.base_url}/invoices/outgoing"
        params = {
            "q[created_at_gt]": created_at_gt,
            "q[created_at_lt]": created_at_lt,
            "q[since]": since,
            "q[before]": before,
            "page": page,
            "items": items,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_specific_invoice(self, payment_hash):
        """Get details about a specific invoice.

        Args:
            payment_hash (str): Payment hash of the specific invoice.

        Returns:
            dict: Details of the specified invoice.
        """
        url = f"{self.base_url}/invoices/{payment_hash}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def decode_invoice(self, bolt11_invoice):
        """Decode a Bolt11 invoice.

        Args:
            bolt11_invoice (str): Bolt11 invoice string to decode.

        Returns:
            dict: Decoded invoice information.
        """
        url = f"{self.base_url}/decode/bolt11/{bolt11_invoice}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

