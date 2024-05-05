import os
import logging
from dotenv import load_dotenv
class Config:
    def __init__(self):
        load_dotenv()

        self.MAX_AMOUNT = os.getenv('MAX_AMOUNT')
        self.LOG_LEVEL = os.getenv('LOG_LEVEL')

        log_level = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL }

        self.LOG_LEVEL_INT = log_level.get( self.LOG_LEVEL)
        self.LNBITS_URL = os.getenv('LNBITS_URL')
        self.LNBITS_IN_KEY = os.getenv('LNBITS_IN_KEY')
        self.LNBITS_ADMIN_KEY = os.getenv('LNBITS_ADMIN_KEY')