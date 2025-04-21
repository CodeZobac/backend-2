import logging
from logging.handlers import TimedRotatingFileHandler

# Configure logging
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Create a handler that rotates log files daily
handler = TimedRotatingFileHandler("app.log", when="midnight", interval=1)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Log messages at different severity levels
logger.debug("This is a DEBUG message")
logger.info("This is an INFO message")
logger.warning("This is a WARNING message")
logger.error("This is an ERROR message")