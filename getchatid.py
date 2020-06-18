from text import chatidmsg
from telegram.ext import CommandHandler


def GetChatID(update, context):
    update.message.reply_text(f"{chatidmsg} {update.message.from_user.id}.")


chatid_handler = CommandHandler("getchatid", GetChatID)
