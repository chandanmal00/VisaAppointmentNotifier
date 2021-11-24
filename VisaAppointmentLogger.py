
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import VisaAppointmentConstants

#filename = "/tmp/debug.log"
filename = "D:\data\data\debug.log"
#to write to stdout
# logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logging.basicConfig(filename = filename, filemode='a', level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = TimedRotatingFileHandler(filename, when="h", interval=4, backupCount=5)
handler.setFormatter(logFormatter)
handler.suffix = VisaAppointmentConstants.DT_FORMAT
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

for logger_name_skip in ['telethon.network', 'telethon.crypto']:
    log = logging.getLogger(logger_name_skip)
    log.setLevel(logging.WARN)

def getLogger():
    return logger
