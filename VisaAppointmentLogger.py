from logging.handlers import TimedRotatingFileHandler

filename = "D:\data\data\debug.log"

#to write to stdout
# logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = TimedRotatingFileHandler(filename, when="h", interval=4, backupCount=5)
logging.basicConfig(filename = filename, filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

for logger_name_skip in ['telethon.network', 'telethon.crypto']:
    log = logging.getLogger(logger_name_skip)
    log.setLevel(logging.WARN)

def getLogger():
    return logger
