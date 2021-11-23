import json
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
import VisaAppointmentSecrets
import VisaAppointmentConstants
import VisaAppointmentLogger
import time
import checkOnlineStatus

send_sms_flag = True
logger = VisaAppointmentLogger.getLogger()
MESSAGE_ABOVE_LEN_IGNORE = 30
message_src = None
if len(sys.argv)>=2:
    message_src = "From here:" + sys.argv[1]
if message_src is None:
    message_src = "CommandLine:"

logger.info("--"*15)
logger.info('Run started...')

api_id = VisaAppointmentSecrets.telegram_api_id
api_hash = VisaAppointmentSecrets.telegram_api_hash

client = TelegramClient('session_name1', api_id, api_hash)
client.start()

def getAllMessages(messages):
    mess={}
    for m in messages:
        mess[m.id] = m
        logger.debug("date:{}, id: {}, message:{}".format(m.date, m.id, m.message))
    return mess

def getTextMessages(messages):
    out = []
    from_user_id_set = set()
    for m in messages:
        if ignoreNotRelevantMessages(m):
            continue
        if not m.media:
            mesg_lower = m.message.lower()
            from_user_id = m.from_id.user_id #from_id is the user who send the message
            for keyword_good in VisaAppointmentConstants.LIST_MESSAGES_KEYWORDS_GOOD:
                if keyword_good in mesg_lower and from_user_id not in from_user_id_set:
                    logger.debug("date:{}, id: {}, message:{}, type:text".format(m.date, m.id, m.message))
                    from_user_id_set.add(from_user_id) # we want to consider only 1 message from an user
                    out.append(m)
                    break
    return out

def ignoreNotRelevantMessages(message):
    if message.message:
        mesg_lower = message.message.lower()
        if len(mesg_lower) >= MESSAGE_ABOVE_LEN_IGNORE:
            logger.debug("ignoreNotRelevantMessages message spotted(reduced to 30 chars) : {}, isMediaMessage: {}".format(mesg_lower[:MESSAGE_ABOVE_LEN_IGNORE].replace("\n", ""), True if message.media else False))
            return True
        for ignore_mesg_keyword in VisaAppointmentConstants.LIST_MESSAGES_KEYWORDS_IGNORE:
            if ignore_mesg_keyword in mesg_lower:
                logger.debug("ignoreNotRelevantMessages message spotted: {}, isMediaMessage: {}".format(mesg_lower.replace("\n",""), True if message.media else False ))
                return True
    return False

def getMediaMessages(messages):
    out = []
    from_user_id_set = set()
    for m in messages:
        #ignore non-relevant messages
        if ignoreNotRelevantMessages(m):
            continue
        # only photo media and 1 user per message to be considered
        from_user_id = m.from_id.user_id  # from_id is the user who send the message
        if m.media and hasattr(m.media, 'photo') and from_user_id not in from_user_id_set:
            logger.debug("date:{}, id: {}, message:{}, type:media".format(m.date, m.id, m.message))
            from_user_id_set.add(from_user_id)  # we want to consider only 1 message from an user
            out.append(m)
    return out

def getEntityData(entity_id, limit):
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
    logger.debug("Seen is {}".format(out))
    return out

def getEntityMessgaes(entities, last_no_message):
    for entity in entities:
        title = entity.title
        id = entity.id
        messages = getEntityData(entity.id, last_no_message)
        logger.info("title:{}, id:{}".format(title, str(id)))
        logger.info("messages: {}".format(messages))

def filterSeenMessages(seen, messages_out, message_type):
    messages_out_unseen = []
    for mesg in messages_out:
        if mesg.id in seen or str(mesg.id) in seen:
            logger.debug("message of type {} with id:{}, seen:{}".format(message_type, mesg.id, seen))
            continue
        else:
            logger.info("message is unseen: id:{}, type:{}, mesg:{}, seen:{}".format(mesg.id, message_type, mesg.message, seen))
            messages_out_unseen.append(mesg)
    return messages_out_unseen

def sendMessage(cnt, ratio, sms_users):
    #only send if there are more than 1 message and users friendly time
    if TimeUtilities.isUSFriendlyTime():
        logger.info("US friendly time")
        TwilioSendTextMessage.sendSMS("**BulkAppointment** There are {} messages, ratio:{}, login and book VISA, time:{} PST".format(cnt, round(ratio,1), TimeUtilities.getPSTTime()), sms_users)

    if TimeUtilities.isIndiaFriendlyTime():
        sms_users = VisaAppointmentSecrets.india_sms_numbers
        logger.info("India friendly time")
        TwilioSendTextMessage.sendSMS("**BulkAppointment** There are {} messages, ratio:{}, login and book VISA, time:{} PST".format(cnt, round(ratio,1),TimeUtilities.getPSTTime()), sms_users)

def triggerConditionCheck(cnt, total_cnt, message_type_list):
    ratio = cnt/total_cnt
    if 'media' in message_type_list and (ratio >= 0.5 or (cnt >= 4 and ratio >= 0.2)):
        return True

    if (cnt >= 4 and ratio >= 0.6) or (cnt >= 5 and ratio >= 0.32):
        return True
    
    if cnt >=6 :
        return True

    return False

def runApplication():
    ##This is super important for the utility to work, do not delete the lines below
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
    messages = getEntityData(1371184682, 100)
    logger.debug("messages retrieved: {}".format(len(messages)))
    seen = getSeenMessages()
    #added to avoid messaging multiple more than 5 times
    total_cnt = 0
    messages_out = getMediaMessages(messages)
    messages_out_unseen = filterSeenMessages(seen, messages_out, 'media')
    total_cnt = len(messages_out)
    message_type_list = []
    if len(messages_out_unseen)>0:
        message_type_list.append("media")

    #expand seen messages so that we do not double count them
    seen = set(list(seen) + [mesg.id for mesg in messages_out_unseen])
    logger.debug("updated seen is: {}".format(seen))
    messages_out+= getTextMessages(messages)
    messages_out_unseen1 = filterSeenMessages(seen, messages_out, 'text')
    total_cnt += len(messages_out)
    if len(messages_out_unseen1) > 0:
        message_type_list.append("text")

    messages_out_unseen = messages_out_unseen + messages_out_unseen1

    cnt = len(messages_out_unseen)
    logger.info("new message cnt:{}, ratio:{}, total_good_messages:{}, messages_downloaded:{}, out:{}, unseen:{}".format(cnt, cnt / total_cnt, total_cnt, len(messages), [message.id for message in messages_out], [message.id for message in messages_out_unseen]))

    telegram_user_ids=VisaAppointmentSecrets.telegram_user_ids
    sms_users = VisaAppointmentSecrets.us_sms_numbers
    #logger.info("Checking status:{}".format(checkOnlineStatus.checkOnlineStatusV2()))
    #url to validate Pranoy/Chandni number https://console.twilio.com/us1/develop/phone-numbers/manage/verified?frameUrl=%2Fconsole%2Fphone-numbers%2Fverified%3FphoneNumberContains%3D4254948233%26friendlyNameContains%3DanotherOne%26__override_layout__%3Dembed%26bifrost%3Dtrue%26x-target-region%3Dus1

    if checkOnlineStatus.checkOnlineStatus() == 1:
        send_sms_flag = False
        logger.info("We are done, so stopping SMS calls")
    else:
        logger.info("We will continue to SMS since we are not done yet")

    if cnt>=1:
        if cnt>=3:
            ratio = cnt / total_cnt
            out_mesg = "**IMP, Potential Bulk appointment**: {}: we have {} new messages of type:{}, ratio unseen/seen is {} and date is {}, do check Bulk Login Slots... ".format(message_src, cnt, ':'.join(message_type_list), round(ratio,1), messages_out_unseen[0].date)
            TelegramUtils.sendTelegramMessage(out_mesg, telegram_user_ids)
            #added this so we do not get bombarded in the interim if the latest messages all are for same event
            #added check for media type as we are getting false positves with text messages
            if triggerConditionCheck(cnt, total_cnt, message_type_list):
                logger.info("Potential Bulk appointment, Sending text message for {} new messages, ratio:{}".format(cnt, ratio))
                sendMesgCounter = 1 #not used right now
                if send_sms_flag:
                    sendMessage(cnt, ratio, sms_users)
                else:
                    logger.info("We are done, so stopping SMS")
            else:
                logger.info("Skipping sending text message for cnt:{}, ratio:{}".format(cnt, ratio))
        else:
             out_mesg = "{}: we have {} new messages of type:{} and date is {}, check Telegram Message channel - *H1B/H4 Visa Dropbox slots( No Questions only slot availability messages)*".format(message_src, cnt, ':'.join(message_type_list), messages_out_unseen[0].date)
             TelegramUtils.sendTelegramMessage(out_mesg, telegram_user_ids)

        writeMessagesToFile(messages_out_unseen)
        # https://dashboard.sinch.com/sms/api/rest  need to us api, https://www.geeksforgeeks.org/send-sms-updates-mobile-phone-using-python/
        # MessageUtils.sendTextMessage()
    else:
        logger.info("NOTHING to do HERE, sit and chill")

runApplication()

