#!/user/bin/env python3.6

# Based on https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
import logging

# Set up logging
logging.basicConfig(filename='blaulicht_tracker.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

def add_to_log(text, level):
    """
    Log text with level
    """
    level = level.lower()
    if level == 'debug':
        logging.debug(text)
    elif level == 'info':
        logging.info(text)
    elif level == 'warning':
        logging.warning(text)
    elif level == 'error':
        logging.error(text)
    elif level == 'critical':
        logging.critical(text)
    else:
        logging.error(f'Trying to log "{text}", but no usable level was provided!')
