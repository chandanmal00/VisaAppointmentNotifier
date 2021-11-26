import telegram
import VisaAppointmentSecrets
import VisaAppointmentLogger
import TimeUtilities
logger = VisaAppointmentLogger.getLogger()
bot = telegram.Bot(token=VisaAppointmentSecrets.telegram_bot_token)

telegram_user_ids_india = VisaAppointmentSecrets.telegram_user_ids_india
telegram_user_ids_us = VisaAppointmentSecrets.telegram_user_ids_us

def sendMessage(message, senders):
    if message is None:
        message = "It seems there is a slot, check in Telegram H4 group channel: H1B/H4 Visa Dropbox slots( No Questions only slot availability messages)"
    for sender in senders:
        bot.send_message(sender, message)
        logger.info("Sending sender:{}, message: {}".format(sender, message))

def sendTelegramMessage(message):
    if TimeUtilities.isIndiaFriendlyTime():
        sendMessage(message, telegram_user_ids_india)
    if TimeUtilities.isUSFriendlyTime():
        sendMessage(message, telegram_user_ids_us)

    #for sender in senders:
