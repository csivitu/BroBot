from text import (
    notadmin,
    askid,
    alreadyadmin,
    addsuccess,
    repopath,
    filename,
    alreadyremoved,
    errmsg,
    removesuccess,
)
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, Filters
from telegram import ReplyKeyboardMarkup, ForceReply
from github import Github
from invalidmsg import WrongOption
import os


def AdminPanel(update, contex):
    options = [["List Admins"], ["Add Admin"], ["Remove Admin"]]
    update.message.reply_text(
        "Please select an option:",
        reply_markup=ReplyKeyboardMarkup(
            options, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return 0


def AdminOptions(update, context):
    option = update.message.text
    if option == "List Admins":
        try:
            update.message.reply_text(
                Github(os.getenv("API"))
                .get_repo(repopath)
                .get_contents(filename)
                .decoded_content.decode()
                .strip()
            )
            return ConversationHandler.END
        except BaseException:
            update.message.reply_text(errmsg)
            return ConversationHandler.END

    elif option == "Add Admin":
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
                update.message.reply_text(askid, reply_markup=ForceReply())
                return 1
            else:
                update.message.reply_text(notadmin)
                return ConversationHandler.END
        except BaseException:
            update.message.reply_text(errmsg)
            return ConversationHandler.END

    else:
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
                update.message.reply_text(askid, reply_markup=ForceReply())
                return 2
            else:
                update.message.reply_text(notadmin)
                return ConversationHandler.END
        except BaseException:
            update.message.reply_text(errmsg)
            return ConversationHandler.END


def AddAdmin(update, context):
    try:
        g = Github(os.getenv("API"))
        adminlist = [
            i.lower()
            for i in g.get_repo(repopath)
            .get_contents(filename)
            .decoded_content.decode()
            .strip()
            .split("\n")
        ]
        admin = update.message.text.lower()
        if admin in adminlist:
            update.message.reply_text(admin + " " + alreadyadmin)
        else:
            repo = g.get_repo(repopath)
            contents = repo.get_contents(filename)
            adminlist.append(admin)
            repo.update_file(
                contents.path,
                f"added-{admin}-as-admin",
                "\n".join(adminlist),
                contents.sha,
            )
            update.message.reply_text(admin + " " + addsuccess)
        return ConversationHandler.END
    except BaseException:
        update.message.reply_text(errmsg)
        return ConversationHandler.END


def RemoveAdmin(update, context):
    try:
        g = Github(os.getenv("API"))
        adminlist = [
            i.lower()
            for i in g.get_repo(repopath)
            .get_contents(filename)
            .decoded_content.decode()
            .strip()
            .split("\n")
        ]
        admin = update.message.text.lower()
        if admin not in adminlist:
            update.message.reply_text(admin + " " + alreadyremoved)
        else:
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
    except BaseException:
        update.message.reply_text(errmsg)
        return ConversationHandler.END


admin_states = {
    0: [
        MessageHandler(
            Filters.regex("^(List Admins|Add Admin|Remove Admin)$"), AdminOptions
        )
    ],
    1: [MessageHandler(Filters.text, AddAdmin)],
    2: [MessageHandler(Filters.text, RemoveAdmin)],
}
admin_handler = ConversationHandler(
    entry_points=[CommandHandler("adminpanel", AdminPanel)],
    states=admin_states,
    fallbacks=[MessageHandler(Filters.all, WrongOption)],
)
