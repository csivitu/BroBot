from text import startmessage


def start(update, context):
    message = startmessage
    update.message.reply_text(message)
