from datetime import datetime
from dateutil.tz import gettz

def isIndiaFriendlyTime():
    dtobj = datetime.now(tz=gettz('Asia/Kolkata'))
    hour=dtobj.hour
    print(dtobj)
    if hour>=8 and hour<=22:
        return True
    return False


def isUSFriendlyTime():
    dtobj = datetime.now(tz=gettz('US/Seattle'))
    hour = dtobj.hour
    print(dtobj)
    if hour>=8 and hour<=22:
        return True
    return False

def getPSTTime():
    dtobj = datetime.now(tz=gettz('US/Seattle'))
    return dtobj.strftime('%Y%m%d %H:%M')
