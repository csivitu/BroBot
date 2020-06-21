import requests
import random
from misc.text import joke_apis
from telegram.ext import CommandHandler


def joke(update, context):
    api = random.choice(joke_apis)
    response = requests.get(api).json()
    try:
        if response["type"] == "success" or response["type"] == "single":
            try:
                message = response["joke"]
            except BaseException:
                message = response["value"]["joke"]
        else:
            try:
                message = response["setup"] + "\n\n" + response["delivery"]
            except BaseException:
                message = response["setup"] + "\n\n" + response["punchline"]
    except BaseException:
        message = response["value"]
    update.message.reply_text(message)


joke_handler = CommandHandler("joke", joke)
