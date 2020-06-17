from text import aboutwebsite


def about_website(update, context):
    message = aboutwebsite
    update.message.reply_text(message)
