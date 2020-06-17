import requests
import random
from text import jokeapis


def joke(update, context):
    api = random.choice(jokeapis)
    response = requests.get(api).json()
    try:
        if response["type"] == "success" or response["type"] == "single":
            try:
                message = response["joke"]
            except BaseException:
                message = response["value"]["joke"]
                message = message.replace("\\'", "'")
                message = message.replace('\\"', '"')
        else:
            try:
                message = response["setup"] + "\n\n" + response["delivery"]
            except BaseException:
                message = response["setup"] + "\n\n" + response["punchline"]
    except BaseException:
        message = response["value"]
    update.message.reply_text(message)
