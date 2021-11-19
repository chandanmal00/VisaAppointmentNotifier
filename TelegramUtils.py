import telegram
import VisaAppointmentSecrets
import VisaAppointmentLogger
logger = VisaAppointmentLogger.getLogger()
bot = telegram.Bot(token=VisaAppointmentSecrets.telegram_bot_token)

def sendTelegramMessage(message, senders):
    if message is None:
        message = "It seems there is a slot, check in Telegram H4 group channel: H1B/H4 Visa Dropbox slots( No Questions only slot availability messages)"
    for sender in senders:
        bot.send_message(sender, message)
        logger.info("Sending sender:{}, message: {}".format(sender, message))
