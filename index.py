from telegram.ext import Updater
import os
from adminpanel import admin_handler
from dotenv import load_dotenv
from unknown import unknown_handler
from start import start_handler
from meme import meme_handler
from joke import joke_handler
from coronavirus import corona_handler
from addmykey import key_handler
from shell import ssh_handler
from about import about_handler
from getchatid import chatid_handler
from sendsms import sms_handler


config = ".env" if os.path.exists(".env") else "sample.env"
load_dotenv(dotenv_path=config)
token = os.getenv("TOKEN")
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(joke_handler)
dispatcher.add_handler(chatid_handler)
dispatcher.add_handler(corona_handler)
dispatcher.add_handler(meme_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(key_handler)
dispatcher.add_handler(ssh_handler)
dispatcher.add_handler(about_handler)
dispatcher.add_handler(admin_handler)
dispatcher.add_handler(sms_handler)
dispatcher.add_handler(unknown_handler)
updater.start_polling()
updater.idle()
