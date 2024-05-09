import logging

# Setting up logging for the package
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Making classes easily importable
from .account import Account
from .invoice import Invoice
from .payment import Payment

# List of all available classes for `from pyalby import *`
__all__ = ['Account', 'Invoice', 'Payment']