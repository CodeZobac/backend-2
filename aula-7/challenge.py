import logging
from logging.handlers import TimedRotatingFileHandler

# Configure logging to rotate log files daily
logger = logging.getLogger("daily_logger")
logger.setLevel(logging.DEBUG)

# Create a TimedRotatingFileHandler
handler = TimedRotatingFileHandler("daily_log.log", when="midnight", interval=1, backupCount=7)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Example log messages
logger.info("Logging setup complete.")
logger.debug("This is a debug message.")