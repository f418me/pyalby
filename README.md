# pyalby

A Python library for accessing the [Alby Wallet API](https://guides.getalby.com/developer-guide/v/alby-wallet-api/) with both synchronous and asynchronous support. 


<!-- ABOUT THE PROJECT -->
## About The Project

The pyalby library provides a simple way for interacting with the [Alby Wallet API](https://guides.getalby.com/developer-guide/v/alby-wallet-api/) in Python applications. It supports both synchronous and asynchronous operations, making it suitable for various use cases.

### Key Features

- **Dual API Support**: Both synchronous and asynchronous interfaces
- **API Coverage**: Account management, invoice operations, and payment processing
- **Lightning Network Integration**: BOLT11 invoices, keysend payments, and multi-payments
- **Comprehensive Testing**: Unit and integration tests for reliability

### ⚠️ Important Notice

This library is designed for experimental micro-payment applications. Use at your own risk. Always refer to the [official Alby API documentation](https://guides.getalby.com/developer-guide/v/alby-wallet-api/) for the most up-to-date information.


## Technology Stack

### Requirements
- **Python**: 3.10, 3.11, or 3.12
- **Build System**: Poetry (recommended) or pip with setuptools

### Core Dependencies
- **requests** (^2.32.0): HTTP client for synchronous API communication
- **aiohttp** (^3.13.0): HTTP client for asynchronous API communication  
- **python-dotenv** (^1.0.1): Environment variable management

### Development Dependencies
- **pytest** (^8.3.0): Testing framework
- **pytest-asyncio** (^0.23.8): Async testing support
- **responses** (^0.25.0): HTTP request mocking for sync tests
- **aioresponses** (^0.7.6): HTTP request mocking for async tests

### Architecture
- **Synchronous Classes**: `Account`, `Invoice`, `Payment` - for traditional blocking operations
- **Asynchronous Classes**: `AsyncAccount`, `AsyncInvoice`, `AsyncPayment` - for non-blocking operations
- **Shared Utilities**: Common HTTP utilities and error handling
- **Environment Configuration**: Centralized configuration via environment variables

### Project Structure
```
pyalby/
├── pyalby/                 # Main library package
│   ├── __init__.py        # Package exports (sync + async classes)
│   ├── account.py         # Synchronous Account API
│   ├── async_account.py   # Asynchronous Account API
│   ├── invoice.py         # Synchronous Invoice API
│   ├── async_invoice.py   # Asynchronous Invoice API
│   ├── payment.py         # Synchronous Payment API
│   ├── async_payment.py   # Asynchronous Payment API
│   ├── utils.py           # Synchronous HTTP utilities
│   └── async_utils.py     # Asynchronous HTTP utilities
├── tests/
│   ├── unit/              # Unit tests (mocked)
│   └── integration/       # Integration tests (real API)
├── examples/              # Usage examples
└── docs/                  # Documentation
```

<!-- GETTING STARTED -->
## Getting Started

### Installation

#### From PyPI (Recommended)
```bash
pip install pyalby
```

#### Development Installation

**With Poetry (Recommended)**
```bash
git clone https://github.com/f418me/pyalby.git
cd pyalby
poetry install
poetry shell
```

**With pip**
```bash
git clone https://github.com/f418me/pyalby.git
cd pyalby
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### Configuration

You need an Alby account and Alby Hub to use the API.

#### Prerequisites

1. **Create an Alby account** at [getalby.com](https://getalby.com)
2. **Set up Alby Hub** at [albyhub.com](https://albyhub.com/) - This is required for API access and Lightning Network functionality
3. **Generate an access token** in your Alby Hub dashboard
4. **Set up environment variables**:

```bash
# Copy the example file
cp .env-example .env

# Edit .env with your credentials
BASE_URL=https://api.getalby.com
ALBY_ACCESS_TOKEN=your_access_token_here
LOG_LEVEL=INFO
```

Or set the environment variable directly:
```bash
export ALBY_ACCESS_TOKEN=your_access_token_here
```


<!-- USAGE EXAMPLES -->
## Usage

The library provides both synchronous and asynchronous interfaces. You can use either or both depending on your needs.

### Synchronous Usage (Traditional)

```python
from pyalby import Account, Invoice, Payment
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Initialize clients
    account = Account()
    invoice = Invoice()
    payment = Payment()

    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=os.getenv("LOG_LEVEL", "INFO")
    )

    # Fetch account information
    balance = account.get_balance()
    print(f"Balance: {balance['balance']} {balance['currency']}")

    # Create an invoice
    inv = invoice.create_invoice(
        amount=100, 
        description="Test Invoice"
    )
    print(f"Invoice created: {inv['payment_request']}")

    # Pay an invoice (use a real BOLT11 invoice)
    # payment_result = payment.bolt11_payment("lnbc110n1pn...")
    # print(f"Payment result: {payment_result}")

if __name__ == "__main__":
    main()
```

### Asynchronous Usage (High Performance)

```python
import asyncio
from pyalby import AsyncAccount, AsyncInvoice, AsyncPayment

async def main():
    # Initialize async clients
    account = AsyncAccount()
    invoice = AsyncInvoice()
    payment = AsyncPayment()

    try:
        # Fetch multiple pieces of information concurrently
        balance_task = account.get_balance()
        summary_task = account.get_account_summary()
        invoices_task = invoice.get_incoming_invoices()

        # Wait for all operations to complete
        balance, summary, invoices = await asyncio.gather(
            balance_task, summary_task, invoices_task
        )

        print(f"Balance: {balance['balance']} {balance['currency']}")
        print(f"Account items: {len(summary)}")
        print(f"Invoices: {len(invoices)}")

        # Create an invoice asynchronously
        new_invoice = await invoice.create_invoice(
            amount=50,
            description="Async Test Invoice"
        )
        print(f"Async invoice created: {new_invoice['payment_request']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Mixed Usage (Gradual Migration)

You can use both sync and async classes in the same application:

```python
import asyncio
from pyalby import Account, AsyncAccount, AsyncInvoice

async def mixed_example():
    # Use sync for simple operations
    sync_account = Account()
    balance = sync_account.get_balance()
    print(f"Current balance: {balance['balance']}")

    # Use async for operations that benefit from concurrency
    async_account = AsyncAccount()
    async_invoice = AsyncInvoice()

    # Run multiple async operations concurrently
    account_info, invoices = await asyncio.gather(
        async_account.get_account_summary(),
        async_invoice.get_incoming_invoices()
    )

    print(f"Account info: {len(account_info)} items")
    print(f"Invoices: {len(invoices)} found")

if __name__ == "__main__":
    asyncio.run(mixed_example())
```

### Available Classes and Methods

#### Synchronous Classes
- **`Account`**: Account information and balance
  - `get_balance()`, `get_account_summary()`, `get_value4value()`, `get_personal_info()`
- **`Invoice`**: Invoice management  
  - `create_invoice()`, `get_incoming_invoices()`, `get_outgoing_invoices()`, `get_invoice()`, `decode_invoice()`
- **`Payment`**: Payment processing
  - `bolt11_payment()`, `keysend_payment()`, `multi_keysend_payment()`

#### Asynchronous Classes
- **`AsyncAccount`**: Async account operations
- **`AsyncInvoice`**: Async invoice operations  
- **`AsyncPayment`**: Async payment operations

All async classes have identical method signatures to their sync counterparts, but return coroutines that must be awaited.

### Examples

Check the `examples/` directory for more comprehensive usage examples:
- `mixed_usage_example.py`: Demonstrates all mixed sync/async patterns
- Additional examples for specific use cases

The `tests/` directory also contains extensive examples of library usage.

### Testing

**Run all tests:**
```bash
# With Poetry
poetry run pytest

# With pip
pytest
```

**Run specific test types:**
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only (requires valid API token)
pytest tests/integration/

# Mixed usage tests
pytest tests/unit/test_mixed_usage.py
```



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development Notes

### Testing Considerations
- **Integration tests** make real API calls and may send actual payments
- **Unit tests** use mocked responses and are safe to run
- Set up a test environment with minimal funds for integration testing

### Performance
- **Async classes** provide significant performance benefits for concurrent operations
- **Sync classes** are simpler for basic use cases and scripts
- **Mixed usage** allows gradual migration and optimal performance per use case

### Error Handling
Both sync and async classes provide consistent error handling:
- HTTP errors are propagated with detailed information
- Connection errors include retry suggestions  
- Timeout errors indicate network issues

<!-- LICENSE -->
## License

The projec pyalby is released under the terms of the MIT license. See [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT) for further information.


<!-- CONTACT -->
## Contact

[f418.me](https://f418.me) - [info@f418.me](mailto:info@f418.me) - 


