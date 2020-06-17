from text import (
    notadmin,
    askid,
    alreadyadmin,
    addsuccess,
    repopath,
    filename,
    alreadyremoved,
    removesuccess,
)
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, ForceReply
from github import Github
import os


def adminpanel(update, contex):
    adminlist = (
        Github()
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
        options = [["List Admins"], ["Add Admin"], ["Remove Admin"]]
        update.message.reply_text(
            "Please select an option:",
            reply_markup=ReplyKeyboardMarkup(
                options, one_time_keyboard=True, resize_keyboard=True
            ),
        )
        return 0
    else:
        update.message.reply_text(notadmin)
        return ConversationHandler.END


def adminoptions(update, context):
    option = update.message.text
    if option == "List Admins":
        update.message.reply_text(
            Github()
            .get_repo(repopath)
            .get_contents(filename)
            .decoded_content.decode()
            .strip()
        )
        return ConversationHandler.END
    elif option == "Add Admin":
        update.message.reply_text(askid, reply_markup=ForceReply())
        return 1
    else:
        update.message.reply_text(askid, reply_markup=ForceReply())
        return 2


def addadmin(update, context):
    adminlist = [
        i.lower()
        for i in Github()
        .get_repo(repopath)
        .get_contents(filename)
        .decoded_content.decode()
        .strip()
        .split("\n")
    ]
    admin = update.message.text.lower()
    if admin in adminlist:
        update.message.reply_text(admin + " " + alreadyadmin)
    else:
        g = Github(os.getenv("API"))
        repo = g.get_repo(repopath)
        contents = repo.get_contents(filename)
        adminlist.append(admin)
        repo.update_file(
            contents.path, f"added-{admin}-as-admin", "\n".join(adminlist), contents.sha
        )
        update.message.reply_text(admin + " " + addsuccess)
    return ConversationHandler.END


def removeadmin(update, context):
    adminlist = [
        i.lower()
        for i in Github()
        .get_repo(repopath)
        .get_contents(filename)
        .decoded_content.decode()
        .strip()
        .split("\n")
    ]
    admin = update.message.text.lower()
    if admin not in adminlist:
        update.message.reply_text(admin + " " + alreadyremoved)
    else:
        g = Github(os.getenv("API"))
        repo = g.get_repo(repopath)
        contents = repo.get_contents(filename)
        adminlist.remove(admin)
        repo.update_file(
            contents.path,
            f"removed-{admin}-as-admin",
            "\n".join(adminlist),
            contents.sha,
        )
        update.message.reply_text(admin + " " + removesuccess)
    return ConversationHandler.END
