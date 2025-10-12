import logging
import os

# Setting up logging for the package
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Allow setting logging level from an environment variable or default to INFO
log_level = os.getenv('LOG_LEVEL', 'INFO')
logger.setLevel(log_level)

# Making classes easily importable
from .account import Account
from .invoice import Invoice
from .payment import Payment

# Making async classes easily importable
from .async_account import AsyncAccount
from .async_invoice import AsyncInvoice
from .async_payment import AsyncPayment

# List of all available classes for `from pyalby import *`
__all__ = ['Account', 'Invoice', 'Payment', 'AsyncAccount', 'AsyncInvoice', 'AsyncPayment']