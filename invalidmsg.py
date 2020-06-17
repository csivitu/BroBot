from text import invalidmessage
from telegram.ext import ConversationHandler


def wrongOption(update, context):
    message = invalidmessage
    update.message.reply_text(message)
    return ConversationHandler.END
