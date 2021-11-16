import json
import logging
import telegram
import VisaAppointmentConstants
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



logger = logging.getLogger()
logger.setLevel(logging.INFO)

bot = telegram.Bot(token=VisaAppointmentConstants.telegram_bot_token)

updates = bot.getUpdates()
user_ids=set([2065464808])
for u in updates:
    id= u['message']['chat']['id']
    user_ids.add(id)
    print(id)
    #print(json_data)

for id in user_ids:
    bot.send_message(id, "how are you")