import logging

import TelegramLocalMessageStore
import TelegramUtils
import TimeUtilities
import TwilioSendTextMessage
from telethon import TelegramClient, events, sync
import datetime
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetDialogsRequest
import sys
import VisaAppointmentConstants

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

message_src = None
if len(sys.argv)>=2:
    message_src = "From here:" + sys.argv[1]
if message_src is None:
    message_src = "CommandLine:"

logger.info("--"*15)
logger.info('Run started...')

api_id = VisaAppointmentConstants.telegram_api_id
api_hash = VisaAppointmentConstants.telegram_api_hash

client = TelegramClient('session_name1', api_id, api_hash)
client.start()

def getAllMessages(messages):
    mess={}
    for m in messages:
        mess[m.id] = m
        print(m.date, m.id, m.message)
    return mess

def getTextMessages(messages):
    out=[]
    for m in messages:
        if isBlacklistMessage(m):
            continue
        if not m.media:
            #ignore messages with ? mark and big messages too
            if '?' in m.message or len(m.message)>=20:
                continue
            if 'ss' in m.message.lower() or 'available' in m.message.lower() or 'bulk' in m.message.lower():
                print(m.date, m.id, m.message)
                out.append(m)
    return out

def isBlacklistMessage(message):
    if message.message:
        mesg_lower = message.message.lower()
        if 'fake' in mesg_lower or 'spam' in mesg_lower or 'old' in mesg_lower:
            print("Blacklist message spotted : {}".format(mesg_lower))
            return True
    return False

def getMediaMessages(messages):
    messages_out=[]
    for m in messages:
        #only photo media
        if isBlacklistMessage(m):
            continue
        if m.media and hasattr(m.media,'photo'):
            #
            if m.message:
                continue
            print(m.date, m.id, m.media)
            messages_out.append(m)
    return messages_out

def get_entity_data(entity_id, limit):
    entity = client.get_entity(entity_id)
    today = datetime.datetime.today()
    posts = client(GetHistoryRequest(
                   peer=entity,
                   limit=limit,
                   offset_date=None,
                   offset_id=0,
                   max_id=0,
                   min_id=0,
                   add_offset=0,
                   hash=0))
    messages = []
    for message in posts.messages:
        messages.append(message)
    return messages

def writeMessagesToFile(messages_out):
    TelegramLocalMessageStore.writeMessageToFile(messages_out)

def getSeenMessages():
    out = TelegramLocalMessageStore.readFilePrintMessages()
    print("Seen is", out)
    return out

def getEntityMessgaes(entities, last_no_message):
    for entity in entities:
        title = entity.title
        id = entity.id
        messages = get_entity_data(entity.id, last_no_message)
        print(title + ' :' + str(id))
        print(messages)
        print('#######')

def filterSeenMessages(seen, messages_out):
    messages_out_unseen = []
    for mesg in messages_out:
        print(mesg.id, seen)
        if mesg.id in seen or str(mesg.id) in seen:
            continue
        else:
            messages_out_unseen.append(mesg)
    return messages_out_unseen

def sendMessage(cnt, ratio, sms_users):
    #only send if there are more than 1 message and its friendly time
    if TimeUtilities.isUSFriendlyTime():
        print("US friendly time")
        TwilioSendTextMessage.sendSMS("There are {} messages, ratio:{}, login and book VISA, time:{} PST".format(cnt, round(ratio,1), TimeUtilities.getPSTTime()), sms_users)

    if TimeUtilities.isIndiaFriendlyTime():
        sms_users = VisaAppointmentConstants.india_sms_numbers
        print("India friendly time")
        TwilioSendTextMessage.sendSMS("There are {} messages, ratio:{}, login and book VISA, time:{} PST".format(cnt, round(ratio,1),TimeUtilities.getPSTTime()), sms_users)

result = client(GetDialogsRequest(
             offset_date=None,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=100,
             hash=0))
entities = result.chats
##If we want to get last x messages from a channel, max is 100 (limited by Telegram)
#getEntityMessgaes(100)

##mesages from a specific entity, it only returns last 100 messages
messages = get_entity_data(1371184682, 100)
print("messages retrieved:", len(messages))
seen= getSeenMessages()
#added to avoid messaging multiple more than 5 times
total_cnt = 0
messages_out = getMediaMessages(messages)
messages_out_unseen=filterSeenMessages(seen, messages_out)
total_cnt = len(messages_out)
message_type = []
if len(messages_out_unseen)>0:
    message_type.append("media")

messages_out+= getTextMessages(messages)
messages_out_unseen1=filterSeenMessages(seen, messages_out)
total_cnt += len(messages_out)
if len(messages_out_unseen1)>0:
    message_type.append("text")

messages_out_unseen = messages_out_unseen + messages_out_unseen1


cnt=len(messages_out_unseen)
print("Filtered cnt:", cnt, [message.id for message in messages_out], [message.id for message in messages_out_unseen])

user_ids=VisaAppointmentConstants.telegram_user_ids
sms_users = VisaAppointmentConstants.us_sms_numbers
#url to validate Pranoy/Chandni number https://console.twilio.com/us1/develop/phone-numbers/manage/verified?frameUrl=%2Fconsole%2Fphone-numbers%2Fverified%3FphoneNumberContains%3D4254948233%26friendlyNameContains%3DanotherOne%26__override_layout__%3Dembed%26bifrost%3Dtrue%26x-target-region%3Dus1
if cnt>=1:
    if cnt>=3:
        ratio = cnt / total_cnt
        out_mesg = "{}: we have {} messages of type:{}, ratio unseen/seen is {} and date is {}, do check Bulk Login Slots... ".format(message_src, cnt, ':'.join(message_type), round(ratio,1), messages_out_unseen[0].date)
        TelegramUtils.sendTelegramMessage(out_mesg, user_ids)
        if ratio>=0.6:
            sendMessage = 1
            #sendMessage(cnt, ratio, sms_users)
    else:
        out_mesg = "{}: we have {} messages of type:{} and date is {}, check Telegram Message channel - H1B/H4 Visa Dropbox slots( No Questions only slot availability messages".format(message_src, cnt, ':'.join(message_type), messages_out_unseen[0].date)
        TelegramUtils.sendTelegramMessage( out_mesg, user_ids)

    writeMessagesToFile(messages_out_unseen)
    # https://dashboard.sinch.com/sms/api/rest  need to us api, https://www.geeksforgeeks.org/send-sms-updates-mobile-phone-using-python/
    # MessageUtils.sendTextMessage()
else:
    logger.info("NOTHING to do HERE, sit and chill")
