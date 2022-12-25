from telegram import ReplyKeyboardMarkup
from botinit import MAIN_MENU, CURR_GIVING
from telegram.ext import ConversationHandler


def start(update, context):
    text = "Hello World!"
    reply_keyboard = [
        ["Make an offer", "Offer history"],
        ["What this bot can do?", "Help"],
        ["Done"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)
    return MAIN_MENU


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


def offer_curr_choice(update, context):
    text = "Choose the currency of your offer"
    reply_keyboard = [
        ["CHF", "SEK", "PLN"],
        ["CZK", "USD", "EUR"],
        ["UAH", "CAD", "GBP"],
        ["Done"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)
    return CURR_GIVING


def offer_crypt_choice(update, context):
    update.message.reply_text("See your offers histroy")
    return MAIN_MENU


def done():
    return ConversationHandler.END


def faq(update, context):
    text = """This bot is capable of making 
    your P2P transactions filter easier"""
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=text
    )
    return MAIN_MENU


