from telegram.ext import Updater
import os
from dotenv import load_dotenv
from handlers.adminpanel import admin_handler
from handlers.unknown import unknown_handler
from handlers.start import start_handler
from handlers.meme import meme_handler
from handlers.joke import joke_handler
from handlers.coronavirus import corona_handler
from handlers.addmykey import key_handler
from handlers.shell import ssh_handler
from handlers.about import about_handler
from handlers.getchatid import chatid_handler
from handlers.sendsms import sms_handler


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
