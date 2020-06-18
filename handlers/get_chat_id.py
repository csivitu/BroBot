from misc.text import chat_id_msg
from telegram.ext import CommandHandler


def get_chat_id(update, context):
    update.message.reply_text(f"{chat_id_msg} {update.message.from_user.id}.")


chatid_handler = CommandHandler("getchatid", get_chat_id)
