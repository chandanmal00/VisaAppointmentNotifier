from datetime import datetime
from datetime import timedelta
from dateutil.tz import gettz
import VisaAppointmentLogger
import VisaAppointmentConstants

logger = VisaAppointmentLogger.getLogger()

def isIndiaFriendlyTime():
    dtobj = datetime.now(tz=gettz('Asia/Kolkata'))
    hour=dtobj.hour
    if hour>=8 and hour<=21:
        return True
    return False


def isUSFriendlyTime():
    dtobj = datetime.now(tz=gettz('US/Seattle'))
    hour = dtobj.hour
    if hour>=8 and hour<=21:
        return True
    return False

def getPSTTime():
    dtobj = datetime.now(tz=gettz('US/Seattle'))
    return dtobj.strftime('%Y%m%d %H:%M')

##this helps in having a rolling based hourly store
def getFileNames(filename):
    today = datetime.now().strftime(VisaAppointmentConstants.DT_FORMAT)
    today_24hr_back = (datetime.now() + timedelta(hours=-25)).strftime(VisaAppointmentConstants.DT_FORMAT)
    return filename + "_" + today, filename + "_" +today_24hr_back
