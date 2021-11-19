# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import VisaAppointmentSecrets
import VisaAppointmentLogger

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = VisaAppointmentSecrets.twilio_account_sid
auth_token = VisaAppointmentSecrets.twilio_auth_token
logger =  VisaAppointmentLogger.getLogger()

def sendSMS(send_message, toList):
    client = Client(account_sid, auth_token)
    if toList is None:
        toList =VisaAppointmentSecrets.us_sms_default_list
    for to in toList:
        logger.info("Sending Twilio message:{} to: {}".format(send_message, to))
        message = client.messages \
            .create(
            body=send_message,
            from_=VisaAppointmentSecrets.twilio_number,
            to=to
        )

    logger.info("Message success Id from Twilio: {}".format(message.sid))

