# pyalby

A python library of methods for accessing [Alby Wallet API](https://guides.getalby.com/developer-guide/v/alby-wallet-api/). 


<!-- ABOUT THE PROJECT -->
## About The Project

<!-- 
[![Product Name Screen Shot][product-screenshot]](https://example.com)
-->
The python library pyalby contains methods for accessing [Alby Wallet API](https://guides.getalby.com/developer-guide/v/alby-wallet-api/). 
The main purpose of this library is to provide a simple way to interact with the Alby API when using python.

Note:
Custodial Wallets are not recommended for the use of storing large amounts.
This library is for experimental purposes in the area of micro-payments. Use it at your own risk.
This library is not a replacement for the official Alby API documentation. It is recommended to read the official documentation before using this library.


<!-- GETTING STARTED -->
## Getting Started

### Clone the repo

Requires Python 3.10 or 3.11

```
git clone https://github.com/f418me/pyalby.git
cd pyalby
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Library Installation

```
pip install pyalby
````

## Alby Access Token

You need an alby account and generate an access token to use the API.
Copy .env-example to .env and update the variables with your Alby token.
Or just set the environment variable ALBY_ACCESS_TOKEN.

```
BASE_URL = https://api.getalby.com
ALBY_ACCESS_TOKEN = XYZ
LOG_LEVEL = INFO
```


<!-- USAGE EXAMPLES -->
## Usage
After the import of pyalby you can access the complete API using the related methods. In the tests folder you find all examples of the usage of the library.

 ```bash
from pyalby import Account, Invoice, Payment
import logging
import os

# Load environment variables
load_dotenv()

def main():
    
    account = Account()
    invoice = Invoice()
    payment = Payment()

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=str(os.getenv("LOG_LEVEL")))

    # Fetch account summary
    summary_data = account.get_account_summary()
    print("Account Summary:", summary_data)

    # Create an invoice
    inv = invoice.create_invoice(amount=100, description="Alby Test Invoice")
    print("Invoice created successfully")
    print(inv)

    # Pay an invoice
    pay = payment.bolt11_payment("lnbc110n1pn...")
    print(pay)


if __name__ == "__main__":
    main()
   ```

<!-- ROADMAP -->
## Roadmap

- [ ] Add Webhook API
- [ ] Add GitHub Docs pages
- [ ] Add Support of async requests
- [ ] CI pipeline
- [ ] Add Python 3.12 support


See the [open issues](https://github.com/f418me/pyalby/issues) for a full list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Other

Be aware that the integration tests send real keysend payments.

<!-- LICENSE -->
## License

The projec pyalby is released under the terms of the MIT license. See [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT) for further information.


<!-- CONTACT -->
## Contact

[f418.me](https://f418.me) - [info@f418.me](mailto:info@f418.me) - 


