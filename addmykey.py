from text import keymsg, keyapi
import requests
from urllib.parse import quote_plus
from telegram.ext import ConversationHandler


def askkey(update, context):
    text = keymsg
    update.message.reply_text(text)
    return 0


def addkey(update, context):
    text = requests.get(keyapi + quote_plus(update.message.text)).text.strip()
    update.message.reply_text(text)
    return ConversationHandler.END
