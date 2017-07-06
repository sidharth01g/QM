# Create a logger object.
import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME)
logger = logging.getLogger('your-module')

# Initialize coloredlogs.
import coloredlogs
coloredlogs.install(level='DEBUG')

# Some examples.
logger.debug("this is a debugging message")
logger.info("this is an informational message")
logger.warn("this is a warning message")
logger.error("this is an error message")
logger.critical("this is a critical message")
