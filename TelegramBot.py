import json
import logging
import telegram
import VisaAppointmentConstants
import VisaAppointmentLogger
logger = VisaAppointmentLogger.getLogger()

bot = telegram.Bot(token=VisaAppointmentConstants.telegram_bot_token)
def sendMessageFromBot(user_ids):
    for id in user_ids:
        bot.send_message(id, "how are you")

def getUpdatesToBotMessages():
    updates = bot.getUpdates()
    user_ids=VisaAppointmentConstants.telegram_user_ids
    for u in updates:
        id= u['message']['chat']['id']
        user_ids.add(id)
        logger.info("Userid to add: {}".format(id))

if __name__ == '__main__':
    getUpdatesToBotMessages()

