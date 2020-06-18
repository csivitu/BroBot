from misc.text import start_message
from telegram.ext import CommandHandler


def start(update, context):
    message = start_message
    update.message.reply_text(message)


start_handler = CommandHandler("start", start)
