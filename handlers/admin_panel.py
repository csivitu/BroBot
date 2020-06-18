from misc.text import (
    not_admin,
    ask_id,
    already_admin,
    add_success,
    repo_path,
    file_name,
    already_removed,
    err_msg,
    remove_success,
)
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, Filters
from telegram import ReplyKeyboardMarkup, ForceReply
from github import Github
from misc.invalid_msg import wrong_option
import os


def admin_panel(update, contex):
    options = [["List Admins"], ["Add Admin"], ["Remove Admin"]]
    update.message.reply_text(
        "Please select an option:",
        reply_markup=ReplyKeyboardMarkup(
            options, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return 0


def admin_options(update, context):
    option = update.message.text
    if option == "List Admins":
        try:
            update.message.reply_text(
                Github(os.getenv("API"))
                .get_repo(repo_path)
                .get_contents(file_name)
                .decoded_content.decode()
                .strip()
            )
            return ConversationHandler.END
        except BaseException:
            update.message.reply_text(err_msg)
            return ConversationHandler.END

    elif option == "Add Admin":
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
                update.message.reply_text(ask_id, reply_markup=ForceReply())
                return 1
            else:
                update.message.reply_text(not_admin)
                return ConversationHandler.END
        except BaseException:
            update.message.reply_text(err_msg)
            return ConversationHandler.END

    else:
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
                update.message.reply_text(ask_id, reply_markup=ForceReply())
                return 2
            else:
                update.message.reply_text(not_admin)
                return ConversationHandler.END
        except BaseException:
            update.message.reply_text(err_msg)
            return ConversationHandler.END


def add_admin(update, context):
    try:
        g = Github(os.getenv("API"))
        adminlist = [
            i.lower()
            for i in g.get_repo(repo_path)
            .get_contents(file_name)
            .decoded_content.decode()
            .strip()
            .split("\n")
        ]
        admin = update.message.text.lower()
        if admin in adminlist:
            update.message.reply_text(admin + " " + already_admin)
        else:
            repo = g.get_repo(repo_path)
            contents = repo.get_contents(file_name)
            adminlist.append(admin)
            repo.update_file(
                contents.path,
                f"added-{admin}-as-admin",
                "\n".join(adminlist),
                contents.sha,
            )
            update.message.reply_text(admin + " " + add_success)
        return ConversationHandler.END
    except BaseException:
        update.message.reply_text(err_msg)
        return ConversationHandler.END


def remove_admin(update, context):
    try:
        g = Github(os.getenv("API"))
        adminlist = [
            i.lower()
            for i in g.get_repo(repo_path)
            .get_contents(file_name)
            .decoded_content.decode()
            .strip()
            .split("\n")
        ]
        admin = update.message.text.lower()
        if admin not in adminlist:
            update.message.reply_text(admin + " " + already_removed)
        else:
            repo = g.get_repo(repo_path)
            contents = repo.get_contents(file_name)
            adminlist.remove(admin)
            repo.update_file(
                contents.path,
                f"removed-{admin}-as-admin",
                "\n".join(adminlist),
                contents.sha,
            )
            update.message.reply_text(admin + " " + remove_success)
        return ConversationHandler.END
    except BaseException:
        update.message.reply_text(err_msg)
        return ConversationHandler.END


admin_states = {
    0: [
        MessageHandler(
            Filters.regex("^(List Admins|Add Admin|Remove Admin)$"), admin_options
        )
    ],
    1: [MessageHandler(Filters.text, add_admin)],
    2: [MessageHandler(Filters.text, remove_admin)],
}
admin_handler = ConversationHandler(
    entry_points=[CommandHandler("adminpanel", admin_panel)],
    states=admin_states,
    fallbacks=[MessageHandler(Filters.all, wrong_option)],
)
