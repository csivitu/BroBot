from misc.text import repo_link
from telegram.ext import CommandHandler


def about_website(update, context):
    update.message.reply_text(repo_link)


about_handler = CommandHandler("about", about_website)
