
import requests
import bs4 as bs
import json
import json
from datetime import datetime
import time
import VisaAppointmentLogger
import traceback

logger = VisaAppointmentLogger.getLogger()

def getResponse(url):

    #send headers as browser
    headers = {
    #     'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    #     'Accept-Encoding' : 'gzip, deflate, br',
    #     'Accept-Language' : 'en-US,en;q=0.5',
    #     'Connection' : 'keep-alive',
    #     'DNT' : '1',
    #     'Sec-Fetch-Dest' : 'document',
    #     'Sec-Fetch-Mode' : 'navigate',
    #     'Sec-Fetch-Site' : 'cross-site',
    #     'Sec-GPC' : '1',
    #     'TE' : 'trailers',
    #     'Upgrade-Insecure-Requests' : '1',
         'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0',
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = json.loads(resp.text)
            if 'records' in data:
                status = data['records'][0]['fields']["Status"]
                logger.info("Status is: {}".format(status))
                if status=="Done":
                    return 1
    except Exception as e:
        logger.error("Error checknig the website for status:{}, trace:{}".format(e, traceback.format_exc()))
        j=0
    return 0


def checkOnlineStatus():
    #https: // v1.nocodeapi.com / cmaloo / airtable / ESoExvuzNuhgkqze?tableName = Table1
    #https://v1.nocodeapi.com/cmaloo/airtable/ESoExvuzNuhgkqze?tableName=Table1
    #{"records":[{"id":"recG2BkY6p7vo76Lm","fields":{"Name":"value","Notes":"1\n","Status":"Done"},"createdTime":"2021-11-23T02:16:33.000Z"}]}
    #{"records":[{"id":"recG2BkY6p7vo76Lm","fields":{"Name":"value","Notes":"1\n","Status":"Todo"},"createdTime":"2021-11-23T02:16:33.000Z"}]}
    dt = datetime.now()
    logger.info("Trying to check hour:{}".format(dt.hour))
    if dt.hour == 21 and dt.minute == 30 and dt.second>=25:
        logger.info("checked status for hour:{}".format(dt.hour, dt.minute))
        out = getResponse("https://v1.nocodeapi.com/cmaloo/airtable/ESoExvuzNuhgkqze?tableName=Table1")
        logger.info("Sleeping 20 seconds as we checked: status: {}".format(out))
        time.sleep(20)
        return out
    return 0
