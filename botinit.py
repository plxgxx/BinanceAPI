import os
import telegram.ext
from telegram.ext import Updater

""" inicialise handlers and start the bot """




bot_token = os.getenv("BOT_TOKEN")  # variable, because it is neaded on webhook
updater = Updater(token=bot_token, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher


def start(update, context):
    update.message.reply_text("Hello World!")

def help(update, context):
    update.message.reply_text(
        """
        /start -> Welcome to the channel
        /help -> Get answers on your questions
        /faq -> What this bot can do?
        """
    )
def faq(update, context):
    update.message.reply_text("""This bot is capable of making 
    your P2P transactions filter easier""")


dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
dispatcher.add_handler(telegram.ext.CommandHandler('faq', faq))

updater.start_polling()
updater.idle()
