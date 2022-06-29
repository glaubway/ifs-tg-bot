from os import environ
import logging

if environ.get('LOGGING_LEVEL'):
    logging_level = environ.get('LOGGING_LEVEL')
else:
    logging_level = 'INFO'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging_level
)

def myLogger(app_name):
    return logging.getLogger(app_name)
