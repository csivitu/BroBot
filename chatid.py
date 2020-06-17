from text import chatidmsg


def getChatID(update, context):
    update.message.reply_text(f"{chatidmsg} {update.message.from_user.id}.")
