import os
import telegram.ext
from telegram.ext import Updater
from telegram.ext import CallbackContext

""" inicialise handlers and start the bot """

bot_token = os.getenv("BOT_TOKEN")  # variable, because it is neaded on webhook
updater = Updater(token=bot_token, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher


def start(update, context):
    text = "Hello World!"
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=text
    )


def help(update, context):
    text = """
        /start -> Welcome to the channel
        /help -> Get answers on your questions
        /faq -> What this bot can do?
        """
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=text
    )




def faq(update, context):
    text = """This bot is capable of making 
    your P2P transactions filter easier"""
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=text
    )


dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
dispatcher.add_handler(telegram.ext.CommandHandler('faq', faq))

updater.start_polling()
updater.idle()
