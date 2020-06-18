from text import invalidmessage
from telegram.ext import ConversationHandler


def WrongOption(update, context):
    message = invalidmessage
    update.message.reply_text(message)
    return ConversationHandler.END
