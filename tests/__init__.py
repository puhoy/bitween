from bitween.log import setup_logging
import logging
import os

os.environ['BITWEEN_TESTING'] = "True"


setup_logging(default_level=logging.ERROR)