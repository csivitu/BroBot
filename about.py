from text import aboutwebsite
from telegram.ext import CommandHandler


def AboutWebsite(update, context):
    message = aboutwebsite
    update.message.reply_text(message)


about_handler = CommandHandler("about", AboutWebsite)
