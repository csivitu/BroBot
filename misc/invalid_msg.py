from misc.text import invalid_message
from telegram.ext import ConversationHandler


def wrong_option(update, context):
    message = invalid_message
    update.message.reply_text(message)
    return ConversationHandler.END
