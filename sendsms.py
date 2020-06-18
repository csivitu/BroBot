from text import (
    askno,
    askm,
    notadmin,
    repopath,
    filename,
    textapi,
    textkey,
    sendingfail,
    errmsg,
    smssuccess,
)
from telegram import ForceReply
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from github import Github
import threading
import string
import requests
import os
import proxyscrape
import random
from invalidmsg import WrongOption

sessions = {}
sockets = proxyscrape.create_collector("default", "http")


def AskNum(update, context):
    try:
        adminlist = (
            Github(os.getenv("API"))
            .get_repo(repopath)
            .get_contents(filename)
            .decoded_content.decode()
            .strip()
            .split("\n")
        )
        if str(update.message.from_user.id) in adminlist or (
            update.message.from_user.username
            and update.message.from_user.username.lower()
            in [i.lower() for i in adminlist]
        ):
            update.message.reply_text(askno, reply_markup=ForceReply())
            return 0
        else:
            update.message.reply_text(notadmin)
            return ConversationHandler.END
    except BaseException:
        update.message.reply_text(errmsg)
        return ConversationHandler.END


def SMS(update, number):
    key = textkey
    message = update.message.text
    collector = sockets.get_proxies()
    random.shuffle(collector)
    gotresp = False
    for i in collector:
        try:
            resp = requests.post(
                textapi,
                {"phone": number, "message": message, "key": key,},
                proxies={"http": f"http://{i.host}:{i.port}"},
                timeout=15,
            )
            gotresp = True
            break
        except BaseException:
            pass
    if gotresp:
        resp = resp.json()
    else:
        resp = requests.post(
            textapi, {"phone": number, "message": message, "key": key,},
        ).json()
    if resp["success"]:
        update.message.reply_text(f"{smssuccess}{resp['textId']}.")
    else:
        update.message.reply_text(f"{sendingfail} {resp['error']}")


def AskMsg(update, context):
    sessions[update.message.from_user.id] = update.message.text.translate(
        {ord(i): None for i in string.whitespace}
    )
    update.message.reply_text(askm, reply_markup=ForceReply())
    return 1


def SendSMS(update, context):
    number = sessions[update.message.from_user.id]
    del sessions[update.message.from_user.id]
    threading.Thread(target=SMS, args=[update, number]).start()
    return ConversationHandler.END


sms_states = {
    0: [MessageHandler(Filters.text, AskMsg)],
    1: [MessageHandler(Filters.text, SendSMS)],
}
sms_handler = ConversationHandler(
    entry_points=[CommandHandler("sendsms", AskNum)],
    states=sms_states,
    fallbacks=[MessageHandler(Filters.all, WrongOption)],
)