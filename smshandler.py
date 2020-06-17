from text import (
    askno,
    askm,
    notadmin,
    repopath,
    filename,
    textapi,
    proxyapi,
    textkey,
    proxyregex,
    sendingfail,
    errmsg,
    smssuccess,
)
import requests
from re import findall
from telegram import ForceReply
from telegram.ext import ConversationHandler
from github import Github
import threading
import random
import string
import os

sessions = {}


def asknum(update, context):
    try:
        adminlist = (
            Github(os.getenv("API"))
            .get_repo(repopath)
            .get_contents(filename)
            .decoded_content.decode()
            .strip()
            .split("\n")
        )
        if str(
            update.message.from_user.id
        ) in adminlist or update.message.from_user.username.lower() in [
            i.lower() for i in adminlist
        ]:
            update.message.reply_text(askno, reply_markup=ForceReply())
            return 0
        else:
            update.message.reply_text(notadmin)
            return ConversationHandler.END
    except BaseException:
        update.message.reply_text(errmsg)
        return ConversationHandler.END


def sms(update, number):
    key = textkey
    message = update.message.text
    r = requests.get(proxyapi)
    matches = findall(proxyregex, r.text)
    revised = [m.replace("<td>", "") for m in matches]
    sockets = [f"{s.split('</td>')[0]}:{s.split('</td>')[1]}" for s in revised]
    random.shuffle(sockets)
    gotresp = False
    for i in sockets:
        try:
            resp = requests.post(
                textapi,
                {"phone": number, "message": message, "key": key,},
                proxies={"http": f"http://{i}"},
                timeout=60,
            ).json()
            gotresp = True
            break
        except BaseException:
            pass
    if not gotresp:
        resp = requests.post(
            textapi, {"phone": number, "message": message, "key": key,},
        ).json()
    if resp["success"]:
        update.message.reply_text(smssuccess)
    else:
        update.message.reply_text(sendingfail)


def askmsg(update, context):
    sessions[update.message.from_user.id] = update.message.text.translate(
        {ord(i): None for i in string.whitespace}
    )
    update.message.reply_text(askm, reply_markup=ForceReply())
    return 1


def sendsms(update, context):
    number = sessions[update.message.from_user.id]
    del sessions[update.message.from_user.id]
    threading.Thread(target=sms, args=[update, number]).start()
    return ConversationHandler.END
