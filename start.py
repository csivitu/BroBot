from text import startmessage
from telegram.ext import CommandHandler


def Start(update, context):
    message = startmessage
    update.message.reply_text(message)


start_handler = CommandHandler("start", Start)
