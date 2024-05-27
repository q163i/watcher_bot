import logging
import sys
from config import LOG_LEVEL, LOG_FORMAT

def custom_logger():
    logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL, format=LOG_FORMAT)
    return logging.getLogger()