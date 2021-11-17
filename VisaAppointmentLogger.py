
import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

for logger_name_skip in ['telethon.network', 'telethon.crypto']:
    log = logging.getLogger(logger_name_skip)
    log.setLevel(logging.WARN)

def getLogger():
    return logger
