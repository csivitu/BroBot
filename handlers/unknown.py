import requests
from urllib.parse import quote_plus
from misc.text import unknown_message, chat_api, math_api
import random
from telegram.ext import MessageHandler, Filters


def unknown(update, context):
    try:
        mathans = requests.get(
            f"""{math_api}{quote_plus(update.message.text.lower().replace("what's", "").replace("what is", "").replace("?", "").strip())}"""
        ).text.strip()
        if "Error" in mathans:
            text = quote_plus(update.message.text)
            api = chat_api + text
            response = requests.get(api).json()
            message = response["response"]
            update.message.reply_text(message)
        else:
            message = random.choice([f"It is {mathans}.", f"It's {mathans}.", mathans])
            update.message.reply_text(message)
    except BaseException:
        message = unknown_message
        update.message.reply_text(message)


unknown_handler = MessageHandler(Filters.all, unknown)
