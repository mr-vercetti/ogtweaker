import logging

logger = logging
date_format = "%d-%m-%y %H:%M:%S"
msg_format = "%(asctime)s: %(levelname)s: %(message)s"
logger.basicConfig(format=msg_format, datefmt=date_format, level=logging.ERROR)