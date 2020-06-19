from misc.text import (
    ask_no,
    ask_message,
    not_admin,
    repo_path,
    file_name,
    text_api,
    text_key,
    sending_fail,
    err_msg,
    sms_success,
    proxy_api,
)
from telegram import ForceReply
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from github import Github
import threading
import string
import requests
import os
from misc.invalid_msg import wrong_option

sessions = {}


def ask_num(update, context):
    try:
        admin_list = (
            Github(os.getenv("API"))
            .get_repo(repo_path)
            .get_contents(file_name)
            .decoded_content.decode()
            .strip()
            .split("\n")
        )
        if str(update.message.from_user.id) in admin_list or (
            update.message.from_user.username
            and update.message.from_user.username.lower()
            in [i.lower() for i in admin_list]
        ):
            update.message.reply_text(ask_no, reply_markup=ForceReply())
            return 0
        else:
            update.message.reply_text(not_admin)
            return ConversationHandler.END
    except BaseException:
        update.message.reply_text(err_msg)
        return ConversationHandler.END


def sms(update, number):
    key = text_key
    message = update.message.text
    while True:
        i = requests.get(proxy_api).json()[0]
        try:
            resp = requests.post(
                text_api,
                {"phone": number, "message": message, "key": key,},
                proxies={"http": f"http://{i['Ip']}:{i['Port']}"},
                timeout=15,
            ).json()
            break
        except BaseException:
            pass
    if resp["success"]:
        update.message.reply_text(f"{sms_success}{resp['textId']}.")
    else:
        update.message.reply_text(f"{sending_fail} {resp['error']}")


def ask_msg(update, context):
    sessions[update.message.from_user.id] = update.message.text.translate(
        {ord(i): None for i in string.whitespace}
    )
    update.message.reply_text(ask_message, reply_markup=ForceReply())
    return 1


def send_sms(update, context):
    number = sessions[update.message.from_user.id]
    del sessions[update.message.from_user.id]
    threading.Thread(target=sms, args=[update, number]).start()
    return ConversationHandler.END


sms_states = {
    0: [MessageHandler(Filters.text, ask_msg)],
    1: [MessageHandler(Filters.text, send_sms)],
}
sms_handler = ConversationHandler(
    entry_points=[CommandHandler("sendsms", ask_num)],
    states=sms_states,
    fallbacks=[MessageHandler(Filters.all, wrong_option)],
)
