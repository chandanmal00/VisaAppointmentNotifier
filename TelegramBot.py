import json
import logging
import telegram
import VisaAppointmentConstants
import VisaAppointmentLogger
logger = VisaAppointmentLogger.getLogger()

###README
#See how to create a bot: https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot
##you need to work within telegram app: Enter @Botfather in the search tab and choose this bot.

##This will help you get the userIds whom you want to notify when an appointment is available.
#Typically the person who needs to get notified needs to sign with the Bot you create in the above setup,
#send a messgage to bot and will will use the blow function to poll who is sending message to the bot and it will also help in setting permissions which allows Bot to message you too

#Once you get this Id, add it to Secrets file: VisaAppointmentSecrets.py

bot = telegram.Bot(token=VisaAppointmentConstants.telegram_bot_token)
def sendMessageFromBot(user_ids):
    for id in user_ids:
        bot.send_message(id, "how are you")

def getUpdatesToBotMessages():
    updates = bot.getUpdates()
    user_ids=VisaAppointmentConstants.telegram_user_ids
    for u in updates:
        id = u['message']['chat']['id']
        user_ids.add(id)
        logger.info("Userid to add: {}".format(id))

if __name__ == '__main__':
    getUpdatesToBotMessages()
