from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    ConversationHandler,
    CommandHandler,
)
import os
from invalidmsg import wrongOption
from adminpanel import adminpanel, adminoptions, addadmin, removeadmin
from dotenv import load_dotenv
from unknownHandler import unknown
from startHandler import start
from memeHandler import meme
from jokeHandler import joke
from coronaHandler import countrySelection, dateSelection, coronaupdates
from addmykey import askkey, addkey
from shell import shellsession, runcommand
from about import about_website
from chatid import getChatID
from smshandler import asknum, askmsg, sendsms


config = ".env" if os.path.exists(".env") else "sample.env"
load_dotenv(dotenv_path=config)
token = os.getenv("TOKEN")
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
joke_handler = CommandHandler("joke", joke)
dispatcher.add_handler(joke_handler)
cID = CommandHandler("getchatid", getChatID)
dispatcher.add_handler(cID)
corona_states = {
    0: [MessageHandler(Filters.text, dateSelection)],
    1: [MessageHandler(Filters.text, coronaupdates)],
}
corona_handler = ConversationHandler(
    entry_points=[CommandHandler("coronavirus", countrySelection)],
    states=corona_states,
    fallbacks=[MessageHandler(Filters.all, wrongOption)],
)
dispatcher.add_handler(corona_handler)
meme_handler = CommandHandler("meme", meme)
dispatcher.add_handler(meme_handler)
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
key_states = {0: [MessageHandler(Filters.text, addkey)]}
key_handler = ConversationHandler(
    entry_points=[CommandHandler("addmykey", askkey)],
    states=key_states,
    fallbacks=[MessageHandler(Filters.all, wrongOption)],
)
dispatcher.add_handler(key_handler)
ssh_states = {0: [MessageHandler(Filters.text, runcommand)]}
ssh_handler = ConversationHandler(
    entry_points=[CommandHandler("shell", shellsession)],
    states=ssh_states,
    fallbacks=[MessageHandler(Filters.all, wrongOption)],
)
dispatcher.add_handler(ssh_handler)
about_handler = CommandHandler("about", about_website)
dispatcher.add_handler(about_handler)
admin_states = {
    0: [
        MessageHandler(
            Filters.regex("^(List Admins|Add Admin|Remove Admin)$"), adminoptions
        )
    ],
    1: [MessageHandler(Filters.text, addadmin)],
    2: [MessageHandler(Filters.text, removeadmin)],
}
admin_handler = ConversationHandler(
    entry_points=[CommandHandler("adminpanel", adminpanel)],
    states=admin_states,
    fallbacks=[MessageHandler(Filters.all, wrongOption)],
)
dispatcher.add_handler(admin_handler)
sms_states = {
    0: [MessageHandler(Filters.text, askmsg)],
    1: [MessageHandler(Filters.text, sendsms)],
}
sms_handler = ConversationHandler(
    entry_points=[CommandHandler("sendsms", asknum)],
    states=sms_states,
    fallbacks=[MessageHandler(Filters.all, wrongOption)],
)
dispatcher.add_handler(sms_handler)
unknown_handler = MessageHandler(Filters.all, unknown)
dispatcher.add_handler(unknown_handler)
updater.start_polling()
updater.idle()
