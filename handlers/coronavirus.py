import requests
from telegram import ReplyKeyboardMarkup
import random
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, Filters
from misc.text import invalid_message, corona_api, ask_date, ask_country
from misc.invalid_msg import wrong_option

sessions = {}


def country_selection(update, context):
    api = corona_api
    response = requests.get(api).json()
    countries = list(response.keys())
    random_country = random.choice(countries)
    response["World"] = []
    for i in range(len(response[random_country])):
        confirmed = 0
        recovered = 0
        deaths = 0
        for j in countries:
            confirmed += response[j][i]["confirmed"]
            deaths += response[j][i]["deaths"]
            recovered += response[j][i]["recovered"]
        response["World"].append(
            {
                "date": response[random_country][i]["date"],
                "confirmed": confirmed,
                "deaths": deaths,
                "recovered": recovered,
            }
        )
    countries = ["World"] + sorted(countries)
    options = []
    for i in range(len(countries)):
        options.append([countries[i]])
    update.message.reply_text(
        ask_country,
        reply_markup=ReplyKeyboardMarkup(
            options, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    sessions[update.message.from_user.id] = [response]
    return 0


def date_selection(update, context):
    country = update.message.text
    sessions[update.message.from_user.id].append(country)
    if country in sessions[update.message.from_user.id][0]:
        options = []
        for i in sessions[update.message.from_user.id][0][country]:
            options.append([i["date"]])
        options = options[::-1]
        update.message.reply_text(
            ask_date,
            reply_markup=ReplyKeyboardMarkup(
                options, one_time_keyboard=True, resize_keyboard=True
            ),
        )
        return 1
    else:
        message = invalid_message
        update.message.reply_text(message)
        return ConversationHandler.END


def corona_updates(update, context):
    date = update.message.text
    data = None
    for i in range(
        len(
            sessions[update.message.from_user.id][0][
                sessions[update.message.from_user.id][1]
            ]
        )
    ):
        if (
            sessions[update.message.from_user.id][0][
                sessions[update.message.from_user.id][1]
            ][i]["date"]
            == date
        ):
            data = sessions[update.message.from_user.id][0][
                sessions[update.message.from_user.id][1]
            ][i]
            break
    if data:
        message = f'Cases: {data["confirmed"]}\n'
        message += f'Deaths: {data["deaths"]}\n'
        message += f'Recovered: {data["recovered"]}\n'
        try:
            message += f'New cases on {date}: {data["confirmed"] - sessions[update.message.from_user.id][0][sessions[update.message.from_user.id][1]][i-1]["confirmed"]}\n'
            message += f'New deaths on {date}: {data["deaths"] - sessions[update.message.from_user.id][0][sessions[update.message.from_user.id][1]][i-1]["deaths"]}\n'
            message += f'New recovered on {date}: {data["recovered"] - sessions[update.message.from_user.id][0][sessions[update.message.from_user.id][1]][i-1]["recovered"]}'
        except BaseException:
            message += f'New cases on {date}: {data["confirmed"]}\n'
            message += f'New deaths on {date}: {data["deaths"]}\n'
            message += f'New recovered on {date}: {data["recovered"]}'
    else:
        message = invalid_message
    update.message.reply_text(message)
    del sessions[update.message.from_user.id]
    return ConversationHandler.END


corona_states = {
    0: [MessageHandler(Filters.text, date_selection)],
    1: [MessageHandler(Filters.text, corona_updates)],
}
corona_handler = ConversationHandler(
    entry_points=[CommandHandler("coronavirus", country_selection)],
    states=corona_states,
    fallbacks=[MessageHandler(Filters.all, wrong_option)],
)
