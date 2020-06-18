import requests
import random
from text import subreddits, memeapi
from telegram.ext import CommandHandler


def Meme(update, context):
    options = subreddits
    choice = random.choice((options + ["all"]))
    api = memeapi + choice
    if choice != "all":
        response = requests.get(api).json()
    else:
        response = requests.get(api).json()
        while response["subreddit"] in options:
            response = requests.get(api).json()
    update.message.reply_photo(response["url"], caption=response["title"])


meme_handler = CommandHandler("meme", Meme)
