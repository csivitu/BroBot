from misc.text import key_msg, key_api, repo_path, file_name, not_admin, err_msg
import requests
from urllib.parse import quote_plus
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, Filters
from misc.invalidmsg import wrong_option
from telegram import ForceReply
from github import Github
import os


def ask_key(update, context):
    try:
        adminlist = (
            Github(os.getenv("API"))
            .get_repo(repo_path)
            .get_contents(file_name)
            .decoded_content.decode()
            .strip()
            .split("\n")
        )
        if str(update.message.from_user.id) in adminlist or (
            update.message.from_user.username
            and update.message.from_user.username.lower()
            in [i.lower() for i in adminlist]
        ):
            text = key_msg
            update.message.reply_text(text, reply_markup=ForceReply())
            return 0
        else:
            update.message.reply_text(not_admin)
            return ConversationHandler.END
    except BaseException:
        update.message.reply_text(err_msg)
        return ConversationHandler.END


def add_key(update, context):
    text = requests.get(key_api + quote_plus(update.message.text)).text.strip()
    update.message.reply_text(text)
    return ConversationHandler.END


key_states = {0: [MessageHandler(Filters.text, add_key)]}
key_handler = ConversationHandler(
    entry_points=[CommandHandler("addmykey", ask_key)],
    states=key_states,
    fallbacks=[MessageHandler(Filters.all, wrong_option)],
)
