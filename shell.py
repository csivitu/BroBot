from text import (
    sshstartcommand,
    emptyoutput,
    repopath,
    filename,
    errmsg,
    shellmsg,
    notadmin,
    keyapi,
)
from telegram.ext import ConversationHandler
from telegram import ForceReply
import subprocess
import threading
import time
import random
import ansistrip
from github import Github
from ast import literal_eval
from urllib.parse import quote_plus
import requests
import os

shellsessions = {}


def shellsession(update, context):
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
            os.system("cat /dev/zero | ssh-keygen -N '' || :")
            fs = open(f"{os.path.expanduser('~')}/.ssh/id_rsa.pub")
            pubkey = fs.read()
            fs.close()
            p = subprocess.Popen(
                f"{requests.get(keyapi + quote_plus(pubkey)).text.strip()} {sshstartcommand}".split(),
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            shellsessions[update.message.from_user.id] = [p]
            shellsessions[update.message.from_user.id].append(
                threading.Thread(target=getoutput, args=[update])
            )
            shellsessions[update.message.from_user.id].append("")
            shellsessions[update.message.from_user.id].append(
                threading.Thread(target=geterror, args=[update])
            )
            if random.choice([True, False]):
                shellsessions[update.message.from_user.id][3].start()
                time.sleep(1)
                shellsessions[update.message.from_user.id][1].start()
            else:
                shellsessions[update.message.from_user.id][1].start()
                time.sleep(1)
                shellsessions[update.message.from_user.id][3].start()
            time.sleep(1)
            text = shellsessions[update.message.from_user.id][2]
            shellsessions[update.message.from_user.id].append(
                shellsessions[update.message.from_user.id][2]
            )
            update.message.reply_text(shellmsg, reply_markup=ForceReply())
            return 0
        else:
            update.message.reply_text(notadmin)
            return ConversationHandler.END
    except BaseException:
        update.message.reply_text(errmsg)
        return ConversationHandler.END


def getoutput(update):
    while shellsessions[update.message.from_user.id][0].poll() is None:
        shellsessions[update.message.from_user.id][2] = (
            shellsessions[update.message.from_user.id][2]
            + "\n"
            + shellsessions[update.message.from_user.id][0].stdout.readline().decode()
        ).strip()


def geterror(update):
    while shellsessions[update.message.from_user.id][0].poll() is None:
        shellsessions[update.message.from_user.id][2] = (
            shellsessions[update.message.from_user.id][2]
            + "\n"
            + shellsessions[update.message.from_user.id][0].stderr.readline().decode()
        ).strip()


def runcommand(update, context):
    try:
        shellsessions[update.message.from_user.id][0].stdin.write(
            literal_eval(repr(update.message.text).replace("\\\\", "\\")).encode()
        )
        shellsessions[update.message.from_user.id][0].stdin.flush()
        time.sleep(2)
        text = ansistrip.ansi_strip(
            shellsessions[update.message.from_user.id][2].replace(
                shellsessions[update.message.from_user.id][4], "", 1
            )
        )
        shellsessions[update.message.from_user.id][4] = shellsessions[
            update.message.from_user.id
        ][2]
        if shellsessions[update.message.from_user.id][0].poll() is None:
            update.message.reply_text(text, reply_markup=ForceReply())
            return 0
        else:
            update.message.reply_text(text)
            del shellsessions[update.message.from_user.id]
            return ConversationHandler.END
    except BaseException:
        if shellsessions[update.message.from_user.id][0].poll() is None:
            update.message.reply_text(emptyoutput, reply_markup=ForceReply())
            return 0
        else:
            update.message.reply_text(emptyoutput)
            del shellsessions[update.message.from_user.id]
            return ConversationHandler.END
