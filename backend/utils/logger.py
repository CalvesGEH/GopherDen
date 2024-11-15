import logging
from pathlib import Path

LOGGER_LEVEL = "debug"
LOGGER_FILE = "gopherden.log"
    

fileLogger = logging.FileHandler(LOGGER_FILE)
fileLogger.setLevel(logging.DEBUG)
consoleLogger = logging.StreamHandler()
consoleLogger.setLevel(getattr(logging, LOGGER_LEVEL.upper(), 10))

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        fileLogger,
        consoleLogger
    ]
)
# Disables watchfile's file change logging
logging.getLogger('watchfiles.main').setLevel(logging.WARNING)

# Function to get or create a logger
def get_logger(name=None):
    if name is None:
        name = __name__
    return logging.getLogger(name)