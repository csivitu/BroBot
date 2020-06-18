from misc.text import invalid_message
from telegram.ext import ConversationHandler


def wrong_option(update, context):
    message = invalidmessage
    update.message.reply_text(message)
    return ConversationHandler.END
