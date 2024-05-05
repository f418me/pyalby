import logging

# Setting up logging for the package
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Package constants or configurations
PACKAGE_CONSTANT = "Some important value"

# Making classes easily importable
from .account import Account