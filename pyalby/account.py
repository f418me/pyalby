import requests
import os
from dotenv import load_dotenv

load_dotenv()


class Account:

    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.access_token = os.getenv('ALBY_ACCESS_TOKEN')
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def get_value4value(self):
        url = f"{self.base_url}/user/value4value"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_balance(self):
        url = f"{self.base_url}/balance"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_account_summary(self):
        url = f"{self.base_url}/user/summary"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_personal_info(self):
        url = f"{self.base_url}/user/me"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()