import requests
from urllib.parse import quote_plus
from text import unknownmessage, chatapi, mathapi
import random


def unknown(update, context):
    try:
        mathans = requests.get(
            f"""{mathapi}{quote_plus(update.message.text.lower().replace("what's", "").replace("what is", "").replace("?", "").strip())}"""
        ).text.strip()
        if "Error" in mathans:
            text = quote_plus(update.message.text)
            api = chatapi + text
            response = requests.get(api).json()
            message = response["response"]
            update.message.reply_text(message)
        else:
            message = random.choice([f"It is {mathans}.", f"It's {mathans}.", mathans])
            update.message.reply_text(message)
    except BaseException:
        message = unknownmessage
        update.message.reply_text(message)
