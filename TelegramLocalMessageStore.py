import os.path
import VisaAppointmentLogger
import TimeUtilities
from datetime import datetime
from datetime import timedelta
logger = VisaAppointmentLogger.getLogger()
#filename = "D:\data\data\store.log"
filename = "/tmp/store.log"

def readFilePrintMessages():
    out = set([])
    local_filename, local_filename_hr_back = TimeUtilities.getFileNames(filename)
    logger.info("local store file names: {} {}".format(local_filename, local_filename_hr_back))
    for fnames in [local_filename, local_filename_hr_back]:
        if os.path.exists(local_filename):
            fw = open(local_filename, "r")
            for line in fw:
                #print("data in file is:",line, line [:-1])
                line=line[:-1]
                out.add(line)
            fw.close()
    return out

def  writeMessageToFile(messages):
    out = set([])
    #we want to open in append mode, so we can add to the file
    local_filename, local_filename_hr_back = TimeUtilities.getFileNames(filename)
    fw = open(local_filename, "a")
    for message in messages:
        logger.info("Writing message: {}".format(message.id))
        if message.id in out:
            continue
        logger.info("Wrote message: {}".format(message.id))
        fw.write(str(message.id)+"\n")
        out.add(message.id)
    fw.close()
