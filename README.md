# VisaAppointmentNotifier
2021 is a horror story for getting US visa appointments, there are telegram groups where kind folks collabarate and share if slots are available. The application simply polls the group and update personal groups/send messages instead of checking the big group and the sea of messages there. This application is just a helper/aid to reduce the noise in the Telegram Group for appointments

##Why:

It was a pain to check the embassy website everytime, Lucliky there is a wonderful group where everyone shares the status of appointment availability. 
The idea was to ensure one does not miss the Bulk Slot which is window of 2-3 mins

##What:

The application simply polls the DropBox group(H1b/H4 Visa Dropbox Slots) in Telegram and does certain heuristics to classify a potential availability.
The next step is in general for you to act - typically check the real telegram group to ensure its real and then keep the login ready in incognito mode in the browser.
**Tip: Please ensure everything is prefelled in your browser before checking the Telegram Group, this way you just hit the login button incase.


##Prereqs:

1. Python and some libraries : https://github.com/chandanmal00/VisaAppointmentNotifier/blob/main/TelegramReadme
2. If you want text: create a Twilio Account - https://www.twilio.com/try-twilio  - They give you a credit of 15+$ which is good enough for our use case
3. If you want Telegram notification: We need to create a telegram bot from your account:  https://github.com/chandanmal00/VisaAppointmentNotifier/blob/main/TelegramBot.py
4. If your python geek, you can run the file TelegramChanneMessageNotifierMain.py : https://github.com/chandanmal00/VisaAppointmentNotifier/blob/main/TelegramChanneMessageNotifierMain.py
OR alternatively install Pycharm to run the code
5. You need to setup secrets/configurations which are mentioned below in How section

*I will start writing the insturctions on each topic.

##How:

1. TelegramChanneMessageNotifierMain.py is the main starting place - this will run the application polling every 30 secs: https://github.com/chandanmal00/VisaAppointmentNotifier/blob/main/TelegramChanneMessageNotifierMain.py#L257

2. You will need to setup certain properties in VisaAppointmentSecrets.py : https://github.com/chandanmal00/VisaAppointmentNotifier/blob/main/VisaAppointmentSecrets.py
This are essentially your Twilio Credentials, India/US phone numbers, Telegram Ids to send messages, Telegram credentials

##Other Tips

Nothing figured out on my own, all due to great work of everyone in the amazing Telegram Community, but here is what helped
1. *Making sure: you have both mobile and laptop credentials saved like Amazon 1 click style
2. *The checkbox and the captcha are a pain, so it takes time to get used to it, specially the autocomplete in safari has been a big pain for me that screwed me 2 times earlier
3. *Time is your friend and being active during these two slots mentioned below is super important:
4. *Typically Sunday PST, Monday PST, Tuesday PST are the ones where bulk slots are available
5. Key Slots - 18, 48 mins is real and these times have worked best

*1st slot - 6:48 - 7PM  PST
*2nd slot - 8:48 -9:10PM PST


##Example Output Notifications

1. Telegram Notifications:
<img width="611" alt="Screen Shot 2021-12-06 at 5 57 03 AM" src="https://user-images.githubusercontent.com/25375284/144770351-75658867-5ad2-4160-9e75-999b196b178d.png">

>>The first one is the one you need to act ON, the 2nd is just a casual one to make note of

2. Text Message Notification:
This is simlar to first one, but more stricter and much more accurate. The idea was to text only when must and also to save on texting costs.

![WhatsApp Image 2021-12-06 at 5 59 35 AM](https://user-images.githubusercontent.com/25375284/144770470-a0e3b7eb-7624-4333-827e-396852717dfa.jpeg)



**Wish Everyone Best luck, everyone gets the appointment and are able to meet their loved ones, Aameen!











